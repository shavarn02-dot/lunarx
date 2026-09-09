import argparse
import sys
from pathlib import Path

# Ensure ISRO repository root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import cv2
import logging

from src.pipeline import run_registration_pipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("LunarRegCLI")


def main():
    parser = argparse.ArgumentParser(description="SIH26166 Chandrayaan-2 Lunar Image Registration Pipeline")
    parser.add_argument("--source", "-s", type=str, required=True, help="Path to source Chandrayaan-2 image (PDS4 XML/IMG, GeoTIFF, NPZ, PNG)")
    parser.add_argument("--reference", "-r", type=str, required=True, help="Path to reference Chandrayaan-2 image")
    parser.add_argument("--method", "-m", type=str, default="superpoint_lightglue", choices=["sift", "orb", "superpoint_lightglue", "loftr"], help="Feature matching algorithm")
    parser.add_argument("--preprocessing", "-p", type=str, default="clahe", choices=["raw", "clahe", "gradient", "phase_congruency"], help="Illumination preprocessing method")
    parser.add_argument("--model", type=str, default="affine", choices=["affine", "homography", "rigid"], help="Geometric transformation model")
    parser.add_argument("--estimator", type=str, default="USAC_MAGSAC", choices=["USAC_MAGSAC", "RANSAC"], help="Robust consensus estimator")
    parser.add_argument("--no-subpixel", action="store_true", help="Disable sub-pixel refinement stage")
    parser.add_argument("--no-spatial", action="store_true", help="Disable spatial coverage enforcement")
    parser.add_argument("--output-dir", "-o", type=str, default="data/outputs", help="Directory to save registered outputs and metrics")

    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    logger.info("================================================================================")
    logger.info("SIH26166: Chandrayaan-2 Lunar Image Registration System")
    logger.info(f"Source Image:    {args.source}")
    logger.info(f"Reference Image: {args.reference}")
    logger.info(f"Matcher:         {args.method}")
    logger.info(f"Preprocessing:   {args.preprocessing}")
    logger.info(f"Geometry Model:  {args.model}")
    logger.info(f"Robust Estimator:{args.estimator}")
    logger.info("================================================================================")

    output = run_registration_pipeline(
        source_path=args.source,
        reference_path=args.reference,
        method=args.method,
        preprocessing=args.preprocessing,
        model_type=args.model,
        robust_estimator=args.estimator,
        enforce_spatial_coverage=not args.no_spatial,
        subpixel_enabled=not args.no_subpixel,
    )

    report_dict = output.quality_report.to_dict()

    # Save artifacts
    src_stem = Path(args.source).stem
    ref_stem = Path(args.reference).stem
    prefix = f"{src_stem}_to_{ref_stem}_{args.method}"

    # Save registered warped image
    warped_path = out_dir / f"{prefix}_registered.png"
    cv2.imwrite(str(warped_path), output.warped_image)

    # Save match visualization
    matches_path = out_dir / f"{prefix}_matches.png"
    cv2.imwrite(str(matches_path), output.visualization_matches)

    # Save checkerboard
    checker_path = out_dir / f"{prefix}_checkerboard.png"
    cv2.imwrite(str(checker_path), output.visualization_checkerboard)

    # Save difference heatmap
    diff_path = out_dir / f"{prefix}_difference.png"
    cv2.imwrite(str(diff_path), output.visualization_difference)

    # Save metrics JSON
    json_path = out_dir / f"{prefix}_metrics.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_dict, f, indent=2)

    logger.info("--------------------------------------------------------------------------------")
    logger.info(f"STATUS:                 {report_dict['status']}")
    if report_dict.get('failure_reason'):
        logger.warning(f"DIAGNOSTIC:             {report_dict['failure_reason']}")
    logger.info(f"Raw Match Count:        {report_dict['raw_match_count']}")
    logger.info(f"Inlier Count:           {report_dict['inlier_match_count']}")
    logger.info(f"Inlier Ratio:           {report_dict['inlier_ratio_percent']}%")
    logger.info(f"Coarse Reproj RMSE:     {report_dict['reprojection_rmse_coarse_px']} px")
    logger.info(f"Refined Reproj RMSE:    {report_dict['reprojection_rmse_refined_px']} px")
    logger.info(f"Δ RMSE (Improvement):   {report_dict['delta_rmse_px']} px")
    logger.info(f"Spatial Coverage:       {report_dict['spatial_coverage_percent']}%")
    logger.info(f"Grid Occupancy:         {report_dict['grid_occupancy_percent']}% ({report_dict['occupied_cells']}/{report_dict['total_cells']} cells)")
    logger.info(f"Photometric NCC:        {report_dict['photometric_ncc']}")
    logger.info(f"Runtime:                {report_dict['runtime_sec']} seconds")
    logger.info("--------------------------------------------------------------------------------")
    logger.info(f"Saved Registered Image: {warped_path}")
    logger.info(f"Saved Match Plot:       {matches_path}")
    logger.info(f"Saved Metrics JSON:     {json_path}")
    logger.info("================================================================================")


if __name__ == "__main__":
    main()
