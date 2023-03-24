import os
import sys
from setuptools import setup

from jittok import __author__, __description__, __email__, __package_name__, __version__

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"), "r") as fin:
    __long_description__ = fin.read()

install_requires = ["regex", "pykakasi"]
dev_extras_require = ["flake8", "pytest", "black", "mypy", "tox", "isort", "types-regex", "pytest-mock"]

if sys.version_info < (3, 7):
    install_requires += ["dataclasses"]
    dev_extras_require += ["types-dataclasses"]

setup(
    name=__package_name__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    license="MIT",
    url="https://github.com/osoken/jittok",
    description=__description__,
    long_description=__long_description__,
    long_description_content_type="text/markdown",
    package_data={__package_name__: ["py.typed"]},
    packages=[
        __package_name__,
        f"{__package_name__}.jptext",
        f"{__package_name__}.jpdatetime",
        f"{__package_name__}.jpaddress",
    ],
    install_requires=install_requires,
    extras_require={
        "dev": dev_extras_require,
    },
)
