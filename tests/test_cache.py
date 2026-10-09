import time

from dev_toolkit.cache import ttl_cache


def test_ttl_cache_hit_and_miss():
    calls = 0

    @ttl_cache(ttl=10.0, maxsize=10)
    def add(a: int, b: int) -> int:
        nonlocal calls
        calls += 1
        return a + b

    assert add(1, 2) == 3
    assert calls == 1
    assert add(1, 2) == 3
    assert calls == 1  # Cache hit

    info = add.cache_info()
    assert info.hits == 1
    assert info.misses == 1
    assert info.currsize == 1


def test_ttl_cache_expiration():
    calls = 0

    @ttl_cache(ttl=0.1, maxsize=10)
    def getValue() -> int:
        nonlocal calls
        calls += 1
        return 42

    assert getValue() == 42
    assert calls == 1

    time.sleep(0.15)

    assert getValue() == 42
    assert calls == 2  # Expired, recalculated


def test_ttl_cache_maxsize_eviction():
    @ttl_cache(ttl=10.0, maxsize=2)
    def identity(x: int) -> int:
        return x

    identity(1)
    identity(2)
    assert identity.cache_info().currsize == 2

    identity(3)  # Evicts 1
    assert identity.cache_info().currsize == 2

    identity.cache_clear()
    assert identity.cache_info().currsize == 0
    assert identity.cache_info().hits == 0
