# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('twomartens/markdown/markdown.py').read(),
    re.M
).group(1)

with open("README.rst", "rb") as f:
    long_desc = f.read().decode()

setup(
    name="twomartens.markdown",
    namespace_packages=["twomartens"],
    packages=["twomartens.markdown"],
    entry_points={
        "console_scripts": ['tm-parse-markdown = twomartens.markdown.markdown:main']
    },
    version=version,
    package_data={"twomartens.markdown": ["templates/skeleton.*"]},
    license="Apache Software License",
    install_requires=["modgrammar"],
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Environment :: Console",
        "Topic :: Text Processing :: Markup",
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
