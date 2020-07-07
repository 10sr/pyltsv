"""LTSV writer."""

import string

from typing import cast  # noqa: I001  # isort sorts this wrongly
from typing import ClassVar
from typing import FrozenSet
from typing import Generic
from typing import IO  # noqa: I001  # isort sorts this wrongly
from typing import Iterable
from typing import List
from typing import Mapping
from typing import Optional
from typing import Text
from typing import Tuple
from typing import TypeVar
from typing import Union


def writer(ltsvfile, strict=False, delimiter=None, labeldelimiter=None, eol=None):
    # type: (IO[Text], bool, Optional[Text], Optional[Text], Optional[Text]) -> StrWriter
    """Get LTSV writer for unicode str.

    :param ltsvfile: File-like object to write output
    :param strict: Enable strict formatting
    :param delimiter: Set custom field delimiter
    :param labeldelimiter: Set custom label delimiter
    :param eol: Set custom EOL character
    :returns: StrWriter object
    """
    return StrWriter(ltsvfile, StrLineFormatter(strict, delimiter, labeldelimiter, eol))


def bwriter(ltsvfile, strict=False, delimiter=None, labeldelimiter=None, eol=None):
    # type: (IO[bytes], bool, Optional[bytes], Optional[bytes], Optional[bytes]) -> BytesWriter
    """Get LTSV writer for bytes.

    :param ltsvfile: File-like object to write output
    :param strict: Enable strict formatting
    :param delimiter: Set custom field delimiter
    :param labeldelimiter: Set custom label delimiter
    :param eol: Set custom EOL character
    :returns: BytesWriter object
    """
    return BytesWriter(
        ltsvfile, BytesLineFormatter(strict, delimiter, labeldelimiter, eol)
    )


T = TypeVar("T", Text, bytes)


_INPUT_DICT = Mapping[T, Optional[T]]
_INPUT_TUPLE = Iterable[Tuple[T, Optional[T]]]


class BaseWriter(Generic[T]):
    """Base LTSV writer."""

    def __init__(self, ltsvfile, formatter):
        # type: (IO[T], BaseLineFormatter[T]) -> None
        """Initialize.

        :param ltsvfile: File-like object to read input
        :param formatter: BaseLineFormatter object
        """
        self._ltsvfile = ltsvfile  # type: IO[T]
        self._formatter = formatter  # type: BaseLineFormatter[T]
        return

    def writerow(self, row):
        # type: (Union[_INPUT_DICT[T], _INPUT_TUPLE[T]]) -> int
        """Write one row object.

        :param row: Input object
        :returns: the number of texts or bytes written
        """
        line = self._formatter.format(row)
        n = self._ltsvfile.write(line)
        if n is None:  # Python2  # pragma: no cover
            n = len(line)
        return n

    def writerows(self, rows):
        # type: (Iterable[Union[_INPUT_DICT[T], _INPUT_TUPLE[T]]]) -> int
        """Write row objects.

        :param rows: Iterable of input objects
        :returns: the total number of texts or bytes written
        """
        total = 0
        for row in rows:
            total += self.writerow(row)
        return total


class StrWriter(BaseWriter[Text]):
    """LTSV writer for unicode str."""


class BytesWriter(BaseWriter[bytes]):
    """LTSV writer for bytes."""


class BaseLineFormatter(Generic[T]):
    """Base LTSV line formatter."""

    strict = False
    delimiter = None  # type: T
    labeldelimiter = None  # type: T
    eol = None  # type: T
    _empty_value = None  # type: T

    class FormatterConfigError(ValueError):
        """Invalid formatter configuration given."""

    class FormatError(ValueError):
        """Error was found while formatting row data."""

        def __init__(self, msg, input_):
            # type: (Text, object) -> None
            # (Text, Union[_INPUT_DICT[T], _INPUT_TUPLE[T]]) -> None
            """Initialize.

            :param msg: Error message
            :param input_: Input row data
            """
            super(BaseLineFormatter.FormatError, self).__init__(msg, input_)
            self.input = input_
            return

    class InvalidInputFormatError(FormatError):
        """Invalid input was found in data."""

    class InvalidLabelFormatError(FormatError):
        """Invalid label was found in data."""

    class InvalidValueFormatError(FormatError):
        """Invalid value was found in data."""

    def __init__(self, strict=False, delimiter=None, labeldelimiter=None, eol=None):
        # type: (bool, Optional[T], Optional[T], Optional[T]) -> None
        """Initialize.

        TODO: Write about strict mode

        :param strict: Enable strict mode
        :param delimiter: Set custom field delimiter
        :param labeldelimiter: Set custom label delimiter
        :param eol: Set eol value
        :raises FormatterConfigError: Invalid formatter configuration given
        """
        self.strict = strict
        if self.strict and (
            delimiter is not None or labeldelimiter is not None or eol is not None
        ):
            raise self.FormatterConfigError(
                "Cannot change format configs when strict=True"
            )

        if delimiter is not None:
            self.delimiter = delimiter
        if labeldelimiter is not None:
            self.labeldelimiter = labeldelimiter
        if eol is not None:
            self.eol = eol
        return

    def format(self, row):
        # type: (Union[_INPUT_DICT[T], _INPUT_TUPLE[T]],) -> T
        """Format data into a LTSV line.

        :param row: Data
        :returns: One LTSV line
        :raises InvalidInputFormatError: Unexpected input format
        """
        # TODO: Implement strict mode

        items = []  # type: Iterable[Tuple[T, Optional[T]]]
        if isinstance(row, Mapping):
            items = row.items()
        elif isinstance(row, Iterable):
            items = cast(Iterable[Tuple[T, Optional[T]]], row)
        else:
            raise self.InvalidInputFormatError("Unknown input object", row)

        if len(items) == 0:
            return self._empty_value + self.eol

        fields = []  # type: List[T]
        for k, v in items:
            if v is None:
                fields.append(k + self.labeldelimiter)
            else:
                fields.append(k + self.labeldelimiter + v)
        return self.delimiter.join(fields) + self.eol


class StrLineFormatter(BaseLineFormatter[Text]):
    """LTSV line formatter for unicode str."""

    delimiter = u"\t"
    labeldelimiter = u":"
    eol = u"\n"
    _empty_value = u""


class BytesLineFormatter(BaseLineFormatter[bytes]):
    """LTSV line formatter for unicode bytes."""

    delimiter = b"\t"
    labeldelimiter = b":"
    eol = b"\n"
    _empty_value = b""
