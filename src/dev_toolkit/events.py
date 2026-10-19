from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any

__all__ = ["EventEmitter"]


class EventEmitter:
    """A simple, robust event emitter (pub-sub) implementation."""

    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable[..., Any]]] = defaultdict(list)

    def on(self, event: str, listener: Callable[..., Any]) -> EventEmitter:
        """Register an event listener for a given event name."""
        self._listeners[event].append(listener)
        return self

    def off(self, event: str, listener: Callable[..., Any]) -> EventEmitter:
        """Remove a specific listener from an event name."""
        if event in self._listeners:
            try:
                self._listeners[event].remove(listener)
            except ValueError:
                pass
        return self

    def emit(self, event: str, *args: Any, **kwargs: Any) -> list[Any]:
        """Emit an event, invoking all registered listeners with provided arguments."""
        results = []
        for listener in list(self._listeners[event]):
            results.append(listener(*args, **kwargs))
        return results

    def once(self, event: str, listener: Callable[..., Any]) -> EventEmitter:
        """Register a listener that automatically unregisters after its first invocation."""

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            self.off(event, wrapper)
            return listener(*args, **kwargs)

        return self.on(event, wrapper)
