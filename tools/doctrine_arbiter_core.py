"""Core of the doctrine arbiter: validation law, ledger fold, check pass,
scorecard (R10, 2026-09-30). The tool's full spec (three laws, instrument
metric tables, verdict semantics) lives in the entrypoint docstring
tools/doctrine_arbiter.py; this module is that spec as code."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Optional

from tools.doctrine_arbiter_instruments import (
    InstrumentPaths, InstrumentError, MEASURERS)

ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "memory" / "doctrine" / "LEDGER.jsonl"
SCORECARD_PATH = ROOT / "memory" / "doctrine" / "scorecard_latest.json"

KINDS = ("rib", "spec_amendment", "route_pitch")
OPS = ("==", "!=", "<", "<=", ">", ">=")
STATUSES = ("PENDING", "VINDICATED", "EXPIRED", "VOID", "RETIRED")
TERMINAL = ("VINDICATED", "EXPIRED")
ANOMALY_SURFACES = ("steps", "oral_law_index", "burns_ledger")
EXIT_OK, EXIT_ATTENTION, EXIT_ERROR = 0, 1, 2

# metric tables per instrument: metric name -> required selector keys
INSTRUMENTS: dict[str, dict[str, tuple[str, ...]]] = {
    "gps_ledger": {"pass_rate": ("model_id", "task_shape"),
                   "sample_size": ("model_id", "task_shape")},
    "duel_table": {"win_rate": ("model",), "decided": ("model",),
                   "ties": ("model",)},
    "parity_gate": {"parity_ok": (), "diverged_seqs": ()},
    "anomaly_counts": {"anomaly_count": ()},
}
OPTIONAL_SELECTOR_KEYS: dict[str, set[str]] = {
    "gps_ledger": set(), "duel_table": set(),
    "parity_gate": {"mode"}, "anomaly_counts": {"surface"},
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def utc_today() -> date:
    return datetime.now(timezone.utc).date()


# ------------------------------------------------------------ validation ----

def parse_deadline(value: str) -> Optional[date]:
    """ISO YYYY-MM-DD or None. Dates only: a deadline is a day the
    prediction must have materialized by (checks run at day grain)."""
    try:
        return date.fromisoformat(str(value).strip())
    except (ValueError, TypeError):
        return None


def prediction_void_reasons(item: dict[str, Any]) -> list[str]:
    """The pre-registration law as code. Returns every reason the item's
    four-tuple {id, source_verdict, predicted_outcome, deadline} fails
    the registration contract; empty list = active doctrine."""
    reasons: list[str] = []
    if not str(item.get("id") or "").strip():
        reasons.append("id missing")
    if not str(item.get("source_verdict") or "").strip():
        reasons.append("source_verdict missing")
    if parse_deadline(item.get("deadline", "")) is None:
        reasons.append(f"deadline unparseable: {item.get('deadline')!r}")
    pred = item.get("predicted_outcome")
    if not isinstance(pred, dict) or not pred:
        reasons.append("pre-registration law: no predicted_outcome")
        return reasons
    if (not str(pred.get("instrument") or "").strip()
            and not str(pred.get("metric") or "").strip()
            and pred.get("value") is None):
        reasons.append("pre-registration law: no predicted_outcome")  # all-blank
        return reasons
    instrument = pred.get("instrument")
    if instrument not in INSTRUMENTS:
        reasons.append(f"unknown instrument: {instrument!r}")
        return reasons
    metric = pred.get("metric")
    if metric not in INSTRUMENTS[instrument]:
        reasons.append(f"unknown metric {metric!r} for instrument {instrument!r}")
        return reasons
    selector = pred.get("selector")
    if not isinstance(selector, dict):
        reasons.append("selector missing/not an object")
        return reasons
    required = INSTRUMENTS[instrument][metric]
    for key in required:
        if not str(selector.get(key) or "").strip():
            reasons.append(f"selector.{key} required for {instrument}.{metric}")
    allowed = set(required) | OPTIONAL_SELECTOR_KEYS[instrument]
    reasons.extend(f"selector.{key} not a {instrument} key"
                   for key in selector if key not in allowed)
    if instrument == "anomaly_counts" and selector.get("surface") not in (
            None,) + ANOMALY_SURFACES:
        reasons.append(f"unknown surface: {selector['surface']!r}")
    if pred.get("op") not in OPS:
        reasons.append(f"unknown op: {pred.get('op')!r}")
    if not isinstance(pred.get("value"), (int, float, bool)):
        reasons.append("value missing or not number/bool")
    return reasons


def compare(measured: Any, op: str, value: Any) -> bool:
    """The predicate. Numbers compare numerically; bools as bools; ==/!=
    also tolerate cross-kind (1 == True) exactly like Python. Ordering
    ops on incomparable kinds are False, never a crash."""
    if op == "==":
        return measured == value
    if op == "!=":
        return measured != value
    try:
        return {"<": measured < value, "<=": measured <= value,
                ">": measured > value, ">=": measured >= value}[op]
    except TypeError:
        return False


# ------------------------------------------------------------- the ledger ---

def append_row(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")


def read_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                rows.append(json.loads(stripped))
    return rows


@dataclass
class DoctrineItem:
    """One doctrine id's derived state (the fold of its ledger rows)."""

    id: str
    kind: str = ""
    claim: str = ""
    source_verdict: str = ""
    predicted_outcome: dict[str, Any] = field(default_factory=dict)
    deadline: str = ""
    registered_ts: str = ""
    status: str = "PENDING"
    void_reasons: list[str] = field(default_factory=list)
    checks: list[dict[str, Any]] = field(default_factory=list)
    vindicated_ts: Optional[str] = None
    expired_ts: Optional[str] = None
    retired_ts: Optional[str] = None
    retire_note: str = ""

    @property
    def retire_candidate(self) -> bool:
        return self.status == "EXPIRED"

    def as_dict(self) -> dict[str, Any]:
        return {"id": self.id, "kind": self.kind, "claim": self.claim,
                "source_verdict": self.source_verdict,
                "predicted_outcome": self.predicted_outcome,
                "deadline": self.deadline,
                "registered_ts": self.registered_ts, "status": self.status,
                "void_reasons": self.void_reasons,
                "checks_n": len(self.checks),
                "last_check": self.checks[-1] if self.checks else None,
                "vindicated_ts": self.vindicated_ts,
                "expired_ts": self.expired_ts,
                "retired_ts": self.retired_ts, "retire_note": self.retire_note,
                "retire_candidate": self.retire_candidate}


def fold_ledger(rows: list[dict[str, Any]]) -> dict[str, DoctrineItem]:
    """Event-sourced state: registrations create, checks score, retirement
    closes. First terminal check verdict freezes the status; VOID rows
    never leave VOID no matter what later rows claim (registration-time
    status is itself law); orphan rows (no registration) are ignored."""
    items: dict[str, DoctrineItem] = {}
    for row in rows:
        rtype = row.get("type")
        if rtype == "registration":
            item = DoctrineItem(
                id=str(row.get("id") or ""), kind=str(row.get("kind") or ""),
                claim=str(row.get("claim") or ""),
                source_verdict=str(row.get("source_verdict") or ""),
                predicted_outcome=row.get("predicted_outcome") or {},
                deadline=str(row.get("deadline") or ""),
                registered_ts=str(row.get("registered_ts") or ""))
            if row.get("status") == "VOID":
                item.status = "VOID"
                item.void_reasons = list(row.get("void_reasons") or [])
            items[item.id] = item
        elif rtype == "check":
            item = items.get(str(row.get("id") or ""))
            if item is None or item.status != "PENDING":
                continue
            item.checks.append(row)
            verdict = row.get("verdict")
            if verdict == "VINDICATED":
                item.status, item.vindicated_ts = "VINDICATED", str(row.get("ts") or "")
            elif verdict == "EXPIRED":
                item.status, item.expired_ts = "EXPIRED", str(row.get("ts") or "")
        elif rtype == "retirement":
            item = items.get(str(row.get("id") or ""))
            if item is not None:
                item.status = "RETIRED"
                item.retired_ts = str(row.get("ts") or "")
                item.retire_note = str(row.get("note") or "")
    return items


# ------------------------------------------------------------ check pass ----

def run_check(items: dict[str, DoctrineItem], ledger_path: Path,
              paths: InstrumentPaths, today: Optional[date] = None
              ) -> tuple[list[DoctrineItem], int]:
    """Score every PENDING item against its instrument. Appends one check
    row per measured item (PENDING verdicts too: each row is evidence the
    pass ran and what the instrument said, in full, under instrument_saw).
    Terminal and VOID items are never touched. Returns (items in ledger
    order, exit_code)."""
    today = today or utc_today()
    exit_code = EXIT_OK
    for item in items.values():
        if item.status == "EXPIRED":
            exit_code = EXIT_ATTENTION  # standing flag until retired
        if item.status != "PENDING":
            continue
        pred = item.predicted_outcome
        try:
            measured_doc = MEASURERS[pred["instrument"]](
                pred.get("selector") or {}, paths)
        except InstrumentError as exc:
            raise InstrumentError(f"{item.id}: {exc}") from exc
        if measured_doc is None or measured_doc.get(pred["metric"]) is None:
            measured, satisfies = None, False
        else:
            measured = measured_doc[pred["metric"]]
            satisfies = compare(measured, pred["op"], pred["value"])
        deadline = parse_deadline(item.deadline)
        # Vindication must land INSIDE the term: the pre-registered claim
        # is "this holds by <deadline>", so a truth first measured after
        # the deadline is a late arrival, not a vindication (the same
        # discipline a prediction market resolves by). An estate that
        # never ran the check in time owns the EXPIRED verdict.
        if satisfies and (deadline is None or today <= deadline):
            verdict = "VINDICATED"
        elif deadline is not None and today > deadline:
            verdict = "EXPIRED"
        else:
            verdict = "PENDING"
        ts = utc_now_iso()
        append_row(ledger_path, {
            "type": "check", "id": item.id, "ts": ts, "measured": measured,
            "satisfies": satisfies, "verdict": verdict,
            "instrument_saw": measured_doc})
        item.checks.append({"type": "check", "id": item.id, "ts": ts,
                            "measured": measured, "satisfies": satisfies,
                            "verdict": verdict})
        if verdict == "VINDICATED":
            item.status, item.vindicated_ts = "VINDICATED", ts
        elif verdict == "EXPIRED":
            item.status, item.expired_ts = "EXPIRED", ts
            exit_code = EXIT_ATTENTION
    return list(items.values()), exit_code


# ------------------------------------------------------------- scorecard ---

_STATUS_ORDER = {"EXPIRED": 0, "VINDICATED": 1, "PENDING": 2,
                 "RETIRED": 3, "VOID": 4}


def render_scorecard(items: list[DoctrineItem], generated_ts: str,
                     ledger_path: Path) -> str:
    lines = [f"DOCTRINE SCORECARD {generated_ts} "
             f"(ledger {ledger_path}, {len(items)} item(s))"]
    for item in sorted(items, key=lambda i: (_STATUS_ORDER.get(i.status, 9), i.id)):
        pred = item.predicted_outcome
        if pred:
            sel = " ".join(f"{k}={v}" for k, v in
                           sorted((pred.get("selector") or {}).items()))
            claim = (f"{pred.get('instrument')}.{pred.get('metric')} "
                     f"{pred.get('op')} {pred.get('value')!r}"
                     + (f" [{sel}]" if sel else ""))
        else:
            claim = "(no prediction)"
        last = item.checks[-1] if item.checks else None
        measured = (f"measured {last['measured']!r} ({last['ts']})"
                    if last else "never checked")
        lines.append(f"  {item.id:<24} {item.status:<10} {item.kind:<14} {claim}")
        if item.status == "VINDICATED":
            tail = f"    vindicated {item.vindicated_ts} | {measured}"
        elif item.status == "EXPIRED":
            tail = (f"    deadline {item.deadline} | {measured}"
                    " | RETIRE CANDIDATE (operator gate: retire --id;"
                    " never auto-removed)")
        elif item.status == "VOID":
            tail = "    void at registration: " + "; ".join(item.void_reasons)
        elif item.status == "RETIRED":
            tail = (f"    deadline {item.deadline} | {measured}"
                    f" | retired {item.retired_ts}: {item.retire_note}")
        else:
            tail = f"    deadline {item.deadline} | {measured}"
        lines.append(tail)
    counts = {s: sum(1 for i in items if i.status == s) for s in STATUSES}
    lines.append(f"SUMMARY: VINDICATED {counts['VINDICATED']} | EXPIRED "
                 f"{counts['EXPIRED']} (retire candidates) | PENDING "
                 f"{counts['PENDING']} | VOID {counts['VOID']} | RETIRED "
                 f"{counts['RETIRED']}")
    return "\n".join(lines)


def scorecard_document(items: list[DoctrineItem], ledger_path: Path
                       ) -> dict[str, Any]:
    return {
        "schema": "doctrine_scorecard.v1",
        "generated_ts": utc_now_iso(),
        "ledger": str(ledger_path),
        "summary": {s: sum(1 for i in items if i.status == s)
                    for s in STATUSES},
        "retire_candidates": [i.id for i in items if i.retire_candidate],
        "items": [i.as_dict() for i in
                  sorted(items, key=lambda i: (i.status, i.id))],
    }
