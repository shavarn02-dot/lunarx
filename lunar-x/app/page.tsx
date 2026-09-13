"use client"
import React, { useEffect, useState } from "react"
import { GeospatialHeader } from "../components/geospatial-header"
import { GeospatialCanvas } from "../components/geospatial-canvas"
import { FloatingHud } from "../components/floating-hud"
import { TelemetryDock } from "../components/telemetry-dock"
import { ImageModal } from "../components/image-modal"
import { AnalyticsDrawer } from "../components/analytics-drawer"
import type { Config, ImageInfo, Pair, RegistrationResult } from "../components/types"

const API = process.env.NEXT_PUBLIC_LUNARX_API_URL || ""
const fallbackPair: Pair = {
  id: "tmc_crater",
  name: "Crater field – TMC-2 cross-pass (600 x 600)",
  source_img: "ch2_tmc_crater_scene_src.png",
  reference_img: "ch2_tmc_crater_scene_ref.png",
  sensor: "TMC-2 (5.0m)",
  orbit: "Orbit 3922 vs 3943",
}

const makeBlank = (filename: string): ImageInfo => ({
  filename,
  preview: `/images/${filename}`,
})

export default function Page() {
  const [online, setOnline] = useState(false)
  const [pairs, setPairs] = useState<Pair[]>([fallbackPair])
  const [pairId, setPairId] = useState(fallbackPair.id)
  const [source, setSource] = useState<ImageInfo>(makeBlank(fallbackPair.source_img))
  const [reference, setReference] = useState<ImageInfo>(makeBlank(fallbackPair.reference_img))
  const [uploading, setUploading] = useState<"source" | "reference" | null>(null)
  const [config, setConfig] = useState<Config>({
    method: "sift",
    preprocessing: "clahe",
    model_type: "homography",
    subpixel: true,
    spatial_filter: true,
    reproj_thresh: 3,
  })
  const [result, setResult] = useState<RegistrationResult | null>(null)
  const [running, setRunning] = useState(false)
  const [error, setError] = useState("")

  // Workstation HUD States
  const [viewMode, setViewMode] = useState<"split" | "matches" | "checkerboard" | "difference" | "side">("split")
  const [loupeActive, setLoupeActive] = useState(false)
  const [showGrid, setShowGrid] = useState(true)
  const [analyticsOpen, setAnalyticsOpen] = useState(false)
  const [uploadModalOpen, setUploadModalOpen] = useState(false)

  // Fetch initial health and pairs list
  useEffect(() => {
    Promise.all([
      fetch(`${API}/api/health`).then(r => (r.ok ? r.json() : Promise.reject())),
      fetch(`${API}/api/pairs`).then(r => (r.ok ? r.json() : Promise.reject())),
    ])
      .then(([_, p]) => {
        setOnline(true)
        if (Array.isArray(p) && p.length > 0) {
          setPairs(p)
          applyPair(p[0])
        }
      })
      .catch(() => setOnline(false))
  }, [])

  function applyPair(p: Pair) {
    setPairId(p.id)
    const common = {
      sensor: p.sensor || "TMC-2",
      resolution: p.resolution || "5.0 m/px",
      orbit: p.orbit || "Orbit 3922",
      provenance: "ISRO Mission Archive; validated",
    }
    setSource({ ...makeBlank(p.source_img), ...common })
    setReference({ ...makeBlank(p.reference_img), ...common })
    setResult(null)
    setError("")
  }

  async function handleUpload(file: File, side: "source" | "reference") {
    setUploading(side)
    setError("")
    const preview = URL.createObjectURL(file)
    const localInfo: ImageInfo = {
      filename: file.name,
      preview,
      provenance: "User Upload; validated",
    }
    side === "source" ? setSource(localInfo) : setReference(localInfo)

    try {
      const fd = new FormData()
      fd.append("file", file)
      const res = await fetch(`${API}/api/upload`, { method: "POST", body: fd })
      if (res.ok) {
        const data = await res.json()
        const uploadedInfo: ImageInfo = {
          filename: data.filename || file.name,
          preview,
          provenance: "User Upload; validated",
        }
        side === "source" ? setSource(uploadedInfo) : setReference(uploadedInfo)
        setOnline(true)
      }
    } catch {
      // preview stays functional
    } finally {
      setUploading(null)
    }
  }

  async function runRegistration() {
    setRunning(true)
    setResult(null)
    setError("")

    try {
      const res = await fetch(`${API}/api/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          source_filename: source.filename,
          reference_filename: reference.filename,
          ...config,
        }),
      })

      if (!res.ok) {
        const errJson = await res.json().catch(() => null)
        throw new Error(errJson?.detail || errJson?.error || `Server HTTP ${res.status}`)
      }

      const data: RegistrationResult = await res.json()
      setResult(data)
      setOnline(true)

      if (!data.success) {
        setError(data.error || "The registration pipeline flagged this image pair.")
      }
    } catch (err: any) {
      setOnline(false)
      setError(err instanceof Error ? err.message : "Unable to reach registration engine.")
    } finally {
      setRunning(false)
    }
  }

  function exportReport() {
    if (!result) return
    const rows = [
      ["Parameter", "Value"],
      ["Mission", "ISRO Chandrayaan-2 (PS-SIH26166)"],
      ["Source Image", source.filename],
      ["Reference Image", reference.filename],
      ["Matcher", config.method],
      ["Enhancement", config.preprocessing],
      ["Transformation Model", config.model_type],
      ["Success Status", String(result.success)],
      ["Runtime (sec)", String(result.runtime_sec ?? "")],
      ["Reprojection RMSE Coarse", String(result.metrics?.reproj_rmse_coarse ?? "")],
      ["Reprojection RMSE Refined", String(result.metrics?.reproj_rmse_refined ?? "")],
      ["Verified Inliers", String(result.metrics?.inliers ?? "")],
      ["Raw Matches", String(result.metrics?.raw_matches ?? "")],
      ["Inlier Ratio %", String(result.metrics?.inlier_ratio_pct ?? "")],
      ["Spatial Coverage %", String(result.metrics?.spatial_coverage_pct ?? "")],
      ["Grid Occupancy %", String(result.metrics?.grid_occupancy_pct ?? "")],
      ["Photometric NCC", String(result.metrics?.photometric_ncc ?? "")],
      ["Photometric RMSE", String(result.metrics?.photometric_rmse ?? "")],
    ]
    const csv = rows.map(r => r.map(v => `"${v.replace(/"/g, '""')}"`).join(",")).join("\n")
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" })
    const link = document.createElement("a")
    link.href = URL.createObjectURL(blob)
    link.download = `lunarx-registration-${source.filename}-to-${reference.filename}.csv`
    link.click()
    URL.revokeObjectURL(link.href)
  }

  const currentPair = pairs.find(p => p.id === pairId)

  return (
    <div className="lunarx-workstation-app">
      {/* Top Glassmorphic Navigation */}
      <GeospatialHeader
        online={online}
        pairs={pairs}
        selectedPairId={pairId}
        onSelectPair={applyPair}
        onOpenUpload={() => setUploadModalOpen(true)}
        onExport={exportReport}
        activeSensor={currentPair?.sensor}
      />

      {/* Error / Alert Banner */}
      {error && (
        <div className="workstation-error-toast" role="alert">
          <div className="toast-icon">⚠</div>
          <div className="toast-content">
            <strong>REGISTRATION SERVICE ALERT</strong>
            <span>{error}</span>
          </div>
          <button className="toast-dismiss" onClick={() => setError("")}>
            ✕
          </button>
        </div>
      )}

      {/* Main Full-Bleed Workstation Stage */}
      <main className="workstation-viewport">
        {/* Geospatial Canvas (Center) */}
        <GeospatialCanvas
          source={source}
          reference={reference}
          result={result}
          running={running}
          viewMode={viewMode}
          loupeActive={loupeActive}
          showGrid={showGrid}
        />

        {/* Floating HUD Tools (Left) */}
        <FloatingHud
          viewMode={viewMode}
          setViewMode={setViewMode}
          loupeActive={loupeActive}
          setLoupeActive={setLoupeActive}
          showGrid={showGrid}
          setShowGrid={setShowGrid}
          onToggleAnalytics={() => setAnalyticsOpen(true)}
          hasResult={!!result}
        />

        {/* Floating Telemetry & Control Dock (Bottom) */}
        <TelemetryDock
          config={config}
          setConfig={setConfig}
          result={result}
          running={running}
          onRun={runRegistration}
        />
      </main>

      {/* Slide-over Deep Analytics Drawer */}
      <AnalyticsDrawer
        isOpen={analyticsOpen}
        onClose={() => setAnalyticsOpen(false)}
        result={result}
        config={config}
      />

      {/* Modal for Image Upload & Replacement */}
      <ImageModal
        isOpen={uploadModalOpen}
        onClose={() => setUploadModalOpen(false)}
        source={source}
        reference={reference}
        uploading={uploading}
        onUpload={handleUpload}
      />
    </div>
  )
}
