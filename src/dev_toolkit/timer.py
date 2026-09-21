"""High-precision execution benchmarking utilities."""

import functools
import time
from collections.abc import Callable
from typing import Any, Self


class Timer:
    """Context manager for measuring execution time in seconds."""

    def __init__(self) -> None:
        self.elapsed: float = 0.0
        self._start_time: float | None = None

    def __enter__(self) -> Self:
        self._start_time = time.perf_counter()
        return self

    def __exit__(self, *args: object) -> None:
        if self._start_time is not None:
            self.elapsed = time.perf_counter() - self._start_time


def timed(callback: Callable[[str, float], None] | None = None) -> Callable[..., Any]:
    """Decorator to measure and optionally report function execution duration."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed = time.perf_counter() - start
                if callback:
                    callback(func.__name__, elapsed)

        return wrapper

    return decorator
