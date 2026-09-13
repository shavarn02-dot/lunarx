import { NextRequest, NextResponse } from 'next/server'

export const runtime = 'nodejs'
const ENGINE = 'http://127.0.0.1:8000/api'
const offline = () => NextResponse.json({ error: 'The Python processing engine is unavailable. No registration was performed. You can inspect the images or explore the saved example.' }, { status: 503 })

export async function GET(_request: NextRequest, { params }: { params: Promise<{ action: string }> }) {
  if ((await params).action !== 'health') return new NextResponse(null, { status: 404 })
  try {
    const response = await fetch(`${ENGINE}/health`, { cache: 'no-store', signal: AbortSignal.timeout(2000) })
    return NextResponse.json(await response.json(), { status: response.status })
  } catch { return offline() }
}

export async function POST(request: NextRequest, { params }: { params: Promise<{ action: string }> }) {
  const { action } = await params
  if (!['register', 'upload'].includes(action)) return new NextResponse(null, { status: 404 })
  const origin = request.headers.get('origin')
  if (origin && new URL(origin).host !== request.headers.get('host') && new URL(origin).host !== request.headers.get('x-forwarded-host')) return NextResponse.json({ error: 'Cross-origin request rejected.' }, { status: 403 })
  try {
    let body: BodyInit
    let headers: HeadersInit | undefined
    if (action === 'upload') {
      if (Number(request.headers.get('content-length') || 0) > 21 * 1024 * 1024) return NextResponse.json({ error: 'Maximum file size is 20 MB.' }, { status: 413 })
      const form = await request.formData()
      const file = form.get('file')
      if (!(file instanceof File) || file.size > 20 * 1024 * 1024 || !/\.(png|jpe?g|tiff?)$/i.test(file.name)) return NextResponse.json({ error: 'Choose a PNG, JPEG or TIFF image under 20 MB.' }, { status: 400 })
      const safeForm = new FormData()
      safeForm.append('file', file, `upload_${crypto.randomUUID()}.${file.name.split('.').pop()?.toLowerCase()}`)
      body = safeForm
    } else {
      const data = await request.json()
      const validName = (value: unknown) => typeof value === 'string' && /^[\w. -]+\.(png|jpe?g|tiff?)$/i.test(value) && !value.includes('..')
      if (!validName(data.source_filename) || !validName(data.reference_filename) || !['sift', 'orb', 'superpoint_lightglue', 'loftr'].includes(data.method) || !['clahe', 'gradient', 'raw'].includes(data.preprocessing) || !['affine', 'homography', 'rigid'].includes(data.model_type) || typeof data.subpixel !== 'boolean' || typeof data.spatial_filter !== 'boolean' || typeof data.reproj_thresh !== 'number' || !Number.isFinite(data.reproj_thresh) || data.reproj_thresh < .5 || data.reproj_thresh > 10) return NextResponse.json({ error: 'Invalid registration settings.' }, { status: 400 })
      body = JSON.stringify(data)
      headers = { 'Content-Type': 'application/json' }
    }
    const response = await fetch(`${ENGINE}/${action}`, { method: 'POST', body, headers, signal: AbortSignal.timeout(action === 'register' ? 175000 : 30000) })
    return NextResponse.json(await response.json(), { status: response.status })
  } catch (error) {
    if (error instanceof SyntaxError) return NextResponse.json({ error: 'Invalid request data.' }, { status: 400 })
    return offline()
  }
}
