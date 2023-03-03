import os

import pytest
from pytest_mock import MockerFixture

from jittok import jpaddress


def test_zipcode_to_address(mocker: MockerFixture) -> None:
    _zipcode_to_address_map = mocker.patch("jittok.jpaddress.core._zipcode_to_address_map")
    _zipcode_to_address_map.get.return_value = jpaddress.Address(
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
    actual = jpaddress.zipcode_to_address("100-0001")
    assert actual.prefecture == "東京都"
    assert actual.city == "千代田区"
    assert actual.town == "千代田"
    assert actual.prefecture_kana == "トウキョウト"
    assert actual.city_kana == "チヨダク"
    assert actual.town_kana == "チヨダ"
    assert actual.prefecture_kanji == "東京都"
    assert actual.city_kanji == "千代田区"
    assert actual.town_kanji == "千代田"
    assert actual.prefecture_romaji == "Tokyo-to"
    assert actual.city_romaji == "Chiyoda-ku"
    assert actual.town_romaji == "Chiyoda"
    assert str(actual) == "東京都 千代田区 千代田"


def test_zipcode_to_address_raises_value_error(mocker: MockerFixture) -> None:
    _zipcode_to_address_map = mocker.patch("jittok.jpaddress.core._zipcode_to_address_map")
    _zipcode_to_address_map.get.return_value = None
    with pytest.raises(ValueError):
        jpaddress.zipcode_to_address("100-0001")


def test__init_address_data() -> None:
    wd = os.path.dirname(__file__)
    with open(os.path.join(wd, "fixtures", "zipcode.csv"), "r", encoding="utf-8") as fin:
        actual = jpaddress.core._init_address_data(fin)
    assert len(actual) == 10
    assert actual["0600000"] == jpaddress.Address(
        prefecture="北海道",
        city="札幌市中央区",
        town="",
        prefecture_kana="ホッカイドウ",
        city_kana="サッポロシチュウオウク",
        town_kana="",
        prefecture_kanji="北海道",
        city_kanji="札幌市中央区",
        town_kanji="",
        prefecture_romaji="Hokkaido",
        city_romaji="Sapporo-shi Chuo-ku",
        town_romaji="",
    )
    assert actual["0640941"] == jpaddress.Address(
        prefecture="北海道",
        city="札幌市中央区",
        town="旭ケ丘",
        prefecture_kana="ホッカイドウ",
        city_kana="サッポロシチュウオウク",
        town_kana="アサヒガオカ",
        prefecture_kanji="北海道",
        city_kanji="札幌市中央区",
        town_kanji="旭ケ丘",
        prefecture_romaji="Hokkaido",
        city_romaji="Sapporo-shi Chuo-ku",
        town_romaji="Asahigaoka",
    )
