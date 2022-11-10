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
    x_ = x.translate(
        str.maketrans(
            {
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
            }
        )
    ).replace(",", "")
    m = re.match(r"^(?P<minus>-)?((?P<千>[0-9]*)千)?((?P<百>[0-9]*)百)?((?P<十>[0-9]*)十)?((?P<一>[0-9]*))?$", x_)
    if m is not None:
        return (-1 if m["minus"] is not None else 1) * (
            (0 if m["千"] is None else (1 if len(m["千"]) == 0 else int(m["千"]))) * 1000
            + (0 if m["百"] is None else (1 if len(m["百"]) == 0 else int(m["百"]))) * 100
            + (0 if m["十"] is None else (1 if len(m["十"]) == 0 else int(m["十"]))) * 10
            + (0 if m["一"] is None or len(m["一"]) == 0 else int(m["一"]))
        )
    return float(x_)
