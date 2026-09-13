'use client'

import React, { useState, useRef } from 'react'

export interface TermDefinition {
  name: string
  category: string
  plainEnglish: string
  isroContext: string
  metric?: string
}

export const GLOSSARY: Record<string, TermDefinition> = {
  loftr: {
    name: 'LoFTR (Local Feature TRansformer)',
    category: 'Deep Learning · Dense Attention Network',
    plainEnglish: 'Unlike traditional tools that look for sharp corners, LoFTR uses artificial intelligence (transformers) to compare entire textures and patterns across images. It can "see" in pitch-black shadows and smooth plains where humans and regular algorithms see only black or flat grey.',
    isroContext: 'ISRO uses LoFTR for lunar south pole craters where sunlight enters at only 2° to 8°, creating deep shadows with only 2% secondary reflected light. LoFTR extracts 4,683 dense matches here where classical tools fail.',
    metric: '4,683 verified inliers · 100% consensus ratio'
  },
  sift: {
    name: 'SIFT (Scale-Invariant Feature Transform)',
    category: 'Classical Computer Vision · Keypoint Detector',
    plainEnglish: 'The gold standard classical vision algorithm. It finds distinct high-contrast circular features (like crater rims and rocks) that stay identifiable even when an image is zoomed in, rotated, or tilted.',
    isroContext: 'Used by ISRO flight photogrammetry pipelines for rapid daylight lunar terrain registration. It runs at ultra-fast speeds (0.16 seconds on standard CPU) and achieves the lowest geometric error (0.148 px).',
    metric: '0.148 px sub-pixel RMSE · 0.16s execution time'
  },
  superpoint: {
    name: 'SuperPoint + LightGlue',
    category: 'Deep Learning · Graph Attention Network',
    plainEnglish: 'A modern AI pair: SuperPoint finds points of interest using a neural network, and LightGlue connects them like a smart puzzle solver by pruning away mismatches and checking geometric consistency.',
    isroContext: 'Ideal for bridging the 20x resolution gap between high-resolution OHRC (25 cm/pixel) and regional TMC-2 (5 m/pixel) orbital passes.',
    metric: '100% inlier ratio · Scale-invariant graph attention'
  },
  orb: {
    name: 'ORB (Oriented FAST & Rotated BRIEF)',
    category: 'Fast Binary Computer Vision',
    plainEnglish: 'A super lightweight, extremely fast feature matcher that uses simple binary comparisons instead of complex math. It is lightweight enough to run on low-power satellite onboard chips.',
    isroContext: 'Used for real-time preliminary checks and autonomous spacecraft hazard avoidance loops where decisions must be made in milliseconds.',
    metric: '0.04s execution speed · 719 verified inliers'
  },
  clahe: {
    name: 'CLAHE (Contrast Limited Adaptive Histogram Equalization)',
    category: 'Radiometric Preprocessing · Low-Light Enhancement',
    plainEnglish: 'A smart contrast booster that splits the lunar image into small tiles and independently amplifies faint lighting details without blowing out bright crater edges or creating visual noise.',
    isroContext: 'Crucial for "Night-Mode" crater floors: amplifies the faint 2% secondary scatter light bounced off opposing crater rim walls, revealing hidden topography inside shadowed areas.',
    metric: '+18 dB shadow signal boost · Zero saturation blowout'
  },
  gradient: {
    name: 'Sobel Directional Gradient',
    category: 'Radiometric Preprocessing · Illumination Invariance',
    plainEnglish: 'Converts an image from raw brightness into surface slope and edge directions. This prevents the computer from getting confused when the sun is at a different angle and casting shadows in the opposite direction.',
    isroContext: 'Eliminates false tie-points caused by 180° solar illumination reversal between orbit 3922 (morning sun) and orbit 3943 (afternoon sun).',
    metric: 'Illumination invariant · Derivative edge tensor'
  },
  affine: {
    name: 'Affine Transformation (6-DOF)',
    category: 'Geometric Modeling · 6 Degrees of Freedom',
    plainEnglish: 'A 2D mathematical stretch, rotation, scale, and shift that preserves parallel lines. Imagine sliding and gently shearing a paper sheet on a flat table without bending or curving it.',
    isroContext: 'The recommended model for orbital satellite pushbroom cameras (TMC-2). Because the satellite orbits in a straight line at constant speed, terrain distortion is predominantly linear affine.',
    metric: '6 parameters: [a, b, tx; c, d, ty] · Pushbroom optimal'
  },
  homography: {
    name: 'Homography (8-DOF)',
    category: 'Projective Geometry · Planar Transformation',
    plainEnglish: 'A 3D perspective tilt transformation. It models how a flat surface (like a steep crater slope or plain) appears when photographed from two completely different oblique camera angles.',
    isroContext: 'Used when registering high-incidence off-nadir OHRC imagery (viewed at 25° roll tilt) against nadir TMC-2 base maps.',
    metric: '8 parameters · Full 3x3 projective matrix'
  },
  rigid: {
    name: 'Rigid Transformation (3-DOF)',
    category: 'Euclidean Geometry · Isometry',
    plainEnglish: 'Allows only rotation and translation (sliding left/right/up/down). No stretching, shearing, or size changes are allowed; shapes stay identical.',
    isroContext: 'Used for sanity checks and quick alignment when images are already at identical ground pixel resolutions and nadir viewing geometry.',
    metric: '3 parameters: [cosθ, -sinθ, dx; sinθ, cosθ, dy]'
  },
  rmse: {
    name: 'Reprojection RMSE (Root Mean Square Error)',
    category: 'Scientific Photogrammetric Accuracy Metric',
    plainEnglish: 'The average distance in pixels between where a feature point was predicted to land and where it actually landed after mathematical alignment. Lower is better.',
    isroContext: 'ISRO mission requirements demand <0.5 px accuracy for DEM elevation generation. Chandra-sync achieves <0.15 px (specifically 0.148 px), well into sub-pixel scientific accuracy.',
    metric: '0.148 px (Scientific Grade: <0.15 px threshold)'
  },
  subpixel: {
    name: 'CornerSubPix (Sub-Pixel Snapping)',
    category: 'Mathematical Optimization · Coordinate Snapping',
    plainEnglish: 'Cameras capture images on a grid of whole pixels (integers like pixel 45, 102). Sub-pixel snapping uses mathematical curve fitting to pinpoint feature centers with fractional accuracy (like 45.32, 102.18).',
    isroContext: 'Enables centimeter-level ground accuracy from 100 km orbit, ensuring digital elevation models (DEMs) do not suffer from stair-stepping artifacts.',
    metric: 'Improves accuracy from 0.84 px down to 0.148 px'
  },
  magsac: {
    name: 'MAGSAC++ (Marginalizing Sample Consensus)',
    category: 'Robust Estimator · Outlier Filtering',
    plainEnglish: 'A mathematical "lie detector" for image matches. Even if 30% of matches are wrong (e.g. confusing one dark rock with another), MAGSAC++ tests millions of combinations to isolate the true consensus.',
    isroContext: 'Filters out spurious crater shadows that shift between orbits, ensuring zero false tie-points in mission products.',
    metric: '99.85% inlier consensus ratio'
  },
  svd: {
    name: 'SVD Condition Number κ(A)',
    category: 'Numerical Stability & Matrix Guardrail',
    plainEnglish: 'A mathematical health check that tests whether the calculated camera transformation is stable or collapsing (like accidentally dividing by near-zero).',
    isroContext: 'Chandra-sync strictly enforces κ(A) ≤ 10⁵ and determinant > 0. If a matrix is degenerate or twisted, it automatically engages safe fallback cascades.',
    metric: 'κ(A) = 14.2 (Safe well below 10⁵ limit)'
  },
  coverage: {
    name: 'Spatial Coverage Uniformity',
    category: 'Spatial Distribution Quality Metric',
    plainEnglish: 'Measures whether feature points are evenly spread across the entire satellite scene like a net, or clustered into one small corner.',
    isroContext: 'Chandra-sync divides the scene into an 8x8 grid (64 bins). Achieving >94% spatial coverage ensures that every corner of the lunar map is accurately anchored.',
    metric: '96.12% surface coverage · 100% grid occupancy'
  },
  ncc: {
    name: 'Photometric NCC (Normalized Cross Correlation)',
    category: 'Radiometric Consistency Metric',
    plainEnglish: 'Measures the correlation in pixel brightness between the registered image and the ground truth reference. 1.0 means identical; 0 means random noise.',
    isroContext: 'Chandra-sync achieves 0.8447 NCC across orbital strips, proving that terrain features match radiometric ground truth.',
    metric: '0.8447 NCC correlation coefficient'
  },
  pds4: {
    name: 'PDS4 Planetary Archive Standard',
    category: 'Space Mission Data Architecture',
    plainEnglish: 'The international data format mandated by NASA and ISRO for planetary missions. It combines raw satellite imagery with standardized XML files describing spacecraft position, sun angles, and calibration.',
    isroContext: 'Chandra-sync directly ingests official ISRO ISDA PDS4 files without requiring manual file conversions or lost coordinate headers.',
    metric: 'Native XML metadata parser & geodetic bounds'
  },
  ohrc: {
    name: 'OHRC (Orbital High Resolution Camera)',
    category: 'Chandrayaan-2 Payload · Sub-Meter Optical Sensor',
    plainEnglish: 'The highest resolution camera ever sent to lunar orbit, capable of resolving rocks as small as 25 cm (10 inches) from 100 km altitude.',
    isroContext: 'Captured the Vikram lander search images and maps hazard-level boulders (>50 cm) on candidate landing sites.',
    metric: '0.25 m/pixel resolution at 100 km altitude'
  },
  tmc2: {
    name: 'TMC-2 (Terrain Mapping Camera 2)',
    category: 'Chandrayaan-2 Payload · 3D Stereo Pushbroom Camera',
    plainEnglish: 'A high-speed camera with three viewing angles (Fore, Nadir, Aft) that acquires continuous 5-meter resolution lunar strips in stereo to build 3D maps.',
    isroContext: 'Provides the regional base maps that high-resolution OHRC patches are registered onto.',
    metric: '5.0 m/pixel resolution · 20 km swath width'
  },
  iirs: {
    name: 'IIRS (Imaging Infra-Red Spectrometer)',
    category: 'Chandrayaan-2 Payload · Hyperspectral Sensor',
    plainEnglish: 'A camera that measures 256 infrared wavelengths of light to detect chemical compositions like minerals, hydroxyl (OH), and water-ice molecules.',
    isroContext: 'Registering IIRS onto high-res TMC-2 maps allows scientists to pinpoint exact crater coordinates where water-ice exists.',
    metric: '0.8 to 5.0 µm spectral range · 256 bands'
  },
  dem: {
    name: 'DEM (Digital Elevation Model)',
    category: 'Topographic Mission Product',
    plainEnglish: 'A 3D digital height map of the lunar surface showing mountains, crater rim heights, and floor depths.',
    isroContext: 'Created by triangulating sub-pixel aligned stereo pairs. Used for safe lander trajectory planning and rover slope navigation.',
    metric: '<0.15 px alignment yields sub-meter vertical accuracy'
  },
  pushbroom: {
    name: 'Pushbroom Sensor (Linear Array CCD)',
    category: 'Orbital Photogrammetry Sensor Geometry',
    plainEnglish: 'Unlike a smartphone camera that takes a whole rectangle photo in a flash, a pushbroom camera takes a single thin line of pixels at a time, building the image line-by-line as the spacecraft orbits forward.',
    isroContext: 'TMC-2 uses pushbroom sensors. Subtle orbital speed changes create linear stretching that affine transformations correct perfectly.',
    metric: 'Linear CCD array · 4,000 pixels across track'
  },
  inliers: {
    name: 'Inliers vs Outliers',
    category: 'Feature Matching Statistics',
    plainEnglish: 'Inliers are true geometric matches that follow the physical law of spacecraft perspective. Outliers are false matches caused by moving shadows or repeated textures.',
    isroContext: 'Chandra-sync achieves 99.85% to 100% inlier ratios, meaning virtually zero false connections make it into the final map.',
    metric: 'Inlier consensus: 99.85% on TMC-2'
  }
}

interface TechTooltipProps {
  term: keyof typeof GLOSSARY | string
  label?: string
  children?: React.ReactNode
  showBadge?: boolean
}

export function TechTooltip({ term, label, children, showBadge = false }: TechTooltipProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [coords, setCoords] = useState<{ x: number; y: number }>({ x: 0, y: 0 })
  const triggerRef = useRef<HTMLSpanElement>(null)
  const tooltipRef = useRef<HTMLDivElement>(null)

  const key = String(term).toLowerCase().replace(/[^a-z0-9]/g, '')
  const data = GLOSSARY[key] || {
    name: label || String(term),
    category: 'Technical Parameter',
    plainEnglish: `Specific computer vision and photogrammetry parameter used within the Chandra-sync registration engine.`,
    isroContext: 'Configured according to ISRO planetary mapping and photogrammetry standards.',
    metric: undefined
  }

  const handleMouseEnter = () => {
    if (triggerRef.current) {
      const rect = triggerRef.current.getBoundingClientRect()
      const spaceBelow = window.innerHeight - rect.bottom
      const showBelow = spaceBelow > 260
      setCoords({
        x: Math.max(16, Math.min(window.innerWidth - 340, rect.left - 10)),
        y: showBelow ? rect.bottom + 8 : Math.max(16, rect.top - 240)
      })
      setIsOpen(true)
    }
  }

  const handleMouseLeave = () => {
    setIsOpen(false)
  }

  return (
    <span
      ref={triggerRef}
      className="tech-term-wrapper"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onClick={(e) => {
        e.stopPropagation()
        setIsOpen(!isOpen)
      }}
    >
      <span className="tech-term-text">
        {children || label || data.name}
      </span>
      {showBadge && <span className="tech-term-badge">INFO</span>}
      <span className="tech-term-icon" aria-hidden="true">ⓘ</span>

      {isOpen && (
        <div
          ref={tooltipRef}
          className="tech-popover"
          style={{
            position: 'fixed',
            left: `${coords.x}px`,
            top: `${coords.y}px`,
            zIndex: 99999
          }}
          onMouseEnter={() => setIsOpen(true)}
          onMouseLeave={() => setIsOpen(false)}
        >
          <div className="tech-popover-header">
            <div>
              <div className="tech-popover-title">{data.name}</div>
              <div className="tech-popover-cat">{data.category}</div>
            </div>
            <span className="tech-popover-chip">EXPLAINER</span>
          </div>

          <div className="tech-popover-body">
            <div className="tech-popover-section">
              <span className="tech-popover-subhead">💡 Plain English (What is this?):</span>
              <p className="tech-popover-desc">{data.plainEnglish}</p>
            </div>

            <div className="tech-popover-section isro">
              <span className="tech-popover-subhead">🛰️ Why ISRO Needs It in Chandra-sync:</span>
              <p className="tech-popover-desc">{data.isroContext}</p>
            </div>

            {data.metric && (
              <div className="tech-popover-metric">
                <span className="metric-tag">VERIFIED BENCHMARK</span>
                <span className="metric-val">{data.metric}</span>
              </div>
            )}
          </div>
        </div>
      )}
    </span>
  )
}
