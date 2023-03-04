import os

from jittok import blob

work_dir = os.path.dirname(os.path.abspath(__file__))
fixtures_dir = os.path.join(work_dir, "fixtures")


def test_open_zipfile() -> None:
    with open(os.path.join(fixtures_dir, "zipcode_mid.csv"), "rb") as fin:
        expected = fin.read()

    with blob.open_zipfile(os.path.join(fixtures_dir, "zipcodes.zip"), "zipcode_mid.csv") as sut:
        actual = sut.read()

    assert actual == expected
