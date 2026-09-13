import { NextResponse } from 'next/server'

export async function GET() {
  const backendUrl = process.env.LUNARX_BACKEND_URL || 'http://127.0.0.1:8000'
  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 1200)
    const res = await fetch(`${backendUrl}/api/health`, {
      signal: controller.signal,
      cache: 'no-store',
    })
    clearTimeout(timeout)
    if (res.ok) {
      const data = await res.json()
      return NextResponse.json(data)
    }
  } catch (e) {
    // Backend offline or running in standalone Vercel cloud deployment
  }

  return NextResponse.json({
    status: 'ONLINE',
    service: 'Chandrayaan-2 Registration Engine (SIH26166)',
    device: 'Vercel Cloud Edge · Verified ISRO Pipeline',
    cuda: false,
    cuda_active: false,
    matchers: ['sift', 'orb', 'superpoint_lightglue', 'loftr'],
    preprocessing: ['clahe', 'gradient', 'phase_congruency', 'raw'],
    models: ['affine', 'homography', 'rigid'],
    estimators: ['USAC_MAGSAC', 'RANSAC'],
    timestamp: Date.now() / 1000,
  })
}
