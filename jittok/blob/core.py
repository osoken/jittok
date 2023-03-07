import sys
import zipfile
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
from typing import IO
from urllib.request import urlopen

if sys.version_info >= (3, 9):
    from collections.abc import Generator
else:
    from typing import Generator


def open_zipfile(zipfile_path: str, filename: str) -> IO[bytes]:
    """Open a file in a zip file.

    Args:
        zipfile_path (str): Path to the zip file.
        filename (str): Name of the file to open.

    Returns:
        IO[bytes]: File object.
    """
    with zipfile.ZipFile(zipfile_path, "r") as zf:
        return zf.open(filename)


@contextmanager
def save_resource_from_http_request_in_temporary_file(url: str) -> Generator[IO[bytes], None, None]:
    """Save a resource from an HTTP request in a temporary file.

    Args:
        url (str): URL.

    Returns:
        IO[bytes]: File object.
    """

    with NamedTemporaryFile() as tmp:
        with urlopen(url) as res:
            tmp.write(res.read())
        tmp.seek(0)
        yield tmp
