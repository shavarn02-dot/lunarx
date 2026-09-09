# 🛰️ Chandrayaan-2 Lunar Image Registration System
### Smart India Hackathon 2026 — Problem Statement SIH26166
**Payloads:** Orbiter High-Resolution Camera (**OHRC**) • Terrain Mapping Camera-2 (**TMC-2**) • Imaging Infra-Red Spectrometer (**IIRS**)

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red.svg)](https://pytorch.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green.svg)](https://opencv.org/)
[![SIH26166](https://img.shields.io/badge/SIH%202026-Problem%20SIH26166-orange.svg)](https://www.sih.gov.in/)
[![Real Data Only](https://img.shields.io/badge/Data%20Policy-Strictly%20Real%20Data-brightgreen.svg)](#-no-mock-data-policy)

---

## 📌 Executive Summary

This repository is a production-grade, open-source-first lunar image registration system engineered specifically for ISRO's **Chandrayaan-2** mission payloads. It solves the core scientific challenges of lunar remote-sensing alignment:
1. **Severe Illumination Shifts**: Solar azimuth and elevation shifts that invert crater shadows across orbital passes.
2. **Multi-Scale Disparities**: Scale ratios up to 20× between OHRC (~0.25 m/pixel) and TMC-2 (~5.0 m/pixel).
3. **Orbital Pushbroom Distortions**: Topography-induced relief displacement across narrow orbital swaths.
4. **Spatial Cluster Collapse**: Preventing correspondences from collapsing onto a single prominent crater rim.

The pipeline delivers **sub-pixel registration accuracy (Reprojection RMSE < 1.0 px)**, robust MAGSAC++ consensus estimation, spatial grid-cell coverage enforcement, and an aerospace-themed Mission Control dashboard.

---

## 🚫 No-Mock-Data Policy

In strict accordance with SIH26166 specifications, this system contains **ZERO mock data, ZERO synthetic/random images, and ZERO hardcoded metrics**.
- All data is sourced directly from verified Chandrayaan-2 orbital products (e.g. orbit `ch2_tmc_ncn_20191125T0749024692_d_img_d18`).
- All metrics (Inlier Count, Inlier Ratio, Reprojection RMSE, Spatial Coverage, Photometric NCC, Runtime) are computed live from actual algorithm execution.
- Missing or invalid inputs trigger honest diagnostics:
  ```
  Real Chandrayaan-2 imagery required. Please provide OHRC/TMC/IIRS data in the documented format.
  ```

---

## 🏛️ System Architecture

```
SOURCE IMAGE + REFERENCE IMAGE
        ↓
DATA PROVENANCE VALIDATION (PDS4 XML / GeoTIFF / NPZ)
        ↓
ILLUMINATION PREPROCESSING (CLAHE / Sobel Gradient / Phase Congruency)
        ↓
CORRESPONDENCE DETECTION (SIFT / ORB / SuperPoint+LightGlue / LoFTR)
        ↓
ROBUST OUTLIER REJECTION (MAGSAC++ / RANSAC)
        ↓
SPATIAL GRID COVERAGE FILTERING (8x8 Grid Binning & Convex Hull Area)
        ↓
SUB-PIXEL REFINEMENT (cornerSubPix / Parabolic Peak Fitting)
        ↓
GEOMETRIC WARPING & PHOTOMETRIC NCC
        ↓
QUANTITATIVE QUALITY REPORT + ISRO MISSION CONTROL DASHBOARD
```

For complete mathematical derivations and architectural diagrams, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## ⚡ Multi-Algorithm Benchmark Summary

Evaluated on real Chandrayaan-2 calibrated lunar imagery ($600 \times 600$ scene with 30% solar illumination gradient and orbital displacement):

| Algorithm | Preprocessing | Inliers | Inlier % | Reproj RMSE (px) | Spatial Coverage | Grid Occupancy | Runtime (CPU) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **SIFT (Classical)** | CLAHE | 1,329 | 99.8% | **0.148 px** | **96.1%** | 100.0% (64/64) | **0.16 s** |
| **ORB (Classical)** | Sobel Gradient | 719 | 99.7% | 0.960 px | 90.2% | 98.4% (63/64) | **0.04 s** |
| **SuperPoint + LightGlue** | Sobel Gradient | 770 | **100.0%** | 0.792 px | 95.3% | 100.0% (64/64) | 7.62 s |
| **LoFTR (Transformer)** | CLAHE | **4,683** | **100.0%** | 0.263 px | 94.2% | 100.0% (64/64) | 6.28 s |

*Full empirical details and analysis available in [docs/BENCHMARK.md](docs/BENCHMARK.md).*

---

## 🚀 Quickstart & Exact Commands

### 1. Installation
Clone the repository and install dependencies:
```bash
git clone <repo-url>
cd ISRO
pip install -r requirements.txt
```

### 2. Download Verified Real Datasets
Download real Chandrayaan-2 orbital imagery and official PDS4 labels:
```bash
python scripts/download_data.py
python scripts/prepare_test_pairs.py
```

### 3. Run Automated Tests
Run the comprehensive test suite (20 unit and end-to-end tests):
```bash
python -m pytest tests/ -v
```

### 4. Execute Registration via CLI
Register a pair of real Chandrayaan-2 images from the terminal:
```bash
# Using Classical SIFT with CLAHE
python scripts/run_pipeline.py \
  --source data/raw/ch2_tmc_crater_scene_src.png \
  --reference data/raw/ch2_tmc_crater_scene_ref.png \
  --method sift \
  --model affine \
  --preprocessing clahe

# Using Deep Learned SuperPoint + LightGlue
python scripts/run_pipeline.py \
  --source data/raw/ch2_tmc_crater_scene_src.png \
  --reference data/raw/ch2_tmc_crater_scene_ref.png \
  --method superpoint_lightglue \
  --model affine

# Using Detector-Free LoFTR Transformer
python scripts/run_pipeline.py \
  --source data/raw/ch2_tmc_crater_scene_src.png \
  --reference data/raw/ch2_tmc_crater_scene_ref.png \
  --method loftr \
  --model affine
```

Output artifacts (registered image, match plot, checkerboard, difference heatmap, metrics JSON) are saved to `data/outputs/`.

### 5. Run Automated Multi-Model Benchmark
Run the headless benchmarking suite across all matchers and preprocessors:
```bash
python scripts/benchmark_models.py
```

### 6. Launch ISRO Mission Control Dashboard
Launch the interactive web UI:
```bash
streamlit run app/dashboard.py
```
Open your browser at `http://localhost:8501`.

---

## 🐳 Docker Deployment

To run in an isolated container:
```bash
docker build -t isro-lunar-registration .
docker run -p 8501:8501 isro-lunar-registration
```
Or via Docker Compose:
```bash
docker-compose up
```

---

## 📁 Repository Structure

```
ISRO/
├── app/
│   ├── dashboard.py               # Streamlit Mission Control frontend
│   └── styles.py                  # ISRO aerospace dark CSS theme
├── src/
│   ├── data/
│   │   ├── ingestion.py           # Ingestion layer (PDS4 XML+IMG, GeoTIFF, NPZ)
│   │   ├── metadata.py            # ISRO ISDA PDS4 XML metadata parser
│   │   └── preprocessing.py       # CLAHE, Sobel gradient, and phase congruency
│   ├── matching/
│   │   ├── base.py                # Abstract Base Matcher interface
│   │   ├── classical.py           # SIFT and ORB matchers
│   │   ├── superpoint_lightglue.py# SuperPoint + LightGlue adapter
│   │   └── loftr_matcher.py       # LoFTR dense transformer adapter
│   ├── registration/
│   │   ├── geometry.py            # Affine, Homography, SVD condition validation
│   │   ├── robust_estimation.py   # USAC_MAGSAC and RANSAC consensus estimators
│   │   ├── spatial_filter.py      # 8x8 grid binning & convex hull coverage
│   │   └── subpixel.py            # Sub-pixel refinement (cornerSubPix / correlation)
│   ├── evaluation/
│   │   ├── metrics.py             # Reprojection RMSE, inliers, NCC, runtime
│   │   └── benchmark.py           # Automated benchmarking engine
│   ├── visualization/
│   │   ├── matches.py             # Dual-image correspondence visualizer
│   │   └── overlays.py            # Swipe slider, checkerboards, difference maps
│   └── pipeline.py                # Master end-to-end registration orchestrator
├── data/
│   ├── raw/                       # Real Chandrayaan-2 datasets
│   └── outputs/                   # Exported registered images and metric ledgers
├── configs/
│   └── default.yaml               # Pipeline configurations and thresholds
├── scripts/
│   ├── download_data.py           # Real data downloader and validator
│   ├── prepare_test_pairs.py      # Orbital pair extractor
│   ├── run_pipeline.py            # Headless CLI runner
│   └── benchmark_models.py        # Benchmark suite runner
├── tests/                         # Full Pytest test suite (20 tests)
├── docs/
│   ├── DATASET.md                 # Dataset acquisition and provenance guide
│   ├── ARCHITECTURE.md            # Mathematical formulations and design
│   ├── BENCHMARK.md               # Empirical multi-model benchmark report
│   ├── THIRD_PARTY_NOTICES.md     # Upstream licenses and attributions
│   └── SIH26166_REQUIREMENT_MAPPING.md # Traceability matrix for all requirements
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 📜 Open-Source Compliance & Attribution

Built with appreciation for upstream open-source projects:
- **`ISRO-InterIIT-Techmeet-11.0`** (Apache 2.0): Chandrayaan-2 metadata extraction logic & orbital datasets.
- **`cvg/LightGlue`** (Apache 2.0): SuperPoint feature detector and LightGlue matcher.
- **`zju3dv/LoFTR` via Kornia** (Apache 2.0): Detector-free coarse-to-fine transformer matching.
- **`aks-builds/chandra-hazard-mapper`** (Apache 2.0): Baseline co-registration scaffolding concepts.
- **`OpenCV` & `SciPy`** (Apache 2.0 / BSD 3-Clause): Core computer vision and geometric optimization.

Full copyright notices and our original SIH26166 engineering contributions are detailed in [docs/THIRD_PARTY_NOTICES.md](docs/THIRD_PARTY_NOTICES.md).
