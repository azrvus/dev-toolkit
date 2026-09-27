"""Tests for human-readable formatting utilities."""

import pytest

from dev_toolkit.formatters import format_bytes, format_duration


def test_format_bytes_binary():
    assert format_bytes(500) == "500.00 B"
    assert format_bytes(1024) == "1.00 KiB"
    assert format_bytes(1048576) == "1.00 MiB"
    assert format_bytes(1572864) == "1.50 MiB"


def test_format_bytes_decimal():
    assert format_bytes(1000, binary=False) == "1.00 KB"
    assert format_bytes(1000000, binary=False) == "1.00 MB"


def test_format_bytes_negative():
    with pytest.raises(ValueError):
        format_bytes(-10)


def test_format_duration():
    assert format_duration(0) == "0s"
    assert format_duration(45) == "45s"
    assert format_duration(90) == "1m 30s"
    assert format_duration(8070) == "2h 14m 30s"


def test_format_duration_negative():
    with pytest.raises(ValueError):
        format_duration(-5)
