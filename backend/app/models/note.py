from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.core.database import Base


class Category(str, enum.Enum):
    idea = "idea"
    article = "article"
    task = "task"
    quote = "quote"
    resource = "resource"
    journal = "journal"
    other = "other"


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[Category] = mapped_column(
        SAEnum(Category), default=Category.other, nullable=False
    )
    tags: Mapped[str | None] = mapped_column(String(500), nullable=True)  # comma-separated
    source_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    is_pinned: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
