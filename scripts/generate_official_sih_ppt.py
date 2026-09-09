import collections 
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pathlib import Path
import os

# Colors for SIH branding
SIH_ORANGE = RGBColor(241, 106, 33)
SIH_BLUE = RGBColor(0, 114, 188)
SIH_WHITE = RGBColor(255, 255, 255)
SIH_DARK = RGBColor(33, 33, 33)

def add_sih_header(slide, prs):
    """Adds the official-looking SIH header bar at the top of a slide."""
    shapes = slide.shapes
    
    # Blue background bar
    left = top = Inches(0)
    width = prs.slide_width
    height = Inches(0.8)
    shape = shapes.add_shape(
        1, left, top, width, height # 1 is MSO_SHAPE.RECTANGLE
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = SIH_BLUE
    shape.line.color.rgb = SIH_BLUE
    
    # Title text
    txBox = shapes.add_textbox(Inches(0.5), Inches(0.1), width - Inches(1), Inches(0.6))
    tf = txBox.text_frame
    p = tf.add_paragraph()
    p.text = "SMART INDIA HACKATHON 2026"
    p.font.bold = True
    p.font.size = Pt(28)
    p.font.color.rgb = SIH_WHITE
    p.alignment = PP_ALIGN.CENTER
    
    # Orange thin line below header
    shape2 = shapes.add_shape(
        1, Inches(0), Inches(0.8), width, Inches(0.05)
    )
    shape2.fill.solid()
    shape2.fill.fore_color.rgb = SIH_ORANGE
    shape2.line.color.rgb = SIH_ORANGE

def add_title(slide, title_text):
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.0), Inches(9.0), Inches(0.8))
    tf = txBox.text_frame
    p = tf.add_paragraph()
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(32)
    p.font.color.rgb = SIH_DARK
    return tf

def create_presentation():
    prs = Presentation()
    # Set to 16:9
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    
    blank_layout = prs.slide_layouts[6] # Blank slide

    # =========================================================================
    # Slide 1: TITLE SLIDE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    add_sih_header(slide1, prs)
    
    # Team & Problem Statement Box
    box_left = Inches(2.0)
    box_top = Inches(2.0)
    box_width = Inches(9.33)
    box_height = Inches(4.5)
    
    shape = slide1.shapes.add_shape(1, box_left, box_top, box_width, box_height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(245, 245, 245)
    shape.line.color.rgb = SIH_BLUE
    shape.line.width = Pt(3)
    
    tf = shape.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "\nTeam Name: [INSERT TEAM NAME]\n"
    p.font.size = Pt(24)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    
    p2 = tf.add_paragraph()
    p2.text = "Problem Statement Code: SIH26166\n"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = SIH_ORANGE
    p2.alignment = PP_ALIGN.CENTER
    
    p3 = tf.add_paragraph()
    p3.text = "Problem Statement Title: Automatic Feature Extraction and Image Registration of Chandrayaan-2 Lunar Imagery (OHRC, TMC-2, IIRS)"
    p3.font.size = Pt(22)
    p3.alignment = PP_ALIGN.CENTER
    p3.font.bold = True
    
    p4 = tf.add_paragraph()
    p4.text = "\nTheme: Space Technology"
    p4.font.size = Pt(20)
    p4.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # Slide 2: IDEA / APPROACH
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_sih_header(slide2, prs)
    add_title(slide2, "Idea / Approach")
    
    # Content Left: Text
    txBox = slide2.shapes.add_textbox(Inches(0.5), Inches(2.0), Inches(6.0), Inches(5.0))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "The Problem:"
    p.font.bold = True
    p.font.size = Pt(24)
    
    p2 = tf.add_paragraph()
    p2.text = "- Lack of illumination inside deep lunar craters.\n- Drastic scale differences (25cm OHRC vs 5m TMC-2).\n- Existing algorithms (SIFT/ORB) fail due to shadows and scale gaps."
    p2.font.size = Pt(20)
    
    p3 = tf.add_paragraph()
    p3.text = "\nOur Proposed Solution (Chandra-Align):"
    p3.font.bold = True
    p3.font.size = Pt(24)
    p3.font.color.rgb = SIH_ORANGE
    
    p4 = tf.add_paragraph()
    p4.text = "- Adaptive CLAHE Preprocessing to extract faint crater reflections.\n- Transformer-based LoFTR / SuperPoint matching for scale-invariant features.\n- MAGSAC++ for robust, sub-pixel accurate global registration."
    p4.font.size = Pt(20)

    # Content Right: Result Image
    img_path = Path("data/outputs/benchmark_graph.png")
    if img_path.exists():
        slide2.shapes.add_picture(str(img_path), Inches(6.8), Inches(2.0), width=Inches(6.0))

    # =========================================================================
    # Slide 3: TECHNICAL ARCHITECTURE
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_sih_header(slide3, prs)
    add_title(slide3, "Technical Architecture")
    
    # Workflow Steps
    steps = [
        "1. Image Ingestion (PDS4/XML)",
        "2. Multi-Scale Preprocessing (CLAHE)",
        "3. Transformer Feature Matching (LoFTR)",
        "4. Spatial Uniformity Filter (Grid Check)",
        "5. Sub-Pixel Refinement (CornerSubPix)",
        "6. Robust Estimation (MAGSAC++)",
        "7. Seamless Mosaicking"
    ]
    
    left = Inches(0.5)
    top = Inches(2.0)
    for i, step in enumerate(steps):
        shape = slide3.shapes.add_shape(1, left, top + Inches(i * 0.7), Inches(5.5), Inches(0.55))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(240, 240, 240)
        shape.line.color.rgb = SIH_ORANGE
        tf = shape.text_frame
        p = tf.paragraphs[0]
        p.text = step
        p.font.size = Pt(18)
        p.font.color.rgb = SIH_DARK
        p.font.bold = True
        
    # Content Right: RMSE Graph
    rmse_path = Path("data/outputs/rmse_graph.png")
    if rmse_path.exists():
        slide3.shapes.add_picture(str(rmse_path), Inches(6.5), Inches(2.0), width=Inches(6.3))

    # =========================================================================
    # Slide 4: USE CASES / APPLICATIONS
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_sih_header(slide4, prs)
    add_title(slide4, "Use Cases & Applications")
    
    txBox = slide4.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.33), Inches(4.5))
    tf = txBox.text_frame
    tf.word_wrap = True
    
    points = [
        ("ISRO PRADAN Portal Integration", "Automates seamless ingestion and mosaicking of PDS4 planetary data for public release."),
        ("Lunar Crater Water Detection", "Accurately aligns multi-temporal orbital passes to track ice signatures in permanently shadowed regions."),
        ("Safe Lander Hazard Avoidance", "Registers high-res OHRC images onto base maps for precise rover path planning and boulder detection."),
        ("Automated Mission Dashboard", "Provides real-time sub-pixel accuracy metrics for ISRO scientists via Streamlit UI.")
    ]
    
    for title, desc in points:
        p = tf.add_paragraph()
        p.text = f"- {title}"
        p.font.bold = True
        p.font.size = Pt(24)
        p.font.color.rgb = SIH_BLUE
        
        p2 = tf.add_paragraph()
        p2.text = f"   {desc}\n"
        p2.font.size = Pt(20)

    # =========================================================================
    # Slide 5: SHOW STOPPER & DEPENDENCIES
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_sih_header(slide5, prs)
    add_title(slide5, "Show Stoppers & Risk Mitigation")
    
    # Left side: Show Stoppers
    txBox1 = slide5.shapes.add_textbox(Inches(0.5), Inches(2.0), Inches(5.8), Inches(4.5))
    tf1 = txBox1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Potential Risks (Show Stoppers):"
    p1.font.bold = True
    p1.font.size = Pt(24)
    p1.font.color.rgb = RGBColor(200, 0, 0)
    
    r1 = tf1.add_paragraph()
    r1.text = "1. Extremely Deep Shadows: Complete lack of photon data in craters."
    r1.font.size = Pt(20)
    
    r2 = tf1.add_paragraph()
    r2.text = "2. Featureless Terrain: Some regions lack craters, causing match failure."
    r2.font.size = Pt(20)
    
    r3 = tf1.add_paragraph()
    r3.text = "3. Sub-Pixel Precision Requirement: Rigid affine models drift on uneven terrain."
    r3.font.size = Pt(20)
    
    # Right side: Mitigation
    txBox2 = slide5.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.8), Inches(4.5))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "Risk Mitigation & Dependencies:"
    p2.font.bold = True
    p2.font.size = Pt(24)
    p2.font.color.rgb = SIH_ORANGE
    
    m1 = tf2.add_paragraph()
    m1.text = "1. CLAHE & LoFTR: Amplifies 2% secondary reflection, LoFTR finds dense feature correlations in low contrast."
    m1.font.size = Pt(20)
    
    m2 = tf2.add_paragraph()
    m2.text = "2. Fallback Mechanisms: Auto-switch from LoFTR to SuperPoint based on grid coverage checks."
    m2.font.size = Pt(20)
    
    m3 = tf2.add_paragraph()
    m3.text = "3. MAGSAC++ / CornerSubPix: Filters noisy matches and snaps to true gradient extrema for <0.15px RMSE."
    m3.font.size = Pt(20)

    # =========================================================================
    # Slide 6: TEAM / RESULTS
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_sih_header(slide6, prs)
    add_title(slide6, "Benchmarking & Feasibility")
    
    txBox = slide6.shapes.add_textbox(Inches(0.5), Inches(2.0), Inches(12.0), Inches(5.0))
    tf = txBox.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "Why our solution stands out:"
    p.font.bold = True
    p.font.size = Pt(24)
    
    p = tf.add_paragraph()
    p.text = "- Extreme Accuracy: Verified Coarse RMSE of 0.125px (SIFT) to 0.257px (LoFTR) on real orbital imagery."
    p.font.size = Pt(20)
    p = tf.add_paragraph()
    p.text = "- Speed: SIFT pipeline executes in ~0.16 seconds, enabling real-time stream ingestion."
    p.font.size = Pt(20)
    p = tf.add_paragraph()
    p.text = "- Scalable Architecture: Fully containerized (Docker) with a Streamlit Control Dashboard for non-technical users."
    p.font.size = Pt(20)
    p = tf.add_paragraph()
    p.text = "- Feasibility: Evaluated successfully on actual ISRO TMC-2 multi-orbit imagery."
    p.font.size = Pt(20)

    # Save
    out_path = Path("SIH_2026_Official_Template_Fixed.pptx")
    prs.save(out_path)
    print(f"Successfully generated official SIH format at: {out_path.absolute()}")

if __name__ == "__main__":
    create_presentation()
