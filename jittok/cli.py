from argparse import ArgumentParser

from . import jptext


def setup_argument_parser() -> ArgumentParser:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="module_name")
    jptext.cli.setup_argument_subparser(subparsers)
    return parser


def main() -> None:
    parser = setup_argument_parser()
    args = parser.parse_args()
    if args.subcommand == "jptext":
        jptext.cli.main(args)
    else:
        parser.print_help()
