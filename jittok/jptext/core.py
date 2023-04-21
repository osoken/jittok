import math
import re
import sys
import unicodedata
from typing import Optional, Union

import pykakasi
import regex

from .exceptions import UnknownEncodingError

if sys.version_info < (3, 9):
    from typing import Pattern

    PatternT = Union[Pattern[str], regex.regex.Pattern]
else:
    PatternT = Union[re.Pattern[str], regex.regex.Pattern[str]]

kks = pykakasi.kakasi()

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


def guess_encoding(x: bytes, hint: Optional[Union[str, PatternT]] = None) -> str:
    if hint is None:
        return guess_encoding(
            x,
            regex.compile(
                r"[\p{Script=Han}\u3041-\u309F\u30A1-\u30FF\uFF01-\uFF0F\uFF1A-\uFF20"
                r"\uFF3B-\uFF40\uFF5B-\uFF65\u3000-\u303F]+"
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


_basic_number_string = r"(?:(?:(?:[0-9]{0,3})(?:,[0-9]{3})+)|(?:[0-9]*))(?:\.[0-9]+)?"
_four_digits_string_regex_str = (
    rf"^((?P<千>{_basic_number_string})千)?"
    rf"((?P<百>{_basic_number_string})百)?"
    rf"((?P<十>{_basic_number_string})十)?"
    rf"((?P<一>{_basic_number_string}))?$"
)

numeric_string_regex = re.compile(
    r"^(?P<minus>-)?"
    + "".join(
        (
            rf"(?:(?P<{dig}>({_basic_number_string}千)?"
            rf"({_basic_number_string}百)?"
            rf"({_basic_number_string}十)?"
            rf"({_basic_number_string})?)?{dig})?"
            for dig in [
                "無量大数",
                "不可思議",
                "那由他",
                "阿僧祇",
                "恒河沙",
                "極",
                "載",
                "正",
                "澗",
                "溝",
                "穣",
                "𥝱",
                "垓",
                "京",
                "兆",
                "億",
                "万",
            ]
        )
    )
    + (
        rf"(?P<一>({_basic_number_string}千)?"
        rf"({_basic_number_string}百)?"
        rf"({_basic_number_string}十)?"
        rf"({_basic_number_string})?)?$"
    )
)

_four_digits_string_regex = re.compile(_four_digits_string_regex_str)
trans_map = str.maketrans(
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


def to_numeric(x: str) -> Union[float, int]:
    if not isinstance(x, str):
        raise TypeError(f"to_numeric() argument must be a string, not '{type(x)}'")
    if len(x) == 0:
        raise ValueError(f"invalid literal: {x}")
    x_ = x.translate(trans_map)
    m = numeric_string_regex.match(x_)
    if m is None or len(m[0]) == 0:
        raise ValueError(f"invalid literal: {x}")
    buf = 0
    valid = False
    for i, k in enumerate(
        [
            "一",
            "万",
            "億",
            "兆",
            "京",
            "垓",
            "𥝱",
            "穣",
            "溝",
            "澗",
            "正",
            "載",
            "極",
            "恒河沙",
            "阿僧祇",
            "那由他",
            "不可思議",
            "無量大数",
        ]
    ):
        digits = m[k]
        if digits is None:
            continue
        if len(digits) > 0:
            buf += _parse_sen_digits(digits) * (10000**i)
            valid = True
    if not valid:
        raise ValueError(f"invalid literal: {x}")
    return (-1 if m["minus"] is not None else 1) * buf


def _parse_sen_digits(x: str) -> Union[float, int]:
    m = _four_digits_string_regex.match(x)
    if m is not None:
        s = (
            (0 if m["千"] is None else (1 if len(m["千"]) == 0 else float(m["千"].replace(",", "")))) * 1000
            + (0 if m["百"] is None else (1 if len(m["百"]) == 0 else float(m["百"].replace(",", "")))) * 100
            + (0 if m["十"] is None else (1 if len(m["十"]) == 0 else float(m["十"].replace(",", "")))) * 10
            + (0 if m["一"] is None or len(m["一"]) == 0 else float(m["一"].replace(",", "")))
        )
        if s == math.floor(s):
            return int(s)
        return s
    return 0


normalize_trans_map = str.maketrans(
    {
        "˗": "-",
        "֊": "-",
        "‐": "-",
        "‑": "-",
        "‒": "-",
        "–": "-",
        "⁃": "-",
        "⁻": "-",
        "₋": "-",
        "−": "-",
        "　": " ",
        "\u200b": " ",
        "\ufeff": " ",
        "\t": " ",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
    }
)

parentheses_left = re.compile(r"([^\s(])\(")
parentheses_right = re.compile(r"\)([^\s)])")


def normalize(
    x: str,
    newline_to_space: bool = False,
    remove_multiple_spaces: bool = False,
    remove_variation_selectors: bool = False,
) -> str:
    normalized_string = parentheses_right.sub(
        r") \1", parentheses_left.sub(r"\1 (", unicodedata.normalize("NFKC", x).translate(normalize_trans_map))
    )
    if newline_to_space:
        normalized_string = re.sub(r"[\n\r]", " ", normalized_string)
    if remove_multiple_spaces:
        normalized_string = re.sub(r" +", " ", normalized_string)
    if remove_variation_selectors:
        normalized_string = re.sub(r"[\U000e0100-\U000e01ef]", "", normalized_string)
    return normalized_string


def kanji_to_kana(x: str) -> str:
    return "".join(d["kana"] for d in kks.convert(x))


def kanji_to_hiragana(x: str) -> str:
    return "".join(d["hira"] for d in kks.convert(x))


def kanji_to_romaji(x: str) -> str:
    return "".join(d["hepburn"] for d in kks.convert(x))
