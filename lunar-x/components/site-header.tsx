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

interface SiteHeaderProps {
  activeTab?: number
  onSelectTab?: (tabIndex: number) => void
}

export function SiteHeader({ activeTab, onSelectTab }: SiteHeaderProps) {
  const { theme, toggleTheme } = useTheme()
  const isDark = theme === 'g100'

  const handleNavClick = (e: React.MouseEvent, index: number) => {
    e.preventDefault()
    if (onSelectTab) {
      onSelectTab(index)
    }
  }

  return (
    <Header aria-label="ISRO Chandrayaan-2 Planetary Imagery Registration">
      <SkipToContent />
      <HeaderName href="/" prefix="ISRO SAC">
        CHANDRA-ALIGN • SIH26166
      </HeaderName>
      <HeaderNavigation aria-label="ISRO Planetary Image Registration Navigation">
        <HeaderMenuItem 
          href="#overview" 
          isActive={activeTab === 0}
          onClick={(e) => handleNavClick(e, 0)}
        >
          Mission Control
        </HeaderMenuItem>
        <HeaderMenuItem 
          href="#matching" 
          isActive={activeTab === 1}
          onClick={(e) => handleNavClick(e, 1)}
        >
          Feature Matching
        </HeaderMenuItem>
        <HeaderMenuItem 
          href="#interactive" 
          isActive={activeTab === 2}
          onClick={(e) => handleNavClick(e, 2)}
        >
          Interactive Inspector &amp; Blending
        </HeaderMenuItem>
        <HeaderMenuItem 
          href="#outputs" 
          isActive={activeTab === 3}
          onClick={(e) => handleNavClick(e, 3)}
        >
          Registered Outputs
        </HeaderMenuItem>
        <HeaderMenuItem 
          href="#benchmarks" 
          isActive={activeTab === 4}
          onClick={(e) => handleNavClick(e, 4)}
        >
          Benchmark Leaderboard
        </HeaderMenuItem>
        <HeaderMenuItem 
          href="#architecture" 
          isActive={activeTab === 5}
          onClick={(e) => handleNavClick(e, 5)}
        >
          System Architecture
        </HeaderMenuItem>
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
