import type { ImageInfo } from './types'
import { Explainer } from './explainer'

export function ImageInput({
  label,
  image,
  onUpload,
  uploading,
}: {
  label: string
  image: ImageInfo
  onUpload: (file: File) => void
  uploading: boolean
}) {
  const isSource = label.toLowerCase().includes('source')
  const termKey = isSource ? 'source_image' : 'reference_image'

  return (
    <article className="image-input">
      <div className="section-label">
        <Explainer termKey={termKey} showIndicator={true}>
          <span>{label}</span>
        </Explainer>
      </div>
      <div className="input-preview">
        <img
          src={image.preview}
          alt={`${label.toLowerCase()} lunar image preview`}
        />
      </div>
      <div className="file-row">
        <code title={image.filename}>{image.filename}</code>
        <label className="upload-button">
          {uploading ? 'Uploading…' : 'Replace image'}
          <input
            type="file"
            accept=".png,.jpg,.jpeg,.tif,.tiff"
            disabled={uploading}
            onChange={(e) => e.target.files?.[0] && onUpload(e.target.files[0])}
          />
        </label>
      </div>
      <dl className="metadata">
        <div>
          <dt>
            <Explainer termKey="tmc2_sensor" showIndicator={true}>
              <span>Instrument</span>
            </Explainer>
          </dt>
          <dd>{image.sensor || 'Not available'}</dd>
        </div>
        <div>
          <dt>Resolution</dt>
          <dd>{image.resolution || 'Not available'}</dd>
        </div>
        <div>
          <dt>Orbit</dt>
          <dd>{image.orbit || 'Not available'}</dd>
        </div>
        <div>
          <dt>
            <Explainer termKey="provenance" showIndicator={true}>
              <span>Provenance</span>
            </Explainer>
          </dt>
          <dd>{image.provenance || 'Awaiting validation'}</dd>
        </div>
      </dl>
    </article>
  )
}
