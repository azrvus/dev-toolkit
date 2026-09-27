"""Human-readable string formatting utilities."""


def format_bytes(size: float, binary: bool = True) -> str:
    """Format a byte count into a human-readable string (e.g., 1.50 MiB or 1.50 MB)."""
    if size < 0:
        raise ValueError("Size cannot be negative")

    factor = 1024.0 if binary else 1000.0
    units = (
        ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]
        if binary
        else ["B", "KB", "MB", "GB", "TB", "PB"]
    )

    current_size = float(size)
    for unit in units[:-1]:
        if current_size < factor:
            return f"{current_size:.2f} {unit}"
        current_size /= factor

    return f"{current_size:.2f} {units[-1]}"


def format_duration(seconds: float) -> str:
    """Format seconds into a compact human-readable duration (e.g., '2h 14m 30s')."""
    if seconds < 0:
        raise ValueError("Duration cannot be negative")

    if seconds == 0:
        return "0s"

    total = int(seconds)
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)

    parts: list[str] = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")

    return " ".join(parts)
