"""
Geometric Transformation Models and Stability Verification.
SIH26166 Compliant.
"""
from dataclasses import dataclass
from typing import Tuple, Optional, Dict, Any
import numpy as np
import cv2
import logging

logger = logging.getLogger(__name__)


@dataclass
class GeometricValidation:
    is_valid: bool
    condition_number: float
    determinant: float
    scale_x: float
    scale_y: float
    rotation_deg: float
    shear: float
    message: str


def validate_matrix_stability(matrix: np.ndarray, model_type: str = "affine", max_cond: float = 1e5) -> GeometricValidation:
    """
    Validate mathematical conditioning of estimated transformation matrix.
    Prevents degenerate or collapsed warps from being accepted as valid registrations.
    """
    if matrix is None or matrix.size == 0:
        return GeometricValidation(
            is_valid=False, condition_number=float("inf"), determinant=0.0,
            scale_x=0.0, scale_y=0.0, rotation_deg=0.0, shear=0.0, message="Matrix is None or empty."
        )

    # Extract 2x2 linear portion
    if matrix.shape == (2, 3):
        A = matrix[:2, :2]
    elif matrix.shape == (3, 3):
        # Normalize homography by bottom-right element if non-zero
        if abs(matrix[2, 2]) > 1e-8:
            matrix = matrix / matrix[2, 2]
        A = matrix[:2, :2]
    else:
        return GeometricValidation(
            is_valid=False, condition_number=float("inf"), determinant=0.0,
            scale_x=0.0, scale_y=0.0, rotation_deg=0.0, shear=0.0, message=f"Unsupported shape: {matrix.shape}"
        )

    # SVD for condition number and singular values
    try:
        U, S, Vt = np.linalg.svd(A)
    except Exception as e:
        return GeometricValidation(
            is_valid=False, condition_number=float("inf"), determinant=0.0,
            scale_x=0.0, scale_y=0.0, rotation_deg=0.0, shear=0.0, message=f"SVD decomposition failed: {e}"
        )

    s_max = float(S[0])
    s_min = float(S[1]) if len(S) > 1 and S[1] > 1e-12 else 1e-12
    cond = s_max / s_min
    det = float(np.linalg.det(A))

    # Decompose affine components: scale, rotation, shear
    scale_x = float(np.sqrt(A[0, 0] ** 2 + A[1, 0] ** 2))
    scale_y = float(np.sqrt(A[0, 1] ** 2 + A[1, 1] ** 2))
    rotation_rad = float(np.arctan2(A[1, 0], A[0, 0]))
    rotation_deg = float(np.degrees(rotation_rad))
    shear = float(A[0, 1] / (scale_y + 1e-12))

    # Validation criteria:
    # 1. Determinant must be positive (no reflection of lunar surface)
    # 2. Condition number must be below limit
    # 3. Scale must be physically bounded (between 0.05 and 20.0)
    reasons = []
    if det <= 0:
        reasons.append(f"Negative or zero determinant (det={det:.4f}, reflection/collapse).")
    if cond > max_cond:
        reasons.append(f"Ill-conditioned matrix (cond={cond:.1e} > {max_cond:.1e}).")
    if scale_x < 0.05 or scale_x > 20.0 or scale_y < 0.05 or scale_y > 20.0:
        reasons.append(f"Extreme scaling out of physical bounds (sx={scale_x:.2f}, sy={scale_y:.2f}).")

    is_valid = len(reasons) == 0
    msg = "Valid geometric transformation." if is_valid else " ; ".join(reasons)

    return GeometricValidation(
        is_valid=is_valid,
        condition_number=round(cond, 2),
        determinant=round(det, 4),
        scale_x=round(scale_x, 4),
        scale_y=round(scale_y, 4),
        rotation_deg=round(rotation_deg, 2),
        shear=round(shear, 4),
        message=msg,
    )


def warp_lunar_image(
    image: np.ndarray,
    matrix: np.ndarray,
    target_shape: Tuple[int, int],
    model_type: str = "affine"
) -> np.ndarray:
    """
    Warp image using estimated transformation matrix into target frame.
    target_shape is (height, width).
    """
    h_out, w_out = target_shape
    if matrix.shape == (2, 3):
        warped = cv2.warpAffine(
            image, matrix, (w_out, h_out),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=0
        )
    elif matrix.shape == (3, 3):
        warped = cv2.warpPerspective(
            image, matrix, (w_out, h_out),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=0
        )
    else:
        raise ValueError(f"Invalid matrix shape for warping: {matrix.shape}")
    return warped
