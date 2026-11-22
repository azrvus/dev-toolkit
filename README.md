# Dev Toolkit

[![CI](https://github.com/azrvus/dev-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/azrvus/dev-toolkit/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Published distribution name: `azrvus-dev-toolkit`; Python import: `dev_toolkit`;
CLI command: `dev-toolkit`.

Python 3.11+ utilities with no runtime dependencies. Includes JSON file I/O,
text helpers, validation, retries, caching, environment checks, and process tools.

## Installation

Install from GitHub (verified in a fresh virtual environment):

```bash
python -m pip install 'git+https://github.com/azrvus/dev-toolkit.git'
```

Public PyPI installation is pending release verification. Do not use
`pip install azrvus-dev-toolkit` or `uv add azrvus-dev-toolkit` yet.

## Python examples

```python
from dev_toolkit import is_email, slugify, read_json, write_json

assert slugify("Hello World") == "hello-world"
assert is_email("user@example.com")
write_json("example.json", {"status": "ok"})
assert read_json("example.json") == {"status": "ok"}
```

`write_json` creates parent directories and refuses to overwrite existing files
unless `overwrite=True` is passed.

## Command line

```bash
dev-toolkit --help
dev-toolkit --version
dev-toolkit
dev-toolkit --verbose
```

With no subcommand, the CLI prints `Dev Toolkit CLI operational.`. With `--verbose`
(or `-v`), it also prints `Verbose mode enabled.`. Library utilities are used
through Python imports. The dataset validation subcommand is documented below.

## Development

```bash
uv venv
uv pip install -e . pytest ruff
uv run pytest
uv run ruff check .
```

CI runs tests and Ruff on Python 3.11 and 3.12. Test results are checked in CI;
no coverage percentage is claimed.

## License

[MIT](LICENSE).

## Validate LLM evaluation datasets

Check local UTF-8 JSONL without sending data anywhere. Each line must be a JSON
object. Blank lines, empty files, malformed JSON, nonfinite numbers, missing keys,
and unreadable input are errors. Required keys are top-level; null values count
as present. Errors include line numbers and never print complete records.

```bash
dev-toolkit validate-jsonl examples/eval-valid.jsonl --required-key prompt --required-key expected
# Valid JSONL. (exit 0)
dev-toolkit validate-jsonl examples/eval-invalid.jsonl --required-key prompt --required-key expected
# line 1: missing required keys: ['expected']
# line 2: expected a JSON object
# exit 1; diagnostics go to stderr
```

The command checks JSON structure and key presence, not semantic correctness or
model quality. File-level errors use `file:` instead of a line number.

```python
from dev_toolkit import validate_jsonl

for issue in validate_jsonl("examples/eval-valid.jsonl", required_keys=["prompt"]):
    print(issue.line, issue.message)
```

The API yields issues lazily and reads one line at a time; consume the iterator
to perform validation. It retains no records and has no runtime dependencies.
