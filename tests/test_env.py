"""Tests for environment variable utilities."""

from dev_toolkit.env import check_required_env, get_env_summary, mask_secret


def test_mask_secret():
    # 18 chars total: 14 asterisks + '1234'
    assert mask_secret("supersecretkey1234") == "**************1234"
    assert mask_secret("123") == "***"


def test_check_required_env(monkeypatch):
    monkeypatch.setenv("TEST_VAR_A", "1")
    missing = check_required_env(["TEST_VAR_A", "TEST_VAR_B"])
    assert missing == ["TEST_VAR_B"]


def test_get_env_summary(monkeypatch):
    monkeypatch.setenv("DEBUG", "true")
    summary = get_env_summary()
    assert summary["DEBUG"] is True