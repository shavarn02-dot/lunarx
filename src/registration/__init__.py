"""
Geometric registration, robust estimation, spatial filtering, and sub-pixel refinement package.
"""
from src.registration.geometry import validate_matrix_stability, warp_lunar_image, GeometricValidation
from src.registration.robust_estimation import (
    estimate_robust_transformation,
    compute_reprojection_rmse,
    RobustEstimationResult,
)
from src.registration.spatial_filter import (
    filter_spatial_correspondences,
    compute_convex_hull_coverage,
    SpatialDistributionResult,
)
from src.registration.subpixel import (
    refine_subpixel_correspondences,
    SubpixelRefinementResult,
)

__all__ = [
    "validate_matrix_stability",
    "warp_lunar_image",
    "GeometricValidation",
    "estimate_robust_transformation",
    "compute_reprojection_rmse",
    "RobustEstimationResult",
    "filter_spatial_correspondences",
    "compute_convex_hull_coverage",
    "SpatialDistributionResult",
    "refine_subpixel_correspondences",
    "SubpixelRefinementResult",
]
