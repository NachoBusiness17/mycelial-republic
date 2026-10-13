#!/usr/bin/env python3
"""chain_repair — standing verb for the verkle chain race class.

Cause class (proven twice on bytes, 2026-09-27, receipts
CHAIN_RACE_REPAIR_20260927.md + the burn-down addendum): concurrent
append from a long-lived process running OLDER verkle_knot code (module
loaded at process start) computes its committed root from a pre-race leaf
set; the verify gate then refuses every append and downstream organs
(memlang anchoring, wave ticks) freeze. The post-append self-heal in
mag/verkle_knot (landed 2026-09-27) cures NEW appends in processes on
current code; this verb repairs the already-committed bad tail row(s)
whenever a mixed-version writer strikes again.

What it does: under the module's own verkle_lock, walk from the tail to
the first row whose committed verkle_root != merkle(all leaf hashes through
that row); rewrite that row's root fields to the recomputed truth; stamp a
chain_race_repaired note naming this tool; refresh the tip; verify.

Exit 0 = chain was consistent or repaired green; 1 = still broken (do not
loop — file the incident); 2 = unexpected shape.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.verkle_knot import (  # noqa: E402
    _load_chain_rows, _merkle_root, _verify_chain_consistent, verkle_lock,
    _tip_for_tail, _write_tip_atomic, TIP, CHAIN,
)


def find_bad_tail_index(rows: list[dict]) -> int | None:
    hashes: list[str] = []
    for i, r in enumerate(rows):
        if r.get("leaf_hash"):
            hashes.append(str(r["leaf_hash"]))
        if r.get("verkle_root") and r["verkle_root"] != _merkle_root(hashes):
            return i
    return None


def repair(*, dry: bool = False) -> int:
    ok, why = _verify_chain_consistent()
    if ok:
        print(f"CHAIN-REPAIR: nothing to do ({why})")
        return 0
    with verkle_lock(timeout=120.0):
        rows = _load_chain_rows()
        bad_i = find_bad_tail_index(rows)
        if bad_i is None:
            print("CHAIN-REPAIR: re-verify under lock says consistent; racy read")
            return 0
        bad = rows[bad_i]
        old_root = str(bad.get("verkle_root"))
        hashes = [str(r["leaf_hash"]) for r in rows if r.get("leaf_hash")]
        true_root = _merkle_root(hashes)
        true_parent = _merkle_root(hashes[:-1]) if len(hashes) > 1 else ""
        print(f"CHAIN-REPAIR: row {bad_i} ({bad.get('session_id')}) "
              f"{old_root[:16]} -> {true_root[:16]}"
              + (" [dry]" if dry else ""))
        if dry:
            return 0
        bad["verkle_root"] = true_root
        bad["parent_verkle_root"] = true_parent
        bad["n_leaves"] = len(hashes)
        bad["chain_race_repaired"] = (
            f"{datetime.now(timezone.utc).date().isoformat()}: committed root "
            "was computed over a pre-race leaf set (mixed-version concurrent "
            "append); tools/chain_repair.py; receipts under watch/inbox/")
        lines = CHAIN.read_text(encoding="utf-8", errors="replace").splitlines()
        if len(lines) != len(rows):
            print(f"CHAIN-REPAIR: row/line count mismatch "
                  f"({len(rows)} rows vs {len(lines)} lines); refusing")
            return 2
        lines[bad_i] = json.dumps(bad, ensure_ascii=False)
        tmp = CHAIN.with_suffix(".jsonl.tmp")
        tmp.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
        tmp.replace(CHAIN)
        tip = _tip_for_tail(rows, hashes, true_root)
        # T1W1 ticket 4 (2026-10-01, RACTOR): the chain got tmp+replace three
        # lines up but the tip rode a bare TIP.write_text, so a torn tip write
        # froze every later append via the integrity gate (which since T1W1
        # ticket 7 fails closed on a corrupt tip). Rides the same atomic
        # writer the main path uses (_write_tip_atomic, the AG5 contract).
        _write_tip_atomic(tip)
    ok2, why2 = _verify_chain_consistent()
    print(f"CHAIN-REPAIR: post-verify {ok2} ({why2})")
    return 0 if ok2 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    return repair(dry=a.dry)


if __name__ == "__main__":
    sys.exit(main())
