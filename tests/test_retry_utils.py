import asyncio

import pytest

from dev_toolkit.retry_utils import retry_with_backoff


def test_sync_retry_success_after_failure():
    attempts = 0

    @retry_with_backoff(retries=3, base_delay=0.01, backoff_factor=1.0)
    def flaky_fn() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("Temporary glitch")
        return "success"

    assert flaky_fn() == "success"
    assert attempts == 3


def test_sync_retry_exceeds_max_attempts():
    attempts = 0

    @retry_with_backoff(retries=2, base_delay=0.01, exceptions=(ValueError,))
    def failing_fn() -> None:
        nonlocal attempts
        attempts += 1
        raise ValueError("Persistent error")

    with pytest.raises(ValueError, match="Persistent error"):
        failing_fn()

    assert attempts == 3


def test_async_retry_success():
    attempts = 0

    @retry_with_backoff(retries=2, base_delay=0.01)
    async def async_flaky() -> int:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise RuntimeError("Async error")
        return 100

    res = asyncio.run(async_flaky())
    assert res == 100
    assert attempts == 2


def test_retry_on_retry_callback():
    retried_attempts = []

    def callback(exc: BaseException, attempt: int, delay: float) -> None:
        retried_attempts.append((attempt, delay))

    @retry_with_backoff(
        retries=2,
        base_delay=0.01,
        on_retry=callback,
        jitter="none",
    )
    def fail_twice() -> None:
        raise KeyError("Missing key")

    with pytest.raises(KeyError):
        fail_twice()

    assert len(retried_attempts) == 2
    assert retried_attempts[0][0] == 1
    assert retried_attempts[1][0] == 2
