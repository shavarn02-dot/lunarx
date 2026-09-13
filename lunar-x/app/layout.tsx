import type { Metadata } from 'next'
import type { ReactNode } from 'react'
import { ThemeProvider } from '@/components/theme-provider'
import './globals.scss'
import './isro-console.css'
import './chandra-sync.css'

export const metadata: Metadata = {
  title: 'Chandra-sync | ISRO Chandrayaan-2 Planetary Image Registration System',
  description:
    'Chandra-sync: Autonomous Sub-Pixel Image Registration & Multi-Sensor Lunar Photogrammetry (OHRC, TMC-2, IIRS) - ISRO SIH26166',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
