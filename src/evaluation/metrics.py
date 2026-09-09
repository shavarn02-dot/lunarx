"""
Quantitative Quality & Evaluation Engine.
SIH26166 Compliant.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Tuple
import numpy as np
import cv2
import logging

logger = logging.getLogger(__name__)


@dataclass
class RegistrationQualityReport:
    raw_match_count: int
    inlier_match_count: int
    inlier_ratio: float
    reprojection_rmse_coarse: float
    reprojection_rmse_refined: float
    delta_rmse: float
    subpixel_improved: bool
    spatial_coverage_percent: float
    grid_occupancy_percent: float
    occupied_cells: int
    total_cells: int
    photometric_ncc: float
    photometric_rmse: float
    runtime_sec: float
    model_type: str
    condition_number: float
    is_stable: bool
    status: str
    failure_reason: str = ""
    ground_truth_available: bool = False
    ground_truth_rmse: Optional[float] = None
    error_type_label: str = "Mathematical Reprojection Residual"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "failure_reason": self.failure_reason,
            "raw_match_count": self.raw_match_count,
            "inlier_match_count": self.inlier_match_count,
            "inlier_ratio_percent": round(self.inlier_ratio * 100.0, 2),
            "reprojection_rmse_coarse_px": round(self.reprojection_rmse_coarse, 4) if self.reprojection_rmse_coarse != float("inf") else None,
            "reprojection_rmse_refined_px": round(self.reprojection_rmse_refined, 4) if self.reprojection_rmse_refined != float("inf") else None,
            "delta_rmse_px": round(self.delta_rmse, 4),
            "subpixel_improved": self.subpixel_improved,
            "spatial_coverage_percent": round(self.spatial_coverage_percent, 2),
            "grid_occupancy_percent": round(self.grid_occupancy_percent, 2),
            "occupied_cells": self.occupied_cells,
            "total_cells": self.total_cells,
            "photometric_ncc": round(self.photometric_ncc, 4),
            "photometric_rmse": round(self.photometric_rmse, 4),
            "runtime_sec": round(self.runtime_sec, 4),
            "model_type": self.model_type,
            "matrix_condition_number": self.condition_number,
            "is_matrix_stable": self.is_stable,
            "ground_truth_available": self.ground_truth_available,
            "ground_truth_rmse": self.ground_truth_rmse,
            "error_metric_definition": self.error_type_label,
        }


def compute_photometric_consistency(
    warped_img_u8: np.ndarray,
    ref_img_u8: np.ndarray
) -> Tuple[float, float]:
    """
    Compute Normalized Cross-Correlation (NCC) and intensity RMSE on the
    mutually overlapping non-black pixels of registered images.
    """
    # Overlap mask: pixels where warped image is non-zero
    mask = (warped_img_u8 > 0) & (ref_img_u8 > 0)
    if np.sum(mask) < 100:
        return 0.0, float("inf")

    v1 = warped_img_u8[mask].astype(np.float64)
    v2 = ref_img_u8[mask].astype(np.float64)

    # Photometric RMSE
    rmse = float(np.sqrt(np.mean((v1 - v2) ** 2)))

    # Normalized Cross Correlation
    mean1 = np.mean(v1)
    mean2 = np.mean(v2)
    std1 = np.std(v1)
    std2 = np.std(v2)

    if std1 > 1e-6 and std2 > 1e-6:
        ncc = float(np.mean((v1 - mean1) * (v2 - mean2)) / (std1 * std2))
    else:
        ncc = 0.0

    return round(ncc, 4), round(rmse, 2)
