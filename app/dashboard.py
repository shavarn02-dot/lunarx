"""
ISRO Mission Control Dashboard for Chandrayaan-2 Lunar Image Registration.
SIH26166 Compliant — Strictly Real Lunar Data, Zero Mock Data.
"""
import streamlit as st
import sys
from pathlib import Path

# Ensure ISRO repo root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import csv
import io
import time
import numpy as np
import cv2
from PIL import Image

from src.data.ingestion import load_lunar_image, LunarImageRecord, DataProvenance
from src.pipeline import run_registration_pipeline, PipelineOutput
from src.visualization.overlays import create_split_slider_composite, create_checkerboard_overlay, create_difference_heatmap
from app.styles import ISRO_THEME_CSS

# Page configuration
st.set_page_config(
    page_title="ISRO Chandrayaan-2 Lunar Registration | SIH26166",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply CSS
st.markdown(ISRO_THEME_CSS, unsafe_allow_html=True)

# Header Banner
st.markdown("""
<div class="isro-header">
    <div class="isro-title">
        <span>🛰️ CHANDRAYAAN-2 LUNAR IMAGE REGISTRATION SYSTEM</span>
    </div>
    <div class="isro-subtitle">
        Smart India Hackathon 2026 — Problem Statement <b>SIH26166</b> | ISRO / Department of Space
        <br>Payloads: <b>OHRC</b> (~0.25 m/px) • <b>TMC-2</b> (~5.0 m/px) • <b>IIRS</b> (~80 m/px) | Real Data Pipeline
    </div>
</div>
""", unsafe_allow_html=True)


# Sidebar Configuration
st.sidebar.markdown("### ⚙️ MISSION PARAMETERS")

data_mode = st.sidebar.radio(
    "Data Source Mode",
    ["Verified Pre-Loaded Chandrayaan-2 Scenes", "Upload Custom Chandrayaan-2 Products"],
    index=0
)

# Pre-defined verified real Chandrayaan-2 scenes
sample_pair = None
src_file = None
ref_file = None

raw_dir = Path("data/raw")
raw_dir.mkdir(parents=True, exist_ok=True)

if data_mode == "Verified Pre-Loaded Chandrayaan-2 Scenes":
    preset = st.sidebar.selectbox(
        "Select Real Orbital Scene",
        [
            "Pair 1: TMC-2 Crater Terrain (Cross-Pass Scene, 600x600, Solar Illumination Shift)",
            "Pair 2: TMC-2 Orbit Strip Crop vs OHRC High-Resolution Scene",
        ]
    )
    if "Pair 1" in preset:
        src_file = raw_dir / "ch2_tmc_crater_scene_src.png"
        ref_file = raw_dir / "ch2_tmc_crater_scene_ref.png"
    else:
        src_file = raw_dir / "ch2_tmc_ncn_patch_crop.jpg"
        ref_file = raw_dir / "ch2_ohr_ncp_overlap_patch.jpg"
else:
    st.sidebar.info("Upload official PDS4 XML+IMG, GeoTIFF, NPZ, or calibrated PNG/JPEG.")
    up_src = st.sidebar.file_uploader("Source Lunar Image", type=["png", "jpg", "jpeg", "tif", "tiff", "npz", "img"])
    up_ref = st.sidebar.file_uploader("Reference Lunar Image", type=["png", "jpg", "jpeg", "tif", "tiff", "npz", "img"])
    if up_src and up_ref:
        # Save temporary uploads
        temp_src = raw_dir / f"upload_src_{up_src.name}"
        temp_ref = raw_dir / f"upload_ref_{up_ref.name}"
        with open(temp_src, "wb") as f:
            f.write(up_src.getbuffer())
        with open(temp_ref, "wb") as f:
            f.write(up_ref.getbuffer())
        src_file = temp_src
        ref_file = temp_ref

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 ALGORITHM SELECTION")

matcher_choice = st.sidebar.selectbox(
    "Feature Matcher",
    ["superpoint_lightglue", "sift", "orb", "loftr"],
    index=0,
    help="SIFT/ORB: Classical fast baseline; SuperPoint+LightGlue: Learned illumination-invariant sparse matcher; LoFTR: Dense transformer matcher."
)

prep_choice = st.sidebar.selectbox(
    "Illumination Preprocessing",
    ["clahe", "gradient", "phase_congruency", "raw"],
    index=0,
    help="CLAHE: Local contrast equalization; Gradient: Sobel orientation; Phase Congruency: Frequency-domain edge invariance."
)

model_choice = st.sidebar.selectbox(
    "Geometric Transformation",
    ["affine", "homography", "rigid"],
    index=0,
    help="Affine: 6 DOF (pushbroom strips); Homography: 8 DOF (projective); Rigid: 3 DOF (rotation+translation)."
)

estimator_choice = st.sidebar.selectbox(
    "Robust Outlier Estimator",
    ["USAC_MAGSAC", "RANSAC"],
    index=0,
    help="MAGSAC++: Modern threshold-free consensus; RANSAC: Classical consensus."
)

reproj_slider = st.sidebar.slider("Reprojection Threshold (pixels)", 1.0, 10.0, 3.0, 0.5)

enforce_spatial = st.sidebar.checkbox("Enforce Spatial Coverage Filtering", value=True)
min_coverage_pct = st.sidebar.slider("Min Grid Occupancy (%)", 5, 50, 15, 5)

enable_subpixel = st.sidebar.checkbox("Enable Sub-Pixel Refinement", value=True)

btn_run = st.sidebar.button("🚀 EXECUTE REGISTRATION PIPELINE")


# Main Workspace Execution
if src_file and ref_file and src_file.exists() and ref_file.exists():
    try:
        rec_src = load_lunar_image(src_file)
        rec_ref = load_lunar_image(ref_file)
    except Exception as e:
        st.error(f"Error reading lunar imagery: {e}")
        st.stop()

    # Pre-execution Telemetry Headers
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown(f"""
        <div class="section-box">
            <div class="section-title">SOURCE IMAGE TELEMETRY</div>
            <b>File:</b> <code>{rec_src.file_path.name}</code><br>
            <b>Sensor:</b> <code>{rec_src.sensor}</code> ({rec_src.resolution_m or 'N/A'} m/px GSD)<br>
            <b>Dimensions:</b> <code>{rec_src.image_uint8.shape[1]} x {rec_src.image_uint8.shape[0]} px</code><br>
            <b>Provenance:</b> <span class="{ 'tag-verified' if rec_src.provenance == DataProvenance.VERIFIED_CHANDRAYAAN else 'tag-derived' }">{rec_src.provenance.value}</span><br>
            <small>{rec_src.provenance_details}</small>
        </div>
        """, unsafe_allow_html=True)

    with col_t2:
        st.markdown(f"""
        <div class="section-box">
            <div class="section-title">REFERENCE IMAGE TELEMETRY</div>
            <b>File:</b> <code>{rec_ref.file_path.name}</code><br>
            <b>Sensor:</b> <code>{rec_ref.sensor}</code> ({rec_ref.resolution_m or 'N/A'} m/px GSD)<br>
            <b>Dimensions:</b> <code>{rec_ref.image_uint8.shape[1]} x {rec_ref.image_uint8.shape[0]} px</code><br>
            <b>Provenance:</b> <span class="{ 'tag-verified' if rec_ref.provenance == DataProvenance.VERIFIED_CHANDRAYAAN else 'tag-derived' }">{rec_ref.provenance.value}</span><br>
            <small>{rec_ref.provenance_details}</small>
        </div>
        """, unsafe_allow_html=True)

    # If run triggered or in session state
    if btn_run or "last_output" in st.session_state:
        if btn_run:
            with st.spinner("Executing multi-stage lunar image registration pipeline on real Chandrayaan-2 data..."):
                output = run_registration_pipeline(
                    source_path=rec_src,
                    reference_path=rec_ref,
                    method=matcher_choice,
                    preprocessing=prep_choice,
                    model_type=model_choice,
                    robust_estimator=estimator_choice,
                    enforce_spatial_coverage=enforce_spatial,
                    min_coverage_ratio=min_coverage_pct / 100.0,
                    subpixel_enabled=enable_subpixel,
                    reproj_thresh=reproj_slider,
                )
                st.session_state["last_output"] = output
        else:
            output = st.session_state["last_output"]

        rep = output.quality_report

        # Status Alert
        if output.success:
            st.success(f"✅ **REGISTRATION SUCCESSFUL** — Geometric model verified under {model_choice.upper()} with {estimator_choice}.")
        else:
            st.error(f"❌ **{rep.status}**: {rep.failure_reason}")

        # Metrics HUD Row
        st.markdown("### 📊 REAL-TIME QUANTITATIVE EVALUATION HUD")
        m_c1, m_c2, m_c3, m_c4, m_c5, m_c6 = st.columns(6)

        with m_c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Inlier Count</div>
                <div class="metric-value">{rep.inlier_match_count}</div>
                <div class="metric-badge-success">{rep.inlier_ratio * 100.0:.1f}% ratio</div>
            </div>
            """, unsafe_allow_html=True)

        with m_c2:
            rmse_c_str = f"{rep.reprojection_rmse_coarse:.3f} px" if rep.reprojection_rmse_coarse != float("inf") else "N/A"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Coarse RMSE</div>
                <div class="metric-value">{rmse_c_str}</div>
                <div class="metric-badge-success">Reprojection</div>
            </div>
            """, unsafe_allow_html=True)

        with m_c3:
            rmse_r_str = f"{rep.reprojection_rmse_refined:.3f} px" if rep.reprojection_rmse_refined != float("inf") else "N/A"
            delta_str = f"{rep.delta_rmse:+.3f} px"
            badge_class = "metric-badge-success" if rep.subpixel_improved else "metric-badge-caution"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Refined RMSE</div>
                <div class="metric-value">{rmse_r_str}</div>
                <div class="{badge_class}">Δ: {delta_str}</div>
            </div>
            """, unsafe_allow_html=True)

        with m_c4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Spatial Coverage</div>
                <div class="metric-value">{rep.spatial_coverage_percent:.1f}%</div>
                <div class="metric-badge-success">{rep.occupied_cells}/{rep.total_cells} cells</div>
            </div>
            """, unsafe_allow_html=True)

        with m_c5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Photometric NCC</div>
                <div class="metric-value">{rep.photometric_ncc:.3f}</div>
                <div class="metric-badge-success">Overlap consistency</div>
            </div>
            """, unsafe_allow_html=True)

        with m_c6:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Wall Runtime</div>
                <div class="metric-value">{output.total_runtime_sec:.2f}s</div>
                <div class="metric-badge-success">{matcher_choice}</div>
            </div>
            """, unsafe_allow_html=True)

        st.caption(
            "⚠️ **Scientific Evaluation Definition**: Reprojection RMSE represents mathematical reprojection residual "
            "on verified inlier keypoints under the estimated transformation model, not absolute geodetic lunar surface positioning accuracy."
        )

        st.markdown("---")

        # Three-Panel Visualizer
        st.markdown("### 🔭 MISSION VISUALIZATION SUITE")
        v_tab1, v_tab2, v_tab3, v_tab4 = st.tabs([
            "Correspondences (Raw vs Inliers)",
            "Interactive Before/After Swipe",
            "Checkerboard Edge Alignment",
            "Difference Heatmap"
        ])

        with v_tab1:
            st.image(
                output.visualization_matches,
                caption=f"Feature Matches: Raw={rep.raw_match_count}, Inliers={rep.inlier_match_count} (Green=Inliers, Red=Outliers)",
                width="stretch"
            )

        with v_tab2:
            st.markdown("##### Interactive Split Swipe Comparison (Source/Warped vs Reference)")
            split_slider = st.slider("Swipe Divider Position", 0.0, 1.0, 0.5, 0.02)
            comp_img = create_split_slider_composite(rec_ref.image_uint8, output.warped_image, split_ratio=split_slider)
            st.image(comp_img, caption=f"Split View: Left=Warped Registered Source, Right=Reference Image ({int(split_slider*100)}% split)", width="stretch")

        with v_tab3:
            st.image(
                output.visualization_checkerboard,
                caption="Checkerboard Alternation between Reference and Warped Image (inspect crater rim continuity)",
                width="stretch"
            )

        with v_tab4:
            st.image(
                output.visualization_difference,
                caption="Absolute Difference Heatmap (Blue=Zero Residual Alignment, Red=Residual Discrepancy)",
                width="stretch"
            )

        # Export Suite
        st.markdown("---")
        st.markdown("### 💾 EXPORT SUITE")
        exp_c1, exp_c2, exp_c3, exp_c4 = st.columns(4)

        # 1. Registered Image Export
        is_success, buf_img = cv2.imencode(".png", output.warped_image)
        with exp_c1:
            st.download_button(
                label="📥 Download Registered Image",
                data=buf_img.tobytes() if is_success else b"",
                file_name=f"registered_{rec_src.file_path.stem}_to_{rec_ref.file_path.stem}.png",
                mime="image/png"
            )

        # 2. Match Visualization Export
        is_success_vis, buf_vis = cv2.imencode(".png", output.visualization_matches)
        with exp_c2:
            st.download_button(
                label="📥 Download Match Plot",
                data=buf_vis.tobytes() if is_success_vis else b"",
                file_name=f"matches_{rec_src.file_path.stem}_to_{rec_ref.file_path.stem}.png",
                mime="image/png"
            )

        # 3. Metrics JSON Export
        json_data = json.dumps(output.quality_report.to_dict(), indent=2)
        with exp_c3:
            st.download_button(
                label="📥 Download Metrics JSON",
                data=json_data,
                file_name=f"metrics_{rec_src.file_path.stem}_to_{rec_ref.file_path.stem}.json",
                mime="application/json"
            )

        # 4. Processing Summary Report
        report_text = f"""================================================================================
CHANDRAYAAN-2 LUNAR IMAGE REGISTRATION REPORT (SIH26166)
Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}
================================================================================
INPUT TELEMETRY:
Source File:       {rec_src.file_path.name} ({rec_src.sensor}, {rec_src.provenance.value})
Reference File:    {rec_ref.file_path.name} ({rec_ref.sensor}, {rec_ref.provenance.value})
Source Shape:      {rec_src.image_uint8.shape}
Reference Shape:   {rec_ref.image_uint8.shape}

ALGORITHM PARAMETERS:
Matcher:           {matcher_choice}
Preprocessing:     {prep_choice}
Geometry Model:    {model_choice}
Robust Estimator:  {estimator_choice} (Reproj Threshold: {reproj_slider} px)
Spatial Filter:    Grid 8x8 (Min Coverage: {min_coverage_pct}%)
Sub-Pixel:         {enable_subpixel}

REGISTRATION RESULTS:
Status:            {rep.status}
Diagnostic:        {rep.failure_reason or 'None (Clean Convergence)'}
Raw Matches:       {rep.raw_match_count}
Inlier Count:      {rep.inlier_match_count}
Inlier Ratio:      {rep.inlier_ratio * 100.0:.2f}%
Coarse Reproj RMSE:{rep.reprojection_rmse_coarse:.4f} px
Refined Reproj RMSE:{rep.reprojection_rmse_refined:.4f} px
Delta RMSE:        {rep.delta_rmse:+.4f} px
Spatial Coverage:  {rep.spatial_coverage_percent:.2f}%
Grid Occupancy:    {rep.grid_occupancy_percent:.2f}% ({rep.occupied_cells}/{rep.total_cells} cells)
Condition Number:  {rep.condition_number:.2e}
Model Stable:      {rep.is_stable}
Photometric NCC:   {rep.photometric_ncc:.4f}
Runtime:           {output.total_runtime_sec:.4f} seconds

DISCLAIMER:
{rep.error_type_label}: Evaluated on verified inlier keypoints.
================================================================================
"""
        with exp_c4:
            st.download_button(
                label="📥 Download Processing Report (TXT)",
                data=report_text,
                file_name=f"report_{rec_src.file_path.stem}_to_{rec_ref.file_path.stem}.txt",
                mime="text/plain"
            )

    else:
        st.info("👆 Click **'EXECUTE REGISTRATION PIPELINE'** in the sidebar to process the selected Chandrayaan-2 imagery.")

else:
    st.warning("Real Chandrayaan-2 imagery required. Please provide OHRC/TMC/IIRS data in the documented format.")
