"""Plumbing test for namma.sweep without a GPU: a stand-in for `python -m namma run`, a local folder for Drive.

    python tests/test_sweep.py
"""
import json
import os
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from namma import sweep  # noqa: E402
from namma.config import Config  # noqa: E402
from namma.workspace import Workspace, read_json, write_json  # noqa: E402

STUB = """#!/usr/bin/env bash
# stands in for: <venv python> -m namma run --job DIR   (args: -m namma run --job DIR)
job="$5"
python3 - "$job" <<'PY'
import json, sys, time, pathlib
job = pathlib.Path(sys.argv[1])
def status(**k):
    p = job / "status.json"; cur = json.loads(p.read_text()) if p.exists() else {}
    cur.update(k, updated=time.time()); p.write_text(json.dumps(cur))
status(state="running", stage="train", message="step 100")
time.sleep(float(__import__("os").environ.get("STUB_SECONDS", "3")))
job_json = json.loads((job / "job.json").read_text())
cfg = job_json["config"]
# like the real pipeline: a variant forked after train has a valid train receipt, so training is skipped
if job_json.get("fork_after") != "train":
    (job / "train" / "eval.json").write_text(json.dumps({"psnr": 20.0 + cfg["train"]["cap_max"] / 1e7, "ssim": 0.9, "gaussians": cfg["train"]["cap_max"]}))
status(state="finished", stage=None, progress=1.0, message="done")
PY
"""


def make_canonical(root):
    """A finished-up-to-train main job with real receipts and outputs."""
    ws = Workspace(root / "main-abc")
    write_json(ws.root / "job.json", {"job_id": "main-abc", "video_name": "v.mp4", "video_path": "/x/v.mp4", "video_sha256": "0" * 64,
                                      "smoke": False, "created": 1, "config": Config().to_dict()})
    files = {"frames": ["frames/images/a.jpg", "frames/frame_metrics.csv"], "sfm": ["sfm/sparse/images.bin", "sfm/undistorted/sparse/x.bin", "sfm/undistorted/images/a.jpg"],
             "priors": ["dataset/sparse/points3D.bin", "dataset/images/a.jpg", "priors/a.jpg.npz"],
             "train": ["train/final.pt", "train/eval.json", "train/metrics.jsonl"]}
    for stage, rels in files.items():
        for rel in rels:
            (ws.root / rel).parent.mkdir(parents=True, exist_ok=True)
            (ws.root / rel).write_text(f"{stage}:{rel}")
        write_json(ws.stages / f"{stage}.json", {"stage": stage, "settings": "h", "outputs": rels, "metrics": {}})
    return ws


def check(condition, message):
    print(("ok   " if condition else "FAIL ") + message, flush=True)
    if not condition:
        raise SystemExit(1)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        canon = make_canonical(tmp)
        base = Config().to_dict()

        # ---- validation -------------------------------------------------------------------
        grid = [{"name": "cap-1.5M", "settings": {"train": {"cap_max": 1500000}}},
                {"name": "mesh fine", "settings": {"mesh": {"voxel": 0.015}}, "fork_after": "train"},
                {"name": "noop", "settings": {}},
                {"name": "typo", "settings": {"train": {"cap_maxx": 1}}},
                {"name": "badtype", "settings": {"train": {"steps": "many"}}},
                {"name": "wrongfork", "settings": {"priors": {"resolution_level": 5}}, "fork_after": "priors"},
                {"name": "wrongfork2", "settings": {"train": {"steps": 1000}}, "fork_after": "train"},
                {"name": "cap-1.5M", "settings": {"train": {"cap_max": 2000000}}},
                {"name": "ok sfm", "settings": {"priors": {"resolution_level": 5}}, "fork_after": "sfm"}]
        variants, problems = sweep.validate(canon.root, grid)
        check([v["name"] for v in variants] == ["cap-1.5M", "mesh fine", "ok sfm"], f"valid variants: {[v['name'] for v in variants]}")
        joined = "\n".join(problems)
        for needle in ("noop: changes nothing", "unknown setting train.cap_maxx", "train.steps should be int", "wrongfork2: changes settings",
                       "share the folder", "wrongfork: changes settings"):
            check(needle in joined, f"problem reported: {needle}")
        check('Set "fork_after" to "sfm"' in joined, "suggests the earlier fork stage")
        check(variants[0]["changes"] == {"train.cap_max": [1000000, 1500000]}, f"changes: {variants[0]['changes']}")
        check(sweep.validate(canon.root, [{"name": "n", "settings": {"train": {"cap_max": 1500000.0}}}])[0][0]["config"]["train"]["cap_max"] == 1500000,
              "whole floats become ints")

        # ---- prepare: links, receipts, no damage to the main job ---------------------------
        v = variants[0]
        ws = sweep.prepare(canon.root, v)
        for rel in ("frames/images/a.jpg", "dataset/sparse/points3D.bin", "priors/a.jpg.npz", "sfm/sparse/images.bin"):
            check(os.stat(canon.root / rel).st_ino == os.stat(ws.root / rel).st_ino, f"hard-linked: {rel}")
        check(not (ws.root / "train" / "final.pt").exists(), "train not shared for a priors fork")
        check(sorted(p.stem for p in ws.stages.glob("*.json")) == ["frames", "priors", "sfm"], "receipts copied: frames, sfm, priors")
        job = read_json(ws.root / "job.json")
        check(job["config"]["train"]["cap_max"] == 1500000 and job["job_id"] == ws.root.name and job["sweep_of"] == "main-abc", "variant job.json")
        check(read_json(canon.root / "job.json")["config"] == base, "main job.json untouched")
        check((ws.logs).is_dir(), "variant has a logs folder (the old launcher crashed without it)")
        # a train fork shares train, a later re-fork to priors must drop the linked train results
        mesh_variant = variants[1]
        mws = sweep.prepare(canon.root, mesh_variant)
        check(os.stat(canon.root / "train/final.pt").st_ino == os.stat(mws.root / "train/final.pt").st_ino, "train fork links final.pt")
        check(sorted(p.stem for p in mws.stages.glob("*.json")) == ["frames", "priors", "sfm", "train"], "train fork copies the train receipt")
        mesh_variant2 = {**mesh_variant, "fork_after": "priors"}
        sweep.prepare(canon.root, mesh_variant2)
        check(not (mws.root / "train" / "final.pt").exists() and not (mws.stages / "train.json").exists(), "re-forking earlier removes linked train results")

        # ---- the manager ---------------------------------------------------------------------
        stub = tmp / "stub-python"
        stub.write_text(STUB)
        stub.chmod(stub.stat().st_mode | stat.S_IEXEC)
        drive = tmp / "drive"
        drive.mkdir()
        grid_file = tmp / "grid.json"
        grid_file.write_text(json.dumps([
            {"name": "a", "settings": {"train": {"cap_max": 1500000}}},
            {"name": "b", "settings": {"train": {"cap_max": 2000000}}},
            {"name": "c", "settings": {"train": {"cap_max": 2500000}}},
            {"name": "m", "settings": {"mesh": {"voxel": 0.015}}, "fork_after": "train"}]))
        env = {**os.environ, "PYTHONPATH": str(REPO), "STUB_SECONDS": "3"}
        cmd = [sys.executable, "-m", "namma.sweep", "start", "--canonical", str(canon.root), "--grid", str(grid_file),
               "--venv-python", str(stub), "--remote-root", "Backups", "--max-parallel", "2", "--launch-gap", "0.5",
               "--poll", "0.5", "--fs", f"local:{drive}"]
        checked = json.loads(subprocess.run(cmd[:3] + ["--canonical", str(canon.root), "--grid", str(grid_file)] if False else
                                            [sys.executable, "-m", "namma.sweep", "check", "--canonical", str(canon.root), "--grid", str(grid_file)],
                                            env=env, cwd=REPO, capture_output=True, text=True).stdout)
        check(not checked["problems"] and len(checked["variants"]) == 4, "check command accepts the grid")
        started = time.time()
        done = subprocess.run(cmd, env=env, cwd=REPO, capture_output=True, text=True, timeout=180)
        print(done.stdout[-1500:], done.stderr[-1500:])
        check(done.returncode == 0, "manager exited 0")
        state = read_json(tmp / "sweep_status.json")
        check(state["state"] == "finished", f"sweep state: {state['state']} ({state.get('message')})")
        check(all(r["state"] == "finished" for r in state["variants"].values()), "every variant finished")
        for name in "abcm":
            d = tmp / f"main-abc__{name}"
            check(read_json(d / "status.json")["state"] == "finished", f"variant {name} ran")
        check(read_json(tmp / "main-abc__c" / "train" / "eval.json")["gaussians"] == 2500000, "variant c used its own settings")
        check((canon.root / "train" / "eval.json").read_text() == "train:train/eval.json", "main eval.json untouched (variants write their own)")
        check((canon.root / "train" / "final.pt").read_text() == "train:train/final.pt", "main final.pt untouched")
        check(started and (drive / "Backups").is_dir(), "Drive folder created once")
        folders = sorted(p.name for p in (drive / "Backups").iterdir())
        check(folders == [f"main-abc__{n}" for n in "abcm"], f"one Drive folder per variant: {folders}")

        # a second click finds everything finished and starts nothing
        again = subprocess.run(cmd, env=env, cwd=REPO, capture_output=True, text=True, timeout=60)
        check(again.returncode == 0 and "started" not in again.stdout, "re-running starts nothing new")

        # a stopped session: status says running but no process -> relaunched, not stuck
        write_json(tmp / "main-abc__a" / "status.json", {"state": "running", "stage": "train"})
        (tmp / "main-abc__a" / "train" / "eval.json").unlink()
        write_json(tmp / "main-abc__b" / "status.json", {"state": "failed", "error": "boom"})
        again = subprocess.run(cmd, env=env, cwd=REPO, capture_output=True, text=True, timeout=120)
        check(again.stdout.count("started main-abc__") == 2, f"stopped and failed variants are resumed: {again.stdout.count('started main-abc__')}")

        # blocked when the main run has not finished the shared stage and is not running
        (canon.stages / "priors.json").unlink()
        (tmp / "main-abc__a" / "status.json").unlink()
        write_json(tmp / "sweep_status.json", {})
        blocked = subprocess.run(cmd, env=env, cwd=REPO, capture_output=True, text=True, timeout=60)
        row = read_json(tmp / "sweep_status.json")["variants"]["a"]
        check(row["state"] == "blocked" and "not running" in row["note"], f"blocked variant explains itself: {row['note']}")
    print("\nALL SWEEP CHECKS PASSED")


if __name__ == "__main__":
    main()