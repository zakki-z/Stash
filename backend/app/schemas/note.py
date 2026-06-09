from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

from app.models.note import Category


class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    category: Category = Category.other
    tags: Optional[str] = None
    source_url: Optional[str] = None
    is_pinned: bool = False


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1)
    summary: Optional[str] = None
    category: Optional[Category] = None
    tags: Optional[str] = None
    source_url: Optional[str] = None
    is_pinned: Optional[bool] = None


class NoteOut(NoteBase):
    id: int
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
