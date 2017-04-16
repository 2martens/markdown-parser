# Markdown Parser

This program was created in the context of the code competition of it-talents.com in 
April 2017. It is split into two main components. The parser side takes the Markdown
input and creates an internal representation. The renderer component uses the internal
representation and creates the HTML output. 

In general the system is designed to be modular and expandable. For example a renderer
for LaTeX could be relatively easily added.

## Installation

### Easy way

Use the package manager of Python.

```
pip install twomartens.markdown
```

### A bit more complicated
  
1. Download the package from the [PyPi](https://pypi.python.org/pypi/twomartens.markdown/).
2. Extract the files
3. Run `python setup.py install` from the directory you extracted the files to

### The Git way (No actual installation)

1. Clone the [GitHub repository](https://github.com/frmwrk123/markdown-parser) 
2. Run `python markdown-runner.py` to use the tool

## Usage

