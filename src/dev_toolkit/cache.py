from __future__ import annotations

import time
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any, TypeVar

__all__ = ["CacheInfo", "ttl_cache"]

F = TypeVar("F", bound=Callable[..., Any])


@dataclass(frozen=True)
class CacheInfo:
    hits: int
    misses: int
    maxsize: int | None
    currsize: int


@dataclass
class _CacheEntry:
    value: Any
    expires_at: float


def ttl_cache(ttl: float = 60.0, maxsize: int | None = 128) -> Callable[[F], F]:
    """Decorator to cache function results with a TTL and maxsize (LRU)."""

    def decorator(func: F) -> F:
        cache: OrderedDict[tuple[Any, ...], _CacheEntry] = OrderedDict()
        hits = 0
        misses = 0

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal hits, misses

            # Make kwargs hashable by sorting keys
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()

            if key in cache:
                entry = cache[key]
                if now < entry.expires_at:
                    hits += 1
                    cache.move_to_end(key)
                    return entry.value
                else:
                    # Expired entry
                    del cache[key]

            misses += 1
            result = func(*args, **kwargs)
            expires_at = now + ttl

            # Evict LRU item if maxsize is reached
            if maxsize is not None and len(cache) >= maxsize > 0:
                cache.popitem(last=False)

            if maxsize is None or maxsize > 0:
                cache[key] = _CacheEntry(value=result, expires_at=expires_at)

            return result

        def cache_info() -> CacheInfo:
            # Clean expired items count check
            return CacheInfo(
                hits=hits,
                misses=misses,
                maxsize=maxsize,
                currsize=len(cache),
            )

        def cache_clear() -> None:
            nonlocal hits, misses
            cache.clear()
            hits = 0
            misses = 0

        wrapper.cache_info = cache_info  # type: ignore[attr-defined]
        wrapper.cache_clear = cache_clear  # type: ignore[attr-defined]

        return wrapper  # type: ignore[return-value]

    return decorator
