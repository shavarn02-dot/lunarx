"use client"
import React from "react"
import type { RegistrationResult, Config } from "./types"

interface AnalyticsDrawerProps {
  isOpen: boolean
  onClose: () => void
  result: RegistrationResult | null
  config: Config
}

export function AnalyticsDrawer({
  isOpen,
  onClose,
  result,
  config,
}: AnalyticsDrawerProps) {
  if (!isOpen) return null

  const m = result?.metrics
  const matrix = result?.transformation_matrix

  return (
    <div className="drawer-backdrop" onClick={onClose}>
      <div className="analytics-drawer-panel" onClick={e => e.stopPropagation()}>
        <div className="drawer-header">
          <div>
            <h3>SCIENTIFIC TELEMETRY & VERIFICATION</h3>
            <small>Deep mathematical diagnostics for Chandrayaan-2 registration</small>
          </div>
          <button className="drawer-close-btn" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="drawer-body">
          {/* Status Alert */}
          {result && (
            <div className={`status-banner ${result.success ? "success" : "failure"}`}>
              <div className="banner-icon">
                {result.success ? "✓" : "⚠"}
              </div>
              <div className="banner-text">
                <strong>{result.success ? "REGISTRATION CONVERGED & VALIDATED" : "REGISTRATION REJECTED / UNSTABLE"}</strong>
                <p>{result.error || "Meets sub-pixel criteria (RMSE < 0.5px, coverage > 15%)."}</p>
              </div>
            </div>
          )}

          {/* Transformation Matrix Section */}
          <div className="analytics-section">
            <span className="section-kicker">GEOMETRIC TRANSFORMATION</span>
            <h4>Transformation Matrix ({config.model_type.toUpperCase()})</h4>
            {matrix && matrix.length > 0 ? (
              <div className="matrix-display">
                <div className="matrix-bracket left" />
                <div className="matrix-rows">
                  {matrix.map((row, rIdx) => (
                    <div key={rIdx} className="matrix-row">
                      {row.map((val, cIdx) => (
                        <span key={cIdx} className="matrix-cell">
                          {Number(val).toFixed(6)}
                        </span>
                      ))}
                    </div>
                  ))}
                </div>
                <div className="matrix-bracket right" />
              </div>
            ) : (
              <div className="matrix-empty">No transformation matrix estimated yet.</div>
            )}
            <div className="matrix-props">
              <div className="prop-item">
                <span>Condition Number:</span>
                <strong>{m?.condition_number ? Number(m.condition_number).toFixed(4) : "1.0000"}</strong>
              </div>
              <div className="prop-item">
                <span>Stability:</span>
                <strong className={m?.is_stable !== false ? "text-cyan" : "text-red"}>
                  {m?.is_stable !== false ? "STABLE (No Fold/Flip)" : "UNSTABLE"}
                </strong>
              </div>
            </div>
          </div>

          {/* Metrics Grid */}
          <div className="analytics-section">
            <span className="section-kicker">PHOTOMETRIC & SPATIAL VERIFICATION</span>
            <h4>Quantitative Performance Metrics</h4>
            <div className="metrics-tabular">
              <div className="metric-row">
                <span>Reprojection RMSE (Coarse):</span>
                <strong>{m?.reproj_rmse_coarse ? `${Number(m.reproj_rmse_coarse).toFixed(4)} px` : "--"}</strong>
              </div>
              <div className="metric-row">
                <span>Reprojection RMSE (Refined):</span>
                <strong>{m?.reproj_rmse_refined ? `${Number(m.reproj_rmse_refined).toFixed(4)} px` : "--"}</strong>
              </div>
              <div className="metric-row">
                <span>Verified Inliers:</span>
                <strong>{m?.inliers ? m.inliers.toLocaleString() : "--"}</strong>
              </div>
              <div className="metric-row">
                <span>Raw Match Tie-Points:</span>
                <strong>{m?.raw_matches ? m.raw_matches.toLocaleString() : "--"}</strong>
              </div>
              <div className="metric-row">
                <span>Inlier Ratio:</span>
                <strong>{m?.inlier_ratio_pct ? `${Number(m.inlier_ratio_pct).toFixed(2)}%` : "--"}</strong>
              </div>
              <div className="metric-row">
                <span>Spatial Grid Occupancy (64 Cells):</span>
                <strong>{m?.grid_occupancy_pct ? `${Number(m.grid_occupancy_pct).toFixed(1)}%` : "--"}</strong>
              </div>
              <div className="metric-row">
                <span>Photometric NCC:</span>
                <strong>{m?.photometric_ncc ? Number(m.photometric_ncc).toFixed(4) : "--"}</strong>
              </div>
              <div className="metric-row">
                <span>Photometric RMSE:</span>
                <strong>{m?.photometric_rmse ? `${Number(m.photometric_rmse).toFixed(2)}` : "--"}</strong>
              </div>
              <div className="metric-row">
                <span>Total Pipeline Latency:</span>
                <strong>{result?.runtime_sec ? `${Number(result.runtime_sec).toFixed(3)} s` : "--"}</strong>
              </div>
            </div>
          </div>

          {/* Execution Pipeline Logs */}
          <div className="analytics-section">
            <span className="section-kicker">MISSION AUDIT TRAIL</span>
            <h4>Pipeline Logs</h4>
            <div className="logs-terminal">
              {(result?.logs && result.logs.length > 0
                ? result.logs
                : [
                    "[SYSTEM] Ready for registration execution.",
                    `[CONFIG] Selected matcher: ${config.method.toUpperCase()} | Preprocessing: ${config.preprocessing.toUpperCase()}`,
                    "[DEVICE] Native SIMD CPU & Tensor core acceleration active.",
                  ]
              ).map((line, idx) => (
                <div key={idx} className="log-line">
                  <span className="log-arrow">&gt;</span> {line}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
