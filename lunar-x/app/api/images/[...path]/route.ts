import { NextRequest, NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const resolvedParams = await params
  const filename = resolvedParams.path.join('/')

  // Potential directories where images might be located
  const projectRoot = path.resolve(process.cwd(), '..')
  const candidateDirs = [
    path.resolve(process.cwd(), 'public', 'images'),
    path.resolve(projectRoot, 'data', 'upload_samples'),
    path.resolve(projectRoot, 'data', 'raw'),
    path.resolve(projectRoot, 'data', 'outputs'),
    path.resolve(projectRoot, 'ppt_visuals'),
  ]

  let foundPath: string | null = null

  for (const dir of candidateDirs) {
    const fullPath = path.join(dir, filename)
    if (fs.existsSync(fullPath)) {
      foundPath = fullPath
      break
    }
  }

  if (!foundPath) {
    return new NextResponse(`Image not found: ${filename}`, { status: 404 })
  }

  try {
    const buffer = fs.readFileSync(foundPath)
    const ext = path.extname(foundPath).toLowerCase()
    let contentType = 'image/png'
    if (ext === '.jpg' || ext === '.jpeg') contentType = 'image/jpeg'
    else if (ext === '.webp') contentType = 'image/webp'
    else if (ext === '.svg') contentType = 'image/svg+xml'

    return new NextResponse(buffer, {
      status: 200,
      headers: {
        'Content-Type': contentType,
        'Cache-Control': 'no-store, must-revalidate',
      },
    })
  } catch (err: any) {
    return new NextResponse(`Error reading image: ${err.message}`, { status: 500 })
  }
}
