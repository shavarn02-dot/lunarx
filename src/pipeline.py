"""
Master End-to-End Registration Pipeline.
SIH26166 Compliant.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any, Union, Tuple
import time
import numpy as np
import cv2
import logging

from src.data.ingestion import load_lunar_image, LunarImageRecord, DataProvenance
from src.data.preprocessing import preprocess_image
from src.matching import get_matcher, MatchResult
from src.registration import (
    estimate_robust_transformation,
    filter_spatial_correspondences,
    refine_subpixel_correspondences,
    warp_lunar_image,
    RobustEstimationResult,
    SpatialDistributionResult,
    SubpixelRefinementResult,
)
from src.evaluation.metrics import (
    RegistrationQualityReport,
    compute_photometric_consistency,
)
from src.visualization import (
    draw_correspondences,
    draw_spatial_grid_overlay,
    create_checkerboard_overlay,
    create_difference_heatmap,
    create_split_slider_composite,
)

logger = logging.getLogger(__name__)


@dataclass
class PipelineOutput:
    source_record: LunarImageRecord
    reference_record: LunarImageRecord
    preprocessed_source: np.ndarray
    preprocessed_reference: np.ndarray
    match_result: MatchResult
    robust_result: RobustEstimationResult
    spatial_result: SpatialDistributionResult
    subpixel_result: Optional[SubpixelRefinementResult]
    warped_image: np.ndarray
    quality_report: RegistrationQualityReport
    visualization_matches: np.ndarray
    visualization_grid: np.ndarray
    visualization_checkerboard: np.ndarray
    visualization_difference: np.ndarray
    success: bool
    total_runtime_sec: float


def run_registration_pipeline(
    source_path: Union[str, Path, LunarImageRecord],
    reference_path: Union[str, Path, LunarImageRecord],
    method: str = "superpoint_lightglue",
    preprocessing: str = "clahe",
    model_type: str = "affine",
    robust_estimator: str = "USAC_MAGSAC",
    enforce_spatial_coverage: bool = True,
    grid_rows: int = 8,
    grid_cols: int = 8,
    min_coverage_ratio: float = 0.15,
    subpixel_enabled: bool = True,
    subpixel_method: str = "corner_subpix",
    reproj_thresh: float = 3.0,
    config: Optional[Dict[str, Any]] = None
) -> PipelineOutput:
    """
    Execute full SIH26166 registration workflow.
    Strictly un-simulated, operating exclusively on supplied inputs.
    """
    t_start = time.perf_counter()

    # Step 1: Load and Validate Provenance
    if isinstance(source_path, LunarImageRecord):
        rec_src = source_path
    else:
        rec_src = load_lunar_image(source_path)

    if isinstance(reference_path, LunarImageRecord):
        rec_ref = reference_path
    else:
        rec_ref = load_lunar_image(reference_path)

    # Step 2: Preprocessing
    src_pre = preprocess_image(rec_src.image_uint8, method=preprocessing)
    ref_pre = preprocess_image(rec_ref.image_uint8, method=preprocessing)

    # Step 3: Feature Matching
    matcher = get_matcher(method)
    match_res = matcher.match(src_pre, ref_pre)

    # If matching failed to find minimum points
    if not match_res.success or match_res.count < 4:
        total_time = time.perf_counter() - t_start
        empty_spatial = filter_spatial_correspondences(
            np.empty((0, 2), dtype=np.float32), np.empty((0, 2), dtype=np.float32)
        )
        empty_robust = estimate_robust_transformation(
            np.empty((0, 2), dtype=np.float32), np.empty((0, 2), dtype=np.float32), model_type=model_type
        )
        report = RegistrationQualityReport(
            raw_match_count=match_res.num_raw_matches,
            inlier_match_count=0,
            inlier_ratio=0.0,
            reprojection_rmse_coarse=float("inf"),
            reprojection_rmse_refined=float("inf"),
            delta_rmse=0.0,
            subpixel_improved=False,
            spatial_coverage_percent=0.0,
            grid_occupancy_percent=0.0,
            occupied_cells=0,
            total_cells=grid_rows * grid_cols,
            photometric_ncc=0.0,
            photometric_rmse=float("inf"),
            runtime_sec=total_time,
            model_type=model_type,
            condition_number=float("inf"),
            is_stable=False,
            status="FAILED",
            failure_reason=(
                f"REGISTRATION FAILED — {match_res.error_message}"
                if match_res.error_message
                else "REGISTRATION FAILED — insufficient reliable correspondences."
            ),
        )
        empty_vis = draw_correspondences(rec_src.image_uint8, rec_ref.image_uint8, np.empty((0, 2)), np.empty((0, 2)))
        return PipelineOutput(
            source_record=rec_src, reference_record=rec_ref,
            preprocessed_source=src_pre, preprocessed_reference=ref_pre,
            match_result=match_res, robust_result=empty_robust,
            spatial_result=empty_spatial, subpixel_result=None,
            warped_image=np.zeros_like(rec_ref.image_uint8),
            quality_report=report,
            visualization_matches=empty_vis,
            visualization_grid=rec_src.image_uint8,
            visualization_checkerboard=rec_ref.image_uint8,
            visualization_difference=rec_ref.image_uint8,
            success=False, total_runtime_sec=total_time,
        )

    # Step 4: Robust Estimation & Outlier Rejection
    robust_res = estimate_robust_transformation(
        match_res.keypoints_src, match_res.keypoints_ref,
        model_type=model_type, method=robust_estimator, reproj_thresh=reproj_thresh
    )

    if not robust_res.success:
        total_time = time.perf_counter() - t_start
        empty_spatial = filter_spatial_correspondences(
            np.empty((0, 2), dtype=np.float32), np.empty((0, 2), dtype=np.float32)
        )
        report = RegistrationQualityReport(
            raw_match_count=match_res.num_raw_matches,
            inlier_match_count=robust_res.inlier_count,
            inlier_ratio=robust_res.inlier_ratio,
            reprojection_rmse_coarse=float("inf"),
            reprojection_rmse_refined=float("inf"),
            delta_rmse=0.0,
            subpixel_improved=False,
            spatial_coverage_percent=0.0,
            grid_occupancy_percent=0.0,
            occupied_cells=0,
            total_cells=grid_rows * grid_cols,
            photometric_ncc=0.0,
            photometric_rmse=float("inf"),
            runtime_sec=total_time,
            model_type=model_type,
            condition_number=robust_res.validation.condition_number,
            is_stable=robust_res.validation.is_valid,
            status="FAILED",
            failure_reason=robust_res.diagnostic,
        )
        vis_matches = draw_correspondences(
            rec_src.image_uint8, rec_ref.image_uint8,
            match_res.keypoints_src, match_res.keypoints_ref,
            inlier_mask=robust_res.inlier_mask
        )
        return PipelineOutput(
            source_record=rec_src, reference_record=rec_ref,
            preprocessed_source=src_pre, preprocessed_reference=ref_pre,
            match_result=match_res, robust_result=robust_res,
            spatial_result=empty_spatial, subpixel_result=None,
            warped_image=np.zeros_like(rec_ref.image_uint8),
            quality_report=report,
            visualization_matches=vis_matches,
            visualization_grid=rec_src.image_uint8,
            visualization_checkerboard=rec_ref.image_uint8,
            visualization_difference=rec_ref.image_uint8,
            success=False, total_runtime_sec=total_time,
        )

    # Step 5: Spatial Distribution & Coverage Enforcement
    src_inliers = match_res.keypoints_src[robust_res.inlier_mask]
    ref_inliers = match_res.keypoints_ref[robust_res.inlier_mask]
    conf_inliers = match_res.confidence[robust_res.inlier_mask]

    spatial_res = filter_spatial_correspondences(
        src_inliers, ref_inliers, confidences=conf_inliers,
        image_shape=rec_src.image_uint8.shape[:2],
        grid_rows=grid_rows, grid_cols=grid_cols,
        min_coverage_ratio=min_coverage_ratio,
        enforce_coverage=enforce_spatial_coverage
    )

    if enforce_spatial_coverage and not spatial_res.meets_threshold:
        total_time = time.perf_counter() - t_start
        report = RegistrationQualityReport(
            raw_match_count=match_res.num_raw_matches,
            inlier_match_count=robust_res.inlier_count,
            inlier_ratio=robust_res.inlier_ratio,
            reprojection_rmse_coarse=robust_res.reproj_rmse,
            reprojection_rmse_refined=robust_res.reproj_rmse,
            delta_rmse=0.0,
            subpixel_improved=False,
            spatial_coverage_percent=spatial_res.convex_hull_coverage_ratio * 100.0,
            grid_occupancy_percent=spatial_res.grid_occupancy_ratio * 100.0,
            occupied_cells=spatial_res.occupied_cells,
            total_cells=spatial_res.total_cells,
            photometric_ncc=0.0,
            photometric_rmse=float("inf"),
            runtime_sec=total_time,
            model_type=model_type,
            condition_number=robust_res.validation.condition_number,
            is_stable=robust_res.validation.is_valid,
            status="FAILED",
            failure_reason=spatial_res.diagnostic,
        )
        vis_matches = draw_correspondences(
            rec_src.image_uint8, rec_ref.image_uint8,
            match_res.keypoints_src, match_res.keypoints_ref,
            inlier_mask=robust_res.inlier_mask
        )
        vis_grid = draw_spatial_grid_overlay(
            rec_src.image_uint8, src_inliers, grid_rows=grid_rows, grid_cols=grid_cols
        )
        return PipelineOutput(
            source_record=rec_src, reference_record=rec_ref,
            preprocessed_source=src_pre, preprocessed_reference=ref_pre,
            match_result=match_res, robust_result=robust_res,
            spatial_result=spatial_res, subpixel_result=None,
            warped_image=np.zeros_like(rec_ref.image_uint8),
            quality_report=report,
            visualization_matches=vis_matches,
            visualization_grid=vis_grid,
            visualization_checkerboard=rec_ref.image_uint8,
            visualization_difference=rec_ref.image_uint8,
            success=False, total_runtime_sec=total_time,
        )

    # Step 6: Sub-Pixel Refinement
    final_matrix = robust_res.matrix
    subpixel_res = None
    rmse_refined = robust_res.reproj_rmse
    delta_rmse = 0.0
    subpixel_improved = False

    if subpixel_enabled and robust_res.matrix is not None:
        subpixel_res = refine_subpixel_correspondences(
            src_pre, ref_pre,
            src_inliers, ref_inliers,
            initial_matrix=robust_res.matrix,
            model_type=model_type,
            method=subpixel_method
        )
        if subpixel_res.improved:
            final_matrix = subpixel_res.refined_matrix
        else:
            final_matrix = robust_res.matrix
        rmse_refined = subpixel_res.rmse_refined
        delta_rmse = subpixel_res.delta_rmse
        subpixel_improved = subpixel_res.improved

    # Step 7: Warp Source Image into Reference Frame
    warped_img = warp_lunar_image(
        rec_src.image_uint8, final_matrix,
        target_shape=rec_ref.image_uint8.shape[:2],
        model_type=model_type
    )

    # Step 8: Photometric Consistency on Warped Overlap
    ncc, p_rmse = compute_photometric_consistency(warped_img, rec_ref.image_uint8)

    total_time = time.perf_counter() - t_start

    # Step 9: Build Quality Report
    report = RegistrationQualityReport(
        raw_match_count=match_res.num_raw_matches,
        inlier_match_count=robust_res.inlier_count,
        inlier_ratio=robust_res.inlier_ratio,
        reprojection_rmse_coarse=robust_res.reproj_rmse,
        reprojection_rmse_refined=rmse_refined,
        delta_rmse=delta_rmse,
        subpixel_improved=subpixel_improved,
        spatial_coverage_percent=spatial_res.convex_hull_coverage_ratio * 100.0,
        grid_occupancy_percent=spatial_res.grid_occupancy_ratio * 100.0,
        occupied_cells=spatial_res.occupied_cells,
        total_cells=spatial_res.total_cells,
        photometric_ncc=ncc,
        photometric_rmse=p_rmse,
        runtime_sec=total_time,
        model_type=model_type,
        condition_number=robust_res.validation.condition_number,
        is_stable=robust_res.validation.is_valid,
        status="SUCCESS",
        failure_reason="",
    )

    # Step 10: Visualizations
    vis_matches = draw_correspondences(
        rec_src.image_uint8, rec_ref.image_uint8,
        match_res.keypoints_src, match_res.keypoints_ref,
        inlier_mask=robust_res.inlier_mask
    )
    vis_grid = draw_spatial_grid_overlay(
        rec_src.image_uint8, src_inliers, grid_rows=grid_rows, grid_cols=grid_cols
    )
    vis_checker = create_checkerboard_overlay(rec_ref.image_uint8, warped_img)
    vis_diff = create_difference_heatmap(rec_ref.image_uint8, warped_img)

    return PipelineOutput(
        source_record=rec_src,
        reference_record=rec_ref,
        preprocessed_source=src_pre,
        preprocessed_reference=ref_pre,
        match_result=match_res,
        robust_result=robust_res,
        spatial_result=spatial_res,
        subpixel_result=subpixel_res,
        warped_image=warped_img,
        quality_report=report,
        visualization_matches=vis_matches,
        visualization_grid=vis_grid,
        visualization_checkerboard=vis_checker,
        visualization_difference=vis_diff,
        success=True,
        total_runtime_sec=total_time,
    )
