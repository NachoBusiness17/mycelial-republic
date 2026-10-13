"""protocol_table: the verbs-as-data layer behind server/protocol (2026-09-29).

Mickey17 return 17 named the defect: server/ gates verbs AS CODE (protocol.py
hardcodes VERBS, world.py validates with if/elif, dispatch is string equality)
while the stolen law sits two directories away: wow_bones R01 "legal() as a
frozen hashable table" and Dispatch already proving gate-before-verb over any
compiled table. This module is that law landed on OUR wire.

THE TABLE (JSON-serializable, frozen at compile):
    rows     : one {verb, required_state, handler_name, reject_code} per verb
    enums    : session_states (ordered ranks), reject_codes, transport_reject_codes
    digest   : sha256 over the canonical JSON bytes of the whole document

THE DIGEST (the contract version):
    protocol_digest = sha256(canonical_json({schema, session_states,
    reject_codes, transport_reject_codes, rows})) where canonical_json is
    sort_keys=True, separators=(",",":"), ensure_ascii=False, utf-8: the same
    canonicalization law as world.row_sha and wow_bones.bones_digest. The
    digest excludes itself, so it is a pure function of the table bytes.
    Any edit to any row, state, or code moves it. Sessions bind to it as a
    hashable contract version: you are not the first Mickey, the digest is.

THE STATES (the NOT_YOUR_TURN machinery):
    CONNECTED  TCP accepted, no valid sid (pre-hello)
    AUTHED     hello accepted, sid registered (the only state v0 grants)
    TURN_HELD  reserved for v1 turn modes; v0 never grants it
    A verb passes the gate when rank(session_state) >= rank(required_state).
    Every v0 row requires AUTHED and rejects with UNKNOWN_SID (an unauthed
    ask arrives with a sid the world never issued: exactly what the wire
    already says). NOT_YOUR_TURN is live machinery, not vocabulary on a
    shelf: compile a row with required_state TURN_HELD and the gate emits
    it. The default v0 table has no such row, so v0 still never emits it.

DISPATCH DECISION (adapt vs reimplement, justified):
    Reimplemented minimal in the wow_bones.Dispatch SHAPE, not by importing
    it. wow_bones.Dispatch speaks the WoW refusal vocabulary
    (UNKNOWN_OPCODE / STATUS_MISMATCH / STATUS_NEVER / STATUS_UNHANDLED),
    has no per-row reject_code column, and eats the bones.json fixture
    envelope ({tables:{client_opcodes}, enums:{session_status}}): bolting
    our typed rejects onto it needs a translation shim thicker than the
    kernel, and it would couple the wire layer to the mag fixture
    extractor. What IS kept verbatim is the call contract, pinned by a
    shape-equivalence test against wow_bones.Dispatch itself:
    dispatch(verb, state) -> {ok, reason, handler_ran} with the ordering
    law (gate before verb, handler provably never fired on refusal) and
    the calls log.

THE MOTION DIALECT (X9 2026-09-30, receipt watch/inbox/hydrology/X9_MOTION.md):
    Rows may declare an args payload contract: "args": {name: spec} where
    spec is "u8" (an int 0..255 — bools ARE ints in Python and True is
    rejected: a bool is a verdict, not an intensity; every violation of the
    u8 law, type or range, rejects BAD_INTENSITY) or "target" (a non-empty
    node name the caller knows, rejects UNKNOWN_TARGET). The compiled
    contract REQUIRES those codes in reject_codes before a row may declare
    the spec, and BAD_ARGS whenever any row declares args at all (the
    shape law: exact key set, dict only, and a schema-less verb given a
    payload is BAD_ARGS too). ProtocolDispatch.ask(verb, state, args,
    targets) extends the ordering law: verb existence, then the state gate,
    then the payload law, and only then the handler; every refusal is
    typed and handler_ran is provably False. The motion contract
    MOTION_TABLE compiles DEFAULT plus idle/flee/pursue/carry/dance rows
    ({intensity_q8: u8, dir: target}, handlers rig_*): the flock policy
    (roblox_to_godot/systems/fish_brain.gd decide()) emits these rows and
    the rig applies them (X9_MOTION integration note). DEFAULT stays the
    bound v0 wire, byte-identical — a spec that never declares args
    compiles to the same digest as before, so the schema string stays
    protocol_table.v1; MOTION_DIGEST is a NEW contract version, not an
    edit of the old one.

THE ANTI-CHEAT CONTRACT (LW7 2026-09-30, S20's design; receipt
    watch/inbox/last_mile_20260930/LW7_ANTICHEAT.md):
    ANTICHEAT_TABLE compiles the DEFAULT rows plus two receipt-level
    reject codes, RATE_CAP and STALE_NONCE. They ride the VOCABULARY, not
    per-verb rows: a second action in a tick is illegal whichever verb it
    carries, and a replayed id is stale on every verb alike, so no row may
    own these laws. ReceiptGate is the executable law (its docstring
    states the two laws verbatim); the ENFORCEMENT POINT is
    server/server.py at the action branch, which orders nonce law ->
    world validation -> rate cap -> stage, so a RATE_CAP or STALE_NONCE
    reject lands at receipt and never stages. Disputed tags route through
    the mag/gwap_payload agreement engine at the same call site (stub: the
    cop report is owed, so a fresh dispute scores 0.0 and verdicts
    DISPUTE — the row the judge queue consumes). DEFAULT stays the bound
    v0 wire, byte-identical; ANTICHEAT_DIGEST is a NEW contract version,
    the X9/LW6 law again.

Run:
    .venv/Scripts/python.exe -m server.protocol_table   # print the contract
Tests: tests/test_protocol_table.py, tests/test_motion_rows.py, tests/test_chat.py, tests/test_anticheat.py, tests/test_auth_srp6.py

Schema: protocol_table.v1 . deterministic + $0 . compile is pure, no writes
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import sys
from pathlib import Path
from types import MappingProxyType
from typing import Any, Container

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCHEMA = "protocol_table.v1"

# The document the digest is taken over. Row order is semantic (it fixes the
# VERBS tuple order), so canonical JSON sorts keys but never reorders rows.
DEFAULT_SPEC: dict[str, Any] = {
    "schema": SCHEMA,
    "session_states": ["CONNECTED", "AUTHED", "TURN_HELD"],
    "reject_codes": [
        "UNKNOWN_SID",
        "NOT_YOUR_TURN",
        "UNKNOWN_VERB",
        "UNKNOWN_TARGET",
        "DRY_POOL",
    ],
    "transport_reject_codes": ["BAD_AUTH", "BAD_JSON", "UNKNOWN_OP"],
    "rows": [
        {"verb": "boil", "required_state": "AUTHED",
         "handler_name": "world_boil", "reject_code": "UNKNOWN_SID"},
        {"verb": "valve", "required_state": "AUTHED",
         "handler_name": "world_valve", "reject_code": "UNKNOWN_SID"},
        {"verb": "join", "required_state": "AUTHED",
         "handler_name": "world_join", "reject_code": "UNKNOWN_SID"},
        {"verb": "tag", "required_state": "AUTHED",
         "handler_name": "world_tag", "reject_code": "UNKNOWN_SID"},
    ],
}

# handler_name names the apply-step owner in MountainWorld._apply
# (server/world.py): the boil/valve/join/tag branches. A later lane binds
# these to methods by name; the table only pins the binding point.

_ROW_KEYS = frozenset({"verb", "required_state", "handler_name", "reject_code"})

# X9 2026-09-30: an args-bearing row may also carry "args", a payload law
# {name: spec}. Each spec names its typed reject code; compile refuses a
# row whose spec's code is missing from the spec's own reject_codes (the
# vocabulary is closed — no runtime code can leak outside the contract).
_ARG_GRAMMAR: dict[str, str] = {"u8": "BAD_INTENSITY", "target": "UNKNOWN_TARGET"}


class ProtocolSpecError(ValueError):
    """Typed, fail-closed refusal to compile a malformed table spec."""


def canonical_json(doc: dict[str, Any]) -> str:
    """The house canonical form (world.row_sha / wow_bones digest law)."""
    return json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclasses.dataclass(frozen=True)
class ProtocolRow:
    """One verb as data. Frozen: assignment raises, and rows live in a tuple.

    X9 2026-09-30: args is the optional payload contract — a sorted tuple of
    (name, spec) pairs from _ARG_GRAMMAR; () means the verb takes no args."""
    verb: str
    required_state: str
    handler_name: str
    reject_code: str
    args: tuple[tuple[str, str], ...] = ()

    def to_dict(self) -> dict[str, str]:
        # Hand-built, NOT dataclasses.asdict: the default table's document
        # must stay byte-identical (an always-present empty-args key would
        # move PROTOCOL_DIGEST and break the byte-identical v0 pin), so
        # "args" appears only when the row declares one.
        d = {"verb": self.verb, "required_state": self.required_state,
             "handler_name": self.handler_name, "reject_code": self.reject_code}
        if self.args:
            d["args"] = {name: spec for name, spec in self.args}
        return d


class ProtocolTable:
    """The frozen compiled contract. Mutation of any view it hands out is
    either refused (frozen dataclass, tuple, MappingProxyType) or isolated
    (to_document returns a deep copy)."""

    __slots__ = ("_rows", "_verbs", "_states", "_reject", "_transport",
                 "_digest", "_document")

    def __init__(self, spec: dict[str, Any]):
        rows, states, reject, transport = _validate_spec(spec)
        self._rows: tuple[ProtocolRow, ...] = tuple(rows)
        self._verbs: tuple[str, ...] = tuple(r.verb for r in self._rows)
        self._states: dict[str, int] = states
        self._reject: tuple[str, ...] = reject
        self._transport: tuple[str, ...] = transport
        self._document = {
            "schema": spec["schema"],
            "session_states": list(states),
            "reject_codes": list(reject),
            "transport_reject_codes": list(transport),
            "rows": [r.to_dict() for r in self._rows],
        }
        self._digest = hashlib.sha256(
            canonical_json(self._document).encode("utf-8")
        ).hexdigest()

    # ------------------------------------------------------------ views ----
    @property
    def schema(self) -> str:
        return self._document["schema"]

    @property
    def rows(self) -> tuple[ProtocolRow, ...]:
        return self._rows

    @property
    def verbs(self) -> tuple[str, ...]:
        return self._verbs

    @property
    def session_states(self) -> MappingProxyType[str, int]:
        return MappingProxyType(self._states)

    @property
    def reject_codes(self) -> tuple[str, ...]:
        return self._reject

    @property
    def transport_reject_codes(self) -> tuple[str, ...]:
        return self._transport

    @property
    def digest(self) -> str:
        return self._digest

    def row(self, verb: str) -> ProtocolRow | None:
        for r in self._rows:
            if r.verb == verb:
                return r
        return None

    def state_rank(self, state: str) -> int | None:
        return self._states.get(state)

    def to_document(self) -> dict[str, Any]:
        """A fresh deep copy, JSON-serializable; mutating it cannot touch us."""
        return json.loads(canonical_json(self._document))

    def __repr__(self) -> str:  # pragma: no cover - convenience only
        return (f"ProtocolTable(schema={self.schema!r}, verbs={self.verbs!r}, "
                f"digest={self._digest[:12]}...)")


def _validate_spec(
    spec: dict[str, Any],
) -> tuple[list[ProtocolRow], dict[str, int], tuple[str, ...], tuple[str, ...]]:
    """Fail closed: every violation is a typed ProtocolSpecError, never a
    half-compiled table."""
    if not isinstance(spec, dict):
        raise ProtocolSpecError("spec must be a dict")
    if spec.get("schema") != SCHEMA:
        raise ProtocolSpecError(f"spec schema must be {SCHEMA!r}")

    raw_states = spec.get("session_states")
    if (not isinstance(raw_states, list) or not raw_states
            or not all(isinstance(s, str) and s for s in raw_states)):
        raise ProtocolSpecError("session_states must be a non-empty list of names")
    if len(set(raw_states)) != len(raw_states):
        raise ProtocolSpecError("session_states must be unique")
    states = {s: i for i, s in enumerate(raw_states)}

    reject = _vocab(spec.get("reject_codes"), "reject_codes")
    transport = _vocab(spec.get("transport_reject_codes"), "transport_reject_codes")
    overlap = set(reject) & set(transport)
    if overlap:
        raise ProtocolSpecError(
            f"action and transport vocabularies must be disjoint, shared: {sorted(overlap)}")

    raw_rows = spec.get("rows")
    if not isinstance(raw_rows, list) or not raw_rows:
        raise ProtocolSpecError("rows must be a non-empty list")

    rows: list[ProtocolRow] = []
    seen_verbs: set[str] = set()
    seen_handlers: set[str] = set()
    for i, row in enumerate(raw_rows):
        if not isinstance(row, dict) or not (_ROW_KEYS <= set(row) <= _ROW_KEYS | {"args"}):
            raise ProtocolSpecError(
                f"row {i} must have exactly the keys {sorted(_ROW_KEYS)} "
                f"(args optional, X9)")
        if not isinstance(row["verb"], str) or not row["verb"]:
            raise ProtocolSpecError(f"row {i}: verb must be a non-empty string")
        if row["verb"] in seen_verbs:
            raise ProtocolSpecError(f"row {i}: duplicate verb {row['verb']!r}")
        if row["required_state"] not in states:
            raise ProtocolSpecError(
                f"row {i} ({row['verb']}): required_state "
                f"{row['required_state']!r} not in session_states")
        if row["reject_code"] not in reject:
            raise ProtocolSpecError(
                f"row {i} ({row['verb']}): reject_code {row['reject_code']!r} "
                f"not in reject_codes")
        if not isinstance(row["handler_name"], str) or not row["handler_name"]:
            raise ProtocolSpecError(
                f"row {i} ({row['verb']}): handler_name must be a non-empty string")
        if row["handler_name"] in seen_handlers:
            raise ProtocolSpecError(
                f"row {i}: duplicate handler_name {row['handler_name']!r} "
                f"(one verb, one owner)")
        seen_verbs.add(row["verb"])
        seen_handlers.add(row["handler_name"])
        args: tuple[tuple[str, str], ...] = ()
        if "args" in row:
            raw_args = row["args"]
            if (not isinstance(raw_args, dict) or not raw_args
                    or not all(isinstance(k, str) and k for k in raw_args)):
                raise ProtocolSpecError(
                    f"row {i} ({row['verb']}): args must be a non-empty "
                    f"name->spec dict")
            for name, spec in raw_args.items():
                if spec not in _ARG_GRAMMAR:
                    raise ProtocolSpecError(
                        f"row {i} ({row['verb']}): arg {name!r} spec {spec!r} "
                        f"not in {sorted(_ARG_GRAMMAR)}")
                if _ARG_GRAMMAR[spec] not in reject:
                    raise ProtocolSpecError(
                        f"row {i} ({row['verb']}): arg {name!r} rejects with "
                        f"{_ARG_GRAMMAR[spec]!r} but it is not in reject_codes")
            if "BAD_ARGS" not in reject:
                # ask() rejects every shape violation with BAD_ARGS; a table
                # that declares payloads must own that code up front
                raise ProtocolSpecError(
                    f"row {i} ({row['verb']}): args rows require BAD_ARGS "
                    f"in reject_codes")
            args = tuple(sorted(raw_args.items()))
        rows.append(ProtocolRow(verb=row["verb"],
                                required_state=row["required_state"],
                                handler_name=row["handler_name"],
                                reject_code=row["reject_code"],
                                args=args))
    return rows, states, reject, transport


def _vocab(raw: Any, name: str) -> tuple[str, ...]:
    if (not isinstance(raw, list) or not raw
            or not all(isinstance(c, str) and c for c in raw)):
        raise ProtocolSpecError(f"{name} must be a non-empty list of codes")
    if len(set(raw)) != len(raw):
        raise ProtocolSpecError(f"{name} must be unique")
    return tuple(raw)


def compile_table(spec: dict[str, Any] | None = None) -> ProtocolTable:
    """Pure: same spec in, same table and digest out, every time."""
    return ProtocolTable(DEFAULT_SPEC if spec is None else spec)


# The bound v0 contract: compiled once at import, pinned by its digest.
DEFAULT_TABLE = compile_table()
PROTOCOL_DIGEST: str = DEFAULT_TABLE.digest

# The wire surface, table-backed. server/protocol.py re-exports these so its
# existing API (VERBS, REJECT_CODES, TRANSPORT_REJECT_CODES) keeps its exact
# values and order while the table becomes the source of truth behind them.
VERBS: tuple[str, ...] = DEFAULT_TABLE.verbs
REJECT_CODES: tuple[str, ...] = DEFAULT_TABLE.reject_codes
TRANSPORT_REJECT_CODES: tuple[str, ...] = DEFAULT_TABLE.transport_reject_codes


def _check_args(row: ProtocolRow, args: Any, targets: Container[str]) -> str | None:
    """The payload law for args-bearing rows: exact key set, then each value
    against its spec. Returns the typed reject code, or None when legal.

    u8: an int 0..255 — a bool is rejected explicitly (bool subclasses int,
    and True is a verdict, not an intensity); any type OR range violation
    is BAD_INTENSITY, one code for the whole law.
    target: a non-empty string present in the caller's known targets —
    dir is a node NAME (the board's vocabulary), never a Vector2."""
    if not isinstance(args, dict) or set(args) != {name for name, _ in row.args}:
        return "BAD_ARGS"
    for name, spec in row.args:
        value = args[name]
        if spec == "u8":
            if (isinstance(value, bool) or not isinstance(value, int)
                    or not 0 <= value <= 255):
                return _ARG_GRAMMAR[spec]
        elif spec == "target":
            if not isinstance(value, str) or not value or value not in targets:
                return _ARG_GRAMMAR[spec]
    return None


class ProtocolDispatch:
    """The ORDERING LAW on our wire, executable (wow_bones.Dispatch shape).

    The gate is evaluated on the table BEFORE the verb runs (AzerothCore
    WorldSession.cpp:436, proven executable in mag/wow_bones.py Dispatch).
    A verb asked for in the wrong state is refused with a typed reason and
    the handler provably never fires.
    """

    def __init__(self, table: ProtocolTable | None = None):
        self.table = table if table is not None else DEFAULT_TABLE
        self.calls: list[str] = []

    def verbs(self) -> list[str]:
        return sorted(self.table.verbs)

    def dispatch(self, verb: str, session_state: str) -> dict[str, Any]:
        """Verb existence, then state gate, then (only on pass) the handler.
        Refusals are typed and handler_ran is False on every one of them."""
        row = self.table.row(verb)
        if row is None:
            return {"ok": False, "reason": "UNKNOWN_VERB", "handler_ran": False}
        rank = self.table.state_rank(session_state)
        if rank is None:
            # internal invariant guard (caller passed a state outside the
            # enum); mirrors Dispatch's UNKNOWN_STATUS, never a wire code
            return {"ok": False, "reason": "UNKNOWN_STATE", "handler_ran": False}
        if rank < self.table.session_states[row.required_state]:
            return {"ok": False, "reason": row.reject_code, "handler_ran": False}
        self.calls.append(verb)
        return {
            "ok": True,
            "reason": "DISPATCHED",
            "handler": row.handler_name,
            "required_state": row.required_state,
            "handler_ran": True,
        }

    def validate(self, session_state: str, verb: str) -> tuple[bool, str | None]:
        """World-shape contract ((ok, why) like MountainWorld.validate) so a
        later lane swaps the if/elif ladder for this 1:1."""
        out = self.dispatch(verb, session_state)
        if out["ok"]:
            return True, None
        return False, out["reason"]

    def ask(self, verb: str, session_state: str, args: Any = None,
            targets: Container[str] = ()) -> dict[str, Any]:
        """A verb ask WITH a payload (X9 motion dialect). The ordering law
        holds end to end: verb existence, then the state gate, then the
        payload law, and only then the handler. Refusals are typed at every
        layer and handler_ran is provably False on every one of them — a
        CONNECTED session is refused UNKNOWN_SID before its payload is even
        looked at, and a legal session with an illegal payload never fires."""
        row = self.table.row(verb)
        if row is None:
            return {"ok": False, "reason": "UNKNOWN_VERB", "handler_ran": False}
        rank = self.table.state_rank(session_state)
        if rank is None:
            return {"ok": False, "reason": "UNKNOWN_STATE", "handler_ran": False}
        if rank < self.table.session_states[row.required_state]:
            return {"ok": False, "reason": row.reject_code, "handler_ran": False}
        if row.args:
            bad = _check_args(row, args, targets)
            if bad is not None:
                return {"ok": False, "reason": bad, "handler_ran": False}
        elif args is not None:
            return {"ok": False, "reason": "BAD_ARGS", "handler_ran": False}
        self.calls.append(verb)
        return {"ok": True, "reason": "DISPATCHED", "handler": row.handler_name,
                "required_state": row.required_state,
                "args": dict(args) if isinstance(args, dict) else None,
                "handler_ran": True}


DEFAULT_DISPATCH = ProtocolDispatch(DEFAULT_TABLE)


# ------------------------------------------------------- X9 motion (2026-09-30)
# The motion dialect: the Godot rig's steering vocabulary as table rows —
# idle/flee/pursue/carry/dance, each carrying the payload law
# {intensity_q8: u8 (0..255 urgency), dir: target node name}. This is a
# STRICT SUPERSET contract: the v0 base rows ride along unchanged so the
# rig consumes one table, while DEFAULT (the bound server wire) stays
# byte-identical — the server adopts motion rows in a later lane, when
# world.py owns a rig_* apply-step. handler_name still names the apply-step
# owner; for these rows that owner is the RIG (game.gd's row consumer, per
# the X9_MOTION integration note), not MountainWorld._apply.
MOTION_VERBS: tuple[str, ...] = ("idle", "flee", "pursue", "carry", "dance")

MOTION_SPEC: dict[str, Any] = {
    "schema": SCHEMA,
    "session_states": list(DEFAULT_SPEC["session_states"]),
    "reject_codes": list(DEFAULT_SPEC["reject_codes"]) + ["BAD_ARGS", "BAD_INTENSITY"],
    "transport_reject_codes": list(DEFAULT_SPEC["transport_reject_codes"]),
    "rows": [dict(r) for r in DEFAULT_SPEC["rows"]] + [
        {"verb": verb, "required_state": "AUTHED",
         "handler_name": f"rig_{verb}", "reject_code": "UNKNOWN_SID",
         "args": {"intensity_q8": "u8", "dir": "target"}}
        for verb in MOTION_VERBS
    ],
}

MOTION_TABLE = compile_table(MOTION_SPEC)
MOTION_DIGEST: str = MOTION_TABLE.digest
MOTION_DISPATCH = ProtocolDispatch(MOTION_TABLE)


# ------------------------------------------------------- LW6 chat (2026-09-30)
# The chat dialect (S19's spec, receipt watch/inbox/last_mile_20260930/
# LW6_CHAT.md): say/whisper as table rows, the same X9 law — a NEW contract
# version compiled from the DEFAULT rows, so the bound v0 wire stays
# byte-identical (PROTOCOL_DIGEST does not move; the pinned surface tests
# in tests/test_protocol_table.py are the proof). No args specs here: chat
# text rides the EXISTING action op's `target` string field (zero new ops
# on the wire), so its law lives in world.validate exactly like DRY_POOL —
# the only table-side requirement is that BAD_TEXT be in the closed
# reject vocabulary before any row may reject with it.
#   say     {verb: say, target: <text>}          -> next tick's events,
#              staged and applied like every other verb (determinism law
#              untouched: the tick is still the only mutator)
#   whisper {verb: whisper, target: 'user|text'} -> a direct line to that
#              sid only, OUTSIDE the canonical tick (world.direct outbox,
#              drained per-sid; server-side queue routing is the next lane)
# handler_name names the MountainWorld._apply/stage owners (world_say,
# world_whisper) — no orphan handlers: server/world.py owns both branches.
CHAT_VERBS: tuple[str, ...] = ("say", "whisper")

CHAT_SPEC: dict[str, Any] = {
    "schema": SCHEMA,
    "session_states": list(DEFAULT_SPEC["session_states"]),
    "reject_codes": list(DEFAULT_SPEC["reject_codes"]) + ["BAD_TEXT"],
    "transport_reject_codes": list(DEFAULT_SPEC["transport_reject_codes"]),
    "rows": [dict(r) for r in DEFAULT_SPEC["rows"]] + [
        {"verb": "say", "required_state": "AUTHED",
         "handler_name": "world_say", "reject_code": "UNKNOWN_SID"},
        {"verb": "whisper", "required_state": "AUTHED",
         "handler_name": "world_whisper", "reject_code": "UNKNOWN_SID"},
    ],
}

CHAT_TABLE = compile_table(CHAT_SPEC)
CHAT_DIGEST: str = CHAT_TABLE.digest
CHAT_DISPATCH = ProtocolDispatch(CHAT_TABLE)


# ------------------------------------------------- LW7 anti-cheat (2026-09-30)
# S20's design (watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md, S20): the
# server-authoritative world kills position/velocity cheats by
# construction; the real surfaces are action spam (the 2026-09-29 demo
# logged 30 tags / 30 ticks from one client with no cap), replay abuse
# (a winning tape re-fed to the wire to re-earn its credit), and
# collusion (a later lane, through the agreement engine). This lands the
# first two as receipt laws over the DEFAULT rows; the codes ride the
# closed reject vocabulary, never per-verb rows (see the module docstring
# for why).
ANTICHEAT_SPEC: dict[str, Any] = {
    "schema": SCHEMA,
    "session_states": list(DEFAULT_SPEC["session_states"]),
    "reject_codes": list(DEFAULT_SPEC["reject_codes"])
    + ["RATE_CAP", "STALE_NONCE"],
    "transport_reject_codes": list(DEFAULT_SPEC["transport_reject_codes"]),
    "rows": [dict(r) for r in DEFAULT_SPEC["rows"]],
}

ANTICHEAT_TABLE = compile_table(ANTICHEAT_SPEC)
ANTICHEAT_DIGEST: str = ANTICHEAT_TABLE.digest

# The nonce sentinel: "the action carried no 'n' field at all" is a third
# state, distinct from every legal and illegal id value.
NO_NONCE = object()


class ReceiptGate:
    """The RATE_CAP + STALE_NONCE receipt laws, executable (LW7, S20).

    The enforcement point (server/server.py, the action branch) calls
    these in the order: admit_nonce -> world validation -> admit_cap ->
    world.stage -> commit. The split is the law:

    STALE_NONCE (the replay law): per-session monotonic action ids. The
    v0 wire made 'n' optional, so nonce-less actions stay legal for
    sessions that never bound themselves — but the first action that
    carries 'n' BINDS the session: every later action must carry a
    non-bool int 'n' strictly greater than the high-water mark
    (type(n) is int: a bool is a verdict, not an id, the X9 u8 law
    again; floats and strings are not ids either). An id BURNS AT
    RECEIPT, the moment it passes this gate — not at staging: a
    rate-capped or world-rejected action still spends its id. That is
    what makes a replayed tape worthless against the session that
    produced it: every recorded id sits at or below the high-water, so
    every row of the tape rejects STALE_NONCE while the world log still
    verifies it. Tapes verify; they cannot re-earn.

    RATE_CAP (the spam law): per-sid, per-tick staged-action budget of
    1. The tick bucket is the tick the action would apply at
    (world.tick_count + 1 — the receipt window between two ticks);
    admit_cap only READS the spent set, and commit spends it, and the
    server commits ONLY on a world ack. A world-rejected action (DRY_POOL
    and friends) therefore leaves the budget untouched: a client that
    misfires at a dry pool has not spent its tick. The second acked
    action in the same bucket rejects RATE_CAP at receipt and never
    stages. Whisper (LW6) acks without a tick of its own, but an ack is
    an ack: it spends the sid's window like every other verb.
    """

    __slots__ = ("_staged_tick", "_nonce_hwm")

    def __init__(self) -> None:
        self._staged_tick: dict[str, int] = {}
        self._nonce_hwm: dict[str, int] = {}

    def admit_nonce(self, sid: str, nonce: Any) -> str | None:
        """The replay envelope. Returns STALE_NONCE or None; a passing id
        burns NOW, before the cap or the world can refuse the action."""
        if nonce is NO_NONCE:
            if sid in self._nonce_hwm:
                # a bound session cannot unbind: stripping 'n' off a
                # replayed tape is the first trick the law forecloses
                return "STALE_NONCE"
            return None
        if type(nonce) is not int:
            return "STALE_NONCE"
        hwm = self._nonce_hwm.get(sid)
        if hwm is not None and nonce <= hwm:
            return "STALE_NONCE"
        self._nonce_hwm[sid] = nonce
        return None

    def admit_cap(self, sid: str, applies_at_tick: int) -> str | None:
        """The spam envelope, read-only: has this sid already spent its
        budget in this tick bucket? Spending happens in commit()."""
        if self._staged_tick.get(sid) == applies_at_tick:
            return "RATE_CAP"
        return None

    def commit(self, sid: str, applies_at_tick: int) -> None:
        """Spend the sid's tick bucket. The server calls this ONLY on a
        world ack; cap and nonce are separate laws with separate spend
        semantics on purpose (the nonce burns at receipt, the cap at ack)."""
        self._staged_tick[sid] = applies_at_tick

    # views for tests and operability
    def nonce_hwm(self, sid: str) -> int | None:
        return self._nonce_hwm.get(sid)

    def staged_tick(self, sid: str) -> int | None:
        return self._staged_tick.get(sid)


# ------------------------------------------------- B4 SRP6 auth verbs (2026-09-30)
# The auth dialect (B4, receipt watch/inbox/last_mile_20260930/B4_SRP6_PORT.md):
# the LW4-proven SRP6 handshake ported onto OUR wire as three pre-auth verbs
# -- srp_register, srp_challenge, srp_proof -- law: verbs are frozen data rows
# like every other verb, never hardcoded strings. The X9/LW6/LW7 law again:
# SRP6_AUTH_TABLE compiles the DEFAULT rows plus the auth rows as a NEW
# contract version; DEFAULT (the bound v0 wire) stays byte-identical and
# PROTOCOL_DIGEST does not move.
#
# WHY required_state is CONNECTED: these verbs run PRE-auth by definition
# (their whole job is to mint the first sid), so their floor is the lowest
# rank -- rank(any_state) >= rank(CONNECTED) always holds, and the row's
# reject_code slot is a reserved never-fires slot, exactly the v0
# NOT_YOUR_TURN precedent ("the code exists so v1 does not invent a new
# vocabulary mid-stream"). The REAL laws of this dialect -- BAD_PROOF (M1
# mismatch or malformed proof) and STALE_CHALLENGE (proof with no pending
# single-use handshake: the replay/nonce law) -- ride the closed reject
# VOCABULARY, never per-verb rows, the LW6 BAD_TEXT / LW7 RATE_CAP law: a
# replayed proof is stale on whichever arm carried it, and no row may own
# that. The enforcement point is server/server.py's op ladder, which gates
# every srp_* op through SRP6_AUTH_DISPATCH BEFORE its handler runs (gate
# before verb, the ordering law), resolves the peer state AUTHED/CONNECTED
# like state_for_sid does, and refuses typed on any gate failure.
# handler_name names the owner in server/server.py (_on_srp_* methods);
# the math lives in server/auth_srp6.py, ported from tools/realmd_client.
SRP6_AUTH_VERBS: tuple[str, ...] = ("srp_register", "srp_challenge", "srp_proof")

SRP6_AUTH_SPEC: dict[str, Any] = {
    "schema": SCHEMA,
    "session_states": list(DEFAULT_SPEC["session_states"]),
    "reject_codes": list(DEFAULT_SPEC["reject_codes"])
    + ["BAD_PROOF", "STALE_CHALLENGE"],
    "transport_reject_codes": list(DEFAULT_SPEC["transport_reject_codes"]),
    "rows": [dict(r) for r in DEFAULT_SPEC["rows"]] + [
        {"verb": verb, "required_state": "CONNECTED",
         "handler_name": f"auth_{verb}", "reject_code": "UNKNOWN_SID"}
        for verb in SRP6_AUTH_VERBS
    ],
}

SRP6_AUTH_TABLE = compile_table(SRP6_AUTH_SPEC)
SRP6_AUTH_DIGEST: str = SRP6_AUTH_TABLE.digest
SRP6_AUTH_DISPATCH = ProtocolDispatch(SRP6_AUTH_TABLE)


# ------------------------------------------- V7 identity verbs (2026-09-30/10-01)
# The identity-binding dialect (V7, receipt watch/inbox/last_mile_20260930/
# V7_IDENTITY_BIND.md; math in server/identity_binding.py): GitHub-published
# SSH-key proof of first contact. THE PROMOTION (the receipt's table law):
# V7 landed the frozen rows inside identity_binding.py and named this file
# (B4's placement, the verb registry) as their promoted home "when the
# server.py wiring lane lands" — this is that lane. The spec below is
# BYTE-IDENTICAL to identity_binding.IDENTITY_AUTH_SPEC (same DEFAULT base,
# same two rows, same reject vocabulary in the same order), so
# IDENTITY_AUTH_DIGEST == identity_binding.IDENTITY_AUTH_DIGEST and the two
# compilations are one contract; tests/test_identity_wiring.py pins the
# equality so neither copy can drift without failing a test.
#
# The laws are the receipt's, unchanged: identity_challenge / identity_proof
# are frozen data rows, required_state CONNECTED (pre-auth by definition, the
# B4 precedent; the reject_code slot is a reserved never-fires slot),
# handler_name names the server/server.py owners (_on_identity_* handlers,
# the auth_srp_* precedent). The dialect's real laws ride the closed reject
# VOCABULARY, never per-verb rows (the LW6/LW7 law): BAD_PROOF (signature
# does not verify), STALE_CHALLENGE (no pending single-use challenge, user
# mismatch, or expired — the replay/nonce law), NO_KEYS (the .keys fetch
# failed or the login publishes nothing — LW2's wrong-username signal).
# DEFAULT (the bound v0 wire) stays byte-identical and PROTOCOL_DIGEST does
# not move; IDENTITY_AUTH_DIGEST is a NEW contract version, the X9/LW6/LW7/
# B4 law again.
IDENTITY_AUTH_VERBS: tuple[str, ...] = ("identity_challenge", "identity_proof")

IDENTITY_AUTH_SPEC: dict[str, Any] = {
    "schema": SCHEMA,
    "session_states": list(DEFAULT_SPEC["session_states"]),
    "reject_codes": list(DEFAULT_SPEC["reject_codes"])
    + ["BAD_PROOF", "STALE_CHALLENGE", "NO_KEYS"],
    "transport_reject_codes": list(DEFAULT_SPEC["transport_reject_codes"]),
    "rows": [dict(r) for r in DEFAULT_SPEC["rows"]] + [
        {"verb": "identity_challenge", "required_state": "CONNECTED",
         "handler_name": "auth_identity_challenge", "reject_code": "UNKNOWN_SID"},
        {"verb": "identity_proof", "required_state": "CONNECTED",
         "handler_name": "auth_identity_proof", "reject_code": "UNKNOWN_SID"},
    ],
}

IDENTITY_AUTH_TABLE = compile_table(IDENTITY_AUTH_SPEC)
IDENTITY_AUTH_DIGEST: str = IDENTITY_AUTH_TABLE.digest
IDENTITY_AUTH_DISPATCH = ProtocolDispatch(IDENTITY_AUTH_TABLE)


def validate(session_state: str, verb: str) -> tuple[bool, str | None]:
    """The action op-ladder's table-driven gate (DEFAULT contract)."""
    return DEFAULT_DISPATCH.validate(session_state, verb)


def state_for_sid(sid: str, roster: Container[str]) -> str:
    """Resolve the session state the ladder gates on: a sid the world never
    issued means the asker is CONNECTED, a registered sid means AUTHED.
    v0 grants nothing higher, so TURN_HELD is reachable only in v1."""
    return "AUTHED" if sid in roster else "CONNECTED"


def main() -> int:  # pragma: no cover - operability convenience
    doc = DEFAULT_TABLE.to_document()
    doc["protocol_digest"] = PROTOCOL_DIGEST
    print(json.dumps(doc, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
