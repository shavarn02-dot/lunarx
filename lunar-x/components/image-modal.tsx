"use client"
import React, { useRef } from "react"
import type { ImageInfo } from "./types"

interface ImageModalProps {
  isOpen: boolean
  onClose: () => void
  source: ImageInfo
  reference: ImageInfo
  uploading: "source" | "reference" | null
  onUpload: (file: File, side: "source" | "reference") => void
}

export function ImageModal({
  isOpen,
  onClose,
  source,
  reference,
  uploading,
  onUpload,
}: ImageModalProps) {
  const sourceFileRef = useRef<HTMLInputElement>(null)
  const refFileRef = useRef<HTMLInputElement>(null)

  if (!isOpen) return null

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-glass" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <div>
            <h3>ORBITAL IMAGE INGESTION</h3>
            <small>Provide raw lunar imagery from TMC-2 or OHRC sensors</small>
          </div>
          <button className="modal-close-btn" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="modal-grid">
          {/* Source Image Card */}
          <div className="ingest-card">
            <div className="card-top">
              <span className="ingest-label">SOURCE IMAGE (SENSING PASS)</span>
              <button
                className="ingest-replace-btn"
                onClick={() => sourceFileRef.current?.click()}
                disabled={uploading === "source"}
              >
                {uploading === "source" ? "Uploading..." : "Browse File"}
              </button>
              <input
                ref={sourceFileRef}
                type="file"
                accept="image/*"
                style={{ display: "none" }}
                onChange={e => {
                  const f = e.target.files?.[0]
                  if (f) onUpload(f, "source")
                }}
              />
            </div>
            <div className="ingest-preview">
              <img src={source.preview} alt="Source Preview" />
            </div>
            <div className="ingest-meta">
              <div className="meta-row">
                <span>File:</span>
                <code>{source.filename}</code>
              </div>
              <div className="meta-row">
                <span>Sensor:</span>
                <span>{source.sensor || "TMC-2"}</span>
              </div>
              <div className="meta-row">
                <span>Resolution:</span>
                <span>{source.resolution || "5.0 m/px"}</span>
              </div>
            </div>
          </div>

          {/* Reference Image Card */}
          <div className="ingest-card">
            <div className="card-top">
              <span className="ingest-label">REFERENCE IMAGE (BASE MAP)</span>
              <button
                className="ingest-replace-btn"
                onClick={() => refFileRef.current?.click()}
                disabled={uploading === "reference"}
              >
                {uploading === "reference" ? "Uploading..." : "Browse File"}
              </button>
              <input
                ref={refFileRef}
                type="file"
                accept="image/*"
                style={{ display: "none" }}
                onChange={e => {
                  const f = e.target.files?.[0]
                  if (f) onUpload(f, "reference")
                }}
              />
            </div>
            <div className="ingest-preview">
              <img src={reference.preview} alt="Reference Preview" />
            </div>
            <div className="ingest-meta">
              <div className="meta-row">
                <span>File:</span>
                <code>{reference.filename}</code>
              </div>
              <div className="meta-row">
                <span>Sensor:</span>
                <span>{reference.sensor || "TMC-2"}</span>
              </div>
              <div className="meta-row">
                <span>Resolution:</span>
                <span>{reference.resolution || "5.0 m/px"}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <button className="modal-done-btn" onClick={onClose}>
            Apply Imagery & Return to Canvas
          </button>
        </div>
      </div>
    </div>
  )
}
