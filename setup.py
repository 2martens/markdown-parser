# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('twomartens.markdown/markdown.py').read(),
    re.M
).group(1)

with open("README.md", "rb") as f:
    long_desc = f.read().decode("utf-8")

setup(
    name="twomartens.markdown",
    packages=["twomartens.markdown"],
    entry_points={
        "console_scripts": ['markdown = twomartens.markdown.markdown:main']
    },
    version=version,
    description="Markdown parser that renders the markdown in HTML",
    long_description=long_desc,
    author="Jim Martens",
    author_email="github@2martens.de",
    url="https://github.com/frmwrk123/markdown-parser",
)
