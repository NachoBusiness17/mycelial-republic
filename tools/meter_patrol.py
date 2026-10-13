#!/usr/bin/env python3
"""meter_patrol.py - dated witness meters for the institutional cluster (B2-469, 2026-09-26).

The disease this meters (watch/inbox/burn_wave_20260926/B2_166_rubric_scoring_20260926.md
Evidence 5, and the B2-24 carrier scan before it): both window-scored runs judged
the rubric's institutional items 1-4 with NO pulled source, so "no receipt" in the
archive was the only witness and a real event could sit outside the archive unseen.
A window scorer reading archive silence could not tell "someone looked and the
wires were quiet" from "nobody looked at all".

The organ: once a day (rides the MagCensusPatrolDaily scheduled task via
scripts/census_patrol_daily.ps1, the $0 daily surface that already exists) it
appends ONE dated row per meter class to watch/inbox/DATED_METERS.jsonl:

  state RECEIPT : at least one dated artifact under watch/inbox/ (modified in the
                  sweep window) byte-matches this class's boundary-true keyword
                  set. Pointers are CANDIDATES for a scorer to inspect, never a
                  HIT verdict; verdicts belong to the pre-registered rubric run.
  state NOBS    : no observation exists for this class in the sweep window. The
                  row says so explicitly (LAW-13, experiment-on-absence: name the
                  absence precisely), because archive silence is NOT evidence of
                  absence and must never again be the sole basis for a MISS.

Honesty bars:
  - No backfill, ever. Days before this organ's first run get no rows; a missed
    day is named as a GAP (exit 1, alert path in the cron script), never patched
    with invented rows (fabrication law).
  - Boundary-true matching only: the B2-166 sweep's "ebs"-inside-"website"
    substring disease is barred structurally (word-boundary / case-sensitive
    patterns below, regression-tested).
  - The sweep is archive-local by design and says so in every NOBS note: this
    organ witnesses the archive's witness state, it does not pull external wires.
    A NOBS streak is the scorer's signal to demand a wire pull, not a MISS.

Meter classes are frozen from the pre-registered cards (institutional cluster,
watch/inbox/WATER_WATCHLIST_20260921.json meter_hook; arms in
watch/inbox/WINDOW_2122_SCORING_RUBRIC_20260920.md). Changing a boundary is a
rubric amendment, not a tool edit: rows carry schema dated_meter_v1 so a boundary
change must ship a new schema version.

Idempotent per (date, meter_class): a rerun the same day tops up missing classes
and never duplicates rows.

Exit codes: 0 = rows current; 1 = GAP (a date since the ledger's last metered
day holds zero rows; today's rows are still written first); 2 = cannot verify
(missing inbox, unwritable ledger, unparsable existing row). Fail-closed: the
organ never guesses, never passes on a broken ledger.

Usage: python tools/meter_patrol.py [--root PATH] [--date YYYY-MM-DD] [--self-test]

The default run reads file bytes on disk only: no network, no keys, $0.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parent.parent
INBOX_RELPATH = Path("watch") / "inbox"
LEDGER_RELPATH = INBOX_RELPATH / "DATED_METERS.jsonl"
SCHEMA = "dated_meter_v1"
ORGAN = "meter_patrol"
MAX_SWEEP_BYTES = 5_000_000  # skip oversized files; a meter is not a corpus dig
MAX_POINTERS = 5
SWEEP_SUFFIXES = (".md", ".json", ".jsonl", ".txt")

# The institutional cluster: rubric items 1-4, pre-registered 2026-09-20/21.
# Case-sensitive tokens (EBS, MOEX) block the substring disease; lowercase
# phrases carry word boundaries for the same reason.
METERS: dict[str, dict] = {
    "g20_blackout_gt1m_6h": {
        "arm": "HIT 1: unscheduled G20 blackout/comms outage >1M customers and >6h",
        "patterns": [re.compile(r"\bblackout\b", re.IGNORECASE),
                     re.compile(r"\bpower outage\b", re.IGNORECASE),
                     re.compile(r"\bgrid failure\b", re.IGNORECASE),
                     re.compile(r"\binternet shutdown\b", re.IGNORECASE)],
    },
    "national_alert_nonweather": {
        "arm": "HIT 2: national non-weather, non-test emergency-alert activation",
        "patterns": [re.compile(r"\bEBS\b"),
                     re.compile(r"\bIPAWS\b"),
                     re.compile(r"\bemergency alert\b", re.IGNORECASE)],
    },
    "moex_xrp_halt": {
        "arm": "HIT 3: MOEX XRP futures launch halted or disrupted",
        "patterns": [re.compile(r"\bMOEX\b"),
                     re.compile(r"\bMoscow Exchange\b", re.IGNORECASE)],
    },
    "g20_circuit_breaker": {
        "arm": "HIT 4: G20 market-wide circuit breaker",
        "patterns": [re.compile(r"\bcircuit breaker\b", re.IGNORECASE),
                     re.compile(r"\btrading halt\b", re.IGNORECASE),
                     re.compile(r"\bmarket halt\b", re.IGNORECASE)],
    },
}


class MeterError(Exception):
    """Cannot-verify condition; main() maps this to exit 2."""


def row_is_todayish(row: dict) -> bool:
    """A ledger row this organ owns (schema + organ + class in the frozen set)."""
    return (row.get("schema") == SCHEMA and row.get("organ") == ORGAN
            and row.get("meter_class") in METERS)


def load_metered(ledger: Path) -> dict:
    """Existing (date, meter_class) pairs plus the max metered date.

    A row that parses as JSON but lacks the dated-meter shape is skipped as
    foreign (the ledger file is inbox-shared); a row that does not parse as
    JSON at all is cannot-verify (fail closed, never skip silently).
    """
    metered: set[tuple[str, str]] = set()
    max_day: date | None = None
    if not ledger.is_file():
        return {"pairs": metered, "max_day": max_day}
    for lineno, raw in enumerate(ledger.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise MeterError(f"{ledger.name} line {lineno} is not JSON: {exc}") from None
        if not isinstance(row, dict) or not row_is_todayish(row):
            continue
        day = row.get("date")
        if not isinstance(day, str):
            raise MeterError(f"{ledger.name} line {lineno} meter row has no date")
        try:
            date.fromisoformat(day)
        except ValueError:
            raise MeterError(f"{ledger.name} line {lineno} meter date unparsable: {day!r}") from None
        metered.add((day, row["meter_class"]))
        if max_day is None or day > max_day.isoformat():
            max_day = date.fromisoformat(day)
    return {"pairs": metered, "max_day": max_day}


def sweep_hits(root: Path, since: date, today: date) -> dict[str, list[str]]:
    """Boundary-true candidate pointers per class from inbox bytes.

    Sweep window: files whose mtime local date falls in (since, today]. The
    ledger itself is excluded (self-match guard). Case-sensitive tokens and
    word boundaries do the boundary-true work (the "website"/"ebs" disease).
    Pointers are repo-relative POSIX paths.
    """
    hits: dict[str, list[str]] = {cls: [] for cls in METERS}
    inbox = root / INBOX_RELPATH
    if not inbox.is_dir():
        raise MeterError(f"inbox missing: {inbox}")
    for path in sorted(inbox.rglob("*")):
        if not path.is_file() or path == inbox / LEDGER_RELPATH.name:
            continue
        if path.suffix.lower() not in SWEEP_SUFFIXES:
            continue
        try:
            mtime_day = date.fromtimestamp(path.stat().st_mtime)
        except OSError as exc:
            raise MeterError(f"cannot stat {path.name}: {exc}") from None
        if not (since < mtime_day <= today):
            continue
        if path.stat().st_size > MAX_SWEEP_BYTES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            raise MeterError(f"cannot read {path.name}: {exc}") from None
        rel = path.relative_to(root).as_posix()
        for cls, spec in METERS.items():
            if any(p.search(text) for p in spec["patterns"]):
                hits[cls].append(rel)
    return hits


def build_row(day: date, now_utc: str, cls: str, pointers: list[str]) -> dict:
    """One dated witness row. RECEIPT carries candidates; NOBS names the absence."""
    if pointers:
        return {
            "schema": SCHEMA, "ts": now_utc, "date": day.isoformat(),
            "organ": ORGAN, "meter_class": cls, "state": "RECEIPT",
            "pointers": pointers[:MAX_POINTERS], "pointer_count": len(pointers),
            "note": ("candidate pointers only, never a HIT verdict; scoring belongs "
                     "to the pre-registered rubric run"),
        }
    return {
        "schema": SCHEMA, "ts": now_utc, "date": day.isoformat(),
        "organ": ORGAN, "meter_class": cls, "state": "NOBS",
        "pointers": [], "pointer_count": 0,
        "note": ("no observation on file for this class in the sweep window; archive "
                 "silence is not evidence of absence (LAW-13); a NOBS streak demands "
                 "a wire pull before any window scoring cites this class"),
    }


def run(root: Path, today: date | None = None) -> int:
    """Gather bytes, write today's rows, report. Returns the process exit code."""
    today = today or date.today()
    inbox = root / INBOX_RELPATH
    ledger = root / LEDGER_RELPATH
    try:
        state = load_metered(ledger)
        hits = sweep_hits(root, state["max_day"] or (today - timedelta(days=1)), today)
    except MeterError as exc:
        print(f"METER-PATROL: cannot verify - {exc}")
        return 2
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows, new, existing = [], 0, 0
    for cls in METERS:
        if (today.isoformat(), cls) in state["pairs"]:
            existing += 1
            continue
        rows.append(build_row(today, now_utc, cls, hits[cls]))
        new += 1
    if rows:
        try:
            with ledger.open("a", encoding="utf-8", newline="") as f:
                for row in rows:
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
        except OSError as exc:
            print(f"METER-PATROL: cannot verify - ledger unwritable: {exc}")
            return 2
    print(f"METER-PATROL: ok - {today.isoformat()} rows current "
          f"({new} new, {existing} already metered) at {ledger.as_posix()}")
    exit_code = 0
    if state["max_day"] is not None:
        cursor = state["max_day"] + timedelta(days=1)
        gaps = []
        while cursor < today:
            if not any((cursor.isoformat(), cls) in state["pairs"] for cls in METERS):
                gaps.append(cursor.isoformat())
            cursor += timedelta(days=1)
        if gaps:
            print("METER-PATROL: GAP - no meter rows for: " + ", ".join(gaps))
            print("  Gap days are NOT backfilled (no fabrication): they hold no witness. "
                  "Decide whether they need a manual wire pull before window scoring cites them.")
            exit_code = 1
    for row in rows:
        head = row["state"]
        ptr = f" -> {row['pointer_count']} candidate(s)" if head == "RECEIPT" else ""
        print(f"  {row['date']} {row['meter_class']}: {head}{ptr}")
    return exit_code


def self_test() -> int:
    """Contract checks on synthetic bytes: boundary truth, states, idempotency,
    gap detection, fail-closed. Mirrors the census patrol self-test style."""
    import tempfile
    checks = 0
    # Boundary truth: "website" must never arm the EBS meter (B2-166 disease).
    hits = {cls: any(p.search("read it on the website") for p in s["patterns"])
            for cls, s in METERS.items()}
    assert not hits["national_alert_nonweather"], "substring disease: website matched EBS"
    checks += 1
    assert any(p.search("EBS alert") for p in METERS["national_alert_nonweather"]["patterns"])
    assert any(p.search("MOEX halted") for p in METERS["moex_xrp_halt"]["patterns"])
    assert not any(p.search("moex halted") for p in METERS["moex_xrp_halt"]["patterns"])
    checks += 1
    # Row shapes: RECEIPT carries pointers, NOBS names the absence.
    r = build_row(date(2026, 9, 26), "T", "moex_xrp_halt", ["watch/inbox/x.md"])
    n = build_row(date(2026, 9, 26), "T", "moex_xrp_halt", [])
    assert r["state"] == "RECEIPT" and r["pointers"] and "never a HIT verdict" in r["note"]
    assert n["state"] == "NOBS" and n["pointers"] == [] and "not evidence of absence" in n["note"]
    checks += 1
    # Idempotency + gap detection + fail-closed on a synthetic estate.
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / INBOX_RELPATH).mkdir(parents=True)
        (root / INBOX_RELPATH / "note.md").write_text("MOEX XRP futures halted today", encoding="utf-8")
        ledger = root / LEDGER_RELPATH
        assert run(root, today=date(2026, 9, 26)) == 0
        first = ledger.read_text(encoding="utf-8").splitlines()
        assert len(first) == 4, f"expected 4 rows, got {len(first)}"
        moex = [json.loads(x) for x in first if json.loads(x)["meter_class"] == "moex_xrp_halt"][0]
        assert moex["state"] == "RECEIPT" and moex["pointers"] == ["watch/inbox/note.md"]
        checks += 1
        assert run(root, today=date(2026, 9, 26)) == 0  # rerun: no duplicates
        assert len(ledger.read_text(encoding="utf-8").splitlines()) == 4
        checks += 1
        # A skipped day is named, never backfilled: 09-27 stays dark, the
        # 09-28 run writes its own rows and names the 09-27 gap (exit 1).
        assert run(root, today=date(2026, 9, 28)) == 1
        days = {json.loads(x)["date"] for x in ledger.read_text(encoding="utf-8").splitlines()}
        assert days == {"2026-09-26", "2026-09-28"}, "backfill happened (fabrication)"
        checks += 1
        # Fail-closed: a corrupted ledger line is exit 2, never a skip.
        ledger.write_text("{not json\n", encoding="utf-8")
        assert run(root, today=date(2026, 9, 28)) == 2
        checks += 1
    print(f"METER-PATROL: self-test ok ({checks} check groups)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="dated institutional-cluster meters (B2-469)")
    parser.add_argument("--root", type=Path, default=ESTATE_ROOT,
                        help="estate root holding watch/inbox (default: this repo)")
    parser.add_argument("--date", type=date.fromisoformat, default=None,
                        help="meter this ISO date instead of today (testing only)")
    parser.add_argument("--self-test", action="store_true", help="run the self-test and exit")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    return run(args.root.resolve(), today=args.date)


if __name__ == "__main__":
    sys.exit(main())
