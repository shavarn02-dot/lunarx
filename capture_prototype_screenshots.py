import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path("data/prototype_screenshots").resolve()
OUT_DIR.mkdir(parents=True, exist_ok=True)

URL = "https://lunarx-pi.vercel.app"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # Set high-DPI device scale factor for ultra-sharp presentation screenshots
    context = browser.new_context(
        viewport={"width": 1600, "height": 1000},
        device_scale_factor=2
    )
    page = context.new_page()

    print("[1/7] Navigating to LUNARX Vercel Prototype...")
    page.goto(URL, wait_until="networkidle", timeout=45000)
    time.sleep(2)

    # Screenshot 1: Workspace Header & Input Selection
    page.screenshot(path=str(OUT_DIR / "01_prototype_overview.png"), full_page=False)
    print("Saved: 01_prototype_overview.png")

    # Screenshot 2: Input Grid Close-Up
    input_section = page.locator(".input-section")
    if input_section.count() > 0:
        input_section.screenshot(path=str(OUT_DIR / "02_prototype_input_pair.png"))
        print("Saved: 02_prototype_input_pair.png")

    # Click 'Run registration'
    print("[2/7] Clicking 'Run registration'...")
    run_btn = page.locator("button.run:has-text('Run registration')")
    if run_btn.count() > 0:
        run_btn.click()
    else:
        page.locator("button:has-text('Run registration')").click()

    # Wait for result to appear (look for 'Successful' or 'Verified')
    print("[3/7] Waiting for registration pipeline execution...")
    page.wait_for_selector(".metrics-row, .quality.verified", timeout=30000)
    time.sleep(2)

    # Screenshot 3: Full Result Dashboard
    page.screenshot(path=str(OUT_DIR / "03_prototype_full_dashboard.png"), full_page=True)
    print("Saved: 03_prototype_full_dashboard.png")

    # Screenshot 4: Metrics Row
    metrics_row = page.locator(".metrics-row")
    if metrics_row.count() > 0:
        metrics_row.screenshot(path=str(OUT_DIR / "04_prototype_metrics_cards.png"))
        print("Saved: 04_prototype_metrics_cards.png")

    # Screenshot 5: Match Vectors Tab
    print("[4/7] Capturing Match Vectors View...")
    match_tab = page.locator("button:has-text('Match vectors')")
    if match_tab.count() > 0:
        match_tab.click()
        time.sleep(1.5)
        viewer = page.locator(".result")
        if viewer.count() > 0:
            viewer.screenshot(path=str(OUT_DIR / "05_prototype_match_vectors.png"))
            print("Saved: 05_prototype_match_vectors.png")

    # Screenshot 6: Checkerboard Tab
    print("[5/7] Capturing Checkerboard View...")
    checker_tab = page.locator("button:has-text('Checkerboard')")
    if checker_tab.count() > 0:
        checker_tab.click()
        time.sleep(1.5)
        viewer = page.locator(".result")
        if viewer.count() > 0:
            viewer.screenshot(path=str(OUT_DIR / "06_prototype_checkerboard.png"))
            print("Saved: 06_prototype_checkerboard.png")

    # Screenshot 7: Quality Verification Badge
    print("[6/7] Capturing Quality Verification Card...")
    quality = page.locator(".quality")
    if quality.count() > 0:
        quality.screenshot(path=str(OUT_DIR / "07_prototype_quality_verified.png"))
        print("Saved: 07_prototype_quality_verified.png")

    # Screenshot 8: Advanced Details (Matrix & Telemetry)
    print("[7/7] Expanding & Capturing Advanced Mathematical Details...")
    details = page.locator(".advanced")
    if details.count() > 0:
        summary = details.locator("summary")
        summary.click()
        time.sleep(1)
        details.screenshot(path=str(OUT_DIR / "08_prototype_transformation_matrix.png"))
        print("Saved: 08_prototype_transformation_matrix.png")

    browser.close()
    print("\nSUCCESS: All prototype screenshots captured in data/prototype_screenshots/")
