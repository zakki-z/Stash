"""
Simple rule-based summarizer and categorizer.
Can be swapped for an LLM call without touching any other layer.
"""

from app.models.note import Category

_CATEGORY_KEYWORDS: dict[Category, list[str]] = {
    Category.idea: ["idea", "concept", "what if", "maybe", "brainstorm", "hypothesis"],
    Category.article: ["article", "read", "author", "published", "source", "blog", "post"],
    Category.task: ["todo", "task", "done", "fix", "implement", "build", "ship", "deadline"],
    Category.quote: ["said", "quote", '"', "—", "words of", "motto"],
    Category.resource: ["link", "http", "tutorial", "docs", "documentation", "reference", "learn"],
    Category.journal: ["today", "feeling", "I am", "I feel", "diary", "reflection", "grateful"],
}


def auto_summarize(content: str, max_sentences: int = 2) -> str:
    """Return the first `max_sentences` sentences as a naive summary."""
    import re

    sentences = re.split(r"(?<=[.!?])\s+", content.strip())
    summary_sentences = [s.strip() for s in sentences[:max_sentences] if s.strip()]
    return " ".join(summary_sentences) if summary_sentences else content[:200]


def auto_categorize(title: str, content: str) -> Category:
    """Score each category by keyword hits and return the best match."""
    text = (title + " " + content).lower()
    scores: dict[Category, int] = {cat: 0 for cat in _CATEGORY_KEYWORDS}

    for category, keywords in _CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[category] += 1

    best = max(scores, key=lambda c: scores[c])
    return best if scores[best] > 0 else Category.other
