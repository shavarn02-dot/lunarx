'use client'

import { useState } from 'react'
import { ArrowRight, Upload, SettingsAdjust, ChevronDown, Image as ImageIcon, Renew } from '@carbon/icons-react'
import { PAIRS, imageUrl, type ImagePair, type Settings } from './registration-data'

interface Props { pair: ImagePair; settings: Settings; busy: boolean; online: boolean; onPair: (pair: ImagePair) => void; onSettings: (settings: Settings) => void; onUpload: (source: File, reference: File) => Promise<void>; onRun: () => void; onReconnect: () => void }
export function RegistrationControls({ pair, settings, busy, online, onPair, onSettings, onUpload, onRun, onReconnect }: Props) {
  const [inputMode, setInputMode] = useState<'sample' | 'upload'>('sample')
  const [source, setSource] = useState<File | null>(null)
  const [reference, setReference] = useState<File | null>(null)
  const update = (key: keyof Settings, value: string | number | boolean) => onSettings({ ...settings, [key]: value })
  return (
    <aside className="controls-panel" aria-label="Registration configuration">
      <fieldset disabled={busy}>
        <section className="control-section">
          <div className="section-heading"><ImageIcon size={18} /><h2>Input images</h2><span className="step-label font-mono">01</span></div>
          <div className="input-switch" role="group" aria-label="Image input method"><button aria-pressed={inputMode === 'sample'} className={inputMode === 'sample' ? 'selected' : ''} onClick={() => setInputMode('sample')}>Sample dataset</button><button aria-pressed={inputMode === 'upload'} className={inputMode === 'upload' ? 'selected' : ''} onClick={() => setInputMode('upload')}><Upload size={15} />Upload pair</button></div>
          {inputMode === 'sample' ? <div className="field"><label htmlFor="pair-select">Image pair</label><select id="pair-select" value={pair.id} onChange={event => { const selected = PAIRS.find(p => p.id === event.target.value); if (selected) onPair(selected) }}>{pair.id === 'custom' && <option value="custom">Uploaded image pair</option>}{PAIRS.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}</select></div> : <div className="upload-fields"><label className="upload-field"><Upload size={18} /><span>Source image <small>{source?.name || 'Choose PNG, JPEG or TIFF'}</small></span><input aria-label="Upload source image" type="file" accept=".png,.jpg,.jpeg,.tif,.tiff" onChange={event => setSource(event.target.files?.[0] || null)} /></label><label className="upload-field"><Upload size={18} /><span>Reference image <small>{reference?.name || 'Choose PNG, JPEG or TIFF'}</small></span><input aria-label="Upload reference image" type="file" accept=".png,.jpg,.jpeg,.tif,.tiff" onChange={event => setReference(event.target.files?.[0] || null)} /></label><button className="secondary-button" disabled={!source || !reference} onClick={() => { if (source && reference) void onUpload(source, reference) }}>Load image pair<ArrowRight size={16} /></button><p className="field-hint">Maximum 20 MB per image. TIFF files may not support browser previews.</p></div>}
          <div className="pair-previews">{[{ file: pair.source, label: 'Source', letter: 'A' }, { file: pair.reference, label: 'Reference', letter: 'B' }].map(item => <figure key={item.label}><div className="thumbnail"><img src={imageUrl(item.file)} alt={`${item.label} lunar terrain thumbnail`} /><span className="thumb-letter font-mono">{item.letter}</span></div><figcaption>{item.label}<span className="font-mono">{pair.sensor}</span></figcaption></figure>)}</div>
          <p className="field-hint">{pair.description}</p>
        </section>
        <section className="control-section settings-section">
          <div className="section-heading"><SettingsAdjust size={18} /><h2>Registration settings</h2><span className="step-label font-mono">02</span></div>
          <div className="field"><label htmlFor="method">Matching method</label><select id="method" value={settings.method} onChange={event => update('method', event.target.value)}><option value="sift">SIFT</option><option value="orb">ORB</option><option value="superpoint_lightglue">SuperPoint + LightGlue</option><option value="loftr">LoFTR</option></select><p className="field-hint">{settings.method === 'sift' ? 'Reliable feature matching across scale and rotation.' : settings.method === 'orb' ? 'Lightweight matching for a faster first pass.' : 'Learned feature matching. Requires the corresponding model on the engine.'}</p></div>
          <div className="field"><label htmlFor="preprocessing">Image enhancement</label><select id="preprocessing" value={settings.preprocessing} onChange={event => update('preprocessing', event.target.value)}><option value="clahe">Adaptive contrast · CLAHE</option><option value="gradient">Gradient magnitude</option><option value="raw">None · Original pixels</option></select></div>
          <details className="advanced-settings"><summary>Advanced settings<ChevronDown size={16} /></summary><div className="advanced-body"><div className="field"><label htmlFor="model">Transformation</label><select id="model" value={settings.model_type} onChange={event => update('model_type', event.target.value)}><option value="affine">Affine</option><option value="homography">Homography</option><option value="rigid">Rigid</option></select></div><label className="check-field"><input type="checkbox" checked={settings.subpixel} onChange={event => update('subpixel', event.target.checked)} />Sub-pixel refinement</label><label className="check-field"><input type="checkbox" checked={settings.spatial_filter} onChange={event => update('spatial_filter', event.target.checked)} />Spatial filtering</label><div className="field"><label htmlFor="threshold">Reprojection threshold <span className="font-mono">{settings.reproj_thresh} px</span></label><input id="threshold" type="range" min="0.5" max="10" step="0.5" value={settings.reproj_thresh} onChange={event => update('reproj_thresh', Number(event.target.value))} /></div></div></details>
        </section>
      </fieldset>
      <div className="run-section"><button className="primary-button" disabled={busy} onClick={onRun}>{busy ? <><Renew className="spinning" size={18} />Please wait…</> : <>Run registration<ArrowRight size={18} /></>}</button><p className="run-hint">{online ? 'Ready to align your image pair.' : 'Processing engine is currently offline.'}</p>{!online && <button className="text-button" disabled={busy} onClick={onReconnect}><Renew size={14} />Check connection</button>}</div>
    </aside>
  )
}
