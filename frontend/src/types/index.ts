export type Category =
  | 'idea'
  | 'article'
  | 'task'
  | 'quote'
  | 'resource'
  | 'journal'
  | 'other'

export interface Note {
  id: number
  title: string
  content: string
  summary: string | null
  category: Category
  tags: string | null
  source_url: string | null
  is_pinned: boolean
  created_at: string
  updated_at: string
}

export interface NoteCreate {
  title: string
  content: string
  category?: Category
  tags?: string
  source_url?: string
  is_pinned?: boolean
}

export interface NoteUpdate {
  title?: string
  content?: string
  summary?: string
  category?: Category
  tags?: string
  source_url?: string
  is_pinned?: boolean
}

export interface Stats {
  total: number
  pinned: number
  by_category: Record<Category, number>
}
