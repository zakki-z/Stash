"""
Unit tests for app/services/summarizer.py — auto_summarize()
Pure function: no DB, no HTTP client needed.
"""

from app.services.summarizer import auto_summarize


class TestAutoSummarize:
    def test_returns_first_two_sentences(self):
        result = auto_summarize("First sentence. Second sentence. Third sentence.")
        assert "First sentence." in result
        assert "Second sentence." in result
        assert "Third" not in result

    def test_single_sentence_content(self):
        assert auto_summarize("Only one sentence here") == "Only one sentence here"

    def test_no_punctuation_falls_back_to_truncation(self):
        text = "no punctuation at all so no split happens"
        result = auto_summarize(text)
        assert result
        assert len(result) <= 200

    def test_exclamation_mark_is_a_sentence_boundary(self):
        result = auto_summarize("Really? Yes! Third sentence.")
        assert "Really?" in result
        assert "Yes!" in result
        assert "Third" not in result

    def test_strips_leading_and_trailing_whitespace(self):
        result = auto_summarize("  Hello world.  Another sentence.  ")
        assert not result.startswith(" ")
        assert not result.endswith(" ")

    def test_max_sentences_param_is_respected(self):
        text = "One. Two. Three. Four."
        assert auto_summarize(text, max_sentences=1) == "One."
        assert "Two" not in auto_summarize(text, max_sentences=1)
