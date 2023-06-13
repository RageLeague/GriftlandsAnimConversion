# GriftlandsAnimConversion

A python tool to help convert from Griftlands animation format to more useful formats.

## Prerequisites

- Python (3.10.6+)
- Pillow fork of PIL (9.0.1+)
- tkinter

## Griftlands Animation Formats

The format for Griftlands' animation is revealed to us by Kevin from Klei in the Griftlands Discord server. See the info folder for more info.

The data is encoded in binary in the order according to `format_structure.png`.

Integers are encoded as 32-bits, little endian (least significant byte first). Floats are 32-bit floats, little endian. Booleans are integers that can have value 0 or 1. Each string has a 32-bit integer signifying its length, followed by N bytes ASCII representation of the string (no null terminators), as explained by `(int, string)`.

## Notice

This tool is no longer being developed, because it is taking too much work, and there isn't really that much demand for it. I am leaving this repository up for future references. It has an implementation of the Griftlands Animation format and the reading/writing of it, but none of the conversion tools are actually in place. See `source/model/ganim_format.py` for the data structure and `source/model/ganim_io.py` for reading/writing it.

It has a GUI tool in place for reading/writing .tex files and .png files, though. Simply run `test.py` while having the prereqs installed.
