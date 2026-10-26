#!/usr/bin/env python3
"""queue_census -- is the explore backlog a backlog, or a vanity count?

Born from the 2026-10-24 lens run, where three lenses independently attacked the
census that the map assumed: diogenes ("1,521 open is a vanity count"), wallas
("rows may be one observation reworded"), jung ("decay may have claimed most").
They were right, so this measures the queue's composition instead of its size.

    python tools/queue_census.py            # human readout
    python tools/queue_census.py --json
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "memory" / "percolator" / "explore.jsonl"
DECAY = ROOT / "memory" / "percolator" / "explore_decay.jsonl"


def norm(row: dict) -> str:
    t = (row.get("signal") or row.get("text") or row.get("canonical") or "").lower()
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    rows = [json.loads(l) for l in QUEUE.read_text(encoding="utf-8").splitlines() if l.strip()]
    open_rows = [r for r in rows if r.get("status") == "open"]
    probe_status_rows = [r for r in rows if r.get("status") == "probe"]
    decayed = set()
    if DECAY.is_file():
        for line in DECAY.read_text(encoding="utf-8").splitlines():
            try:
                d = json.loads(line)
                if d.get("canonical"):
                    decayed.add(d["canonical"])
            except json.JSONDecodeError:
                pass

    # a probe row can be recognised two ways: legacy rows carry a probe_* domain
    # while still status="open"; rows written after 2026-10-24 carry status="probe".
    def is_probe(r: dict) -> bool:
        return (str(r.get("domain") or "").startswith("probe_")
                or str(r.get("status") or "") == "probe")

    probe = [r for r in open_rows if is_probe(r)]
    live = [r for r in open_rows if not is_probe(r)]
    texts = [norm(r) for r in live if norm(r)]
    exact = collections.Counter(texts)
    prefix = collections.Counter(" ".join(t.split()[:6]) for t in texts if t)
    dup_exact = sum(c - 1 for c in exact.values() if c > 1)
    dup_near = sum(c - 1 for c in prefix.values() if c > 1)
    distinct = len(exact)

    out = {
        "schema": "queue_census.v1",
        "rows_total": len(rows),
        "open": len(open_rows),
        "probe_status_rows": len(probe_status_rows),
        "probe_open": len(probe),
        "probe_share_pct": round(100 * len(probe) / len(open_rows), 1) if open_rows else 0,
        "live_open": len(live),
        "decayed": sum(1 for r in open_rows if r.get("canonical") in decayed),
        "distinct_texts": distinct,
        "near_duplicates": dup_near,
        "near_dup_share_pct": round(100 * dup_near / len(texts), 1) if texts else 0,
        "exact_duplicates": dup_exact,
        "real_backlog_est": distinct - dup_near,
        "domains": collections.Counter(r.get("domain") for r in open_rows).most_common(8),
    }
    if args.json:
        print(json.dumps(out, indent=2, default=str))
        return 0
    print(f"QUEUE {out['open']} open of {out['rows_total']} rows")
    print(f"  probe_* chatter   {out['probe_open']:5d}  ({out['probe_share_pct']}% of open)")
    print(f"  live              {out['live_open']:5d}")
    print(f"  decayed           {out['decayed']:5d}")
    print(f"  distinct texts    {out['distinct_texts']:5d}")
    print(f"  near-duplicates   {out['near_duplicates']:5d}  ({out['near_dup_share_pct']}% share a 6-word opening)")
    print(f"  => real backlog   ~{out['real_backlog_est']:5d} distinct live observations")
    # T6 (Hall) + T3 (McLuhan), 2026-10-24: a census with only numbers reads as data and
    # produces no action in a cold reader (0/3 agreement on "what does this imply?").
    # One verb fixes that. The verb is chosen by composition, not taste.
    if out["probe_share_pct"] >= 40:
        verb = "filter probe chatter at the writer"
    elif out["near_dup_share_pct"] >= 25:
        verb = "dedupe before consuming"
    elif out["real_backlog_est"] > 2000:
        verb = "build or extend a consumer"
    else:
        verb = "consume the live set; nothing structural is blocking"
    print(f"  NEXT  {verb}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
