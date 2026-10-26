#!/usr/bin/env python3
"""fifty_wide_guard.py - fifty-wide wave pre-flight guard (GO item 8, D1 ruling).

The disease this meters (watch/inbox/burn_claims_50wide_20261003.md, D1 in
corpus/steal/MASTER_MICKEY17_V2.md section 7): the 2026-10-03 fifty-wide burn
wave fired 50 flash lanes while the extraction artifact
memory/runs/burn_audit_claims.json held 60 distinct units, so 10 units carried
no recorded verdict and no per-agent artifact existed on disk to explain the
drop. The prior em-dash hypothesis is REFUTED (measured 2 em-dash units, never
10; the number is in the D1 record). There was no runner file: the wave was a
main-session Task-agent fan-out (the protocol shape in the receipt), so nothing
asserted the extracted unit count against the lane count before firing.

Bar stated in numbers BEFORE reading anything:

  a fifty-wide dispatch is allowed to fire only when the extraction artifact's
  unit count EQUALS the lane count (the dispatch plan's length, or an explicit
  --lanes). Any mismatch is exit 1 with the dropped-unit list printed to stdout
  and appended to the wave receipt; the guard never renumbers, trims, or pads
  the plan to make the counts meet.

Fail-closed by construction: a missing or unparseable units artifact, plan, or
receipt parent is exit 2 (cannot verify), never a pass. Duplicate plan keys and
plan keys absent from the extraction are exit 1 even when the lengths match,
because both mean the fan-out would not cover the units it claims.

Dispatch-log retention (a07#1 operator sub-item): every passing pre-flight
appends one JSONL row to memory/runs/fifty_wide/dispatch_log.jsonl (units path,
units sha256, unit-key sha256, lanes, plan length, UTC moment, plus the wave
slug when --wave is passed) so wave counts are replayable after the fact. The
--wave slug is the replay-pair join key: fifty_wide_archive.py --verify finds
this row by it and fails PAIR-INCOMPLETE when the pre-flight half is absent.
The log is written by this tool before the
operator fires the lanes; keeping per-agent results archived next to it stays
an operator behavior (convention: memory/runs/fifty_wide/<wave>/agents/).

Exit codes: 0 = pass (counts meet, log row written); 1 = FAIL (mismatch,
duplicates, or unknown keys; dropped units printed and filed to the receipt);
2 = cannot verify (missing or unparseable inputs).

Usage:
  python tools/fifty_wide_guard.py --units memory/runs/burn_audit_claims.json \
      --plan <dispatch_plan.json> [--lanes N] [--receipt watch/inbox/<wave>.md] \
      [--log memory/runs/fifty_wide/dispatch_log.jsonl] [--no-log]

The plan file is a JSON list; each entry is one of: "file:line", ["file", line],
or {"file": ..., "line": ...} / {"id": ...}. Unit identity mirrors that shape.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = ESTATE_ROOT / "memory" / "runs" / "fifty_wide" / "dispatch_log.jsonl"

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_CANNOT_VERIFY = 2


def unit_key(unit: object) -> str:
    """Canonical string key for one extraction unit.

    Identity is (file, line) when the unit carries both (the burn-claims
    extraction shape), else "id", else the canonical JSON of the unit itself.
    Raises ValueError on non-dict units without an identity, which callers
    surface as exit 2, not a silent pass.
    """
    if isinstance(unit, dict):
        if "file" in unit and "line" in unit:
            return f"{unit['file']}:{unit['line']}"
        if "id" in unit:
            return str(unit["id"])
    raise ValueError(f"unit has no file+line or id identity: {json.dumps(unit)[:120]}")


def plan_entry_key(entry: object) -> str:
    """Canonical string key for one dispatch-plan entry.

    Accepts "file:line", ["file", line], or {"file":..., "line":...} / {"id":...}.
    Raises ValueError on shapes that cannot name a unit.
    """
    if isinstance(entry, str):
        return entry
    if isinstance(entry, (list, tuple)) and len(entry) == 2:
        return f"{entry[0]}:{entry[1]}"
    if isinstance(entry, dict):
        return unit_key(entry)
    raise ValueError(f"plan entry has no recognizable identity: {json.dumps(entry)[:120]}")


def load_json_list(path: Path, what: str) -> tuple[list[object] | None, str]:
    """Read a JSON list file. Returns (list, "") or (None, reason)."""
    if not path.is_file():
        return None, f"{what} file not found: {path}"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return None, f"{what} file unparseable: {path}: {type(e).__name__}: {e}"
    if not isinstance(data, list):
        return None, f"{what} file is not a JSON list: {path}"
    return data, ""


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def guard(
    units: list[object],
    plan: list[object],
    lanes: int | None,
) -> tuple[bool, list[str], list[str], list[str], dict]:
    """Core verdict. Returns (ok, errors, dropped, unknown, stats).

    dropped = extraction keys absent from the plan (the units that would carry
    no verdict). unknown = plan keys absent from the extraction (renumbering
    smell). errors = fail-loud reasons; empty errors means pass.
    """
    errors: list[str] = []
    dropped: list[str] = []
    unknown: list[str] = []
    try:
        unit_keys = [unit_key(u) for u in units]
    except ValueError as e:
        return False, [f"extraction unit identity error: {e}"], dropped, unknown, {}
    try:
        plan_keys = [plan_entry_key(p) for p in plan]
    except ValueError as e:
        return False, [f"plan entry identity error: {e}"], dropped, unknown, {}

    lane_count = lanes if lanes is not None else len(plan_keys)
    stats = {
        "units": len(unit_keys),
        "plan": len(plan_keys),
        "lanes": lane_count,
        "distinct_units": len(set(unit_keys)),
    }

    unit_set = set(unit_keys)
    plan_set = set(plan_keys)
    dropped = [k for k in unit_keys if k not in plan_set]
    unknown = [k for k in plan_keys if k not in unit_set]

    dupes = sorted({k for k in plan_keys if plan_keys.count(k) > 1})
    if dupes:
        errors.append(f"duplicate plan keys (one lane cannot own two units): {dupes}")

    if len(unit_keys) != lane_count:
        errors.append(
            f"UNIT/LANE MISMATCH: extraction holds {len(unit_keys)} units "
            f"({stats['distinct_units']} distinct) but the dispatch declares "
            f"{lane_count} lanes; firing is blocked"
        )
    elif stats["distinct_units"] != len(unit_keys):
        errors.append(
            f"extraction holds duplicate unit keys: {len(unit_keys)} units, "
            f"{stats['distinct_units']} distinct; the denominator is not countable"
        )
    if unknown:
        errors.append(f"plan keys absent from the extraction: {unknown}")

    return (not errors), errors, dropped, unknown, stats


def receipt_section(
    moment: str,
    units_path: Path,
    units_sha: str,
    stats: dict,
    errors: list[str],
    dropped: list[str],
    unknown: list[str],
) -> str:
    lines = [
        "",
        f"## fifty-wide guard {'PASS' if not errors else 'FAIL'} ({moment})",
        "",
        f"- units: {units_path} (sha256 {units_sha[:16]}...), {stats.get('units', 0)} units",
        f"- lanes: {stats.get('lanes', 0)}, plan entries: {stats.get('plan', 0)}",
    ]
    if errors:
        for e in errors:
            lines.append(f"- ERROR: {e}")
    if dropped:
        lines.append(f"- DROPPED UNITS ({len(dropped)} in extraction, absent from plan):")
        lines.extend(f"  - {k}" for k in dropped)
    if unknown:
        lines.append(f"- UNKNOWN PLAN KEYS ({len(unknown)}):")
        lines.extend(f"  - {k}" for k in unknown)
    if not errors and not dropped and not unknown:
        lines.append("- every extraction unit owns exactly one lane; counts meet")
    lines.append("")
    return "\n".join(lines)


def append_receipt(receipt_path: Path, section: str) -> str:
    """Append the guard section to the wave receipt. Returns "" or an error."""
    try:
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        with receipt_path.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(section)
        return ""
    except OSError as e:
        return f"receipt append failed: {receipt_path}: {type(e).__name__}: {e}"


def append_log(log_path: Path, row: dict) -> str:
    """Append one dispatch-log row (JSONL). Returns "" or an error."""
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        return ""
    except OSError as e:
        return f"dispatch log append failed: {log_path}: {type(e).__name__}: {e}"


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="fifty-wide wave pre-flight guard")
    parser.add_argument("--units", required=True, help="extraction artifact JSON list")
    parser.add_argument("--plan", required=True, help="dispatch plan JSON list")
    parser.add_argument("--lanes", type=int, default=None,
                        help="declared lane count; defaults to the plan length")
    parser.add_argument("--receipt", default=None,
                        help="wave receipt to append the guard section to")
    parser.add_argument("--wave", default=None,
                        help="wave slug stamped into the dispatch-log row; the join key "
                             "fifty_wide_archive.py --verify matches to close the replay pair")
    parser.add_argument("--log", default=None,
                        help=f"dispatch log JSONL (default {DEFAULT_LOG})")
    parser.add_argument("--no-log", action="store_true",
                        help="skip the dispatch-log row (test/dry use)")
    args = parser.parse_args(argv)

    moment = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    units_path = Path(args.units)
    plan_path = Path(args.plan)

    units, err = load_json_list(units_path, "units")
    if err:
        print(f"FIFTY-WIDE GUARD: CANNOT-VERIFY: {err}")
        return EXIT_CANNOT_VERIFY
    plan, err = load_json_list(plan_path, "plan")
    if err:
        print(f"FIFTY-WIDE GUARD: CANNOT-VERIFY: {err}")
        return EXIT_CANNOT_VERIFY

    ok, errors, dropped, unknown, stats = guard(units, plan, args.lanes)
    units_sha = sha256_of(units_path)

    if not ok:
        print("FIFTY-WIDE GUARD: FAIL")
        for e in errors:
            print(f"  {e}")
        if dropped:
            print(f"  dropped units ({len(dropped)}):")
            for k in dropped:
                print(f"    {k}")
        if args.receipt:
            rerr = append_receipt(
                Path(args.receipt),
                receipt_section(moment, units_path, units_sha, stats, errors, dropped, unknown),
            )
            if rerr:
                print(f"  {rerr}")
        return EXIT_FAIL

    print(
        f"FIFTY-WIDE GUARD: ok: {stats['units']} units == {stats['lanes']} lanes; "
        f"firing may proceed ({moment})"
    )
    if args.receipt:
        rerr = append_receipt(
            Path(args.receipt),
            receipt_section(moment, units_path, units_sha, stats, [], [], []),
        )
        if rerr:
            print(f"  {rerr}")
    if not args.no_log:
        key_digest = hashlib.sha256(
            "\n".join(unit_key(u) for u in units).encode("utf-8")
        ).hexdigest()
        row = {
            "moment": moment,
            "units": str(units_path),
            "units_sha256": units_sha,
            "unit_keys_sha256": key_digest,
            "units_count": stats["units"],
            "lanes": stats["lanes"],
            "plan_entries": stats["plan"],
            "guard": "fifty_wide_guard.py",
        }
        if args.wave:
            row["wave"] = args.wave
        lerr = append_log(Path(args.log) if args.log else DEFAULT_LOG, row)
        if lerr:
            print(f"  {lerr}")
            return EXIT_CANNOT_VERIFY
    return EXIT_PASS


if __name__ == "__main__":
    sys.exit(run())
