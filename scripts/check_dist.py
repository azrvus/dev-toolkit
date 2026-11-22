"""Check distribution metadata and smoke-test both artifacts outside the checkout."""

import email
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UV = shutil.which("uv")
if UV is None:
    raise SystemExit("Install uv before checking distributions")


def run(*args, cwd, env):
    return subprocess.run(
        args, cwd=cwd, env=env, check=True, capture_output=True, text=True
    ).stdout.strip()


def main():
    """Verify metadata, then install and exercise wheel and source distribution."""
    artifacts = sorted(
        p for p in (ROOT / "dist").iterdir() if p.name.endswith((".whl", ".tar.gz"))
    )
    assert len(artifacts) == 2, "Expected exactly one wheel and one sdist"
    for artifact in artifacts:
        if artifact.suffix == ".whl":
            with zipfile.ZipFile(artifact) as archive:
                metadata_path = next(
                    name for name in archive.namelist() if name.endswith("/METADATA")
                )
                metadata = email.message_from_bytes(archive.read(metadata_path))
                assert any(name.endswith("/LICENSE") for name in archive.namelist())
        else:
            assert artifact.name.endswith(".tar.gz")
            with tarfile.open(artifact) as archive:
                member = next(m for m in archive if m.name.endswith("/PKG-INFO"))
                metadata = email.message_from_bytes(archive.extractfile(member).read())
                assert any(m.name.endswith("/LICENSE") for m in archive)
        assert metadata["Name"] == "azrvus-dev-toolkit"
        assert metadata["Requires-Python"] == ">=3.11"
        assert metadata["License-Expression"] == "MIT"
        assert not metadata.get_all("Requires-Dist")
        assert metadata["Project-URL"]
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            env = dict(os.environ)
            env.pop("PYTHONPATH", None)
            env.pop("VIRTUAL_ENV", None)
            venv = work / "venv"
            run(UV, "venv", "--python", sys.executable, str(venv), cwd=work, env=env)
            scripts = venv / ("Scripts" if os.name == "nt" else "bin")
            python = scripts / ("python.exe" if os.name == "nt" else "python")
            cli = scripts / ("dev-toolkit.exe" if os.name == "nt" else "dev-toolkit")
            run(
                UV,
                "pip",
                "install",
                "--python",
                str(python),
                str(artifact),
                cwd=work,
                env=env,
            )
            version = run(
                str(python),
                "-c",
                (
                    "import dev_toolkit as d; from importlib.metadata import version; "
                    "assert all(hasattr(d, n) for n in d.__all__); "
                    "assert d.__version__ == version('azrvus-dev-toolkit'); "
                    "print(d.__version__)"
                ),
                cwd=work,
                env=env,
            )
            assert version == metadata["Version"]
            assert run(str(cli), "--version", cwd=work, env=env) == (
                f"dev-toolkit {version}"
            )
            assert "validate-jsonl" in run(str(cli), "--help", cwd=work, env=env)
            assert run(str(cli), cwd=work, env=env) == "Dev Toolkit CLI operational."
            assert "Verbose mode enabled." in run(str(cli), "-v", cwd=work, env=env)
            data = work / "valid.jsonl"
            data.write_text('{"prompt":"synthetic"}\n', encoding="utf-8")
            assert (
                run(
                    str(cli),
                    "validate-jsonl",
                    str(data),
                    "--required-key",
                    "prompt",
                    cwd=work,
                    env=env,
                )
                == "Valid JSONL."
            )
            invalid = subprocess.run(
                [str(cli), "validate-jsonl", str(data), "--required-key", "expected"],
                cwd=work,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            assert invalid.returncode == 1
            assert "line 1: missing required keys" in invalid.stderr
            assert "synthetic" not in invalid.stderr
        print(f"Verified {artifact.name}")


if __name__ == "__main__":
    main()
