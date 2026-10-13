"""dirac_loop_shim — import seam so script-mode tools (visor) can reach
mag.dirac_loop regardless of how they were launched. One function, no state.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def dirac_rank(scope: str = "operational") -> dict:
    from mag.dirac_loop import rank

    return rank(scope=scope)
