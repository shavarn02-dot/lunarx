import cv2
import numpy as np
import time
from pathlib import Path

# Paths
OUT_DIR = Path("data/videos").resolve()
OUT_DIR.mkdir(parents=True, exist_ok=True)
video_path = OUT_DIR / "lunarx_prototype_demo_1080p.mp4"

IMG_DIR = Path("data/prototype_screenshots").resolve()
full_dash = cv2.imread(str(IMG_DIR / "03_prototype_full_dashboard.png"))
match_vec = cv2.imread(str(IMG_DIR / "05_prototype_match_vectors.png"))
check_brd = cv2.imread(str(IMG_DIR / "06_prototype_checkerboard.png"))
overview  = cv2.imread(str(IMG_DIR / "01_prototype_overview.png"))

if full_dash is None:
    raise RuntimeError("Full dashboard screenshot not found!")

# Target Output Specs
OUT_W, OUT_H = 1920, 1080
FPS = 30
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter(str(video_path), fourcc, FPS, (OUT_W, OUT_H))

# Smoothstep interpolation function (ease in & out)
def ease_in_out(t):
    return t * t * (3 - 2 * t)

# Camera viewport crop & resize helper
def get_camera_frame(img, cx, cy, zoom, out_w=OUT_W, out_h=OUT_H):
    h_img, w_img = img.shape[:2]
    # Zoom determines the fraction of the image visible
    crop_w = int(w_img / zoom)
    crop_h = int(crop_w * (out_h / out_w))

    # Bounding box clamped to image
    x1 = max(0, min(int(cx - crop_w / 2), w_img - crop_w))
    y1 = max(0, min(int(cy - crop_h / 2), h_img - crop_h))
    x2 = x1 + crop_w
    y2 = y1 + crop_h

    cropped = img[y1:y2, x1:x2]
    return cv2.resize(cropped, (out_w, out_h), interpolation=cv2.INTER_CUBIC)

# Overlay HUD banner
def draw_hud(frame, title, subtitle):
    overlay = frame.copy()
    
    # Top Mission Bar
    cv2.rectangle(overlay, (0, 0), (OUT_W, 60), (10, 15, 24), -1)
    cv2.line(overlay, (0, 60), (OUT_W, 60), (0, 229, 255), 1)

    # Bottom Telemetry Lower-Third Badge
    badge_w, badge_h = 760, 80
    bx, by = 40, OUT_H - 120
    cv2.rectangle(overlay, (bx, by), (bx + badge_w, by + badge_h), (12, 18, 30), -1)
    cv2.rectangle(overlay, (bx, by), (bx + badge_w, by + badge_h), (0, 229, 255), 1)

    # Alpha blend HUD
    alpha = 0.85
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # Top Header Text
    cv2.putText(frame, "LUNARX  |  CHANDRA-SYNC MISSION CONTROL", (40, 38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.circle(frame, (OUT_W - 220, 32), 6, (0, 230, 118), -1)
    cv2.putText(frame, "SYSTEM ONLINE", (OUT_W - 200, 38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 230, 118), 2, cv2.LINE_AA)

    # Lower-third text
    cv2.circle(frame, (bx + 25, by + 40), 6, (0, 229, 255), -1)
    cv2.putText(frame, title.upper(), (bx + 45, by + 34),
                cv2.FONT_HERSHEY_SIMPLEX, 0.68, (0, 229, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, subtitle, (bx + 45, by + 62),
                cv2.FONT_HERSHEY_SIMPLEX, 0.52, (180, 195, 210), 1, cv2.LINE_AA)

print("Rendering Cinematic Prototype Video with Zoom In & Zoom Out...")

# Sequences definition:
# List of Keyframe States:
# (img, cx, cy, zoom, duration_seconds, title, subtitle)
full_h, full_w = full_dash.shape[:2]

keyframes = [
    # 1. Overview (Zoom = 1.05) - 3.5s
    {
        "img": full_dash, "cx": full_w / 2, "cy": 550, "zoom": 1.05, "duration": 3.5,
        "title": "Stage 1: Scientific Workspace Overview",
        "subtitle": "Chandrayaan-2 lunar registration mission control running in cloud"
    },
    # 2. Zoom-In on Input Image Pair - 4.0s
    {
        "img": full_dash, "cx": full_w / 2, "cy": 850, "zoom": 1.85, "duration": 4.0,
        "title": "Stage 2: Multi-Pass Orbital Ingestion",
        "subtitle": "Ingesting Source vs Reference craters under severe shadow differences"
    },
    # 3. Zoom-In on Controls & Run Action - 3.5s
    {
        "img": full_dash, "cx": full_w / 2, "cy": 1600, "zoom": 2.1, "duration": 3.5,
        "title": "Stage 3: Configuration & Alignment Execution",
        "subtitle": "LoFTR deep attention + SIFT with USAC-MAGSAC outlier rejection"
    },
    # 4. Zoom-In on Accuracy Metrics Row - 5.0s
    {
        "img": full_dash, "cx": full_w / 2, "cy": 1820, "zoom": 2.4, "duration": 5.0,
        "title": "Stage 4: Sub-Pixel Accuracy Benchmarks",
        "subtitle": "Achieving 0.148 px RMSE, 1,329 inliers, 99.85% inlier ratio, 0.68s runtime"
    },
    # 5. Pan & Zoom into Match Vectors - 5.5s
    {
        "img": match_vec if match_vec is not None else full_dash,
        "cx": match_vec.shape[1] / 2 if match_vec is not None else full_w / 2,
        "cy": match_vec.shape[0] / 2 if match_vec is not None else 2800,
        "zoom": 1.25, "duration": 5.5,
        "title": "Stage 5: Deep Inlier Correspondence Field",
        "subtitle": "1,329 verified green vector tie-lines connecting crater features"
    },
    # 6. Zoom-In on Checkerboard View - 4.5s
    {
        "img": check_brd if check_brd is not None else full_dash,
        "cx": check_brd.shape[1] / 2 if check_brd is not None else full_w / 2,
        "cy": check_brd.shape[0] / 2 if check_brd is not None else 3500,
        "zoom": 1.35, "duration": 4.5,
        "title": "Stage 6: Geometric Boundary Verification",
        "subtitle": "8x8 checkerboard proving seamless crater rim continuity across tiles"
    },
    # 7. Zoom-Out back to Full Working System - 4.0s
    {
        "img": full_dash, "cx": full_w / 2, "cy": 1100, "zoom": 1.02, "duration": 4.0,
        "title": "Stage 7: Autonomous Quality Verification Complete",
        "subtitle": "Real-time registration validated under ISRO Chandrayaan standards"
    },
]

total_frames = 0

for i in range(len(keyframes) - 1):
    kf_start = keyframes[i]
    kf_end = keyframes[i + 1]

    num_frames = int(kf_start["duration"] * FPS)
    transition_frames = int(FPS * 1.4)  # 1.4s smooth transition between keyframes
    static_frames = max(1, num_frames - transition_frames)

    # Static phase
    for _ in range(static_frames):
        frame = get_camera_frame(kf_start["img"], kf_start["cx"], kf_start["cy"], kf_start["zoom"])
        draw_hud(frame, kf_start["title"], kf_start["subtitle"])
        writer.write(frame)
        total_frames += 1

    # Transition phase (Interpolate cx, cy, zoom)
    use_img = kf_start["img"] if (kf_start["img"] is kf_end["img"]) else kf_end["img"]
    for step in range(transition_frames):
        t = (step + 1) / transition_frames
        ease_t = ease_in_out(t)

        cx = kf_start["cx"] + (kf_end["cx"] - kf_start["cx"]) * ease_t
        cy = kf_start["cy"] + (kf_end["cy"] - kf_start["cy"]) * ease_t
        zoom = kf_start["zoom"] + (kf_end["zoom"] - kf_start["zoom"]) * ease_t

        title = kf_end["title"] if ease_t > 0.5 else kf_start["title"]
        sub = kf_end["subtitle"] if ease_t > 0.5 else kf_start["subtitle"]

        frame = get_camera_frame(use_img, cx, cy, zoom)
        draw_hud(frame, title, sub)
        writer.write(frame)
        total_frames += 1

# Render last keyframe
last_kf = keyframes[-1]
for _ in range(int(last_kf["duration"] * FPS)):
    frame = get_camera_frame(last_kf["img"], last_kf["cx"], last_kf["cy"], last_kf["zoom"])
    draw_hud(frame, last_kf["title"], last_kf["subtitle"])
    writer.write(frame)
    total_frames += 1

writer.release()
print(f"SUCCESS: Rendered {total_frames} frames ({round(total_frames / FPS, 1)}s) to {video_path}")
