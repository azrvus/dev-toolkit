"""Dev Toolkit package initialization."""

from dev_toolkit.env import check_required_env, get_env_summary, mask_secret
from dev_toolkit.io import ensure_dir, read_json, write_json
from dev_toolkit.system import get_system_info, print_system_summary
from dev_toolkit.text import normalize_whitespace, slugify, truncate_words

__version__ = "0.1.0"
__all__ = [
    "check_required_env",
    "ensure_dir",
    "get_env_summary",
    "get_system_info",
    "mask_secret",
    "normalize_whitespace",
    "print_system_summary",
    "read_json",
    "slugify",
    "truncate_words",
    "write_json",
]
