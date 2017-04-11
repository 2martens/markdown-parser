# -*- coding: utf-8 -*-


"""markdown.markdown: provides entry point main()."""


import argparse


__version__ = "0.1.0"


def main():
    parser = argparse.ArgumentParser(description="Parses markdown and produces an HTML representation.")
    parser.add_argument("-r", "--renderer", dest="renderer", default="html", choices=["html"],
                        help="This describes the output format.")
    parser.add_argument("input", metavar="input", type=argparse.FileType('r'), help="The input file in markdown")
    parser.add_argument("output", metavar="output", type=argparse.FileType('w'), help="The output file")
    
    args = parser.parse_args()
