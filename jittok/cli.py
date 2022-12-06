from argparse import ArgumentParser

from . import jptext


def setup_argument_parser() -> ArgumentParser:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()
    jptext.cli.setup_argument_subparser(subparsers)
    return parser


def main() -> None:
    parser = setup_argument_parser()
    args = parser.parse_args()
    parser.print_help()
