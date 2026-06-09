"""
Integration tests for DELETE /api/notes/{id}
Covers: successful deletion, post-delete 404, deleting a non-existent note.
"""


class TestDeleteNote:
    def test_delete_returns_204(self, client, make_note):
        note_id = make_note(title="Delete me", content="bye").json()["id"]
        assert client.delete(f"/api/notes/{note_id}").status_code == 204

    def test_deleted_note_is_no_longer_retrievable(self, client, make_note):
        note_id = make_note(title="Gone", content="poof").json()["id"]
        client.delete(f"/api/notes/{note_id}")
        assert client.get(f"/api/notes/{note_id}").status_code == 404

    def test_deleted_note_absent_from_list(self, client, make_note):
        note_id = make_note(title="WillVanish", content="bye").json()["id"]
        client.delete(f"/api/notes/{note_id}")
        ids = [n["id"] for n in client.get("/api/notes/").json()]
        assert note_id not in ids

    def test_nonexistent_id_returns_404(self, client):
        assert client.delete("/api/notes/999999").status_code == 404
