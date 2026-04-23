#!/usr/bin/env python3
"""Convert JPG image to pseudo point cloud via MiDaS (paths from project_paths.py)."""

from __future__ import annotations

import cv2
import numpy as np
import open3d as o3d
import torch

from project_paths import INPUT_JPG, JPG_CLOUD

# Camera/depth settings (edit directly)
FX = 1000.0
FY = 1000.0
CX = None  # None -> image center
CY = None  # None -> image center
MAX_DEPTH = 3.0
VOXEL_SIZE = 0.0


def estimate_depth_midas(rgb_bgr: np.ndarray) -> np.ndarray:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    midas = torch.hub.load("intel-isl/MiDaS", "DPT_Large")
    midas.to(device)
    midas.eval()

    transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
    transform = transforms.dpt_transform

    img_rgb = cv2.cvtColor(rgb_bgr, cv2.COLOR_BGR2RGB)
    input_batch = transform(img_rgb).to(device)

    with torch.no_grad():
        prediction = midas(input_batch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img_rgb.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

    depth = prediction.cpu().numpy()
    depth = depth - depth.min()
    depth = depth / (depth.max() + 1e-8)
    return depth


def main() -> None:
    img = cv2.imread(str(INPUT_JPG), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"Could not read image: {INPUT_JPG}")

    h, w = img.shape[:2]
    cx = CX if CX is not None else w / 2.0
    cy = CY if CY is not None else h / 2.0

    depth_norm = estimate_depth_midas(img)
    depth_m = (depth_norm * MAX_DEPTH).astype(np.float32)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    color_o3d = o3d.geometry.Image(rgb)
    depth_o3d = o3d.geometry.Image(depth_m)

    rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
        color_o3d,
        depth_o3d,
        depth_scale=1.0,
        depth_trunc=MAX_DEPTH,
        convert_rgb_to_intensity=False,
    )

    intrinsics = o3d.camera.PinholeCameraIntrinsic(
        width=w,
        height=h,
        fx=FX,
        fy=FY,
        cx=cx,
        cy=cy,
    )

    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, intrinsics)
    pcd = pcd.remove_non_finite_points()[0]

    if VOXEL_SIZE > 0:
        pcd = pcd.voxel_down_sample(VOXEL_SIZE)

    ok = o3d.io.write_point_cloud(str(JPG_CLOUD), pcd)
    if not ok:
        raise RuntimeError(f"Failed to save point cloud: {JPG_CLOUD}")

    print(f"Saved point cloud: {JPG_CLOUD} ({len(pcd.points)} points)")


if __name__ == "__main__":
    main()
