from argparse import Namespace
from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from jittok.jptext import cli


def test_main_normalize(mocker: MockerFixture) -> None:
    sys = mocker.patch("jittok.jptext.cli.sys")
    sys.stdin.read.return_value = "今日はｲｲ天気"
    normalize = mocker.patch.object(cli, "normalize", return_value="正規化されたきれいな文字列")
    args = MagicMock(spec=Namespace)
    args.subcommand = "jptext"
    args.subsubcommand = "normalize"
    cli.main(args)
    sys.stdout.write.assert_called_once_with("正規化されたきれいな文字列")
    normalize.assert_called_once_with("今日はｲｲ天気")
