"""Python Library for LTSV."""


def reader(ltsvfile, strict=False, delimiter=None, labeldelimiter=None):
    return StrReader(ltsvfile, strict)


class StrReader(object):
    delimiter = "\t"
    labeldelimiter = ":"

    def __init__(self, ltsvfile, strict, delimiter=None, labeldelimiter=None):
        self.ltsvfile = ltsvfile
        self.strict = strict
        if delimiter is not None:
            self.delimiter = delimiter
        if labeldelimiter is not None:
            self.labeldelimiter = labeldelimiter
        return

    def __iter__(self):
        return self

    def __next__(self):
        r = self.readline()
        if r is None:
            raise StopIteration
        return r

    def readline(self):
        line = self.ltsvfile.readline()
        if line == "":
            return None
        return _parse(line, self.strict, self.delimiter, self.labeldelimiter)


def _parse(line, strict=False, delimiter="\t", labeldelimiter=":"):
    if line.endswith("\r\n"):
        line = line[:-2]
    elif line.endswith("\n"):
        line = line[:-1]

    fields = line.split(delimiter)
    r = []
    for field in fields:
        if field == "":
            continue
        k, _, v = field.partition(labeldelimiter)
        r.append((k, v))
    return r

def test_1():
    from io import StringIO
    f = StringIO("a:1\tb:2\na:3\tb:4")
    for d in reader(f):
        print(dict(d))
    return


if __name__ == "__main__":
    test_1()
