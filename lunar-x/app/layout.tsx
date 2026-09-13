import type { Metadata } from 'next'
import type { ReactNode } from 'react'
import './globals.scss'

export const metadata: Metadata = {
  title: 'LUNARX | Chandra-Sync Scientific Workspace',
  description:
    'Autonomous Lunar Image Registration & Matching (PS-SIH26166)',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        {children}
      </body>
    </html>
  )
}
