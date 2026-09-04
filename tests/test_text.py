"""Tests for text processing utilities."""

from dev_toolkit.text import normalize_whitespace, slugify, truncate_words


def test_slugify():
    assert slugify(" Hello World! ") == "hello-world"
    assert slugify("Python & Fast-API -- 2026") == "python-fast-api-2026"


def test_truncate_words():
    sample = "The quick brown fox jumps over the lazy dog"
    assert truncate_words(sample, 4) == "The quick brown fox..."
    assert truncate_words(sample, 10) == sample


def test_normalize_whitespace():
    raw_text = "  Lots   of    extra \n spaces \t here.  "
    assert normalize_whitespace(raw_text) == "Lots of extra spaces here."