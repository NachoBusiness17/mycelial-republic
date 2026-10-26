"""verb_anchor -- anchor the verb kifu tail into the verkle chain (THE 50 / W9 / T43, 2026-09-19).

Two hash chains live in this repo and until now nothing tied them together:

  1. THE VERB KIFU   watch/inbox/verb_trace.jsonl -- mag/verb.py's append-only
     execution record (feels / witness / vow / abide / confident ...). Every
     row commits to its predecessor: row["ph"] is the previous hash and
     row["h"] = sha256(prev + canonical row)[:16] (mag/verb.py::_emit).
  2. THE CHAIN       memory/biography/verkle_chain.jsonl -- the Merkle-Verkle
     knot chain (mag/verkle_knot.py), tip in memory/biography/verkle_tip.json,
     the fleet's tamper-evident memory substrate (mag/chain_substrate.py).

This tool anchors (1) into (2): it verifies the kifu hash chain, reads its
tail, and commits the tail hash as ONE live anchor row in the verkle chain.

ONE LIVE ROW: the anchor uses the fixed session_id "verb-anchor", so
append_verkle_knot's amend-in-place path keeps it to a single chain row that
is refreshed (never duplicated) as the kifu grows. Identical content skips;
a grown kifu amends the same row in place.

WHAT THE ROW CARRIES (readable straight off the chain row, no knot file
needed): dossier_commit = the kifu tail hash (the anchor itself),
tension_index = compact pointer "verb_trace@<tail16> rows=N window=W",
dominant_theme = "verb_trace", start/end minute = kifu first/last row ts.

INTEGRITY: refuses to anchor an unverified kifu (verify_trace().breaks > 0),
and mag/verkle_knot.py itself refuses to extend an unverified chain. After
the write an O(log n) inclusion proof is built for the anchor row and
reconstructed; the run only reports ok=True when the proof verification
reaches the committed root.

PURE POSTURE: verb_anchor never writes to verb_trace.jsonl. It is a reader
of the kifu and a writer to the chain; a writer to both would rot its own
anchor by moving the tail it just committed.

Run:
  .venv/Scripts/python.exe tools/verb_anchor.py              # anchor now
  .venv/Scripts/python.exe tools/verb_anchor.py --check      # verify only, no write
  .venv/Scripts/python.exe tools/verb_anchor.py --window 50  # smaller tail census
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

try:
    from config import ROOT
except Exception:  # running as a script, not via the package
    ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag import verb as mag_verb          # noqa: E402  (kifu verifier)
from mag import verkle_knot               # noqa: E402  (the chain)

TRACE = ROOT / "watch" / "inbox" / "verb_trace.jsonl"
CHAIN = ROOT / "memory" / "biography" / "verkle_chain.jsonl"
ANCHOR_SESSION_ID = "verb-anchor"
SCHEMA = "verb_anchor.v1"
DEFAULT_WINDOW = 200


def _parse_ts(ts: str) -> datetime | None:
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except Exception:
        return None


def kifu_state(window: int = DEFAULT_WINDOW) -> dict:
    """Read + verify the verb kifu, return the tail the anchor commits to."""
    if not TRACE.is_file():
        return {"ok": False, "error": f"no verb kifu at {TRACE}"}
    rows = [json.loads(ln) for ln in
            TRACE.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not rows:
        return {"ok": False, "error": "verb kifu is empty"}
    verdict = mag_verb.verify_trace()
    if verdict["breaks"]:
        return {"ok": False,
                "error": (f"refusing to anchor an unverified kifu: "
                          f"{verdict['breaks']} hash breaks in {verdict['rows']} rows"),
                "kifu": verdict}
    tail = rows[-window:]
    tail_hash = str(rows[-1].get("h") or "")
    if not tail_hash:
        return {"ok": False, "error": "kifu tail row carries no hash to anchor"}
    census = Counter(str(r.get("verb") or "?") for r in tail)
    first_ts, last_ts = str(tail[0].get("ts") or ""), str(tail[-1].get("ts") or "")
    return {"ok": True, "rows_total": verdict["rows"], "legacy_rows": verdict["legacy"],
            "breaks": verdict["breaks"], "healthy": verdict["healthy"],
            "tail_hash": tail_hash, "tail_ts": last_ts, "first_ts": first_ts,
            "window": len(tail), "verb_census": dict(census)}


def _dossier(k: dict) -> dict:
    """Dossier shaped for verkle_knot.build_leaf_from_dossier: the fields that
    survive into the leaf and the chain row carry the anchor binding."""
    t0, t1 = _parse_ts(k["first_ts"]), _parse_ts(k["tail_ts"])
    minutes = None
    if t0 and t1:
        minutes = round((t1 - t0).total_seconds() / 60.0, 3)
    pointer = (f"verb_trace@{k['tail_hash']} rows={k['rows_total']} "
               f"window={k['window']}")
    return {
        "session_id": ANCHOR_SESSION_ID,
        "time": {
            "created_at": {"iso_minute": k["first_ts"], "date": k["first_ts"][:10]},
            "updated_at": {"iso_minute": k["tail_ts"]},
        },
        "scalar_knot": {
            "duration_minutes": minutes,
            "tension_index": pointer,
            "theme_vector": {
                "basis": ["verb_trace"],
                "dominant": "verb_trace",
                "raw": [1.0],
                "normalized": [1.0],
            },
        },
        "content_commit": {"hex": k["tail_hash"]},
    }


def anchor_row() -> dict | None:
    """The current anchor row from the chain (None = not anchored yet)."""
    if not CHAIN.is_file():
        return None
    for ln in reversed(CHAIN.read_text(encoding="utf-8").splitlines()):
        if not ln.strip():
            continue
        r = json.loads(ln)
        if str(r.get("session_id") or "") == ANCHOR_SESSION_ID:
            return r
    return None


def _proof_for(index: int) -> dict:
    p = verkle_knot.prove(index)
    return {"index": p.get("index"), "verified": bool(p.get("verified")),
            "equation": p.get("equation"), "error": p.get("error")}


def anchor(window: int = DEFAULT_WINDOW) -> dict:
    """Verify the kifu, commit its tail as the one live anchor row, prove it."""
    k = kifu_state(window)
    if not k.get("ok"):
        return {"ok": False, "schema": SCHEMA, "error": k.get("error"),
                "kifu": k.get("kifu", {})}
    res = verkle_knot.append_verkle_knot(_dossier(k))
    if not res.get("ok"):
        return {"ok": False, "schema": SCHEMA, "error": res.get("error", "chain append refused"),
                "chain_result": res, "kifu_tail": k["tail_hash"]}
    row = anchor_row()
    if row is None:
        return {"ok": False, "schema": SCHEMA, "error": "anchor row vanished after append"}
    proof = _proof_for(int(row.get("index", -1)))
    bound = str(row.get("dossier_commit") or "") == k["tail_hash"]
    return {
        "ok": bool(proof.get("verified") and bound),
        "schema": SCHEMA,
        "anchored": not bool(res.get("skipped")),
        "amended": bool(res.get("amended")),
        "anchor_row": {
            "index": row.get("index"),
            "filename": row.get("filename"),
            "leaf_hash": row.get("leaf_hash"),
            "verkle_root": (row.get("verkle_root") or "")[:16],
            "dossier_commit": row.get("dossier_commit"),
            "tension_index": row.get("tension_index"),
        },
        "kifu_tail": k["tail_hash"],
        "binding_holds": bound,
        "inclusion_proof": proof,
        "chain_root": (res.get("verkle_root") or "")[:16],
        "n_leaves": res.get("n_leaves"),
        "kifu": {kk: k[kk] for kk in ("rows_total", "legacy_rows", "breaks",
                                      "healthy", "tail_ts", "window", "verb_census")},
    }


def check(window: int = DEFAULT_WINDOW) -> dict:
    """Verify-only: is the live anchor row still bound to the kifu tail?"""
    k = kifu_state(window)
    row = anchor_row()
    if not k.get("ok"):
        return {"ok": False, "schema": SCHEMA, "check": True,
                "error": k.get("error"), "kifu": k.get("kifu")}
    if row is None:
        return {"ok": False, "schema": SCHEMA, "check": True,
                "error": "no anchor row in the chain yet (run without --check)"}
    bound = str(row.get("dossier_commit") or "") == k["tail_hash"]
    proof = _proof_for(int(row.get("index", -1)))
    return {"ok": bool(bound and proof.get("verified")), "schema": SCHEMA, "check": True,
            "binding_holds": bound,
            "anchor_row": {"index": row.get("index"), "dossier_commit": row.get("dossier_commit"),
                           "tension_index": row.get("tension_index")},
            "kifu_tail": k["tail_hash"], "inclusion_proof": proof,
            "kifu": {kk: k[kk] for kk in ("rows_total", "breaks", "healthy", "window")}}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="anchor the verb kifu tail into the verkle chain")
    ap.add_argument("--check", action="store_true", help="verify only, write nothing")
    ap.add_argument("--window", type=int, default=DEFAULT_WINDOW,
                    help=f"tail rows summarized in the anchor (default {DEFAULT_WINDOW})")
    a = ap.parse_args(argv)
    out = check(a.window) if a.check else anchor(a.window)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
