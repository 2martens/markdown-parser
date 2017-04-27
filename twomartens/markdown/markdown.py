# -*- coding: utf-8 -*-

#   Copyright 2017 Jim Martens
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""markdown.markdown: provides entry point main()."""


import argparse

import modgrammar

from .parser import parse as markdown_parse
from .transform import transform

__version__ = "1.0.0.a1"


def main():
    """The entry point of the application. Glues the various parts of the application together."""
    parser = argparse.ArgumentParser(description="Parses markdown and produces an HTML representation.")
    parser.add_argument("-f", "--format", dest="format", default="html", choices=["html"],
                        help="This describes the output format.")
    parser.add_argument("input", metavar="input", type=argparse.FileType('r'), help="The input file in markdown")
    parser.add_argument("output", metavar="output", type=argparse.FileType('w'), help="The output file")
    
    args = parser.parse_args()

    # load file content
    markdown = args.input.read()

    try:
        # parse markdown
        structure = markdown_parse(markdown)

        # compile output
        output = transform(structure, args.format)

        # write output
        args.output.write(output)

        # give feedback to console
        print("The output file has been written.")
    except modgrammar.ParseError as pe:
        # the input is no valid markdown as per our grammar definition
        raise pe
