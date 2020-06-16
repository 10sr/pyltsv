# mypy: allow-untyped-decorators
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

from pyltsv.read import StrLineParser


class TestReader(unittest.TestCase):
    """Test reader."""

    def test_reader(self):
        # type: () -> None
        """Test basic usage of reader."""
        f = StringIO(u"a:1\tb:2\n\na:3\tb:4\n")
        ret = list(pyltsv.reader(f))
        self.assertEqual(len(ret), 3)
        self.assertEqual(list(ret[0]), [(u"a", u"1"), (u"b", u"2")])
        self.assertEqual(list(ret[1]), [])
        self.assertEqual(list(ret[2]), [(u"a", u"3"), (u"b", u"4")])
        return

    def test_reader_readline(self):
        # type: () -> None
        """Test readline of reader."""
        f = StringIO(u"a:1\tb:2\n\na:3\tb:4\n")
        r = pyltsv.reader(f)
        self.assertEqual(list(r.readline() or []), [(u"a", u"1"), (u"b", u"2")])
        self.assertEqual(list(r.readline() or []), [])
        self.assertEqual(list(r.readline() or []), [(u"a", u"3"), (u"b", u"4")])
        self.assertEqual(r.readline(), None)  # end of file
        return


class TestBreader(unittest.TestCase):
    """Test breader."""

    def test_breader(self):
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
        [("basic", u"a:1\tb:2\n", [(u"a", u"1"), (u"b", u"2")]),]
    )
    def test_parse(self, name, input, expected):
        # type: (str, Text, List[Tuple[Text, Optional[Text]]]) -> None
        """Test basic usage of parse.

        :param name: Name of this parameter
        :param input: Input LTSV line
        :param expected: Expected parsed result
        """
        parser = StrLineParser()
        actual = parser.parse(input)
        self.assertEqual(list(actual), expected)
        return
