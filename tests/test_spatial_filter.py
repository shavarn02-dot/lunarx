"""
Unit tests for spatial correspondence filtering and coverage.
SIH26166 Compliant.
"""
import numpy as np
from src.registration.spatial_filter import filter_spatial_correspondences, compute_convex_hull_coverage


def test_spatial_filter_well_distributed():
    # Points spread uniformly across an 800x800 area
    grid_y, grid_x = np.mgrid[50:750:8j, 50:750:8j]
    pts = np.vstack([grid_x.ravel(), grid_y.ravel()]).T.astype(np.float32)

    res = filter_spatial_correspondences(
        src_pts=pts,
        ref_pts=pts,
        image_shape=(800, 800),
        grid_rows=8,
        grid_cols=8,
        min_coverage_ratio=0.15
    )

    assert res.meets_threshold is True
    assert res.grid_occupancy_ratio > 0.80
    assert res.convex_hull_coverage_ratio > 0.80


def test_spatial_filter_clustered_rejection():
    # Points clustered in a tiny 20x20 crater corner
    pts = np.random.uniform(10, 30, size=(50, 2)).astype(np.float32)

    res = filter_spatial_correspondences(
        src_pts=pts,
        ref_pts=pts,
        image_shape=(800, 800),
        grid_rows=8,
        grid_cols=8,
        min_coverage_ratio=0.15
    )

    # Clustered points should fail spatial coverage requirement
    assert res.meets_threshold is False
    assert res.occupied_cells <= 2
    assert "REGISTRATION FLAGGED / REJECTED" in res.diagnostic
