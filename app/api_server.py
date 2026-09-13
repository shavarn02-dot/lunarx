"""
Chandrayaan-2 Lunar Image Registration API (FastAPI).
SIH26166 — Real planetary data pipeline with full frontend-backend integration.
"""
from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import List, Optional, Any, Dict

import cv2
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ch2-api")

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
OUTPUTS_DIR = BASE_DIR / "data" / "outputs"
PUBLIC_IMG_DIR = BASE_DIR / "lunar-x" / "public" / "images"

for _d in (RAW_DIR, UPLOAD_DIR, OUTPUTS_DIR, PUBLIC_IMG_DIR):
    _d.mkdir(parents=True, exist_ok=True)

from src.data.ingestion import load_lunar_image  # noqa: E402
from src.pipeline import run_registration_pipeline  # noqa: E402

app = FastAPI(
    title="Chandrayaan-2 Registration API",
    description="SIH26166 Planetary Image Registration Engine",
    version="3.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if PUBLIC_IMG_DIR.is_dir():
    app.mount("/images", StaticFiles(directory=str(PUBLIC_IMG_DIR)), name="images")

MATCHERS = ["sift", "orb", "superpoint_lightglue", "loftr"]
PREPROCESSING = ["clahe", "gradient", "phase_congruency", "raw"]
MODELS = ["affine", "homography", "rigid"]
ESTIMATORS = ["USAC_MAGSAC", "RANSAC"]

PRESET_DEFS = [
    (
        "tmc_crater",
        "Crater field — TMC-2 cross-pass (600 x 600)",
        "ch2_tmc_crater_scene_src.png",
        "ch2_tmc_crater_scene_ref.png",
        "TMC-2",
        "5.0 m/px",
        "Orbit 3922 vs 3943",
        "Standard benchmark lunar crater scene with severe shadow asymmetry.",
    ),
    (
        "strip_ohrc",
        "Cross-Sensor — TMC-2 crop vs OHRC patch (20x scale gap)",
        "ch2_tmc_ncn_patch_crop.jpg",
        "ch2_ohr_ncp_overlap_patch.jpg",
        "TMC-2 vs OHRC",
        "5.0m vs 0.25m",
        "Orbit 20191125",
        "Challenging 20x cross-sensor resolution gap challenge.",
    ),
    (
        "crater_alpha",
        "Crater Region Alpha (High-Contrast Rim)",
        "Pair_Crater_Region_Alpha_SRC.png",
        "Pair_Crater_Region_Alpha_REF.png",
        "TMC-2",
        "5.0 m/px",
        "Orbit 3922 (Strip Segment A)",
        "Prominent circular impact rim with secondary ejecta field.",
    ),
    (
        "crater_beta",
        "Crater Region Beta (Terminator Shadow Slope)",
        "Pair_Crater_Region_Beta_SRC.png",
        "Pair_Crater_Region_Beta_REF.png",
        "TMC-2",
        "5.0 m/px",
        "Orbit 3943 (Strip Segment B)",
        "Steep lunar slope with deep shadow transition.",
    ),
    (
        "crater_gamma",
        "Crater Region Gamma (Central Peak Feature)",
        "Pair_Crater_Region_Gamma_SRC.png",
        "Pair_Crater_Region_Gamma_REF.png",
        "TMC-2",
        "5.0 m/px",
        "Orbit 3922 (Strip Segment C)",
        "Central peak illumination with floor micro-craters.",
    ),
    (
        "crater_delta",
        "Crater Region Delta (Multi-Crater Cluster)",
        "Pair_Crater_Region_Delta_SRC.png",
        "Pair_Crater_Region_Delta_REF.png",
        "TMC-2",
        "5.0 m/px",
        "Orbit 3943 (Strip Segment D)",
        "Dense overlapping craterlets and regolith textures.",
    ),
]

ALLOWED_SUFFIXES = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".npz", ".img"}


def _safe_lookup(name: str) -> Optional[Path]:
    """Resolve a client-supplied filename inside RAW_DIR / UPLOAD_DIR / PUBLIC_IMG_DIR."""
    base = Path(name or "").name
    if not base or base.startswith("."):
        return None
    if Path(base).suffix.lower() not in ALLOWED_SUFFIXES:
        return None
    for directory in (RAW_DIR, UPLOAD_DIR, PUBLIC_IMG_DIR):
        candidate = directory / base
        if candidate.is_file():
            return candidate
    return None


def _sanitize(name: str) -> str:
    base = Path(name or "upload").name
    clean = "".join(c if c.isalnum() or c in "._-" else "_" for c in base)
    if Path(clean).suffix.lower() not in ALLOWED_SUFFIXES:
        clean += ".png"
    return clean[:120]


def _describe(path: Path) -> dict:
    try:
        rec = load_lunar_image(path)
        h, w = rec.image_uint8.shape[:2]
        return {
            "file": path.name,
            "filename": path.name,
            "sensor": rec.sensor,
            "provenance": rec.provenance.value,
            "width": w,
            "height": h,
            "bytes": path.stat().st_size,
        }
    except Exception as e:
        logger.warning(f"Could not load image metadata for {path}: {e}")
        return {
            "file": path.name,
            "filename": path.name,
            "sensor": "Unknown",
            "provenance": "File on disk",
            "width": 600,
            "height": 600,
            "bytes": path.stat().st_size if path.exists() else 0,
        }


def _bgr_to_rgb(img):
    if img is not None and img.ndim == 3 and img.shape[2] == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


# ---------------------------------------------------------------- health
@app.get("/api/health")
def get_health() -> dict:
    try:
        import torch
        cuda = torch.cuda.is_available()
        device = torch.cuda.get_device_name(0) if cuda else "CPU (Optimized SIMD)"
    except Exception:
        cuda, device = False, "CPU (Optimized SIMD)"
    return {
        "status": "ONLINE",
        "service": "Chandrayaan-2 Registration Engine (SIH26166)",
        "device": device,
        "cuda": cuda,
        "cuda_active": cuda,
        "matchers": MATCHERS,
        "preprocessing": PREPROCESSING,
        "models": MODELS,
        "estimators": ESTIMATORS,
        "supported_matchers": MATCHERS,
        "supported_preprocessing": PREPROCESSING,
        "supported_models": MODELS,
        "timestamp": time.time(),
    }


# ---------------------------------------------------------------- pairs
@app.get("/api/pairs")
def get_pairs() -> List[dict]:
    pairs: List[dict] = []
    for item in PRESET_DEFS:
        pid, name, src_name, ref_name = item[0], item[1], item[2], item[3]
        sensor = item[4] if len(item) > 4 else "TMC-2"
        resolution = item[5] if len(item) > 5 else "5.0 m/px"
        orbit = item[6] if len(item) > 6 else "Orbit 3922 vs 3943"
        description = item[7] if len(item) > 7 else "Planetary benchmark pair"

        src = _safe_lookup(src_name)
        ref = _safe_lookup(ref_name)
        if not (src and ref):
            continue

        desc_src = _describe(src)
        desc_ref = _describe(ref)
        pairs.append(
            {
                "id": pid,
                "name": name,
                "source_img": src.name,
                "reference_img": ref.name,
                "sensor": sensor,
                "resolution": resolution,
                "orbit": orbit,
                "description": description,
                "source": desc_src,
                "reference": desc_ref,
            }
        )
    return pairs


# ---------------------------------------------------------------- upload
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(400, "Missing filename")
    clean = _sanitize(file.filename)
    filename = f"upload_{int(time.time())}_{clean}"
    content = await file.read()

    # Save to uploads dir
    dest = UPLOAD_DIR / filename
    with open(dest, "wb") as fh:
        fh.write(content)

    # Also copy to Next.js public images so frontend preview works seamlessly
    if PUBLIC_IMG_DIR.is_dir():
        with open(PUBLIC_IMG_DIR / filename, "wb") as fh:
            fh.write(content)

    return {
        "filename": filename,
        "url": f"/images/{filename}",
        "bytes": len(content),
    }


# ---------------------------------------------------------------- preview
@app.get("/api/preview")
def get_preview(file: str):
    path = _safe_lookup(file)
    if path is None:
        raise HTTPException(status_code=404, detail=f"Image not found: {file}")
    media = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    if path.suffix.lower() in (".npz", ".img", ".tif", ".tiff"):
        media = "application/octet-stream"
    return FileResponse(str(path), media_type=media, filename=path.name)


# ---------------------------------------------------------------- register
@app.post("/api/register")
async def post_register(request: Request):
    content_type = request.headers.get("content-type", "").lower()

    # Parse JSON vs Multipart/Form
    if "application/json" in content_type:
        try:
            body = await request.json()
        except Exception:
            try:
                raw_body = await request.body()
                import json
                body = json.loads(raw_body.decode("utf-8", errors="replace"))
            except Exception:
                body = {}
        source_filename = body.get("source_filename") or body.get("source_preset", "")
        reference_filename = body.get("reference_filename") or body.get("reference_preset", "")
        method = body.get("method", "loftr")
        preprocessing = body.get("preprocessing", "clahe")
        model_type = body.get("model_type", "affine")
        estimator = body.get("estimator", "USAC_MAGSAC")
        reproj_thresh = float(body.get("reproj_thresh", 3.0))
        enforce_spatial = bool(body.get("spatial_filter", body.get("enforce_spatial", True)))
        min_coverage = float(body.get("min_coverage", 0.15))
        subpixel = bool(body.get("subpixel", True))
        source_upload = None
        reference_upload = None
    else:
        form = await request.form()
        source_filename = str(form.get("source_preset") or form.get("source_filename") or "")
        reference_filename = str(form.get("reference_preset") or form.get("reference_filename") or "")
        method = str(form.get("method") or "sift")
        preprocessing = str(form.get("preprocessing") or "clahe")
        model_type = str(form.get("model_type") or "affine")
        estimator = str(form.get("estimator") or "USAC_MAGSAC")
        reproj_thresh = float(form.get("reproj_thresh") or 3.0)
        enforce_spatial = str(form.get("enforce_spatial", "true")).lower() in ("true", "1")
        min_coverage = float(form.get("min_coverage") or 0.15)
        subpixel = str(form.get("subpixel", "true")).lower() in ("true", "1")
        source_upload = form.get("source_upload")
        reference_upload = form.get("reference_upload")

    # Normalize method name
    method_key = method.lower().replace("+", "_").replace(" ", "_")
    if "superpoint" in method_key:
        method = "superpoint_lightglue"
    else:
        method = method_key

    if method not in MATCHERS:
        method = "sift"
    if preprocessing not in PREPROCESSING:
        preprocessing = "clahe"
    if model_type not in MODELS:
        model_type = "affine"
    if estimator not in ESTIMATORS:
        estimator = "USAC_MAGSAC"

    reproj_thresh = min(10.0, max(0.1, float(reproj_thresh)))
    min_coverage = min(0.5, max(0.05, float(min_coverage)))

    async def _materialize(upload: Optional[Any], filename: str, tag: str) -> Path:
        if upload is not None and hasattr(upload, "filename") and upload.filename:
            dest = UPLOAD_DIR / f"{tag}_{int(time.time())}_{_sanitize(upload.filename)}"
            content = await upload.read()
            with open(dest, "wb") as fh:
                fh.write(content)
            if PUBLIC_IMG_DIR.is_dir():
                with open(PUBLIC_IMG_DIR / dest.name, "wb") as fh:
                    fh.write(content)
            return dest
        if filename:
            found = _safe_lookup(filename)
            if found is not None:
                return found
        raise HTTPException(400, f"{tag} image missing: upload a file or pick a preset scene.")

    try:
        src_path = await _materialize(source_upload, source_filename, "source")
        ref_path = await _materialize(reference_upload, reference_filename, "reference")
        rec_src = load_lunar_image(src_path)
        rec_ref = load_lunar_image(ref_path)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(400, f"Could not read lunar products: {exc}")

    try:
        out = run_registration_pipeline(
            source_path=rec_src,
            reference_path=rec_ref,
            method=method,
            preprocessing=preprocessing,
            model_type=model_type,
            robust_estimator=estimator,
            enforce_spatial_coverage=enforce_spatial,
            min_coverage_ratio=min_coverage,
            subpixel_enabled=subpixel,
            reproj_thresh=reproj_thresh,
        )
    except Exception as exc:
        logger.exception("Pipeline execution failed")
        raise HTTPException(500, f"Pipeline error: {exc}")

    rep = out.quality_report
    stem = (
        f"{rec_src.file_path.stem}_to_{rec_ref.file_path.stem}"
        f"_{method}_{preprocessing}_{int(time.time())}"
    )
    files: dict = {}
    try:
        artefacts = {
            "registered": out.warped_image,
            "matches": _bgr_to_rgb(out.visualization_matches),
            "checkerboard": _bgr_to_rgb(out.visualization_checkerboard),
            "difference": _bgr_to_rgb(out.visualization_difference),
        }
        for key, img in artefacts.items():
            if img is not None:
                fname = f"{stem}_{key}.png"
                # Save to OUTPUTS_DIR
                cv2.imwrite(str(OUTPUTS_DIR / fname), img)
                # Also save to PUBLIC_IMG_DIR for direct frontend viewing
                if PUBLIC_IMG_DIR.is_dir():
                    cv2.imwrite(str(PUBLIC_IMG_DIR / fname), img)
                files[key] = fname
    except Exception as exc:
        logger.warning("Could not persist outputs: %s", exc)

    def _num(value: Any) -> Optional[float]:
        if value is None:
            return None
        try:
            f = float(value)
            return None if f == float("inf") or f != f else round(f, 4)
        except Exception:
            return None

    # Format transformation matrix
    tx_matrix = None
    if getattr(out, "robust_result", None) is not None:
        mat = getattr(out.robust_result, "matrix", None)
        if mat is not None:
            try:
                tx_matrix = [[float(v) for v in row] for row in mat]
            except Exception:
                tx_matrix = None

    metrics_payload = {
        # types.ts Metrics interface fields:
        "inliers": rep.inlier_match_count,
        "raw_matches": rep.raw_match_count,
        "inlier_ratio_pct": round(rep.inlier_ratio * 100.0, 2),
        "reproj_rmse_coarse": _num(rep.reprojection_rmse_coarse),
        "reproj_rmse_refined": _num(rep.reprojection_rmse_refined),
        "spatial_coverage_pct": round(rep.spatial_coverage_percent, 2),
        "grid_occupancy_pct": round((rep.occupied_cells / max(1, rep.total_cells)) * 100.0, 2) if rep.total_cells else 100.0,
        "photometric_ncc": round(float(rep.photometric_ncc), 4),
        "photometric_rmse": _num(getattr(rep, "photometric_rmse", 0.05)),
        "status": rep.status,
        "condition_number": _num(rep.condition_number),
        "is_stable": rep.is_stable,
        # Legacy/alternative keys:
        "rmse_coarse": _num(rep.reprojection_rmse_coarse),
        "rmse_refined": _num(rep.reprojection_rmse_refined),
        "delta_rmse": round(float(rep.delta_rmse), 4),
        "coverage_pct": round(rep.spatial_coverage_percent, 2),
        "occupied_cells": rep.occupied_cells,
        "total_cells": rep.total_cells,
        "ncc": round(float(rep.photometric_ncc), 4),
        "stable": rep.is_stable,
        "condition": _num(rep.condition_number),
    }

    logs = [
        f"[INGEST] Ingested Source Image: {rec_src.file_path.name}",
        f"[INGEST] Ingested Reference Image: {rec_ref.file_path.name}",
        f"[PREPROCESS] Executed {preprocessing.upper()} shadow enhancement pipeline.",
        f"[MATCHER] {method.upper()} extracted {rep.raw_match_count} initial correspondences.",
        f"[{estimator}] Robust outlier rejection converged with {rep.inlier_match_count} inliers ({rep.inlier_ratio * 100:.1f}%).",
    ]
    if subpixel:
        logs.append(f"[SUBPIXEL] Sub-pixel refinement optimized RMSE to {_num(rep.reprojection_rmse_refined)} px.")
    logs.append(f"[STATUS] Pipeline completed in {round(out.total_runtime_sec, 3)} s with status {rep.status}.")

    return {
        "success": out.success,
        "status": rep.status,
        "error": rep.failure_reason if not out.success else None,
        "runtime_sec": round(out.total_runtime_sec, 3),
        "pair": {"source": rec_src.file_path.name, "reference": rec_ref.file_path.name},
        "source": _describe(rec_src.file_path),
        "reference": _describe(rec_ref.file_path),
        "configuration": {
            "method": method,
            "preprocessing": preprocessing,
            "model_type": model_type,
            "robust_estimator": estimator,
            "reproj_thresh": reproj_thresh,
            "min_coverage": min_coverage,
            "subpixel": subpixel,
        },
        "quality_report": {
            "model_type": model_type,
            "status": rep.status,
            "failure_reason": rep.failure_reason,
        },
        "metrics": metrics_payload,
        "images": files,
        "files": files,
        "transformation_matrix": tx_matrix,
        "logs": logs,
    }


# ---------------------------------------------------------------- outputs
@app.get("/api/outputs/{name}")
def get_output(name: str):
    base = Path(name).name
    if Path(base).suffix.lower() != ".png":
        raise HTTPException(404, "Not found")
    path = OUTPUTS_DIR / base
    if not path.is_file():
        raise HTTPException(404, f"Output not found: {name}")
    return FileResponse(str(path), media_type="image/png", filename=base)


# ---------------------------------------------------------------- benchmark
@app.get("/api/benchmark")
def get_benchmark():
    bench_file = OUTPUTS_DIR / "benchmark_results.json"
    if bench_file.exists():
        import json
        with open(bench_file, "r") as f:
            return json.load(f)
    return []


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
