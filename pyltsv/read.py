"""LTSV reader."""

from typing import Generic
from typing import IO  # noqa: I001  # isort sorts this wrongly
from typing import Iterable
from typing import Optional
from typing import Text
from typing import Tuple
from typing import TypeVar
from typing import Union


def reader(ltsvfile, strict=False, delimiter=None, labeldelimiter=None, eols=None):
    # type: (IO[Text], bool, Optional[Text], Optional[Text], Optional[Iterable[Text]]) -> StrReader
    """Get LTSV reader for unicode str.

    :param ltsvfile: File-like object to read input
    :param strict: Enable strict parsing
    :param delimiter: Set custom field delimiter
    :param labeldelimiter: Set custom label delimiter
    :param eols: Set custom EOL characters
    :returns: StrReader object
    """
    return StrReader(ltsvfile, StrLineParser(strict, delimiter, labeldelimiter, eols))


def breader(ltsvfile, strict=False, delimiter=None, labeldelimiter=None, eols=None):
    # type: (IO[bytes], bool, Optional[bytes], Optional[bytes], Optional[Iterable[bytes]]) -> BytesReader
    """Get LTSV reader for bytes.

    :param ltsvfile: File-like object to read input
    :param strict: Enable strict parsing
    :param delimiter: Set custom field delimiter
    :param labeldelimiter: Set custom label delimiter
    :param eols: Set custom EOL characters
    :returns: BytesReader object
    """
    return BytesReader(
        ltsvfile, BytesLineParser(strict, delimiter, labeldelimiter, eols)
    )


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
        # type: () -> Iterable[Tuple[T, T]]
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
        # type: () -> Optional[Iterable[Tuple[T, T]]]
        """Read one line and return parsed object.

        :returns: parsed object or None for EOF
        """
        line = self._ltsvfile.readline()
        if len(line) == 0:
            return None
        return self._parser.parse(line)


class StrReader(BaseReader[Text]):
    """LTSV reader for unicode str."""


class BytesReader(BaseReader[bytes]):
    """LTSV reader for bytes."""


U = TypeVar("U", Text, bytes)


class BaseLineParser(Generic[U]):
    """Base LTSV line parser."""

    strict = False
    delimiter = None  # type: U
    labeldelimiter = None  # type: U
    eols = None  # type: Iterable[U]
    _empty_value = None  # type: U

    class ParserConfigError(ValueError):
        """Invalid parser configuration given."""

    class ParseError(ValueError):
        """Error was found while parsing LTSV input."""

        def __init__(self, msg, input_):
            # type: (Text, Union[Text, bytes]) -> None
            """Initialize.

            :param msg: Error message
            :param input_: Input LTSV line
            """
            super(BaseLineParser.ParseError, self).__init__(msg, input_)
            self.input = input_
            return

    class EmptyFieldParseError(ParseError):
        """Empty field was found in input."""

    class LabelOnlyParseError(ParseError):
        """Label delimiter was not found in field."""

    def __init__(self, strict=False, delimiter=None, labeldelimiter=None, eols=None):
        # type: (bool, Optional[U], Optional[U], Optional[Iterable[U]]) -> None
        """Initialize.

        TODO: Write about strict mode

        :param strict: Enable strict mode
        :param delimiter: Set custom field delimiter
        :param labeldelimiter: Set custom label delimiter
        :param eols: Possible eol values
        :raises ParserConfigError: Invalid parser configuration given
        """
        self.strict = strict
        if self.strict and (
            delimiter is not None or labeldelimiter is not None or eols is not None
        ):
            raise self.ParserConfigError(
                "Cannot change parser configs when strict=True"
            )

        if delimiter is not None:
            self.delimiter = delimiter
        if labeldelimiter is not None:
            self.labeldelimiter = labeldelimiter
        if eols is not None:
            self.eols = eols
        return

    def parse(self, line):
        # type: (U,) -> Iterable[Tuple[U, U]]
        """Parse one line.

        Errors will be raised only when strict is set to True.

        :param line: Line to parse.
        :returns: Parsed object.
        :raises EmptyFieldParseError: Empty field found in input
        :raises LabelOnlyParseError: label delimiter was not found in field
        """
        for eol in self.eols:
            if line.endswith(eol):
                line = line[: len(eol) * (-1)]
                break

        if len(line) == 0:
            return []

        fields = line.split(self.delimiter)
        r = []
        for field in fields:
            if len(field) == 0:
                if self.strict:
                    raise self.EmptyFieldParseError("Empty field found in input", line)
                continue
            if self.labeldelimiter in field:
                k, _, v = field.partition(self.labeldelimiter)
                r.append((k, v))
            else:
                if self.strict:
                    raise self.LabelOnlyParseError(
                        "Label delimiter was not found in field", line
                    )
                r.append((field, self._empty_value))
        return r


class StrLineParser(BaseLineParser[Text]):
    """LTSV line parser for unicode str."""

    delimiter = u"\t"
    labeldelimiter = u":"
    eols = (u"\r\n", u"\n")
    _empty_value = u""


class BytesLineParser(BaseLineParser[bytes]):
    """LTSV line parser for bytes."""

    delimiter = b"\t"
    labeldelimiter = b":"
    eols = (b"\r\n", b"\n")
    _empty_value = b""
