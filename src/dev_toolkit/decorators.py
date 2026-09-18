"""Decorators for function execution resilience."""

import functools
import time
from collections.abc import Callable
from typing import Any


def retry(
    max_attempts: int = 3,
    delay: float = 0.1,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[..., Any]:
    """Retry a function execution upon catching specified exceptions."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise
                    time.sleep(delay)

        return wrapper

    return decorator
