#!/usr/bin/env python3
"""gate_age_patrol.py - operator-gate age alarm, register-driven (Q40, 2026-10-01).

The disease this meters (watch/inbox/mountain_climb/FIFTY_QUESTIONS_ANSWERED.md
row Q40, grep evidence: "grep attention.md + queue/todo.md for gate-age rows on
Adam invite / Nous top-up / Phase-2 GO -> 0 hits (only closed Cerebras row
carried owed-since)"): an operator-only gate can stall indefinitely with no
alarm, because the row ABSENT from the tracking surfaces IS the answer - lanes
burn quota rediscovering a block the estate already paid to discover (the LW2
pattern). The sister tool tools/gate_digest.py (2026-09-30) renders open gates
at one glance but hardcodes them in Python and never alerts on age; this patrol
is the alarm layer: a JSON register (configs/gate_register.json) + an age bar.

Bar stated in numbers BEFORE reading anything:

  an OPEN register row is STALLED when its age in days exceeds the bar
  (default 14, --days flag). Age counts whole days from the row's `opened`
  ISO date to today. Decided rows never alarm (append-only estate law: the
  decided row IS the record). A same-day or young open gate is tolerable -
  operators sleep - so inside the bar is green, reported as evidence.

WARN-only (the fossil_check law shape): exit 1 signals the alarm and appends
one attention.md block per the estate alert convention; nothing is blocked,
no gate is closed, no register row is mutated by this tool. Enforce, and any
scheduling, are operator-gated.

NO-CRONS LAW: this lane wires NO schedule. The tool runs on demand. If the
operator wants it daily, the recipe is the census-patrol shape (a sibling of
scripts/census_patrol_daily.ps1 calling
`.venv\\Scripts\\python.exe tools\\gate_age_patrol.py >> logs/gate_age_patrol.log`
registered via the scripts/register_*_task.ps1 pattern) - an operator decision,
never a lane's.

No-fabrication law: every register row must cite a receipt that EXISTS on disk
and names the gate being opened. The patrol validates receipt existence and
fail-closes on its absence; whether the receipt truly names the gate is the
seeding lane's receipt-backed responsibility (see the register's seed_note).

Exit codes: 0 = every open gate inside the bar (or no open gates); 1 = one or
more open gates over the bar (WARN; attention row appended); 2 = cannot verify
(register unreadable, row shape invalid, fabricated-looking date, or a cited
receipt missing from disk).

Usage: python tools/gate_age_patrol.py [--root PATH] [--days N]
       [--register PATH] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parent.parent
REGISTER_RELPATH = "configs/gate_register.json"
ATTENTION_RELPATH = "memory/attention.md"

DEFAULT_THRESHOLD_DAYS = 14
VALID_STATUS = ("open", "decided")


class PatrolError(Exception):
    """Cannot-verify condition; main() maps this to exit 2."""


def load_register(path: Path) -> dict:
    """Read the register JSON. Raises PatrolError on unreadable/bad schema."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise PatrolError(f"register unreadable at {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise PatrolError(f"register is not valid JSON: {exc}") from exc
    if not isinstance(data, dict) or data.get("schema") != "gate_register.v1":
        raise PatrolError("register must be a JSON object with schema gate_register.v1")
    gates = data.get("gates")
    if not isinstance(gates, list) or not gates:
        raise PatrolError("register must carry a non-empty gates list")
    return data


def validate_row(row: dict, root: Path, index: int) -> dict:
    """Validate one register row against shape + disk. Fail-closed PatrolError.

    Enforced: required fields, status vocabulary, ISO dates, opened not in the
    future (fabrication smell, freshness_check.py convention), decided rows
    carry a decided date not before opened, and the cited source_receipt
    exists on disk (the no-fabrication teeth - a row without a real receipt
    file is a validation error, never a silent skip).
    """
    where = f"gates[{index}]"
    for field in ("slug", "name", "opened", "status", "source_receipt"):
        if not isinstance(row.get(field), str) or not row[field].strip():
            raise PatrolError(f"{where}: field '{field}' missing or not a non-empty string")
    if row["status"] not in VALID_STATUS:
        raise PatrolError(f"{where} ({row['slug']}): status must be one of {VALID_STATUS}, got {row['status']!r}")
    try:
        opened = date.fromisoformat(row["opened"])
    except ValueError as exc:
        raise PatrolError(f"{where} ({row['slug']}): opened is not an ISO date: {row['opened']!r}") from exc
    decided = None
    if row["status"] == "decided":
        raw = row.get("decided")
        if not isinstance(raw, str) or not raw.strip():
            raise PatrolError(f"{where} ({row['slug']}): decided row must carry a decided ISO date")
        try:
            decided = date.fromisoformat(raw)
        except ValueError as exc:
            raise PatrolError(f"{where} ({row['slug']}): decided is not an ISO date: {raw!r}") from exc
        if decided < opened:
            raise PatrolError(f"{where} ({row['slug']}): decided {decided} predates opened {opened}")
    receipt = root / row["source_receipt"]
    if not receipt.is_file():
        raise PatrolError(
            f"{where} ({row['slug']}): source_receipt not on disk: {row['source_receipt']} "
            "(no-fabrication law: every row must cite a real receipt; fix the row or land the receipt)"
        )
    return {"slug": row["slug"], "name": row["name"], "opened": opened,
            "decided": decided, "status": row["status"],
            "source_receipt": row["source_receipt"]}


def age_patrol(rows: list[dict], today: date,
               threshold_days: int = DEFAULT_THRESHOLD_DAYS) -> dict:
    """Pure verdict core. STALLED = any open row older than the bar.

    Age counts whole days from `opened` to `today`. A future-dated opened is
    a fabrication smell and fail-closes (exit 2), never negative-age silence.
    Decided rows are counted and reported, never alarmed (append-only law:
    the decided row is the closure record).
    """
    if threshold_days < 1:
        raise PatrolError(f"threshold must be >= 1 day, got {threshold_days}")
    open_rows = [r for r in rows if r["status"] == "open"]
    for row in rows:
        if row["opened"] > today:
            return {"ok": False, "verdict": "UNVERIFIABLE", "exit": 2,
                    "reason": f"gate {row['slug']} opened {row['opened']} is dated in the "
                              f"future (fabrication smell)"}
    stalled = []
    for row in open_rows:
        age = (today - row["opened"]).days
        if age > threshold_days:
            stalled.append({**row, "age_days": age})
    if stalled:
        detail = "; ".join(f"{r['slug']} {r['age_days']}d (bar {threshold_days}d, "
                           f"opened {r['opened'].isoformat()})" for r in stalled)
        return {"ok": False, "verdict": "STALLED", "exit": 1,
                "reason": f"{len(stalled)} open gate(s) over the bar: {detail}",
                "stalled": stalled}
    return {"ok": True, "verdict": "OK", "exit": 0,
            "reason": f"{len(open_rows)} open gate(s), all inside the {threshold_days}d bar; "
                      f"{len(rows) - len(open_rows)} decided row(s) on record"}


def alert_block(verdict: dict, today: date, threshold_days: int) -> tuple[str, str]:
    """Render the attention.md alert (estate convention) + its dedup key.

    Key shape mirrors the x-radar convention (`key: x-radar-holes ...`):
    one key line per patrol day, so repeated same-day runs append once.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    slugs = ",".join("+".join(r["slug"].split()) for r in verdict["stalled"])
    lines = [
        "",
        "---",
        "",
        f"### Gate-age patrol fired ({now})",
        "",
        f"- verdict: GATE-AGE: {verdict['verdict']} - {verdict['reason']} (exit {verdict['exit']})",
        "- register: configs/gate_register.json (append-only; this alert names rows, it never edits them)",
        "- response: decide the named gate(s) at the operator console, then flip each register row to",
        "  decided with a close-receipt citation in the SAME named edit that updates tools/gate_digest.py;",
        "  or raise the bar by name (--days) in the operator's own hand. WARN-only: nothing is blocked.",
        f"- key: gate-age {slugs} {today.isoformat()}",
        "",
    ]
    return "\n".join(lines), f"- key: gate-age {slugs} {today.isoformat()}"


def append_attention(attention_path: Path, block: str, key_line: str) -> bool:
    """Append the alert once per key (same-day dedup). Returns True if written."""
    existing = ""
    if attention_path.is_file():
        existing = attention_path.read_text(encoding="utf-8", errors="replace")
    if key_line in existing:
        return False
    with attention_path.open("a", encoding="utf-8", newline="\n") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(block)
    return True


def run(root: Path = ESTATE_ROOT, register_path: Path | None = None,
        attention_path: Path | None = None, threshold_days: int = DEFAULT_THRESHOLD_DAYS,
        today: date | None = None, write_attention: bool = True) -> int:
    """Gather bytes, validate, print the verdict, alert on WARN.

    Returns the process exit code. WARN is exit 1 with the attention append;
    cannot-verify returns exit 2 before any alert; green prints evidence rows
    and appends nothing (attention.md carries alerts, not OK receipts).
    """
    today = today or date.today()
    register_path = register_path or root / REGISTER_RELPATH
    attention_path = attention_path or root / ATTENTION_RELPATH
    try:
        data = load_register(register_path)
        rows = [validate_row(row, root, i) for i, row in enumerate(data["gates"])]
        verdict = age_patrol(rows, today, threshold_days)
    except PatrolError as exc:
        print(f"GATE-AGE: cannot verify, {exc}")
        return 2
    head = (f"{len(rows)} registered ({sum(1 for r in rows if r['status'] == 'open')} open / "
            f"{sum(1 for r in rows if r['status'] == 'decided')} decided), bar {threshold_days}d")
    print(f"GATE-AGE: {'ok' if verdict['ok'] else verdict['verdict'].lower()} - {head}")
    for row in rows:
        age = (today - row["opened"]).days
        state = row["status"].upper()
        tail = f", decided {row['decided'].isoformat()}" if row["decided"] else ""
        print(f"  {state:<7} {row['slug']} ({age}d since {row['opened'].isoformat()}{tail})")
        print(f"          receipt: {row['source_receipt']}")
    if verdict["ok"]:
        print(f"GATE-AGE: ok - {verdict['reason']}")
        return 0
    if verdict["exit"] == 2:
        print(f"GATE-AGE: {verdict['reason']}")
        return 2
    print(f"GATE-AGE: stalled - {verdict['reason']}")
    print("  Fix: the named gate(s) are operator-only decisions; decide them and flip the register")
    print("  rows to decided with close-receipt citations (append-only, never delete rows).")
    if not write_attention:
        print("  (dry-run: attention.md not appended)")
        return 1
    block, key_line = alert_block(verdict, today, threshold_days)
    try:
        wrote = append_attention(attention_path, block, key_line)
    except OSError as exc:
        print(f"GATE-AGE: cannot verify, attention append failed: {exc}")
        return 2
    if wrote:
        rel = attention_path.relative_to(root).as_posix() if attention_path.is_relative_to(root) \
            else str(attention_path)
        print(f"  alerted: appended gate-age row to {rel} (key line: {key_line.strip()})")
    else:
        print(f"  alerted: already present for today (dedup on key line), no double append")
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="operator-gate age alarm over configs/gate_register.json (Q40, WARN-only)")
    parser.add_argument("--root", type=Path, default=ESTATE_ROOT,
                        help="estate root holding the register, receipts and attention.md")
    parser.add_argument("--days", type=int, default=DEFAULT_THRESHOLD_DAYS,
                        help=f"age bar in days (default {DEFAULT_THRESHOLD_DAYS})")
    parser.add_argument("--register", type=Path, default=None,
                        help="override register path (default configs/gate_register.json under root)")
    parser.add_argument("--dry-run", action="store_true",
                        help="print the WARN without appending to memory/attention.md")
    args = parser.parse_args(argv)
    return run(args.root.resolve(), register_path=args.register, threshold_days=args.days,
               write_attention=not args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
