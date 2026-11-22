#!/usr/bin/env python3
"""Entry program for make.fun bounty news-image-20261121.

Sum up 21 November 2026's world news in one image.

The image (entry.png, 1024x1024, generated offline by build_image.py
from Reuters/AP/CNN/NYT reporting of Saturday 21 November 2026) is
bundled in this repository. This program deterministically copies it
to /output/entry.png using only the Python standard library: no
network, no randomness, no dependencies, so both runs write the
same bytes.
"""
import os
import shutil


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
