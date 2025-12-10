# w1_py_parse

A Python parser for Texas RRC W-1 data files.

## Description

This tool allows for parsing fixed-width data files from the Texas Railroad Commission, specifically handling schema format 01.

## Installation

```bash
pip install w1_py_parse
```

## Usage

```python
from w1_py_parse.parser import RRCParser

parser = RRCParser()
result = parser.parse("path/to/data.dat")
print(result.header)
print(result.records)
```

## Credits

**Made almost entirely with Google DeepMind's Gemini 3 Pro.**

This project serves as a demonstration of the capabilities of advanced AI in software development.
