import re
from typing import Union

codec_list = [
    "cp932",
    "euc_jp",
    "gbk",
    "iso2022_jp",
    "johab",
    "utf_16",
    "utf_16_be",
    "utf_32",
    "utf_32_be",
    "utf_7",
    "utf_8",
    "utf_8_sig",
]


def guess_encoding(x: bytes, hint: Union[str, re.Pattern]) -> str:
    if isinstance(hint, str):
        return guess_encoding(x, re.compile(hint))
    for c in codec_list:
        try:
            buf = x.decode(c)
            if hint.match(buf) is not None:
                return c
        except ValueError:
            ...
