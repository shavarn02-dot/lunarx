"""
Before/After Registration Visual Overlays: Checkerboard, Blends, Difference Heatmaps.
SIH26166 Compliant.
"""
from typing import Tuple
import numpy as np
import cv2


def create_checkerboard_overlay(
    ref_u8: np.ndarray,
    warped_u8: np.ndarray,
    square_size: int = 48
) -> np.ndarray:
    """
    Construct an alternating checkerboard between the reference and warped images
    to visually inspect edge alignment and registration continuity.
    """
    h = min(ref_u8.shape[0], warped_u8.shape[0])
    w = min(ref_u8.shape[1], warped_u8.shape[1])

    r_crop = ref_u8[:h, :w]
    w_crop = warped_u8[:h, :w]

    # Create checker mask
    grid_y, grid_x = np.indices((h, w))
    checker_mask = ((grid_y // square_size) + (grid_x // square_size)) % 2 == 0

    out = np.where(checker_mask, r_crop, w_crop)

    # Convert to BGR for clean visualization
    out_bgr = cv2.cvtColor(out, cv2.COLOR_GRAY2BGR) if out.ndim == 2 else out
    return out_bgr


def create_difference_heatmap(
    ref_u8: np.ndarray,
    warped_u8: np.ndarray
) -> np.ndarray:
    """
    Compute absolute pixel difference and apply a colormap to highlight residual misalignments.
    """
    h = min(ref_u8.shape[0], warped_u8.shape[0])
    w = min(ref_u8.shape[1], warped_u8.shape[1])

    r_crop = ref_u8[:h, :w]
    w_crop = warped_u8[:h, :w]

    # Mask non-overlapping black areas
    valid_mask = (w_crop > 0) & (r_crop > 0)
    diff = np.abs(r_crop.astype(np.int16) - w_crop.astype(np.int16)).astype(np.uint8)
    diff[~valid_mask] = 0

    # Apply JET or INFERNO colormap
    heatmap = cv2.applyColorMap(diff, cv2.COLORMAP_JET)
    heatmap[~valid_mask] = [20, 20, 20]  # Dark gray background for non-overlap
    return heatmap


def create_split_slider_composite(
    ref_u8: np.ndarray,
    warped_u8: np.ndarray,
    split_ratio: float = 0.5
) -> np.ndarray:
    """
    Generate split-view composite (Source/Warped on left, Reference on right).
    """
    h = min(ref_u8.shape[0], warped_u8.shape[0])
    w = min(ref_u8.shape[1], warped_u8.shape[1])

    split_x = int(w * split_ratio)
    split_x = max(0, min(w, split_x))

    r_crop = cv2.cvtColor(ref_u8[:h, :w], cv2.COLOR_GRAY2BGR) if ref_u8.ndim == 2 else ref_u8[:h, :w]
    w_crop = cv2.cvtColor(warped_u8[:h, :w], cv2.COLOR_GRAY2BGR) if warped_u8.ndim == 2 else warped_u8[:h, :w]

    composite = np.zeros_like(r_crop)
    composite[:, :split_x] = w_crop[:, :split_x]
    composite[:, split_x:] = r_crop[:, split_x:]

    # Draw separator line
    cv2.line(composite, (split_x, 0), (split_x, h), (0, 229, 255), 2)
    return composite
