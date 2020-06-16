"""LTSV reader."""

from typing import Generic
from typing import IO  # noqa: I001  # isort sorts this wrongly
from typing import Iterable
from typing import Optional
from typing import Text
from typing import Tuple
from typing import TypeVar


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


T = TypeVar("T", Text, bytes)


class BaseReader(Generic[T]):
    """Base LTSV reader."""

    def __init__(self, ltsvfile, parser):
        # type: (IO[T], BaseLineParser[T]) -> None
        """Initialize.

        :param ltsvfile: File-like object to read input
        :param parser: BaseLineParser object
        """
        self._ltsvfile = ltsvfile  # type: IO[T]
        self._parser = parser  # type: BaseLineParser[T]
        return

    def __iter__(self):
        # type: () -> BaseReader[T]
        """Get iter object.

        :returns: Iter object
        """
        return self

    def __next__(self):
        # type: () -> Iterable[Tuple[T, Optional[T]]]
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
        # type: () -> Optional[Iterable[Tuple[T, Optional[T]]]]
        """Read one line and return parsed object.

        :returns: parsed object or None for EOF
        """
        line = self._ltsvfile.readline()
        if len(line) == 0:
            return None
        return self._parser.parse(line)


class StrReader(BaseReader[Text]):
    """LTSV reader for unicode str."""


U = TypeVar("U", Text, bytes)


class BaseLineParser(Generic[U]):
    """Base LTSV line parser."""

    strict = False

    def __init__(self, strict=False, delimiter=None, labeldelimiter=None, eols=None):
        # type: (bool, Optional[U], Optional[U], Optional[Iterable[U]]) -> None
        """Initialize.

        TODO: Write about strict mode

        :param strict: Enable strict mode
        :param delimiter: Set custom field delimiter
        :param labeldelimiter: Set custom label delimiter
        :param eols: Possible eol values
        """
        self.strict = strict
        if delimiter is not None:
            self.delimiter = delimiter  # type: U
        if labeldelimiter is not None:
            self.labeldelimiter = labeldelimiter  # type: U
        if eols is not None:
            self.eols = eols  # type: Iterable[U]
        return

    def parse(self, line):
        # type: (U,) -> Iterable[Tuple[U, Optional[U]]]
        """Parse one line.

        :param line: Line to parse.
        :returns: Parsed object.
        """
        for eol in self.eols:
            if line.endswith(eol):
                line = line[: len(eol)]
                break

        fields = line.split(self.delimiter)
        r = []
        for field in fields:
            if len(field) == 0:
                continue
            k, _, v = field.partition(self.labeldelimiter)
            r.append((k, v))
        return r


class StrLineParser(BaseLineParser[Text]):
    """LTSV line parser."""

    delimiter = u"\t"
    labeldelimiter = u":"
    eols = (u"\r\n", u"\n")