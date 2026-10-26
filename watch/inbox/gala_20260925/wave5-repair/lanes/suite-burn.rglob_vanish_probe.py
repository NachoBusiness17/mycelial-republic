"""suite-burn wave5 primitive probe: rglob vs vanished-directory mid-walk.

Deterministic: force rglob to list a parent, delete a queued subdir, continue
iteration. Records the exact exception class the f-15 run saw
(FileNotFoundError [WinError 2]) vs os.walk's onerror tolerance.
"""
from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path

base = Path(tempfile.mkdtemp(prefix="rglob_vanish_"))
(base / "keep").mkdir()
(base / "keep" / "a.py").write_text("x", encoding="utf-8")
(base / "sub" / "deep").mkdir(parents=True)
(base / "sub" / "deep" / "b.py").write_text("x", encoding="utf-8")

it = base.rglob("*.py")
first = next(it)  # scandir(base): queues keep/ and sub/
print("first yielded:", first.relative_to(base))
shutil.rmtree(base / "sub")  # the concurrent-cleanup interference
try:
    rest = sorted(it)
    print("rglob COMPLETED:", [p.relative_to(base) for p in rest])
except OSError as e:
    print(f"rglob RAISED: {type(e).__name__}: {e}")

# the fixed walker's primitive under the same interference
def onerror(e):
    print("os.walk onerror fired:", type(e).__name__)

got = []
for dirpath, dirnames, filenames in os.walk(base, onerror=onerror):
    for fn in filenames:
        if fn.endswith(".py"):
            got.append(str(Path(dirpath, fn).relative_to(base)))
print("os.walk survived:", sorted(got))
shutil.rmtree(base, ignore_errors=True)
