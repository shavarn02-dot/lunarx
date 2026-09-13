'use client'

import React from 'react'

interface ChandraLogoProps {
  size?: 'sm' | 'md' | 'lg'
  showSubtitle?: boolean
}

export function ChandraLogo({ size = 'md', showSubtitle = true }: ChandraLogoProps) {
  const iconSize = size === 'sm' ? 32 : size === 'lg' ? 48 : 40

  return (
    <div className={`chandra-brand-lockup size-${size}`}>
      <div className="chandra-logo-container" style={{ width: iconSize, height: iconSize }}>
        <svg
          viewBox="0 0 100 100"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="chandra-logo-svg"
        >
          <defs>
            {/* Outer Glow filter */}
            <filter id="lunar-glow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>

            {/* Saffron and Cyan Gradients */}
            <linearGradient id="orbit-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#F97316" />
              <stop offset="50%" stopColor="#FF9E58" />
              <stop offset="100%" stopColor="#38BDF8" />
            </linearGradient>

            <linearGradient id="moon-grad" x1="20%" y1="0%" x2="80%" y2="100%">
              <stop offset="0%" stopColor="#FFFFFF" />
              <stop offset="60%" stopColor="#E2E8F0" />
              <stop offset="100%" stopColor="#64748B" />
            </linearGradient>

            <radialGradient id="space-bg" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#1E293B" />
              <stop offset="100%" stopColor="#0B0E17" />
            </radialGradient>
          </defs>

          {/* Deep Space Outer Ring */}
          <circle cx="50" cy="50" r="48" fill="url(#space-bg)" stroke="rgba(56, 189, 248, 0.3)" strokeWidth="1.5" />

          {/* Reticle Radar Coordinates */}
          <circle cx="50" cy="50" r="38" stroke="rgba(255, 255, 255, 0.08)" strokeDasharray="3 3" strokeWidth="1" />
          <line x1="50" y1="6" x2="50" y2="18" stroke="#38BDF8" strokeWidth="1.5" />
          <line x1="50" y1="82" x2="50" y2="94" stroke="#38BDF8" strokeWidth="1.5" />
          <line x1="6" y1="50" x2="18" y2="50" stroke="#38BDF8" strokeWidth="1.5" />
          <line x1="82" y1="50" x2="94" y2="50" stroke="#38BDF8" strokeWidth="1.5" />

          {/* Stylized Lunar Crescent */}
          <path
            d="M 54 22 C 37 22 24 35 24 52 C 24 69 37 82 54 82 C 43 78 36 66 36 52 C 36 38 43 26 54 22 Z"
            fill="url(#moon-grad)"
            filter="url(#lunar-glow)"
          />

          {/* Micro Crater Details */}
          <circle cx="34" cy="46" r="2.2" fill="#475569" opacity="0.6" />
          <circle cx="40" cy="62" r="3.0" fill="#475569" opacity="0.5" />
          <circle cx="36" cy="34" r="1.8" fill="#475569" opacity="0.6" />

          {/* Elliptical Chandrayaan Orbital Path */}
          <ellipse
            cx="50"
            cy="50"
            rx="41"
            ry="21"
            transform="rotate(-28 50 50)"
            stroke="url(#orbit-grad)"
            strokeWidth="2.2"
            strokeDasharray="6 3"
            strokeLinecap="round"
          />

          {/* Active Spacecraft / Synced Node Reticle */}
          <g transform="translate(74, 30)">
            <circle cx="0" cy="0" r="4.5" fill="#F97316" />
            <circle cx="0" cy="0" r="8" stroke="#F97316" strokeWidth="1" opacity="0.7">
              <animate attributeName="r" values="5;11;5" dur="2s" repeatCount="indefinite" />
              <animate attributeName="opacity" values="0.8;0;0.8" dur="2s" repeatCount="indefinite" />
            </circle>
            {/* Satellite Solar Panels */}
            <line x1="-7" y1="0" x2="-4.5" y2="0" stroke="#38BDF8" strokeWidth="2" />
            <line x1="4.5" y1="0" x2="7" y2="0" stroke="#38BDF8" strokeWidth="2" />
          </g>

          {/* Central Target Crosshair */}
          <circle cx="50" cy="50" r="1.5" fill="#10B981" />
        </svg>
      </div>

      <div className="chandra-brand-text">
        <div className="chandra-title-wrap">
          <span className="chandra-brand-name">CHANDRA<span className="accent-sync">-SYNC</span></span>
          <span className="isro-badge">ISRO · SIH26166</span>
        </div>
        {showSubtitle && (
          <div className="chandra-brand-sub">
            Sub-Pixel Autonomous Lunar Image Registration &amp; Mission Photogrammetry
          </div>
        )}
      </div>
    </div>
  )
}
