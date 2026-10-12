from __future__ import annotations

from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from typing import Any, TypeVar

__all__ = ["run_parallel", "run_parallel_processes"]

T = TypeVar("T")
R = TypeVar("R")


def run_parallel(
    func: Callable[[T], R],
    items: list[T],
    max_workers: int | None = None,
    timeout: float | None = None,
) -> list[R | Exception]:
    """Execute a function across a list of items in parallel using threads.

    Returns a list of results or Exceptions if an item fails.
    """
    results: list[Any] = [None] * len(items)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(func, item): i for i, item in enumerate(items)
        }
        for future in as_completed(future_to_index, timeout=timeout):
            index = future_to_index[future]
            try:
                results[index] = future.result()
            except Exception as exc:  # noqa: BLE001
                results[index] = exc
    return results


def run_parallel_processes(
    func: Callable[[T], R],
    items: list[T],
    max_workers: int | None = None,
    timeout: float | None = None,
) -> list[R | Exception]:
    """Execute a function across a list of items in parallel using processes.

    Returns a list of results or Exceptions if an item fails.
    """
    results: list[Any] = [None] * len(items)
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(func, item): i for i, item in enumerate(items)
        }
        for future in as_completed(future_to_index, timeout=timeout):
            index = future_to_index[future]
            try:
                results[index] = future.result()
            except Exception as exc:  # noqa: BLE001
                results[index] = exc
    return results
