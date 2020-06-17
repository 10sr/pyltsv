"""Python Library for LTSV."""

from . import read

breader = read.breader
reader = read.reader
ParserConfigError = read.BaseLineParser.ParserConfigError
