#!/usr/bin/env python3
"""ledger_append_gate -- pre-append schema gate for memory/burns/LEDGER.jsonl.

FORCED BY the PROBE-C detector-miss (watch/inbox/BURN_adversarial-self-probes_20260926_d.md,
2026-09-26): the boolean fresh_failure_mode check existed only as a lane census, nothing
invoked it on append, and 401 new violations accumulated between two same-day censuses
(watch/inbox/BURN_middle-path-doctrine_20260926_f.md). Detection with no schedule is a
miss. This module is the pre-registered append gate: the WRITER calls it before appending.
It never appends, never mutates the ledger (duplicate scan is read-only), and refuses with
exit 2 so a caller cannot mistake a refusal for a success path.

Contract (validated BEFORE any append):
  (a) the line parses as a JSON object;
  (b) required fields, with types:
        ts                  str, ISO-8601 UTC (trailing Z or +00:00 offset, real calendar date)
        slug                str, nonempty
        verdict             str, nonempty
        fresh_failure_mode  bool (strict type: prose strings, ints, null all refuse)
        landing             str, nonempty; either an explicit owed-marker ("owed"/"missing",
                            case-insensitive) or a path that exists (absolute, repo-relative,
                            or cwd-relative)
        one_line            str
  (c) duplicate check: a byte-identical one_line value already present in the ledger refuses;
  (d) exit 0 + "VALID" on pass, exit 2 + reason on fail. The gate never appends itself.

Usage:
  python tools/ledger_append_gate.py --line '{"ts": "2026-09-27T00:00:00Z", ...}'
  python tools/ledger_append_gate.py --file candidate.json --ledger memory/burns/LEDGER.jsonl
  from tools.ledger_append_gate import validate_line
      ok = validate_line(raw_line, ledger_path)   # raises Refusal on any refusal

Adoption is cross-window by contract: tools/ledger_lock.py append (the sanctioned
single-writer path, JSON-validates only) is the natural caller, and NOTHING is wired at
landing (per the _d falsifier, wiring is a visible adoption step, never smuggled inside
this build). The _d falsifier also named a verdict enum and a per-line sha pin; both stay
owed. This build pins the boolean-ffm core, the landing/owed split, and the byte-identical
duplicate check the C8 census measurements were blind to. Known boundary, inherited by
design: paraphrased (non-byte-identical) one_line re-branding of a solved mode still
passes; catching that needs a similarity check, deliberately out of scope here.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = REPO / "memory" / "burns" / "LEDGER.jsonl"

REQUIRED_FIELDS = ("ts", "slug", "verdict", "fresh_failure_mode", "landing", "one_line")

# ISO-8601 UTC only: fleet convention is "...Z"; +00:00 accepted as the same instant.
ISO_UTC_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)$")

# Explicit owed-marker vocabulary mirrors ledger_close_check.MISSING_RE ("owed", "missing").
OWED_RE = re.compile(r"\b(owed|missing)\b", re.IGNORECASE)


class Refusal(ValueError):
    """A gate refusal reason. The calling writer must not append the line."""


def _landing_exists(landing: str) -> tuple[bool, str]:
    """Resolve landing against absolute, repo-root, then cwd; report which one hit."""
    p = Path(landing)
    candidates = [p] if p.is_absolute() else [REPO / p, p]
    for c in candidates:
        if c.exists():
            return True, str(c)
    return False, str(candidates[0])


def validate_line(line: str, ledger_path: Path | str = DEFAULT_LEDGER) -> dict:
    """Validate one candidate JSONL line against the ledger contract.

    Returns a result dict with ok=True on pass. Raises Refusal (ValueError) with a
    single actionable reason on any refusal. Never writes anywhere.
    """
    # (a) JSON parses
    try:
        row = json.loads(line)
    except ValueError as e:
        raise Refusal(f"(a) line does not parse as JSON: {e}")
    if not isinstance(row, dict):
        raise Refusal("(a) line parses but is not a JSON object (ledger rows are objects)")

    # (b) required fields present
    absent = [f for f in REQUIRED_FIELDS if f not in row]
    if absent:
        raise Refusal(f"(b) required field(s) missing: {', '.join(absent)}")

    # ts: ISO-8601 UTC string, lexically shaped and calendar-valid
    ts = row["ts"]
    if not isinstance(ts, str) or not ISO_UTC_RE.match(ts):
        raise Refusal(
            "(b) ts must be an ISO-8601 UTC string like 2026-09-27T01:42:30Z "
            f"(Z or +00:00 offset required), got {ts!r}")
    try:
        _dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError as e:
        raise Refusal(f"(b) ts is shaped like ISO-8601 but is not a real timestamp: {e}")

    # slug / verdict: nonempty strings
    for field in ("slug", "verdict"):
        v = row[field]
        if not isinstance(v, str) or not v.strip():
            raise Refusal(f"(b) {field} must be a nonempty string, got {v!r}")

    # fresh_failure_mode: strict boolean. This is the check the PROBE-C forgery
    # slipped past: a prose string re-branding a solved mode as fresh. Evidence it
    # was needed and unused before landing: BURN_middle-path-doctrine_20260926_f.md
    # counted 401 new violations accumulating between two same-day censuses.
    ffm = row["fresh_failure_mode"]
    if not isinstance(ffm, bool):
        raise Refusal(
            "(b) fresh_failure_mode must be boolean true/false (strict type), "
            f"got {type(ffm).__name__}: {ffm!r}")

    # landing: owed-marker OR a path that exists right now
    landing = row["landing"]
    if not isinstance(landing, str) or not landing.strip():
        raise Refusal(f"(b) landing must be a nonempty string, got {landing!r}")
    if OWED_RE.search(landing):
        landing_state = "owed-marker"
    else:
        exists, resolved = _landing_exists(landing)
        if not exists:
            raise Refusal(
                f"(b) landing path does not exist on disk and carries no owed-marker "
                f"(owed|missing): {landing} (resolved {resolved})")
        landing_state = f"exists ({resolved})"

    # one_line: string (contract pins type; emptiness is not this gate's law)
    one_line = row["one_line"]
    if not isinstance(one_line, str):
        raise Refusal(f"(b) one_line must be a string, got {type(one_line).__name__}")

    # (c) duplicate: byte-identical one_line already banked refuses
    ledger = Path(ledger_path)
    rows_scanned = 0
    unparsable = 0
    if ledger.exists():
        with ledger.open("r", encoding="utf-8") as f:
            for raw in f:
                raw = raw.strip()
                if not raw:
                    continue
                rows_scanned += 1
                try:
                    prior = json.loads(raw)
                except ValueError:
                    unparsable += 1  # legacy dirt: history is not this gate's charge
                    continue
                if isinstance(prior, dict) and prior.get("one_line") == one_line:
                    raise Refusal(
                        f"(c) duplicate one_line already in ledger "
                        f"(row {rows_scanned} of {ledger}): {one_line[:120]}")

    return {
        "ok": True,
        "rows_scanned": rows_scanned,
        "legacy_unparsable": unparsable,
        "landing_state": landing_state,
        "ts": ts,
        "slug": row["slug"],
        "verdict": row["verdict"],
        "fresh_failure_mode": ffm,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="ledger_append_gate",
        description="Pre-append schema gate for LEDGER.jsonl rows (never appends)")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--line", help="candidate JSONL line as a string")
    src.add_argument("--file", help="file containing exactly the candidate JSON line")
    ap.add_argument("--ledger", default=str(DEFAULT_LEDGER),
                    help="ledger scanned for duplicates (default memory/burns/LEDGER.jsonl)")
    args = ap.parse_args(argv)

    line = args.line if args.line is not None else Path(args.file).read_text(encoding="utf-8")
    try:
        result = validate_line(line, args.ledger)
    except Refusal as e:
        print(f"REFUSE {e}", file=sys.stderr)
        return 2
    print(
        f"VALID row passes the append gate (duplicate scan: {result['rows_scanned']} rows, "
        f"{result['legacy_unparsable']} legacy unparsable; landing {result['landing_state']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
