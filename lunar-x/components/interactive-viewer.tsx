'use client'

import React, { useState, useRef, useEffect, useCallback } from 'react'

export type ViewMode = 'matches' | 'registered' | 'checkerboard' | 'difference' | 'split'

interface InteractiveViewerProps {
  viewMode: ViewMode
  setViewMode: (mode: ViewMode) => void
  currentImageFile: string
  referenceImageFile: string
  registeredImageFile: string
  sensorName: string
  orbitName: string
  inlierCount: number
  reprojRmse: number
  getImageUrl: (fn?: string) => string
  handleImgError: (e: React.SyntheticEvent<HTMLImageElement, Event>, fn?: string) => void
}

export function InteractiveViewer({
  viewMode,
  setViewMode,
  currentImageFile,
  referenceImageFile,
  registeredImageFile,
  sensorName,
  orbitName,
  inlierCount,
  reprojRmse,
  getImageUrl,
  handleImgError
}: InteractiveViewerProps) {
  const [splitPos, setSplitPos] = useState(50)
  const [isDragging, setIsDragging] = useState(false)
  const [showReticle, setShowReticle] = useState(true)
  const [zoomLevel, setZoomLevel] = useState(1)
  const [isFullscreen, setIsFullscreen] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)

  const handlePointerDown = (e: React.PointerEvent) => {
    if (viewMode !== 'split') return
    setIsDragging(true)
    handleMove(e.clientX)
  }

  const handleMove = useCallback((clientX: number) => {
    if (!containerRef.current) return
    const rect = containerRef.current.getBoundingClientRect()
    const x = clientX - rect.left
    const pct = Math.max(2, Math.min(98, (x / rect.width) * 100))
    setSplitPos(pct)
  }, [])

  useEffect(() => {
    const onPointerMove = (e: PointerEvent) => {
      if (!isDragging) return
      handleMove(e.clientX)
    }
    const onPointerUp = () => {
      if (isDragging) setIsDragging(false)
    }

    if (isDragging) {
      window.addEventListener('pointermove', onPointerMove)
      window.addEventListener('pointerup', onPointerUp)
    }
    return () => {
      window.removeEventListener('pointermove', onPointerMove)
      window.removeEventListener('pointerup', onPointerUp)
    }
  }, [isDragging, handleMove])

  const captions: Record<ViewMode, { title: string; hint: string }> = {
    matches: {
      title: 'Correspondences Vector Field',
      hint: `Green vectors = Verified Inliers (${inlierCount}) · Red vectors = Rejected Outliers`
    },
    registered: {
      title: 'Registered Warped Overlay',
      hint: 'Source image mathematically projected into the exact Reference frame coordinate system'
    },
    checkerboard: {
      title: 'Checkerboard Continuity Test',
      hint: 'Alternating tiles of Reference and Registered Source; check crater rim edges across seams'
    },
    difference: {
      title: 'Radiometric Residual Heatmap',
      hint: 'Dark pixels indicate sub-pixel alignment; light pixels reflect differing solar incidence angles'
    },
    split: {
      title: 'Interactive Split Comparison',
      hint: 'Drag the slider across to compare Ground Truth Reference vs Registered Source'
    }
  }

  const activeCaption = captions[viewMode]

  return (
    <div className={`cv-viewer-panel ${isFullscreen ? 'fullscreen-mode' : ''}`}>
      {/* Viewer Control Bar */}
      <div className="viewer-toolbar">
        <div className="mode-segmented-group">
          {(['matches', 'registered', 'checkerboard', 'difference', 'split'] as ViewMode[]).map((m) => (
            <button
              key={m}
              type="button"
              className={`mode-tab-btn ${viewMode === m ? 'active' : ''}`}
              onClick={() => setViewMode(m)}
            >
              {m === 'matches' && 'Vectors (Matches)'}
              {m === 'registered' && 'Overlay'}
              {m === 'checkerboard' && 'Checkerboard'}
              {m === 'difference' && 'Residual Heatmap'}
              {m === 'split' && 'Interactive Split'}
            </button>
          ))}
        </div>

        <div className="viewer-utility-tools">
          <button
            type="button"
            className={`tool-icon-btn ${showReticle ? 'active' : ''}`}
            onClick={() => setShowReticle(!showReticle)}
            title="Toggle Mission HUD Reticle"
          >
            Reticle
          </button>

          <button
            type="button"
            className="tool-icon-btn"
            onClick={() => setZoomLevel(zoomLevel === 1 ? 1.5 : zoomLevel === 1.5 ? 2 : 1)}
            title="Zoom Factor"
          >
            Zoom {zoomLevel}x
          </button>

          <button
            type="button"
            className="tool-icon-btn"
            onClick={() => setIsFullscreen(!isFullscreen)}
            title="Toggle Fullscreen"
          >
            {isFullscreen ? 'Exit' : 'Fullscreen'}
          </button>
        </div>
      </div>

      {/* Primary Visual Canvas */}
      <div
        ref={containerRef}
        className={`cv-canvas-viewport ${isDragging ? 'is-dragging' : ''}`}
        onPointerDown={handlePointerDown}
      >
        {/* HUD Crosshairs Overlay */}
        {showReticle && (
          <div className="hud-reticle-overlay" pointer-events="none">
            <div className="hud-corner top-left" />
            <div className="hud-corner top-right" />
            <div className="hud-corner bottom-left" />
            <div className="hud-corner bottom-right" />
            <div className="hud-center-crosshair" />
            <div className="hud-coords-badge">
              89.9°S · 0.0°E · ALT 100.4 km
            </div>
            <div className="hud-scale-badge">
              SCALE: 500m
            </div>
          </div>
        )}

        {/* Viewport Content */}
        <div
          className="canvas-image-layer"
          style={{ transform: `scale(${zoomLevel})`, transformOrigin: 'center center' }}
        >
          {viewMode === 'split' ? (
            <div className="split-canvas-wrapper">
              {/* Underlying Base Image (Reference Frame) */}
              <img
                src={getImageUrl(referenceImageFile)}
                alt="Reference Baseline"
                className="split-img base"
                onError={(e) => handleImgError(e, referenceImageFile)}
                draggable={false}
              />

              {/* Overlaid Clipped Image (Registered Moving Image) */}
              <div
                className="split-clipped-layer"
                style={{ width: `${splitPos}%` }}
              >
                <img
                  src={getImageUrl(registeredImageFile)}
                  alt="Registered Target"
                  className="split-img overlay"
                  onError={(e) => handleImgError(e, registeredImageFile)}
                  draggable={false}
                />
              </div>

              {/* Interactive Divider Line */}
              <div
                className="split-divider-handle"
                style={{ left: `${splitPos}%` }}
              >
                <div className="divider-line" />
                <div className="handle-orb">
                  <span aria-hidden="true">↔</span>
                </div>
              </div>

              {/* Labels */}
              <div className="split-pill-label left">
                Reference Frame (0%)
              </div>
              <div className="split-pill-label right">
                Registered Frame ({Math.round(splitPos)}%)
              </div>
            </div>
          ) : (
            <div className="single-image-wrapper">
              <img
                src={getImageUrl(currentImageFile)}
                alt={viewMode}
                className="viewer-main-img"
                onError={(e) => handleImgError(e, currentImageFile)}
                draggable={false}
              />
            </div>
          )}
        </div>

        {/* Top-Right Telemetry Watermark */}
        <div className="canvas-sensor-watermark">
          <span className="watermark-tag">{sensorName}</span>
          <span className="watermark-orbit">{orbitName}</span>
        </div>
      </div>

      {/* Interactive Bottom Caption & Slider for Split Mode */}
      <div className="viewer-bottom-bar">
        <div className="caption-text-block">
          <span className="caption-mode-title">{activeCaption.title}:</span>
          <span className="caption-mode-hint">{activeCaption.hint}</span>
        </div>

        {viewMode === 'split' ? (
          <div className="split-range-controls">
            <span className="range-tag">REF (0%)</span>
            <input
              type="range"
              min="0"
              max="100"
              value={splitPos}
              onChange={(e) => setSplitPos(Number(e.target.value))}
              className="split-slider-input"
            />
            <span className="range-tag active">REG ({Math.round(splitPos)}%)</span>
          </div>
        ) : (
          <div className="viewer-kpi-pill">
            <span className="kpi-bullet" />
            <span>RMSE: <b>{Number(reprojRmse).toFixed(3)} px</b></span>
            <span className="kpi-divider">|</span>
            <span>Inliers: <b>{inlierCount}</b></span>
          </div>
        )}
      </div>
    </div>
  )
}
