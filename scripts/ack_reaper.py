#!/usr/bin/env python3
"""ACK REAPER — Chair 3 burial fix (trailer wave lane T3, 2026-09-12).

Holds and alerts that sit past their TTL must SCREAM, not just exist.

Inputs (repo files are data):
  logs/failure_kb_alerts.jsonl      — fired alerts
  state/failure_kb_alerts_read.json — seen markers, key "<alert_ts>|<sig>" -> last-seen ISO
  state/*hold*.json                 — hold files with a ttl/created shape

Behavior:
  - alert due when its seen marker is missing OR older than --realert-hours (default 24)
  - hold due when now - created exceeds its ttl (unparseable hold = due, safest)
  - due items: LOUD stdout block + one row appended to watch/inbox/ACK_REAPER_QUEUE.md
  - after screaming, markers are advanced (alerts in the read file, holds in
    state/ack_reaper_holds.json) so a second run within the window is quiet (idempotent)
  - exit 0 ALWAYS — the reaper never breaks the cadence
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from glob import glob
from typing import Any

DEFAULT_REALERT_HOURS = 24.0
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


def _parse_ts(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _write_json_atomic(path: str, data: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, sort_keys=True)
    os.replace(tmp, path)


def _append_queue(path: str, now: datetime, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("# ACK REAPER QUEUE — un-acked alerts and over-TTL holds\n\n")
            fh.write("| reaped_at | kind | key | reason |\n|---|---|---|---|\n")
    with open(path, "a", encoding="utf-8") as fh:
        for r in rows:
            cells = (r.get("kind", "?"), r.get("key", "?"), r.get("reason", ""))
            fh.write("| %s | %s | %s | %s |\n" % (_iso(now), cells[0], cells[1], cells[2]))


def collect_due_alerts(alerts_log: str, read_file: str, now: datetime,
                       realert_hours: float) -> tuple[list[dict[str, str]], dict[str, str]]:
    """Returns (due list, {key: new_marker}) for every alert row in the log."""
    due: list[dict[str, str]] = []
    markers: dict[str, str] = {}
    try:
        seen = _load_json(read_file)
        if not isinstance(seen, dict):
            seen = {}
    except (OSError, ValueError):
        seen = {}
    cutoff = timedelta(hours=realert_hours)
    try:
        with open(alerts_log, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
    except OSError:
        lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if not isinstance(row, dict):
            continue
        key = "%s|%s" % (row.get("ts") or "?", row.get("sig") or "?")
        marker_ts = _parse_ts(seen.get(key))
        if marker_ts is None or (now - marker_ts) >= cutoff:
            age = "?"
            fired = _parse_ts(row.get("ts"))
            if fired:
                age = "%dh" % int((now - fired).total_seconds() // 3600)
            reason = "never-acked" if marker_ts is None else \
                "acked %dh ago > %gh re-alert window" % (
                    int((now - marker_ts).total_seconds() // 3600), realert_hours)
            due.append({"kind": "ALERT", "key": key,
                        "reason": "%s; type=%s count=%s sample=%r" % (
                            reason, row.get("type"), row.get("count"),
                            (row.get("sample") or "")[:80])})
            markers[key] = _iso(now)
    return due, markers


def _hold_times(path: str, blob: Any) -> tuple[datetime | None, float | None, str]:
    """Extract (created, ttl_hours, note) from a hold file, any reasonable shape."""
    if not isinstance(blob, dict):
        return None, None, "hold file is not a JSON object"
    created = None
    for k in ("created", "created_at", "ts", "placed_at"):
        created = _parse_ts(blob.get(k))
        if created:
            break
    ttl = None
    for k in ("ttl_hours", "ttl", "ttl_h"):
        v = blob.get(k)
        if isinstance(v, (int, float)) and v > 0:
            ttl = float(v)
            break
    if ttl is None:
        expires = None
        for k in ("expires", "expires_at", "expire_ts"):
            expires = _parse_ts(blob.get(k))
            if expires:
                break
        if expires and created:
            ttl = (expires - created).total_seconds() / 3600.0
    return created, ttl, ""


def collect_due_holds(state_dir: str, now: datetime,
                      realert_hours: float) -> tuple[list[dict[str, str]], dict[str, str]]:
    due: list[dict[str, str]] = []
    ledger: dict[str, str] = {}
    ledger_path = os.path.join(state_dir, "ack_reaper_holds.json")
    try:
        prev = _load_json(ledger_path)
        if not isinstance(prev, dict):
            prev = {}
    except (OSError, ValueError):
        prev = {}
    for path in sorted(glob(os.path.join(state_dir, "*hold*.json"))):
        if path.endswith("ack_reaper_holds.json"):
            continue
        name = os.path.basename(path)
        try:
            blob = _load_json(path)
            created, ttl, note = _hold_times(path, blob)
        except (OSError, ValueError):
            created, ttl, note = None, None, "hold file unreadable/invalid JSON"
        if created is None or ttl is None:
            last = _parse_ts(prev.get(name))
            re_screamed = last is not None and (now - last) < timedelta(hours=realert_hours)
            if not re_screamed:
                due.append({"kind": "HOLD", "key": name,
                            "reason": "over/unreadable ttl (%screated=%s ttl=%s)" % (
                                (note + "; ") if note else "", created, ttl)})
                ledger[name] = _iso(now)
            continue
        age_h = (now - created).total_seconds() / 3600.0
        last = _parse_ts(prev.get(name))
        re_screamed = last is not None and (now - last) < timedelta(hours=realert_hours)
        if age_h > ttl and not re_screamed:
            due.append({"kind": "HOLD", "key": name,
                        "reason": "age %gh > ttl %gh (placed %s)" % (
                            round(age_h, 1), ttl, _iso(created))})
            ledger[name] = _iso(now)
    return due, ledger


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="ack reaper — over-TTL alerts/holds SCREAM")
    ap.add_argument("--root", default=REPO, help="repo root (default: script's repo)")
    ap.add_argument("--realert-hours", type=float, default=DEFAULT_REALERT_HOURS)
    ap.add_argument("--now", default=None, help="override clock, ISO 8601 (tests)")
    ap.add_argument("--dry-run", action="store_true", help="scream but write nothing")
    args = ap.parse_args(argv)

    try:
        now = _parse_ts(args.now) or datetime.now(timezone.utc)
        state_dir = os.path.join(args.root, "state")
        alerts_log = os.path.join(args.root, "logs", "failure_kb_alerts.jsonl")
        read_file = os.path.join(state_dir, "failure_kb_alerts_read.json")
        queue = os.path.join(args.root, "watch", "inbox", "ACK_REAPER_QUEUE.md")

        due_alerts, alert_markers = collect_due_alerts(
            alerts_log, read_file, now, args.realert_hours)
        due_holds, hold_ledger = collect_due_holds(state_dir, now, args.realert_hours)
        due = due_alerts + due_holds

        if not due:
            print("[ack_reaper] quiet — nothing past its ack window. exit 0")
            return 0

        print("[ack_reaper] SCREAM — %d item(s) past their ack window:" % len(due))
        for item in due:
            print("  ** %s %s" % (item["kind"], item["key"]))
            print("     %s" % item["reason"])

        if not args.dry_run:
            _append_queue(queue, now, due)
            if alert_markers:
                try:
                    seen = _load_json(read_file)
                    if not isinstance(seen, dict):
                        seen = {}
                except (OSError, ValueError):
                    seen = {}
                seen.update(alert_markers)
                _write_json_atomic(read_file, seen)
            if hold_ledger:
                _write_json_atomic(os.path.join(state_dir, "ack_reaper_holds.json"),
                                   hold_ledger)
            print("[ack_reaper] %d row(s) appended to %s; markers advanced. exit 0"
                  % (len(due), os.path.relpath(queue, args.root)))
        else:
            print("[ack_reaper] dry-run: nothing written. exit 0")
    except Exception as exc:  # noqa: BLE001 — the reaper never breaks the cadence
        print("[ack_reaper] ERROR (swallowed, cadence preserved): %r. exit 0" % (exc,))
    return 0


if __name__ == "__main__":
    sys.exit(main())
