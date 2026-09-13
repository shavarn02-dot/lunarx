import type { RegistrationResult } from './types'
import { Explainer } from './explainer'

export function AdvancedDetails({
  result,
}: {
  result: RegistrationResult | null
}) {
  const m = result?.metrics

  return (
    <details className="advanced panel">
      <summary>Advanced technical details</summary>
      {!result ? (
        <p className="empty">Technical output will appear after registration.</p>
      ) : (
        <div className="detail-grid">
          <Detail
            label="Model"
            value={String(
              result.configuration?.model_type ??
                result.quality_report?.model_type ??
                'Not available'
            )}
            termKey="transformation"
          />
          <Detail
            label="Estimator"
            value={String(result.configuration?.robust_estimator ?? 'USAC_MAGSAC')}
            termKey="verified_inliers"
          />
          <Detail
            label="Condition number"
            value={format(m?.condition_number)}
            termKey="condition_number"
          />
          <Detail
            label="Grid occupancy"
            value={unit(m?.grid_occupancy_pct, '%')}
            termKey="grid_occupancy"
          />
          <Detail
            label="NCC"
            value={format(m?.photometric_ncc)}
            termKey="photometric_ncc"
          />
          <Detail
            label="Photometric RMSE"
            value={unit(m?.photometric_rmse, ' intensity')}
          />
          <Detail
            label="Threshold"
            value={unit(result.configuration?.reproj_thresh as number | undefined, ' px')}
            termKey="reproj_thresh_option"
          />
          <Detail
            label="Matrix stability"
            value={
              m?.is_stable == null
                ? 'Not available'
                : m.is_stable
                ? 'Stable'
                : 'Unstable'
            }
            termKey="condition_number"
          />
          <div className="matrix">
            <Explainer termKey="transformation_matrix" showIndicator={true}>
              <span>Transformation matrix</span>
            </Explainer>
            <pre>
              {result.transformation_matrix
                ? result.transformation_matrix
                    .map((r) => r.map((v) => v.toFixed(6)).join('   '))
                    .join('\n')
                : 'Not available'}
            </pre>
          </div>
          <div className="matrix">
            <span>Source record</span>
            <pre>{JSON.stringify(result.source ?? {}, null, 2)}</pre>
          </div>
          <div className="matrix">
            <span>Reference record</span>
            <pre>{JSON.stringify(result.reference ?? {}, null, 2)}</pre>
          </div>
        </div>
      )}
    </details>
  )
}

function Detail({
  label,
  value,
  termKey,
}: {
  label: string
  value: string
  termKey?: string
}) {
  return (
    <div className="detail">
      <span>
        {termKey ? (
          <Explainer termKey={termKey} showIndicator={true}>
            <span>{label}</span>
          </Explainer>
        ) : (
          label
        )}
      </span>
      <code>{value}</code>
    </div>
  )
}

function format(v: number | null | undefined) {
  return v == null || !Number.isFinite(v) ? 'Not available' : String(v)
}

function unit(v: number | null | undefined, s: string) {
  return v == null || !Number.isFinite(v) ? 'Not available' : `${v}${s}`
}
