"use client"
import React from "react"
import type { Config, RegistrationResult } from "./types"

interface TelemetryDockProps {
  config: Config
  setConfig: React.Dispatch<React.SetStateAction<Config>>
  result: RegistrationResult | null
  running: boolean
  onRun: () => void
}

export function TelemetryDock({
  config,
  setConfig,
  result,
  running,
  onRun,
}: TelemetryDockProps) {
  const m = result?.metrics
  const inlierRatio = m?.inlier_ratio_pct ?? (result ? 0 : 99.4)
  const inlierCount = m?.inliers ?? (result ? 0 : "--")
  const rmse = m?.reproj_rmse_refined ?? (result ? 0 : 0.18)
  const coverage = m?.spatial_coverage_pct ?? (result ? 0 : 96.1)

  // Circumference for circular gauge (r=26 => 2 * pi * 26 ~= 163.36)
  const radius = 26
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference - (Math.min(100, Math.max(0, inlierRatio)) / 100) * circumference

  return (
    <div className="floating-telemetry-dock">
      {/* 1. Subpixel Convergence Mini Chart */}
      <div className="telemetry-card convergence-card">
        <div className="card-header">
          <span>SUBPIXEL CONVERGENCE</span>
          <small>{rmse ? `${Number(rmse).toFixed(2)} px` : "--"}</small>
        </div>
        <div className="chart-wrapper">
          <svg viewBox="0 0 100 36" className="convergence-svg">
            <defs>
              <linearGradient id="curveGlow" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#00e5ff" stopOpacity="0.4" />
                <stop offset="100%" stopColor="#00e5ff" stopOpacity="0.0" />
              </linearGradient>
            </defs>
            <path
              d="M 5 6 Q 25 24, 55 28 T 95 30 L 95 36 L 5 36 Z"
              fill="url(#curveGlow)"
            />
            <path
              d="M 5 6 Q 25 24, 55 28 T 95 30"
              fill="none"
              stroke="#00e5ff"
              strokeWidth="2"
              strokeLinecap="round"
            />
            <circle cx="95" cy="30" r="2.5" fill="#00e5ff" />
          </svg>
          <div className="chart-labels">
            <span>Coarse: 1.50</span>
            <span>Refined: {rmse ? `${Number(rmse).toFixed(2)} px` : "0.18 px"}</span>
          </div>
        </div>
      </div>

      {/* 2. Spatial Histogram Mini Chart */}
      <div className="telemetry-card histogram-card">
        <div className="card-header">
          <span>SPATIAL COVERAGE</span>
          <small>{coverage ? `${Number(coverage).toFixed(1)}%` : "--"}</small>
        </div>
        <div className="histogram-bars">
          {[4, 12, 19, 28, 45, 62, 78, 92, 85, 68, 54, 38, 22, 14, 8].map((val, idx) => (
            <div
              key={idx}
              className="histogram-bar"
              style={{
                height: `${val}%`,
                backgroundColor: result?.success === false ? "#ff5252" : "#00e5ff",
                opacity: 0.35 + (val / 100) * 0.65,
              }}
            />
          ))}
        </div>
        <div className="chart-labels">
          <span>0%</span>
          <span>64-Grid Occupancy</span>
          <span>100%</span>
        </div>
      </div>

      {/* 3. Inlier Ratio Circular Gauge */}
      <div className="telemetry-card gauge-card">
        <div className="gauge-container">
          <svg width="68" height="68" viewBox="0 0 68 68">
            {/* Background track */}
            <circle
              cx="34"
              cy="34"
              r={radius}
              stroke="rgba(255,255,255,0.08)"
              strokeWidth="5"
              fill="none"
            />
            {/* Progress circle */}
            <circle
              cx="34"
              cy="34"
              r={radius}
              stroke={result?.success === false ? "#ff5252" : "#00e5ff"}
              strokeWidth="5"
              strokeLinecap="round"
              fill="none"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              transform="rotate(-90 34 34)"
              style={{ transition: "stroke-dashoffset 0.8s ease" }}
            />
          </svg>
          <div className="gauge-value">
            <strong>{inlierRatio ? `${Number(inlierRatio).toFixed(1)}%` : "0%"}</strong>
            <span>INLIERS</span>
          </div>
        </div>
        <div className="gauge-meta">
          <strong>{inlierCount.toLocaleString()}</strong>
          <small>Verified Ties</small>
        </div>
      </div>

      {/* 4. Controls & Config Section */}
      <div className="telemetry-controls">
        <div className="control-group">
          <label>Matcher</label>
          <div className="chip-selector">
            {[
              { id: "sift", label: "SIFT (Fast)" },
              { id: "loftr", label: "LoFTR (Deep)" },
              { id: "superpoint_lightglue", label: "SuperPoint" },
              { id: "orb", label: "ORB" },
            ].map(item => (
              <button
                key={item.id}
                className={`chip ${config.method === item.id ? "active" : ""}`}
                onClick={() => setConfig(prev => ({ ...prev, method: item.id }))}
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>

        <div className="control-group">
          <label>Enhancement & Model</label>
          <div className="chip-selector">
            {[
              { id: "clahe", label: "CLAHE" },
              { id: "gradient", label: "Gradient" },
              { id: "phase_congruency", label: "Phase Cong." },
            ].map(item => (
              <button
                key={item.id}
                className={`chip ${config.preprocessing === item.id ? "active" : ""}`}
                onClick={() => setConfig(prev => ({ ...prev, preprocessing: item.id }))}
              >
                {item.label}
              </button>
            ))}
            <div className="chip-divider" />
            <select
              value={config.model_type}
              onChange={e => setConfig(prev => ({ ...prev, model_type: e.target.value }))}
              className="chip-select"
            >
              <option value="affine">Affine (6-DOF)</option>
              <option value="homography">Homography (8-DOF)</option>
              <option value="rigid">Rigid (3-DOF)</option>
            </select>
          </div>
        </div>
      </div>

      {/* 5. Main Action Execution Button */}
      <div className="telemetry-action">
        <button
          className={`execute-registration-btn ${running ? "running" : ""}`}
          onClick={onRun}
          disabled={running}
        >
          <div className="btn-glow" />
          <div className="btn-content">
            {running ? (
              <>
                <span className="radar-spinner" />
                <span>PROCESSING ORBIT...</span>
              </>
            ) : (
              <>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <polygon points="5 3 19 12 5 21 5 3" />
                </svg>
                <span>RUN AUTONOMOUS REGISTRATION</span>
              </>
            )}
          </div>
        </button>
      </div>
    </div>
  )
}
