"""arena_beats - the D10 ractive: beat capture + the instrument table.

The weld (eleven-doors D10, 2026-10-05): the run's ruled transcript
events ARE the beat grid - strength = roll_value (the dice roll is the
beat's strength; the dice-law carrier welded to the damage map),
downbeat = k%4==0 (the damage-map 4/4 measure). tools/beat_map's
damage_map contract decides zone/hp/imp deterministically; this module
captures the grid and renders the instrument table. The BANKING half
lives in arena_gwap.actor_payloads (beat/zone/hp appended to both
sides' commit qualifier); tavern rows carry no roll_committed, so they
carry no beats - honestly unmeasured, never a guessed grid.

Usage:
  python tools/arena_beats.py <run_dir>    # the beat-damage table
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.beat_map import damage_map  # noqa: E402


def read_rows(run_dir: Path) -> list[dict]:
    tpath = Path(run_dir) / "transcript.jsonl"
    if not tpath.is_file():
        return []
    out = []
    for line in tpath.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def beat_grid(rows: list[dict]) -> tuple[list[dict], dict]:
    """(grid, lookup): grid = damage_map rows per ruled beat in transcript
    order; lookup keys (actor, scene, turn) -> the damage row."""
    ruled = [r for r in rows if r.get("roll_committed")]
    beats = [{"t": float(k), "strength": float(r.get("roll_value") or 0),
              "downbeat": k % 4 == 0} for k, r in enumerate(ruled)]
    mapped = damage_map(beats)
    lookup = {}
    for k, r in enumerate(ruled):
        lookup[(str(r.get("actor")), str(r.get("scene")), str(r.get("turn")))] = mapped[k]
    return mapped, lookup


def table(run_dir: Path | str) -> str:
    rows = read_rows(Path(run_dir))
    grid, _lookup = beat_grid(rows)
    ruled = [r for r in rows if r.get("roll_committed")]
    lines = [f"BEAT-DAMAGE TABLE {run_dir} ({len(grid)} beats)"]
    for k, (r, m) in enumerate(zip(ruled, grid)):
        lines.append(
            f"  {k:3d} {r.get('scene')}:{r.get('turn')} "
            f"{str(r.get('actor'))[:10]:10s} roll={r.get('roll_value'):>2} "
            f"{'DOWN' if m['downbeat'] else '  off'} "
            f"zone={m['zone']:5s} hp={m['hp']} imp={m['imp']}")
    lines.append(f"  TOTAL hp banked: {sum(m['hp'] for m in grid)}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="arena_beats",
                                 description="beat-damage table for one run (D10)")
    ap.add_argument("run_dir")
    args = ap.parse_args(argv)
    print(table(args.run_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
