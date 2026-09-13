import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData()
    const file = formData.get('file') as File | null
    if (!file) {
      return NextResponse.json({ error: 'No file uploaded' }, { status: 400 })
    }

    const backendUrl = process.env.LUNARX_BACKEND_URL || 'http://127.0.0.1:8000'
    try {
      const controller = new AbortController()
      const timeout = setTimeout(() => controller.abort(), 15000)
      const forwardData = new FormData()
      forwardData.append('file', file)
      const res = await fetch(`${backendUrl}/api/upload`, {
        method: 'POST',
        body: forwardData,
        signal: controller.signal,
      })
      clearTimeout(timeout)
      if (res.ok) {
        const data = await res.json()
        return NextResponse.json({ ...data, backend: true })
      }
    } catch (e) {
      // Backend offline or running on Vercel
    }

    // Fallback: tell frontend to keep the local blob preview
    const filename = `upload_${Date.now()}_upload_src_${file.name}`
    return NextResponse.json({
      filename,
      url: '',
      bytes: file.size,
      backend: false,
      local_only: true,
    })
  } catch (err: any) {
    return NextResponse.json({ error: err?.message || 'Upload failed' }, { status: 500 })
  }
}
