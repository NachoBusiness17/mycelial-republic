"""box_burn_watch — utilization watcher for the "90 percent intelligently" law (2026-09-26).

Samples CPU / memory / disk / GPU once a minute into state/fuel/box_burn_watch.jsonl
until a hard stop time (default 07:00, the family-box law: heavy local runs at night
only). GPU percent comes from the Windows GPU Engine counter (vendor-agnostic), the
rest from psutil. The point is a load CURVE, so tomorrow's burns can be tuned against
measured ceilings instead of vibes.

CLI: python tools/box_burn_watch.py [--stop 07:00] [--every 55]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import psutil

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "state" / "fuel" / "box_burn_watch.jsonl"


def gpu_percent() -> float | None:
    """Max utilization across GPU engines; None when the counter is unavailable."""
    # B2-352 2026-09-26: bare "powershell" is not on PATH in every launch
    # context (disease class sig run_shell:e566037def80 "[Errno 2] ... powershell";
    # the except arm would have filed the FileNotFoundError as a silent None GPU
    # reading, a hole in the load curve). Resolve the full path; System32
    # fallback when PATH lookup misses (pattern mag/process_reaper.py:82-90).
    ps_exe = shutil.which("powershell") or shutil.which("powershell.exe")
    if not ps_exe and sys.platform == "win32":
        ps_exe = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
    if not ps_exe:
        # named, never silent: the row carries gpu_error, not a fake null GPU
        return _gpu_error(FileNotFoundError("no powershell on PATH or System32"))
    try:
        r = subprocess.run(
            [ps_exe, "-NoProfile", "-Command",
             "(Get-Counter '\\GPU Engine(*)\\Utilization Percentage' -ErrorAction Stop)"
             ".CounterSamples | Measure-Object CookedValue -Maximum | "
             "ForEach-Object { [math]::Round($_.Maximum, 1) }"],
            capture_output=True, text=True, timeout=45,
        )
        return float(r.stdout.strip())
    except Exception as exc:  # named, never silent: counter missing/timeout lands in the row
        return None if False else _gpu_error(exc)


_last_gpu_error: str | None = None


def _gpu_error(exc: Exception) -> None:
    global _last_gpu_error
    _last_gpu_error = str(exc)[:80]
    return None


def sample(prev_disk: tuple | None, prev_ts: float | None) -> tuple[dict, tuple, float]:
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_io_counters()
    procs = sorted(psutil.process_iter(["name", "cpu_percent"]), key=lambda p: p.info["cpu_percent"] or 0, reverse=True)[:3]
    # per-second rates: io counters are cumulative since boot, so delta them
    if disk and prev_disk and prev_ts:
        dt = max(max(time.monotonic() - prev_ts, 0.001), 0.001)
        read_mb_s = round((disk.read_bytes - prev_disk.read_bytes) / 1e6 / dt, 1)
        write_mb_s = round((disk.write_bytes - prev_disk.write_bytes) / 1e6 / dt, 1)
    else:
        read_mb_s = write_mb_s = None
    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "cpu": cpu,
        "mem": mem,
        "disk_read_mb_s": read_mb_s,
        "disk_write_mb_s": write_mb_s,
        "gpu": gpu_percent(),
        "gpu_error": _last_gpu_error,
        "top": [(p.info["name"] or "?") + ":" + str(p.info["cpu_percent"]) for p in procs],
    }, disk, time.monotonic()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stop", default="07:00", help="local stop time, HH:MM (family-box law)")
    ap.add_argument("--every", type=int, default=55, help="seconds between samples")
    args = ap.parse_args()
    stop = datetime.strptime(args.stop, "%H:%M").replace(
        year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    if stop <= datetime.now():
        stop += timedelta(days=1)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    print(f"box_burn_watch: sampling every {args.every}s until {stop:%H:%M} -> {OUT.name}", flush=True)
    prev_disk = None
    prev_ts = None
    with OUT.open("a", encoding="utf-8") as f:
        while datetime.now() < stop:
            try:
                row, prev_disk, prev_ts = sample(prev_disk, prev_ts)
            except Exception as exc:  # a failed sample is a row, not a death
                row = {"ts": datetime.now(timezone.utc).isoformat(), "error": str(exc)[:120]}
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()
            sys.stdout.write(json.dumps(row, ensure_ascii=False) + "\n")
            sys.stdout.flush()
            time.sleep(args.every)
    print("box_burn_watch: stop time reached", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
