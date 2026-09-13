import type { Config } from './types'
import { Explainer } from './explainer'

const matcherNames: Record<string, string> = {
  sift: 'SIFT',
  orb: 'ORB',
  superpoint_lightglue: 'SuperPoint + LightGlue',
  loftr: 'LoFTR',
}

const methodToTermKey: Record<string, string> = {
  sift: 'sift',
  orb: 'orb',
  superpoint_lightglue: 'superpoint_lightglue',
  loftr: 'loftr',
}

const prepToTermKey: Record<string, string> = {
  clahe: 'clahe',
  gradient: 'gradient',
  phase_congruency: 'phase_congruency',
}

const modelToTermKey: Record<string, string> = {
  affine: 'affine',
  homography: 'homography',
  rigid: 'rigid',
}

export function RegistrationControls({
  config,
  setConfig,
  onRun,
  running,
}: {
  config: Config
  setConfig: (v: Config) => void
  onRun: () => void
  running: boolean
}) {
  const patch = (p: Partial<Config>) => setConfig({ ...config, ...p })

  return (
    <section className="controls panel">
      <div>
        <p className="section-label">Registration controls</p>
        <h2>Configure alignment</h2>
      </div>

      <div className="control-grid">
        <label>
          <Explainer
            termKey={methodToTermKey[config.method] || 'feature_matcher'}
            showIndicator={true}
          >
            <span>Feature matcher</span>
          </Explainer>
          <select
            value={config.method}
            onChange={(e) => patch({ method: e.target.value })}
          >
            {Object.entries(matcherNames).map(([v, l]) => (
              <option key={v} value={v}>
                {l}
              </option>
            ))}
          </select>
        </label>

        <label>
          <Explainer
            termKey={prepToTermKey[config.preprocessing] || 'preprocessing'}
            showIndicator={true}
          >
            <span>Preprocessing</span>
          </Explainer>
          <select
            value={config.preprocessing}
            onChange={(e) => patch({ preprocessing: e.target.value })}
          >
            <option value="clahe">CLAHE</option>
            <option value="gradient">Gradient</option>
            <option value="raw">Raw</option>
            <option value="phase_congruency">Phase congruency</option>
          </select>
        </label>

        <label>
          <Explainer
            termKey={modelToTermKey[config.model_type] || 'transformation'}
            showIndicator={true}
          >
            <span>Transformation</span>
          </Explainer>
          <select
            value={config.model_type}
            onChange={(e) => patch({ model_type: e.target.value })}
          >
            <option value="affine">Affine</option>
            <option value="homography">Homography</option>
            <option value="rigid">Rigid</option>
          </select>
        </label>
      </div>

      <details>
        <summary>Advanced options</summary>
        <div className="advanced-controls">
          <label>
            <input
              type="checkbox"
              checked={config.subpixel}
              onChange={(e) => patch({ subpixel: e.target.checked })}
            />{' '}
            <Explainer termKey="subpixel" showIndicator={true}>
              <span>Sub-pixel refinement</span>
            </Explainer>
          </label>
          <label>
            <input
              type="checkbox"
              checked={config.spatial_filter}
              onChange={(e) => patch({ spatial_filter: e.target.checked })}
            />{' '}
            <Explainer termKey="spatial_filter_option" showIndicator={true}>
              <span>8×8 spatial coverage validation</span>
            </Explainer>
          </label>
          <label>
            <Explainer termKey="reproj_thresh_option" showIndicator={true}>
              <span>Reprojection threshold</span>
            </Explainer>{' '}
            <span>
              <input
                type="number"
                min="0.1"
                max="20"
                step="0.1"
                value={config.reproj_thresh}
                onChange={(e) => patch({ reproj_thresh: Number(e.target.value) })}
              />{' '}
              px
            </span>
          </label>
        </div>
      </details>

      <Explainer termKey="run_registration_btn" showIndicator={false}>
        <button
          className="primary run"
          disabled={running}
          onClick={onRun}
        >
          {running ? (
            <>
              <span className="spinner" />
              Running registration…
            </>
          ) : (
            'Run registration'
          )}
        </button>
      </Explainer>
    </section>
  )
}
