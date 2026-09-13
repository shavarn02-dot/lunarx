import { Explainer } from './explainer'

const glossaryKeyMap: Record<string, string> = {
  PDS4: 'provenance',
  LoFTR: 'loftr',
  'MAGSAC++': 'verified_inliers',
  RMSE: 'reproj_rmse',
  'Sub-pixel refinement': 'subpixel',
  'Spatial coverage': 'spatial_coverage',
  NCC: 'photometric_ncc',
}

const items = [
  ['PDS4', 'A planetary-data standard that packages imagery with machine-readable mission metadata.'],
  ['LoFTR', 'A detector-free matcher that compares image regions directly, useful in low-texture scenes.'],
  ['MAGSAC++', 'A robust estimator that rejects incorrect correspondences before solving the transformation.'],
  ['RMSE', 'Average reprojection error in pixels after alignment. Lower values indicate tighter geometric agreement.'],
  ['Sub-pixel refinement', 'A precision step that adjusts correspondence coordinates to fractions of a pixel.'],
  ['Spatial coverage', 'Checks that accepted matches span the image instead of clustering in one region.'],
  ['NCC', 'Normalized cross-correlation; a measure of photometric similarity over the valid overlap.'],
]

export function Glossary() {
  return (
    <details className="glossary panel">
      <summary>Technical glossary</summary>
      <div className="glossary-grid">
        {items.map(([term, text]) => {
          const termKey = glossaryKeyMap[term]
          return (
            <div key={term}>
              <dt>
                {termKey ? (
                  <Explainer termKey={termKey} showIndicator={true}>
                    <span>{term}</span>
                  </Explainer>
                ) : (
                  term
                )}
              </dt>
              <dd>{text}</dd>
            </div>
          )
        })}
      </div>
    </details>
  )
}
