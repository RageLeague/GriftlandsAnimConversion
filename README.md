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
