import { useStats } from '../hooks/useStats'
import { COLORS, ICONS } from './CategoryBadge'
import type { Category } from '../types'

export function StatsBar() {
  const stats = useStats()
  if (!stats) return null

  return (
    <div className="stats-bar">
      <div className="stat-item">
        <span className="stat-value">{stats.total}</span>
        <span className="stat-label">Total</span>
      </div>
      <div className="stat-divider" />
      <div className="stat-item">
        <span className="stat-value">📌 {stats.pinned}</span>
        <span className="stat-label">Pinned</span>
      </div>
      <div className="stat-divider" />
      {Object.entries(stats.by_category).map(([cat, count]) => (
        <div key={cat} className="stat-item">
          <span className="stat-value" style={{ color: COLORS[cat as Category] }}>
            {ICONS[cat as Category]} {count}
          </span>
          <span className="stat-label">{cat}</span>
        </div>
      ))}
    </div>
  )
}
