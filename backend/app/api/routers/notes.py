from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.models.note import Category
from app.schemas.note import NoteCreate, NoteUpdate, NoteOut
from app.services.note_service import note_service

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[NoteOut])
def list_notes(
    search: Optional[str] = Query(None),
    category: Optional[Category] = Query(None),
    pinned_only: bool = Query(False),
    db: Session = Depends(get_db),
):
    return note_service.get_all(db, search=search, category=category, pinned_only=pinned_only)


@router.get("/{note_id}", response_model=NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = note_service.get_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post("/", response_model=NoteOut, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    return note_service.create(db, payload)


@router.patch("/{note_id}", response_model=NoteOut)
def update_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db)):
    note = note_service.update(db, note_id, payload)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    deleted = note_service.delete(db, note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
