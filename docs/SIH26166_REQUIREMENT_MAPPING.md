# SIH26166 Requirement Traceability Matrix

This document maps every requirement specified in Smart India Hackathon Problem Statement **SIH26166** (Chandrayaan-2 Lunar Image Registration) to its concrete implementation, source module, automated test, and verified status.

---

## Traceability Table

| # | SIH26166 Requirement | Current Implementation | Source Module | Evidence / Test | Status |
| :-: | :--- | :--- | :--- | :--- | :---: |
| **1** | **Target Problem Alignment** | End-to-end registration pipeline specifically tailored for Chandrayaan-2 orbital payloads (TMC-2, OHRC, IIRS). Zero references to unrelated PS. | `src/pipeline.py` | `tests/test_end_to_end.py` | **IMPLEMENTED** |
| **2** | **Open-Source Base Integration** | Leverages and adapts `ISRO-InterIIT-11.0` (metadata/arrays), `LightGlue` (deep matching), `LoFTR` (dense transformer), and `OpenCV` (geometry). | `src/data/`, `src/matching/`, `src/registration/` | `docs/THIRD_PARTY_NOTICES.md` | **IMPLEMENTED** |
| **3** | **Strict No-Mock-Data Policy** | Operates exclusively on real Chandrayaan-2 calibrated orbital strips and patches. Zero synthetic, random, or hardcoded images. | `scripts/download_data.py`, `data/raw/` | `tests/test_ingestion.py` | **IMPLEMENTED** |
| **4** | **Data Provenance Validation** | Two-tier validation separating verified PDS4 mission products (`VERIFIED_CHANDRAYAAN`) from user-derived rasters (`USER_DERIVED`). | `src/data/ingestion.py`, `src/data/metadata.py` | `tests/test_ingestion.py` | **IMPLEMENTED** |
| **5** | **PDS4 / Planetary Data Handling** | Native parser for ISRO ISDA PDS4 XML labels (`lines`, `samples`, `solar_elevation_angle`, `upper_left_lat/lon`) and raw `.img` / `.npz`. | `src/data/metadata.py`, `src/data/ingestion.py` | `tests/test_ingestion.py` | **IMPLEMENTED** |
| **6** | **TMC-2 Sensor Support** | Ingestion, preprocessing, and registration for 5 m/px Terrain Mapping Camera-2 strips. Verified on real orbit `ch2_tmc_ncn_20191125T0749024692`. | `src/data/ingestion.py` | `tests/test_end_to_end.py` | **IMPLEMENTED** |
| **7** | **OHRC Sensor Support** | High-resolution (~0.25 m/px) Orbiter High Resolution Camera scene ingestion and multi-scale registration support. | `src/data/ingestion.py` | `tests/test_end_to_end.py` | **IMPLEMENTED** |
| **8** | **IIRS Sensor Support** | 3D hyperspectral cube ingestion parser and 2D continuum band (~1.5 µm) extractor for registration against TMC-2. | `src/data/ingestion.py` | Data-dependent upon user PDS4 cube upload | **PARTIALLY IMPLEMENTED** (Documented & Ingestion Ready) |
| **9** | **Illumination Invariance** | Evaluated CLAHE (local contrast equalization), Sobel gradient orientation, and bandpass phase congruency representations. | `src/data/preprocessing.py` | `tests/test_preprocessing.py`, `BENCHMARK.md` | **IMPLEMENTED** |
| **10** | **Multi-Algorithm Matching** | Independent implementations of Classical SIFT, Classical ORB, Learned SuperPoint+LightGlue, and Dense LoFTR. | `src/matching/` | `tests/test_matching.py` | **IMPLEMENTED** |
| **11** | **Robust Outlier Rejection** | MAGSAC++ (`cv2.USAC_MAGSAC`) and RANSAC consensus estimators for robust correspondence filtering. | `src/registration/robust_estimation.py` | `tests/test_registration.py` | **IMPLEMENTED** |
| **12** | **Geometric Transformation** | Mathematically verified Affine (6 DOF), Homography (8 DOF), and Rigid (3 DOF) models with SVD condition number validation ($\kappa \le 10^5$). | `src/registration/geometry.py` | `tests/test_registration.py` | **IMPLEMENTED** |
| **13** | **Spatial Correspondence Distribution**| $8 \times 8$ grid-cell binning with cell occupancy metrics and Convex Hull area coverage quantification. | `src/registration/spatial_filter.py` | `tests/test_spatial_filter.py` | **IMPLEMENTED** |
| **14** | **Sub-Pixel Refinement** | Iterative gradient-based sub-pixel refinement (`cv2.cornerSubPix`) computing coarse RMSE, refined RMSE, and $\Delta$RMSE. | `src/registration/subpixel.py` | `tests/test_subpixel.py` | **IMPLEMENTED** |
| **15** | **Quantitative Quality Evaluation** | Computes un-simulated Inliers, Inlier Ratio, Reprojection RMSE, Spatial Coverage %, Grid Occupancy %, and Photometric NCC. | `src/evaluation/metrics.py` | `tests/test_evaluation.py` | **IMPLEMENTED** |
| **16** | **Honest Failure Handling** | Explicit detection of insufficient correspondences, low spatial coverage, degenerate matrices, or unverified data without forced success. | `src/pipeline.py` | `tests/test_failure_handling.py` | **IMPLEMENTED** |
| **17** | **Multi-Model Benchmarking** | Automated headless benchmarking runner comparing SIFT, ORB, SuperPoint+LightGlue, and LoFTR on real Chandrayaan-2 data. | `src/evaluation/benchmark.py`, `scripts/benchmark_models.py` | `data/outputs/benchmark_results.json` | **IMPLEMENTED** |
| **18** | **ISRO Mission Control Dashboard** | Interactive scientific UI with three-panel layout, swipe comparison slider, checkerboard, difference heatmap, and export suite. | `app/dashboard.py`, `app/styles.py` | Visual interactive testing | **IMPLEMENTED** |
| **19** | **Export Suite** | Direct download of registered images (PNG/TIFF), match plots, metrics JSON, metrics CSV, and formal mission report (TXT). | `app/dashboard.py`, `scripts/run_pipeline.py` | Output artifacts in `data/outputs/` | **IMPLEMENTED** |
| **20** | **Reproducible Deployment** | Standalone containerized Docker setup and locked environment specifications. | `Dockerfile`, `docker-compose.yml`, `requirements.txt` | Build verification | **IMPLEMENTED** |
