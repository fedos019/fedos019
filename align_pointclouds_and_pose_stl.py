#!/usr/bin/env python3
"""Align STL-derived point cloud to image-derived point cloud and apply pose to STL."""

from __future__ import annotations

import numpy as np
import open3d as o3d

from project_paths import ALIGNED_STL, INPUT_STL, JPG_CLOUD, STL_CLOUD, TRANSFORM_TXT

# Registration settings (edit directly)
VOXEL_SIZE = 0.01
ICP_THRESHOLD = 0.03
SAVE_TRANSFORM = True


def preprocess_cloud(pcd: o3d.geometry.PointCloud, voxel_size: float):
    pcd_down = pcd.voxel_down_sample(voxel_size)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=voxel_size * 2.0, max_nn=30)
    )
    fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=voxel_size * 5.0, max_nn=100),
    )
    return pcd_down, fpfh


def execute_global_registration(
    source_down: o3d.geometry.PointCloud,
    target_down: o3d.geometry.PointCloud,
    source_fpfh,
    target_fpfh,
    voxel_size: float,
):
    distance_threshold = voxel_size * 1.5
    return o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down,
        target_down,
        source_fpfh,
        target_fpfh,
        mutual_filter=True,
        max_correspondence_distance=distance_threshold,
        estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        ransac_n=4,
        checkers=[
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(distance_threshold),
        ],
        criteria=o3d.pipelines.registration.RANSACConvergenceCriteria(200000, 1000),
    )


def main() -> None:
    src = o3d.io.read_point_cloud(str(STL_CLOUD))
    tgt = o3d.io.read_point_cloud(str(JPG_CLOUD))
    if src.is_empty() or tgt.is_empty():
        raise ValueError("Source/target point cloud is empty or unreadable")

    src_down, src_fpfh = preprocess_cloud(src, VOXEL_SIZE)
    tgt_down, tgt_fpfh = preprocess_cloud(tgt, VOXEL_SIZE)

    global_reg = execute_global_registration(src_down, tgt_down, src_fpfh, tgt_fpfh, VOXEL_SIZE)

    src_down.estimate_normals()
    tgt_down.estimate_normals()

    icp = o3d.pipelines.registration.registration_icp(
        src_down,
        tgt_down,
        max_correspondence_distance=ICP_THRESHOLD,
        init=global_reg.transformation,
        estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPlane(),
    )

    transform = icp.transformation

    mesh = o3d.io.read_triangle_mesh(str(INPUT_STL))
    if mesh.is_empty():
        raise ValueError(f"Could not read STL mesh: {INPUT_STL}")

    mesh.transform(transform)
    ok = o3d.io.write_triangle_mesh(str(ALIGNED_STL), mesh)
    if not ok:
        raise RuntimeError(f"Failed to write transformed STL: {ALIGNED_STL}")

    if SAVE_TRANSFORM:
        np.savetxt(TRANSFORM_TXT, transform, fmt="%.8f")

    print("Registration done")
    print(f"fitness={icp.fitness:.6f}, rmse={icp.inlier_rmse:.6f}")
    print("transform:\n", transform)


if __name__ == "__main__":
    main()
