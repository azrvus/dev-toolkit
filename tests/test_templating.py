from pathlib import Path

import pytest

from dev_toolkit.templating import render_string, render_template_file


def test_render_string():
    template = "Hello, {{ name }}! Welcome to {{ project }}."
    context = {"name": "Alice", "project": "Dev Toolkit"}
    result = render_string(template, context)
    assert result == "Hello, Alice! Welcome to Dev Toolkit."


def test_render_template_file(tmp_path: Path):
    tpl_file = tmp_path / "greeting.txt"
    tpl_file.write_text("User: {{ user }}", encoding="utf-8")

    result = render_template_file(tpl_file, {"user": "Bob"})
    assert result == "User: Bob"


def test_render_template_not_found():
    with pytest.raises(FileNotFoundError):
        render_template_file("non_existent_template_999.txt", {})
