"""headless — shared Windows headless-spawn helper.

One source of truth for `creationflags` so NO console window ever pops from a
subprocess while a user is gaming. The codebase history proved `DETACHED_PROCESS`
alone is NOT enough (window-storm lesson) — `CREATE_NO_WINDOW` is REQUIRED.

  no_window_flags(detached=False) -> int  creationflags for a headless spawn.
  run_headless(args, **kw) -> CompletedProcess   subprocess.run with no window.
  popen_headless(args, **kw) -> Popen            subprocess.Popen with no window.

On non-Windows, returns 0 / behaves like plain subprocess (headless anyway).
"""
from __future__ import annotations

import os
import subprocess
from typing import Any


def no_window_flags(*, detached: bool = False) -> int:
    """creationflags that guarantee no console window on Windows (0 elsewhere)."""
    if os.name != "nt":
        return 0
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
    flags |= getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    if detached:
        flags |= getattr(subprocess, "DETACHED_PROCESS", 0x00000008)
    return flags


def run_headless(args, **kw: Any) -> subprocess.CompletedProcess:
    """subprocess.run with CREATE_NO_WINDOW (plus NEW_PROCESS_GROUP)."""
    kw.setdefault("creationflags", no_window_flags())
    return subprocess.run(args, **kw)


def popen_headless(args, **kw: Any) -> subprocess.Popen:
    """subprocess.Popen with CREATE_NO_WINDOW (plus NEW_PROCESS_GROUP [+ DETACHED])."""
    kw.setdefault("creationflags", no_window_flags(detached=bool(kw.pop("detached", False))))
    return subprocess.Popen(args, **kw)


def _selfcheck() -> None:
    if os.name == "nt":
        assert no_window_flags() & getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
    print("headless helper OK")


if __name__ == "__main__":
    _selfcheck()
