import codecs
import csv
import sys
from dataclasses import dataclass
from typing import Dict, Optional

from .. import jptext
from ..blob import open_zipfile, save_resource_from_http_request_in_temporary_file
from .exceptions import ZipcodeNotFoundError

if sys.version_info >= (3, 9):
    from collections.abc import Generator, Iterable
else:
    from typing import Generator, Iterable

import pykakasi

kks = pykakasi.kakasi()
address_lookup_cache: Optional["AddressLookup"] = None


@dataclass(eq=True, frozen=True)
class Address:
    zipcode: str
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


def zipcode_to_address(zipcode: str) -> Address:
    """Convert a zipcode to an address.

    Args:
        zipcode (str): Zipcode.

    Returns:
        Address: Address.

    Raises:
        ValueError: Invalid zipcode.

    >>> from unittest.mock import patch
    >>> with patch("jittok.jpaddress.core.address_lookup_cache") as mock:
    ...     mock.__getitem__.return_value = Address(zipcode='1000001', prefecture='東京都', city='千代田区', town='千代田', prefecture_kana='トウキョウト', city_kana='チヨダク', town_kana='チヨダ', prefecture_kanji='東京都', city_kanji='千代田区', town_kanji='千代田', prefecture_romaji='Tokyo-to', city_romaji='Chiyoda-ku', town_romaji='Chiyoda')
    ...     zipcode_to_address("1000001")
    Address(zipcode='1000001', prefecture='東京都', city='千代田区', town='千代田', prefecture_kana='トウキョウト', city_kana='チヨダク', town_kana='チヨダ', prefecture_kanji='東京都', city_kanji='千代田区', town_kanji='千代田', prefecture_romaji='Tokyo-to', city_romaji='Chiyoda-ku', town_romaji='Chiyoda')
    """  # noqa: E501
    global address_lookup_cache
    if address_lookup_cache is None:
        address_lookup_cache = AddressLookup()
    retval = address_lookup_cache[zipcode]
    return retval


def _tidy_romaji_name(name: str) -> str:
    """Tidy up the romaji name.

    Args:
        name (str): Romaji name.

    Returns:
        str: Tidied up romaji name.

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


class AddressLookup(Dict[str, Address]):
    def __init__(self, data: Optional[Iterable[Address]] = None) -> None:
        if data is None:
            super(AddressLookup, self).__init__(self.from_japanpost_zipfile().items())
        else:
            super(AddressLookup, self).__init__({a.zipcode: a for a in data})

    def __missing__(self, key: str) -> Address:
        raise ZipcodeNotFoundError(f"Invalid zipcode: {key}")

    def search(self, search_word: str) -> Generator[Address, None, None]:
        for v in self.values():
            if search_word in v.prefecture or search_word in v.city or search_word in v.town:
                yield v

    @classmethod
    def from_csv_string_iterable(cls, readable: Iterable[str]) -> "AddressLookup":
        """Initialize AddressLookup class from a string iterable."""
        retval = AddressLookup([])
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
            a_prefecture_raw = d[a_prefecture_idx]
            a_city_raw = d[a_city_idx]
            a_town_raw = d[a_town_idx] if d[a_town_idx] != "IKANIKEISAIGANAIBAAI" else ""
            retval[d[zip_code_idx]] = Address(
                zipcode=d[zip_code_idx],
                prefecture=prefecture_kanji,
                city=city_kanji,
                town=town_kanji,
                prefecture_kana=jptext.kanji_to_kana(prefecture_kanji),
                city_kana=jptext.kanji_to_kana(city_kanji),
                town_kana=jptext.kanji_to_kana(town_kanji),
                prefecture_kanji=prefecture_kanji,
                city_kanji=city_kanji,
                town_kanji=town_kanji,
                prefecture_romaji=_tidy_romaji_name(a_prefecture_raw),
                city_romaji=_tidy_romaji_name(a_city_raw),
                town_romaji=_tidy_romaji_name(a_town_raw),
            )
        return retval

    @classmethod
    def from_csv_local_zipfile(
        cls, zipfile_path: str, filename_in_zipfile: str, encoding: Optional[str] = None
    ) -> "AddressLookup":
        """Initialize AddressLookup class from a CSV file in a ZIP file."""
        with open_zipfile(zipfile_path, filename_in_zipfile) as f:
            return cls.from_csv_string_iterable(codecs.getreader(encoding if encoding is not None else "utf-8")(f))

    @classmethod
    def from_csv_remote_zipfile(
        cls, zipfile_url: str, filename_in_zipfile: str, encoding: Optional[str] = None
    ) -> "AddressLookup":
        """Initialize AddressLookup class from a CSV file in a ZIP file."""
        with save_resource_from_http_request_in_temporary_file(zipfile_url) as f:
            return cls.from_csv_local_zipfile(f.name, filename_in_zipfile, encoding=encoding)

    @classmethod
    def from_japanpost_zipfile(cls) -> "AddressLookup":
        """Initialize AddressLookup class from a CSV file in a ZIP file."""
        return cls.from_csv_remote_zipfile(
            "https://www.post.japanpost.jp/zipcode/dl/roman/ken_all_rome.zip", "KEN_ALL_ROME.csv", encoding="CP932"
        )

    def __getitem__(self, key: str) -> Address:
        return super(AddressLookup, self).__getitem__(key.replace("-", ""))
