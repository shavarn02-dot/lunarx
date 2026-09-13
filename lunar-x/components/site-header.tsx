'use client'

import React from 'react'

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
  const tabs = [
    { id: 'console', label: 'Mission control', desc: 'Run registration and inspect evidence' },
    { id: 'pipeline', label: 'Pipeline', desc: 'Six-stage architecture' },
    { id: 'benchmarks', label: 'Benchmarks', desc: 'Verified performance data' },
    { id: 'mitigations', label: 'Risks and mitigations', desc: 'Constraints and safeguards' },
    { id: 'information', label: 'Information', desc: 'Mission impact and glossary' },
  ]

  return (
    <header className="chandra-header">
      {/* Top Telemetry & Brand Bar */}
      <div className="header-primary-bar">
        <div className="header-container">
          <div className="product-lockup">
            <span className="product-mark" aria-hidden="true">C</span>
            <span className="product-name">Chandra-sync</span>
          </div>

          <div className="header-telemetry-zone">
            <div className={`engine-status-pill ${apiOnline ? 'online' : 'cached'}`}>
              <span className={`status-pulse-dot ${apiOnline ? 'pulse' : 'off'}`} />
              <div className="status-meta">
                <span className="status-label">{apiOnline ? 'Engine online' : 'Cache mode'}</span>
                <span className="status-device">{apiOnline ? `Device: ${apiDevice}` : 'Air-gapped local demo'}</span>
              </div>
            </div>
            {onExportReport && (
              <button
                type="button"
                className="header-action-btn"
                onClick={onExportReport}
                title="Download mission verification report"
              >
                Export CSV
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
                {isActive && <span className="tab-active-indicator" aria-hidden="true" />}
              </button>
            )
          })}
        </div>
      </div>
    </header>
  )
}
