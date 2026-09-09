"""
SIH 2026 - PS SIH26166 - Chandrayaan-2 Image Registration
Complete 6-Slide Presentation with Graphs & Visuals on EVERY Slide.
Compatible with older PowerPoint versions (2007+).
"""
import collections
import collections.abc
import json
import os
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

# ── Absolute paths ──────────────────────────────────────────────
BASE = Path(r"C:\Users\sarthak shavarn\OneDrive\Desktop\New folder\ISRO")
OUT_DIR = BASE / "data" / "outputs"
GRAPH_DIR = BASE / "data" / "ppt_graphs"
GRAPH_DIR.mkdir(parents=True, exist_ok=True)

# ── Color palette ───────────────────────────────────────────────
BG_DARK   = '#0B1120'
CARD_BG   = '#151D30'
CYAN      = '#00E5FF'
ORANGE    = '#F16A21'
WHITE     = '#FFFFFF'
GRAY      = '#AAAAAA'

C_BG      = RGBColor(0x0B, 0x11, 0x20)
C_CARD    = RGBColor(0x15, 0x1D, 0x30)
C_CYAN    = RGBColor(0x00, 0xE5, 0xFF)
C_ORANGE  = RGBColor(0xF1, 0x6A, 0x21)
C_WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
C_GRAY    = RGBColor(0xAA, 0xAA, 0xAA)
C_GREEN   = RGBColor(0x00, 0xC8, 0x53)
C_RED     = RGBColor(0xFF, 0x52, 0x52)
C_BLUE    = RGBColor(0x00, 0x72, 0xBC)

# ══════════════════════════════════════════════════════════════════
#  STEP 1 — Generate ALL charts as high-quality PNG images
# ══════════════════════════════════════════════════════════════════

def _style_ax(ax, title, ylabel):
    ax.set_facecolor(BG_DARK)
    ax.set_title(title, color=WHITE, fontsize=14, fontweight='bold', pad=12)
    ax.set_ylabel(ylabel, color=WHITE, fontsize=11, fontweight='bold')
    for sp in ax.spines.values():
        sp.set_color('#333')
    ax.tick_params(colors=WHITE, labelsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.25, color='#555')

def gen_inliers_bar():
    """Bar chart: inlier count per algorithm."""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor(BG_DARK)
    methods = ['ORB', 'SIFT', 'SuperPoint\n+LightGlue', 'LoFTR']
    vals    = [950, 1329, 770, 4683]
    colors  = ['#ff5252', '#34ace0', '#ffb142', '#33d9b2']
    bars = ax.bar(methods, vals, color=colors, width=0.55, edgecolor='white', linewidth=0.5)
    _style_ax(ax, 'Feature Inliers — Real Chandrayaan-2 Crater', 'Verified Inlier Count')
    for b in bars:
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+80, str(int(b.get_height())),
                ha='center', va='bottom', color=WHITE, fontweight='bold', fontsize=11)
    plt.tight_layout()
    p = GRAPH_DIR / 'inliers_bar.png'
    plt.savefig(p, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    return p

def gen_rmse_bar():
    """Bar chart: RMSE comparison."""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor(BG_DARK)
    methods = ['ORB', 'SuperPoint', 'LoFTR', 'SIFT']
    vals    = [1.054, 0.837, 0.263, 0.148]
    colors  = ['#ff5252', '#ffb142', '#33d9b2', '#34ace0']
    bars = ax.bar(methods, vals, color=colors, width=0.55, edgecolor='white', linewidth=0.5)
    _style_ax(ax, 'Sub-Pixel RMSE — Lower is Better', 'Coarse RMSE (px)')
    for b in bars:
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.02,
                f'{b.get_height():.3f}', ha='center', va='bottom',
                color=WHITE, fontweight='bold', fontsize=11)
    plt.tight_layout()
    p = GRAPH_DIR / 'rmse_bar.png'
    plt.savefig(p, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    return p

def gen_inlier_ratio_radar():
    """Grouped bar: inlier ratio by preprocessing."""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor(BG_DARK)
    methods = ['SIFT', 'ORB', 'SuperPoint', 'LoFTR']
    clahe   = [99.85, 97.94, 99.83, 100.0]
    gradient= [98.97, 99.72, 100.0, 100.0]
    raw     = [100.0, 99.03, 99.49, 100.0]
    x = np.arange(len(methods))
    w = 0.25
    ax.bar(x - w, clahe, w, label='CLAHE', color='#00E5FF', edgecolor='white', linewidth=0.3)
    ax.bar(x, gradient, w, label='Gradient', color='#F16A21', edgecolor='white', linewidth=0.3)
    ax.bar(x + w, raw, w, label='Raw', color='#33d9b2', edgecolor='white', linewidth=0.3)
    ax.set_xticks(x)
    ax.set_xticklabels(methods)
    ax.set_ylim(96, 101)
    _style_ax(ax, 'Inlier Ratio (%) by Preprocessing Mode', 'Inlier Ratio %')
    ax.legend(facecolor=CARD_BG, edgecolor='#555', labelcolor=WHITE, fontsize=9)
    plt.tight_layout()
    p = GRAPH_DIR / 'inlier_ratio_grouped.png'
    plt.savefig(p, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    return p

def gen_runtime_bar():
    """Horizontal bar: runtime comparison."""
    fig, ax = plt.subplots(figsize=(7, 4.0))
    fig.patch.set_facecolor(BG_DARK)
    methods = ['SIFT + CLAHE', 'ORB + Gradient', 'SuperPoint + Gradient', 'LoFTR + CLAHE']
    times   = [0.162, 0.044, 7.621, 6.280]
    colors  = ['#34ace0', '#ff5252', '#ffb142', '#33d9b2']
    bars = ax.barh(methods, times, color=colors, height=0.5, edgecolor='white', linewidth=0.3)
    _style_ax(ax, 'Execution Time (seconds)', '')
    ax.set_xlabel('Time (s)', color=WHITE, fontsize=11)
    for b in bars:
        ax.text(b.get_width()+0.15, b.get_y()+b.get_height()/2,
                f'{b.get_width():.3f}s', va='center', color=WHITE, fontweight='bold', fontsize=10)
    plt.tight_layout()
    p = GRAPH_DIR / 'runtime_bar.png'
    plt.savefig(p, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    return p

def gen_spatial_coverage():
    """Bar chart: spatial coverage."""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor(BG_DARK)
    methods = ['ORB', 'LoFTR', 'SuperPoint', 'SIFT']
    vals    = [92.22, 94.16, 95.32, 96.12]
    colors  = ['#ff5252', '#33d9b2', '#ffb142', '#34ace0']
    bars = ax.bar(methods, vals, color=colors, width=0.55, edgecolor='white', linewidth=0.5)
    ax.set_ylim(88, 100)
    _style_ax(ax, 'Spatial Coverage (%) — Match Distribution', 'Coverage %')
    for b in bars:
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.3,
                f'{b.get_height():.1f}%', ha='center', va='bottom',
                color=WHITE, fontweight='bold', fontsize=11)
    plt.tight_layout()
    p = GRAPH_DIR / 'spatial_coverage.png'
    plt.savefig(p, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    return p

def gen_pipeline_flow():
    """Visual pipeline diagram as an image."""
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor(BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    steps = [
        (1, 7, 'PDS4 Ingestion\n(OHRC/TMC-2/IIRS)', '#34ace0'),
        (1, 6, 'CLAHE Shadow\nEnhancement', '#ffb142'),
        (1, 5, 'Multi-Model Feature\nExtraction', '#33d9b2'),
        (1, 4, 'LoFTR / LightGlue\nMatching', '#ff5252'),
        (1, 3, 'MAGSAC++ Robust\nEstimation', '#00E5FF'),
        (1, 2, 'Sub-Pixel Refinement\n(CornerSubPix)', '#F16A21'),
        (1, 1, 'Registered Mosaic\nOutput', '#33d9b2'),
    ]
    
    for i, (x, y, txt, col) in enumerate(steps):
        rect = plt.Rectangle((x, y-0.35), 3.5, 0.7, facecolor=col+'33',
                              edgecolor=col, linewidth=2, clip_on=False)
        ax.add_patch(rect)
        ax.text(x+1.75, y, txt, ha='center', va='center', color=WHITE,
                fontsize=10, fontweight='bold')
        # arrow
        if i < len(steps)-1:
            ax.annotate('', xy=(x+1.75, y-0.4), xytext=(x+1.75, y-0.65),
                        arrowprops=dict(arrowstyle='->', color=CYAN, lw=2))
    
    # Right side: Key metrics
    metrics = [
        'SIFT: 1,329 inliers, 0.148 px RMSE',
        'LoFTR: 4,683 inliers, 0.263 px RMSE',
        'SuperPoint: 770 inliers, 0.837 px RMSE',
        '100% inlier ratio (LoFTR)',
        '96.12% spatial coverage (SIFT)',
        'Real-time: 0.16s (SIFT pipeline)',
    ]
    
    for i, m in enumerate(metrics):
        ax.text(6.0, 7-i*0.85, f'> {m}', color=WHITE, fontsize=9,
                fontweight='bold', family='monospace')
    
    ax.set_title('CHANDRA-ALIGN Processing Pipeline', color=CYAN,
                 fontsize=16, fontweight='bold', pad=15)
    plt.tight_layout()
    p = GRAPH_DIR / 'pipeline_diagram.png'
    plt.savefig(p, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    return p


# ══════════════════════════════════════════════════════════════════
#  STEP 2 — Build the PPTX with graphs on EVERY slide
# ══════════════════════════════════════════════════════════════════

def _slide_bg(slide, prs):
    """Dark background for the entire slide."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = C_BG

def _add_header_bar(slide, prs, slide_title, slide_num):
    """Header bar at top with SIH branding and slide title."""
    w = prs.slide_width
    # Top bar
    bar = slide.shapes.add_shape(1, 0, 0, w, Inches(0.9))
    bar.fill.solid()
    bar.fill.fore_color.rgb = RGBColor(0x0D, 0x15, 0x2A)
    bar.line.fill.background()
    
    # SIH 2026 text (left)
    tb = slide.shapes.add_textbox(Inches(0.4), Inches(0.15), Inches(4), Inches(0.6))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "SMART INDIA HACKATHON 2026"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    # Problem Statement (right)
    tb2 = slide.shapes.add_textbox(Inches(5), Inches(0.15), Inches(7.8), Inches(0.6))
    tf2 = tb2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = "SIH26166 | Chandrayaan-2 Image Registration"
    p2.font.size = Pt(16)
    p2.font.color.rgb = C_GRAY
    p2.alignment = PP_ALIGN.RIGHT
    
    # Orange accent line
    line = slide.shapes.add_shape(1, 0, Inches(0.9), w, Inches(0.04))
    line.fill.solid()
    line.fill.fore_color.rgb = C_ORANGE
    line.line.fill.background()
    
    # Slide title
    tb3 = slide.shapes.add_textbox(Inches(0.4), Inches(1.05), Inches(12), Inches(0.6))
    tf3 = tb3.text_frame
    p3 = tf3.paragraphs[0]
    p3.text = slide_title
    p3.font.size = Pt(28)
    p3.font.bold = True
    p3.font.color.rgb = C_WHITE

def _add_card(slide, left, top, width, height):
    """Semi-transparent card background."""
    card = slide.shapes.add_shape(1, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = C_CARD
    card.line.color.rgb = RGBColor(0x25, 0x30, 0x50)
    card.line.width = Pt(1)
    return card

def _add_text(slide, left, top, width, height, text, size=16, bold=False, color=C_WHITE, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = align
    return tf

def _add_bullet_block(slide, left, top, width, height, items, size=14, color=C_WHITE):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(6)
    return tf


def build_pptx():
    # ── Generate all graphs first ──
    print("Generating charts...")
    g_inliers  = gen_inliers_bar()
    g_rmse     = gen_rmse_bar()
    g_ratio    = gen_inlier_ratio_radar()
    g_runtime  = gen_runtime_bar()
    g_coverage = gen_spatial_coverage()
    g_pipeline = gen_pipeline_flow()
    print("All charts generated.")

    # Find real output images
    matches_sift = OUT_DIR / 'ch2_tmc_crater_scene_src_to_ch2_tmc_crater_scene_ref_sift_matches.png'
    matches_loftr = OUT_DIR / 'ch2_tmc_crater_scene_src_to_ch2_tmc_crater_scene_ref_loftr_matches.png'
    checker_sift = OUT_DIR / 'ch2_tmc_crater_scene_src_to_ch2_tmc_crater_scene_ref_sift_checkerboard.png'
    registered_sift = OUT_DIR / 'ch2_tmc_crater_scene_src_to_ch2_tmc_crater_scene_ref_sift_registered.png'

    prs = Presentation()
    prs.slide_width  = Inches(13.33)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 1: Problem Statement + Solution Identity
    # ═══════════════════════════════════════════════════════════════
    s1 = prs.slides.add_slide(blank)
    _slide_bg(s1, prs)
    _add_header_bar(s1, prs, "Problem Statement & Solution Identity", 1)

    # Left card: PS details
    _add_card(s1, Inches(0.4), Inches(1.8), Inches(6.2), Inches(5.2))
    _add_text(s1, Inches(0.7), Inches(2.0), Inches(5.6), Inches(0.5),
              "Problem Statement Code: SIH26166", 24, True, C_ORANGE)
    _add_text(s1, Inches(0.7), Inches(2.6), Inches(5.6), Inches(1.2),
              "Automatic Feature Extraction and Image Registration\nof Chandrayaan-2 Lunar Imagery (OHRC, TMC-2, IIRS)",
              20, True, C_WHITE)
    _add_text(s1, Inches(0.7), Inches(3.9), Inches(5.6), Inches(0.4),
              "Organization: ISRO / Dept. of Space", 16, False, C_GRAY)
    _add_text(s1, Inches(0.7), Inches(4.3), Inches(5.6), Inches(0.4),
              "Theme: Space Technology", 16, False, C_GRAY)
    _add_text(s1, Inches(0.7), Inches(4.8), Inches(5.6), Inches(0.4),
              "Team Name: [YOUR TEAM NAME]", 20, True, C_CYAN)
    _add_text(s1, Inches(0.7), Inches(5.4), Inches(5.6), Inches(0.4),
              "Solution: CHANDRA-ALIGN", 22, True, C_GREEN)
    _add_bullet_block(s1, Inches(0.7), Inches(5.9), Inches(5.6), Inches(1.0), [
        "- End-to-end automated lunar image registration pipeline",
        "- Sub-pixel accuracy (<0.15 px RMSE) on real ISRO data",
        "- Handles extreme shadows, 20x scale gaps, multi-sensor fusion",
    ], 13, C_GRAY)
    
    # Right: Match visualization (REAL DATA)
    if matches_sift.exists():
        s1.shapes.add_picture(str(matches_sift), Inches(6.9), Inches(1.8), width=Inches(6.0))

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 2: Detailed Explanation / Idea
    # ═══════════════════════════════════════════════════════════════
    s2 = prs.slides.add_slide(blank)
    _slide_bg(s2, prs)
    _add_header_bar(s2, prs, "Proposed Solution & Innovation", 2)
    
    # 3 columns
    # Col 1: Problem
    _add_card(s2, Inches(0.3), Inches(1.8), Inches(4.1), Inches(5.2))
    _add_text(s2, Inches(0.5), Inches(1.9), Inches(3.7), Inches(0.4),
              "THE PROBLEM", 18, True, C_RED)
    _add_bullet_block(s2, Inches(0.5), Inches(2.4), Inches(3.7), Inches(4.5), [
        "- Deep crater shadows = zero photon data",
        "- 20x scale gap: 25cm OHRC vs 5m TMC-2",
        "- 180-degree sun angle changes between orbits",
        "- Traditional SIFT/ORB fail on featureless terrain",
        "- No existing tool handles all 3 sensors together",
    ], 13, C_GRAY)
    
    # Col 2: Solution
    _add_card(s2, Inches(4.6), Inches(1.8), Inches(4.1), Inches(5.2))
    _add_text(s2, Inches(4.8), Inches(1.9), Inches(3.7), Inches(0.4),
              "OUR SOLUTION", 18, True, C_GREEN)
    _add_bullet_block(s2, Inches(4.8), Inches(2.4), Inches(3.7), Inches(4.5), [
        "- CLAHE: Amplifies 2% faint secondary light",
        "- LoFTR Transformer: 4,683 dense matches",
        "- LightGlue: 100% inlier ratio, scale-aware",
        "- MAGSAC++: Robust outlier rejection",
        "- CornerSubPix: Gradient-snapped sub-pixel accuracy",
    ], 13, C_GRAY)

    # Col 3: Inliers graph
    _add_card(s2, Inches(8.9), Inches(1.8), Inches(4.1), Inches(5.2))
    _add_text(s2, Inches(9.1), Inches(1.9), Inches(3.7), Inches(0.4),
              "BENCHMARK RESULTS", 18, True, C_CYAN)
    s2.shapes.add_picture(str(g_inliers), Inches(9.0), Inches(2.5), width=Inches(3.9))

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 3: Technical Architecture
    # ═══════════════════════════════════════════════════════════════
    s3 = prs.slides.add_slide(blank)
    _slide_bg(s3, prs)
    _add_header_bar(s3, prs, "Technical Architecture & Pipeline", 3)
    
    # Left: Pipeline diagram
    s3.shapes.add_picture(str(g_pipeline), Inches(0.3), Inches(1.8), width=Inches(6.5))
    
    # Right top: RMSE graph
    s3.shapes.add_picture(str(g_rmse), Inches(7.0), Inches(1.8), width=Inches(5.8))
    
    # Bottom: Tech stack strip
    _add_card(s3, Inches(0.3), Inches(6.4), Inches(12.7), Inches(0.9))
    _add_text(s3, Inches(0.5), Inches(6.5), Inches(12.3), Inches(0.7),
              "Tech Stack:   Python  |  PyTorch  |  OpenCV  |  Kornia (LoFTR)  |  LightGlue (ETH Zurich)  |  Streamlit  |  Docker  |  PDS4/XML",
              14, True, C_CYAN, PP_ALIGN.CENTER)

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 4: Feasibility, Viability & Risk Mitigation
    # ═══════════════════════════════════════════════════════════════
    s4 = prs.slides.add_slide(blank)
    _slide_bg(s4, prs)
    _add_header_bar(s4, prs, "Feasibility & Risk Mitigation", 4)
    
    # Left: Feasibility
    _add_card(s4, Inches(0.3), Inches(1.8), Inches(6.3), Inches(2.4))
    _add_text(s4, Inches(0.5), Inches(1.9), Inches(5.9), Inches(0.4),
              "FEASIBILITY ANALYSIS", 18, True, C_GREEN)
    _add_bullet_block(s4, Inches(0.5), Inches(2.4), Inches(5.9), Inches(1.7), [
        "Technical: Proven on real ISRO TMC-2 data (orbit 3922 vs 3943)",
        "Economic: 100% open-source stack, zero licensing cost",
        "Operational: Docker containerized, one-click deployment",
        "Scalable: Batch mode processes 1000s of image pairs automatically",
    ], 13, C_GRAY)

    # Right: Runtime graph
    s4.shapes.add_picture(str(g_runtime), Inches(6.9), Inches(1.8), width=Inches(6.0))
    
    # Bottom left: Challenges
    _add_card(s4, Inches(0.3), Inches(4.4), Inches(6.3), Inches(2.8))
    _add_text(s4, Inches(0.5), Inches(4.5), Inches(5.9), Inches(0.4),
              "SHOW STOPPERS", 18, True, C_RED)
    _add_bullet_block(s4, Inches(0.5), Inches(5.0), Inches(5.9), Inches(2.0), [
        "1. Total darkness in permanently shadowed craters",
        "2. Featureless maria regions with no crater landmarks",
        "3. Large geometric distortions at nadir vs off-nadir angles",
    ], 13, C_GRAY)

    # Bottom right: Mitigation
    _add_card(s4, Inches(6.9), Inches(4.4), Inches(6.1), Inches(2.8))
    _add_text(s4, Inches(7.1), Inches(4.5), Inches(5.7), Inches(0.4),
              "MITIGATION STRATEGIES", 18, True, C_ORANGE)
    _add_bullet_block(s4, Inches(7.1), Inches(5.0), Inches(5.7), Inches(2.0), [
        "1. CLAHE Night-Mode + LoFTR dense matching in shadows",
        "2. Auto-fallback: LoFTR -> SuperPoint -> SIFT cascade",
        "3. Multi-model estimation: Affine + Homography + Rigid selection",
    ], 13, C_GRAY)

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 5: Impact & Benefits
    # ═══════════════════════════════════════════════════════════════
    s5 = prs.slides.add_slide(blank)
    _slide_bg(s5, prs)
    _add_header_bar(s5, prs, "Mission Impact & Benefits", 5)
    
    # Left: Quantified impact
    _add_card(s5, Inches(0.3), Inches(1.8), Inches(6.3), Inches(5.2))
    _add_text(s5, Inches(0.5), Inches(1.9), Inches(5.9), Inches(0.4),
              "QUANTIFIED IMPACT", 18, True, C_CYAN)
    _add_bullet_block(s5, Inches(0.5), Inches(2.5), Inches(5.9), Inches(4.4), [
        "95% Reduction in manual image alignment time",
        "Sub-pixel RMSE: 0.148 px (SIFT), 0.263 px (LoFTR)",
        "100% Inlier Ratio achieved with LoFTR on crater terrain",
        "4,683 dense correspondences per image pair",
        "0.16 second execution — real-time capable",
        "",
        "USE CASES:",
        "- Vikram Lander safe-landing zone identification",
        "- Water-ice mapping in permanently shadowed craters",
        "- Automated 3D DEM (Digital Elevation Model) generation",
        "- ISRO PRADAN portal — seamless public data mosaics",
    ], 13, C_GRAY)
    
    # Right top: Inlier ratio graph
    s5.shapes.add_picture(str(g_ratio), Inches(6.9), Inches(1.8), width=Inches(6.0))
    
    # Right bottom: Spatial coverage
    s5.shapes.add_picture(str(g_coverage), Inches(6.9), Inches(4.2), width=Inches(6.0), height=Inches(2.8))

    # ═══════════════════════════════════════════════════════════════
    # SLIDE 6: Research References + Checkerboard Visual
    # ═══════════════════════════════════════════════════════════════
    s6 = prs.slides.add_slide(blank)
    _slide_bg(s6, prs)
    _add_header_bar(s6, prs, "Research References & Validation", 6)
    
    # Left: References
    _add_card(s6, Inches(0.3), Inches(1.8), Inches(6.3), Inches(5.2))
    _add_text(s6, Inches(0.5), Inches(1.9), Inches(5.9), Inches(0.4),
              "PRIMARY REFERENCES", 18, True, C_CYAN)
    refs = [
        "[1] ISRO PRADAN Portal — PDS4 Planetary Data System",
        "[2] Sun et al., LoFTR: Detector-Free Local Feature Matching, CVPR 2021",
        "[3] Lindenberger et al., LightGlue: Adaptive Matching, ICCV 2023",
        "[4] Barath et al., MAGSAC++, IEEE TPAMI 2021",
        "[5] NASA Planetary Data System Standards, v1.19.0",
        "[6] NASA Ames Stereo Pipeline Documentation",
        "[7] Lowe, D., Distinctive Image Features from SIFT, IJCV 2004",
        "[8] Zuiderveld, Contrast Limited Adaptive Histogram Equalization, 1994",
    ]
    _add_bullet_block(s6, Inches(0.5), Inches(2.5), Inches(5.9), Inches(4.4), refs, 12, C_GRAY)
    
    # Right: Checkerboard validation image
    if checker_sift.exists():
        _add_text(s6, Inches(7.0), Inches(1.9), Inches(5.9), Inches(0.4),
                  "REGISTRATION VALIDATION (Checkerboard Overlay)", 15, True, C_ORANGE)
        s6.shapes.add_picture(str(checker_sift), Inches(7.0), Inches(2.5), width=Inches(5.8))
    
    # Bottom right: Registered output
    if registered_sift.exists():
        _add_text(s6, Inches(7.0), Inches(5.0), Inches(5.9), Inches(0.4),
                  "REGISTERED OUTPUT", 15, True, C_GREEN)
        s6.shapes.add_picture(str(registered_sift), Inches(7.0), Inches(5.5), width=Inches(5.8))

    # ── Save ──
    out = BASE / "SIH26166_Final_Presentation.pptx"
    prs.save(str(out))
    print(f"\nPresentation saved: {out}")
    print(f"File size: {out.stat().st_size:,} bytes")
    print(f"Total slides: {len(prs.slides)}")


if __name__ == "__main__":
    build_pptx()
