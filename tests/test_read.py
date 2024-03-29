# mypy: allow-untyped-decorators
# -*- coding: utf-8 -*-
"""Test reader."""

import unittest

from typing import List
from typing import Optional
from typing import Text
from typing import Tuple

from parameterized import parameterized
from six import BytesIO
from six import StringIO

import pyltsv

from pyltsv.read import BytesLineParser
from pyltsv.read import StrLineParser


class TestReader(unittest.TestCase):
    """Test reader."""

    def test_iter(self):
        # type: () -> None
        """Test basic usage of reader."""
        f = StringIO(u"a:1\tb:2\n\na:3\tb:4\n")
        ret = list(pyltsv.reader(f))
        self.assertEqual(len(ret), 3)
        self.assertEqual(list(ret[0]), [(u"a", u"1"), (u"b", u"2")])
        self.assertEqual(list(ret[1]), [])
        self.assertEqual(list(ret[2]), [(u"a", u"3"), (u"b", u"4")])
        return

    def test_readline(self):
        # type: () -> None
        """Test readline of reader."""
        f = StringIO(u"a:1\tb:2\n\na:3\tb:4\n")
        r = pyltsv.reader(f)
        self.assertEqual(list(r.readline() or []), [(u"a", u"1"), (u"b", u"2")])
        self.assertEqual(list(r.readline() or []), [])
        self.assertEqual(list(r.readline() or []), [(u"a", u"3"), (u"b", u"4")])
        self.assertEqual(r.readline(), None)  # end of file
        return

    def test_invalid_strict_setup(self):
        # type: () -> None
        """Test invalid setup of strict mode."""
        f = StringIO(u"a:1\tb:2\n\na:3\tb:4\n")
        with self.assertRaises(pyltsv.ParserConfigError):
            _ = pyltsv.reader(f, strict=True, delimiter=",")
        return


class TestBreader(unittest.TestCase):
    """Test breader."""

    def test_iter(self):
        # type: () -> None
        """Test basic usage of breader."""
        f = BytesIO(b"a:1\tb:2\n\na:3\tb:4\n")
        ret = list(pyltsv.breader(f))
        self.assertEqual(len(ret), 3)
        self.assertEqual(list(ret[0]), [(b"a", b"1"), (b"b", b"2")])
        self.assertEqual(list(ret[1]), [])
        self.assertEqual(list(ret[2]), [(b"a", b"3"), (b"b", b"4")])
        return


class TestStrLineParser(unittest.TestCase):
    """Test StrLineParser."""

    @parameterized.expand(
        [
            ("basic", u"a:1\tb:2\n", [(u"a", u"1"), (u"b", u"2")]),
            ("crlf", u"a:1\tb:2\r\n", [(u"a", u"1"), (u"b", u"2")]),
            ("empty", u"\n", []),
            ("labelonly", u"a\n", [(u"a", "")]),
            ("emptyvalue", u"a:\n", [(u"a", u"")]),
            ("emptykey", u":1\n", [(u"", u"1")]),
            (
                "blankfield",
                u"\ta:1\t\tb:2\n",
                [(u"a", u"1"), (u"b", u"2")],
            ),
            # When directly passed newlines are allowed when strict=False
            (
                "newlineinside",
                u"\ta:1\n\t\tb:2\n",
                [(u"a", u"1\n"), (u"b", u"2")],
            ),
        ]
    )
    def test_parse(self, name, input, expected):
        # type: (str, Text, List[Tuple[Text, Optional[Text]]]) -> None
        """Test basic usage of parse.

        :param name: Name of this parameter
        :param input: Input LTSV line
        :param expected: Expected parsed result
        """
        actual = StrLineParser().parse(input)
        self.assertEqual(list(actual), expected)
        return

    @parameterized.expand(
        [
            ("basic", u"a=1,b=3|", [(u"a", u"1"), (u"b", u"3")]),
        ]
    )
    def test_parse_custom_params(self, name, input, expected):
        # type: (str, Text, List[Tuple[Text, Optional[Text]]]) -> None
        """Test parser with custom parameters.

        :param name: Name of this parameter
        :param input: Input line
        :param expected: Expected parsed result
        """
        actual = StrLineParser(delimiter=u",", labeldelimiter=u"=", eols=(u"|",)).parse(
            input
        )
        self.assertEqual(list(actual), expected)
        return

    def test_parse_strict_invalid_config(self):
        # type: () -> None
        """Test parser with strict mode enabled and invalid config given."""
        with self.assertRaises(StrLineParser.ParserConfigError):
            _ = StrLineParser(strict=True, delimiter=u",")
        return

    @parameterized.expand(
        [
            ("basic", u"a:1\tb:2\n", [(u"a", u"1"), (u"b", u"2")]),
            ("crlf", u"a:1\tb:2\r\n", [(u"a", u"1"), (u"b", u"2")]),
            ("empty", u"\n", []),
            ("emptyvalue", u"a:\n", [(u"a", u"")]),
            ("colonvalue", u"a::\n", [(u"a", u":")]),
        ]
    )
    def test_parse_strict_ok(self, name, input, expected):
        # type: (str, Text, List[Tuple[Text, Optional[Text]]]) -> None
        """Test parser with strict mode enabled and invalid config given.

        :param name: Name of this parameter
        :param input: Input line
        :param expected: Expected parsed result
        """
        actual = StrLineParser(strict=True).parse(input)
        self.assertEqual(list(actual), expected)
        return

    @parameterized.expand(
        [
            ("emptyfield", u"a:1\t\tb:2\n", StrLineParser.EmptyFieldParseError),
            ("labelonly", u"a:1\tb\n", StrLineParser.LabelOnlyParseError),
            ("startswithtab", u"\ta:1\t\tb:2\n", StrLineParser.EmptyFieldParseError),
            ("emptylabel", u"a:1\t:2\n", StrLineParser.InvalidLabelParseError),
            ("invalidlabel", u"^:1\tb:2\n", StrLineParser.InvalidLabelParseError),
            ("invalidlabel", u"a:1\tあ:2\n", StrLineParser.InvalidLabelParseError),
            ("invalidvalue", u"a:1\n\tb:2\n", StrLineParser.InvalidValueParseError),
        ]
    )
    def test_parse_strict_err(self, name, input, expected_err):
        # type: (str, Text, StrLineParser.ParseError) -> None
        """Test parser with strict mode enabled and invalid input given.

        :param name: Name of this parameter
        :param input: Input line
        :param expected_err: Expected Error
        """
        parser = StrLineParser(strict=True)
        with self.assertRaises(expected_err):  # type: ignore
            _ = parser.parse(input)
        return


class TestBytesLineParser(unittest.TestCase):
    """Test BytesLineParser."""

    def test_parse(self):
        # type: () -> None
        """Test basic usage of parse."""
        actual = BytesLineParser().parse(b"a:1\tb:2\n")
        self.assertEqual(list(actual), [(b"a", b"1"), (b"b", b"2")])
        return

    @parameterized.expand(
        [
            ("emptyfield", b"a:1\t\tb:2\n", BytesLineParser.EmptyFieldParseError),
            ("labelonly", b"a:1\tb\n", BytesLineParser.LabelOnlyParseError),
            ("startswithtab", b"\ta:1\t\tb:2\n", BytesLineParser.EmptyFieldParseError),
            ("emptylabel", b"a:1\t:2\n", BytesLineParser.InvalidLabelParseError),
            ("invalidlabel", b"^:1\tb:2\n", BytesLineParser.InvalidLabelParseError),
            (
                "invalidlabel",
                u"a:1\tあ:2\n".encode("utf-8"),
                BytesLineParser.InvalidLabelParseError,
            ),
            ("invalidvalue", b"a:1\n\tb:2\n", BytesLineParser.InvalidValueParseError),
        ]
    )
    def test_parse_strict_err(self, name, input, expected_err):
        # type: (str, bytes, BytesLineParser.ParseError) -> None
        """Test parser with strict mode enabled and invalid input given.

        :param name: Name of this parameter
        :param input: Input line
        :param expected_err: Expected Error
        """
        parser = BytesLineParser(strict=True)
        with self.assertRaises(expected_err):  # type: ignore
            _ = parser.parse(input)
        return
