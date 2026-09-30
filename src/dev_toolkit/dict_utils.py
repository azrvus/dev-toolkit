"""Dictionary and sequence manipulation utilities."""

from collections.abc import Callable, Generator, Sequence
from typing import Any, TypeVar

T = TypeVar("T")


def get_in(data: dict[str, Any], keys: list[str], default: Any = None) -> Any:
    """Safely extract nested dictionary values using a key path."""
    curr = data
    for k in keys:
        if isinstance(curr, dict) and k in curr:
            curr = curr[k]
        else:
            return default
    return curr


def flatten_dict(
    d: dict[str, Any], parent_key: str = "", sep: str = "."
) -> dict[str, Any]:
    """Flatten nested dictionary keys into single string paths."""
    items: list[tuple[str, Any]] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def deep_merge(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge two dictionaries."""
    result = dict(dict1)
    for k, v in dict2.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def pick(d: dict[str, Any], keys: Sequence[str]) -> dict[str, Any]:
    """Return a dictionary containing only the specified keys."""
    key_set = set(keys)
    return {k: v for k, v in d.items() if k in key_set}


def omit(d: dict[str, Any], keys: Sequence[str]) -> dict[str, Any]:
    """Return a dictionary excluding the specified keys."""
    key_set = set(keys)
    return {k: v for k, v in d.items() if k not in key_set}


def filter_keys(
    d: dict[str, Any], predicate: Callable[[str, Any], bool]
) -> dict[str, Any]:
    """Recursively filter a dictionary by key-value predicate function."""
    res: dict[str, Any] = {}
    for k, v in d.items():
        if isinstance(v, dict):
            filtered_v = filter_keys(v, predicate)
            if predicate(k, filtered_v):
                res[k] = filtered_v
        elif predicate(k, v):
            res[k] = v
    return res


def chunk_list(items: Sequence[T], chunk_size: int) -> Generator[list[T], None, None]:
    """Yield successive fixed-size chunks from a sequence."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be strictly positive")
    for i in range(0, len(items), chunk_size):
        yield list(items[i : i + chunk_size])
