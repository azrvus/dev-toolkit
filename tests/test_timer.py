"""Tests for timer and benchmarking utilities."""

import time

from dev_toolkit.timer import Timer, timed


def test_timer_context_manager():
    with Timer() as t:
        time.sleep(0.01)

    assert t.elapsed >= 0.009  # Account for minor clock drift


def test_timed_decorator():
    reported_name = None
    reported_time = None

    def sample_callback(name: str, duration: float) -> None:
        nonlocal reported_name, reported_time
        reported_name = name
        reported_time = duration

    @timed(callback=sample_callback)
    def compute_heavy_task():
        time.sleep(0.01)
        return "done"

    result = compute_heavy_task()
    assert result == "done"
    assert reported_name == "compute_heavy_task"
    assert reported_time is not None
    assert reported_time >= 0.009
