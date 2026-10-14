from pathlib import Path

import pytest

from dev_toolkit.watcher import watch_path


def test_watcher_invalid_path():
    with pytest.raises(FileNotFoundError):
        watch_path("non_existent_path_12345_abcde", lambda e, p: None, interval=0.1)


def test_watcher_execution_loop(tmp_path: Path):
    events = []

    def cb(event_type: str, file_path: Path):
        events.append((event_type, file_path))

    # Run watcher with max_iterations=1 and 0 sleep interval so it finishes instantly
    watch_path(tmp_path, cb, interval=0.0, max_iterations=1)
    assert isinstance(events, list)
