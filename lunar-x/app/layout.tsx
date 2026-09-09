import type { Metadata } from 'next'
import type { ReactNode } from 'react'
import { ThemeProvider } from '@/components/theme-provider'
import './globals.scss'

export const metadata: Metadata = {
  title: 'CHANDRA-ALIGN | ISRO Chandrayaan-2 Planetary Image Registration System',
  description:
    'Automatic Feature Extraction and Sub-Pixel Image Registration of Chandrayaan-2 Lunar Imagery (OHRC, TMC-2, IIRS) - SIH26166',
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
