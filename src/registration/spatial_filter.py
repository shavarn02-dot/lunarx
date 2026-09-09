"""
Spatial Correspondence Filtering and Coverage Enforcement.
SIH26166 Compliant.
"""
from dataclasses import dataclass
from typing import Tuple, List, Optional, Dict, Any
import numpy as np
from scipy.spatial import ConvexHull
import logging

logger = logging.getLogger(__name__)


@dataclass
class SpatialDistributionResult:
    filtered_src_pts: np.ndarray      # Shape (K, 2)
    filtered_ref_pts: np.ndarray      # Shape (K, 2)
    filtered_confidences: np.ndarray  # Shape (K,)
    grid_rows: int
    grid_cols: int
    occupied_cells: int
    total_cells: int
    grid_occupancy_ratio: float       # In [0.0, 1.0]
    convex_hull_coverage_ratio: float # In [0.0, 1.0]
    meets_threshold: bool
    diagnostic: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "occupied_cells": self.occupied_cells,
            "total_cells": self.total_cells,
            "grid_occupancy_percent": round(self.grid_occupancy_ratio * 100.0, 2),
            "convex_hull_coverage_percent": round(self.convex_hull_coverage_ratio * 100.0, 2),
            "meets_threshold": self.meets_threshold,
            "diagnostic": self.diagnostic,
        }


def compute_convex_hull_coverage(pts: np.ndarray, image_shape: Tuple[int, int]) -> float:
    """
    Calculate the ratio of the convex hull area of inlier points
    to the total scene bounding area.
    """
    if len(pts) < 3:
        return 0.0

    try:
        hull = ConvexHull(pts)
        hull_area = float(hull.volume)  # In 2D, hull.volume is the polygon area
    except Exception:
        return 0.0

    # Bounding area of the points or scene
    x_min, y_min = np.min(pts, axis=0)
    x_max, y_max = np.max(pts, axis=0)
    box_area = max(1.0, float((x_max - x_min) * (y_max - y_min)))
    
    coverage = min(1.0, max(0.0, hull_area / box_area))
    return coverage


def filter_spatial_correspondences(
    src_pts: np.ndarray,
    ref_pts: np.ndarray,
    confidences: Optional[np.ndarray] = None,
    image_shape: Optional[Tuple[int, int]] = None,
    grid_rows: int = 8,
    grid_cols: int = 8,
    max_matches_per_cell: int = 5,
    min_coverage_ratio: float = 0.15,
    enforce_coverage: bool = True
) -> SpatialDistributionResult:
    """
    Partition correspondence coordinates into an R x C grid, limit dominant
    crater rim clusters, and enforce minimum spatial dispersion.
    """
    n = len(src_pts)
    if confidences is None:
        confidences = np.ones(n, dtype=np.float32)

    if n == 0:
        return SpatialDistributionResult(
            filtered_src_pts=np.empty((0, 2), dtype=np.float32),
            filtered_ref_pts=np.empty((0, 2), dtype=np.float32),
            filtered_confidences=np.empty((0,), dtype=np.float32),
            grid_rows=grid_rows, grid_cols=grid_cols,
            occupied_cells=0, total_cells=grid_rows * grid_cols,
            grid_occupancy_ratio=0.0, convex_hull_coverage_ratio=0.0,
            meets_threshold=False,
            diagnostic="REGISTRATION FAILED — zero points available for spatial distribution."
        )

    # Determine coordinate bounds
    if image_shape is not None:
        h_bound, w_bound = float(image_shape[0]), float(image_shape[1])
        x_min, y_min = 0.0, 0.0
        x_max, y_max = w_bound, h_bound
    else:
        x_min, y_min = float(np.min(src_pts[:, 0])), float(np.min(src_pts[:, 1]))
        x_max, y_max = float(np.max(src_pts[:, 0])), float(np.max(src_pts[:, 1]))

    w_extent = max(1.0, x_max - x_min)
    h_extent = max(1.0, y_max - y_min)

    cell_w = w_extent / float(grid_cols)
    cell_h = h_extent / float(grid_rows)

    # Grid bins: (row, col) -> list of point indices
    grid: Dict[Tuple[int, int], List[int]] = {}
    for i in range(n):
        c = int((src_pts[i, 0] - x_min) / cell_w)
        r = int((src_pts[i, 1] - y_min) / cell_h)
        c = max(0, min(grid_cols - 1, c))
        r = max(0, min(grid_rows - 1, r))
        grid.setdefault((r, c), []).append(i)

    # Filter top matches per cell
    selected_indices: List[int] = []
    for (r, c), idxs in grid.items():
        # Sort by confidence descending
        sorted_idxs = sorted(idxs, key=lambda idx: confidences[idx], reverse=True)
        selected_indices.extend(sorted_idxs[:max_matches_per_cell])

    selected_indices = sorted(list(set(selected_indices)))

    filt_src = src_pts[selected_indices]
    filt_ref = ref_pts[selected_indices]
    filt_conf = confidences[selected_indices]

    occupied_cells = len(grid)
    total_cells = grid_rows * grid_cols
    grid_occupancy_ratio = float(occupied_cells) / float(total_cells)

    hull_coverage = compute_convex_hull_coverage(filt_src, (int(h_extent), int(w_extent)))

    meets_threshold = grid_occupancy_ratio >= min_coverage_ratio
    if meets_threshold:
        diag = f"SUCCESS: Adequate spatial coverage ({grid_occupancy_ratio * 100.0:.1f}% grid occupancy across {occupied_cells}/{total_cells} cells)."
    else:
        diag = (
            f"REGISTRATION FLAGGED / REJECTED — insufficient spatial coverage "
            f"({grid_occupancy_ratio * 100.0:.1f}% occupied < {min_coverage_ratio * 100.0:.1f}% required). "
            f"Matches are clustered within only {occupied_cells} localized cells."
        )

    return SpatialDistributionResult(
        filtered_src_pts=filt_src,
        filtered_ref_pts=filt_ref,
        filtered_confidences=filt_conf,
        grid_rows=grid_rows,
        grid_cols=grid_cols,
        occupied_cells=occupied_cells,
        total_cells=total_cells,
        grid_occupancy_ratio=grid_occupancy_ratio,
        convex_hull_coverage_ratio=hull_coverage,
        meets_threshold=meets_threshold,
        diagnostic=diag,
    )
