#!/usr/bin/env python3
"""Convert STL mesh to point cloud (paths are configured in project_paths.py)."""

from __future__ import annotations

import open3d as o3d

from project_paths import INPUT_STL, STL_CLOUD

NUM_POINTS = 200_000
METHOD = "poisson"  # "poisson" or "uniform"


def main() -> None:
    mesh = o3d.io.read_triangle_mesh(str(INPUT_STL))
    if mesh.is_empty():
        raise ValueError(f"Could not read mesh or mesh is empty: {INPUT_STL}")

    mesh.compute_vertex_normals()

    if METHOD == "poisson":
        pcd = mesh.sample_points_poisson_disk(number_of_points=NUM_POINTS)
    elif METHOD == "uniform":
        pcd = mesh.sample_points_uniformly(number_of_points=NUM_POINTS)
    else:
        raise ValueError(f"Unsupported METHOD: {METHOD}")

    ok = o3d.io.write_point_cloud(str(STL_CLOUD), pcd)
    if not ok:
        raise RuntimeError(f"Failed to write point cloud to {STL_CLOUD}")

    print(f"Saved point cloud: {STL_CLOUD} ({len(pcd.points)} points)")


if __name__ == "__main__":
    main()
