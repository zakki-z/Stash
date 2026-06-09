import { useState, useEffect } from 'react'
import { statsApi } from '../api/client'
import type { Stats } from '../types'

export function useStats() {
  const [stats, setStats] = useState<Stats | null>(null)

  useEffect(() => {
    statsApi.get().then(setStats).catch(() => null)
  }, [])

  return stats
}
