import { useState, useEffect, useCallback } from 'react'
import { notesApi } from '../api/client'
import type { Note, NoteCreate, NoteUpdate, Category } from '../types'

interface Filters {
  search?: string
  category?: Category
  pinned_only?: boolean
}

export function useNotes(filters: Filters = {}) {
  const [notes, setNotes] = useState<Note[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await notesApi.list(filters)
      setNotes(data)
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }, [filters.search, filters.category, filters.pinned_only]) // eslint-disable-line

  useEffect(() => { load() }, [load])

  const createNote = async (payload: NoteCreate) => {
    const note = await notesApi.create(payload)
    setNotes(prev => [note, ...prev])
    return note
  }

  const updateNote = async (id: number, payload: NoteUpdate) => {
    const note = await notesApi.update(id, payload)
    setNotes(prev => prev.map(n => (n.id === id ? note : n)))
    return note
  }

  const deleteNote = async (id: number) => {
    await notesApi.delete(id)
    setNotes(prev => prev.filter(n => n.id !== id))
  }

  const togglePin = (note: Note) =>
    updateNote(note.id, { is_pinned: !note.is_pinned })

  return { notes, loading, error, reload: load, createNote, updateNote, deleteNote, togglePin }
}
