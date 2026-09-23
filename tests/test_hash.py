"""Tests for hashing utilities."""

import pytest

from dev_toolkit.hash import get_file_hash, get_str_hash


def test_get_str_hash():
    # Known SHA-256 hash for "hello world"
    expected = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    assert get_str_hash("hello world", algorithm="sha256") == expected


def test_get_str_hash_md5():
    # Known MD5 hash for "hello world"
    expected = "5eb63bbbe01eeed093cb22bb8f5acdc3"
    assert get_str_hash("hello world", algorithm="md5") == expected


def test_get_str_hash_invalid_algo():
    with pytest.raises(ValueError) as exc_info:
        get_str_hash("test", algorithm="invalid_algo")
    assert "Unsupported hash algorithm" in str(exc_info.value)


def test_get_file_hash(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("hello world", encoding="utf-8")

    expected = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    assert get_file_hash(file_path, algorithm="sha256") == expected


def test_get_file_hash_not_found():
    with pytest.raises(FileNotFoundError):
        get_file_hash("non_existent_file.txt")
