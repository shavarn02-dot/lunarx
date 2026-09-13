'use client'

import React, { useState, useEffect } from 'react'
import { ChandraLogo } from './chandra-logo'

interface SiteHeaderProps {
  apiOnline: boolean
  apiDevice: string
  activeTab: string
  setActiveTab: (tab: string) => void
  onExportReport?: () => void
}

export function SiteHeader({
  apiOnline,
  apiDevice,
  activeTab,
  setActiveTab,
  onExportReport
}: SiteHeaderProps) {
  const [currentTimeUTC, setCurrentTimeUTC] = useState('')
  const [currentTimeIST, setCurrentTimeIST] = useState('')

  useEffect(() => {
    const updateTime = () => {
      const now = new Date()
      // UTC time
      setCurrentTimeUTC(now.toISOString().substring(11, 19) + ' UTC')
      // IST time (+5:30)
      const istDate = new Date(now.getTime() + 5.5 * 60 * 60 * 1000)
      setCurrentTimeIST(istDate.toISOString().substring(11, 19) + ' IST')
    }
    updateTime()
    const timer = setInterval(updateTime, 1000)
    return () => clearInterval(timer)
  }, [])

  const tabs = [
    { id: 'console', label: '⚡ Mission Control', desc: 'Active Ingestion & Visual Inspector' },
    { id: 'pipeline', label: '🔄 6-Stage Pipeline', desc: 'PDS4 to GeoTIFF Architecture' },
    { id: 'benchmarks', label: '📊 Verified Benchmarks', desc: 'Quantitative Accuracy & Charts' },
    { id: 'mitigations', label: '🛡️ Showstoppers & Risks', desc: 'Shadow Inversion & Scale Gaps' },
    { id: 'usecases', label: '🚀 Mission Impact & DEM', desc: 'Vikram Lander & PRADAN Products' },
    { id: 'glossary', label: '📖 Non-Tech Glossary', desc: 'Interactive Explanations for Judges' },
  ]

  return (
    <header className="chandra-header">
      {/* Top Telemetry & Brand Bar */}
      <div className="header-primary-bar">
        <div className="header-container">
          {/* Brand Logo Lockup */}
          <ChandraLogo size="md" showSubtitle={true} />

          {/* Telemetry Status Indicators */}
          <div className="header-telemetry-zone">
            {/* Mission Clock Clocks */}
            <div className="telemetry-clocks">
              <span className="clock-item">
                <span className="clock-dot live" />
                <span className="clock-val">{currentTimeUTC || '12:00:00 UTC'}</span>
              </span>
              <span className="clock-sep">/</span>
              <span className="clock-item">
                <span className="clock-val ist">{currentTimeIST || '17:30:00 IST'}</span>
              </span>
            </div>

            {/* Sensor Resoluton Badges */}
            <div className="sensor-tags-row">
              <span className="sensor-tag ohrc" title="Orbital High Resolution Camera (0.25 m/px)">
                OHRC 0.25m
              </span>
              <span className="sensor-tag tmc" title="Terrain Mapping Camera 2 (5.0 m/px)">
                TMC-2 5.0m
              </span>
              <span className="sensor-tag iirs" title="Imaging Infra-Red Spectrometer (Hyperspectral)">
                IIRS Hyper
              </span>
            </div>

            {/* Backend Engine Status Card */}
            <div className={`engine-status-pill ${apiOnline ? 'online' : 'cached'}`}>
              <span className={`status-pulse-dot ${apiOnline ? 'pulse' : 'off'}`} />
              <div className="status-meta">
                <span className="status-label">
                  {apiOnline ? 'FASTAPI ENGINE ONLINE' : 'VERIFIED CACHE MODE'}
                </span>
                <span className="status-device">
                  {apiOnline ? `Device: ${apiDevice}` : 'Air-Gapped Local Demo'}
                </span>
              </div>
            </div>

            {/* Quick Export Action */}
            {onExportReport && (
              <button
                type="button"
                className="header-action-btn"
                onClick={onExportReport}
                title="Download SIH26166 Mission Verification Report"
              >
                📥 Export CSV
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Navigation Tab Bar */}
      <div className="header-nav-bar">
        <div className="header-container nav-scroll">
          {tabs.map((tab) => {
            const isActive = activeTab === tab.id
            return (
              <button
                key={tab.id}
                type="button"
                className={`nav-tab-link ${isActive ? 'active' : ''}`}
                onClick={() => setActiveTab(tab.id)}
              >
                <span className="tab-title">{tab.label}</span>
                <span className="tab-desc">{tab.desc}</span>
                {isActive && <div className="tab-active-indicator" />}
              </button>
            )
          })}
        </div>
      </div>
    </header>
  )
}
