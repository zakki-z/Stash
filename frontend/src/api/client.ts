import type { Note, NoteCreate, NoteUpdate, Stats, Category } from '../types'

const BASE = '/api'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail ?? `HTTP ${res.status}`)
  }
  if (res.status === 204) return undefined as T
  return res.json()
}

export const notesApi = {
  list(params?: { search?: string; category?: Category; pinned_only?: boolean }): Promise<Note[]> {
    const qs = new URLSearchParams()
    if (params?.search) qs.set('search', params.search)
    if (params?.category) qs.set('category', params.category)
    if (params?.pinned_only) qs.set('pinned_only', 'true')
    return request(`/notes/?${qs}`)
  },

  get(id: number): Promise<Note> {
    return request(`/notes/${id}`)
  },

  create(payload: NoteCreate): Promise<Note> {
    return request('/notes/', { method: 'POST', body: JSON.stringify(payload) })
  },

  update(id: number, payload: NoteUpdate): Promise<Note> {
    return request(`/notes/${id}`, { method: 'PATCH', body: JSON.stringify(payload) })
  },

  delete(id: number): Promise<void> {
    return request(`/notes/${id}`, { method: 'DELETE' })
  },
}

export const statsApi = {
  get(): Promise<Stats> {
    return request('/stats/')
  },
}
