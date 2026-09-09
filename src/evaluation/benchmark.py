"""
Automated Multi-Algorithm Benchmarking Engine.
SIH26166 Compliant — Real Data Evaluation Only.
"""
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import csv
import time
import logging

from src.data.ingestion import load_lunar_image, LunarImageRecord

logger = logging.getLogger(__name__)


def run_benchmark_on_pair(
    source_path: Path,
    reference_path: Path,
    methods: Optional[List[str]] = None,
    preprocess_methods: Optional[List[str]] = None,
    model_type: str = "affine"
) -> List[Dict[str, Any]]:
    """
    Execute benchmark on a single real Chandrayaan-2 image pair across multiple matchers.
    """
    methods = methods or ["sift", "orb", "superpoint_lightglue", "loftr"]
    preprocess_methods = preprocess_methods or ["clahe"]

    from src.pipeline import run_registration_pipeline

    rec_src = load_lunar_image(source_path)
    rec_ref = load_lunar_image(reference_path)

    results = []
    for m in methods:
        for p in preprocess_methods:
            logger.info(f"Benchmarking pair [{source_path.name} <-> {reference_path.name}] with method='{m}', prep='{p}'...")
            try:
                out = run_registration_pipeline(
                    source_path=rec_src,
                    reference_path=rec_ref,
                    method=m,
                    preprocessing=p,
                    model_type=model_type,
                    enforce_spatial_coverage=True,
                    subpixel_enabled=True,
                )
                rep = out.quality_report.to_dict()
                row = {
                    "source": source_path.name,
                    "reference": reference_path.name,
                    "method": m,
                    "preprocessing": p,
                    "status": rep["status"],
                    "raw_matches": rep["raw_match_count"],
                    "inliers": rep["inlier_match_count"],
                    "inlier_ratio_pct": rep["inlier_ratio_percent"],
                    "reproj_rmse_coarse": rep["reprojection_rmse_coarse_px"],
                    "reproj_rmse_refined": rep["reprojection_rmse_refined_px"],
                    "delta_rmse": rep["delta_rmse_px"],
                    "spatial_coverage_pct": rep["spatial_coverage_percent"],
                    "grid_occupancy_pct": rep["grid_occupancy_percent"],
                    "photometric_ncc": rep["photometric_ncc"],
                    "runtime_sec": rep["runtime_sec"],
                    "failure_reason": rep.get("failure_reason", ""),
                }
            except Exception as e:
                logger.error(f"Benchmark error on {m}+{p}: {e}")
                row = {
                    "source": source_path.name,
                    "reference": reference_path.name,
                    "method": m,
                    "preprocessing": p,
                    "status": "ERROR",
                    "raw_matches": 0,
                    "inliers": 0,
                    "inlier_ratio_pct": 0.0,
                    "reproj_rmse_coarse": None,
                    "reproj_rmse_refined": None,
                    "delta_rmse": 0.0,
                    "spatial_coverage_pct": 0.0,
                    "grid_occupancy_pct": 0.0,
                    "photometric_ncc": 0.0,
                    "runtime_sec": 0.0,
                    "failure_reason": str(e),
                }
            results.append(row)

    return results


def export_benchmark_results(
    results: List[Dict[str, Any]],
    output_dir: Path,
    filename_stem: str = "benchmark_results"
):
    """
    Save benchmark outputs to JSON, CSV, and Markdown.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # JSON export
    json_path = output_dir / f"{filename_stem}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # CSV export
    csv_path = output_dir / f"{filename_stem}.csv"
    if results:
        fieldnames = list(results[0].keys())
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    # Markdown table export
    md_path = output_dir / f"{filename_stem}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Real Chandrayaan-2 Registration Benchmark\n\n")
        f.write("| Method | Prep | Status | Raw | Inliers | Inlier % | RMSE Coarse (px) | RMSE Refined (px) | Δ RMSE | Spatial Coverage % | Runtime (s) |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for r in results:
            rmse_c = f"{r['reproj_rmse_coarse']:.3f}" if r['reproj_rmse_coarse'] is not None else "N/A"
            rmse_r = f"{r['reproj_rmse_refined']:.3f}" if r['reproj_rmse_refined'] is not None else "N/A"
            f.write(
                f"| **{r['method']}** | {r['preprocessing']} | {r['status']} | "
                f"{r['raw_matches']} | {r['inliers']} | {r['inlier_ratio_pct']:.1f}% | "
                f"{rmse_c} | {rmse_r} | {r['delta_rmse']:+.3f} | "
                f"{r['spatial_coverage_pct']:.1f}% | {r['runtime_sec']:.2f}s |\n"
            )

    logger.info(f"Exported benchmark reports to {output_dir.resolve()}")
