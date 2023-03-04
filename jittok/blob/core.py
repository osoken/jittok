import zipfile
from typing import IO


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
