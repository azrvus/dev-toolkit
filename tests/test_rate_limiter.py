"""Tests for rate limiting utilities."""

from unittest.mock import MagicMock, patch

import pytest
from dev_toolkit.rate_limiter import TokenBucket, rate_limit


def test_token_bucket_non_blocking_success():
    bucket = TokenBucket(rate=10, capacity=10)
    assert bucket.consume(tokens=5, block=False) is True


def test_token_bucket_non_blocking_insufficient_tokens():
    bucket = TokenBucket(rate=1, capacity=1)
    assert bucket.consume(tokens=1, block=False) is True
    assert bucket.consume(tokens=1, block=False) is False


def test_token_bucket_blocking_wait():
    current_time = 100.0

    def mock_monotonic():
        return current_time

    def mock_sleep(seconds):
        nonlocal current_time
        current_time += seconds

    with (
        patch(
            "dev_toolkit.rate_limiter.time.monotonic",
            side_effect=mock_monotonic,
        ),
        patch(
            "dev_toolkit.rate_limiter.time.sleep",
            side_effect=mock_sleep,
        ) as spy_sleep,
    ):
        bucket = TokenBucket(rate=10, capacity=10)
        assert bucket.consume(tokens=10, block=False) is True
        bucket.consume(tokens=5, block=True)
        spy_sleep.assert_called_once_with(0.5)


def test_token_bucket_invalid_params():
    with pytest.raises(ValueError):
        TokenBucket(rate=0)

    with pytest.raises(ValueError):
        TokenBucket(rate=10, capacity=-1)

    bucket = TokenBucket(rate=5)
    with pytest.raises(ValueError):
        bucket.consume(tokens=0)


def test_rate_limit_decorator():
    mock_func = MagicMock(return_value="done")
    decorated = rate_limit(rate=100)(mock_func)

    assert decorated() == "done"
    assert mock_func.call_count == 1