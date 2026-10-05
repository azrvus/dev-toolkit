"""Data validation utilities for standard formats and bounds."""

import ipaddress
import re
from urllib.parse import urlparse

_EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def is_email(value: str) -> bool:
    """Validate whether a string matches a standard email format."""
    if not isinstance(value, str):
        return False
    return bool(_EMAIL_REGEX.match(value.strip()))


def is_url(value: str, require_protocol: bool = True) -> bool:
    """Validate whether a string is a valid HTTP/HTTPS URL."""
    if not isinstance(value, str):
        return False

    target = value.strip()
    if not require_protocol and not target.startswith(("http://", "https://")):
        target = f"http://{target}"

    try:
        parsed = urlparse(target)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except (ValueError, AttributeError):
        return False


def is_ipv4(value: str) -> bool:
    """Check if a string is a valid IPv4 address."""
    if not isinstance(value, str):
        return False
    try:
        return ipaddress.ip_address(value.strip()).version == 4
    except ValueError:
        return False


def is_ipv6(value: str) -> bool:
    """Check if a string is a valid IPv6 address."""
    if not isinstance(value, str):
        return False
    try:
        return ipaddress.ip_address(value.strip()).version == 6
    except ValueError:
        return False


def in_range(
    value: float,
    min_val: float | None = None,
    max_val: float | None = None,
    inclusive: bool = True,
) -> bool:
    """Verify if a numeric value falls within lower and upper bounds."""
    if not isinstance(value, (int, float)):
        return False

    if inclusive:
        if min_val is not None and value < min_val:
            return False
        if max_val is not None and value > max_val:
            return False
    else:
        if min_val is not None and value <= min_val:
            return False
        if max_val is not None and value >= max_val:
            return False

    return True
