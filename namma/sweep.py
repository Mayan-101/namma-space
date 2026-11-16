"""Hyperparameter sweep: retrain a room under several settings on one shared camera solve.

Every variant is an ordinary pipeline job. It shares the main job's finished upstream stages (hard links, so
no extra disk) and re-runs everything after them with its own settings, so the only difference between the
results is the setting under test. Each variant gets its own Drive uploader and is restored from Drive when a
new molab session starts, so a shutdown costs at most the steps since its last checkpoint.

Runs with the notebook's Python (it holds the Google Drive login); the GPU work runs in the venv, as in driver.py.

    python -m namma.sweep check --canonical JOB --grid grid.json
    python -m namma.sweep start --canonical JOB --grid grid.json --venv-python PY [--remote-root NammaSpaceBackups]
                                [--max-parallel 3] [--min-vram-mib 12000] [--fs drive]

grid.json is a list of {"name": ..., "settings": {"train": {"cap_max": 1500000}}, "fork_after": "priors"}.
`fork_after` is the last stage shared with the main job: frames, sfm, priors (default) or train (settings that
only change the mesh). A variant may only change settings of stages *after* its fork stage.

Folders: <jobs-root>/<main job>__<name>/ (one job each), <jobs-root>/sweep_status.json, sweep.log.
On Drive: <remote-root>/<main job>__<name>/ (checkpoints and results).
"""
import argparse
import fcntl
import json
import os
import shutil
import subprocess
import sys
import time
import traceback
from pathlib import Path

from namma.config import Config
from namma.driver import notebook_env, venv_env
from namma.pipeline import SECTIONS
from namma.workspace import STAGES, Workspace, read_json, write_json

REPO = Path(__file__).resolve().parents[1]
UPLOAD_WAIT = 3 * 3600
# fork_after -> (folders hard-linked from the main job, stages whose receipts are copied)
FORKS = {
    "frames": (["frames"], ["frames"]),
    "sfm": (["frames", "sfm"], ["frames", "sfm"]),
    "priors": (["frames", "sfm", "dataset", "priors"], ["frames", "sfm", "priors"]),
    "train": (["frames", "sfm", "dataset", "priors", "train"], ["frames", "sfm", "priors", "train"]),
}
OWN_FOLDERS = ("train", "mesh", "export")  # always the variant's own unless the fork shares them


# ---- planning ---------------------------------------------------------------------------------
def variant_dir(canonical, name):
    canon = Path(canonical)
    safe = "".join(c if c.isalnum() or c in "-_" else "-" for c in name)
    return canon.parent / f"{canon.name}__{safe}"


def variant_config(base_config, overrides):
    """The main job's saved settings plus the variant's changes (KeyError for a setting that does not exist)."""
    settings = json.loads(json.dumps(base_config))
    for section, values in (overrides or {}).items():
        if section not in settings:
            raise KeyError(f"unknown settings section '{section}' (choose from {', '.join(settings)})")
        if not isinstance(values, dict):
            raise ValueError(f"'{section}' must be an object of settings")
        for key, new in values.items():
            if key not in settings[section]:
                raise KeyError(f"unknown setting {section}.{key}")
            old = settings[section][key]
            numeric = isinstance(old, (int, float)) and not isinstance(old, bool) and isinstance(new, (int, float)) and not isinstance(new, bool)
            if old is not None and not numeric and type(new) is not type(old):
                raise ValueError(f"{section}.{key} should be {type(old).__name__}, not {type(new).__name__}")
            if isinstance(old, int) and not isinstance(old, bool) and isinstance(new, float) and new != int(new):
                raise ValueError(f"{section}.{key} must be a whole number")
            settings[section][key] = int(new) if isinstance(old, int) and not isinstance(old, bool) and numeric else new
    return Config.from_dict(settings)


def changes_between(a, b):
    return {f"{s}.{k}": [a[s][k], b[s][k]] for s in a for k in a[s] if a[s][k] != b[s].get(k)}


def validate(canonical, grid):
    """(variants, problems). Nothing is created or changed."""
    canon = Path(canonical).resolve()
    job = read_json(canon / "job.json", {})
    if not job:
        return [], [f"{canon} has no job.json: start the main reconstruction first."]
    if not isinstance(grid, list) or not grid:
        return [], ["The sweep grid must be a non-empty JSON list."]
    base = Config.from_dict(job["config"])
    variants, problems, seen = [], [], {}
    for index, entry in enumerate(grid, 1):
        name = entry.get("name") if isinstance(entry, dict) else None
        if not isinstance(name, str) or not name.strip():
            problems.append(f"Entry {index} needs a text \"name\".")
            continue
        directory = variant_dir(canon, name)
        if directory.name in seen:
            problems.append(f"'{name}' and '{seen[directory.name]}' would share the folder {directory.name}; rename one.")
            continue
        seen[directory.name] = name
        fork = entry.get("fork_after", "priors")
        if fork not in FORKS:
            problems.append(f"{name}: fork_after must be one of {', '.join(FORKS)}.")
            continue
        try:
            cfg = variant_config(job["config"], entry.get("settings"))
        except (KeyError, ValueError, TypeError, AttributeError) as error:
            problems.append(f"{name}: {error.args[0] if error.args else error}")
            continue
        changes = changes_between(base.to_dict(), cfg.to_dict())
        if not changes:
            problems.append(f"{name}: changes nothing compared with the main run, so it would repeat the same result. "
                            "Remove it or change a setting.")
            continue
        if cfg.stage_hash(*SECTIONS[fork]) != base.stage_hash(*SECTIONS[fork]):
            usable = [f for f in FORKS if cfg.stage_hash(*SECTIONS[f]) == base.stage_hash(*SECTIONS[f])]
            problems.append(f"{name}: changes settings that the '{fork}' stage depends on, so it cannot share that stage. "
                            + (f"Set \"fork_after\" to \"{usable[-1]}\"." if usable else "Nothing can be shared: run it as its own video job."))
            continue
        variants.append({"name": name, "dir": directory, "overrides": entry.get("settings") or {}, "fork_after": fork,
                         "changes": changes, "config": cfg.to_dict()})
    return variants, problems


# ---- one variant's folder ---------------------------------------------------------------------
def _link_tree(src, dst):
    """Hard-link every file of src into dst (copy when a link is impossible)."""
    shutil.rmtree(dst, ignore_errors=True)
    dst.mkdir(parents=True)
    for path in sorted(Path(src).rglob("*")):
        target = dst / path.relative_to(src)
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.link(path, target)
        except OSError:
            shutil.copy2(path, target)


def stage_complete(job_dir, stage):
    """A stage whose receipt exists and whose outputs are all on disk (after a Drive restore, MoGe maps may not be)."""
    job_dir = Path(job_dir)
    receipt = read_json(job_dir / "stages" / f"{stage}.json")
    return bool(receipt) and all((job_dir / rel).exists() for rel in receipt.get("outputs", []))


def prepare(canonical, variant):
    """Create or update the variant's job folder. Shared stages are linked once per fork; settings are rewritten every time."""
    canon, dst = Path(canonical).resolve(), Path(variant["dir"])
    canon_job = read_json(canon / "job.json")
    ws = Workspace(dst)
    folders, receipts = FORKS[variant["fork_after"]]
    marker = ws.root / "sweep_fork.json"
    mark = {"fork_after": variant["fork_after"], "canonical": str(canon)}
    if read_json(marker, {}) != mark:
        for sub in folders:
            _link_tree(canon / sub, ws.root / sub)
        for stage in STAGES:
            (ws.stages / f"{stage}.json").unlink(missing_ok=True)
        for stage in receipts:
            shutil.copy2(canon / "stages" / f"{stage}.json", ws.stages / f"{stage}.json")
        for sub in OWN_FOLDERS:  # never keep linked or older results of a stage this variant re-runs
            if sub not in folders:
                shutil.rmtree(ws.root / sub, ignore_errors=True)
                (ws.root / sub).mkdir()
        write_json(marker, mark)
    previous = read_json(ws.root / "job.json", {})
    write_json(ws.root / "job.json", {**canon_job, "job_id": dst.name, "smoke": False, "config": variant["config"],
                                      "created": previous.get("created", time.time()), "sweep_of": canon.name,
                                      "variant": variant["name"], "fork_after": variant["fork_after"]})
    return ws


# ---- processes --------------------------------------------------------------------------------
def process_running(job_dir, *words):
    """True while a process has every word and the job folder among its arguments (zombies have none)."""
    job = str(Path(job_dir).resolve())
    for cmdline in Path("/proc").glob("[0-9]*/cmdline"):
        try:
            args = cmdline.read_bytes().decode(errors="replace").split("\0")
        except OSError:
            continue
        if job in args and all(word in args for word in words):
            return True
    return False


def free_vram_mib():
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=10)
        return int(out.stdout.strip().splitlines()[0])
    except Exception:
        return None


class Sweep:
    def __init__(self, args):
        self.args = args
        self.canon = Path(args.canonical).resolve()
        self.root = self.canon.parent
        self.status_path = self.root / "sweep_status.json"
        self.uploader_started = {}

    def status(self, **fields):
        write_json(self.status_path, {**read_json(self.status_path, {}), **fields, "updated": time.time()})

    @staticmethod
    def log(message):
        print(f"{time.strftime('%H:%M:%S')} {message}", flush=True)

    def remote(self, variant):
        return f"{self.args.remote_root}/{Path(variant['dir']).name}"

    def keep_uploader(self, variant, force=False):
        """One Drive uploader per variant (it takes a lock, so a second one would only exit). Not restarted more than every 5 min."""
        directory = Path(variant["dir"])
        if process_running(directory, "namma.backup", "upload"):
            return
        if not force and time.time() - self.uploader_started.get(variant["name"], 0) < 300:
            return
        self.uploader_started[variant["name"]] = time.time()
        with open(directory / "logs" / "uploader.log", "ab") as log:
            subprocess.Popen([sys.executable, "-m", "namma.backup", "upload", "--job", str(directory), "--remote",
                              self.remote(variant), "--fs", self.args.fs], cwd=REPO, env=notebook_env(str(REPO)),
                             stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)

    def launch(self, variant):
        from namma import backup
        ws = prepare(self.canon, variant)
        self.status_row(variant, state="starting", note="restoring from Drive")
        try:
            self.log(f"{variant['name']}: restored {backup.restore(ws.root, self.remote(variant), self.args.fs)}")
        except Exception as error:  # a failed restore only means more recomputation
            self.log(f"{variant['name']}: restore failed ({type(error).__name__}: {error}); starting from the shared stages")
        self.keep_uploader(variant, force=True)  # before the pipeline, so it sees this run's end
        with open(ws.logs / "sweep-run.log", "ab") as log:
            proc = subprocess.Popen([self.args.venv_python, "-m", "namma", "run", "--job", str(ws.root)], cwd=REPO,
                                    env=venv_env(), stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                                    start_new_session=True)
        self.log(f"{variant['name']}: started {ws.root.name} (pid {proc.pid})")
        return proc

    def status_row(self, variant, **row):
        rows = read_json(self.status_path, {}).get("variants", {})
        rows[variant["name"]] = {**rows.get(variant["name"], {}), **row}
        self.status(variants=rows)

    # ---- the loop --------------------------------------------------------------------------
    def run(self):
        a = self.args
        try:
            grid = json.loads(Path(a.grid).read_text())
        except (OSError, ValueError) as error:
            self.status(state="failed", error=f"Cannot read the sweep grid: {error}")
            return 1
        variants, problems = validate(self.canon, grid)
        if problems:
            self.status(state="failed", error="; ".join(problems))
            self.log("Not started: " + "; ".join(problems))
            return 1
        lock = open(self.root / "sweep.lock", "a")
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self.log("A sweep is already running for this folder")
            return 0
        self.status(state="running", error=None, traceback=None, message="starting", started=time.time(), grid=str(a.grid),
                    variants={v["name"]: {"state": "queued", "dir": str(v["dir"]), "changes": v["changes"],
                                          "fork_after": v["fork_after"]} for v in variants})
        try:
            return self.loop(variants)
        except BaseException as error:
            self.status(state="failed", error=f"{type(error).__name__}: {error}"[-2000:], traceback=traceback.format_exc()[-4000:])
            self.log("FAILED: " + traceback.format_exc()[-4000:])
            return 1

    def loop(self, variants):
        from namma import backup
        a = self.args
        backup.ensure_folders([a.remote_root] + [self.remote(v) for v in variants], a.fs)  # one process: concurrent creation duplicates folders
        procs, attempted, last_launch = {}, set(), 0.0
        while True:
            canon_alive = process_running(self.canon, "namma", "run")
            running = {v["name"] for v in variants if process_running(v["dir"], "namma", "run")}
            for name in [n for n, p in procs.items() if p.poll() is not None]:
                del procs[name]  # reap, so finished children do not stay as zombies
            active = len(running) + int(canon_alive)
            rows, queue = {}, []
            for v in variants:
                st = read_json(Path(v["dir"]) / "status.json", {})
                if v["name"] in running:
                    rows[v["name"]] = {"state": "running", "note": st.get("message", "")}
                    self.keep_uploader(v)
                elif st.get("state") == "finished" and read_json(Path(v["dir"]) / "job.json", {}).get("config") == v["config"]:
                    rows[v["name"]] = {"state": "finished", "note": ""}
                elif v["name"] in attempted:
                    rows[v["name"]] = {"state": "failed", "note": st.get("error") or "the run stopped before finishing (see its logs/sweep-run.log)"}
                else:
                    rows[v["name"]] = {"state": "queued", "note": "retrying after an earlier failure" if st.get("state") == "failed" else ""}
                    queue.append(v)
            launched, blocked = None, 0
            for v in queue:
                name = v["name"]
                missing = [s for s in FORKS[v["fork_after"]][1] if not stage_complete(self.canon, s)]
                if missing:
                    if canon_alive:
                        rows[name]["note"] = f"waiting for the main run to finish its {missing[0]} stage"
                    else:
                        rows[name] = {"state": "blocked", "note": f"the main run is not running and has not finished {missing[0]}: click 3. Start / resume"}
                        blocked += 1
                    continue
                free = free_vram_mib()
                if launched or active >= a.max_parallel:
                    rows[name]["note"] = "waiting for a free slot"
                elif time.time() - last_launch < a.launch_gap:
                    rows[name]["note"] = "starting soon"
                elif free is not None and free < a.min_vram_mib:
                    rows[name]["note"] = f"waiting for GPU memory ({free:,} MiB free)"
                else:
                    self.status(message=f"starting {name}")
                    try:
                        procs[name] = self.launch(v)
                    except Exception as error:
                        attempted.add(name)
                        rows[name] = {"state": "failed", "note": f"could not start: {type(error).__name__}: {error}"}
                        self.log(f"{name}: could not start: {traceback.format_exc()[-1500:]}")
                        continue
                    attempted.add(name)
                    last_launch, launched = time.time(), name
                    active += 1
                    rows[name] = {"state": "running", "note": "starting"}
            counts = {s: sum(1 for r in rows.values() if r["state"] == s) for s in ("finished", "running", "queued", "blocked", "failed")}
            self.status(variants={n: {**read_json(self.status_path, {}).get("variants", {}).get(n, {}), **r} for n, r in rows.items()},
                        message=", ".join(f"{c} {s}" for s, c in counts.items() if c))
            if not running and launched is None and counts["queued"] == 0:
                break
            time.sleep(a.poll)
        waited, limit = 0.0, UPLOAD_WAIT if not counts["failed"] else 900
        while any(process_running(v["dir"], "namma.backup", "upload") for v in variants) and waited < limit:
            self.status(message="Waiting for the last Drive uploads")
            time.sleep(a.poll)
            waited += a.poll
        done = counts["finished"] == len(variants)
        self.status(state="finished" if done else "partial", message=", ".join(f"{c} {s}" for s, c in counts.items() if c))
        return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m namma.sweep")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("check", "start"):
        sub = commands.add_parser(name)
        sub.add_argument("--canonical", required=True, help="the main job folder")
        sub.add_argument("--grid", required=True, help="JSON file with the variants")
    start = commands.choices["start"]
    start.add_argument("--venv-python", required=True)
    start.add_argument("--remote-root", default="NammaSpaceBackups")
    start.add_argument("--max-parallel", type=int, default=3, help="jobs on the GPU at once, the main run included")
    start.add_argument("--min-vram-mib", type=int, default=12000)
    start.add_argument("--launch-gap", type=float, default=30.0, help="seconds between launches")
    start.add_argument("--poll", type=float, default=10.0)
    start.add_argument("--fs", default="drive", help="'drive' or local:/folder for tests")
    args = parser.parse_args(argv)
    if args.command == "start":
        return Sweep(args).run()
    try:
        grid = json.loads(Path(args.grid).read_text())
    except (OSError, ValueError) as error:
        print(json.dumps({"variants": [], "problems": [f"Cannot read the sweep grid: {error}"]}))
        return 1
    variants, problems = validate(args.canonical, grid)
    print(json.dumps({"variants": [{"name": v["name"], "fork_after": v["fork_after"], "changes": v["changes"]} for v in variants],
                      "problems": problems}))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())