# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('twomartens/markdown/markdown.py').read(),
    re.M
).group(1)

with open("README.md", "rb") as f:
    long_desc = f.read().decode("utf-8")

setup(
    name="twomartens.markdown",
    namespace_packages=["twomartens"],
    packages=["twomartens.markdown"],
    entry_points={
        "console_scripts": ['tm-parse-markdown = twomartens.markdown.markdown:main']
    },
    version=version,
    package_data={"twomartens.markdown": ["templates/skeleton.*"]},
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    description="Markdown parser that renders the markdown in HTML",
    long_description=long_desc,
    author="Jim Martens",
    author_email="github@2martens.de",
    url="https://github.com/frmwrk123/markdown-parser",
)
