import type { Metadata } from 'next'
import type { ReactNode } from 'react'
import './globals.scss'

export const metadata: Metadata = {
  title: 'LunarX | Chandrayaan-2 Image Alignment',
  description: 'A clear workspace for aligning and reviewing Chandrayaan-2 lunar imagery for ISRO SIH 26166.',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return <html lang="en"><body>{children}</body></html>
}
