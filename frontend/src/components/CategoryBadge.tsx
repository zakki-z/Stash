import type { Category } from '../types'

const COLORS: Record<Category, string> = {
  idea: '#f59e0b',
  article: '#3b82f6',
  task: '#10b981',
  quote: '#8b5cf6',
  resource: '#06b6d4',
  journal: '#ec4899',
  other: '#6b7280',
}

const ICONS: Record<Category, string> = {
  idea: '💡',
  article: '📄',
  task: '✅',
  quote: '💬',
  resource: '🔗',
  journal: '📔',
  other: '📦',
}

interface Props {
  category: Category
  size?: 'sm' | 'md'
}

export function CategoryBadge({ category, size = 'sm' }: Props) {
  const color = COLORS[category]
  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '4px',
        padding: size === 'sm' ? '2px 8px' : '4px 12px',
        borderRadius: '999px',
        fontSize: size === 'sm' ? '11px' : '13px',
        fontWeight: 600,
        letterSpacing: '0.04em',
        background: `${color}22`,
        color,
        border: `1px solid ${color}44`,
        textTransform: 'uppercase',
      }}
    >
      {ICONS[category]} {category}
    </span>
  )
}

export { COLORS, ICONS }
