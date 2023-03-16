import re
from datetime import datetime


def strptime(date_string: str, format: str) -> datetime:
    """Convert a string to a datetime object according to a format string.

    Args:
        date_string (str): The string to convert.
        format (str): The format string.

    Returns:
        datetime: The datetime object.

    Raises:
        ValueError: If the string does not match the format.

    Examples:
        >>> from datetime import datetime
        >>> from jittok.jpdatetime import strptime
        >>> strptime("2019-01-01", "%Y-%m-%d")
        datetime.datetime(2019, 1, 1, 0, 0)
        >>> strptime("2019-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        datetime.datetime(2019, 1, 1, 0, 0)
        >>> strptime("昭和64年1月1日", "%Y年%m月%d日")
        datetime.datetime(1989, 1, 1, 0, 0)
        >>> strptime("平成31年1月1日", "%Y年%m月%d日")
        datetime.datetime(2019, 1, 1, 0, 0)
        >>> strptime("令和元年1月1日", "%Y年%m月%d日")
        datetime.datetime(2019, 1, 1, 0, 0)
        >>> strptime("令和2年1月1日", "%Y年%m月%d日")
        datetime.datetime(2020, 1, 1, 0, 0)
    """
    return datetime.strptime(convert_wareki_year_to_seireki_year(date_string), format)


_era_regex_year = (
    (re.compile("令和(?P<y>[元0-9]+)"), 2018),
    (re.compile("平成(?P<y>[元0-9]+)"), 1988),
    (re.compile("昭和(?P<y>[元0-9]+)"), 1925),
    (re.compile("大正(?P<y>[元0-9]+)"), 1911),
    (re.compile("明治(?P<y>[元0-9]+)"), 1867),
)


def convert_wareki_year_to_seireki_year(date_string: str) -> str:
    for era_regex, year in _era_regex_year:
        m = re.search(era_regex, date_string)
        if m is not None:
            return f'{date_string[:m.start()]}{int(m.group("y").replace("元", "1")) + year}{date_string[m.end():]}'
    return date_string
