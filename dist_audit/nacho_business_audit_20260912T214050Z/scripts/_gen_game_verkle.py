"""_gen_game_verkle.py — emit the REAL verkle knot + standing-wave snapshot for game.html.

The operator corrected (2026-08-15): render the VERKLE KNOT STRUCTURE + STANDING WAVE, not the fish.
This generator delegates to the ONE reusable source of truth (mag.verkle_render.js_file) so the game,
dashboard, and CLI all render the same real chain — no duplicated logic (self-steal).

Schema: _gen_game_verkle.v1 · deterministic + $0 · reuse: mag.verkle_render
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

OUT = ROOT / "game_verkle_knots.js"


def main() -> int:
    from mag import verkle_render

    n = verkle_render.js_file(OUT)
    t = verkle_render.tip()
    print(f"wrote {OUT.name}: {n} real knots, n_leaves={t['n_leaves']}, root={t['root'][:12]}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
