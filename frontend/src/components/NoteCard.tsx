import type { Note } from '../types'
import { CategoryBadge } from './CategoryBadge'

interface Props {
  note: Note
  onEdit: (note: Note) => void
  onDelete: (id: number) => void
  onTogglePin: (note: Note) => void
}

export function NoteCard({ note, onEdit, onDelete, onTogglePin }: Props) {
  const tags = note.tags ? note.tags.split(',').map(t => t.trim()).filter(Boolean) : []
  const date = new Date(note.updated_at).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
  })

  return (
    <div className={`note-card${note.is_pinned ? ' pinned' : ''}`}>
      <div className="note-card-header">
        <CategoryBadge category={note.category} />
        <button
          className={`pin-btn${note.is_pinned ? ' active' : ''}`}
          onClick={() => onTogglePin(note)}
          title={note.is_pinned ? 'Unpin' : 'Pin'}
        >
          📌
        </button>
      </div>

      <h3 className="note-title">{note.title}</h3>

      {note.summary && (
        <p className="note-summary">{note.summary}</p>
      )}

      {tags.length > 0 && (
        <div className="note-tags">
          {tags.map(tag => (
            <span key={tag} className="tag">#{tag}</span>
          ))}
        </div>
      )}

      <div className="note-footer">
        <span className="note-date">{date}</span>
        <div className="note-actions">
          <button className="action-btn" onClick={() => onEdit(note)}>Edit</button>
          <button className="action-btn danger" onClick={() => onDelete(note.id)}>Delete</button>
        </div>
      </div>
    </div>
  )
}
