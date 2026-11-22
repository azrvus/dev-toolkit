"""Streaming validation of local UTF-8 evaluation datasets."""

import json
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class JsonlIssue:
    """An actionable error without dataset contents; line 0 denotes file errors."""

    line: int
    message: str


def _reject_constant(value: str) -> None:
    raise ValueError("nonstandard JSON constant")


def validate_jsonl(
    path: str | Path, required_keys: Iterable[str] = ()
) -> Iterator[JsonlIssue]:
    """Yield errors reading one line at a time, without retaining records.

    Blank lines and empty files are invalid. Keys are top-level and presence-only;
    null values are allowed. Missing/unreadable files and invalid UTF-8 yield errors.
    JSON must be strict (NaN and Infinity are rejected). No record text is returned.
    """
    keys = tuple(dict.fromkeys(required_keys))
    line_number = 0
    try:
        with Path(path).open("rb") as stream:
            for line_number, raw in enumerate(stream, 1):
                try:
                    line = raw.decode("utf-8")
                except UnicodeDecodeError:
                    yield JsonlIssue(line_number, "invalid UTF-8; save as UTF-8")
                    continue
                if not line.strip():
                    yield JsonlIssue(line_number, "blank line; remove it or add an object")
                    continue
                try:
                    record = json.loads(line, parse_constant=_reject_constant)
                except json.JSONDecodeError as error:
                    yield JsonlIssue(
                        line_number, f"invalid JSON at column {error.colno}; check syntax"
                    )
                    continue
                except (ValueError, RecursionError):
                    yield JsonlIssue(line_number, "invalid JSON; use finite, nested JSON")
                    continue
                if not isinstance(record, dict):
                    yield JsonlIssue(line_number, "expected a JSON object")
                    continue
                missing = [key for key in keys if key not in record]
                if missing:
                    yield JsonlIssue(line_number, f"missing required keys: {missing!r}")
        if line_number == 0:
            yield JsonlIssue(0, "empty file; add at least one JSON object")
    except OSError:
        yield JsonlIssue(0, "cannot read input; check path and permissions")
