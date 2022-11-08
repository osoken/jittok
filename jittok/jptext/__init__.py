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


def to_numeric(x: str) -> Union[float, int]:
    return int(x.replace(",", ""))
