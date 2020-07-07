"""Python Library for LTSV."""

from . import read
from . import write

breader = read.breader
reader = read.reader
ParserConfigError = read.BaseLineParser.ParserConfigError
ParseError = read.BaseLineParser.ParseError
EmptyFieldParseError = read.BaseLineParser.EmptyFieldParseError
LabelOnlyParseError = read.BaseLineParser.LabelOnlyParseError
InvalidLabelParseError = read.BaseLineParser.InvalidLabelParseError
InvalidValueParseError = read.BaseLineParser.InvalidValueParseError

bwriter = write.bwriter
writer = write.writer
FormatterConfigError = write.BaseLineFormatter.FormatterConfigError
FormatError = write.BaseLineFormatter.FormatError
InvalidInputFormatError = write.BaseLineFormatter.InvalidInputFormatError
InvalidValueFormatError = write.BaseLineFormatter.InvalidValueFormatError
