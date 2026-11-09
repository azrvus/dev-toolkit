import pytest

from dev_toolkit.env_validator import get_env_or_raise, validate_env


def test_get_env_success(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "hello")
    assert get_env_or_raise("TEST_VAR") == "hello"


def test_get_env_missing(monkeypatch):
    monkeypatch.delenv("TEST_VAR", raising=False)
    with pytest.raises(ValueError, match="TEST_VAR"):
        get_env_or_raise("TEST_VAR")


def test_validate_env_success(monkeypatch):
    monkeypatch.setenv("HOST", "localhost")
    monkeypatch.setenv("PORT", "8080")
    result = validate_env(["HOST", "PORT"])
    assert result == {"HOST": "localhost", "PORT": "8080"}


def test_validate_env_missing(monkeypatch):
    monkeypatch.delenv("PORT", raising=False)
    monkeypatch.setenv("HOST", "localhost")
    with pytest.raises(ValueError, match="PORT"):
        validate_env(["HOST", "PORT"])
