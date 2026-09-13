import type { Metadata, Viewport } from 'next'
import type { ReactNode } from 'react'
import { IBM_Plex_Sans, IBM_Plex_Mono } from 'next/font/google'
import './globals.css'

const sans = IBM_Plex_Sans({ subsets: ['latin'], weight: ['400', '500', '600', '700'], variable: '--font-plex-sans' })
const mono = IBM_Plex_Mono({ subsets: ['latin'], weight: ['400', '500'], variable: '--font-plex-mono' })

export const metadata: Metadata = {
  title: 'Chandra-sync | Lunar Image Registration',
  description: 'A focused workspace to compare, align, and evaluate lunar images. Chandrayaan-2 image registration research project for Smart India Hackathon 2026.',
}
export const viewport: Viewport = { themeColor: '#111a25', width: 'device-width', initialScale: 1 }

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={`bg-background ${sans.variable} ${mono.variable}`}>
      <body className="font-sans"><a className="skip-link" href="#workspace">Skip to workspace</a>{children}</body>
    </html>
  )
}
