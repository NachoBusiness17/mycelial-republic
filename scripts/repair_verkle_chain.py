"""Repair dangling verkle chain rows using by-session pointer files. (2026-08-25)

The lost-update race (fixed same day by verkle_lock in mag/verkle_knot.py) left
chain rows pointing at knot filenames that had been unlinked by an amend whose
chain rewrite was clobbered. Evidence survives:
  - knots/by-session_{sid}.json pointers → the CURRENT knot file per session
  - the knot files themselves (leaf_hash + full leaf payload)

Repair algorithm (under verkle_lock, whole run):
  1. Load chain rows. For every row whose filename is missing on disk:
     resolve the session's by-session pointer; if that target file exists,
     adopt it: filename := pointer target, leaf_hash/theme fields := knot file.
  2. Dedupe: keep the LAST row per session_id (same rule as consolidate).
  3. Hand the corrected rows to _consolidate_chain_one_leaf_per_session_unlocked
     which rewrites the chain (recomputed indices/roots), tip, and evolution.

Default is DRY RUN: prints the plan. --apply executes it.
Unrecoverable rows (no resolvable file) are reported and KEPT with an
`evidence_lost` flag — never silently dropped, never fabricated.

CLI:
  python scripts/repair_verkle_chain.py            # dry run
  python scripts/repair_verkle_chain.py --apply    # do it
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag.verkle_knot import (  # noqa: E402
    CHAIN,
    KNOTS,
    verkle_lock,
)


def _pointer_name(session_id: str) -> Path:
    sid = re.sub(r"[^A-Za-z0-9._-]+", "-", str(session_id or ""))[:12]
    return KNOTS / f"by-session_{sid}.json"


def _knot_fields(fname: str) -> dict | None:
    p = KNOTS / fname
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def plan_and_repair(apply: bool) -> int:
    rows = [json.loads(l) for l in CHAIN.read_text(encoding="utf-8").splitlines() if l.strip()]
    knots = {p.name for p in KNOTS.glob("*.knot.json")}
    dangling = [r for r in rows if r.get("filename") and r["filename"] not in knots]
    print(f"chain rows: {len(rows)}  dangling: {len(dangling)}")

    repaired, unrecoverable = [], []
    for r in rows:
        if r.get("filename") and r["filename"] in knots:
            continue
        sid = r.get("session_id") or ""
        ptr = _pointer_name(sid)
        target = None
        if ptr.is_file():
            try:
                target = json.loads(ptr.read_text(encoding="utf-8")).get("filename")
            except (json.JSONDecodeError, OSError):
                target = None
        if target and target in knots:
            knot = _knot_fields(target) or {}
            r["filename"] = target
            if knot.get("leaf_hash"):
                r["leaf_hash"] = knot["leaf_hash"]
            for k in ("dominant_theme", "theme_vector_normalized", "tension_index", "dossier_commit"):
                if knot.get(k) is not None:
                    r[k] = knot[k]
            r["repaired_from_pointer"] = True
            repaired.append(r["session_id"])
        else:
            r["evidence_lost"] = True
            unrecoverable.append((r.get("session_id"), r.get("filename")))

    print(f"recoverable via pointer: {len(repaired)}")
    print(f"unrecoverable (kept, flagged evidence_lost): {len(unrecoverable)}")
    for sid, fn in unrecoverable[:10]:
        print(f"  LOST sid={sid} file={fn}")

    # dedupe check (last-per-session wins, consolidate enforces the same rule)
    sids = [r.get("session_id") for r in rows]
    dups = len(sids) - len(set(sids))
    print(f"duplicate-session rows to be dropped by consolidate: {dups}")

    if not apply:
        print("DRY RUN — no changes written. Re-run with --apply.")
        return 0

    from mag.verkle_knot import _consolidate_chain_one_leaf_per_session_unlocked
    with verkle_lock():
        # rows were read pre-lock; re-read under lock and re-apply repairs so we
        # never clobber an append that happened while we were planning
        fresh = [json.loads(l) for l in CHAIN.read_text(encoding="utf-8").splitlines() if l.strip()]
        fresh_knots = {p.name for p in KNOTS.glob("*.knot.json")}
        fix_by_sid = {r.get("session_id"): r for r in rows if r.get("repaired_from_pointer") or r.get("evidence_lost")}
        for r in fresh:
            sid = r.get("session_id")
            if sid in fix_by_sid and r.get("filename") and r["filename"] not in fresh_knots:
                fix = fix_by_sid[sid]
                if fix.get("repaired_from_pointer"):
                    for k in ("filename", "leaf_hash", "dominant_theme",
                              "theme_vector_normalized", "tension_index", "dossier_commit"):
                        if fix.get(k) is not None:
                            r[k] = fix[k]
                    r["repaired_from_pointer"] = True
                else:
                    r["evidence_lost"] = True
        CHAIN.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in fresh) + "\n",
                         encoding="utf-8")
        out = _consolidate_chain_one_leaf_per_session_unlocked()
    print("consolidate:", {k: out[k] for k in ("ok", "before", "after", "removed")})
    print("new root:", out.get("root"))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true", help="execute (default: dry run)")
    args = ap.parse_args()
    return plan_and_repair(apply=args.apply)


if __name__ == "__main__":
    raise SystemExit(main())
