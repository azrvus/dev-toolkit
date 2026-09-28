"""Tests for decorator utilities."""

from unittest.mock import MagicMock, call, patch

import pytest

from dev_toolkit.decorators import retry


def test_retry_success_first_attempt():
    mock_func = MagicMock(return_value="success")
    decorated = retry(max_attempts=3)(mock_func)

    assert decorated() == "success"
    assert mock_func.call_count == 1


def test_retry_eventual_success():
    mock_func = MagicMock(side_effect=[ValueError("fail"), ValueError("fail"), "ok"])
    decorated = retry(max_attempts=3, delay=0.01, exceptions=(ValueError,))(mock_func)

    assert decorated() == "ok"
    assert mock_func.call_count == 3


def test_retry_exceed_attempts():
    mock_func = MagicMock(side_effect=ValueError("persistent failure"))
    decorated = retry(max_attempts=2, delay=0.01, exceptions=(ValueError,))(mock_func)

    with pytest.raises(ValueError) as exc_info:
        decorated()

    assert "persistent failure" in str(exc_info.value)
    assert mock_func.call_count == 2


def test_retry_backoff_and_callback():
    failures = [ValueError("err1"), ValueError("err2"), "success"]
    mock_func = MagicMock(side_effect=failures)
    callback_mock = MagicMock()

    decorated = retry(
        max_attempts=3,
        delay=0.1,
        backoff_factor=2.0,
        jitter=False,
        exceptions=(ValueError,),
        on_retry=callback_mock,
    )(mock_func)

    with patch("time.sleep") as mock_sleep:
        res = decorated()

    assert res == "success"
    assert mock_func.call_count == 3
    assert callback_mock.call_count == 2
    # Sleep times: attempt 1 -> 0.1s, attempt 2 -> 0.2s
    mock_sleep.assert_has_calls([call(0.1), call(0.2)])


def test_retry_invalid_parameters():
    with pytest.raises(ValueError):
        retry(max_attempts=0)

    with pytest.raises(ValueError):
        retry(delay=-1.0)
