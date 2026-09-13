"""
Chandrayaan-2 Lunar Image Registration API (FastAPI).
SIH26166 — real data only. No mock, no synthetic, no hardcoded metrics.

Contract:
  GET  /api/health          service + device + supported options
  GET  /api/pairs           preset pairs probed from data/raw (only files on disk)
  GET  /api/preview?file=   source/reference image bytes (data/raw or data/uploads)
  POST /api/register        multipart: preset filenames and/or uploaded files + params
  GET  /api/outputs/{name}  result artefacts produced by live runs in data/outputs
"""
from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import List, Optional

import cv2
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ch2-api")

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
OUTPUTS_DIR = BASE_DIR / "data" / "outputs"
for _d in (RAW_DIR, UPLOAD_DIR, OUTPUTS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

from src.data.ingestion import load_lunar_image  # noqa: E402
from src.pipeline import run_registration_pipeline  # noqa: E402

app = FastAPI(title="Chandrayaan-2 Registration API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MATCHERS = ["sift", "orb", "superpoint_lightglue", "loftr"]
PREPROCESSING = ["clahe", "gradient", "phase_congruency", "raw"]
MODELS = ["affine", "homography", "rigid"]
ESTIMATORS = ["USAC_MAGSAC", "RANSAC"]

# (id, display name, source file, reference file) — served only if both exist.
PRESET_DEFS = [
    (
        "tmc_crater",
        "Crater field — TMC-2 cross-pass (600 x 600)",
        "ch2_tmc_crater_scene_src.png",
        "ch2_tmc_crater_scene_ref.png",
    ),
    (
        "strip_ohrc",
        "Orbit strip — TMC-2 crop vs OHRC patch",
        "ch2_tmc_ncn_patch_crop.jpg",
        "ch2_ohr_ncp_overlap_patch.jpg",
    ),
]

ALLOWED_SUFFIXES = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".npz", ".img"}


def _safe_lookup(name: str) -> Optional[Path]:
    """Resolve a client-supplied filename inside RAW_DIR / UPLOAD_DIR only."""
    base = Path(name or "").name
    if not base or base.startswith("."):
        return None
    if Path(base).suffix.lower() not in ALLOWED_SUFFIXES:
        return None
    for directory in (RAW_DIR, UPLOAD_DIR):
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
    rec = load_lunar_image(path)
    h, w = rec.image_uint8.shape[:2]
    return {
        "file": path.name,
        "sensor": rec.sensor,
        "provenance": rec.provenance.value,
        "width": w,
        "height": h,
        "bytes": path.stat().st_size,
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
        device = torch.cuda.get_device_name(0) if cuda else "CPU"
    except Exception:
        cuda, device = False, "CPU"
    return {
        "status": "ONLINE",
        "service": "Chandrayaan-2 Registration Engine (SIH26166)",
        "device": device,
        "cuda": cuda,
        "matchers": MATCHERS,
        "preprocessing": PREPROCESSING,
        "models": MODELS,
        "estimators": ESTIMATORS,
        "timestamp": time.time(),
    }


# ---------------------------------------------------------------- pairs
@app.get("/api/pairs")
def get_pairs() -> List[dict]:
    pairs: List[dict] = []
    for pid, name, src_name, ref_name in PRESET_DEFS:
        src = RAW_DIR / src_name
        ref = RAW_DIR / ref_name
        if not (src.is_file() and ref.is_file()):
            continue
        try:
            pairs.append(
                {
                    "id": pid,
                    "name": name,
                    "source": _describe(src),
                    "reference": _describe(ref),
                }
            )
        except Exception as exc:  # unreadable product -> skip, never fake
            logger.warning("Skipping preset %s: %s", pid, exc)
    return pairs


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
async def post_register(
    source_preset: str = Form(default=""),
    reference_preset: str = Form(default=""),
    source_upload: Optional[UploadFile] = File(default=None),
    reference_upload: Optional[UploadFile] = File(default=None),
    method: str = Form(default="sift"),
    preprocessing: str = Form(default="clahe"),
    model_type: str = Form(default="affine"),
    estimator: str = Form(default="USAC_MAGSAC"),
    reproj_thresh: float = Form(default=3.0),
    enforce_spatial: bool = Form(default=True),
    min_coverage: float = Form(default=0.15),
    subpixel: bool = Form(default=True),
):
    if method not in MATCHERS:
        raise HTTPException(400, f"Unknown matcher: {method}")
    if preprocessing not in PREPROCESSING:
        raise HTTPException(400, f"Unknown preprocessing: {preprocessing}")
    if model_type not in MODELS:
        raise HTTPException(400, f"Unknown model: {model_type}")
    if estimator not in ESTIMATORS:
        raise HTTPException(400, f"Unknown estimator: {estimator}")
    reproj_thresh = min(10.0, max(1.0, float(reproj_thresh)))
    min_coverage = min(0.5, max(0.05, float(min_coverage)))

    async def _materialize(upload: Optional[UploadFile], preset: str, tag: str) -> Path:
        if upload is not None and upload.filename:
            dest = UPLOAD_DIR / f"{tag}_{int(time.time())}_{_sanitize(upload.filename)}"
            with open(dest, "wb") as fh:
                fh.write(await upload.read())
            return dest
        if preset:
            found = _safe_lookup(preset)
            if found is not None:
                return found
        raise HTTPException(400, f"{tag} image missing: upload a file or pick a preset scene.")

    try:
        src_path = await _materialize(source_upload, source_preset, "source")
        ref_path = await _materialize(reference_upload, reference_preset, "reference")
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
            fname = f"{stem}_{key}.png"
            cv2.imwrite(str(OUTPUTS_DIR / fname), img)
            files[key] = fname
    except Exception as exc:
        logger.warning("Could not persist outputs: %s", exc)

    def _num(value: float):
        f = float(value)
        return None if f == float("inf") or f != f else round(f, 4)

    return {
        "success": out.success,
        "status": rep.status,
        "failure_reason": rep.failure_reason,
        "runtime_sec": round(out.total_runtime_sec, 3),
        "pair": {"source": rec_src.file_path.name, "reference": rec_ref.file_path.name},
        "config": {
            "method": method,
            "preprocessing": preprocessing,
            "model": model_type,
            "estimator": estimator,
            "reproj_thresh": reproj_thresh,
            "min_coverage": min_coverage,
            "subpixel": subpixel,
        },
        "metrics": {
            "raw_matches": rep.raw_match_count,
            "inliers": rep.inlier_match_count,
            "inlier_ratio_pct": round(rep.inlier_ratio * 100.0, 2),
            "rmse_coarse": _num(rep.reprojection_rmse_coarse),
            "rmse_refined": _num(rep.reprojection_rmse_refined),
            "delta_rmse": round(float(rep.delta_rmse), 4),
            "coverage_pct": round(rep.spatial_coverage_percent, 2),
            "occupied_cells": rep.occupied_cells,
            "total_cells": rep.total_cells,
            "ncc": round(float(rep.photometric_ncc), 4),
            "stable": rep.is_stable,
            "condition": _num(rep.condition_number),
        },
        "files": files,
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
