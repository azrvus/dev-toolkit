from dev_toolkit.events import EventEmitter


def test_event_emitter_basic():
    emitter = EventEmitter()
    results = []

    emitter.on("data", lambda x: results.append(x))
    emitter.emit("data", "hello")

    assert results == ["hello"]


def test_event_emitter_off():
    emitter = EventEmitter()
    results = []

    listener = lambda x: results.append(x)
    emitter.on("ping", listener)
    emitter.off("ping", listener)
    emitter.emit("ping", "test")

    assert results == []


def test_event_emitter_once():
    emitter = EventEmitter()
    counter = []

    emitter.once("click", lambda: counter.append(1))
    emitter.emit("click")
    emitter.emit("click")

    assert len(counter) == 1
