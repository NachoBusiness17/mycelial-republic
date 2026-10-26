"""LIGHT WALK — walk the old paths wide through the salon lightmap.

Operator order, 2026-09-22: "walk the old paths and test them wide."
Reuses mag/room_state.py's own wall/token definitions (correct by construction):
one pass over the WHOLE trajectory tape (memory/trajectory/steps.jsonl), a rolling
200-step attention window (the lightmap's own window), and at every window position
we ask the lightmap's question: which walls are lit?

Emitted per wall: lit_ratio (share of windows lit), longest dark streak (in steps),
first/last fire, dark-events after first fire (the wall's ghost history).
Emitted globally: windows walked, invariants-never-dark verdict, deepest ghosts.

$0, stdlib only. Output: watch/inbox/LIGHT_WALK_<date>.json (path confined to
watch/inbox by resolve+is_relative_to, same guard as estate_smith_chart.py).
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STEPS = ROOT / "memory" / "trajectory" / "steps.jsonl"
OUT = (ROOT / "watch" / "inbox").resolve()
WINDOW = 200

WALLS = {
    "chain":      ["verkle_chain", "verkle_knot"],
    "memory":     ["biography", "MEMORY.md"],
    "watch":      ["watch/"],
    "immune":     ["refeed_guard", "watchdog", "grounding_wave"],
    "lanes":      ["auth_tracks", "fuel_feed"],
    "room":       ["CONVO.md", "room.jsonl", "queue/handoff"],
    "board":      ["room.html", "board.js", "live.html"],
    "organs":     ["mag/", "overseer"],
    "boot_check": ["boot_check", "boot.py"],
    "sensors":    ["steps.jsonl", "read_receipts", "trajectory"],
}
INVARIANTS = ["chain", "room", "boot_check"]


def out_path() -> Path:
    name = f"LIGHT_WALK_{datetime.now(timezone.utc).strftime('%Y%m%d')}.json"
    p = (OUT / name).resolve()
    if not p.is_relative_to(OUT):
        raise ValueError("output path escapes watch/inbox")
    return p


def main() -> int:
    hits = []          # per step: bitmask of walls hit
    step_ts = []
    with open(STEPS, encoding="utf-8") as f:
        for line in f:
            try:
                s = json.loads(line)
            except Exception:
                hits.append(0)
                step_ts.append(None)
                continue
            cmd = str(s.get("command", ""))
            mask = 0
            for i, (_, toks) in enumerate(WALLS.items()):
                if any(t in cmd for t in toks):
                    mask |= 1 << i
            hits.append(mask)
            step_ts.append(s.get("ts"))

    n = len(hits)
    names = list(WALLS.keys())
    lit_counts = [0] * len(names)
    first_fire = [None] * len(names)
    last_fire = [None] * len(names)
    dark_run = [0] * len(names)
    longest_dark = [0] * len(names)
    dark_events = [0] * len(names)
    ever = [False] * len(names)

    def window_bitmask(i):
        lo = max(0, i - WINDOW + 1)
        m = 0
        for j in range(lo, i + 1):
            m |= hits[j]
        return m

    prev = None
    for i in range(n):
        m = window_bitmask(i)
        for w in range(len(names)):
            lit = (m >> w) & 1
            if lit:
                lit_counts[w] += 1
                if not ever[w]:
                    ever[w] = True
                    first_fire[w] = step_ts[i]
                last_fire[w] = step_ts[i]
                dark_run[w] = 0
            else:
                dark_run[w] += 1
                if ever[w]:
                    longest_dark[w] = max(longest_dark[w], dark_run[w])
            if prev is not None and ever[w] and (prev >> w) & 1 and not lit:
                dark_events[w] += 1
        prev = m

    rows = []
    for w, name in enumerate(names):
        rows.append({
            "wall": name,
            "lit_ratio": round(lit_counts[w] / max(n, 1), 4),
            "longest_dark_steps": longest_dark[w],
            "dark_events_after_first_fire": dark_events[w],
            "first_fire": first_fire[w],
            "last_fire": last_fire[w],
            "invariant_seed": name in INVARIANTS,
        })
    rows.sort(key=lambda r: -r["lit_ratio"])

    inv_dark = [r["wall"] for r in rows if r["invariant_seed"] and r["first_fire"] is None]
    deep_ghosts = [r["wall"] for r in rows if r["lit_ratio"] < 0.05 and r["first_fire"] is not None]

    out = {
        "schema": "light_walk.v1",
        "ts": datetime.now(timezone.utc).isoformat(),
        "window": WINDOW,
        "steps_walked": n,
        "tape_span": [step_ts[0], step_ts[-1]] if n else [],
        "walls": rows,
        "invariants_never_dark": [w for w in INVARIANTS if w not in inv_dark],
        "invariants_never_fired": inv_dark,
        "deep_ghosts_lit_under_5pct": deep_ghosts,
    }
    p = out_path()
    p.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print(f"LIGHT WALK {now()}  window={WINDOW}  steps={n}")
    print(f"tape: {step_ts[0]} -> {step_ts[-1]}")
    for r in rows:
        print(f"  {r['wall']:11s} lit {r['lit_ratio']*100:5.1f}%  longest dark {r['longest_dark_steps']:5d} steps  dark-events {r['dark_events_after_first_fire']:3d}")
    print(f"  invariants never dark: {out['invariants_never_dark']}")
    print(f"  invariants never fired: {out['invariants_never_fired'] or 'none'}")
    print(f"  deep ghosts (<5% lit): {deep_ghosts or 'none'}")
    print(f"  wrote {p}")
    return 0


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


if __name__ == "__main__":
    sys.exit(main())
