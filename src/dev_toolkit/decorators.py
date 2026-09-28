"""Function decorators for common runtime behavior modifications."""

import functools
import random
import time
from collections.abc import Callable
from typing import Any


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    on_retry: Callable[[Exception, int], None] | None = None,
) -> Callable[..., Any]:
    """Decorator to retry a function invocation with backoff and optional jitter."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    if delay < 0:
        raise ValueError("delay cannot be negative")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    if attempt == max_attempts:
                        raise

                    if on_retry:
                        on_retry(err, attempt)

                    sleep_time = current_delay
                    if jitter:
                        sleep_time = random.uniform(0, current_delay)

                    time.sleep(sleep_time)
                    current_delay *= backoff_factor

        return wrapper

    return decorator
