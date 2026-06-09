import { useState, useCallback } from 'react'
import { useNotes } from '../hooks/useNotes'
import { NoteCard } from '../components/NoteCard'
import { NoteForm } from '../components/NoteForm'
import { StatsBar } from '../components/StatsBar'
import { ICONS } from '../components/CategoryBadge'
import type {Note, Category, NoteCreate, NoteUpdate} from '../types'

const CATEGORIES: Category[] = ['idea', 'article', 'task', 'quote', 'resource', 'journal', 'other']

export function VaultPage() {
  const [search, setSearch] = useState('')
  const [activeCategory, setActiveCategory] = useState<Category | undefined>()
  const [pinnedOnly, setPinnedOnly] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [editingNote, setEditingNote] = useState<Note | null>(null)
  const [debouncedSearch, setDebouncedSearch] = useState('')

  // Debounce search
  const handleSearch = useCallback((val: string) => {
    setSearch(val)
    clearTimeout((window as any)._searchTimer)
    ;(window as any)._searchTimer = setTimeout(() => setDebouncedSearch(val), 300)
  }, [])

  const { notes, loading, error, createNote, updateNote, deleteNote, togglePin } = useNotes({
    search: debouncedSearch || undefined,
    category: activeCategory,
    pinned_only: pinnedOnly,
  })

  const openCreate = () => { setEditingNote(null); setShowForm(true) }
  const openEdit = (note: Note) => { setEditingNote(note); setShowForm(true) }
  const closeForm = () => { setShowForm(false); setEditingNote(null) }

  const handleSubmit = async (data: NoteCreate | NoteUpdate) => {
    if (editingNote) {
      await updateNote(editingNote.id, data as NoteUpdate)
    } else {
      await createNote(data as NoteCreate)
    }
    closeForm()
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('Delete this note?')) await deleteNote(id)
  }

  return (
    <div className="vault-page">
      {/* Header */}
      <header className="vault-header">
        <div className="header-left">
          <div className="logo">
            <span className="logo-text">Stash</span>
          </div>
        </div>
        <button className="btn-primary" onClick={openCreate}>+ New Note</button>
      </header>

      {/* Stats */}
      <StatsBar />

      {/* Filters */}
      <div className="filters">
        <input
          className="search-input"
          placeholder="Search notes…"
          value={search}
          onChange={e => handleSearch(e.target.value)}
        />
        <div className="category-filters">
          <button
            className={`filter-btn${!activeCategory ? ' active' : ''}`}
            onClick={() => setActiveCategory(undefined)}
          >
            All
          </button>
          {CATEGORIES.map(cat => (
            <button
              key={cat}
              className={`filter-btn${activeCategory === cat ? ' active' : ''}`}
              onClick={() => setActiveCategory(activeCategory === cat ? undefined : cat)}
            >
              {ICONS[cat]} {cat}
            </button>
          ))}
          <button
            className={`filter-btn pin-filter${pinnedOnly ? ' active' : ''}`}
            onClick={() => setPinnedOnly(p => !p)}
          >
            📌 Pinned
          </button>
        </div>
      </div>

      {/* Notes Grid */}
      <main className="notes-grid">
        {loading && <div className="state-msg">Loading…</div>}
        {error && <div className="state-msg error">{error}</div>}
        {!loading && !error && notes.length === 0 && (
          <div className="empty-state">
            <p>Your vault is empty.</p>
            <button className="btn-primary" onClick={openCreate}>Add your first note</button>
          </div>
        )}
        {notes.map(note => (
          <NoteCard
            key={note.id}
            note={note}
            onEdit={openEdit}
            onDelete={handleDelete}
            onTogglePin={togglePin}
          />
        ))}
      </main>

      {/* Modal */}
      {showForm && (
        <NoteForm
          note={editingNote}
          onSubmit={handleSubmit}
          onCancel={closeForm}
        />
      )}
    </div>
  )
}
