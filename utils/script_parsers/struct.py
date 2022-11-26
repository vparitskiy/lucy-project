import mmap


def mmap_io(src):
    with open(src, "rb") as f:
        return mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)


def read_string(stream, end=b"\x00"):
    s = b""
    while True:
        b = stream.read(len(end))
        if b == end or not b:
            return s
        s += b


def iter_strings(src, offset, end=b"\x00"):
    stream = mmap_io(src)
    stream.seek(offset)

    string = read_string(stream, end=end)
    offset += len(string) + len(end)
    while string:
        yield string
        string = read_string(stream, end=end)
        if string == b"\x00":
            string = read_string(stream, end=end)
