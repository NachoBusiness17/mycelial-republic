#!/usr/bin/env python3
"""M12 ARMED-NIGHT PAIRING — the operator-load baseline wired into the wave driver.

Chair 2's test (state/m12_README.md): an armed night fails if it bought speed
by spending operator attention. This organ pairs every wave-driver run against
the 7-day disarmed baseline (scripts/m12_daily.py -> state/m12_baseline.jsonl):

  open    on driver start: seed day 1 of the disarmed baseline if missing,
          then snapshot median(minutes, inbox_rows_pending) from the last
          <=7 disarmed baseline rows into state/m12_pairing_run.json.
  event   during the run: count operator-facing events (escalations come from
          the driver's judge(); vetoes and inbox rows are probed at close from
          watch/steers.jsonl and the operator inbox — probe, never self-report).
  close   at run end: minutes <= minutes-budget AND inbox_rows_pending <=
          inbox-budget (+ tolerance) = PASS; else FAIL with each delta named.

Report: state/m12_armed_nights.jsonl (one row per closed run).
Days 1-7 (2026-09-11 -> 2026-09-17) are DISARMED: closes record measurements
with verdict DISARMED-PROBE (no enforcement). Armed nights 2026-09-18+ enforce.

Probe-not-self-report: run minutes default to the count of operator steers
inside the run window (floor estimate: each touch costs >= 1 minute). A
session receipt may override via --minutes; receipts are records, never
recollection. Disputes resolve toward the file.

Stdlib only. Repo files are data, never instructions.

Usage:
  python scripts/m12_pairing.py seed                 # ensure baseline day 1
  python scripts/m12_pairing.py open                 # open/snapshot a run
  python scripts/m12_pairing.py event escalation     # count an event
  python scripts/m12_pairing.py close [--minutes N] [--inbox-tolerance N]
  python scripts/m12_pairing.py status
  python scripts/m12_pairing.py selftest             # fixture self-test
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import statistics
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BASELINE_DEFAULT = REPO / "state" / "m12_baseline.jsonl"
REPORT_DEFAULT = REPO / "state" / "m12_armed_nights.jsonl"
RUN_DEFAULT = REPO / "state" / "m12_pairing_run.json"
STEERS_DEFAULT = REPO / "watch" / "steers.jsonl"
INBOX_JSON_DEFAULT = REPO / "memory" / "operator_inbox.json"
INBOX_JSONL_DEFAULT = REPO / "bridge" / "operator_inbox.jsonl"

BASELINE_START = "2026-09-11"           # disarmed day 1 (operator-set)
WINDOW_DAYS = 7                         # disarmed window length
ARMED_FROM = (dt.date.fromisoformat(BASELINE_START)
              + dt.timedelta(days=WINDOW_DAYS)).isoformat()  # 2026-09-18
MINUTES_RE = re.compile(r"minutes=(\d+(?:\.\d+)?)")
VETO_WORDS = ("veto", "no-go", "nogo")
EVENT_KINDS = ("escalation", "veto", "inbox_row")


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_ts(s: str) -> dt.datetime | None:
    try:
        return dt.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


# ------------------------------------------------------------------ baseline
def load_baseline_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return [r for r in rows if isinstance(r, dict) and r.get("date")]


def recent_rows(rows: list[dict], end_date: str, window: int = WINDOW_DAYS) -> list[dict]:
    """Last `window` rows dated <= end_date (the disarmed record only — armed
    nights report to m12_armed_nights.jsonl, never back into the baseline)."""
    dated = sorted((r for r in rows if str(r["date"]) <= end_date),
                   key=lambda r: r["date"])
    return dated[-window:]


def budgets(rows: list[dict]) -> dict:
    """median(minutes) from rows annotated minutes=N in notes; median(inbox)."""
    inbox_vals = [r.get("inbox_rows_pending") for r in rows
                  if isinstance(r.get("inbox_rows_pending"), (int, float))]
    minutes_vals = []
    for r in rows:
        m = MINUTES_RE.search(str(r.get("notes") or ""))
        if m:
            minutes_vals.append(float(m.group(1)))
    return {
        "days_used": len(rows),
        "dates": [r["date"] for r in rows],
        "minutes_median": statistics.median(minutes_vals) if minutes_vals else None,
        "inbox_median": statistics.median(inbox_vals) if inbox_vals else None,
    }


# ----------------------------------------------------------------- seeding
def ensure_day1(baseline_path: Path = BASELINE_DEFAULT,
                day: str = BASELINE_START) -> str:
    """Seed disarmed day 1 if not present. Idempotent. Canonical seeding
    delegates to scripts/m12_daily.py (same probe semantics, same file)."""
    rows = load_baseline_rows(baseline_path)
    if any(r.get("date") == day for r in rows):
        return "present"
    if baseline_path.resolve() != BASELINE_DEFAULT.resolve():
        # non-canonical path (fixture): write a minimal day row in place
        row = {"date": day, "steers_authored": 0, "git_commits_by_foste": None,
               "hermes_jobs_operator_initiated": 0, "inbox_rows_pending": 0,
               "notes": "seeded-by-m12_pairing (fixture path)"}
        with open(baseline_path, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        return "seeded"
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import m12_daily  # noqa: E402 — same-directory sibling
    m12_daily.write_row(m12_daily.build_row(day))
    return "seeded"


# ------------------------------------------------------------------- probes
def inbox_pending(inbox_json: Path = INBOX_JSON_DEFAULT,
                  inbox_jsonl: Path = INBOX_JSONL_DEFAULT) -> int:
    """Mirror of m12_daily.count_inbox_pending, parametrized for fixtures."""
    try:
        data = json.loads(inbox_json.read_text(encoding="utf-8", errors="replace"))
        committed = data.get("committed") if isinstance(data, dict) else None
        if committed is not None:
            return sum(1 for x in committed if isinstance(x, dict)
                       and x.get("status") == "pending")
    except (OSError, json.JSONDecodeError):
        pass
    try:
        n = 0
        for line in inbox_jsonl.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if str(row.get("status") or "").upper() in ("PENDING", "OPEN", "DEFERRED"):
                n += 1
        return n
    except OSError:
        return 0


def steers_between(steers_path: Path, start_ts: str, end_ts: str) -> dict:
    """Operator touches inside [start, end]: operator steers, and how many of
    them are vetoes (authority=operator + veto/no-go in the row text)."""
    start, end = _parse_ts(start_ts), _parse_ts(end_ts)
    out = {"operator_steers": 0, "vetoes": 0}
    if not steers_path.exists():
        return out
    for line in steers_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = _parse_ts(row.get("ts"))
        if ts is None or start is None or end is None:
            continue
        if not (start <= ts <= end):
            continue
        if "operator" not in str(row.get("authority") or "").lower():
            continue
        out["operator_steers"] += 1
        text = json.dumps(row, ensure_ascii=False).lower()
        if any(w in text for w in VETO_WORDS):
            out["vetoes"] += 1
    return out


# --------------------------------------------------------------- run state
def _load_run(run_path: Path) -> dict | None:
    if not run_path.exists():
        return None
    try:
        return json.loads(run_path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        return None


def _save_run(run_path: Path, run: dict) -> None:
    run_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = run_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(run, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(run_path)


def open_run(run_path: Path = RUN_DEFAULT, baseline_path: Path = BASELINE_DEFAULT,
             now: str | None = None) -> dict:
    """Open tonight's pairing run: seed day 1 if missing, snapshot budgets.
    A stale unclosed run from a previous date is closed as STALE_CLOSED first."""
    now = now or now_iso()
    existing = _load_run(run_path)
    if existing:
        if str(existing.get("date")) == now[:10]:
            return existing  # reattach to tonight's run
        close_run(run_path=run_path, verdict_override="STALE_CLOSED",
                  reason_override=f"run opened {existing.get('opened_ts')} was never closed; "
                                  f"closed by next open at {now}")
    ensure_day1(baseline_path)
    today = now[:10]
    bud = budgets(recent_rows(load_baseline_rows(baseline_path), today))
    run = {
        "run_id": f"M12-{today}-{now[11:13]}{now[14:16]}Z",
        "opened_ts": now,
        "date": today,
        "baseline_path": str(baseline_path),
        "budgets": bud,
        "events": {"escalations": 0, "vetoes": 0, "inbox_rows": 0},
    }
    _save_run(run_path, run)
    return run


def ensure_run(run_path: Path = RUN_DEFAULT,
               baseline_path: Path = BASELINE_DEFAULT) -> dict:
    """Driver-start hook: open if absent, reattach if tonight's run is live."""
    run = _load_run(run_path)
    if run and str(run.get("date")) == now_iso()[:10]:
        return run
    return open_run(run_path=run_path, baseline_path=baseline_path)


def note_event(kind: str, n: int = 1, run_path: Path = RUN_DEFAULT) -> dict:
    """Count an operator-facing event into the live run (driver hook)."""
    if kind not in EVENT_KINDS:
        raise ValueError(f"unknown event kind: {kind}")
    run = _load_run(run_path)
    if run is None:
        run = open_run(run_path=run_path)
    key = kind + "s"  # escalation(s) / veto(es) / inbox_row(s)
    run["events"][key] = int(run["events"].get(key, 0)) + n
    _save_run(run_path, run)
    return run


# ------------------------------------------------------------------- close
def close_run(run_path: Path = RUN_DEFAULT, report_path: Path = REPORT_DEFAULT,
              steers_path: Path = STEERS_DEFAULT,
              inbox_json: Path = INBOX_JSON_DEFAULT,
              inbox_jsonl: Path = INBOX_JSONL_DEFAULT,
              minutes_override: float | None = None,
              inbox_tolerance: float = 0.0,
              verdict_override: str | None = None,
              reason_override: str | None = None,
              closed_ts: str | None = None) -> dict:
    """Close the run, pair against the snapshot budgets, append the report row.
    PASS  = minutes <= minutes-budget AND inbox <= inbox-budget (+ tolerance).
    FAIL  = otherwise, with every delta named in `reason`."""
    run = _load_run(run_path)
    if run is None:
        raise SystemExit("no live pairing run to close (m12_pairing_run.json missing)")
    closed_ts = closed_ts or now_iso()
    touched = steers_between(steers_path, run["opened_ts"], closed_ts)
    minutes = (float(minutes_override) if minutes_override is not None
               else float(touched["operator_steers"]))
    minutes_method = ("receipt-override" if minutes_override is not None
                      else "probe: operator steers in window (floor, each touch >=1 min)")
    inbox_rows = inbox_pending(inbox_json, inbox_jsonl)
    bud = run.get("budgets") or {}
    mb, ib = bud.get("minutes_median"), bud.get("inbox_median")
    minutes_delta = None if mb is None else round(minutes - float(mb), 2)
    inbox_delta = None if ib is None else round(inbox_rows - float(ib), 2)

    if verdict_override:
        verdict, reason = verdict_override, (reason_override or "")
    elif mb is None and ib is None:
        verdict = "UNPROVEN"
        reason = "no disarmed baseline rows on record — nothing to pair against"
    elif str(run.get("date")) < ARMED_FROM:
        verdict = "DISARMED-PROBE"
        reason = (f"disarmed window ({BASELINE_START} -> {ARMED_FROM}): measurement only; "
                  f"minutes {minutes:g} vs budget {mb}, inbox {inbox_rows} vs budget {ib}")
    else:
        fails = []
        if mb is not None and minutes > float(mb):
            fails.append(f"minutes {minutes:g} exceeds budget {mb:g} by +{minutes_delta:g}")
        if ib is not None and inbox_rows > float(ib) + float(inbox_tolerance):
            tol = f" (tolerance {inbox_tolerance:g})" if inbox_tolerance else ""
            fails.append(f"inbox rows {inbox_rows} exceed budget {ib:g}{tol} "
                         f"by +{inbox_delta:g}")
        verdict = "FAIL" if fails else "PASS"
        reason = ("; ".join(fails) if fails else
                  f"minutes {minutes:g} <= {mb:g}; inbox {inbox_rows} <= {ib:g}")

    row = {
        "run_id": run.get("run_id"), "night": run.get("date"),
        "opened_ts": run.get("opened_ts"), "closed_ts": closed_ts,
        "minutes": minutes, "minutes_method": minutes_method,
        "minutes_budget": mb, "minutes_delta": minutes_delta,
        "inbox_rows": inbox_rows, "inbox_budget": ib, "inbox_delta": inbox_delta,
        "escalations": int((run.get("events") or {}).get("escalations", 0)),
        "vetoes_counted": int((run.get("events") or {}).get("vetoes", 0)),
        "vetoes_probed": touched["vetoes"], "operator_steers": touched["operator_steers"],
        "days_used": bud.get("days_used"), "baseline_dates": bud.get("dates"),
        "verdict": verdict, "reason": reason,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    run_path.unlink(missing_ok=True)
    return row


# ---------------------------------------------------------------------- CLI
def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(description="M12 armed-night pairing")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("seed")
    sub.add_parser("open")
    sub.add_parser("status")
    sub.add_parser("selftest")
    pe = sub.add_parser("event")
    pe.add_argument("kind", choices=EVENT_KINDS)
    pe.add_argument("--n", type=int, default=1)
    pc = sub.add_parser("close")
    pc.add_argument("--minutes", type=float, default=None,
                    help="session-receipt override for run minutes (probe is the default)")
    pc.add_argument("--inbox-tolerance", type=float, default=0.0,
                    help="inbox budget tolerance (needs the operator's number)")
    args = ap.parse_args()

    if args.cmd == "seed":
        print(f"{ensure_day1()} {BASELINE_START}")
    elif args.cmd == "open":
        print(json.dumps(open_run(), ensure_ascii=False))
    elif args.cmd == "status":
        run = _load_run(RUN_DEFAULT)
        print(json.dumps(run or {"note": "no live run"}, ensure_ascii=False))
    elif args.cmd == "event":
        print(json.dumps(note_event(args.kind, args.n), ensure_ascii=False))
    elif args.cmd == "close":
        print(json.dumps(close_run(minutes_override=args.minutes,
                                   inbox_tolerance=args.inbox_tolerance),
                         ensure_ascii=False))
    elif args.cmd == "selftest":
        return selftest()
    return 0


# ----------------------------------------------------------------- selftest
def selftest() -> int:
    """Fixture self-test: synthetic baseline/steers/inbox in a tempdir; proves
    budget math, PASS, FAIL-with-named-delta, seeding idempotence, window filter."""
    checks: list[tuple[str, bool]] = []

    def check(name: str, cond: bool) -> None:
        checks.append((name, bool(cond)))
        print(f"[{'PASS' if cond else 'FAIL'}] {name}")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        base, steers = root / "baseline.jsonl", root / "steers.jsonl"
        inbox_json, report, run_path = root / "inbox.json", root / "report.jsonl", root / "run.json"

        # fixture baseline: 7 disarmed days 09-05..09-11 (09-11 IS day 1,
        # pre-seeded exactly like the real baseline before the first armed open);
        # minutes median 4, inbox median 2
        mins = [2, 4, 4, 4, 5, 5, 7]
        inbx = [1, 2, 2, 2, 3, 3, 9]
        with open(base, "w", encoding="utf-8", newline="\n") as fh:
            for i, (m, n) in enumerate(zip(mins, inbx)):
                d = (dt.date(2026, 9, 5) + dt.timedelta(days=i)).isoformat()
                fh.write(json.dumps({"date": d, "inbox_rows_pending": n,
                                     "notes": f"minutes={m}"}) + "\n")

        # fixture steers: 1 operator veto IN window, 1 operator steer OUT, 1 seat steer IN
        with open(steers, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps({"id": "s1", "ts": "2026-09-18T02:00:00Z",
                                 "authority": "operator", "note": "VETO: no-go on lane 3"}) + "\n")
            fh.write(json.dumps({"id": "s2", "ts": "2026-09-18T23:00:00Z",
                                 "authority": "operator", "note": "later, outside window"}) + "\n")
            fh.write(json.dumps({"id": "s3", "ts": "2026-09-18T03:00:00Z",
                                 "authority": "seat-x", "note": "not the operator"}) + "\n")
        with open(inbox_json, "w", encoding="utf-8") as fh:
            json.dump({"committed": [{"status": "pending"}, {"status": "pending"},
                                     {"status": "done"}]}, fh)

        # 1. budget snapshot
        run = open_run(run_path=run_path, baseline_path=base,
                       now="2026-09-18T01:00:00Z")
        b = run["budgets"]
        check("budget snapshot: minutes median 4", b["minutes_median"] == 4)
        check("budget snapshot: inbox median 2", b["inbox_median"] == 2)
        check("budget snapshot: 7 disarmed days used", b["days_used"] == 7)

        # 2. event counting
        note_event("escalation", 2, run_path=run_path)
        check("event counting: 2 escalations",
              _load_run(run_path)["events"]["escalations"] == 2)

        # 3. window probe: only the in-window operator veto counts
        probe = steers_between(steers, "2026-09-18T01:00:00Z", "2026-09-18T09:00:00Z")
        check("window probe: 1 operator steer in window",
              probe["operator_steers"] == 1)
        check("window probe: veto recognized", probe["vetoes"] == 1)

        # 4. PASS close (armed night): minutes 1 <= 4, inbox 2 <= 2
        row = close_run(run_path=run_path, report_path=report, steers_path=steers,
                        inbox_json=inbox_json, inbox_jsonl=root / "none.jsonl",
                        closed_ts="2026-09-18T09:00:00Z")
        check("armed PASS verdict", row["verdict"] == "PASS")
        check("armed PASS: no deltas over budget",
              row["minutes_delta"] == -3 and row["inbox_delta"] == 0)
        check("close clears the run state", not run_path.exists())

        # 5. FAIL close names the deltas (receipt override 9 min, inbox 5 pending)
        with open(inbox_json, "w", encoding="utf-8") as fh:
            json.dump({"committed": [{"status": "pending"} for _ in range(5)]}, fh)
        open_run(run_path=run_path, baseline_path=base, now="2026-09-18T10:00:00Z")
        row = close_run(run_path=run_path, report_path=report, steers_path=steers,
                        inbox_json=inbox_json, inbox_jsonl=root / "none.jsonl",
                        minutes_override=9, closed_ts="2026-09-18T11:00:00Z")
        check("armed FAIL verdict", row["verdict"] == "FAIL")
        check("FAIL names minutes delta +5",
              "minutes 9 exceeds budget 4 by +5" in row["reason"])
        check("FAIL names inbox delta +3",
              "inbox rows 5 exceed budget 2 by +3" in row["reason"])

        # 6. disarmed day (today, 09-11) records a probe, never enforces
        open_run(run_path=run_path, baseline_path=base, now="2026-09-11T22:00:00Z")
        row = close_run(run_path=run_path, report_path=report, steers_path=steers,
                        inbox_json=inbox_json, inbox_jsonl=root / "none.jsonl",
                        minutes_override=1, closed_ts="2026-09-11T23:00:00Z")
        check("disarmed day -> DISARMED-PROBE (no enforcement)",
              row["verdict"] == "DISARMED-PROBE")

        # 7. report file: one row per close
        n_rows = sum(1 for ln in report.read_text(encoding="utf-8").splitlines() if ln.strip())
        check("report: 3 rows for 3 closes", n_rows == 3)

        # 8. re-open seeds day 1 idempotently (present, no duplicate)
        check("day-1 seeding: already present",
              ensure_day1(base, "2026-09-11") == "present")
        lines = [ln for ln in base.read_text(encoding="utf-8").splitlines() if ln.strip()]
        check("baseline unchanged after reseed check", len(lines) == 7)

    failed = [n for n, ok in checks if not ok]
    print(f"\nselftest: {len(checks) - len(failed)}/{len(checks)} checks passed"
          + (f"; FAILED: {failed}" if failed else " — all green"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
