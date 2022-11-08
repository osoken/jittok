import os

import pytest

from jittok import jptext


@pytest.mark.parametrize(
    ["original_codec"],
    [
        ["euc_jp"],
        ["gbk"],
        ["iso2022_jp"],
        ["utf_16"],
        ["utf_16_be"],
        ["utf_32"],
        ["utf_32_be"],
        ["utf_7"],
        ["utf_8"],
        ["utf_8_sig"],
    ],
)
def test_guess_encoding(original_codec: str) -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, "fixtures", "jptext", "codecs", f"{original_codec}.txt"), "rb") as fin:
        somebin = fin.read()
    expected = original_codec
    actual = jptext.guess_encoding(somebin, hint=r"^期")
    assert actual == expected


@pytest.mark.parametrize(
    ["original_codec"],
    [
        ["euc_jp"],
        ["gbk"],
        ["iso2022_jp"],
        ["utf_16"],
        ["utf_16_be"],
        ["utf_32"],
        ["utf_32_be"],
        ["utf_7"],
        ["utf_8"],
        ["utf_8_sig"],
    ],
)
def test_guess_encoding_without_hint(original_codec: str) -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, "fixtures", "jptext", "codecs", f"{original_codec}.txt"), "rb") as fin:
        somebin = fin.read()
    expected = original_codec
    actual = jptext.guess_encoding(somebin)
    assert actual == expected
