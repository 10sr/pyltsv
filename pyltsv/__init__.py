"""Python Library for LTSV."""

from typing import Iterable
from typing import Optional
from typing import Text
from typing import TextIO
from typing import Tuple


def reader(ltsvfile, strict=False, delimiter=None, labeldelimiter=None):
    # type: (TextIO, bool, Optional[Text], Optional[Text]) -> StrReader
    return StrReader(ltsvfile, StrLineParser(strict, delimiter, labeldelimiter))


class StrReader(object):
    def __init__(self, ltsvfile, parser):
        # type: (TextIO, StrLineParser) -> None
        self._ltsvfile = ltsvfile
        self._parser = parser
        return

    def __iter__(self):
        # type: () -> StrReader
        return self

    def __next__(self):
        # type: () -> Iterable[Tuple[Text, Optional[Text]]]
        r = self.readline()
        if r is None:
            raise StopIteration
        return r

    def readline(self):
        # type: () -> Optional[Iterable[Tuple[Text, Optional[Text]]]]
        line = self._ltsvfile.readline()
        if line == "":
            return None
        return self._parser.parse(line)


class StrLineParser(object):
    strict = False
    delimiter = "\t"
    labeldelimiter = ":"

    def __init__(self, strict=False, delimiter=None, labeldelimiter=None):
        # type: (bool, Optional[Text], Optional[Text]) -> None
        self.strict = strict
        if delimiter is not None:
            self.delimiter = delimiter
        if labeldelimiter is not None:
            self.labeldelimiter = labeldelimiter
        return

    def parse(self, line):
        # type: (Text,) -> Iterable[Tuple[Text, Optional[Text]]]
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
