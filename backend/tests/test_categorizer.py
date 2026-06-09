"""
Unit tests for app/services/summarizer.py — auto_categorize()
Pure function: no DB, no HTTP client needed.
"""

from app.services.summarizer import auto_categorize
from app.models.note import Category


class TestAutoCategorize:
    def test_detects_task(self):
        assert auto_categorize("Fix the login bug", "todo: implement oauth") == Category.task

    def test_detects_idea(self):
        assert auto_categorize("New idea", "what if we brainstorm a new concept") == Category.idea

    def test_detects_resource(self):
        assert auto_categorize("Useful link", "http://docs.example.com tutorial") == Category.resource

    def test_detects_journal(self):
        assert auto_categorize("Daily diary", "today I am feeling grateful reflection") == Category.journal

    def test_detects_quote(self):
        assert auto_categorize("Favourite quote", 'He said "to be or not to be"') == Category.quote

    def test_detects_article(self):
        assert auto_categorize("Weekend read", "author published blog post source") == Category.article

    def test_no_keywords_returns_other(self):
        assert auto_categorize("xyz", "xyz") == Category.other

    def test_title_keywords_also_count(self):
        # keyword "idea" is in the title only
        assert auto_categorize("idea", "") == Category.idea

    def test_highest_score_wins(self):
        # task keywords dominate
        result = auto_categorize("todo fix ship build implement", "task task task")
        assert result == Category.task
