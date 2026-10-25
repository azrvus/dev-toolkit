from __future__ import annotations

__all__ = ["blue", "bold", "green", "red", "yellow"]

_RESET = "\033[0m"


def _colorize(text: str, code: str) -> str:
    return f"\033[{code}m{text}{_RESET}"


def red(text: str) -> str:
    """Format text with ANSI red color."""
    return _colorize(text, "31")


def green(text: str) -> str:
    """Format text with ANSI green color."""
    return _colorize(text, "32")


def yellow(text: str) -> str:
    """Format text with ANSI yellow color."""
    return _colorize(text, "33")


def blue(text: str) -> str:
    """Format text with ANSI blue color."""
    return _colorize(text, "34")


def bold(text: str) -> str:
    """Format text with ANSI bold style."""
    return _colorize(text, "1")
