"""
Dual-Image Match Correspondence Visualizer and Spatial Grid Overlay.
SIH26166 Compliant.
"""
from typing import Optional, Tuple
import numpy as np
import cv2


def draw_correspondences(
    src_u8: np.ndarray,
    ref_u8: np.ndarray,
    src_pts: np.ndarray,
    ref_pts: np.ndarray,
    inlier_mask: Optional[np.ndarray] = None,
    max_draw: int = 150
) -> np.ndarray:
    """
    Render side-by-side dual image visualization showing correspondences.
    Inliers are drawn in green/cyan; rejected outliers are drawn in red.
    """
    h1, w1 = src_u8.shape[:2]
    h2, w2 = ref_u8.shape[:2]

    # Target height is max of both
    canvas_h = max(h1, h2) + 60  # Extra 60px for header banner
    canvas_w = w1 + w2

    canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

    # Convert source and reference to BGR
    c_src = cv2.cvtColor(src_u8, cv2.COLOR_GRAY2BGR) if src_u8.ndim == 2 else src_u8.copy()
    c_ref = cv2.cvtColor(ref_u8, cv2.COLOR_GRAY2BGR) if ref_u8.ndim == 2 else ref_u8.copy()

    # Place images below header banner
    canvas[60: 60 + h1, 0: w1] = c_src
    canvas[60: 60 + h2, w1: w1 + w2] = c_ref

    # Draw header banner
    cv2.rectangle(canvas, (0, 0), (canvas_w, 60), (15, 20, 30), -1)
    cv2.line(canvas, (0, 60), (canvas_w, 60), (0, 229, 255), 2)
    cv2.line(canvas, (w1, 60), (w1, canvas_h), (60, 70, 90), 1)

    n_total = len(src_pts)
    n_inliers = int(np.sum(inlier_mask)) if inlier_mask is not None else n_total

    header_text = f"SIH26166 CORRESPONDENCE: Raw Matches={n_total} | Inliers={n_inliers}"
    if inlier_mask is not None and n_total > 0:
        ratio = (n_inliers / float(n_total)) * 100.0
        header_text += f" ({ratio:.1f}%)"
    cv2.putText(canvas, header_text, (20, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 229, 255), 2, cv2.LINE_AA)

    # Labels for source and reference
    cv2.putText(canvas, "SOURCE SCENE", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(canvas, "REFERENCE SCENE", (w1 + 20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

    if n_total == 0:
        return canvas

    # Sample points to draw to avoid overwhelming clutter
    indices = np.arange(n_total)
    if n_total > max_draw:
        # Prioritize inliers if available
        if inlier_mask is not None:
            in_idx = np.where(inlier_mask)[0]
            out_idx = np.where(~inlier_mask)[0]
            n_in = min(len(in_idx), int(max_draw * 0.8))
            n_out = min(len(out_idx), max_draw - n_in)
            samp_in = np.random.choice(in_idx, n_in, replace=False) if len(in_idx) > 0 else []
            samp_out = np.random.choice(out_idx, n_out, replace=False) if len(out_idx) > 0 else []
            indices = np.concatenate([samp_in, samp_out]).astype(int)
        else:
            indices = np.random.choice(indices, max_draw, replace=False).astype(int)

    for idx in indices:
        i = int(idx)
        p1 = (int(round(src_pts[i, 0])), int(round(src_pts[i, 1])) + 60)
        p2 = (int(round(ref_pts[i, 0])) + w1, int(round(ref_pts[i, 1])) + 60)

        is_inlier = bool(inlier_mask[i]) if inlier_mask is not None else True
        color = (0, 230, 115) if is_inlier else (50, 50, 230)  # Green vs Red (BGR)
        thickness = 2 if is_inlier else 1

        cv2.circle(canvas, p1, 4, color, -1, cv2.LINE_AA)
        cv2.circle(canvas, p2, 4, color, -1, cv2.LINE_AA)
        cv2.line(canvas, p1, p2, color, thickness, cv2.LINE_AA)

    return canvas


def draw_spatial_grid_overlay(
    img_u8: np.ndarray,
    pts: np.ndarray,
    grid_rows: int = 8,
    grid_cols: int = 8
) -> np.ndarray:
    """
    Render grid cells over the image and highlight cells that contain correspondences.
    """
    h, w = img_u8.shape[:2]
    canvas = cv2.cvtColor(img_u8, cv2.COLOR_GRAY2BGR) if img_u8.ndim == 2 else img_u8.copy()

    cell_w = w / float(grid_cols)
    cell_h = h / float(grid_rows)

    # Determine occupied cells
    occupied = set()
    for p in pts:
        c = int(p[0] / cell_w)
        r = int(p[1] / cell_h)
        c = max(0, min(grid_cols - 1, c))
        r = max(0, min(grid_rows - 1, r))
        occupied.add((r, c))

    # Highlight occupied cells with semi-transparent overlay
    overlay = canvas.copy()
    for (r, c) in occupied:
        x1, y1 = int(c * cell_w), int(r * cell_h)
        x2, y2 = int((c + 1) * cell_w), int((r + 1) * cell_h)
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 200, 255), -1)

    cv2.addWeighted(overlay, 0.25, canvas, 0.75, 0, canvas)

    # Draw grid lines
    for c in range(grid_cols + 1):
        x = int(c * cell_w)
        cv2.line(canvas, (x, 0), (x, h), (100, 120, 150), 1)
    for r in range(grid_rows + 1):
        y = int(r * cell_h)
        cv2.line(canvas, (0, y), (w, y), (100, 120, 150), 1)

    # Draw points
    for p in pts:
        cv2.circle(canvas, (int(round(p[0])), int(round(p[1]))), 3, (0, 255, 0), -1, cv2.LINE_AA)

    return canvas
