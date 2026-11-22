# Dev Toolkit

[![CI](https://github.com/azrvus/dev-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/azrvus/dev-toolkit/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Python 3.11+ utilities with no runtime dependencies. Includes JSON file I/O,
text helpers, validation, retries, caching, environment checks, and process tools.

## Installation

Install from GitHub (verified in a fresh virtual environment):

```bash
python -m pip install 'git+https://github.com/azrvus/dev-toolkit.git'
```

Public PyPI installation is pending release verification. Do not use
`pip install dev-toolkit` or `uv add dev-toolkit` yet.

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

The CLI currently prints `Dev Toolkit CLI operational.`. With `--verbose`
(or `-v`), it also prints `Verbose mode enabled.`. Library utilities are used
through Python imports; the CLI does not expose each utility as a command.

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
