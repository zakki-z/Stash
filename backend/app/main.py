from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.models import Note  # noqa: F401 — ensures table is registered
from app.api.routers import notes, stats

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_TITLE, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes.router, prefix="/api")
app.include_router(stats.router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}
