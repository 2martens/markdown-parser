# coding=utf-8

"""markdown.renderer: provides rendering functionality"""
import os
from string import Template

import modgrammar

from .grammars import Heading


TAB_SEP = "    "


def render(structure: modgrammar.Grammar, output_format: str) -> str:
    """Renders the given structure in the given output format.

    :param modgrammar.Grammar structure: 
    :param str output_format: the output format
    """
    return globals().get("_" + output_format + "_render")(structure)


def _html_render(structure: modgrammar.Grammar) -> str:
    """Renders the given structure in HTML and returns the finished output.
    
    :param modgrammar.Grammar structure: the structure which is rendered
    """
    replacements = {"list": "ul", "quote": "blockquote"}
    elements = _extract_elements(structure, replacements)

    script_dir = os.path.dirname(__file__)
    filename = "templates/skeleton.html"
    with open(os.path.join(script_dir, filename)) as file:
        html = file.read()

    template = Template(html)
    content = ""
    heading = structure.find(Heading)
    title = heading.text

    for tag, text, children in elements:
        if content != "":
            content = content + "\n"
        content = content + _html_render_block(tag, children, text)

    output = template.substitute(title=title, content=content)
    return output


def _html_render_block(tag: str, elements: list, text: str = None, nesting: int = 1) -> str:
    content = (nesting * TAB_SEP) + "<" + tag + ">"
    if len(elements) == 0 and text is not None:
        content = content + text
    for _tag, _text, _children in elements:
        if nesting == 1:
            content = content + "\n"
        if _text is not None and len(_children) == 0:
            content = content + \
                      (
                          ((nesting + 1) * TAB_SEP) if nesting == 1 else ""
                      ) + \
                      _html_render_item(_tag, _text, _tag != "text")
        else:
            content = content + _html_render_block(_tag, _children, _text, nesting + 1)
    if nesting == 1 and len(elements):
        content = content + "\n" + (nesting * TAB_SEP)
    content = content + "</" + tag + ">"
    return content


def _html_render_item(tag: str, text: str, include_tags=True) -> str:
    opening_tag = "<" + tag + ">"
    closing_tag = "</" + tag + ">"
    if include_tags:
        return opening_tag + text + closing_tag
    else:
        return " " + text


def _extract_elements(structure: modgrammar.Grammar, replacements: map = None) -> list:
    elements = []

    for elem in structure.elements:
        tag = elem.tag if hasattr(elem, "tag") else None
        text = elem.text if hasattr(elem, "text") else None
        children = []
        if replacements is not None and tag is not None:
            tag = replacements[tag] if tag in replacements else tag
        if (tag is None or text is None) and hasattr(elem, "elements") and len(elem.elements):
            children = _extract_elements(elem)
        if tag is not None:
            elements.append((tag, text, children))
        elif len(children):
            elements = elements + children

    return elements
