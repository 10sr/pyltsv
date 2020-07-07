# mypy: allow-untyped-decorators
# -*- coding: utf-8 -*-
"""Test reader."""

import unittest

from collections import OrderedDict
from typing import List
from typing import Optional
from typing import Text
from typing import Tuple

from parameterized import parameterized
from six import BytesIO
from six import StringIO

import pyltsv

from pyltsv.write import BytesLineFormatter
from pyltsv.write import StrLineFormatter


class TestWriter(unittest.TestCase):
    """Test writer."""

    def test_writerow_tuple(self):
        # type: () -> None
        """Test basic usage of writer."""
        f = StringIO(u"")
        n = pyltsv.writer(f).writerow(((u"a", u"1"), (u"b", u"2")))
        self.assertEqual(n, 8)
        self.assertEqual(f.getvalue(), u"a:1\tb:2\n")
        return

    def test_writerow_dict(self):
        # type: () -> None
        """Test basic usage of writer."""
        f = StringIO(u"")
        n = pyltsv.writer(f).writerow(dict({u"a": u"1", u"b": u"2"}))
        self.assertEqual(n, 8)
        self.assertIn(f.getvalue(), (u"a:1\tb:2\n", u"b:2\ta:1\n"))
        return

    def test_writerow_ordereddict(self):
        # type: () -> None
        """Test basic usage of writer."""
        f = StringIO(u"")
        n = pyltsv.writer(f).writerow(OrderedDict(((u"a", u"1"), (u"b", u"2"))))
        self.assertEqual(n, 8)
        self.assertEqual(f.getvalue(), u"a:1\tb:2\n")
        return

    def test_writerows(self):
        # type: () -> None
        """Test basic usage of writer."""
        row1 = ((u"a", u"1"), (u"b", u"2"))
        row2 = ((u"a", u"3"), (u"b", u"4"))
        f = StringIO(u"")
        n = pyltsv.writer(f).writerows((row1, row2))
        self.assertEqual(n, 16)
        self.assertEqual(f.getvalue(), u"a:1\tb:2\na:3\tb:4\n")
        return
