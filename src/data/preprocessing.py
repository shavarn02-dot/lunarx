"""
Illumination-Invariant Preprocessing Pipeline for Lunar Imagery.
SIH26166 Compliant.
"""
from typing import Optional, Dict, Any, Union
import numpy as np
import cv2
import logging

logger = logging.getLogger(__name__)


def apply_clahe(img_u8: np.ndarray, clip_limit: float = 2.5, grid_size: tuple[int, int] = (8, 8)) -> np.ndarray:
    """
    Apply Contrast-Limited Adaptive Histogram Equalization.
    Enhances subtle shadow gradients inside craters while suppressing noise.
    """
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
    return clahe.apply(img_u8)


def apply_gradient_representation(img_u8: np.ndarray) -> np.ndarray:
    """
    Compute Sobel gradient magnitude representation.
    Provides first-order illumination invariance across crater rims.
    """
    gx = cv2.Sobel(img_u8, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(img_u8, cv2.CV_32F, 0, 1, ksize=3)
    mag = cv2.magnitude(gx, gy)
    
    # Normalize magnitude to uint8
    vmax = float(np.max(mag))
    if vmax > 0:
        norm_mag = (mag / vmax * 255.0).clip(0, 255).astype(np.uint8)
    else:
        norm_mag = np.zeros_like(img_u8)
    return norm_mag


def apply_phase_congruency_proxy(img_u8: np.ndarray) -> np.ndarray:
    """
    Frequency-domain bandpass / local energy proxy for phase congruency.
    Preserves structural crater topography invariant to illumination shifts.
    """
    # Difference of Gaussians (DoG) as an efficient real-time proxy for bandpass phase congruency
    g1 = cv2.GaussianBlur(img_u8, (3, 3), 1.0)
    g2 = cv2.GaussianBlur(img_u8, (9, 9), 2.5)
    dog = cv2.subtract(g1, g2)
    
    # Scale to full 8-bit dynamic range
    vmax = float(np.max(dog))
    if vmax > 0:
        return ((dog / vmax) * 255.0).clip(0, 255).astype(np.uint8)
    return dog


def preprocess_image(
    img_u8: np.ndarray,
    method: str = "clahe",
    params: Optional[Dict[str, Any]] = None
) -> np.ndarray:
    """
    Dispatch preprocessing on 8-bit grayscale lunar imagery.
    Candidate methods: 'raw', 'clahe', 'gradient', 'phase_congruency'.
    """
    method = method.lower()
    params = params or {}

    if method == "raw" or method == "none":
        return img_u8.copy()

    elif method == "clahe":
        clip_limit = params.get("clip_limit", 2.5)
        grid_size = tuple(params.get("tile_grid_size", (8, 8)))
        return apply_clahe(img_u8, clip_limit=clip_limit, grid_size=grid_size)

    elif method == "gradient" or method == "sobel":
        return apply_gradient_representation(img_u8)

    elif method == "phase_congruency" or method == "bandpass":
        return apply_phase_congruency_proxy(img_u8)

    else:
        logger.warning(f"Unknown preprocessing method '{method}'. Defaulting to CLAHE.")
        return apply_clahe(img_u8)
