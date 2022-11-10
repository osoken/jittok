import os
from typing import Union

import pytest

from jittok import jptext

current_dir = os.path.dirname(os.path.abspath(__file__))
fixture_root = os.path.join(current_dir, "fixtures", "jptext", "codecs")


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
    with open(os.path.join(fixture_root, f"{original_codec}.txt"), "rb") as fin:
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
    with open(os.path.join(fixture_root, f"{original_codec}.txt"), "rb") as fin:
        somebin = fin.read()
    expected = original_codec
    actual = jptext.guess_encoding(somebin)
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
def test_decode(original_codec: str) -> None:
    with open(os.path.join(fixture_root, f"{original_codec}.txt"), "rb") as fin:
        somebin = fin.read()
    expected = "期待した値"
    actual = jptext.decode(somebin)
    assert actual == expected


@pytest.mark.parametrize(
    ["argument", "expected"],
    [
        ["123", 123],
        ["123,234", 123234],
        ["3.14", 3.14],
        ["-1000", -1000],
        ["-3,321,123,000", -3321123000],
        ["-12.322", -12.322],
        ["一", 1],
        ["二", 2],
        ("壱", 1),
        ("十", 10),
        ("十一", 11),
        ("2十", 20),
        ("百十", 110),
        ("千弐百", 1200),
        ("1232千", 1232000),
        ("三千一", 3001),
        ("１２３", 123),
        ("1百", 100),
        ("〇千", 0),
        ("-2十", -20),
        ("零", 0),
    ],
)
def test_to_numeric(argument: str, expected: Union[float, int]) -> None:
    actual = jptext.to_numeric(argument)
    assert actual == expected
