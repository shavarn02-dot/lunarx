'use client'

import {
  Header,
  HeaderName,
  HeaderNavigation,
  HeaderMenuItem,
  HeaderGlobalBar,
  HeaderGlobalAction,
  SkipToContent,
} from '@carbon/react'
import { Asleep, Light } from '@carbon/icons-react'
import { useTheme } from '@/components/theme-provider'

export function SiteHeader() {
  const { theme, toggleTheme } = useTheme()
  const isDark = theme === 'g100'

  return (
    <Header aria-label="ISRO Satellite Imagery Analysis">
      <SkipToContent />
      <HeaderName href="/" prefix="ISRO">
        Bhuvan Analytics
      </HeaderName>
      <HeaderNavigation aria-label="ISRO Satellite Imagery Analysis">
        <HeaderMenuItem href="#overview">Overview</HeaderMenuItem>
        <HeaderMenuItem href="#analysis">Analysis</HeaderMenuItem>
        <HeaderMenuItem href="#metrics">Metrics</HeaderMenuItem>
      </HeaderNavigation>
      <HeaderGlobalBar>
        <HeaderGlobalAction
          aria-label={isDark ? 'Switch to light theme' : 'Switch to dark theme'}
          tooltipAlignment="end"
          onClick={toggleTheme}
        >
          {isDark ? <Light size={20} /> : <Asleep size={20} />}
        </HeaderGlobalAction>
      </HeaderGlobalBar>
    </Header>
  )
}
