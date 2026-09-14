import { NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'

export async function GET() {
  const backendUrl =
    (process.env.LUNARX_BACKEND_URL && !process.env.LUNARX_BACKEND_URL.includes('onrender.com'))
      ? process.env.LUNARX_BACKEND_URL
      : 'https://turbo-incident-delhi-greatly.trycloudflare.com'

  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 8000)
    const res = await fetch(`${backendUrl}/api/health`, {
      signal: controller.signal,
      cache: 'no-store',
    })
    clearTimeout(timeout)
    if (res.ok) {
      const data = await res.json()
      return NextResponse.json(data)
    }
    return NextResponse.json(
      { status: 'OFFLINE', error: `Backend returned status ${res.status}` },
      { status: res.status }
    )
  } catch (err: any) {
    return NextResponse.json(
      {
        status: 'OFFLINE',
        error: `Cannot reach Python backend at ${backendUrl}: ${err?.message}`,
      },
      { status: 503 }
    )
  }
}
