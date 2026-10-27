from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import Any

__all__ = ["retry"]


def retry(
    exceptions: type[Exception] | tuple[type[Exception], ...] = Exception,
    retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator to retry a function upon raising specified exceptions."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    attempt += 1
                    if attempt >= retries:
                        raise
                    time.sleep(current_delay)
                    current_delay *= backoff
            return func(*args, **kwargs)

        return wrapper

    return decorator
