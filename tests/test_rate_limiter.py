from unittest.mock import patch
import pytest
from dev_toolkit.rate_limiter import TokenBucket, rate_limit


def test_token_bucket_blocking_wait():
    current_time = 100.0

    def mock_monotonic():
        return current_time

    def mock_sleep(seconds):
        nonlocal current_time
        current_time += seconds

    # Target the import inside dev_toolkit.rate_limiter
    with patch("dev_toolkit.rate_limiter.time.monotonic", side_effect=mock_monotonic), \
         patch("dev_toolkit.rate_limiter.time.sleep", side_effect=mock_sleep) as spy_sleep:
        
        # Instantiate inside the patch block so bucket.last_refill starts at 100.0
        bucket = TokenBucket(rate=10, capacity=10)
        
        # Drain the bucket completely
        assert bucket.consume(tokens=10, block=False) is True

        # Consuming 5 tokens at rate=10/s requires a 0.5s wait
        bucket.consume(tokens=5, block=True)

        # Verify sleep was called with expected duration
        spy_sleep.assert_called_once_with(0.5)