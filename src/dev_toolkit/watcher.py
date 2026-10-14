from __future__ import annotations

import time
from collections.abc import Callable
from pathlib import Path

__all__ = ["watch_path"]


def watch_path(
    path: str | Path,
    callback: Callable[[str, Path], None],
    interval: float = 1.0,
    extensions: list[str] | None = None,
    max_iterations: int | None = None,
) -> None:
    """Watch a file or directory for modifications, creations, or deletions.

    Polls the path at the specified interval and invokes the callback function
    with an event type ('created', 'modified', 'deleted') and the path.
    """
    target = Path(path)
    if not target.exists():
        raise FileNotFoundError(f"Target path does not exist: {target}")

    known_files: dict[Path, float] = {}

    def _snapshot(p: Path) -> dict[Path, float]:
        snapshot: dict[Path, float] = {}
        if p.is_file():
            if extensions is None or p.suffix in extensions:
                snapshot[p] = p.stat().st_mtime
        elif p.is_dir():
            for child in p.rglob("*"):
                if child.is_file() and (
                    extensions is None or child.suffix in extensions
                ):
                    snapshot[child] = child.stat().st_mtime
        return snapshot

    known_files = _snapshot(target)

    iterations = 0
    try:
        while max_iterations is None or iterations < max_iterations:
            current_files = _snapshot(target) if target.exists() else {}

            for fpath, mtime in current_files.items():
                if fpath not in known_files:
                    callback("created", fpath)
                elif mtime != known_files[fpath]:
                    callback("modified", fpath)

            for fpath in known_files:
                if fpath not in current_files:
                    callback("deleted", fpath)

            known_files = current_files
            iterations += 1

            if max_iterations is not None and iterations >= max_iterations:
                break

            time.sleep(interval)
    except KeyboardInterrupt:
        pass
