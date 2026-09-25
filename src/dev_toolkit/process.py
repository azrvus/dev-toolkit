"""Subprocess execution and command runner utilities."""

import dataclasses
import shlex
import subprocess
from pathlib import Path


@dataclasses.dataclass(frozen=True)
class ProcessResult:
    """Dataclass holding command execution outputs and metadata."""

    command: list[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def success(self) -> bool:
        """Return True if the process completed with returncode 0."""
        return self.returncode == 0


def run_command(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    timeout: float | None = None,
    check: bool = False,
) -> ProcessResult:
    """Execute a system command safely and capture its output."""
    if isinstance(cmd, str):
        cmd_args = shlex.split(cmd)
    else:
        cmd_args = list(cmd)

    if not cmd_args:
        raise ValueError("Command cannot be empty")

    try:
        completed = subprocess.run(
            cmd_args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as err:
        raise TimeoutError(
            f"Command '{' '.join(cmd_args)}' timed out after {timeout} seconds"
        ) from err

    result = ProcessResult(
        command=cmd_args,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )

    if check and not result.success:
        raise RuntimeError(
            f"Command '{' '.join(cmd_args)}' failed with exit code {result.returncode}:\n{result.stderr}"
        )

    return result
