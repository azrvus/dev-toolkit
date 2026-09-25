"""Dev Toolkit package initialization."""

from dev_toolkit.async_io import read_json_async, write_json_async
from dev_toolkit.cli import main, parse_args
from dev_toolkit.decorators import retry
from dev_toolkit.dict_utils import deep_merge, flatten_dict, get_in
from dev_toolkit.env import check_required_env, get_env_summary, mask_secret
from dev_toolkit.hash import get_file_hash, get_str_hash
from dev_toolkit.http import fetch_json
from dev_toolkit.io import ensure_dir, read_json, write_json
from dev_toolkit.logger import get_json_logger
from dev_toolkit.process import ProcessResult, run_command
from dev_toolkit.system import get_system_info, print_system_summary
from dev_toolkit.text import (
    camel_to_snake,
    normalize_whitespace,
    sanitize_filename,
    slugify,
    snake_to_camel,
    truncate_words,
)
from dev_toolkit.timer import Timer, timed

__version__ = "0.1.0"
__all__ = [
    "ProcessResult",
    "Timer",
    "camel_to_snake",
    "check_required_env",
    "deep_merge",
    "ensure_dir",
    "fetch_json",
    "flatten_dict",
    "get_env_summary",
    "get_file_hash",
    "get_in",
    "get_json_logger",
    "get_str_hash",
    "get_system_info",
    "main",
    "mask_secret",
    "normalize_whitespace",
    "parse_args",
    "print_system_summary",
    "read_json",
    "read_json_async",
    "retry",
    "run_command",
    "sanitize_filename",
    "slugify",
    "snake_to_camel",
    "timed",
    "truncate_words",
    "write_json",
    "write_json_async",
]
