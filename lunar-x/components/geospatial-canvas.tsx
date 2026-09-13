"use client"
import React, { useState, useRef, useCallback, useEffect } from "react"
import type { ImageInfo, RegistrationResult } from "./types"

interface GeospatialCanvasProps {
  source: ImageInfo
  reference: ImageInfo
  result: RegistrationResult | null
  running: boolean
  viewMode: "split" | "matches" | "checkerboard" | "difference" | "side"
  loupeActive: boolean
  showGrid: boolean
}

export function GeospatialCanvas({
  source,
  reference,
  result,
  running,
  viewMode,
  loupeActive,
  showGrid,
}: GeospatialCanvasProps) {
  const [sliderPos, setSliderPos] = useState(50)
  const [isDragging, setIsDragging] = useState(false)
  const [mousePos, setMousePos] = useState<{ x: number; y: number; relX: number; relY: number } | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  const registeredImg = result?.images?.registered || reference.preview
  const rawSourceImg = source.preview
  const matchesImg = result?.images?.matches
  const checkerboardImg = result?.images?.checkerboard
  const diffImg = result?.images?.difference

  const handlePointerMove = useCallback(
    (e: React.PointerEvent<HTMLDivElement> | PointerEvent) => {
      if (!containerRef.current) return
      const rect = containerRef.current.getBoundingClientRect()
      const x = Math.max(0, Math.min(e.clientX - rect.left, rect.width))
      const y = Math.max(0, Math.min(e.clientY - rect.top, rect.height))
      const pct = Math.max(2, Math.min(98, (x / rect.width) * 100))

      setMousePos({ x, y, relX: x / rect.width, relY: y / rect.height })
      if (isDragging) {
        setSliderPos(pct)
      }
    },
    [isDragging]
  )

  const handlePointerDown = (e: React.PointerEvent<HTMLDivElement>) => {
    setIsDragging(true)
    handlePointerMove(e)
  }

  const handlePointerUp = useCallback(() => {
    setIsDragging(false)
  }, [])

  useEffect(() => {
    if (isDragging) {
      window.addEventListener("pointerup", handlePointerUp)
      window.addEventListener("pointermove", handlePointerMove)
      return () => {
        window.removeEventListener("pointerup", handlePointerUp)
        window.removeEventListener("pointermove", handlePointerMove)
      }
    }
  }, [isDragging, handlePointerUp, handlePointerMove])

  return (
    <div
      ref={containerRef}
      className={`geospatial-canvas ${running ? "scanning" : ""}`}
      onPointerDown={viewMode === "split" ? handlePointerDown : undefined}
      onPointerMove={handlePointerMove}
      onPointerLeave={() => setMousePos(null)}
    >
      {/* Radar scanning line during execution */}
      {running && <div className="radar-sweep" />}

      {/* Coordinate Grid HUD Overlay */}
      {showGrid && (
        <div className="coordinate-grid-hud">
          <div className="grid-line horizontal" style={{ top: "25%" }}>
            <span>32°10' S</span>
          </div>
          <div className="grid-line horizontal" style={{ top: "50%" }}>
            <span>40°00' S (Orbit Meridian)</span>
          </div>
          <div className="grid-line horizontal" style={{ top: "75%" }}>
            <span>67°45' S</span>
          </div>
          <div className="grid-line vertical" style={{ left: "25%" }}>
            <span>19°12' E</span>
          </div>
          <div className="grid-line vertical" style={{ left: "50%" }}>
            <span>22°30' E</span>
          </div>
          <div className="grid-line vertical" style={{ left: "75%" }}>
            <span>41°05' E</span>
          </div>
          <div className="reticle reticle-center" />
          <div className="reticle-coords">
            LAT: -40.00° / LON: +22.50° · ELEV: -1,842m · SUB-PIXEL 0.05m
          </div>
        </div>
      )}

      {/* VIEW MODES */}
      {viewMode === "split" && (
        <div className="split-view-container">
          {/* Base Layer: Registered Aligned (or Reference) */}
          <div className="layer registered-layer">
            <img src={registeredImg} alt="Registered Target" />
            <div className="layer-tag right-tag">
              <span>{result ? "REGISTERED ALIGNMENT" : "REFERENCE IMAGE"}</span>
              <small>{reference.filename}</small>
            </div>
          </div>

          {/* Top Layer: Unregistered Source, clipped by slider */}
          <div
            className="layer source-layer"
            style={{ clipPath: `inset(0 calc(100% - ${sliderPos}%) 0 0)` }}
          >
            <img src={rawSourceImg} alt="Raw Source" />
            <div className="layer-tag left-tag">
              <span>RAW UNREGISTERED</span>
              <small>{source.filename}</small>
            </div>
          </div>

          {/* Interactive Split Divider Handle */}
          <div className="split-handle" style={{ left: `${sliderPos}%` }}>
            <div className="handle-line" />
            <div className="handle-pill">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <path d="M15 18l-6-6 6-6" />
                <path d="M9 18l6-6-6-6" />
              </svg>
            </div>
          </div>
        </div>
      )}

      {viewMode === "matches" && (
        <div className="single-view-container">
          <img src={matchesImg || rawSourceImg} alt="Feature Correspondence Matches" />
          <div className="layer-tag full-tag">
            <span>INLIER CORRESPONDENCE VECTORS (USAC-MAGSAC)</span>
            <small>{result?.metrics?.inliers ?? 0} verified tie points</small>
          </div>
        </div>
      )}

      {viewMode === "checkerboard" && (
        <div className="single-view-container">
          <img src={checkerboardImg || rawSourceImg} alt="Alignment Checkerboard" />
          <div className="layer-tag full-tag">
            <span>CHECKERBOARD CONTINUITY VERIFICATION</span>
            <small>8x8 tile overlay</small>
          </div>
        </div>
      )}

      {viewMode === "difference" && (
        <div className="single-view-container">
          <img src={diffImg || rawSourceImg} alt="Photometric Difference Residual" />
          <div className="layer-tag full-tag">
            <span>PHOTOMETRIC RESIDUAL ERROR MAP</span>
            <small>NCC: {result?.metrics?.photometric_ncc ?? "N/A"}</small>
          </div>
        </div>
      )}

      {viewMode === "side" && (
        <div className="side-by-side-container">
          <div className="side-pane">
            <img src={rawSourceImg} alt="Source" />
            <div className="layer-tag">
              <span>SOURCE</span>
              <small>{source.filename}</small>
            </div>
          </div>
          <div className="side-pane">
            <img src={registeredImg} alt="Registered" />
            <div className="layer-tag">
              <span>{result ? "REGISTERED" : "REFERENCE"}</span>
              <small>{reference.filename}</small>
            </div>
          </div>
        </div>
      )}

      {/* Magnifying Loupe Tool (Hover 4x zoom) */}
      {loupeActive && mousePos && (
        <div
          className="magnifying-loupe"
          style={{
            left: `${mousePos.x}px`,
            top: `${mousePos.y}px`,
            backgroundImage: `url(${registeredImg})`,
            backgroundPosition: `${mousePos.relX * 100}% ${mousePos.relY * 100}%`,
          }}
        >
          <div className="loupe-reticle" />
          <span className="loupe-badge">4X SUB-PIXEL</span>
        </div>
      )}
    </div>
  )
}
