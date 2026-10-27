import pytest

from dev_toolkit.retry import retry


def test_retry_success_on_first_try():
    @retry(retries=3, delay=0.01)
    def always_succeeds():
        return "ok"

    assert always_succeeds() == "ok"


def test_retry_eventual_success():
    attempts = 0

    @retry(retries=3, delay=0.01)
    def flaky():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("fail")
        return "success"

    assert flaky() == "success"
    assert attempts == 3


def test_retry_exhausted():
    @retry(retries=2, delay=0.01)
    def always_fails():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        always_fails()
