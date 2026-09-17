"""Command-line interface utilities."""

import argparse
import sys
from collections.abc import Sequence
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("dev-toolkit")
except PackageNotFoundError:
    __version__ = "0.1.0"


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for dev-toolkit."""
    parser = argparse.ArgumentParser(
        prog="dev-toolkit",
        description="Developer utility toolkit CLI.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="enable verbose output",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser.parse_args(args)


def main(args: Sequence[str] | None = None) -> int:
    """CLI entrypoint execution."""
    parsed_args = parse_args(args)
    if parsed_args.verbose:
        print("Verbose mode enabled.")
    print("Dev Toolkit CLI operational.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
