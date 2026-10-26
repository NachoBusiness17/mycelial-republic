"""State snapshot — in-the-moment classification for posterity + training.

Every session/escalation contributes a structured "current state summary" to a
local pile (memory/pile/state_summaries.jsonl). The overnight job
(tools/pile_classify.py) later drains the pile with a local model and folds the
classifications into case law + training rows.

This is the "classification in the moment model": capture the structured
summary (goal/outcome/tier/lessons) at the moment it happens — cheap,
deterministic, provenance-attached — instead of re-deriving it later.

Q48 production broker wiring (2026-10-01,
watch/inbox/mountain_climb/FIFTY_QUESTIONS_ANSWERED.md): a production capture
also files its durable evidence through the effect broker — switchboard
propose -> grant -> mark_executing -> effect_broker.execute("board_write") ->
complete/fail -> commit_receipt (the swarm_cycle._blackboard_note pattern,
mag/swarm_cycle.py:109) — and the broker banks one meter row on
memory/runs/effect_broker/effects.jsonl. Every row (pile + meter + board note)
carries the same corr_id (env MAG_CORR_ID per the AH14 law; a fresh uuid4
hex8 mint when the lane set none, the duel_harness series-mint shape), so
`tools/estate_query.py --corr` joins them. board_write is used because it is
the one effect class estate policy lets headless tooling dispatch (fs_write /
model_call / lane_spawn / tool_invoke / network_access are operator-tier per
switchboard_v2._implicit_authority + policy require_confirmation) — the pile
row itself stays the classify feed, unchanged.

Fail-visible law: a capture whose broker evidence cannot be banked returns
ok=False with the incident named (the pile row is still returned — it did
land); an effect that cannot be banked is an incident, not a silent pass.
The meter meters production work only (AH18 law): when PILE is redirected
off the production pile (this organ's test convention, tests/test_state_pile.
py _iso), the filing is skipped with a loud `skipped` marker, never a test
row on the production ledger.

Callers:
  escalate_on_loop (wired)   → kind=escalation
  session close / run close  → kind=session_end (callable / CLI)
  operator / seat            → any moment worth keeping

CLI:
  python -m mag.state_snapshot capture --goal "..." --outcome ok --tier local [--lesson "..."]
  python -m mag.state_snapshot status
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import ROOT  # noqa: E402

PILE_DIR = ROOT / "memory" / "pile"
PILE = PILE_DIR / "state_summaries.jsonl"
CLASSIFIED = PILE_DIR / "classified.jsonl"
TRAINING = PILE_DIR / "training_rows.jsonl"

# Production pile, captured at import.  The broker filing gates on
# PILE == _PROD_PILE: tests redirect ss.PILE (the established convention for
# this organ) and thereby opt the capture out of the production meter —
# structurally, not by discipline (the B2-336 conftest principle, applied at
# the organ seam because this organ's ledger gate lives here).
_PROD_PILE = PILE

_KINDS = {"session_end", "escalation", "run_close", "autoaim", "operator"}
_OUTCOMES = {"ok", "fail", "escalated", "loop", "unknown"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _append(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def _load_ids(path: Path) -> set[str]:
    """ids AND state_hashes already in the pile (dedup keys)."""
    if not path.is_file():
        return set()
    keys = set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            row = json.loads(line)
            keys.add(row.get("id"))
            if row.get("state_hash"):
                keys.add(row.get("state_hash"))
        except (json.JSONDecodeError, TypeError):
            continue
    return keys


def _state_hash(goal: str, outcome: str, kind: str, tier: str) -> str:
    return hashlib.sha256(f"{kind}|{tier}|{goal}|{outcome}".encode("utf-8")).hexdigest()[:16]


def _capture_corr_id() -> str:
    """corr_id for one capture: env MAG_CORR_ID wins (AH14 law,
    mag/trajectory_step.py — joins the lane's trajectory/burns/duel rows);
    a fresh uuid4 hex8 mint when the lane set none (the duel_harness
    series-mint shape, tools/duel_harness.py series_corr_id), so the pile
    row and the broker meter row share one id even outside a corr-carrying
    lane."""
    from mag.trajectory_step import corr_id
    return corr_id() or uuid.uuid4().hex[:8]


def _file_broker_evidence(row: dict[str, Any], corr: str) -> dict[str, Any]:
    """File the capture's durable evidence through the effect broker (Q48).

    Full authority mesh, the swarm_cycle._blackboard_note pattern
    (mag/swarm_cycle.py:109): switchboard propose (tool-output label —
    truthful, this organ is deterministic tooling) -> grant ->
    mark_executing -> effect_broker.execute("board_write") ->
    complete/fail -> commit_receipt.  The broker banks one effects.jsonl
    meter row whose corr_id is the note's `event` (= `corr`), joining the
    pile row.  The grant event_id carries a unique suffix (corr + row id)
    because the switchboard replay guard denies a second grant on the same
    event_id and a corr-carrying lane may capture more than once.

    Skips (loudly) when PILE is not the production pile: the production
    meter meters production work only.  Never raises — every failure is
    returned as {"ok": False, "error": ...} so capture_summary can report
    the incident instead of the caller's try/except swallowing it.
    """
    if PILE.resolve() != _PROD_PILE.resolve():
        return {"ok": True, "skipped": "non-production pile; no broker row banked"}
    try:
        from mag import effect_broker as eb
        from mag import switchboard_v2 as sb

        summary = (f"state_snapshot {row['kind']}: outcome={row['outcome']} "
                   f"tier={row.get('tier') or '-'} "
                   f"goal='{(row.get('goal') or '')[:120]}' row={row['id']}")
        note = {
            "ts": row["ts"],
            "owner": "state_snapshot",
            "kind": "state_summary",
            "text": summary,
            "event": corr,  # write_board_note persists this; the broker's
                            # meter row takes its corr_id from here
        }
        proposal = sb.propose(
            event_id=f"{corr}-{row['id']}",
            requested_effect="board_write",
            capabilities=["board_write"],
            memory_scope="state_snapshot",
            budget={"max_calls": 3},
            ttl_seconds=900,
            content=summary,
            source="state_snapshot",
            authority_label="tool-output",
        )
        authority = sb.grant(proposal)
        if authority.get("status") != "AUTHORIZED":
            return {"ok": False,
                    "error": f"switchboard denied: {authority.get('deny_reason')}",
                    "authority_status": authority.get("status")}
        executing = sb.mark_executing(
            authority, {"effect": "board_write", "organ": "state_snapshot"})
        receipt = eb.execute("board_write", {"note": note}, executing)
        result = receipt.get("result", {}) or {}
        if receipt.get("status") == "RECEIPT_COMMITTED" and result.get("ok"):
            terminal = sb.complete(
                executing,
                {"broker_receipt": receipt.get("receipt_path"),
                 "path": result.get("path"), "seq": result.get("seq"),
                 "effect_row_logged": result.get("effect_row_logged", False)},
            )
        else:
            terminal = sb.fail(
                executing,
                receipt.get("error") or result.get("err") or "board_write failed",
                {"broker_receipt": receipt.get("receipt_path"), "result": result},
            )
        committed = sb.commit_receipt(terminal, receipt)
        ok = bool(committed.get("ok") and result.get("ok"))
        out = {
            "ok": ok,
            "effect": "board_write",
            "corr_id": corr,
            "seq": result.get("seq"),
            "path": result.get("path"),
            "receipt": receipt.get("receipt_path"),
            "authority_status": (committed.get("decision") or {}).get("status"),
            "meter_row": bool(result.get("effect_row_logged")),
        }
        if not ok:
            out["error"] = (receipt.get("error") or result.get("err")
                            or "switchboard receipt commit failed")
        return out
    except Exception as e:
        # Incident, never a silent pass: the exception is named in the return
        # so callers that check the dict see it even if their own try/except
        # would have swallowed a raise.
        return {"ok": False, "error": f"broker filing raised: {e!r}"}


def capture_summary(
    *,
    goal: str = "",
    outcome: str = "unknown",
    tier: str = "",
    kind: str = "session_end",
    lessons: list[str] | None = None,
    source: str = "",
    session_id: str | None = None,
    state_hash: str | None = None,
) -> dict[str, Any]:
    """Append one structured state summary to the pile (dedup by state_hash)
    and file its durable evidence through the effect broker (Q48 wiring)."""
    outcome = outcome if outcome in _OUTCOMES else "unknown"
    kind = kind if kind in _KINDS else "session_end"
    sh = state_hash or _state_hash(goal, outcome, kind, tier)
    if sh in _load_ids(PILE):
        return {"ok": False, "error": "duplicate state (already captured)", "id": sh}
    corr = _capture_corr_id()
    row = {
        "id": f"st-{uuid.uuid4().hex[:10]}",
        "ts": _now(),
        "kind": kind,
        "tier": tier[:24],
        "source": source[:60],
        "goal": (goal or "")[:300],
        "outcome": outcome,
        "lessons": [str(l)[:200] for l in (lessons or [])[:3]],
        "session_id": session_id,
        "state_hash": sh,
        "corr_id": corr,
        "classified": False,
    }
    _append(PILE, row)
    broker = _file_broker_evidence(row, corr)
    if broker.get("ok"):
        return {"ok": True, "row": row, "broker": broker}
    # Fail-visible: the pile row landed but the brokered evidence could not
    # be banked — an incident, not a silent pass.  The row is still returned
    # (it exists on the pile); ok=False is what the CLI turns into exit 1.
    return {"ok": False,
            "error": f"broker evidence filing failed: {broker.get('error')}",
            "row": row, "broker": broker}


def status() -> dict[str, Any]:
    from collections import Counter

    rows = [json.loads(l) for l in PILE.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()] if PILE.is_file() else []
    kinds = Counter(r.get("kind") for r in rows)
    outcomes = Counter(r.get("outcome") for r in rows)
    classified_n = sum(1 for r in rows if r.get("classified"))
    return {
        "ok": True,
        "schema": "state_snapshot.v1",
        "pile": len(rows),
        "classified": classified_n,
        "unclassified": len(rows) - classified_n,
        "by_kind": dict(kinds),
        "by_outcome": dict(outcomes),
        "pile_path": str(PILE),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="state-snapshot", description="In-the-moment state summary capture.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_cap = sub.add_parser("capture")
    p_cap.add_argument("--goal", default="")
    p_cap.add_argument("--outcome", choices=list(_OUTCOMES), default="unknown")
    p_cap.add_argument("--tier", default="")
    p_cap.add_argument("--kind", choices=list(_KINDS), default="session_end")
    p_cap.add_argument("--lesson", action="append")
    p_cap.add_argument("--source", default="")
    p_cap.add_argument("--session-id", default=None)
    sub.add_parser("status")
    args = ap.parse_args(argv)

    if args.cmd == "capture":
        r = capture_summary(goal=args.goal, outcome=args.outcome, tier=args.tier, kind=args.kind,
                            lessons=args.lesson, source=args.source, session_id=args.session_id)
        print(json.dumps(r, indent=2, ensure_ascii=False))
        # Q48 fail-visible: a capture whose brokered evidence could not be
        # banked is an incident — exit 1, never a silent pass.
        return 0 if r.get("ok") else 1
    else:
        print(json.dumps(status(), indent=2, ensure_ascii=False))
        return 0



if __name__ == "__main__":
    raise SystemExit(main())
