from __future__ import annotations

from typing import Any

__all__ = ["colorize", "format_table", "progress_bar"]

_COLORS: dict[str, str] = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m",
}


def colorize(text: str, color: str, bold: bool = False) -> str:
    """Wrap text in ANSI escape codes for colored terminal output."""
    color_code = _COLORS.get(color.lower(), "")
    if not color_code:
        return text

    bold_code = "\033[1m" if bold else ""
    return f"{bold_code}{color_code}{text}{_COLORS['reset']}"


def progress_bar(
    iteration: int,
    total: int,
    length: int = 30,
    fill: str = "█",
    empty: str = "-",
) -> str:
    """Generate a text-based progress bar string."""
    if total <= 0:
        return f"[{empty * length}] 0.0%"

    percent = min(100.0, max(0.0, (iteration / total) * 100))
    filled_length = int(length * iteration // total)
    filled_length = min(length, max(0, filled_length))

    bar = fill * filled_length + empty * (length - filled_length)
    return f"[{bar}] {percent:.1f}%"


def format_table(data: list[dict[str, Any]], headers: list[str] | None = None) -> str:
    """Format a list of dictionaries into an ASCII table string."""
    if not data:
        return ""

    cols = headers if headers else list(data[0].keys())

    # Calculate max column widths
    col_widths: dict[str, int] = {col: len(str(col)) for col in cols}
    for row in data:
        for col in cols:
            val_str = str(row.get(col, ""))
            col_widths[col] = max(col_widths[col], len(val_str))

    # Build header row and divider
    header_str = (
        "| " + " | ".join(str(col).ljust(col_widths[col]) for col in cols) + " |"
    )
    divider = "+-" + "-+-".join("-" * col_widths[col] for col in cols) + "-+"

    # Build data rows
    rows: list[str] = []
    for row in data:
        row_str = (
            "| "
            + " | ".join(str(row.get(col, "")).ljust(col_widths[col]) for col in cols)
            + " |"
        )
        rows.append(row_str)

    return "\n".join([divider, header_str, divider] + rows + [divider])
