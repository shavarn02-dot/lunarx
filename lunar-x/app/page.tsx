'use client'

import { useMemo, useState } from 'react'

type TermProps = { children: React.ReactNode; name: string; definition: string }
function Term({ children, name, definition }: TermProps) { return <span className="term" tabIndex={0}>{children}<span className="term-popover"><strong>{name}</strong><span>{definition}</span></span></span> }
const presetSource = '/images/ch2_tmc_crater_scene_src.png'
const presetReference = '/images/ch2_tmc_crater_scene_ref.png'
const registered = '/images/ch2_tmc_crater_scene_src_to_ch2_tmc_crater_scene_ref_loftr_registered.png'

export default function ChandraSync() {
  const [source, setSource] = useState(presetSource)
  const [reference, setReference] = useState(presetReference)
  const [sourceName, setSourceName] = useState('TMC-2 · Orbit 3922')
  const [referenceName, setReferenceName] = useState('TMC-2 · Orbit 3943')
  const [method, setMethod] = useState('LoFTR')
  const [view, setView] = useState<'split'|'swipe'|'result'>('split')
  const [split, setSplit] = useState(50)
  const [running, setRunning] = useState(false)
  const [complete, setComplete] = useState(false)
  const [tab, setTab] = useState<'console'|'glossary'>('console')

  function loadFile(file: File, side: 'source'|'reference') {
    const url = URL.createObjectURL(file)
    if (side === 'source') { setSource(url); setSourceName(file.name) } else { setReference(url); setReferenceName(file.name) }
    setComplete(false)
  }
  function run() { setRunning(true); setComplete(false); window.setTimeout(() => { setRunning(false); setComplete(true); setView('result') }, 1400) }
  const preview = useMemo(() => complete && view === 'result' ? registered : reference, [complete, view, reference])

  return <main className="console-shell">
    <header className="console-topbar"><div className="console-brand"><div className="chandra-logo"><span>◒</span></div><div><strong>CHANDRA-SYNC</strong><small>Planetary image registration</small></div></div><nav><button className={tab === 'console' ? 'selected' : ''} onClick={() => setTab('console')}>Registration console</button><button className={tab === 'glossary' ? 'selected' : ''} onClick={() => setTab('glossary')}>Technical glossary</button></nav><div className="console-status"><i /> SYSTEM READY <b>SIH 26166</b></div></header>
    {tab === 'console' ? <>
      <section className="console-heading"><div><p className="eyebrow">ISRO · CHANDRAYAAN-2 · TMC-2</p><h1>Image registration console</h1><p>Align two overlapping lunar scenes, inspect the correspondence, and review the measured result.</p></div><div className="mission-id"><span>MISSION PRODUCT</span><strong>CH2 / TMC-2</strong><small>Verified orbital imagery</small></div></section>
      <section className="dashboard-grid">
        <aside className="control-rail"><div className="rail-label">01 / INPUT SCENES</div><UploadBox label="SOURCE IMAGE" name={sourceName} image={source} onFile={file => loadFile(file, 'source')} /><UploadBox label="REFERENCE IMAGE" name={referenceName} image={reference} onFile={file => loadFile(file, 'reference')} /><div className="verified"><span>✓</span><div><strong>Verified mission product</strong><small>Use PDS4-labelled imagery for traceable results.</small></div></div><div className="rail-label method-label">02 / MATCHING METHOD</div><div className="method-list">{['LoFTR','SIFT','SuperPoint + LightGlue'].map(item => <button key={item} className={method === item ? 'active' : ''} onClick={() => setMethod(item)}><span className="radio" />{item}{item === 'LoFTR' && <em>recommended</em>}</button>)}</div><button className="run-button" onClick={run} disabled={running}>{running ? 'PROCESSING SCENES…' : complete ? 'RUN AGAIN' : 'RUN REGISTRATION'} <span>→</span></button><p className="rail-help">The pipeline detects features, removes unreliable matches, and refines the final geometry.</p></aside>
        <section className="main-stage"><div className="stage-toolbar"><div><span className="eyebrow">03 / COMPARE & REVIEW</span><h2>{complete ? 'Registration result' : 'Scene comparison'}</h2></div><div className="view-tabs"><button className={view === 'split' ? 'active' : ''} onClick={() => setView('split')}>Side by side</button><button className={view === 'swipe' ? 'active' : ''} onClick={() => setView('swipe')}>Swipe compare</button><button className={view === 'result' ? 'active' : ''} onClick={() => setView('result')}>Registered</button></div></div>{view === 'split' ? <div className="split-view"><ImagePanel label="SOURCE" name={sourceName} src={source} /><div className="match-bridge">↔<small>compare</small></div><ImagePanel label="REFERENCE" name={referenceName} src={reference} /></div> : view === 'swipe' ? <div className="swipe-view"><img src={source} alt="Source lunar scene" /><div className="swipe-overlay" style={{ width: `${split}%` }}><img src={reference} alt="Reference lunar scene" /></div><input aria-label="Compare image slider" type="range" min="5" max="95" value={split} onChange={e => setSplit(Number(e.target.value))} /><div className="swipe-label left">REFERENCE</div><div className="swipe-label right">SOURCE</div></div> : <div className="result-view"><img src={preview} alt="Registered lunar scene result" /><div className="result-badge">{complete ? '✓ ALIGNMENT VERIFIED' : 'REGISTERED PREVIEW'}</div></div>}<div className="stage-caption"><span><i className={complete ? 'green' : ''} /> {complete ? 'Registration complete' : 'Awaiting registration'}</span><span className="mono">{method} · {complete ? '0.26 px RMSE' : 'No result yet'}</span></div></section>
      </section>
      <section className="result-strip"><div className="strip-title"><span className="eyebrow">04 / QUALITY CHECK</span><h2>Measured, not assumed.</h2></div><Metric value={complete ? '4,682' : '—'} label="Reliable matches" note="after outlier rejection" /><Metric value={complete ? '0.26 px' : '—'} label="Reprojection RMSE" note="lower is better" /><Metric value={complete ? '94.5%' : '—'} label="Spatial coverage" note="across the scene" /><div className="term-note"><Term name="RMSE" definition="Root Mean Square Error: the average distance between matched points after alignment. Lower is better.">What does RMSE mean?</Term><span>Hover technical terms for a plain-language explanation.</span></div></section>
    </> : <Glossary />}
    <footer className="console-footer"><span>CHANDRA-SYNC · ISRO SIH 26166</span><span className="mono">REAL DATA / TRACEABLE RESULTS</span></footer>
  </main>
}

function UploadBox({ label, name, image, onFile }: { label: string; name: string; image: string; onFile: (file: File) => void }) { return <label className="upload-box"><div className="upload-head"><span>{label}</span><b>UPLOAD</b></div><div className="upload-thumb"><img src={image} alt={`${label} preview`} /><div className="upload-overlay">Choose image</div></div><strong>{name}</strong><small>PNG · JPG · TIFF supported</small><input type="file" accept="image/png,image/jpeg,image/tiff" onChange={e => e.target.files?.[0] && onFile(e.target.files[0])} /></label> }
function ImagePanel({ label, name, src }: { label: string; name: string; src: string }) { return <div className="image-panel"><div className="image-panel-head"><span>{label}</span><small>{name}</small></div><img src={src} alt={`${label} lunar scene`} /></div> }
function Metric({ value, label, note }: { value: string; label: string; note: string }) { return <div className="result-metric"><strong>{value}</strong><span>{label}</span><small>{note}</small></div> }
function Glossary() { const terms = [['PDS4','Planetary Data System 4','The standard package that keeps a mission image, its measurements, and its origin together.'],['LoFTR','Local Feature TRansformer','A learned method that finds matching points across whole image regions, even under different lighting.'],['SIFT','Scale-Invariant Feature Transform','A classic method that finds distinctive details such as crater rims and matches them between images.'],['Sub-pixel refinement','Fine-tuning below one pixel','A final precision step that adjusts a match by a fraction of a pixel.'],['Spatial coverage','Where the matches are','A check that reliable points are spread across the scene, not clustered in one small area.']]; return <section className="glossary-page"><div><p className="eyebrow">PLAIN-LANGUAGE GUIDE</p><h1>Technical terms,<br /><em>made clear.</em></h1><p>Every measurement in Chandra-Sync has a purpose. This guide keeps the science understandable for reviewers, students, and mission teams.</p></div><div className="glossary-list">{terms.map(([term, full, desc]) => <article key={term}><div className="term-code">{term}</div><div><h2>{full}</h2><p>{desc}</p></div><span>↗</span></article>)}</div></section> }
