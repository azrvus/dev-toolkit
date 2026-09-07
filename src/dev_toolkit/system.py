"""System utility functions for environment inspection."""

import platform
import sys


def get_system_info() -> dict[str, str]:
    """Return key platform and Python environment metadata."""
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "python_version": sys.version.split()[0],
        "python_implementation": platform.python_implementation(),
    }


def print_system_summary() -> None:
    """Print formatted system information to stdout."""
    info = get_system_info()
    print("=== System Information ===")
    for key, val in info.items():
        formatted_key = key.replace("_", " ").title()
        print(f"{formatted_key:<22}: {val}")
