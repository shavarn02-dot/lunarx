"""
End-to-End Acceptance Test on Real Chandrayaan-2 Lunar Imagery.
SIH26166 Compliant — Real Data Verification Only.
"""
from pathlib import Path
import pytest
import numpy as np

from src.pipeline import run_registration_pipeline


def test_end_to_end_real_chandrayaan_sift():
    src_path = Path("data/raw/ch2_tmc_crater_scene_src.png")
    ref_path = Path("data/raw/ch2_tmc_crater_scene_ref.png")

    if not src_path.exists() or not ref_path.exists():
        pytest.skip("Real Chandrayaan test pair not found in data/raw.")

    output = run_registration_pipeline(
        source_path=src_path,
        reference_path=ref_path,
        method="sift",
        preprocessing="clahe",
        model_type="affine",
        robust_estimator="USAC_MAGSAC",
        enforce_spatial_coverage=True,
        subpixel_enabled=True,
    )

    # Acceptance Criteria Verification
    assert output.success is True
    report = output.quality_report
    assert report.status == "SUCCESS"
    assert report.inlier_match_count > 100, f"Expected > 100 inliers, got {report.inlier_match_count}"
    assert report.reprojection_rmse_coarse < 1.0, f"Expected coarse RMSE < 1.0 px, got {report.reprojection_rmse_coarse}"
    assert report.spatial_coverage_percent > 50.0, f"Expected spatial coverage > 50%, got {report.spatial_coverage_percent}"
    assert report.grid_occupancy_percent > 75.0, f"Expected grid occupancy > 75%, got {report.grid_occupancy_percent}"
    assert report.photometric_ncc > 0.70, f"Expected photometric NCC > 0.70, got {report.photometric_ncc}"

    # Visualizations non-empty
    assert output.warped_image.shape == (600, 600)
    assert output.visualization_matches.shape[0] > 600
    assert output.visualization_checkerboard.shape[:2] == (600, 600)
    assert output.visualization_difference.shape[:2] == (600, 600)


def test_end_to_end_real_chandrayaan_superpoint_lightglue():
    src_path = Path("data/raw/ch2_tmc_crater_scene_src.png")
    ref_path = Path("data/raw/ch2_tmc_crater_scene_ref.png")

    if not src_path.exists() or not ref_path.exists():
        pytest.skip("Real Chandrayaan test pair not found in data/raw.")

    output = run_registration_pipeline(
        source_path=src_path,
        reference_path=ref_path,
        method="superpoint_lightglue",
        preprocessing="clahe",
        model_type="affine",
        robust_estimator="USAC_MAGSAC",
        enforce_spatial_coverage=True,
        subpixel_enabled=True,
    )

    assert output.success is True
    report = output.quality_report
    assert report.status == "SUCCESS"
    assert report.inlier_match_count > 50
    assert report.reprojection_rmse_coarse < 1.5
    assert report.spatial_coverage_percent > 50.0
    assert report.photometric_ncc > 0.70
