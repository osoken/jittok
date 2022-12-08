from argparse import ArgumentParser, _SubParsersAction
from unittest.mock import MagicMock

from jittok.jptext import cli


def test_setup_argument_subparser() -> None:
    subparsers = MagicMock(spec=_SubParsersAction)
    cli.setup_argument_subparser(subparsers)
