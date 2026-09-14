#!/usr/bin/env python3
"""chain_index_completion.py -- sidecar completion index for off-chain knots.

The verkle chain (memory/biography/verkle_chain.jsonl) indexes ~7,200 of the
~28,400 knot files in memory/biography/knots/. This script scans the knots,
diffs against the chain (linked by the chain row's `filename` field), and
appends an INDEX-ONLY row per off-chain knot to a SIDEcar file
(memory/biography/chain_index_completion.jsonl).

ADDITIVE ONLY:
- never modifies or deletes any knot file
- never touches verkle_chain.jsonl (the sidecar is what chain tooling merges later)
- idempotent: knots already present in the sidecar are skipped on re-run
- honest errors: unparseable knots go to parse_errors, processing continues

stdlib-only. Exit codes: 0 clean, 1 fatal (I/O).
"""

import json
import os
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOTS_DIR = os.path.join(REPO, "memory", "biography", "knots")
CHAIN_PATH = os.path.join(REPO, "memory", "biography", "verkle_chain.jsonl")
SIDECAR_PATH = os.path.join(REPO, "memory", "biography", "chain_index_completion.jsonl")
STATS_PATH = os.path.join(REPO, "memory", "audit", "chain_completion_stats.json")
ROOM_PATH = os.path.join(REPO, "watch", "room.jsonl")

BATCH_SIZE = 5000
INDEXED_BY = "chain_index_completion_v0"


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_chain_keys():
    """Return set of knot filenames already indexed in the main chain.

    Primary link: chain row `filename`. Fallback for rows missing it:
    (session_id, ts) tuple match against knot start_minute.
    """
    filenames = set()
    session_ts = set()
    n_rows = 0
    with open(CHAIN_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                n_rows += 1
                continue  # count the row, skip it honestly
            n_rows += 1
            fn = row.get("filename")
            if fn:
                filenames.add(fn)
            else:
                session_ts.add((row.get("session_id"), row.get("ts")))
    return filenames, session_ts, n_rows


def load_sidecar_keys():
    """Filenames already appended to the sidecar (idempotent re-runs)."""
    if not os.path.exists(SIDECAR_PATH):
        return set()
    done = set()
    with open(SIDECAR_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                done.add(json.loads(line).get("knot_file"))
            except json.JSONDecodeError:
                continue
    return done


def knot_ts(knot):
    for key in ("start_minute", "end_minute", "date"):
        v = knot.get(key)
        if v:
            return v
    return None


def main():
    print("[1/4] scanning knots dir: %s" % KNOTS_DIR)
    knot_files = sorted(
        fn for fn in os.listdir(KNOTS_DIR) if fn.endswith(".knot.json")
    )
    total_knots = len(knot_files)
    print("      knots found: %d" % total_knots)

    print("[2/4] loading main chain: %s" % CHAIN_PATH)
    chain_fns, chain_session_ts, chain_rows = load_chain_keys()
    print("      chain rows: %d, indexed filenames: %d" % (chain_rows, len(chain_fns)))

    sidecar_done = load_sidecar_keys()
    if sidecar_done:
        print("      sidecar already holds %d rows (idempotent skip)" % len(sidecar_done))

    print("[3/4] diffing and indexing off-chain knots (batch=%d)" % BATCH_SIZE)
    indexed_now = 0
    already_indexed = 0
    parse_errors = []
    out_f = open(SIDECAR_PATH, "a", encoding="utf-8")
    try:
        batch = []
        for i, fn in enumerate(knot_files, 1):
            if fn in chain_fns:
                already_indexed += 1
            elif fn in sidecar_done:
                already_indexed += 1  # sidecar already covers it; not new
            else:
                path = os.path.join(KNOTS_DIR, fn)
                try:
                    with open(path, "r", encoding="utf-8") as kf:
                        knot = json.load(kf)
                except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
                    parse_errors.append({"knot_file": fn, "error": str(e)[:200]})
                    continue
                # fallback match: chain row without filename linked by session+ts
                if (knot.get("session_id"), knot_ts(knot)) in chain_session_ts:
                    already_indexed += 1
                    continue
                batch.append({
                    "knot_file": fn,
                    "session_id": knot.get("session_id"),
                    "ts": knot_ts(knot),
                    "dominant_theme": knot.get("dominant_theme"),
                    "leaf_hash": knot.get("leaf_hash"),
                    "indexed_by": INDEXED_BY,
                    "indexed_ts": utc_now(),
                })
                if len(batch) >= BATCH_SIZE:
                    for row in batch:
                        out_f.write(json.dumps(row, ensure_ascii=False) + "\n")
                    out_f.flush()
                    indexed_now += len(batch)
                    print("      progress: %d/%d scanned, %d indexed, %d errors"
                          % (i, total_knots, indexed_now, len(parse_errors)))
                    batch = []
            if i % BATCH_SIZE == 0:
                print("      progress: %d/%d scanned, %d indexed, %d errors"
                      % (i, total_knots, indexed_now, len(parse_errors)))
        if batch:
            for row in batch:
                out_f.write(json.dumps(row, ensure_ascii=False) + "\n")
            out_f.flush()
            indexed_now += len(batch)
    finally:
        out_f.close()

    stats = {
        "run_ts": utc_now(),
        "tool": INDEXED_BY,
        "knots_dir": os.path.relpath(KNOTS_DIR, REPO),
        "chain_path": os.path.relpath(CHAIN_PATH, REPO),
        "sidecar_path": os.path.relpath(SIDECAR_PATH, REPO),
        "total_knots_found": total_knots,
        "chain_rows_loaded": chain_rows,
        "already_indexed_count": already_indexed,
        "newly_indexed_count": indexed_now,
        "parse_error_count": len(parse_errors),
        "parse_errors": parse_errors,
        "coverage_note": "sidecar + main chain now cover every parseable knot; "
                         "verkle_chain.jsonl untouched (sidecar is merge-later).",
    }

    os.makedirs(os.path.dirname(STATS_PATH), exist_ok=True)
    with open(STATS_PATH, "w", encoding="utf-8") as sf:
        json.dump(stats, sf, indent=2)
    print("[4/4] stats written: %s" % STATS_PATH)

    room_row = {
        "ts": "2026-09-04",
        "thread": "build",
        "seat": "card-worker",
        "type": "receipt",
        "item": "chain_index_completion",
        "gist": "knots=%d already_indexed=%d newly_indexed=%d parse_errors=%d; "
                "sidecar=%s (verkle_chain.jsonl untouched); honest-errors list in stats"
                % (total_knots, already_indexed, indexed_now, len(parse_errors),
                   os.path.relpath(SIDECAR_PATH, REPO)),
    }
    with open(ROOM_PATH, "a", encoding="utf-8") as rf:
        rf.write(json.dumps(room_row, ensure_ascii=False) + "\n")
    print("room row appended: %s" % ROOM_PATH)

    print("DONE knots=%d already=%d new=%d errors=%d"
          % (total_knots, already_indexed, indexed_now, len(parse_errors)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
