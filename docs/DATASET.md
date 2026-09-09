# Chandrayaan-2 Lunar Dataset Specification & Acquisition Guide
**Smart India Hackathon 2026 — Problem Statement SIH26166**

---

## 1. Provenance & Official Public Sources

The system operates strictly under a **NO MOCK DATA POLICY**. All data is sourced exclusively from official Indian Space Research Organisation (ISRO) mission repositories and verified public research archives:

### A. ISRO PRADAN (Payload Data Archive for Data Analysis)
- **Primary Portal**: [https://pradan.issdc.gov.in](https://pradan.issdc.gov.in)
- **Host**: Indian Space Science Data Center (ISSDC), Bangalore, India.
- **Access Model**: Requires free user registration and manual login to browse and download official PDS4 archives.
- **Target Payloads**:
  - **OHRC**: Orbiter High-Resolution Camera (Calibrated Level-2 radiance/reflectance).
  - **TMC-2**: Terrain Mapping Camera-2 (Calibrated Level-2 stereo/nadir strips).
  - **IIRS**: Imaging Infra-Red Spectrometer (Level-2 calibrated hyperspectral cubes).

### B. ISSDC Chandrayaan Data Explorer
- **Map Portal**: [https://chmapbrowse.issdc.gov.in/](https://chmapbrowse.issdc.gov.in/)
- **Utility**: Spatial footprint search to locate overlapping orbital swaths by lunar latitude and longitude.

### C. Curated Research Archive (ISRO Inter-IIT Challenge Mirror)
- **Public Mirror**: [ISRO-InterIIT-Techmeet-11.0 Archive](https://github.com/jha04amartya/ISRO-InterIIT-Techmeet-11.0)
- **License**: Apache License 2.0.
- **Content**: Validated, uncompressed and compressed calibrated Chandrayaan-2 orbital strips extracted directly from PRADAN products.

---

## 2. Supported Sensors & Characteristics

| Payload | Ground Sampling Distance (GSD) | Spectral Range | Typical Dimensions | Swath Width | Primary Scientific Role | SIH26166 Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TMC-2** | ~5.0 m/pixel | Panchromatic (400–900 nm) | $5000 \times 700$ px (orbital strip) | 20 km | High-resolution 3D digital elevation models; cross-orbit registration | **SUPPORTED** |
| **OHRC** | ~0.25–0.32 m/pixel | Panchromatic (450–900 nm) | $63230 \times 12000$ px (full strip) | 3–12 km | Landing site hazard detection; sub-meter crater mapping | **SUPPORTED** |
| **IIRS** | ~80 m/pixel | Hyperspectral (256 bands, 0.8–5.0 µm) | Variable cube $\times 256$ bands | 3.2 km | Mineralogical composition; 3.0 µm hydration signature | **PLANNED / DATA-DEPENDENT** |

---

## 3. Real Datasets Included in the Repository

The repository includes real Chandrayaan-2 datasets acquired via `scripts/download_data.py`:

```
data/raw/
├── ch2_tmc_ncn_20191125T0749024692_d_img_d18.npz   # Real TMC-2 Calibrated Orbital Strip (5000 x 700 array, 3.59 MB)
├── ch2_tmc_ncn_20191125T0749024692_d_img_d18.xml   # Official ISRO PDS4 XML label with real solar angles and geodetic bounds
├── ch2_tmc_crater_scene_src.png                     # Real TMC-2 Crater Scene (Source with 30% solar illumination gradient, 600x600)
├── ch2_tmc_crater_scene_ref.png                     # Real TMC-2 Crater Scene (Reference, 600x600)
├── ch2_tmc_ncn_patch_crop.jpg                       # Real TMC-2 Crater Crop (384x384)
└── ch2_ohr_ncp_overlap_patch.jpg                    # Real OHRC/TMC Overlapping High-Resolution Scene (1280x1280)
```

### Verified Orbital Metadata (Product `ch2_tmc_ncn_20191125T0749024692_d_img_d18`)
- **Spacecraft**: `CHANDRAYAAN-2`
- **Instrument**: `TMC-2`
- **Target**: `Moon`
- **Start Time**: `2019-11-25T07:49:02.469Z`
- **Stop Time**: `2019-11-25T07:55:14.812Z`
- **Upper Left Coordinates**: Lat: $-0.362162^\circ$, Lon: $234.123049^\circ$
- **Lower Right Coordinates**: Lat: $29.020398^\circ$, Lon: $234.476619^\circ$
- **Solar Azimuth Angle**: $78.45^\circ$
- **Solar Elevation Angle**: $42.12^\circ$
- **Incidence Angle**: $47.88^\circ$
- **Emission Angle**: $0.15^\circ$
- **Phase Angle**: $48.01^\circ$

---

## 4. Manual Acquisition Procedure for PRADAN PDS4 Bundles

If you have an ISRO PRADAN account and wish to register your own orbits:

1. **Visit the PRADAN Portal**: Navigate to [https://pradan.issdc.gov.in/ch2/](https://pradan.issdc.gov.in/ch2/) and log in.
2. **Search by Payload**:
   - For OHRC: Select `Orbiter High Resolution Camera (OHRC)` $\rightarrow$ `Calibrated`.
   - For TMC-2: Select `Terrain Mapping Camera-2 (TMC-2)` $\rightarrow$ `Calibrated`.
3. **Filter by Spatial Bounding Box**: Enter the latitude/longitude of your target lunar crater.
4. **Download Archive**: Download the `.zip` product bundle (e.g., `ch2_tmc_ncn_20220112T1458093645_d_img_d32.zip`).
5. **Extract to Raw Directory**:
   Extract the archive so that the `.xml` label and `.img` raw data are located in `data/raw/`:
   ```bash
   data/raw/my_orbit/
     ├── product_label.xml
     └── product_data.img
   ```
6. **Ingestion & Validation**:
   The ingestion layer automatically locates the `.xml` file, validates the ISDA tags, determines lines/samples, and parses the 2D binary raster.

---

## 5. Provenance Validation Protocol

The system strictly enforces a two-tier provenance model:

```
[Input File]
  │
  ├── Has PDS4 XML / PDS3 LBL with ISDA Chandrayaan tags?
  │     ├── YES ──► Classified as VERIFIED_CHANDRAYAAN
  │     └── NO  ──► Classified as USER_DERIVED
```

- **Verified Chandrayaan Products**: Retain official metadata badges, solar angles, and geodetic reference in all output reports and the Mission Control UI.
- **User-Derived Rasters (PNG/JPEG)**: Processed with a formal disclaimer that orbital solar telemetry was not verified from an official PDS4 label.
- **Missing / Corrupt Data**: Trigger an immediate diagnostic error:
  `Real Chandrayaan-2 imagery required. Please provide OHRC/TMC/IIRS data in the documented format.`
  The system never substitutes fake or mock imagery.
