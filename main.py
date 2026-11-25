#!/usr/bin/env python3
"""news-image-20261125 entry: copy the bundled entry.png to /output/entry.png.

Pure standard library, deterministic: the same input file is copied byte for
byte on every run, so two runs write identical output. Outside the grader's
container, MAKEFUN_OUTPUT_DIR stands in for /output."""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"),
                os.path.join(OUT_DIR, "entry.png"))
