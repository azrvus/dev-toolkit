from __future__ import annotations

import re

__all__ = ["capitalize_words", "normalize_spaces", "to_snake_case"]


def normalize_spaces(text: str) -> str:
    """Remove extra whitespace from text and normalize inner spacing."""
    return " ".join(text.split())


def capitalize_words(text: str) -> str:
    """Capitalize the first letter of each word in a string."""
    return " ".join(word.capitalize() for word in text.split())


def to_snake_case(text: str) -> str:
    """Convert a camelCase or PascalCase string into snake_case."""
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
