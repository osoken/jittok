from argparse import ArgumentParser

from .jptext import cli as jptext_cli


def main() -> None:
    parser = setup_argument_parser()
    args = parser.parse_args()
    if args.subcommand == "jptext":
        jptext_cli.main(args)
    else:
        parser.print_help()


def setup_argument_parser() -> ArgumentParser:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")
    jptext_cli.setup_argument_subparser(subparsers.add_parser("jptext"))
    return parser
