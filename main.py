"""Entry point for make.fun news-image-20261122.

Copies the pre-rendered poster (entry.png, built by make_image.py) to the
grader's output directory. No network, no randomness: identical bytes every
run. Validates the artifact (PNG magic, 1024x1024, <= 1 MiB) before writing,
and replaces the destination atomically.
"""
import os
import struct
import sys
import tempfile

MAX_BYTES = 1024 * 1024
MAX_DIM = 1024


def validate(path: str) -> None:
    with open(path, "rb") as fh:
        data = fh.read(MAX_BYTES + 1)
    assert len(data) <= MAX_BYTES, "entry.png exceeds 1 MiB"
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "entry.png is not a PNG"
    assert data[12:16] == b"IHDR", "PNG missing IHDR"
    w, h = struct.unpack(">II", data[16:24])
    assert (w, h) == (MAX_DIM, MAX_DIM), f"bad dimensions {w}x{h}"


def main() -> int:
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    validate(src)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    fd, tmp = tempfile.mkstemp(dir=out_dir, suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh, open(src, "rb") as s:
            fh.write(s.read())
        os.replace(tmp, dst)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
