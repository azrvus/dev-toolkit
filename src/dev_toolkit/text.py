"""Text manipulation and normalization utilities."""

import re


def normalize_whitespace(text: str) -> str:
    """Replace multiple whitespace characters with a single space and strip leading/trailing spaces."""
    return re.sub(r"\s+", " ", text).strip()


def slugify(text: str) -> str:
    """Convert a string into a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return re.sub(r"^-+|-+$", "", text)


def truncate_words(text: str, max_words: int, suffix: str = "...") -> str:
    """Truncate text to a maximum number of words."""
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + suffix


def camel_to_snake(text: str) -> str:
    """Convert CamelCase or lowerCamelCase string to snake_case."""
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snake_to_camel(text: str, uppercase_first: bool = False) -> str:
    """Convert snake_case string to camelCase or PascalCase."""
    components = text.split("_")
    if uppercase_first:
        return "".join(x.title() for x in components)
    return components[0] + "".join(x.title() for x in components[1:])


def sanitize_filename(filename: str, replacement: str = "_") -> str:
    """Remove or replace characters that are invalid in file system paths."""
    cleaned = re.sub(r'[\\/*?:"<>|]', replacement, filename)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned
