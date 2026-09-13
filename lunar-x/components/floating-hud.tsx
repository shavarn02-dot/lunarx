"use client"
import React from "react"

interface FloatingHudProps {
  viewMode: "split" | "matches" | "checkerboard" | "difference" | "side"
  setViewMode: (mode: "split" | "matches" | "checkerboard" | "difference" | "side") => void
  loupeActive: boolean
  setLoupeActive: (val: boolean | ((prev: boolean) => boolean)) => void
  showGrid: boolean
  setShowGrid: (val: boolean | ((prev: boolean) => boolean)) => void
  onToggleAnalytics: () => void
  hasResult: boolean
}

export function FloatingHud({
  viewMode,
  setViewMode,
  loupeActive,
  setLoupeActive,
  showGrid,
  setShowGrid,
  onToggleAnalytics,
  hasResult,
}: FloatingHudProps) {
  return (
    <aside className="floating-hud-dock" aria-label="Inspection Tools">
      <div className="hud-title">HUD TOOLS</div>

      {/* Loupe Magnifier */}
      <button
        className={`hud-tool-btn ${loupeActive ? "active" : ""}`}
        onClick={() => setLoupeActive(prev => !prev)}
        title="4X Sub-pixel Loupe Magnifier"
      >
        <div className="hud-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
            <line x1="11" y1="8" x2="11" y2="14" />
            <line x1="8" y1="11" x2="14" y2="11" />
          </svg>
        </div>
        <div className="hud-label">
          <strong>Magnifying Loupe</strong>
          <small>{loupeActive ? "Active (Hover)" : "4X Sub-Pixel Inspection"}</small>
        </div>
      </button>

      {/* Split-Screen Slider */}
      <button
        className={`hud-tool-btn ${viewMode === "split" ? "active" : ""}`}
        onClick={() => setViewMode("split")}
        title="Interactive Split Before/After Slider"
      >
        <div className="hud-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="3" width="18" height="18" rx="2" />
            <line x1="12" y1="3" x2="12" y2="21" />
            <path d="M8 12l-2-2 2-2" />
            <path d="M16 12l2-2-2-2" />
          </svg>
        </div>
        <div className="hud-label">
          <strong>Split Slider</strong>
          <small>Swipe Before & After</small>
        </div>
      </button>

      {/* Inlier Match Vector Field */}
      <button
        className={`hud-tool-btn ${viewMode === "matches" ? "active" : ""}`}
        onClick={() => setViewMode("matches")}
        disabled={!hasResult}
        title="Vector Field Match Visualizer"
      >
        <div className="hud-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="5" cy="5" r="2" />
            <circle cx="19" cy="5" r="2" />
            <circle cx="5" cy="19" r="2" />
            <circle cx="19" cy="19" r="2" />
            <line x1="7" y1="5" x2="17" y2="5" strokeDasharray="2 2" />
            <line x1="7" y1="19" x2="17" y2="19" strokeDasharray="2 2" />
            <line x1="5" y1="7" x2="19" y2="17" />
          </svg>
        </div>
        <div className="hud-label">
          <strong>Vector Field</strong>
          <small>Tie-Point Vectors</small>
        </div>
      </button>

      {/* Checkerboard Toggle */}
      <button
        className={`hud-tool-btn ${viewMode === "checkerboard" ? "active" : ""}`}
        onClick={() => setViewMode("checkerboard")}
        disabled={!hasResult}
        title="Checkerboard Alignment Verification"
      >
        <div className="hud-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <rect x="3" y="3" width="9" height="9" />
            <rect x="12" y="12" width="9" height="9" />
            <rect x="12" y="3" width="9" height="9" fillOpacity="0.3" />
            <rect x="3" y="12" width="9" height="9" fillOpacity="0.3" />
          </svg>
        </div>
        <div className="hud-label">
          <strong>Checkerboard</strong>
          <small>Edge Continuity</small>
        </div>
      </button>

      {/* Difference Heatmap */}
      <button
        className={`hud-tool-btn ${viewMode === "difference" ? "active" : ""}`}
        onClick={() => setViewMode("difference")}
        disabled={!hasResult}
        title="Photometric Residual Heatmap"
      >
        <div className="hud-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="9" />
            <path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor" fillOpacity="0.4" />
          </svg>
        </div>
        <div className="hud-label">
          <strong>Residual Heatmap</strong>
          <small>Photometric Delta</small>
        </div>
      </button>

      {/* Coordinate Grid HUD Toggle */}
      <button
        className={`hud-tool-btn ${showGrid ? "active" : ""}`}
        onClick={() => setShowGrid(prev => !prev)}
        title="Toggle Lunar Lat/Lon Coordinate Grid"
      >
        <div className="hud-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="3" y1="9" x2="21" y2="9" />
            <line x1="3" y1="15" x2="21" y2="15" />
            <line x1="9" y1="3" x2="9" y2="21" />
            <line x1="15" y1="3" x2="15" y2="21" />
          </svg>
        </div>
        <div className="hud-label">
          <strong>Grid & Reticle</strong>
          <small>{showGrid ? "Enabled" : "Disabled"}</small>
        </div>
      </button>

      <div className="hud-separator" />

      {/* Deep Science Drawer Trigger */}
      <button
        className="hud-tool-btn analytics-btn"
        onClick={onToggleAnalytics}
        title="Open Deep Telemetry & Matrix Diagnostics"
      >
        <div className="hud-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
          </svg>
        </div>
        <div className="hud-label">
          <strong>Deep Analytics</strong>
          <small>Matrix, Logs & NCC</small>
        </div>
      </button>
    </aside>
  )
}
