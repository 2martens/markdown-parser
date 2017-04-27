Markdown Parser
===============

This program was created in the context of the code competition of it-talents.com in 
April 2017. It is split into two main components. The parser side takes the Markdown
input and creates an internal representation. The transform component uses the internal
representation and creates the HTML output. 

In general the system is designed to be modular and expandable. For example a transformation
for LaTeX could be relatively easily added.

Installation
------------

Easy way
^^^^^^^^

Use the package manager of Python::

   pip install twomartens.markdown

A bit more complicated
^^^^^^^^^^^^^^^^^^^^^^

1. Download the package from the `PyPi <https://pypi.python.org/pypi/twomartens.markdown/>`_
2. Extract the files
3. Run ``python setup.py install`` from the directory you extracted the files to

The Git way (No actual installation)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Clone the `GitHub repository <https://github.com/frmwrk123/markdown-parser>`_
2. Run ``python markdown-runner.py`` to use the tool

Usage
-----

The usage is very easy. Once installed you can use ``tm-parse-markdown`` to access the program. Alternatively use
``python markdown-runner.py`` instead if you followed the Git way. The rest applies to both forms in the same way.
The program accepts two parameters. The first needs to be the name of a file containing Markdown code. The second
parameter has to be the name of the output file. The file doesn't have to exist already but if it does it will be
overwritten completely. The output file will contain the markup in the selected output format (as of now it is always
HTML).

To allow for easier extension the program accepts the ``-f, --format`` option. It can be used to specify the output
format. Currently only HTML is supported which is also selected by default. Therefore it is not required to specify
the option for the program to work.

Example::

   tm-parse-markdown my-markdown-file.md my-html-file.html


Example (with option)::

   tm-parse-markdown --format html my-markdown-file.md my-html-file.html

Markdown Syntax
---------------

The markdown parser supports the following syntax. More might be added later.

Headings
^^^^^^^^

All headings from H1 to H6 are supported.

Examples::

   # H1 heading
   ## H2 heading
   ### H3 heading
   #### H4 heading
   ##### H5 heading
   ###### H6 heading

Bold text
^^^^^^^^^

Bold text is supported.

Example::

    **bold text**
    the **bold text** can even appear in normal paragraphs

Italic text
^^^^^^^^^^^

Italic text is supported.

Example::

   *some italic text*
   the *italic text* can also appear in paragraphs

Inline code
^^^^^^^^^^^

Inline code segments are supported.

Example::

   a paragraph with `inline code`

Links
^^^^^

The parser supports links.

Example::

   a paragraph with [a link](https://example.com "title")

   another with another [link](https://example.com)
   or for change an automatic link <https://example.com>

Lists
^^^^^

Both unordered and ordered lists are supported. The list items for unordered lists have to start their line with
``*``, ``-`` or ``+`` immediately followed by a space. These symbols can be used interchangeably even within one list.
An empty line must precede a list.

Example::


   * this starts a list
   * which continues here
   * and here
   - even here
   + and here

   * but this is a new list
   * which even contains **bold text** and *italic text*
   * or an `inline code segment`
   * or a [link](https://example.com), <https://example.com>

The list items of ordered lists have to start with numbers (``0-9``), followed by a dot (``.``) and a space.
It doesn't matter for the output which numbers stand in front of the dot.

Example::


   1.  this starts an ordered list
   2.  which is continued here
   9.  and here
   0.  it can also contain **bold text**
   11. and *italic text*
   99. and `inline code`
   42. and a [link](https://example.com "title"), <https://example.com>

   0. a new list is started here

Quotes
^^^^^^

As of now only block quotes are supported. Inline quotes might be added later.

Examples::

   > This starts a one line quote.

   > A new quote starts here
   > and continues in the next line.
   > It can contain **bold text** and *italic text*.
   > inline `code blocks` are also possible
   > The same goes for [links](https://example.com), <https://example.com>

Code blocks
^^^^^^^^^^^

Code blocks are supported. They have to be preceded and followed by an empty line. Each line must start with either 4
spaces or one tab. The text is encoded so that you can easily use for example HTML tags in a code block. Further spaces
beyond these four spaces or one tab are represented in the output unchanged.

Example::

   <!DOCTYPE html>
   <html>
       <head>
           <title>Test</title>
       </head>
       <body>
       </body>
   </html>

Paragraphs
^^^^^^^^^^

Paragraphs are naturally supported as well. They are separated from each other with empty lines.

Example::

   A paragraph starts here. It contains **bold text** or *italic text*.
   It continues in the next line with a `code segment`.
   Finally there are also [links](https://example.com "title")

   This text belongs to a new paragraph.

