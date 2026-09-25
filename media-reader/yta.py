#!/usr/bin/env python3
"""yta.py was renamed mread.py on 2026-09-25 [dr-dqm]. This forwards, and says
so, so an old note or a sibling's copied command still works."""
import os
import sys
from pathlib import Path

target = Path(__file__).resolve().with_name("mread.py")
print("[yta.py is now mread.py — forwarding; update the command]", file=sys.stderr)
os.execv(sys.executable, [sys.executable, str(target), *sys.argv[1:]])
