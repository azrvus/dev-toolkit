from dev_toolkit.color import blue, bold, green, red, yellow


def test_color_formatting():
    assert red("error").startswith("\033[31m")
    assert green("ok").startswith("\033[32m")
    assert yellow("warn").startswith("\033[33m")
    assert blue("info").startswith("\033[34m")
    assert bold("text").startswith("\033[1m")


def test_color_resets():
    assert red("test").endswith("\033[0m")
