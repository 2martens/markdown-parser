# coding=utf-8

"""markdown.parser: provides parsing capability"""
import modgrammar

from .grammars import MarkdownGrammar


def parse(text: str) -> modgrammar.Grammar:
    """Parses the given text and returns a result object.
    
    :param str text: the input text
    """
    parser = MarkdownGrammar.parser()
    return parser.parse_string(text)
