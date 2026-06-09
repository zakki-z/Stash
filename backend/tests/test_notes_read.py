"""
Integration tests for GET /api/notes/ and GET /api/notes/{id}
Covers: retrieval by ID, 404 handling, list, search, category filter, pinned filter.
"""


class TestGetNoteById:
    def test_returns_200_and_correct_id(self, client, make_note):
        note_id = make_note(title="Readable").json()["id"]
        r = client.get(f"/api/notes/{note_id}")
        assert r.status_code == 200
        assert r.json()["id"] == note_id

    def test_nonexistent_id_returns_404(self, client):
        assert client.get("/api/notes/999999").status_code == 404


class TestListNotes:
    def test_returns_200_and_array(self, client):
        r = client.get("/api/notes/")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_search_matches_title(self, client, make_note):
        make_note(title="UniqueSearchTitle42", content="irrelevant")
        titles = [n["title"] for n in client.get("/api/notes/?search=UniqueSearchTitle42").json()]
        assert "UniqueSearchTitle42" in titles

    def test_search_matches_content(self, client, make_note):
        make_note(title="Plain", content="UniqueContentPhrase99")
        contents = [n["content"] for n in client.get("/api/notes/?search=UniqueContentPhrase99").json()]
        assert any("UniqueContentPhrase99" in c for c in contents)

    def test_search_matches_tags(self, client, make_note):
        make_note(title="Tagged", content="x", tags="UniqueTag55")
        tags = [n["tags"] for n in client.get("/api/notes/?search=UniqueTag55").json()]
        assert any(t and "UniqueTag55" in t for t in tags)

    def test_category_filter_returns_only_matching(self, client, make_note):
        make_note(title="A task note", content="todo implement", category="task")
        results = client.get("/api/notes/?category=task").json()
        assert results
        assert all(n["category"] == "task" for n in results)

    def test_pinned_only_filter(self, client, make_note):
        make_note(title="Unpinned", content="regular")
        make_note(title="Pinned", content="important", is_pinned=True)
        results = client.get("/api/notes/?pinned_only=true").json()
        assert results
        assert all(n["is_pinned"] for n in results)

    def test_invalid_category_returns_422(self, client):
        assert client.get("/api/notes/?category=nonexistent").status_code == 422
