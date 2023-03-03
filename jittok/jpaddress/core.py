import csv
import sys
from dataclasses import dataclass

import pykakasi

from .. import jptext

if sys.version_info >= (3, 7):
    from collections.abc import Iterable, Mapping
else:
    from typing import Iterable, Mapping


kks = pykakasi.kakasi()

import pykakasi

from .. import jptext

kks = pykakasi.kakasi()


@dataclass(eq=True, frozen=True)
class Address:
    prefecture: str
    city: str
    town: str
    prefecture_kana: str
    city_kana: str
    town_kana: str
    prefecture_kanji: str
    city_kanji: str
    town_kanji: str
    prefecture_romaji: str
    city_romaji: str
    town_romaji: str

    def __str__(self) -> str:
        return f"{self.prefecture} {self.city} {self.town}"


_zipcode_to_address_map = {
    "1000001": Address(
        prefecture="東京都",
        city="千代田区",
        town="千代田",
        prefecture_kana="トウキョウト",
        city_kana="チヨダク",
        town_kana="チヨダ",
        prefecture_kanji="東京都",
        city_kanji="千代田区",
        town_kanji="千代田",
        prefecture_romaji="Tokyo-to",
        city_romaji="Chiyoda-ku",
        town_romaji="Chiyoda",
    )
}


def zipcode_to_address(zipcode: str) -> Address:
    """Convert a zipcode to an address."""
    retval = _zipcode_to_address_map.get(zipcode.replace("-", ""))
    if retval is None:
        raise ValueError(f"Invalid zipcode: {zipcode}")
    return retval


def _tidy_romaji_name(name: str) -> str:
    """Tidy up the romaji name.
    >>> _tidy_romaji_name("TOKYO")
    'Tokyo'
    >>> _tidy_romaji_name("TOKYO TO")
    'Tokyo-to'
    >>> _tidy_romaji_name("TOKYO TO CHIYODA KU")
    'Tokyo-to Chiyoda-ku'
    >>> _tidy_romaji_name("MIYAKEJIMA MIYAKE MURA")
    'Miyakejima Miyake-mura'
    """
    retval = f"{name.title()} "
    retval = retval.replace(" To ", "-to ")
    retval = retval.replace(" Ku ", "-ku ")
    retval = retval.replace(" Shi ", "-shi ")
    retval = retval.replace(" Cho ", "-cho ")
    retval = retval.replace(" Mura ", "-mura ")
    retval = retval.replace(" Gun ", "-gun ")
    return retval.strip()


def _init_address_data(readable: Iterable[str]) -> Mapping[str, Address]:
    """Initialize the zipcode to address map."""
    retval = {}
    zip_code_idx = 0
    prefecture_idx = 1
    city_idx = 2
    town_idx = 3
    a_prefecture_idx = 4
    a_city_idx = 5
    a_town_idx = 6
    for d in csv.reader(readable):
        prefecture_kanji = jptext.normalize(d[prefecture_idx]).replace(" ", "")
        city_kanji = jptext.normalize(d[city_idx]).replace(" ", "")
        town_kanji = jptext.normalize(d[town_idx]).replace(" ", "") if d[town_idx] != "以下に掲載がない場合" else ""
        prefecture_data = kks.convert(prefecture_kanji)
        city_data = kks.convert(city_kanji)
        town_data = kks.convert(town_kanji)
        a_prefecture_raw = d[a_prefecture_idx]
        a_city_raw = d[a_city_idx]
        a_town_raw = d[a_town_idx] if d[a_town_idx] != "IKANIKEISAIGANAIBAAI" else ""
        retval[d[zip_code_idx]] = Address(
            prefecture=prefecture_kanji,
            city=city_kanji,
            town=town_kanji,
            prefecture_kana="".join(dd["kana"] for dd in prefecture_data),
            city_kana="".join(dd["kana"] for dd in city_data),
            town_kana="".join(dd["kana"] for dd in town_data),
            prefecture_kanji=prefecture_kanji,
            city_kanji=city_kanji,
            town_kanji=town_kanji,
            prefecture_romaji=_tidy_romaji_name(a_prefecture_raw),
            city_romaji=_tidy_romaji_name(a_city_raw),
            town_romaji=_tidy_romaji_name(a_town_raw),
        )
    return retval
