from unittest.mock import call

from pytest_mock import MockerFixture

from jittok import cli


def test_setup_argument_parser(mocker: MockerFixture) -> None:
    jptext_cli = mocker.patch("jittok.cli.jptext_cli")
    ArgumentParser = mocker.patch("jittok.cli.ArgumentParser")
    parser = ArgumentParser.return_value
    subparsers = parser.add_subparsers.return_value
    actual = cli.setup_argument_parser()
    jptext_cli.setup_argument_subparser.assert_called_once_with(subparsers.add_parser.return_value)
    parser.add_subparsers.assert_called_once_with(dest="subcommand")
    subparsers.add_parser.assert_has_calls([call("jptext")])
    assert actual == parser


def test_main_print_help(mocker: MockerFixture) -> None:
    setup_argument_parser = mocker.patch("jittok.cli.setup_argument_parser")
    parser = setup_argument_parser.return_value
    args = parser.parse_args.return_value
    args.subcommand = None
    cli.main()
    setup_argument_parser.assert_called_once_with()
    parser.parse_args.assert_called_once_with()
    parser.print_help.assert_called_once_with()


def test_main_jptext(mocker: MockerFixture) -> None:
    setup_argument_parser = mocker.patch("jittok.cli.setup_argument_parser")
    jptext_cli = mocker.patch("jittok.cli.jptext_cli")
    parser = setup_argument_parser.return_value
    args = parser.parse_args.return_value
    args.subcommand = "jptext"
    cli.main()
    setup_argument_parser.assert_called_once_with()
    parser.parse_args.assert_called_once_with()
    parser.print_help.assert_not_called()
    jptext_cli.main.assert_called_once_with(args)
