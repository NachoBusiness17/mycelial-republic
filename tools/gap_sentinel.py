#!/usr/bin/env python3
"""gap_sentinel.py - estate metabolism gap sentinel (Mickey17 wave 3, 2026-09-29).

The disease this meters (watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md return 24,
telemetry lane): rollup snapshots land in dashboard/static/index_data/ every index
run and NOTHING ever diffs two of them (estate metabolism does not exist), and
sensors go silent for days unalerted (x_radar.json dark Sep 22-25; byte witness:
memory/runs/x_reply_radar/ err_*.log jumps 2026-09-21 straight to 2026-09-26).

Bar stated in numbers BEFORE reading anything:

  GROWTH: between two consecutive rollup runs, a project is flagged when its
  bytes/day growth exceeds the bar (default 1.0 GiB/day, sized to the 1.1GB
  kpi.jsonl zero-reader class). Windows shorter than MIN_WINDOW_DAYS (0.25d)
  are evidence only, never a flag: two runs inside hours make bytes/day explode
  without any disease (the census patrol's same-window law, B2-215).
  SILENCE: a watched sensor is flagged when its newest byte is older than the
  bar (default 2.0 days). Byte-truth order: an embedded top-level date field
  when the writer stamps one, else file mtime. x_radar.json stamps none (its
  keys are threads/leaderboard/patterns; mag/x_reply_radar.py emit() writes no
  date), so mtime is its truth and the verdict names the source. A sensor file
  gone missing entirely is a deeper silence and flags as SENSOR-MISSING.

Fail-closed by construction: a missing or unparsable rollup.json, last_run.json
or history row is exit 2, never a guess. A first run with no prior snapshot is
baseline-only (exit 0): the estate overwrote rollup.json every run and kept no
history, which IS the disease; logs/gap_sentinel/history.jsonl (one row per
rollup run, keyed on the last_run ts) is the fix going forward.

Alerts: memory/attention.md blocks in the estate patrol shape (### Gap sentinel
fired (stamp) + verdict/record/response bullets, shape matched to the census
patrol and FTS daily blocks already living in that file, read before writing).
Idempotent by key: every alert lands FIRST in logs/gap_sentinel/alerted.jsonl
(single writer: this tool; the B2-465 fts law, because attention.md is a hot
multi-writer file where best-effort appends lose bytes), and the key bullet is
also grepped inside attention.md, so a lost jsonl row does not double-file a
surviving block and a lost block does not double-file a surviving row (either
survivor heals the jsonl). A persistent gap stays exit 1 but never re-files:
the key carries the gap's origin (growth window, or the stale stamp), so the
alert refires only when a NEW gap origin appears.

Exit codes: 0 = no gaps; 1 = gaps found (alert filed once per key); 2 = cannot
verify. Usage: python tools/gap_sentinel.py [--root PATH] [--growth-gib N]
[--silence-days N] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parent.parent

GIB = 1024 ** 3
DEFAULT_GROWTH_GIB = 1.0
DEFAULT_SILENCE_DAYS = 2.0
MIN_WINDOW_DAYS = 0.25

ROLLUP_RELPATH = "dashboard/static/index_data/rollup.json"
LASTRUN_RELPATH = "dashboard/static/index_data/last_run.json"
HISTORY_RELPATH = "logs/gap_sentinel/history.jsonl"
ALERTED_RELPATH = "logs/gap_sentinel/alerted.jsonl"
RUNLOG_RELPATH = "logs/gap_sentinel/run.log"
ATTENTION_RELPATH = "memory/attention.md"

# Every watched sensor inherits gap detection free (the return 24 ask): add a
# row, get silence metering.
SENSORS = (
    "dashboard/static/x_radar.json",
)
# Top-level fields accepted as an embedded content date when a writer stamps
# one (fresher truth than mtime for writers that rewrite in place).
DATE_FIELDS = ("ts", "date", "fetched_at", "generated_at", "generated", "as_of", "updated_at")


class SentinelError(Exception):
    """Cannot-verify condition; run() maps this to exit 2."""


def parse_iso(raw: str) -> datetime:
    """ISO-8601 to aware UTC datetime; SentinelError on garbage (fail-closed)."""
    try:
        stamp = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise SentinelError(f"unparsable timestamp {raw!r}: {exc}") from exc
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    return stamp.astimezone(timezone.utc)


def load_snapshot(root: Path) -> dict:
    """rollup.json + last_run.json -> {"ts", "total_bytes", "projects": name -> bytes}."""
    rollup_p = root / ROLLUP_RELPATH
    lastrun_p = root / LASTRUN_RELPATH
    for p in (rollup_p, lastrun_p):
        if not p.is_file():
            raise SentinelError(f"missing input: {p.relative_to(root).as_posix()}")
    try:
        rollup = json.loads(rollup_p.read_text(encoding="utf-8"))
        lastrun = json.loads(lastrun_p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SentinelError(f"unparsable input: {exc}") from exc
    if not isinstance(rollup, dict) or not isinstance(lastrun.get("ts"), str):
        raise SentinelError("rollup.json/last_run.json shape is not the snapshot contract")
    projects: dict[str, int] = {}
    for name, row in rollup.items():
        if isinstance(row, dict) and isinstance(row.get("bytes"), int):
            projects[name] = row["bytes"]
    return {
        "ts": parse_iso(lastrun["ts"]),
        "total_bytes": lastrun.get("total_bytes") if isinstance(lastrun.get("total_bytes"), int)
        else sum(projects.values()),
        "projects": projects,
    }


def load_history(path: Path) -> list[dict]:
    """history.jsonl rows oldest-first, ts_dt added. Unparsable row = exit-2 disease."""
    if not path.is_file():
        return []
    rows: list[dict] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SentinelError(f"history row {i} unparsable: {exc}") from exc
        if not isinstance(row.get("ts"), str) or not isinstance(row.get("projects"), dict):
            raise SentinelError(f"history row {i} is not the snapshot contract")
        row["ts_dt"] = parse_iso(row["ts"])
        rows.append(row)
    rows.sort(key=lambda r: r["ts_dt"])
    return rows


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def record_snapshot(history: list[dict], snap: dict, path: Path) -> bool:
    """Append the snapshot when its rollup-run ts is unseen (dedupe on ts)."""
    if any(r["ts_dt"] == snap["ts"] for r in history):
        return False
    append_jsonl(path, {"ts": snap["ts"].isoformat(), "total_bytes": snap["total_bytes"],
                        "projects": snap["projects"]})
    return True


def compute_growth(prev: dict, cur: dict) -> dict:
    """Pure diff of two snapshots -> window days + per-project bytes/day rows."""
    days = (cur["ts_dt"] - prev["ts_dt"]).total_seconds() / 86400.0
    names = sorted(set(prev["projects"]) | set(cur["projects"]))
    rows = []
    for name in names:
        delta = cur["projects"].get(name, 0) - prev["projects"].get(name, 0)
        per_day = (delta / days) if days > 0 else (float("inf") if delta > 0 else 0.0)
        rows.append({"project": name, "bytes_delta": delta, "bytes_per_day": per_day})
    return {"days": days, "rows": rows, "total_delta": cur["total_bytes"] - prev["total_bytes"]}


def growth_flags(growth: dict, bar_bytes: float) -> list[dict]:
    """Projects over the bar. Sub-MIN_WINDOW_DAYS windows flag nothing."""
    if growth["days"] < MIN_WINDOW_DAYS:
        return []
    return [r for r in growth["rows"] if r["bytes_per_day"] > bar_bytes]


def gib(n: float) -> str:
    return f"{n / GIB:.2f} GiB"


def sensor_freshness(path: Path, now: datetime, max_age_days: float) -> dict:
    """Newest byte truth for one sensor: embedded date field when stamped, else mtime."""
    if not path.is_file():
        return {"ok": False, "missing": True, "source": "absent", "age_days": None, "stamp": None}
    stamp = None
    source = "mtime"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        data = None
    if isinstance(data, dict):
        for field in DATE_FIELDS:
            if isinstance(data.get(field), str):
                try:
                    stamp = parse_iso(data[field])
                except SentinelError:
                    stamp = None
                if stamp is not None:
                    source = f"field:{field}"
                    break
    if stamp is None:
        stamp = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    age_days = (now - stamp).total_seconds() / 86400.0
    ok = 0.0 <= age_days <= max_age_days  # negative age = future stamp, fabrication smell
    return {"ok": ok, "missing": False, "source": source, "age_days": age_days, "stamp": stamp}


def alerted_keys(path: Path) -> set[str]:
    """Keys already filed. An unparsable alerted row proves nothing, so it is
    skipped and the alert re-files (duplicate block, never a lost alert)."""
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


def file_alert(attention_p: Path, alerted_p: Path, key: str, block: str, now: datetime) -> bool:
    """Idempotent alert: jsonl record first (single writer), attention.md second
    (best-effort, B2-465 multi-writer law). True only when newly filed."""
    if key in alerted_keys(alerted_p):
        return False
    text = attention_p.read_text(encoding="utf-8", errors="replace") if attention_p.is_file() else ""
    if f"- key: {key}" in text:
        append_jsonl(alerted_p, {"ts": now.isoformat(), "key": key, "healed": True})
        return False
    append_jsonl(alerted_p, {"ts": now.isoformat(), "key": key})
    attention_p.parent.mkdir(parents=True, exist_ok=True)
    with attention_p.open("a", encoding="utf-8") as fh:
        fh.write(block)
    return True


def alert_block(stamp_local: str, verdict: str, response: str, key: str) -> str:
    """Estate patrol shape: matched to the census/FTS blocks in memory/attention.md."""
    return (
        "\n---\n\n"
        f"### Gap sentinel fired ({stamp_local})\n\n"
        f"- verdict: {verdict} (exit 1)\n"
        "- record: `logs/gap_sentinel/alerted.jsonl` (single-writer truth; this "
        "attention.md block is best-effort per the B2-465 multi-writer law)\n"
        f"- response: {response}\n"
        f"- key: {key}\n"
    )


GROWTH_RESPONSE = (
    "the named projects grew past the bytes/day bar between consecutive rollup runs; "
    "find WHAT grew (the 1.1GB kpi.jsonl zero-reader class) before trusting any "
    "size-derived metric."
)
SILENCE_RESPONSE = (
    "the sensor wrote nothing newer than its stamp; the Sep 22-25 x_radar hole looked "
    "exactly like this and nothing alerted. Restart or inspect the writer that owns "
    "the sensor (mag/x_reply_radar.py for x_radar.json) and treat every dashboard it "
    "feeds as stale until it writes again."
)


def run(root: Path, growth_bytes: float = DEFAULT_GROWTH_GIB * GIB,
        silence_days: float = DEFAULT_SILENCE_DAYS, dry_run: bool = False,
        now: datetime | None = None) -> int:
    """One sentinel pass. Returns the process exit code (0 ok, 1 gaps, 2 cannot verify)."""
    now = now or datetime.now(timezone.utc)
    try:
        snap = load_snapshot(root)
        history = load_history(root / HISTORY_RELPATH)
    except SentinelError as exc:
        print(f"GAP-SENTINEL: cannot verify, {exc}")
        return 2
    prev = next((r for r in reversed(history) if r["ts_dt"] != snap["ts"]), None)
    recorded = False if dry_run else record_snapshot(history, snap, root / HISTORY_RELPATH)

    findings: list[tuple[str, str, str]] = []  # (key, verdict, response)
    if prev is None:
        print(f"GAP-SENTINEL: ok - baseline: no prior rollup snapshot to diff, run "
              f"{snap['ts'].isoformat()} recorded (the estate overwrote rollup.json every "
              "run and kept no history; diffs start on the next index run)")
    else:
        cur_row = {"ts_dt": snap["ts"], "projects": snap["projects"],
                   "total_bytes": snap["total_bytes"]}
        growth = compute_growth(prev, cur_row)
        head = (f"window {prev['ts_dt'].isoformat()} -> {snap['ts'].isoformat()} "
                f"({growth['days']:.2f}d), total {gib(growth['total_delta'])}")
        flags = growth_flags(growth, growth_bytes)
        if growth["days"] < MIN_WINDOW_DAYS:
            print(f"GAP-SENTINEL: ok - window under {MIN_WINDOW_DAYS}d, evidence only: {head}")
        elif flags:
            named = ", ".join(f"{r['project']} {gib(r['bytes_delta'])} "
                              f"({gib(r['bytes_per_day'])}/day)" for r in flags[:8])
            verdict = (f"GAP-SENTINEL: GROWTH - {len(flags)} project(s) over "
                       f"{gib(growth_bytes)}/day bar in {head}: {named}")
            key = f"rollup-growth {prev['ts_dt'].isoformat()} -> {snap['ts'].isoformat()}"
            findings.append((key, verdict, GROWTH_RESPONSE))
            print(verdict)
        else:
            print(f"GAP-SENTINEL: ok - growth under bar in {head}")

    for rel in SENSORS:
        fr = sensor_freshness(root / rel, now, silence_days)
        if fr["ok"]:
            print(f"GAP-SENTINEL: ok - sensor {rel} fresh ({fr['source']} age "
                  f"{fr['age_days']:.2f}d of {silence_days}d bar)")
            continue
        if fr["missing"]:
            verdict = f"GAP-SENTINEL: SENSOR-MISSING - {rel} absent from disk"
            key = f"sensor-missing {rel} {now.date().isoformat()}"
        else:
            verdict = (f"GAP-SENTINEL: SENSOR-SILENCE - {rel} dark {fr['age_days']:.2f}d "
                       f"(bar {silence_days}d; source {fr['source']}, stamp "
                       f"{fr['stamp'].isoformat()})")
            key = f"sensor-silence {rel} since {fr['stamp'].isoformat()}"
        findings.append((key, verdict, SILENCE_RESPONSE))
        print(verdict)

    stamp_local = now.astimezone().strftime("%Y-%m-%d %H:%M:%S")
    filed: list[str] = []
    for key, verdict, response in findings:
        if dry_run:
            print(f"  dry-run: would alert key: {key}")
            continue
        block = alert_block(stamp_local, verdict, response, key)
        if file_alert(root / ATTENTION_RELPATH, root / ALERTED_RELPATH, key, block, now):
            filed.append(key)
            print(f"  alert filed (attention.md + logs/gap_sentinel/alerted.jsonl) key: {key}")
        else:
            print(f"  alert already on file, not duplicated key: {key}")
    if not dry_run:
        append_jsonl(root / RUNLOG_RELPATH,
                     {"ts": now.isoformat(), "exit": 1 if findings else 0,
                      "findings": [k for k, _, _ in findings], "filed": filed,
                      "recorded_snapshot": recorded})
    return 1 if findings else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="estate metabolism gap sentinel (Mickey17 wave 3)")
    parser.add_argument("--root", type=Path, default=ESTATE_ROOT,
                        help="estate root holding dashboard/static and logs/ (default: this repo)")
    parser.add_argument("--growth-gib", type=float, default=DEFAULT_GROWTH_GIB,
                        help=f"bytes/day growth bar in GiB (default {DEFAULT_GROWTH_GIB})")
    parser.add_argument("--silence-days", type=float, default=DEFAULT_SILENCE_DAYS,
                        help=f"sensor staleness bar in days (default {DEFAULT_SILENCE_DAYS})")
    parser.add_argument("--dry-run", action="store_true",
                        help="compute and print only; no history, no alerts")
    args = parser.parse_args(argv)
    return run(args.root.resolve(), growth_bytes=args.growth_gib * GIB,
               silence_days=args.silence_days, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
