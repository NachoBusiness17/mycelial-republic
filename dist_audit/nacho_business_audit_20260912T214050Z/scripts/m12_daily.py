#!/usr/bin/env python3
"""M12 OPERATOR-LOAD BASELINE — Chair 2's missing organ.

The operator is the only unmetered organ in the fleet. This script probes
operator-activity signals from repo surfaces (probe, never self-report) and
writes ONE row per day to state/m12_baseline.jsonl:

  {date, steers_authored, git_commits_by_foste,
   hermes_jobs_operator_initiated, inbox_rows_pending, notes}

Idempotent: re-running on the same day UPDATES today's row (by date), never
duplicates. Rows are keyed on the local date; UTC date is also accepted when
matching signal timestamps (box clock skew tolerated).

Signals:
  steers_authored              watch/steers.jsonl rows with "operator" in the
                               authority field and today's date in ts
  git_commits_by_foste         git log --author=foste since local midnight
                               (null if git unavailable)
  hermes_jobs_operator_initiated  files in memory/runs/hermes_jobs/ touched today
  inbox_rows_pending           unresolved rows in memory/operator_inbox.json
                               (status == "pending"); falls back to
                               bridge/operator_inbox.jsonl OPEN/DEFERRED rows

Usage: python scripts/m12_daily.py [--date YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STEERS = REPO / "watch" / "steers.jsonl"
HERMES = REPO / "memory" / "runs" / "hermes_jobs"
INBOX_JSON = REPO / "memory" / "operator_inbox.json"
INBOX_JSONL = REPO / "bridge" / "operator_inbox.jsonl"
BASELINE = REPO / "state" / "m12_baseline.jsonl"


def today_dates() -> set[str]:
    """Local + UTC date strings for today (box clock skew tolerated)."""
    now = dt.datetime.now()
    return {now.strftime("%Y-%m-%d"), now.astimezone(dt.timezone.utc).strftime("%Y-%m-%d")}


def count_steers(days: set[str]) -> int:
    if not STEERS.exists():
        return 0
    n = 0
    for line in STEERS.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        auth = str(row.get("authority") or "")
        ts = str(row.get("ts") or "")
        if "operator" in auth.lower() and ts[:10] in days:
            n += 1
    return n


def count_git_commits(days: set[str]) -> int | None:
    since = min(days) + "T00:00:00"
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO), "log", "--author=foste",
             "--since=" + since, "--format=%H"],
            capture_output=True, text=True, timeout=30, check=True,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return sum(1 for ln in out.stdout.splitlines() if ln.strip())


def count_hermes(days: set[str]) -> int:
    if not HERMES.is_dir():
        return 0
    day_tokens = {d.replace("-", "") for d in days}
    midnight = dt.datetime.combine(dt.date.today(), dt.time.min).timestamp()
    n = 0
    for f in HERMES.iterdir():
        if not f.is_file():
            continue
        m = re.search(r"(\d{8})T", f.name)
        if m and m.group(1) in day_tokens:
            n += 1
        elif f.stat().st_mtime >= midnight:
            n += 1
    return n


def count_inbox_pending() -> int:
    # Primary organ: memory/operator_inbox.json (mag/operator_inbox.py semantics)
    try:
        data = json.loads(INBOX_JSON.read_text(encoding="utf-8", errors="replace"))
        committed = data.get("committed") if isinstance(data, dict) else None
        if committed is not None:
            return sum(1 for x in committed if isinstance(x, dict)
                       and x.get("status") == "pending")
    except (OSError, json.JSONDecodeError):
        pass
    # Fallback: bridge switchboard proposals (best-effort)
    try:
        n = 0
        for line in INBOX_JSONL.read_text(encoding="utf-8", errors="replace").splitlines():
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


def build_row(date_override: str | None) -> dict:
    days = today_dates()
    if date_override:
        days = {date_override}
    notes: list[str] = []
    git_n = count_git_commits(days)
    if git_n is None:
        notes.append("git=unavailable")
    return {
        "date": date_override or dt.date.today().isoformat(),
        "steers_authored": count_steers(days),
        "git_commits_by_foste": git_n,
        "hermes_jobs_operator_initiated": count_hermes(days),
        "inbox_rows_pending": count_inbox_pending(),
        "notes": "; ".join(notes),
    }


def write_row(row: dict) -> str:
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    existed = False
    if BASELINE.exists():
        for line in BASELINE.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("date") == row["date"]:
                existed = True  # today's row gets replaced, not duplicated
                continue
            rows.append(r)
    rows.append(row)
    tmp = BASELINE.with_suffix(".jsonl.tmp")
    tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                   encoding="utf-8")
    tmp.replace(BASELINE)
    return ("updated" if existed else "appended") + f" {row['date']}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None, help="override row date YYYY-MM-DD")
    args = ap.parse_args()
    row = build_row(args.date)
    action = write_row(row)
    print(json.dumps({"action": action, "row": row}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
