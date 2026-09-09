"""
Unit tests for sub-pixel refinement layer.
SIH26166 Compliant.
"""
import numpy as np
import cv2

from src.registration.subpixel import refine_subpixel_correspondences


def test_subpixel_refinement_execution():
    # Synthetic image with high contrast corner patterns
    img1 = np.zeros((200, 200), dtype=np.uint8)
    cv2.rectangle(img1, (40, 40), (80, 80), 255, -1)
    cv2.rectangle(img1, (120, 120), (160, 160), 255, -1)

    img2 = img1.copy()

    # Initial integer points near corners
    pts1 = np.array([[40.0, 40.0], [80.0, 80.0], [120.0, 120.0], [160.0, 160.0]], dtype=np.float32)
    pts2 = pts1.copy()
    initial_mat = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], dtype=np.float32)

    res = refine_subpixel_correspondences(
        img1, img2, pts1, pts2, initial_matrix=initial_mat, model_type="affine"
    )

    assert res.refined_src_pts.shape == pts1.shape
    assert res.refined_ref_pts.shape == pts2.shape
    assert res.refined_matrix is not None
    assert isinstance(res.delta_rmse, float)
    assert res.scientific_disclaimer != ""
