import os

import pytest
from pytest_mock import MockerFixture

from jittok import jpaddress


def test_zipcode_to_address(mocker: MockerFixture) -> None:
    address_lookup_cache = mocker.patch("jittok.jpaddress.core.address_lookup_cache")
    address_lookup_cache.__getitem__.return_value = jpaddress.Address(
        zipcode="1000001",
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
    assert actual.zipcode == "1000001"
    assert str(actual) == "東京都 千代田区 千代田"


def test_zipcode_to_address_raises_value_error(mocker: MockerFixture) -> None:
    from jittok.jpaddress.exceptions import ZipcodeNotFoundError

    address_lookup_cache = mocker.patch("jittok.jpaddress.core.address_lookup_cache")
    address_lookup_cache.__getitem__.side_effect = ZipcodeNotFoundError("0010000")
    with pytest.raises(ZipcodeNotFoundError):
        jpaddress.zipcode_to_address("0010000")


def test_address_lookup_from_csv_string_iterable() -> None:
    wd = os.path.dirname(__file__)
    with open(os.path.join(wd, "fixtures", "zipcode.csv"), "r", encoding="utf-8") as fin:
        actual = jpaddress.AddressLookup.from_csv_string_iterable(fin)
    assert len(actual) == 10
    assert actual["0600000"] == jpaddress.Address(
        zipcode="0600000",
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
        zipcode="0640941",
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


def test_address_lookup_from_csv_local_zipfile(mocker: MockerFixture) -> None:
    open_zipfile = mocker.patch("jittok.jpaddress.core.open_zipfile")
    from_csv_string_iterable = mocker.patch("jittok.jpaddress.AddressLookup.from_csv_string_iterable")
    codecs = mocker.patch("jittok.jpaddress.core.codecs")
    actual = jpaddress.AddressLookup.from_csv_local_zipfile("zipfile.zip", "zipcode.csv")
    assert actual == from_csv_string_iterable.return_value
    open_zipfile.assert_called_once_with("zipfile.zip", "zipcode.csv")
    codecs.getreader.assert_called_once_with("utf-8")
    from_csv_string_iterable.assert_called_once_with(codecs.getreader.return_value.return_value)
    codecs.getreader.return_value.assert_called_once_with(open_zipfile.return_value.__enter__.return_value)


def test_address_lookup_from_csv_local_zipfile_accepts_encoding(mocker: MockerFixture) -> None:
    open_zipfile = mocker.patch("jittok.jpaddress.core.open_zipfile")
    from_csv_string_iterable = mocker.patch("jittok.jpaddress.AddressLookup.from_csv_string_iterable")
    codecs = mocker.patch("jittok.jpaddress.core.codecs")
    actual = jpaddress.AddressLookup.from_csv_local_zipfile("zipfile.zip", "zipcode.csv", encoding="euc-jp")
    assert actual == from_csv_string_iterable.return_value
    open_zipfile.assert_called_once_with("zipfile.zip", "zipcode.csv")
    codecs.getreader.assert_called_once_with("euc-jp")
    from_csv_string_iterable.assert_called_once_with(codecs.getreader.return_value.return_value)
    codecs.getreader.return_value.assert_called_once_with(open_zipfile.return_value.__enter__.return_value)


def test_address_lookup_from_csv_remote_zipfile(mocker: MockerFixture) -> None:
    save_resource_from_http_request_in_temporary_file = mocker.patch(
        "jittok.jpaddress.core.save_resource_from_http_request_in_temporary_file"
    )
    from_csv_local_zipfile = mocker.patch("jittok.jpaddress.AddressLookup.from_csv_local_zipfile")
    actual = jpaddress.AddressLookup.from_csv_remote_zipfile("http://example.com/zipcode.zip", "zipcode.csv")
    assert actual == from_csv_local_zipfile.return_value
    save_resource_from_http_request_in_temporary_file.assert_called_once_with("http://example.com/zipcode.zip")
    from_csv_local_zipfile.assert_called_once_with(
        save_resource_from_http_request_in_temporary_file.return_value.__enter__.return_value.name,
        "zipcode.csv",
        encoding=None,
    )


def test_address_lookup_from_csv_remote_zipfile_accepts_encoding(mocker: MockerFixture) -> None:
    save_resource_from_http_request_in_temporary_file = mocker.patch(
        "jittok.jpaddress.core.save_resource_from_http_request_in_temporary_file"
    )
    from_csv_local_zipfile = mocker.patch("jittok.jpaddress.AddressLookup.from_csv_local_zipfile")
    actual = jpaddress.AddressLookup.from_csv_remote_zipfile(
        "http://example.com/zipcode.zip", "zipcode.csv", encoding="CP932"
    )
    assert actual == from_csv_local_zipfile.return_value
    save_resource_from_http_request_in_temporary_file.assert_called_once_with("http://example.com/zipcode.zip")
    from_csv_local_zipfile.assert_called_once_with(
        save_resource_from_http_request_in_temporary_file.return_value.__enter__.return_value.name,
        "zipcode.csv",
        encoding="CP932",
    )


def test_from_japanpost_zipfile(mocker: MockerFixture) -> None:
    from_csv_remote_zipfile = mocker.patch("jittok.jpaddress.AddressLookup.from_csv_remote_zipfile")
    actual = jpaddress.AddressLookup.from_japanpost_zipfile()
    assert actual == from_csv_remote_zipfile.return_value
    from_csv_remote_zipfile.assert_called_once_with(
        "https://www.post.japanpost.jp/zipcode/dl/roman/ken_all_rome.zip", "KEN_ALL_ROME.csv", encoding="CP932"
    )


def test_address_lookup_default_uses_japanpost_data(mocker: MockerFixture) -> None:
    address = jpaddress.core.Address(
        zipcode="0010000",
        prefecture_kana="ホッカイドウ",
        city_kana="サッポロシ",
        town_kana="ミナミ",
        prefecture_kanji="北海道",
        city_kanji="札幌市",
        town_kanji="南",
        prefecture="北海道",
        city="札幌市",
        town="南",
        prefecture_romaji="Hokkaido",
        city_romaji="Sapporo-shi",
        town_romaji="Minami",
    )
    from_japanpost_zipfile = mocker.patch(
        "jittok.jpaddress.AddressLookup.from_japanpost_zipfile",
    )
    from_japanpost_zipfile.return_value = {"0010000": address}
    sut = jpaddress.AddressLookup()
    expected = address
    actual = sut["0010000"]
    assert actual == expected


def test_address_lookup_init_with_address_data_iterable() -> None:
    address0 = jpaddress.core.Address(
        zipcode="0010000",
        prefecture_kana="ホッカイドウ",
        city_kana="サッポロシ",
        town_kana="ミナミ",
        prefecture_kanji="北海道",
        city_kanji="札幌市",
        town_kanji="南",
        prefecture="北海道",
        city="札幌市",
        town="南",
        prefecture_romaji="Hokkaido",
        city_romaji="Sapporo-shi",
        town_romaji="Minami",
    )
    address1 = jpaddress.core.Address(
        zipcode="0010001",
        prefecture_kana="トウキョウト",
        city_kana="トウキョウシ",
        town_kana="ミナトマチ",
        prefecture_kanji="東京都",
        city_kanji="東京市",
        town_kanji="港町",
        prefecture="東京都",
        city="東京市",
        town="港町",
        prefecture_romaji="Tokyo-to",
        city_romaji="Tokyo-shi",
        town_romaji="Minato-machi",
    )
    sut = jpaddress.AddressLookup([address0, address1])
    expected = address0
    actual = sut["0010000"]
    assert actual == expected


def test_address_lookup_raises_error_when_zipcode_is_not_found(mocker: MockerFixture) -> None:
    from jittok.jpaddress.exceptions import ZipcodeNotFoundError

    from_japanpost_zipfile = mocker.patch("jittok.jpaddress.AddressLookup.from_japanpost_zipfile")
    from_japanpost_zipfile.return_value = {}
    sut = jpaddress.AddressLookup()
    with pytest.raises(ZipcodeNotFoundError):
        sut["0010000"]


def test_address_lookup_search(mocker: MockerFixture) -> None:
    address0 = jpaddress.core.Address(
        zipcode="0010000",
        prefecture_kana="ホッカイドウ",
        city_kana="サッポロシ",
        town_kana="ミナミ",
        prefecture_kanji="北海道",
        city_kanji="札幌市",
        town_kanji="南",
        prefecture="北海道",
        city="札幌市",
        town="南",
        prefecture_romaji="Hokkaido",
        city_romaji="Sapporo-shi",
        town_romaji="Minami",
    )
    address1 = jpaddress.core.Address(
        zipcode="0010001",
        prefecture_kana="トウキョウト",
        city_kana="トウキョウシ",
        town_kana="ミナトマチ",
        prefecture_kanji="東京都",
        city_kanji="東京市",
        town_kanji="港町",
        prefecture="東京都",
        city="東京市",
        town="港町",
        prefecture_romaji="Tokyo-to",
        city_romaji="Tokyo-shi",
        town_romaji="Minato-machi",
    )

    from_japanpost_zipfile = mocker.patch("jittok.jpaddress.AddressLookup.from_japanpost_zipfile")
    from_japanpost_zipfile.return_value = {"0010000": address0, "0010001": address1}
    sut = jpaddress.AddressLookup()
    expected = iter([address0])
    actual = sut.search("北海")
    assert list(actual) == list(expected)


def test_address_lookup_getitem_removes_hyphen() -> None:
    address = jpaddress.core.Address(
        zipcode="0010000",
        prefecture_kana="ホッカイドウ",
        city_kana="サッポロシ",
        town_kana="ミナミ",
        prefecture_kanji="北海道",
        city_kanji="札幌市",
        town_kanji="南",
        prefecture="北海道",
        city="札幌市",
        town="南",
        prefecture_romaji="Hokkaido",
        city_romaji="Sapporo-shi",
        town_romaji="Minami",
    )
    sut = jpaddress.AddressLookup([address])
    expected = address
    actual = sut["001-0000"]
    assert actual == expected
