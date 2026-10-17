from __future__ import annotations

import json

os = __import__("os")
from pathlib import Path
from typing import Any

__all__ = ["ConfigManager"]


class ConfigManager:
    """A robust configuration manager supporting defaults, JSON file loading,

    and environment variable overrides with prefix matching.
    """

    def __init__(
        self,
        defaults: dict[str, Any] | None = None,
        config_path: str | Path | None = None,
        env_prefix: str | None = None,
    ) -> None:
        self._data: dict[str, Any] = defaults.copy() if defaults else {}
        self.config_path = Path(config_path) if config_path else None
        self.env_prefix = env_prefix

        if self.config_path and self.config_path.exists():
            self.load_file(self.config_path)

        if self.env_prefix:
            self.load_env(self.env_prefix)

    def load_file(self, path: str | Path) -> None:
        """Load and merge configuration from a JSON file."""
        file_path = Path(path)
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                content = json.load(f)
                if isinstance(content, dict):
                    self._data.update(content)

    def load_env(self, prefix: str) -> None:
        """Override configuration values using environment variables matching the prefix."""
        prefix_upper = prefix.upper() + "_"
        for key, val in os.environ.items():
            if key.startswith(prefix_upper):
                config_key = key[len(prefix_upper) :].lower()
                # Try parsing JSON primitives (bool, int, float), fallback to string
                try:
                    parsed_val = json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    parsed_val = val
                self._data[config_key] = parsed_val

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a configuration value by key."""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self._data[key] = value

    def to_dict(self) -> dict[str, Any]:
        """Return a copy of the full configuration dictionary."""
        return self._data.copy()

    def save(self, path: str | Path | None = None) -> None:
        """Save the current configuration to a JSON file."""
        target = Path(path) if path else self.config_path
        if not target:
            raise ValueError("No configuration file path specified.")
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=4)
