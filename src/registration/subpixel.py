"""
Sub-Pixel Correspondence Refinement Layer.
SIH26166 Compliant.
"""
from dataclasses import dataclass
from typing import Tuple, Optional, Dict, Any
import numpy as np
import cv2
import logging

from src.registration.geometry import validate_matrix_stability, GeometricValidation
from src.registration.robust_estimation import compute_reprojection_rmse

logger = logging.getLogger(__name__)


@dataclass
class SubpixelRefinementResult:
    refined_src_pts: np.ndarray       # Shape (N, 2), float32 sub-pixel coordinates
    refined_ref_pts: np.ndarray       # Shape (N, 2), float32 sub-pixel coordinates
    refined_matrix: np.ndarray        # Refined transformation matrix
    rmse_coarse: float                # Reprojection RMSE before refinement
    rmse_refined: float               # Reprojection RMSE after refinement
    delta_rmse: float                 # Improvement: coarse - refined (positive = improved)
    mean_subpixel_shift: float        # Average fractional shift in pixels
    max_subpixel_shift: float         # Maximum shift applied to any keypoint
    method: str
    improved: bool
    scientific_disclaimer: str = (
        "Note: Metric represents mathematical reprojection residual on matched inliers, "
        "not absolute geodetic lunar surface positioning accuracy."
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "method": self.method,
            "rmse_coarse": round(self.rmse_coarse, 4),
            "rmse_refined": round(self.rmse_refined, 4),
            "delta_rmse": round(self.delta_rmse, 4),
            "mean_subpixel_shift": round(self.mean_subpixel_shift, 4),
            "max_subpixel_shift": round(self.max_subpixel_shift, 4),
            "improved": self.improved,
            "disclaimer": self.scientific_disclaimer,
        }


def _refine_with_corner_subpix(
    img_u8: np.ndarray,
    pts: np.ndarray,
    win_size: Tuple[int, int] = (5, 5),
    zero_zone: Tuple[int, int] = (-1, -1),
    max_iters: int = 30,
    epsilon: float = 0.01
) -> np.ndarray:
    """Refine coordinates using gradient dot-product minimization (cv2.cornerSubPix)."""
    if len(pts) == 0:
        return pts.copy()

    h, w = img_u8.shape[:2]
    # Filter points too close to image boundary
    margin = max(win_size) + 1
    valid_mask = (
        (pts[:, 0] >= margin) & (pts[:, 0] < w - margin) &
        (pts[:, 1] >= margin) & (pts[:, 1] < h - margin)
    )

    refined = pts.copy().astype(np.float32)
    if not np.any(valid_mask):
        return refined

    sub_pts = pts[valid_mask].reshape(-1, 1, 2).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iters, epsilon)

    try:
        sub_refined = cv2.cornerSubPix(img_u8, sub_pts, win_size, zero_zone, criteria)
        refined[valid_mask] = sub_refined.reshape(-1, 2)
    except Exception as e:
        logger.warning(f"cornerSubPix refinement encountered error: {e}")

    return refined


def _reestimate_model(
    src_pts: np.ndarray,
    ref_pts: np.ndarray,
    model_type: str = "affine"
) -> Optional[np.ndarray]:
    """Re-estimate geometric model with unweighted least-squares on refined points."""
    if len(src_pts) < (4 if model_type == "homography" else 3):
        return None

    try:
        if model_type == "affine":
            mat, _ = cv2.estimateAffine2D(src_pts, ref_pts, method=cv2.LMEDS)
            return mat
        elif model_type == "homography":
            mat, _ = cv2.findHomography(src_pts, ref_pts, method=cv2.LMEDS)
            return mat
        elif model_type == "rigid":
            mat, _ = cv2.estimateAffinePartial2D(src_pts, ref_pts, method=cv2.LMEDS)
            return mat
    except Exception as e:
        logger.error(f"Least squares re-estimation failed: {e}")
    return None


def refine_subpixel_correspondences(
    src_img_u8: np.ndarray,
    ref_img_u8: np.ndarray,
    src_pts: np.ndarray,
    ref_pts: np.ndarray,
    initial_matrix: np.ndarray,
    model_type: str = "affine",
    method: str = "corner_subpix",
    win_size: Tuple[int, int] = (5, 5),
    max_iters: int = 30,
    epsilon: float = 0.01
) -> SubpixelRefinementResult:
    """
    Sub-pixel refinement stage for inlier keypoint correspondences.
    Calculates exact coarse vs refined RMSE and records displacement deltas.
    """
    rmse_coarse = compute_reprojection_rmse(src_pts, ref_pts, initial_matrix)

    if len(src_pts) < 4:
        return SubpixelRefinementResult(
            refined_src_pts=src_pts.copy(),
            refined_ref_pts=ref_pts.copy(),
            refined_matrix=initial_matrix,
            rmse_coarse=rmse_coarse,
            rmse_refined=rmse_coarse,
            delta_rmse=0.0,
            mean_subpixel_shift=0.0,
            max_subpixel_shift=0.0,
            method=method,
            improved=False,
        )

    # Refine point coordinates
    ref_src = _refine_with_corner_subpix(src_img_u8, src_pts, win_size=win_size, max_iters=max_iters, epsilon=epsilon)
    ref_ref = _refine_with_corner_subpix(ref_img_u8, ref_pts, win_size=win_size, max_iters=max_iters, epsilon=epsilon)

    # Calculate shift magnitudes
    shift_src = np.linalg.norm(ref_src - src_pts, axis=1)
    shift_ref = np.linalg.norm(ref_ref - ref_pts, axis=1)
    total_shifts = 0.5 * (shift_src + shift_ref)
    mean_shift = float(np.mean(total_shifts))
    max_shift = float(np.max(total_shifts))

    # Re-estimate transformation on refined points
    refined_mat = _reestimate_model(ref_src, ref_ref, model_type=model_type)
    if refined_mat is None:
        refined_mat = initial_matrix

    validation = validate_matrix_stability(refined_mat, model_type=model_type)
    if not validation.is_valid:
        # If refined matrix is degenerate, retain initial matrix
        refined_mat = initial_matrix

    rmse_refined = compute_reprojection_rmse(ref_src, ref_ref, refined_mat)
    delta_rmse = rmse_coarse - rmse_refined
    improved = rmse_refined <= rmse_coarse

    return SubpixelRefinementResult(
        refined_src_pts=ref_src,
        refined_ref_pts=ref_ref,
        refined_matrix=refined_mat,
        rmse_coarse=rmse_coarse,
        rmse_refined=rmse_refined,
        delta_rmse=delta_rmse,
        mean_subpixel_shift=mean_shift,
        max_subpixel_shift=max_shift,
        method=method,
        improved=improved,
    )
