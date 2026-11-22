"""Entry point for make.fun news-image-20261122.

Copies the pre-rendered poster (entry.png, built by make_image.py) to the
grader's output directory. No network, no randomness: identical bytes every run.
"""
import os
import shutil
import sys


def main() -> int:
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
