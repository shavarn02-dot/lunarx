"""
Unit tests for geometric transformation and robust estimation.
SIH26166 Compliant.
"""
import numpy as np
import pytest

from src.registration.geometry import validate_matrix_stability, warp_lunar_image
from src.registration.robust_estimation import (
    estimate_robust_transformation,
    compute_reprojection_rmse,
)


def test_matrix_stability_valid():
    # Affine matrix: 2.0 degree rotation, (10, -5) shift
    theta = np.radians(2.0)
    mat = np.array([
        [np.cos(theta), -np.sin(theta), 10.0],
        [np.sin(theta),  np.cos(theta), -5.0],
    ], dtype=np.float32)

    val = validate_matrix_stability(mat, model_type="affine")
    assert val.is_valid is True
    assert val.determinant > 0.9
    assert val.condition_number < 1.1


def test_matrix_stability_degenerate():
    # Degenerate collapsed matrix (det = 0)
    mat_zero = np.zeros((2, 3), dtype=np.float32)
    val = validate_matrix_stability(mat_zero, model_type="affine")
    assert val.is_valid is False

    # Negative determinant (reflection)
    mat_reflect = np.array([[-1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], dtype=np.float32)
    val_ref = validate_matrix_stability(mat_reflect, model_type="affine")
    assert val_ref.is_valid is False


def test_reprojection_rmse_calculation():
    # Points with known exact affine transformation
    src = np.array([[10.0, 20.0], [50.0, 60.0], [100.0, 120.0]], dtype=np.float32)
    mat = np.array([[1.0, 0.0, 5.0], [0.0, 1.0, -3.0]], dtype=np.float32)
    ref = np.array([[15.0, 17.0], [55.0, 57.0], [105.0, 117.0]], dtype=np.float32)

    rmse = compute_reprojection_rmse(src, ref, mat)
    assert rmse < 1e-5


def test_robust_estimation_with_outliers():
    # 50 inlier points with exact affine shift + 20 random outliers
    np.random.seed(42)
    src_inliers = np.random.uniform(50, 450, size=(50, 2)).astype(np.float32)
    ref_inliers = src_inliers + np.array([12.5, -8.0], dtype=np.float32)

    src_outliers = np.random.uniform(50, 450, size=(20, 2)).astype(np.float32)
    ref_outliers = np.random.uniform(50, 450, size=(20, 2)).astype(np.float32)

    src_all = np.vstack([src_inliers, src_outliers])
    ref_all = np.vstack([ref_inliers, ref_outliers])

    res = estimate_robust_transformation(src_all, ref_all, model_type="affine")
    assert res.success is True
    assert res.inlier_count >= 48  # Robustly rejects outliers
    assert res.reproj_rmse < 0.1
