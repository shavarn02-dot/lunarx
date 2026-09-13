import { Explainer } from './explainer'

const metricKeyMap: Record<string, string> = {
  'Registration status': 'registration_status',
  'Reprojection RMSE': 'reproj_rmse',
  'Verified inliers': 'verified_inliers',
  'Inlier ratio': 'inlier_ratio',
  'Spatial coverage': 'spatial_coverage',
  'Processing time': 'processing_time',
}

export function MetricCard({
  label,
  value,
  help,
  termKey,
}: {
  label: string
  value: string
  help?: string
  termKey?: string
}) {
  const resolvedKey = termKey || metricKeyMap[label]
  return (
    <div className="metric">
      <span>
        {resolvedKey ? (
          <Explainer termKey={resolvedKey} showIndicator={true}>
            <span>{label}</span>
          </Explainer>
        ) : (
          <span>{label}</span>
        )}
        {help && <abbr title={help}>?</abbr>}
      </span>
      <strong>{value}</strong>
    </div>
  )
}
