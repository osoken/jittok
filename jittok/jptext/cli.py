import sys
from argparse import ArgumentParser, Namespace

from . import normalize


def setup_argument_subparser(parser: ArgumentParser) -> None:
    subsubparsers = parser.add_subparsers(dest="subsubcommand")
    subsubparsers.add_parser("normalize")


def main(args: Namespace) -> None:
    if args.subsubcommand == "normalize":
        sys.stdout.write(normalize(sys.stdin.read()))
    else:
        args.print_help()
