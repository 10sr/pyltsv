"""Python Library for LTSV."""

from . import read

breader = read.breader
reader = read.reader
ParserConfigError = read.BaseLineParser.ParserConfigError
ParseError = read.BaseLineParser.ParseError
EmptyFieldParseError = read.BaseLineParser.EmptyFieldParseError
LabelOnlyParseError = read.BaseLineParser.LabelOnlyParseError
InvalidLabelParseError = read.BaseLineParser.InvalidLabelParseError
InvalidValueParseError = read.BaseLineParser.InvalidValueParseError
