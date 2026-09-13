import { NextResponse } from 'next/server'

const DEFAULT_PAIRS = [
  {
    id: 'tmc_crater',
    name: 'Crater field — TMC-2 cross-pass (600 x 600)',
    source_img: 'ch2_tmc_crater_scene_src.png',
    reference_img: 'ch2_tmc_crater_scene_ref.png',
    sensor: 'TMC-2',
    resolution: '5.0 m/px',
    orbit: 'Orbit 3922 vs 3943',
    description: 'Standard benchmark lunar crater scene with severe shadow asymmetry.',
    source: {
      file: 'ch2_tmc_crater_scene_src.png',
      sensor: 'TMC-2',
      provenance: 'VERIFIED_CHANDRAYAAN',
      width: 600,
      height: 600,
    },
    reference: {
      file: 'ch2_tmc_crater_scene_ref.png',
      sensor: 'TMC-2',
      provenance: 'VERIFIED_CHANDRAYAAN',
      width: 600,
      height: 600,
    },
  },
  {
    id: 'strip_ohrc',
    name: 'Cross-Sensor — TMC-2 crop vs OHRC patch (20x scale gap)',
    source_img: 'ch2_tmc_ncn_patch_crop.jpg',
    reference_img: 'ch2_ohr_ncp_overlap_patch.jpg',
    sensor: 'TMC-2 vs OHRC',
    resolution: '5.0m vs 0.25m',
    orbit: 'Orbit 20191125',
    description: 'Challenging 20x cross-sensor resolution gap challenge.',
    source: {
      file: 'ch2_tmc_ncn_patch_crop.jpg',
      sensor: 'TMC-2',
      provenance: 'VERIFIED_CHANDRAYAAN',
      width: 384,
      height: 384,
    },
    reference: {
      file: 'ch2_ohr_ncp_overlap_patch.jpg',
      sensor: 'OHRC',
      provenance: 'VERIFIED_CHANDRAYAAN',
      width: 1280,
      height: 1280,
    },
  },
  {
    id: 'crater_alpha',
    name: 'Crater Region Alpha (High-Contrast Rim)',
    source_img: 'Pair_Crater_Region_Alpha_SRC.png',
    reference_img: 'Pair_Crater_Region_Alpha_REF.png',
    sensor: 'TMC-2',
    resolution: '5.0 m/px',
    orbit: 'Orbit 3922 (Strip Segment A)',
    description: 'Prominent circular impact rim with secondary ejecta field.',
  },
  {
    id: 'crater_beta',
    name: 'Crater Region Beta (Terminator Shadow Slope)',
    source_img: 'Pair_Crater_Region_Beta_SRC.png',
    reference_img: 'Pair_Crater_Region_Beta_REF.png',
    sensor: 'TMC-2',
    resolution: '5.0 m/px',
    orbit: 'Orbit 3943 (Strip Segment B)',
    description: 'Steep lunar slope with deep shadow transition.',
  },
  {
    id: 'crater_gamma',
    name: 'Crater Region Gamma (Central Peak Feature)',
    source_img: 'Pair_Crater_Region_Gamma_SRC.png',
    reference_img: 'Pair_Crater_Region_Gamma_REF.png',
    sensor: 'TMC-2',
    resolution: '5.0 m/px',
    orbit: 'Orbit 3922 (Strip Segment C)',
    description: 'Central peak illumination with floor micro-craters.',
  },
  {
    id: 'crater_delta',
    name: 'Crater Region Delta (Multi-Crater Cluster)',
    source_img: 'Pair_Crater_Region_Delta_SRC.png',
    reference_img: 'Pair_Crater_Region_Delta_REF.png',
    sensor: 'TMC-2',
    resolution: '5.0 m/px',
    orbit: 'Orbit 3943 (Strip Segment D)',
    description: 'Dense overlapping craterlets and regolith textures.',
  },
]

export async function GET() {
  const backendUrl =
    process.env.LUNARX_BACKEND_URL ||
    (process.env.NODE_ENV === 'production' || process.env.VERCEL
      ? 'https://lunarx-backend.onrender.com'
      : 'http://127.0.0.1:8000')
  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 6000)
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
  } catch (e) {
    // Backend offline or running in standalone Vercel cloud deployment
  }

  return NextResponse.json(DEFAULT_PAIRS)
}
