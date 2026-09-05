"""Command-line interface entry point for dev-toolkit."""

import argparse
import sys

from dev_toolkit.system import print_system_summary


def main() -> None:
    """Parse CLI arguments and dispatch commands."""
    parser = argparse.ArgumentParser(
        prog="dev-toolkit",
        description="Developer utility toolkit for system inspection and environment tasks.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Subcommand: sysinfo
    subparsers.add_parser("sysinfo", help="Print detailed system environment summary")

    args = parser.parse_args()

    if args.command == "sysinfo":
        print_system_summary()
    else:
        parser.print_help()
        sys.exit(0 if len(sys.argv) > 1 else 1)


if __name__ == "__main__":
    main()
