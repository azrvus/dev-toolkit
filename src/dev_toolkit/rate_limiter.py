"""Rate limiting and execution throttling utilities."""

import functools
import threading
import time
from collections.abc import Callable
from typing import Any


class TokenBucket:
    """Thread-safe token bucket rate limiter."""

    def __init__(self, rate: float, capacity: float | None = None) -> None:
        """Initialize token bucket.

        :param rate: Tokens added per second.
        :param capacity: Maximum bucket capacity. Defaults to rate.
        """
        if rate <= 0:
            raise ValueError("Rate must be strictly positive")

        self.rate = float(rate)
        self.capacity = float(capacity) if capacity is not None else float(rate)

        if self.capacity <= 0:
            raise ValueError("Capacity must be strictly positive")

        self.tokens = self.capacity
        self.last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        delta = now - self.last_refill
        self.last_refill = now
        self.tokens = min(self.capacity, self.tokens + delta * self.rate)

    def consume(self, tokens: float = 1.0, block: bool = True) -> bool:
        """Consume a specified number of tokens from the bucket.

        If block is True, sleeps until sufficient tokens are available.
        Returns True if tokens were consumed, False otherwise.
        """
        if tokens <= 0:
            raise ValueError("Tokens to consume must be positive")

        while True:
            with self._lock:
                self._refill()
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return True

                if not block:
                    return False

                needed = tokens - self.tokens
                wait_time = needed / self.rate

            time.sleep(wait_time)


def rate_limit(
    rate: float, capacity: float | None = None, tokens: float = 1.0
) -> Callable[..., Any]:
    """Decorator to rate-limit function execution using a TokenBucket."""
    bucket = TokenBucket(rate=rate, capacity=capacity)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            bucket.consume(tokens=tokens, block=True)
            return func(*args, **kwargs)

        return wrapper

    return decorator
