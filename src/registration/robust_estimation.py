"""
Robust Outlier Rejection: MAGSAC++ and RANSAC Estimators.
SIH26166 Compliant.
"""
from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any
import numpy as np
import cv2
import logging

from src.registration.geometry import validate_matrix_stability, GeometricValidation

logger = logging.getLogger(__name__)


@dataclass
class RobustEstimationResult:
    matrix: Optional[np.ndarray]
    model_type: str
    inlier_mask: np.ndarray        # Boolean 1D array of shape (N,)
    inlier_count: int
    raw_count: int
    inlier_ratio: float
    reproj_rmse: float
    validation: GeometricValidation
    success: bool
    diagnostic: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_type": self.model_type,
            "raw_count": self.raw_count,
            "inlier_count": self.inlier_count,
            "inlier_ratio": round(self.inlier_ratio, 4),
            "reproj_rmse": round(self.reproj_rmse, 4),
            "is_stable": self.validation.is_valid,
            "condition_number": self.validation.condition_number,
            "determinant": self.validation.determinant,
            "scale_x": self.validation.scale_x,
            "scale_y": self.validation.scale_y,
            "rotation_deg": self.validation.rotation_deg,
            "success": self.success,
            "diagnostic": self.diagnostic,
        }


def compute_reprojection_rmse(
    src_pts: np.ndarray,
    ref_pts: np.ndarray,
    matrix: np.ndarray
) -> float:
    """
    Compute Root Mean Squared Error (RMSE) of reprojection residuals.
    src_pts: (N, 2), ref_pts: (N, 2), matrix: (2, 3) or (3, 3)
    """
    if len(src_pts) == 0 or matrix is None:
        return float("inf")

    src_h = np.hstack([src_pts, np.ones((len(src_pts), 1), dtype=np.float32)])  # (N, 3)

    if matrix.shape == (2, 3):
        # Affine mapping: p' = A * p + t
        pred = (matrix @ src_h.T).T  # (N, 2)
    elif matrix.shape == (3, 3):
        # Homography mapping: p' = H * p / (h31*x + h32*y + h33)
        pred_h = (matrix @ src_h.T).T  # (N, 3)
        w = pred_h[:, 2:3]
        w = np.where(np.abs(w) < 1e-8, 1e-8, w)
        pred = pred_h[:, :2] / w
    else:
        return float("inf")

    diff = ref_pts - pred
    sq_err = np.sum(diff ** 2, axis=1)
    rmse = float(np.sqrt(np.mean(sq_err)))
    return rmse


def estimate_robust_transformation(
    src_pts: np.ndarray,
    ref_pts: np.ndarray,
    model_type: str = "affine",
    method: str = "USAC_MAGSAC",
    reproj_thresh: float = 3.0,
    confidence: float = 0.999,
    max_iters: int = 10000
) -> RobustEstimationResult:
    """
    Estimate transformation matrix using statistically robust consensus (MAGSAC++ or RANSAC).
    Filters false correspondences and verifies geometric stability.
    """
    n_raw = len(src_pts)
    empty_mask = np.zeros(n_raw, dtype=bool)
    model_type = model_type.lower()

    min_required = 4 if model_type == "homography" else (3 if model_type == "affine" else 2)
    if n_raw < min_required:
        return RobustEstimationResult(
            matrix=None, model_type=model_type, inlier_mask=empty_mask,
            inlier_count=0, raw_count=n_raw, inlier_ratio=0.0, reproj_rmse=float("inf"),
            validation=validate_matrix_stability(None), success=False,
            diagnostic=f"REGISTRATION FAILED — insufficient reliable correspondences (found {n_raw}, required >= {min_required})."
        )

    # Determine OpenCV estimator flag
    if method.upper() == "USAC_MAGSAC" and hasattr(cv2, "USAC_MAGSAC"):
        cv_method = cv2.USAC_MAGSAC
    else:
        cv_method = cv2.RANSAC

    matrix = None
    inlier_mask_raw = None

    try:
        if model_type == "affine":
            matrix, inlier_mask_raw = cv2.estimateAffine2D(
                src_pts, ref_pts,
                method=cv_method,
                ransacReprojThreshold=reproj_thresh,
                maxIters=max_iters,
                confidence=confidence
            )
        elif model_type == "homography":
            matrix, inlier_mask_raw = cv2.findHomography(
                src_pts, ref_pts,
                method=cv_method,
                ransacReprojThreshold=reproj_thresh,
                maxIters=max_iters,
                confidence=confidence
            )
        elif model_type == "rigid":
            # OpenCV estimateAffinePartial2D only supports RANSAC or LMEDS
            rigid_method = cv2.RANSAC if (hasattr(cv2, "USAC_MAGSAC") and cv_method == cv2.USAC_MAGSAC) else cv_method
            matrix, inlier_mask_raw = cv2.estimateAffinePartial2D(
                src_pts, ref_pts,
                method=rigid_method,
                ransacReprojThreshold=reproj_thresh,
                maxIters=max_iters,
                confidence=confidence
            )
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    except Exception as e:
        logger.error(f"Error during robust estimation: {e}")
        matrix = None

    if matrix is None or inlier_mask_raw is None:
        return RobustEstimationResult(
            matrix=None, model_type=model_type, inlier_mask=empty_mask,
            inlier_count=0, raw_count=n_raw, inlier_ratio=0.0, reproj_rmse=float("inf"),
            validation=validate_matrix_stability(None), success=False,
            diagnostic="REGISTRATION FAILED — consensus estimation could not find a valid geometric model."
        )

    inlier_mask = inlier_mask_raw.ravel().astype(bool)
    inlier_count = int(np.sum(inlier_mask))
    inlier_ratio = inlier_count / float(n_raw) if n_raw > 0 else 0.0

    validation = validate_matrix_stability(matrix, model_type=model_type)

    if inlier_count < min_required:
        return RobustEstimationResult(
            matrix=matrix, model_type=model_type, inlier_mask=inlier_mask,
            inlier_count=inlier_count, raw_count=n_raw, inlier_ratio=inlier_ratio,
            reproj_rmse=float("inf"), validation=validation, success=False,
            diagnostic=f"REGISTRATION FAILED — too few inliers ({inlier_count} < {min_required}) after outlier rejection."
        )

    if not validation.is_valid:
        return RobustEstimationResult(
            matrix=matrix, model_type=model_type, inlier_mask=inlier_mask,
            inlier_count=inlier_count, raw_count=n_raw, inlier_ratio=inlier_ratio,
            reproj_rmse=float("inf"), validation=validation, success=False,
            diagnostic=f"REGISTRATION FAILED — unstable transformation ({validation.message})"
        )

    # Compute RMSE on inlier points
    src_inliers = src_pts[inlier_mask]
    ref_inliers = ref_pts[inlier_mask]
    rmse = compute_reprojection_rmse(src_inliers, ref_inliers, matrix)

    return RobustEstimationResult(
        matrix=matrix,
        model_type=model_type,
        inlier_mask=inlier_mask,
        inlier_count=inlier_count,
        raw_count=n_raw,
        inlier_ratio=inlier_ratio,
        reproj_rmse=rmse,
        validation=validation,
        success=True,
        diagnostic="SUCCESS: Robust geometric model verified.",
    )
