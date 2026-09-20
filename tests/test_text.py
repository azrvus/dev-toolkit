"""Tests for text utilities."""

from dev_toolkit.text import (
    camel_to_snake,
    normalize_whitespace,
    sanitize_filename,
    slugify,
    snake_to_camel,
    truncate_words,
)


def test_normalize_whitespace():
    assert normalize_whitespace("  hello   world  \n") == "hello world"


def test_slugify():
    assert slugify(" Hello World! ") == "hello-world"
    assert slugify("Python & FastApi") == "python-fastapi"


def test_truncate_words():
    text = "The quick brown fox jumps over the lazy dog"
    assert truncate_words(text, 4) == "The quick brown fox..."
    assert truncate_words(text, 10) == text


def test_camel_to_snake():
    assert camel_to_snake("CamelCase") == "camel_case"
    assert camel_to_snake("lowerCamelCase") == "lower_camel_case"
    assert camel_to_snake("HTTPResponseCode") == "http_response_code"


def test_snake_to_camel():
    assert snake_to_camel("snake_case") == "snakeCase"
    assert snake_to_camel("snake_case", uppercase_first=True) == "SnakeCase"


def test_sanitize_filename():
    assert sanitize_filename("invalid/file:name?.txt") == "invalid_file_name_.txt"
    assert sanitize_filename("  clean  name.pdf  ") == "clean name.pdf"
