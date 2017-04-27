# coding=utf-8

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

"""markdown.compiler: provides compiling functionality"""
import os
from string import Template

import modgrammar

from .grammars import Heading

TAB_SEP = "    "


def transform(structure: modgrammar.Grammar, output_format: str) -> str:
    """Transforms the given structure into the given output format.

    :param modgrammar.Grammar structure: 
    :param str output_format: the output format
    """
    return globals().get("_" + output_format + "_transform")(structure)


def _html_transform(structure: modgrammar.Grammar) -> str:
    """Transforms the given structure into HTML and returns the finished output.
    
    The first heading in the markdown text will be used for the HTML title element.
    
    :param modgrammar.Grammar structure: the structure which is transformed
    """
    replacements = {"unordered_list": "ul", "quote": "blockquote", "ordered_list": "ol"}
    elements = _extract_elements(structure, replacements)

    script_dir = os.path.dirname(__file__)
    filename = "templates/skeleton.html"
    with open(os.path.join(script_dir, filename)) as file:
        html = file.read()

    template = Template(html)
    content = ""
    heading = structure.find(Heading)
    title = heading.text

    for tag, text, children, attributes, options in elements:
        if content != "":
            content = content + "\n"
        content = content + _html_build_block(tag, children, text, attributes, options)

    output = template.substitute(title=title, content=content)
    return output


def _html_build_block(tag: str, elements: list, text: str = None, attributes: map = None, options: map = None,
                      nesting: int = 1) -> str:
    """Builds an HTML block element and returns the HTML output.
    
    Level 1 elements are indented by four spaces. Level 2 elements are indented by 8 spaces and so on.
    Level 1 elements with children get their tags on a separate line. The tags of level 2 (or higher) elements are on
    the same line with the rest of the content.
    
    Parameters
    ----------
    :param str tag: the HTML tag for this block element
    :param list elements: a list of all the child elements
    :param str text: the text of the block element between the HTML tags if available
    :param map attributes: a map of all attributes of this block element
    :param map options: a map of options for this block element
    :param int nesting: the level this block is on (e.g. direct child of body element is on level 1)
    """
    attributes = attributes if attributes is not None else {}
    default_options = {"indentation": True, "onlyOuterLinebreaks": False}
    options = {**default_options, **options} if options is not None else default_options
    content = (nesting * TAB_SEP) + "<" + tag + _html_build_attributes(attributes) + ">"
    inserted_linebreaks = 0
    inserted_indents = 0
    if len(elements) == 0 and text is not None:
        content = content + text
    for _tag, _text, _children, _attributes, _options in elements:
        _options = {**default_options, **_options} if _options is not None else default_options
        if nesting == 1 and options["indentation"] and ((options["onlyOuterLinebreaks"] and inserted_linebreaks == 0)
                                                        or (not options["onlyOuterLinebreaks"])):
            content = content + "\n"
            inserted_linebreaks += 1
        if _text is not None and len(_children) == 0:
            indent = ((nesting + 1) * TAB_SEP)
            if (nesting == 1 and options["indentation"]
                and (not options["onlyOuterLinebreaks"]
                     or (options["onlyOuterLinebreaks"] and inserted_indents == 0))):
                content += indent
                inserted_indents += 1
            content += _html_build_item(_tag, _text, _attributes, _tag != "text")
        else:
            content = content + _html_build_block(_tag, _children, _text, _attributes, _options, nesting + 1)
    if nesting == 1 and len(elements) and options["indentation"]:
        content = content + "\n" + (nesting * TAB_SEP)
    content = content + "</" + tag + ">"
    return content


def _html_build_item(tag: str, text: str, attributes: map = None, include_tags=True) -> str:
    """Builds an HTML inline element and returns the HTML output.
    
    :param str tag: the HTML tag
    :param str text: the text between the HTML tags
    :param map attributes: map of attributes
    :param bool include_tags: True if the tags should be part of the output
    """
    attributes = attributes if attributes is not None else {}
    opening_tag = "<" + tag + _html_build_attributes(attributes) + ">"
    closing_tag = "</" + tag + ">"
    if include_tags:
        return opening_tag + text + closing_tag
    else:
        return text


def _html_build_attributes(attributes: map) -> str:
    """Builds the attributes and returns the HTML output.

    :param map attributes: map of attributes 
    """
    result = ""
    for name in attributes:
        if result != "":
            result += " "
        result += name + '="' + attributes[name] + '"'

    if result != "":
        result = " " + result

    return result


def _extract_elements(structure: modgrammar.Grammar, replacements: map = None) -> list:
    """Extracts the relevant data for all elements in the given structure and returns it in a list.
    
    This data includes the tag, text, children, attributes and options.
    
    :param modgrammar.Grammar structure: the structure from which the elements are extracted
    :param map replacements: an optional map of replacements for found tags 
    """
    elements = []

    for elem in structure.elements:
        tag = elem.tag if hasattr(elem, "tag") else None
        text = elem.text if hasattr(elem, "text") else None
        children = []
        attributes = elem.attributes if hasattr(elem, "attributes") else {}
        options = elem.options if hasattr(elem, "options") else {}
        if replacements is not None and tag is not None:
            tag = replacements[tag] if tag in replacements else tag
        if (tag is None or text is None) and hasattr(elem, "elements") and len(elem.elements):
            children = _extract_elements(elem)
        if tag is not None:
            elements.append((tag, text, children, attributes, options))
        elif len(children):
            elements = elements + children

    return elements
