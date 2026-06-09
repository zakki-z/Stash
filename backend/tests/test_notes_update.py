"""
Integration tests for PATCH /api/notes/{id}
Covers: field updates, summary regeneration, partial patch, 404 handling.
"""


class TestUpdateNote:
    def test_patch_title(self, client, make_note):
        note_id = make_note(title="Old Title", content="Content.").json()["id"]
        r = client.patch(f"/api/notes/{note_id}", json={"title": "New Title"})
        assert r.status_code == 200
        assert r.json()["title"] == "New Title"

    def test_patch_content_regenerates_summary(self, client, make_note):
        note_id = make_note(title="T", content="Original content.").json()["id"]
        data = client.patch(f"/api/notes/{note_id}", json={"content": "Updated content. New sentence."}).json()
        assert "Updated content." in data["summary"]
        assert "Original" not in data["summary"]

    def test_patch_pin_status(self, client, make_note):
        note_id = make_note(title="Pin me", content="x").json()["id"]
        assert client.patch(f"/api/notes/{note_id}", json={"is_pinned": True}).json()["is_pinned"] is True

    def test_patch_category(self, client, make_note):
        note_id = make_note(title="T", content="x").json()["id"]
        data = client.patch(f"/api/notes/{note_id}", json={"category": "journal"}).json()
        assert data["category"] == "journal"

    def test_partial_patch_preserves_untouched_fields(self, client, make_note):
        note_id = make_note(title="Keep Me", content="Keep this too.", tags="a,b").json()["id"]
        client.patch(f"/api/notes/{note_id}", json={"is_pinned": True})
        data = client.get(f"/api/notes/{note_id}").json()
        assert data["title"] == "Keep Me"
        assert data["tags"] == "a,b"

    def test_nonexistent_id_returns_404(self, client):
        assert client.patch("/api/notes/999999", json={"title": "x"}).status_code == 404
