"""Command-line interface utilities."""

import argparse
import sys
from collections.abc import Sequence

from dev_toolkit._version import __version__
from dev_toolkit.jsonl import validate_jsonl

_SIGNATURES = {
    None: "  .------.\n  | >_   |  dev-toolkit\n  '------'  azrvus",
    "validate-jsonl": "  .---.\n  |{ }|  validate-jsonl\n  '--v'  azrvus",
}


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
    parser.add_argument(
        "--no-art", action="store_true", help="hide the terminal ASCII signature"
    )
    commands = parser.add_subparsers(dest="command")
    validate = commands.add_parser(
        "validate-jsonl", help="validate a local UTF-8 JSONL evaluation dataset"
    )
    validate.add_argument("path", help="path to the dataset")
    validate.add_argument(
        "--required-key", action="append", default=[], metavar="KEY",
        help="require a top-level key (repeat for multiple keys)",
    )
    return parser.parse_args(args)


def main(args: Sequence[str] | None = None) -> int:
    """CLI entrypoint execution."""
    parsed_args = parse_args(args)
    if sys.stdout.isatty() and not parsed_args.no_art:
        print(_SIGNATURES[parsed_args.command], flush=True)
    if parsed_args.command == "validate-jsonl":
        invalid = False
        for issue in validate_jsonl(parsed_args.path, parsed_args.required_key):
            invalid = True
            location = f"line {issue.line}" if issue.line else "file"
            print(f"{location}: {issue.message}", file=sys.stderr)
        if invalid:
            return 1
        print("Valid JSONL.")
        return 0
    if parsed_args.verbose:
        print("Verbose mode enabled.")
    print("Dev Toolkit CLI operational.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
