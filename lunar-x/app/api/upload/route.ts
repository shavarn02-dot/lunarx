import { NextRequest, NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData()
    const file = formData.get('file') as File | null
    if (!file) {
      return NextResponse.json({ error: 'No file uploaded' }, { status: 400 })
    }

    const backendUrl =
      process.env.LUNARX_BACKEND_URL ||
      (process.env.NODE_ENV === 'production' || process.env.VERCEL
        ? 'https://lunarx-backend.onrender.com'
        : 'http://127.0.0.1:8000')

    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 45000)
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
      return NextResponse.json(data)
    }

    const errDetail = await res.text().catch(() => '')
    return NextResponse.json(
      { error: `Backend upload failed (${res.status}): ${errDetail}` },
      { status: res.status }
    )
  } catch (err: any) {
    return NextResponse.json(
      { error: `Upload pipeline error: ${err?.message || 'Connection failed'}` },
      { status: 503 }
    )
  }
}
