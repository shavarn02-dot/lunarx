"use client"
import React from "react"
import type { Pair } from "./types"

interface GeospatialHeaderProps {
  online: boolean
  pairs: Pair[]
  selectedPairId: string
  onSelectPair: (p: Pair) => void
  onOpenUpload: () => void
  onExport: () => void
  activeSensor?: string | null
}

export function GeospatialHeader({
  online,
  pairs,
  selectedPairId,
  onSelectPair,
  onOpenUpload,
  onExport,
  activeSensor,
}: GeospatialHeaderProps) {
  const currentPair = pairs.find(p => p.id === selectedPairId) || pairs[0]

  return (
    <header className="geospatial-header">
      {/* Brand & Mission Badge */}
      <div className="header-left">
        <div className="isro-badge">
          <div className="isro-symbol">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path
                d="M12 2L14.5 9.5H22L16 14L18.5 21.5L12 17L5.5 21.5L8 14L2 9.5H9.5L12 2Z"
                fill="#ff9100"
              />
            </svg>
          </div>
          <div className="mission-title">
            <span className="brand-name">LUNARX</span>
            <span className="mission-sub">CHANDRA-SYNC · SIH26166</span>
          </div>
        </div>

        {/* Orbit & Sensor Telemetry Tag */}
        <div className="sensor-tag-container">
          <div className="sensor-chip">
            <span className="sensor-dot" />
            <span className="sensor-name">
              {activeSensor || currentPair?.sensor || "TMC-2 (5.0m) vs. OHRC (0.25m)"}
            </span>
            <span className="sensor-divider">|</span>
            <span className="orbit-info">{currentPair?.orbit || "Orbit 3922 / 3943"}</span>
          </div>
        </div>
      </div>

      {/* Center: Preset Selector */}
      <div className="header-center">
        <div className="preset-selector-bar">
          <span className="preset-label">SCENE:</span>
          <select
            value={selectedPairId}
            onChange={e => {
              const p = pairs.find(x => x.id === e.target.value)
              if (p) onSelectPair(p)
            }}
            className="preset-dropdown"
          >
            {pairs.map(p => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Right Controls */}
      <div className="header-right">
        {/* Upload Custom Imagery Button */}
        <button className="hdr-btn upload-btn" onClick={onOpenUpload} title="Upload custom lunar orbit images">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="17 8 12 3 7 8" />
            <line x1="12" y1="3" x2="12" y2="15" />
          </svg>
          <span>Upload Image</span>
        </button>

        {/* Export GeoTIFF & Report */}
        <button className="hdr-btn export-btn" onClick={onExport} title="Export GeoTIFF & CSV Scientific Report">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="7 10 12 15 17 10" />
            <line x1="12" y1="15" x2="12" y2="3" />
          </svg>
          <span>Export Report</span>
        </button>

        {/* System Online Status Badge */}
        <div className={`system-status-indicator ${online ? "online" : "offline"}`}>
          <span className="radar-ping" />
          <span className="status-text">{online ? "SYSTEM ONLINE" : "SYSTEM OFFLINE"}</span>
        </div>
      </div>
    </header>
  )
}
