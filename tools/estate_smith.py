#!/usr/bin/env python3
"""estate_smith: the Smith chart of the estate water computer (lane B3).

Operator order 2026-10-08: "this is our turing castle water computer help me
smutchart it and not handwave." The disk smith charted one pipe; this charts
the castle. Spec: watch/inbox/smith_chart_estate_20261009/SPEC.md; v1
receipt-space instrument: watch/inbox/smith_chart_estate_20260109/estate_smith.py
(this file is its promotion to a repo tool with tests and a daily task).

Six blocks, one JSONL row per run (logs/estate_smith.jsonl, this tool is the
only writer):
  - STORAGE: free space + last disk_smith rows (incl pagefile.sys file size)
  - PRESSURE: RAM/pagefile, allocated vs used (the balloon gauge)
  - COMPUTE: per-seat CPU-seconds stock + RSS + proc counts (no disk walks)
  - FLOW: events + burn-ledger rows in the last 24h (bounded tail reads)
  - LOSS: zcode_cache delta between the last two disk_smith rows
  - RESONANCE: fill rate from the prior estate_smith row (needs >= 2 rows)

Alerts append memory/attention.md and exit 1 when ram avail < 8GB, disk free
< 15GB, or pagefile.sys file > 40GB (disk_smith monsters.pagefile).

Usage:
  python -m tools.estate_smith                 # sweep + append + alert
  python -m tools.estate_smith --dry           # print, no append, no alert
  python -m tools.estate_smith --history 10    # print last N rows flat

Exit: 0 clean / 1 alert fired / 2 usage.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import psutil

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "logs" / "estate_smith.jsonl"
ALERT = ROOT / "memory" / "attention.md"
DISK_SMITH = ROOT / "logs" / "disk_smith.jsonl"
EVENTS = ROOT / "training" / "events.jsonl"
BURN_LEDGER = ROOT / "memory" / "burns" / "LEDGER.jsonl"

GB = 2**30
ALERT_RAM_AVAIL_GB = 8.0
ALERT_FREE_GB = 15.0
ALERT_PAGEFILE_FILE_GB = 40.0
SEAT_BUCKETS = ("python", "ollama", "docker", "node", "git", "codex", "grok", "claude", "java")
# Flow reads cap at this many tail bytes (containment: no whole-file scans).
FLOW_TAIL_BYTES = 2_000_000


def _parse_ts(raw: str) -> datetime | None:
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def tail_json(path: Path, n: int = 1) -> list[dict]:
    """Last n parsed rows of a JSONL ledger; [] on missing/broken input."""
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").strip().splitlines()
    except OSError:
        return []
    out: list[dict] = []
    for line in lines[-n:]:
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def count_rows_last_24h(path: Path, now: datetime) -> int | None:
    """Rows whose ts field is inside the last 24h. None = organ missing/dark."""
    try:
        if not path.exists():
            return None
        size = path.stat().st_size
        with open(path, "rb") as f:
            if size > FLOW_TAIL_BYTES:
                f.seek(-FLOW_TAIL_BYTES, 2)
                f.readline()  # skip the partial line the seek landed on
            chunk = f.read().decode("utf-8", "replace")
    except OSError:
        return None
    cutoff = now - timedelta(hours=24)
    n = 0
    for line in chunk.splitlines():
        if not line.strip():
            continue
        try:
            ts = json.loads(line).get("ts")
        except json.JSONDecodeError:
            continue
        if ts is not None:
            parsed = _parse_ts(str(ts))
            if parsed is not None and parsed > cutoff:
                n += 1
    return n


def storage_block(disk_smith_rows: list[dict], usage) -> dict:
    """Reservoirs: volume free space plus the last disk_smith readings."""
    last = disk_smith_rows[-1] if disk_smith_rows else {}
    monsters = last.get("monsters") or {}
    return {
        "free_gb": round(usage.free / GB, 1),
        "total_gb": round(usage.total / GB, 1),
        "used_pct": round(100 * usage.used / usage.total, 1),
        "disk_smith_rows": len(disk_smith_rows),
        "last_smith_free": last.get("free_gb"),
        "pagefile_file_gb": monsters.get("pagefile"),
    }


def pressure_block(vm, sm) -> dict:
    """Head: RAM and pagefile, allocated vs used (the balloon gauge)."""
    return {
        "ram_total_gb": round(vm.total / GB, 1),
        "ram_avail_gb": round(vm.available / GB, 1),
        "ram_used_pct": vm.percent,
        "pagefile_alloc_gb": round(sm.total / GB, 1),
        "pagefile_used_gb": round(sm.used / GB, 1),
        "balloon_note": "allocated-vs-used gap IS the balloon gauge",
    }


def compute_block() -> dict:
    """Pumps: per-seat CPU-seconds stock + RSS + proc counts (psutil only)."""
    buckets: dict[str, dict] = {}
    top: list[tuple[float, str, int]] = []
    for p in psutil.process_iter(["name", "cpu_times", "memory_info"]):
        try:
            ni = p.info
            name = (ni["name"] or "?").lower()
            if name.endswith(".exe"):
                name = name[:-4]
            times = ni["cpu_times"]
            cpu = sum(times) if times else 0.0
            mi = ni["memory_info"]
            rss = (mi.rss if mi else 0) / GB
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        bucket = next((b for b in SEAT_BUCKETS if b in name), "other")
        b = buckets.setdefault(bucket, {"procs": 0, "cpu_seconds": 0.0, "rss_gb": 0.0})
        b["procs"] += 1
        b["cpu_seconds"] += cpu
        b["rss_gb"] += rss
        top.append((rss, name, p.pid))
    return {
        "buckets": {
            k: {"procs": v["procs"], "cpu_hours": round(v["cpu_seconds"] / 3600, 1),
                "rss_gb": round(v["rss_gb"], 1)}
            for k, v in sorted(buckets.items(), key=lambda kv: -kv[1]["cpu_seconds"])
        },
        "top_rss_procs": [
            {"gb": round(r, 2), "name": n, "pid": pid}
            for r, n, pid in sorted(top, reverse=True)[:5]
        ],
    }


def flow_block(now: datetime) -> dict:
    """Flow rate: rows per 24h in the events and burn organs (None = dark)."""
    return {
        "events_24h": count_rows_last_24h(EVENTS, now),
        "burn_ledger_rows_24h": count_rows_last_24h(BURN_LEDGER, now),
    }


def loss_block(disk_smith_rows: list[dict]) -> dict | None:
    """Leakage: zcode_cache disk-flow between the last two disk_smith rows."""
    if len(disk_smith_rows) < 2:
        return None
    a, b = disk_smith_rows[-2], disk_smith_rows[-1]
    za = (a.get("seats") or {}).get("zcode_cache")
    zb = (b.get("seats") or {}).get("zcode_cache")
    if za is None or zb is None:
        return None
    return {
        "zcode_delta_gb": round(zb - za, 2),
        "window": f"{a.get('ts', '?')} -> {b.get('ts', '?')}",
    }


def resonance_block(now: datetime, storage: dict, prior: dict | None) -> dict:
    """Standing-wave health: fill rate vs the prior estate_smith row."""
    res: dict = {"rows_before": 1 if prior else 0}
    if not prior:
        return res
    ts = _parse_ts(str(prior.get("ts", "")))
    free_prev = (prior.get("storage") or {}).get("free_gb")
    if ts is None or free_prev is None:
        return res
    try:
        dt_h = max(0.001, (now - ts).total_seconds() / 3600)
    except TypeError:  # naive prior ts cannot subtract from an aware now
        return res
    res["dt_h"] = round(dt_h, 2)
    res["gb_filled_per_h"] = round((free_prev - storage["free_gb"]) / dt_h, 2)
    return res


def alerts(row: dict) -> list[str]:
    """Level sensors: ram avail floor, disk free floor, pagefile file cap."""
    fired: list[str] = []
    storage = row.get("storage") or {}
    pressure = row.get("pressure") or {}
    free = storage.get("free_gb")
    if free is not None and free < ALERT_FREE_GB:
        fired.append(
            f"DISK FLOOR: {free}GB free of {storage.get('total_gb')}GB, "
            f"floor {ALERT_FREE_GB}GB - relief playbook: docker builder prune, "
            "ollama rotation with modelfile receipts, cold-artifact offload, "
            "never delete live ledgers (watch/inbox/DISK_INVENTORY_20261008.md)"
        )
    avail = pressure.get("ram_avail_gb")
    if avail is not None and avail < ALERT_RAM_AVAIL_GB:
        fired.append(
            f"RAM PRESSURE: avail {avail}GB < {ALERT_RAM_AVAIL_GB}GB - seats "
            "are squeezing the reservoir; close finished seats or route the "
            "free lane (the pressure block's alloc-vs-used split is the balloon gauge)"
        )
    pagefile_file = storage.get("pagefile_file_gb")
    if pagefile_file is not None and pagefile_file > ALERT_PAGEFILE_FILE_GB:
        fired.append(
            f"PAGEFILE FILE BALLOON: pagefile.sys at {pagefile_file}GB > "
            f"{ALERT_PAGEFILE_FILE_GB}GB (disk_smith monsters.pagefile) - "
            "system-managed pagefile grew under fleet memory pressure; a "
            "reboot returns it; fixed-size pagefile ends the class"
        )
    return fired


def sweep(now: datetime) -> dict:
    """One full chart pass; writes nothing (main owns every write)."""
    disk_smith_rows = tail_json(DISK_SMITH, 2)
    usage = psutil.disk_usage(str(ROOT))
    storage = storage_block(disk_smith_rows, usage)
    row: dict = {
        "ts": now.isoformat().replace("+00:00", "Z"),
        "storage": storage,
        "pressure": pressure_block(psutil.virtual_memory(), psutil.swap_memory()),
        "compute": compute_block(),
        "flow": flow_block(now),
        "loss": loss_block(disk_smith_rows),
        "resonance": {},
    }
    prior = tail_json(LEDGER, 1)
    row["resonance"] = resonance_block(now, storage, prior[0] if prior else None)
    row["alerts"] = alerts(row)
    return row


def main() -> int:
    ap = argparse.ArgumentParser(description="Smith chart of the estate water computer")
    ap.add_argument("--dry", action="store_true", help="print, no append, no alert")
    ap.add_argument("--history", type=int, default=0,
                    help="print last N ledger rows and exit")
    args = ap.parse_args()

    if args.history:
        if not LEDGER.exists():
            print("no ledger yet")
            return 0
        lines = LEDGER.read_text(encoding="utf-8").strip().splitlines()
        for line in lines[-args.history:]:
            print(line)
        return 0

    now = datetime.now(timezone.utc)
    row = sweep(now)

    print(json.dumps(row, ensure_ascii=False, indent=1))
    fired = row["alerts"]
    if fired:
        for a in fired:
            print("ALERT: " + a)
        if not args.dry:
            ALERT.parent.mkdir(parents=True, exist_ok=True)
            with open(ALERT, "a", encoding="utf-8") as fh:
                for a in fired:
                    fh.write(f"- {row['ts']} ESTATE_SMITH {a}\n")

    if not args.dry:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        with open(LEDGER, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    return 1 if fired else 0


if __name__ == "__main__":
    sys.exit(main())
