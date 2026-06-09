from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.note import Note, Category

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(func.count(Note.id)).scalar()
    pinned = db.query(func.count(Note.id)).filter(Note.is_pinned == True).scalar()

    by_category = (
        db.query(Note.category, func.count(Note.id))
        .group_by(Note.category)
        .all()
    )

    return {
        "total": total,
        "pinned": pinned,
        "by_category": {cat.value: count for cat, count in by_category},
    }
