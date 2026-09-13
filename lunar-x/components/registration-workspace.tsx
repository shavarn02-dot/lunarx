'use client'

import { useEffect, useRef, useState } from 'react'
import { ArrowRight, Close, Information, Reset, Help } from '@carbon/icons-react'
import { SiteHeader } from './site-header'
import { InteractiveViewer, type ViewMode } from './interactive-viewer'
import { RegistrationControls } from './registration-controls'
import { RegistrationResults } from './registration-results'
import { PAIRS, DEFAULT_SETTINGS, downloadReport, type ImagePair, type Settings, type Benchmark, type RegistrationResult } from './registration-data'

export function RegistrationWorkspace({ initialOnline, benchmark }: { initialOnline: boolean; benchmark: Benchmark }) {
  const [tab, setTab] = useState<'workspace' | 'results'>('workspace')
  const [pair, setPair] = useState(PAIRS[0])
  const [settings, setSettings] = useState<Settings>(DEFAULT_SETTINGS)
  const [online, setOnline] = useState(initialOnline)
  const [busy, setBusy] = useState(false)
  const [result, setResult] = useState<RegistrationResult | null>(null)
  const [mode, setMode] = useState<ViewMode>('original')
  const [message, setMessage] = useState('')
  const help = useRef<HTMLDialogElement>(null)
  const feedback = useRef<HTMLDivElement>(null)
  useEffect(() => {
    if (message) feedback.current?.scrollIntoView({ block: 'nearest', behavior: 'instant' })
  }, [message])
  const invalidate = () => { setResult(null); setMode('original'); setMessage('') }
  const changePair = (next: ImagePair) => { invalidate(); setPair(next) }
  const changeSettings = (next: Settings) => { invalidate(); setSettings(next) }
  const example = () => {
    const stem = 'ch2_tmc_crater_scene_src_to_ch2_tmc_crater_scene_ref_sift'
    setPair(PAIRS[0]); setSettings(DEFAULT_SETTINGS); setMode('overlay'); setMessage('')
    setResult({ success: true, runtime_sec: benchmark.runtime_sec, metrics: benchmark, images: { matches: `${stem}_matches.png`, registered: `${stem}_registered.png`, checkerboard: `${stem}_checkerboard.png`, difference: `${stem}_difference.png` }, provenance: 'saved', pairName: PAIRS[0].name, method: benchmark.method, preprocessing: benchmark.preprocessing })
  }
  const reconnect = async () => {
    setBusy(true)
    try { const response = await fetch('/api/engine/health'); setOnline(response.ok); setMessage(response.ok ? 'Processing engine connected. You can run a registration.' : 'The Python processing engine is unavailable. You can still compare images and explore the saved example.') }
    catch { setOnline(false); setMessage('Could not reach the processing engine. Please try again.') }
    finally { setBusy(false) }
  }
  const run = async () => {
    setBusy(true); setMessage(''); setResult(null); setMode('original')
    try {
      const response = await fetch('/api/engine/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ source_filename: pair.source, reference_filename: pair.reference, ...settings }), signal: AbortSignal.timeout(180000) })
      const data = await response.json()
      if (!response.ok) { if (response.status === 503) setOnline(false); throw new Error(data.error || data.detail || 'Registration could not be completed.') }
      setOnline(true)
      if (!data.success || !data.metrics || !data.images) throw new Error(data.error || 'The engine could not find a reliable alignment. Try another matching method or image pair.')
      setResult({ ...data, provenance: 'live', pairName: pair.name, method: settings.method, preprocessing: settings.preprocessing }); setMode('overlay')
      setMessage('Registration complete. Inspect the aligned images and quality measurements below.')
    } catch (error) { setMessage(error instanceof Error ? error.message : 'Registration failed. Please try again.') }
    finally { setBusy(false) }
  }
  const upload = async (source: File, reference: File) => {
    if ([source, reference].some(file => file.size > 20 * 1024 * 1024 || !/\.(png|jpe?g|tiff?)$/i.test(file.name))) { setMessage('Choose PNG, JPEG or TIFF images under 20 MB each.'); return }
    setBusy(true); setMessage('')
    try {
      const send = async (file: File) => {
        const form = new FormData(); form.append('file', file)
        const response = await fetch('/api/engine/upload', { method: 'POST', body: form })
        const data = await response.json()
        if (!response.ok || !data.filename) throw new Error(data.error || 'Image upload failed.')
        return data.filename as string
      }
      const src = await send(source); const ref = await send(reference)
      changePair({ id: 'custom', name: 'Uploaded image pair', source: src, reference: ref, sensor: 'CUSTOM', description: `${source.name} / ${reference.name}` }); setOnline(true)
    } catch (error) { setMessage(error instanceof Error ? error.message : 'Could not upload images. Please try again.') }
    finally { setBusy(false) }
  }
  return (
    <div className="app-shell">
      <SiteHeader online={online} activeTab={tab} onTabChange={setTab} onHelp={() => help.current?.showModal()} onExport={() => result && downloadReport(result)} hasResult={Boolean(result)} />
      <main id="workspace">
        <div className="workspace-intro"><div><div className="eyebrow font-mono">CHANDRAYAAN–2 / IMAGE ANALYSIS</div><h1>{tab === 'workspace' ? 'A clearer frame of reference.' : 'Alignment, measured.'}</h1><p>{tab === 'workspace' ? 'Compare lunar terrain. Align observations. Inspect every detail.' : 'Review registration quality and take your outputs further.'}</p></div><button className="subtle-button new-session" disabled={busy} onClick={() => { invalidate(); setPair(PAIRS[0]); setSettings(DEFAULT_SETTINGS); setTab('workspace') }}><Reset size={16} />Reset workspace</button></div>
        {message && <div ref={feedback} className="feedback" role="status"><Information size={19} /><p>{message}</p><button className="icon-button" aria-label="Dismiss notification" onClick={() => setMessage('')}><Close size={18} /></button></div>}
        {tab === 'workspace' ? <div className="workbench"><RegistrationControls pair={pair} settings={settings} busy={busy} online={online} onPair={changePair} onSettings={changeSettings} onUpload={upload} onRun={run} onReconnect={reconnect} /><div className="inspection-column"><InteractiveViewer key={pair.source + pair.reference} pair={pair} result={result} mode={mode} onModeChange={setMode} /><RegistrationResults result={result} onExample={example} />{result && <button className="results-shortcut text-button" onClick={() => setTab('results')}>Review quality & download outputs<ArrowRight size={16} /></button>}<div className="workspace-note"><Information size={16} /><p>{!online ? 'Image inspection is available offline. New registrations require the Python processing engine.' : 'Registration aligns the source image to the fixed reference image.'}</p></div></div></div> : <RegistrationResults result={result} onExample={example} expanded />}
      </main>
      <footer className="site-footer"><span className="font-mono">CHANDRA-SYNC <span className="footer-divider">/</span> SIH 2026</span><span>Lunar image registration research</span><button className="text-button" onClick={() => help.current?.showModal()}><Help size={15} />Quick guide</button></footer>
      <dialog ref={help} className="guide-dialog" onClick={event => { if (event.target === event.currentTarget) help.current?.close() }}><div className="dialog-header"><span className="eyebrow font-mono">QUICK GUIDE</span><button className="icon-button" aria-label="Close quick guide" onClick={() => help.current?.close()}><Close size={21} /></button></div><h2>A pair of images. One shared frame.</h2><p>Registration aligns two observations of the same lunar terrain so their features can be compared.</p><ol className="guide-steps"><li><strong>Choose your images</strong><p>Select a sample pair, or upload a source image and a fixed reference. Uploads require the engine.</p></li><li><strong>Run registration</strong><p>Start with SIFT and adaptive contrast. Advanced settings let you adjust the transformation and refinement.</p></li><li><strong>Inspect the alignment</strong><p>Drag the comparison divider, zoom into crater edges, then inspect matches, checkerboard and difference views.</p></li><li><strong>Review and export</strong><p>Check measured error and spatial coverage in Results. Download images and a JSON report.</p></li></ol><div className="guide-note">Engine offline? Explore the saved example. Archived results are labelled and are never presented as a new run.</div><button className="primary-button" onClick={() => help.current?.close()}>Back to workspace<ArrowRight size={17} /></button></dialog>
    </div>
  )
}
