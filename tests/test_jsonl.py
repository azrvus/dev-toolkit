"""Validation behavior, privacy, and CLI regression tests."""

import pytest

from dev_toolkit import validate_jsonl
from dev_toolkit.cli import main


@pytest.mark.parametrize(
    ("content", "lines", "message"),
    [
        (b'', [0], "empty file"),
        (b'\n', [1], "blank line"),
        (b'{}\n\n{}', [2], "blank line"),
        (b'[]\nnull\n1\n"text"\n', [1, 2, 3, 4], "JSON object"),
        (b'{secret\n', [1], "invalid JSON"),
        (b'{"x":NaN}\n{"x":Infinity}', [1, 2], "invalid JSON"),
        (b'{}\n\xff\n{}', [2], "UTF-8"),
    ],
)
def test_invalid_inputs(tmp_path, content, lines, message):
    path = tmp_path / "input.jsonl"
    path.write_bytes(content)
    issues = list(validate_jsonl(path))
    assert [issue.line for issue in issues] == lines
    assert all(message in issue.message for issue in issues)
    assert all("secret" not in issue.message for issue in issues)


def test_required_keys_and_unicode(tmp_path):
    path = tmp_path / "input.jsonl"
    path.write_text('{"prompt":"مرحبا","expected":null}\n{}', encoding="utf-8")
    issues = list(validate_jsonl(path, ["prompt", "expected"]))
    assert len(issues) == 1
    assert issues[0].line == 2
    assert "prompt" in issues[0].message
    assert "expected" in issues[0].message


def test_valid_cli_and_api(tmp_path, capsys):
    path = tmp_path / "input.jsonl"
    path.write_text('{"prompt":"hello","expected":null}', encoding="utf-8")
    assert list(validate_jsonl(path, ["prompt", "expected"])) == []
    assert main(["validate-jsonl", str(path), "--required-key", "prompt",
                 "--required-key", "expected"]) == 0
    assert capsys.readouterr().out == "Valid JSONL.\n"


def test_missing_file_and_directory(tmp_path, capsys):
    for path in [tmp_path / "missing", tmp_path]:
        assert main(["validate-jsonl", str(path)]) == 1
        assert "cannot read input" in capsys.readouterr().err


def test_invalid_cli_does_not_echo_record(tmp_path, capsys):
    path = tmp_path / "input.jsonl"
    path.write_text('{"private":"sensitive-value"}\nnot-json', encoding="utf-8")
    assert main(["validate-jsonl", str(path), "--required-key", "prompt"]) == 1
    output = capsys.readouterr()
    assert "line 1: missing required keys" in output.err
    assert "line 2: invalid JSON" in output.err
    assert "sensitive-value" not in output.err
    assert output.out == ""
