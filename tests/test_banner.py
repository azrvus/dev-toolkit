from dev_toolkit.banner import print_banner, print_box, print_divider


def test_print_divider():
    div = print_divider("-", 10)
    assert div == "----------"


def test_print_box():
    box = print_box("Hello", padding=1, border_char="#")
    assert "#####" in box
    assert "# Hello #" in box


def test_print_banner():
    banner = print_banner("Dev Toolkit", "v0.1.0")
    assert "DEV TOOLKIT" in banner
    assert "v0.1.0" in banner
