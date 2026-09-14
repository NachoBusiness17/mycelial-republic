"""chain_guard.py — the verkle chain canary (2026-08-25).

THE INCIDENT: 2026-08-25 ~13:38 the live chain was rebuilt from a PRE-REPAIR
lineage (1,039 evidence_lost flags -> 0, the 6 duplicate rows back) by a raw
restore outside verkle_lock. Source unidentified; no code path in the repo
restores backups over the live chain. Both seats' flags have now been lost
twice to silent restores. Trust is not the fix — a CANARY is.

The canary: a repair-state marker records what the repaired chain SHOULD look
like (evidence_lost count, root, timestamp, who). check() compares the live
chain against it. If evidence_lost ever drops while dangling rows remain, a
pre-repair restore happened — REGRESSION, alarm loudly.

CLI:
  python -m mag.chain_guard check                     # healthy / regression
  python -m mag.chain_guard mark --expected N --root <root> [--note "..."]
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

CHAIN = ROOT / "memory" / "biography" / "verkle_chain.jsonl"
KNOTS = ROOT / "memory" / "biography" / "knots"
MARKER = ROOT / "memory" / "biography" / "verkle_repair_state.json"
TIP = ROOT / "memory" / "biography" / "verkle_tip.json"


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_rows() -> list[dict]:
    if not CHAIN.is_file():
        return []
    return [json.loads(l) for l in CHAIN.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]


def _tip_root() -> str | None:
    if TIP.is_file():
        try:
            return str(json.loads(TIP.read_text(encoding="utf-8")).get("root") or "")[:16]
        except Exception:  # noqa: BLE001
            return None
    return None


def mark(*, expected: int, root: str = "", note: str = "", by: str = "chain_guard") -> dict:
    """Write the repair-state canary. Call AFTER a repair lands on a quiesced chain."""
    state = {
        "schema": "verkle_repair_state.v1",
        "evidence_lost_expected": int(expected),
        "repair_root": str(root)[:16],
        "marked_at": _utc(),
        "marked_by": by,
        "note": note,
    }
    MARKER.parent.mkdir(parents=True, exist_ok=True)
    MARKER.write_text(json.dumps(state, indent=2), encoding="utf-8")
    return {"ok": True, **state}


def check() -> dict:
    """Compare the live chain against the canary. The alarm every seat watches."""
    rows = _load_rows()
    dangling = [r for r in rows if r.get("filename") and not (KNOTS / str(r["filename"])).is_file()]
    flagged = [r for r in rows if r.get("evidence_lost")]
    sids = [r.get("session_id") for r in rows]
    dups = len(sids) - len(set(sids))
    tip_root = _tip_root()

    # ── tip-vs-chain canary (2026-09-11, Hermes boot finding) ──
    # The CHAIN_STOP incident proved that the tip bookmark and the chain rows
    # can diverge silently (tip froze at a poisoned snapshot while rows
    # continued). This check recomputes the merkle root from the chain rows
    # and compares against the tip. If they diverge, the tip is stale or
    # poisoned.
    chain_root_match = None
    chain_root = None
    try:
        from mag.verkle_knot import _load_chain_rows, _merkle_root
        rows_v = _load_chain_rows()
        hashes = [r.get("leaf_hash") for r in rows_v if r.get("leaf_hash")]
        if hashes:
            chain_root = _merkle_root(hashes)
            if tip_root:
                chain_root_match = (chain_root[:16] == tip_root[:16])
    except Exception:
        chain_root_match = None  # can't compute — report, don't alarm

    live = {
        "rows": len(rows),
        "dangling": len(dangling),
        "evidence_lost": len(flagged),
        "dup_sessions": dups,
        "tip_root": _tip_root(),
        "chain_root": chain_root[:16] if chain_root else None,
        "tip_matches_chain": chain_root_match,
    }

    if not MARKER.is_file():
        return {"ok": True, "state": "unmarked", **live,
                "note": "no repair-state marker yet — run `mark` after the next repair lands"}

    try:
        m = json.loads(MARKER.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {"ok": False, "state": "marker_unreadable", **live}

    expected = int(m.get("evidence_lost_expected") or 0)
    # THE LAW (2026-08-25, corrected after a false alarm): a dangling row
    # WITHOUT the evidence_lost flag is the only regression. A flagged count
    # BELOW the marker's expected is NOT a regression by itself — lost
    # sessions legitimately re-folded into real knots stop being dangling and
    # stop being flagged (recovery, not stripping). Absolute-count drift is
    # reported, not alarmed.
    unflagged_dangling = [r for r in dangling if not r.get("evidence_lost")]
    regression = len(unflagged_dangling) > 0
    state = "regression" if regression else "healthy"
    return {
        "ok": not regression,
        "state": state,
        **live,
        "dangling_unflagged": len(unflagged_dangling),
        "expected_evidence_lost": expected,
        "flag_drift": expected - len(flagged),
        "marker_root": m.get("repair_root"),
        "marker_at": m.get("marked_at"),
        "alarm": ("REGRESSION: dangling row(s) lack the evidence_lost flag — a pre-repair "
                  "restore or flag-stripping amend happened.") if regression else None,
    }


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    ap = argparse.ArgumentParser(prog="chain-guard", description="Verkle chain canary")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("check", help="compare live chain against the canary")
    p = sub.add_parser("mark", help="write the canary after a repair lands")
    p.add_argument("--expected", type=int, required=True)
    p.add_argument("--root", default="")
    p.add_argument("--note", default="")
    p.add_argument("--by", default="chain_guard")
    a = ap.parse_args(argv)
    if a.cmd == "check":
        print(json.dumps(check(), indent=2, default=str))
    else:
        print(json.dumps(mark(expected=a.expected, root=a.root, note=a.note, by=a.by), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
