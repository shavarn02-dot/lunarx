import { NextRequest, NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'
export const maxDuration = 60

export async function POST(req: NextRequest) {
  let body: any = {}
  try {
    body = await req.json()
  } catch {
    body = {}
  }

  const backendUrl =
    (process.env.LUNARX_BACKEND_URL && !process.env.LUNARX_BACKEND_URL.includes('onrender.com'))
      ? process.env.LUNARX_BACKEND_URL
      : 'https://communication-earthquake-chief-tahoe.trycloudflare.com'

  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 60000)

    const res = await fetch(`${backendUrl}/api/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: controller.signal,
    })
    clearTimeout(timeout)

    const data = await res.json().catch(() => null)
    if (!data) {
      return NextResponse.json(
        {
          success: false,
          status: 'FAILED',
          error: `Registration pipeline returned HTTP ${res.status}`,
        },
        { status: res.status }
      )
    }

    // Prefix dynamically generated output images with the backend URL so frontend loads real files
    if (data.images && typeof data.images === 'object') {
      for (const k of Object.keys(data.images)) {
        const val = data.images[k]
        if (val && typeof val === 'string' && !val.startsWith('http')) {
          data.images[k] = `${backendUrl}/images/${val.replace(/^\/images\//, '')}`
        }
      }
    }

    return NextResponse.json(data, { status: res.status })
  } catch (err: any) {
    const isTimeout = err?.name === 'AbortError'
    return NextResponse.json(
      {
        success: false,
        status: 'OFFLINE',
        error: isTimeout
          ? 'Registration pipeline timed out after 60s. Please retry or pick a faster matcher (SIFT/ORB).'
          : `Python Registration Engine unreachable (${err?.message || 'Connection failed'}). Backend must be running at ${backendUrl}.`,
      },
      { status: 503 }
    )
  }
}
