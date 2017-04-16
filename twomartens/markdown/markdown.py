# -*- coding: utf-8 -*-


"""markdown.markdown: provides entry point main()."""


import argparse

import modgrammar

from .parser import parse as markdown_parse
from .renderer import render

__version__ = "1.0.0.dev4"


def main():
    """The entry point of the application. Glues the various parts of the application together."""
    parser = argparse.ArgumentParser(description="Parses markdown and produces an HTML representation.")
    parser.add_argument("-r", "--renderer", dest="renderer", default="html", choices=["html"],
                        help="This describes the output format.")
    parser.add_argument("input", metavar="input", type=argparse.FileType('r'), help="The input file in markdown")
    parser.add_argument("output", metavar="output", type=argparse.FileType('w'), help="The output file")
    
    args = parser.parse_args()

    # load file content
    markdown = args.input.read()

    try:
        # parse markdown
        structure = markdown_parse(markdown)

        # render output
        output = render(structure, args.renderer)

        # write output
        args.output.write(output)

        # give feedback to console
        print("The output file has been written.")
    except modgrammar.ParseError as pe:
        # the input is no valid markdown as per our grammar definition
        raise pe
