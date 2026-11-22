# Release procedure

The first public version is **0.1.0**. Publication is pending PyPI Trusted
Publisher setup and verification; building a distribution is not publication.

## One-time account setup

Register a pending GitHub Trusted Publisher at
<https://pypi.org/manage/account/publishing/> using these exact values:

| Field | Value |
| --- | --- |
| PyPI project name | `dev-toolkit` |
| GitHub owner | `azrvus` |
| Repository | `dev-toolkit` |
| Workflow filename | `release.yml` |
| Environment | `pypi` |

No password or API token belongs in repository secrets or chat. If TestPyPI is
configured, use the same fields at
<https://test.pypi.org/manage/account/publishing/> with environment `testpypi`.
The two registries have separate accounts and publisher configurations.

See [PyPI's pending publisher guide](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/).
A 404 for the project does not reserve the name or guarantee PyPI will accept it.
Recheck <https://pypi.org/pypi/dev-toolkit/json> immediately before publishing;
if someone else owns it, stop and select a new distribution name with the maintainer.

## Verify and optionally rehearse

After all code PRs are merged and main CI is green:

```bash
gh workflow run release.yml -R azrvus/dev-toolkit --ref main -f destination=verify
```

This builds and checks wheel/sdist without publishing. When the TestPyPI account
and publisher are configured, use `-f destination=testpypi` to rehearse. Watch the
run and verify the TestPyPI version before continuing. TestPyPI versions cannot
be overwritten; do not dispatch the same version twice after a successful upload.

## Publish intentionally

1. Fetch main and record its verified commit. Confirm all checks are green and
   `src/dev_toolkit/_version.py` agrees with the release tag `v0.1.0`.
2. Recheck the public project name and confirm Trusted Publisher configuration.
3. Publish a GitHub release against that exact merged commit:

   ```bash
   gh release create v0.1.0 -R azrvus/dev-toolkit --target VERIFIED_COMMIT \
     --title 'Dev Toolkit 0.1.0' --notes-file RELEASE_NOTES.md
   ```

4. Watch the Release workflow. The build job repeats tests, Ruff, metadata checks,
   and isolated artifact installs. Only the separate publishing job has OIDC
   permission. It publishes the downloaded build artifacts without checking out
   or executing package code. A prerelease does not publish to public PyPI.
5. Confirm <https://pypi.org/project/dev-toolkit/0.1.0/> and test all three public
   install paths in fresh environments outside the checkout:

   ```bash
   python -m pip install dev-toolkit==0.1.0
   uv add dev-toolkit==0.1.0
   uv tool install dev-toolkit==0.1.0
   ```

   Isolate the uv tool directories using `UV_TOOL_DIR` and `UV_TOOL_BIN_DIR`.
   Check imports, `dev-toolkit --version`, `--help`, `--verbose`, and valid/invalid
   JSONL exit codes. These public install commands remain pending until verified.
6. Update README installation copy through a small PR after public verification.

If GitHub requires an environment approval, approve the named deployment in the
workflow run. If OIDC reports an invalid publisher, check all five fields above;
fix the account configuration and rerun the failed publishing job. Do not bypass
protections or substitute a long-lived token.
