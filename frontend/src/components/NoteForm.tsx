import { useState, useEffect } from 'react'
import type { Note, NoteCreate, NoteUpdate, Category } from '../types'

const CATEGORIES: Category[] = ['idea', 'article', 'task', 'quote', 'resource', 'journal', 'other']

interface Props {
  note?: Note | null
  onSubmit: (data: NoteCreate | NoteUpdate) => Promise<void>
  onCancel: () => void
}

export function NoteForm({ note, onSubmit, onCancel }: Props) {
  const [title, setTitle] = useState(note?.title ?? '')
  const [content, setContent] = useState(note?.content ?? '')
  const [category, setCategory] = useState<Category>(note?.category ?? 'other')
  const [tags, setTags] = useState(note?.tags ?? '')
  const [sourceUrl, setSourceUrl] = useState(note?.source_url ?? '')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (note) {
      setTitle(note.title)
      setContent(note.content)
      setCategory(note.category)
      setTags(note.tags ?? '')
      setSourceUrl(note.source_url ?? '')
    }
  }, [note])

  const handleSubmit = async () => {
    if (!title.trim() || !content.trim()) {
      setError('Title and content are required.')
      return
    }
    setSaving(true)
    setError(null)
    try {
      await onSubmit({
        title: title.trim(),
        content: content.trim(),
        category,
        tags: tags.trim() || undefined,
        source_url: sourceUrl.trim() || undefined,
      })
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{note ? 'Edit Note' : 'New Note'}</h2>
          <button className="close-btn" onClick={onCancel}>✕</button>
        </div>

        {error && <p className="form-error">{error}</p>}

        <div className="form-group">
          <label>Title</label>
          <input
            className="form-input"
            value={title}
            onChange={e => setTitle(e.target.value)}
            placeholder="Give it a name..."
          />
        </div>

        <div className="form-group">
          <label>Category</label>
          <select className="form-select" value={category} onChange={e => setCategory(e.target.value as Category)}>
            {CATEGORIES.map(c => (
              <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Content</label>
          <textarea
            className="form-textarea"
            value={content}
            onChange={e => setContent(e.target.value)}
            placeholder="Dump your thoughts here..."
            rows={8}
          />
        </div>

        <div className="form-group">
          <label>Tags <span className="label-hint">(comma-separated)</span></label>
          <input
            className="form-input"
            value={tags}
            onChange={e => setTags(e.target.value)}
            placeholder="ml, finance, reading"
          />
        </div>

        <div className="form-group">
          <label>Source URL <span className="label-hint">(optional)</span></label>
          <input
            className="form-input"
            value={sourceUrl}
            onChange={e => setSourceUrl(e.target.value)}
            placeholder="https://..."
          />
        </div>

        <div className="modal-footer">
          <button className="btn-secondary" onClick={onCancel}>Cancel</button>
          <button className="btn-primary" onClick={handleSubmit} disabled={saving}>
            {saving ? 'Saving…' : note ? 'Update' : 'Create'}
          </button>
        </div>
      </div>
    </div>
  )
}
