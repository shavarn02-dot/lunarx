'use client'
import React, { useState, useRef, useEffect } from 'react'
import { EXPLAINER_DICT, ExplainerItem } from './explainer-data'

export interface ExplainerProps {
  termKey?: string
  term?: string
  title?: string
  whatItDoes?: string
  projectRole?: string
  keywords?: string[]
  children?: React.ReactNode
  className?: string
  as?: 'span' | 'div'
  showIndicator?: boolean
  placement?: 'top' | 'bottom' | 'auto'
}

function escapeRegex(str: string) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function highlightKeywords(text: string, keywords?: string[]): React.ReactNode[] {
  if (!keywords || keywords.length === 0) return [text]

  const sorted = [...keywords].filter(Boolean).sort((a, b) => b.length - a.length)
  if (sorted.length === 0) return [text]

  const escaped = sorted.map((k) => escapeRegex(k))
  const pattern = new RegExp(`(${escaped.join('|')})`, 'gi')

  const parts = text.split(pattern)
  return parts.map((part, i) => {
    const isMatch = sorted.some((k) => k.toLowerCase() === part.toLowerCase())
    if (isMatch) {
      return (
        <span key={i} className="pencil-underline">
          {part}
        </span>
      )
    }
    return part
  })
}

export function Explainer({
  termKey,
  term,
  title,
  whatItDoes,
  projectRole,
  keywords,
  children,
  className = '',
  as: Component = 'span',
  showIndicator = false,
  placement = 'auto',
}: ExplainerProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [actualPlacement, setActualPlacement] = useState<'top' | 'bottom'>('top')
  const [shiftX, setShiftX] = useState(0)
  const triggerRef = useRef<HTMLElement>(null)
  const popoverRef = useRef<HTMLDivElement>(null)

  const dictItem: ExplainerItem | undefined = termKey ? EXPLAINER_DICT[termKey] : undefined
  const item: ExplainerItem = {
    title: title || dictItem?.title || term || termKey || 'LunarX Technical Concept',
    whatItDoes:
      whatItDoes ||
      dictItem?.whatItDoes ||
      'Ye ek core mathematical aur geometric step hai jo lunar imagery ko accurately map karne ke liye zaroori hai.',
    projectRole:
      projectRole ||
      dictItem?.projectRole ||
      'ISRO Chandrayaan-2 sub-pixel accuracy target ko reliably achieve karne mein contribute karta hai.',
    keywords: keywords || dictItem?.keywords || [],
  }

  useEffect(() => {
    if (!isOpen || !triggerRef.current) return

    const triggerRect = triggerRef.current.getBoundingClientRect()
    const viewportWidth = window.innerWidth
    const spaceAbove = triggerRect.top
    const spaceBelow = window.innerHeight - triggerRect.bottom

    if (placement === 'auto') {
      // If not enough room on top, flip to bottom
      if (spaceAbove < 290 && spaceBelow > 240) {
        setActualPlacement('bottom')
      } else {
        setActualPlacement('top')
      }
    } else {
      setActualPlacement(placement)
    }

    const centerX = triggerRect.left + triggerRect.width / 2
    const cardHalfWidth = 175
    let offset = 0
    if (centerX - cardHalfWidth < 16) {
      offset = 16 - (centerX - cardHalfWidth)
    } else if (centerX + cardHalfWidth > viewportWidth - 16) {
      offset = (viewportWidth - 16) - (centerX + cardHalfWidth)
    }
    setShiftX(offset)
  }, [isOpen, placement])

  return (
    <Component
      ref={triggerRef as any}
      className={`explainer-trigger ${className}`}
      onMouseEnter={() => setIsOpen(true)}
      onMouseLeave={() => setIsOpen(false)}
      onFocus={() => setIsOpen(true)}
      onBlur={() => setIsOpen(false)}
      tabIndex={0}
      role="button"
      aria-haspopup="dialog"
      aria-expanded={isOpen}
      onClick={(e) => {
        e.stopPropagation()
        setIsOpen((prev) => !prev)
      }}
    >
      {children ? children : <span>{item.title}</span>}
      {showIndicator && <span className="explainer-pencil-tag" aria-hidden="true">✎</span>}

      {isOpen && (
        <div
          ref={popoverRef}
          className={`handwritten-note-card placement-${actualPlacement}`}
          style={{
            transform: `translateX(calc(-50% + ${shiftX}px))`,
            ['--arrow-shift' as any]: `${-shiftX}px`,
          }}
          role="tooltip"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="note-top-badge">
            <span className="note-pin-icon">📌</span>
            <span className="note-badge-text">Teacher & Scientist Explainer</span>
            <span className="note-hindi-pill">सरल समझ</span>
          </div>

          <h4 className="note-title">{item.title}</h4>

          <div className="note-section">
            <div className="note-section-title">
              <span className="note-bullet">✎</span> Ye feature kya kaam karta hai?
            </div>
            <p className="note-body-text">
              {highlightKeywords(item.whatItDoes, item.keywords)}
            </p>
          </div>

          <div className="note-section">
            <div className="note-section-title">
              <span className="note-bullet">🚀</span> Project (LunarX) mein iska kya kaam hai?
            </div>
            <p className="note-body-text">
              {highlightKeywords(item.projectRole, item.keywords)}
            </p>
          </div>

          <div className="note-footer">
            <span>ISRO PS-26166 · Chandrayaan-2 TMC-2 Matching</span>
            <span className="note-watermark">Handwritten Note</span>
          </div>
        </div>
      )}
    </Component>
  )
}
export default Explainer
