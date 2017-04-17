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

"""markdown.grammars: Contains the grammars for markdown."""
import html
import re

import modgrammar

grammar_whitespace_mode = "explicit"
grammar_whitespace = modgrammar.WS_NOEOL


class SingleWhitespace(modgrammar.SPACE):
    """Defines the grammar for a single whitespace character"""
    grammar_max = 1
    regexp = re.compile('[^\S' + modgrammar.util.EOL_CHARS + '\t]')


class SimpleText(modgrammar.Grammar):
    """Defines the grammar for simple text."""
    grammar = (modgrammar.REPEAT(SingleWhitespace, min=0, max=3, collapse=True),
               modgrammar.WORD(startchars="^\s#>*[`", restchars="^*[<`" + modgrammar.util.EOL_CHARS, escapes=True,
                               fullmatch=True))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        spaces = ""
        for elem in self.find_all(SingleWhitespace):
            spaces += elem.string
        self.text = spaces + self[1].string
        self.tag = "text"


class EmptyLine(modgrammar.Grammar):
    """Defines the grammar for an empty line."""
    grammar = (modgrammar.BOL, modgrammar.OPTIONAL(modgrammar.SPACE), modgrammar.EOL)


class Heading(modgrammar.Grammar):
    """Defines the grammar for a heading."""
    grammar = (modgrammar.BOL, modgrammar.REPEAT(modgrammar.L("#"), min=1, max=6),
               modgrammar.L(" "), modgrammar.REST_OF_LINE, modgrammar.EOL)

    def grammar_elem_init(self, sessiondata):
        """Saves the headline for later use."""
        self.text = self[3].string
        hashtags = self[1].string
        self.tag = "h" + str(len(hashtags))


class Bold(modgrammar.Grammar):
    """Defines the grammar for bold text."""
    grammar = (modgrammar.L("**"), modgrammar.WORD("^*" + modgrammar.util.EOL_CHARS, fullmatch=True),
               modgrammar.L("**"))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.text = self[1].string
        self.tag = "b"


class Italic(modgrammar.Grammar):
    """Defines the grammar for italic text."""
    grammar = (modgrammar.L("*"), modgrammar.WORD("^*" + modgrammar.util.EOL_CHARS, fullmatch=True), modgrammar.L("*"))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.text = self[1].string
        self.tag = "i"


class InlineCode(modgrammar.Grammar):
    """Defines the grammar for inline code segments."""
    grammar = (modgrammar.L("`"), modgrammar.WORD("^`" + modgrammar.util.EOL_CHARS, fullmatch=True), modgrammar.L("`"))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.text = html.escape(self[1].string)
        self.tag = "code"


class LinkTitle(modgrammar.Grammar):
    """Defines the grammar for a link title."""
    grammar = (modgrammar.WORD(startchars='^")' + modgrammar.util.EOL_CHARS, escapes=True, fullmatch=True))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.text = self[0].string


class AutomaticLink(modgrammar.Grammar):
    """Defines the grammar for an automatic link."""
    grammar = (modgrammar.L("<"), modgrammar.WORD(startchars="^[>\s`*", escapes=True, fullmatch=True),
               modgrammar.L(">"))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.text = self[1].string
        self.attributes = {"href": self[1].string}
        self.tag = "a"


class Link(modgrammar.Grammar):
    """Defines the grammar for a link."""
    grammar = (modgrammar.L("["), modgrammar.WORD(startchars="^]`*" + modgrammar.util.EOL_CHARS, fullmatch=True),
               modgrammar.L("]("), modgrammar.WORD(startchars="^\s)", escapes=True, fullmatch=True),
               modgrammar.OPTIONAL(modgrammar.L(' "'),
                                   LinkTitle,
                                   modgrammar.L('"')),
               modgrammar.L(")"))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.text = self[1].string
        self.attributes = {"href": self[3].string}
        link_title = self.find(LinkTitle)
        if link_title is not None:
            self.attributes["title"] = link_title.text
        self.tag = "a"


class QuoteLine(modgrammar.Grammar):
    """Defines the grammar for a single line quote."""
    grammar = (modgrammar.BOL, modgrammar.L(">"),
               modgrammar.REPEAT(modgrammar.OR(Bold, Italic, InlineCode, Link, AutomaticLink, SimpleText),
                                 collapse=True),
               modgrammar.EOL)

    grammar_collapse = False


class Quote(modgrammar.Grammar):
    """Defines the grammar for a quote."""
    grammar = (modgrammar.REPEAT(QuoteLine, min=1, collapse=True))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use and appends a space to each SimpleText that is followed by an EOL character."""
        self.tag = "quote"
        self.options = {"onlyOuterLinebreaks": True}
        highest_index = len(self.elements) - 1
        current_index = -1
        add_space_at_start = False
        for elem in self.elements:
            current_index += 1
            _length = len(elem.elements)
            _eol_index = _length - 1
            _first_content_index = 2
            _last_content_index = _eol_index - 1
            if add_space_at_start and elem[_first_content_index].grammar_name == "SimpleText":
                elem[_first_content_index].text = " " + elem[_first_content_index].text
                add_space_at_start = False
            if current_index < highest_index:
                if elem[_last_content_index].grammar_name == "SimpleText":
                    text = elem[_last_content_index].text.rstrip()
                    elem[_last_content_index].text = text + " "
                else:
                    add_space_at_start = True


class UnorderedListItem(modgrammar.Grammar):
    """Defines the grammar for an unordered list item."""
    grammar = (modgrammar.BOL, modgrammar.OR(modgrammar.L("* "), modgrammar.L("- "), modgrammar.L("+ ")),
               modgrammar.REPEAT(modgrammar.OR(Bold, Italic, InlineCode, Link, AutomaticLink, SimpleText),
                                 collapse=True))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.tag = "li"


class UnorderedList(modgrammar.Grammar):
    """Defines the grammar for an unordered list."""
    grammar = (EmptyLine, modgrammar.LIST_OF(UnorderedListItem, sep=modgrammar.EOL, collapse=True), modgrammar.EOL)

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.tag = "unordered_list"


class OrderedListItem(modgrammar.Grammar):
    """Defines the grammar for an unordered list item."""
    grammar = (modgrammar.BOL, modgrammar.WORD(startchars="0-9", fullmatch=True),
               modgrammar.L(". "), modgrammar.REPEAT(modgrammar.OR(Bold, Italic, InlineCode, Link, AutomaticLink,
                                                                   SimpleText), collapse=True))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.tag = "li"


class OrderedList(modgrammar.Grammar):
    """Defines the grammar for an unordered list."""
    grammar = (EmptyLine, modgrammar.LIST_OF(OrderedListItem, sep=modgrammar.EOL, collapse=True), modgrammar.EOL)

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.tag = "ordered_list"


class CodeBlock(modgrammar.Grammar):
    """Defines the grammar for a code block."""
    grammar = (modgrammar.REPEAT(modgrammar.BOL, modgrammar.L("    ") | modgrammar.L("\t"),
                                 modgrammar.REST_OF_LINE,
                                 modgrammar.EOL, collapse=True))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.tag = "code"
        text = ""
        for elem in self.find_all(modgrammar.REST_OF_LINE):
            if text != "":
                text += "\n"
            text += html.escape(elem.string)
        self.text = text
        self.options = {"indentation": False}


class PreBlock(modgrammar.Grammar):
    """Defines the grammar for a pre block."""
    grammar = (modgrammar.OPTIONAL(EmptyLine), CodeBlock, modgrammar.OPTIONAL(EmptyLine))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.tag = "pre"
        self.options = {"indentation": False}


class Text(modgrammar.Grammar):
    """Defines the grammar for normal text."""
    grammar = (modgrammar.REPEAT(
        modgrammar.BOL,
        modgrammar.REPEAT(modgrammar.OR(Bold, Italic, InlineCode, Link, AutomaticLink, SimpleText), collapse=True),
        modgrammar.EOL, collapse=True))

    def grammar_elem_init(self, sessiondata):
        """Appends a space to each SimpleText that is followed by an EOL character."""
        highest_index = len(self.elements) - 1
        current_index = -1
        add_space_at_start = False
        for elem in self.elements:
            current_index += 1
            _length = len(elem.elements)
            _eol_index = _length - 1
            _first_content_index = 1
            _last_content_index = _eol_index - 1
            if add_space_at_start and elem[_first_content_index].grammar_name == "SimpleText":
                elem[_first_content_index].text = " " + elem[_first_content_index].text
                add_space_at_start = False
            if current_index < highest_index:
                if elem[_last_content_index].grammar_name == "SimpleText":
                    text = elem[_last_content_index].text.rstrip()
                    elem[_last_content_index].text = text + " "
                else:
                    add_space_at_start = True


class Paragraph(modgrammar.Grammar):
    """Defines the grammar for a paragraph."""
    grammar = (modgrammar.OPTIONAL(EmptyLine), Text, modgrammar.OPTIONAL(EmptyLine))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.tag = "p"
        self.options = {"onlyOuterLinebreaks": True}


class MarkdownGrammar(modgrammar.Grammar):
    """Provides the grammar for Markdown."""
    grammar = (modgrammar.REPEAT(modgrammar.OR(Heading, UnorderedList, OrderedList, Quote, Paragraph,
                                               EmptyLine, PreBlock), collapse=True))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.content = self[0].string
