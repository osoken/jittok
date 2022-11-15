import re
from typing import Optional, Pattern, Union

import regex

from .exceptions import UnknownEncodingError

codec_list = [
    "utf_8",
    "utf_8_sig",
    "utf_7",
    "utf_16",
    "utf_16_be",
    "utf_32",
    "utf_32_be",
    "euc_jp",
    "gbk",
    "iso2022_jp",
]


def guess_encoding(x: bytes, hint: Optional[Union[str, Pattern[str]]] = None) -> str:
    if hint is None:
        return guess_encoding(
            x,
            regex.compile(
                r'[\p{Script=Han}\u3041-\u309F\u30A1-\u30FF\uFF01-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF40\uFF5B-\uFF65\u3000-\u303F]+'
            ),
        )
    if isinstance(hint, str):
        return guess_encoding(x, re.compile(hint))
    for c in codec_list:
        try:
            buf = x.decode(c)
            if hint.match(buf) is not None:
                return c
        except ValueError:
            ...
    raise UnknownEncodingError()


def decode(x: bytes) -> str:
    return x.decode(guess_encoding(x))


numeric_string_regex = re.compile(
    r"(?P<minus>-)?"
    r"(?:(?P<兆>([0-9.]*千)?([0-9.]*百)?([0-9.]*十)?([0-9.]*)?)?兆)?"
    r"(?:(?P<億>([0-9.]*千)?([0-9.]*百)?([0-9.]*十)?([0-9.]*)?)?億)?"
    r"(?:(?P<万>([0-9.]*千)?([0-9.]*百)?([0-9.]*十)?([0-9.]*)?)?万)?"
    r"(?P<一>([0-9.]*千)?([0-9.]*百)?([0-9.]*十)?([0-9.]*)?)?"
)

four_digits_string_regex = re.compile(r"^((?P<千>[0-9.]*)千)?((?P<百>[0-9.]*)百)?((?P<十>[0-9.]*)十)?((?P<一>[0-9.]*))?$")


def to_numeric(x: str) -> Union[float, int]:
    x_ = x.translate(
        str.maketrans(
            {
                "１": "1",
                "２": "2",
                "３": "3",
                "４": "4",
                "５": "5",
                "６": "6",
                "７": "7",
                "８": "8",
                "９": "9",
                "０": "0",
                "一": "1",
                "二": "2",
                "三": "3",
                "四": "4",
                "五": "5",
                "六": "6",
                "七": "7",
                "八": "8",
                "九": "9",
                "〇": "0",
                "壱": "1",
                "弐": "2",
                "参": "3",
                "零": "0",
            }
        )
    ).replace(",", "")
    m = numeric_string_regex.match(x_)
    return (-1 if m["minus"] is not None else 1) * (
        (_parse_sen_digits(m["兆"]) if m["兆"] is not None else 0) * 1000000000000
        + (_parse_sen_digits(m["億"]) if m["億"] is not None else 0) * 100000000
        + (_parse_sen_digits(m["万"]) if m["万"] is not None else 0) * 10000
        + (_parse_sen_digits(m["一"]) if m["一"] is not None else 0)
    )


def _parse_sen_digits(x: str) -> Union[float, int]:
    m = four_digits_string_regex.match(x)
    if m is not None:
        return (
            (0 if m["千"] is None else (1 if len(m["千"]) == 0 else float(m["千"]))) * 1000
            + (0 if m["百"] is None else (1 if len(m["百"]) == 0 else float(m["百"]))) * 100
            + (0 if m["十"] is None else (1 if len(m["十"]) == 0 else float(m["十"]))) * 10
            + (0 if m["一"] is None or len(m["一"]) == 0 else float(m["一"]))
        )
    return 0
