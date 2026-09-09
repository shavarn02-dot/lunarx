"""
Unit tests for honest failure detection and diagnostic reporting.
SIH26166 Compliant — No Forced Successes.
"""
import numpy as np
from pathlib import Path
import pytest

from src.pipeline import run_registration_pipeline
from src.data.ingestion import LunarImageRecord, DataProvenance
from src.data.metadata import ChandrayaanMetadata


def test_failure_on_disjoint_images():
    # Two completely unrelated uniform images (no shared lunar features)
    img1 = np.full((300, 300), 50, dtype=np.uint8)
    img2 = np.full((300, 300), 200, dtype=np.uint8)

    rec1 = LunarImageRecord(
        image=img1.astype(np.float32) / 255.0, image_uint8=img1,
        file_path=Path("synthetic1.png"), metadata=ChandrayaanMetadata(),
        provenance=DataProvenance.USER_DERIVED, sensor="LUNAR_OPTICAL",
        resolution_m=5.0, original_shape=(300, 300),
        min_val=50.0, max_val=50.0, mean_val=50.0, std_val=0.0
    )
    rec2 = LunarImageRecord(
        image=img2.astype(np.float32) / 255.0, image_uint8=img2,
        file_path=Path("synthetic2.png"), metadata=ChandrayaanMetadata(),
        provenance=DataProvenance.USER_DERIVED, sensor="LUNAR_OPTICAL",
        resolution_m=5.0, original_shape=(300, 300),
        min_val=200.0, max_val=200.0, mean_val=200.0, std_val=0.0
    )

    out = run_registration_pipeline(rec1, rec2, method="sift")
    assert out.success is False
    assert out.quality_report.status == "FAILED"
    assert "REGISTRATION FAILED" in out.quality_report.failure_reason
    assert out.quality_report.inlier_match_count == 0


def test_failure_on_insufficient_matches():
    # Only 2 points provided (need at least 3 for affine, 4 for homography)
    src_pts = np.array([[10.0, 10.0], [20.0, 20.0]], dtype=np.float32)
    ref_pts = np.array([[15.0, 15.0], [25.0, 25.0]], dtype=np.float32)

    from src.registration.robust_estimation import estimate_robust_transformation
    res = estimate_robust_transformation(src_pts, ref_pts, model_type="affine")
    assert res.success is False
    assert "insufficient reliable correspondences" in res.diagnostic
