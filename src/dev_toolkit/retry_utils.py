from __future__ import annotations

import asyncio
import inspect
import random
import time
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

__all__ = ["retry_with_backoff"]

F = TypeVar("F", bound=Callable[..., Any])


def _calculate_delay(
    attempt: int,
    base_delay: float,
    max_delay: float,
    backoff_factor: float,
    jitter: str,
) -> float:
    delay = min(max_delay, base_delay * (backoff_factor**attempt))

    if jitter == "full":
        return random.uniform(0, delay)
    elif jitter == "equal":
        return (delay / 2) + random.uniform(0, delay / 2)

    return delay


def retry_with_backoff(
    retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    jitter: str = "none",
    exceptions: tuple[type[BaseException], ...] = (Exception,),
    on_retry: Callable[[BaseException, int, float], None] | None = None,
) -> Callable[[F], F]:
    """Decorator to retry synchronous or asynchronous functions with exponential backoff and jitter."""

    def decorator(func: F) -> F:
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                for attempt in range(retries + 1):
                    try:
                        return await func(*args, **kwargs)
                    except exceptions as exc:
                        if attempt == retries:
                            raise

                        delay = _calculate_delay(
                            attempt,
                            base_delay,
                            max_delay,
                            backoff_factor,
                            jitter,
                        )
                        if on_retry:
                            on_retry(exc, attempt + 1, delay)

                        await asyncio.sleep(delay)

            return async_wrapper  # type: ignore[return-value]

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    if attempt == retries:
                        raise

                    delay = _calculate_delay(
                        attempt,
                        base_delay,
                        max_delay,
                        backoff_factor,
                        jitter,
                    )
                    if on_retry:
                        on_retry(exc, attempt + 1, delay)

                    time.sleep(delay)

        return sync_wrapper  # type: ignore[return-value]

    return decorator
