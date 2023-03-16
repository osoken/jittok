from datetime import datetime

import pytest

from jittok.jpdatetime import strptime


@pytest.mark.parametrize(
    ["datestring", "formatstring", "expected"],
    [
        ("2019-01-01", "%Y-%m-%d", datetime(2019, 1, 1)),
        ("2019-01-01 00:00:00", "%Y-%m-%d %H:%M:%S", datetime(2019, 1, 1)),
        ("昭和64年1月1日", "%Y年%m月%d日", datetime(1989, 1, 1)),
        ("平成31年1月1日", "%Y年%m月%d日", datetime(2019, 1, 1)),
        ("令和元年1月1日", "%Y年%m月%d日", datetime(2019, 1, 1)),
        ("令和2年1月1日", "%Y年%m月%d日", datetime(2020, 1, 1)),
        ("明治7年10月11日", "%Y年%m月%d日", datetime(1874, 10, 11)),
        ("大正元年", "%Y年", datetime(1912, 1, 1)),
        ("昭和元年", "%Y年", datetime(1926, 1, 1)),
        ("平成元年", "%Y年", datetime(1989, 1, 1)),
        ("令和元年", "%Y年", datetime(2019, 1, 1)),
    ],
)
def test_jpdatetime_strptime(datestring: str, formatstring: str, expected: datetime) -> None:
    """Test jpdatetime.strptime()"""
    actual = strptime(datestring, formatstring)
    assert actual == expected
