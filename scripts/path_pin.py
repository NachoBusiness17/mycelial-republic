"""B2-438 repo-root path pin for runner-driven scripts.

Runner-driven scripts (coding_session_loop, governor_autorun, lane_runner)
execute scripts/ that accept path overrides. A repo-external override must
be refused loudly at the entry point, not silently written. The escape hatch
is explicit and named: MAG_ALLOW_EXTERNAL_PATH=1 (the selftest arm sets it,
never the drivers).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def pin_under_root(path, root, what: str) -> str:
    """Resolve path against root; refuse (SystemExit 2) if it lands outside.

    Relative paths are joined under root first (their intended meaning);
    absolute paths must already be inside root.
    """
    p = Path(path)
    if not p.is_absolute():
        p = Path(root) / p
    if os.environ.get("MAG_ALLOW_EXTERNAL_PATH") == "1":
        return str(p)
    rp = p.resolve()
    rr = Path(root).resolve()
    try:
        rp.relative_to(rr)
    except ValueError:
        print(
            f"PATH PIN REFUSED: {what}={path} resolves to {rp}, outside the "
            f"repo root {rr}. Set MAG_ALLOW_EXTERNAL_PATH=1 only in a "
            f"selftest/sandbox.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return str(rp)
