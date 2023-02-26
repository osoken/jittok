import csv
from dataclasses import dataclass
from io import BufferedReader


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


def _init_address_data(readable: BufferedReader) -> dict:
    """Initialize the zipcode to address map."""
    retval = {}
    zip_code_idx = 0
    prefecture_idx = 1
    city_idx = 2
    town_idx = 3
    for d in csv.reader(readable):
        retval[d[zip_code_idx]] = Address(
            prefecture=d[prefecture_idx],
            city=d[city_idx],
            town=d[town_idx],
            prefecture_kana="",
            city_kana="",
            town_kana="",
            prefecture_kanji="",
            city_kanji="",
            town_kanji="",
            prefecture_romaji="",
            city_romaji="",
            town_romaji="",
        )
    return retval
