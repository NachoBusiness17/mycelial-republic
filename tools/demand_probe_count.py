#!/usr/bin/env python3
# prior_art: tools/queue_census.py, tools/venue_mine.py -- both count rows in the
#   estate; neither tracks whether an artifact changed later behaviour.
"""demand_probe_count -- did the artifacts create demand (T1, Bernays)?

Counts citations of the two demand-probe artifacts inside receipts, state files and
queue hints, against a control: the same 60 rows cited with no artifact present.
Run it any time; the clock started when demand_probe_20261024/CLOCK.txt was written.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "watch" / "inbox" / "demand_probe_20261024"
SCAN = [ROOT / "watch" / "inbox", ROOT / "state", ROOT / "queue"]


def load_rows(limit: int = 60) -> list[dict]:
    q = ROOT / "memory" / "percolator" / "explore.jsonl"
    rows = [json.loads(l) for l in q.read_text(encoding="utf-8").splitlines() if l.strip()]
    live = [r for r in rows if r.get("status") == "open"
            and not str(r.get("domain") or "").startswith("probe_")]
    return live[-limit:]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    rows = load_rows()
    keys = [str(r.get("canonical") or "")[:12] for r in rows if r.get("canonical")]
    words = [w for r in rows for w in re.findall(r"[a-z]{7,}", str(r.get("signal") or "").lower())]
    top_words = sorted(set(words))[:40]

    a_name, b_name = "A_digest", "B_spec"
    hits = {"A": 0, "B": 0, "control": 0, "files": 0}
    for base in SCAN:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if not p.is_file() or p.stat().st_size > 2_000_000:
                continue
            if PROBE in p.parents:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            low = text.lower()
            touched = False
            if a_name.lower() in low:
                hits["A"] += 1; touched = True
            if b_name.lower() in low:
                hits["B"] += 1; touched = True
            if any(k and k in text for k in keys):
                hits["control"] += 1; touched = True
            if touched:
                hits["files"] += 1
    out = {"schema": "demand_probe.v1", "ts": datetime.now(timezone.utc).isoformat(),
           "probe_dir": str(PROBE), "rows": len(rows), "citations": hits,
           "verdict": _verdict(hits)}
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"rows {len(rows)} · A {hits['A']} · B {hits['B']} · control {hits['control']}")
        print(f"verdict: {out['verdict']}")
    return 0


def _verdict(h: dict) -> str:
    if h["A"] == 0 and h["B"] == 0:
        return "dead - neither artifact moved anything (Bernays falsified for this estate)"
    if h["A"] + h["B"] <= h["control"]:
        return "neutral - artifacts cited no more than the bare rows"
    return "demand created - an artifact is being cited ahead of the rows"


if __name__ == "__main__":
    sys.exit(main())
