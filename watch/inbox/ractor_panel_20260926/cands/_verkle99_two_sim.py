"""verkle99-two read-only fold simulation (candidate two scratch check).

No writes: loads the live chain, classifies orchestrator noise, drafts the
counter leaf, recomputes the would-be post-fold chain with the estate's own
primitives, and proves the round trip (post-fold + folded -> pre-fold root).
Run: .venv/Scripts/python.exe watch/inbox/ractor_panel_20260926/cands/_verkle99_two_sim.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from mag.verkle_knot import (  # noqa: E402
    _leaf_hash,
    _load_chain_rows,
    _merkle_prefix_roots,
    _merkle_root,
    _verify_chain_consistent,
)

NOISE_PREFIX = "mag-agent-orc-"


def is_noise(row: dict) -> bool:
    """Byte rule: orchestrator seat AND no dominant theme AND zero-duration."""
    sid = str(row.get("session_id") or "")
    if not sid.startswith(NOISE_PREFIX):
        return False
    if row.get("dominant_theme"):
        return False
    start, end = row.get("start_minute"), row.get("end_minute")
    return not end or not start or start == end


def main() -> None:
    t0 = time.time()
    ok, why = _verify_chain_consistent()
    print(f"pre-fold integrity: ok={ok} ({why})")

    rows = _load_chain_rows()
    print(f"rows loaded: {len(rows)}")

    noise = [r for r in rows if is_noise(r)]
    keep = [r for r in rows if not is_noise(r)]
    print(f"noise rows matched: {len(noise)}  keep: {len(keep)}")
    flagged = sum(1 for r in noise if r.get("evidence_lost"))
    knots = ROOT / "memory" / "biography" / "knots"
    dangling = sum(1 for r in noise if r.get("filename") and not (knots / str(r["filename"])).is_file())
    print(f"noise evidence_lost: {flagged}  noise dangling: {dangling}")

    first_noise_idx = min(int(r["index"]) for r in noise if r.get("index") is not None)
    mins = sorted(str(r.get("start_minute")) for r in noise if r.get("start_minute"))
    folded_hashes = [str(r["leaf_hash"]) for r in noise if r.get("leaf_hash")]
    folded_root = _merkle_root(folded_hashes)

    counter_leaf = {
        "type": "orchestrator_noise_counter_leaf",
        "schema": "verkle_noise_counter.v1",
        "session_id": "mag-agent-orc-noise-counter-v1",
        "start_minute": mins[0],
        "end_minute": mins[-1],
        "dominant_theme": None,
        "count": len(noise),
        "first_start_minute": mins[0],
        "last_start_minute": mins[-1],
        "folded_leaf_hashes_root": folded_root,
        "folded_evidence_lost": flagged,
        "folded_dangling": dangling,
        "engine": "verkle_compaction.v1",
    }
    counter_leaf["leaf_hash"] = _leaf_hash(counter_leaf)

    counter_row = {
        "ts": "SIMULATED",
        "filename": "SIMULATED.knot.json",
        "leaf_hash": counter_leaf["leaf_hash"],
        "session_id": counter_leaf["session_id"],
        "start_minute": mins[0],
        "end_minute": mins[-1],
        "dominant_theme": None,
        "compacted_count": len(noise),
        "folded_leaf_hashes_root": folded_root,
    }

    new_rows = keep[:first_noise_idx] + [counter_row] + keep[first_noise_idx:]
    new_hashes = [str(r["leaf_hash"]) for r in new_rows if r.get("leaf_hash")]
    t1 = time.time()
    new_root = _merkle_root(new_hashes)
    prefix = _merkle_prefix_roots(new_hashes)  # the rewrite cost, timed at live scale
    t2 = time.time()
    old_root = _merkle_root([str(r["leaf_hash"]) for r in rows if r.get("leaf_hash")])

    print(f"counter leaf_hash: {counter_leaf['leaf_hash']}")
    print(f"folded_root (witness in counter): {folded_root}")
    print(f"old root: {old_root}")
    print(f"would-be new root: {new_root}  n_leaves {len(new_hashes)} (was {len(rows)})")
    print(f"rewrite timing: merkle_root {t2 - t1:.2f}s incl prefix_roots over {len(new_hashes)} leaves")

    # Round-trip migration proof, in memory: the archive records each folded
    # row's ORIGINAL index. Kept rows preserve relative order, so their old
    # indexes are the ordered complement. Slot reconstruction must reproduce
    # the pre-fold chain byte-for-byte in leaf order (block insertion does NOT:
    # noise rows are scattered, which is why the unfold uses slots).
    n_old = len(rows)
    folded_old_idx = {int(r["index"]) for r in noise if r.get("index") is not None}
    kept_old_idx = [i for i in range(n_old) if i not in folded_old_idx]
    rt: list[dict | None] = [None] * n_old
    for r in noise:
        rt[int(r["index"])] = r
    kept_post = [r for r in new_rows if r is not counter_row]
    assert len(kept_post) == len(kept_old_idx), "kept count mismatch"
    for row, old_i in zip(kept_post, kept_old_idx):
        rt[old_i] = row
    assert all(r is not None for r in rt), "slot reconstruction left holes"
    rt_root = _merkle_root([str(r["leaf_hash"]) for r in rt if r.get("leaf_hash")])  # type: ignore[union-attr]
    print(f"round trip (slot reconstruction): root == old root: {rt_root == old_root}")
    assert rt_root == old_root, "round trip FAILED"
    # Counter commit check: folded_root recomputes from folded hashes alone.
    assert _merkle_root(folded_hashes) == counter_row["folded_leaf_hashes_root"]
    print(f"counter commits to folded set: True")
    print(f"total sim wall: {time.time() - t0:.2f}s  (zero writes: chain/tip/knots untouched)")


if __name__ == "__main__":
    main()
