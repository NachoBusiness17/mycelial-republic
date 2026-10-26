#!/usr/bin/env python3
"""x_radar_backfill.py - x_radar run-history census + HOLES stanza writer (Mickey17 W3, 2026-09-29).

The disease this heals (telemetry finding, watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md
return 24): the daily X recon (mag/x_reply_radar.py) went dark Sep 22-25 and NOTHING
rendered or alerted the gap; earlier, Sep 8-10 produced 0-byte raws under 402 "Grok
Build usage balance exhausted" errors. dashboards silently skip absent days.

What it does (idempotent, derived-data-only; re-run any time):

  1. CENSUS memory/runs/x_reply_radar/ per calendar day: out_*.json size (0 bytes =
     failed run), err_*.log content (402 text vs "(empty stderr)"), and watch/
     X_REPLY_RADAR_*.md corroboration matched by HEADER date, never filename (the
     20260906-named card is a daemon-import artifact: mag/x_reply_radar.py freezes
     CARD at module import, so its filename says 2026-09-06 while its content is the
     2026-09-11 run; header date is the truth).
  2. WRITE dashboard/static/x_radar_gaps.json - the durable per-day table + holes
     (each hole exactly {missing_dates, cause, first_seen, days}).
  3. INJECT a "HOLES" key into dashboard/static/x_radar.json (same hole stanzas) so
     the live sensor file itself renders the gap. Schema-safe: the file's contract
     is {threads, leaderboard, patterns} and no consumer rejects extra keys
     (estate_walk.html lists the path as a graph node only; tools/gap_sentinel.py
     reads top-level date fields ts/date/fetched_at/generated_at/generated/as_of/
     updated_at only - none added). WARNING: mag/x_reply_radar.py emit() rewrites
     x_radar.json wholesale every daily run, wiping HOLES; re-run this tool to
     re-inject (x_radar_gaps.json is the durable record and is never touched by
     emit()). That writer is NOT this lane's file to fix.
  4. FILE one idempotent attention alert (estate patrol block shape) documenting the
     holes. Idempotent by key, single-writer jsonl first (logs/x_radar_backfill/
     alerted.jsonl) + key-grep inside memory/attention.md, the B2-465 dual-survivor
     heal borrowed from tools/gap_sentinel.py. The key carries the hole origin
     (gap ranges), so a NEW hole re-alerts, a persistent one never re-files.

Exit codes: 0 = no holes; 1 = holes found (alert filed once per origin);
2 = cannot verify (runs dir absent/unreadable, or gaps file written but the
x_radar.json injection was skipped as unsafe - unparsable target).

Usage: python tools/x_radar_backfill.py [--root PATH] [--start YYYY-MM-DD]
       [--end YYYY-MM-DD] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RUNS_RELPATH = "memory/runs/x_reply_radar"
RADAR_RELPATH = "dashboard/static/x_radar.json"
GAPS_RELPATH = "dashboard/static/x_radar_gaps.json"
WATCH_GLOB = "X_REPLY_RADAR_*.md"
ATTENTION_RELPATH = "memory/attention.md"
ALERTED_RELPATH = "logs/x_radar_backfill/alerted.jsonl"

ERR_402_MARK = "402"
ERR_402_TEXT = ("402 Payment Required: Grok Build usage balance exhausted "
                "(grok CLI, err_*.log byte-witness)")

# Telemetry receipt that first named the Sep 22-25 silent hole (no same-day
# witness existed - that silence is the disease itself).
TELEMETRY_RECEIPT = "watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md (return 24)"
TELEMETRY_DATE = "2026-09-29"

PREHISTORY_NOTE = (
    "watch/X_REPLY_RADAR_20260906.md is a daemon-import artifact: mag/x_reply_radar.py "
    "freezes the card path at module import (2026-09-06) while header dates run daily; "
    "its surviving content is the 2026-09-11 run (mtime 2026-09-11 08:05). No raws "
    "survive for 09-06/09-07, so the census window opens at the first raw attempt "
    "2026-09-08. Days before that are witness-only prehistory, not counted holes."
)

HEADER_RE = re.compile(r"^# X REPLY RADAR - (\d{4}-\d{2}-\d{2})", re.M)


class CannotVerify(Exception):
    """Exit-2 condition: the census inputs are not there to read."""


def _days(start: date, end: date) -> list[date]:
    out, cur = [], start
    while cur <= end:
        out.append(cur)
        cur += timedelta(days=1)
    return out


def card_dates(watch_dir: Path) -> set[str]:
    """Header dates of every radar card. Header date is truth, filename is not."""
    seen: set[str] = set()
    if not watch_dir.is_dir():
        return seen
    for p in sorted(watch_dir.glob(WATCH_GLOB)):
        m = HEADER_RE.search(p.read_text(encoding="utf-8", errors="replace")[:200])
        if m:
            seen.add(m.group(1))
    return seen


def classify_err(text: str) -> str:
    if ERR_402_MARK in text and "balance exhausted" in text:
        return "402-balance-exhausted"
    return "empty"


def census(runs_dir: Path, watch_dir: Path, start: date | None, end: date) -> dict:
    """Per-day byte truth: out present/size, err log cause, card corroboration."""
    if not runs_dir.is_dir():
        raise CannotVerify(f"runs dir absent: {runs_dir.as_posix()}")
    cards = card_dates(watch_dir)
    outs: dict[str, int] = {}
    for p in runs_dir.glob("out_*.json"):
        m = re.match(r"out_(\d{4}-\d{2}-\d{2})\.json$", p.name)
        if m:
            outs[m.group(1)] = p.stat().st_size
    errs: dict[str, str] = {}
    for p in runs_dir.glob("err_*.log"):
        m = re.match(r"err_(\d{4}-\d{2}-\d{2})\.log$", p.name)
        if m:
            errs[m.group(1)] = classify_err(p.read_text(encoding="utf-8", errors="replace"))

    # Window opens at the first raw attempt on disk unless --start overrides.
    first_raw = min(outs) if outs else None
    win_start = start or (date.fromisoformat(first_raw) if first_raw else end)

    days = []
    for d in _days(win_start, end):
        ds = d.isoformat()
        size = outs.get(ds)
        err = errs.get(ds, "no-err-log")
        if size is None:
            status = "missing"          # writer never completed a subprocess return
        elif size == 0:
            status = "empty-raw"        # ran, grok returned nothing
        else:
            status = "ok"
        days.append({"date": ds, "out_bytes": size, "err": err,
                     "card": ds in cards, "status": status})
    return {"days": days, "cards_seen": sorted(cards)}


def build_holes(days: list[dict]) -> list[dict]:
    """Contiguous non-ok days -> one stanza per gap, exactly the W3 ask shape
    ({missing_dates, cause, first_seen} + a days helper)."""
    holes: list[dict] = []
    run: list[dict] = []
    for day in days + [{"status": "ok", "date": None}]:  # sentinel flushes the tail
        if day["status"] != "ok":
            run.append(day)
            continue
        if not run:
            continue
        dates = [d["date"] for d in run]
        errs = {d["err"] for d in run}
        if "missing" in {d["status"] for d in run}:
            # Zero artifacts at all: the writer never ran (no out, no err, no card).
            # No same-day witness existed - the telemetry receipt named it 2026-09-29.
            cause = ("writer never ran: zero artifacts (no out_*, no err_*, no card) "
                     f"on those days; no in-repo scheduler owns mag.x_reply_radar run; "
                     f"first named by {TELEMETRY_RECEIPT}")
            first_seen = TELEMETRY_DATE
        else:
            cause = ERR_402_TEXT
            for d in run:
                if d["err"] == "no-err-log":
                    cause += (f"; {d['date']} left a 0-byte raw with no surviving err "
                              "log (cause era-matched, not byte-proven for that day)")
            first_seen = next((d["date"] for d in run if d["err"] == "402-balance-exhausted"),
                              run[0]["date"])
        holes.append({"missing_dates": dates, "cause": cause,
                      "first_seen": first_seen, "days": len(dates)})
        run = []
    return holes


def write_gaps(gaps_path: Path, cov: dict, holes: list[dict], now: datetime) -> dict:
    days = cov["days"]
    ok = sum(1 for d in days if d["status"] == "ok")
    payload = {
        "schema": 1,
        "generated_at": now.isoformat(),
        "sensor": RADAR_RELPATH,
        "source_dir": RUNS_RELPATH,
        "method": ("out_YYYY-MM-DD.json byte size + err_YYYY-MM-DD.log content + "
                   "card HEADER-date match (filenames carry a daemon import-date artifact)"),
        "coverage": {
            "start": days[0]["date"] if days else None,
            "end": days[-1]["date"] if days else None,
            "days_expected": len(days),
            "days_ok": ok,
            "days_missing": len(days) - ok,
        },
        "days": days,
        "holes": holes,
        "prehistory": PREHISTORY_NOTE,
    }
    gaps_path.parent.mkdir(parents=True, exist_ok=True)
    gaps_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def inject_holes(radar_path: Path, holes: list[dict]) -> bool:
    """One-time-safe edit: add/replace top-level HOLES, preserve every other key.
    Returns False (and changes nothing) when the target is missing/unparsable."""
    if not radar_path.is_file():
        return False
    try:
        data = json.loads(radar_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    if not isinstance(data, dict):
        return False
    data["HOLES"] = holes
    radar_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return True


def alerted_keys(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    keys: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row.get("key"), str):
            keys.add(row["key"])
    return keys


def alert_block(stamp_local: str, holes: list[dict], key: str) -> str:
    spans = "; ".join(f"{h['missing_dates'][0]}..{h['missing_dates'][-1]} ({h['days']}d)"
                      for h in holes)
    return (
        "\n---\n\n"
        f"### X-radar hole census ({stamp_local})\n\n"
        f"- verdict: XRADAR-HOLES - dashboard/static/x_radar.json has unrendered gaps: "
        f"{spans}; causes and byte witnesses in dashboard/static/x_radar_gaps.json "
        f"(exit 1)\n"
        "- record: `logs/x_radar_backfill/alerted.jsonl` (single-writer truth; this "
        "attention.md block is best-effort per the B2-465 multi-writer law) + "
        "`tools/x_radar_backfill.py` census output\n"
        "- response: re-run `python tools/x_radar_backfill.py` to refresh "
        "x_radar_gaps.json and re-inject HOLES into x_radar.json (mag/x_reply_radar.py "
        "emit() wipes it every daily run); treat the Sep 22-25 window as never-sampled, "
        "not zero-engagement, in any trend read\n"
        f"- key: {key}\n"
    )


def file_alert(attention_p: Path, alerted_p: Path, holes: list[dict],
               key: str, now: datetime) -> bool:
    """Idempotent once per hole-origin (gap ranges live in the key)."""
    if key in alerted_keys(alerted_p):
        return False
    text = attention_p.read_text(encoding="utf-8", errors="replace") if attention_p.is_file() else ""
    if f"- key: {key}" in text:
        alerted_p.parent.mkdir(parents=True, exist_ok=True)
        with alerted_p.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"ts": now.isoformat(), "key": key, "healed": True}) + "\n")
        return False
    alerted_p.parent.mkdir(parents=True, exist_ok=True)
    with alerted_p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ts": now.isoformat(), "key": key}) + "\n")
    attention_p.parent.mkdir(parents=True, exist_ok=True)
    with attention_p.open("a", encoding="utf-8") as fh:
        fh.write(alert_block(now.astimezone().strftime("%Y-%m-%d %H:%M:%S"), holes, key))
    return True


def run(root: Path, start: date | None, end: date | None,
        dry_run: bool = False) -> int:
    now = datetime.now(timezone.utc)
    # Census end defaults to LOCAL today, not UTC: the estate's radar cadence is
    # 08:0x local, so just-past-midnight-UTC would frame the not-yet-run fresh
    # local day as a hole (a fabrication, not a silence).
    end = end or now.astimezone().date()
    runs_dir = root / RUNS_RELPATH
    try:
        cov = census(runs_dir, root / "watch", start, end)
    except CannotVerify as exc:
        print(f"XRADAR-BACKFILL: cannot verify, {exc}")
        return 2
    holes = build_holes(cov["days"])

    print(f"XRADAR-BACKFILL: census {cov['days'][0]['date']}..{cov['days'][-1]['date']} "
          f"({len(cov['days'])}d expected, "
          f"{sum(1 for d in cov['days'] if d['status'] == 'ok')} ok, {len(holes)} hole(s))")
    for d in cov["days"]:
        if d["status"] != "ok":
            print(f"  hole-day {d['date']} status={d['status']} out_bytes={d['out_bytes']} "
                  f"err={d['err']} card={d['card']}")

    if dry_run:
        print("XRADAR-BACKFILL: dry-run, nothing written")
        return 1 if holes else 0

    gaps_path = root / GAPS_RELPATH
    payload = write_gaps(gaps_path, cov, holes, now)
    radar_path = root / RADAR_RELPATH
    injected = inject_holes(radar_path, holes) if holes else True

    # Validate both JSONs parse (the W3 ask) straight off the disk bytes.
    for p in (gaps_path, radar_path):
        json.loads(p.read_text(encoding="utf-8"))
    print(f"XRADAR-BACKFILL: wrote {GAPS_RELPATH} (parses; "
          f"{payload['coverage']['days_expected']}d table) "
          f"+ HOLES {'injected into' if injected and holes else 'left out of'} "
          f"{RADAR_RELPATH} (parses)")

    if holes:
        key = "x-radar-holes " + "+".join(
            f"{h['missing_dates'][0]}..{h['missing_dates'][-1]}" for h in holes)
        filed = file_alert(root / ATTENTION_RELPATH, root / ALERTED_RELPATH, holes, key, now)
        print(f"XRADAR-BACKFILL: alert {'filed' if filed else 'already on file, not duplicated'} "
              f"key: {key}")
        if not injected:
            print(f"XRADAR-BACKFILL: cannot verify injection - {RADAR_RELPATH} unparsable; "
                  f"HOLES lives only in {GAPS_RELPATH}")
            return 2
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="x_radar run-history census + HOLES stanza writer")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--start", type=date.fromisoformat, default=None,
                        help="census window start (default: first out_*.json attempt on disk)")
    parser.add_argument("--end", type=date.fromisoformat, default=None,
                        help="census window end (default: today UTC)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    return run(args.root.resolve(), args.start, args.end, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
