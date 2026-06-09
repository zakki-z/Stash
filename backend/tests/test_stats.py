"""
Integration tests for GET /api/stats/
Covers: response shape, count correctness, live increment on create.
"""


class TestStats:
    def test_returns_200(self, client):
        assert client.get("/api/stats/").status_code == 200

    def test_response_has_expected_keys(self, client):
        data = client.get("/api/stats/").json()
        assert "total" in data
        assert "pinned" in data
        assert "by_category" in data

    def test_counts_are_non_negative(self, client):
        data = client.get("/api/stats/").json()
        assert data["total"] >= 0
        assert data["pinned"] >= 0

    def test_total_increments_on_create(self, client, make_note):
        before = client.get("/api/stats/").json()["total"]
        make_note(title="Stats total", content="counting")
        assert client.get("/api/stats/").json()["total"] == before + 1

    def test_pinned_increments_when_note_is_pinned(self, client, make_note):
        before = client.get("/api/stats/").json()["pinned"]
        make_note(title="Stats pinned", content="x", is_pinned=True)
        assert client.get("/api/stats/").json()["pinned"] == before + 1

    def test_pinned_unchanged_for_unpinned_note(self, client, make_note):
        before = client.get("/api/stats/").json()["pinned"]
        make_note(title="Not pinned", content="x", is_pinned=False)
        assert client.get("/api/stats/").json()["pinned"] == before

    def test_by_category_is_dict(self, client):
        assert isinstance(client.get("/api/stats/").json()["by_category"], dict)


class TestHealth:
    def test_health_endpoint_returns_ok(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}
