'use client'

export function Header({online,onExport}:{online:boolean;onExport:()=>void}){return <header className="topbar"><div className="brand"><b>LUNARX</b><span>Chandra-Sync</span><small>Autonomous Lunar Image Registration & Matching</small></div><div className="header-actions"><span className="problem-id">PS-SIH26166</span><span className="system-state"><i className={online?'online':''}/>{online?'System online':'System offline'}</span><button className="secondary" onClick={onExport}>Export report</button></div></header>}
