from __future__ import annotations

import itertools
import sys
import threading
import time
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from types import TracebackType

__all__ = ["Spinner"]

_SPINNER_STYLES: dict[str, list[str]] = {
    "dots": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
    "line": ["-|", "\\", "|", "/"],
    "block": ["█", "▓", "▒", "░"],
}


class Spinner:
    """A thread-safe terminal loading spinner context manager."""

    def __init__(
        self,
        text: str = "Loading...",
        style: str = "dots",
        delay: float = 0.1,
        stream: Any = sys.stdout,
    ) -> None:
        self.text = text
        self.delay = delay
        self.stream = stream
        self.frames = _SPINNER_STYLES.get(style, _SPINNER_STYLES["dots"])
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def _spin(self) -> None:
        for frame in itertools.cycle(self.frames):
            if self._stop_event.is_set():
                break
            sys.stdout.write(f"\r{frame} {self.text}")
            sys.stdout.flush()
            time.sleep(self.delay)

    def start(self) -> Self:
        """Start the spinner animation thread."""
        if self._thread is not None and self._thread.is_alive():
            return self

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()
        return self

    def stop(self, final_text: str | None = None) -> None:
        """Stop the spinner animation and clear or finalize the line."""
        if self._thread is None:
            return

        self._stop_event.set()
        self._thread.join()
        self._thread = None

        # Clear line and print final message if provided
        sys.stdout.write("\r\033[K")
        if final_text:
            self.stream.write(f"{final_text}\n")
        self.stream.flush()

    def update_text(self, text: str) -> None:
        """Update the message displayed next to the spinner."""
        self.text = text

    def __enter__(self) -> Self:
        return self.start()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            self.stop("❌ Failed!")
        else:
            self.stop("✔ Done!")
