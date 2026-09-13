'use client'

import { useRef, useState } from 'react'
import { ZoomIn, ZoomOut, FitToScreen, Maximize, ArrowsHorizontal, Compare, Image as ImageIcon } from '@carbon/icons-react'
import { imageUrl, type ImagePair, type RegistrationResult } from './registration-data'

export type ViewMode = 'original' | 'overlay' | 'matches' | 'checkerboard' | 'difference'
const MODES: { id: ViewMode; label: string }[] = [{ id: 'original', label: 'Compare' }, { id: 'overlay', label: 'Aligned' }, { id: 'matches', label: 'Matches' }, { id: 'checkerboard', label: 'Checkerboard' }, { id: 'difference', label: 'Difference' }]

function Raster({ file, alt, style }: { file: string; alt: string; style?: React.CSSProperties }) {
  const [failed, setFailed] = useState(false)
  return failed ? <div className="raster-error" role="status"><ImageIcon size={24} /><span>Image preview unavailable</span><small>Try a PNG or JPEG image.</small></div> : <img src={imageUrl(file)} alt={alt} draggable={false} style={style} onError={() => setFailed(true)} />
}

export function InteractiveViewer({ pair, result, mode, onModeChange }: { pair: ImagePair; result: RegistrationResult | null; mode: ViewMode; onModeChange: (mode: ViewMode) => void }) {
  const [split, setSplit] = useState(50)
  const [zoom, setZoom] = useState(1)
  const [dimensions, setDimensions] = useState('')
  const [notice, setNotice] = useState('')
  const viewer = useRef<HTMLElement>(null)
  const compare = mode === 'original' || mode === 'overlay'
  const leftFile = mode === 'overlay' && result ? result.images.registered : pair.source
  const singleFile = result && !compare ? result.images[mode as 'matches' | 'checkerboard' | 'difference'] : pair.source
  const fullscreen = async () => {
    try { if (document.fullscreenElement) await document.exitFullscreen(); else await viewer.current?.requestFullscreen() }
    catch { setNotice('Fullscreen is not available in this preview. Use the zoom controls to inspect details.') }
  }
  const captions = { original: 'Slide to compare the original source and reference images.', overlay: 'Compare the aligned source against the reference. Look for continuous crater edges.', matches: 'Feature correspondences between source and reference images.', checkerboard: 'Alternating image tiles reveal discontinuities along terrain edges.', difference: 'Pixel differences can reflect both misalignment and changes in illumination.' }
  return (
    <section className="viewer-panel" ref={viewer} aria-label="Image comparison viewer">
      <div className="viewer-heading"><div className="inline-group"><Compare size={19} /><h2>Image comparison</h2></div><span className="small-badge font-mono">{result?.provenance === 'saved' ? 'SAVED EXAMPLE' : result ? 'LIVE RESULT' : 'ORIGINAL IMAGES'}</span></div>
      <div className="viewer-toolbar"><div className="view-modes" role="group" aria-label="Image display mode">{MODES.map(item => <button key={item.id} aria-pressed={mode === item.id} disabled={item.id !== 'original' && !result} title={item.id !== 'original' && !result ? 'Run registration or load the saved example first' : item.label} onClick={() => onModeChange(item.id)} className={mode === item.id ? 'selected' : ''}>{item.label}</button>)}</div><button className="icon-button fullscreen-button" aria-label="Expand image viewer" onClick={fullscreen}><Maximize size={18} /></button></div>
      <div className="image-stage">
        <div className="stage-labels"><span className="image-label"><span className="label-marker">A</span>{mode === 'overlay' ? 'Aligned source' : compare ? 'Source image' : MODES.find(item => item.id === mode)?.label}</span>{compare && <span className="image-label"><span className="label-marker outlined">B</span>Reference image</span>}</div>
        <div className="image-scroll">
          <div className={`raster-frame ${compare ? 'comparison' : 'single'}`} style={{ width: compare ? `calc(min(100%, var(--stage-height)) * ${zoom})` : `${zoom * 100}%` }}>
            {compare ? <><img key={pair.reference} className="base-raster" src={imageUrl(pair.reference)} alt="Lunar reference image" draggable={false} onLoad={event => setDimensions(`${event.currentTarget.naturalWidth} × ${event.currentTarget.naturalHeight} px`)} /><div className="clipped-raster" style={{ clipPath: `inset(0 ${100 - split}% 0 0)` }}><Raster key={leftFile} file={leftFile} alt={mode === 'overlay' ? 'Aligned lunar source' : 'Original lunar source'} /></div><div className="split-divider" style={{ left: `${split}%` }}><span><ArrowsHorizontal size={18} /></span></div><input className="comparison-range" aria-label="Image comparison divider" type="range" min="0" max="100" value={split} onChange={event => setSplit(Number(event.target.value))} /></> : <Raster key={singleFile} file={singleFile} alt={`${mode} registration visualization`} />}
          </div>
        </div>
        <div className="stage-bottom"><span className="font-mono image-dimensions">{dimensions || pair.sensor}</span><div className="zoom-controls"><button aria-label="Zoom out" disabled={zoom <= 1} onClick={() => setZoom(value => Math.max(1, value - .25))}><ZoomOut size={18} /></button><span className="font-mono">{Math.round(zoom * 100)}%</span><button aria-label="Zoom in" disabled={zoom >= 3} onClick={() => setZoom(value => Math.min(3, value + .25))}><ZoomIn size={18} /></button><span className="tool-separator" /><button aria-label="Fit image to view" onClick={() => setZoom(1)}><FitToScreen size={18} /></button></div></div>
      </div>
      <div className="viewer-caption"><ArrowsHorizontal size={16} /><p>{notice || captions[mode]}</p>{compare && <button className="text-button" onClick={() => setSplit(50)}>Reset divider</button>}</div>
    </section>
  )
}
