"""Tests for lightweight data validation utilities."""

from dev_toolkit.validators import (
    in_range,
    is_email,
    is_ipv4,
    is_ipv6,
    is_url,
)


def test_is_email():
    assert is_email("user@example.com") is True
    assert is_email("user.name+tag@domain.co.uk") is True
    assert is_email("invalid-email") is False
    assert is_email("@domain.com") is False
    assert is_email(12345) is False


def test_is_url():
    assert is_url("https://example.com/path?query=1") is True
    assert is_url("http://localhost:8080") is True
    assert is_url("example.com", require_protocol=False) is True
    assert is_url("ftp://example.com") is False
    assert is_url("not a url") is False


def test_is_ipv4():
    assert is_ipv4("192.168.1.1") is True
    assert is_ipv4("127.0.0.1") is True
    assert is_ipv4("256.0.0.1") is False
    assert is_ipv4("2001:db8::1") is False


def test_is_ipv6():
    assert is_ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334") is True
    assert is_ipv6("::1") is True
    assert is_ipv6("192.168.1.1") is False
    assert is_ipv6("invalid_ip") is False


def test_in_range():
    assert in_range(5, min_val=1, max_val=10) is True
    assert in_range(1, min_val=1, inclusive=True) is True
    assert in_range(1, min_val=1, inclusive=False) is False
    assert in_range(10.5, min_val=0.0, max_val=10.0) is False
    assert in_range("5", min_val=1) is False
