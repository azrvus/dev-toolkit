"""Utilities for text normalization, slug generation, and string truncation."""

import re


def slugify(value: str) -> str:
    """Convert a string into a clean, URL-safe slug."""
    value = value.lower().strip()
    # Remove non-alphanumeric characters (except spaces and hyphens)
    value = re.sub(r"[^\w\s-]", "", value)
    # Replace whitespace and repeated hyphens with a single hyphen
    value = re.sub(r"[\s_-]+", "-", value)
    return value.strip("-")


def truncate_words(text: str, max_words: int, suffix: str = "...") -> str:
    """Truncate text to a maximum number of words without cutting words in half."""
    words = text.strip().split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + suffix


def normalize_whitespace(text: str) -> str:
    """Collapse multiple spaces, tabs, and newlines into a single space."""
    return " ".join(text.split())
