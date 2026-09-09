"""
Generate ALL high-quality visuals for SIH26166 Presentation.
These images should be drag-and-dropped into Canva / Google Slides / PowerPoint.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from pathlib import Path

OUT = Path(r"C:\Users\sarthak shavarn\OneDrive\Desktop\New folder\ISRO\ppt_visuals")
OUT.mkdir(parents=True, exist_ok=True)

# ── Theme ──
BG = '#0B1120'
CARD = '#151D30'
CYAN = '#00E5FF'
ORANGE = '#F16A21'
GREEN = '#00C853'
RED = '#FF5252'
YELLOW = '#FFB142'
TEAL = '#33D9B2'
BLUE = '#34ACE0'
WHITE = '#FFFFFF'
GRAY = '#999999'
LIGHT_GRAY = '#CCCCCC'


def save(fig, name):
    p = OUT / f'{name}.png'
    fig.savefig(p, dpi=250, bbox_inches='tight', facecolor=fig.get_facecolor(),
                pad_inches=0.3)
    plt.close(fig)
    print(f"  Saved: {p.name} ({p.stat().st_size//1024} KB)")


# ═══════════════════════════════════════════════════════════════
# 1. SYSTEM ARCHITECTURE DIAGRAM (Professional Layered)
# ═══════════════════════════════════════════════════════════════
def gen_architecture():
    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Title
    ax.text(7, 8.6, 'CHANDRA-ALIGN  |  System Architecture', ha='center',
            fontsize=20, fontweight='bold', color=CYAN, family='sans-serif')
    ax.plot([1, 13], [8.35, 8.35], color=ORANGE, linewidth=2)

    # ── Layer 1: Data Ingestion ──
    y = 7.2
    box = FancyBboxPatch((0.5, y), 13, 0.9, boxstyle="round,pad=0.1",
                          facecolor='#1a2744', edgecolor=CYAN, linewidth=1.5)
    ax.add_patch(box)
    ax.text(7, y+0.45, 'DATA INGESTION LAYER', ha='center', va='center',
            fontsize=13, fontweight='bold', color=WHITE)

    # Sub-boxes in layer 1
    for i, (label, col) in enumerate([
        ('OHRC\n(25 cm/px)', BLUE), ('TMC-2\n(5 m/px)', TEAL), ('IIRS\n(Spectral)', YELLOW),
        ('PDS4 / XML\nParser', ORANGE)
    ]):
        x = 1.5 + i * 3.1
        box = FancyBboxPatch((x, y-0.9), 2.5, 0.75, boxstyle="round,pad=0.08",
                              facecolor=col+'22', edgecolor=col, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x+1.25, y-0.52, label, ha='center', va='center',
                fontsize=9, fontweight='bold', color=WHITE)

    # Arrow
    ax.annotate('', xy=(7, 5.5), xytext=(7, 6.15),
                arrowprops=dict(arrowstyle='->', color=CYAN, lw=2.5))

    # ── Layer 2: Preprocessing ──
    y2 = 4.8
    box = FancyBboxPatch((0.5, y2), 13, 0.9, boxstyle="round,pad=0.1",
                          facecolor='#1a2744', edgecolor=ORANGE, linewidth=1.5)
    ax.add_patch(box)
    ax.text(7, y2+0.45, 'ADAPTIVE PREPROCESSING', ha='center', va='center',
            fontsize=13, fontweight='bold', color=WHITE)

    for i, (label, col) in enumerate([
        ('CLAHE Shadow\nEnhancement', CYAN), ('Gradient Map\nExtraction', YELLOW),
        ('Multi-Scale\nPyramid', TEAL), ('16-bit to 8-bit\nNormalization', ORANGE)
    ]):
        x = 1.5 + i * 3.1
        box = FancyBboxPatch((x, y2-0.9), 2.5, 0.75, boxstyle="round,pad=0.08",
                              facecolor=col+'22', edgecolor=col, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x+1.25, y2-0.52, label, ha='center', va='center',
                fontsize=9, fontweight='bold', color=WHITE)

    # Arrow
    ax.annotate('', xy=(7, 3.1), xytext=(7, 3.75),
                arrowprops=dict(arrowstyle='->', color=CYAN, lw=2.5))

    # ── Layer 3: Feature Matching ──
    y3 = 2.4
    box = FancyBboxPatch((0.5, y3), 6, 0.9, boxstyle="round,pad=0.1",
                          facecolor='#1a2744', edgecolor=GREEN, linewidth=1.5)
    ax.add_patch(box)
    ax.text(3.5, y3+0.45, 'FEATURE MATCHING', ha='center', va='center',
            fontsize=13, fontweight='bold', color=WHITE)

    for i, (label, col) in enumerate([
        ('SIFT', BLUE), ('LoFTR', TEAL), ('LightGlue', YELLOW)
    ]):
        x = 1.0 + i * 2.0
        box = FancyBboxPatch((x, y3-0.8), 1.6, 0.65, boxstyle="round,pad=0.08",
                              facecolor=col+'22', edgecolor=col, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x+0.8, y3-0.48, label, ha='center', va='center',
                fontsize=10, fontweight='bold', color=WHITE)

    # ── Layer 3b: Robust Estimation ──
    box = FancyBboxPatch((7.0, y3), 6.5, 0.9, boxstyle="round,pad=0.1",
                          facecolor='#1a2744', edgecolor=RED, linewidth=1.5)
    ax.add_patch(box)
    ax.text(10.25, y3+0.45, 'ROBUST ESTIMATION & OUTPUT', ha='center', va='center',
            fontsize=13, fontweight='bold', color=WHITE)

    for i, (label, col) in enumerate([
        ('MAGSAC++', RED), ('SubPixel', ORANGE), ('Mosaic', GREEN)
    ]):
        x = 7.5 + i * 2.1
        box = FancyBboxPatch((x, y3-0.8), 1.7, 0.65, boxstyle="round,pad=0.08",
                              facecolor=col+'22', edgecolor=col, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x+0.85, y3-0.48, label, ha='center', va='center',
                fontsize=10, fontweight='bold', color=WHITE)

    # Connect Layer 3 parts
    ax.annotate('', xy=(7.0, y3+0.45), xytext=(6.5, y3+0.45),
                arrowprops=dict(arrowstyle='->', color=CYAN, lw=2))

    # ── Bottom: Key Results ──
    y4 = 0.3
    box = FancyBboxPatch((0.5, y4), 13, 0.9, boxstyle="round,pad=0.1",
                          facecolor=CYAN+'15', edgecolor=CYAN, linewidth=2)
    ax.add_patch(box)
    ax.text(7, y4+0.45,
            'VERIFIED:  1,329 SIFT inliers  |  4,683 LoFTR inliers  |  0.148 px RMSE  |  96.12% Coverage  |  0.16s Runtime',
            ha='center', va='center', fontsize=11, fontweight='bold', color=CYAN)

    save(fig, '01_system_architecture')


# ═══════════════════════════════════════════════════════════════
# 2. PIPELINE FLOWCHART (Step-by-step with arrows)
# ═══════════════════════════════════════════════════════════════
def gen_pipeline_flow():
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.axis('off')

    ax.text(7, 6.6, 'Processing Pipeline Flow', ha='center',
            fontsize=18, fontweight='bold', color=CYAN)
    ax.plot([2, 12], [6.35, 6.35], color=ORANGE, linewidth=1.5)

    steps = [
        ('Input Images\n(OHRC / TMC-2 / IIRS)', BLUE, 'PDS4 XML\nParsing'),
        ('CLAHE Shadow\nEnhancement', YELLOW, 'Adaptive\nHistogram'),
        ('Feature Detection\n& Matching', TEAL, 'SIFT / LoFTR\n/ LightGlue'),
        ('Spatial Grid\nFiltering', ORANGE, 'Uniformity\nCheck'),
        ('MAGSAC++ Robust\nEstimation', RED, 'Outlier\nRejection'),
        ('Sub-Pixel\nRefinement', GREEN, 'CornerSubPix'),
        ('Registered\nMosaic Output', CYAN, 'Aligned\nImage'),
    ]

    for i, (title, col, sub) in enumerate(steps):
        x = 1.0 + i * 1.8
        # Main box
        box = FancyBboxPatch((x-0.05, 3.5), 1.6, 1.8, boxstyle="round,pad=0.15",
                              facecolor=col+'20', edgecolor=col, linewidth=2)
        ax.add_patch(box)
        # Step number circle
        circle = plt.Circle((x+0.75, 5.6), 0.25, color=col, zorder=5)
        ax.add_patch(circle)
        ax.text(x+0.75, 5.6, str(i+1), ha='center', va='center',
                fontsize=12, fontweight='bold', color=WHITE, zorder=6)
        # Title
        ax.text(x+0.75, 4.7, title, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color=WHITE)
        # Subtitle
        ax.text(x+0.75, 3.9, sub, ha='center', va='center',
                fontsize=7.5, color=GRAY, style='italic')
        # Arrow to next
        if i < len(steps) - 1:
            ax.annotate('', xy=(x+1.65, 4.4), xytext=(x+1.55, 4.4),
                        arrowprops=dict(arrowstyle='->', color=CYAN, lw=2))

    # Bottom metrics
    metrics = [
        ('0.148 px', 'Best RMSE'),
        ('4,683', 'Max Inliers'),
        ('100%', 'Inlier Ratio'),
        ('96.12%', 'Coverage'),
        ('0.16s', 'Speed (SIFT)'),
    ]
    for i, (val, label) in enumerate(metrics):
        x = 1.5 + i * 2.4
        box = FancyBboxPatch((x, 0.8), 2.0, 1.4, boxstyle="round,pad=0.1",
                              facecolor=CARD, edgecolor='#333', linewidth=1)
        ax.add_patch(box)
        ax.text(x+1.0, 1.7, val, ha='center', va='center',
                fontsize=16, fontweight='bold', color=CYAN)
        ax.text(x+1.0, 1.15, label, ha='center', va='center',
                fontsize=9, color=GRAY)

    save(fig, '02_pipeline_flowchart')


# ═══════════════════════════════════════════════════════════════
# 3. BAR CHART: Inlier Count Comparison
# ═══════════════════════════════════════════════════════════════
def gen_inliers_chart():
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    methods = ['ORB', 'SuperPoint\n+ LightGlue', 'SIFT', 'LoFTR']
    vals    = [950, 770, 1329, 4683]
    colors  = [RED, YELLOW, BLUE, TEAL]

    bars = ax.bar(methods, vals, color=colors, width=0.55,
                  edgecolor='white', linewidth=0.6)

    for b in bars:
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+80,
                f'{int(b.get_height()):,}', ha='center', va='bottom',
                color=WHITE, fontweight='bold', fontsize=14)

    ax.set_ylabel('Verified Inlier Count', fontsize=13, fontweight='bold', color=WHITE)
    ax.set_title('Feature Matching Performance — Real Chandrayaan-2 Crater Data',
                 fontsize=15, fontweight='bold', color=WHITE, pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#444')
    ax.spines['bottom'].set_color('#444')
    ax.tick_params(colors=WHITE, labelsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.2, color='#555')

    save(fig, '03_inliers_comparison')


# ═══════════════════════════════════════════════════════════════
# 4. BAR CHART: RMSE Accuracy
# ═══════════════════════════════════════════════════════════════
def gen_rmse_chart():
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    methods = ['ORB', 'SuperPoint', 'LoFTR', 'SIFT']
    vals    = [1.054, 0.837, 0.263, 0.148]
    colors  = [RED, YELLOW, TEAL, BLUE]

    bars = ax.bar(methods, vals, color=colors, width=0.55,
                  edgecolor='white', linewidth=0.6)
    for b in bars:
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.02,
                f'{b.get_height():.3f} px', ha='center', va='bottom',
                color=WHITE, fontweight='bold', fontsize=13)

    ax.set_ylabel('Reprojection RMSE (pixels)', fontsize=13, fontweight='bold', color=WHITE)
    ax.set_title('Sub-Pixel Accuracy — Lower = Better',
                 fontsize=15, fontweight='bold', color=WHITE, pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#444')
    ax.spines['bottom'].set_color('#444')
    ax.tick_params(colors=WHITE, labelsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.2, color='#555')

    # Target line
    ax.axhline(y=0.5, color=GREEN, linestyle='--', linewidth=1.5, alpha=0.7)
    ax.text(3.5, 0.53, 'Target: <0.5 px', color=GREEN, fontsize=10, style='italic')

    save(fig, '04_rmse_accuracy')


# ═══════════════════════════════════════════════════════════════
# 5. GROUPED BAR: Preprocessing Comparison
# ═══════════════════════════════════════════════════════════════
def gen_preprocessing_comparison():
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    methods = ['SIFT', 'ORB', 'SuperPoint', 'LoFTR']
    clahe   = [1329, 950, 601, 4683]
    gradient= [287, 719, 770, 4691]
    raw     = [602, 714, 583, 4682]

    x = np.arange(len(methods))
    w = 0.25
    ax.bar(x - w, clahe, w, label='CLAHE', color=CYAN, edgecolor='white', linewidth=0.3)
    ax.bar(x, gradient, w, label='Gradient', color=ORANGE, edgecolor='white', linewidth=0.3)
    ax.bar(x + w, raw, w, label='Raw', color=TEAL, edgecolor='white', linewidth=0.3)

    ax.set_xticks(x)
    ax.set_xticklabels(methods)
    ax.set_ylabel('Inlier Count', fontsize=13, fontweight='bold', color=WHITE)
    ax.set_title('Preprocessing Impact on Feature Matching',
                 fontsize=15, fontweight='bold', color=WHITE, pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#444')
    ax.spines['bottom'].set_color('#444')
    ax.tick_params(colors=WHITE, labelsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.2, color='#555')
    ax.legend(facecolor=CARD, edgecolor='#555', labelcolor=WHITE, fontsize=11)

    save(fig, '05_preprocessing_comparison')


# ═══════════════════════════════════════════════════════════════
# 6. HORIZONTAL BAR: Runtime Speed
# ═══════════════════════════════════════════════════════════════
def gen_runtime():
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    methods = ['ORB + Gradient\n(Fastest)', 'SIFT + Raw', 'SIFT + CLAHE',
               'LoFTR + CLAHE', 'SuperPoint + Gradient', 'SuperPoint + CLAHE']
    times   = [0.044, 0.115, 0.162, 6.280, 7.621, 9.937]
    colors  = [GREEN, BLUE, CYAN, TEAL, YELLOW, RED]

    bars = ax.barh(methods, times, color=colors, height=0.5,
                   edgecolor='white', linewidth=0.3)
    for b in bars:
        ax.text(b.get_width()+0.15, b.get_y()+b.get_height()/2,
                f'{b.get_width():.3f}s', va='center', color=WHITE,
                fontweight='bold', fontsize=11)

    ax.set_xlabel('Execution Time (seconds)', fontsize=13, fontweight='bold', color=WHITE)
    ax.set_title('Processing Speed — Real-Time Capable',
                 fontsize=15, fontweight='bold', color=WHITE, pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#444')
    ax.spines['bottom'].set_color('#444')
    ax.tick_params(colors=WHITE, labelsize=10)
    ax.grid(axis='x', linestyle='--', alpha=0.2, color='#555')

    # Real-time zone
    ax.axvline(x=1.0, color=GREEN, linestyle='--', linewidth=1.5, alpha=0.7)
    ax.text(1.1, 5.3, 'Real-Time\nThreshold', color=GREEN, fontsize=9, style='italic')

    save(fig, '06_runtime_speed')


# ═══════════════════════════════════════════════════════════════
# 7. SPATIAL COVERAGE BAR
# ═══════════════════════════════════════════════════════════════
def gen_spatial():
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    methods = ['ORB', 'LoFTR', 'SuperPoint', 'SIFT']
    coverage = [92.22, 94.16, 95.32, 96.12]
    grid_occ = [87.50, 100.0, 100.0, 100.0]
    colors  = [RED, TEAL, YELLOW, BLUE]

    x = np.arange(len(methods))
    w = 0.3
    bars1 = ax.bar(x - w/2, coverage, w, label='Spatial Coverage %', color=colors,
                   edgecolor='white', linewidth=0.4)
    bars2 = ax.bar(x + w/2, grid_occ, w, label='Grid Occupancy %',
                   color=[c+'77' for c in colors], edgecolor='white', linewidth=0.4)

    ax.set_ylim(80, 105)
    ax.set_xticks(x)
    ax.set_xticklabels(methods)
    ax.set_ylabel('Percentage (%)', fontsize=13, fontweight='bold', color=WHITE)
    ax.set_title('Match Distribution Quality',
                 fontsize=15, fontweight='bold', color=WHITE, pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#444')
    ax.spines['bottom'].set_color('#444')
    ax.tick_params(colors=WHITE, labelsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.2, color='#555')
    ax.legend(facecolor=CARD, edgecolor='#555', labelcolor=WHITE, fontsize=11)

    for b in bars1:
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.3,
                f'{b.get_height():.1f}', ha='center', va='bottom',
                color=WHITE, fontweight='bold', fontsize=10)

    save(fig, '07_spatial_coverage')


# ═══════════════════════════════════════════════════════════════
# 8. TECH STACK BANNER
# ═══════════════════════════════════════════════════════════════
def gen_tech_stack():
    fig, ax = plt.subplots(figsize=(14, 2.5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 2.5)
    ax.axis('off')

    ax.text(7, 2.1, 'Technology Stack', ha='center',
            fontsize=16, fontweight='bold', color=CYAN)

    techs = [
        ('Python 3.11', BLUE), ('PyTorch', RED), ('OpenCV', GREEN),
        ('Kornia\n(LoFTR)', TEAL), ('LightGlue\n(ETH Zurich)', YELLOW),
        ('Streamlit', ORANGE), ('Docker', BLUE), ('PDS4/XML', GRAY)
    ]

    for i, (name, col) in enumerate(techs):
        x = 0.5 + i * 1.7
        box = FancyBboxPatch((x, 0.4), 1.4, 1.2, boxstyle="round,pad=0.1",
                              facecolor=col+'22', edgecolor=col, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x+0.7, 1.0, name, ha='center', va='center',
                fontsize=9, fontweight='bold', color=WHITE)

    save(fig, '08_tech_stack')


# ═══════════════════════════════════════════════════════════════
#  RUN ALL
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("Generating all SIH presentation visuals...\n")
    gen_architecture()
    gen_pipeline_flow()
    gen_inliers_chart()
    gen_rmse_chart()
    gen_preprocessing_comparison()
    gen_runtime()
    gen_spatial()
    gen_tech_stack()
    print(f"\nAll visuals saved to: {OUT}")
    print(f"Total files: {len(list(OUT.glob('*.png')))}")
    print("\nNext steps:")
    print("1. Open Canva (canva.com) -> Search 'Technology Presentation'")
    print("2. Pick a dark/professional template")
    print("3. Drag-and-drop these images into your slides")
    print("4. Add your text content around them")
