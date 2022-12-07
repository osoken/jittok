from pytest_mock import MockerFixture

from jittok import cli


def test_setup_argument_parser(mocker: MockerFixture):
    jptext = mocker.patch("jittok.cli.jptext")
    ArgumentParser = mocker.patch("jittok.cli.ArgumentParser")
    actual = cli.setup_argument_parser()
    parser = ArgumentParser.return_value
    jptext.cli.setup_argument_subparser.assert_called_once_with(parser.add_subparsers.return_value)
    parser.add_subparsers.assert_called_once_with(dest="module_name")
    assert actual == parser


def test_main(mocker: MockerFixture):
    setup_argument_parser = mocker.patch("jittok.cli.setup_argument_parser")
    parser = setup_argument_parser.return_value
    args = parser.parse_args.return_value
    args.subcommand = None
    actual = cli.main()
    assert actual is None
    setup_argument_parser.assert_called_once_with()
    parser.parse_args.assert_called_once_with()
    parser.print_help.assert_called_once_with()
