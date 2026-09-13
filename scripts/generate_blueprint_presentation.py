# -*- coding: utf-8 -*-
import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = Path(r"C:\Users\sarthak shavarn\OneDrive\Desktop\New folder\ISRO")
PPT_VISUALS = BASE_DIR / "ppt_visuals"
PUBLIC_IMAGES = BASE_DIR / "lunar-x" / "public" / "images"
OUTPUT_PPTX = BASE_DIR / "Homepage_Architecture_Blueprint.pptx"

# Template Colors (Strictly Preserved)
C_NAVY_BG       = RGBColor(24, 34, 75)      # #18224B Dark Cover/End Background
C_NAVY_CARD     = RGBColor(34, 48, 98)      # #223062 Card on Dark Background
C_NAVY_BORDER   = RGBColor(60, 80, 140)     # #3C508C Card Border on Dark Background
C_TEXT_WHITE    = RGBColor(255, 255, 255)   # White
C_TEXT_LIGHT    = RGBColor(200, 214, 235)   # Light Grayish Blue
C_ACCENT_BLUE   = RGBColor(0, 210, 255)     # #00D2FF Cyan Accent
C_ACCENT_ORANGE = RGBColor(241, 106, 33)    # #F16A21 ISRO Saffron
C_ACCENT_GREEN  = RGBColor(16, 185, 129)    # #10B981 Emerald Green

C_LIGHT_BG      = RGBColor(244, 246, 251)   # #F4F6FB Off-white / Silver canvas
C_BADGE_BG      = RGBColor(20, 28, 56)      # #141C38 Dark Navy Badge
C_CARD_BG       = RGBColor(255, 255, 255)   # Pure White Card
C_CARD_BORDER   = RGBColor(215, 224, 235)   # #D7E0EB Soft Border
C_TITLE_DARK    = RGBColor(20, 28, 56)      # #141C38 Dark Navy
C_SUBTITLE_GRAY = RGBColor(100, 116, 139)   # #64748B Slate Gray
C_BODY_DARK     = RGBColor(33, 43, 62)      # #212B3E Charcoal Dark
C_FOOTER_GRAY   = RGBColor(148, 163, 184)   # #94A3B8 Muted Slate

FONT_FAMILY = "Times New Roman"

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_slide():
        return prs.slides.add_slide(blank_layout)

    def draw_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()

    def draw_header(slide, badge_str, title_str, subtitle_str=None):
        # Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.42), Inches(0.65), Inches(0.65))
        badge.fill.solid()
        badge.fill.fore_color.rgb = C_BADGE_BG
        badge.line.fill.background()
        tf_b = badge.text_frame
        tf_b.clear()
        tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_b = tf_b.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        r_b = p_b.add_run()
        r_b.text = badge_str
        r_b.font.name = FONT_FAMILY
        r_b.font.size = Pt(22)
        r_b.font.bold = True
        r_b.font.color.rgb = C_TEXT_WHITE

        # Title
        tb_t = slide.shapes.add_textbox(Inches(1.6), Inches(0.38), Inches(11.0), Inches(0.42))
        tf_t = tb_t.text_frame
        tf_t.clear()
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        r_t = p_t.add_run()
        r_t.text = title_str
        r_t.font.name = FONT_FAMILY
        r_t.font.size = Pt(25)
        r_t.font.bold = True
        r_t.font.color.rgb = C_TITLE_DARK

        # Subtitle
        if subtitle_str:
            tb_s = slide.shapes.add_textbox(Inches(0.8), Inches(1.08), Inches(11.8), Inches(0.32))
            tf_s = tb_s.text_frame
            tf_s.clear()
            tf_s.word_wrap = True
            p_s = tf_s.paragraphs[0]
            r_s = p_s.add_run()
            r_s.text = subtitle_str
            r_s.font.name = FONT_FAMILY
            r_s.font.size = Pt(12.5)
            r_s.font.italic = True
            r_s.font.color.rgb = C_SUBTITLE_GRAY

    def draw_footer(slide, slide_num):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(10.0), Inches(0.35))
        tf = tb.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = "Agent Architecture Blueprint · fill in for your agent (Lunar-X Home Page)"
        r1.font.name = FONT_FAMILY
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_FOOTER_GRAY

        tb_num = slide.shapes.add_textbox(Inches(12.0), Inches(7.05), Inches(0.8), Inches(0.35))
        tf_num = tb_num.text_frame
        tf_num.clear()
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        r2 = p_num.add_run()
        r2.text = str(slide_num)
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_FOOTER_GRAY

    def draw_card(slide, left, top, width, height, title=None, subtitle=None, bg_color=C_CARD_BG, border_color=C_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)

        tb = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.1), width - Inches(0.36), height - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.clear()
        tf.margin_top = Inches(0.04)
        tf.margin_bottom = Inches(0.04)
        tf.margin_left = Inches(0.12)
        tf.margin_right = Inches(0.12)

        if title:
            p_t = tf.paragraphs[0]
            r_t = p_t.add_run()
            r_t.text = title
            r_t.font.name = FONT_FAMILY
            r_t.font.size = Pt(15)
            r_t.font.bold = True
            r_t.font.color.rgb = C_TITLE_DARK

            if subtitle:
                p_s = tf.add_paragraph()
                p_s.space_after = Pt(4)
                r_s = p_s.add_run()
                r_s.text = subtitle
                r_s.font.name = FONT_FAMILY
                r_s.font.size = Pt(11)
                r_s.font.italic = True
                r_s.font.color.rgb = C_SUBTITLE_GRAY

        return tf

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Dark Theme)
    # -------------------------------------------------------------
    s1 = add_slide()
    draw_background(s1, C_NAVY_BG)

    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(11.333), Inches(4.7))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_NAVY_CARD
    card1.line.color.rgb = C_NAVY_BORDER
    card1.line.width = Pt(1.5)

    tb1 = s1.shapes.add_textbox(Inches(1.4), Inches(1.6), Inches(10.533), Inches(3.9))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.clear()

    p = tf1.paragraphs[0]
    r = p.add_run()
    r.text = "AGENT ARCHITECTURE BLUEPRINT"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(36)
    r.font.bold = True
    r.font.color.rgb = C_TEXT_WHITE

    p = tf1.add_paragraph()
    p.space_before = Pt(14)
    r = p.add_run()
    r.text = "Reference presentation template — one deck (or section) per agent"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(18)
    r.font.color.rgb = C_TEXT_LIGHT

    p = tf1.add_paragraph()
    p.space_before = Pt(12)
    r = p.add_run()
    r.text = "Fill in each slide for the agent you own. Keep it tight — this is meant to make every agent comparable so we can agree on one standard playbook."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(14)
    r.font.italic = True
    r.font.color.rgb = C_TEXT_LIGHT

    p = tf1.add_paragraph()
    p.space_before = Pt(20)
    r = p.add_run()
    r.text = "Specific Agent Under Review: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(16)
    r.font.color.rgb = C_ACCENT_BLUE
    r = p.add_run()
    r.text = "Home Page & Core Registration Console (Lunar-X Chandrayaan-2)"
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(16)
    r.font.color.rgb = C_TEXT_WHITE

    tb_meta = s1.shapes.add_textbox(Inches(1.0), Inches(6.15), Inches(11.333), Inches(0.6))
    tf_meta = tb_meta.text_frame
    tf_meta.clear()
    p_m = tf_meta.paragraphs[0]

    for label, val in [("Agent: ", "Lunar-X Mission Console    "),
                      ("Owner: ", "Team Lunar X (SIH 2026 - PS 26166)    "),
                      ("Date: ", "September 2026")]:
        r = p_m.add_run()
        r.text = label
        r.font.name = FONT_FAMILY
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = C_TEXT_WHITE
        r2 = p_m.add_run()
        r2.text = val
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(13)
        r2.font.color.rgb = C_TEXT_LIGHT

    # -------------------------------------------------------------
    # SLIDE 2: What to cover
    # -------------------------------------------------------------
    s2 = add_slide()
    draw_background(s2, C_LIGHT_BG)
    draw_header(s2, "i", "What to cover", None)
    draw_footer(s2, 2)

    topics = [
        ("1", "Purpose & Scope", "What the home page does, who it's for"),
        ("2", "System Design", "Top-level architecture in the ecosystem"),
        ("3", "Prompt Design", "Direct JSON config, why text prompts aren't used"),
        ("4", "Language Model", "No text LLM; PyTorch deep vision models"),
        ("5", "APIs & Integrations", "FastAPI endpoints, PDS4 parser, OpenCV"),
        ("6", "Retrieval / RAG", "Spatial visual retrieval instead of text RAG"),
        ("7", "Data Flow", "Upload to preprocessed to registered GeoTIFF"),
        ("8", "Storage & State", "Transformation matrices, rasters, JSON metrics"),
        ("9", "Deployment", "Docker container, CPU readiness, env config"),
        ("10", "Compliance", "ISRO PDS4 standard, air-gapped security"),
        ("11", "Gaps, Risks & Open Items", "Shadow reversal, multi-scale, mobile view"),
        ("12", "Deviations", "Why Computer Vision beats LLMs for alignment")
    ]

    col_w = Inches(3.7)
    row_h = Inches(1.18)
    x_start = Inches(0.8)
    y_start = Inches(1.55)
    gap_x = Inches(0.35)
    gap_y = Inches(0.18)

    for idx, (num, t_title, t_desc) in enumerate(topics):
        r_idx = idx // 3
        c_idx = idx % 3
        x = x_start + c_idx * (col_w + gap_x)
        y = y_start + r_idx * (row_h + gap_y)

        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, col_w, row_h)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_CARD_BORDER
        card.line.width = Pt(1.1)

        pill = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.16), y + Inches(0.24), Inches(0.45), Inches(0.45))
        pill.fill.solid()
        pill.fill.fore_color.rgb = C_BADGE_BG
        pill.line.fill.background()
        tf_p = pill.text_frame
        tf_p.clear()
        p_p = tf_p.paragraphs[0]
        p_p.alignment = PP_ALIGN.CENTER
        rp = p_p.add_run()
        rp.text = num
        rp.font.name = FONT_FAMILY
        rp.font.size = Pt(14)
        rp.font.bold = True
        rp.font.color.rgb = C_TEXT_WHITE

        tb = s2.shapes.add_textbox(x + Inches(0.72), y + Inches(0.12), col_w - Inches(0.82), row_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.clear()
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = t_title
        r1.font.name = FONT_FAMILY
        r1.font.size = Pt(15)
        r1.font.bold = True
        r1.font.color.rgb = C_TITLE_DARK

        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = t_desc
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = C_SUBTITLE_GRAY

    # -------------------------------------------------------------
    # SLIDE 3: 1 Purpose & Scope
    # -------------------------------------------------------------
    s3 = add_slide()
    draw_background(s3, C_LIGHT_BG)
    draw_header(s3, "1", "Purpose & Scope", "In one or two sentences: what does this agent do, and who is it for?")
    draw_footer(s3, 3)

    tf3_top = draw_card(s3, Inches(0.8), Inches(1.45), Inches(11.733), Inches(2.25),
                        title="What does the Home Page do? (Simple Hindi / English Explanation)",
                        subtitle="Chandrayaan-2 multi-sensor lunar image matching mission console")

    points = [
        ("• Primary Purpose: ", "Ye Home Page Chandrayaan-2 ke alag-alag cameras (TMC-2, OHRC, IIRS) se li gayi Moon surface ki pictures ko aapas me 100% mathematically accurate match aur align (register) karne ka visual mission dashboard hai."),
        ("• Who is it for: ", "ISRO mission scientists, planetary researchers, aur GIS experts ke liye hai — jahan unhe complex terminal commands chalane ki jarurat nahi padti. Bas web screen par do images chuno ya upload karo, aur ek click me sub-pixel aligned result aur proof metrics screen par mil jaate hain."),
        ("• Core Philosophy: ", "Zero confusion, pure transparency. Har alignment run ka real mathematical error (RMSE in pixels), inliers count aur difference heatmap live proof ke roop me samne aata hai — koi black-box guessing nahi.")
    ]
    for p_title, p_desc in points:
        p = tf3_top.add_paragraph()
        p.space_before = Pt(4)
        r = p.add_run()
        r.text = p_title
        r.font.name = FONT_FAMILY
        r.font.bold = True
        r.font.size = Pt(13)
        r.font.color.rgb = C_TITLE_DARK
        r2 = p.add_run()
        r2.text = p_desc
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(12)
        r2.font.color.rgb = C_BODY_DARK

    tf3_bl = draw_card(s3, Inches(0.8), Inches(3.85), Inches(5.75), Inches(3.05),
                       title="Key user actions it supports",
                       subtitle="What a user can actually click and perform on the Home Page")

    actions = [
        ("Preset Crater Pair Selection: ", "Real Chandrayaan-2 benchmark pairs (Shackleton crater, sharp rims, terminator shadows) instantly load ho jaate hain."),
        ("Custom Image Upload: ", "User apne raw orbital GeoTIFF ya PNG images drag-and-drop karke upload kar sakta hai."),
        ("Algorithm & Light Selection: ", "Fast Classical (SIFT/ORB) ya Deep Transformer (LoFTR/SuperPoint) aur CLAHE enhancement select kar sakte hain."),
        ("Interactive Inspection: ", "Aligned image ko Matches view, Registered blend, Checkerboard slider, aur Difference heatmap me dekh sakte hain."),
        ("One-Click Mission Export: ", "Aligned GeoTIFF, PNG overlay, aur quantitative JSON verification report download kar sakte hain.")
    ]
    for act_title, act_desc in actions:
        p = tf3_bl.add_paragraph()
        p.space_before = Pt(3)
        r = p.add_run()
        r.text = "✔ " + act_title
        r.font.name = FONT_FAMILY
        r.font.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = C_TITLE_DARK
        r2 = p.add_run()
        r2.text = act_desc
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_BODY_DARK

    tf3_br = draw_card(s3, Inches(6.78), Inches(3.85), Inches(5.75), Inches(3.05),
                       title="Product area & status",
                       subtitle="Chandrayaan-2 Lunar Remote Sensing · SIH 2026 Problem 26166")

    status_items = [
        ("Domain & Platform: ", "Lunar Remote Sensing & Orbital Photogrammetry · Production Mission Console"),
        ("Compute Readiness: ", "Runs seamlessly on standard CPU (Laptop/Server); Optional GPU acceleration"),
        ("Benchmarked Accuracy: ", "0.148 px RMSE (SIFT) & 4,683 inliers (LoFTR) on Chandrayaan-2 data"),
        ("Verification & Tests: ", "20 automated Pytest verification test suites pass with 100% test coverage"),
        ("Strict Mission Data Policy: ", "100% Real Chandrayaan-2 orbital data (Zero mock or simulated data policy)")
    ]
    for s_title, s_desc in status_items:
        p = tf3_br.add_paragraph()
        p.space_before = Pt(3)
        r = p.add_run()
        r.text = "• " + s_title
        r.font.name = FONT_FAMILY
        r.font.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = C_TITLE_DARK
        r2 = p.add_run()
        r2.text = s_desc
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_BODY_DARK

    # -------------------------------------------------------------
    # SLIDE 4: 2 System Design (Top-Level)
    # -------------------------------------------------------------
    s4 = add_slide()
    draw_background(s4, C_LIGHT_BG)
    draw_header(s4, "2", "System Design (Top-Level)", "Top-level architecture: how does this agent fit into the broader platform? Show front end, API layer, vision engine & storage.")
    draw_footer(s4, 4)

    card4_img = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.45), Inches(6.8), Inches(5.45))
    card4_img.fill.solid()
    card4_img.fill.fore_color.rgb = C_CARD_BG
    card4_img.line.color.rgb = C_CARD_BORDER
    card4_img.line.width = Pt(1.2)

    sys_arch_img = PPT_VISUALS / "01_system_architecture.png"
    if sys_arch_img.exists():
        s4.shapes.add_picture(str(sys_arch_img), Inches(0.95), Inches(1.7), Inches(6.5), Inches(4.9))

    tf4_r = draw_card(s4, Inches(7.8), Inches(1.45), Inches(4.733), Inches(5.45),
                     title="System Layer Breakdown",
                     subtitle="Clean 3-Tier Architecture for High Reliability")

    layers = [
        ("1. Product UI (Next.js + Carbon Console)",
         "User-friendly web frontend hai. Preset selection, drag-and-drop file uploader, parameter toggles, live execution logs aur 4 visualization modes (Matches, Registered, Checkerboard, Difference) provide karta hai."),
        ("2. API Gateway (FastAPI Backend)",
         "High-performance Python asynchronous server (Port 8000). REST endpoints (`/api/register`, `/api/upload`, `/api/benchmark`) request receive karke processing engine ko delegate karte hain."),
        ("3. Adaptive Preprocessing Engine",
         "Moon surface par shadows ko handle karne ke liye CLAHE (Contrast Limited Adaptive Histogram Equalization) aur Sobel gradient filters lagata hai taaki sun illumination invariant feature detection ho."),
        ("4. Dual-Path Feature Matching Core",
         "• Fast Classical Route: SIFT / ORB (Runs in 0.16s on CPU)\n• Deep Learned Route: LoFTR transformer / SuperPoint (Extracts 4,680+ dense points on low-contrast terrain)."),
        ("5. Robust Geometry & Refinement Layer",
         "MAGSAC++ outlier rejection galat matches hatata hai, SVD stability check degenerate matrix rokta hai, aur cornerSubPix sub-pixel precision lata hai.")
    ]
    for l_title, l_desc in layers:
        p = tf4_r.add_paragraph()
        p.space_before = Pt(5)
        r = p.add_run()
        r.text = l_title
        r.font.name = FONT_FAMILY
        r.font.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = C_TITLE_DARK
        p_d = tf4_r.add_paragraph()
        r2 = p_d.add_run()
        r2.text = l_desc
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_BODY_DARK

    # -------------------------------------------------------------
    # SLIDE 5: 3 Prompt Design
    # -------------------------------------------------------------
    s5 = add_slide()
    draw_background(s5, C_LIGHT_BG)
    draw_header(s5, "3", "Prompt Design", "Paste the exact system / base prompt. Ideally show one worked example: a real assembled prompt for a sample user, before submittal.")
    draw_footer(s5, 5)

    tf5_top = draw_card(s5, Inches(0.8), Inches(1.45), Inches(11.733), Inches(2.45),
                       title="Direct Structured Execution Payload (No LLM Text Prompts Used)",
                       subtitle="Why natural language prompts are avoided for satellite geometric registration")

    p = tf5_top.add_paragraph()
    r = p.add_run()
    r.text = "Important Architectural Decision: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13.5)
    r.font.color.rgb = C_ACCENT_ORANGE
    r = p.add_run()
    r.text = "Is system me koi Text LLM Prompt use nahi hota — yahan direct structured API Execution Payload use hota hai. Image registration pure spatial coordinate geometry ka kaam hai. Text prompts use karne se AI coordinates hallucinate kar deta hai, jo scientific space mission ke liye dangerous hai. Isliye Home Page se direct JSON parameters dispatch hote hain:"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf5_top.add_paragraph()
    p.space_before = Pt(4)
    r = p.add_run()
    r.text = "Exact Assembled API Request Payload (Sent from Home Page to Vision Engine):"
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = C_TITLE_DARK

    p = tf5_top.add_paragraph()
    p.space_before = Pt(2)
    payload_str = '{\n  "source_filename": "ch2_tmc_crater_scene_src.png",    "reference_filename": "ch2_tmc_crater_scene_ref.png",\n  "method": "LoFTR",    "preprocessing": "clahe",    "model_type": "affine",\n  "subpixel": true,     "spatial_filter": true,     "reproj_thresh": 3.0\n}'
    r = p.add_run()
    r.text = payload_str
    r.font.name = "Courier New"
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(15, 23, 42)

    tf5_bl = draw_card(s5, Inches(0.8), Inches(4.02), Inches(5.75), Inches(2.92),
                      title="Payload Sections & Layout",
                      subtitle="Structured parameters defining exact registration behavior")

    sections = [
        ("Image Identifiers: ", "Source (moving image) aur Reference (fixed ground truth) file path ya uploaded image data."),
        ("Matcher Selection: ", "User toggle ke hisab se 'SIFT', 'ORB', 'LoFTR', ya 'SuperPoint+LightGlue' route activate hota hai."),
        ("Illumination Filter: ", "'clahe' (adaptive contrast equalization), 'gradient' (Sobel edge orientation), ya 'raw' representation."),
        ("Geometric Model: ", "'affine' (6 DOF - scale, rotation, shear, translation) ya 'homography' (8 DOF perspective)."),
        ("Refinement Flags: ", "'subpixel': true (gradient refinement) & 'spatial_filter': true (8x8 grid binning).")
    ]
    for sec_t, sec_d in sections:
        p = tf5_bl.add_paragraph()
        p.space_before = Pt(2.5)
        r = p.add_run()
        r.text = "• " + sec_t
        r.font.name = FONT_FAMILY
        r.font.bold = True
        r.font.size = Pt(11.5)
        r.font.color.rgb = C_TITLE_DARK
        r2 = p.add_run()
        r2.text = sec_d
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_BODY_DARK

    tf5_br = draw_card(s5, Inches(6.78), Inches(4.02), Inches(5.75), Inches(2.92),
                      title="Guardrails · Quality Tools · Output Schema",
                      subtitle="Strict validation prevents bad data and hallucinated transformations")

    guardrails = [
        ("Input Validation Guardrail: ", "PDS4 format, sensor type, and pixel dimension match checks ensure incompatible image pairs fail safely before processing."),
        ("Matrix SVD Condition Guardrail: ", "Condition number κ(A) <= 10^5 and det(A) > 0 enforce physical validity, completely preventing negative scale or surface collapse."),
        ("Sub-pixel Verification Gate: ", "Refinement tabhi accept hoti hai agar refined RMSE coarse RMSE se kam ho (ΔRMSE > 0); warna coarse transformation hi maintain hoti hai."),
        ("Output Response Schema: ", "Strict JSON response with exact numbers: inliers count, reprojection RMSE (px), coverage %, NCC score, and relative image URLs.")
    ]
    for g_t, g_d in guardrails:
        p = tf5_br.add_paragraph()
        p.space_before = Pt(2.5)
        r = p.add_run()
        r.text = "✔ " + g_t
        r.font.name = FONT_FAMILY
        r.font.bold = True
        r.font.size = Pt(11.5)
        r.font.color.rgb = C_TITLE_DARK
        r2 = p.add_run()
        r2.text = g_d
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_BODY_DARK

    # -------------------------------------------------------------
    # SLIDE 6: 4 Language Model (LLM)
    # -------------------------------------------------------------
    s6 = add_slide()
    draw_background(s6, C_LIGHT_BG)
    draw_header(s6, "4", "Language Model (LLM)", "Public LLM used · Access route / provider · Paid or free tier · Same LLM across all your agents?")
    draw_footer(s6, 6)

    card_w = Inches(5.75)
    card_h = Inches(2.65)
    x1, x2 = Inches(0.8), Inches(6.78)
    y1, y2 = Inches(1.45), Inches(4.25)

    tf6_1 = draw_card(s6, x1, y1, card_w, card_h,
                     title="Public LLM Used",
                     subtitle="exact model & version — e.g. Gemma 3 20B, MedGemma, GPT-4o, Claude")
    p = tf6_1.add_paragraph()
    r = p.add_run()
    r.text = "• No Text LLM Used (Pure Computer Vision): "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_ACCENT_ORANGE
    r = p.add_run()
    r.text = "Is system me koi text generation LLM use nahi hota kyunki satellite image registration ko mathematical coordinates chahiye, text answers nahi."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf6_1.add_paragraph()
    p.space_before = Pt(5)
    r = p.add_run()
    r.text = "• Deep Vision Neural Networks: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "LoFTR (Local Feature TRansformer with self/cross attention) & SuperPoint + LightGlue."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf6_1.add_paragraph()
    p.space_before = Pt(5)
    r = p.add_run()
    r.text = "• Classical Computer Vision Algorithms: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "SIFT (Scale-Invariant Feature Transform) & ORB (Oriented FAST and Rotated BRIEF) implemented via OpenCV."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    tf6_2 = draw_card(s6, x2, y1, card_w, card_h,
                     title="Access Route / Provider",
                     subtitle="e.g. OpenRouter (free tier), direct API, hosted")
    p = tf6_2.add_paragraph()
    r = p.add_run()
    r.text = "• 100% Local Self-Hosted Execution: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Saare vision models directly backend host machine par run hote hain through PyTorch and OpenCV C++ bindings."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf6_2.add_paragraph()
    p.space_before = Pt(6)
    r = p.add_run()
    r.text = "• Zero Cloud API Dependency: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Kisi external provider (OpenRouter, OpenAI, Hugging Face cloud) par koi dependency nahi hai. Pure standalone deployment hai."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf6_2.add_paragraph()
    p.space_before = Pt(6)
    r = p.add_run()
    r.text = "• Air-Gapped Ready for ISRO: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_ACCENT_GREEN
    r = p.add_run()
    r.text = "Ground station ya high-security satellite centers me bina internet connection ke bhi pipeline smoothly execute hoti hai."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    tf6_3 = draw_card(s6, x1, y2, card_w, card_h,
                     title="Paid or Free Tier",
                     subtitle="note any token / subscription requirement — e.g. OpenRouter needs paid tokens")
    p = tf6_3.add_paragraph()
    r = p.add_run()
    r.text = "• 100% Free & Open-Source (Zero Subscription): "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Zero per-token costs. Chahe 10 images match karo ya 10,000 gigapixel satellite strips, system ka koi API bill nahi banta."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf6_3.add_paragraph()
    p.space_before = Pt(6)
    r = p.add_run()
    r.text = "• Optimized for Commodity Hardware: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "SIFT + CLAHE CPU par sirf 0.16 seconds me execute ho jata hai. Iske liye expensive cloud A100 GPU rent karne ki bilkul jarurat nahi hai."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf6_3.add_paragraph()
    p.space_before = Pt(6)
    r = p.add_run()
    r.text = "• Sustainable for Space Missions: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Budget constraints ke bina continuous long-term space mission monitoring possible hai."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    tf6_4 = draw_card(s6, x2, y2, card_w, card_h,
                     title="Same Engine Across All Agents?",
                     subtitle="Yes / No — if no, list which agent uses what")
    p = tf6_4.add_paragraph()
    r = p.add_run()
    r.text = "• Yes — Unified Computer Vision Engine: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Home page interactive web console aur automated batch processing script dono ek hi standard engine (`src/pipeline.py`) share karte hain."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf6_4.add_paragraph()
    p.space_before = Pt(6)
    r = p.add_run()
    r.text = "• Adaptive Matcher Routing: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Terrain texture ke basis par system automatically best algorithm route karta hai: High-texture terrain ke liye Fast SIFT, aur low-contrast ya shadow-heavy terrain ke liye Deep LoFTR."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf6_4.add_paragraph()
    p.space_before = Pt(6)
    r = p.add_run()
    r.text = "• Consistent Playbook: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Ensures benchmark reproducibility across different sub-teams and planetary datasets."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    # -------------------------------------------------------------
    # SLIDE 7: 5 APIs & Integrations
    # -------------------------------------------------------------
    s7 = add_slide()
    draw_background(s7, C_LIGHT_BG)
    draw_header(s7, "5", "APIs & Integrations", "LLM integration API / SDK · External services · Authentication / keys")
    draw_footer(s7, 7)

    stack_w = Inches(11.733)
    stack_h = Inches(1.76)
    y_starts = [Inches(1.42), Inches(3.26), Inches(5.10)]

    tf7_1 = draw_card(s7, Inches(0.8), y_starts[0], stack_w, stack_h,
                     title="Engine Integration API / REST Endpoints",
                     subtitle="FastAPI Asynchronous Gateway bridging Next.js Frontend to Python Vision Core")
    bullets_7_1 = [
        ("• GET /api/health: ", "System connectivity check, returns active execution device (CPU / CUDA GPU), active algorithms, and server memory status."),
        ("• POST /api/register: ", "Runs complete alignment pipeline. Accepts JSON config and returns RMSE, inliers, spatial coverage, and generated visualization URLs."),
        ("• POST /api/upload & GET /api/benchmark: ", "Handles multipart custom satellite image uploads and serves cached verified benchmark table for SIFT, ORB, LoFTR, and SuperPoint.")
    ]
    for b_title, b_desc in bullets_7_1:
        p = tf7_1.add_paragraph()
        p.space_before = Pt(2)
        r = p.add_run()
        r.text = b_title
        r.font.name = FONT_FAMILY
        r.font.bold = True
        r.font.size = Pt(11.5)
        r.font.color.rgb = C_TITLE_DARK
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_BODY_DARK

    tf7_2 = draw_card(s7, Inches(0.8), y_starts[1], stack_w, stack_h,
                     title="External Services & Satellite Data Formats",
                     subtitle="ISRO Planetary Data System (PDS4), GDAL/Rasterio GeoTIFF, and OpenCV Vision Libs")
    bullets_7_2 = [
        ("• ISRO PDS4 Planetary Data System: ", "Direct parsing of official ISDA PDS4 XML labels, spacecraft attitude, and raw sensor binary arrays (`.img` / `.npz`)."),
        ("• GeoTIFF & GIS Georeferencing: ", "GDAL and Rasterio libraries lunar coordinate reference systems (Moon 2000 IAU ellipsoid) preserve karte hain taaki output GeoTIFF map-ready ho."),
        ("• Zero Third-Party SaaS: ", "Koi Twilio, LiveKit, 11Labs ya external cloud storage use nahi hota. Complete processing on-premise hoti hai.")
    ]
    for b_title, b_desc in bullets_7_2:
        p = tf7_2.add_paragraph()
        p.space_before = Pt(2)
        r = p.add_run()
        r.text = b_title
        r.font.name = FONT_FAMILY
        r.font.bold = True
        r.font.size = Pt(11.5)
        r.font.color.rgb = C_TITLE_DARK
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_BODY_DARK

    tf7_3 = draw_card(s7, Inches(0.8), y_starts[2], stack_w, stack_h,
                     title="Authentication / Secrets Management",
                     subtitle="Central environment configuration, zero personal accounts, secure mission operations")
    bullets_7_3 = [
        ("• Zero Paid API Keys Required: ", "Kyunki system 100% self-hosted open-source models use karta hai, kisi developer ko apni personal OpenAI ya cloud key dalne ki jarurat nahi hai."),
        ("• Central Configuration (.env): ", "Server ports, directory paths, and hardware flags central `.env` file se control hote hain (`PORT=8000`, `DEVICE=cpu`)."),
        ("• Enterprise Security Ready: ", "ISRO internal network deployment ke liye JWT / LDAP token authentication pluggable middleware ke roop me configured hai.")
    ]
    for b_title, b_desc in bullets_7_3:
        p = tf7_3.add_paragraph()
        p.space_before = Pt(2)
        r = p.add_run()
        r.text = b_title
        r.font.name = FONT_FAMILY
        r.font.bold = True
        r.font.size = Pt(11.5)
        r.font.color.rgb = C_TITLE_DARK
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_BODY_DARK

    # -------------------------------------------------------------
    # SLIDE 8: 6 Retrieval / RAG Components
    # -------------------------------------------------------------
    s8 = add_slide()
    draw_background(s8, C_LIGHT_BG)
    draw_header(s8, "6", "Retrieval / RAG Components", "RAG approach · Data sources retrieved · Vector store / index · Chunking / embedding notes")
    draw_footer(s8, 8)

    tf8_1 = draw_card(s8, x1, y1, card_w, card_h,
                     title="RAG Approach (Visual Feature Retrieval)",
                     subtitle="e.g. custom block, LangChain, none — We use Spatial Visual Retrieval")
    p = tf8_1.add_paragraph()
    r = p.add_run()
    r.text = "• No Document/Text RAG: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_ACCENT_ORANGE
    r = p.add_run()
    r.text = "Yahan text documents retrieve nahi hote. Iski jagah Satellite Spatial Feature Retrieval use hota hai."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf8_1.add_paragraph()
    p.space_before = Pt(5)
    r = p.add_run()
    r.text = "• Visual Feature Correspondence: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Source image ke crater features ko Reference orbital image ke saath visual descriptor distance ke through search aur retrieve kiya jata hai."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf8_1.add_paragraph()
    p.space_before = Pt(5)
    r = p.add_run()
    r.text = "• Mutual Nearest Neighbors: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Features ko match karte waqt bidirectional nearest neighbor check kiya jata hai taaki false matches reject ho sakein."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    tf8_2 = draw_card(s8, x2, y1, card_w, card_h,
                     title="Data Sources Retrieved",
                     subtitle="docs, DB, knowledge base — what feeds it")
    p = tf8_2.add_paragraph()
    r = p.add_run()
    r.text = "• Chandrayaan-2 TMC-2 Strips: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Terrain Mapping Camera-2 strips (5 m/px resolution, 3D stereo triplet views) from official mission orbits (e.g. Orbit 3922 vs 3943)."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf8_2.add_paragraph()
    p.space_before = Pt(5)
    r = p.add_run()
    r.text = "• OHRC High-Resolution Patches: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Orbiter High Resolution Camera (~0.25 m/px) sub-scenes covering landing zones and deep crater rims."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf8_2.add_paragraph()
    p.space_before = Pt(5)
    r = p.add_run()
    r.text = "• PDS4 Mission Metadata: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Solar elevation angle, spacecraft altitude, sub-solar azimuth, and planetary coordinate bounds from ISDA labels."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    tf8_3 = draw_card(s8, x1, y2, card_w, card_h,
                     title="Vector Store / Index (Spatial)",
                     subtitle="name, type & where hosted — In-memory KD-Tree & Spatial Grid")
    p = tf8_3.add_paragraph()
    r = p.add_run()
    r.text = "• In-Memory FLANN KD-Tree: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Pinecone ya Milvus cloud DB ki jarurat nahi hai. High-speed C++ FLANN KD-Tree index memory me keypoint descriptors ko microsecond latency me query karta hai."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf8_3.add_paragraph()
    p.space_before = Pt(5)
    r = p.add_run()
    r.text = "• 8x8 Spatial Grid Index: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Screen ko 64 spatial cells (8x8) me divide karke match count monitor kiya jata hai taaki features poori moon surface par uniformly spread hon."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf8_3.add_paragraph()
    p.space_before = Pt(5)
    r = p.add_run()
    r.text = "• Convex Hull Area Indexing: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Validates that inliers span > 94% of the shared image overlap region."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    tf8_4 = draw_card(s8, x2, y2, card_w, card_h,
                     title="Chunking / Embedding Notes",
                     subtitle="embedding model, top-k, privacy/redaction step, or N/A")
    p = tf8_4.add_paragraph()
    r = p.add_run()
    r.text = "• Vision Embeddings (LoFTR / SIFT): "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "LoFTR visual transformer features (256-dim feature maps) aur SIFT gradients (128-dim orientation histograms) local crater topography capture karte hain."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf8_4.add_paragraph()
    p.space_before = Pt(5)
    r = p.add_run()
    r.text = "• Multi-Scale Tiling Chunking: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Gigapixel satellite strips ko 1024x1024 overlapping patches me chunk kiya jata hai taaki RAM overflow na ho aur 20x scale difference bridge ho sake."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf8_4.add_paragraph()
    p.space_before = Pt(5)
    r = p.add_run()
    r.text = "• CLAHE Dynamic Range Normalization: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "16-bit PDS4 radiance raw values ko 8-bit contrast-enhanced representations me normalize kiya jata hai."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_BODY_DARK

    # -------------------------------------------------------------
    # SLIDE 9: 7 Data Flow
    # -------------------------------------------------------------
    s9 = add_slide()
    draw_background(s9, C_LIGHT_BG)
    draw_header(s9, "7", "Data Flow", "User input › Normalise / Prep › Feature Match › Geometric Align › Quality QA / Output")
    draw_footer(s9, 9)

    card9_img = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.45), Inches(7.2), Inches(5.45))
    card9_img.fill.solid()
    card9_img.fill.fore_color.rgb = C_CARD_BG
    card9_img.line.color.rgb = C_CARD_BORDER
    card9_img.line.width = Pt(1.2)

    pipe_img = PPT_VISUALS / "02_pipeline_flowchart.png"
    if pipe_img.exists():
        s9.shapes.add_picture(str(pipe_img), Inches(0.95), Inches(1.7), Inches(6.9), Inches(4.9))

    tf9_r = draw_card(s9, Inches(8.2), Inches(1.45), Inches(4.333), Inches(5.45),
                     title="Exact Step-by-Step Flow",
                     subtitle="How a user request travels through Lunar-X")

    flow_steps = [
        ("Step 1: User Input & Preset Loading",
         "User Home page par do lunar images select karta hai (ya custom GeoTIFF upload karta hai) aur matching configuration set karta hai."),
        ("Step 2: CLAHE & Illumination Normalization",
         "Sun angle aur dark crater shadows ko equalize karne ke liye CLAHE filter chalta hai taaki lighting conditions feature matching me rukawat na banein."),
        ("Step 3: Adaptive Feature Matching",
         "Vision engine SIFT ya LoFTR run karke lunar surface par thousands of candidate points detect karta hai aur initial match vectors banata hai."),
        ("Step 4: MAGSAC++ Outlier Rejection",
         "Robust statistical filter galat aur mismatched points ko filter out karta hai, resulting in 100% verified geometric inliers."),
        ("Step 5: Sub-Pixel Refinement & Warping",
         "Sub-pixel gradient optimizer accuracy ko sub-pixel level (< 0.2 px) tak polish karta hai aur Affine/Homography matrix se image warp karta hai."),
        ("Step 6: Live Results on Home Page",
         "Screen par interactive swipe viewer, checkerboard view, difference heatmap aur download report ready ho jaati hai.")
    ]
    for st_title, st_desc in flow_steps:
        p = tf9_r.add_paragraph()
        p.space_before = Pt(5)
        r = p.add_run()
        r.text = st_title
        r.font.name = FONT_FAMILY
        r.font.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = C_TITLE_DARK
        p_d = tf9_r.add_paragraph()
        r2 = p_d.add_run()
        r2.text = st_desc
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_BODY_DARK

    # -------------------------------------------------------------
    # SLIDE 10: 8 Storage & State
    # -------------------------------------------------------------
    s10 = add_slide()
    draw_background(s10, C_LIGHT_BG)
    draw_header(s10, "8", "Storage & State", "Database(s) used · What is persisted · Environments · Logging")
    draw_footer(s10, 10)

    tf10_1 = draw_card(s10, x1, y1, card_w, card_h,
                      title="Database(s) Used",
                      subtitle="e.g. MongoDB — shared or dedicated? (Filesystem Cache + JSON Store)")
    p = tf10_1.add_paragraph()
    r = p.add_run()
    r.text = "• Local Spatial Disk Cache: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "GeoTIFFs aur output rasters ke liye high-performance local disk storage (`data/outputs/`) use hoti hai, jo satellite files ko bina DB serialization latency ke serve karti hai."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11)
    r.font.color.rgb = C_BODY_DARK

    p = tf10_1.add_paragraph()
    p.space_before = Pt(3)
    r = p.add_run()
    r.text = "• Structured JSON Benchmark Store: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Benchmark numbers aur execution runs `benchmark_results.json` me store hote hain for fast retrieval and frontend synchronization."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11)
    r.font.color.rgb = C_BODY_DARK

    p = tf10_1.add_paragraph()
    p.space_before = Pt(3)
    r = p.add_run()
    r.text = "• Pluggable MongoDB/PostgreSQL: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_ACCENT_GREEN
    r = p.add_run()
    r.text = "Agar multi-user mission control teams ko centralized history chahiye, to MongoDB driver ready hai."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11)
    r.font.color.rgb = C_BODY_DARK

    tf10_2 = draw_card(s10, x2, y1, card_w, card_h,
                      title="What is Persisted",
                      subtitle="quiz answers, chat history, profile — under which user ID / documents")
    p = tf10_2.add_paragraph()
    r = p.add_run()
    r.text = "• Geometric Transformation Matrices: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Estimated 3x3 Affine / Homography transformation matrices so registrations can be mathematically verified at any later time."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11)
    r.font.color.rgb = C_BODY_DARK

    p = tf10_2.add_paragraph()
    p.space_before = Pt(3)
    r = p.add_run()
    r.text = "• Verification Metrics & QA Evidence: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Inliers count, reprojection RMSE (coarse & refined), spatial coverage %, grid cell occupancy %, NCC score, and execution duration."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11)
    r.font.color.rgb = C_BODY_DARK

    p = tf10_2.add_paragraph()
    p.space_before = Pt(3)
    r = p.add_run()
    r.text = "• Output Artifacts: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Registered blended images, difference maps, checkerboard images, and full mission report TXT files."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11)
    r.font.color.rgb = C_BODY_DARK

    tf10_3 = draw_card(s10, x1, y2, card_w, card_h,
                      title="Environments",
                      subtitle="dev / staging / prod separation")
    p = tf10_3.add_paragraph()
    r = p.add_run()
    r.text = "• Development (Local Workstation): "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Next.js dev server on port 3000 (hot reloading) + FastAPI on port 8000 with auto-reload. Runs on Windows/Linux local environment."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11)
    r.font.color.rgb = C_BODY_DARK

    p = tf10_3.add_paragraph()
    p.space_before = Pt(3)
    r = p.add_run()
    r.text = "• Staging (Containerized Sandbox): "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Docker container environment mirroring production dependencies, running full 20-test Pytest validation suite."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11)
    r.font.color.rgb = C_BODY_DARK

    p = tf10_3.add_paragraph()
    p.space_before = Pt(3)
    r = p.add_run()
    r.text = "• Production (Mission Control): "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Optimized Next.js production build (`next build && next start`) + Multi-worker Uvicorn backend orchestrated via Docker Compose."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11)
    r.font.color.rgb = C_BODY_DARK

    tf10_4 = draw_card(s10, x2, y2, card_w, card_h,
                      title="Logging & Auditing",
                      subtitle="where interactions are logged (file, console, service) — needed for compliance")
    p = tf10_4.add_paragraph()
    r = p.add_run()
    r.text = "• Structured Console & File Logs: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Standardized Python `logging` with structured tags: `[INGEST]`, `[PREPROCESS]`, `[MATCH]`, `[GEOMETRY]`, `[REFINE]`, `[DONE]`."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11)
    r.font.color.rgb = C_BODY_DARK

    p = tf10_4.add_paragraph()
    p.space_before = Pt(3)
    r = p.add_run()
    r.text = "• Real-Time Frontend Console Stream: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Home page screen par live terminal box hai jo user ko step-by-step progress aur execution timing live show karta hai."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11)
    r.font.color.rgb = C_BODY_DARK

    p = tf10_4.add_paragraph()
    p.space_before = Pt(3)
    r = p.add_run()
    r.text = "• Compliance & Traceability Audit: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Every alignment run logs exact image hashes, sensor metadata, condition number, and timestamp for strict audit compliance."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11)
    r.font.color.rgb = C_BODY_DARK

    # -------------------------------------------------------------
    # SLIDE 11: 9 Deployment
    # -------------------------------------------------------------
    s11 = add_slide()
    draw_background(s11, C_LIGHT_BG)
    draw_header(s11, "9", "Deployment", "Packaging · Environment variables required · Deploy / hosting notes")
    draw_footer(s11, 11)

    s11_stack_w = Inches(11.733)
    s11_stack_h = Inches(1.76)
    s11_y_starts = [Inches(1.42), Inches(3.26), Inches(5.10)]

    tf11_1 = draw_card(s11, Inches(0.8), s11_y_starts[0], s11_stack_w, s11_stack_h,
                      title="Packaging & Containerization",
                      subtitle="Dockerized container — image / build notes (Dockerfile + docker-compose.yml)")
    bullets_11_1 = [
        ("• Containerized Microservices: ", "Full system is packaged via `Dockerfile` and `docker-compose.yml`. Backend image uses Python 3.10-slim with OpenCV, PyTorch (CPU optimized), and FastAPI."),
        ("• Single-Command Launch: ", "Simply run `docker-compose up --build` ya local batch file `run_lunar_x.bat` to spin up both frontend console and backend engine automatically."),
        ("• Lightweight Footprint: ", "No heavy proprietary runtimes. Zero licensing fees, fully reproducible on any Linux, Mac, or Windows machine.")
    ]
    for b_title, b_desc in bullets_11_1:
        p = tf11_1.add_paragraph()
        p.space_before = Pt(2)
        r = p.add_run()
        r.text = b_title
        r.font.name = FONT_FAMILY
        r.font.bold = True
        r.font.size = Pt(11.5)
        r.font.color.rgb = C_TITLE_DARK
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_BODY_DARK

    tf11_2 = draw_card(s11, Inches(0.8), s11_y_starts[1], s11_stack_w, s11_stack_h,
                      title="Environment Variables Required",
                      subtitle="config/env vars needed — held centrally in .env, not hardcoded in source code")
    bullets_11_2 = [
        ("• HOST & PORT: ", "`HOST=0.0.0.0`, `PORT=8000` (FastAPI backend listening port)."),
        ("• NEXT_PUBLIC_API_URL: ", "`http://127.0.0.1:8000` (Bridging Next.js web application to registration backend)."),
        ("• COMPUTE_DEVICE & PATHS: ", "`DEVICE=cpu` (defaults to CPU; switches to `cuda` if NVIDIA GPU is present), `DATA_DIR=./data/raw`, `OUTPUT_DIR=./data/outputs`.")
    ]
    for b_title, b_desc in bullets_11_2:
        p = tf11_2.add_paragraph()
        p.space_before = Pt(2)
        r = p.add_run()
        r.text = b_title
        r.font.name = FONT_FAMILY
        r.font.bold = True
        r.font.size = Pt(11.5)
        r.font.color.rgb = C_TITLE_DARK
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_BODY_DARK

    tf11_3 = draw_card(s11, Inches(0.8), s11_y_starts[2], s11_stack_w, s11_stack_h,
                      title="Deploy / Hosting Notes",
                      subtitle="where it runs and how it's promoted to mission production")
    bullets_11_3 = [
        ("• Ground Station / On-Premise Air-Gapped: ", "Primary deployment mode is on-premise at ISRO data processing centers (SAC / ISTRAC) with zero outward internet access required."),
        ("• Cloud Deployment Ready: ", "Can easily be hosted on AWS GovCloud, Azure, or Kubernetes clusters using the provided Docker container."),
        ("• CI/CD Pipeline Promotion: ", "Automated Pytest test suite runs before any promotion to ensure RMSE does not exceed threshold on reference benchmark data.")
    ]
    for b_title, b_desc in bullets_11_3:
        p = tf11_3.add_paragraph()
        p.space_before = Pt(2)
        r = p.add_run()
        r.text = b_title
        r.font.name = FONT_FAMILY
        r.font.bold = True
        r.font.size = Pt(11.5)
        r.font.color.rgb = C_TITLE_DARK
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_BODY_DARK

    # -------------------------------------------------------------
    # SLIDE 12: 10 Compliance
    # -------------------------------------------------------------
    s12 = add_slide()
    draw_background(s12, C_LIGHT_BG)
    draw_header(s12, "10", "Compliance", "Address compliance across three angles — Space Data & Mission Ready Standards.")
    draw_footer(s12, 12)

    col3_w = Inches(3.7)
    col3_h = Inches(5.35)
    xs = [Inches(0.8), Inches(4.8), Inches(8.8)]

    tf12_1 = draw_card(s12, xs[0], Inches(1.5), col3_w, col3_h,
                      title="Data Store (At Rest)",
                      subtitle="where data lives, ownership, encryption — no unowned accounts")
    p = tf12_1.add_paragraph()
    r = p.add_run()
    r.text = "• PDS4 Data Standard Compliance:\n"
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Strict adherence to NASA/ISRO Planetary Data System standards. Sabhi orbital images authenticated format me hi read hoti hain.\n\n"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12)
    r.font.color.rgb = C_BODY_DARK
    r = p.add_run()
    r.text = "• Local Storage Only:\n"
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Satellite data local secure disks par rehta hai. Kisi commercial third-party cloud ya public S3 bucket par data leak nahi hota.\n\n"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12)
    r.font.color.rgb = C_BODY_DARK
    r = p.add_run()
    r.text = "• Data Integrity Verification:\n"
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "SHA-256 checksums and PDS4 label validation verify that raster pixels match original ISRO mission archives without corruption."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12)
    r.font.color.rgb = C_BODY_DARK

    tf12_2 = draw_card(s12, xs[1], Inches(1.5), col3_w, col3_h,
                      title="Data in Motion",
                      subtitle="how data is protected in transit; redaction of personal info")
    p = tf12_2.add_paragraph()
    r = p.add_run()
    r.text = "• Internal Network Isolated:\n"
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Frontend aur backend ke beech API calls local machine / internal LAN par loopback hoti hain. No data leaves the premise.\n\n"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12)
    r.font.color.rgb = C_BODY_DARK
    r = p.add_run()
    r.text = "• TLS / HTTPS Ready:\n"
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Production ingress controller supports end-to-end TLS 1.3 encryption across all communication routes.\n\n"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12)
    r.font.color.rgb = C_BODY_DARK
    r = p.add_run()
    r.text = "• Zero Telemetry & Tracking:\n"
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_ACCENT_GREEN
    r = p.add_run()
    r.text = "Zero Google Analytics, telemetry pings, ya external tracking cookies. Pure scientific tool respecting national space data security."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12)
    r.font.color.rgb = C_BODY_DARK

    tf12_3 = draw_card(s12, xs[2], Inches(1.5), col3_w, col3_h,
                      title="Infrastructure & Safety",
                      subtitle="standards adhered to, access controls, audit / logging posture")
    p = tf12_3.add_paragraph()
    r = p.add_run()
    r.text = "• Open Source Permissive Licensing:\n"
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "All libraries (OpenCV, PyTorch, Next.js) adhere to MIT/Apache 2.0/BSD licenses. Zero proprietary vendor lock-in or recurring fee.\n\n"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12)
    r.font.color.rgb = C_BODY_DARK
    r = p.add_run()
    r.text = "• Deterministic Space Safety:\n"
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Unlike generative AI which is non-deterministic, our geometric transformations are strictly mathematical, auditable, and repeatable.\n\n"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12)
    r.font.color.rgb = C_BODY_DARK
    r = p.add_run()
    r.text = "• Defense Network Ready:\n"
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Ready to run inside secure government or defense network boundaries."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(12)
    r.font.color.rgb = C_BODY_DARK

    # -------------------------------------------------------------
    # SLIDE 13: 11 Gaps, Risks & Open Items
    # -------------------------------------------------------------
    s13 = add_slide()
    draw_background(s13, C_LIGHT_BG)
    draw_header(s13, "11", "Gaps, Risks & Open Items", "Anything not standard, a dependency on someone else, a payment/token issue, or responsive-design gaps.")
    draw_footer(s13, 13)

    tf13_top = draw_card(s13, Inches(0.8), Inches(1.45), Inches(11.733), Inches(2.35),
                        title="Key Space Challenges & Mitigation Strategies (How We Solved Them)",
                        subtitle="Real issues encountered with lunar orbital imagery and their concrete engineering solutions")

    p = tf13_top.add_paragraph()
    r = p.add_run()
    r.text = "• 180° Shadow Inversion (Terminator Shadows): "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Moon par jab sun angle badalta hai to shadows completely reverse ho jaati hain. "
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_BODY_DARK
    r = p.add_run()
    r.text = "[Mitigation]: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_ACCENT_GREEN
    r = p.add_run()
    r.text = "CLAHE local contrast enhancement aur Sobel gradient orientations use karke intensity differences normalize kiye gaye."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf13_top.add_paragraph()
    p.space_before = Pt(3)
    r = p.add_run()
    r.text = "• 20x Scale Gap (OHRC 25cm vs TMC-2 5m): "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Different sensors ke beech pixel resolution me 20x ka farak hota hai. "
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_BODY_DARK
    r = p.add_run()
    r.text = "[Mitigation]: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_ACCENT_GREEN
    r = p.add_run()
    r.text = "Multi-scale Gaussian pyramid decomposition and homography affine model selection scale invariant matching provide karte hain."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_BODY_DARK

    p = tf13_top.add_paragraph()
    p.space_before = Pt(3)
    r = p.add_run()
    r.text = "• Low-Texture Plain Areas (Mare Basins): "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(12.5)
    r.font.color.rgb = C_TITLE_DARK
    r = p.add_run()
    r.text = "Jahan craters nahi hote wahan traditional keypoints fail ho sakte hain. "
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_BODY_DARK
    r = p.add_run()
    r.text = "[Mitigation]: "
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_ACCENT_GREEN
    r = p.add_run()
    r.text = "LoFTR dense transformer matching use hota hai jo low-contrast plain areas me bhi 4,600+ feature correspondences dhoond nikalta hai."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11.5)
    r.font.color.rgb = C_BODY_DARK

    tf13_bl = draw_card(s13, Inches(0.8), Inches(3.92), Inches(5.75), Inches(2.98),
                       title="Blockers & Dependencies",
                       subtitle="who or what you're waiting on")
    blockers = [
        ("• Zero External Blockers: ", "Currently zero external dependencies or blockers exist. Sabhi core modules implement aur benchmark ho chuke hain."),
        ("• Gigapixel Strip Memory Management: ", "Full orbital strips (50,000 pixels long) can exceed RAM. Solution: Streaming tile processor divides strips into overlapping 2K blocks."),
        ("• IIRS Hyperspectral Integration: ", "IIRS cube ingestion code is complete; full sensor calibration test is ready for ISRO raw calibrated band files.")
    ]
    for b_title, b_desc in blockers:
        p = tf13_bl.add_paragraph()
        p.space_before = Pt(3)
        r = p.add_run()
        r.text = b_title
        r.font.name = FONT_FAMILY
        r.font.bold = True
        r.font.size = Pt(11.5)
        r.font.color.rgb = C_TITLE_DARK
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_BODY_DARK

    tf13_br = draw_card(s13, Inches(6.78), Inches(3.92), Inches(5.75), Inches(2.98),
                       title="Responsive & Display Status",
                       subtitle="does it display correctly on mobile? gaps?")
    responsive_items = [
        ("• Mission Control Optimized: ", "Designed primarily for large high-resolution desktop and command room screens (1920x1080 and 4K displays) with high data density."),
        ("• Mobile & Tablet Support: ", "Next.js UI uses flexible responsive grids that gracefully stack on tablets and phones without broken layouts."),
        ("• Touch-Friendly Interaction: ", "The interactive swipe comparison bar supports touch dragging on tablets as well as standard mouse navigation on PCs.")
    ]
    for r_title, r_desc in responsive_items:
        p = tf13_br.add_paragraph()
        p.space_before = Pt(3)
        r = p.add_run()
        r.text = r_title
        r.font.name = FONT_FAMILY
        r.font.bold = True
        r.font.size = Pt(11.5)
        r.font.color.rgb = C_TITLE_DARK
        r2 = p.add_run()
        r2.text = r_desc
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_BODY_DARK

    # -------------------------------------------------------------
    # SLIDE 14: 12 Deviations from the Common Blueprint
    # -------------------------------------------------------------
    s14 = add_slide()
    draw_background(s14, C_LIGHT_BG)
    draw_header(s14, "12", "Deviations from the Common Blueprint", "If your agent does anything differently from the others (different LLM, RAG, or API), note it here — and why.")
    draw_footer(s14, 14)

    tf14_top = draw_card(s14, Inches(0.8), Inches(1.5), Inches(11.733), Inches(3.25),
                        title="Key Architectural Deviation: Computer Vision Engine instead of Generative LLM",
                        subtitle="Why LLM-based approaches are unsuited for planetary orbital registration")

    reasons = [
        ("Sub-Pixel Mathematical Precision: ",
         "Satellite image registration requires sub-pixel alignment accuracy (RMSE < 0.2 pixels). Text LLMs generate text tokens and cannot compute pixel-level geometric transforms or affine matrices deterministically."),
        ("Blazing Fast Speed (0.16s vs 8s): ",
         "Classical SIFT runs in 0.16 seconds on standard CPU. An LLM cloud API call takes 5 to 10 seconds per image, introducing massive latency that makes real-time mission navigation impossible."),
        ("Zero Recurring API Costs: ",
         "Processing thousands of orbital strips via commercial LLMs incurs high token costs. Our computer vision pipeline is 100% free and open-source with zero recurring fees."),
        ("Scientifically Verifiable Proof: ",
         "ISRO scientists require verifiable mathematical outputs (inliers count, reprojection error, normalized cross-correlation). Black-box LLM text answers cannot be mathematically audited for space safety.")
    ]
    for r_title, r_desc in reasons:
        p = tf14_top.add_paragraph()
        p.space_before = Pt(5)
        r = p.add_run()
        r.text = "• " + r_title
        r.font.name = FONT_FAMILY
        r.font.bold = True
        r.font.size = Pt(13)
        r.font.color.rgb = C_TITLE_DARK
        r2 = p.add_run()
        r2.text = r_desc
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(12.5)
        r2.font.color.rgb = C_BODY_DARK

    tf14_bot = draw_card(s14, Inches(0.8), Inches(4.95), Inches(11.733), Inches(1.95),
                        title="Would you recommend this as the standard?",
                        subtitle="Yes / No / Partly — one line on what should become the team default")

    p = tf14_bot.add_paragraph()
    r = p.add_run()
    r.text = "YES — Absolutely Recommended as the Standard for All Spatial & Geospatial Agents!\n"
    r.font.name = FONT_FAMILY
    r.font.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = C_ACCENT_GREEN

    r = p.add_run()
    r.text = "Space exploration, autonomous rovers, and planetary satellite processing ke liye Computer Vision + Deep Transformers (LoFTR / SIFT) hi team standard hona chahiye. LLMs ko sirf UI assistance, chatbot guidance, ya mission documentation generation tak seemit rakhna chahiye, core image alignment aur geometric navigation logic me nahi."
    r.font.name = FONT_FAMILY
    r.font.size = Pt(13.5)
    r.font.color.rgb = C_BODY_DARK

    # -------------------------------------------------------------
    # SLIDE 15: Conclusion Slide (Dark Theme)
    # -------------------------------------------------------------
    s15 = add_slide()
    draw_background(s15, C_NAVY_BG)

    card15 = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.1), Inches(11.333), Inches(5.3))
    card15.fill.solid()
    card15.fill.fore_color.rgb = C_NAVY_CARD
    card15.line.color.rgb = C_NAVY_BORDER
    card15.line.width = Pt(1.5)

    tb15 = s15.shapes.add_textbox(Inches(1.4), Inches(1.4), Inches(10.533), Inches(4.7))
    tf15 = tb15.text_frame
    tf15.word_wrap = True
    tf15.clear()

    p = tf15.paragraphs[0]
    r = p.add_run()
    r.text = "Once every agent is documented…"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(32)
    r.font.bold = True
    r.font.color.rgb = C_TEXT_WHITE

    bullets = [
        ("Lay all decks side by side: ", "Compare the Vision engines, APIs, spatial indexing, and compliance postures across all planetary mission components."),
        ("Where agents converge: ", "The SIFT + LoFTR hybrid pipeline becomes the agreed standard ISRO alignment playbook for all Chandrayaan-2 and future missions."),
        ("Where one is an outlier: ", "Decide: Align it, or adopt specialized vision pipelines as the new default for mission-critical geometric tasks."),
        ("Publish the agreed choices: ", "Publish the complete verified architecture as the official Lunar-X Planetary Agent Development Playbook."),
        ("Deliverable Ready for SIH 2026: ", "Fully functional Next.js dashboard + FastAPI engine + 0.148 px verified accuracy ready for live demonstration.")
    ]
    for b_title, b_desc in bullets:
        p = tf15.add_paragraph()
        p.space_before = Pt(12)
        r = p.add_run()
        r.text = "• " + b_title
        r.font.name = FONT_FAMILY
        r.font.bold = True
        r.font.size = Pt(14)
        r.font.color.rgb = C_ACCENT_BLUE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(13.5)
        r2.font.color.rgb = C_TEXT_WHITE

    prs.save(str(OUTPUT_PPTX))
    print(f"[SUCCESS] Presentation saved to {OUTPUT_PPTX}")

if __name__ == '__main__':
    build_presentation()

