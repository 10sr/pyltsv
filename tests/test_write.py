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
        pyltsv.writer(f).writerow(((u"a", u"1"), (u"b", u"2")))
        self.assertEqual(f.getvalue(), u"a:1\tb:2\n")
        return

    def test_writerow_dict(self):
        # type: () -> None
        """Test basic usage of writer."""
        f = StringIO(u"")
        pyltsv.writer(f).writerow(OrderedDict(((u"a", u"1"), (u"b", u"2"))))
        self.assertEqual(f.getvalue(), u"a:1\tb:2\n")
        return
