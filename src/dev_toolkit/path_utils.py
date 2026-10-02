"""Filesystem path and directory pattern utilities."""

from collections.abc import Generator, Sequence
from pathlib import Path


def get_dir_size(directory: str | Path) -> int:
    """Recursively calculate total size in bytes for a directory."""
    dir_path = Path(directory)
    if not dir_path.exists() or not dir_path.is_dir():
        raise ValueError(
            f"Directory '{directory}' does not exist or is not a directory"
        )

    return sum(
        f.stat().st_size
        for f in dir_path.rglob("*")
        if f.is_file() and not f.is_symlink()
    )


def replace_extension(path: str | Path, new_ext: str) -> Path:
    """Replace or set the file extension of a path."""
    p = Path(path)
    if not new_ext.startswith(".") and new_ext != "":
        new_ext = f".{new_ext}"
    return p.with_suffix(new_ext)


def find_files(
    directory: str | Path,
    patterns: Sequence[str] = ("*",),
    exclude_dirs: Sequence[str] = (".git", "__pycache__", ".venv"),
) -> Generator[Path, None, None]:
    """Yield files matching any pattern while avoiding specified directories."""
    dir_path = Path(directory)
    if not dir_path.exists() or not dir_path.is_dir():
        raise ValueError(
            f"Directory '{directory}' does not exist or is not a directory"
        )

    exclude_set = set(exclude_dirs)

    for item in dir_path.rglob("*"):
        if any(part in exclude_set for part in item.parts):
            continue
        if item.is_file() and any(item.match(pat) for pat in patterns):
            yield item


def get_tree(
    directory: str | Path,
    max_depth: int = 2,
    exclude_dirs: Sequence[str] = (".git", "__pycache__", ".venv"),
) -> str:
    """Generate a clean ASCII tree representation of a directory layout."""
    dir_path = Path(directory)
    if not dir_path.exists() or not dir_path.is_dir():
        raise ValueError(
            f"Directory '{directory}' does not exist or is not a directory"
        )

    lines = [f"{dir_path.name}/"]
    exclude_set = set(exclude_dirs)

    def _build_tree(current: Path, prefix: str, depth: int) -> None:
        if depth > max_depth:
            return
        entries = sorted(
            [e for e in current.iterdir() if e.name not in exclude_set],
            key=lambda x: (not x.is_dir(), x.name.lower()),
        )
        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "└── " if is_last else "├── "
            lines.append(
                f"{prefix}{connector}{entry.name}{'/' if entry.is_dir() else ''}"
            )
            if entry.is_dir():
                extension = "    " if is_last else "│   "
                _build_tree(entry, prefix + extension, depth + 1)

    _build_tree(dir_path, "", 1)
    return "\n".join(lines)
