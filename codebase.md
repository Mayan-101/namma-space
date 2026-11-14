<codebase>
<project_structure>
.
├── .gitattributes
├── .gitignore
├── LICENSE
├── README.md
├── THIRD_PARTY_NOTICES.md
├── docs
│   ├── CAPTURE_SOP.md
│   └── MOLAB_SETUP.md
├── env
│   ├── patches
│   │   └── gsplat-relocation-sign.patch
│   └── requirements.lock.txt
├── molab_setup.sh
├── namma
│   ├── __init__.py
│   ├── __main__.py
│   ├── backup.py
│   ├── config.py
│   ├── driver.py
│   ├── export.py
│   ├── frames.py
│   ├── gpu_check.py
│   ├── mesh.py
│   ├── pipeline.py
│   ├── priors.py
│   ├── sfm.py
│   ├── trainer.py
│   └── workspace.py
├── notebooks
│   └── namma_space.py
├── tests
│   ├── fake_gsplat.py
│   ├── run_local_pipeline.py
│   └── sample
│       └── README.md
└── viewer
    ├── README.md
    ├── THIRD_PARTY_NOTICES.md
    ├── aholo
    │   ├── AHOLO-LICENSE.txt
    │   ├── camera-control.ts
    │   ├── index.html
    │   ├── index.ts
    │   ├── performance.js
    │   ├── saved-walk.js
    │   ├── style.css
    │   └── walking-tools.js
    ├── package-lock.json
    ├── package.json
    ├── scripts
    │   ├── colmap-views.mjs
    │   ├── namma-pipeline.py
    │   ├── package-aholo-scene.mjs
    │   ├── package-scene.mjs
    │   ├── scene-assets.mjs
    │   └── scene-pipeline.py
    ├── server
    │   └── scene-library.mjs
    ├── src
    │   ├── demo.js
    │   ├── navigation.js
    │   ├── scene-alignment.js
    │   └── scene-package.js
    ├── test
    │   ├── navigation.test.js
    │   ├── package-aholo.test.js
    │   ├── performance-budget.test.js
    │   ├── saved-walk.test.js
    │   ├── scene-alignment.test.js
    │   ├── scene-package.test.js
    │   └── scene-pipeline.test.py
    ├── vendor
    │   └── manycore-aholo-viewer-1.10.0.tgz
    └── vite.config.js

14 directories, 60 files
</project_structure>

<file src=".gitattributes">
* text=auto eol=lf
*.cmd text eol=crlf
*.tgz binary
*.mp4 binary
*.glb binary
*.spz binary

</file>

<file src=".gitignore">
__pycache__/
*.pyc
.venv/
setup-logs/
node_modules/
viewer/dist/
viewer/data/
viewer/output/
test-results/
output/
data/
.wrangler/
*.mp4

</file>

<file src="LICENSE">
MIT License

Copyright (c) 2026 Akarsh Shrivastav and Mayan S Hiremath (team ruakpeedkahem (rpk))

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Third-party components keep their own licences; see THIRD_PARTY_NOTICES.md.

</file>

<file src="README.md">
# Namma Space

**One ordinary video of an indoor space becomes a photorealistic 3D room you can walk through in a web browser.**
Team ruakpeedkahem (rpk): Akarsh Shrivastav, Mayan S Hiremath, NIT Goa · Techfest 2026-27, IIT Bombay.

- **Live walkthrough:** https://namma-space-7ny.pages.dev/ (open **Walking setup > Enter saved walking setup**,
  then WASD to move and drag to look; best on a desktop browser using its dedicated GPU). Mirror:
  https://thecodenottakent-t.github.io/namma-space/ (slower to load from India)
- **Capture SOP:** [docs/CAPTURE_SOP.md](docs/CAPTURE_SOP.md)
- **Sample data:** [tests/sample/](tests/sample/) (30 s of our classroom capture)

```
video ──> keyframes ──> camera poses ──> depth/normal priors ──> Gaussian splat ──> collision mesh ──> package
          (PyAV,         (COLMAP via       (MoGe-2, aligned to     (gsplat, MCMC,     (TSDF of rendered     (splat PLY + GLB
           sharpness +    pycolmap, CPU)    SfM, metric scale)      30,000 steps)      depth, Open3D)        + hashes)
           optical flow)
                                     all on a free Molab GPU, every stage backed up to Google Drive
                                                              │
                                                              v
                       viewer/: import ──> browser viewer (Aholo) with first-person walking ──> static website
```

## Repository layout

| Path | What it is |
| --- | --- |
| `notebooks/namma_space.py` | The marimo notebook you open on Molab: Get code, Run setup, Start |
| `molab_setup.sh` | Pinned GPU environment: Python 3.12, PyTorch 2.11 + CUDA 13.0, gsplat, MoGe-2, self-checks |
| `namma/` | The pipeline: `frames`, `sfm`, `priors`, `trainer`, `mesh`, `export`, plus `backup` (Drive), `driver`, `pipeline`, `gpu_check` |
| `env/` | Locked Python requirements and the one gsplat patch |
| `viewer/` | Browser viewer, importer and static-demo packager ([viewer/README.md](viewer/README.md)) |
| `tests/` | Local end-to-end pipeline test (stand-in renderer) and the sample clip |
| `docs/` | Molab details ([MOLAB_SETUP.md](docs/MOLAB_SETUP.md)) and the capture SOP |

## Reproduce the room

You need a Google account with Drive and a free [Molab](https://molab.marimo.io) account (NVIDIA GPU runtime).

1. **Capture** a room following [docs/CAPTURE_SOP.md](docs/CAPTURE_SOP.md), or use
   [`tests/sample/classroom_30s.mp4`](tests/sample/). Upload the video to Google Drive.
2. **Open the notebook:** create a Molab notebook from `notebooks/namma_space.py` and select a GPU.
3. **1. Get code** clones this repository into `/marimo/namma-space`.
4. **2. Run setup** installs the pinned environment and runs real GPU checks; wait for **overall PASS**. The first
   setup compiles gsplat's CUDA kernels (about an hour on Molab's RTX PRO 6000) and saves the build to your
   Drive, so later sessions restore it in seconds. Logs: `setup-logs/<time>/`.
5. **Connect Google Drive:** Files panel > *Remote storage* > *Google Drive*, then run the cell it inserts.
6. **Reconstruct:** enter the video path inside My Drive (e.g. `NammaSpace/classroom_30s.mp4`) and click
   **3. Start**. A 20-second smoke test runs first, then the full job. Progress, a photo | render | depth preview
   and the log appear in the notebook. Everything finished is copied to `NammaSpaceBackups/` on Drive and
   verified; if Molab stops, run steps 3–6 again and the job resumes from Drive.
7. **Download** `NammaSpaceBackups/<job>/<n>-download-<id>/` from Drive and open it in the viewer
   ([viewer/README.md](viewer/README.md)): import, look around, set the floor and scale, walk, and package a website.

Measured on Molab for our 4 min 47 s classroom video (613 keyframes): frame selection 12 min, camera poses
32 min, depth priors 3.5 min, training 14 min, mesh and export 1 min. Result: all 613 frames posed at 1.0 px
mean reprojection error; 20.7 dB PSNR and 0.888 SSIM on 26 held-out frames; 1,000,000 Gaussians; 199,999-triangle
collision mesh; 24 MB web model.

## Check the code without a GPU

```bash
python -m venv .venv && .venv/bin/pip install -r env/requirements.lock.txt   # Linux, Python 3.12
python tests/run_local_pipeline.py tests/sample/classroom_30s.mp4 /tmp/namma-test
cd viewer && npm ci && npm test && python3 test/scene-pipeline.test.py
```

The pipeline test runs every stage on the clip with a small stand-in renderer instead of gsplat, kills training
after its first checkpoint, resumes it, checks the export format, backs up to a local folder standing in for
Drive, restores into a fresh job and checks that finished stages are not repeated. It tests the plumbing, not
image quality.

## Settings that matter

Defaults (`namma/config.py`) are the ones that produced the Round 1 room. Two more are implemented but have not
run on a GPU yet: `train.strategy = "default"` (original 3DGS densification, grows past 1M Gaussians) and
`priors.image_long_side = 3840` (4K training images from 4K video).

## Licences

Our code: MIT ([LICENSE](LICENSE)). Every pipeline and viewer component allows commercial use; see
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

</file>

<file src="THIRD_PARTY_NOTICES.md">
# Third-party components

Namma Space is our own orchestration, capture SOP, quality checks, backup/resume and viewer integration
around the open-source components below. We do not claim their algorithms. Every component used by the
pipeline allows commercial use.

## Reconstruction pipeline (`namma/`, run on Molab)

| Component | Role | Licence |
| --- | --- | --- |
| [gsplat](https://github.com/nerfstudio-project/gsplat) (commit `512d366`, patched in `env/patches/`) | Differentiable Gaussian splat rendering, MCMC training | Apache-2.0 |
| [COLMAP / pycolmap](https://github.com/colmap/colmap) 4.2.1, CPU build | SIFT features, matching, camera poses, undistortion | BSD-3-Clause (GPU SiftGPU is never used) |
| [MoGe-2](https://github.com/microsoft/MoGe) code and [moge-2-vitl-normal](https://huggingface.co/Ruicheng/moge-2-vitl-normal) weights | Monocular depth and normal priors | MIT |
| [utils3d](https://github.com/EasternJournalist/utils3d) (MoGe dependency) | Geometry utilities | MIT |
| [Open3D](https://github.com/isl-org/Open3D) 0.19 | TSDF fusion of rendered depth into the collision mesh | MIT |
| [PyTorch](https://github.com/pytorch/pytorch) 2.11 | Training runtime | BSD-3-Clause |
| [OpenCV](https://github.com/opencv/opencv), [PyAV](https://github.com/PyAV-Org/PyAV), [trimesh](https://github.com/mikedh/trimesh), NumPy, SciPy | Images, video decoding, GLB export, maths | Apache-2.0 / BSD-3-Clause / MIT / BSD-3-Clause / BSD-3-Clause |
| [marimo](https://github.com/marimo-team/marimo), [gdrive-fsspec](https://github.com/marimo-team/gdrive-fsspec) | Cloud notebook, Google Drive backup | Apache-2.0 / BSD-3-Clause |

The COLMAP vocabulary tree used for loop detection is downloaded from COLMAP's release page; its licence is
not stated (set `sfm.loop_detection` to false to avoid it). MoGe's MIT weights were trained partly on
research datasets; that is a general uncertainty, not a stated restriction.

## Viewer (`viewer/`)

See [`viewer/THIRD_PARTY_NOTICES.md`](viewer/THIRD_PARTY_NOTICES.md): Aholo Viewer, Three.js, recast-navigation,
PlayCanvas splat-transform and Vite, all MIT.

## Methods

3D Gaussian Splatting (Kerbl et al., SIGGRAPH 2023); 3D Gaussian Splatting as MCMC (Kheradmand et al.,
NeurIPS 2024); MoGe-2 (Wang et al., 2025); Structure-from-Motion Revisited (Schönberger and Frahm, CVPR 2016);
KinectFusion-style TSDF fusion (Newcombe et al., 2011).



</file>

<file src="docs/CAPTURE_SOP.md">
# Capture SOP

One continuous video per connected space, recorded at walking pace. No extra hardware is required; a
phone works, and a camera on a gimbal works better. Our Round 1 classroom was filmed on a DSLR on a gimbal
at 1/500 s, f/8, 1080p 50 fps, in 4 min 47 s.

## Camera settings

- Main 1x lens, landscape, standard video. Prefer **4K** (sharper training images); 1080p works.
- Fast shutter (1/250 s or faster) so frames are not motion-blurred; enough aperture depth (f/5.6–f/8) to keep
  near furniture and far walls in focus.
- Lock focus and, if possible, exposure and white balance. No zoom or lens switching while recording;
  portrait or cinematic effects off.
- Bright, steady light. Avoid shooting into backlit windows; keep doors, curtains and people still.

## Route

1. Start where a doorway, furniture and some floor are visible together.
2. Walk a slow loop around the room, aiming diagonally across it rather than straight at a nearby blank wall.
   Move your body; do not only rotate in place.
3. Keep part of the previous view in frame at all times. At corners take a small step and turn a little,
   several times, instead of one fast 90° pan.
4. Return to the start (this closes the loop), then cross through the walkable middle and show furniture from
   several sides.
5. Do one lower pass looking slightly down at the floor, furniture legs and door thresholds: the collision
   mesh for walking is built from these surfaces.
6. Tilt up gradually for upper walls and ceiling, then return to a familiar view.

## Before leaving

- Pause the video at a few corners: edges must not be smeared or doubled.
- Measure one clearly visible distance (a door height, a bench length) for the viewer's scale step.
- Copy the original file straight to Google Drive; messaging apps recompress video.

## What the pipeline checks

Frame selection keeps only sharp frames (relative to the surrounding second) and adds a frame whenever the
image has moved about 7% of its width. Camera posing stops with a report if fewer than 50% of frames can be
placed and warns below 90%; cameras placed far outside the room are detected and the slower, more accurate
mapper is used instead. Training reports held-out image quality and stops below 16 dB PSNR.

</file>

<file src="docs/MOLAB_SETUP.md">
# Namma Space on molab: video to walkable 3D room

One notebook (`notebooks/namma_space.py`) does everything. Part A prepares the GPU environment
(every molab session starts empty); Part B reconstructs a room from a video on Google Drive.

## Part A: environment

1. Upload `notebooks/namma_space.py` to molab and open it on a GPU.
2. **1. Get code** – clones (or fast-forwards) `main` from https://github.com/TheCodeNotTakenT-T/namma-space into `/marimo/namma-space`. Edited files are never overwritten.
3. **2. Run setup + GPU checks** – wait for *finished* and overall PASS. Send back the offered archive if it fails.

What setup does (`bash molab_setup.sh`, logs in `setup-logs/<time>/`):

| Stage | Detail |
|---|---|
| preflight | Linux, `nvidia-smi`, driver CUDA ≥ 13.0, git/gcc/curl/flock, uv; CPU/RAM/disk |
| python | `uv venv --python 3.12` at `.venv`; exact `env/requirements.lock.txt` (Torch 2.11.0+cu130, NumPy 1.26.4, Open3D 0.19.0, pycolmap 4.2.1, PyAV, cuda-toolkit 13.0.2 with nvcc 13.0.88, …) |
| cuda-environment | `CUDA_HOME` = the venv's `nvidia/cu13`; nvcc must equal Torch's CUDA; arch from this GPU; `MAX_JOBS` from CPUs/RAM |
| gsplat-source | gsplat at a pinned commit in `/opt/namma-src/gsplat` + `env/patches/gsplat-relocation-sign.patch` (sm_120 fix, upstream PR #1060) |
| extensions | builds gsplat (reused when toolchain and sources match) |
| moge | MoGe-2 + utils3d at pinned commits, `--no-deps` (keeps NumPy 1.26.4) |
| gpu-checks | `python -m namma check`: environment, torch_cuda, gsplat (render + backward, relocation kernel, depth→normal), pipeline_imports (incl. pycolmap without CUDA), open3d_tsdf |

## Part B: reconstruction

1. Connect Google Drive: Files panel > *Remote storage* > *Google Drive*, run the cell it inserts.
2. Enter the video path inside *My Drive* (e.g. `NammaSpace/classroom.mp4`), click **3. Start / resume**.
3. The detached driver (`python -m namma.driver`, notebook Python) copies the video, creates the job
   (`/opt/namma-jobs/<name>-<hash>`), restores anything already verified on Drive, starts the uploaders,
   runs the smoke test (first 20 s, tiny settings) and then the full job (`python -m namma run`, GPU venv).
4. Watch the status panel (stage, progress, Drive backup, latest photo | render | depth preview, log).
5. **Show download buttons** offers the `DOWNLOAD_THIS` files. They are also on Drive under
   `NammaSpaceBackups/<job>/<seq>-download-<id>/`. Open it in the browser viewer as described in
   [`viewer/README.md`](../viewer/README.md).

Stages and what survives a molab stop (everything is uploaded with a checksum check and VERIFIED.json):

| Stage | Work | Backed up |
|---|---|---|
| frames | sharp, overlapping keyframes (PyAV + OpenCV) | frames + metrics |
| sfm | pycolmap CPU SIFT, sequential + long-range matching, global then incremental mapper, gravity levelling, undistortion | sparse models, undistorted images, database |
| priors | undistorts the original frames at `priors.image_long_side` (1920 px); MoGe-2 metric depth + normals aligned to the SfM points; scene scaled to metres (estimated) | metric model + per-frame scales (maps are recomputed) |
| train | gsplat MCMC (1M Gaussians, 30,000 steps), L1+SSIM, depth/normal priors, per-frame colour correction, checkpoints every 2,500 steps | every checkpoint, final model |
| mesh | TSDF fusion of rendered depth (Open3D 0.19), cleanup, ≤200k triangles, GLB | room.glb |
| export | `DOWNLOAD_THIS/result-<id>/` zip (parts ≤ 90 MiB) in the importer's format | the files themselves |

If molab stops: open the notebook again, redo Part A, reconnect Drive and click Start with the same video.
Finished stages and the newest checkpoint are restored; training continues from that checkpoint.

## Licences (commercial use)

gsplat (Apache-2.0), pycolmap/COLMAP CPU path (BSD-3; GPU SIFT is never used), MoGe-2 code and weights (MIT),
PyAV (BSD-3), OpenCV (Apache-2.0), Open3D (MIT), trimesh (MIT), PyTorch (BSD). The vocabulary tree used for loop
detection is downloaded from COLMAP's release page; its licence is unstated (set `sfm.loop_detection` false to avoid it).
MoGe's weights are MIT-licensed, but they were trained partly on research-only datasets; that is a general legal
uncertainty, not a stated restriction.

## Publishing the compiled gsplat (so nobody has to compile it)

Compiling gsplat for the RTX PRO 6000 takes over an hour. After one setup has compiled it, every later setup
can download it instead, if it is published as a GitHub release asset:

1. After a setup that PASSED (and ran once more, so the archive exists), the files
   `/opt/namma-cache/gsplat-<signature>.tar` and `gsplat-<signature>.tar.sha256` exist on molab. They are also
   on Google Drive in `NammaSpaceBackups/_build-cache/` after you click Start. Download both.
2. On GitHub, in `TheCodeNotTakenT-T/namma-space`, create a release with the tag `gsplat-prebuilt`
   and attach both files unchanged (needs write access to the repository).
3. Every later setup looks for `https://github.com/TheCodeNotTakenT-T/namma-space/releases/download/gsplat-prebuilt/gsplat-<signature>.tar`,
   checks its SHA-256 and installs it in seconds. To use another repository, set `NAMMA_PREBUILT_BASE`.

The signature covers Python, PyTorch, CUDA compiler, gcc, GPU architecture, build flags and the gsplat
source, so a published build is only used where it is exactly valid; anything else compiles from the
pinned source. gsplat is Apache-2.0, so redistributing the build is allowed (its licence file is inside).

</file>

<file src="env/patches/gsplat-relocation-sign.patch">
diff --git a/gsplat/cuda/csrc/RelocationCUDA.cu b/gsplat/cuda/csrc/RelocationCUDA.cu
index ae56aff65..4ac2a6f4b 100644
--- a/gsplat/cuda/csrc/RelocationCUDA.cu
+++ b/gsplat/cuda/csrc/RelocationCUDA.cu
@@ -66,9 +66,13 @@ __global__ void relocation_kernel(
     {
         for(int k = 0; k <= (i - 1); ++k)
         {
-            float bin_coeff  = binoms[(i - 1) * n_max + k];
-            float term       = (pow(-1.0f, k) / sqrt(static_cast<float>(k + 1))) * pow(new_opacity, k + 1);
-            denom_sum       += (bin_coeff * term);
+            float bin_coeff = binoms[(i - 1) * n_max + k];
+            // k is an integer, so compute the alternating sign exactly. Under
+            // -use_fast_math, pow(-1.0f, k) can be lowered to an approximation
+            // that returns NaN for negative bases on some GPU architectures.
+            float sign      = (k & 1) ? -1.0f : 1.0f;
+            float term      = (sign / sqrt(static_cast<float>(k + 1))) * pow(new_opacity, k + 1);
+            denom_sum      += (bin_coeff * term);
         }
     }
     float coeff = (opacities[idx] / denom_sum);

</file>

<file src="env/requirements.lock.txt">
--index-url https://pypi.org/simple
--extra-index-url https://download.pytorch.org/whl/cu130

absl-py==2.5.1            # via tensorboard
addict==2.4.0             # via open3d, -r requirements.txt
annotated-types==0.8.0    # via pydantic
asttokens==3.0.2          # via stack-data
attrs==26.1.0             # via jsonschema, referencing
av==19.0.2                # via -r requirements.txt
beautifulsoup4==4.15.0    # via gdown
blinker==1.9.0            # via flask
certifi==2026.10.23       # via requests
charset-normalizer==3.5.2  # via requests
click==8.5.0              # via flask
cloudpickle==3.1.2        # via joblib
cmake==4.4.4              # via -r requirements.txt
comm==0.2.3               # via dash, ipywidgets
configargparse==1.9.0     # via open3d
contourpy==1.3.3          # via matplotlib
cuda-bindings==13.4.4     # via torch
cuda-pathfinder==1.8.4    # via cuda-bindings
cuda-toolkit==13.0.2      # via torch, -r requirements.txt
cycler==0.12.1            # via matplotlib
dash==4.4.1               # via open3d
einops==0.8.2             # via -r requirements.txt
executing==2.3.0          # via stack-data
fastjsonschema==2.22.2    # via nbformat
ffmpeg-python==0.2.0      # via -r requirements.txt
filelock==4.2.4           # via gdown, huggingface-hub, torch, transformers
flask==3.1.3              # via dash, open3d
fonttools==4.68.0         # via matplotlib
fsspec==2026.9.0          # via huggingface-hub, torch
future==1.0.0             # via ffmpeg-python
gdown==6.4.2              # via -r requirements.txt
grpcio==1.85.0            # via tensorboard
hf-xet==1.7.1             # via huggingface-hub
huggingface-hub==0.36.2   # via timm, tokenizers, transformers, -r requirements.txt
idna==3.20                # via requests
importlib-metadata==10.1.0  # via dash
ipython==9.17.1           # via ipywidgets
ipython-pygments-lexers==1.1.1  # via ipython
ipywidgets==8.1.9         # via open3d
itsdangerous==2.2.0       # via flask
janus==2.0.0              # via dash
jaxtyping==0.3.11         # via -r requirements.txt
jedi==0.20.1              # via ipython
jinja2==3.1.6             # via flask, torch
joblib==1.6.0             # via scikit-learn
jsonschema==4.26.0        # via nbformat
jsonschema-specifications==2025.9.1  # via jsonschema
jupyter-core==5.9.1       # via nbformat
jupyterlab-widgets==3.0.17  # via ipywidgets
kiwisolver==1.5.1         # via matplotlib
lpips==0.1.4              # via -r requirements.txt
markdown==3.11.2          # via tensorboard
markdown-it-py==4.2.0     # via rich
markupsafe==3.0.4         # via flask, jinja2, werkzeug
matplotlib==3.11.2        # via open3d, -r requirements.txt
matplotlib-inline==0.2.2  # via ipython
mdurl==0.1.2              # via markdown-it-py
mpmath==1.3.0             # via sympy
narwhals==2.28.0          # via plotly, scikit-learn
nbformat==5.11.1          # via open3d
nest-asyncio==1.6.0       # via dash
networkx==3.7             # via torch
ninja==1.13.2             # via -r requirements.txt
numpy==1.26.4             # via contourpy, lpips, matplotlib, open3d, opencv-python, pandas, plyfile, pycocotools, pycolmap, pyquaternion, roma, scikit-learn, scipy, tensorboard, torchvision, transformers, trimesh, -r requirements.txt
nvidia-cublas==13.1.0.3   # via cuda-toolkit, nvidia-cudnn-cu13, nvidia-cusolver
nvidia-cuda-cccl==13.0.85  # via cuda-toolkit
nvidia-cuda-crt==13.0.88  # via cuda-toolkit, nvidia-cuda-nvcc
nvidia-cuda-cupti==13.0.85  # via cuda-toolkit
nvidia-cuda-nvcc==13.0.88  # via cuda-toolkit
nvidia-cuda-nvrtc==13.0.88  # via cuda-toolkit
nvidia-cuda-runtime==13.0.96  # via cuda-toolkit, nvidia-cuda-nvcc
nvidia-cudnn-cu13==9.19.0.56  # via torch
nvidia-cufft==12.0.0.61   # via cuda-toolkit
nvidia-cufile==1.15.1.6   # via cuda-toolkit
nvidia-curand==10.4.0.35  # via cuda-toolkit
nvidia-cusolver==12.0.4.66  # via cuda-toolkit
nvidia-cusparse==12.6.3.3  # via cuda-toolkit, nvidia-cusolver
nvidia-cusparselt-cu13==0.8.0  # via torch
nvidia-nccl-cu13==2.28.9  # via torch
nvidia-nvjitlink==13.0.88  # via cuda-toolkit, nvidia-cufft, nvidia-cusolver, nvidia-cusparse
nvidia-nvshmem-cu13==3.4.5  # via torch
nvidia-nvtx==13.0.85      # via cuda-toolkit
nvidia-nvvm==13.0.88      # via cuda-toolkit, nvidia-cuda-nvcc
open3d==0.19.0            # via -r requirements.txt
opencv-python==4.11.0.86  # via -r requirements.txt
packaging==26.3           # via huggingface-hub, matplotlib, plotly, tensorboard, transformers, wheel, -r requirements.txt
pandas==3.0.6             # via open3d
parso==0.8.7              # via jedi
pexpect==4.9.0            # via ipython
pillow==13.0.0            # via matplotlib, open3d, tensorboard, torchvision
platformdirs==4.14.0      # via jupyter-core, yapf
plotly==7.1.0             # via dash
plyfile==1.1.3            # via -r requirements.txt
prompt-toolkit==3.0.53    # via ipython
protobuf==7.36.2          # via tensorboard
psutil==7.2.2             # via ipython
ptyprocess==0.7.0         # via pexpect
pure-eval==0.2.4          # via stack-data
pycocotools==2.0.11       # via -r requirements.txt
pycolmap==4.2.1           # via -r requirements.txt
pydantic==2.14.1          # via dash
pydantic-core==2.50.1     # via pydantic
pygments==2.21.0          # via ipython, ipython-pygments-lexers
pyparsing==3.3.3          # via matplotlib
pyquaternion==0.9.9       # via open3d
pysocks==1.7.1            # via requests
python-dateutil==3.0.0    # via matplotlib, pandas
pyyaml==6.0.3             # via huggingface-hub, open3d, timm, transformers
referencing==0.37.0       # via jsonschema, jsonschema-specifications
regex==2026.9.29          # via transformers
requests==2.34.2          # via dash, gdown, huggingface-hub, transformers
retrying==1.4.2           # via dash
rich==15.0.0              # via -r requirements.txt
roma==1.8.0               # via -r requirements.txt
rpds-py==2026.9.1         # via jsonschema, referencing
safetensors==0.8.0        # via timm, transformers
scikit-learn==1.9.1       # via open3d
scipy==1.17.1             # via lpips, scikit-learn, -r requirements.txt
setuptools==80.10.2       # via dash, tensorboard, torch, -r requirements.txt
six==1.17.0               # via python-dateutil
soupsieve==3.0.4          # via beautifulsoup4
stack-data==0.6.3         # via ipython
sympy==1.14.0             # via torch
tensorboard==2.21.0       # via -r requirements.txt
tensorboard-data-server==0.7.2  # via tensorboard
threadpoolctl==3.7.0      # via scikit-learn
timm==1.0.30              # via -r requirements.txt
tokenizers==0.19.1        # via transformers
torch==2.11.0+cu130       # via lpips, roma, timm, torchvision, -r requirements.txt
torchvision==0.26.0+cu130  # via lpips, timm, -r requirements.txt
tqdm==4.70.1              # via gdown, huggingface-hub, lpips, open3d, transformers
traitlets==5.16.1         # via ipython, ipywidgets, jupyter-core, matplotlib-inline, nbformat
transformers==4.44.2      # via -r requirements.txt
trimesh==5.2.0            # via -r requirements.txt
triton==3.6.0             # via torch
typing-extensions==4.16.0  # via beautifulsoup4, dash, grpcio, huggingface-hub, pydantic, pydantic-core, referencing, torch, typing-inspection
typing-inspection==0.4.4  # via pydantic
tzdata==2026.6            # via python-dateutil
urllib3==2.8.0            # via gdown, requests
wadler-lindig==0.1.8      # via jaxtyping
wcwidth==0.9.4            # via prompt-toolkit
werkzeug==3.1.9           # via dash, flask, open3d, tensorboard
wheel==0.48.0             # via -r requirements.txt
widgetsnbextension==4.0.16  # via ipywidgets
yapf==0.43.0              # via -r requirements.txt
zipp==4.1.2               # via importlib-metadata

</file>

<file src="molab_setup.sh">
#!/usr/bin/env bash
# Reproducible Linux/NVIDIA (Molab) setup for Namma Space. Safe to rerun.
#
#   bash molab_setup.sh             # install, build gsplat + MoGe, run GPU checks
#   bash molab_setup.sh --check     # only rerun the GPU checks/report
#   bash molab_setup.sh --rebuild   # rebuild gsplat even if a cached build exists
#
# Everything is logged to setup-logs/<UTC time>/ and packed into
# setup-logs/namma-setup-<UTC time>.tar.gz. Return that file when asking for help.
set -Eeuo pipefail
# Molab injects these for its own Python 3.13; they break the isolated venv.
unset PYTHONPATH PYTHONSAFEPATH PYTHONHOME

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

# ---- Pinned inputs ---------------------------------------------------------------------------
PYTHON_VERSION=3.12
MIN_DRIVER_CUDA=13.0                          # Torch 2.11.0+cu130 runtime
GSPLAT_URL=https://github.com/nerfstudio-project/gsplat.git
GSPLAT_COMMIT=512d366b67073d77ca099ede742683c165dfc23b   # main, 19 Sep 2026 (1.6.0 dev; CUDA 13 support)
GSPLAT_DIR=/opt/namma-src/gsplat              # outside /marimo: a molab restart cannot half-restore it
CACHE_DIR=/opt/namma-cache                    # compiled gsplat by build signature; the notebook syncs it with Drive
# Published compiled builds: <base>/gsplat-<signature>.tar + .tar.sha256 (GitHub release assets).
PREBUILT_BASE="${NAMMA_PREBUILT_BASE:-https://github.com/TheCodeNotTakenT-T/namma-space/releases/download/gsplat-prebuilt}"
MOGE_COMMIT=74fbce054ebed49800de42d0ad0e83495065719a     # microsoft/MoGe (MIT), MoGe-2 model used
UTILS3D_COMMIT=62f09d58509485564e24d5d9f6aac9ee9ebc0c37  # pinned by MoGe's pyproject
VENV="${NAMMA_VENV:-$REPO_ROOT/.venv}"
VENV_PY="$VENV/bin/python"

MODE=full
REBUILD=0
for arg in "$@"; do
    case "$arg" in
        --check) MODE=check ;;
        --rebuild) REBUILD=1 ;;
        *) echo "Unknown option: $arg"; exit 2 ;;
    esac
done

mkdir -p "$REPO_ROOT/setup-logs"
exec 9>"$REPO_ROOT/setup-logs/.lock"
flock -n 9 || { echo "Another molab_setup.sh is running in this repository."; exit 1; }
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
LOG_DIR="$REPO_ROOT/setup-logs/$STAMP"
mkdir -p "$LOG_DIR"
exec > >(tee -a "$LOG_DIR/setup.log") 2>&1
TIMINGS="$LOG_DIR/timings.tsv"
printf 'step\tseconds\n' > "$TIMINGS"

finish() {
    local code=$?
    echo "$STAMP" > "$REPO_ROOT/setup-logs/LATEST"
    if [[ $code == 0 ]]; then
        echo "SETUP PASSED. Report: $LOG_DIR/report.md"
    else
        echo "SETUP FAILED (exit $code). Full log: $LOG_DIR/setup.log"
    fi
    echo "Download and return: $REPO_ROOT/setup-logs/namma-setup-$STAMP.tar.gz"
    tar -czf "$REPO_ROOT/setup-logs/namma-setup-$STAMP.tar.gz" -C "$REPO_ROOT/setup-logs" "$STAMP" 2>/dev/null || true
}
trap finish EXIT

step() {  # step <name> <function>: run, time and record one setup stage
    local name=$1 started=$SECONDS
    echo; echo "==== $name ($(date -u +%H:%M:%S) UTC)"
    "$2"
    printf '%s\t%s\n' "$name" "$((SECONDS - started))" >> "$TIMINGS"
}

# ---- Stages ---------------------------------------------------------------------------------
preflight() {
    [[ "$(uname -s)" == Linux ]] || { echo "Run this on the Linux GPU machine."; exit 1; }
    command -v nvidia-smi >/dev/null || { echo "nvidia-smi missing: select a GPU runtime."; exit 1; }
    for tool in git gcc curl tar flock; do
        command -v "$tool" >/dev/null || { echo "Missing required tool: $tool"; exit 1; }
    done
    nvidia-smi | tee "$LOG_DIR/nvidia-smi.txt"
    local driver_cuda
    driver_cuda="$(grep -o 'CUDA Version: [0-9.]*' "$LOG_DIR/nvidia-smi.txt" | awk '{print $3}')"
    if [[ "$(printf '%s\n%s\n' "$MIN_DRIVER_CUDA" "$driver_cuda" | sort -V | sed -n 1p)" != "$MIN_DRIVER_CUDA" ]]; then
        echo "Driver supports CUDA $driver_cuda; Torch cu130 needs $MIN_DRIVER_CUDA or newer."; exit 1
    fi
    if ! command -v uv >/dev/null; then
        python3 -m pip install --quiet uv
    fi
    { uv --version; gcc --version | sed -n 1p; ldd --version | sed -n 1p; git -C "$REPO_ROOT" rev-parse HEAD
      git -C "$REPO_ROOT" status --short; echo "cpus=$(nproc)"; free -g; df -h "$REPO_ROOT" "$HOME"; } \
        | tee "$LOG_DIR/host.txt"
}

install_python() {
    if [[ -x "$VENV_PY" ]] && ! "$VENV_PY" -c "import sys; assert sys.version.startswith('$PYTHON_VERSION.')" 2>/dev/null; then
        local saved="$VENV-preserved-$STAMP"
        echo "Existing $VENV is not Python $PYTHON_VERSION; moving it to $saved (nothing deleted)."
        mv "$VENV" "$saved"
    elif [[ -e "$VENV" ]] && ! "$VENV_PY" -c "import torch, numpy" 2>/dev/null; then
        # A molab shutdown keeps some files of the venv but not its interpreter or binaries.
        echo "$VENV is incomplete (interrupted install or molab shutdown); recreating it from the lock file."
        rm -rf "$VENV"
    fi
    [[ -x "$VENV_PY" ]] || uv venv --python "$PYTHON_VERSION" --seed "$VENV"
    uv pip install --python "$VENV_PY" --index-strategy unsafe-best-match -r env/requirements.lock.txt
    uv pip freeze --python "$VENV_PY" > "$LOG_DIR/pip-freeze.txt"
}

cuda_environment() {
    # nvcc comes from the pinned cuda-toolkit wheels inside the venv, matching Torch's CUDA.
    CUDA_HOME="$("$VENV_PY" -c 'import nvidia, pathlib; print(pathlib.Path(list(nvidia.__path__)[0]) / "cu13")')"
    # The venv's bin holds ninja: without it on PATH, torch builds extensions one file at a time.
    export CUDA_HOME PATH="$VENV/bin:$CUDA_HOME/bin:$PATH"
    command -v ninja >/dev/null || { echo "ninja missing from $VENV/bin (parallel builds impossible)"; exit 1; }
    [[ -x "$CUDA_HOME/bin/nvcc" ]] || { echo "nvcc missing at $CUDA_HOME/bin"; exit 1; }
    # The linker needs the unversioned name; the wheel only ships libcudart.so.13.
    [[ -e "$CUDA_HOME/lib/libcudart.so" ]] || ln -s libcudart.so.13 "$CUDA_HOME/lib/libcudart.so"
    export LD_LIBRARY_PATH="$CUDA_HOME/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
    # Kept from the original multi-extension build: part of the cached gsplat build's signature.
    export NVCC_FLAGS="--device-entity-has-hidden-visibility=false -static-global-template-stub=false"
    # Older rasterizer headers rely on transitive fixed-width integer declarations.
    export NVCC_PREPEND_FLAGS="--pre-include=stdint.h,cstdint,cstddef"
    # CUDA 13 moved CCCL (cub/thrust/libcu++) out of include/; gsplat's host .cpp files need it too.
    local limits cccl
    limits="$(find -L "$CUDA_HOME" -path '*/cuda/std/limits' -print -quit)"
    [[ -n "$limits" ]] || { echo "CCCL headers (cuda/std/limits) not found under $CUDA_HOME"; exit 1; }
    cccl="$(dirname "$(dirname "$(dirname "$limits")")")"
    echo "CCCL include dir: $cccl"
    if [[ "$cccl" != "$CUDA_HOME/include" ]]; then
        NVCC_PREPEND_FLAGS+=" -I$cccl"
        export CPLUS_INCLUDE_PATH="$cccl${CPLUS_INCLUDE_PATH:+:$CPLUS_INCLUDE_PATH}"
        export CUDA_INC_PATH="$cccl"   # torch adds this to both g++ and nvcc include paths
    fi
    export FORCE_CUDA=1
    # Parallel nvcc jobs: one per CPU, at most one per 4 GiB of available RAM.
    local ram_jobs
    ram_jobs="$(awk '/MemAvailable/ {print int($2 / 4194304)}' /proc/meminfo)"
    export MAX_JOBS="${MAX_JOBS:-$(( ram_jobs < $(nproc) ? (ram_jobs > 0 ? ram_jobs : 1) : $(nproc) ))}"
    if [[ -z "${TORCH_CUDA_ARCH_LIST:-}" ]]; then
        TORCH_CUDA_ARCH_LIST="$("$VENV_PY" -c 'import torch; print("%d.%d" % torch.cuda.get_device_capability())')"
    fi
    export TORCH_CUDA_ARCH_LIST
    local nvcc_release torch_cuda
    nvcc_release="$(nvcc --version | grep -o 'release [0-9.]*' | awk '{print $2}')"
    torch_cuda="$("$VENV_PY" -c 'import torch; print(torch.version.cuda)')"
    echo "CUDA_HOME=$CUDA_HOME nvcc=$nvcc_release torch_cuda=$torch_cuda arch=$TORCH_CUDA_ARCH_LIST MAX_JOBS=$MAX_JOBS"
    [[ "$nvcc_release" == "$torch_cuda" ]] || { echo "nvcc $nvcc_release does not match Torch CUDA $torch_cuda"; exit 1; }
    nvcc --list-gpu-arch > "$LOG_DIR/nvcc-gpu-arch.txt"
    grep -qx "compute_${TORCH_CUDA_ARCH_LIST//./}" "$LOG_DIR/nvcc-gpu-arch.txt" \
        || { echo "nvcc cannot target compute capability $TORCH_CUDA_ARCH_LIST"; exit 1; }
}

signature() {  # identity of one extension build: toolchain + exact sources
    local top
    top="$(git -C "$1" rev-parse --show-toplevel)"
    {
        "$VENV_PY" -c 'import sys, torch; print(sys.version, torch.__version__, torch.version.cuda)'
        nvcc --version | tail -2
        gcc --version | sed -n 1p
        # Paths inside the venv are written as <venv>: a published build must match wherever the repo is cloned.
        echo "$TORCH_CUDA_ARCH_LIST|$NVCC_FLAGS|${NVCC_PREPEND_FLAGS//$VENV/<venv>}|${FAST_MATH:-1}|${CPLUS_INCLUDE_PATH//$VENV/<venv>}"
        if [[ "$top" == "$REPO_ROOT" ]]; then
            git ls-files -s "$1"
            git diff HEAD -- "$1"
        else  # its own checkout (gsplat): pinned commit + our patch
            git -C "$top" rev-parse HEAD
            git -C "$top" diff
        fi
    } | sha256sum | cut -d' ' -f1
}

fetch_gsplat() {
    local dir=$GSPLAT_DIR patch="$REPO_ROOT/env/patches/gsplat-relocation-sign.patch"
    if [[ "$(git -C "$dir" rev-parse HEAD 2>/dev/null)" != "$GSPLAT_COMMIT" ]]; then
        rm -rf "$dir"   # scratch copy of pinned upstream source, never edited by hand
        mkdir -p "$dir"
        git -C "$dir" init -q
        git -C "$dir" fetch -q --depth 1 "$GSPLAT_URL" "$GSPLAT_COMMIT"
        git -C "$dir" checkout -q --detach FETCH_HEAD
        git -C "$dir" submodule update -q --init --recursive --depth 1
    fi
    if git -C "$dir" apply --reverse --check "$patch" 2>/dev/null; then
        echo "gsplat relocation patch already applied."
    else
        git -C "$dir" apply "$patch"
    fi
    git -C "$dir" log -1 --format='gsplat %H %cd'
    git -C "$dir" diff --stat
}

install_moge() {  # pure Python; --no-deps keeps NumPy 1.26.4 (MoGe 3.0's pyproject asks for numpy>=2)
    local stamp="$VENV/.namma-builds/moge" want="$MOGE_COMMIT $UTILS3D_COMMIT"
    if [[ -f "$stamp" && "$(cat "$stamp")" == "$want" ]] && "$VENV_PY" -c "import moge.model.v2, utils3d_moge" 2>/dev/null; then
        echo "MoGe already installed at the pinned commits."
        return
    fi
    if ! "$VENV_PY" -m pip install --no-deps --no-cache-dir --force-reinstall             "moge @ git+https://github.com/microsoft/MoGe.git@$MOGE_COMMIT"             "utils3d_moge @ git+https://github.com/EasternJournalist/utils3d-moge.git@$UTILS3D_COMMIT"             > "$LOG_DIR/install-moge.log" 2>&1; then
        tail -n 30 "$LOG_DIR/install-moge.log"; echo "MoGe install failed."; exit 1
    fi
    mkdir -p "$VENV/.namma-builds"
    echo "$want" > "$stamp"
}

save_cache() {  # save_cache <distribution> <signature>: pack the installed files so later sessions skip compiling
    local archive="$CACHE_DIR/$1-$2.tar"
    [[ ! -f "$archive" ]] || return 0
    mkdir -p "$CACHE_DIR"
    "$VENV_PY" - "$1" "$archive" <<'PY'
import importlib.metadata as md, pathlib, sys, tarfile
dist, archive = md.distribution(sys.argv[1]), pathlib.Path(sys.argv[2])
base = pathlib.Path(dist.locate_file(""))
with tarfile.open(archive.with_suffix(".part"), "w") as tar:
    for rel in dist.files:
        if (base / rel).exists():
            tar.add(base / rel, arcname=str(rel))
archive.with_suffix(".part").rename(archive)
PY
    sha256sum "$archive" | cut -d' ' -f1 > "$archive.sha256"
    echo "$1: compiled build saved to $archive (uploaded to Drive when you click Start)"
}

fetch_prebuilt() {  # fetch_prebuilt <file>: download a published build if one matches this exact signature
    local tmp="$CACHE_DIR/$1.download" want
    mkdir -p "$CACHE_DIR"
    if ! want="$(curl -fsSL --max-time 30 "$PREBUILT_BASE/$1.sha256")"; then
        echo "No published build for this signature at $PREBUILT_BASE ($1); compiling instead."
        return 1
    fi
    echo "Downloading the published build $1"
    curl -fsSL --retry 3 "$PREBUILT_BASE/$1" -o "$tmp" || { rm -f "$tmp"; return 1; }
    if [[ "$(sha256sum "$tmp" | cut -d' ' -f1)" != "${want%% *}" ]]; then
        echo "Published build failed its checksum; ignoring it."
        rm -f "$tmp"
        return 1
    fi
    mv "$tmp" "$CACHE_DIR/$1"
    echo "${want%% *}" > "$CACHE_DIR/$1.sha256"
}

build_one() {  # build_one <name> <path> <required:1|0>
    local name=$1 path=$2 required=$3 started=$SECONDS
    local stamps="$VENV/.namma-builds" sig
    mkdir -p "$stamps"
    sig="$(signature "$path")"
    if [[ $REBUILD == 0 && -f "$stamps/$name" && "$(cat "$stamps/$name")" == "$sig" ]]; then
        echo "$name: cached build matches toolchain and sources."
        printf 'build:%s\tcached\n' "$name" >> "$TIMINGS"
        [[ $name != gsplat ]] || save_cache gsplat "$sig"
        return
    fi
    if [[ $REBUILD == 0 && $name == gsplat && ! -f "$CACHE_DIR/$name-$sig.tar" ]]; then
        fetch_prebuilt "$name-$sig.tar" || true
    fi
    if [[ $REBUILD == 0 && -f "$CACHE_DIR/$name-$sig.tar" ]]; then
        tar -xf "$CACHE_DIR/$name-$sig.tar" -C "$("$VENV_PY" -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')"
        echo "$sig" > "$stamps/$name"
        echo "$name: restored the compiled build from $CACHE_DIR (no compilation)."
        printf 'build:%s\trestored\n' "$name" >> "$TIMINGS"
        return
    fi
    rm -f "$stamps/$name"
    rm -rf "$path/build"   # generated objects from another toolchain
    echo "$name: building (log: $LOG_DIR/build-$name.log)"
    if "$VENV_PY" -m pip install --no-build-isolation --no-deps --no-cache-dir --force-reinstall -v "$path" \
            > "$LOG_DIR/build-$name.log" 2>&1; then
        echo "$sig" > "$stamps/$name"
        printf 'build:%s\t%s\n' "$name" "$((SECONDS - started))" >> "$TIMINGS"
        [[ $name != gsplat ]] || save_cache gsplat "$sig"
    else
        printf 'build:%s\tfailed\n' "$name" >> "$TIMINGS"
        tail -n 40 "$LOG_DIR/build-$name.log"
        if [[ $required == 1 ]]; then
            echo "Required extension $name failed to build."; exit 1
        fi
        echo "Optional extension $name failed."
    fi
}

build_extensions() {
    build_one gsplat "$GSPLAT_DIR" 1
    uv pip freeze --python "$VENV_PY" > "$LOG_DIR/pip-freeze-after-build.txt"
}

gpu_checks() {
    NAMMA_GSPLAT_SRC="$GSPLAT_DIR" "$VENV_PY" -m namma check --out "$LOG_DIR"
}

# ---- Run ------------------------------------------------------------------------------------
step preflight preflight
if [[ $MODE == full ]]; then
    step python install_python
fi
step cuda-environment cuda_environment
if [[ $MODE == full ]]; then
    step gsplat-source fetch_gsplat
    step extensions build_extensions
    step moge install_moge
fi
step gpu-checks gpu_checks

</file>

<file src="namma/__init__.py">
"""Namma Space: phone/DSLR video to a walkable Gaussian-splat room. Public entry point: ``python -m namma``."""

</file>

<file src="namma/__main__.py">
"""Single public command for the Namma Space workflow.

    python -m namma check --out setup-logs/<run>            # GPU/native-extension checks + report
    python -m namma prepare --video V --jobs-root DIR       # create the job (and its smoke test) for a video
    python -m namma run --job DIR [--until STAGE]           # run or resume every stage
    python -m namma status --job DIR                        # print the job's status.json
Drive backup/restore runs with the notebook's Python: python -m namma.backup --help
"""
import argparse
import json
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m namma")
    commands = parser.add_subparsers(dest="command", required=True)

    check = commands.add_parser("check", help="Run real GPU checks of every native extension and write a report")
    check.add_argument("--out", required=True, help="Directory for report.json / report.md")
    check.add_argument("--only", nargs="*", help="Run only these check names")

    prepare = commands.add_parser("prepare", help="Create the job folder for a video")
    prepare.add_argument("--video", required=True)
    prepare.add_argument("--jobs-root", required=True)
    prepare.add_argument("--settings", help='JSON overrides, e.g. {"train": {"steps": 40000}}')

    run = commands.add_parser("run", help="Run or resume a job")
    run.add_argument("--job", required=True)
    run.add_argument("--until", help="Stop after this stage")

    status = commands.add_parser("status", help="Show a job's status")
    status.add_argument("--job", required=True)

    args = parser.parse_args(argv)
    if args.command == "check":
        from namma import gpu_check
        return gpu_check.run_all(args.out, args.only)
    if args.command == "prepare":
        from namma import pipeline
        print(json.dumps(pipeline.prepare(args.video, args.jobs_root, json.loads(args.settings) if args.settings else None)))
        return 0
    if args.command == "run":
        from namma import pipeline
        return pipeline.run(args.job, args.until)
    if args.command == "status":
        from namma.workspace import Workspace, read_json
        print(json.dumps(read_json(Workspace(args.job).root / "status.json", {}), indent=1))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())

</file>

<file src="namma/backup.py">
"""Google Drive backup and restore for long jobs on molab (whose files vanish when a session ends).

The GPU worker never talks to Drive. When a stage finishes it commits an *outbox entry*: files plus a
MANIFEST.json (written last). A separate uploader runs with the notebook's own Python, which already
holds molab's Drive login (Files > Remote storage > Google Drive), uploads each entry, checks every
file (Drive md5 or a full read-back) and writes VERIFIED.json next to it on Drive. `restore` brings
verified stages and the newest training checkpoint back into a fresh session.

Remote layout: <remote>/<seq>-<stage>-<id>/{files..., MANIFEST.json, VERIFIED.json}
This module uses only the standard library (plus gdrive_fsspec inside upload/restore/fetch).

    python -m namma.backup upload  --job DIR --remote NammaSpaceBackups/<job>
    python -m namma.backup restore --job DIR --remote NammaSpaceBackups/<job>
    python -m namma.backup fetch   --job DIR --video "<path on Drive>"
"""
import argparse
import fcntl
import hashlib
import json
import os
import sys
import tarfile
import time
import uuid
from pathlib import Path

from namma.workspace import read_json, sha256_file, write_json

BLOCK = 64 * 2 ** 20
STAGE_FILES = {  # what each finished stage contributes to a restore (paths relative to the job)
    "frames": ["frames/images", "frames/frame_metrics.csv"],
    "sfm": ["sfm/sparse", "sfm/undistorted/images", "sfm/undistorted/sparse", "sfm/database.db"],
    "priors": ["dataset/sparse", "dataset/priors_scales.json"],  # MoGe maps are recomputed (repair mode)
    "mesh": ["mesh/room.glb"],
    "export": ["export/DOWNLOAD_THIS"],
}


# ---- producer side (worker) -------------------------------------------------------------------
def _next_seq(outbox):
    outbox.mkdir(parents=True, exist_ok=True)
    with open(outbox / "SEQ.lock", "a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        counter = outbox / "SEQ"
        value = int(counter.read_text()) + 1 if counter.exists() else 1
        counter.write_text(str(value))
        return value


def commit(ws, stage, files=(), tar_paths=(), meta=None):
    """Queue files for Drive. `tar_paths` (relative to the job) are packed into one tar first."""
    seq = _next_seq(ws.outbox)
    entry = ws.outbox / f"{seq:06d}-{stage}-{uuid.uuid4().hex[:6]}"
    entry.mkdir()
    listed = [Path(f) for f in files]
    existing = [p for p in tar_paths if (ws.root / p).exists()]
    if existing:
        archive = entry / f"{stage}.tar"
        with tarfile.open(archive, "w") as tar:
            for rel in existing:
                tar.add(ws.root / rel, arcname=rel)
        listed.append(archive)
    receipt = ws.receipt(stage)
    manifest = {"job": ws.job.get("job_id"), "stage": stage, "seq": seq, "created": time.time(), "meta": meta or {},
                "receipt": receipt,
                "files": [{"name": p.name, "path": str(p.resolve()), "bytes": p.stat().st_size, "sha256": sha256_file(p)}
                          for p in listed]}
    write_json(entry / "MANIFEST.json", manifest)  # written last: marks the entry complete
    return entry


def commit_stage(ws, stage):
    if stage in STAGE_FILES:
        return commit(ws, stage, tar_paths=STAGE_FILES[stage])
    return commit(ws, stage)


# ---- Drive access (notebook Python) -----------------------------------------------------------
def drive_fs(spec):
    if spec.startswith("local:"):  # tests: a plain folder stands in for Drive
        import fsspec
        return fsspec.filesystem("file"), spec[len("local:"):].rstrip("/") + "/"
    import pydata_google_auth.cache
    from gdrive_fsspec import GoogleDriveFileSystem
    token = pydata_google_auth.cache.READ_WRITE._path
    if not os.path.exists(token):
        raise RuntimeError("Google Drive is not connected: in molab open Files > Remote storage > Google Drive and run the cell it adds")
    fs = GoogleDriveFileSystem(token="cache", auth_kwargs={"use_local_webserver": False},
                               use_listings_cache=False, skip_instance_cache=True)
    return fs, ""


def _remote_md5(fs, path):
    try:
        return fs.info(path, fields="md5Checksum,size").get("md5Checksum")
    except TypeError:  # older gdrive_fsspec without `fields`
        return fs.info(path).get("md5Checksum")
    except Exception:
        return None


def put_verified(fs, local, remote, expected_sha=None):
    md5, sha = hashlib.md5(), hashlib.sha256()
    size = 0
    with open(local, "rb") as src, fs.open(remote, "wb", block_size=BLOCK) as dst:
        while chunk := src.read(BLOCK):
            md5.update(chunk)
            sha.update(chunk)
            dst.write(chunk)
            size += len(chunk)
    if expected_sha and sha.hexdigest() != expected_sha:
        raise IOError(f"{local} changed while uploading")
    remote_md5 = _remote_md5(fs, remote)
    if remote_md5 is None or size < 32 * 2 ** 20:  # no server checksum, or small enough to read back fully
        check = hashlib.sha256()
        with fs.open(remote, "rb", block_size=BLOCK) as f:
            while chunk := f.read(BLOCK):
                check.update(chunk)
        if check.hexdigest() != sha.hexdigest():
            raise IOError(f"read-back mismatch for {remote}")
    elif remote_md5 != md5.hexdigest():
        raise IOError(f"Drive md5 mismatch for {remote}")
    return sha.hexdigest()


def get_verified(fs, remote, local, sha256):
    local = Path(local)
    local.parent.mkdir(parents=True, exist_ok=True)
    tmp = local.with_name(local.name + ".part")
    digest = hashlib.sha256()
    with fs.open(remote, "rb", block_size=BLOCK) as src, open(tmp, "wb") as dst:
        while chunk := src.read(BLOCK):
            digest.update(chunk)
            dst.write(chunk)
    if digest.hexdigest() != sha256:
        tmp.unlink()
        raise IOError(f"downloaded {remote} does not match its manifest")
    tmp.replace(local)


def upload_loop(job_dir, remote, fs_spec="drive", once=False):
    from namma.workspace import Workspace
    ws = Workspace(job_dir)
    status_path = ws.root / "backup_status.json"
    lock = open(ws.root / "uploader.lock", "a")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("uploader already running for this job")
        return 0
    try:
        fs, prefix = drive_fs(fs_spec)
    except Exception as error:
        write_json(status_path, {"state": "auth_error", "error": str(error), "time": time.time()})
        raise
    base = prefix + remote.strip("/")
    uploaded_bytes, errors, started = 0, 0, time.time()
    while True:
        pipeline_state = read_json(ws.root / "status.json", {})  # read BEFORE scanning the outbox
        pending = sorted(e for e in ws.outbox.iterdir() if e.is_dir() and (e / "MANIFEST.json").exists()
                         and not (e / "UPLOADED.json").exists()) if ws.outbox.exists() else []
        for entry in pending:
            manifest = read_json(entry / "MANIFEST.json")
            folder = f"{base}/{entry.name}"
            write_json(status_path, {"state": "uploading", "entry": entry.name, "uploaded_bytes": uploaded_bytes,
                                     "errors": errors, "time": time.time()})
            try:
                fs.makedirs(base, exist_ok=True)
                fs.makedirs(folder, exist_ok=True)
                for item in manifest["files"]:
                    if not Path(item["path"]).exists():
                        item["missing"] = True  # e.g. an old checkpoint pruned after a newer one was written
                        continue
                    put_verified(fs, item["path"], f"{folder}/{item['name']}", item["sha256"])
                    uploaded_bytes += item["bytes"]
                with fs.open(f"{folder}/MANIFEST.json", "w") as f:
                    f.write(json.dumps(manifest, indent=1))
                verified = {"verified": time.time(), "files": [i["name"] for i in manifest["files"] if not i.get("missing")]}
                with fs.open(f"{folder}/VERIFIED.json", "w") as f:
                    f.write(json.dumps(verified))
                write_json(entry / "UPLOADED.json", {"remote": folder, **verified})
                if manifest["stage"] == "checkpoint" and verified["files"]:
                    _drop_older_checkpoints(fs, base, entry.name)
                for item in manifest["files"]:  # outbox tars are copies: free the disk
                    if Path(item["path"]).parent == entry and item["name"].endswith(".tar"):
                        Path(item["path"]).unlink(missing_ok=True)
            except Exception as error:
                errors += 1
                write_json(status_path, {"state": "retrying", "entry": entry.name, "error": f"{type(error).__name__}: {error}",
                                         "uploaded_bytes": uploaded_bytes, "errors": errors, "time": time.time()})
                time.sleep(min(300, 10 * errors))
                break
        else:
            state = pipeline_state.get("state")
            write_json(status_path, {"state": "idle", "uploaded_bytes": uploaded_bytes, "errors": errors,
                                     "pipeline": state, "time": time.time()})
            # Stop only when the outbox was empty AFTER the pipeline reported its end in this session.
            if once or (not pending and state in ("finished", "failed") and pipeline_state.get("updated", 0) >= started):
                return 0
            time.sleep(10)


def _drop_older_checkpoints(fs, base, newest):
    """Checkpoints are ~2 GB each; Drive keeps only the newest verified one."""
    for path in fs.ls(base, detail=False):
        name = path.rstrip("/").rsplit("/", 1)[-1]
        if "-checkpoint-" in name and name < newest:
            try:
                fs.rm(path, recursive=True)
            except Exception:
                pass


def ensure_folders(remotes, fs_spec="drive"):
    """Create the backup folders once, from one process (concurrent creation makes duplicate Drive folders)."""
    fs, prefix = drive_fs(fs_spec)
    for remote in remotes:
        fs.makedirs(prefix + remote.strip("/"), exist_ok=True)


def restore(job_dir, remote, fs_spec="drive"):
    """Bring verified stages (and the newest training checkpoint) back from Drive."""
    from namma.workspace import Workspace
    ws = Workspace(job_dir)
    fs, prefix = drive_fs(fs_spec)
    base = prefix + remote.strip("/")
    if not fs.exists(base):
        return {"restored": [], "note": "nothing on Drive yet"}
    entries = sorted(p.rstrip("/").rsplit("/", 1)[-1] for p in fs.ls(base, detail=False))
    seqs = [int(e.split("-", 1)[0]) for e in entries if e.split("-", 1)[0].isdigit()]
    if seqs:  # first, so new entries never reuse numbers already on Drive even if a download fails
        current = int((ws.outbox / "SEQ").read_text()) if (ws.outbox / "SEQ").exists() else 0
        (ws.outbox / "SEQ").write_text(str(max(current, max(seqs))))
    verified = [e for e in entries if fs.exists(f"{base}/{e}/VERIFIED.json")]
    restored, newest_ckpt = [], None
    for name in verified:
        manifest = json.loads(fs.cat_file(f"{base}/{name}/MANIFEST.json"))
        stage = manifest["stage"]
        if stage == "checkpoint":
            usable = manifest["files"] and not manifest["files"][0].get("missing")
            if usable and (newest_ckpt is None or manifest["meta"]["step"] > newest_ckpt[0]["meta"]["step"]):
                newest_ckpt = (manifest, name)
            continue
        receipt = manifest.get("receipt")
        if not receipt or ws.receipt(stage) == receipt:
            continue
        for item in manifest["files"]:
            if item.get("missing"):
                continue
            local = ws.root / "restore" / item["name"]
            get_verified(fs, f"{base}/{name}/{item['name']}", local, item["sha256"])
            if item["name"].endswith(".tar"):
                with tarfile.open(local) as tar:
                    tar.extractall(ws.root, filter="data")
                local.unlink()
            elif stage == "train":
                local.replace(ws.train / item["name"])
        write_json(ws.stages / f"{stage}.json", receipt)
        restored.append(stage)
    if newest_ckpt and not (ws.stages / "train.json").exists():
        manifest, name = newest_ckpt
        item = manifest["files"][0]
        get_verified(fs, f"{base}/{name}/{item['name']}", ws.train / "ckpt" / item["name"], item["sha256"])
        restored.append(f"checkpoint step {manifest['meta']['step']}")
    return {"restored": restored}


def fetch_video(job_dir, remote_video, fs_spec="drive"):
    """Copy the source video from Drive into the job (sessions start empty)."""
    from namma.workspace import Workspace
    ws = Workspace(job_dir)
    fs, prefix = drive_fs(fs_spec)
    remote = prefix + remote_video.strip("/")
    info = fs.info(remote)
    target = ws.input / ("video" + Path(remote).suffix.lower())
    if target.exists() and target.stat().st_size == int(info["size"]):
        return {"video": str(target), "bytes": target.stat().st_size, "cached": True}
    tmp = target.with_name(target.name + ".part")
    done = 0
    with fs.open(remote, "rb", block_size=BLOCK) as src, open(tmp, "wb") as dst:
        while chunk := src.read(BLOCK):
            dst.write(chunk)
            done += len(chunk)
            write_json(ws.root / "fetch_status.json", {"bytes": done, "total": int(info["size"]), "time": time.time()})
    tmp.replace(target)
    return {"video": str(target), "bytes": done, "md5": info.get("md5Checksum"), "cached": False}


def cache_sync(local_dir, remote, direction, fs_spec="drive"):
    """Copy compiled-build archives (<name>-<signature>.tar) between /opt/namma-cache and Drive."""
    fs, prefix = drive_fs(fs_spec)
    base = prefix + remote.strip("/")
    local_dir = Path(local_dir)
    local_dir.mkdir(parents=True, exist_ok=True)
    fs.makedirs(base, exist_ok=True)
    remote_names = {p.rstrip("/").rsplit("/", 1)[-1] for p in fs.ls(base, detail=False)}
    moved = []
    if direction == "push":
        for tar in sorted(local_dir.glob("*.tar")):
            if tar.name not in remote_names:
                sha = put_verified(fs, tar, f"{base}/{tar.name}")
                with fs.open(f"{base}/{tar.name}.sha256", "w") as f:
                    f.write(sha)
                moved.append(tar.name)
    else:
        for name in sorted(n for n in remote_names if n.endswith(".tar")):
            if not (local_dir / name).exists() and f"{name}.sha256" in remote_names:
                sha = fs.cat_file(f"{base}/{name}.sha256").decode().strip()
                get_verified(fs, f"{base}/{name}", local_dir / name, sha)
                moved.append(name)
    return {direction: moved}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m namma.backup")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("cache-push", "cache-pull"):
        p = sub.add_parser(name)
        p.add_argument("--dir", default="/opt/namma-cache")
        p.add_argument("--remote", default="NammaSpaceBackups/_build-cache")
        p.add_argument("--fs", default="drive")
    for name in ("upload", "restore", "fetch"):
        p = sub.add_parser(name)
        p.add_argument("--job", required=True)
        p.add_argument("--fs", default="drive", help="'drive' or local:/folder for tests")
        if name == "fetch":
            p.add_argument("--video", required=True)
        else:
            p.add_argument("--remote", required=True)
        if name == "upload":
            p.add_argument("--once", action="store_true")
    args = parser.parse_args(argv)
    if args.command in ("cache-push", "cache-pull"):
        print(json.dumps(cache_sync(args.dir, args.remote, args.command.split("-")[1], args.fs)))
        return 0
    if args.command == "upload":
        return upload_loop(args.job, args.remote, args.fs, args.once)
    result = restore(args.job, args.remote, args.fs) if args.command == "restore" else fetch_video(args.job, args.video, args.fs)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())

</file>

<file src="namma/config.py">
"""Pipeline settings. Defaults target a 2-10 minute indoor walkthrough video on one large GPU."""
import dataclasses
import hashlib
import json
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FramesConfig:
    shift: float = 0.07          # median image motion between keyframes, fraction of width
    min_gap: float = 0.15        # seconds; lets fast camera moves still get enough frames
    max_gap: float = 1.0         # seconds; guarantees >= 1 frame/s
    window: float = 0.2          # seconds searched around a trigger for the sharpest frame
    min_rel_sharp: float = 0.8   # sharpness relative to the +-1 s rolling median
    sharp_width: int = 1920
    flow_width: int = 640
    jpeg_quality: int = 95
    max_frames: int = 2000       # refuse silently huge selections; raise min_gap instead
    start_s: float = 0.0
    end_s: float = 0.0           # 0 = until the end


@dataclass
class SfmConfig:
    max_image_size: int = 3200   # SIFT extraction resolution (long side)
    max_features: int = 8192
    camera_model: str = "OPENCV"
    overlap: int = 20            # sequential neighbours matched per frame
    quadratic_overlap: int = 10  # second pass: +1,+2,+4,... long-range hops
    loop_detection: bool = True  # only if the vocabulary tree can be fetched
    vocab_tree_url: str = ("https://github.com/colmap/colmap/releases/download/3.11.1/"
                           "vocab_tree_faiss_flickr100K_words256K.bin")
    mapper: str = "auto"         # auto = global, then incremental if registration is low
    max_global_error: float = 1.5  # px; above this (or with outlier cameras) the incremental mapper also runs
    outlier_factor: float = 6.0    # cameras farther than this x the median distance from the median centre are outliers
    min_registered: float = 0.5  # below this the job stops; below warn_registered it continues with a warning
    warn_registered: float = 0.9
    train_long_side: int = 1920  # training image size after undistortion


@dataclass
class PriorsConfig:
    enabled: bool = True
    model: str = "Ruicheng/moge-2-vitl-normal"   # MIT code and weights
    resolution_level: int = 9
    min_points: int = 30         # sparse points needed to trust a frame's depth scale
    image_long_side: int = 1920  # training images are undistorted from the original frames at this size (3840: untested)
    prior_long_side: int = 1920  # MoGe maps are stored at this size; training upsamples them


# Per-strategy values of the TrainConfig fields left at None (gsplat simple_trainer's defaults and its mcmc preset).
STRATEGY_DEFAULTS = {"default": {"init_opacity": 0.1, "init_scale": 1.0, "opacity_reg": 0.0, "scale_reg": 0.0},
                     "mcmc": {"init_opacity": 0.5, "init_scale": 0.1, "opacity_reg": 0.01, "scale_reg": 0.01}}


@dataclass
class TrainConfig:
    steps: int = 30_000
    strategy: str = "mcmc"       # "mcmc" (Round 1 room); "default" = original 3DGS densification (untested on GPU)
    cap_max: int = 1_000_000     # mcmc only: gsplat's default; 3M collapsed to fog on a classroom (cause not yet found)
    max_gaussians: int = 6_000_000  # default only: densification stops here (web viewer limit)
    sh_degree: int = 3
    sh_degree_interval: int = 1000
    ssim_lambda: float = 0.2
    opacity_reg: Optional[float] = None  # None = STRATEGY_DEFAULTS
    scale_reg: Optional[float] = None
    init_opacity: Optional[float] = None
    init_scale: Optional[float] = None
    depth_lambda: float = 0.2    # log-depth L1 against aligned priors, decays to depth_lambda_end
    depth_lambda_end: float = 0.02
    normal_lambda: float = 0.05  # 1 - cos against prior normals, from normal_start
    normal_start: int = 3000
    appearance: bool = True      # per-image affine colour correction (exposure / white balance)
    test_every: int = 24         # every Nth frame is held out for evaluation
    checkpoint_every: int = 2500
    preview_every: int = 2500
    max_bad_steps: int = 50      # consecutive non-finite steps before stopping
    min_psnr: float = 16.0       # held-out PSNR below this means training failed; stop before meshing
    normalize_world: bool = True  # train at gsplat's scale (median camera distance 1); export stays metric

    def value(self, name):
        """A field left at None takes the strategy's default."""
        value = getattr(self, name)
        return STRATEGY_DEFAULTS[self.strategy][name] if value is None else value


@dataclass
class MeshConfig:
    voxel: float = 0.02          # metres (scene is metric after the priors stage)
    trunc_voxels: float = 4.0
    max_depth: float = 12.0
    render_long_side: int = 960
    max_views: int = 400
    min_alpha: float = 0.5
    target_triangles: int = 200_000   # viewer limit is 250,000
    min_component_fraction: float = 0.002


@dataclass
class Config:
    frames: FramesConfig = field(default_factory=FramesConfig)
    sfm: SfmConfig = field(default_factory=SfmConfig)
    priors: PriorsConfig = field(default_factory=PriorsConfig)
    train: TrainConfig = field(default_factory=TrainConfig)
    mesh: MeshConfig = field(default_factory=MeshConfig)

    def to_dict(self):
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data):
        cfg = cls()
        for section, values in (data or {}).items():
            target = getattr(cfg, section)
            for key, value in values.items():
                if not hasattr(target, key):
                    raise KeyError(f"Unknown setting {section}.{key}")
                setattr(target, key, value)
        return cfg

    def stage_hash(self, *sections):
        """Hash of the settings a stage depends on; a change re-runs that stage."""
        blob = json.dumps({s: dataclasses.asdict(getattr(self, s)) for s in sections}, sort_keys=True)
        return hashlib.sha256(blob.encode()).hexdigest()[:16]


def smoke_config():
    """Tiny settings for the end-to-end test that runs before a long job."""
    cfg = Config()
    cfg.frames.end_s = 20.0
    cfg.frames.max_gap = 0.5
    cfg.sfm.max_image_size = 1600
    cfg.sfm.loop_detection = False
    cfg.sfm.min_registered = 0.2  # the smoke test proves the toolchain, not the opening seconds
    cfg.sfm.train_long_side = 960
    cfg.priors.image_long_side = 960
    cfg.priors.prior_long_side = 960
    cfg.train.steps = 1500
    cfg.train.cap_max = 200_000
    cfg.train.max_gaussians = 200_000
    cfg.train.checkpoint_every = 500
    cfg.train.preview_every = 500
    cfg.train.normal_start = 500
    cfg.train.sh_degree_interval = 300
    cfg.train.min_psnr = 12.0  # 1500 steps prove the toolchain, not the final quality
    cfg.mesh.voxel = 0.04
    cfg.mesh.max_views = 60
    cfg.mesh.target_triangles = 50_000
    return cfg

</file>

<file src="namma/driver.py">
"""Start or resume a reconstruction from the notebook: one detached process per click.

Runs with the notebook's Python (it holds molab's Google Drive login) and drives the GPU venv:
  1. copy the video from Drive (sessions start empty),
  2. create the job (named after the video's content, so every session finds the same backups),
  3. restore whatever is already verified on Drive, then start one uploader per job,
  4. run the ~10 minute smoke test (first 20 s of video, tiny settings) unless it already passed,
  5. run or resume the full job.
Progress goes to <jobs-root>/driver_status.json; each job keeps its own status.json.
"""
import argparse
import json
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path

from namma import backup
from namma.workspace import read_json, write_json


def _status(root, **fields):
    current = read_json(root / "driver_status.json", {})
    current.update(fields, updated=time.time())
    write_json(root / "driver_status.json", current)


def notebook_env(repo):
    """The notebook's own environment (Drive login, gdrive_fsspec) with this repository importable."""
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(p for p in (repo, env.get("PYTHONPATH", "")) if p)
    return env


def venv_env():
    """molab sets PYTHONPATH/PYTHONSAFEPATH for its own Python; they break the GPU venv."""
    return {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "PYTHONSAFEPATH", "PYTHONHOME")}


def _uploader(job, remote, fs_spec, repo):
    log = open(Path(job) / "logs" / "uploader.log", "ab")
    return subprocess.Popen([sys.executable, "-m", "namma.backup", "upload", "--job", job, "--remote", remote, "--fs", fs_spec],
                            cwd=repo, env=notebook_env(repo), stdin=subprocess.DEVNULL, stdout=log,
                            stderr=subprocess.STDOUT, start_new_session=True)


def _run_stage_process(venv_py, job, repo, log_name):
    with open(Path(job) / "logs" / log_name, "ab") as log:
        return subprocess.run([venv_py, "-m", "namma", "run", "--job", job], cwd=repo, env=venv_env(),
                              stdout=log, stderr=subprocess.STDOUT).returncode


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m namma.driver")
    parser.add_argument("--video", required=True, help="Video path on Google Drive (or a local file with --local-video)")
    parser.add_argument("--jobs-root", default="/opt/namma-jobs")
    parser.add_argument("--remote-root", default="NammaSpaceBackups")
    parser.add_argument("--venv-python", required=True)
    parser.add_argument("--skip-smoke", action="store_true")
    parser.add_argument("--local-video", action="store_true")
    parser.add_argument("--fs", default="drive")
    parser.add_argument("--settings", help="JSON overrides for a new job")
    args = parser.parse_args(argv)
    repo = str(Path(__file__).resolve().parents[1])
    root = Path(args.jobs_root)
    root.mkdir(parents=True, exist_ok=True)
    _status(root, state="running", step="starting", error=None, video=args.video, started=time.time())
    try:
        if args.local_video:
            video = args.video
        else:
            _status(root, step="copying the video from Google Drive")
            video = backup.fetch_video(root / "_incoming", args.video, args.fs)["video"]
        _status(root, step="creating the job (hashing the video)")
        cmd = [args.venv_python, "-m", "namma", "prepare", "--video", video, "--jobs-root", str(root)]
        if args.settings:
            cmd += ["--settings", args.settings]
        prepared = subprocess.run(cmd, cwd=repo, env=venv_env(), capture_output=True, text=True)
        if prepared.returncode:
            raise RuntimeError("prepare failed:\n" + prepared.stdout[-2000:] + prepared.stderr[-4000:])
        info = json.loads(prepared.stdout.strip().splitlines()[-1])
        _status(root, job=info["job"], smoke_job=info["smoke_job"], job_id=info["job_id"])
        jobs = [(info["smoke_job"], f"{args.remote_root}/{info['job_id']}-smoke"), (info["job"], f"{args.remote_root}/{info['job_id']}")]
        backup.ensure_folders([args.remote_root] + [remote for _, remote in jobs], args.fs)
        try:  # keep this session's compiled gsplat so the next session's setup skips compiling
            _status(root, step="saving the compiled gsplat build to Drive", cache=backup.cache_sync(
                "/opt/namma-cache", f"{args.remote_root}/_build-cache", "push", args.fs))
        except Exception as error:
            _status(root, cache_error=f"{type(error).__name__}: {error}")
        for job, remote in jobs:
            _status(root, step=f"restoring backups for {Path(job).name}")
            try:
                restored = backup.restore(job, remote, args.fs)
                _status(root, **{f"restored_{Path(job).name}": restored})
            except Exception as error:  # a failed restore only means more recomputation
                _status(root, **{f"restore_error_{Path(job).name}": f"{type(error).__name__}: {error}"})
            _uploader(job, remote, args.fs, repo)
        smoke_state = read_json(Path(info["smoke_job"]) / "status.json", {}).get("state")
        if not args.skip_smoke and smoke_state != "finished":
            _status(root, step="smoke test (first 20 s of video, tiny settings)")
            if _run_stage_process(args.venv_python, info["smoke_job"], repo, "driver-run.log"):
                error = read_json(Path(info["smoke_job"]) / "status.json", {}).get("error")
                raise RuntimeError(f"Smoke test failed, full run not started: {error}")
        _status(root, step="full reconstruction")
        if _run_stage_process(args.venv_python, info["job"], repo, "driver-run.log"):
            error = read_json(Path(info["job"]) / "status.json", {}).get("error")
            raise RuntimeError(f"Reconstruction failed: {error}")
        _status(root, state="finished", step="done; waiting for the last Drive uploads")
        return 0
    except Exception as error:
        _status(root, state="failed", error=f"{type(error).__name__}: {error}", traceback=traceback.format_exc()[-4000:])
        return 1


if __name__ == "__main__":
    sys.exit(main())

</file>

<file src="namma/export.py">
"""DOWNLOAD_THIS package in the format the desktop importer (scene-pipeline.py) already accepts.

result-<id>.zip contains namma-result.json, namma-input.json, cameras.json, assets/room.ply
(standard 3DGS PLY), assets/room.glb (collision, same frame, identity transform) and assets/views.json.
Archives over 90 MiB are split into .partNNN pieces with a .parts.json manifest of SHA-256 sums.
"""
import json
import math
import shutil
import subprocess
import time
import uuid
import zipfile
from pathlib import Path

import numpy as np
import torch

from namma import trainer as T
from namma.workspace import read_json, sha256_file, write_json

PART = 90 * 1024 ** 2
REPO = Path(__file__).resolve().parents[1]


def write_ply(splats, path):
    """Inria 3DGS layout: x y z nx ny nz f_dc_0..2 f_rest_0..44 opacity scale_0..2 rot_0..3 (wxyz)."""
    means = splats["means"].float().cpu()
    n = len(means)
    sh0 = splats["sh0"].float().cpu().reshape(n, 3)
    shN = splats["shN"].float().cpu().transpose(1, 2).reshape(n, -1)  # channel-major like the reference
    quats = torch.nn.functional.normalize(splats["quats"].float().cpu(), dim=-1)
    data = torch.cat([means, torch.zeros(n, 3), sh0, shN, splats["opacities"].float().cpu().reshape(n, 1),
                      splats["scales"].float().cpu(), quats], 1).numpy().astype(np.float32)
    finite = np.isfinite(data).all(1)
    data = data[finite]
    names = (["x", "y", "z", "nx", "ny", "nz"] + [f"f_dc_{i}" for i in range(3)] + [f"f_rest_{i}" for i in range(shN.shape[1])]
             + ["opacity"] + [f"scale_{i}" for i in range(3)] + [f"rot_{i}" for i in range(4)])
    header = ("ply\nformat binary_little_endian 1.0\n" + f"element vertex {len(data)}\n"
              + "".join(f"property float {name}\n" for name in names) + "end_header\n")
    with open(path, "wb") as f:
        f.write(header.encode())
        f.write(data.tobytes())
    return {"splats": int(len(data)), "dropped_non_finite": int((~finite).sum()), "sh_rest": int(shN.shape[1])}


def camera_entries(frames):
    cameras, views = [], []
    for i, frame in enumerate(frames):
        c2w = frame.c2w.numpy().astype(float)
        fx, fy = float(frame.K[0, 0]), float(frame.K[1, 1])
        cameras.append({"id": i, "img_name": Path(frame.name).stem, "width": frame.width, "height": frame.height,
                        "position": c2w[:3, 3].tolist(), "rotation": c2w[:3, :3].tolist(), "fx": fx, "fy": fy})
        views.append({"name": Path(frame.name).stem, "fov": math.degrees(2 * math.atan(frame.height / (2 * fy))),
                      "position": c2w[:3, 3].tolist(), "forward": c2w[:3, 2].tolist(), "up": (-c2w[:3, 1]).tolist()})
    return cameras, views


def _code_commit():
    try:
        return subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    except OSError:
        return ""


def split_archive(archive, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    digest = sha256_file(archive)
    if archive.stat().st_size <= PART:
        target = out_dir / archive.name
        shutil.copy2(archive, target)
        return [target], {"archive": archive.name, "sha256": digest, "parts": []}
    parts, manifest = [], {"archive": archive.name, "sha256": digest, "parts": []}
    with open(archive, "rb") as src:
        index = 1
        while chunk := src.read(PART):
            part = out_dir / f"{archive.name}.part{index:03d}"
            part.write_bytes(chunk)
            parts.append(part)
            manifest["parts"].append({"name": part.name, "bytes": len(chunk), "sha256": sha256_file(part)})
            index += 1
    manifest_path = out_dir / f"{archive.name}.parts.json"
    write_json(manifest_path, manifest)
    return parts + [manifest_path], manifest


def run(ws, cfg):
    state = torch.load(ws.train / "final.pt", map_location="cpu", weights_only=False)
    frames, _, _ = T.load_dataset(ws, with_priors=False)
    result_id = uuid.uuid4().hex[:12]
    stage = ws.export / f"result-{result_id}"
    shutil.rmtree(ws.export, ignore_errors=True)
    (stage / "assets").mkdir(parents=True)
    ply = write_ply(state["splats"], stage / "assets" / "room.ply")
    shutil.copy2(ws.mesh / "room.glb", stage / "assets" / "room.glb")
    cameras, views = camera_entries(frames)
    write_json(stage / "cameras.json", cameras)
    write_json(stage / "assets" / "views.json", views)

    job = ws.job
    receipts = {s: (ws.receipt(s) or {}).get("metrics", {}) for s in ("frames", "sfm", "priors", "train", "mesh")}
    priors, mesh = receipts["priors"], receipts["mesh"]
    warnings = [w for m in receipts.values() for w in m.get("warnings", [])]
    write_json(stage / "namma-input.json", {"video": job.get("video_name"), "videoSha256": job.get("video_sha256"),
                                            "frames": receipts["frames"]})
    result = {
        "schemaVersion": 1, "type": "namma-planargs-result", "inputId": job.get("job_id"),
        "algorithm": {"name": "namma-gsplat-mcmc", "commit": _code_commit(),
                      "components": "gsplat (Apache-2.0), pycolmap (BSD-3), MoGe-2 (MIT), Open3D (MIT)"},
        "scale": {"calibrated": False, "estimatedMetric": bool(priors.get("metric_scale")),
                  "note": "Units are metres estimated from monocular depth; confirm with a tape measurement in the viewer."},
        "capture": {"originalFrameCount": receipts["frames"].get("decoded_frames"),
                    "inputImages": receipts["sfm"].get("total"), "registeredImages": receipts["sfm"].get("registered"),
                    "trainingSteps": receipts["train"].get("steps"), "diagnostic": False},
        "artifacts": {"splat": {"path": "assets/room.ply", "sha256": sha256_file(stage / "assets" / "room.ply")},
                      "mesh": {"path": "assets/room.glb", "sha256": sha256_file(stage / "assets" / "room.glb"),
                               "triangleCount": mesh.get("triangles"), "coordinateSpace": "raw-ply-v1"},
                      "views": {"path": "assets/views.json", "sha256": sha256_file(stage / "assets" / "views.json")}},
        "walkingSuggestion": {"up": [0.0, -1.0, 0.0], "floor": mesh.get("floor"), "startCamera": 0},
        "quality": {"validated": False, "walkingApproved": False, "evaluation": receipts["train"], "warnings": warnings},
        "meshProcessing": mesh, "training": cfg.to_dict()["train"],
        "runtime": {"created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "torch": torch.__version__},
    }
    write_json(stage / "namma-result.json", result)

    archive = ws.export / f"result-{result_id}.zip"
    with zipfile.ZipFile(archive, "x", zipfile.ZIP_DEFLATED, compresslevel=1) as zf:
        for path in sorted(stage.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(stage).as_posix())
    download = ws.export / "DOWNLOAD_THIS" / archive.stem
    files, manifest = split_archive(archive, download)
    (download / "READ_ME.txt").write_text(
        "Namma Space reconstruction\n\n"
        "Open it in the viewer (viewer/README.md in the namma-space repository): Namma Pipeline.cmd -> "
        f"'1. Import a trained result' -> select {(archive.name + '.parts.json') if manifest['parts'] else archive.name} "
        "(keep all parts in one folder).\n\n"
        f"Splats: {ply['splats']:,}  Collision triangles: {mesh.get('triangles')}\n"
        f"Held-out PSNR: {receipts['train'].get('psnr')}  SSIM: {receipts['train'].get('ssim')}\n"
        + ("Warnings:\n- " + "\n- ".join(warnings) + "\n" if warnings else ""))
    previews = sorted((ws.train / "previews").glob("*.jpg"))
    if previews:
        shutil.copy2(previews[-1], download / "preview_photo_render_depth.jpg")
    (download / "report.json").write_text(json.dumps({"stages": receipts, "ply": ply, "archive": manifest}, indent=1, default=str))
    return {"result_id": result_id, "archive_bytes": archive.stat().st_size, "parts": len(manifest["parts"]),
            "download_dir": str(download), **ply}, [download]

</file>

<file src="namma/frames.py">
"""Pick sharp, well-overlapping frames from a video (PyAV BSD-3, OpenCV Apache-2.0).

Pass 1 decodes every frame at reduced size and measures
  sharpness = sqrt(var(Laplacian) * mean(Sobel^2)), relative to its +-1 s rolling median, and
  motion    = median forward/backward-checked Lucas-Kanade flow, as a fraction of the width.
A keyframe is triggered when the accumulated motion since the last one reaches `shift` or `max_gap`
seconds pass (never before `min_gap`); the sharpest frame within +-`window` s of the trigger wins.
Pass 2 decodes again and writes only the chosen frames at full resolution.
"""
import csv
import math
from concurrent.futures import ThreadPoolExecutor

import av
import cv2
import numpy as np


def _colorspace(frame):
    cs = int(frame.colorspace)  # 1 = BT.709, 2 = unspecified
    if cs in (0, 2) or cs > 10:
        return "ITU709" if frame.height >= 720 else "ITU601"
    return cs


def _color_range(frame):
    r = int(frame.color_range)  # 1 = limited (MPEG), 2 = full (JPEG)
    return r if r in (1, 2) else 1


def _gray(frame, width):
    height = int(round(frame.height * width / frame.width / 2) * 2)
    return frame.reformat(width=width, height=height, format="gray", src_colorspace=_colorspace(frame),
                          src_color_range=_color_range(frame), dst_color_range="JPEG",
                          interpolation="AREA").to_ndarray()


def _rgb(frame):
    return frame.reformat(format="rgb24", src_colorspace=_colorspace(frame), src_color_range=_color_range(frame),
                          dst_color_range="JPEG", interpolation="BICUBIC").to_ndarray()


def _sharpness(gray):
    g = gray.astype(np.float32)
    lap = cv2.Laplacian(g, cv2.CV_32F, ksize=3).var()
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)
    return math.sqrt(max(float(lap), 1e-6) * max(float(np.mean(gx * gx + gy * gy)), 1e-6))


def _motion(prev, cur):
    pts = cv2.goodFeaturesToTrack(prev, maxCorners=500, qualityLevel=0.01, minDistance=7)
    if pts is None or len(pts) < 20:
        return float("nan")
    nxt, st, _ = cv2.calcOpticalFlowPyrLK(prev, cur, pts, None, winSize=(21, 21), maxLevel=4)
    back, st2, _ = cv2.calcOpticalFlowPyrLK(cur, prev, nxt, None, winSize=(21, 21), maxLevel=4)
    ok = (st[:, 0] == 1) & (st2[:, 0] == 1) & (np.linalg.norm((back - pts)[:, 0], axis=1) < 1.0)
    if ok.sum() < 20:
        return float("nan")
    return float(np.median(np.linalg.norm((nxt - pts)[ok, 0], axis=1))) / prev.shape[1]


def _in_range(t, cfg):
    return t >= cfg.start_s and (cfg.end_s <= 0 or t <= cfg.end_s)


def analyse(video, cfg, progress=None):
    rows, prev = [], None
    with av.open(str(video)) as container:
        stream = container.streams.video[0]
        stream.thread_type = "AUTO"
        fps = float(stream.average_rate or stream.guessed_rate or 30)
        total = stream.frames or 0
        for i, frame in enumerate(container.decode(stream)):
            t = float(frame.pts * stream.time_base) if frame.pts is not None else i / fps
            if cfg.end_s > 0 and t > cfg.end_s:
                break
            if not _in_range(t, cfg):
                continue
            gray = _gray(frame, min(cfg.sharp_width, frame.width))
            small = cv2.resize(gray, (cfg.flow_width, int(round(gray.shape[0] * cfg.flow_width / gray.shape[1]))),
                               interpolation=cv2.INTER_AREA)
            rows.append({"idx": i, "t": t, "sharp": _sharpness(gray),
                         "motion": 0.0 if prev is None else _motion(prev, small), "luma": float(small.mean())})
            prev = small
            if progress and i % 300 == 0:
                progress(i, total)
    return rows, fps


def select(rows, fps, cfg, min_gap):
    n = len(rows)
    sharp = np.array([r["sharp"] for r in rows])
    half = max(1, int(fps))
    rolling = np.array([np.median(sharp[max(0, i - half): i + half + 1]) for i in range(n)])
    rel = sharp / np.maximum(rolling, 1e-9)
    motion = np.array([r["motion"] for r in rows])
    motion = np.where(np.isnan(motion), cfg.shift, motion)  # lost tracking forces a keyframe
    cum = np.cumsum(motion)
    t = np.array([r["t"] for r in rows])
    w = max(1, int(round(cfg.window * fps)))
    first = int(np.argmax(rel[: max(1, int(fps * 0.5))]))
    chosen, last = [first], first
    while True:
        k = last + 1
        while k < n and not (t[k] - t[last] >= min_gap and (cum[k] - cum[last] >= cfg.shift or t[k] - t[last] >= cfg.max_gap)):
            k += 1
        if k >= n:
            break
        candidates = [j for j in range(max(last + 1, k - w), min(n, k + w + 1)) if t[j] - t[last] >= min_gap] or [k]
        good = [j for j in candidates if rel[j] >= cfg.min_rel_sharp]
        last = max(good or candidates, key=lambda j: rel[j])
        chosen.append(last)
    for i, r in enumerate(rows):
        r["rel_sharp"] = float(rel[i])
    return chosen, cum


def export(video, wanted, out_dir, quality):
    out_dir.mkdir(parents=True, exist_ok=True)
    wanted = set(wanted)
    params = [cv2.IMWRITE_JPEG_QUALITY, quality]
    with ThreadPoolExecutor(max_workers=8) as pool, av.open(str(video)) as container:
        stream = container.streams.video[0]
        stream.thread_type = "AUTO"
        futures = []
        for i, frame in enumerate(container.decode(stream)):
            if i in wanted:
                path = out_dir / f"frame_{i:06d}.jpg"
                futures.append(pool.submit(cv2.imwrite, str(path), cv2.cvtColor(_rgb(frame), cv2.COLOR_RGB2BGR), params))
            if i >= max(wanted):
                break
        ok = all(f.result() for f in futures)
    if not ok:
        raise RuntimeError("Writing selected frames failed")


def run(ws, cfg, video):
    fc = cfg.frames
    ws.status(stage="frames", message="Measuring sharpness and motion of every frame")
    rows, fps = analyse(video, fc, lambda i, n: ws.status(progress=i / n if n else None))
    if len(rows) < 10:
        raise RuntimeError(f"Only {len(rows)} frames decoded from {video}")
    min_gap = fc.min_gap
    chosen, cum = select(rows, fps, fc, min_gap)
    while len(chosen) > fc.max_frames:
        min_gap *= 1.25
        chosen, cum = select(rows, fps, fc, min_gap)
    images = ws.frames / "images"
    for old in images.glob("*.jpg"):
        old.unlink()
    ws.status(message=f"Writing {len(chosen)} full-resolution frames", progress=None)
    export(video, [rows[j]["idx"] for j in chosen], images, fc.jpeg_quality)
    selected = set(chosen)
    with open(ws.frames / "frame_metrics.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) + ["selected"])
        writer.writeheader()
        for j, r in enumerate(rows):
            writer.writerow({**r, "selected": int(j in selected)})
    gaps = np.diff(cum[chosen]) if len(chosen) > 1 else np.array([0.0])
    duration = rows[-1]["t"] - rows[0]["t"]
    return {"decoded_frames": len(rows), "video_fps": fps, "selected": len(chosen),
            "selected_per_second": round(len(chosen) / duration, 3) if duration else None, "min_gap_used": min_gap,
            "median_shift": float(np.median(gaps)), "gaps_over_2_5x_shift": int((gaps > 2.5 * fc.shift).sum()),
            "median_rel_sharpness": float(np.median([rows[j]["rel_sharp"] for j in chosen]))}

</file>

<file src="namma/gpu_check.py">
"""Real GPU checks for the Namma Space environment (gsplat, MoGe-2, pycolmap, Open3D).

Every check runs in its own subprocess (a CUDA fault in one cannot hide or
poison the others), executes a small real CUDA operation, and records the
imported binary paths, timings and numeric evidence. Import-only is never
treated as a pass for a native module.

Run from the repository root with the training venv:
    .venv/bin/python -m namma check --out setup-logs/<run>
"""
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Every check is required: setup passes only when all of them pass.
CHECKS = ("environment", "torch_cuda", "gsplat", "pipeline_imports", "open3d_tsdf")


class CheckFailed(AssertionError):
    """A failed check that still carries the evidence it collected."""

    def __init__(self, message, details):
        super().__init__(message)
        self.details = details


def _module_file(name):
    module = sys.modules.get(name)
    return getattr(module, "__file__", None) if module else None


def _command(args):
    try:
        out = subprocess.run(args, capture_output=True, text=True, timeout=60)
        return (out.stdout + out.stderr).strip()
    except (OSError, subprocess.TimeoutExpired) as error:
        return f"unavailable: {error}"


def _assert_outside_source(path, label):
    """Native binaries must come from this venv's build, not stale files in the source tree."""
    if path is None:
        raise AssertionError(f"{label}: no binary path")
    resolved = Path(path).resolve()
    source = os.environ.get("NAMMA_GSPLAT_SRC")
    if source and Path(source).resolve() in resolved.parents:
        raise AssertionError(f"{label} imported from the source tree ({resolved}), not the built venv package")
    return str(resolved)


def check_environment():
    import importlib.metadata as md
    import torch

    details = {
        "python": sys.version.split()[0],
        "executable": sys.executable,
        "platform": platform.platform(),
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda,
        "cudnn": torch.backends.cudnn.version(),
        "torch_arch_list": torch.cuda.get_arch_list(),
        "cuda_available": torch.cuda.is_available(),
        "env": {k: os.environ.get(k) for k in ("CUDA_HOME", "TORCH_CUDA_ARCH_LIST", "NVCC_FLAGS",
                                               "NVCC_PREPEND_FLAGS", "MAX_JOBS")},
        "nvidia_smi": _command(["nvidia-smi", "--query-gpu=name,driver_version,memory.total,compute_cap",
                                "--format=csv,noheader"]),
        "gcc": (_command(["gcc", "--version"]) or "no output").splitlines()[0],
        "repo_commit": _command(["git", "-C", str(REPO), "rev-parse", "HEAD"]),
        "repo_dirty": bool(_command(["git", "-C", str(REPO), "status", "--porcelain", "--untracked-files=no"])),
        "gsplat_source": os.environ.get("NAMMA_GSPLAT_SRC"),
        "packages": {},
    }
    for name in ("torch", "torchvision", "numpy", "scipy", "open3d", "opencv-python", "huggingface-hub",
                 "pycolmap", "cuda-toolkit", "nvidia-cuda-nvcc", "gsplat", "moge", "utils3d_moge", "av",
                 "trimesh", "jaxtyping"):
        try:
            details["packages"][name] = md.version(name)
        except md.PackageNotFoundError:
            details["packages"][name] = None

    cuda_home = os.environ.get("CUDA_HOME")
    nvcc = shutil.which("nvcc") or (cuda_home and str(Path(cuda_home) / "bin" / "nvcc"))
    details["nvcc_path"] = nvcc
    details["nvcc"] = _command([nvcc, "--version"]) if nvcc else "missing"
    match = re.search(r"release (\d+\.\d+)", details["nvcc"])
    details["nvcc_release"] = match.group(1) if match else None

    problems = []
    if torch.cuda.is_available():
        capability = torch.cuda.get_device_capability()
        details["device"] = torch.cuda.get_device_name()
        details["compute_capability"] = f"{capability[0]}.{capability[1]}"
        free, total = torch.cuda.mem_get_info()
        details["vram_gib"] = {"free": round(free / 2**30, 2), "total": round(total / 2**30, 2)}
        if f"sm_{capability[0]}{capability[1]}" not in details["torch_arch_list"]:
            problems.append(f"Torch build lacks kernels for sm_{capability[0]}{capability[1]}")
    else:
        problems.append("PyTorch cannot use CUDA (driver too old for this Torch CUDA build, or no GPU)")
    if details["nvcc_release"] != torch.version.cuda:
        problems.append(f"nvcc {details['nvcc_release']} does not match Torch CUDA {torch.version.cuda}")
    if problems:
        raise CheckFailed("; ".join(problems), details)
    return details


def check_torch_cuda():
    import torch
    torch.manual_seed(0)
    layer = torch.nn.Linear(64, 64).cuda()
    x = torch.randn(128, 64, device="cuda")
    loss = layer(x).square().mean()
    loss.backward()
    torch.cuda.synchronize()
    expected = (x @ layer.weight.T + layer.bias).square().mean()
    assert torch.isfinite(layer.weight.grad).all() and layer.weight.grad.abs().sum() > 0
    assert torch.allclose(loss, expected, rtol=1e-4), "matmul result mismatch"
    return {"loss": loss.item(), "grad_norm": layer.weight.grad.norm().item()}


def check_gsplat():
    """Render + backward with gsplat, the patched MCMC relocation kernel, and depth_to_normal."""
    import importlib.util
    import math
    import gsplat
    import torch
    from gsplat.relocation import compute_relocation
    from gsplat.rendering import rasterization
    from gsplat.utils import depth_to_normal

    spec = importlib.util.find_spec("gsplat.csrc")
    binary = _assert_outside_source(spec.origin, "gsplat") if spec and spec.origin else gsplat.__file__
    torch.manual_seed(0)
    device = "cuda"
    n, width, height = 4000, 160, 120
    means = torch.empty(n, 3, device=device).uniform_(-1, 1)
    means[:, 2] = means[:, 2].abs() * 1.5 + 2.5
    params = {
        "means": means.requires_grad_(),
        "scales": torch.full((n, 3), math.log(0.03), device=device).requires_grad_(),
        "quats": torch.nn.functional.normalize(torch.randn(n, 4, device=device), dim=-1).requires_grad_(),
        "opacities": torch.full((n,), 1.0, device=device).requires_grad_(),
        "colors": (torch.randn(n, 16, 3, device=device) * 0.2).requires_grad_(),
    }
    K = torch.tensor([[150.0, 0, width / 2], [0, 150.0, height / 2], [0, 0, 1]], device=device)
    renders, alphas, info = rasterization(params["means"], params["quats"], torch.exp(params["scales"]),
                                          torch.sigmoid(params["opacities"]), params["colors"],
                                          torch.eye(4, device=device)[None], K[None], width, height, sh_degree=3,
                                          render_mode="RGB+ED", packed=False)
    assert renders.shape == (1, height, width, 4) and torch.isfinite(renders).all(), "non-finite render"
    coverage = float((alphas > 0.5).float().mean())
    assert coverage > 0.1, f"only {coverage:.0%} of pixels covered"
    (renders[..., :3].mean() + 0.1 * renders[..., 3].mean()).backward()
    grads = {}
    for name, p in params.items():
        assert p.grad is not None and torch.isfinite(p.grad).all(), f"bad gradient for {name}"
        grads[name] = float(p.grad.norm())
        assert grads[name] > 0, f"zero gradient for {name}"
    normals = depth_to_normal(renders[..., 3:4].detach(), torch.eye(4, device=device)[None], K[None])
    assert torch.isfinite(normals).all(), "non-finite normals"

    n_max = 51  # every MCMC split ratio, including the sm_120 fast-math sign case (upstream PR #1060)
    binoms = torch.zeros(n_max, n_max, device=device)
    for i in range(n_max):
        for k in range(i + 1):
            binoms[i, k] = math.comb(i, k)
    opac = torch.linspace(0.05, 0.95, n_max, device=device)
    scales = torch.linspace(0.1, 1.6, n_max * 3, device=device).reshape(n_max, 3)
    ratios = torch.arange(1, n_max + 1, device=device, dtype=torch.int32)
    import inspect
    accepted = inspect.signature(compute_relocation).parameters
    inputs = {"opacities": opac, "scales": scales, "ratios": ratios, "binoms": binoms}
    new_opac, new_scales = compute_relocation(**{k: v for k, v in inputs.items() if k in accepted})
    assert torch.isfinite(new_opac).all() and torch.isfinite(new_scales).all(), "relocation produced NaN"
    assert (new_scales > 0).all() and ((new_opac > 0) & (new_opac <= 1)).all(), "relocation out of range"
    return {"binary": binary, "version": gsplat.__version__, "coverage": coverage, "grad_norms": grads,
            "relocation_min_scale_ratio": float((new_scales / scales).min())}


def check_pipeline_imports():
    """Everything the video pipeline imports, with licence-relevant facts."""
    import av
    import moge.model.v2  # noqa: F401  (MoGe-2; weights download on first use)
    import pycolmap
    import trimesh  # noqa: F401
    for module in ("frames", "sfm", "priors", "trainer", "mesh", "export", "backup", "pipeline"):
        __import__(f"namma.{module}")
    has_cuda = bool(getattr(pycolmap, "has_cuda", False))
    assert not has_cuda, "pycolmap was built with CUDA: its GPU SIFT (SiftGPU) is not licensed for commercial use"
    return {"pycolmap": pycolmap.__version__, "pycolmap_cuda": has_cuda, "av": av.__version__,
            "moge": _module_file("moge")}


def check_open3d_tsdf():
    """Synthetic plane fusion; Open3D 0.20 produced zero vertices for this case on Molab."""
    import numpy as np
    import open3d as o3d
    depth = np.ascontiguousarray(np.full((128, 128), 2.0, dtype=np.float32))
    color = np.ascontiguousarray(np.full((128, 128, 3), 128, dtype=np.uint8))
    rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
        o3d.geometry.Image(color), o3d.geometry.Image(depth), depth_scale=1.0, depth_trunc=10.0,
        convert_rgb_to_intensity=False)
    volume = o3d.pipelines.integration.ScalableTSDFVolume(
        voxel_length=0.04, sdf_trunc=0.16, color_type=o3d.pipelines.integration.TSDFVolumeColorType.RGB8)
    intrinsic = o3d.camera.PinholeCameraIntrinsic(128, 128, 100, 100, 63.5, 63.5)
    for _ in range(3):
        volume.integrate(rgbd, intrinsic, np.eye(4))
    mesh = volume.extract_triangle_mesh()
    vertices, triangles = len(mesh.vertices), len(mesh.triangles)
    assert vertices > 0 and triangles > 0, "synthetic TSDF produced an empty mesh"
    return {"open3d": o3d.__version__, "vertices": vertices, "triangles": triangles}


def run_one(name):
    os.chdir(REPO)
    sys.path.insert(0, str(REPO))
    started = time.perf_counter()
    record = {"name": name, "required": True}
    try:
        record["details"] = globals()["check_" + name]()
        record["status"] = "pass"
    except BaseException as error:  # report every failure, including import errors
        record["status"] = "fail"
        record["details"] = getattr(error, "details", None)
        record["error"] = f"{type(error).__name__}: {error}"
        record["traceback"] = traceback.format_exc()[-4000:]
    record["seconds"] = round(time.perf_counter() - started, 3)
    print("NAMMA_CHECK_RESULT " + json.dumps(record, default=str), flush=True)


def run_all(out_dir, only=None):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    names = [n for n in CHECKS if not only or n in only]
    results = []
    for name in names:
        started = time.perf_counter()
        process = subprocess.run([sys.executable, "-m", "namma.gpu_check", name], cwd=REPO,
                                 capture_output=True, text=True, timeout=900)
        (out / f"check-{name}.log").write_text(process.stdout + process.stderr, encoding="utf-8")
        lines = [l for l in process.stdout.splitlines() if l.startswith("NAMMA_CHECK_RESULT ")]
        if lines:
            record = json.loads(lines[-1][len("NAMMA_CHECK_RESULT "):])
        else:  # crashed before reporting (segfault, abort)
            record = {"name": name, "required": True, "status": "fail",
                      "error": f"process exited {process.returncode} without a result; see check-{name}.log",
                      "seconds": round(time.perf_counter() - started, 3)}
        results.append(record)
        mark = "PASS" if record["status"] == "pass" else ("FAIL" if record["required"] else "optional-fail")
        print(f"{mark:>13}  {name:<14} {record['seconds']:>8.2f}s  {record.get('error', '')}", flush=True)

    failed = [r["name"] for r in results if r["status"] != "pass" and r["required"]]
    report = {"overall": "fail" if failed else "pass", "failed_required": failed,
              "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "checks": results}
    (out / "report.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    (out / "report.md").write_text(_markdown(report), encoding="utf-8")
    print(f"Overall: {report['overall'].upper()}  report: {out / 'report.md'}", flush=True)
    return 1 if failed else 0


def _markdown(report):
    lines = [f"# Namma Space environment check: {report['overall'].upper()}", "",
             f"Generated {report['generated_utc']}. Each check runs in its own process; a native-module pass "
             "means a real CUDA operation (and backward where relevant) ran and matched a reference.", "",
             "| Check | Required | Result | Seconds | Binary / error |", "|---|---|---|---|---|"]
    for r in report["checks"]:
        detail = r.get("error") or (r.get("details") or {}).get("binary", "")
        lines.append(f"| {r['name']} | {'yes' if r['required'] else 'no'} | {r['status']} | {r['seconds']} | {detail} |")
    env = next((r.get("details") for r in report["checks"] if r["name"] == "environment"), None)
    if env:
        lines += ["", "## Environment", "", "```json", json.dumps(env, indent=2, default=str), "```"]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    run_one(sys.argv[1])

</file>

<file src="namma/mesh.py">
"""Collision mesh: TSDF fusion of depth rendered from the trained splats (Open3D 0.19, MIT).

The mesh is built in exactly the splat's coordinate frame (no transform), cleaned of small floating
pieces, decimated to the viewer's triangle budget and written as GLB (trimesh, MIT).
"""
import numpy as np
import open3d as o3d
import torch
import trimesh

from namma import trainer as T
from namma.workspace import read_json


def load_splats(ws, device="cuda"):
    state = torch.load(ws.train / "final.pt", map_location="cpu", weights_only=False)
    return {k: v.to(device) for k, v in state["splats"].items()}, state["sh_degree"]


def scaled(frame, long_side):
    s = min(1.0, long_side / max(frame.width, frame.height))
    K = frame.K.clone()
    K[:2] *= s
    return T.Frame(frame.name, K, frame.c2w, max(1, round(frame.width * s)), max(1, round(frame.height * s)), frame.image)


def run(ws, cfg, device="cuda"):
    mc = cfg.mesh
    splats, sh_degree = load_splats(ws, device)
    frames, _, _ = T.load_dataset(ws, with_priors=False)
    metric = bool((ws.receipt("priors") or {}).get("metrics", {}).get("metric_scale"))
    # Without metric priors the scene unit is arbitrary: size the voxel from the camera spread instead.
    voxel = mc.voxel if metric else T.scene_scale(frames) / 300
    max_depth = mc.max_depth if metric else T.scene_scale(frames) * 4
    volume = o3d.pipelines.integration.ScalableTSDFVolume(
        voxel_length=voxel, sdf_trunc=voxel * mc.trunc_voxels, color_type=o3d.pipelines.integration.TSDFVolumeColorType.RGB8)
    picks = np.unique(np.linspace(0, len(frames) - 1, min(mc.max_views, len(frames))).round().astype(int))
    # Depth range from what the model actually renders, not from assumptions about the scene.
    sample = []
    with torch.no_grad():
        for i in picks[:: max(1, len(picks) // 12)]:
            renders, alphas, _ = T.render(splats, scaled(frames[i], mc.render_long_side), sh_degree, device)
            covered = alphas[0, ..., 0] > mc.min_alpha
            sample.append((float(covered.float().mean()), renders[0, ..., 3][covered].float().cpu().numpy()))
    coverage = float(np.mean([c for c, _ in sample]))
    depths = np.concatenate([d for _, d in sample]) if sample else np.zeros(0)
    if coverage < 0.05 or depths.size == 0:
        raise RuntimeError(f"Rendered views are almost empty (coverage {coverage:.1%}); the trained model is unusable")
    max_depth = min(max_depth, float(np.percentile(depths, 99)) * 1.5)
    with torch.no_grad():
        for k, i in enumerate(picks):
            ws.status(stage="mesh", message=f"Fusing rendered depth {k + 1}/{len(picks)}", progress=k / len(picks))
            frame = scaled(frames[i], mc.render_long_side)
            renders, alphas, _ = T.render(splats, frame, sh_degree, device)
            rgb = np.ascontiguousarray((renders[0, ..., :3].clamp(0, 1) * 255).byte().cpu().numpy())
            depth = renders[0, ..., 3].float().cpu().numpy()
            depth[(alphas[0, ..., 0].cpu().numpy() < mc.min_alpha) | ~np.isfinite(depth) | (depth > max_depth)] = 0
            rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
                o3d.geometry.Image(rgb), o3d.geometry.Image(np.ascontiguousarray(depth, dtype=np.float32)),
                depth_scale=1.0, depth_trunc=max_depth, convert_rgb_to_intensity=False)
            K = frame.K.numpy().astype(np.float64)
            intrinsic = o3d.camera.PinholeCameraIntrinsic(frame.width, frame.height, K[0, 0], K[1, 1], K[0, 2], K[1, 2])
            volume.integrate(rgbd, intrinsic, np.linalg.inv(frame.c2w.numpy().astype(np.float64)))
    ws.status(message="Extracting and cleaning the mesh", progress=None)
    mesh = volume.extract_triangle_mesh()
    raw_triangles = len(mesh.triangles)
    if raw_triangles == 0:
        raise RuntimeError("TSDF fusion produced an empty mesh (check rendered depth / Open3D version)")
    mesh.remove_degenerate_triangles()
    mesh.remove_duplicated_triangles()
    mesh.remove_duplicated_vertices()
    clusters, counts, _ = mesh.cluster_connected_triangles()
    clusters, counts = np.asarray(clusters), np.asarray(counts)
    keep = counts >= max(100, mc.min_component_fraction * counts.sum())
    mesh.remove_triangles_by_mask(~keep[clusters])
    mesh.remove_unreferenced_vertices()
    if len(mesh.triangles) > mc.target_triangles:
        mesh = mesh.simplify_quadric_decimation(mc.target_triangles)
        mesh.remove_degenerate_triangles()
        mesh.remove_unreferenced_vertices()
    vertices = np.asarray(mesh.vertices, dtype=np.float32)
    faces = np.asarray(mesh.triangles, dtype=np.uint32)
    colors = (np.asarray(mesh.vertex_colors) * 255).astype(np.uint8) if mesh.has_vertex_colors() else None
    glb = ws.mesh / "room.glb"
    trimesh.Trimesh(vertices, faces, vertex_colors=colors, process=False).export(glb, file_type="glb")
    floor = estimate_floor(vertices, faces)
    return {"voxel": voxel, "metric": metric, "views": len(picks), "raw_triangles": raw_triangles,
            "triangles": len(faces), "vertices": len(vertices), "components_kept": int(keep.sum()),
            "components_dropped": int((~keep).sum()), "floor": floor,
            "bounds_min": vertices.min(0).tolist(), "bounds_max": vertices.max(0).tolist()}, [glb]


def estimate_floor(vertices, faces):
    """Lowest large horizontal surface (world up is -Y after namma.sfm.level_and_center)."""
    tri = vertices[faces]
    normals = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    area = np.linalg.norm(normals, axis=1)
    up = np.abs(normals[:, 1]) > 0.9 * np.maximum(area, 1e-12)
    if area[up].sum() <= 0:
        return None
    heights = tri[up].mean(1)[:, 1]  # larger y = lower (y points down)
    hist, edges = np.histogram(heights, bins=100, weights=area[up])
    lowest_big = [i for i in range(len(hist)) if hist[i] > 0.05 * hist.sum()]
    if not lowest_big:
        return None
    i = max(lowest_big)
    return {"y": float((edges[i] + edges[i + 1]) / 2), "up": [0.0, -1.0, 0.0],
            "area_fraction": float(hist[i] / hist.sum())}

</file>

<file src="namma/pipeline.py">
"""Video -> frames -> camera poses -> depth/normal priors -> splat training -> collision mesh -> DOWNLOAD_THIS.

Every stage writes a receipt when it finishes; a rerun skips stages whose receipt matches the current
settings and whose outputs exist, and training resumes from its newest checkpoint. Finished stages
and checkpoints are queued for the Drive uploader (namma.backup).
"""
import re
import shutil
import time
import traceback
from pathlib import Path

from namma import backup
from namma.config import Config, smoke_config
from namma.workspace import STAGES, Workspace, sha256_file, write_json

SECTIONS = {"frames": ("frames",), "sfm": ("frames", "sfm"), "priors": ("frames", "sfm", "priors"),
            "train": ("frames", "sfm", "priors", "train"), "mesh": ("frames", "sfm", "priors", "train", "mesh"),
            "export": ("frames", "sfm", "priors", "train", "mesh")}


def create_job(job_dir, job_id, video, sha256, name, smoke=False, overrides=None):
    ws = Workspace(job_dir)
    if not (ws.root / "job.json").exists():
        settings = (smoke_config() if smoke else Config()).to_dict()
        for section, values in (overrides or {}).items():
            settings[section].update(values)
        write_json(ws.root / "job.json", {"job_id": job_id, "video_name": name, "video_path": str(video),
                                          "video_sha256": sha256, "smoke": smoke, "created": time.time(),
                                          "config": Config.from_dict(settings).to_dict()})
    return ws


def prepare(video, jobs_root, overrides=None):
    """Move a fetched video into its job folder (named after its content) and create the job plus a smoke test."""
    video = Path(video)
    sha256 = sha256_file(video)
    stem = re.sub(r"[^A-Za-z0-9]+", "-", video.stem).strip("-")[:40] or "video"
    job_id = f"{stem}-{sha256[:10]}"
    main = Workspace(Path(jobs_root) / job_id)
    target = main.input / ("video" + video.suffix.lower())
    ours = (Path(jobs_root) / "_incoming").resolve() in video.resolve().parents  # a copy fetched from Drive
    if video.resolve() != target.resolve():
        if target.exists() and target.stat().st_size == video.stat().st_size:
            if ours:
                video.unlink()
        elif ours:
            video.replace(target)
        else:  # never move or delete a user's own file
            shutil.copy2(video, target)
    create_job(main.root, job_id, target, sha256, video.name, overrides=overrides)
    smoke = create_job(Path(jobs_root) / f"{job_id}-smoke", f"{job_id}-smoke", target, sha256, video.name, smoke=True)
    return {"job_id": job_id, "job": str(main.root), "smoke_job": str(smoke.root), "video": str(target)}


def _stage(ws, cfg, name, repair=False):
    from namma import export, frames, mesh, priors, sfm, trainer
    if name == "frames":
        return frames.run(ws, cfg, ws.job["video_path"]), [ws.frames / "images", ws.frames / "frame_metrics.csv"]
    if name == "sfm":
        return sfm.run(ws, cfg), [ws.sfm / "sparse", ws.sfm / "undistorted" / "sparse", ws.sfm / "undistorted" / "images"]
    if name == "priors":
        return priors.run(ws, cfg, repair=repair), [ws.dataset / "sparse", ws.dataset / "images", ws.priors]
    if name == "train":
        def on_checkpoint(path, step):
            _safe_commit(ws, "checkpoint", files=[path], meta={"step": step, "settings": cfg.stage_hash("frames", "sfm", "priors", "train")})
        return trainer.run(ws, cfg, on_checkpoint=on_checkpoint)
    if name == "mesh":
        return mesh.run(ws, cfg)
    if name == "export":
        return export.run(ws, cfg)
    raise KeyError(name)


def _safe_commit(ws, stage, **kwargs):
    """A failed backup must not fail a finished stage; the work is still on local disk."""
    try:
        backup.commit(ws, stage, **kwargs)
    except Exception as error:
        ws.log(f"WARNING could not queue {stage} for Drive backup: {type(error).__name__}: {error}")


def run(job_dir, until=None):
    ws = Workspace(job_dir)
    job = ws.job
    if not job:
        raise RuntimeError(f"{job_dir} has no job.json; create the job first")
    cfg = Config.from_dict(job["config"])
    ws.status(state="running", started=time.time(), error=None)
    ws.log(f"Job {job['job_id']} ({'smoke test' if job.get('smoke') else 'full run'})")
    try:
        for name in STAGES:
            settings = cfg.stage_hash(*SECTIONS[name])
            if ws.is_done(name, settings):
                ws.log(f"{name}: already done, skipping")
                continue
            # Priors can be rebuilt from a restored scale file without changing the reconstruction, so
            # later stages stay valid; any other re-run makes them stale.
            repair = name == "priors" and (ws.receipt(name) or {}).get("settings") == settings
            if not repair:
                ws.invalidate_from(name)
            started = time.time()
            ws.status(stage=name, message="starting", progress=None)
            ws.log(f"{name}: starting")
            result = _stage(ws, cfg, name, repair)
            metrics, outputs = result if isinstance(result, tuple) else (result, [])
            ws.finish(name, settings, outputs, metrics, started)
            _safe_commit(ws, name, files=[p for p in outputs if Path(p).is_file()] if name == "train" else (),
                         tar_paths=backup.STAGE_FILES.get(name, ()))
            if name == "export":  # the result as plain files, downloadable straight from Drive
                _safe_commit(ws, "download", files=sorted(p for p in (ws.export / "DOWNLOAD_THIS").rglob("*") if p.is_file()))
            ws.log(f"{name}: done in {time.time() - started:.0f} s")
            if name == until:
                break
        ws.status(state="finished" if until in (None, "export") else "paused", stage=None, message="done", progress=1.0)
        return 0
    except Exception as error:
        ws.log("FAILED: " + "".join(traceback.format_exception(error))[-4000:])
        ws.status(state="failed", error=f"{type(error).__name__}: {error}", traceback=traceback.format_exc()[-6000:])
        return 1

</file>

<file src="namma/priors.py">
"""Per-frame metric depth and normals from MoGe-2 (Microsoft, MIT code and weights), aligned to COLMAP.

For every training frame the MoGe depth is compared with the depth of the frame's triangulated SfM points;
a robust per-frame log-scale fit gives s_i (COLMAP units per metre). Their median makes the whole scene
metric: the reconstruction is scaled by 1/median, so later stages work in metres (estimated, not
tape-measured). Each frame's depth prior is corrected by s_i / median so priors agree with the model.
If MoGe is unavailable the stage still writes the dataset, without priors or metric scale.
"""
import math
import shutil

import cv2
import numpy as np
import pycolmap

from namma.sfm import cam_from_world
from namma.workspace import read_json, write_json


def _observed_depths(rec, image, point_ids):
    pose = cam_from_world(image)
    R, t = np.asarray(pose.rotation.matrix()), np.asarray(pose.translation)
    uv, z, w = [], [], []
    for p2d in image.points2D:
        pid = p2d.point3D_id
        if pid not in point_ids:
            continue
        point = rec.points3D[pid]
        if point.track.length() < 3 or point.error > 1.5:
            continue
        depth = (R @ point.xyz + t)[2]
        if depth > 0:
            uv.append(p2d.xy)
            z.append(depth)
            w.append(point.track.length() / (1.0 + point.error))
    return np.array(uv).reshape(-1, 2), np.array(z), np.array(w)


def robust_log_scale(z_sfm, d_prior, weights, inlier=0.07):
    """Weighted mode of log(z_sfm / d_prior), refined on inliers (scale only: metric priors)."""
    r = np.log(z_sfm) - np.log(d_prior)
    best, best_score = None, -1.0
    for c in r[:: max(1, len(r) // 200)]:
        score = weights[np.abs(r - c) < inlier].sum()
        if score > best_score:
            best, best_score = c, score
    inliers = np.abs(r - best) < 2 * inlier
    estimate = float(np.average(r[inliers], weights=weights[inliers]))
    return estimate, int(inliers.sum()), float(inliers.mean())


def _load_moge(name, log):
    try:
        import torch
        from moge.model.v2 import MoGeModel
        return MoGeModel.from_pretrained(name).to("cuda").eval(), torch
    except Exception as error:
        log(f"WARNING MoGe unavailable ({type(error).__name__}: {error}); training without depth/normal priors")
        return None, None


def run(ws, cfg, repair=False):
    """Normal mode builds dataset/ from the frames undistorted at priors.image_long_side. Repair mode (after a Drive restore brought back
    dataset/sparse and dataset/priors_scales.json) only recomputes the MoGe maps with the stored scales."""
    pc = cfg.priors
    src = _undistort(ws, pc.image_long_side)
    scales_path = ws.dataset / "priors_scales.json"
    stored = read_json(scales_path) if repair and (ws.dataset / "sparse").exists() else None
    rec = pycolmap.Reconstruction(src / "sparse")
    names = sorted(img.name for img in rec.images.values() if img.has_pose)
    out_images = ws.dataset / "images"
    if stored is None:
        shutil.rmtree(ws.dataset, ignore_errors=True)
    shutil.rmtree(out_images, ignore_errors=True)
    out_images.mkdir(parents=True)
    for name in names:
        shutil.copy2(src / "images" / name, out_images / name)
    shutil.rmtree(ws.priors, ignore_errors=True)
    ws.priors.mkdir()
    if stored is not None:
        ws.log("priors: repair mode, reusing the stored metric scale and per-frame corrections")
        if stored.get("log_k") is None:  # first session had no priors: nothing to recompute
            return {**stored.get("metrics", {}), "priors": False, "metric_scale": False, "repaired": True}

    model, torch = _load_moge(cfg.priors.model, ws.log) if cfg.priors.enabled else (None, None)
    if model is None:
        if stored is None:
            rec.write(_sparse_dir(ws))
            write_json(scales_path, {"log_k": None, "scales": {}})
        return {"priors": False, "metric_scale": False, "frames": len(names),
                "warnings": ["No depth/normal priors: geometry is learned from photos only and the scale is arbitrary."]}

    point_ids = set(rec.points3D.keys())
    by_name = {img.name: img for img in rec.images.values()}
    scales, rows = {}, []
    for k, name in enumerate(names):
        ws.status(stage="priors", message=f"MoGe-2 depth/normals {k + 1}/{len(names)}", progress=k / len(names))
        image = by_name[name]
        camera = rec.cameras[image.camera_id]
        rgb = cv2.cvtColor(cv2.imread(str(out_images / name)), cv2.COLOR_BGR2RGB)
        s = min(1.0, pc.prior_long_side / max(rgb.shape[:2]))  # maps are stored smaller; training upsamples them
        if s < 1.0:
            rgb = cv2.resize(rgb, (round(rgb.shape[1] * s), round(rgb.shape[0] * s)), interpolation=cv2.INTER_AREA)
        H, W = rgb.shape[:2]
        fx, fy, cx, cy = camera.params[:4] if camera.model_name == "PINHOLE" else (camera.params[0],) * 2 + tuple(camera.params[1:3])
        fx, fy, cx, cy = fx * W / camera.width, fy * H / camera.height, cx * W / camera.width, cy * H / camera.height
        with torch.no_grad():
            out = model.infer(torch.from_numpy(rgb).cuda().permute(2, 0, 1).float() / 255,
                              fov_x=math.degrees(2 * math.atan(W / (2 * fx))), resolution_level=cfg.priors.resolution_level)
        depth = out["depth"].float().cpu().numpy()
        mask = out["mask"].cpu().numpy().astype(bool) & np.isfinite(depth) & (depth > 0)
        normal = out["normal"].float().cpu().numpy() if "normal" in out else None
        if normal is not None:
            # Orient normals towards the camera (OpenCV camera frame: x right, y down, z forward).
            u, v = np.meshgrid(np.arange(W) + 0.5, np.arange(H) + 0.5)
            rays = np.stack([(u - cx) / fx, (v - cy) / fy, np.ones_like(u)], -1)
            normal = np.where((np.sum(normal * rays, -1) > 0)[..., None], -normal, normal)
            normal /= np.maximum(np.linalg.norm(normal, axis=-1, keepdims=True), 1e-6)
            mask &= np.isfinite(normal).all(-1)

        uv, z, w = _observed_depths(rec, image, point_ids)
        uv = uv * [W / camera.width, H / camera.height]
        ui =np.clip(uv[:, 0].astype(int), 0, W - 1) if len(uv) else np.zeros(0, int)
        vi = np.clip(uv[:, 1].astype(int), 0, H - 1) if len(uv) else np.zeros(0, int)
        ok = mask[vi, ui] if len(uv) else np.zeros(0, bool)
        row = {"name": name, "points": int(ok.sum())}
        if ok.sum() >= cfg.priors.min_points:
            log_s, n_in, frac = robust_log_scale(z[ok], depth[vi[ok], ui[ok]], w[ok])
            if n_in >= cfg.priors.min_points and frac >= 0.5:
                scales[name] = log_s
            row.update(log_scale=log_s, inliers=n_in, inlier_fraction=frac)
        rows.append(row)
        np.savez(ws.priors / f"{name}.npz", depth=np.where(mask, depth, 0).astype(np.float16), mask=mask,
                 **({"normal": np.where(mask[..., None], normal, 0).astype(np.float16)} if normal is not None else {}))

    if stored is not None and stored.get("log_k") is not None:
        scales, log_k = stored["scales"], stored["log_k"]
        _apply_corrections(ws, names, scales, log_k)
        return {**stored.get("metrics", {}), "repaired": True}
    if len(scales) < max(5, 0.2 * len(names)):
        ws.log(f"WARNING only {len(scales)} frames had a reliable depth scale; priors disabled")
        shutil.rmtree(ws.priors, ignore_errors=True)
        ws.priors.mkdir()
        rec.write(_sparse_dir(ws))
        write_json(scales_path, {"log_k": None, "scales": {}})
        return {"priors": False, "metric_scale": False, "frames": len(names), "per_frame": rows,
                "warnings": ["Depth priors could not be aligned to the camera reconstruction; trained without them."]}

    log_values = np.array(list(scales.values()))
    log_k = float(np.median(log_values))
    mad = float(np.median(np.abs(log_values - log_k)))
    _apply_corrections(ws, names, scales, log_k)
    rec.transform(pycolmap.Sim3d(math.exp(-log_k), pycolmap.Rotation3d(), np.zeros(3)))
    rec.write(_sparse_dir(ws))
    metrics = {"priors": True, "metric_scale": True, "metres_per_original_unit": math.exp(-log_k),
               "scale_spread_mad_log": mad, "frames": len(names), "frames_with_reliable_scale": len(scales),
               "per_frame": rows}
    write_json(scales_path, {"log_k": log_k, "scales": scales, "metrics": metrics})
    return metrics


def _apply_corrections(ws, names, scales, log_k):
    """Per-frame correction so each saved prior matches the (metric) reconstruction."""
    for name in names:
        path = ws.priors / f"{name}.npz"
        data = dict(np.load(path))
        correction = math.exp(scales.get(name, log_k) - log_k)
        data["depth"] = (data["depth"].astype(np.float32) * correction).astype(np.float16)
        data["scale_reliable"] = np.array(name in scales)
        np.savez(path, **data)


def _undistort(ws, long_side):
    """Training images straight from the original frames (sfm/undistorted is only 1920 px)."""
    out = ws.root / "undistorted"
    shutil.rmtree(out, ignore_errors=True)
    ws.status(stage="priors", message=f"Undistorting frames at {long_side} px")
    options = pycolmap.UndistortCameraOptions()
    options.max_image_size = long_side
    pycolmap.undistort_images(out, ws.sfm / "sparse", ws.frames / "images", output_type="COLMAP",
                              undistort_options=options, jpeg_quality=95)
    return out


def _sparse_dir(ws):
    path = ws.dataset / "sparse"
    path.mkdir(parents=True, exist_ok=True)
    return path

</file>

<file src="namma/sfm.py">
"""Camera poses with pycolmap (BSD-3), CPU SIFT only.

COLMAP's GPU SIFT is SiftGPU, licensed for non-profit research only, so it is never used here; the
PyPI pycolmap wheel has no CUDA, which guarantees that. Matching is sequential (video order) plus a
quadratic long-range pass and, if the vocabulary tree can be fetched, loop detection. The global
mapper runs first; the incremental mapper is tried when too few frames register.
"""
import shutil
import urllib.request

import numpy as np
import pycolmap


def cam_from_world(image):
    pose = image.cam_from_world
    return pose() if callable(pose) else pose


def camera_center(image):
    pose = cam_from_world(image)
    R = np.asarray(pose.rotation.matrix())
    return -R.T @ np.asarray(pose.translation)


def _rotation_between(a, b):
    a, b = a / np.linalg.norm(a), b / np.linalg.norm(b)
    v, c = np.cross(a, b), float(np.dot(a, b))
    if np.linalg.norm(v) < 1e-9:
        return np.eye(3) if c > 0 else np.diag([1.0, -1.0, -1.0])
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx / (1 + c)


def level_and_center(rec):
    """Rotate so the average camera 'up' becomes world -Y (OpenCV/COLMAP convention), centre on the cameras."""
    ups, centers = [], []
    for image in rec.images.values():
        if not image.has_pose:
            continue
        R = np.asarray(cam_from_world(image).rotation.matrix())
        ups.append(R.T @ np.array([0.0, -1.0, 0.0]))
        centers.append(camera_center(image))
    up = np.mean(ups, axis=0)
    R = _rotation_between(up, np.array([0.0, -1.0, 0.0]))
    t = -R @ np.median(centers, axis=0)  # median: one far-off camera must not move the origin
    rec.transform(pycolmap.Sim3d(1.0, pycolmap.Rotation3d(R), t))
    return {"up_tilt_deg": float(np.degrees(np.arccos(np.clip(-up[1] / np.linalg.norm(up), -1, 1)))),
            "up_consistency": float(np.linalg.norm(up))}


def _vocab_tree(ws, url, log):
    path = ws.root.parent / "_assets" / url.rsplit("/", 1)[-1]
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            log(f"Downloading vocabulary tree {url}")
            tmp = path.with_suffix(".part")
            urllib.request.urlretrieve(url, tmp)
            tmp.rename(path)
        except Exception as error:  # loop detection is an improvement, not a requirement
            log(f"Vocabulary tree unavailable ({error}); continuing without loop detection")
            return None
    return path


def outlier_cameras(rec, factor):
    """Registered images whose centre lies far outside the rest (global mapping can place a few absurdly)."""
    ids = [i for i, img in rec.images.items() if img.has_pose]
    if len(ids) < 5:
        return []
    centers = np.array([camera_center(rec.images[i]) for i in ids])
    dist = np.linalg.norm(centers - np.median(centers, axis=0), axis=1)
    limit = factor * max(float(np.median(dist)), 1e-9)
    return [i for i, d in zip(ids, dist) if d > limit]


def _summary(rec, total, factor=6.0):
    outliers = len(outlier_cameras(rec, factor))
    return {"registered": rec.num_reg_images() - outliers, "outlier_cameras": outliers, "total": total,
            "fraction": (rec.num_reg_images() - outliers) / max(total, 1),
            "points": rec.num_points3D(), "mean_reprojection_error": rec.compute_mean_reprojection_error(),
            "mean_track_length": rec.compute_mean_track_length()}


def _best(recs):
    return max(recs.values(), key=lambda r: (r.num_reg_images(), -r.compute_mean_reprojection_error())) if recs else None


def run(ws, cfg):
    sc = cfg.sfm
    images = ws.frames / "images"
    names = sorted(p.name for p in images.glob("*.jpg"))
    if len(names) < 10:
        raise RuntimeError(f"Only {len(names)} frames to reconstruct")
    for old in ("database.db", "global", "incremental", "sparse", "undistorted"):
        target = ws.sfm / old
        shutil.rmtree(target, ignore_errors=True) if target.is_dir() else target.unlink(missing_ok=True)
    db = ws.sfm / "database.db"

    ws.status(stage="sfm", message=f"Extracting SIFT features from {len(names)} frames (CPU)", progress=None)
    reader = pycolmap.ImageReaderOptions()
    reader.camera_model = sc.camera_model
    extraction = pycolmap.FeatureExtractionOptions()
    extraction.use_gpu = False
    extraction.max_image_size = sc.max_image_size
    extraction.sift.max_num_features = sc.max_features
    pycolmap.extract_features(db, images, image_names=names, camera_mode=pycolmap.CameraMode.SINGLE,
                              reader_options=reader, extraction_options=extraction, device=pycolmap.Device.cpu)

    matching = pycolmap.FeatureMatchingOptions()
    matching.use_gpu = False
    matching.guided_matching = True
    pairing = pycolmap.SequentialPairingOptions()
    pairing.overlap = sc.overlap
    pairing.quadratic_overlap = False
    vocab = _vocab_tree(ws, sc.vocab_tree_url, ws.log) if sc.loop_detection and len(names) > 60 else None
    if vocab:
        pairing.loop_detection = True
        pairing.vocab_tree_path = str(vocab)
        pairing.loop_detection_period = 5
        pairing.loop_detection_num_images = 30
        pairing.loop_detection_min_index_distance = 30
    ws.status(message=f"Matching neighbouring frames (overlap {sc.overlap}, loop detection {'on' if vocab else 'off'})")
    pycolmap.match_sequential(db, matching_options=matching, pairing_options=pairing, device=pycolmap.Device.cpu)
    if sc.quadratic_overlap > 0:
        far = pycolmap.SequentialPairingOptions()
        far.overlap = sc.quadratic_overlap
        far.quadratic_overlap = True
        ws.status(message="Matching long-range frame pairs")
        pycolmap.match_sequential(db, matching_options=matching, pairing_options=far, device=pycolmap.Device.cpu)

    candidates = {}
    if sc.mapper in ("auto", "global"):
        ws.status(message="Global mapping (rotation averaging + global positioning)")
        out = ws.sfm / "global"
        out.mkdir()
        try:
            best = _best(pycolmap.global_mapping(db, images, out))
            if best is not None:
                candidates["global"] = best
                ws.log(f"global mapper: {_summary(best, len(names), sc.outlier_factor)}")
        except Exception as error:
            ws.log(f"global mapper failed: {error}")
    glob = _summary(candidates["global"], len(names), sc.outlier_factor) if candidates else None
    if sc.mapper == "incremental" or (sc.mapper == "auto" and (
            glob is None or glob["fraction"] < sc.warn_registered or glob["outlier_cameras"] > 0
            or glob["mean_reprojection_error"] > sc.max_global_error)):
        ws.status(message="Incremental mapping")
        out = ws.sfm / "incremental"
        out.mkdir()
        best = _best(pycolmap.incremental_mapping(db, images, out))
        if best is not None:
            candidates["incremental"] = best
            ws.log(f"incremental mapper: {_summary(best, len(names), sc.outlier_factor)}")
    if not candidates:
        raise RuntimeError("COLMAP could not reconstruct any cameras")
    # Among models that pose at least 95% as many (non-outlier) frames as the best one, take the most accurate.
    scored = {k: _summary(v, len(names), sc.outlier_factor) for k, v in candidates.items()}
    most = max(s["registered"] for s in scored.values())
    mapper = min((k for k, s in scored.items() if s["registered"] >= 0.95 * most),
                 key=lambda k: scored[k]["mean_reprojection_error"])
    rec, summary = candidates[mapper], scored[mapper]
    ws.log(f"chose the {mapper} reconstruction: {summary}")
    if summary["fraction"] < sc.min_registered:
        raise RuntimeError(f"Only {summary['registered']}/{len(names)} frames got a camera pose "
                           f"({summary['fraction']:.0%} < {sc.min_registered:.0%}). The video may move too fast, "
                           f"be blurry, or lack texture. Details: {summary}")
    warnings = []
    if summary["fraction"] < sc.warn_registered:
        warnings.append(f"Only {summary['registered']}/{len(names)} frames ({summary['fraction']:.0%}) got a camera pose; "
                        "parts of the room seen only in the other frames will be missing.")
        ws.log("WARNING " + warnings[-1])
    level = level_and_center(rec)
    sparse = ws.sfm / "sparse"
    sparse.mkdir()
    rec.write(sparse)

    ws.status(message="Undistorting frames to training resolution")
    undistort = pycolmap.UndistortCameraOptions()
    undistort.max_image_size = sc.train_long_side
    pycolmap.undistort_images(ws.sfm / "undistorted", sparse, images, output_type="COLMAP",
                              undistort_options=undistort, jpeg_quality=95)
    return {"mapper": mapper, **summary, **level, "candidates": {k: _summary(v, len(names)) for k, v in candidates.items()},
            "loop_detection": bool(vocab), "warnings": warnings}  # outlier cameras are dropped by trainer.load_dataset

</file>

<file src="namma/trainer.py">
"""Gaussian Splatting training on gsplat (Apache-2.0), resumable.

Follows gsplat's examples/simple_trainer.py recipe (MCMC densification with a fixed Gaussian budget,
L1 + SSIM, opacity/scale regularisation, SH degree warm-up) and adds:
  * per-frame affine colour correction for video exposure / white-balance drift (training only; the
    exported model keeps the uncorrected colours),
  * log-depth and normal-consistency losses against the aligned MoGe priors (namma.priors),
  * non-finite loss/gradient guards and full-state checkpoints for resuming after a Molab shutdown.
"""
import math
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Optional

import cv2
import numpy as np
import pycolmap
import torch
import torch.nn.functional as F

from namma.sfm import cam_from_world
from namma.workspace import sha256_file, write_json

SH_C0 = 0.28209479177387814
OUTLIER_FACTOR = 6.0  # same rule as namma.sfm.outlier_cameras
BACKEND = None  # tests may install a stand-in renderer here


def backend():
    global BACKEND
    if BACKEND is None:
        from gsplat.losses import ssim_loss
        from gsplat.rendering import rasterization
        from gsplat.strategy import DefaultStrategy, MCMCStrategy
        from gsplat.utils import depth_to_normal
        BACKEND = SimpleNamespace(rasterization=rasterization, DefaultStrategy=DefaultStrategy, MCMCStrategy=MCMCStrategy,
                                  ssim_loss=ssim_loss, depth_to_normal=depth_to_normal)
    return BACKEND


@dataclass
class Frame:
    name: str
    K: torch.Tensor          # [3, 3]
    c2w: torch.Tensor        # [4, 4] OpenCV convention
    width: int
    height: int
    image: torch.Tensor      # [H, W, 3] uint8 (CPU)
    depth: Optional[torch.Tensor] = None    # [H, W] float16 metres (0 = invalid)
    normal: Optional[torch.Tensor] = None   # [H, W, 3] float16, camera frame, facing the camera


def load_dataset(ws, with_priors=True):
    rec = pycolmap.Reconstruction(ws.dataset / "sparse")
    images = sorted((img for img in rec.images.values() if img.has_pose), key=lambda img: img.name)

    def load(img):
        cam = rec.cameras[img.camera_id]
        fx, fy, cx, cy = cam.params[:4] if cam.model_name == "PINHOLE" else (cam.params[0],) * 2 + tuple(cam.params[1:3])
        pose = cam_from_world(img)
        w2c = np.eye(4)
        w2c[:3, :3] = np.asarray(pose.rotation.matrix())
        w2c[:3, 3] = np.asarray(pose.translation)
        rgb = cv2.cvtColor(cv2.imread(str(ws.dataset / "images" / img.name)), cv2.COLOR_BGR2RGB)
        frame = Frame(img.name, torch.tensor([[fx, 0, cx], [0, fy, cy], [0, 0, 1]], dtype=torch.float32),
                      torch.from_numpy(np.linalg.inv(w2c)).float(), rgb.shape[1], rgb.shape[0], torch.from_numpy(rgb))
        prior = ws.priors / f"{img.name}.npz"
        if with_priors and prior.exists():
            data = np.load(prior)
            frame.depth = torch.from_numpy(data["depth"])
            if "normal" in data:
                frame.normal = torch.from_numpy(data["normal"])
        return frame

    # A few cameras (and points) placed absurdly far away by SfM would set the scene scale, learning rates
    # and initial Gaussians for the whole room: leave them out.
    centers = np.array([np.asarray(cam_from_world(img).rotation.matrix()).T @ -np.asarray(cam_from_world(img).translation)
                        for img in images])
    middle = np.median(centers, axis=0)
    dist = np.linalg.norm(centers - middle, axis=1)
    keep = dist <= OUTLIER_FACTOR * max(float(np.median(dist)), 1e-9)
    images = [img for img, k in zip(images, keep) if k]
    with ThreadPoolExecutor(8) as pool:
        frames = list(pool.map(load, images))
    reach = 4 * max(float(dist[keep].max()), 1e-6) + 20 * max(float(np.median(dist)), 1e-6)
    xyz, rgb = [], []
    for point in rec.points3D.values():
        if point.track.length() >= 2 and np.linalg.norm(point.xyz - middle) <= reach:
            xyz.append(point.xyz)
            rgb.append(point.color)
    if (~keep).any():
        print(f"load_dataset: ignored {int((~keep).sum())} outlier cameras", flush=True)
    return frames, np.array(xyz, np.float32), np.array(rgb, np.float32) / 255.0


def split(frames, test_every):
    test = list(range(0, len(frames), test_every)) if len(frames) >= 3 * test_every else []
    train = [i for i in range(len(frames)) if i not in set(test)]
    return train, test


def scene_scale(frames):
    centers = torch.stack([f.c2w[:3, 3] for f in frames])
    return float((centers - centers.median(0).values).norm(dim=1).max()) * 1.1 + 1e-6


def normalise(frames, xyz):
    """Move and scale the scene in place so the median camera distance from the median camera centre is 1,
    as gsplat's simple_trainer does (normalize_world_space). Its MCMC position noise is covariance times the
    means learning rate, so in a metric room it would grow with the square of the room's size."""
    centers = torch.stack([f.c2w[:3, 3] for f in frames])
    center = centers.median(0).values
    norm = float((centers - center).norm(dim=1).median().clamp_min(1e-6))
    for f in frames:
        f.c2w = f.c2w.clone()
        f.c2w[:3, 3] = (f.c2w[:3, 3] - center) / norm
        if f.depth is not None:
            f.depth = f.depth / norm
    xyz -= center.numpy()
    xyz /= norm
    return center, norm


def init_splats(xyz, rgb, tc, scale, device):
    from scipy.spatial import cKDTree
    points = torch.from_numpy(xyz)
    dist, _ = cKDTree(xyz).query(xyz, k=4)
    dist_avg = torch.from_numpy(np.sqrt((dist[:, 1:] ** 2).mean(1))).float().clamp_min(1e-7)
    n = len(points)
    shs = torch.zeros(n, (tc.sh_degree + 1) ** 2, 3)
    shs[:, 0] = (torch.from_numpy(rgb) - 0.5) / SH_C0
    params = {
        "means": (points, 1.6e-4 * scale),
        "scales": (torch.log(dist_avg * tc.value("init_scale"))[:, None].repeat(1, 3), 5e-3),
        "quats": (F.normalize(torch.rand(n, 4), dim=-1), 1e-3),
        "opacities": (torch.logit(torch.full((n,), tc.value("init_opacity"))), 5e-2),
        "sh0": (shs[:, :1], 2.5e-3),
        "shN": (shs[:, 1:], 2.5e-3 / 20),
    }
    return {k: v for k, (v, _) in params.items()}, {k: lr for k, (_, lr) in params.items()}


def make_optimizers(splats, lrs):
    return {k: torch.optim.Adam([{"params": splats[k], "lr": lrs[k], "name": k}], eps=1e-15) for k in splats}


def render(splats, frame, sh_degree, device, mode="RGB+ED"):
    viewmat = torch.linalg.inv(frame.c2w).to(device)[None]
    colors = torch.cat([splats["sh0"], splats["shN"]], 1)
    renders, alphas, info = backend().rasterization(
        means=splats["means"], quats=splats["quats"], scales=torch.exp(splats["scales"]),
        opacities=torch.sigmoid(splats["opacities"]), colors=colors, viewmats=viewmat, Ks=frame.K.to(device)[None],
        width=frame.width, height=frame.height, sh_degree=sh_degree, render_mode=mode, packed=False,
        rasterize_mode="classic")
    return renders, alphas, info


def _fit(prior, frame):
    """[h, w, c] prior map -> [H, W, c] at the frame's size (nearest, so invalid zeros do not smear)."""
    if prior.shape[:2] == (frame.height, frame.width):
        return prior
    return F.interpolate(prior.permute(2, 0, 1)[None], size=(frame.height, frame.width), mode="nearest")[0].permute(1, 2, 0)


def lambda_at(step, steps, start, end):
    t = min(max(step / max(steps, 1), 0.0), 1.0)
    return start * (end / start) ** t if start > 0 and end > 0 else start


def ssim_value(a, b):
    return 1.0 - float(backend().ssim_loss(a.permute(0, 3, 1, 2), b.permute(0, 3, 1, 2)))


class Trainer:
    def __init__(self, ws, cfg, device="cuda"):
        self.ws, self.cfg, self.tc, self.device = ws, cfg, cfg.train, device
        self.ckpt_dir = ws.train / "ckpt"
        sparse = ws.dataset / "sparse"
        fingerprint = "".join(sha256_file(p) for p in sorted(sparse.glob("*.bin")))
        self.settings = cfg.stage_hash("frames", "sfm", "priors", "train") + ":" + fingerprint[:32]
        self.ckpt_dir.mkdir(parents=True, exist_ok=True)
        self.frames, xyz, rgb = load_dataset(ws)
        if len(xyz) < 100:
            raise RuntimeError(f"Only {len(xyz)} sparse points to initialise from")
        self.center, self.norm = normalise(self.frames, xyz) if self.tc.normalize_world else (torch.zeros(3), 1.0)
        self.train_ids, self.test_ids = split(self.frames, self.tc.test_every)
        self.scale = scene_scale(self.frames)
        self.has_priors = any(f.depth is not None for f in self.frames)
        params, self.lrs = init_splats(xyz, rgb, self.tc, self.scale, device)
        self._set_params(params)
        n = len(self.frames)
        self.app_A = torch.nn.Parameter(torch.eye(3, device=device).repeat(n, 1, 1))
        self.app_b = torch.nn.Parameter(torch.zeros(n, 3, device=device))
        self.app_opt = torch.optim.Adam([self.app_A, self.app_b], lr=1e-3)
        start = min(500, self.tc.steps // 10)
        if self.tc.strategy == "mcmc":
            self.strategy = backend().MCMCStrategy(cap_max=self.tc.cap_max, refine_stop_iter=int(self.tc.steps * 0.83),
                                                   refine_start_iter=start)
            self.strategy_state = self.strategy.initialize_state()
        else:  # the original 3DGS split/clone/prune schedule, at gsplat simple_trainer's settings
            self.strategy = backend().DefaultStrategy(refine_start_iter=start, refine_stop_iter=self.tc.steps // 2)
            self.strategy_state = self.strategy.initialize_state(scene_scale=self.scale)
        self.strategy.check_sanity(self.splats, self.optimizers)
        self.step = 0
        self.order, self.cursor = [], 0
        self.rng = np.random.default_rng(0)
        self.bad_steps = 0

    def _set_params(self, tensors):
        self.splats = torch.nn.ParameterDict({k: torch.nn.Parameter(v.to(self.device).contiguous()) for k, v in tensors.items()})
        self.optimizers = make_optimizers(self.splats, self.lrs)
        self.scheduler = torch.optim.lr_scheduler.ExponentialLR(self.optimizers["means"], gamma=0.01 ** (1.0 / self.tc.steps))

    # ---- checkpoints ----------------------------------------------------------------------
    def save(self):
        path = self.ckpt_dir / f"step_{self.step:06d}.pt"
        state = {"step": self.step, "splats": {k: v.detach().cpu() for k, v in self.splats.items()},
                 "optimizers": {k: o.state_dict() for k, o in self.optimizers.items()},
                 "scheduler": self.scheduler.state_dict(), "strategy_state": self.strategy_state,
                 "app": {"A": self.app_A.detach().cpu(), "b": self.app_b.detach().cpu(), "opt": self.app_opt.state_dict()},
                 "order": self.order, "cursor": self.cursor, "rng": self.rng.bit_generator.state,
                 "torch_rng": torch.get_rng_state(), "cuda_rng": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,
                 "frames": [f.name for f in self.frames], "settings": self.settings}
        tmp = path.with_suffix(".tmp")
        torch.save(state, tmp)
        tmp.replace(path)
        older = sorted(p for p in self.ckpt_dir.glob("step_*.pt") if p != path and int(p.stem[5:]) < self.step)
        for old in older[:-1]:  # keep this one and the previous one
            old.unlink(missing_ok=True)
        return path

    def resume(self):
        ckpts = sorted(self.ckpt_dir.glob("step_*.pt"))
        for path in reversed(ckpts):
            try:
                state = torch.load(path, map_location="cpu", weights_only=False)
            except Exception as error:  # a checkpoint cut off by a shutdown
                self.ws.log(f"Skipping unreadable checkpoint {path.name}: {error}")
                continue
            if state.get("frames") != [f.name for f in self.frames] or state.get("settings") != self.settings:
                self.ws.log(f"Removing checkpoint {path.name}: it belongs to different frames/settings")
                path.unlink(missing_ok=True)
                continue
            self._set_params(state["splats"])
            for k, opt in self.optimizers.items():
                opt.load_state_dict(state["optimizers"][k])
            self.scheduler.load_state_dict(state["scheduler"])
            self.strategy_state = {k: (v.to(self.device) if torch.is_tensor(v) else v) for k, v in state["strategy_state"].items()}
            with torch.no_grad():
                self.app_A.copy_(state["app"]["A"])
                self.app_b.copy_(state["app"]["b"])
            self.app_opt.load_state_dict(state["app"]["opt"])
            self.order, self.cursor = state["order"], state["cursor"]
            self.rng.bit_generator.state = state["rng"]
            torch.set_rng_state(state["torch_rng"])
            if state.get("cuda_rng") is not None and torch.cuda.is_available():
                torch.cuda.set_rng_state_all(state["cuda_rng"])
            self.step = state["step"]
            self.ws.log(f"Resumed training at step {self.step} from {path.name} ({len(self.splats['means'])} Gaussians)")
            return True
        return False

    # ---- one optimisation step ---------------------------------------------------------------
    def _next_frame(self):
        if self.cursor >= len(self.order):
            self.order = [int(i) for i in self.rng.permutation(self.train_ids)]
            self.cursor = 0
        index = self.order[self.cursor]
        self.cursor += 1
        return index

    def train_step(self):
        tc, step = self.tc, self.step
        index = self._next_frame()
        frame = self.frames[index]
        gt = frame.image.to(self.device, non_blocking=True).float()[None] / 255.0
        sh_degree = min(step // tc.sh_degree_interval, tc.sh_degree)
        renders, alphas, info = render(self.splats, frame, sh_degree, self.device)
        if self.tc.strategy != "mcmc":
            self.strategy.step_pre_backward(self.splats, self.optimizers, self.strategy_state, step, info)
        rgb, depth = renders[..., :3], renders[..., 3:4]
        if tc.appearance and step >= 1000:
            rgb = torch.einsum("bhwc,dc->bhwd", rgb, self.app_A[index]) + self.app_b[index]
        rgb_c = rgb.clamp(0, 1)
        l1 = (rgb - gt).abs().mean()
        loss = (1 - tc.ssim_lambda) * l1 + tc.ssim_lambda * backend().ssim_loss(rgb_c.permute(0, 3, 1, 2), gt.permute(0, 3, 1, 2))
        terms = {"l1": l1.item()}
        if frame.depth is not None:
            prior = _fit(frame.depth.to(self.device).float()[..., None], frame)[None]
            valid = (prior > 0) & (depth > 1e-4) & (alphas > 0.5)
            if valid.sum() > 100:
                depth_loss = (torch.log(depth[valid]) - torch.log(prior[valid])).abs().mean()
                loss = loss + lambda_at(step, tc.steps, tc.depth_lambda, tc.depth_lambda_end) * depth_loss
                terms["depth"] = depth_loss.item()
            if frame.normal is not None and step >= tc.normal_start:
                normal_world = backend().depth_to_normal(depth, frame.c2w.to(self.device)[None], frame.K.to(self.device)[None])
                prior_n = _fit(frame.normal.to(self.device).float(), frame) @ frame.c2w[:3, :3].to(self.device).T
                h, w = normal_world.shape[1:3]
                if (h, w) != prior_n.shape[:2]:  # some depth_to_normal versions crop the border
                    dy, dx = (prior_n.shape[0] - h) // 2, (prior_n.shape[1] - w) // 2
                    prior_n = prior_n[dy:dy + h, dx:dx + w]
                    valid_n = valid[0, dy:dy + h, dx:dx + w, 0]
                else:
                    valid_n = valid[0, ..., 0]
                if valid_n.sum() > 100:
                    cos = (F.normalize(normal_world[0], dim=-1) * prior_n).sum(-1).abs()
                    normal_loss = (1 - cos[valid_n]).mean()
                    loss = loss + tc.normal_lambda * normal_loss
                    terms["normal"] = normal_loss.item()
        if tc.value("opacity_reg"):
            loss = loss + tc.value("opacity_reg") * torch.sigmoid(self.splats["opacities"]).mean()
        if tc.value("scale_reg"):
            loss = loss + tc.value("scale_reg") * torch.exp(self.splats["scales"]).mean()
        if tc.appearance and step >= 1000:
            loss = loss + 1e-2 * ((self.app_A[index] - torch.eye(3, device=self.device)).square().mean() + self.app_b[index].square().mean())

        if not torch.isfinite(loss):
            return self._skip(f"non-finite loss {terms}")
        loss.backward()
        bad = [k for k, p in self.splats.items() if p.grad is not None and not torch.isfinite(p.grad).all()]
        if bad:
            return self._skip(f"non-finite gradients in {bad}")
        for opt in self.optimizers.values():
            opt.step()
            opt.zero_grad(set_to_none=True)
        if tc.appearance and step >= 1000:
            self.app_opt.step()
        self.app_opt.zero_grad(set_to_none=True)
        self.scheduler.step()
        if tc.strategy == "mcmc":
            self.strategy.step_post_backward(self.splats, self.optimizers, self.strategy_state, step, info,
                                             lr=self.scheduler.get_last_lr()[0])
        else:
            self.strategy.step_post_backward(self.splats, self.optimizers, self.strategy_state, step, info, packed=False)
            if len(self.splats["means"]) > tc.max_gaussians and self.strategy.refine_stop_iter > step:
                self.strategy.refine_stop_iter = step
                self.ws.log(f"step {step}: {len(self.splats['means']):,} Gaussians, densification stopped (max_gaussians)")
        self.bad_steps = 0
        self.step += 1
        terms["loss"] = loss.item()
        terms["psnr"] = (-10 * torch.log10(F.mse_loss(rgb_c.detach(), gt).clamp_min(1e-10))).item()
        return terms

    def _skip(self, reason):
        for opt in list(self.optimizers.values()) + [self.app_opt]:
            opt.zero_grad(set_to_none=True)
        self.bad_steps += 1
        self.ws.log(f"step {self.step}: skipped, {reason}")
        if self.bad_steps >= self.tc.max_bad_steps:
            raise RuntimeError(f"{self.bad_steps} consecutive non-finite steps at step {self.step}: {reason}")
        self.step += 1
        return None

    # ---- evaluation / previews ------------------------------------------------------------------
    @torch.no_grad()
    def evaluate(self):
        ids = self.test_ids or self.train_ids[:: max(1, len(self.train_ids) // 20)]
        psnr, ssim = [], []
        for i in ids:
            frame = self.frames[i]
            renders, _, _ = render(self.splats, frame, self.tc.sh_degree, self.device, mode="RGB")
            rgb = renders[..., :3].clamp(0, 1)
            gt = frame.image.to(self.device).float()[None] / 255.0
            psnr.append(float(-10 * torch.log10(F.mse_loss(rgb, gt).clamp_min(1e-10))))
            ssim.append(ssim_value(rgb, gt))
        return {"views": len(ids), "held_out": bool(self.test_ids), "psnr": float(np.mean(psnr)), "ssim": float(np.mean(ssim))}

    @torch.no_grad()
    def preview(self):
        frame = self.frames[(self.test_ids or self.train_ids)[0]]
        renders, alphas, _ = render(self.splats, frame, self.tc.sh_degree, self.device)
        rgb = (renders[0, ..., :3].clamp(0, 1) * 255).byte().cpu().numpy()
        depth = renders[0, ..., 3].cpu().numpy()
        valid = alphas[0, ..., 0].cpu().numpy() > 0.5
        lo, hi = np.percentile(depth[valid], [2, 98]) if valid.any() else (0, 1)
        depth_img = cv2.applyColorMap((np.clip((depth - lo) / max(hi - lo, 1e-6), 0, 1) * 255).astype(np.uint8), cv2.COLORMAP_TURBO)
        canvas = np.concatenate([frame.image.numpy()[..., ::-1], rgb[..., ::-1], depth_img], axis=1)
        scale = min(1.0, 2400 / canvas.shape[1])
        canvas = cv2.resize(canvas, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        path = self.ws.train / "previews" / f"step_{self.step:06d}.jpg"
        path.parent.mkdir(exist_ok=True)
        cv2.imwrite(str(path), canvas, [cv2.IMWRITE_JPEG_QUALITY, 88])
        return path

    def snapshot(self):
        return {k: v.detach().cpu().clone() for k, v in self.splats.items()}

    def restore(self, splats):
        with torch.no_grad():
            for k, v in splats.items():
                self.splats[k].data = v.to(self.device)

    def export_final(self):
        """final.pt is in the dataset's (metric) world, whatever the training normalisation."""
        splats = self.snapshot()
        splats["means"] = splats["means"] * self.norm + self.center
        splats["scales"] = splats["scales"] + math.log(self.norm)
        path = self.ws.train / "final.pt"
        torch.save({"splats": splats, "sh_degree": self.tc.sh_degree}, path)
        return path


def run(ws, cfg, on_checkpoint=None):
    torch.manual_seed(0)
    trainer = Trainer(ws, cfg)
    trainer.resume()
    tc = cfg.train
    log_path = ws.train / "metrics.jsonl"
    started, last_report = time.time(), time.time()
    window, history, best = [], [], None  # best = (held-out PSNR, step, splats on CPU)
    while trainer.step < tc.steps:
        terms = trainer.train_step()
        if terms:
            window.append(terms)
        step = trainer.step
        if step % 100 == 0 or step == tc.steps:
            if window:
                mean = {k: float(np.mean([t[k] for t in window if k in t])) for k in window[-1]}
                elapsed = time.time() - last_report
                record = {"step": step, "gaussians": len(trainer.splats["means"]), **mean,
                          "steps_per_s": round(len(window) / max(elapsed, 1e-6), 2)}
                with open(log_path, "a") as f:
                    f.write(__import__("json").dumps(record) + "\n")
                remaining = (tc.steps - step) / max(record["steps_per_s"], 1e-6)
                ws.status(stage="train", progress=step / tc.steps,
                          message=f"step {step}/{tc.steps}, {record['gaussians']:,} Gaussians, PSNR {mean.get('psnr', 0):.2f}, "
                                  f"~{remaining / 60:.0f} min left")
                window, last_report = [], time.time()
        if step % tc.preview_every == 0 and step < tc.steps:
            trainer.preview()
        if step % tc.checkpoint_every == 0 and step < tc.steps:
            path = trainer.save()
            if on_checkpoint:
                on_checkpoint(path, step)
            score = trainer.evaluate()
            history.append({"step": step, "psnr": round(score["psnr"], 2), "ssim": round(score["ssim"], 4)})
            with open(log_path, "a") as f:
                f.write(__import__("json").dumps({"eval": history[-1]}) + "\n")
            if best is None or score["psnr"] > best[0]:
                best = (score["psnr"], step, trainer.snapshot())
            elif score["psnr"] < best[0] - 3:
                ws.log(f"WARNING held-out PSNR fell from {best[0]:.1f} dB (step {best[1]}) to {score['psnr']:.1f} dB at step {step}")
    trainer.preview()
    metrics = trainer.evaluate()
    if best is not None and best[0] > metrics["psnr"] + 0.5:
        ws.log(f"Exporting the step {best[1]} model (held-out PSNR {best[0]:.1f} dB) instead of the final one ({metrics['psnr']:.1f} dB)")
        trainer.restore(best[2])
        metrics = {**trainer.evaluate(), "exported_step": best[1]}
    final = trainer.export_final()
    if metrics["psnr"] < tc.min_psnr:
        raise RuntimeError(f"Training did not converge (held-out PSNR {metrics['psnr']:.1f} dB, scene scale "
                           f"{trainer.scale:.3g}). Check the camera reconstruction (outlier cameras, pose error).")
    metrics.update(gaussians=len(trainer.splats["means"]), steps=tc.steps, minutes=round((time.time() - started) / 60, 1),
                   priors=trainer.has_priors, scene_scale=trainer.scale, world_scale=trainer.norm, eval_history=history)
    write_json(ws.train / "eval.json", metrics)
    return metrics, [final, ws.train / "eval.json", log_path]

</file>

<file src="namma/workspace.py">
"""One job's folder: stage outputs, completion receipts, status and logs.

    <job>/job.json           source video identity + settings
    <job>/stages/<s>.json    receipt written when stage <s> finished (settings hash, outputs, metrics)
    <job>/status.json        what the notebook shows (stage, progress, message)
    <job>/logs/              pipeline.log and per-stage logs
    <job>/outbox/            files waiting for the Drive uploader (see namma.backup)
"""
import hashlib
import json
import os
import time
from pathlib import Path

STAGES = ("frames", "sfm", "priors", "train", "mesh", "export")


def write_json(path, data):
    """Atomic JSON write: a reader never sees a half-written file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, indent=1, default=str))
    os.replace(tmp, path)


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def sha256_file(path, block=8 << 20):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(block):
            digest.update(chunk)
    return digest.hexdigest()


class Workspace:
    def __init__(self, root):
        self.root = Path(root).resolve()
        for sub in ("stages", "logs", "input", "frames", "sfm", "dataset", "priors", "train", "mesh", "export", "outbox"):
            (self.root / sub).mkdir(parents=True, exist_ok=True)

    def __getattr__(self, name):
        if name in ("stages", "logs", "input", "frames", "sfm", "dataset", "priors", "train", "mesh", "export", "outbox"):
            return self.root / name
        raise AttributeError(name)

    @property
    def job(self):
        return read_json(self.root / "job.json", {})

    def receipt(self, stage):
        return read_json(self.stages / f"{stage}.json")

    def is_done(self, stage, settings_hash):
        receipt = self.receipt(stage)
        if not receipt or receipt.get("settings") != settings_hash:
            return False
        return all((self.root / rel).exists() for rel in receipt.get("outputs", []))

    def finish(self, stage, settings_hash, outputs, metrics, started):
        receipt = {"stage": stage, "settings": settings_hash, "finished": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "seconds": round(time.time() - started, 1),
                   "outputs": [str(Path(p).resolve().relative_to(self.root)) for p in outputs], "metrics": metrics}
        write_json(self.stages / f"{stage}.json", receipt)
        return receipt

    def invalidate_from(self, stage):
        """A re-run stage makes every later stage stale."""
        for later in STAGES[STAGES.index(stage):]:
            (self.stages / f"{later}.json").unlink(missing_ok=True)

    def status(self, **fields):
        current = read_json(self.root / "status.json", {})
        current.update(fields, updated=time.time())
        write_json(self.root / "status.json", current)

    def log(self, message):
        line = f"{time.strftime('%H:%M:%S')} {message}"
        print(line, flush=True)
        with open(self.logs / "pipeline.log", "a") as f:
            f.write(line + "\n")

</file>

<file src="notebooks/namma_space.py">
import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")

with app.setup:
    import io
    import json
    import os
    import shutil
    import subprocess
    import sys
    import tarfile
    import time
    from pathlib import Path

    import marimo as mo


@app.function
def git(repo, *args, stdin=None):
    return subprocess.run(["git", "-C", str(repo), *args], input=stdin, capture_output=True, text=True)


@app.function
def get_checkout(repo, source, ref):
    """Make `repo` a Git checkout of `ref` from `source` without overwriting anyone's edits.

    After a shutdown molab restores source files but not `.git`, logs or the environment, so the folder
    may hold files from an older checkout. A file is replaced only when Git history shows it is an
    unmodified committed version; anything else is left in place and listed. An existing checkout is
    only fast-forwarded, which Git refuses if it would touch local changes.
    """
    repo = Path(repo)
    branch = f"refs/heads/{ref}"
    if (repo / ".git").exists() and git(repo, "rev-parse", "--verify", "-q", "HEAD").returncode == 0:
        current = git(repo, "symbolic-ref", "-q", "HEAD").stdout.strip()
        if current != branch:
            return f"{repo} is on {current or 'a detached HEAD'}, not {ref}; left unchanged."
        before = git(repo, "rev-parse", "--short", "HEAD").stdout.strip()
        fetched = git(repo, "fetch", "-q", "--no-tags", source, branch)
        if fetched.returncode:
            return f"{repo} left unchanged; fetching {ref} failed:\n{fetched.stderr}"
        merged = git(repo, "merge", "--ff-only", "-q", "FETCH_HEAD")
        if merged.returncode:
            return f"{repo} left unchanged; it cannot fast-forward without touching local changes:\n{merged.stderr}"
        after = git(repo, "rev-parse", "--short", "HEAD").stdout.strip()
        return f"{repo}: already at {ref} {after}." if after == before else f"{repo}: updated {before} -> {after}."
    repo.mkdir(parents=True, exist_ok=True)
    for args in (["init", "-q"],
                 ["fetch", "-q", "--no-tags", "--update-head-ok", source, f"+{branch}:{branch}"],
                 ["symbolic-ref", "HEAD", branch],
                 ["reset", "-q"]):  # index = branch tip; files on disk untouched
        result = git(repo, *args)
        if result.returncode:
            return f"git {' '.join(args)} failed:\n{result.stdout}{result.stderr}"
    git(repo, "remote", "add", "origin", source)
    deleted = [p for p in git(repo, "ls-files", "-z", "--deleted").stdout.split("\0") if p]
    changed = sorted({p for p in git(repo, "ls-files", "-z", "--modified").stdout.split("\0") if p} - set(deleted))
    hashes = git(repo, "hash-object", "--stdin-paths", stdin="\n".join(changed)).stdout.split() if changed else []
    known = {line.split()[0] for line in git(repo, "rev-list", "--objects", "--all").stdout.splitlines()}
    stale = [p for p, h in zip(changed, hashes) if h in known]
    edited = [p for p, h in zip(changed, hashes) if h not in known]
    restore = deleted + stale
    if restore:
        result = git(repo, "checkout", "--pathspec-from-file=-", "--pathspec-file-nul", stdin="\0".join(restore))
        if result.returncode:
            return f"git checkout failed:\n{result.stderr}"
    untracked = [p for p in git(repo, "ls-files", "-z", "--others", "--exclude-standard").stdout.split("\0") if p]
    lines = [f"Checked out {ref} in {repo}.",
             f"Files written: {len(deleted)} missing, {len(stale)} from an older commit."]
    if edited:
        lines.append(f"{len(edited)} file(s) differ from every committed version and were LEFT AS THEY ARE:")
        lines += [f"  {p}" for p in edited[:20]]
    if untracked:
        lines.append(f"{len(untracked)} untracked file(s) kept (not part of {ref}), e.g. {untracked[0]}")
    return "\n".join(lines)


@app.function
def setup_running(repo):
    """True while a molab_setup.sh process for this repository is alive."""
    repo = Path(repo).resolve()
    for cmdline in Path("/proc").glob("[0-9]*/cmdline"):
        try:
            args = cmdline.read_bytes().split(b"\0")
            cwd = Path(f"/proc/{cmdline.parent.name}/cwd").resolve()
        except OSError:
            continue
        for arg in args:
            if arg.endswith(b"molab_setup.sh") and (cwd / arg.decode(errors="replace")).resolve() == repo / "molab_setup.sh":
                return True
    return False


@app.function
def machine_summary(repo):
    try:
        mem = dict(line.split(":", 1) for line in Path("/proc/meminfo").read_text().splitlines())
        ram = f"RAM free {int(mem['MemAvailable'].split()[0]) / 2**20:.0f}/{int(mem['MemTotal'].split()[0]) / 2**20:.0f} GiB"
    except (OSError, KeyError, ValueError):
        ram = "RAM unknown"
    disk = shutil.disk_usage(repo if Path(repo).exists() else "/")
    return f"{ram} · disk free {disk.free / 2**30:.0f}/{disk.total / 2**30:.0f} GiB"


@app.function
def tar_bytes(folder):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        archive.add(folder, arcname=Path(folder).name)
    return buffer.getvalue()


@app.function
def process_running(pattern):
    for cmdline in Path("/proc").glob("[0-9]*/cmdline"):
        try:
            if pattern.encode() in cmdline.read_bytes():
                return True
        except OSError:
            continue
    return False


@app.function
def read_json(path):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return {}


@app.function
def drive_connected():
    """molab's Remote storage cell caches the Google login in pydata-google-auth's credentials file."""
    try:
        import pydata_google_auth.cache
        return os.path.exists(pydata_google_auth.cache.READ_WRITE._path)
    except ImportError:
        return False


@app.function
def ensure_gdrive_fork():
    """PyPI gdrive_fsspec lacks the multi-chunk resumable-upload fix that large checkpoints need."""
    import importlib.metadata
    commit = "dd9bb3025b26091d4a29ac4e81cc3d88910203bd"
    try:
        if commit in (importlib.metadata.distribution("gdrive_fsspec").read_text("direct_url.json") or ""):
            return "pinned gdrive_fsspec already installed"
    except importlib.metadata.PackageNotFoundError:
        pass
    spec = f"gdrive_fsspec @ git+https://github.com/marimo-team/gdrive-fsspec@{commit}"
    for cmd in ([sys.executable, "-m", "pip", "install", "--quiet", spec], ["uv", "pip", "install", "--python", sys.executable, spec]):
        try:
            if subprocess.run(cmd, capture_output=True, text=True).returncode == 0:
                return "installed pinned gdrive_fsspec"
        except FileNotFoundError:
            continue
    return "could not install the pinned gdrive_fsspec; large uploads may fail"


@app.function
def setup_passed(repo):
    logs = Path(repo) / "setup-logs"
    latest = (logs / "LATEST").read_text().strip() if (logs / "LATEST").exists() else ""
    return read_json(logs / latest / "report.json").get("overall") == "pass" if latest else False


@app.cell
def _():
    mo.md("""
    # Namma Space: video to walkable 3D room

    **Part A – environment (once per molab session, ~20–30 min the first time)**
    1. **Get code** – check out the active branch. Files you edited are never overwritten.
    2. **Run setup** – installs the pinned Python packages and CUDA compiler, builds gsplat, installs MoGe-2
       and runs real GPU checks. Wait for *finished* with an overall PASS.

    **Part B – reconstruction**
    - Connect Google Drive: Files panel (left) > *Remote storage* > *Google Drive*, then run the cell it adds.
    - Enter the video's path inside *My Drive* and click **Start / resume**. A 10-minute smoke test on the
      first 20 seconds runs first; if it passes, the full reconstruction starts (typically 1–3 hours).
    - Everything finished is backed up to Drive as it completes. **If molab stops**, open this notebook again,
      redo Part A, connect Drive and click Start again with the same video: finished stages and the latest
      training checkpoint are restored instead of recomputed.
    - The result appears under *Download* below and on Drive (folder `NammaSpaceBackups/<job>/…-download-…`).
    """)
    return


@app.cell
def _():
    workspace = mo.ui.text(value="/marimo/namma-space", label="Repository folder", full_width=True)
    source = mo.ui.text(
        value="https://github.com/TheCodeNotTakenT-T/namma-space.git",
        label="Code source: Git URL or an uploaded .bundle file",
        full_width=True,
    )
    ref = mo.ui.text(value="main", label="Branch")
    get_code = mo.ui.run_button(label="1. Get code")
    run_setup = mo.ui.run_button(label="2. Run setup + GPU checks")
    rebuild = mo.ui.checkbox(label="Rebuild native extensions even if cached")
    mo.vstack([workspace, source, ref, get_code, mo.hstack([run_setup, rebuild], justify="start")])
    return get_code, rebuild, ref, run_setup, source, workspace


@app.cell
def _(get_code, ref, source, workspace):
    mo.stop(not get_code.value)
    _repo = Path(workspace.value)
    _message = get_checkout(_repo, source.value, ref.value)
    _state = git(_repo, "log", "-1", "--format=%H %d %s")
    _status = git(_repo, "status", "--short")
    mo.md(f"```\n{_message}\n\nHEAD: {_state.stdout or _state.stderr}\nLocal changes:\n{_status.stdout or 'none'}\n```")
    return


@app.cell
def _(rebuild, run_setup, workspace):
    mo.stop(not run_setup.value)
    _repo = Path(workspace.value)
    if not (_repo / ".git").exists() or not (_repo / "molab_setup.sh").exists():
        _out = mo.md(f"`{_repo}` is not a complete checkout yet. Click **1. Get code** first.")
    elif setup_running(_repo):
        _out = mo.md("Setup is already running; progress is shown below.")
    else:
        _logs = _repo / "setup-logs"
        _logs.mkdir(exist_ok=True)
        _note = ""
        if drive_connected():  # a compiled gsplat saved by an earlier session skips the long compile
            _env = {**os.environ, "PYTHONPATH": os.pathsep.join(p for p in (str(_repo), os.environ.get("PYTHONPATH", "")) if p)}
            _pull = subprocess.run([sys.executable, "-m", "namma.backup", "cache-pull"], cwd=_repo, env=_env,
                                   capture_output=True, text=True)
            _note = f" Build cache from Drive: {(_pull.stdout or _pull.stderr).strip()[-300:]}"
        _args = ["bash", str(_repo / "molab_setup.sh")] + (["--rebuild"] if rebuild.value else [])
        # A separate session keeps the setup running if the notebook kernel restarts.
        with open(_logs / "notebook-launch.log", "ab") as _launch_log:
            subprocess.Popen(_args, cwd=_repo, stdout=_launch_log, stderr=subprocess.STDOUT, start_new_session=True)
        _out = mo.md("Setup started. Progress appears below." + _note)
    _out
    return


@app.cell
def _():
    refresh = mo.ui.refresh(default_interval="10s", options=["5s", "10s", "30s"])
    refresh
    return (refresh,)


@app.cell
def _(refresh, workspace):
    refresh
    _repo = Path(workspace.value)
    _logs = _repo / "setup-logs"
    _latest = (_logs / "LATEST").read_text().strip() if (_logs / "LATEST").exists() else None
    _runs = sorted(p for p in _logs.glob("20*") if p.is_dir()) if _logs.exists() else []
    _run = _runs[-1] if _runs else None
    _parts = [mo.md(f"_{machine_summary(_repo)} (checked {time.strftime('%H:%M:%S')})_")]
    if _run is None:
        _parts.append(mo.md("No setup run in this session yet."))
    else:
        _log = _run / "setup.log"
        _tail = _log.read_text(errors="replace").splitlines()[-25:] if _log.exists() else []
        if _latest == _run.name:
            _state = "finished"
        elif setup_running(_repo):
            _state = "running"
        else:
            _state = "STOPPED before finishing (process killed or out of memory); download its logs below"
        _parts.append(mo.md(f"**Run {_run.name}** – {_state}\n\n```\n" + "\n".join(_tail) + "\n```"))
        _report = _run / "report.md"
        if _report.exists():
            _parts.append(mo.md(_report.read_text()))
        _archive = _logs / f"namma-setup-{_run.name}.tar.gz"
        if _state == "finished" and _archive.exists():
            _parts.append(mo.download(data=_archive.read_bytes(), filename=_archive.name,
                                      label=f"Download {_archive.name} (send this back)"))
        elif _state != "running":
            _parts.append(mo.download(data=tar_bytes(_run), filename=f"namma-setup-{_run.name}-partial.tar.gz",
                                      label="Download the logs of this stopped run (send this back)"))
    mo.vstack(_parts)
    return


@app.cell
def _():
    video = mo.ui.text(value="", placeholder="e.g. NammaSpace/classroom.mp4 (inside My Drive), or /full/local/path.mp4",
                       label="Video", full_width=True)
    jobs_root = mo.ui.text(value="/opt/namma-jobs", label="Working folder (temporary; backups go to Drive)", full_width=True)
    remote_root = mo.ui.text(value="NammaSpaceBackups", label="Backup folder on Google Drive")
    skip_smoke = mo.ui.checkbox(label="Skip the smoke test")
    start = mo.ui.run_button(label="3. Start / resume reconstruction")
    mo.vstack([mo.md("## Reconstruct a room"), video, jobs_root, remote_root, mo.hstack([start, skip_smoke], justify="start")])
    return jobs_root, remote_root, skip_smoke, start, video


@app.cell
def _(jobs_root, remote_root, skip_smoke, start, video, workspace):
    mo.stop(not start.value)
    _repo = Path(workspace.value)
    _venv = _repo / ".venv" / "bin" / "python"
    _problems = []
    if not _venv.exists() or not setup_passed(_repo):
        _problems.append("Run **2. Run setup** first and wait for an overall PASS (the GPU environment is rebuilt each session).")
    if not video.value.strip():
        _problems.append("Enter the video path.")
    if not drive_connected():
        _problems.append("Connect Google Drive (Files > Remote storage > Google Drive, run the inserted cell). "
                         "Without it nothing survives a molab stop.")
    if process_running("namma.driver"):
        _problems.append("A reconstruction is already running; progress is shown below.")
    if _problems:
        _out = mo.md("\n".join(f"- {p}" for p in _problems))
    else:
        _fork = ensure_gdrive_fork()
        Path(jobs_root.value).mkdir(parents=True, exist_ok=True)
        _args = [sys.executable, "-m", "namma.driver", "--video", video.value.strip(), "--jobs-root", jobs_root.value,
                 "--remote-root", remote_root.value, "--venv-python", str(_venv)]
        _args += (["--skip-smoke"] if skip_smoke.value else []) + (["--local-video"] if video.value.strip().startswith("/") else [])
        _env = {**os.environ, "PYTHONPATH": os.pathsep.join(p for p in (str(_repo), os.environ.get("PYTHONPATH", "")) if p)}
        with open(Path(jobs_root.value) / "driver.log", "ab") as _log:
            subprocess.Popen(_args, cwd=_repo, env=_env, stdin=subprocess.DEVNULL, stdout=_log, stderr=subprocess.STDOUT,
                             start_new_session=True)
        _out = mo.md(f"Started ({_fork}). Progress appears below; it keeps running if this tab disconnects.")
    _out
    return


@app.cell
def _(jobs_root, refresh):
    refresh
    _root = Path(jobs_root.value)
    _driver = read_json(_root / "driver_status.json")
    _parts = [mo.md("**Google Drive:** " + ("connected" if drive_connected() else
                    "NOT connected – Files panel > Remote storage > Google Drive, then run the cell it inserts."))]
    if not _driver:
        _parts.append(mo.md("No reconstruction started in this session."))
    else:
        _state = _driver.get("state")
        if _state == "running" and not process_running("namma.driver"):
            _state = "STOPPED (the driver process is gone; click Start again to resume)"
        _parts.append(mo.md(f"**Reconstruction:** {_state} – {_driver.get('step', '')}"
                            + (f"\n\n**Error:** `{_driver['error']}`" if _driver.get("error") else "")))
        for _key, _title in (("smoke_job", "Smoke test"), ("job", "Full run")):
            if not _driver.get(_key):
                continue
            _job = Path(_driver[_key])
            _st, _bk = read_json(_job / "status.json"), read_json(_job / "backup_status.json")
            _line = (f"**{_title}:** {_st.get('state', 'waiting')} · stage `{_st.get('stage') or '-'}` · {_st.get('message', '')}"
                     + (f" · {_st['progress']:.0%}" if isinstance(_st.get("progress"), (int, float)) else "")
                     + f"\n\nDrive backup: {_bk.get('state', 'not started')}, {_bk.get('uploaded_bytes', 0) / 2**30:.2f} GiB uploaded"
                     + (f" (last error: {_bk['error']})" if _bk.get("error") else "")
                     + (f"\n\n**Error:** `{_st['error']}`" if _st.get("error") else ""))
            _parts.append(mo.md(_line))
            _previews = sorted((_job / "train" / "previews").glob("*.jpg"))
            if _previews:
                _parts.append(mo.image(src=_previews[-1].read_bytes(), caption=f"{_title}: photo | render | depth, {_previews[-1].stem}"))
            _log = _job / "logs" / "pipeline.log"
            if _log.exists():
                _tail = "\n".join(_log.read_text(errors="replace").splitlines()[-30:])
                _parts.append(mo.accordion({f"{_title} log": mo.md(f"```\n{_tail}\n```")}))
    mo.vstack(_parts)
    return


@app.cell
def _():
    show_downloads = mo.ui.run_button(label="Show download buttons for the finished result")
    show_downloads
    return (show_downloads,)


@app.cell
def _(jobs_root, show_downloads):
    mo.stop(not show_downloads.value)
    _driver = read_json(Path(jobs_root.value) / "driver_status.json")
    _folder = Path(_driver.get("job", "/nonexistent")) / "export" / "DOWNLOAD_THIS"
    _files = sorted(p for p in _folder.rglob("*") if p.is_file()) if _folder.exists() else []
    if _files:
        _out = mo.vstack([mo.md("Download every file into one folder, then import it in the viewer (*Namma Pipeline.cmd > 1. Import a trained result*, see `viewer/README.md`). "
                                f"(Also on Google Drive: `{_driver.get('job_id')}`, folder `…-download-…`.)")]
                         + [mo.download(data=p.read_bytes(), filename=p.name, label=f"{p.name} ({p.stat().st_size / 2**20:.0f} MiB)")
                            for p in _files])
    else:
        _out = mo.md("No finished result yet.")
    _out
    return


if __name__ == "__main__":
    app.run()

</file>

<file src="tests/fake_gsplat.py">
"""Tiny differentiable stand-in for the gsplat calls namma.trainer uses, for CPU/GPU tests without gsplat.

It splats isotropic Gaussians with DC colour only and composites them front to back. It is NOT a
replacement for gsplat: it only lets the pipeline's data flow, losses, checkpoints and exports run.
"""
from types import SimpleNamespace

import torch
import torch.nn.functional as F

SH_C0 = 0.28209479177387814


def rasterization(means, quats, scales, opacities, colors, viewmats, Ks, width, height, sh_degree=None,
                  render_mode="RGB", **_):
    w2c, K = viewmats[0], Ks[0]
    cam = means @ w2c[:3, :3].T + w2c[:3, 3]
    z = cam[:, 2]
    keep = z > 0.05
    cam, z, scales, opacities, rgb = cam[keep], z[keep], scales[keep], opacities[keep], colors[keep, 0] * SH_C0 + 0.5
    u = K[0, 0] * cam[:, 0] / z + K[0, 2]
    v = K[1, 1] * cam[:, 1] / z + K[1, 2]
    radius = (K[0, 0] * scales.mean(-1) / z).clamp(0.5, 40.0)
    ys, xs = torch.meshgrid(torch.arange(height, device=means.device) + 0.5,
                            torch.arange(width, device=means.device) + 0.5, indexing="ij")
    order = torch.argsort(z)
    d2 = (xs.reshape(1, -1) - u[order, None]) ** 2 + (ys.reshape(1, -1) - v[order, None]) ** 2
    alpha = (opacities[order, None] * torch.exp(-0.5 * d2 / radius[order, None] ** 2)).clamp(max=0.99)
    transmit = torch.cumprod(torch.cat([torch.ones_like(alpha[:1]), 1 - alpha[:-1]], 0), 0)
    weight = alpha * transmit                                   # [N, H*W]
    acc = weight.sum(0)
    image = (weight[..., None] * rgb[order, None, :]).sum(0)
    out = [image]
    if render_mode in ("RGB+ED", "ED"):
        out.append(((weight * z[order, None]).sum(0) / acc.clamp_min(1e-6))[:, None])
    renders = torch.cat(out, -1).reshape(1, height, width, -1)
    return renders, acc.reshape(1, height, width, 1), {}


class MCMCStrategy:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def check_sanity(self, params, optimizers):
        assert set(params) == set(optimizers)

    def initialize_state(self):
        return {"binoms": torch.zeros(2)}

    def step_post_backward(self, params, optimizers, state, step, info, lr):
        pass


class DefaultStrategy:
    def __init__(self, refine_start_iter=500, refine_stop_iter=15000, **kwargs):
        self.refine_start_iter, self.refine_stop_iter = refine_start_iter, refine_stop_iter

    def check_sanity(self, params, optimizers):
        assert set(params) == set(optimizers)

    def initialize_state(self, scene_scale=1.0):
        return {"grad2d": None, "count": None, "scene_scale": scene_scale}

    def step_pre_backward(self, params, optimizers, state, step, info):
        pass

    def step_post_backward(self, params, optimizers, state, step, info, packed=False):
        pass


def ssim_loss(a, b):
    return F.mse_loss(a, b)


def depth_to_normal(depths, camtoworlds, Ks):
    _, H, W, _ = depths.shape
    K, c2w = Ks[0], camtoworlds[0]
    ys, xs = torch.meshgrid(torch.arange(H, device=depths.device) + 0.5, torch.arange(W, device=depths.device) + 0.5, indexing="ij")
    rays = torch.stack([(xs - K[0, 2]) / K[0, 0], (ys - K[1, 2]) / K[1, 1], torch.ones_like(xs)], -1)
    points = (rays * depths[0]) @ c2w[:3, :3].T + c2w[:3, 3]
    dx = points[2:, 1:-1] - points[:-2, 1:-1]
    dy = points[1:-1, 2:] - points[1:-1, :-2]
    normal = F.normalize(torch.cross(dx, dy, dim=-1), dim=-1)
    return F.pad(normal.permute(2, 0, 1), (1, 1, 1, 1)).permute(1, 2, 0)[None]


BACKEND = SimpleNamespace(rasterization=rasterization, DefaultStrategy=DefaultStrategy, MCMCStrategy=MCMCStrategy,
                          ssim_loss=ssim_loss, depth_to_normal=depth_to_normal)

</file>

<file src="tests/run_local_pipeline.py">
"""Local end-to-end test of the pipeline plumbing with a stand-in renderer (tests/fake_gsplat.py).

    python tests/run_local_pipeline.py VIDEO WORK_DIR

Checks: every stage runs on a short clip; training is killed after its first checkpoint and resumes
from it; the export matches the importer contract; Drive backup to a local folder, restore into a
fresh job, and the rerun skips finished stages. Not a quality test and not a gsplat/GPU validation.
"""
import json
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
SETTINGS = {"sfm": {"train_long_side": 48, "min_registered": 0.4, "loop_detection": False, "max_image_size": 1280},
            "priors": {"enabled": False, "image_long_side": 48, "prior_long_side": 48},
            "train": {"steps": 240, "cap_max": 4000, "checkpoint_every": 80, "preview_every": 80, "normal_start": 40,
                      "sh_degree_interval": 40, "test_every": 8, "min_psnr": 0.0},
            "mesh": {"render_long_side": 48, "max_views": 16, "voxel": 0.05, "target_triangles": 20000}}


def child(job, until):
    """Run the pipeline with the stand-in renderer (separate process so it can be killed)."""
    import namma.trainer as T
    sys.path.insert(0, str(REPO / "tests"))
    import fake_gsplat
    T.BACKEND = fake_gsplat.BACKEND
    from namma import pipeline
    return pipeline.run(job, until or None)


def run_child(job, until="", kill_when=None):
    proc = subprocess.Popen([sys.executable, __file__, "--child", job, until], cwd=REPO)
    if kill_when:
        while proc.poll() is None and not kill_when():
            time.sleep(0.5)
        if proc.poll() is None:
            proc.kill()
            proc.wait()
            return "killed"
    return proc.wait()


def fake_priors(job):
    """MoGe cannot run here; write plausible priors so the depth/normal losses execute."""
    import numpy as np
    from namma.workspace import Workspace
    ws = Workspace(job)
    for img in sorted((ws.dataset / "images").glob("*.jpg")):
        import cv2
        h, w = cv2.imread(str(img)).shape[:2]
        normal = np.zeros((h, w, 3), np.float16)
        normal[..., 2] = -1
        np.savez(ws.priors / f"{img.name}.npz", depth=np.full((h, w), 2.0, np.float16), mask=np.ones((h, w), bool), normal=normal)


def check(condition, message):
    print(("PASS " if condition else "FAIL ") + message, flush=True)
    if not condition:
        sys.exit(1)


def main(video, work):
    work = Path(work)
    shutil.rmtree(work, ignore_errors=True)
    (work / "incoming").mkdir(parents=True)
    shutil.copy(video, work / "incoming" / "clip.mp4")
    from namma import backup, pipeline
    from namma.workspace import Workspace, read_json
    info = pipeline.prepare(work / "incoming" / "clip.mp4", work / "jobs", SETTINGS)
    job = info["job"]
    ws = Workspace(job)
    check(run_child(job, "priors") == 0, "frames, sfm, priors stages")
    fake_priors(job)
    ckpt = ws.train / "ckpt" / "step_000080.pt"
    check(run_child(job, "train", kill_when=ckpt.exists) == "killed", "training interrupted after its first checkpoint")
    check(run_child(job) == 0, "rerun resumes and finishes all stages")
    log = (ws.logs / "pipeline.log").read_text()
    check("Resumed training at step 80" in log, "training resumed from step 80")
    check("frames: already done" in log and "sfm: already done" in log, "finished stages skipped on rerun")

    download = next((ws.export / "DOWNLOAD_THIS").iterdir())
    archives = list(download.glob("*.zip")) or [download / json.loads(next(download.glob("*.parts.json")).read_text())["archive"]]
    with zipfile.ZipFile(archives[0]) as zf:
        names = set(zf.namelist())
        result = json.loads(zf.read("namma-result.json"))
        ply = zf.read("assets/room.ply")
        glb = zf.read("assets/room.glb")
    check({"namma-result.json", "cameras.json", "assets/room.ply", "assets/room.glb", "assets/views.json"} <= names, "archive layout")
    header = ply[: ply.index(b"end_header\n")].decode()
    count = int(header.split("element vertex ")[1].split()[0])
    check(header.count("property float") == 62 and len(ply) - len(header) - 11 == count * 62 * 4, f"PLY layout ({count} splats, 62 floats)")
    import hashlib
    check(result["artifacts"]["splat"]["sha256"] == hashlib.sha256(ply).hexdigest(), "splat sha256 in namma-result.json")
    check(result["artifacts"]["mesh"]["coordinateSpace"] == "raw-ply-v1", "mesh coordinate space")
    import trimesh
    mesh = trimesh.load(trimesh.util.wrap_as_stream(glb), file_type="glb", force="mesh")
    check(len(mesh.faces) == result["artifacts"]["mesh"]["triangleCount"] > 0, f"GLB loads ({len(mesh.faces)} triangles)")

    drive = work / "drive"
    check(backup.upload_loop(job, f"NammaSpaceBackups/{info['job_id']}", f"local:{drive}", once=True) == 0, "upload to local 'Drive'")
    verified = list(drive.rglob("VERIFIED.json"))
    check(len(verified) >= 7, f"{len(verified)} verified backup entries")

    fresh = work / "fresh"
    (fresh / "incoming").mkdir(parents=True)
    shutil.copy(video, fresh / "incoming" / "clip.mp4")
    info2 = pipeline.prepare(fresh / "incoming" / "clip.mp4", fresh / "jobs", SETTINGS)
    restored = backup.restore(info2["job"], f"NammaSpaceBackups/{info['job_id']}", f"local:{drive}")
    print(restored)
    check({"frames", "sfm", "priors", "train", "mesh", "export"} <= set(restored["restored"]), "restore brought every stage back")
    check(run_child(info2["job"]) == 0, "restored job reruns")
    log2 = (Workspace(info2["job"]).logs / "pipeline.log").read_text()
    check("train: already done" in log2 and "priors: repair mode" not in log2 or "train: already done" in log2,
          "training not repeated after restore")
    print("ALL LOCAL PIPELINE CHECKS PASSED")


if __name__ == "__main__":
    if sys.argv[1] == "--child":
        sys.exit(child(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else ""))
    main(sys.argv[1], sys.argv[2])

</file>

<file src="tests/sample/README.md">
# Sample data

`classroom_30s.mp4`: the first 30 seconds of our Round 1 capture (NIT Goa classroom, DSLR on a gimbal,
1/500 s, f/8, 1920×1080), re-encoded to H.264 without audio (18 MB).

To reconstruct it, upload the file to your Google Drive (for example `NammaSpace/classroom_30s.mp4`), open the
Molab notebook as described in the main README, enter that path in **Video** and click **Start**. The smoke test
reconstructs the first 20 seconds with small settings; the full job then reconstructs the whole clip. A 30-second
clip covers only one corner of the room; the full 4 min 47 s video produced the published classroom.

For a local check of the pipeline's plumbing without a GPU (stand-in renderer, not gsplat):

```bash
python tests/run_local_pipeline.py tests/sample/classroom_30s.mp4 /tmp/namma-test
```

</file>

<file src="viewer/README.md">
# Namma Space viewer

Browser viewer for reconstructed rooms: Gaussian splat rendering (Aholo Viewer) with first-person walking on
the matching collision mesh (Recast/Detour). It also imports pipeline results and packages a room as a static
website.

Requirements: Node.js 18 or newer and Python 3.9 or newer (with tkinter for the desktop launcher).

```bash
cd viewer
npm ci          # installs Three.js, recast-navigation, Vite, splat-transform and the vendored Aholo package
```

## 1. Import a trained result

A finished Molab run leaves `result-<id>.zip.part001…` and `result-<id>.zip.parts.json` in
`DOWNLOAD_THIS/result-<id>/` (also on Google Drive). Keep the parts next to the `.parts.json`.

- **Windows:** double-click `Namma Pipeline.cmd` in the repository root and choose **1. Import a trained result**.
- **Any OS:** `python3 viewer/scripts/namma-pipeline.py` opens the same window, or import from the command line:

```bash
python3 viewer/scripts/scene-pipeline.py --geometry path/to/result-<id>.zip.parts.json --title "My room"
python3 viewer/scripts/namma-pipeline.py --open <scene id printed above>
```

The importer checks every part's size and SHA-256, converts the trained PLY to a compressed web model
(`preview.spz`), checks the collision mesh and writes the room to `data/scene-library/<id>/` (ignored by Git).
Google Drive sometimes renames `…part001` to `…part001.zip` when it downloads a folder; the importer accepts
either name (the SHA-256 check still applies).

## 2. Look around and walk

The viewer runs at `http://127.0.0.1:5174/aholo/?scene=<id>` (`npm run dev` starts it; the launcher does this
for you). Free flight: **WASD** to move, drag to look. To walk with collisions, open **Walking setup**:

1. **Load matching collision estimate**, then **Pick three floor points** on the floor.
2. Enter one real distance in metres and **Pick measurement endpoints** for it.
3. **Build walking surfaces**, tick the review box, **Pick a walking start**, and walk with **WASD** and the mouse.
4. **Download walking setup** saves the floor, scale and entrance for packaging.

For smooth playback on laptops with two GPUs, run the browser on the dedicated GPU (Windows: Settings > System >
Display > Graphics > your browser > High performance) and set **Display quality** to **Balanced**.

## 3. Package a browser demo

Choose **3. Package a browser demo** in the launcher (or run `npm run build`, then
`node scripts/package-aholo-scene.mjs --scene ../data/scene-library/<id>/scene.json --setup namma-walking-setup.json --output ../output/demo`).
The output folder is a static website: the viewer, `scene/{scene.json,preview.spz,collision.glb}`, the walking
setup and licence files. Host it on any static host (GitHub Pages, Netlify, Vercel); visitors click **Enter room**.

## Tests

```bash
npm test                                   # viewer, walking, packaging (Node test runner)
python3 test/scene-pipeline.test.py        # importer: part checks, unsafe archives, wrong model
```

</file>

<file src="viewer/THIRD_PARTY_NOTICES.md">
# Third-party components in the Namma Space viewer

The browser viewer, importer and demo packager build on these open-source components. Each keeps its own
licence; the demo packager copies the licence files of every runtime package into `licenses/`.

| Component | Role | Licence |
| --- | --- | --- |
| [Aholo Viewer](https://github.com/manycoretech/aholo-viewer) 1.10.0 (vendored in `vendor/`) | Gaussian splat rendering in the browser | MIT, copyright 2026 MANYCORE, INC. |
| [Three.js](https://github.com/mrdoob/three.js) 0.186 | Scene graph, cameras, GLB loading | MIT, three.js authors |
| [recast-navigation](https://github.com/isaac-mason/recast-navigation-js) 0.43 | Navigation mesh and collision for walking | MIT, Isaac Mason; upstream Recast/Detour: zlib |
| [PlayCanvas splat-transform](https://github.com/playcanvas/splat-transform) 3.10.1 (import only) | Converts the trained PLY to the compressed web format | MIT, PlayCanvas Ltd.; its dependencies include @adobe/spz (MIT) and meshoptimizer (MIT) |
| [Vite](https://github.com/vitejs/vite) 6 (build only) | Development server and production build | MIT |

Scenes (captured rooms) are not covered by these licences; they belong to whoever captured them.

</file>

<file src="viewer/aholo/AHOLO-LICENSE.txt">
The MIT License

Copyright © 2026 MANYCORE, INC.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

</file>

<file src="viewer/aholo/camera-control.ts">
interface CameraControlVector3 {
    x: number;
    y: number;
    z: number;
}

interface CameraControlEuler extends CameraControlVector3 {
    order?: string;
    set?: (x: number, y: number, z: number, order?: string) => unknown;
}

interface CameraControlQuaternion extends CameraControlVector3 {
    w: number;
}

interface CameraControlMatrix4 {
    _elements: Float32Array;
}

interface CameraControlCamera {
    position: CameraControlVector3;
    rotation: CameraControlEuler;
    up?: CameraControlVector3;
    quaternion?: CameraControlQuaternion;
}

interface CameraControlOptions {
    enabled?: boolean;
    keyboardEnabled?: boolean;
    pointerEnabled?: boolean;
    orbitEnabled?: boolean;
    useOrbit?: boolean;
    orbitCenter?: CameraControlVector3;
    orbitMinDistance?: number;
    moveSpeed?: number;
    lookSpeed?: number;
    wheelSpeed?: number;
    panSpeed?: number;
    rollSpeed?: number;
    shiftMultiplier?: number;
    ctrlMultiplier?: number;
    capsMultiplier?: number;
}

interface CameraControlState {
    position: CameraControlVector3;
    rotation: CameraControlVector3;
    moving: boolean;
    rotating: boolean;
    panning: boolean;
    orbiting: boolean;
    touching: boolean;
    interacting: boolean;
    speedMultiplier: number;
    activePointers: number;
    orbitCenter: CameraControlVector3;
    orbitDistance: number;
}

type PointerMode = 'rotate' | 'pan' | 'orbit';

interface PointerTrack {
    pointerId: number;
    pointerType: string;
    button: number;
    mode: PointerMode;
    lastX: number;
    lastY: number;
    x: number;
    y: number;
}

const DEFAULT_OPTIONS: Required<CameraControlOptions> = {
    enabled: true,
    keyboardEnabled: true,
    pointerEnabled: true,
    orbitEnabled: true,
    useOrbit: false,
    orbitCenter: { x: 0, y: 0, z: 0 },
    orbitMinDistance: 0.01,
    moveSpeed: 0.4,
    lookSpeed: 0.004,
    wheelSpeed: 0.006,
    panSpeed: 0.006,
    rollSpeed: 0,  // R/F would roll the horizon; the viewer keeps it level
    ctrlMultiplier: 2,
    shiftMultiplier: 3,
    capsMultiplier: 20,
};

const KEYBOARD_CONTROL_KEYS = new Set([
    'KeyW',
    'KeyA',
    'KeyS',
    'KeyD',
    'KeyQ',
    'KeyE',
    'KeyR',
    'KeyF',
    'ShiftLeft',
    'ShiftRight',
    'ControlLeft',
    'ControlRight',
    'AltLeft',
    'AltRight',
    'CapsLock',
]);

const MAX_PITCH = Math.PI / 2 - 0.001;
const EPSILON = 1e-6;
const DEFAULT_UP: CameraControlVector3 = { x: 0, y: 1, z: 0 };
const DEFAULT_ORBIT_CENTER: CameraControlVector3 = { x: 0, y: 0, z: 0 };

/**
 * Lightweight free-flight camera controls for website and Playground preview surfaces.
 */
export class CameraControl {
    enabled: boolean;
    keyboardEnabled: boolean;
    pointerEnabled: boolean;
    orbitEnabled: boolean;
    useOrbit: boolean;
    orbitMinDistance: number;
    moveSpeed: number;
    lookSpeed: number;
    wheelSpeed: number;
    panSpeed: number;
    rollSpeed: number;
    shiftMultiplier: number;
    ctrlMultiplier: number;
    capsMultiplier: number;

    readonly #camera: CameraControlCamera;
    readonly #element: HTMLElement;
    readonly #pointers = new Map<number, PointerTrack>();
    readonly #keys = new Set<string>();
    readonly #orbitCenter = copyVector(DEFAULT_ORBIT_CENTER);
    readonly #initialTabIndex: string | null;
    readonly #initialTouchAction: string;
    #lastTime = 0;
    #wheelDelta = 0;
    #capsLock = false;
    #altKey = false;
    #moving = false;
    #rotating = false;
    #panning = false;
    #orbiting = false;
    #disposed = false;

    constructor(camera: CameraControlCamera, element: HTMLElement, options: CameraControlOptions = {}) {
        this.#camera = camera;
        this.#element = element;
        this.#initialTabIndex = element.getAttribute('tabindex');
        this.#initialTouchAction = element.style.touchAction;

        const resolved = {
            ...DEFAULT_OPTIONS,
            ...options,
        };

        this.enabled = resolved.enabled;
        this.keyboardEnabled = resolved.keyboardEnabled;
        this.pointerEnabled = resolved.pointerEnabled;
        this.orbitEnabled = resolved.orbitEnabled;
        this.useOrbit = resolved.useOrbit;
        this.orbitMinDistance = Math.max(EPSILON, resolved.orbitMinDistance);
        this.setOrbitCenter(resolved.orbitCenter);
        this.moveSpeed = resolved.moveSpeed;
        this.lookSpeed = resolved.lookSpeed;
        this.wheelSpeed = resolved.wheelSpeed;
        this.panSpeed = resolved.panSpeed;
        this.rollSpeed = resolved.rollSpeed;
        this.shiftMultiplier = resolved.shiftMultiplier;
        this.ctrlMultiplier = resolved.ctrlMultiplier;
        this.capsMultiplier = resolved.capsMultiplier;

        if (this.#initialTabIndex === null) {
            element.tabIndex = 0;
        }

        element.style.touchAction = 'none';
        element.addEventListener('pointerdown', this.#onPointerDown);
        element.addEventListener('pointermove', this.#onPointerMove);
        element.addEventListener('pointerup', this.#onPointerUp);
        element.addEventListener('pointercancel', this.#onPointerUp);
        element.addEventListener('contextmenu', this.#onContextMenu);
        element.addEventListener('wheel', this.#onWheel, { passive: false });
        element.addEventListener('keydown', this.#onKeyDown);
        element.addEventListener('keyup', this.#onKeyUp);
        window.addEventListener('keyup', this.#onKeyUp);
        window.addEventListener('blur', this.#onBlur);
    }

    setOptions(options: CameraControlOptions) {
        const { orbitCenter, ...rest } = options;

        if (orbitCenter !== undefined) {
            this.setOrbitCenter(orbitCenter);
        }

        for (const [key, value] of Object.entries(rest)) {
            if (value !== undefined) {
                if (key === 'orbitMinDistance' && typeof value === 'number') {
                    this.orbitMinDistance = Math.max(EPSILON, value);
                } else {
                    (this as unknown as Record<string, unknown>)[key] = value;
                }
            }
        }
    }

    setOrbitCenter(center: CameraControlVector3) {
        this.#orbitCenter.x = center.x;
        this.#orbitCenter.y = center.y;
        this.#orbitCenter.z = center.z;
    }

    stop() {
        for (const pointer of this.#pointers.values()) {
            if (this.#element.hasPointerCapture(pointer.pointerId)) {
                this.#element.releasePointerCapture(pointer.pointerId);
            }
        }

        this.#keys.clear();
        this.#pointers.clear();
        this.#wheelDelta = 0;
        this.#altKey = false;
        this.#moving = false;
        this.#rotating = false;
        this.#panning = false;
        this.#orbiting = false;
    }

    update(deltaSeconds?: number) {
        if (this.#disposed || !this.enabled) {
            return false;
        }

        const now = performance.now();
        const delta = deltaSeconds ?? Math.min((now - (this.#lastTime || now)) / 1000, 0.1);
        this.#lastTime = now;

        const pointerChanged = this.pointerEnabled ? this.#updatePointers() : false;
        const keyboardChanged = this.keyboardEnabled ? this.#updateKeyboard(delta) : false;
        const wheelChanged = this.pointerEnabled ? this.#updateWheel() : false;

        return pointerChanged || keyboardChanged || wheelChanged;
    }

    getState(): CameraControlState {
        const position = this.#camera.position;
        const rotation = this.#camera.rotation;
        const touching = Array.from(this.#pointers.values()).some(pointer => pointer.pointerType === 'touch');
        const interacting =
            this.#moving || this.#rotating || this.#panning || this.#orbiting || this.#pointers.size > 0;

        return {
            position: { x: position.x, y: position.y, z: position.z },
            rotation: { x: rotation.x, y: rotation.y, z: rotation.z },
            moving: this.#moving,
            rotating: this.#rotating,
            panning: this.#panning,
            orbiting: this.#orbiting,
            touching,
            interacting,
            speedMultiplier: this.#getSpeedMultiplier(),
            activePointers: this.#pointers.size,
            orbitCenter: copyVector(this.#orbitCenter),
            orbitDistance: this.#getOrbitDistance(),
        };
    }

    dispose() {
        if (this.#disposed) {
            return;
        }

        this.stop();
        this.#disposed = true;
        this.#element.removeEventListener('pointerdown', this.#onPointerDown);
        this.#element.removeEventListener('pointermove', this.#onPointerMove);
        this.#element.removeEventListener('pointerup', this.#onPointerUp);
        this.#element.removeEventListener('pointercancel', this.#onPointerUp);
        this.#element.removeEventListener('contextmenu', this.#onContextMenu);
        this.#element.removeEventListener('wheel', this.#onWheel);
        this.#element.removeEventListener('keydown', this.#onKeyDown);
        this.#element.removeEventListener('keyup', this.#onKeyUp);
        window.removeEventListener('keyup', this.#onKeyUp);
        window.removeEventListener('blur', this.#onBlur);
        this.#element.style.touchAction = this.#initialTouchAction;

        if (this.#initialTabIndex === null) {
            this.#element.removeAttribute('tabindex');
        } else {
            this.#element.setAttribute('tabindex', this.#initialTabIndex);
        }
    }

    #onPointerDown = (event: PointerEvent) => {
        if (!this.enabled || !this.pointerEnabled) {
            return;
        }

        this.#element.focus({ preventScroll: true });
        this.#altKey = event.altKey;
        this.#pointers.set(event.pointerId, {
            pointerId: event.pointerId,
            pointerType: event.pointerType,
            button: event.button,
            mode: this.#getPointerMode(event.pointerType, event.button),
            lastX: event.clientX,
            lastY: event.clientY,
            x: event.clientX,
            y: event.clientY,
        });
        this.#element.setPointerCapture(event.pointerId);
        event.preventDefault();
    };

    #onPointerMove = (event: PointerEvent) => {
        const pointer = this.#pointers.get(event.pointerId);

        if (!pointer) {
            return;
        }

        this.#altKey = event.altKey;
        pointer.x = event.clientX;
        pointer.y = event.clientY;
        event.preventDefault();
    };

    #onPointerUp = (event: PointerEvent) => {
        if (this.#pointers.has(event.pointerId)) {
            this.#pointers.delete(event.pointerId);

            if (this.#element.hasPointerCapture(event.pointerId)) {
                this.#element.releasePointerCapture(event.pointerId);
            }

            if (this.#pointers.size === 0) {
                this.#rotating = false;
                this.#panning = false;
                this.#orbiting = false;
            }
        }
    };

    #onContextMenu = (event: MouseEvent) => {
        event.preventDefault();
    };

    #onWheel = (event: WheelEvent) => {
        if (!this.enabled || !this.pointerEnabled) {
            return;
        }

        this.#wheelDelta += event.deltaY;
        event.preventDefault();
    };

    #onKeyDown = (event: KeyboardEvent) => {
        if (!this.enabled || !this.keyboardEnabled || !KEYBOARD_CONTROL_KEYS.has(event.code)) {
            return;
        }

        this.#keys.add(event.code);
        this.#capsLock = event.getModifierState('CapsLock');
        this.#altKey = event.altKey || event.code === 'AltLeft' || event.code === 'AltRight';
        event.preventDefault();
    };

    #onKeyUp = (event: KeyboardEvent) => {
        this.#keys.delete(event.code);
        this.#capsLock = event.getModifierState('CapsLock');
        this.#altKey = event.altKey;
    };

    #onBlur = () => {
        this.stop();
    };

    #updatePointers() {
        const pointers = Array.from(this.#pointers.values());
        this.#rotating = false;
        this.#panning = false;
        this.#orbiting = false;

        if (pointers.length === 0) {
            return false;
        }

        let updated = false;

        if (pointers.length >= 2) {
            const first = pointers[0];
            const second = pointers[1];
            const lastMidX = (first.lastX + second.lastX) * 0.5;
            const lastMidY = (first.lastY + second.lastY) * 0.5;
            const midX = (first.x + second.x) * 0.5;
            const midY = (first.y + second.y) * 0.5;
            const lastDistance = distance(first.lastX, first.lastY, second.lastX, second.lastY);
            const currentDistance = distance(first.x, first.y, second.x, second.y);
            const panX = midX - lastMidX;
            const panY = midY - lastMidY;
            const pinch = currentDistance - lastDistance;

            updated = this.#panByPixels(panX, panY) || updated;
            updated = this.#moveAlongView(pinch * this.wheelSpeed) || updated;
            this.#panning = Math.abs(panX) + Math.abs(panY) + Math.abs(pinch) > 0.001;
        } else {
            const pointer = pointers[0];
            const mode = this.#getPointerMode(pointer.pointerType, pointer.button);

            if (pointer.mode !== mode) {
                pointer.mode = mode;
                pointer.lastX = pointer.x;
                pointer.lastY = pointer.y;
            }

            const deltaX = pointer.x - pointer.lastX;
            const deltaY = pointer.y - pointer.lastY;

            if (mode === 'pan') {
                updated = this.#panByPixels(deltaX, deltaY);
                this.#panning = updated;
            } else if (mode === 'orbit') {
                updated = this.#orbitByPixels(deltaX, deltaY);
                this.#orbiting = true;
            } else {
                updated = this.#rotateByPixels(deltaX, deltaY);
                this.#rotating = updated;
            }
        }

        for (const pointer of pointers) {
            pointer.lastX = pointer.x;
            pointer.lastY = pointer.y;
        }

        return updated;
    }

    #updateKeyboard(deltaSeconds: number) {
        const forwardInput = numberFromKey(this.#keys, 'KeyW') - numberFromKey(this.#keys, 'KeyS');
        const strafeInput = numberFromKey(this.#keys, 'KeyD') - numberFromKey(this.#keys, 'KeyA');
        const verticalInput = numberFromKey(this.#keys, 'KeyQ') - numberFromKey(this.#keys, 'KeyE');
        const rollInput = numberFromKey(this.#keys, 'KeyR') - numberFromKey(this.#keys, 'KeyF');
        const multiplier = this.#getSpeedMultiplier();
        let updated = false;

        const movementLength = Math.hypot(forwardInput, strafeInput, verticalInput);
        this.#moving = movementLength > 0;

        if (movementLength > 0) {
            const scale = (this.moveSpeed * multiplier * deltaSeconds) / Math.max(1, movementLength);
            const basis = getCameraBasis(this.#camera);
            const position = this.#camera.position;

            position.x +=
                (basis.forward.x * forwardInput + basis.right.x * strafeInput + basis.up.x * verticalInput) * scale;
            position.y +=
                (basis.forward.y * forwardInput + basis.right.y * strafeInput + basis.up.y * verticalInput) * scale;
            position.z +=
                (basis.forward.z * forwardInput + basis.right.z * strafeInput + basis.up.z * verticalInput) * scale;
            updated = true;
        }

        if (rollInput !== 0) {
            rollCamera(this.#camera, rollInput * this.rollSpeed * deltaSeconds);
            this.#rotating = true;
            updated = true;
        } else if (this.#pointers.size === 0) {
            this.#rotating = false;
        }

        return updated;
    }

    #updateWheel() {
        if (Math.abs(this.#wheelDelta) < 0.001) {
            return false;
        }

        const delta = -this.#wheelDelta * this.wheelSpeed;
        this.#wheelDelta = 0;
        return this.#moveAlongView(delta);
    }

    #rotateByPixels(deltaX: number, deltaY: number) {
        if (Math.abs(deltaX) + Math.abs(deltaY) < 0.001) {
            return false;
        }

        rotateCamera(this.#camera, -deltaX * this.lookSpeed, -deltaY * this.lookSpeed);
        return true;
    }

    #orbitByPixels(deltaX: number, deltaY: number) {
        if (Math.abs(deltaX) + Math.abs(deltaY) < 0.001) {
            return false;
        }

        return orbitCamera(
            this.#camera,
            this.#orbitCenter,
            -deltaX * this.lookSpeed,
            -deltaY * this.lookSpeed,
            this.orbitMinDistance,
        );
    }

    #panByPixels(deltaX: number, deltaY: number) {
        if (Math.abs(deltaX) + Math.abs(deltaY) < 0.001) {
            return false;
        }

        const basis = getCameraBasis(this.#camera);
        const position = this.#camera.position;
        const x = deltaX * this.panSpeed;
        const y = -deltaY * this.panSpeed;

        position.x += basis.right.x * x + basis.viewUp.x * y;
        position.y += basis.right.y * x + basis.viewUp.y * y;
        position.z += basis.right.z * x + basis.viewUp.z * y;
        return true;
    }

    #moveAlongView(distanceValue: number) {
        if (Math.abs(distanceValue) < 0.001) {
            return false;
        }

        const forward = getCameraBasis(this.#camera).forward;
        const position = this.#camera.position;
        position.x += forward.x * distanceValue;
        position.y += forward.y * distanceValue;
        position.z += forward.z * distanceValue;
        return true;
    }

    #getSpeedMultiplier() {
        let multiplier = 1;

        if (this.#keys.has('ShiftLeft') || this.#keys.has('ShiftRight')) {
            multiplier *= this.shiftMultiplier;
        }

        if (this.#keys.has('ControlLeft') || this.#keys.has('ControlRight')) {
            multiplier *= this.ctrlMultiplier;
        }

        if (this.#capsLock || this.#keys.has('CapsLock')) {
            multiplier *= this.capsMultiplier;
        }

        return multiplier;
    }

    #getPointerMode(pointerType: string, button: number): PointerMode {
        if (pointerType === 'mouse') {
            if (button === 1 || button === 2) {
                return 'pan';
            }

            if (button === 0 && this.orbitEnabled && (this.useOrbit || this.#isOrbitModifierActive())) {
                return 'orbit';
            }
        }

        return 'rotate';
    }

    #isOrbitModifierActive() {
        return this.#altKey || this.#keys.has('AltLeft') || this.#keys.has('AltRight');
    }

    #getOrbitDistance() {
        return lengthVector(subtractVectors(this.#camera.position, this.#orbitCenter));
    }
}

function rotateCamera(camera: CameraControlCamera, yawDelta: number, pitchDelta: number) {
    const basis = getCameraBasis(camera);
    const orientation = getCameraOrientationBasis(camera);
    const rollAngle = getForwardAxisRoll(orientation.forward, orientation.up, orientation.viewUp);
    const currentPitch = Math.asin(clamp(dotVector(basis.forward, basis.up), -1, 1));
    const nextPitch = clamp(currentPitch + pitchDelta, -MAX_PITCH, MAX_PITCH);
    const horizontalForward =
        normalizeVector(projectOnPlane(basis.forward, basis.up)) ?? getPerpendicularUnit(basis.up);
    const yawedForward = rotateVectorAroundAxis(horizontalForward, basis.up, yawDelta);
    const forward = normalizeVector(
        addVectors(multiplyVector(yawedForward, Math.cos(nextPitch)), multiplyVector(basis.up, Math.sin(nextPitch))),
    );

    if (!forward) {
        return;
    }

    setCameraLookBasis(camera, forward, getViewUpWithRoll(forward, basis.up, rollAngle));
}

function orbitCamera(
    camera: CameraControlCamera,
    center: CameraControlVector3,
    yawDelta: number,
    pitchDelta: number,
    minDistance: number,
) {
    const basis = getCameraBasis(camera);
    const orientation = getCameraOrientationBasis(camera);
    const rollAngle = getForwardAxisRoll(orientation.forward, orientation.up, orientation.viewUp);
    const safeMinDistance = Math.max(EPSILON, minDistance);
    let distanceValue = lengthVector(subtractVectors(camera.position, center));
    let forward = normalizeVector(subtractVectors(center, camera.position)) ??
        normalizeVector(orientation.forward) ?? { x: 0, y: 0, z: -1 };

    if (distanceValue < safeMinDistance) {
        distanceValue = safeMinDistance;
        forward = normalizeVector(orientation.forward) ?? forward;
    }

    const currentPitch = Math.asin(clamp(dotVector(forward, basis.up), -1, 1));
    const nextPitch = clamp(currentPitch + pitchDelta, -MAX_PITCH, MAX_PITCH);
    const horizontalForward = normalizeVector(projectOnPlane(forward, basis.up)) ?? getPerpendicularUnit(basis.up);
    const yawedForward = rotateVectorAroundAxis(horizontalForward, basis.up, yawDelta);
    const nextForward = normalizeVector(
        addVectors(multiplyVector(yawedForward, Math.cos(nextPitch)), multiplyVector(basis.up, Math.sin(nextPitch))),
    );

    if (!nextForward) {
        return false;
    }

    camera.position.x = center.x - nextForward.x * distanceValue;
    camera.position.y = center.y - nextForward.y * distanceValue;
    camera.position.z = center.z - nextForward.z * distanceValue;
    setCameraLookBasis(camera, nextForward, getViewUpWithRoll(nextForward, basis.up, rollAngle));
    return true;
}

function rollCamera(camera: CameraControlCamera, rollDelta: number) {
    const basis = getCameraOrientationBasis(camera);
    const viewUp = normalizeVector(rotateVectorAroundAxis(basis.viewUp, basis.forward, -rollDelta));

    if (!viewUp) {
        return;
    }

    setCameraLookBasis(camera, basis.forward, viewUp);
}

function getCameraBasis(camera: CameraControlCamera) {
    const orientation = getCameraOrientationBasis(camera);
    const right = normalizeVector(crossVectors(orientation.forward, orientation.up)) ?? orientation.right;
    const viewUp = normalizeVector(crossVectors(right, orientation.forward)) ?? orientation.viewUp;

    return {
        forward: orientation.forward,
        right,
        up: orientation.up,
        viewUp,
    };
}

function getCameraOrientationBasis(camera: CameraControlCamera) {
    const up = getCameraUp(camera);
    const matrix = getCameraRotationMatrix(camera);
    const elements = matrix._elements;
    const forward = normalizeVector({
        x: -elements[8],
        y: -elements[9],
        z: -elements[10],
    }) ?? { x: 0, y: 0, z: -1 };
    const matrixRight =
        normalizeVector({
            x: elements[0],
            y: elements[1],
            z: elements[2],
        }) ?? getPerpendicularUnit(up);
    const viewUp =
        normalizeVector({
            x: elements[4],
            y: elements[5],
            z: elements[6],
        }) ??
        normalizeVector(crossVectors(matrixRight, forward)) ??
        up;

    return {
        forward,
        right: matrixRight,
        up,
        viewUp,
    };
}

function getForwardAxisRoll(forward: CameraControlVector3, up: CameraControlVector3, viewUp: CameraControlVector3) {
    const levelViewUp = getViewUpWithRoll(forward, up, 0);
    return angleAroundAxis(levelViewUp, viewUp, forward);
}

function getViewUpWithRoll(forward: CameraControlVector3, up: CameraControlVector3, rollAngle: number) {
    const right = normalizeVector(crossVectors(forward, up)) ?? getPerpendicularUnit(forward);
    const viewUp = normalizeVector(crossVectors(right, forward)) ?? up;
    return normalizeVector(rotateVectorAroundAxis(viewUp, forward, rollAngle)) ?? viewUp;
}

function setCameraLookBasis(camera: CameraControlCamera, forward: CameraControlVector3, up: CameraControlVector3) {
    const right = normalizeVector(crossVectors(forward, up)) ?? getPerpendicularUnit(up);
    const viewUp = normalizeVector(crossVectors(right, forward)) ?? up;
    const back = multiplyVector(forward, -1);
    const matrix = makeBasisMatrix(right, viewUp, back);
    const rotation = camera.rotation;
    const matrixRotation = rotation as CameraControlEuler & {
        setFromRotationMatrix?: (matrix: CameraControlMatrix4, order?: string) => unknown;
    };

    if (typeof matrixRotation.setFromRotationMatrix === 'function') {
        matrixRotation.setFromRotationMatrix(matrix, rotation.order);
        return;
    }

    const euler = getEulerFromRotationMatrix(matrix, rotation.order ?? 'XYZ');

    if (typeof rotation.set === 'function') {
        rotation.set(euler.x, euler.y, euler.z, euler.order);
    } else {
        rotation.x = euler.x;
        rotation.y = euler.y;
        rotation.z = euler.z;
    }
}

function getCameraUp(camera: CameraControlCamera) {
    return normalizeVector(camera.up ?? DEFAULT_UP) ?? DEFAULT_UP;
}

function getCameraRotationMatrix(camera: CameraControlCamera) {
    if (camera.quaternion) {
        return makeRotationMatrixFromQuaternion(camera.quaternion);
    }

    return makeRotationMatrixFromEuler(camera.rotation);
}

function makeRotationMatrixFromQuaternion(quaternion: CameraControlQuaternion): CameraControlMatrix4 {
    const { x, y, z, w } = quaternion;
    const x2 = x + x;
    const y2 = y + y;
    const z2 = z + z;
    const xx = x * x2;
    const xy = x * y2;
    const xz = x * z2;
    const yy = y * y2;
    const yz = y * z2;
    const zz = z * z2;
    const wx = w * x2;
    const wy = w * y2;
    const wz = w * z2;

    return makeMatrix([
        1 - (yy + zz),
        xy + wz,
        xz - wy,
        0,
        xy - wz,
        1 - (xx + zz),
        yz + wx,
        0,
        xz + wy,
        yz - wx,
        1 - (xx + yy),
        0,
        0,
        0,
        0,
        1,
    ]);
}

function makeRotationMatrixFromEuler(rotation: CameraControlEuler): CameraControlMatrix4 {
    const x = rotation.x;
    const y = rotation.y;
    const z = rotation.z;
    const a = Math.cos(x);
    const b = Math.sin(x);
    const c = Math.cos(y);
    const d = Math.sin(y);
    const e = Math.cos(z);
    const f = Math.sin(z);
    const ae = a * e;
    const af = a * f;
    const be = b * e;
    const bf = b * f;

    return makeMatrix([
        c * e,
        af + be * d,
        bf - ae * d,
        0,
        -c * f,
        ae - bf * d,
        be + af * d,
        0,
        d,
        -b * c,
        a * c,
        0,
        0,
        0,
        0,
        1,
    ]);
}

function makeBasisMatrix(
    xAxis: CameraControlVector3,
    yAxis: CameraControlVector3,
    zAxis: CameraControlVector3,
): CameraControlMatrix4 {
    return makeMatrix([
        xAxis.x,
        xAxis.y,
        xAxis.z,
        0,
        yAxis.x,
        yAxis.y,
        yAxis.z,
        0,
        zAxis.x,
        zAxis.y,
        zAxis.z,
        0,
        0,
        0,
        0,
        1,
    ]);
}

function makeMatrix(elements: number[]): CameraControlMatrix4 {
    return {
        _elements: Float32Array.from(elements),
    };
}

function getEulerFromRotationMatrix(matrix: CameraControlMatrix4, order: string) {
    const te = matrix._elements;
    const m11 = te[0];
    const m12 = te[4];
    const m13 = te[8];
    const m23 = te[9];
    const m33 = te[10];
    const euler = {
        x: 0,
        y: Math.asin(clamp(m13, -1, 1)),
        z: 0,
        order,
    };

    if (Math.abs(m13) < 0.99999) {
        euler.x = Math.atan2(-m23, m33);
        euler.z = Math.atan2(-m12, m11);
    } else {
        const m22 = te[5];
        const m32 = te[6];
        euler.x = Math.atan2(m32, m22);
    }

    return euler;
}

function projectOnPlane(vector: CameraControlVector3, normal: CameraControlVector3) {
    return subtractVectors(vector, multiplyVector(normal, dotVector(vector, normal)));
}

function angleAroundAxis(from: CameraControlVector3, to: CameraControlVector3, axis: CameraControlVector3) {
    const projectedFrom = normalizeVector(projectOnPlane(from, axis));
    const projectedTo = normalizeVector(projectOnPlane(to, axis));

    if (!projectedFrom || !projectedTo) {
        return 0;
    }

    return Math.atan2(dotVector(crossVectors(projectedFrom, projectedTo), axis), dotVector(projectedFrom, projectedTo));
}

function rotateVectorAroundAxis(vector: CameraControlVector3, axis: CameraControlVector3, angle: number) {
    const cos = Math.cos(angle);
    const sin = Math.sin(angle);
    const cross = crossVectors(axis, vector);
    const axisScale = dotVector(axis, vector) * (1 - cos);

    return addVectors(
        addVectors(multiplyVector(vector, cos), multiplyVector(cross, sin)),
        multiplyVector(axis, axisScale),
    );
}

function getPerpendicularUnit(axis: CameraControlVector3) {
    const helper = Math.abs(axis.y) < 0.9 ? { x: 0, y: 1, z: 0 } : { x: 1, y: 0, z: 0 };
    return normalizeVector(crossVectors(axis, helper)) ?? { x: 1, y: 0, z: 0 };
}

function addVectors(a: CameraControlVector3, b: CameraControlVector3) {
    return {
        x: a.x + b.x,
        y: a.y + b.y,
        z: a.z + b.z,
    };
}

function subtractVectors(a: CameraControlVector3, b: CameraControlVector3) {
    return {
        x: a.x - b.x,
        y: a.y - b.y,
        z: a.z - b.z,
    };
}

function multiplyVector(vector: CameraControlVector3, scale: number) {
    return {
        x: vector.x * scale,
        y: vector.y * scale,
        z: vector.z * scale,
    };
}

function copyVector(vector: CameraControlVector3) {
    return {
        x: vector.x,
        y: vector.y,
        z: vector.z,
    };
}

function lengthVector(vector: CameraControlVector3) {
    return Math.hypot(vector.x, vector.y, vector.z);
}

function dotVector(a: CameraControlVector3, b: CameraControlVector3) {
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

function crossVectors(a: CameraControlVector3, b: CameraControlVector3) {
    return {
        x: a.y * b.z - a.z * b.y,
        y: a.z * b.x - a.x * b.z,
        z: a.x * b.y - a.y * b.x,
    };
}

function normalizeVector(vector: CameraControlVector3) {
    const length = Math.hypot(vector.x, vector.y, vector.z);

    if (length < EPSILON) {
        return undefined;
    }

    return {
        x: vector.x / length,
        y: vector.y / length,
        z: vector.z / length,
    };
}

function numberFromKey(keys: Set<string>, code: string) {
    return keys.has(code) ? 1 : 0;
}

function distance(x1: number, y1: number, x2: number, y2: number) {
    return Math.hypot(x2 - x1, y2 - y1);
}

function clamp(value: number, minimum: number, maximum: number) {
    return Math.min(Math.max(value, minimum), maximum);
}

</file>

<file src="viewer/aholo/index.html">
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Namma Space · ruakpeedkahem (rpk) · NIT Goa</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="./style.css" />
  </head>
  <body>
    <div id="app">
<div class="namma-status">Namma Space by team ruakpeedkahem (rpk): Akarsh Shrivastav, Mayan S Hiremath · NIT Goa · Powered by Aholo · <span id="walk-status">Explore the reconstruction · Open Walking setup to enter.</span></div>
      <!-- 3D Canvas Container -->
      <div id="viewer-container" tabindex="0"></div>

      <!-- Top Floating Navigation -->
      <header class="top-bar">
        <div class="top-bar-left">
          <div class="brand-badge glass-panel">
            <div class="brand-logo">
              <svg viewBox="0 0 24 24">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
              </svg>
            </div>
            <span class="brand-text">Namma Space</span>
          </div>

          <div class="file-info-badge glass-panel">
            <span id="file-status-dot" class="file-status-dot loading"></span>
            <span id="file-name">Choose a room file</span>
            <span id="splat-count" style="color: var(--text-muted); font-size: 11px;">(Loading...)</span>
          </div>
        </div>

        <div class="top-bar-right">
          <div class="stats-badge glass-panel">
            <div class="stat-item">
              <span>Draws/s:</span>
              <span id="stat-fps" class="stat-val">--</span>
            </div>
            <div class="stat-item">
              <span>Submit:</span>
              <span id="stat-ms" class="stat-val">-- ms</span>
            </div>
          </div>

          <input type="file" id="file-input" accept=".ply,.splat,.sog,.spz" style="display: none;" />
          <button id="btn-upload" class="btn" title="Open local PLY/3DGS file">
            <svg viewBox="0 0 24 24">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="17 8 12 3 7 8"></polyline>
              <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
            <span>Open File</span>
          </button>

          <button id="btn-reset" class="btn" title="Reset Camera View (R)">
            <svg viewBox="0 0 24 24">
              <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
              <polyline points="3 3 3 8 8 8"></polyline>
            </svg>
            <span>Reset</span>
          </button>

          <button id="btn-auto-rotate" class="btn" title="Toggle Turntable Rotation">
            <svg viewBox="0 0 24 24">
              <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/>
            </svg>
            <span>Turntable</span>
          </button>

          <button id="btn-settings" class="btn btn-icon" title="Toggle Settings Panel">
            <svg viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
          </button>
        </div>
      </header>

      <!-- Sidebar / Settings Panel -->
      <aside id="sidebar" class="sidebar glass-panel">
        <div class="sidebar-header">
          <div class="sidebar-title">
            <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" fill="none" stroke-width="2">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
            <span>Viewer Controls</span>
          </div>
          <button id="btn-close-sidebar" class="btn btn-icon" style="width: 26px; height: 26px; border: none; background: transparent;">
            <svg viewBox="0 0 24 24">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <!-- Camera Section -->
        <div class="section-group">
          <span class="section-label">Camera & Coordinate System</span>
          
          <div class="control-row">
            <span>Coordinates</span>
            <select id="select-coord" class="select-input">
              <option value="opencv" selected>OpenCV (-Y Up)</option>
              <option value="opengl">OpenGL (+Y Up)</option>
              <option value="aholo">Aholo (+Z Up)</option>
            </select>
          </div>

          <div class="control-row">
            <span>Camera Mode</span>
            <select id="select-camera-mode" class="select-input">
              <option value="orbit">Orbit / Turntable</option>
              <option value="flight" selected>Free Flight (WASD)</option>
            </select>
          </div>

          <div class="control-row" style="flex-direction: column; align-items: flex-start; gap: 6px;">
            <div style="display: flex; justify-content: space-between; width: 100%;">
              <span>FOV</span>
              <span id="val-fov" class="range-val">68°</span>
            </div>
            <div class="range-container">
              <input type="range" id="range-fov" class="range-input" min="30" max="100" value="68" />
            </div>
          </div>

          <div class="control-row" style="flex-direction: column; align-items: flex-start; gap: 6px;">
            <div style="display: flex; justify-content: space-between; width: 100%;">
              <span>Movement Speed</span>
              <span id="val-speed" class="range-val">0.05x</span>
            </div>
            <div class="range-container">
              <input type="range" id="range-speed" class="range-input" min="0.05" max="4.0" step="0.05" value="0.05" />
            </div>
          </div>
        </div>

        <!-- Environment & Background -->
        <div class="section-group">
          <span class="section-label">Environment</span>
          
          <div class="control-row">
            <span>Background</span>
            <div class="color-options">
              <button class="color-btn active" data-color="#0b0f17" style="background: #0b0f17;" title="Dark Slate"></button>
              <button class="color-btn" data-color="#000000" style="background: #000000;" title="Pitch Black"></button>
              <button class="color-btn" data-color="#1f2430" style="background: #1f2430;" title="Studio Gray"></button>
              <button class="color-btn" data-color="#f8fafc" style="background: #f8fafc;" title="Pure White"></button>
            </div>
          </div>
        </div>

        <!-- Splatting Pipeline -->
        <div class="section-group">
          <span class="section-label">Rendering & Pipeline</span>
            <label class="control-row">Display quality
              <select id="performance-mode" class="select-input">
                <option value="balanced">Balanced</option>
                <option value="performance">Performance</option>
                <option value="auto">Auto · target 60 FPS</option>
                <option value="native" selected>Native resolution</option>
              </select>
            </label>
            <p id="resolution-status">100% of CSS resolution</p>
            <p id="frame-pacing" style="font-size:12px">Move to measure frame pacing; idle is not low FPS.</p>
            <button id="download-performance" class="btn">Download performance report</button>
            <p style="font-size:12px">Lower resolution reduces sharpness to improve speed. Auto targets 60 FPS; it cannot guarantee it.</p>
          
          <div class="control-row">
            <span>Splatting Enabled</span>
            <label class="switch">
              <input type="checkbox" id="toggle-splatting" checked />
              <span class="slider"></span>
            </label>
          </div>

          <div class="control-row">
            <span>Precalculate</span>
            <label class="switch">
              <input type="checkbox" id="toggle-precalculate" checked />
              <span class="slider"></span>
            </label>
          </div>

          <div class="control-row">
            <span>Tone Mapping</span>
            <select id="select-tone" class="select-input">
              <option value="linear" selected>Linear</option>
              <option value="reinhard">Reinhard</option>
              <option value="neutral">Neutral</option>
              <option value="aces">ACES</option>
              <option value="acesFilmic">ACES Filmic</option>
            </select>
          </div>

          <div class="control-row" style="flex-direction: column; align-items: flex-start; gap: 6px;">
            <div style="display: flex; justify-content: space-between; width: 100%;">
              <span>Exposure</span>
              <span id="val-exposure" class="range-val">1.0</span>
            </div>
            <div class="range-container">
              <input type="range" id="range-exposure" class="range-input" min="0.2" max="3.0" step="0.1" value="1.0" />
            </div>
          </div>
        </div>

        <!-- Splat Info Summary -->
        <div class="section-group" style="border-top: 1px solid var(--border-color); padding-top: 12px;">
          <span class="section-label">Dataset Info</span>
          <div class="control-row">
            <span>Splats:</span>
            <span id="info-splats" class="stat-val">—</span>
          </div>
          <div class="control-row">
            <span>Format:</span>
            <span id="info-format" class="stat-val">—</span>
          </div>
          <div class="control-row">
            <span>File Size:</span>
            <span id="info-size" class="stat-val">—</span>
          </div>
        </div>
      </aside>

      <!-- Bottom Hint Bar -->
      <footer class="bottom-bar glass-panel">
        <div class="help-shortcut">
          <span class="kbd">L-Click</span>
          <span>Orbit</span>
        </div>
        <div class="help-shortcut">
          <span class="kbd">R-Click</span>
          <span>Pan</span>
        </div>
        <div class="help-shortcut">
          <span class="kbd">Scroll</span>
          <span>Zoom</span>
        </div>
        <div class="help-shortcut">
          <span class="kbd">R</span>
          <span>Reset</span>
        </div>
      </footer>

      <!-- Drag & Drop Zone -->
      <div id="drag-overlay" class="drag-overlay">
        <div class="drag-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
          </svg>
        </div>
        <div class="drag-title">Drop your 3D Gaussian Splat file here</div>
        <div class="drag-subtitle">Supports .ply, .splat, .sog, and .spz</div>
      </div>

      <!-- Loading Overlay -->
      <div id="loading-overlay" class="loading-overlay">
        <div class="spinner"></div>
        <div id="loading-title" class="loading-title">Loading room...</div>
        <div id="loading-subtitle" class="loading-subtitle">Decompressing and parsing 3D Gaussian Splats</div>
      </div>

      <!-- Toast Notification -->
      <div id="toast" class="toast"></div>
    </div>

    <script type="module" src="./index.ts"></script>
  </body>
</html>

</file>

<file src="viewer/aholo/index.ts">
import {
    createViewer,
    setViewerConfig,
    PerspectiveCamera,
    BackgroundMode,
    Vector3,
    Color,
    SplatLoader,
    SplatUtils,
    ToneMapping,
} from '@manycore/aholo-viewer';
import { CameraControl } from './camera-control.js';
import {createWalkingTools} from './walking-tools.js';
import {ResolutionBudget} from './performance.js';
import {validateViewerManifest} from './saved-walk.js';

// DOM Elements
const container = document.getElementById('viewer-container') as HTMLElement;
const loadingOverlay = document.getElementById('loading-overlay') as HTMLElement;
const loadingTitle = document.getElementById('loading-title') as HTMLElement;
const loadingSubtitle = document.getElementById('loading-subtitle') as HTMLElement;
const fileStatusDot = document.getElementById('file-status-dot') as HTMLElement;
const fileNameEl = document.getElementById('file-name') as HTMLElement;
const splatCountEl = document.getElementById('splat-count') as HTMLElement;
const statFps = document.getElementById('stat-fps') as HTMLElement;
const statMs = document.getElementById('stat-ms') as HTMLElement;
const btnUpload = document.getElementById('btn-upload') as HTMLButtonElement;
const fileInput = document.getElementById('file-input') as HTMLInputElement;
const btnReset = document.getElementById('btn-reset') as HTMLButtonElement;
const btnAutoRotate = document.getElementById('btn-auto-rotate') as HTMLButtonElement;
const btnSettings = document.getElementById('btn-settings') as HTMLButtonElement;
const btnCloseSidebar = document.getElementById('btn-close-sidebar') as HTMLButtonElement;
const sidebar = document.getElementById('sidebar') as HTMLElement;
const selectCoord = document.getElementById('select-coord') as HTMLSelectElement;
const selectCameraMode = document.getElementById('select-camera-mode') as HTMLSelectElement;
const rangeFov = document.getElementById('range-fov') as HTMLInputElement;
const valFov = document.getElementById('val-fov') as HTMLElement;
const rangeSpeed = document.getElementById('range-speed') as HTMLInputElement;
const valSpeed = document.getElementById('val-speed') as HTMLElement;
const colorBtns = document.querySelectorAll<HTMLButtonElement>('.color-btn');
const toggleSplatting = document.getElementById('toggle-splatting') as HTMLInputElement;
const togglePrecalculate = document.getElementById('toggle-precalculate') as HTMLInputElement;
const selectTone = document.getElementById('select-tone') as HTMLSelectElement;
const rangeExposure = document.getElementById('range-exposure') as HTMLInputElement;
const valExposure = document.getElementById('val-exposure') as HTMLElement;
const infoSplats = document.getElementById('info-splats') as HTMLElement;
const infoFormat = document.getElementById('info-format') as HTMLElement;
const infoSize = document.getElementById('info-size') as HTMLElement;
const dragOverlay = document.getElementById('drag-overlay') as HTMLElement;
const toastEl = document.getElementById('toast') as HTMLElement;

// State
let viewer: ReturnType<typeof createViewer>;
let camera: PerspectiveCamera;
let control: CameraControl;
let currentSplat: any = null;
let currentCentroid = new Vector3(0, 0, 0);
let currentBoundingDim = 2.0;
let needsRender = true;
let currentBgColor = new Color(0.043, 0.059, 0.09); // #0b0f17
let baseSpeed = 0.5;
let autoRotate = false;
let walkingTools: ReturnType<typeof createWalkingTools>;
const resolutionBudget = new ResolutionBudget();
let performanceMode = 'native';
const motionSamples: number[] = [];
const submitSamples: number[] = [];
function applyResolution() {
    if (!viewer) return;
    // Aholo multiplies this setting by devicePixelRatio internally.
    const scale = performanceMode === 'native' ? window.devicePixelRatio || 1 :
        performanceMode === 'performance' ? .7 : performanceMode === 'auto' ? resolutionBudget.scale : 1;
    viewer.renderPixelRatio = scale / (window.devicePixelRatio || 1);
    const label = document.getElementById('resolution-status');
    if (label) label.textContent = `${Math.round(scale * 100)}% of CSS resolution`;
    needsRender = true;
}

function showToast(message: string, type: 'success' | 'error' = 'success') {
    toastEl.textContent = message;
    toastEl.className = `toast show ${type}`;
    setTimeout(() => {
        toastEl.className = 'toast';
    }, 3500);
}

function updateLoadingState(show: boolean, title = '', subtitle = '') {
    if (show) {
        loadingOverlay.classList.remove('hidden');
        if (title) loadingTitle.textContent = title;
        if (subtitle) loadingSubtitle.textContent = subtitle;
        fileStatusDot.className = 'file-status-dot loading';
    } else {
        loadingOverlay.classList.add('hidden');
        fileStatusDot.className = 'file-status-dot';
    }
}

function applyViewerPipeline() {
    if (!viewer) return;
    const toneMappingMap: Record<string, ToneMapping> = {
        linear: ToneMapping.Linear,
        reinhard: ToneMapping.Reinhard,
        neutral: ToneMapping.Neutral,
        aces: ToneMapping.ACES,
        acesFilmic: ToneMapping.ACESFilmic,
    };

    setViewerConfig(viewer, {
        pipeline: {
            Background: {
                background: {
                    active: BackgroundMode.BasicBackground,
                    basic: { color: currentBgColor, alpha: 1 },
                },
                ground: { enabled: false },
            },
            Splatting: {
                enabled: toggleSplatting.checked,
                pack: {
                    precalculateEnabled: togglePrecalculate.checked,
                },
                toneMapping: {
                    enabled: selectTone.value !== 'linear',
                    toneMapping: toneMappingMap[selectTone.value] ?? ToneMapping.Linear,
                    exposure: Number(rangeExposure.value),
                },
            },
            TAA: { enabled: false },
        },
    });
    needsRender = true;
}

function resetCameraView() {
    if (!camera || !control) return;
    walkingTools?.pause();
    const coord = selectCoord.value;
    const cx = currentCentroid.x;
    const cy = currentCentroid.y;
    const cz = currentCentroid.z;
    // Calibrated framing distance inside the room interior
    const dist = Math.max(2.0, currentBoundingDim * 0.38);

    switch (coord) {
        case 'aholo':
            // +Z Up
            camera.up.set(0, 0, 1);
            camera.position.set(cx, cy - dist * 0.9, cz + dist * 0.3);
            break;
        case 'opengl':
            // +Y Up
            camera.up.set(0, 1, 0);
            camera.position.set(cx, cy + dist * 0.25, cz + dist);
            break;
        case 'opencv':
        default:
            // -Y Up (standard Gaussian Splatting) - angled to face room interior
            camera.up.set(0, -1, 0);
            camera.position.set(cx + dist * 0.65, cy - dist * 0.2, cz + dist * 0.65);
            break;
    }

    camera.lookAt(new Vector3(cx, cy, cz));
    camera.far = Math.max(5000, dist * 30);
    camera.updateProjectionMatrix();

    control.setOrbitCenter({ x: cx, y: cy, z: cz });
    control.stop();
    needsRender = true;
}

// A room is tens of megabytes: show how much has arrived so a slow connection does not look frozen.
async function downloadWithProgress(response: Response, expected: number): Promise<ArrayBuffer> {
    const reader = response.body?.getReader();
    if (!reader) return response.arrayBuffer();
    const chunks: Uint8Array[] = [];
    let received = 0;
    for (;;) {
        const {done, value} = await reader.read();
        if (done) break;
        chunks.push(value);
        received += value.length;
        loadingSubtitle.textContent = `Downloading room: ${(received / 1e6).toFixed(1)} of ${(expected / 1e6).toFixed(1)} MB`;
    }
    const bytes = new Uint8Array(received);
    let offset = 0;
    for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.length; }
    loadingSubtitle.textContent = 'Checking the room file...';
    return bytes.buffer;
}

async function loadSplatSource(source: string | File, displayName: string, fileSizeStr: string, pairing: any = null) {
    updateLoadingState(true, `Loading ${displayName}...`, 'Reading 3D Gaussian Splat data...');
    fileNameEl.textContent = displayName;
    infoSize.textContent = fileSizeStr;

    try {
        let input = source;
        if (typeof source === 'string' && pairing?.splatHash) {
            const response = await fetch(source);
            if (!response.ok) throw Error('Room visual file is unavailable.');
            const bytes = await downloadWithProgress(response, pairing.splatBytes);
            if (bytes.byteLength !== pairing.splatBytes) throw Error('Room visual file is incomplete.');
            const digest = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)), b => b.toString(16).padStart(2, '0')).join('');
            if (digest !== pairing.splatHash) throw Error('Room visual file changed. Re-import the matching result.');
            input = new File([bytes], displayName);
        }
        let fileType = SplatLoader.SplatFileType.PLY;
        const nameLower = displayName.toLowerCase();
        if (nameLower.endsWith('.sog')) fileType = SplatLoader.SplatFileType.SOG;
        else if (nameLower.endsWith('.spz')) fileType = SplatLoader.SplatFileType.SPZ;
        else if (nameLower.endsWith('.splat')) fileType = SplatLoader.SplatFileType.SPLAT;
        else if (nameLower.endsWith('.ksplat')) fileType = SplatLoader.SplatFileType.KSPLAT;

        loadingSubtitle.textContent = 'Parsing splats with Web Worker...';
        const data = await SplatLoader.parseSplatData(
            fileType,
            input,
            SplatLoader.SplatPackType.Compressed,
        );

        loadingSubtitle.textContent = 'Allocating GPU geometry & shaders...';

        // Remove old splat if exists
        if (currentSplat) {
            viewer.getScene().remove(currentSplat);
            if (typeof currentSplat.freeAllGpuResourceOwned === 'function') {
                currentSplat.freeAllGpuResourceOwned();
            } else if (typeof currentSplat.freeGPU === 'function') {
                currentSplat.freeGPU();
            }
            currentSplat = null;
        }

        const splat = await SplatUtils.createSplat(data);
        viewer.getScene().add(splat);
        currentSplat = splat;
        walkingTools?.setSource(pairing || null);

        // Compute centroid & bounding box
        const count = data.counts;
        splatCountEl.textContent = `(${count.toLocaleString()} splats)`;
        infoSplats.textContent = count.toLocaleString();
        infoFormat.textContent = fileType === SplatLoader.SplatFileType.PLY ? 'PLY (3D Gaussian Splat)' : '3DGS Format';

        const centers = new Float32Array(count * 3);
        data.fillCenters(centers);

        let minX = Infinity, minY = Infinity, minZ = Infinity;
        let maxX = -Infinity, maxY = -Infinity, maxZ = -Infinity;
        let sumX = 0, sumY = 0, sumZ = 0;

        for (let i = 0; i < count; i++) {
            const x = centers[i * 3];
            const y = centers[i * 3 + 1];
            const z = centers[i * 3 + 2];
            if (x < minX) minX = x; if (x > maxX) maxX = x;
            if (y < minY) minY = y; if (y > maxY) maxY = y;
            if (z < minZ) minZ = z; if (z > maxZ) maxZ = z;
            sumX += x; sumY += y; sumZ += z;
        }

        currentCentroid = new Vector3(sumX / count, sumY / count, sumZ / count);
        const sizeX = maxX - minX;
        const sizeY = maxY - minY;
        const sizeZ = maxZ - minZ;
        currentBoundingDim = Math.max(sizeX, sizeY, sizeZ) || 2.0;

        baseSpeed = Math.max(0.1, currentBoundingDim * 0.15);
        control.moveSpeed = baseSpeed * Number(rangeSpeed.value);

        resetCameraView();
        if (pairing?.initialView) {
            const v = pairing.initialView, p = v.position, r = v.rotation;
            if (p?.length === 3 && r?.length === 3 &&
                [...p, ...r.flat(), v.height, v.fy].every(Number.isFinite) && v.fy > 0) {
                camera.position.set(...p);
                // Turning happens around camera.up: the room's up keeps the horizon level; one frame's up is tilted.
                const up = v.up ?? [-r[0][1], -r[1][1], -r[2][1]];
                camera.up.set(up[0], up[1], up[2]);
                const target = {x:p[0]+r[0][2]*3, y:p[1]+r[1][2]*3, z:p[2]+r[2][2]*3};
                camera.lookAt(new Vector3(target.x, target.y, target.z));
                // A walkthrough reads best near a human field of view, not the camera's narrow one.
                camera.fov = Number(rangeFov.value);
                camera.updateProjectionMatrix();
                control.setOrbitCenter(target); control.stop();
            }
        }
        applyViewerPipeline();
        updateLoadingState(false);
        showToast(`Loaded ${displayName} (${count.toLocaleString()} splats)`, 'success');
    } catch (err: any) {
        console.error('Failed to load splat:', err);
        updateLoadingState(false);
        fileStatusDot.className = 'file-status-dot error';
        splatCountEl.textContent = '(Error)';
        showToast(err?.message || 'Failed to load point cloud', 'error');
    }
}

function setupViewer() {
    const width = container.clientWidth || window.innerWidth;
    const height = container.clientHeight || window.innerHeight;

    viewer = createViewer('ply-viewer', container, { antialiasing: false });
    applyResolution();
    camera = new PerspectiveCamera(Number(rangeFov.value), width / height, 0.05, 2000);
    viewer.setCamera(camera);

    control = new CameraControl(camera, container, {
        enabled: true,
        useOrbit: selectCameraMode.value === 'orbit',
        orbitMinDistance: 0.01,
        moveSpeed: baseSpeed,
        lookSpeed: 0.004,
        wheelSpeed: 0.006,
        panSpeed: 0.006,
    });

    applyViewerPipeline();

    // Resize handler
    const onResize = () => {
        const w = container.clientWidth || window.innerWidth;
        const h = container.clientHeight || window.innerHeight;
        if (w > 0 && h > 0) {
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
            applyResolution();
            needsRender = true;
        }
    };
    window.addEventListener('resize', onResize);

    // Frame rendering & FPS loop
    let lastTime = performance.now();
    let frameCount = 0;
    let submissionMs = 0;
    let fpsTimer = performance.now();
    let previousActive = false;
    let frameIntervals: number[] = [];

    function renderLoop(now: number) {
        const interval = now - lastTime;
        const delta = Math.min(interval / 1000, 0.1);
        lastTime = now;

        if (autoRotate && !walkingTools?.isWalking() && control && !control.getState().interacting) {
            const angle = delta * 0.35;
            const x = camera.position.x - currentCentroid.x;
            const z = camera.position.z - currentCentroid.z;
            const cosA = Math.cos(angle);
            const sinA = Math.sin(angle);
            camera.position.x = currentCentroid.x + (x * cosA - z * sinA);
            camera.position.z = currentCentroid.z + (x * sinA + z * cosA);
            camera.lookAt(currentCentroid);
            needsRender = true;
        }

        const moved = control.update(delta);
        const walkingMoved = walkingTools?.tick(moved);
        const active = Boolean(moved || walkingMoved || autoRotate);
        if (active && previousActive && !document.hidden && interval > 0 && interval < 2000) {
            frameIntervals.push(interval);
            motionSamples.push(interval);
            if (motionSamples.length > 3600) motionSamples.shift();
        }
        if (performanceMode === 'auto' && resolutionBudget.sample(interval, active && previousActive && !document.hidden)) applyResolution();
        previousActive = active;
        if (moved || walkingMoved || autoRotate || needsRender) {
            const submitStart = performance.now();
            viewer.render();
            const submittedMs = performance.now() - submitStart;
            submissionMs += submittedMs;
            if (active && !document.hidden) {
                submitSamples.push(submittedMs);
                if (submitSamples.length > 3600) submitSamples.shift();
            }
            frameCount++;
            needsRender = false;
        }

        if (now - fpsTimer >= 500) {
            const fps = Math.round((frameCount * 1000) / (now - fpsTimer));
            statFps.textContent = String(fps);
            statMs.textContent = frameCount ? (submissionMs / frameCount).toFixed(1) + ' ms CPU' : 'idle';
            const pacing = document.getElementById('frame-pacing');
            if (pacing) {
                const sorted = frameIntervals.slice().sort((a,b)=>a-b);
                pacing.textContent = sorted.length ? `Motion p90: ${sorted[Math.floor((sorted.length-1)*.9)].toFixed(1)} ms (60 FPS budget: 16.7 ms)` : 'Move to measure frame pacing; idle is not low FPS.';
            }
            frameIntervals = [];
            submissionMs = 0;
            frameCount = 0;
            fpsTimer = now;
        }

        requestAnimationFrame(renderLoop);
    }

    viewer.requestRenderHandler = () => {
        needsRender = true;
    };

    requestAnimationFrame(renderLoop);
}

function setupUI() {
    document.getElementById('download-performance')?.addEventListener('click', () => {
        const summary = (samples: number[]) => {
            const sorted = samples.slice().sort((a,b)=>a-b);
            const mean = samples.reduce((a,b)=>a+b,0) / samples.length;
            return samples.length ? {samples:samples.length,meanMs:mean,
                p50Ms:sorted[Math.floor((sorted.length-1)*.5)],p90Ms:sorted[Math.floor((sorted.length-1)*.9)],
                p99Ms:sorted[Math.floor((sorted.length-1)*.99)],over33ms:samples.filter(x=>x>33.3).length} : null;
        };
        const report = {version:1,createdAt:new Date().toISOString(),viewer:'aholo',mode:performanceMode,
            viewport:{width:innerWidth,height:innerHeight,devicePixelRatio},renderPixelRatio:viewer.renderPixelRatio,
            splats:infoSplats.textContent,motion:summary(motionSamples),cpuSubmission:summary(submitSamples),
            note:'Foreground moving-frame intervals; not GPU timer measurements. No capture images or file paths included.'};
        const url=URL.createObjectURL(new Blob([JSON.stringify(report,null,2)],{type:'application/json'}));
        const link=document.createElement('a');link.href=url;link.download='namma-performance.json';link.click();
        setTimeout(()=>URL.revokeObjectURL(url),1000);
    });
    document.getElementById('performance-mode')?.addEventListener('change', (event) => {
        performanceMode = (event.target as HTMLSelectElement).value;
        motionSamples.length=0;submitSamples.length=0;
        resolutionBudget.reset(); applyResolution();
    });
    // Open File button
    btnUpload.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', () => {
        const file = fileInput.files?.[0];
        if (file) {
            const sizeMb = (file.size / (1024 * 1024)).toFixed(1) + ' MB';
            loadSplatSource(file, file.name, sizeMb);
        }
        fileInput.value = '';
    });

    // Reset button
    btnReset.addEventListener('click', resetCameraView);

    // Auto rotate turntable button
    btnAutoRotate.addEventListener('click', () => {
        autoRotate = !autoRotate;
        if (autoRotate) {
            walkingTools?.pause();
            btnAutoRotate.classList.add('btn-primary');
            showToast('Turntable auto-rotation active', 'success');
        } else {
            btnAutoRotate.classList.remove('btn-primary');
            showToast('Turntable stopped', 'success');
        }
        needsRender = true;
    });

    // Sidebar toggle
    btnSettings.addEventListener('click', () => {
        sidebar.classList.toggle('hidden');
    });

    btnCloseSidebar.addEventListener('click', () => {
        sidebar.classList.add('hidden');
    });

    // Coordinate system change
    selectCoord.addEventListener('change', () => {
        resetCameraView();
    });

    // Camera mode change
    selectCameraMode.addEventListener('change', () => {
        const selectedMode = selectCameraMode.value;
        walkingTools?.pause();
        selectCameraMode.value = selectedMode;
        const isOrbit = selectCameraMode.value === 'orbit';
        control.setOptions({ useOrbit: isOrbit });
        needsRender = true;
    });

    // FOV slider
    rangeFov.addEventListener('input', () => {
        const fov = Number(rangeFov.value);
        valFov.textContent = `${fov}°`;
        camera.fov = fov;
        camera.updateProjectionMatrix();
        needsRender = true;
    });

    // Speed slider
    rangeSpeed.addEventListener('input', () => {
        const mult = Number(rangeSpeed.value);
        valSpeed.textContent = `${mult.toFixed(2)}x`;
        control.moveSpeed = baseSpeed * mult;
    });

    // Background color buttons
    colorBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            colorBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const hex = btn.dataset.color || '#0b0f17';
            // Parse hex to 0..1 RGB
            const r = parseInt(hex.slice(1, 3), 16) / 255;
            const g = parseInt(hex.slice(3, 5), 16) / 255;
            const b = parseInt(hex.slice(5, 7), 16) / 255;
            currentBgColor = new Color(r, g, b);
            applyViewerPipeline();
        });
    });

    // Pipeline toggles
    toggleSplatting.addEventListener('change', applyViewerPipeline);
    togglePrecalculate.addEventListener('change', applyViewerPipeline);
    selectTone.addEventListener('change', applyViewerPipeline);
    rangeExposure.addEventListener('input', () => {
        valExposure.textContent = Number(rangeExposure.value).toFixed(1);
        applyViewerPipeline();
    });

    // Keyboard shortcuts
    window.addEventListener('keydown', (e) => {
        if (e.target instanceof HTMLInputElement || e.target instanceof HTMLSelectElement) return;
        if (e.key === 'r' || e.key === 'R') {
            resetCameraView();
        }
    });

    // Drag and Drop
    let dragDepth = 0;
    window.addEventListener('dragenter', (e) => {
        e.preventDefault();
        dragDepth++;
        dragOverlay.classList.add('active');
    });

    window.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    window.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dragDepth--;
        if (dragDepth <= 0) {
            dragDepth = 0;
            dragOverlay.classList.remove('active');
        }
    });

    window.addEventListener('drop', (e) => {
        e.preventDefault();
        dragDepth = 0;
        dragOverlay.classList.remove('active');

        const file = e.dataTransfer?.files?.[0];
        if (file) {
            const sizeMb = (file.size / (1024 * 1024)).toFixed(1) + ' MB';
            loadSplatSource(file, file.name, sizeMb);
        }
    });
}

// Bootstrap
async function loadRoomManifest(url: URL) {
    if (url.origin !== location.origin) throw Error('Room manifest must be hosted with this viewer.');
    const response = await fetch(url);
    if (!response.ok) throw Error('Room manifest is unavailable.');
    const manifest = validateViewerManifest(await response.json());
    await loadSplatSource(new URL(manifest.splat.file, url).href, manifest.title + '.spz',
        (manifest.splat.bytes / 1024 / 1024).toFixed(1) + ' MB',
        {title: manifest.title, splatHash: manifest.splat.sha256, splatBytes: manifest.splat.bytes,
         collisionUrl: new URL(manifest.collision.file, url).href,
         collisionHash: manifest.collision.sha256, initialView: manifest.initialView,
         walkingSetup: manifest.walkingSetup});
}

async function init() {
    setupViewer();
    setupUI();
    walkingTools=createWalkingTools({viewer,camera,control,container,
        dirty:()=>{viewer.getScene().notifySceneChange();needsRender=true;},
        onWalkingStart:()=>{autoRotate=false;btnAutoRotate.classList.remove('btn-primary');}});

    // Load local point_cloud.ply
    updateLoadingState(false);
    fileNameEl.textContent = 'Choose a room file';
    splatCountEl.textContent = '';
    const portable = new URLSearchParams(location.search).get('manifest');
    if (portable) {
        const roomTools = document.querySelector('.namma-status a') as HTMLElement;
        if (roomTools) roomTools.hidden = true;
        sidebar.classList.add('hidden');
        try {
            await loadRoomManifest(new URL(portable, location.href));
            if (walkingTools.hasSavedSetup()) {
                const enter = document.createElement('button');
                enter.className = 'btn btn-primary'; enter.textContent = 'Enter room';
                enter.title = 'Start walking from the saved entrance';
                enter.onclick = () => walkingTools.resumeSaved();
                document.querySelector('.top-bar-right')?.prepend(enter);
            }
        }
        catch (error: any) { showToast(error.message, 'error'); }
        return;
    }
    if (import.meta.env.DEV) {
        const selected = new URLSearchParams(location.search).get('scene');
        const list = document.createElement('select');
        list.className = 'btn'; list.setAttribute('aria-label', 'Scene library');
        list.innerHTML = '<option value="">Scene library…</option>';
        document.querySelector('.top-bar-right')?.prepend(list);
        try {
            const response = await fetch('/__scenes');
            if (!response.ok) throw Error('Scene library is unavailable.');
            const scenes = await response.json();
            for (const item of scenes) {
                const option = document.createElement('option');
                option.value = item.id; option.textContent = item.title; list.append(option);
            }
            list.value = selected || '';
        } catch (error: any) { showToast(error.message, 'error'); }
        list.onchange = () => { if (list.value) location.href = '/aholo/?scene=' + encodeURIComponent(list.value); };
        if (selected) {
            try {
                const base = '/__scenes/' + encodeURIComponent(selected);
                await loadRoomManifest(new URL(base + '/scene.json', location.href));
            } catch (error: any) { showToast(error.message, 'error'); }
        } else if (!list.options.length) {
            showToast('No rooms imported yet. Import a trained result first (see viewer/README.md), or use Open File.', 'success');
        }
    }
}

init();

</file>

<file src="viewer/aholo/performance.js">
// Frame intervals include browser/GPU scheduling, not just render submission time.
export class ResolutionBudget {
  constructor() { this.scale=1; this.samples=[]; this.elapsed=0; }
  reset(scale=1) { this.scale=scale; this.samples=[]; this.elapsed=0; }
  sample(ms, active=true) {
    // Embedded browsers may throttle a nominally visible tab to one callback/second.
    // Do not reduce quality in response to those suspension-sized gaps.
    if(!active || !Number.isFinite(ms) || ms<=0 || ms>500) {this.samples=[];this.elapsed=0;return false;}
    this.samples.push(ms);this.elapsed+=ms;
    if(this.elapsed<1800 || this.samples.length<20)return false;
    const sorted=this.samples.slice().sort((a,b)=>a-b);
    const p90=sorted[Math.floor((sorted.length-1)*.9)];
    const before=this.scale;
    // Hysteresis and bounded changes prevent rapid resolution oscillation.
    if(p90>19)this.scale=Math.max(.5, +(this.scale-.1).toFixed(2));
    else if(p90<15)this.scale=Math.min(1, +(this.scale+.05).toFixed(2));
    this.samples=[];this.elapsed=0;
    return before!==this.scale;
  }
}

</file>

<file src="viewer/aholo/saved-walk.js">
// Portable calibration belongs to this exact visual/collision pair, never a title.
export const WALK_PROFILE = 'recast-cs005-ch004-height120-climb030-radius015-floorfill-v3';
// Setups store calibration and entrance only, so ones saved under earlier walker settings stay valid.
const EARLIER_PROFILES = ['recast-cs005-ch004-height170-radius025-v2', 'recast-cs008-ch004-height170-radius025-v1'];
const sha = value => typeof value === 'string' && /^[a-f0-9]{64}$/.test(value);
const vector = (value, length) => Array.isArray(value) && value.length === length && value.every(Number.isFinite);
const demand = (ok, message) => { if (!ok) throw Error(message); };

export function sceneIdentity(scene) {
  if (!scene || !sha(scene.splatHash) || !sha(scene.collisionHash)) return null;
  return `${scene.splatHash}:${scene.collisionHash}`;
}

export function validateWalk(saved, scene) {
  demand(saved?.version === 1 && saved.type === 'namma-aholo-walk', 'Unsupported walking setup.');
  demand(saved.sceneIdentity === sceneIdentity(scene) && sceneIdentity(scene), 'Walking setup belongs to different scene files.');
  // These records contain calibration/entrance, never cached nav polygons.
  // Resume rebuilds navigation and checks the entrance using the current grid.
  demand([WALK_PROFILE, ...EARLIER_PROFILES].includes(saved.profile) && saved.coordinateSpace === 'raw-ply-v1', 'Walking settings changed; rebuild this setup.');
  demand(vector(saved.floor?.origin, 3) && vector(saved.floor?.quaternion, 4), 'Invalid saved floor.');
  demand(Math.abs(Math.hypot(...saved.floor.quaternion) - 1) < 1e-5, 'Invalid saved floor rotation.');
  demand(Number.isFinite(saved.metresPerUnit) && saved.metresPerUnit > 0 && saved.metresPerUnit < 1e5, 'Invalid saved scale.');
  demand(Number.isFinite(saved.eyeHeight) && saved.eyeHeight >= 1.2 && saved.eyeHeight <= 1.7, 'Invalid saved eye height.');
  demand(vector(saved.entrance, 3) && vector(saved.forward, 3) && Math.hypot(...saved.forward) > .001, 'Invalid saved entrance.');
  demand(saved.reviewed === true, 'Review the walking surfaces before saving.');
  const m = saved.measurement;
  demand(Number.isFinite(m?.metres) && m.metres > 0 && m.metres <= 40 && Array.isArray(m.endpoints) && m.endpoints.length === 2 && m.endpoints.every(p => vector(p, 3)), 'Invalid saved measurement.');
  const distance = Math.hypot(...m.endpoints[0].map((x, i) => x - m.endpoints[1][i]));
  demand(distance > .001 && Math.abs(m.metres / distance / saved.metresPerUnit - 1) < 1e-6, 'Saved endpoints do not match the scale.');
  // Review/assumed measurements are never upgraded to metric verification.
  return {
    version: 1, type: 'namma-aholo-walk', profile: WALK_PROFILE,
    coordinateSpace: 'raw-ply-v1', sceneIdentity: saved.sceneIdentity,
    floor: {origin: [...saved.floor.origin], quaternion: [...saved.floor.quaternion]},
    metresPerUnit: saved.metresPerUnit, eyeHeight: saved.eyeHeight,
    measurement: {metres: m.metres, endpoints: m.endpoints.map(p => [...p])},
    entrance: [...saved.entrance], forward: [...saved.forward], reviewed: true,
    metricVerified: false,
  };
}

export function loadWalk(storage, scene) {
  const identity = sceneIdentity(scene);
  if (!identity) return null;
  const raw = storage.getItem('namma:walk:v1:' + identity);
  return raw ? validateWalk(JSON.parse(raw), scene) : null;
}

export function saveWalk(storage, scene, saved) {
  const checked = validateWalk(saved, scene);
  storage.setItem('namma:walk:v1:' + checked.sceneIdentity, JSON.stringify(checked));
  return checked;
}

export function validateViewerManifest(m) {
  demand(m?.version === 1 && m.type === 'namma-viewer-scene' && m.coordinateSpace === 'raw-ply-v1', 'Unsupported room manifest.');
  demand(typeof m.title === 'string' && m.title.length > 0 && m.title.length <= 200, 'Invalid room title.');
  demand(m.splat?.file === 'preview.spz' && m.collision?.file === 'collision.glb', 'Unsupported room asset paths.');
  demand(sha(m.splat.sha256) && sha(m.collision.sha256), 'Missing room file identities.');
  demand(Number.isSafeInteger(m.splat.bytes) && m.splat.bytes > 0 && m.splat.bytes <= 150 * 1024 ** 2, 'Room file exceeds the supported browser size.');
  demand(Number.isSafeInteger(m.collision.triangles) && m.collision.triangles > 0 && m.collision.triangles <= 250000, 'Room collision geometry exceeds the walking budget.');
  const clean = {version: 1, type: m.type, coordinateSpace: m.coordinateSpace, title: m.title,
    splat: {...m.splat}, collision: {...m.collision}};
  if (m.initialView) {
    const v = m.initialView;
    demand(vector(v.position, 3) && Array.isArray(v.rotation) && v.rotation.length === 3 && v.rotation.every(r => vector(r, 3)) && Number.isFinite(v.height) && v.height > 0 && Number.isFinite(v.fy) && v.fy > 0, 'Invalid initial camera.');
    clean.initialView = {position: v.position, rotation: v.rotation, height: v.height, fy: v.fy};
    // Room up from all training cameras (older scenes lack it and fall back to the first camera).
    if (vector(v.up, 3) && Math.abs(Math.hypot(...v.up) - 1) < 1e-3) clean.initialView.up = v.up;
  }
  if (m.walkingSetup) clean.walkingSetup = validateWalk(m.walkingSetup, {splatHash: m.splat.sha256, collisionHash: m.collision.sha256});
  return clean;
}

</file>

<file src="viewer/aholo/style.css">
:root {
  --bg-primary: #0b0f17;
  --bg-surface: rgba(18, 24, 38, 0.75);
  --bg-surface-hover: rgba(28, 36, 56, 0.85);
  --border-color: rgba(255, 255, 255, 0.08);
  --border-focus: rgba(99, 102, 241, 0.5);
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --accent-color: #6366f1;
  --accent-glow: rgba(99, 102, 241, 0.25);
  --accent-hover: #4f46e5;
  --success-color: #10b981;
  --warning-color: #f59e0b;
  --danger-color: #ef4444;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-full: 9999px;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body, html {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  font-family: var(--font-sans);
  -webkit-font-smoothing: antialiased;
  user-select: none;
}

#app {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

#viewer-container {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  outline: none;
  cursor: grab;
}

#viewer-container:active {
  cursor: grabbing;
}

/* Glass panel utility */
.glass-panel {
  background: var(--bg-surface);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--border-color);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-md);
  color: var(--text-primary);
}

/* Top Navigation Bar */
.top-bar {
  position: absolute;
  top: 16px;
  left: 16px;
  right: 16px;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
  pointer-events: none;
}

.top-bar-left, .top-bar-right {
  display: flex;
  align-items: center;
  gap: 12px;
  pointer-events: auto;
}

.brand-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px;
  border-radius: var(--radius-full);
}

.brand-logo {
  width: 22px;
  height: 22px;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 12px var(--accent-glow);
}

.brand-logo svg {
  width: 14px;
  height: 14px;
  fill: #fff;
}

.brand-text {
  font-weight: 600;
  font-size: 14px;
  letter-spacing: -0.01em;
}

.file-info-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  font-size: 13px;
  font-family: var(--font-mono);
  color: var(--text-secondary);
}

.file-status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--success-color);
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.6);
}

.file-status-dot.loading {
  background-color: var(--warning-color);
  box-shadow: 0 0 8px rgba(245, 158, 11, 0.6);
  animation: pulse 1.5s infinite;
}

.file-status-dot.error {
  background-color: var(--danger-color);
  box-shadow: 0 0 8px rgba(239, 68, 68, 0.6);
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.85); }
}

.stats-badge {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 14px;
  font-size: 12px;
  font-family: var(--font-mono);
  color: var(--text-secondary);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-val {
  color: var(--text-primary);
  font-weight: 600;
}

/* Action Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 500;
  border-radius: var(--radius-sm);
  cursor: pointer;
  border: 1px solid var(--border-color);
  background: var(--bg-surface);
  color: var(--text-primary);
  transition: all 0.2s ease;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  pointer-events: auto;
}

.btn:hover {
  background: var(--bg-surface-hover);
  border-color: rgba(255, 255, 255, 0.16);
  transform: translateY(-1px);
}

.btn:active {
  transform: translateY(0);
}

.btn-primary {
  background: var(--accent-color);
  border-color: var(--accent-hover);
  box-shadow: 0 4px 14px var(--accent-glow);
}

.btn-primary:hover {
  background: var(--accent-hover);
}

.btn-icon {
  width: 36px;
  height: 36px;
  padding: 0;
  border-radius: var(--radius-sm);
}

.btn svg {
  width: 16px;
  height: 16px;
  stroke: currentColor;
  fill: none;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* Sidebar / Settings Panel */
.sidebar {
  position: absolute;
  top: 74px;
  right: 16px;
  width: 320px;
  max-height: calc(100vh - 96px);
  overflow-y: auto;
  z-index: 10;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s ease;
}

.sidebar.hidden {
  transform: translateX(360px);
  opacity: 0;
  pointer-events: none;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 12px;
}

.sidebar-title {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: -0.01em;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.section-label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.control-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: var(--text-secondary);
}

/* Custom Select */
.select-input {
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  outline: none;
  cursor: pointer;
  transition: border-color 0.2s;
}

.select-input:focus {
  border-color: var(--border-focus);
}

/* Range input */
.range-container {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
}

.range-input {
  flex: 1;
  -webkit-appearance: none;
  appearance: none;
  height: 4px;
  border-radius: 2px;
  background: rgba(255, 255, 255, 0.15);
  outline: none;
}

.range-input::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--accent-color);
  cursor: pointer;
  box-shadow: 0 0 8px var(--accent-glow);
  transition: transform 0.1s;
}

.range-input::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}

.range-val {
  font-family: var(--font-mono);
  font-size: 12px;
  min-width: 38px;
  text-align: right;
  color: var(--text-primary);
}

/* Toggle Switch */
.switch {
  position: relative;
  display: inline-block;
  width: 38px;
  height: 20px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.15);
  transition: 0.2s;
  border-radius: 20px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 14px;
  width: 14px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.2s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: var(--accent-color);
}

input:checked + .slider:before {
  transform: translateX(18px);
}

/* Color presets */
.color-options {
  display: flex;
  gap: 8px;
}

.color-btn {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: transform 0.15s, border-color 0.15s;
}

.color-btn:hover {
  transform: scale(1.15);
}

.color-btn.active {
  border-color: #fff;
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.4);
}

/* Bottom Hint / Help Bar */
.bottom-bar {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 18px;
  border-radius: var(--radius-full);
  font-size: 12px;
  color: var(--text-secondary);
  pointer-events: none;
}

.help-shortcut {
  display: flex;
  align-items: center;
  gap: 6px;
}

.kbd {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 4px;
  padding: 2px 6px;
  font-size: 11px;
  font-family: var(--font-mono);
  color: var(--text-primary);
}

/* Loading Overlay */
.loading-overlay {
  position: absolute;
  inset: 0;
  background: rgba(11, 15, 23, 0.85);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  z-index: 50;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 18px;
  transition: opacity 0.4s ease, visibility 0.4s ease;
}

.loading-overlay.hidden {
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
}

.spinner {
  width: 44px;
  height: 44px;
  border: 3px solid rgba(99, 102, 241, 0.2);
  border-top-color: var(--accent-color);
  border-radius: 50%;
  animation: spin 0.9s cubic-bezier(0.5, 0, 0.5, 1) infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.loading-subtitle {
  font-size: 13px;
  color: var(--text-muted);
  font-family: var(--font-mono);
}

/* Drag and Drop Overlay */
.drag-overlay {
  position: absolute;
  inset: 20px;
  border: 2px dashed var(--accent-color);
  border-radius: var(--radius-lg);
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  z-index: 60;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transition: all 0.2s ease;
}

.drag-overlay.active {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
}

.drag-icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--accent-glow);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent-color);
}

.drag-icon svg {
  width: 28px;
  height: 28px;
}

.drag-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.drag-subtitle {
  font-size: 13px;
  color: var(--text-muted);
}

/* Toast Notification */
.toast {
  position: absolute;
  bottom: 24px;
  right: 24px;
  z-index: 70;
  padding: 12px 20px;
  border-radius: var(--radius-md);
  background: rgba(30, 41, 59, 0.95);
  border: 1px solid var(--border-color);
  backdrop-filter: blur(16px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 10px;
  transform: translateY(60px);
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  pointer-events: none;
}

.toast.show {
  transform: translateY(0);
  opacity: 1;
}

.toast.error {
  border-color: rgba(239, 68, 68, 0.4);
  color: #fca5a5;
}

.toast.success {
  border-color: rgba(16, 185, 129, 0.4);
  color: #86efac;
}

.namma-status{position:fixed;bottom:72px;left:20px;z-index:100;background:#17232ded;color:#fff;padding:10px 14px;border-radius:10px;font:13px sans-serif;max-width:calc(100vw - 40px)}.namma-status a{color:#8ee8e3;margin-left:12px}

.namma-walking{position:fixed;left:16px;top:90px;width:280px;max-height:calc(100vh - 190px);overflow:auto;z-index:110;padding:14px;color:#fff;font:13px/1.5 sans-serif}.namma-walking summary{cursor:pointer;font-weight:600}.namma-walking button{display:block;width:100%;padding:8px;margin:8px 0;cursor:pointer}.namma-walking button:disabled{opacity:.4;cursor:not-allowed}.namma-walking label{display:block;margin:8px 0}.namma-walking input[type=number]{width:100px;margin-left:6px}.namma-walking canvas{background:#14252c;width:240px;max-width:100%}

</file>

<file src="viewer/aholo/walking-tools.js">
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {BufferGeometry, BufferAttribute, Mesh, MeshBasicMaterial, Color, Raycaster, Vector2, Vector3 as ViewVector3} from '@manycore/aholo-viewer';
import {buildNavigation} from '../src/navigation.js';
import {floorAlignment} from '../src/scene-alignment.js';
import {WALK_PROFILE, sceneIdentity, validateWalk, loadWalk, saveWalk} from './saved-walk.js';

// Render in raw reconstruction coordinates; transform only navigation queries to metres/Y-up.
// This keeps appearance, pick geometry and player position in the same source frame.
export function createWalkingTools({viewer,camera,control,container,dirty,onWalkingStart=()=>{}}) {
  const panel=document.createElement('details');panel.className='namma-walking glass-panel';
  panel.innerHTML=`<summary>Walking setup · experimental</summary>
    <button data-action="resume" disabled>Enter saved walking setup</button>
    <p>Reconstructed surfaces are not yet validated room geometry. Inspect floor coverage and obstacles before walking.</p>
    <button data-action="load">Load matching collision estimate</button>
    <label><input type="checkbox" data-field="overlay" checked> Show estimated surfaces</label>
    <button data-action="floor" disabled>1. Pick three floor points</button>
    <label>Measured distance (metres)<input data-field="distance" type="number" value="" min="0.01" step="0.01"></label>
    <button data-action="measure" disabled>2. Pick measurement endpoints</button>
    <button data-action="build" disabled>3. Build walking surfaces</button>
    <label><input data-field="review" type="checkbox"> I reviewed the surfaces and want to test experimental walking</label>
    <button data-action="spawn" disabled>4. Pick a walking start</button>
    <label>Eye height above floor (metres)<input data-field="eye" type="number" value="1.65" min="1.2" max="1.7" step="0.05"></label>
    <button data-action="level" disabled>Look straight ahead</button>
    <button data-action="pause" disabled>Pause walking</button>
    <button data-action="save" disabled>Save this walking entrance</button>
    <button data-action="export" disabled>Download walking setup</button>
    <button data-action="import">Load a saved setup file</button>
    <input data-field="import" type="file" accept=".json" hidden>
    <p data-field="saved" role="status">Setup is saved on this browser after you choose a walking start. Download it to carry it to another browser or demo package.</p>
    <p data-field="status" role="status">Load a supported scene. Gaps in the filmed floor are filled for walking; walls and furniture still block.</p>
    <canvas width="240" height="180" aria-label="Top-down estimated geometry and player position"></canvas>`;
  document.getElementById('app').append(panel);
  const button=name=>panel.querySelector(`[data-action="${name}"]`);
  const field=name=>panel.querySelector(`[data-field="${name}"]`);
  const say=message=>{field('status').textContent=message;};
  let root=null,drawables=[],navigation=null,alignment=null,scale=null,mode=null,picks=[],state=null;
  let rawToNav=new THREE.Matrix4(),navToRaw=new THREE.Matrix4(),bounds=null,mapPoints=[];
  let generation=0, recovered=false, savedControls=null, eyeHeight=1.65;
  let measurement=null, savedSetup=null, restoring=false;
  let previousCameraMode=null;
  const raycaster=new Raycaster();
  const canvas=panel.querySelector('canvas'),ctx=canvas.getContext('2d');
  const mapBase=document.createElement('canvas');mapBase.width=240;mapBase.height=180;
  const mapCtx=mapBase.getContext('2d');let mapDirty=true,lastMapTime=0;
  function pause(){state=null;button('pause').disabled=true;button('level').disabled=true;button('save').disabled=true;control.stop();if(savedControls){Object.assign(control,savedControls);savedControls=null;}if(previousCameraMode!==null){document.getElementById('select-camera-mode').value=previousCameraMode;previousCameraMode=null;}setWalkStatus(false);}
  function setWalkStatus(active){const label=document.getElementById('walk-status');if(label)label.textContent=active?'Experimental walking · Scale uses the supplied measurement.':'Explore the reconstruction · Open Walking setup to enter.';}
  function invalidate(){generation++;pause();navigation?.dispose();navigation=null;button('spawn').disabled=true;field('review').checked=false;}
  function clear(){generation++;invalidate();for(const mesh of drawables){viewer.getScene().remove(mesh);mesh.freeAllGpuResourceOwned?.();}drawables=[];
    root?.traverse(o=>{o.geometry?.dispose();if(o.material){for(const m of [o.material].flat())m.dispose?.();}});
    control.enabled=true;root=null;alignment=null;scale=null;measurement=null;mode=null;picks=[];mapPoints=[];bounds=null;mapDirty=true;drawMap();
    for(const name of ['floor','measure','build'])button(name).disabled=true;dirty();}
  function setSource(scene){clear();recovered=scene;button('load').disabled=!scene;
    field('distance').value='';
    savedSetup=null;button('resume').disabled=true;button('export').disabled=true;
    let savedOrigin='this browser',savedError='';
    try{savedSetup=loadWalk(localStorage,scene);}catch(e){savedError='Browser setup could not be restored: '+e.message+' ';}
    if(!savedSetup)savedOrigin='the scene package';
    if(!savedSetup&&scene?.walkingSetup){try{savedSetup=validateWalk(scene.walkingSetup,scene);}catch(e){field('saved').textContent=e.message;}}
    button('resume').disabled=!savedSetup;button('export').disabled=!savedSetup;
    field('saved').textContent=savedError+(savedSetup?`Saved setup found in ${savedOrigin} for these exact files. Enter it without picking the floor and measurement again. Physical scale still depends on the supplied measurement.`:'Choose a walking start to save setup on this browser. Existing sessions from older versions cannot be recovered after refresh.');
    say(scene?`${typeof scene==='object'?scene.title:scene} selected. Load its matching surfaces. Scale is unverified.`:'No paired collision estimate for this file.');}

  async function load(){
    if(!recovered)return;clear();const token=generation;say('Loading estimated surfaces…');
    try{
      const response=await fetch(recovered.collisionUrl);if(!response.ok)throw Error('Collision estimate unavailable.');
      const bytes=await response.arrayBuffer();
      if(typeof recovered==='object'){
        const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),b=>b.toString(16).padStart(2,'0')).join('');
        if(hash!==recovered.collisionHash)throw Error('Collision file changed. Re-import this scene before walking.');
      }
      const parsed=await new GLTFLoader().parseAsync(bytes,'');
      if(token!==generation)return false;
      root=parsed.scene;root.updateMatrixWorld(true);
      root.traverse(o=>{if(!o.isMesh)return;const g=o.geometry.clone();g.applyMatrix4(o.matrixWorld);
        const geometry=new BufferGeometry();geometry.setAttribute('position',new BufferAttribute(new Float32Array(g.attributes.position.array),3));
        if(g.index)geometry.setIndex(new Uint32Array(g.index.array));
        const material=new MeshBasicMaterial({color:new Color(0.15,0.85,0.65),side:2});
        const mesh=new Mesh(geometry,material);mesh.visible=field('overlay').checked;viewer.getScene().add(mesh);drawables.push(mesh);g.dispose();});
      button('floor').disabled=false;button('measure').disabled=false;dirty();say('Green surfaces are estimates. Pick three widely spaced points on the actual floor.');
      return true;
    }catch(e){say(e.message);return false;}
  }
  button('load').onclick=load;
  field('overlay').onchange=()=>{drawables.forEach(m=>m.visible=field('overlay').checked);dirty();};
  for(const name of ['floor','measure','spawn'])button(name).onclick=()=>{
    pause();mode=name;picks=[];control.enabled=false;
    say(name==='floor'?'Click three floor points, spread apart.':name==='measure'?'Click the two exact endpoints of your tape measurement.':'Click a verified floor location. Escape cancels.');
  };
  container.addEventListener('click',event=>{
    if(!mode||!root)return;
    const box=container.getBoundingClientRect();camera.updateMatrixWorld(true);
    // Pick against the same mesh used for navigation, even when the overlay is hidden.
    drawables.forEach(m=>{m.visible=true;m.updateMatrixWorld(true);});
    raycaster.setFromCamera(new Vector2((event.clientX-box.left)/box.width*2-1,1-(event.clientY-box.top)/box.height*2),camera);
    const hit=raycaster.intersectObjects(drawables,true)[0];
    drawables.forEach(m=>m.visible=field('overlay').checked);
    if(!hit){say('No estimated surface here. Choose an observed surface; missing floor cannot be walked on.');return;}
    const point=new THREE.Vector3(hit.point.x,hit.point.y,hit.point.z);picks.push(point);
    try{
      if(mode==='floor'&&picks.length===3){invalidate();const roomUp=recovered?.initialView?.up;alignment=floorAlignment(picks,new THREE.Vector3(camera.up.x,camera.up.y,camera.up.z),roomUp&&new THREE.Vector3(...roomUp));finish(scale?'Floor reference selected. You can now build walking surfaces; scale still needs verification.':'Floor reference selected. Now pick the measured endpoints.');}
      else if(mode==='measure'&&picks.length===2){
        const metres=Number(field('distance').value),distance=picks[0].distanceTo(picks[1]);
        if(!(metres>0&&metres<=40&&distance>0.001))throw Error('Use a valid measurement and distinct endpoints.');
        invalidate();scale=metres/distance;measurement={metres,endpoints:picks.map(p=>p.toArray())};finish(`Scale estimate: ${scale.toFixed(4)} metres/unit. ${alignment ? "Floor reference is set; you can build walking surfaces." : "Floor reference is missing: choose Pick three floor points and click three separated floor locations."} An assumed distance is not verified scale.`);
      }else if(mode==='spawn'){
        if(!navigation||!field('review').checked)throw Error('Review the geometry and scale first.');
        const nearest=navigation.nearest(point.applyMatrix4(rawToNav));if(!nearest)throw Error('No walkable surface near that point.');
        beginWalk(nearest);
        finish('Experimental walking: WASD; drag to look. Escape pauses. Test walls and furniture before relying on it.');
        persist();
      }else say(`${picks.length} point(s) selected.`);
      button('build').disabled=!(alignment&&scale);
    }catch(e){finish(e.message);}
  });
  function finish(message){mode=null;picks=[];control.enabled=true;say(message);dirty();}
  button('pause').onclick=()=>{pause();say('Walking paused.');};
  button('level').onclick=()=>{upright(true);dirty();};
  field('eye').onchange=()=>{const value=Number(field('eye').value);if(!Number.isFinite(value)||value<1.2||value>1.7){field('eye').value=String(eyeHeight);say('Choose an eye height between 1.2 and 1.7 metres. Check measured scale if furniture still looks too large.');return;}eyeHeight=value;placeCamera();if(state)persist();dirty();};
  window.addEventListener('keydown',event=>{if(event.key==='Escape'){pause();finish('Selection/walking paused.');}});
  field('distance').oninput=()=>{scale=null;measurement=null;invalidate();button('build').disabled=true;};
  field('review').onchange=()=>{if(!field('review').checked)pause();button('spawn').disabled=!navigation||!field('review').checked;};
  async function build(){
    invalidate();const token=generation;button('build').disabled=true;say('Building constrained walking surfaces…');
    try{
      rawToNav=new THREE.Matrix4().compose(new THREE.Vector3(),alignment.quaternion,new THREE.Vector3(scale,scale,scale));
      const origin=alignment.origin.clone().applyMatrix4(rawToNav);rawToNav.setPosition(origin.negate());navToRaw.copy(rawToNav).invert();
      const aligned=new THREE.Group();aligned.add(root.clone(true));aligned.applyMatrix4(rawToNav);aligned.updateMatrixWorld(true);
      const box=new THREE.Box3().setFromObject(aligned),size=box.getSize(new THREE.Vector3());
      if(size.x>40||size.z>40)throw Error('Scale makes this room exceed 40 metres. Check endpoints and outliers.');
      const nav=await buildNavigation(aligned);if(token!==generation){nav.dispose();return false;}navigation=nav;bounds=box;
      mapPoints=[];aligned.traverse(o=>{if(!o.isMesh)return;const a=o.geometry.attributes.position;for(let i=0;i<a.count;i+=12){const p=new THREE.Vector3().fromBufferAttribute(a,i).applyMatrix4(o.matrixWorld);mapPoints.push(p);}});
      mapDirty=true;drawMap();say('Walking surfaces generated, not validated. Inspect coverage, check the review box, then choose a start.');
      return true;
    }catch(e){say(e.message);return false;}finally{button('build').disabled=!(alignment&&scale);}
  }
  button('build').onclick=build;
  function beginWalk(nearest, forward=null){
    // Keep the collision geometry for navigation, but do not draw its debug layer while walking.
    field('overlay').checked=false;drawables.forEach(m=>m.visible=false);
    pause();state=nearest;savedControls={useOrbit:control.useOrbit,moveSpeed:control.moveSpeed,wheelSpeed:control.wheelSpeed};
    const modeSelect=document.getElementById('select-camera-mode');previousCameraMode=modeSelect.value;modeSelect.value='flight';onWalkingStart();
    control.useOrbit=false;control.moveSpeed=1.2/scale;control.wheelSpeed=0;control.enabled=true;
    const up=new THREE.Vector3(0,1,0).transformDirection(navToRaw);camera.up.set(up.x,up.y,up.z);
    placeCamera();
    if(forward)camera.lookAt(new ViewVector3(camera.position.x+forward[0],camera.position.y+forward[1],camera.position.z+forward[2]));
    upright(!forward);button('pause').disabled=false;button('level').disabled=false;button('save').disabled=!sceneIdentity(recovered);
    drawMap();setWalkStatus(true);dirty();
  }
  function persist(){
    if(!state||!sceneIdentity(recovered))return;
    const direction=camera.getWorldDirection(new ViewVector3());
    const raw=new THREE.Vector3().copy(state.point).applyMatrix4(navToRaw);
    try{
      savedSetup=validateWalk({version:1,type:'namma-aholo-walk',profile:WALK_PROFILE,coordinateSpace:'raw-ply-v1',
        sceneIdentity:sceneIdentity(recovered),floor:{origin:alignment.origin.toArray(),quaternion:alignment.quaternion.toArray()},
        metresPerUnit:scale,measurement,eyeHeight,entrance:raw.toArray(),forward:[direction.x,direction.y,direction.z],reviewed:field('review').checked},recovered);
      button('resume').disabled=false;button('export').disabled=false;
      saveWalk(localStorage,recovered,savedSetup);
      field('saved').textContent='Walking entrance saved on this browser. Download setup for a portable backup. This does not certify physical dimensions.';
    }catch(e){field('saved').textContent='Could not save on this browser: '+e.message+(savedSetup?' Download the setup to preserve it.':'');}
  }
  button('save').onclick=persist;
  button('export').onclick=()=>{
    if(!savedSetup)return;
    const blob=new Blob([JSON.stringify(validateWalk(savedSetup,recovered),null,2)],{type:'application/json'});
    const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='namma-walking-setup.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  };
  button('import').onclick=()=>field('import').click();
  field('import').onchange=async()=>{
    const file=field('import').files?.[0],scene=recovered,token=generation;field('import').value='';if(!file)return;
    try{
      if(file.size>65536)throw Error('Walking setup file is too large.');
      const checked=validateWalk(JSON.parse(await file.text()),scene);
      if(token!==generation||scene!==recovered)return;
      savedSetup=checked;button('resume').disabled=false;button('export').disabled=false;
      try{saveWalk(localStorage,recovered,savedSetup);}catch{/* Keep the imported setup usable in this session. */}
      field('saved').textContent='Matching setup loaded. Choose Enter saved walking setup to rebuild and check the entrance.';
    }catch(e){say(e.message);}
  };
  button('resume').onclick=async()=>{
    if(!savedSetup||restoring)return;
    const saved=validateWalk(savedSetup,recovered);restoring=true;button('resume').disabled=true;
    try{
      if(!await load())return;
      const token=generation;
      alignment={origin:new THREE.Vector3().fromArray(saved.floor.origin),quaternion:new THREE.Quaternion().fromArray(saved.floor.quaternion)};
      scale=saved.metresPerUnit;measurement=saved.measurement;eyeHeight=saved.eyeHeight;
      field('distance').value=String(measurement.metres);field('eye').value=String(eyeHeight);
      if(!await build())return;
      // build() increments generation; a source switch during its async work is rejected by build itself.
      if(generation!==token+1)return;
      const nearest=navigation.nearest(new THREE.Vector3().fromArray(saved.entrance).applyMatrix4(rawToNav));
      if(!nearest)throw Error('Saved entrance is no longer walkable. Inspect the surfaces and choose a new start.');
      field('review').checked=true;button('spawn').disabled=false;
      field('overlay').checked=false;drawables.forEach(m=>m.visible=false);
      beginWalk(nearest,saved.forward);say('Saved walking setup restored. WASD to walk; drag to look; Escape pauses.');
    }catch(e){say(e.message);}finally{restoring=false;button('resume').disabled=!savedSetup;}
  };
  function upright(level=false){
    if(!state)return;
    const up=new THREE.Vector3(0,1,0).transformDirection(navToRaw);
    const direction=camera.getWorldDirection(new ViewVector3());
    const forward=new THREE.Vector3(direction.x,direction.y,direction.z);
    const pitch=forward.dot(up);
    const horizontal=forward.clone().addScaledVector(up,-pitch);
    if(horizontal.lengthSq()<1e-8)horizontal.set(0,0,-1).transformDirection(navToRaw);
    horizontal.normalize();
    // Keep mouse-look pitch, but remove roll; avoid a singular look-at at the poles.
    const angle=level?0:Math.asin(THREE.MathUtils.clamp(pitch,-0.996,0.996));
    forward.copy(horizontal).multiplyScalar(Math.cos(angle)).addScaledVector(up,Math.sin(angle));
    camera.up.set(up.x,up.y,up.z);
    camera.lookAt(new ViewVector3(camera.position.x+forward.x,camera.position.y+forward.y,camera.position.z+forward.z));
  }
  function placeCamera(){if(!state)return;const raw=new THREE.Vector3().copy(state.point).add(new THREE.Vector3(0,eyeHeight,0)).applyMatrix4(navToRaw);camera.position.set(raw.x,raw.y,raw.z);}
  function tick(cameraMoved=false){if(!state||!cameraMoved)return false;
    const proposed=new THREE.Vector3(camera.position.x,camera.position.y,camera.position.z).applyMatrix4(rawToNav);
    const delta=proposed.sub(new THREE.Vector3().copy(state.point).add(new THREE.Vector3(0,eyeHeight,0)));delta.y=0;
    // Cap accidental teleports from nonwalking controls, then constrain all motion to the navmesh.
    if(delta.length()>0.3)delta.setLength(0.3);if(delta.lengthSq()>1e-12)navigation.move(state,delta);placeCamera();upright();
    const now=performance.now();if(now-lastMapTime>=100){drawMap();lastMapTime=now;}return true;
  }
  function drawMap(){ctx.clearRect(0,0,240,180);if(!bounds)return;const size=bounds.getSize(new THREE.Vector3());const k=Math.min(220/Math.max(size.x,.1),160/Math.max(size.z,.1));
    const xy=p=>[10+(p.x-bounds.min.x)*k,10+(p.z-bounds.min.z)*k];
    if(mapDirty){mapCtx.clearRect(0,0,240,180);mapCtx.fillStyle='#667c86';for(const p of mapPoints){const[x,y]=xy(p);mapCtx.fillRect(x,y,1,1);}mapDirty=false;}
    ctx.drawImage(mapBase,0,0);if(state){const[x,y]=xy(state.point);ctx.fillStyle='#39e6b4';ctx.beginPath();ctx.arc(x,y,4,0,Math.PI*2);ctx.fill();}}
  return {setSource,tick,pause,isWalking:()=>Boolean(state),hasSavedSetup:()=>Boolean(savedSetup),resumeSaved:()=>button('resume').click()};
}

</file>

<file src="viewer/package-lock.json">
{
  "name": "namma-space-viewer",
  "version": "0.1.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "namma-space-viewer",
      "version": "0.1.0",
      "dependencies": {
        "@manycore/aholo-viewer": "file:vendor/manycore-aholo-viewer-1.10.0.tgz",
        "recast-navigation": "^0.43.1",
        "three": "^0.186.1"
      },
      "devDependencies": {
        "@playcanvas/splat-transform": "3.10.1",
        "vite": "^6.4.4"
      },
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@adobe/spz": {
      "version": "0.2.3",
      "resolved": "https://registry.npmjs.org/@adobe/spz/-/spz-0.2.3.tgz",
      "integrity": "sha512-iMiIB+FUxQ2vaNxP012fdIVd4yugyq0PUXBaknGfYDE3xpTNU5PrhbLtnDTGFE9anKOwjneOuanSKqaaNpC68Q==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/@esbuild/aix-ppc64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/aix-ppc64/-/aix-ppc64-0.25.12.tgz",
      "integrity": "sha512-Hhmwd6CInZ3dwpuGTF8fJG6yoWmsToE+vYgD4nytZVxcu1ulHpUQRAB1UJ8+N1Am3Mz4+xOByoQoSZf4D+CpkA==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "aix"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/android-arm": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/android-arm/-/android-arm-0.25.12.tgz",
      "integrity": "sha512-VJ+sKvNA/GE7Ccacc9Cha7bpS8nyzVv0jdVgwNDaR4gDMC/2TTRc33Ip8qrNYUcpkOHUT5OZ0bUcNNVZQ9RLlg==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/android-arm64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/android-arm64/-/android-arm64-0.25.12.tgz",
      "integrity": "sha512-6AAmLG7zwD1Z159jCKPvAxZd4y/VTO0VkprYy+3N2FtJ8+BQWFXU+OxARIwA46c5tdD9SsKGZ/1ocqBS/gAKHg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/android-x64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/android-x64/-/android-x64-0.25.12.tgz",
      "integrity": "sha512-5jbb+2hhDHx5phYR2By8GTWEzn6I9UqR11Kwf22iKbNpYrsmRB18aX/9ivc5cabcUiAT/wM+YIZ6SG9QO6a8kg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/darwin-arm64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/darwin-arm64/-/darwin-arm64-0.25.12.tgz",
      "integrity": "sha512-N3zl+lxHCifgIlcMUP5016ESkeQjLj/959RxxNYIthIg+CQHInujFuXeWbWMgnTo4cp5XVHqFPmpyu9J65C1Yg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/darwin-x64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/darwin-x64/-/darwin-x64-0.25.12.tgz",
      "integrity": "sha512-HQ9ka4Kx21qHXwtlTUVbKJOAnmG1ipXhdWTmNXiPzPfWKpXqASVcWdnf2bnL73wgjNrFXAa3yYvBSd9pzfEIpA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/freebsd-arm64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/freebsd-arm64/-/freebsd-arm64-0.25.12.tgz",
      "integrity": "sha512-gA0Bx759+7Jve03K1S0vkOu5Lg/85dou3EseOGUes8flVOGxbhDDh/iZaoek11Y8mtyKPGF3vP8XhnkDEAmzeg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/freebsd-x64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/freebsd-x64/-/freebsd-x64-0.25.12.tgz",
      "integrity": "sha512-TGbO26Yw2xsHzxtbVFGEXBFH0FRAP7gtcPE7P5yP7wGy7cXK2oO7RyOhL5NLiqTlBh47XhmIUXuGciXEqYFfBQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-arm": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-arm/-/linux-arm-0.25.12.tgz",
      "integrity": "sha512-lPDGyC1JPDou8kGcywY0YILzWlhhnRjdof3UlcoqYmS9El818LLfJJc3PXXgZHrHCAKs/Z2SeZtDJr5MrkxtOw==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-arm64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-arm64/-/linux-arm64-0.25.12.tgz",
      "integrity": "sha512-8bwX7a8FghIgrupcxb4aUmYDLp8pX06rGh5HqDT7bB+8Rdells6mHvrFHHW2JAOPZUbnjUpKTLg6ECyzvas2AQ==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-ia32": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-ia32/-/linux-ia32-0.25.12.tgz",
      "integrity": "sha512-0y9KrdVnbMM2/vG8KfU0byhUN+EFCny9+8g202gYqSSVMonbsCfLjUO+rCci7pM0WBEtz+oK/PIwHkzxkyharA==",
      "cpu": [
        "ia32"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-loong64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-loong64/-/linux-loong64-0.25.12.tgz",
      "integrity": "sha512-h///Lr5a9rib/v1GGqXVGzjL4TMvVTv+s1DPoxQdz7l/AYv6LDSxdIwzxkrPW438oUXiDtwM10o9PmwS/6Z0Ng==",
      "cpu": [
        "loong64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-mips64el": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-mips64el/-/linux-mips64el-0.25.12.tgz",
      "integrity": "sha512-iyRrM1Pzy9GFMDLsXn1iHUm18nhKnNMWscjmp4+hpafcZjrr2WbT//d20xaGljXDBYHqRcl8HnxbX6uaA/eGVw==",
      "cpu": [
        "mips64el"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-ppc64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-ppc64/-/linux-ppc64-0.25.12.tgz",
      "integrity": "sha512-9meM/lRXxMi5PSUqEXRCtVjEZBGwB7P/D4yT8UG/mwIdze2aV4Vo6U5gD3+RsoHXKkHCfSxZKzmDssVlRj1QQA==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-riscv64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-riscv64/-/linux-riscv64-0.25.12.tgz",
      "integrity": "sha512-Zr7KR4hgKUpWAwb1f3o5ygT04MzqVrGEGXGLnj15YQDJErYu/BGg+wmFlIDOdJp0PmB0lLvxFIOXZgFRrdjR0w==",
      "cpu": [
        "riscv64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-s390x": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-s390x/-/linux-s390x-0.25.12.tgz",
      "integrity": "sha512-MsKncOcgTNvdtiISc/jZs/Zf8d0cl/t3gYWX8J9ubBnVOwlk65UIEEvgBORTiljloIWnBzLs4qhzPkJcitIzIg==",
      "cpu": [
        "s390x"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-x64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-x64/-/linux-x64-0.25.12.tgz",
      "integrity": "sha512-uqZMTLr/zR/ed4jIGnwSLkaHmPjOjJvnm6TVVitAa08SLS9Z0VM8wIRx7gWbJB5/J54YuIMInDquWyYvQLZkgw==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/netbsd-arm64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/netbsd-arm64/-/netbsd-arm64-0.25.12.tgz",
      "integrity": "sha512-xXwcTq4GhRM7J9A8Gv5boanHhRa/Q9KLVmcyXHCTaM4wKfIpWkdXiMog/KsnxzJ0A1+nD+zoecuzqPmCRyBGjg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "netbsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/netbsd-x64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/netbsd-x64/-/netbsd-x64-0.25.12.tgz",
      "integrity": "sha512-Ld5pTlzPy3YwGec4OuHh1aCVCRvOXdH8DgRjfDy/oumVovmuSzWfnSJg+VtakB9Cm0gxNO9BzWkj6mtO1FMXkQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "netbsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/openbsd-arm64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/openbsd-arm64/-/openbsd-arm64-0.25.12.tgz",
      "integrity": "sha512-fF96T6KsBo/pkQI950FARU9apGNTSlZGsv1jZBAlcLL1MLjLNIWPBkj5NlSz8aAzYKg+eNqknrUJ24QBybeR5A==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openbsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/openbsd-x64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/openbsd-x64/-/openbsd-x64-0.25.12.tgz",
      "integrity": "sha512-MZyXUkZHjQxUvzK7rN8DJ3SRmrVrke8ZyRusHlP+kuwqTcfWLyqMOE3sScPPyeIXN/mDJIfGXvcMqCgYKekoQw==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openbsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/openharmony-arm64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/openharmony-arm64/-/openharmony-arm64-0.25.12.tgz",
      "integrity": "sha512-rm0YWsqUSRrjncSXGA7Zv78Nbnw4XL6/dzr20cyrQf7ZmRcsovpcRBdhD43Nuk3y7XIoW2OxMVvwuRvk9XdASg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openharmony"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/sunos-x64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/sunos-x64/-/sunos-x64-0.25.12.tgz",
      "integrity": "sha512-3wGSCDyuTHQUzt0nV7bocDy72r2lI33QL3gkDNGkod22EsYl04sMf0qLb8luNKTOmgF/eDEDP5BFNwoBKH441w==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "sunos"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/win32-arm64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-arm64/-/win32-arm64-0.25.12.tgz",
      "integrity": "sha512-rMmLrur64A7+DKlnSuwqUdRKyd3UE7oPJZmnljqEptesKM8wx9J8gx5u0+9Pq0fQQW8vqeKebwNXdfOyP+8Bsg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/win32-ia32": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-ia32/-/win32-ia32-0.25.12.tgz",
      "integrity": "sha512-HkqnmmBoCbCwxUKKNPBixiWDGCpQGVsrQfJoVGYLPT41XWF8lHuE5N6WhVia2n4o5QK5M4tYr21827fNhi4byQ==",
      "cpu": [
        "ia32"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/win32-x64": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-x64/-/win32-x64-0.25.12.tgz",
      "integrity": "sha512-alJC0uCZpTFrSL0CCDjcgleBXPnCrEAhTBILpeAp7M/OFgoqtAetfBzX0xM00MUsVVPpVjlPuMbREqnZCXaTnA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@manycore/aholo-viewer": {
      "version": "1.10.0",
      "resolved": "file:vendor/manycore-aholo-viewer-1.10.0.tgz",
      "integrity": "sha512-/09Y2IHMxH8Mc5T8vcVrh7u6h6M53gnbBM6ChQQ5QsnrdozsCtxzzsD3qIWbBdmFE+g+Ts37GbCasoW5T2be7A==",
      "license": "MIT"
    },
    "node_modules/@napi-rs/lzma-linux-x64-gnu": {
      "version": "1.5.1",
      "resolved": "https://registry.npmjs.org/@napi-rs/lzma-linux-x64-gnu/-/lzma-linux-x64-gnu-1.5.1.tgz",
      "integrity": "sha512-oTXEIha4SsuXdTA4Iyskj0kpdx2yVXdhd75c2v3xGrHFfVMsbhTPZU/nMPL4sWKo4pBHm3aucLaqGlF696dTyQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^22.20 || ^24.12 || >=25"
      }
    },
    "node_modules/@playcanvas/splat-transform": {
      "version": "3.10.1",
      "resolved": "https://registry.npmjs.org/@playcanvas/splat-transform/-/splat-transform-3.10.1.tgz",
      "integrity": "sha512-2/9uCCBHNCJrhGAePCuWFtcxuCqQB93WzKeH4GJ69NJ5Y7cWIKpMsXaBLDaPCAizbYnpAj/eGOMOSHuKBKiZuA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@adobe/spz": "0.2.3",
        "webgpu": "0.6.2"
      },
      "bin": {
        "splat-transform": "bin/cli.mjs"
      },
      "engines": {
        "node": ">=22.0.0"
      },
      "peerDependencies": {
        "playcanvas": "^2.0.0"
      }
    },
    "node_modules/@recast-navigation/core": {
      "version": "0.43.1",
      "resolved": "https://registry.npmjs.org/@recast-navigation/core/-/core-0.43.1.tgz",
      "integrity": "sha512-4igfPgnoV90O92sDSIA0xHa6tanh3z/udlgGmD0SqGQ6PKV4JS2l9jWO8YnxfZuXP/NV52H4c5FU6pSdZc9WDA==",
      "license": "MIT",
      "dependencies": {
        "@recast-navigation/wasm": "0.43.1"
      }
    },
    "node_modules/@recast-navigation/generators": {
      "version": "0.43.1",
      "resolved": "https://registry.npmjs.org/@recast-navigation/generators/-/generators-0.43.1.tgz",
      "integrity": "sha512-w7r6k/A93wWxuSN+Lg+PmlsUVXq06r5bqXmBglolxqDt2O/Y776BIhYtb6P2P6pbYqDWORu9NCZZJzfY4FNpaA==",
      "license": "MIT",
      "dependencies": {
        "@recast-navigation/core": "0.43.1",
        "@recast-navigation/wasm": "0.43.1"
      }
    },
    "node_modules/@recast-navigation/wasm": {
      "version": "0.43.1",
      "resolved": "https://registry.npmjs.org/@recast-navigation/wasm/-/wasm-0.43.1.tgz",
      "integrity": "sha512-XFL6PhO8JodwXUHBSAkfaLUdUEweIkJsdP3HTmtJvMs5fkqEWxWJmBskZlACHJepv55NAriqWxOtuLlG3t7+Hg==",
      "license": "MIT"
    },
    "node_modules/@rollup/rollup-android-arm-eabi": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-android-arm-eabi/-/rollup-android-arm-eabi-4.66.0.tgz",
      "integrity": "sha512-7y4XeoUHPecjfUDRmap8U0q6bjfLAPn7uOGT8BKyqy8uNDOjsGS8rlBhOx6sZLVwwjN6hapvGl2mW9/IS6UNww==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ]
    },
    "node_modules/@rollup/rollup-android-arm64": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-android-arm64/-/rollup-android-arm64-4.66.0.tgz",
      "integrity": "sha512-e8WugYZXpgqrlMXLCudYVRAxAcK7AIY36JxRDwFRD38L9q62G1VsEUW6ijXxzjxYjNB8i1zo3B/ycIQ/qjLC/Q==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ]
    },
    "node_modules/@rollup/rollup-darwin-arm64": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-darwin-arm64/-/rollup-darwin-arm64-4.66.0.tgz",
      "integrity": "sha512-6vkDCfyDjNLokh+Rt1D2KtNgFFMEPdkWha/mbtP4cSjh9xiN8T/JBS/A7nDYKjmMAXHrvR9J3AzUk2LtFbIBLg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ]
    },
    "node_modules/@rollup/rollup-darwin-x64": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-darwin-x64/-/rollup-darwin-x64-4.66.0.tgz",
      "integrity": "sha512-/mzZAX0+Q6eXxvkR0HB0RZCCrsbmFD8DpsvCQoMYABDfq/DjqkbfytuJ7GvZ4AhR/Mgis2fXbZrGqfbcK2Z5fA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ]
    },
    "node_modules/@rollup/rollup-freebsd-arm64": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-freebsd-arm64/-/rollup-freebsd-arm64-4.66.0.tgz",
      "integrity": "sha512-JQJx9E8tUjGqed1RevDmoHaS3V30ODdV8uyvGxlwd4K5se6bkPrMeltSybqAtpJ+ltDRfo7FORQaJG2Hd5nGog==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ]
    },
    "node_modules/@rollup/rollup-freebsd-x64": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-freebsd-x64/-/rollup-freebsd-x64-4.66.0.tgz",
      "integrity": "sha512-GEaUQQjMaG7X1304qMgqLjzCKv6CdDirzJSS+UqUs3xhJ9X2Kjzu0JDbLoUU42FWxwmZqz+SsgU1SlQv9GNRVA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ]
    },
    "node_modules/@rollup/rollup-linux-arm-gnueabihf": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-arm-gnueabihf/-/rollup-linux-arm-gnueabihf-4.66.0.tgz",
      "integrity": "sha512-DgmAU9N0NhDQDzHgFUocDio7zRO8jR/nY/obDGvCR8zbJ6J77Fg6X49yPuExJUpYPbC82EOaRhG969pWzUSnHQ==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-arm-musleabihf": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-arm-musleabihf/-/rollup-linux-arm-musleabihf-4.66.0.tgz",
      "integrity": "sha512-zG09YZ+sk/HoHq+P9gYB0EseQ3M20RbDuKGWey6fbiMDV1LxfXvhgSW9jDaCcvFPMgfLXpimzXY+UYvA8R2mLQ==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-arm64-gnu": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-arm64-gnu/-/rollup-linux-arm64-gnu-4.66.0.tgz",
      "integrity": "sha512-vlArhgyXbcVc1D4WZPoiYuqJIaMiSHBj6etRXua0KlfjlZeuiQyVAPYi0/N49O4mSp3u1iGUBLEjNa8ec81XZg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-arm64-musl": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-arm64-musl/-/rollup-linux-arm64-musl-4.66.0.tgz",
      "integrity": "sha512-RxJZtk0G87YPotDaRDvRqStV8cbqLSC5TroHvQHHKsqBg0ok64RxKgtXeFsa7FBcy7mb4crBrG3xK8USWIqWNA==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-loong64-gnu": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-loong64-gnu/-/rollup-linux-loong64-gnu-4.66.0.tgz",
      "integrity": "sha512-qlGcw959PrLLkZhiBxF3OZ6SQvj+OKY85mCqGNgSRs4LZlDJ6ICqmz6UdxtINdhcXYwNIbZoapQVBAmZlD2hUQ==",
      "cpu": [
        "loong64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-loong64-musl": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-loong64-musl/-/rollup-linux-loong64-musl-4.66.0.tgz",
      "integrity": "sha512-TvTI/7Cy0WvRA1SXgwzu6bwXBnMpmeT/ln5q7WvSpqmXy1VbmEnY8HVIDQNBiaHJvoWqRr0M4FNo7qiqtyMaFw==",
      "cpu": [
        "loong64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-ppc64-gnu": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-ppc64-gnu/-/rollup-linux-ppc64-gnu-4.66.0.tgz",
      "integrity": "sha512-UZEDkSoDRZ50NyLj70nO6mpIK3dvs2cPTTvQb1bA/PBDmr9fvn5KiESuGfh6srd7Zi6Lt9Sv2sVrFr1QoHLvPQ==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-ppc64-musl": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-ppc64-musl/-/rollup-linux-ppc64-musl-4.66.0.tgz",
      "integrity": "sha512-VRbxTvagLh3HRcysx1CNq+HHcvJbSebNI6fCbk7jwmmWHkXjrSIV3igXBpRHUTFdg0pagWGu50xoSZXnrZHjVQ==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-riscv64-gnu": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-riscv64-gnu/-/rollup-linux-riscv64-gnu-4.66.0.tgz",
      "integrity": "sha512-uWdJpvYqh0LE/i+YBL3sMX0a2kUkICENjmrPmyBmMOFc3jMrs6MSQH/pMD+VIpGEoUcr3XkHGLLfymzIqPSRRg==",
      "cpu": [
        "riscv64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-riscv64-musl": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-riscv64-musl/-/rollup-linux-riscv64-musl-4.66.0.tgz",
      "integrity": "sha512-3FUd88pxgWAjK60OgCrika1AcNG+u8zaCdWjg4TlcZTDkt5TGyci8ZU64l3OJ9ax0MEjw3P80B/3PoSQDCLwJQ==",
      "cpu": [
        "riscv64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-s390x-gnu": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-s390x-gnu/-/rollup-linux-s390x-gnu-4.66.0.tgz",
      "integrity": "sha512-qT2rMmgyej62g5AdwktK+Bt2lBu497pzWZe12TTQ5JmZjOYPnEwcPEAOSLTBxBV+6gIES75rXm219v/QkT397A==",
      "cpu": [
        "s390x"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-x64-gnu": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-x64-gnu/-/rollup-linux-x64-gnu-4.66.0.tgz",
      "integrity": "sha512-E46rnZgp7J84Qwe8RMlF+rgimnDo/9fuiGbUArGB0ZkMWf97O7yeSCfKls5x/YJOF0RcuSe9RctuKe1hlxICiA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-x64-musl": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-x64-musl/-/rollup-linux-x64-musl-4.66.0.tgz",
      "integrity": "sha512-Uz1HiZe+qBzqgdPsON+z0wRx3WdATuyzwvGT6cr2VZVrqqko0ZJVfkrQJtwDMuDcAfXYdo7XucaxJ7lTLjEcgg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-openbsd-x64": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-openbsd-x64/-/rollup-openbsd-x64-4.66.0.tgz",
      "integrity": "sha512-Ph7TX3Ex5qdfcb7Tc6eEPugVkRfJ501eTovO4T5029YObfpZ7dzn3RiwpFvGp50nk2QUhvBMZ0PFGlEj6pOYTg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openbsd"
      ]
    },
    "node_modules/@rollup/rollup-openharmony-arm64": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-openharmony-arm64/-/rollup-openharmony-arm64-4.66.0.tgz",
      "integrity": "sha512-nZYPEya7ZkeNxUEiF7qmNZbyLTyRN3MK5cO22KqsaoneUzXJuzBIQRw+7BEQy9LGj2O5vrCE9V3EpK06FYo1tQ==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openharmony"
      ]
    },
    "node_modules/@rollup/rollup-win32-arm64-msvc": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-win32-arm64-msvc/-/rollup-win32-arm64-msvc-4.66.0.tgz",
      "integrity": "sha512-u7aTfS3R6C4hRsqXSzaO6qLZYLVuMkHMvcWlux4IM8IJif1VCl2cgPBSo5gSNoFoStQypQP+qwq8W1IyFBf1QQ==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ]
    },
    "node_modules/@rollup/rollup-win32-ia32-msvc": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-win32-ia32-msvc/-/rollup-win32-ia32-msvc-4.66.0.tgz",
      "integrity": "sha512-e+i9ueHrH1Bafb0cf0woAIVJbYcoC8vRaD+vz+Xi8w6jz9cYJSV3vyKO6ELGSZ6g4W4MJOm2WPLN4/nQf77h7w==",
      "cpu": [
        "ia32"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ]
    },
    "node_modules/@rollup/rollup-win32-x64-gnu": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-win32-x64-gnu/-/rollup-win32-x64-gnu-4.66.0.tgz",
      "integrity": "sha512-KfTCbrtr2zXTqH2E1F+uYlFTrYibxHKqPAHobpd8Kfg49cEHmuHebOidCTDRgqG1suaPFX7oejFQeGE71zWKfA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ]
    },
    "node_modules/@rollup/rollup-win32-x64-msvc": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-win32-x64-msvc/-/rollup-win32-x64-msvc-4.66.0.tgz",
      "integrity": "sha512-xA+neBh1bqkqaS3b48T2UHZnDsTIpb9B0h+TdBzynjF/ymCpYndhfY10RqW0qSKB1HqqQA83mINVhAdwA+mETg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ]
    },
    "node_modules/@types/estree": {
      "version": "1.0.9",
      "resolved": "https://registry.npmjs.org/@types/estree/-/estree-1.0.9.tgz",
      "integrity": "sha512-GhdPgy1el4/ImP05X05Uw4cw2/M93BCUmnEvWZNStlCzEKME4Fkk+YpoA5OiHNQmoS7Cafb8Xa3Pya8m1Qrzeg==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@types/webxr": {
      "version": "0.5.24",
      "resolved": "https://registry.npmjs.org/@types/webxr/-/webxr-0.5.24.tgz",
      "integrity": "sha512-h8fgEd/DpoS9CBrjEQXR+dIDraopAEfu4wYVNY2tEPwk60stPWhvZMf4Foo5FakuQ7HFZoa8WceaWFervK2Ovg==",
      "dev": true,
      "license": "MIT",
      "peer": true
    },
    "node_modules/@webgpu/types": {
      "version": "0.1.74",
      "resolved": "https://registry.npmjs.org/@webgpu/types/-/types-0.1.74.tgz",
      "integrity": "sha512-lgiI4hbuLcI9unnm2cL/tvCaQU45dp0xcLWJh5uB/9MBGvIA4F8XIk7nSiBeg+K4xWGYwgZKn80LmERI5CxoTA==",
      "dev": true,
      "license": "BSD-3-Clause"
    },
    "node_modules/debug": {
      "version": "4.4.3",
      "resolved": "https://registry.npmjs.org/debug/-/debug-4.4.3.tgz",
      "integrity": "sha512-RGwwWnwQvkVfavKVt22FGLw+xYSdzARwm0ru6DhTVA3umU5hZc28V3kO4stgYryrTlLpuvgI9GiijltAjNbcqA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ms": "^2.1.3"
      },
      "engines": {
        "node": ">=6.0"
      },
      "peerDependenciesMeta": {
        "supports-color": {
          "optional": true
        }
      }
    },
    "node_modules/esbuild": {
      "version": "0.25.12",
      "resolved": "https://registry.npmjs.org/esbuild/-/esbuild-0.25.12.tgz",
      "integrity": "sha512-bbPBYYrtZbkt6Os6FiTLCTFxvq4tt3JKall1vRwshA3fdVztsLAatFaZobhkBC8/BrPetoa0oksYoKXoG4ryJg==",
      "dev": true,
      "hasInstallScript": true,
      "license": "MIT",
      "bin": {
        "esbuild": "bin/esbuild"
      },
      "engines": {
        "node": ">=18"
      },
      "optionalDependencies": {
        "@esbuild/aix-ppc64": "0.25.12",
        "@esbuild/android-arm": "0.25.12",
        "@esbuild/android-arm64": "0.25.12",
        "@esbuild/android-x64": "0.25.12",
        "@esbuild/darwin-arm64": "0.25.12",
        "@esbuild/darwin-x64": "0.25.12",
        "@esbuild/freebsd-arm64": "0.25.12",
        "@esbuild/freebsd-x64": "0.25.12",
        "@esbuild/linux-arm": "0.25.12",
        "@esbuild/linux-arm64": "0.25.12",
        "@esbuild/linux-ia32": "0.25.12",
        "@esbuild/linux-loong64": "0.25.12",
        "@esbuild/linux-mips64el": "0.25.12",
        "@esbuild/linux-ppc64": "0.25.12",
        "@esbuild/linux-riscv64": "0.25.12",
        "@esbuild/linux-s390x": "0.25.12",
        "@esbuild/linux-x64": "0.25.12",
        "@esbuild/netbsd-arm64": "0.25.12",
        "@esbuild/netbsd-x64": "0.25.12",
        "@esbuild/openbsd-arm64": "0.25.12",
        "@esbuild/openbsd-x64": "0.25.12",
        "@esbuild/openharmony-arm64": "0.25.12",
        "@esbuild/sunos-x64": "0.25.12",
        "@esbuild/win32-arm64": "0.25.12",
        "@esbuild/win32-ia32": "0.25.12",
        "@esbuild/win32-x64": "0.25.12"
      }
    },
    "node_modules/fdir": {
      "version": "6.5.0",
      "resolved": "https://registry.npmjs.org/fdir/-/fdir-6.5.0.tgz",
      "integrity": "sha512-tIbYtZbucOs0BRGqPJkshJUYdL+SDH7dVM8gjy+ERp3WAUjLEFJE+02kanyHtwjWOnwrKYBiwAmM0p4kLJAnXg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=12.0.0"
      },
      "peerDependencies": {
        "picomatch": "^3 || ^4"
      },
      "peerDependenciesMeta": {
        "picomatch": {
          "optional": true
        }
      }
    },
    "node_modules/fsevents": {
      "version": "2.3.3",
      "resolved": "https://registry.npmjs.org/fsevents/-/fsevents-2.3.3.tgz",
      "integrity": "sha512-5xoDfX+fL7faATnagmWPpbFtwh/R77WmMMqqHGS65C3vvB0YHrgF+B1YmZ3441tMj5n63k0212XNoJwzlhffQw==",
      "dev": true,
      "hasInstallScript": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": "^8.16.0 || ^10.6.0 || >=11.0.0"
      }
    },
    "node_modules/ms": {
      "version": "2.1.3",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.1.3.tgz",
      "integrity": "sha512-6FlzubTLZG3J2a/NVCAleEhjzq5oxgHyaCU9yYXvcLsvoVaHJq/s5xXI6/XXP6tz7R9xAOtHnSO/tXtF3WRTlA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/nanoid": {
      "version": "3.3.20",
      "resolved": "https://registry.npmjs.org/nanoid/-/nanoid-3.3.20.tgz",
      "integrity": "sha512-uKdg2G3GNCKQn9byYOpxbGqrT2fGO5KRt5J/8b3pok8rT6qxGWF6hxMyJiEYtAf+FVyYuD9hRaDqX5uPFYJ4ZQ==",
      "dev": true,
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "bin": {
        "nanoid": "bin/nanoid.cjs"
      },
      "engines": {
        "node": "^10 || ^12 || ^13.7 || ^14 || >=15.0.1"
      }
    },
    "node_modules/picocolors": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/picocolors/-/picocolors-1.1.1.tgz",
      "integrity": "sha512-xceH2snhtb5M9liqDsmEw56le376mTZkEX/jEb/RxNFyegNul7eNslCXP9FDj/Lcu0X8KEyMceP2ntpaHrDEVA==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/picomatch": {
      "version": "4.0.7",
      "resolved": "https://registry.npmjs.org/picomatch/-/picomatch-4.0.7.tgz",
      "integrity": "sha512-qcJu88Q2IWqJsDD529JKMdwGm/dvInW4HvQnRwiH9JtihJvzGOscDtHE3x1pBKeUOTysQ8kVmLnJ2kJu7yhcGA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/jonschlinkert"
      }
    },
    "node_modules/playcanvas": {
      "version": "2.23.3",
      "resolved": "https://registry.npmjs.org/playcanvas/-/playcanvas-2.23.3.tgz",
      "integrity": "sha512-hjDdo5yFtVr/WmDh59pRrT1LC+Rfpq4VXB8Xt3AMB8GfWXj9JzOMq3x+3FTmq/2L2gN37q9V1LMZaLuYshzMXQ==",
      "dev": true,
      "license": "MIT",
      "peer": true,
      "dependencies": {
        "@types/webxr": "^0.5.24",
        "@webgpu/types": "^0.1.70"
      },
      "engines": {
        "node": ">=18.3.0"
      }
    },
    "node_modules/postcss": {
      "version": "8.5.32",
      "resolved": "https://registry.npmjs.org/postcss/-/postcss-8.5.32.tgz",
      "integrity": "sha512-LJlKCCAUFKOuZxipUdYw1NzIITEsPcgyOG9LkvRJvuKj/bRzbuRY0ARXvL0pWGpsZvn8jku+LMep2eU0seHp8g==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/postcss"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "nanoid": "^3.3.20",
        "picocolors": "^1.1.1",
        "source-map-js": "^1.2.2"
      },
      "engines": {
        "node": "^10 || ^12 || >=14"
      }
    },
    "node_modules/recast-navigation": {
      "version": "0.43.1",
      "resolved": "https://registry.npmjs.org/recast-navigation/-/recast-navigation-0.43.1.tgz",
      "integrity": "sha512-BVBQEHE6uqD36opJomVkI5TxMVZ8bBLdDn90mYtBUYJnNlqEuNFOL8DH8lLOksfVVaC+kjykYuS57P6MrxVB7A==",
      "license": "MIT",
      "dependencies": {
        "@recast-navigation/core": "0.43.1",
        "@recast-navigation/generators": "0.43.1"
      }
    },
    "node_modules/rollup": {
      "version": "4.66.0",
      "resolved": "https://registry.npmjs.org/rollup/-/rollup-4.66.0.tgz",
      "integrity": "sha512-Onq6/qO4ARhxIs+jYiHE0pYehadLyMECAiGEqQ+0/aWND3+2PmifJIIqBLYtuBODqHTlOUEQFtIVPyCy0Lck7A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@types/estree": "1.0.9"
      },
      "bin": {
        "rollup": "dist/bin/rollup"
      },
      "engines": {
        "node": ">=18.0.0",
        "npm": ">=8.0.0"
      },
      "optionalDependencies": {
        "@napi-rs/lzma-linux-x64-gnu": "1.5.1",
        "@rollup/rollup-android-arm-eabi": "4.66.0",
        "@rollup/rollup-android-arm64": "4.66.0",
        "@rollup/rollup-darwin-arm64": "4.66.0",
        "@rollup/rollup-darwin-x64": "4.66.0",
        "@rollup/rollup-freebsd-arm64": "4.66.0",
        "@rollup/rollup-freebsd-x64": "4.66.0",
        "@rollup/rollup-linux-arm-gnueabihf": "4.66.0",
        "@rollup/rollup-linux-arm-musleabihf": "4.66.0",
        "@rollup/rollup-linux-arm64-gnu": "4.66.0",
        "@rollup/rollup-linux-arm64-musl": "4.66.0",
        "@rollup/rollup-linux-loong64-gnu": "4.66.0",
        "@rollup/rollup-linux-loong64-musl": "4.66.0",
        "@rollup/rollup-linux-ppc64-gnu": "4.66.0",
        "@rollup/rollup-linux-ppc64-musl": "4.66.0",
        "@rollup/rollup-linux-riscv64-gnu": "4.66.0",
        "@rollup/rollup-linux-riscv64-musl": "4.66.0",
        "@rollup/rollup-linux-s390x-gnu": "4.66.0",
        "@rollup/rollup-linux-x64-gnu": "4.66.0",
        "@rollup/rollup-linux-x64-musl": "4.66.0",
        "@rollup/rollup-openbsd-x64": "4.66.0",
        "@rollup/rollup-openharmony-arm64": "4.66.0",
        "@rollup/rollup-win32-arm64-msvc": "4.66.0",
        "@rollup/rollup-win32-ia32-msvc": "4.66.0",
        "@rollup/rollup-win32-x64-gnu": "4.66.0",
        "@rollup/rollup-win32-x64-msvc": "4.66.0",
        "fsevents": "~2.3.2"
      }
    },
    "node_modules/source-map-js": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/source-map-js/-/source-map-js-1.2.2.tgz",
      "integrity": "sha512-KGj/8Y43x35aZVDtt+J4mK1hoLGHULMYfSkODJNQjNDC3oW1PqPoxMwo0pLUsWM/UEGzON/NxeHywEfNXNP3Vw==",
      "dev": true,
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/three": {
      "version": "0.186.1",
      "resolved": "https://registry.npmjs.org/three/-/three-0.186.1.tgz",
      "integrity": "sha512-blFeqb49wRCSGUGj7gtpfnSGHy2lwDk94RhUmS1c/hTby70kvChbWpkJ4Pm1390LqzzvTmzgXKHPEafJwCb8jA==",
      "license": "MIT"
    },
    "node_modules/tinyglobby": {
      "version": "0.2.17",
      "resolved": "https://registry.npmjs.org/tinyglobby/-/tinyglobby-0.2.17.tgz",
      "integrity": "sha512-wXR/dYpcqKmfWpEdZjiKJOwCNFndD0DMnrW/cYjVGttEkBfVgcLFHoNrlj47mjOVic9yyNu65alsgF4NQyTa2g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "fdir": "^6.5.0",
        "picomatch": "^4.0.4"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "funding": {
        "url": "https://github.com/sponsors/SuperchupuDev"
      }
    },
    "node_modules/vite": {
      "version": "6.4.5",
      "resolved": "https://registry.npmjs.org/vite/-/vite-6.4.5.tgz",
      "integrity": "sha512-4enwjFfi4IwtEh0w+jPzpLVOFQiPHmmzPxcHXQOyEur47o6u0jE573DmGpjA+7irXoMLYRZD5ZaFUEneS3abPg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "esbuild": "^0.25.0",
        "fdir": "^6.4.4",
        "picomatch": "^4.0.2",
        "postcss": "^8.5.3",
        "rollup": "^4.34.9",
        "tinyglobby": "^0.2.13"
      },
      "bin": {
        "vite": "bin/vite.js"
      },
      "engines": {
        "node": "^18.0.0 || ^20.0.0 || >=22.0.0"
      },
      "funding": {
        "url": "https://github.com/vitejs/vite?sponsor=1"
      },
      "optionalDependencies": {
        "fsevents": "~2.3.3"
      },
      "peerDependencies": {
        "@types/node": "^18.0.0 || ^20.0.0 || >=22.0.0",
        "jiti": ">=1.21.0",
        "less": "*",
        "lightningcss": "^1.21.0",
        "sass": "*",
        "sass-embedded": "*",
        "stylus": "*",
        "sugarss": "*",
        "terser": "^5.16.0",
        "tsx": "^4.8.1",
        "yaml": "^2.4.2"
      },
      "peerDependenciesMeta": {
        "@types/node": {
          "optional": true
        },
        "jiti": {
          "optional": true
        },
        "less": {
          "optional": true
        },
        "lightningcss": {
          "optional": true
        },
        "sass": {
          "optional": true
        },
        "sass-embedded": {
          "optional": true
        },
        "stylus": {
          "optional": true
        },
        "sugarss": {
          "optional": true
        },
        "terser": {
          "optional": true
        },
        "tsx": {
          "optional": true
        },
        "yaml": {
          "optional": true
        }
      }
    },
    "node_modules/webgpu": {
      "version": "0.6.2",
      "resolved": "https://registry.npmjs.org/webgpu/-/webgpu-0.6.2.tgz",
      "integrity": "sha512-3L4GfmqJLvYUIEWJngEQY+2HQiUlAFkg8+P8NDDj3Xx5hHHIFO/r8JW+ynfqBj7kHN4mbnwO74uB+lrRtLhp4Q==",
      "dev": true,
      "hasInstallScript": true,
      "license": "MIT",
      "dependencies": {
        "@webgpu/types": "^0.1.72",
        "debug": "^4.4.0"
      }
    }
  }
}

</file>

<file src="viewer/package.json">
{
  "name": "namma-space-viewer",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite --host 127.0.0.1",
    "build": "vite build",
    "test": "node --test"
  },
  "dependencies": {
    "@manycore/aholo-viewer": "file:vendor/manycore-aholo-viewer-1.10.0.tgz",
    "recast-navigation": "^0.43.1",
    "three": "^0.186.1"
  },
  "devDependencies": {
    "@playcanvas/splat-transform": "3.10.1",
    "vite": "^6.4.4"
  },
  "engines": {
    "node": ">=18"
  }
}

</file>

<file src="viewer/scripts/colmap-views.mjs">
import fs from 'node:fs';
import path from 'node:path';
import { Quaternion, Vector3 } from 'three';

// Undistorted COLMAP camera poses, in the same world coordinates Brush imports.
export function cameraView(qvec, tvec) {
  const inverse = new Quaternion(qvec[1], qvec[2], qvec[3], qvec[0]).normalize().conjugate();
  return {
    position: new Vector3(...tvec).negate().applyQuaternion(inverse).toArray(),
    forward: new Vector3(0,0,1).applyQuaternion(inverse).toArray(),
    up: new Vector3(0,-1,0).applyQuaternion(inverse).toArray(),
  };
}
export function readColmapViews(directory) {
  const cameras = fs.readFileSync(path.join(directory,'cameras.bin'));
  let offset = 8;
  const count = Number(cameras.readBigUInt64LE(0)), intrinsics = new Map();
  if(count>10000)throw new Error('Too many cameras.');
  for(let i=0;i<count;i++){
    const id=cameras.readUInt32LE(offset), model=cameras.readInt32LE(offset+4);
    const height=Number(cameras.readBigUInt64LE(offset+16));offset+=24;
    if(model!==0&&model!==1)throw new Error('Expected undistorted pinhole cameras.');
    const fy=cameras.readDoubleLE(offset+(model===1?8:0));
    offset+=(model===1?4:3)*8;
    intrinsics.set(id,2*Math.atan(height/(2*fy))*180/Math.PI);
  }
  const images=fs.readFileSync(path.join(directory,'images.bin')), views=[];
  const imageCount=Number(images.readBigUInt64LE(0));offset=8;
  if(imageCount>10000)throw new Error('Too many views.');
  for(let i=0;i<imageCount;i++){
    const values=Array.from({length:7},(_,k)=>images.readDoubleLE(offset+4+k*8));
    const cameraId=images.readUInt32LE(offset+60);offset+=64;
    const end=images.indexOf(0,offset);if(end<0)throw new Error('Truncated image name.');
    const name=images.toString('utf8',offset,end);offset=end+1;
    const points=Number(images.readBigUInt64LE(offset));offset+=8+points*24;
    if(!Number.isSafeInteger(offset)||offset>images.length)throw new Error('Truncated image observations.');
    views.push({name,fov:intrinsics.get(cameraId)||55,...cameraView(values.slice(0,4),values.slice(4))});
  }
  return views.sort((a,b)=>a.name.localeCompare(b.name));
}

</file>

<file src="viewer/scripts/namma-pipeline.py">
"""Desktop entry point: import a trained result, open the scene library, package a browser demo."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser

ROOT = Path(__file__).resolve().parents[2]


def open_viewer(scene_id=None, browser=True):
    def live():
        try:
            with urllib.request.urlopen("http://127.0.0.1:5174/__scenes", timeout=2) as response:
                return isinstance(json.load(response), list)
        except (OSError, ValueError):
            return False
    if not live():
        log = ROOT / "output/viewer-server.log"
        log.parent.mkdir(exist_ok=True)
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        with log.open("ab") as stream:
            process = subprocess.Popen(
                [shutil.which("node") or "node", str(ROOT / "viewer/node_modules/vite/bin/vite.js"),
                 "--host", "127.0.0.1", "--port", "5174", "--strictPort"],
                cwd=ROOT / "viewer", stdout=stream, stderr=subprocess.STDOUT,
                creationflags=flags)
        for _ in range(40):
            if live():
                break
            if process.poll() is not None:
                raise RuntimeError("Viewer could not start. See " + str(log))
            time.sleep(0.5)
        else:
            raise RuntimeError("Viewer did not become ready. See " + str(log))
    if scene_id and not all(c.isalnum() or c == "-" for c in scene_id):
        raise ValueError("Invalid scene id")
    url = "http://127.0.0.1:5174/aholo/" + ("?scene=" + scene_id if scene_id else "")
    if browser:
        webbrowser.open(url)
    return url


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--open", metavar="SCENE_ID")
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    if args.open:
        print(open_viewer(args.open, not args.no_browser))
        return
    import tkinter as tk
    from tkinter import filedialog, messagebox, simpledialog
    import threading
    window = tk.Tk()
    window.title("Namma Space pipeline")
    window.geometry("580x400")
    window.configure(padx=24, pady=20)
    tk.Label(window, text="Namma Space", font=("Segoe UI", 22, "bold")).pack(anchor="w")
    tk.Label(window, text="Import a trained result, inspect and walk, then package a browser demo.",
             wraplength=520, justify="left").pack(anchor="w", pady=10)
    status = tk.StringVar(value="Original files are preserved. No paid resources are provisioned.")
    buttons = []
    def run(action):
        for button in buttons:
            button.configure(state="disabled")
        status.set("Working… Progress is in the terminal and saved job logs.")
        def work():
            try:
                result = action()
                window.after(0, lambda value=result: status.set(value or "Finished."))
            except Exception as error:
                window.after(0, lambda text=str(error): messagebox.showerror("Stopped", text))
                window.after(0, lambda: status.set("Stopped. Original files and job logs are preserved."))
            finally:
                window.after(0, lambda: [b.configure(state="normal") for b in buttons])
        threading.Thread(target=work, daemon=False).start()
    def import_result():
        file = filedialog.askopenfilename(title="Select geometry/result ZIP or its parts.json",
                                         filetypes=[("Scene result", "*.zip *.json")])
        if not file:
            return
        title = simpledialog.askstring("Scene name", "Name this room:", initialvalue="My room")
        if not title:
            return
        def process():
            spec = importlib.util.spec_from_file_location("scene_pipeline", Path(__file__).with_name("scene-pipeline.py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            result = module.import_scene(file, None, None, title)
            open_viewer(result["id"])
            return "Imported and opened. Inspect the surfaces and set floor/scale before testing walking."
        run(process)
    def view():
        library = ROOT / "data/scene-library"
        choices = sorted(library.glob("*/scene.json")) if library.exists() else []
        if not choices:
            messagebox.showinfo("No imported scenes", "Import a trained result first.")
            return
        run(lambda: open_viewer(choices[-1].parent.name))
    def browser_demo():
        choices = []
        for manifest in sorted((ROOT / "data/scene-library").glob("*/scene.json")):
            try:
                choices.append((str(json.loads(manifest.read_text(encoding="utf-8"))["title"]), manifest))
            except (OSError, ValueError, KeyError):
                continue
        if not choices:
            messagebox.showinfo("No imported scenes", "Import a trained result first.")
            return
        selected = []
        picker = tk.Toplevel(window)
        picker.title("Choose your demo room")
        picker.geometry("460x310")
        tk.Label(picker, text="Choose the room you have tested walking in:").pack(pady=10)
        rooms = tk.Listbox(picker, exportselection=False)
        rooms.pack(fill="both", expand=True, padx=16)
        for title, _ in choices:
            rooms.insert("end", title)
        rooms.selection_set(len(choices) - 1)
        def choose():
            if rooms.curselection():
                selected.append(choices[rooms.curselection()[0]][1])
                picker.destroy()
        tk.Button(picker, text="Use this room", command=choose).pack(pady=12)
        picker.transient(window)
        picker.grab_set()
        window.wait_window(picker)
        if not selected:
            return
        scene = str(selected[0])
        setup = filedialog.askopenfilename(title="Choose namma-walking-setup.json downloaded from that room's Walking setup panel",
            filetypes=[("Walking setup", "*.json")])
        if not setup:
            return
        def package():
            stamp = time.strftime("%Y%m%d-%H%M%S") + "-" + str(time.time_ns())[-6:]
            output = ROOT / "output" / ("aholo-demo-" + stamp)
            log = ROOT / "output" / ("demo-build-" + stamp + ".log")
            log.parent.mkdir(exist_ok=True)
            node = shutil.which("node") or "node"
            with log.open("x", encoding="utf-8") as stream:
                built = subprocess.run([node, str(ROOT / "viewer/node_modules/vite/bin/vite.js"), "build"],
                    cwd=ROOT / "viewer", stdout=stream, stderr=subprocess.STDOUT, timeout=300)
            if built.returncode:
                raise RuntimeError("Viewer build stopped. See " + str(log))
            subprocess.run([node, str(ROOT / "viewer/scripts/package-aholo-scene.mjs"),
                "--scene", scene, "--setup", setup, "--output", str(output)], check=True, timeout=300)
            if sys.platform == "win32":
                os.startfile(output)
            return "Browser demo packaged in " + str(output) + ". Read README.md to preview. Nothing was published."
        run(package)
    for text, callback in [("1. Import a trained result", import_result), ("2. Open my scene library", view),
                           ("3. Package a browser demo", browser_demo)]:
        button = tk.Button(window, text=text, command=callback, anchor="w", padx=12, pady=8)
        button.pack(fill="x", pady=4)
        buttons.append(button)
    tk.Label(window, textvariable=status, wraplength=520, justify="left").pack(anchor="w", pady=14)
    window.mainloop()


if __name__ == "__main__":
    main()

</file>

<file src="viewer/scripts/package-aholo-scene.mjs">
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {validateViewerManifest, validateWalk} from '../aholo/saved-walk.js';
import {existingInside, newOutputInside, inventoryFiles, collectLicences} from './package-scene.mjs';

const workspace = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const readJSON = async file => JSON.parse(await fs.readFile(file, 'utf8'));
const digest = bytes => createHash('sha256').update(bytes).digest('hex');

// Packaging only. This never uploads a room or provisions a host.
export async function packageAholoScene({scenePath, setupPath, output, inspection=false, root=workspace}) {
  root = await fs.realpath(root);
  const library = await existingInside(root, path.join(root, 'data/scene-library'), 'Scene library');
  const input = await existingInside(library, path.resolve(scenePath), 'Imported scene');
  const m = validateViewerManifest(await readJSON(input));
  const scene = {splatHash:m.splat.sha256, collisionHash:m.collision.sha256};
  const setup = setupPath ? validateWalk(await readJSON(path.resolve(setupPath)), scene) : null;
  if (!inspection && !setup) throw Error('Download the walking setup from this room first, then select that JSON file.');
  output = path.resolve(output ?? path.join(root, 'output', 'aholo-demo-' + new Date().toISOString().replace(/[:.]/g, '-')));
  await newOutputInside(root, output);
  const prototype = await existingInside(root, path.join(root, 'viewer'), 'Application');
  const dist = await existingInside(prototype, path.join(prototype, 'dist'), 'Built application');
  const files = (await inventoryFiles(dist)).filter(f => f.relative === path.join('aholo','index.html') || f.relative.startsWith('assets' + path.sep));
  if (!files.some(f => f.relative === path.join('aholo','index.html'))) throw Error('Build the Aholo viewer before packaging.');
  const html = await fs.readFile(path.join(dist,'aholo/index.html'),'utf8');
  const scripts = [...html.matchAll(/src="([^"]+\.js)"/g)].map(m => m[1]);
  const code = (await Promise.all(scripts.map(s => fs.readFile(path.resolve(dist,'aholo',s),'utf8')))).join('\n');
  if (!code.includes('Room manifest must be hosted with this viewer.')) throw Error('The viewer build predates portable scenes. Build again.');
  const assets = {};
  for (const [kind, item] of [['splat',m.splat],['collision',m.collision]]) {
    const file = await existingInside(path.dirname(input), path.join(path.dirname(input), item.file), kind);
    const bytes = await fs.readFile(file);
    if (digest(bytes) !== item.sha256 || (kind === 'splat' && bytes.length !== m.splat.bytes)) throw Error('Changed or incomplete ' + kind + ' file; import the original result again.');
    assets[kind] = bytes;
  }
  const licences = await collectLicences(prototype, root);
  const credits = await fs.readFile(path.join(prototype,'THIRD_PARTY_NOTICES.md'),'utf8');
  // Deliberate whitelist: no source images, local paths, source reports or raw master PLY.
  const manifest = {version:1,type:'namma-viewer-scene',coordinateSpace:'raw-ply-v1',title:m.title,
    splat:{file:'preview.spz',sha256:m.splat.sha256,bytes:assets.splat.length},
    collision:{file:'collision.glb',sha256:m.collision.sha256,triangles:m.collision.triangles},
    ...(m.initialView ? {initialView:m.initialView} : {}), ...(setup ? {walkingSetup:setup} : {}),
    metricVerified:false, warning:'Experimental reconstruction. Walking uses the supplied measurement and reviewed surfaces; physical accuracy is not certified.'};
  await fs.mkdir(output, {recursive:true});
  for (const file of [...files,...licences.files]) {
    const target = path.join(output,file.relative);await fs.mkdir(path.dirname(target),{recursive:true});
    await fs.copyFile(file.source,target,fs.constants.COPYFILE_EXCL);
  }
  await fs.mkdir(path.join(output,'scene'));
  for (const [name, contents] of [
    ['index.html','<!doctype html><html lang="en"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=./aholo/?manifest=../scene/scene.json"><title>Namma Space · ruakpeedkahem (rpk)</title><a href="./aholo/?manifest=../scene/scene.json">Open the room walkthrough</a></html>'],
    ['scene/scene.json',JSON.stringify(manifest,null,2)],
    ['scene/preview.spz',assets.splat], ['scene/collision.glb',assets.collision],
    ['THIRD_PARTY_NOTICES.md',credits], ['license-inventory.json',JSON.stringify(licences.packages,null,2)],
    ['vercel.json',JSON.stringify({version:2,framework:null,buildCommand:null,outputDirectory:'.',headers:[{source:'/(.*)',headers:[{key:'X-Content-Type-Options',value:'nosniff'},{key:'Cache-Control',value:'no-cache'}]}]},null,2)],
    ['README.md',`# Portable Namma Space room\n\nBy team ruakpeedkahem (rpk): Akarsh Shrivastav, Mayan S Hiremath, NIT Goa · https://github.com/TheCodeNotTakenT-T/namma-space\n\nServe this folder over HTTP for local preview or HTTPS for visitors. Start at index.html. Opening a file:// URL will not work.\n\n${setup ? 'Open Walking setup and choose Enter saved walking setup. Floor, scale, height and entrance are included. Surfaces are rebuilt and the entrance checked before movement.' : 'Inspection package only. No saved walking entrance is included.'}\n\nThis package has NOT been published or certified as geometrically accurate. Test the complete walking route and performance on another device before submitting. It contains visible room details; review the scene before sharing. No source photos, master PLY, local paths or cloud logs are included. Keep licenses/ and THIRD_PARTY_NOTICES.md with redistribution.\n\nThis is a static walkthrough, not a hosted video-training service.\n`],
  ]) await fs.writeFile(path.join(output,name),contents,{flag:'wx'});
  return {output,walkingSetupIncluded:Boolean(setup),published:false,splatBytes:assets.splat.length,collisionBytes:assets.collision.length};
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args=process.argv.slice(2), options={};
  try {
    for(let i=0;i<args.length;i++){
      const arg=args[i];if(arg==='--inspection'){options.inspection=true;continue;}
      if(!['--scene','--setup','--output'].includes(arg)||!args[i+1]||args[i+1].startsWith('--'))throw Error('Use --scene PATH --setup PATH [--output PATH].');
      options[arg==='--scene'?'scenePath':arg==='--setup'?'setupPath':'output']=args[++i];
    }
    if(!options.scenePath)throw Error('Choose an imported scene.json.');
    console.log(JSON.stringify(await packageAholoScene(options),null,2));
  } catch(error) {console.error(error.message);process.exitCode=1;}
}

</file>

<file src="viewer/scripts/package-scene.mjs">
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {readColmapViews} from './colmap-views.mjs';
import {validateSetup, validateScenePackage} from '../src/scene-package.js';

const workspace = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const json = async file => JSON.parse(await fs.readFile(file, 'utf8'));
const within = (parent, child) => {
  const relative = path.relative(parent, child);
  return relative !== '' && relative !== '..' && !relative.startsWith('..' + path.sep) && !path.isAbsolute(relative);
};
function demand(condition, message) { if (!condition) throw new Error(message); }
export async function existingInside(parent, target, label) {
  const base = await fs.realpath(parent), resolved = await fs.realpath(target);
  demand(within(base, resolved), `${label} must stay inside ${parent}.`);
  return resolved;
}
export async function newOutputInside(root, target) {
  demand(within(root, target), 'Output must be a new directory inside the workspace.');
  try { await fs.lstat(target); throw new Error('Output already exists; choose a new directory.'); }
  catch (error) { if (error.code !== 'ENOENT') throw error; }
  // Resolve the nearest existing parent to reject junction/symlink escapes, even
  // when one or more output parent directories have not been created yet.
  let ancestor = path.dirname(target);
  while (true) {
    try {
      const real = await fs.realpath(ancestor);
      demand(real === root || within(root, real), 'Output parent resolves outside the workspace.');
      break;
    } catch (error) {
      if (error.code !== 'ENOENT') throw error;
      const next = path.dirname(ancestor);
      if (next === ancestor) throw error;
      ancestor = next;
    }
  }
}
export async function inventoryFiles(directory) {
  const result = [], visited = new Set();
  async function visit(current, relative = '') {
    const resolvedDirectory = await fs.realpath(current);
    demand(resolvedDirectory === directory || within(directory, resolvedDirectory), 'Build output resolves outside its directory.');
    demand(!visited.has(resolvedDirectory), 'Build output contains a directory cycle.');
    visited.add(resolvedDirectory);
    for (const entry of await fs.readdir(current, {withFileTypes:true})) {
      const file = path.join(current, entry.name), name = path.join(relative, entry.name);
      // OneDrive placeholders can be reported as reparse/symlink entries on
      // Windows. Resolve and bound them rather than rejecting normal files.
      const resolved = await fs.realpath(file), stat = await fs.stat(file);
      demand(within(directory, resolved), 'Build output resolves outside its directory.');
      if (stat.isDirectory()) await visit(file, name);
      else if (stat.isFile()) result.push({source:resolved, relative:name});
      else throw new Error('Unsupported build output entry: ' + name);
    }
  }
  await visit(directory);
  return result;
}
async function packageDirectory(name, from, boundary) {
  let cursor = from;
  while (true) {
    const candidate = path.join(cursor, 'node_modules', name);
    try { return await existingInside(boundary, candidate, 'Dependency'); }
    catch (error) { if (error.code !== 'ENOENT') throw error; }
    if (cursor === boundary) break;
    const parent = path.dirname(cursor);
    if (!within(boundary, parent) && parent !== boundary) break;
    cursor = parent;
  }
  throw new Error('Installed dependency not found: ' + name);
}
export async function collectLicences(prototype, root) {
  const visited = new Set(), packages = [], files = [];
  async function visit(name, from, optional = false) {
    let folder;
    try { folder = await packageDirectory(name, from, root); }
    catch (error) { if (optional && /not found/.test(error.message)) return; throw error; }
    if (visited.has(folder)) return;
    visited.add(folder);
    const info = await json(path.join(folder, 'package.json'));
    demand(typeof info.name === 'string' && /^(@[a-z0-9._-]+\/)?[a-z0-9._-]+$/i.test(info.name) && typeof info.version === 'string' && /^[a-z0-9.+_-]+$/i.test(info.version), 'Invalid dependency identity.');
    const notices = [];
    for (const entry of await fs.readdir(folder, {withFileTypes:true})) {
      if (/^(licen[sc]e|notice|copying)(?:[._-].*)?$/i.test(entry.name) && (await fs.stat(path.join(folder, entry.name))).isFile()) {
        const source = await existingInside(folder, path.join(folder, entry.name), 'Licence file');
        const relative = path.join('licenses', info.name.replaceAll('/', '__'), info.version, entry.name);
        files.push({source, relative});
        notices.push(relative.split(path.sep).join('/'));
      }
    }
    packages.push({name:info.name, version:info.version, license:info.license ?? 'See upstream package', notices});
    const dependencies = {...info.dependencies, ...info.optionalDependencies};
    for (const dependency of Object.keys(dependencies).sort()) {
      await visit(dependency, folder, Object.hasOwn(info.optionalDependencies ?? {}, dependency));
    }
  }
  const info = await json(path.join(prototype, 'package.json'));
  for (const name of Object.keys(info.dependencies ?? {}).sort()) await visit(name, prototype);
  return {packages:packages.sort((a,b) => a.name.localeCompare(b.name)), files};
}
function validateViews(views) {
  demand(Array.isArray(views) && views.length > 0, 'No captured viewpoints are available.');
  for (const view of views) {
    demand(typeof view.name === 'string' && view.name.length <= 500, 'Invalid viewpoint name.');
    for (const key of ['position', 'forward', 'up']) demand(Array.isArray(view[key]) && view[key].length === 3 && view[key].every(Number.isFinite), 'Invalid viewpoint vectors.');
    demand(Number.isFinite(view.fov) && view.fov > 0 && view.fov < 180, 'Invalid viewpoint field of view.');
  }
  return views.map(({name, position, forward, up, fov}) => ({name:name.replaceAll('\\', '/').split('/').at(-1), position, forward, up, fov}));
}

// The injectable root is solely for isolated automated fixtures. CLI callers
// always use the workspace containing this script.
export async function packageScene({job, cloudScene, setupPath, output, submission = false, execute = false, root = workspace}) {
  root = await fs.realpath(path.resolve(root));
  const prototype = await existingInside(root, path.join(root, 'viewer'), 'Application');
  demand(Boolean(job)!==Boolean(cloudScene), 'Choose exactly one --job PATH or --cloud-scene PATH.');
  output = path.resolve(output ?? path.join(root, 'output', 'web-demo-' + new Date().toISOString().replace(/[:.]/g, '-')));
  await newOutputInside(root, output);
  let splatBytes, sourceHash, collisionBytes, counts, views, diagnostic, title;
  if(cloudScene){
    const cloudRoot=await existingInside(root,path.join(root,'data','cloud-results'),'Cloud results');
    const manifestPath=await existingInside(cloudRoot,path.resolve(cloudScene),'Cloud scene');
    job=path.dirname(manifestPath);
    const imported=validateScenePackage(await json(manifestPath));
    demand(imported.assets.collision,'Cloud scene needs matching collision geometry.');
    const source=await existingInside(job,path.resolve(job,imported.assets.splat.url),'Cloud splat');
    const collider=await existingInside(job,path.resolve(job,imported.assets.collision.url),'Cloud collision');
    splatBytes=await fs.readFile(source);collisionBytes=await fs.readFile(collider);sourceHash=hash(splatBytes);
    demand(sourceHash===imported.sourceHash&&hash(collisionBytes)===imported.assets.collision.sha256,'Cloud asset hash changed; import the original matching result again.');
    counts={registeredImages:imported.capture?.registeredImages,inputImages:imported.capture?.inputImages,trainingSteps:imported.capture?.trainingSteps};
    views=validateViews(imported.views);diagnostic=imported.capture?.diagnostic!==false;title=imported.title;
  }else{
  const jobs = await existingInside(root, path.join(root, 'data', 'gaussian-jobs'), 'Jobs directory');
  job = await existingInside(jobs, path.resolve(job), 'Job');
  const state = await json(path.join(job, 'status.json'));
  demand(state.splat && Array.isArray(state.splat.files) && state.splat.files.length, 'Job has no completed splat export.');
  const latestFile = [...state.splat.files].sort((a,b) => a.localeCompare(b, undefined, {numeric:true})).at(-1);
  const source = await existingInside(job, path.resolve(state.splat.directory, latestFile), 'Splat');
  demand(path.extname(source).toLowerCase() === '.ply', 'Expected a PLY splat.');
  const pairing = await json(path.join(job, 'collision.json'));
  demand(pairing.coordinateSpace === 'raw-ply-v1', 'Regenerate collision geometry using raw-ply-v1 before packaging.');
  demand(pairing.exitCode === 0, 'Collision generation did not complete successfully.');
  const boundSource = await existingInside(job, path.resolve(pairing.source), 'Bound splat');
  demand(boundSource === source, 'Collision geometry belongs to a different splat.');
  splatBytes = await fs.readFile(source);sourceHash = hash(splatBytes);
  demand(sourceHash === pairing.sourceSha256, 'Splat hash changed; regenerate matching collision geometry.');
  const collision = await existingInside(job, path.resolve(pairing.path), 'Collision geometry');
  demand(path.extname(collision).toLowerCase() === '.glb', 'Expected GLB collision geometry.');
  collisionBytes = await fs.readFile(collision);
  const capture = await json(path.join(job, 'capture.json'));
  counts = {registeredImages:state.alignment?.best?.registeredImages, inputImages:capture.inputCount, trainingSteps:state.splat.trainingSteps};
  const sparse = await existingInside(job, path.join(job, 'dataset', 'sparse'), 'Camera data');
  for (const name of ['cameras.bin', 'images.bin']) await existingInside(job, path.join(sparse, name), 'Camera file');
  views = validateViews(readColmapViews(sparse));diagnostic=state.splat.diagnostic===true;title='Namma Space — '+path.basename(job);
  }
  for (const [key, value] of Object.entries(counts)) demand(Number.isSafeInteger(value) && value > 0, 'Invalid capture metadata: ' + key);
  demand(counts.registeredImages <= counts.inputImages, 'Registered image count exceeds input count.');
  demand(splatBytes.length<=150*1024**2&&collisionBytes.length<=150*1024**2,'A browser asset exceeds 150 MiB. Preserve the master and prepare a smaller web derivative before packaging.');
  let setup = null;
  if (setupPath) {
    const checked = validateSetup(await json(path.resolve(setupPath)), 'paired:' + sourceHash);
    const cleanPoint = p => p === null ? null : ({x:p.x, y:p.y, z:p.z});
    setup = {version:checked.version, sourceKey:checked.sourceKey, collisionHash:checked.collisionHash, transform:{position:checked.transform.position, quaternion:checked.transform.quaternion, scale:checked.transform.scale}, floor:checked.floor === null ? null : {origin:checked.floor.origin, quaternion:checked.floor.quaternion}, confirmed:true, pois:checked.pois.map(p => ({id:p.id, name:p.name, position:cleanPoint(p.position)})), start:cleanPoint(checked.start), checks:checked.checks.map(c => ({label:c.label, realMetres:c.realMetres, modelMetres:c.modelMetres, errorPercent:c.errorPercent}))};
    if(checked.rotationDegrees!==undefined)setup.rotationDegrees=checked.rotationDegrees;
  }
  if(submission){
    demand(setup?.start,'Submission packaging needs a saved floor/scale setup and entrance.');
    demand(setup.checks.length>=2&&setup.checks.every(check=>check.errorPercent<=5),'Submission packaging needs two independent distance checks, each within the project\'s 5% tolerance.');
    demand(counts.registeredImages/counts.inputImages>=0.9,'Submission packaging requires at least 90% registered views under the project quality gate.');
  }
  const dist = await existingInside(prototype, path.join(prototype, 'dist'), 'Built viewer');
  const buildFiles = await inventoryFiles(dist);
  demand(buildFiles.some(file => file.relative === 'index.html'), 'Build the viewer first: npm run build.');
  const reserved = new Set(['scene.json', 'README.md', 'THIRD_PARTY_NOTICES.md', 'package-evidence.json', 'license-inventory.json', 'vercel.json']);
  demand(!buildFiles.some(file => reserved.has(file.relative) || ['scene', 'licenses'].includes(file.relative.split(path.sep)[0])), 'Build contains reserved package paths. Use a clean viewer build.');
  const licences = await collectLicences(prototype, root);
  const credits = await fs.readFile(path.join(prototype, 'THIRD_PARTY_NOTICES.md'), 'utf8');
  const manifest = {
    version:1, title, sourceHash,
    capture:{id:path.basename(job), ...counts, diagnostic},
    assets:{splat:{url:'scene/room.ply', sha256:sourceHash}, collision:{url:'scene/room.collision.glb', sha256:hash(collisionBytes), coordinateSpace:'raw-ply-v1'}},
    views, setup,
    warning:setup ? 'Operator-confirmed setup. Measurements and collision coverage require independent validation; packaging is not accuracy certification.' : 'Inspection only: no confirmed metric scale, floor alignment or walkable setup. This capture may contain gaps.'
  };
  validateScenePackage(manifest);
  const totalAssetBytes=splatBytes.length+collisionBytes.length;
  const summary = {output, capture:manifest.capture, sourceHash, mode:setup ? 'operator-configured' : 'inspection-only', submissionChecksPassed:submission, viewpoints:views.length, includedLicencePackages:licences.packages.length,totalAssetBytes,hostingNote:totalAssetBytes>=95_000_000?'Scene assets approach or exceed the Vercel Hobby CLI source-upload allowance; check the complete deployment size.':'Check the complete deployment size and bandwidth against the selected hosting plan.'};
  if (!execute) return {...summary, created:false, message:'Preview only; add --execute to create a new local folder. Nothing is published.'};
  // Capture data is read into memory before creating output, so a concurrent
  // reconstruction cannot change an asset between its hash and its copy.
  await fs.mkdir(path.dirname(output), {recursive:true});
  await newOutputInside(root, output);
  await fs.mkdir(output, {recursive:false});
  for (const file of [...buildFiles, ...licences.files]) {
    const target = path.join(output, file.relative);
    await fs.mkdir(path.dirname(target), {recursive:true});
    await fs.copyFile(file.source, target, fs.constants.COPYFILE_EXCL);
  }
  await fs.mkdir(path.join(output, 'scene'));
  await fs.writeFile(path.join(output, 'scene', 'room.ply'), splatBytes, {flag:'wx'});
  await fs.writeFile(path.join(output, 'scene', 'room.collision.glb'), collisionBytes, {flag:'wx'});
  await fs.writeFile(path.join(output, 'scene.json'), JSON.stringify(manifest, null, 2), {flag:'wx'});
  await fs.writeFile(path.join(output,'vercel.json'),JSON.stringify({version:2,framework:null,buildCommand:null,outputDirectory:'.',headers:[{source:'/scene.json',headers:[{key:'Cache-Control',value:'no-cache'}]},{source:'/(.*)',headers:[{key:'X-Content-Type-Options',value:'nosniff'}]}]},null,2),{flag:'wx'});
  await fs.writeFile(path.join(output, 'THIRD_PARTY_NOTICES.md'), credits, {flag:'wx'});
  await fs.writeFile(path.join(output, 'license-inventory.json'), JSON.stringify(licences.packages, null, 2), {flag:'wx'});
  await fs.writeFile(path.join(output, 'package-evidence.json'), JSON.stringify({...summary, output:undefined, createdAt:new Date().toISOString(), assetsHashed:true, metricAccuracyCertified:false, navigationValidated:false, sourcePhotosIncluded:false, reconstructionBinariesIncluded:false, published:false}, null, 2), {flag:'wx'});
  await fs.writeFile(path.join(output, 'README.md'), `# Namma Space portable viewer\n\n${manifest.warning}\n\nCapture: ${manifest.capture.id}. ${counts.registeredImages}/${counts.inputImages} registered images; ${counts.trainingSteps} training steps. Diagnostic: ${manifest.capture.diagnostic}.\n\n## Preview locally\n\nServe this directory over HTTP; opening index.html as a file does not work. From this directory, use an installed Python 3 runtime:\n\n\`\`\`powershell\npython -m http.server 4173 --bind 127.0.0.1\n\`\`\`\n\nOpen http://127.0.0.1:4173/ . The packaged scene loads automatically. No COLMAP, Brush, GPU reconstruction server or source photos are needed to view it. Browser WebGL2 and enough GPU memory are required.\n\n## Host when ready\n\nUpload the contents of this folder to a static HTTPS host, keeping scene.json, scene/, assets/, licenses/ and notices together. Review the visible room and any personal information before sharing. This command did not publish anything. Test the public URL in a clean browser before submitting. Hosting from a subfolder requires a viewer build with relative base URLs.\n\n## What this proves\n\nThe hashes in scene.json bind the packaged assets. Collision geometry is a reconstructed approximation, not surveyed ground truth. A saved setup records the operator's calibration; it cannot prove physical accuracy. ${setup ? 'The supplied setup is included; inspect paths and obstruction handling in this package before submission.' : 'Walking is disabled until a genuine measured setup is supplied and its navigation surfaces can be generated. This package is a reconstruction inspection artifact, not the completed submission.'}\n\nOriginal camera photos, databases, machine paths, tool binaries and processing logs are excluded. Camera pose names remain in the viewer. Keep THIRD_PARTY_NOTICES.md, license-inventory.json and licenses/ with redistribution.\n`, {flag:'wx'});
  return {...summary, created:true};
}

async function main() {
  const flags = process.argv.slice(2), options = {};
  for (let i=0; i<flags.length; i++) {
    const flag = flags[i];
    if (flag === '--execute') { options.execute = true; continue; }
    if (flag === '--submission') { options.submission = true; continue; }
    demand(['--job', '--cloud-scene', '--setup', '--output'].includes(flag), 'Unknown argument: ' + flag);
    const value = flags[++i];
    demand(value && !value.startsWith('--'), 'Missing value for ' + flag);
    options[flag === '--setup' ? 'setupPath' : flag === '--cloud-scene' ? 'cloudScene' : flag.slice(2)] = value;
  }
  console.log(JSON.stringify(await packageScene(options), null, 2));
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch(error => { console.error(error.message); process.exitCode = 1; });
}

</file>

<file src="viewer/scripts/scene-assets.mjs">
// Convert an already trained model and its paired mesh; never generate geometry.
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {PLYLoader} from 'three/addons/loaders/PLYLoader.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
const [model, mesh, destination] = process.argv.slice(2);
if (!model || !mesh || !destination) throw Error('Expected model, mesh and output directory.');
const out=path.resolve(destination);
fs.mkdirSync(out,{recursive:true});
const bytes=fs.readFileSync(mesh);
let triangleCount=0, bounds;
if (mesh.toLowerCase().endsWith('.glb')) {
  const {scene}=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
  scene.traverse(o=>{if(o.isMesh)triangleCount+=(o.geometry.index?.count??o.geometry.attributes.position.count)/3;});
  if(!triangleCount || triangleCount>250000)throw Error('Collision mesh must contain 1–250,000 triangles.');
  fs.copyFileSync(mesh,path.join(out,'collision.glb'));
} else {
  const geometry=new PLYLoader().parse(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength));
  const pos=geometry.attributes.position;
  if(!geometry.index)throw Error('Expected a triangle PLY with faces, not a point cloud.');
  const indices=new Uint32Array(geometry.index.array);
  const positions=new Float32Array(pos.array);
  triangleCount=indices.length/3;
  if(!triangleCount || triangleCount>250000 || indices.length%3)throw Error('Mesh exceeds the navigation triangle budget or has no triangles.');
  if(!positions.every(Number.isFinite)||!indices.every(i=>i<pos.count))throw Error('Invalid mesh coordinates or indices.');
  geometry.computeBoundingBox();
  const min=geometry.boundingBox.min.toArray(),max=geometry.boundingBox.max.toArray();bounds={min,max};
  // Raw positions, identity node transform. No renderer-specific axis conversion.
  const binary=Buffer.concat([Buffer.from(positions.buffer),Buffer.from(indices.buffer)]);
  const gltf={asset:{version:'2.0',generator:'Namma scene importer'},scene:0,scenes:[{nodes:[0]}],
    nodes:[{mesh:0}],meshes:[{primitives:[{attributes:{POSITION:0},indices:1,mode:4}]}],
    buffers:[{byteLength:binary.length}],
    bufferViews:[{buffer:0,byteOffset:0,byteLength:positions.byteLength,target:34962},
      {buffer:0,byteOffset:positions.byteLength,byteLength:indices.byteLength,target:34963}],
    accessors:[{bufferView:0,componentType:5126,count:pos.count,type:'VEC3',min,max},
      {bufferView:1,componentType:5125,count:indices.length,type:'SCALAR'}]};
  let json=Buffer.from(JSON.stringify(gltf));json=Buffer.concat([json,Buffer.alloc((4-json.length%4)%4,32)]);
  const header=Buffer.alloc(12);header.writeUInt32LE(0x46546c67);header.writeUInt32LE(2,4);header.writeUInt32LE(28+json.length+binary.length,8);
  const jh=Buffer.alloc(8);jh.writeUInt32LE(json.length);jh.writeUInt32LE(0x4e4f534a,4);
  const bh=Buffer.alloc(8);bh.writeUInt32LE(binary.length);bh.writeUInt32LE(0x004e4942,4);
  const glb=Buffer.concat([header,jh,json,bh,binary]);
  const parsed=await new GLTFLoader().parseAsync(glb.buffer.slice(glb.byteOffset,glb.byteOffset+glb.byteLength),'');
  let actual=0;parsed.scene.traverse(o=>{if(o.isMesh)actual+=o.geometry.index.count/3;});
  if(actual!==triangleCount)throw Error('GLB roundtrip changed triangle count.');
  fs.writeFileSync(path.join(out,'collision.glb'),glb);
}
const cli=fileURLToPath(new URL('../node_modules/@playcanvas/splat-transform/bin/cli.mjs',import.meta.url));
const result=spawnSync(process.execPath,[cli,path.resolve(model),path.join(out,'preview.spz')],{
  stdio:'inherit',windowsHide:true,timeout:600000});
if(result.error)throw result.error;
if(result.status!==0)throw Error('SPZ conversion failed; the original model is preserved.');
fs.writeFileSync(path.join(out,'asset-report.json'),JSON.stringify({
  triangleCount,bounds,coordinateSpace:'raw-ply-v1',meshTransform:'identity',
  preview:'SPZ quantized derivative; source PLY preserved',walkingValidated:false},null,2));

</file>

<file src="viewer/scripts/scene-pipeline.py">
"""Reusable local result import, backup verification and scene-library registration."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import uuid
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024**2), b""):
            h.update(block)
    return h.hexdigest()


def scene_up(cameras):
    """The room's up direction: the mean of every training camera's up (-Y of its camera-to-world rotation).
    One camera's up is tilted wherever that frame was; the mean over a walkthrough is level."""
    total = [0.0, 0.0, 0.0]
    for camera in cameras:
        rotation = camera.get("rotation")
        if not (isinstance(rotation, list) and len(rotation) == 3 and all(isinstance(r, list) and len(r) == 3 for r in rotation)):
            continue
        for i in range(3):
            total[i] -= float(rotation[i][1])
    length = sum(v * v for v in total) ** 0.5
    return [v / length for v in total] if length > 1e-9 else None


def safe_name(name):
    if not isinstance(name, str) or not name or "\\" in name or ":" in name:
        raise ValueError("Invalid archive filename")
    parts = name.split("/")
    if name.startswith("/") or any(p in ("", ".", "..") or p.endswith((".", " ")) for p in parts):
        raise ValueError("Unsafe archive filename: " + name)
    if any(re.match(r"^(con|prn|aux|nul|com[0-9]|lpt[0-9])(?:\.|$)", p, re.I) for p in parts):
        raise ValueError("Reserved filename")
    return name


def join_parts(manifest, output):
    manifest = Path(manifest)
    record = json.loads(manifest.read_text(encoding="utf-8"))
    name = safe_name(record["archive"])
    if "/" in name:
        raise ValueError("Archive must use a plain filename")
    parts = record["parts"]
    if not isinstance(parts, list) or not 1 <= len(parts) <= 500:
        raise ValueError("Invalid part count")
    seen = set()
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    target = output / name
    with target.open("xb") as destination:
        for part in parts:
            part_name = safe_name(part["name"])
            if "/" in part_name or part_name in seen:
                raise ValueError("Invalid or duplicate part name")
            seen.add(part_name)
            source = manifest.parent / part_name
            if not source.exists() and (manifest.parent / (part_name + ".zip")).exists():
                source = manifest.parent / (part_name + ".zip")  # Google Drive folder downloads rename ZIP-looking parts
            if source.stat().st_size != part["bytes"] or sha(source) != part["sha256"]:
                raise ValueError("Missing, truncated or changed part: " + part_name)
            with source.open("rb") as stream:
                shutil.copyfileobj(stream, destination, 8 * 1024**2)
            print("Verified", part_name, flush=True)
    if sha(target) != record["sha256"]:
        raise ValueError("Joined archive checksum mismatch")
    shutil.copy2(manifest, output / manifest.name)
    return target


def extract_archive(source, target):
    target = Path(target)
    with zipfile.ZipFile(source) as z:
        entries = z.infolist()
        if len(entries) > 10000 or sum(i.file_size for i in entries) > 16 * 1024**3:
            raise ValueError("Archive exceeds import limits")
        seen = set()
        for entry in entries:
            name = safe_name(entry.filename.rstrip("/"))
            key = name.casefold()
            if key in seen:
                raise ValueError("Duplicate archive filename")
            seen.add(key)
            if (entry.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("Archive links are not allowed")
        if z.testzip() is not None:
            raise ValueError("Damaged archive")
        z.extractall(target)


def import_scene(geometry, model=None, backup=None, title="Imported room"):
    identity = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8]
    job = ROOT / "data/scene-imports" / identity
    scene = ROOT / "data/scene-library" / identity
    job.mkdir(parents=True)
    state = {"status": "verifying", "title": title, "id": identity}
    def save():
        (job / "status.json").write_text(json.dumps(state, indent=2), encoding="utf-8")
    save()
    try:
        geometry = Path(geometry).resolve(strict=True)
        if geometry.name.endswith(".parts.json"):
            archive = join_parts(geometry, job / "downloads")
        else:
            archive = job / "geometry-source.zip"
            shutil.copy2(geometry, archive)
        extracted = job / "source"
        extract_archive(archive, extracted)
        standard = extracted / "namma-result.json"
        if standard.is_file():
            report = json.loads(standard.read_text())
            def artifact(kind):
                item = report["artifacts"][kind]
                p = extracted / safe_name(item["path"])
                if sha(p) != item["sha256"]:
                    raise ValueError("Changed " + kind + " artifact")
                return p
            model = artifact("splat")
            mesh = artifact("mesh")
            if report["artifacts"]["mesh"].get("coordinateSpace") != "raw-ply-v1":
                raise ValueError("Unsupported mesh coordinate convention")
            source_hash = sha(model)
        else:
            report = json.loads((extracted / "recovery-report.json").read_text())
            if model is None:
                raise ValueError("Select the matching trained Gaussian PLY for this recovery archive.")
            model = Path(model).resolve(strict=True)
            source_hash = sha(model)
            if source_hash != report["sourceModelSha256"]:
                raise ValueError("This geometry belongs to a different trained PLY. Nothing was registered.")
            candidates = list(extracted.glob("*-collision-candidate.ply"))
            if len(candidates) != 1:
                raise ValueError("Expected one collision candidate in recovery ZIP")
            mesh = candidates[0]
        if backup:
            joined = join_parts(backup, job / "depth-backup")
            with zipfile.ZipFile(joined) as z:
                if z.testzip() is not None:
                    raise ValueError("Depth backup ZIP is damaged")
                metadata = json.loads(z.read("recovery-report.json"))
                if metadata["sourceModelSha256"] != source_hash:
                    raise ValueError("Depth backup belongs to another model")
            state["depthBackup"] = str(joined)
        saved_model = job / "trained-model.ply"
        shutil.copy2(model, saved_model)
        if sha(saved_model) != source_hash:
            raise ValueError("Model copy checksum mismatch")
        state["status"] = "converting"
        save()
        scene.mkdir(parents=True)
        command = [shutil.which("node") or "node", str(ROOT / "viewer/scripts/scene-assets.mjs"),
                   str(saved_model), str(mesh), str(scene)]
        with (job / "conversion.log").open("w", encoding="utf-8") as log:
            subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT, timeout=900)
        assets = json.loads((scene / "asset-report.json").read_text())
        record = {
            "version": 1, "type": "namma-viewer-scene", "id": identity, "title": title,
            "sourceModelSha256": source_hash, "coordinateSpace": "raw-ply-v1",
            "splat": {"file": "preview.spz", "sha256": sha(scene / "preview.spz"),
                      "bytes": (scene / "preview.spz").stat().st_size},
            "collision": {"file": "collision.glb", "sha256": sha(scene / "collision.glb"),
                          "triangles": assets["triangleCount"], "kind": "reconstructed-surface"},
            "scaleCalibrated": False, "walkingValidated": False,
            "provenance": {"sourceArchiveSha256": sha(archive), "report": report},
        }
        cameras_file = extracted / "cameras.json"
        if cameras_file.is_file():
            cameras = json.loads(cameras_file.read_text())
            if cameras:
                # Saved PlanarGS camera-to-world pose, used only for framing.
                camera = cameras[0]
                record["initialView"] = {key: camera[key] for key in
                                         ("position", "rotation", "height", "fy")}
                up = scene_up(cameras)
                if up:
                    record["initialView"]["up"] = up
        # Written last: unfinished conversions never appear in the scene library.
        (scene / "scene.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
        state.update(status="ready", scene=str(scene),
                     url="http://127.0.0.1:5174/aholo/?scene=" + identity)
        save()
        print("READY:", state["url"], "\nPreserved inputs and backup:", job, flush=True)
        return state
    except Exception as error:
        state.update(status="failed", error=str(error))
        save()
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--geometry", type=Path, required=True)
    parser.add_argument("--model", type=Path)
    parser.add_argument("--backup", type=Path)
    parser.add_argument("--title", default="Imported room")
    args = parser.parse_args()
    import_scene(args.geometry, args.model, args.backup, args.title)


if __name__ == "__main__":
    main()

</file>

<file src="viewer/server/scene-library.mjs">
import fs from 'node:fs';
import path from 'node:path';
export function sceneLibrary(root) {
  const base=path.resolve(root,'data/scene-library');
  const inside=p=>{const rel=path.relative(base,fs.realpathSync(p));return rel&&!rel.startsWith('..')&&!path.isAbsolute(rel);};
  function read(id) {
    if(!/^[a-zA-Z0-9-]{1,100}$/.test(id))throw Error('Invalid scene id');
    const file=path.join(base,id,'scene.json');
    if(!inside(file))throw Error('Scene path escaped library');
    const m=JSON.parse(fs.readFileSync(file,'utf8'));
    if(m.type!=='namma-viewer-scene'||m.id!==id||m.coordinateSpace!=='raw-ply-v1'||
       m.splat.file!=='preview.spz'||m.collision.file!=='collision.glb')throw Error('Invalid scene manifest');
    return m;
  }
  return (req,res,next)=>{
    const pathname=new URL(req.url,'http://localhost').pathname;
    if(!pathname.startsWith('/__scenes'))return next();
    if(req.method!=='GET'){res.statusCode=405;return res.end();}
    res.setHeader('Cache-Control','no-store');
    try{
      if(pathname==='/__scenes'){
        const scenes=[];
        if(fs.existsSync(base))for(const id of fs.readdirSync(base)){
          try{const m=read(id);scenes.push({id,title:m.title});}catch{/* Incomplete jobs are hidden. */}
        }
        res.setHeader('Content-Type','application/json');return res.end(JSON.stringify(scenes));
      }
      const match=pathname.match(/^\/__scenes\/([a-zA-Z0-9-]{1,100})\/(scene\.json|preview\.spz|collision\.glb)$/);
      if(!match){res.statusCode=404;return res.end('Unknown scene asset');}
      const [,id,name]=match;const m=read(id);
      if(name==='scene.json'){res.setHeader('Content-Type','application/json');return res.end(JSON.stringify(m));}
      const target=path.join(base,id,name);if(!inside(target))throw Error('Asset path escaped library');
      res.setHeader('Content-Type',name.endsWith('.glb')?'model/gltf-binary':'application/octet-stream');
      res.setHeader('Content-Length',fs.statSync(target).size);
      const stream=fs.createReadStream(target);stream.on('error',()=>res.destroy());stream.pipe(res);
    }catch{res.statusCode=404;res.end('Scene unavailable or incomplete');}
  };
}

</file>

<file src="viewer/src/demo.js">
import * as THREE from 'three';
export function makeDemo() {
  const group = new THREE.Group();
  const box = (name, size, position, color) => {
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(...size), new THREE.MeshStandardMaterial({ color, roughness: 0.85 }));
    mesh.name = name; mesh.position.set(...position); group.add(mesh); return mesh;
  };
  box('Floor', [10, 0.2, 8], [0, -0.1, 0], '#cfc9ba');
  box('Back wall', [10, 2.8, 0.15], [0, 1.4, -4], '#e8e4d9');
  box('Left wall', [0.15, 2.8, 8], [-5, 1.4, 0], '#c4d4cd');
  box('Right wall', [0.15, 2.8, 8], [5, 1.4, 0], '#e8e4d9');
  box('Desk', [2.4, 0.9, 1.5], [0, 0.45, 0], '#997a57');
  box('Storage', [1.6, 1.7, 0.65], [-3, 0.85, -3.2], '#60766a');
  box('Seat', [1.8, 0.6, 0.8], [3, 0.3, -2.5], '#bd795f');
  return group;
}

</file>

<file src="viewer/src/navigation.js">
import { init, NavMeshQuery } from 'recast-navigation';
import { generateSoloNavMesh } from 'recast-navigation/generators';
import { Vector3 } from 'three';

export async function buildNavigation(root, {fillHoles = true} = {}) {
  await init();
  root.updateMatrixWorld(true);
  const positions = [], indices = [];
  const p = new Vector3();
  root.traverse(mesh => {
    if (!mesh.isMesh) return;
    const attr = mesh.geometry.attributes.position;
    const offset = positions.length / 3;
    for (let i = 0; i < attr.count; i++) {
      p.fromBufferAttribute(attr, i).applyMatrix4(mesh.matrixWorld);
      positions.push(p.x, p.y, p.z);
    }
    const index = mesh.geometry.index;
    for (let i = 0; i < (index?.count ?? attr.count); i++) indices.push(offset + (index ? index.getX(i) : i));
  });
  if (indices.length / 3 > 250000) throw new Error('Simplify the walking mesh to 250,000 triangles or fewer before importing.');
  if (fillHoles) fillFloor(positions, indices);
  // Forgiving walker for reconstructed rooms, whose noise (small floating blobs, floor bumps) is not furniture:
  // 1.2 m clearance ignores blobs above chest height, a 30 cm step crosses low bumps but not bench seats
  // (~45 cm) or desks, and a 15 cm radius fits between benches. Recast height, climb and radius are in voxels.
  const result = generateSoloNavMesh(positions, indices, {
    cs: 0.05, ch: 0.04, walkableSlopeAngle: 45,
    walkableHeight: Math.ceil(1.2 / 0.04), walkableClimb: Math.floor(0.3 / 0.04),
    walkableRadius: Math.ceil(0.15 / 0.05), minRegionArea: 8, mergeRegionArea: 20,
  });
  if (!result.success) throw new Error('Could not build walking surfaces. Check scale, orientation and floor coverage.');
  return new Navigation(result.navMesh);
}

// Reconstructions leave holes in the floor where it was poorly filmed, and a hole stops the walker. Lay a flat
// floor (two triangles) at the observed floor height under the area the observed floor spans; walls and
// furniture still block because they stand on top of it. Positions are metres with the picked floor at y = 0.
export function fillFloor(positions, indices) {
  const xs = [], zs = [], ys = [];
  let area = 0;
  for (let t = 0; t < indices.length; t += 3) {
    const [a, b, c] = [indices[t], indices[t + 1], indices[t + 2]].map(i => i * 3);
    const ux = positions[b] - positions[a], uy = positions[b + 1] - positions[a + 1], uz = positions[b + 2] - positions[a + 2];
    const vx = positions[c] - positions[a], vy = positions[c + 1] - positions[a + 1], vz = positions[c + 2] - positions[a + 2];
    const nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx;
    const y = (positions[a + 1] + positions[b + 1] + positions[c + 1]) / 3;
    if (Math.abs(ny) > 0.9 * Math.hypot(nx, ny, nz) && Math.abs(y) < 0.25) {
      for (const i of [a, b, c]) { xs.push(positions[i]); zs.push(positions[i + 2]); }
      ys.push(y);
      area += Math.hypot(nx, ny, nz) / 2;
    }
  }
  if (area < 1) return false;  // under 1 m² of observed floor: too little to trust its extent
  const pick = (values, q) => values.slice().sort((u, v) => u - v)[Math.min(values.length - 1, Math.floor(q * values.length))];
  const [x0, x1, z0, z1, y] = [pick(xs, 0.01), pick(xs, 0.99), pick(zs, 0.01), pick(zs, 0.99), pick(ys, 0.5)];
  const base = positions.length / 3;
  positions.push(x0, y, z0, x1, y, z0, x1, y, z1, x0, y, z1);
  indices.push(base, base + 2, base + 1, base, base + 3, base + 2);  // counter-clockwise seen from above (+y)
  return true;
}

export class Navigation {
  constructor(mesh) { this.mesh = mesh; this.query = new NavMeshQuery(mesh); }
  nearest(point) {
    const r = this.query.findClosestPoint(point, { halfExtents: { x: 0.4, y: 0.35, z: 0.4 } });
    return r.success && r.polyRef && new Vector3().copy(r.point).distanceTo(point) < 0.45 ? r : null;
  }
  route(start, end) {
    const target = this.nearest(end);
    if (!target) return null;
    const r = this.query.computePath(start, target.point, { halfExtents: { x: 0.4, y: 0.35, z: 0.4 }, maxPathPolys: 2048 });
    // Detour may return a partial path to an unreachable island. Never present that as success.
    if (!r.success || !r.path.length || new Vector3().copy(r.path.at(-1)).distanceTo(target.point) > 0.12) return null;
    return r.path.map(p => new Vector3().copy(p));
  }
  move(state, delta) {
    // Small local steps keep moveAlongSurface from bridging disconnected surfaces.
    const steps = Math.max(1, Math.ceil(delta.length() / 0.08));
    const step = delta.clone().divideScalar(steps);
    for (let i = 0; i < steps; i++) {
      const r = this.query.moveAlongSurface(state.polyRef, state.point, new Vector3().copy(state.point).add(step));
      if (!r.success || !r.visited.length) break;
      state.polyRef = r.visited.at(-1);
      state.point = r.resultPosition;
      const h = this.query.getPolyHeight(state.polyRef, state.point);
      if (h.success) state.point.y = h.height;
    }
    return state;
  }
  dispose() { this.query.destroy(); this.mesh.destroy(); }
}

</file>

<file src="viewer/src/scene-alignment.js">
import {Quaternion, Vector3} from 'three';

// Three clicks on a bumpy reconstructed floor can tilt the plane by a few degrees, which shows as a swinging
// horizon while turning. When the room's up (from all training cameras) agrees within 15 degrees, use it.
const ROOM_UP_TOLERANCE=Math.cos(15*Math.PI/180);

export function floorAlignment(points, approximateUp=new Vector3(0,1,0), roomUp=null) {
  if(points.length!==3)throw new Error('Select three floor points.');
  const normal=new Vector3().subVectors(points[1],points[0]).cross(new Vector3().subVectors(points[2],points[0]));
  if(normal.length()<0.0001)throw new Error('Choose three floor points spread across an area, not on a straight line.');
  normal.normalize();if(normal.dot(approximateUp)<0)normal.negate();
  if(roomUp){const up=roomUp.clone().normalize();if(normal.dot(up)>ROOM_UP_TOLERANCE)normal.copy(up);}
  return {quaternion:new Quaternion().setFromUnitVectors(normal,new Vector3(0,1,0)),origin:points[0].clone()};
}

export function copySceneTransform(source,target){
  target.position.copy(source.position);target.quaternion.copy(source.quaternion);target.scale.copy(source.scale);target.updateMatrixWorld(true);
}

// Locations are meaningful only for the exact asset and its applied transform.
export function calibratedSceneKey(sourceKey, object) {
  object.updateMatrix();
  return sourceKey + ':' + JSON.stringify(object.matrix.elements.map(value=>Number(value.toFixed(8))));
}

</file>

<file src="viewer/src/scene-package.js">
const hashPattern=/^[a-f0-9]{64}$/;
const finite=(value,limit=1e5)=>typeof value==='number'&&Number.isFinite(value)&&Math.abs(value)<=limit;
const vector=(value,n)=>Array.isArray(value)&&value.length===n&&value.every(x=>finite(x));
const point=value=>value&&['x','y','z'].every(k=>finite(value[k]));
const quaternion=value=>vector(value,4)&&Math.abs(Math.hypot(...value)-1)<0.001;
const requireValue=(condition,message)=>{if(!condition)throw new Error(message);};

export function validatePois(pois) {
  requireValue(Array.isArray(pois)&&pois.length<=1000,'Invalid location list.');
  const ids=new Set();
  for(const p of pois){
    requireValue(p&&typeof p.id==='string'&&p.id.length>0&&p.id.length<=100&&!ids.has(p.id)&&typeof p.name==='string'&&p.name.trim().length>0&&p.name.length<=60&&point(p.position),'Invalid location.');
    ids.add(p.id);
  }
  return pois;
}

export function validateSetup(data,expectedKey) {
  requireValue(data?.version===1&&data.sourceKey===expectedKey&&typeof expectedKey==='string'&&expectedKey.length<=150,'This setup belongs to a different model.');
  const t=data.transform;
  requireValue(t&&vector(t.position,3)&&quaternion(t.quaternion)&&finite(t.scale,1000)&&t.scale>0,'Invalid scene transform.');
  requireValue(data.confirmed===true,'Confirm floor and scale before saving a walking setup.');
  if(data.floor!==null)requireValue(data.floor&&vector(data.floor.origin,3)&&quaternion(data.floor.quaternion),'Invalid floor setup.');
  if(expectedKey.startsWith('paired:')){requireValue(data.floor!==null,'A Gaussian walking setup needs a selected floor.');requireValue(hashPattern.test(data.collisionHash),'A Gaussian setup needs its collision hash.');}
  if(data.rotationDegrees!==undefined)requireValue([0,-90,90,180].includes(data.rotationDegrees),'Invalid orientation preset.');
  validatePois(data.pois);
  requireValue(data.start===null||point(data.start),'Invalid starting point.');
  requireValue(Array.isArray(data.checks)&&data.checks.length<=20,'Invalid measurement checks.');
  for(const c of data.checks){
    requireValue(c&&typeof c.label==='string'&&c.label.length<=100&&finite(c.realMetres,40)&&c.realMetres>0&&finite(c.modelMetres,100)&&c.modelMetres>0&&finite(c.errorPercent),'Invalid measurement check.');
    requireValue(Math.abs(c.errorPercent-Math.abs(c.modelMetres-c.realMetres)/c.realMetres*100)<0.01,'Measurement error does not match its distances.');
  }
  return data;
}

function validateAsset(asset,extension) {
  requireValue(asset&&typeof asset.url==='string'&&asset.url.length<300&&/^[a-zA-Z0-9_./-]+$/.test(asset.url)&&!asset.url.startsWith('/')&&!asset.url.split('/').some(part=>part==='..')&&asset.url.endsWith(extension)&&hashPattern.test(asset.sha256),'Invalid packaged asset.');
}

export function validateScenePackage(data) {
  requireValue(data?.version===1&&typeof data.title==='string'&&data.title.length<=150&&hashPattern.test(data.sourceHash),'Invalid scene package.');
  validateAsset(data.assets?.splat,'.ply');
  requireValue(data.assets.splat.sha256===data.sourceHash,'Scene source hash does not match its splat.');
  if(data.assets.collision){validateAsset(data.assets.collision,'.glb');requireValue(data.assets.collision.coordinateSpace==='raw-ply-v1','Unsupported collision coordinates.');}
  requireValue(Array.isArray(data.views)&&data.views.length<=10000,'Invalid captured viewpoints.');
  for(const v of data.views)requireValue(v&&typeof v.name==='string'&&v.name.length<=250&&vector(v.position,3)&&vector(v.forward,3)&&Math.hypot(...v.forward)>0.1&&vector(v.up,3)&&Math.hypot(...v.up)>0.1&&finite(v.fov,160)&&v.fov>=10,'Invalid captured viewpoint.');
  if(data.setup!==null&&data.setup!==undefined){requireValue(!!data.assets.collision,'A walking scene needs collision geometry.');validateSetup(data.setup,'paired:'+data.sourceHash);requireValue(data.setup.collisionHash===data.assets.collision.sha256,'Setup belongs to different collision geometry.');}
  return data;
}

</file>

<file src="viewer/test/navigation.test.js">
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Group, Mesh, BoxGeometry, MeshBasicMaterial, Vector3 } from 'three';
import { buildNavigation } from '../src/navigation.js';
import { makeDemo } from '../src/demo.js';

test('a 75 cm aisle remains traversable without allowing passage through walls',async()=>{
  const root=new Group();
  const floor=new Mesh(new BoxGeometry(4,.2,8),new MeshBasicMaterial());
  floor.position.y=-.1;root.add(floor);
  for(const x of [-.875,.875]){
    const wall=new Mesh(new BoxGeometry(1,2.5,8),new MeshBasicMaterial());
    wall.position.set(x,1.25,0);root.add(wall);
  }
  const nav=await buildNavigation(root);
  try{
    assert.ok(nav.route(new Vector3(0,.04,-3),new Vector3(0,.04,3)),'clear aisle should connect');
    const state=nav.nearest(new Vector3(0,.04,0));assert.ok(state);
    for(let i=0;i<40;i++)nav.move(state,new Vector3(.04,0,0));
    assert.ok(state.point.x<.375,'body must not enter wall');
  }finally{nav.dispose();}
});

test('routes around the desk and walking cannot pass through it', async () => {
  const nav = await buildNavigation(makeDemo());
  try {
    const start = new Vector3(0,0.04,2.8), end = new Vector3(0,0.04,-2.8);
    const path = nav.route(start,end);
    assert.ok(path && path.length > 2, 'route must turn around the desk');
    for (let i=1;i<path.length;i++) for(let t=0;t<=1;t+=0.02) {
      const p=path[i-1].clone().lerp(path[i],t);
      assert.ok(!(Math.abs(p.x)<1.2 && Math.abs(p.z)<0.75),'route must avoid desk footprint');
    }
    const state=nav.nearest(start); assert.ok(state);
    for(let i=0;i<150;i++)nav.move(state,new Vector3(0,0,-0.04));
    assert.ok(state.point.z>0.75,'walking must stop at desk');
    assert.equal(nav.nearest(new Vector3(100,0,100)),null);
  } finally { nav.dispose(); }
});

test('rejects a partial path to a disconnected floor',async()=>{
  const root=new Group();
  for(const x of [-4,4]){const m=new Mesh(new BoxGeometry(4,0.2,4),new MeshBasicMaterial());m.position.set(x,-0.1,0);root.add(m);}
  const nav=await buildNavigation(root,{fillHoles:false});
  try {assert.equal(nav.route(new Vector3(-4,0.04,0),new Vector3(4,0.04,0)),null);}
  finally {nav.dispose();}
});

const box=(w,h,d,x,y,z)=>{const m=new Mesh(new BoxGeometry(w,h,d),new MeshBasicMaterial());m.position.set(x,y,z);return m;};

test('a hole in the reconstructed floor is filled, a bench still blocks',async()=>{
  const root=new Group();
  root.add(box(4,.02,3,0,-.01,-2.5), box(4,.02,3,0,-.01,2.5));  // floor with a 2 m hole in the middle
  root.add(box(4,.45,.4,0,.225,3.5));                             // bench seat across the far end
  const nav=await buildNavigation(root);
  try{
    assert.ok(nav.route(new Vector3(0,0,-3),new Vector3(0,0,2.5)),'walker crosses the unfilmed floor');
    const state=nav.nearest(new Vector3(0,0,2.5));assert.ok(state);
    for(let i=0;i<60;i++)nav.move(state,new Vector3(0,0,.04));
    assert.ok(state.point.z<3.3,'a 45 cm bench seat still blocks');
  }finally{nav.dispose();}
});

test('floating noise above 1.2 m and bumps under 30 cm do not block walking',async()=>{
  const root=new Group();
  root.add(box(4,.02,8,0,-.01,0));
  root.add(box(4,.1,.6,0,1.45,-1));   // floating blob at head height across the room
  root.add(box(4,.25,.3,0,.125,1));   // 25 cm bump across the room
  const nav=await buildNavigation(root);
  try{assert.ok(nav.route(new Vector3(0,0,-3),new Vector3(0,0,3)),'walker passes under the blob and over the bump');}
  finally{nav.dispose();}
});

</file>

<file src="viewer/test/package-aholo.test.js">
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {packageAholoScene} from '../scripts/package-aholo-scene.mjs';
import {WALK_PROFILE} from '../aholo/saved-walk.js';

const base=fileURLToPath(new URL('../test-results/',import.meta.url));
const hash=b=>createHash('sha256').update(b).digest('hex');
async function fixture(t){
  await fs.mkdir(base,{recursive:true});
  const root=await fs.mkdtemp(path.join(base,'aholo-package-'));
  t.after(async()=>{assert.equal(path.dirname(root),path.resolve(base));await fs.rm(root,{recursive:true,force:true});});
  const write=async(p,data)=>{await fs.mkdir(path.dirname(p),{recursive:true});await fs.writeFile(p,typeof data==='string'?data:JSON.stringify(data));};
  const folder=path.join(root,'data/scene-library/fixture'),scenePath=path.join(folder,'scene.json'),output=path.join(root,'output/demo');
  const splat='fixture splats',mesh='fixture collider',splatHash=hash(splat),collisionHash=hash(mesh);
  const manifest={version:1,type:'namma-viewer-scene',coordinateSpace:'raw-ply-v1',title:'Fixture',
    splat:{file:'preview.spz',sha256:splatHash,bytes:splat.length},collision:{file:'collision.glb',sha256:collisionHash,triangles:12},
    provenance:{privatePath:'C:/private/original'}};
  await write(scenePath,manifest);await write(path.join(folder,'preview.spz'),splat);await write(path.join(folder,'collision.glb'),mesh);
  const setupPath=path.join(root,'setup.json');
  await write(setupPath,{version:1,type:'namma-aholo-walk',profile:WALK_PROFILE,coordinateSpace:'raw-ply-v1',sceneIdentity:splatHash+':'+collisionHash,
    floor:{origin:[0,0,0],quaternion:[0,0,0,1]},metresPerUnit:1,eyeHeight:1.65,
    measurement:{metres:4,endpoints:[[0,0,0],[4,0,0]]},entrance:[0,.04,2],forward:[0,0,-1],reviewed:true});
  await write(path.join(root,'viewer/dist/aholo/index.html'),'<script src="../assets/app.js"></script>');
  await write(path.join(root,'viewer/dist/assets/app.js'),'Room manifest must be hosted with this viewer.');
  await write(path.join(root,'viewer/package.json'),{dependencies:{}});
  await write(path.join(root,'viewer/THIRD_PARTY_NOTICES.md'),'Fixture notices');
  return {root,scenePath,setupPath,output,folder,manifest,write};
}
test('portable Aholo package has relative scene URLs and setup but no private provenance',async t=>{
  const f=await fixture(t);const result=await packageAholoScene(f);
  assert.equal(result.walkingSetupIncluded,true);assert.equal(result.published,false);
  const manifest=JSON.parse(await fs.readFile(path.join(f.output,'scene/scene.json'),'utf8'));
  assert.equal(manifest.walkingSetup.metricVerified,false);assert.equal(manifest.provenance,undefined);
  assert.equal(hash(await fs.readFile(path.join(f.output,'scene/preview.spz'))),manifest.splat.sha256);
  assert.match(await fs.readFile(path.join(f.output,'index.html'),'utf8'),/\.\/aholo\/\?manifest=\.\.\/scene\/scene.json/);
  await assert.rejects(packageAholoScene(f),/already exists/);
});
test('wrong assets, missing setup, stale build and output escapes stop before writing',async t=>{
  const f=await fixture(t);
  await assert.rejects(packageAholoScene({...f,setupPath:undefined}),/walking setup/);
  await assert.rejects(packageAholoScene({...f,output:path.join(f.root,'../escaped-demo')}),/inside the workspace/);
  await f.write(path.join(f.folder,'collision.glb'),'changed');
  await assert.rejects(packageAholoScene(f),/Changed or incomplete collision/);
  await assert.rejects(fs.access(f.output),{code:'ENOENT'});
  await f.write(path.join(f.root,'viewer/dist/assets/app.js'),'old viewer');
  await assert.rejects(packageAholoScene(f),/predates portable/);
});

</file>

<file src="viewer/test/performance-budget.test.js">
import test from 'node:test';
import assert from 'node:assert/strict';
import {ResolutionBudget} from '../aholo/performance.js';

test('sustained slow frames reduce resolution within bounds, then recover gradually',()=>{
  const b=new ResolutionBudget();
  for(let i=0;i<1000;i++)b.sample(35);
  assert.equal(b.scale,.5);
  for(let i=0;i<3000;i++)b.sample(12);
  assert.equal(b.scale,1);
});
test('idle, background gaps and brief stalls do not turn into quality reductions',()=>{
  const b=new ResolutionBudget();
  for(let i=0;i<100;i++){b.sample(35,false);b.sample(1000);}
  assert.equal(b.scale,1);
  for(let i=0;i<100;i++)b.sample(16.7);
  assert.equal(b.scale,1);
  b.sample(80);
  assert.equal(b.scale,1);
});

test('sustained very low foreground FPS still triggers adaptation',()=>{
  const b=new ResolutionBudget();
  for(let i=0;i<120;i++)b.sample(300,true);
  assert.equal(b.scale,.5);
});

</file>

<file src="viewer/test/saved-walk.test.js">
import test from 'node:test';
import assert from 'node:assert/strict';
import {WALK_PROFILE, validateWalk, saveWalk, loadWalk, validateViewerManifest} from '../aholo/saved-walk.js';

const scene = {splatHash: 'a'.repeat(64), collisionHash: 'b'.repeat(64)};
const recipe = () => ({version:1, type:'namma-aholo-walk', profile:WALK_PROFILE,
  coordinateSpace:'raw-ply-v1', sceneIdentity:scene.splatHash+':'+scene.collisionHash,
  floor:{origin:[0,0,0],quaternion:[0,0,0,1]}, metresPerUnit:2, eyeHeight:1.65,
  measurement:{metres:4,endpoints:[[0,0,0],[2,0,0]]}, entrance:[1,0,1], forward:[0,0,-1], reviewed:true});

test('walking setup persists per exact asset pair without certifying measurement', () => {
  const memory = new Map();
  const storage = {getItem:k=>memory.get(k),setItem:(k,v)=>memory.set(k,v)};
  saveWalk(storage, scene, {...recipe(), metricVerified:true});
  const saved = loadWalk(storage, scene);
  assert.equal(saved.metricVerified, false);
  assert.deepEqual(saved.entrance,[1,0,1]);
  assert.equal(loadWalk(storage,{...scene,collisionHash:'c'.repeat(64)}),null);
  assert.throws(()=>validateWalk(saved,{...scene,splatHash:'c'.repeat(64)}),/different scene/);
});

test('stale navigation, broken scale, nonfinite transforms and unreviewed setups are rejected', () => {
  for (const edit of [r=>r.profile='old', r=>r.metresPerUnit=4, r=>r.floor.origin[0]=NaN,
    r=>r.floor.quaternion=[0,0,0,2], r=>r.eyeHeight=12, r=>r.reviewed=false,
    r=>r.entrance=[Infinity,0,0], r=>r.forward=[0,0,0]]) {
    const saved=recipe();edit(saved);assert.throws(()=>validateWalk(saved,scene));
  }
});

test('previous grid calibration migrates without changing measured scale or entrance',()=>{
  const old={...recipe(),profile:'recast-cs008-ch004-height170-radius025-v1'};
  const migrated=validateWalk(old,scene);
  assert.equal(migrated.profile,WALK_PROFILE);
  assert.equal(migrated.metresPerUnit,old.metresPerUnit);
  assert.deepEqual(migrated.entrance,old.entrance);
});

test('portable manifest rejects remote/traversing assets and mismatched walking setup', () => {
  const m={version:1,type:'namma-viewer-scene',coordinateSpace:'raw-ply-v1',title:'Fixture',
    splat:{file:'preview.spz',sha256:scene.splatHash,bytes:100},
    collision:{file:'collision.glb',sha256:scene.collisionHash,triangles:100},walkingSetup:recipe()};
  assert.equal(validateViewerManifest(m).walkingSetup.eyeHeight,1.65);
  assert.throws(()=>validateViewerManifest({...m,splat:{...m.splat,file:'../private.spz'}}));
  assert.throws(()=>validateViewerManifest({...m,collision:{...m.collision,sha256:'c'.repeat(64)}}));
});

test('manifest keeps the room up only when it is a unit vector', () => {
  const view={position:[0,0,0],rotation:[[1,0,0],[0,1,0],[0,0,1]],height:720,fy:650};
  const m={version:1,type:'namma-viewer-scene',coordinateSpace:'raw-ply-v1',title:'Fixture',
    splat:{file:'preview.spz',sha256:scene.splatHash,bytes:100},
    collision:{file:'collision.glb',sha256:scene.collisionHash,triangles:100}};
  assert.deepEqual(validateViewerManifest({...m,initialView:{...view,up:[0,-1,0]}}).initialView.up,[0,-1,0]);
  assert.equal(validateViewerManifest({...m,initialView:{...view,up:[0,-3,0]}}).initialView.up,undefined);
  assert.equal(validateViewerManifest({...m,initialView:view}).initialView.up,undefined);
});

</file>

<file src="viewer/test/scene-alignment.test.js">
import test from 'node:test';
import assert from 'node:assert/strict';
import {Object3D,Vector3} from 'three';
import {floorAlignment,copySceneTransform,calibratedSceneKey} from '../src/scene-alignment.js';
test('tilted floor becomes horizontal and a paired asset keeps identical coordinates',()=>{
  const p=[new Vector3(0,1,0),new Vector3(2,2,0),new Vector3(0,1,2)];
  const aligned=floorAlignment(p);
  const transformed=p.map(v=>v.clone().applyQuaternion(aligned.quaternion));
  assert.ok(Math.abs(transformed[0].y-transformed[1].y)<1e-8);
  assert.ok(Math.abs(transformed[0].y-transformed[2].y)<1e-8);
  const mesh=new Object3D(), splat=new Object3D();mesh.quaternion.copy(aligned.quaternion);mesh.scale.setScalar(0.42);mesh.position.set(3,-2,1);mesh.updateMatrixWorld();
  copySceneTransform(mesh,splat);
  assert.deepEqual(splat.matrixWorld.elements,mesh.matrixWorld.elements);
});
test('slightly tilted floor picks snap to the room up; a different plane does not',()=>{
  const roomUp=new Vector3(0,-1,0);
  const bumpy=[new Vector3(0,0,0),new Vector3(2,-0.1,0),new Vector3(0,0.05,2)];  // ~3 degrees off level
  const snapped=floorAlignment(bumpy,new Vector3(0,-1,0),roomUp);
  assert.ok(roomUp.clone().applyQuaternion(snapped.quaternion).distanceTo(new Vector3(0,1,0))<1e-9);
  const wall=[new Vector3(0,0,0),new Vector3(0,1,0),new Vector3(0,0,1)];
  const kept=floorAlignment(wall,new Vector3(1,0,0),roomUp);
  assert.ok(new Vector3(1,0,0).applyQuaternion(kept.quaternion).distanceTo(new Vector3(0,1,0))<1e-9);
});
test('floor picking rejects a straight line',()=>{
  assert.throws(()=>floorAlignment([new Vector3(),new Vector3(1,0,0),new Vector3(2,0,0)]),/straight line/);
});

test('saved locations cannot cross a change of floor plane or source export',()=>{
  const model=new Object3D(), first=calibratedSceneKey('export-a',model);
  model.rotation.z=0.2;
  assert.notEqual(calibratedSceneKey('export-a',model),first);
  const tilted=calibratedSceneKey('export-a',model);
  model.position.y=1;
  assert.notEqual(calibratedSceneKey('export-a',model),tilted);
  assert.notEqual(calibratedSceneKey('export-b',model),calibratedSceneKey('export-a',model));
});

</file>

<file src="viewer/test/scene-package.test.js">
import test from 'node:test';
import assert from 'node:assert/strict';
import {validateSetup,validateScenePackage} from '../src/scene-package.js';
const hash='a'.repeat(64);
const setup=()=>({version:1,sourceKey:'paired:'+hash,collisionHash:hash,transform:{position:[1,2,3],quaternion:[0,0,0,1],scale:0.5},floor:{origin:[0,0,0],quaternion:[0,0,0,1]},confirmed:true,pois:[],start:null,checks:[]});
test('setup round trip preserves floor, physical check and asset identity',()=>{
  const data=setup();data.checks.push({label:'Door width',realMetres:1,modelMetres:1.02,errorPercent:2});
  assert.deepEqual(validateSetup(JSON.parse(JSON.stringify(data)),data.sourceKey),data);
  assert.throws(()=>validateSetup(data,'paired:'+'b'.repeat(64)),/different model/);
  data.transform.scale=NaN;assert.throws(()=>validateSetup(data,data.sourceKey),/transform/);
});
test('invalid floor, duplicate locations and made-up error percentages are rejected',()=>{
  let d=setup();d.floor=null;assert.throws(()=>validateSetup(d,d.sourceKey),/selected floor/);
  d=setup();d.pois=[{id:'one',name:'Door',position:{x:0,y:0,z:0}},{id:'one',name:'Desk',position:{x:1,y:0,z:1}}];assert.throws(()=>validateSetup(d,d.sourceKey),/location/);
  d=setup();d.checks=[{label:'Width',realMetres:1,modelMetres:2,errorPercent:0}];assert.throws(()=>validateSetup(d,d.sourceKey),/error/);
});
test('portable manifest permits inspection-only scenes and rejects remote or traversing assets',()=>{
  const d={version:1,title:'Room',sourceHash:hash,assets:{splat:{url:'scene/room.ply',sha256:hash}},views:[],setup:null};
  assert.equal(validateScenePackage(d),d);
  for(const url of ['../private.ply','https://example.com/room.ply','/private.ply']){d.assets.splat.url=url;assert.throws(()=>validateScenePackage(d),/asset/);}
});

</file>

<file src="viewer/test/scene-pipeline.test.py">
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "viewer/scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pipeline = load("scene-pipeline")


class PipelineTests(unittest.TestCase):
    def setUp(self):
        (ROOT / "output").mkdir(exist_ok=True)
        self.root = Path(tempfile.mkdtemp(prefix="scene-test-", dir=ROOT / "output")).resolve()

    def tearDown(self):
        self.assertTrue(self.root.is_relative_to((ROOT / "output").resolve()))
        shutil.rmtree(self.root)

    def test_parts_join_and_corruption_rejection(self):
        pieces = [b"first", b"second"]
        records = []
        for index, data in enumerate(pieces):
            name = f"backup.part{index}"
            (self.root / name).write_bytes(data)
            records.append({"name": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
        manifest = self.root / "backup.parts.json"
        manifest.write_text(json.dumps({"archive": "backup.zip",
            "sha256": hashlib.sha256(b"".join(pieces)).hexdigest(), "parts": records}))
        joined = pipeline.join_parts(manifest, self.root / "good")
        self.assertEqual(joined.read_bytes(), b"firstsecond")
        (self.root / records[1]["name"]).write_bytes(b"broken")
        with self.assertRaisesRegex(ValueError, "changed part"):
            pipeline.join_parts(manifest, self.root / "bad")

    def test_archive_traversal_rejected_before_extraction(self):
        archive = self.root / "bad.zip"
        with zipfile.ZipFile(archive, "w") as z:
            z.writestr("../outside.txt", "no")
        with self.assertRaises(ValueError):
            pipeline.extract_archive(archive, self.root / "extracted")
        self.assertFalse((self.root / "outside.txt").exists())

    def test_wrong_model_is_never_registered(self):
        previous = pipeline.ROOT
        pipeline.ROOT = self.root
        try:
            archive = self.root / "geometry.zip"
            with zipfile.ZipFile(archive, "w") as z:
                z.writestr("recovery-report.json", json.dumps({"sourceModelSha256": "0" * 64}))
                z.writestr("room-collision-candidate.ply", "not used")
            model = self.root / "model.ply"
            model.write_bytes(b"wrong model")
            with self.assertRaisesRegex(ValueError, "different trained PLY"):
                pipeline.import_scene(archive, model)
            self.assertFalse((self.root / "data/scene-library").exists())
        finally:
            pipeline.ROOT = previous


if __name__ == "__main__":
    unittest.main()

</file>

<file src="viewer/vite.config.js">
import { defineConfig } from 'vite';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { sceneLibrary } from './server/scene-library.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

export default defineConfig({
  base: './',
  // aholo-viewer resolves its workers relative to import.meta.url, so it must not be prebundled.
  optimizeDeps: { exclude: ['recast-navigation', '@manycore/aholo-viewer'] },
  build: { target: 'es2022', rollupOptions: { input: {
    aholo: fileURLToPath(new URL('./aholo/index.html', import.meta.url)),
  } } },
  plugins: [{name: 'scene-library', configureServer(server) {
    // Imported rooms in <repo>/data/scene-library, served at /__scenes during local development only.
    server.middlewares.use(sceneLibrary(root));
  }}],
});

</file>

</codebase>
