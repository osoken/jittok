from argparse import ArgumentParser

from . import jptext


def setup_argument_parser():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers("subcommand")
    jptext.cli.setup_argument_subparser(subparsers)
    return parser
