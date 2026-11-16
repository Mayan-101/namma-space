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
from namma.workspace import read_json, sha256_file, write_json   # <-- added read_json

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
    """Load frames + sparse points, dropping weak frames identified during the priors stage."""
    rec = pycolmap.Reconstruction(ws.dataset / "sparse")
    images = sorted((img for img in rec.images.values() if img.has_pose), key=lambda img: img.name)

    # --- Quality filtering using priors diagnostics ---
    scales_info = read_json(ws.dataset / "priors_scales.json", {})
    metrics = scales_info.get("metrics", {})
    per_frame = {row["name"]: row for row in metrics.get("per_frame", [])}
    reliable_scales = scales_info.get("scales", {})

    median_log = float(np.median(list(reliable_scales.values()))) if reliable_scales else None

    # Thresholds (can later be moved to cfg.priors)
    MIN_POINTS = 80
    MIN_INLIER_FRAC = 0.50
    MAX_LOG_DEV = 1.0

    def is_weak(name: str) -> bool:
        info = per_frame.get(name)
        if info is None:
            return False

        points = info.get("points", 0)
        frac = info.get("inlier_fraction")
        log_s = info.get("log_scale")

        if points < MIN_POINTS:
            return True
        if frac is not None and frac < MIN_INLIER_FRAC:
            return True
        if log_s is not None and median_log is not None and abs(log_s - median_log) > MAX_LOG_DEV:
            return True
        return False

    original_count = len(images)
    images = [img for img in images if not is_weak(img.name)]
    dropped = original_count - len(images)
    if dropped:
        print(f"load_dataset: dropped {dropped} weak frames "
              f"({dropped / original_count:.1%} of registered cameras)", flush=True)

    if len(images) < 30:
        raise RuntimeError(
            f"Only {len(images)} frames left after quality filtering. "
            "The video may have too many blurry / low-texture sections."
        )

    def load(img):
        cam = rec.cameras[img.camera_id]
        fx, fy, cx, cy = cam.params[:4] if cam.model_name == "PINHOLE" else (cam.params[0],) * 2 + tuple(cam.params[1:3])
        pose = cam_from_world(img)
        w2c = np.eye(4)
        w2c[:3, :3] = np.asarray(pose.rotation.matrix())
        w2c[:3, 3] = np.asarray(pose.translation)
        rgb = cv2.cvtColor(cv2.imread(str(ws.dataset / "images" / img.name)), cv2.COLOR_BGR2RGB)
        frame = Frame(
            img.name,
            torch.tensor([[fx, 0, cx], [0, fy, cy], [0, 0, 1]], dtype=torch.float32),
            torch.from_numpy(np.linalg.inv(w2c)).float(),
            rgb.shape[1], rgb.shape[0],
            torch.from_numpy(rgb),
        )
        prior = ws.priors / f"{img.name}.npz"
        if with_priors and prior.exists():
            data = np.load(prior)
            frame.depth = torch.from_numpy(data["depth"])
            if "normal" in data:
                frame.normal = torch.from_numpy(data["normal"])
        return frame

    # Existing outlier-camera filtering
    centers = np.array([
        np.asarray(cam_from_world(img).rotation.matrix()).T @ -np.asarray(cam_from_world(img).translation)
        for img in images
    ])
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