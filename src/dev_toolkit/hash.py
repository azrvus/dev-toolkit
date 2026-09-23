"""Hashing and checksum calculation utilities."""

import hashlib
from pathlib import Path


def get_str_hash(text: str, algorithm: str = "sha256") -> str:
    """Calculate the hexadecimal hash digest of a string."""
    try:
        hasher = hashlib.new(algorithm)
    except ValueError as err:
        raise ValueError(f"Unsupported hash algorithm: '{algorithm}'") from err

    hasher.update(text.encode("utf-8"))
    return hasher.hexdigest()


def get_file_hash(
    path: str | Path,
    algorithm: str = "sha256",
    chunk_size: int = 65536,
) -> str:
    """Calculate the hexadecimal hash digest of a file using chunked reading."""
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        hasher = hashlib.new(algorithm)
    except ValueError as err:
        raise ValueError(f"Unsupported hash algorithm: '{algorithm}'") from err

    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)

    return hasher.hexdigest()
