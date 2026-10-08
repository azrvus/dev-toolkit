from dev_toolkit.cli_formatters import colorize, format_table, progress_bar


def test_colorize_valid():
    output = colorize("Hello", "red")
    assert "\033[31mHello\033[0m" in output


def test_colorize_invalid_color():
    output = colorize("Hello", "unknown")
    assert output == "Hello"


def test_progress_bar_midway():
    bar = progress_bar(50, 100, length=10)
    assert bar == "[█████-----] 50.0%"


def test_progress_bar_zero_total():
    bar = progress_bar(0, 0, length=10)
    assert bar == "[----------] 0.0%"


def test_format_table():
    data = [
        {"name": "Alice", "role": "Dev"},
        {"name": "Bob", "role": "Ops"},
    ]
    table = format_table(data)
    assert "Alice" in table
    assert "role" in table
    assert "+-" in table
