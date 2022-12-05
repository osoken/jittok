from pytest_mock import MockerFixture

from jittok import cli


def test_setup_argument_parser(mocker: MockerFixture):
    jptext = mocker.patch("jittok.cli.jptext")
    ArgumentParser = mocker.patch("jittok.cli.ArgumentParser")
    actual = cli.setup_argument_parser()
    parser = ArgumentParser.return_value
    jptext.cli.setup_argument_subparser.assert_called_once_with(parser.add_subparsers.return_value)
    parser.add_subparsers.assert_called_once_with("subcommand")
    assert actual == parser
