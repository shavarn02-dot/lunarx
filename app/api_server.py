"""
FastAPI Mission Control Backend for Chandrayaan-2 Lunar Image Registration.
SIH26166 Compliant - Direct integration with real PyTorch / OpenCV registration pipeline.
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from pathlib import Path
import shutil
import time
import json
import cv2
import numpy as np
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ISRO_API")

# Setup project paths
BASE_DIR = Path(__file__).resolve().parent.parent
PUBLIC_IMG_DIR = BASE_DIR / "lunar-x" / "public" / "images"
PUBLIC_IMG_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR = BASE_DIR / "data" / "upload_samples"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR = BASE_DIR / "data" / "outputs"

from src.pipeline import run_registration_pipeline
from src.evaluation.benchmark import run_benchmark_on_pair

app = FastAPI(
    title="ISRO Chandrayaan-2 Registration API",
    description="SIH26166 Planetary Image Registration Engine",
    version="2.0.0"
)

# Enable CORS for Next.js development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static images directory for direct image serving fallback
app.mount("/images", StaticFiles(directory=str(PUBLIC_IMG_DIR)), name="images")

# Preset Crater Pairs
PRESET_PAIRS = [
    {
        "id": "default_tmc",
        "name": "Default TMC Crater Scene (Shackleton Vicinity)",
        "source_img": "ch2_tmc_crater_scene_src.png",
        "reference_img": "ch2_tmc_crater_scene_ref.png",
        "resolution": "0.5 m/px",
        "orbit": "Orbit 3922 vs 3943",
        "illumination": "High solar incidence angle (terminator shadows)",
        "sensor": "TMC-2 (Terrain Mapping Camera)",
        "description": "Standard benchmark lunar crater scene with severe shadow asymmetry and 180° lighting reversal."
    },
    {
        "id": "region_alpha",
        "name": "Crater Region Alpha (High-Contrast Rim)",
        "source_img": "Pair_Crater_Region_Alpha_SRC.png",
        "reference_img": "Pair_Crater_Region_Alpha_REF.png",
        "resolution": "0.5 m/px",
        "orbit": "Orbit 3922 (Strip Segment A)",
        "illumination": "Sharp crater crest highlights with dark floor shadow",
        "sensor": "TMC-2",
        "description": "Prominent circular impact rim with secondary ejecta field."
    },
    {
        "id": "region_beta",
        "name": "Crater Region Beta (Terminator Shadow Slope)",
        "source_img": "Pair_Crater_Region_Beta_SRC.png",
        "reference_img": "Pair_Crater_Region_Beta_REF.png",
        "resolution": "0.5 m/px",
        "orbit": "Orbit 3943 (Strip Segment B)",
        "illumination": "Steep lunar slope with deep shadow transition",
        "sensor": "TMC-2",
        "description": "Challenging terrain with steep crater walls and extensive shadowed slopes."
    },
    {
        "id": "region_gamma",
        "name": "Crater Region Gamma (Central Peak Feature)",
        "source_img": "Pair_Crater_Region_Gamma_SRC.png",
        "reference_img": "Pair_Crater_Region_Gamma_REF.png",
        "resolution": "0.5 m/px",
        "orbit": "Orbit 3922 (Strip Segment C)",
        "illumination": "Central peak illumination with floor micro-craters",
        "sensor": "TMC-2",
        "description": "Complex crater morphology with prominent central uplift peak."
    },
    {
        "id": "region_delta",
        "name": "Crater Region Delta (Multi-Crater Cluster)",
        "source_img": "Pair_Crater_Region_Delta_SRC.png",
        "reference_img": "Pair_Crater_Region_Delta_REF.png",
        "resolution": "0.5 m/px",
        "orbit": "Orbit 3943 (Strip Segment D)",
        "illumination": "Dense overlapping craterlets and regolith textures",
        "sensor": "TMC-2",
        "description": "Cluster of multiple degraded craters testing spatial feature distribution."
    }
]

@app.get("/api/health")
def get_health():
    import torch
    cuda_available = torch.cuda.is_available()
    device_name = torch.cuda.get_device_name(0) if cuda_available else "CPU (Optimized SIMD)"
    return {
        "status": "ONLINE",
        "service": "ISRO Chandrayaan-2 Registration Engine (SIH26166)",
        "device": device_name,
        "cuda_active": cuda_available,
        "supported_matchers": ["sift", "orb", "superpoint_lightglue", "loftr"],
        "supported_preprocessing": ["clahe", "gradient", "raw"],
        "supported_models": ["affine", "homography", "rigid"],
        "timestamp": time.time()
    }

@app.get("/api/pairs")
def get_preset_pairs():
    return PRESET_PAIRS

@app.get("/api/benchmark")
def get_benchmark_results():
    bench_file = OUTPUTS_DIR / "benchmark_results.json"
    if bench_file.exists():
        with open(bench_file, "r") as f:
            return json.load(f)
    return []

class RegistrationRequest(BaseModel):
    source_filename: str
    reference_filename: str
    method: str = "loftr"
    preprocessing: str = "clahe"
    model_type: str = "affine"
    subpixel: bool = True
    spatial_filter: bool = True
    reproj_thresh: float = 3.0

@app.post("/api/register")
def run_registration(req: RegistrationRequest):
    t_start = time.perf_counter()
    logs: List[str] = []

    # Map method name
    method_key = req.method.lower().replace("+", "_").replace(" ", "_")
    if "superpoint" in method_key:
        method_key = "superpoint_lightglue"

    # Resolve image paths (check public/images, upload_samples, and data/raw)
    src_path = None
    ref_path = None
    candidates = [PUBLIC_IMG_DIR, UPLOAD_DIR, BASE_DIR / "data" / "raw"]

    for d in candidates:
        if (d / req.source_filename).exists() and src_path is None:
            src_path = d / req.source_filename
        if (d / req.reference_filename).exists() and ref_path is None:
            ref_path = d / req.reference_filename

    if not src_path or not ref_path:
        raise HTTPException(
            status_code=404,
            detail=f"Images not found: {req.source_filename} or {req.reference_filename}"
        )

    logs.append(f"[INGEST] Ingested Source Image: {req.source_filename}")
    logs.append(f"[INGEST] Ingested Reference Image: {req.reference_filename}")
    logs.append(f"[PREPROCESS] Executing {req.preprocessing.upper()} shadow enhancement pipeline...")
    logs.append(f"[MATCHER] Initializing {req.method.upper()} feature matching engine...")

    try:
        # Run real python registration pipeline
        pipeline_res = run_registration_pipeline(
            source_path=src_path,
            reference_path=ref_path,
            method=method_key,
            preprocessing=req.preprocessing,
            model_type=req.model_type,
            robust_estimator="USAC_MAGSAC",
            enforce_spatial_coverage=req.spatial_filter,
            subpixel_enabled=req.subpixel,
            reproj_thresh=req.reproj_thresh
        )

        inlier_pct = pipeline_res.robust_result.inlier_ratio * 100.0
        logs.append(f"[MAGSAC++] Robust estimation completed in {pipeline_res.robust_result.inlier_count} inliers ({inlier_pct:.1f}%)")
        if pipeline_res.subpixel_result:
            logs.append(f"[SUBPIXEL] CornerSubPix gradient snapped. Refined RMSE = {pipeline_res.subpixel_result.rmse_refined:.4f} px")
        logs.append(f"[MOSAIC] Seamless warped alignment composite generated successfully.")

        # Save output visualizations into public/images so Next.js renders them instantly
        ts = int(time.time())
        stem = f"run_{ts}_{method_key}_{req.preprocessing}"
        
        matches_file = f"{stem}_matches.png"
        registered_file = f"{stem}_registered.png"
        checkerboard_file = f"{stem}_checkerboard.png"
        difference_file = f"{stem}_difference.png"

        cv2.imwrite(str(PUBLIC_IMG_DIR / matches_file), pipeline_res.visualization_matches)
        cv2.imwrite(str(PUBLIC_IMG_DIR / registered_file), pipeline_res.warped_image)
        cv2.imwrite(str(PUBLIC_IMG_DIR / checkerboard_file), pipeline_res.visualization_checkerboard)
        cv2.imwrite(str(PUBLIC_IMG_DIR / difference_file), pipeline_res.visualization_difference)

        coarse_rmse = pipeline_res.robust_result.reproj_rmse
        if pipeline_res.subpixel_result and pipeline_res.subpixel_result.improved:
            refined_rmse = pipeline_res.subpixel_result.rmse_refined
        else:
            refined_rmse = coarse_rmse

        return {
            "success": pipeline_res.success,
            "runtime_sec": round(pipeline_res.total_runtime_sec, 3),
            "metrics": {
                "inliers": pipeline_res.robust_result.inlier_count,
                "raw_matches": pipeline_res.match_result.count,
                "inlier_ratio_pct": round(inlier_pct, 2),
                "reproj_rmse_coarse": round(coarse_rmse, 4),
                "reproj_rmse_refined": round(refined_rmse, 4),
                "spatial_coverage_pct": round(pipeline_res.spatial_result.convex_hull_coverage_ratio * 100.0, 2),
                "grid_occupancy_pct": round(pipeline_res.spatial_result.grid_occupancy_ratio * 100.0, 1),
                "photometric_ncc": round(pipeline_res.quality_report.photometric_ncc, 4),
                "status": pipeline_res.quality_report.status
            },
            "images": {
                "matches": matches_file,
                "registered": registered_file,
                "checkerboard": checkerboard_file,
                "difference": difference_file
            },
            "transformation_matrix": pipeline_res.robust_result.matrix.tolist() if pipeline_res.robust_result.matrix is not None else None,
            "logs": logs
        }

    except Exception as e:
        logger.exception("Pipeline execution failed")
        return {
            "success": False,
            "runtime_sec": round(time.perf_counter() - t_start, 3),
            "error": str(e),
            "logs": logs + [f"[ERROR] Pipeline terminated with error: {str(e)}"]
        }

@app.post("/api/upload")
async def upload_custom_image(file: UploadFile = File(...)):
    filename = file.filename
    dest_public = PUBLIC_IMG_DIR / filename
    dest_samples = UPLOAD_DIR / filename
    
    with open(dest_public, "wb") as f:
        shutil.copyfileobj(file.file, f)
    shutil.copy(dest_public, dest_samples)

    return {
        "filename": filename,
        "size": dest_public.stat().st_size,
        "url": f"/images/{filename}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
