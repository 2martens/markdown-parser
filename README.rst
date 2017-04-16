Markdown Parser
===============

This program was created in the context of the code competition of it-talents.com in 
April 2017. It is split into two main components. The parser side takes the Markdown
input and creates an internal representation. The renderer component uses the internal
representation and creates the HTML output. 

In general the system is designed to be modular and expandable. For example a renderer
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

1. Clone the [GitHub repository](https://github.com/frmwrk123/markdown-parser) 
2. Run ``python markdown-runner.py`` to use the tool

Usage
-----

The usage is very easy. Once installed you can use ``tm-parse-markdown`` to access the program. Alternatively use
``python markdown-runner.py`` instead if you followed the Git way. The rest applies to both forms in the same way.
The program accepts two parameters. The first needs to be the name of a file containing Markdown code. The second
parameter has to be the name of the output file. The file doesn't have to exist already but if it does it will be
overwritten completely. The output file will contain the markup in the selected output format (as of now it is always
HTML).

To allow for easier extension the program accepts the ``-r, --renderer`` option. It can be used to specify the output
format. Currently only HTML is supported which is also selected by default. Therefore it is not required to specify
the option for the program to work.

Example::

   tm-parse-markdown my-markdown-file.md my-html-file.html


Example (with option)::

   tm-parse-markdown --renderer html my-markdown-file.md my-html-file.html

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

Lists
^^^^^

Currently only unordered lists are supported. The list items have to start with ``* `` at the beginning of the line.
An empty line must precede a list.

Example::


   * this starts a list
   * which continues here
   * and here

   * but this is a new list
   * which even contains **bold text** and *italic text*

Quotes
^^^^^^

As of now only block quotes are supported. Inline quotes might be added later.

Examples::

   > This starts a one line quote.

   > A new quote starts here
   > and continues in the next line.
   > It can contain **not rendered bold text** and *not rendered italic text*.

Paragraphs
^^^^^^^^^^

Paragraphs are naturally supported as well. They are separated from each other with empty lines.
