"""Tests for decorator utilities."""

import pytest

from dev_toolkit.decorators import retry


def test_retry_success():
    call_count = 0

    @retry(max_attempts=3, delay=0.01)
    def successful_func():
        nonlocal call_count
        call_count += 1
        return "ok"

    assert successful_func() == "ok"
    assert call_count == 1


def test_retry_eventual_success():
    call_count = 0

    @retry(max_attempts=3, delay=0.01, exceptions=(ValueError,))
    def flaky_func():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise ValueError("Temporary failure")
        return "success"

    assert flaky_func() == "success"
    assert call_count == 2


def test_retry_max_attempts_exceeded():
    call_count = 0

    @retry(max_attempts=3, delay=0.01, exceptions=(RuntimeError,))
    def failing_func():
        nonlocal call_count
        call_count += 1
        raise RuntimeError("Persistent failure")

    with pytest.raises(RuntimeError) as exc_info:
        failing_func()

    assert "Persistent failure" in str(exc_info.value)
    assert call_count == 3
