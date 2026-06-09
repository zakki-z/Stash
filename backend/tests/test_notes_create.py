"""
Integration tests for POST /api/notes/
Covers: request validation, response shape, auto-summarization, auto-categorization.
"""


class TestCreateNote:
    def test_returns_201(self, make_note):
        assert make_note().status_code == 201

    def test_response_contains_id_and_submitted_fields(self, make_note):
        data = make_note(title="My Note", content="Hello world.").json()
        assert "id" in data
        assert data["title"] == "My Note"
        assert data["content"] == "Hello world."

    def test_summary_is_auto_generated_on_create(self, make_note):
        data = make_note(content="Auto-summary test. Second sentence. Third.").json()
        assert data["summary"] is not None
        assert "Auto-summary test." in data["summary"]

    def test_auto_categorization_overrides_default_other(self, make_note):
        data = make_note(title="todo fix bug", content="implement the task deadline").json()
        assert data["category"] != "other"

    def test_explicit_category_is_not_overridden(self, make_note):
        data = make_note(title="Weekly read", content="author blog post", category="article").json()
        assert data["category"] == "article"

    def test_is_pinned_defaults_to_false(self, make_note):
        assert make_note().json()["is_pinned"] is False

    def test_is_pinned_stored_when_true(self, make_note):
        assert make_note(is_pinned=True).json()["is_pinned"] is True

    def test_optional_tags_stored(self, make_note):
        assert make_note(tags="ml,python").json()["tags"] == "ml,python"

    def test_optional_source_url_stored(self, make_note):
        url = "https://example.com/article"
        assert make_note(source_url=url).json()["source_url"] == url

    def test_missing_title_returns_422(self, client):
        assert client.post("/api/notes/", json={"content": "no title"}).status_code == 422

    def test_empty_content_returns_422(self, client):
        assert client.post("/api/notes/", json={"title": "T", "content": ""}).status_code == 422

    def test_missing_content_returns_422(self, client):
        assert client.post("/api/notes/", json={"title": "T"}).status_code == 422
