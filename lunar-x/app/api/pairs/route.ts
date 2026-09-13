import { NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'

export async function GET() {
  const backendUrl =
    process.env.LUNARX_BACKEND_URL || 'https://born-heated-specially-removing.trycloudflare.com'

  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 10000)
    const res = await fetch(`${backendUrl}/api/pairs`, {
      signal: controller.signal,
      cache: 'no-store',
    })
    clearTimeout(timeout)
    if (res.ok) {
      const data = await res.json()
      if (Array.isArray(data) && data.length > 0) {
        return NextResponse.json(data)
      }
    }
    return NextResponse.json(
      { error: `Backend returned status ${res.status}` },
      { status: res.status }
    )
  } catch (err: any) {
    return NextResponse.json(
      { error: `Cannot load orbital pairs from backend: ${err?.message}` },
      { status: 503 }
    )
  }
}
