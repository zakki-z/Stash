from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from app.models.note import Note, Category
from app.schemas.note import NoteCreate, NoteUpdate
from app.services.summarizer import auto_summarize, auto_categorize


class NoteService:
    def get_all(
        self,
        db: Session,
        search: Optional[str] = None,
        category: Optional[Category] = None,
        pinned_only: bool = False,
    ) -> list[Note]:
        query = db.query(Note)

        if search:
            like = f"%{search}%"
            query = query.filter(
                or_(
                    Note.title.ilike(like),
                    Note.content.ilike(like),
                    Note.tags.ilike(like),
                )
            )

        if category:
            query = query.filter(Note.category == category)

        if pinned_only:
            query = query.filter(Note.is_pinned == True)

        return query.order_by(Note.is_pinned.desc(), Note.updated_at.desc()).all()

    def get_by_id(self, db: Session, note_id: int) -> Optional[Note]:
        return db.query(Note).filter(Note.id == note_id).first()

    def create(self, db: Session, payload: NoteCreate) -> Note:
        summary = auto_summarize(payload.content)
        category = payload.category

        # Auto-categorize if not explicitly set
        if category == Category.other:
            category = auto_categorize(payload.title, payload.content)

        note = Note(
            title=payload.title,
            content=payload.content,
            summary=summary,
            category=category,
            tags=payload.tags,
            source_url=payload.source_url,
            is_pinned=payload.is_pinned,
        )
        db.add(note)
        db.commit()
        db.refresh(note)
        return note

    def update(self, db: Session, note_id: int, payload: NoteUpdate) -> Optional[Note]:
        note = self.get_by_id(db, note_id)
        if not note:
            return None

        data = payload.model_dump(exclude_unset=True)

        # Re-summarize if content changed
        if "content" in data:
            data["summary"] = auto_summarize(data["content"])

        for field, value in data.items():
            setattr(note, field, value)

        db.commit()
        db.refresh(note)
        return note

    def delete(self, db: Session, note_id: int) -> bool:
        note = self.get_by_id(db, note_id)
        if not note:
            return False
        db.delete(note)
        db.commit()
        return True


note_service = NoteService()
