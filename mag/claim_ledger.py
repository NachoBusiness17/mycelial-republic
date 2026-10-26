"""mag_claims.v1 - the live-claim ledger: parse, validate, append (fail-closed).

Schema owner: memory/runs/genetic_burn/20261018/G0/lanes/g01-ledger-schema.md
(G0 lane g01-ledger-schema; this module is G1 lane i01-ledger-build).

Ledger file: watch/claims.jsonl, one JSON object per line, append-only
(same event-sourced fold shape as watch/inbox/index_events.jsonl). Rows are
never rewritten or deleted in place; a refresh appends a new row with a
bumped ``claim-<slug>-00N`` suffix and names its predecessor in
``supersedes``.

Laws carried forward (citations in the parent lane file):
- Freeze law (B2-274): pin regexes are owned by this ledger plus the patrol
  selftest, never auto-synced to live carrier bytes. A carrier reword must
  fail the gate loudly instead of silently rephrasing.
- Fail-closed law: a missing ledger, an unparseable line, or a future-dated
  moment is "cannot verify" (exit 2), never a pass, never a guess.
- Accept-by-name law: a stale or contradicted row is carried by a named
  acceptance, never silently ignored, never deleted.
- B2-338 case law: ok output uses the lowercase ``ok`` prefix.
- Consumer law (ORG_SYSTEM_V2 Organ 5): every row names its consumer and its
  verifier in the same registration, or it is a cow, not a spore.

v0 anchor note (GENOME G0, i01 assignment): this module does NOT write the
verkle chain. Every row reserves an ``anchor`` field and v0 stores it as
null; the validator rejects any non-null anchor. The wiring hook point is the
mag/work_register.py:84-92 precedent: there, one fold appends
logs/claims.jsonl (lines 84-85) and then anchors the same fact into the
chain via mag.verkle_knot.append_verkle_knot (lines 88-97) - one integrity
store, never a second. Flipping claim_ledger to write real chain anchors is
an OPERATOR GATE: the chain is the estate's durable spine and a ledger seat
does not self-authorize writes to it. Until the operator lands that gate,
null is the only lawful value.

Exit-code contract (mirrors the census patrol's cannot-verify convention):
  0  ok            every line parsed and validated
  1  invalid       schema defect (bad field, duplicate id, dangling supersedes,
                   non-null anchor, ...)
  2  cannot-verify missing ledger, unparseable JSON line, unparsable or
                   future-dated moment - the base truth itself is unreadable
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

SCHEMA = "mag_claims.v1"
LEDGER_DEFAULT = "watch/claims.jsonl"

# The four verifier kinds the five seed rows need (parent lane, Finding 3).
VERIFIER_KINDS = ("delegate_tool", "yaml_crosscheck", "regen_age", "crown_contradiction")
ON_FAIL_VALUES = ("WARN", "ENFORCE")
VERDICT_VALUES = ("GREEN", "STALE-AT-REGISTRATION", "CONTRADICTED")
PIN_MODES = ("single", "finditer_all")
REGEX_FLAG_NAMES = {
    "MULTILINE": re.MULTILINE,
    "IGNORECASE": re.IGNORECASE,
    "DOTALL": re.DOTALL,
}

# id grammar from the schema table: claim-<slug>-00N, stable, unique, never reused.
ID_RE = re.compile(r"^claim-[a-z0-9][a-z0-9-]*-\d{3}$")

REQUIRED_FIELDS = (
    "schema",
    "id",
    "claim_text",
    "carrier_path",
    "pins",
    "moment",
    "owner",
    "consumer",
    "verifier",
    "on_fail",
    "registration_verdict",
    "receipt",
)
OPTIONAL_FIELDS = ("evidence", "supersedes", "anchor")
ALLOWED_FIELDS = frozenset(REQUIRED_FIELDS) | frozenset(OPTIONAL_FIELDS)

EXIT_OK = 0
EXIT_INVALID = 1
EXIT_CANNOT_VERIFY = 2

# Registration instant is "now" when a seat writes the row; a 60 s grace
# absorbs clock skew so a legitimate now-row is not flagged future. Real
# future-dating (minutes and beyond) still fail-closes per the law.
_FUTURE_SKEW = timedelta(seconds=60)


def norm_flags(value: Any) -> tuple[int, str | None]:
    """Normalize a pin ``flags`` value to a re flag mask."""
    if value is None:
        return 0, None
    names = [value] if isinstance(value, str) else value
    if not isinstance(names, list) or not all(isinstance(n, str) for n in names):
        return 0, "flags: must be a flag-name string or a list of flag names"
    acc = 0
    for n in names:
        if n not in REGEX_FLAG_NAMES:
            return 0, f"flags: unknown regex flag {n!r} (allowed: {sorted(REGEX_FLAG_NAMES)})"
        acc |= REGEX_FLAG_NAMES[n]
    return acc, None


def _rel_path_error(value: Any, field: str) -> str | None:
    """Repo-posix relative path check for carrier_path / receipt / truth paths."""
    if not isinstance(value, str) or not value.strip():
        return f"{field}: must be a non-empty repo-posix path string"
    if "\\" in value:
        return f"{field}: repo paths are posix, got backslash: {value!r}"
    if value.startswith(("/", "~")) or re.match(r"^[A-Za-z]:", value):
        return f"{field}: must be repo-relative, got absolute: {value!r}"
    parts = value.split("/")
    if any(p in ("", ".", "..") for p in parts):
        return f"{field}: empty/dot/dotdot path segment: {value!r}"
    return None


def parse_moment(value: Any) -> datetime | None:
    """Parse an ISO-8601 moment that must carry an explicit UTC designator."""
    if not isinstance(value, str):
        return None
    s = value.strip()
    if s.endswith(("Z", "z")):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    if dt.tzinfo is None:
        return None  # naive moments are ambiguous, hence unusable
    return dt.astimezone(timezone.utc)


def parse_line(text: str) -> tuple[str, Any]:
    """Stage 1: one ledger line -> ("ok", row) or ("cannot_verify", detail)."""
    s = text.strip()
    if not s:
        return "cannot_verify", "blank line (ledger lines are never blank; never rewrite - file the incident)"
    try:
        row = json.loads(s)
    except json.JSONDecodeError as e:
        return "cannot_verify", f"unparseable JSON line: {e.msg} (col {e.colno})"
    if not isinstance(row, dict):
        return "cannot_verify", "line is valid JSON but not an object"
    return "ok", row


def _validate_pin(idx: int, pin: Any, bad) -> None:
    label = f"pins[{idx}]"
    if not isinstance(pin, dict):
        bad(f"{label}: must be an object")
        return
    pin_id = pin.get("pin_id")
    if not isinstance(pin_id, str) or not pin_id.strip():
        bad(f"{label}.pin_id: must be a non-empty slug string")
    claim_regex = pin.get("claim_regex")
    if not isinstance(claim_regex, str) or not claim_regex:
        bad(f"{label}.claim_regex: required frozen python re syntax (stage 2)")
        return
    flags, ferr = norm_flags(pin.get("flags"))
    if ferr:
        bad(f"{label}.{ferr}")
        flags = 0
    try:
        compiled = re.compile(claim_regex, flags)
    except re.error as e:
        bad(f"{label}.claim_regex: does not compile ({e})")
        return
    locator = pin.get("locator_regex")
    if locator is not None:
        if not isinstance(locator, str) or not locator:
            bad(f"{label}.locator_regex: when present it must be a non-empty string (stage 1)")
        else:
            try:
                re.compile(locator, flags)
            except re.error as e:
                bad(f"{label}.locator_regex: does not compile ({e})")
    mode = pin.get("mode", "single")
    if mode not in PIN_MODES:
        bad(f"{label}.mode: must be one of {PIN_MODES}, got {mode!r}")
    capture = pin.get("capture_fields", [])
    if not isinstance(capture, list) or not all(isinstance(c, str) and c for c in capture):
        bad(f"{label}.capture_fields: must be a list of non-empty group names")
    elif len(set(capture)) != len(capture):
        bad(f"{label}.capture_fields: duplicate group names")
    elif len(capture) > compiled.groups:
        bad(f"{label}.capture_fields: {len(capture)} names but the regex has only {compiled.groups} capture groups")
    expected = pin.get("expected")
    if expected is not None and not isinstance(expected, dict):
        bad(f"{label}.expected: when present it must be the registration-moment truth object")


def validate_row(row: dict, now: datetime | None = None) -> list[tuple[str, str]]:
    """Validate one parsed row. Returns (kind, message) problems; empty = valid.

    kind "invalid" is a schema defect (exit 1); kind "cannot_verify" means the
    row's own truth is unreadable (exit 2, the fail-closed law).
    """
    problems: list[tuple[str, str]] = []

    def bad(msg: str) -> None:
        problems.append(("invalid", msg))

    if row.get("schema") != SCHEMA:
        bad(f"schema: expected {SCHEMA!r}, got {row.get('schema')!r}")
    rid = row.get("id")
    if not isinstance(rid, str) or not ID_RE.match(rid):
        bad(f"id: must match claim-<slug>-00N grammar, got {rid!r}")
    claim_text = row.get("claim_text")
    if not isinstance(claim_text, str) or not claim_text.strip():
        bad("claim_text: required non-empty prose in the carrier's own register")
    err = _rel_path_error(row.get("carrier_path"), "carrier_path")
    if err:
        bad(err)
    pins = row.get("pins")
    if not isinstance(pins, list) or not pins:
        bad("pins: required non-empty array of frozen byte claims")
    else:
        seen_pins: set[str] = set()
        for i, pin in enumerate(pins):
            if isinstance(pin, dict) and isinstance(pin.get("pin_id"), str):
                if pin["pin_id"] in seen_pins:
                    bad(f"pins[{i}].pin_id: duplicate within row: {pin['pin_id']!r}")
                seen_pins.add(pin["pin_id"])
            _validate_pin(i, pin, bad)
    dt = parse_moment(row.get("moment"))
    if dt is None:
        # Fail-closed law: an unparsable moment cannot be verified, never guessed.
        problems.append(("cannot_verify", f"moment: not an ISO-8601 UTC instant: {row.get('moment')!r}"))
    else:
        now = now or datetime.now(timezone.utc)
        if dt > now + _FUTURE_SKEW:
            problems.append(
                ("cannot_verify",
                 f"moment: future-dated ({dt.isoformat()} > now); registration instant must not lie ahead")
            )
    for field in ("owner", "consumer"):
        v = row.get(field)
        if not isinstance(v, str) or not v.strip():
            bad(f"{field}: required non-empty string (consumer law: a row without a consumer is a cow, not a spore)")
    verifier = row.get("verifier")
    if not isinstance(verifier, dict):
        bad("verifier: required object {type, args, bar}")
    else:
        if verifier.get("type") not in VERIFIER_KINDS:
            bad(f"verifier.type: must be one of {VERIFIER_KINDS}, got {verifier.get('type')!r}")
        if not isinstance(verifier.get("args"), dict):
            bad("verifier.args: required object")
        if not isinstance(verifier.get("bar"), dict):
            bad("verifier.bar: required object (the pass/fail bars)")
    if row.get("on_fail") not in ON_FAIL_VALUES:
        bad(f"on_fail: must be one of {ON_FAIL_VALUES} (WARN-first; the flip is an operator call)")
    if row.get("registration_verdict") not in VERDICT_VALUES:
        bad(f"registration_verdict: must be one of {VERDICT_VALUES} (honest state at registration; never back-dated green)")
    err = _rel_path_error(row.get("receipt"), "receipt")
    if err:
        bad(err)
    evidence = row.get("evidence")
    if evidence is not None and not isinstance(evidence, dict):
        bad("evidence: when present it must be an object of byte-level pointers")
    sup = row.get("supersedes")
    if sup is not None and (not isinstance(sup, str) or not ID_RE.match(sup)):
        bad(f"supersedes: when present it must be a claim id, got {sup!r}")
    if "anchor" in row and row["anchor"] is not None:
        bad(
            "anchor: v0 stores null only; chain anchoring is operator-gated "
            "(hook point mag/work_register.py:84-92 precedent; a ledger seat never self-authorizes chain writes)"
        )
    unknown = sorted(set(row) - ALLOWED_FIELDS)
    if unknown:
        bad(f"unknown field(s) {unknown}: mag_claims.v1 is closed; bump the schema to add fields")
    return problems


def load_ledger(path: str | Path, now: datetime | None = None) -> dict:
    """Load and validate a whole ledger file. Fail-closed, never raising."""
    p = Path(path)
    if not p.is_file():
        return {
            "exit": EXIT_CANNOT_VERIFY,
            "entries": [],
            "rows": [],
            "problems": [(0, "cannot_verify", f"ledger missing: {p}")],
        }
    entries: list[dict] = []
    problems: list[tuple[int, str, str]] = []
    seen_ids: dict[str, int] = {}
    for lineno, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        kind, obj = parse_line(line)
        row_problems: list[tuple[str, str]] = []
        if kind != "ok":
            row_problems.append((kind, obj))
            entries.append({"lineno": lineno, "row": None, "problems": row_problems})
            problems.append((lineno, kind, obj))
            continue
        row_problems = validate_row(obj, now=now)
        rid = obj.get("id")
        if isinstance(rid, str):
            if rid in seen_ids:
                row_problems.append(
                    ("invalid", f"duplicate id {rid!r}: first seen on line {seen_ids[rid]} (ids are never reused; refresh appends a bumped suffix)")
                )
            else:
                seen_ids[rid] = lineno
        sup = obj.get("supersedes")
        if isinstance(sup, str) and sup not in seen_ids:
            row_problems.append(
                ("invalid", f"supersedes {sup!r} does not reference an earlier row in this ledger")
            )
        for k, msg in row_problems:
            problems.append((lineno, k, msg))
        entries.append({"lineno": lineno, "row": obj, "problems": row_problems})
    if any(k == "cannot_verify" for _, k, _ in problems):
        exit_code = EXIT_CANNOT_VERIFY
    elif problems:
        exit_code = EXIT_INVALID
    else:
        exit_code = EXIT_OK
    return {
        "exit": exit_code,
        "entries": entries,
        "rows": [e["row"] for e in entries if e["row"] is not None],
        "problems": problems,
    }


def append_row(path: str | Path, row: dict, now: datetime | None = None) -> dict:
    """Validate one row and append it as a single line. Append-only.

    Refuses (never partially writes) when the row is invalid, when the id
    already exists, when supersedes dangles, or when the existing ledger
    itself fails validation (an unverifiable base never grows).
    """
    p = Path(path)
    if p.is_file():
        base = load_ledger(p, now=now)
        if base["exit"] != EXIT_OK:
            return {
                "ok": False,
                "exit": base["exit"],
                "errors": [f"base ledger fails validation (exit {base['exit']}); refusing to append onto an unverifiable ledger"]
                + [f"line {n}: {k}: {m}" for n, k, m in base["problems"][:10]],
            }
        existing_ids = {r.get("id") for r in base["rows"] if isinstance(r, dict)}
    else:
        existing_ids = set()
    problems = validate_row(row, now=now)
    rid = row.get("id")
    if isinstance(rid, str):
        if rid in existing_ids:
            problems.append(
                ("invalid", f"duplicate id {rid!r}: already in the ledger; a refresh appends a bumped -00N row naming the predecessor in supersedes")
            )
        sup = row.get("supersedes")
        if isinstance(sup, str) and sup not in existing_ids:
            problems.append(("invalid", f"supersedes {sup!r}: not found in the ledger"))
    if problems:
        kinds = {k for k, _ in problems}
        exit_code = EXIT_CANNOT_VERIFY if "cannot_verify" in kinds else EXIT_INVALID
        return {"ok": False, "exit": exit_code, "errors": [f"{k}: {m}" for k, m in problems]}
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(row, ensure_ascii=False, sort_keys=False) + "\n")
    return {"ok": True, "exit": EXIT_OK, "errors": []}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python -m mag.claim_ledger",
        description=f"{SCHEMA} ledger: parse / validate / append (append-only, fail-closed)",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_check = sub.add_parser("check", help="load + validate a ledger; prints lowercase ok lines (B2-338)")
    p_check.add_argument("ledger", nargs="?", default=LEDGER_DEFAULT)
    p_add = sub.add_parser("append", help="validate one row (JSON file path, or - for stdin) and append it")
    p_add.add_argument("ledger")
    p_add.add_argument("row", help="path to a one-row JSON file, or '-' for stdin")
    args = ap.parse_args(argv)

    if args.cmd == "check":
        res = load_ledger(args.ledger)
        for e in res["entries"]:
            if e["row"] is not None and not e["problems"]:
                print(f"ok {e['row'].get('id')}")
        for lineno, kind, msg in res["problems"]:
            print(f"{kind.replace('_', '-')} line {lineno}: {msg}", file=sys.stderr)
        print(
            f"ok check {args.ledger}: {len(res['rows'])} rows, "
            f"{len(res['problems'])} problems, exit {res['exit']}"
        )
        return res["exit"]

    if args.cmd == "append":
        try:
            text = sys.stdin.read() if args.row == "-" else Path(args.row).read_text(encoding="utf-8")
        except OSError as e:
            print(f"cannot-verify: cannot read row source: {e}", file=sys.stderr)
            return EXIT_CANNOT_VERIFY
        kind, obj = parse_line(text)
        if kind != "ok":
            print(f"cannot-verify: {obj}", file=sys.stderr)
            return EXIT_CANNOT_VERIFY
        res = append_row(args.ledger, obj)
        if res["ok"]:
            print(f"ok appended {obj.get('id')} to {args.ledger}")
            return EXIT_OK
        for e in res["errors"]:
            print(e, file=sys.stderr)
        print(f"append refused, exit {res['exit']}", file=sys.stderr)
        return res["exit"]
    return EXIT_CANNOT_VERIFY


if __name__ == "__main__":
    sys.exit(main())
