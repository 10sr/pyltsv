"""Test reader."""


import unittest

from six import StringIO

import pyltsv


class TestReader(unittest.TestCase):
    """Test reader."""

    def test_reader(self) -> None:
        """Text basic usage of reader."""
        f = StringIO(u"a:1\tb:2\na:3\tb:4")
        ret = list(pyltsv.reader(f))
        self.assertEqual(len(ret), 2)
        return
