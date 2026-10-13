#!/usr/bin/env python3
"""K.17 pilot skeleton — minimal honest effect-intent pilot (contract v0 draft).

Spec:
  memory/vault/astra_v2_companions/effect-broker-contract-v0.md
  memory/vault/astra_v2_companions/effect-intent-v0.schema.json

Scope (the B.14 "minimum honest pilot" shape, on a disposable fixture only):
  1. An immutable intent record is persisted BEFORE any dispatch (B.06/B.08).
     Write-once atomic file. operation_id = "op_" + sha256(exact canonical
     intent bytes) (B.07); the intent bytes are stored verbatim.
  2. Dispatch = one deterministic local effect: one `ledger_insert` line in
     the fixture ledger file, carrying the operation id.
  3. `run --crash-after-intent` records the dispatch attempt, then skips the
     effect — simulated death-after-intent (exit code 3).
  4. Replay = rerun `run` against the same state dir with the same intent:
     a recorded intent with no recorded effect is re-issued exactly once, and
     the postcondition (EXACTLY one ledger effect for the op id) is verified
     by readback before reporting APPLIED.
  5. A second replay finds the committed effect and returns the persisted
     result without executing again (B.09 dedup; idempotent).
  6. `run --hold` models Chair 3's burial case: the intent is persisted, the
     dispatch is journaled, but the effect CANNOT be verified (unverifiable
     destination) -> effect knowledge is UNKNOWN, never APPLIED. A hold row
     {op_id, state: UNKNOWN, opened_ts, ttl_hours, owner: unassigned} lands
     in holds.jsonl so the UNKNOWN survives any restart.
  7. `holds` report lists open holds with age in hours. Any hold older than
     its TTL prints LOUD: "HOLD EXPIRED: <op_id> age <h>h — needs owner or
     NOT_APPLIED_FINAL". Aging is the reaper Chair 3 demanded: nothing is
     silently buried; every stale UNKNOWN demands an owner or a terminal
     NOT_APPLIED_FINAL decision (B.13). When a held op's effect later
     verifies (replay), the hold is closed with resolved_as=APPLIED.

Registered durability profile: "process_crash" only (B.11). Bytes are flushed
via os.fsync before an effect is reported; NO power-loss durability claim.
Timestamps and transport metadata are excluded from the canonical intent
encoding that the digest binds (B.07).

NOT covered (named as next, not silently absent): automatic reaping (the
`holds` report only FLAGS expired holds — resolving them to NOT_APPLIED_FINAL
or assigning an owner is still a human act), owner-epoch receiver fencing
(B.10), cross-process admission-key uniqueness, and single-authoritative-
transaction commit (B.09 proposes SQLite; this pilot is file-native on
purpose).

Stdlib only. Exit codes: 0 ok, 1 error, 2 OPERATION_ID_CONFLICT,
3 simulated death, 4 invariant violation, 5 hold open / hold expired.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

INTENT_SCHEMA = "effect_intent.v0"
PRINCIPAL_ID = "k17-pilot-worker"
DESTINATION_RESOURCE = "fixture_ledger.jsonl"
DESTINATION_ID = "k17.fixture.ledger"
ADAPTER_ID = "k17_pilot.fixture_ledger.v0"
CANONICAL_ENCODING_ID = "k17.canonical_json.v1"
DURABILITY_PROFILE = "process_crash"  # B.11: registered separately from power-loss

INTENTS_DIRNAME = "intents"
ATTEMPTS_FILENAME = "attempts.jsonl"
HOLDS_FILENAME = "holds.jsonl"
DEFAULT_HOLD_TTL_HOURS = 24.0

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_CONFLICT = 2
EXIT_SIMULATED_DEATH = 3
EXIT_INVARIANT = 4
EXIT_HOLD = 5  # hold open (run --hold) or expired hold present (holds)


class OperationIdConflict(Exception):
    """Same operation id, different canonical intent bytes (B.07)."""


class LedgerCorrupt(Exception):
    """A fixture ledger line does not parse — refuse to reason over it."""


def utc_now() -> str:
    """Box-local clock, UTC. Clock source for pilot evidence (B.14)."""
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


# ---------------------------------------------------------------- intent ----

def canonical_intent(payload: str, run_id: str, decision_id: str) -> dict:
    """Canonical intent object.

    Deliberately contains NO timestamp, retry count, epoch, or transport
    metadata: the digest binds exactly the logical operation (B.07). Effect
    ordinal and intent revision are pinned at 0 — one decision, one effect,
    no supersession in this pilot.
    """
    return {
        "schema": INTENT_SCHEMA,
        "adapter": {
            "adapter_id": ADAPTER_ID,
            "canonical_encoding_id": CANONICAL_ENCODING_ID,
        },
        "admission_key": {
            "decision_id": decision_id,
            "effect_ordinal": 0,
            "intent_revision": 0,
        },
        "destination": {
            "destination_id": DESTINATION_ID,
            "resource_id": DESTINATION_RESOURCE,
        },
        "durability_profile": DURABILITY_PROFILE,
        "effect": "ledger_insert",
        "payload": {"media_type": "text/plain", "content": payload},
        "principal_id": PRINCIPAL_ID,
        "run_id": run_id,
    }


def canonical_bytes(obj: dict) -> bytes:
    """Sealed canonical encoding: sorted keys, no whitespace, UTF-8 (B.07)."""
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def operation_id_for(intent_bytes: bytes) -> str:
    return "op_" + hashlib.sha256(intent_bytes).hexdigest()


# ------------------------------------------------------------ primitives ----

def _write_atomic(path: Path, data: bytes) -> None:
    """Write-once publish: temp file, flush, fsync, atomic replace.

    Process-crash durability only: after this returns, a same-OS process
    restart observes the bytes. No power-loss claim is made.
    """
    tmp = path.parent / f".{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp"
    try:
        with open(tmp, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def _append_line(path: Path, row: dict) -> None:
    line = json.dumps(row, sort_keys=True) + "\n"
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(line)
        fh.flush()
        os.fsync(fh.fileno())


def intent_path(state_dir: Path, op_id: str) -> Path:
    return state_dir / INTENTS_DIRNAME / f"{op_id}.json"


def persist_intent(state_dir: Path, op_id: str, intent_bytes: bytes) -> str:
    """Persist the immutable intent BEFORE dispatch. Returns created|reused.

    Write-once: if a record already exists for this op id, the stored intent
    bytes must match exactly, else OPERATION_ID_CONFLICT without dispatch
    (B.07 same-ID/different-payload binding).
    """
    path = intent_path(state_dir, op_id)
    incoming = intent_bytes.decode("utf-8")
    if path.exists():
        stored = json.loads(path.read_text(encoding="utf-8"))
        if stored["intent"] != incoming:
            raise OperationIdConflict(
                f"operation {op_id} already bound to different intent bytes"
            )
        return "reused"
    record = {
        "schema": INTENT_SCHEMA,
        "operation_id": op_id,
        "intent_sha256": hashlib.sha256(intent_bytes).hexdigest(),
        "intent": incoming,  # exact canonical bytes, stored verbatim
        # envelope metadata below is NOT part of the digest (B.07)
        "recorded_at": utc_now(),
        "durability_profile": DURABILITY_PROFILE,
    }
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / INTENTS_DIRNAME).mkdir(parents=True, exist_ok=True)
    _write_atomic(path, (json.dumps(record, sort_keys=True, indent=2) + "\n").encode("utf-8"))
    return "created"


def load_intent(state_dir: Path, op_id: str) -> dict:
    return json.loads(intent_path(state_dir, op_id).read_text(encoding="utf-8"))


def record_attempt(state_dir: Path, op_id: str, mode: str, outcome: str) -> str:
    """Append-only attempt journal. Attempt ids are independently random and
    never replace the operation id (B.07)."""
    attempt_id = "att_" + uuid.uuid4().hex
    state_dir.mkdir(parents=True, exist_ok=True)
    _append_line(
        state_dir / ATTEMPTS_FILENAME,
        {
            "event": "attempt",
            "operation_id": op_id,
            "attempt_id": attempt_id,
            "mode": mode,
            "outcome": outcome,
            "recorded_at": utc_now(),
        },
    )
    return attempt_id


def read_attempts(state_dir: Path, op_id: str | None = None) -> list[dict]:
    path = state_dir / ATTEMPTS_FILENAME
    if not path.exists():
        return []
    rows = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise LedgerCorrupt(f"{ATTEMPTS_FILENAME}:{n}: {exc}") from exc
        if op_id is None or row.get("operation_id") == op_id:
            rows.append(row)
    return rows


# ------------------------------------------------------------------ holds ----

def read_holds(state_dir: Path) -> list[dict]:
    """Append-only hold journal. Every row is evidence; nothing is deleted."""
    path = state_dir / HOLDS_FILENAME
    if not path.exists():
        return []
    rows = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise LedgerCorrupt(f"{HOLDS_FILENAME}:{n}: {exc}") from exc
    return rows


def open_holds(state_dir: Path) -> dict[str, dict]:
    """op_id -> its OPEN hold row (latest event per op must be hold_open)."""
    latest: dict[str, dict | None] = {}
    for row in read_holds(state_dir):
        op_id = row.get("op_id")
        if row.get("event") == "hold_open":
            latest[op_id] = row
        elif row.get("event") == "hold_close":
            latest[op_id] = None
    return {op_id: row for op_id, row in latest.items() if row is not None}


def open_hold(state_dir: Path, op_id: str, ttl_hours: float) -> str:
    """Record an open hold for an unverifiable effect. Idempotent per op id:
    a hold already open is reused, never duplicated (one op, one hold)."""
    if op_id in open_holds(state_dir):
        return "reused"
    state_dir.mkdir(parents=True, exist_ok=True)
    _append_line(
        state_dir / HOLDS_FILENAME,
        {
            "event": "hold_open",
            "op_id": op_id,
            "state": "UNKNOWN",
            "opened_ts": utc_now(),
            "ttl_hours": ttl_hours,
            "owner": "unassigned",
        },
    )
    return "opened"


def close_open_holds(state_dir: Path, op_id: str, resolved_as: str) -> bool:
    """Close the hold when the effect becomes verifiable (verified APPLIED)."""
    if op_id not in open_holds(state_dir):
        return False
    _append_line(
        state_dir / HOLDS_FILENAME,
        {
            "event": "hold_close",
            "op_id": op_id,
            "resolved_as": resolved_as,
            "closed_ts": utc_now(),
        },
    )
    return True


def _parse_clock(value: str | None) -> datetime:
    """Box-local UTC clock, or an explicit --now override (deterministic
    aging tests; the clock source is disclosed, not trusted — B.14)."""
    if value is None:
        return datetime.now(timezone.utc)
    dt = datetime.fromisoformat(value)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


# ----------------------------------------------------- effect (dispatch) ----

def scan_effects(state_dir: Path, op_id: str | None = None) -> list[dict]:
    """Independent destination oracle: read the fixture ledger back."""
    path = state_dir / DESTINATION_RESOURCE
    if not path.exists():
        return []
    effects = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise LedgerCorrupt(f"{DESTINATION_RESOURCE}:{n}: {exc}") from exc
        if op_id is None or row.get("operation_id") == op_id:
            effects.append(row)
    return effects


def commit_effect(state_dir: Path, op_id: str, attempt_id: str, payload: str) -> None:
    """The one deterministic local effect: append one line carrying the op id."""
    _append_line(
        state_dir / DESTINATION_RESOURCE,
        {
            "effect": "ledger_insert",
            "operation_id": op_id,
            "attempt_id": attempt_id,
            "payload_sha256": hashlib.sha256(canonical_bytes({"content": payload})).hexdigest(),
            "committed_at": utc_now(),
        },
    )


# ------------------------------------------------------------------ modes ----

def _emit(payload: dict, code: int) -> int:
    print(json.dumps(payload, indent=2))
    return code


def cmd_run(args) -> int:
    state_dir = Path(args.state_dir)
    if args.hold:
        mode = "hold"
    elif args.crash_after_intent:
        mode = "crash_after_intent"
    else:
        mode = "normal"

    intent_obj = canonical_intent(args.payload, args.run_id, args.decision_id)
    intent_bytes = canonical_bytes(intent_obj)
    op_id = args.operation_id or operation_id_for(intent_bytes)

    # (1) immutable intent BEFORE dispatch (B.06/B.08); conflict -> no dispatch.
    try:
        origin = persist_intent(state_dir, op_id, intent_bytes)
    except OperationIdConflict as exc:
        return _emit(
            {
                "status": "OPERATION_ID_CONFLICT",
                "operation_id": op_id,
                "error": str(exc),
                "dispatched": False,
            },
            EXIT_CONFLICT,
        )

    effects_before = scan_effects(state_dir, op_id)
    if effects_before:
        # (5) B.09 dedup: repeated op id returns the persisted result and
        # does NOT execute again. A previously UNKNOWN effect just became
        # verifiable -> close any open hold with the verified knowledge.
        close_open_holds(state_dir, op_id, "APPLIED")
        attempt_id = record_attempt(state_dir, op_id, mode, "dedup_hit")
        return _emit(
            {
                "status": "DEDUP_APPLIED",
                "operation_id": op_id,
                "intent": origin,
                "attempt_id": attempt_id,
                "executed": False,
                "effect_count": len(effects_before),
            },
            EXIT_OK,
        )

    # (3) dispatch is journaled before the effect, so a crash leaves a
    # detectable intent-without-effect state.
    attempt_id = record_attempt(state_dir, op_id, mode, "dispatched")

    if mode == "hold":
        # Chair 3's case: dispatched, but the effect CANNOT be verified.
        # Effect knowledge is UNKNOWN — never APPLIED, never buried. The
        # hold row is the honest state: owned by no one yet, on a clock.
        hold_action = open_hold(state_dir, op_id, args.ttl_hours)
        return _emit(
            {
                "status": "HOLD_OPEN",
                "operation_id": op_id,
                "attempt_id": attempt_id,
                "hold": {
                    "state": "UNKNOWN",
                    "ttl_hours": args.ttl_hours,
                    "owner": "unassigned",
                    "action": hold_action,
                },
                "executed": False,
                "effect_count": 0,
            },
            EXIT_HOLD,
        )

    if mode == "crash_after_intent":
        # simulated death AFTER intent + dispatch record, BEFORE the effect
        return _emit(
            {
                "status": "SIMULATED_DEATH_AFTER_INTENT",
                "operation_id": op_id,
                "attempt_id": attempt_id,
                "executed": False,
                "effect_count": 0,
            },
            EXIT_SIMULATED_DEATH,
        )

    # (2) the effect, then a readback postcondition check. APPLIED is reserved
    # for a verified postcondition, not mere admission (B.06).
    commit_effect(state_dir, op_id, attempt_id, args.payload)
    effects_after = scan_effects(state_dir, op_id)
    if len(effects_after) != 1:
        return _emit(
            {
                "status": "EFFECT_ANOMALY",
                "operation_id": op_id,
                "attempt_id": attempt_id,
                "effect_count": len(effects_after),
            },
            EXIT_INVARIANT,
        )
    # verified postcondition -> any open hold for this op is resolved.
    close_open_holds(state_dir, op_id, "APPLIED")
    return _emit(
        {
            "status": "APPLIED",
            "operation_id": op_id,
            "intent": origin,
            "attempt_id": attempt_id,
            "executed": True,
            "effect_count": 1,
        },
        EXIT_OK,
    )


def cmd_verify(args) -> int:
    """Independent read of intents, attempts, and the destination oracle."""
    state_dir = Path(args.state_dir)
    intents_dir = state_dir / INTENTS_DIRNAME
    intent_ids = sorted(p.stem for p in intents_dir.glob("*.json")) if intents_dir.exists() else []

    all_effects = scan_effects(state_dir)
    attempts = read_attempts(state_dir)

    operations = []
    violations = []

    # every committed effect must reference a stored intent
    intent_id_set = set(intent_ids)
    for row in all_effects:
        if row.get("operation_id") not in intent_id_set:
            violations.append(f"effect without stored intent: {row.get('operation_id')}")

    for op_id in intent_ids:
        effects = [e for e in all_effects if e.get("operation_id") == op_id]
        n_attempts = sum(1 for a in attempts if a.get("operation_id") == op_id)
        if len(effects) > 1:
            violations.append(
                f"operation {op_id} has {len(effects)} committed effects (dedup broken)"
            )
            knowledge = "VIOLATION"
        elif len(effects) == 1:
            knowledge = "APPLIED"
        else:
            # intent admitted, effect not yet (crashed and unreplayed).
            # NOT UNKNOWN semantics: no reconciliation protocol is modeled here.
            knowledge = "PENDING"
        operations.append(
            {
                "operation_id": op_id,
                "attempts": n_attempts,
                "effects": len(effects),
                "knowledge": knowledge,
            }
        )

    status = "VIOLATION" if violations else "OK"
    open_hold_ids = set(open_holds(state_dir))
    report = {
        "status": status,
        "violations": violations,
        "clock_source": "box-local datetime.now(timezone.utc) (B.14 disclosure)",
        "durability_profile": DURABILITY_PROFILE,
        "totals": {
            "intents": len(intent_ids),
            "attempts": len(attempts),
            "effects": len(all_effects),
            "holds_open": len(open_hold_ids),
        },
        "operations": [
            {**op, "hold_open": op["operation_id"] in open_hold_ids}
            for op in operations
        ],
    }
    if violations:
        return _emit(report, EXIT_INVARIANT)
    return _emit(report, EXIT_OK)


def cmd_holds(args) -> int:
    """Hold-state visibility: list open holds with age; flag expired LOUD.

    Aging is the reaper (Chair 3): a hold past its TTL is not silent state,
    it is a demand — assign an owner or resolve to NOT_APPLIED_FINAL (B.13).
    """
    state_dir = Path(args.state_dir)
    now = _parse_clock(args.now)

    entries = []
    loud = []
    for op_id, row in sorted(open_holds(state_dir).items()):
        opened = datetime.fromisoformat(row["opened_ts"])
        if now.tzinfo is None and opened.tzinfo is not None:
            opened = opened.replace(tzinfo=None)
        age_hours = (now - opened).total_seconds() / 3600.0
        ttl_hours = float(row.get("ttl_hours", DEFAULT_HOLD_TTL_HOURS))
        expired = age_hours > ttl_hours
        entries.append(
            {
                "op_id": op_id,
                "state": row.get("state"),
                "opened_ts": row["opened_ts"],
                "age_hours": round(age_hours, 3),
                "ttl_hours": ttl_hours,
                "owner": row.get("owner"),
                "expired": expired,
            }
        )
        if expired:
            loud.append(
                f"HOLD EXPIRED: {op_id} age {age_hours:.1f}h "
                f"— needs owner or NOT_APPLIED_FINAL"
            )

    for line in loud:
        print(line)
    return _emit(
        {
            "status": "HOLD_EXPIRED" if loud else "OK",
            "holds": entries,
            "totals": {"open": len(entries), "expired": len(loud)},
        },
        EXIT_HOLD if loud else EXIT_OK,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="k17_pilot",
        description="K.17 minimal honest effect-intent pilot (contract v0 draft).",
    )
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--state-dir",
        default="state/k17_pilot_fixture",
        help="disposable state dir holding intents/, attempts.jsonl, fixture ledger",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", parents=[common], help="admit + dispatch one operation")
    group = run_p.add_mutually_exclusive_group(required=True)
    group.add_argument("--normal", action="store_true", help="intent -> attempt -> effect")
    group.add_argument(
        "--crash-after-intent",
        dest="crash_after_intent",
        action="store_true",
        help="intent -> attempt, then simulated death before the effect",
    )
    group.add_argument(
        "--hold",
        action="store_true",
        help="intent -> dispatch to an UNVERIFIABLE destination: effect "
        "knowledge UNKNOWN, hold row opened in holds.jsonl (exit 5)",
    )
    run_p.add_argument(
        "--ttl-hours",
        type=float,
        default=DEFAULT_HOLD_TTL_HOURS,
        help="hold TTL in hours (default 24)",
    )
    run_p.add_argument("--payload", default="k17 pilot effect line")
    run_p.add_argument("--run-id", default="k17-pilot-run-0")
    run_p.add_argument("--decision-id", default="decision-0")
    run_p.add_argument(
        "--operation-id",
        default=None,
        help="force the operation id (caller-assigned identity; enables the "
        "same-ID/different-payload OPERATION_ID_CONFLICT calibration)",
    )

    sub.add_parser("verify", parents=[common], help="independent destination-oracle read")

    holds_p = sub.add_parser(
        "holds", parents=[common], help="open holds with age; expired holds print LOUD"
    )
    holds_p.add_argument(
        "--now",
        default=None,
        help="ISO timestamp override for the clock (deterministic aging checks)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == "run":
            return cmd_run(args)
        if args.cmd == "verify":
            return cmd_verify(args)
        if args.cmd == "holds":
            return cmd_holds(args)
    except LedgerCorrupt as exc:
        return _emit({"status": "LEDGER_CORRUPT", "error": str(exc)}, EXIT_INVARIANT)
    return _emit({"status": "ERROR", "error": f"unknown command {args.cmd!r}"}, EXIT_ERROR)


if __name__ == "__main__":
    sys.exit(main())
