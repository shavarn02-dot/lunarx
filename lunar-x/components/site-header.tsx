'use client'

import { Moon, Help, Workspace, Analytics, Download } from '@carbon/icons-react'

interface SiteHeaderProps {
  online: boolean
  activeTab: 'workspace' | 'results'
  onTabChange: (tab: 'workspace' | 'results') => void
  onHelp: () => void
  onExport: () => void
  hasResult: boolean
}

export function SiteHeader({ online, activeTab, onTabChange, onHelp, onExport, hasResult }: SiteHeaderProps) {
  return (
    <header className="site-header">
      <div className="brand-row">
        <a href="/" className="brand" aria-label="Chandra-sync home">
          <span className="brand-symbol"><Moon size={27} /></span>
          <span className="brand-name">chandra<span className="brand-light">sync</span><span className="brand-caption font-mono">LUNAR IMAGE REGISTRATION</span></span>
        </a>
        <div className="header-right"><span className="mission-label font-mono">CHANDRAYAAN–2 <span>/ RESEARCH WORKSPACE</span></span><button className="icon-button" onClick={onHelp} aria-label="Open quick guide"><Help size={20} /></button></div>
      </div>
      <div className="navigation-row">
        <nav aria-label="Main navigation">
          <button className={`nav-link ${activeTab === 'workspace' ? 'active' : ''}`} aria-current={activeTab === 'workspace' ? 'page' : undefined} onClick={() => onTabChange('workspace')}><Workspace size={17} />Workspace</button>
          <button className={`nav-link ${activeTab === 'results' ? 'active' : ''}`} aria-current={activeTab === 'results' ? 'page' : undefined} onClick={() => onTabChange('results')}><Analytics size={17} />Results{hasResult && <span className="result-count">1</span>}</button>
        </nav>
        <div className="navigation-actions"><span className={`connection ${online ? 'online' : ''}`}><span className="status-dot" />{online ? 'Engine connected' : 'Engine offline'}</span><button className="subtle-button export-button" disabled={!hasResult} onClick={onExport}><Download size={16} />Export report</button></div>
      </div>
    </header>
  )
}
