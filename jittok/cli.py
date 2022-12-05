from argparse import ArgumentParser

from . import jptext


def main() -> None:
    parser = setup_argument_parser()
    args = parser.parse_args()
    if args.subcommand == "jptext":
        jptext.cli.main(args)
    else:
        parser.print_help()


def setup_argument_parser():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers("subcommand")
    jptext.cli.setup_argument_subparser(subparsers)
    return parser
