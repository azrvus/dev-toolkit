from pathlib import Path

from dev_toolkit.config import ConfigManager


def test_config_defaults_and_get():
    cfg = ConfigManager(defaults={"host": "localhost", "port": 8080})
    assert cfg.get("host") == "localhost"
    assert cfg.get("port") == 8080
    assert cfg.get("missing", "default") == "default"


def test_config_file_loading(tmp_path: Path):
    config_file = tmp_path / "config.json"
    config_file.write_text('{"host": "127.0.0.1", "debug": true}', encoding="utf-8")

    cfg = ConfigManager(
        defaults={"host": "localhost", "debug": False}, config_path=config_file
    )
    assert cfg.get("host") == "127.0.0.1"
    assert cfg.get("debug") is True


def test_config_env_overrides(monkeypatch):
    monkeypatch.setenv("APP_PORT", "9000")
    monkeypatch.setenv("APP_HOST", "production-server")

    cfg = ConfigManager(defaults={"port": 8080, "host": "localhost"}, env_prefix="APP")
    assert cfg.get("port") == 9000
    assert cfg.get("host") == "production-server"
