#!/usr/bin/env python3
"""Backward-compatible alias for older docs links."""

from __future__ import annotations

import runpy
from pathlib import Path

TARGET = Path(__file__).with_name("inspect_huf_artifacts.py")

if __name__ == "__main__":
    runpy.run_path(str(TARGET), run_name="__main__")
