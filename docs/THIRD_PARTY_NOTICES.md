# Third-Party Open-Source Notices & Attribution
**Smart India Hackathon 2026 — Problem Statement SIH26166**

This project is built under an **Open-Source-First Development Strategy**. We gratefully acknowledge and credit the upstream open-source projects, algorithms, and models integrated and adapted within this system.

---

## 1. Upstream Open-Source Projects & Dependency Ledger

### A. ISRO-InterIIT-Techmeet-11.0
- **Repository**: [https://github.com/jha04amartya/ISRO-InterIIT-Techmeet-11.0](https://github.com/jha04amartya/ISRO-InterIIT-Techmeet-11.0)
- **Author**: Amartya Jha et al.
- **License**: Apache License 2.0
- **Component Reused**: ISDA PDS4 XML coordinate extraction logic, Chandrayaan-2 orbital intersection tables (`coordinates_tmc2.csv`, `coordinates_ohrc.csv`), and calibrated Chandrayaan-2 orbital array data (`better_cropped_tmc.npz`).
- **Modifications**: Re-engineered from monolithic Jupyter notebooks into modular, type-hinted Python ingestion modules (`src/data/ingestion.py`, `src/data/metadata.py`) with strict two-tier provenance verification.

### B. Chandra Hazard Mapper
- **Repository**: [https://github.com/aks-builds/chandra-hazard-mapper](https://github.com/aks-builds/chandra-hazard-mapper)
- **Author**: aks-builds
- **License**: Apache License 2.0
- **Component Reused**: Baseline orbital co-registration scaffolding concepts and PDS label admission gating ideas.
- **Modifications**: Completely replaced simple RANSAC + Affine with MAGSAC++ (`cv2.USAC_MAGSAC`), added Homography (8 DOF) and Rigid (3 DOF) models, added condition-number stability checks, integrated deep learned matchers, and built spatial grid-cell coverage filtering.

### C. LightGlue & SuperPoint
- **Repository**: [https://github.com/cvg/LightGlue](https://github.com/cvg/LightGlue)
- **Authors**: Philipp Lindenberger, Paul-Edouard Sarlin, Marc Pollefeys (Computer Vision and Geometry Group, ETH Zürich)
- **License**: Apache License 2.0
- **Paper**: *LightGlue: Local Feature Matching at Light Speed*, ICCV 2023.
- **Component Reused**: SuperPoint deep keypoint extractor and LightGlue transformer matcher.
- **Modifications**: Integrated as a modular backend adapter in `src/matching/superpoint_lightglue.py`, with CPU execution optimization, batch unpacking (`rbd`), and scale-aware lunar terrain normalization.

### D. LoFTR (via Kornia)
- **Repository**: [https://github.com/zju3dv/LoFTR](https://github.com/zju3dv/LoFTR) / [https://github.com/kornia/kornia](https://github.com/kornia/kornia)
- **Authors**: Jiaming Sun, Zehong Shen, Yuang Wang, Hujun Bao, Xiaowei Zhou (Zhejiang University) & Kornia contributors.
- **License**: Apache License 2.0
- **Paper**: *LoFTR: Detector-Free Local Feature Matching with Transformers*, CVPR 2021.
- **Component Reused**: Pretrained coarse-to-fine transformer correspondence model via `kornia.feature.LoFTR`.
- **Modifications**: Built an adaptive downsampling and coordinate rescaling adapter (`src/matching/loftr_matcher.py`) to prevent CPU memory exhaustion on large orbital swaths while mapping coordinates back to full resolution.

### E. OpenCV (Open Source Computer Vision Library)
- **Repository**: [https://github.com/opencv/opencv](https://github.com/opencv/opencv)
- **License**: Apache License 2.0
- **Components Used**: SIFT, ORB, `cv2.USAC_MAGSAC`, `cv2.estimateAffine2D`, `cv2.findHomography`, `cv2.warpAffine`, `cv2.warpPerspective`, `cv2.cornerSubPix`, CLAHE.

### F. SciPy & NumPy
- **License**: BSD 3-Clause License
- **Components Used**: `scipy.spatial.ConvexHull` for spatial coverage polygons, array operations, linear algebra SVD.

### G. Streamlit
- **License**: Apache License 2.0
- **Components Used**: Web dashboard framework.

---

## 2. Our SIH26166 Original Engineering Contributions

In strict accordance with academic and engineering integrity, we clearly demarcate third-party libraries from our original engineering for SIH26166:

1. **Multi-Sensor Remote-Sensing Architecture**: Unified pipeline bridging OHRC, TMC-2, and IIRS data products with different ground sampling distances (0.25 m to 80 m).
2. **Chandrayaan-2 PDS4 ISDA XML Ingestion Engine**: Native parsing of ISRO-specific XML namespaces (`http://pds.nasa.gov/pds4/pds/v1` and `https://isda.issdc.gov.in/pds4/isda/v1`), extracting solar elevation, solar azimuth, incidence, emission, and phase angles.
3. **Data Provenance Validation Layer**: Formal two-tier classification separating genuine PDS4 mission products from user-derived rasters.
4. **Lunar Illumination Evaluation Framework**: Systematic comparison of CLAHE, Sobel gradient representations, and bandpass phase congruency under extreme crater shadow shifts.
5. **Spatial Correspondence Filtering Algorithm**: $8 \times 8$ grid-cell binning and non-maximum suppression preventing cluster collapse on prominent crater rims, combined with Convex Hull area coverage quantification.
6. **Sub-Pixel Refinement Engine**: Iterative gradient-based coordinate refinement reporting coarse vs. refined RMSE and $\Delta$RMSE with a formal scientific disclaimer.
7. **Model Stability Validation**: Singular Value Decomposition (SVD) condition number ($\kappa \le 10^5$), determinant checking ($\det > 0$), and scale bounds checking.
8. **Honest Failure Diagnostic Engine**: Rejection of degenerate transformations, clustered points, and unverified data without forced/fake success.
9. **ISRO Mission Control Scientific UI**: Aerospace-themed dashboard with before/after swipe slider, checkerboards, difference heatmaps, and telemetry exports.
10. **Automated Multi-Algorithm Benchmark Suite**: Automated headless runner producing empirical metric ledgers on real Chandrayaan-2 orbital imagery.
