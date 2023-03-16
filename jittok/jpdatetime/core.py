import re
from datetime import datetime


def strptime(date_string: str, format: str) -> datetime:
    """Convert a string to a datetime object according to a format string."""
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
