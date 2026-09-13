'use client'
import { Explainer } from './explainer'

export function Header({
  online,
  onExport,
}: {
  online: boolean
  onExport: () => void
}) {
  return (
    <header className="topbar">
      <div className="brand">
        <b>LUNARX</b>
        <span>Chandra-Sync</span>
        <small>Autonomous Lunar Image Registration & Matching</small>
      </div>
      <div className="header-actions">
        <Explainer termKey="team_id_banner" showIndicator={true}>
          <span className="problem-id">PS-SIH26166</span>
        </Explainer>
        <Explainer termKey="system_state" showIndicator={true}>
          <span className="system-state">
            <i className={online ? 'online' : ''} />
            {online ? 'System online' : 'System offline'}
          </span>
        </Explainer>
        <Explainer termKey="export_report" showIndicator={true}>
          <button className="secondary" onClick={onExport}>
            Export report
          </button>
        </Explainer>
      </div>
    </header>
  )
}
