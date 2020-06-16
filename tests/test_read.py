"""Test reader."""


import unittest

from six import BytesIO
from six import StringIO

import pyltsv


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
