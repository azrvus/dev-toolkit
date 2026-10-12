from dev_toolkit.concurrency import run_parallel, run_parallel_processes


def square(x: int) -> int:
    return x * x


def fail_on_even(x: int) -> int:
    if x % 2 == 0:
        raise ValueError("Even number error")
    return x * 2


def test_run_parallel_success():
    items = [1, 2, 3, 4]
    results = run_parallel(square, items)
    assert results == [1, 4, 9, 16]


def test_run_parallel_with_exceptions():
    items = [1, 2, 3]
    results = run_parallel(fail_on_even, items)
    assert results[0] == 2
    assert isinstance(results[1], ValueError)
    assert results[2] == 6


def test_run_parallel_processes_success():
    items = [5, 6, 7]
    results = run_parallel_processes(square, items)
    assert results == [25, 36, 49]
