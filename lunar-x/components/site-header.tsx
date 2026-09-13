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

  const sideNav = [
    { id: 'console', label: 'Home', icon: '⌂' },
    { id: 'console', label: 'Image registration', icon: '▧' },
    { id: 'benchmarks', label: 'Results', icon: '▤' },
    { id: 'pipeline', label: 'Methodology', icon: '◫' },
    { id: 'information', label: 'About project', icon: 'ⓘ' },
    { id: 'information', label: 'Documentation', icon: '▣' },
  ]

  return (
    <>
      <header className="chandra-header">
        <div className="header-primary-bar">
          <div className="header-container">
            <div className="product-lockup">
              <span className="product-mark" aria-hidden="true">◐</span>
              <div>
                <span className="product-name">LUNARX</span>
                <span className="product-subtitle">Aligning lunar images for a clearer tomorrow</span>
              </div>
            </div>
            <div className="institution-lockup">
              <span className="isro-wordmark">ISRO</span>
              <div><strong>PS - SIH26166</strong><small>Chandrayaan-2 image registration system</small></div>
            </div>
            <div className="header-telemetry-zone">
              <div className={`engine-status-pill ${apiOnline ? 'online' : 'cached'}`}>
                <span className={`status-pulse-dot ${apiOnline ? 'pulse' : 'off'}`} />
                <span className="status-label">{apiOnline ? 'Engine online' : 'Local demo'}</span>
              </div>
              {onExportReport && <button type="button" className="header-action-btn" onClick={onExportReport}>⇩ &nbsp; Export report</button>}
            </div>
          </div>
        </div>
      </header>
      <aside className="lunar-sidebar" aria-label="Project navigation">
        <nav>
          {sideNav.map((item, index) => (
            <button key={`${item.label}-${index}`} type="button" className={`sidebar-link ${activeTab === item.id && (index === 0 || index > 1) ? 'active' : ''}`} onClick={() => setActiveTab(item.id)}>
              <span className="sidebar-icon" aria-hidden="true">{item.icon}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </nav>
        <div className="sidebar-quote">“Exploring the Moon<br />with better insights”<br /><span>— LUNARX</span></div>
      </aside>
    </>
  )
}
