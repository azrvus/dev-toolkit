"""Utilities for safe file operations, JSON processing, and directory management."""

import json
from pathlib import Path
from typing import Any


def ensure_dir(dir_path: str | Path) -> Path:
    """Ensure a directory exists, creating missing parent folders if needed."""
    path = Path(dir_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(file_path: str | Path) -> dict[str, Any]:
    """Safely load and parse a JSON file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Target JSON file does not exist: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(
    file_path: str | Path,
    data: Any,
    indent: int = 2,
    overwrite: bool = True,
) -> Path:
    """Write data to a JSON file, creating parent directories as necessary."""
    path = Path(file_path)
    if path.exists() and not overwrite:
        raise FileExistsError(
            f"File already exists and overwrite is set to False: {path}"
        )

    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)
    return path
