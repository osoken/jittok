import os

from pytest_mock import MockerFixture

from jittok import blob

work_dir = os.path.dirname(os.path.abspath(__file__))
fixtures_dir = os.path.join(work_dir, "fixtures")


def test_open_zipfile() -> None:
    with open(os.path.join(fixtures_dir, "zipcode_mid.csv"), "rb") as fin:
        expected = fin.read()

    with blob.open_zipfile(os.path.join(fixtures_dir, "zipcodes.zip"), "zipcode_mid.csv") as sut:
        actual = sut.read()

    assert actual == expected


def test_save_resource_from_http_request_in_temporary_file(mocker: MockerFixture) -> None:
    from io import BytesIO

    urlopen = mocker.patch("jittok.blob.core.urlopen")
    urlopen.return_value.__enter__.return_value = BytesIO(b"test")
    with blob.save_resource_from_http_request_in_temporary_file("http://example.com") as sut:
        with open(sut.name, "rb") as fin:
            actual = fin.read()
    assert actual == b"test"
