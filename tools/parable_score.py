#!/usr/bin/env python3
"""parable_score -- does a lane keep the lens boundary?

The 2026-10-23 grid found the dominant failure: Jung written with Freud's
"repression", and Ellul/McLuhan blurring into each other. This scores a burn
receipt on exactly those boundaries, so the claim is measurement, not vibe.

    python tools/parable_score.py                 # newest receipt
    python tools/parable_score.py --file X.jsonl
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SPEC = {
    "jung-no-freud": {
        "lens": "jung",
        "need": ["shadow", "double", "persona", "archetype", "mask", "tenth"],
        "forbid": ["cellar", "symptom", "repress", "repetition-compulsion", "unconscious wish"],
    },
    "freud-repetition": {
        "lens": "freud",
        "need": ["repeat", "symptom", "repress"],
        "forbid": ["shadow", "archetype", "persona", "grief", "individuat"],
    },
    "ellul-autonomy": {
        "lens": "ellul",
        "need": ["technique", "efficien", "autonom", "nobody chose", "no one chose", "method"],
        "forbid": ["medium", "sensory", "ratio", "the channel"],
    },
    "mcluhan-medium": {
        "lens": "mcluhan",
        "need": ["medium", "channel", "sensory", "ratio", "the form"],
        "forbid": ["technique", "autonom", "efficien", "ratchet"],
    },
}


def score_row(row: dict) -> dict:
    task = row.get("task", "")
    spec = SPEC.get(task)
    text = row.get("text") or ""
    out = {"lane": row.get("lane"), "task": task, "ok": bool(row.get("ok")),
           "words": len(text.split()), "issues": []}
    if not spec or not text.strip():
        out["issues"].append("no-text")
        return out
    low = text.lower()
    if not (80 <= out["words"] <= 170):
        out["issues"].append(f"len{out['words']}")
    if sum(1 for ch in text if ord(ch) > 127) / max(1, len(text)) > 0.02:
        out["issues"].append("non-en")
    if "mechanism:" not in low:
        out["issues"].append("no-mech")
    if not any(n in low for n in spec["need"]):
        out["issues"].append("no-lens-signal")
    bad = [f for f in spec["forbid"] if f in low]
    if bad:
        out["issues"].append("leak:" + ",".join(bad))
    out["clean"] = not out["issues"]
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=None)
    args = ap.parse_args(argv)
    files = sorted(glob.glob(str(ROOT / "memory" / "runs" / "burn" / "burn_*.jsonl")))
    if not files and not args.file:
        print("no receipts")
        return 2
    path = args.file or files[-1]
    rows = [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]
    scored = [score_row(r) for r in rows]

    print(f"receipt {Path(path).name} · {len(rows)} calls")
    by = collections.defaultdict(list)
    for s in scored:
        by[s["task"]].append(s)

    for task in [t for t in SPEC if t in by]:
        print(f"\n## {task}")
        print(f"{'lane':18s} {'w':>4s} {'clean':5s} issues")
        for s in sorted(by[task], key=lambda x: x["lane"]):
            mark = "yes" if s.get("clean") else "NO"
            print(f"{s['lane']:18s} {s['words']:4d} {mark:5s} {', '.join(s['issues'])[:70]}")

    # cross-lens confusion: a clean score on the *other* lens's task is the tell
    print("\n## boundary leaks")
    leaks = [s for s in scored if any(i.startswith("leak:") for i in s["issues"])]
    if not leaks:
        print("none")
    for s in leaks:
        bad = next(i for i in s["issues"] if i.startswith("leak:"))
        print(f"  {s['lane']:16s} {s['task']:16s} {bad}")

    total = sum(1 for s in scored if s["ok"])
    clean = sum(1 for s in scored if s.get("clean"))
    print(f"\nvalid {total}/{len(scored)} · clean {clean}/{len(scored)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
