"""
Shared test fixtures.
The database module is patched here — before any app import — so every test
module gets the same in-memory SQLite instance automatically.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# ── Patch DB before any app code is imported ────────────────────────────────
import app.core.database as _db_module
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_DB_URI = "sqlite:///file::memory:?uri=true&cache=shared"
_test_engine = create_engine(
    _DB_URI,
    connect_args={"check_same_thread": False, "uri": True},
)
_TestSession = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)

_db_module.engine = _test_engine
_db_module.SessionLocal = _TestSession

# ── Now safe to import app ───────────────────────────────────────────────────
import pytest
from fastapi.testclient import TestClient
from app.core.database import Base, get_db
from main import app

Base.metadata.create_all(bind=_test_engine)


def _override_get_db():
    db = _TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture
def make_note(client):
    """Factory: POST a note with sensible defaults; kwargs override any field."""
    def _make(title="Test Note", content="Some content here.", **kwargs):
        return client.post("/api/notes/", json={"title": title, "content": content, **kwargs})
    return _make
