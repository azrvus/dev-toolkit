from __future__ import annotations

import re
from pathlib import Path
from typing import Any

__all__ = ["render_string", "render_template_file"]

_TOKEN_REGEX = re.compile(r"\{\{\s*([a-zA-Z0-9_.-]+)\s*\}\}")


def render_string(template: str, context: dict[str, Any]) -> str:
    """Render a template string by replacing {{ key }} tokens with context values."""

    def _replacer(match: re.Match[str]) -> str:
        key = match.group(1)
        return str(context.get(key, match.group(0)))

    return _TOKEN_REGEX.sub(_replacer, template)


def render_template_file(path: str | Path, context: dict[str, Any]) -> str:
    """Read a template file from disk and render it with the given context."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Template file not found: {file_path}")
    content = file_path.read_text(encoding="utf-8")
    return render_string(content, context)
