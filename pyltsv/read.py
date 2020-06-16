"""LTSV reader."""

from typing import IO
from typing import Iterable
from typing import Optional
from typing import Text
from typing import Tuple


def reader(ltsvfile, strict=False, delimiter=None, labeldelimiter=None):
    # type: (IO[Text], bool, Optional[Text], Optional[Text]) -> StrReader
    """Get LTSV reader for unicode str.

    :param ltsvfile: File-like object to read input
    :param strict: Enable strict parsing
    :param delimiter: Set custom field delimiter
    :param labeldelimiter: Set custom label delimiter
    :returns: StrReader object
    """
    return StrReader(ltsvfile, StrLineParser(strict, delimiter, labeldelimiter))


class StrReader(object):
    """LTSV reader for unicode str."""

    def __init__(self, ltsvfile, parser):
        # type: (IO[Text], StrLineParser) -> None
        """Initialize.

        :param ltsvfile: File-like object to read input
        :param parser: StrLineParser object
        """
        self._ltsvfile = ltsvfile
        self._parser = parser
        return

    def __iter__(self):
        # type: () -> StrReader
        """Get iter object.

        :returns: Iter object
        """
        return self

    def __next__(self):
        # type: () -> Iterable[Tuple[Text, Optional[Text]]]
        """Return next element.

        :returns: Parsed object
        :raises StopIteration: EOF
        """
        r = self.readline()
        if r is None:
            raise StopIteration
        return r

    next = __next__  # For Python 2.7 compatibility

    def readline(self):
        # type: () -> Optional[Iterable[Tuple[Text, Optional[Text]]]]
        """Read one line and return parsed object.

        :returns: parsed object or None for EOF
        """
        line = self._ltsvfile.readline()
        if line == "":
            return None
        return self._parser.parse(line)


class StrLineParser(object):
    """LTSV line parser."""

    strict = False
    delimiter = u"\t"
    labeldelimiter = u":"

    def __init__(self, strict=False, delimiter=None, labeldelimiter=None):
        # type: (bool, Optional[Text], Optional[Text]) -> None
        """Initialize.

        TODO: Write about strict mode

        :param strict: Enable strict mode
        :param delimiter: Set custom field delimiter
        :param labeldelimiter: Set custom label delimiter
        """
        self.strict = strict
        if delimiter is not None:
            self.delimiter = delimiter
        if labeldelimiter is not None:
            self.labeldelimiter = labeldelimiter
        return

    def parse(self, line):
        # type: (Text,) -> Iterable[Tuple[Text, Optional[Text]]]
        """Parse one line.

        :param line: Line to parse.
        :returns: Parsed object.
        """
        if line.endswith("\r\n"):
            line = line[:-2]
        elif line.endswith("\n"):
            line = line[:-1]

        fields = line.split(self.delimiter)
        r = []
        for field in fields:
            if field == "":
                continue
            k, _, v = field.partition(self.labeldelimiter)
            r.append((k, v))
        return r
