# Dev Toolkit 0.1.0

Published on [PyPI](https://pypi.org/project/azrvus-dev-toolkit/0.1.0/) from
commit `82d0dc466845b63619b9a390912ce103e040e191` through GitHub OIDC.
Fresh public pip, uv add, and isolated uv tool installs passed imports, CLI flags,
and valid/invalid JSONL smoke tests.

- Validate local UTF-8 JSONL evaluation datasets with `dev-toolkit validate-jsonl`.
  Require top-level keys, find malformed JSON and invalid records by line number,
  and return useful exit codes without printing dataset records.
- Use the streaming `validate_jsonl` Python API with no runtime dependencies.
- Use existing utilities for text, JSON I/O, environment checks, caching, retries,
  processes, and more. Fix package exports and restore default IO test discovery.
- Publish as `azrvus-dev-toolkit` with the maintainer username prefix.
- Install the Python 3.11+ package under `dev_toolkit`; run the `dev-toolkit` CLI.
- Include the MIT license, accurate documentation, and one package/CLI version source.
- Verify wheel and source distributions in Python 3.11/3.12 CI, including isolated
  installs, metadata checks, imports, CLI flags, and JSONL command behavior.

Validation at preparation: 134 tests pass. CI also runs Ruff and distribution
checks. The release workflow uses separate build/publish jobs and PyPI Trusted
Publishing, with an optional configured TestPyPI rehearsal.

The validator checks JSON structure and required key presence. It does not grade
model responses, enforce value types, or validate dataset semantics. Blank lines
and empty files are rejected; required keys may have null values.
