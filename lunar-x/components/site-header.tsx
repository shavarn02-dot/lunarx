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
      <div className="header-primary-bar">
        <div className="header-container">
          <div className="product-lockup">
            <span className="product-mark" aria-hidden="true">◐</span>
            <div>
              <span className="product-name">LUNARX</span>
              <span className="product-subtitle">Lunar image registration workspace</span>
            </div>
          </div>
          <div className="header-context"><strong>PS-SIH26166</strong><span>Chandrayaan-2</span></div>
          <div className="header-telemetry-zone">
            <span className={`header-status ${apiOnline ? 'online' : ''}`}><span className="status-pulse-dot" />{apiOnline ? 'Connected' : 'Local processing'}</span>
            {onExportReport && <button type="button" className="header-action-btn" onClick={onExportReport}>Export report</button>}
          </div>
        </div>
      </div>
      <nav className="header-nav-bar" aria-label="Workspace sections">
        <div className="header-container nav-scroll">
          {tabs.map((tab) => {
            const isActive = activeTab === tab.id
            return <button key={tab.id} type="button" className={`nav-tab-link ${isActive ? 'active' : ''}`} onClick={() => setActiveTab(tab.id)}><span className="tab-title">{tab.label}</span><span className="tab-desc">{tab.desc}</span></button>
          })}
        </div>
      </nav>
    </header>
  )
}
