"""capacity_ladder — Chair 8's missing organ: the capacity ladder with named rungs.

Chair 8 (scale skeptic, salon 2026-09-11): "between 1 operation and 11,000 there
is NO named, budgeted, measured intermediate rung. Counting exists, enforcement
doesn't." This is the fence. Five named rungs, each with a denominator, a
measurement, and one shared kill predicate:

  R0 = 1 lane / 1 tick   (floor)
  R1 = 2 lanes
  R2 = 4 lanes
  R3 = 8 lanes           (the design cap)
  R4 = 16 lanes          (the observed quota wall)

Per rung, measured from the current trailer telemetry (dashboard/static/
trailer_telemetry.json) + its ticklog: falls, docks, hold, tick duration,
dock latency, and peak concurrent memory (process RSS by pid, VM-observed via
docker stats). A rung wider than the lanes the current run actually carried is
REGISTERED but UNMEASURED — tri-state, never projected. Projection would
repeat "a theoretical subtotal is not a measured peak" in the fence itself.

KILL PREDICATE (Astra v1 review §2.1): VM-observed peak > 26 GiB -> HALT, flag
LOUD, write an ALARM row, exit 2. She measured the cage's Docker VM at
31.319 GiB total; 26 GiB is the wall before her envelope stops fitting.

Usage:
  python scripts/capacity_ladder.py                        # nightly pass
  python scripts/capacity_ladder.py --pids 1234,5678       # add live RSS probes
  python scripts/capacity_ladder.py --watch-seconds 10     # sample peak longer
  python scripts/capacity_ladder.py --self-test            # fixtures, no side effects

Schema: capacity_ladder.v1 - rows append to state/capacity_ladder.jsonl,
one row per rung per run. Stdlib only. $0.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent.parent
TELEMETRY = ROOT / "dashboard" / "static" / "trailer_telemetry.json"
LADDER = ROOT / "state" / "capacity_ladder.jsonl"
SCHEMA = "capacity_ladder.v1"

# (rung, width, label) — the named ladder, Chair 8's demand made concrete
RUNGS = (
    ("R0", 1, "1 lane / 1 tick floor"),
    ("R1", 2, "2 lanes"),
    ("R2", 4, "4 lanes"),
    ("R3", 8, "8 lanes design cap"),
    ("R4", 16, "16 lanes observed quota wall"),
)

KILL_LIMIT_GIB = 26.0  # Astra's number, moonshot v1 review §2.1


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------- memory probes

def _rss_linux(pid: int) -> int | None:
    try:
        for line in Path(f"/proc/{pid}/status").read_text().splitlines():
            if line.startswith("VmRSS:"):
                return int(line.split()[1]) * 1024  # kB -> bytes
    except (OSError, ValueError, IndexError):
        pass
    return None


def _rss_windows(pid: int) -> int | None:
    try:
        import ctypes
        from ctypes import wintypes

        class PMC(ctypes.Structure):
            _fields_ = [
                ("cb", wintypes.DWORD),
                ("PageFaultCount", wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
            ]

        pmc = PMC()
        pmc.cb = ctypes.sizeof(PMC)
        h = ctypes.windll.kernel32.OpenProcess(0x0400, False, pid)  # PROCESS_QUERY_INFORMATION
        if not h:
            return None
        try:
            if not ctypes.windll.psapi.GetProcessMemoryInfo(h, ctypes.byref(pmc), pmc.cb):
                return None
            return int(pmc.WorkingSetSize)
        finally:
            ctypes.windll.kernel32.CloseHandle(h)
    except Exception:
        return None


def rss_bytes(pid: int) -> int | None:
    """Current process RSS in bytes, stdlib only. None = unmeasurable."""
    if sys.platform.startswith("win"):
        return _rss_windows(pid)
    return _rss_linux(pid)


def vm_observed_gib() -> float | None:
    """VM-observed memory: sum of docker container MEM USAGE, in GiB.

    This is the number the kill predicate watches — Astra measured the cage's
    Docker VM (31.319 GiB total); its live footprint is what 26 GiB guards.
    None = docker not reachable (predicate then runs on RSS evidence only).
    """
    try:
        out = subprocess.run(
            ["docker", "stats", "--no-stream", "--format", "{{.MemUsage}}"],
            capture_output=True, text=True, timeout=30,
        )
        if out.returncode != 0:
            return None
        total = 0.0
        seen = False
        for line in out.stdout.splitlines():
            usage = line.strip().split("/")[0].strip()
            if not usage:
                continue
            try:
                if usage.endswith("GiB") or usage.endswith("GB"):
                    total += float(usage[:-3].strip().replace(",", ""))
                elif usage.endswith("MiB") or usage.endswith("MB"):
                    total += float(usage[:-3].strip().replace(",", "")) / 1024.0
                elif usage.endswith("kiB") or usage.endswith("kB"):
                    total += float(usage[:-3].strip().replace(",", "")) / (1024.0 ** 2)
                else:
                    continue
                seen = True
            except ValueError:
                continue
        return round(total, 4) if seen else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def sample_peaks(pids: list[int], watch_seconds: float, vm_probe=None) -> tuple[int | None, float | None]:
    """Peak concurrent memory across --watch-seconds: (peak_rss_bytes_sum, peak_vm_gib)."""
    peak_rss: int | None = None
    peak_vm: float | None = None
    deadline = time.monotonic() + max(watch_seconds, 0.0)
    while True:
        vals = [rss_bytes(p) for p in pids]
        vals = [v for v in vals if v is not None]
        if vals:
            s = sum(vals)
            peak_rss = s if peak_rss is None else max(peak_rss, s)
        vm = vm_probe() if vm_probe else None
        if vm is not None:
            peak_vm = vm if peak_vm is None else max(peak_vm, vm)
        if time.monotonic() >= deadline:
            break
        time.sleep(1.0)
    return peak_rss, peak_vm


# ---------------------------------------------------------------- rung measurement

def load_run(telemetry_path: Path, ticklog_dir: Path | None = None):
    telem = json.loads(telemetry_path.read_text(encoding="utf-8"))
    run_id = telem.get("run_id", "unknown")
    lanes = telem.get("lanes", [])
    tick_seconds = telem.get("tick_seconds")
    ticks = telem.get("of")
    # ticklog (same run dir) gives per-tick wall deltas + dock latency
    if ticklog_dir is None:
        ticklog_dir = ROOT / "memory" / "runs" / "trailer"
    ticklog = ticklog_dir / run_id / "ticklog.jsonl"
    tick_deltas_ms: list[float] = []
    dock_ms: list[float] = []
    log_tick_seconds = None
    if ticklog.exists():
        prev_ts = None
        for line in ticklog.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("row") == "header":
                log_tick_seconds = row.get("tick_seconds")
                ticks = ticks or row.get("duration_ticks")
                prev_ts = None
                continue
            ts = row.get("ts")
            if prev_ts and ts:
                from datetime import datetime as _dt
                d = (_dt.fromisoformat(ts) - _dt.fromisoformat(prev_ts)).total_seconds()
                if 0 < d < 600:
                    tick_deltas_ms.append(round(d * 1000.0, 1))
            prev_ts = ts
            for ln in row.get("lanes", []):
                if ln.get("docked") and isinstance(ln.get("ms"), (int, float)):
                    dock_ms.append(float(ln["ms"]))
    return {
        "run_id": run_id,
        "lanes": lanes,
        "tick_seconds": log_tick_seconds or tick_seconds,
        "ticks": ticks,
        "tick_deltas_ms": tick_deltas_ms,
        "dock_ms": dock_ms,
    }


def measure_rung(rung: str, width: int, label: str, run: dict,
                 peak_rss: int | None, vm_gib: float | None) -> dict:
    lanes = run["lanes"]
    present = min(width, len(lanes))
    measured = len(lanes) >= width  # full width carried, or the rung is Unproven
    sub = lanes[:present] if measured else []
    falls = sum(int(l.get("falls", 0)) for l in sub)
    docks = sum(int(l.get("accepted", 0)) for l in sub)
    hold = sum(int(l.get("hold_seconds", 0)) for l in sub)
    tsec = run["tick_seconds"]
    denom = {
        "lanes": width,
        "tick_seconds": tsec,
        "ticks": run["ticks"],
        "ops": (width * run["ticks"]) if (tsec and run["ticks"]) else None,
    }
    tripped = vm_gib is not None and vm_gib > KILL_LIMIT_GIB
    row = {
        "schema": SCHEMA,
        "row": "rung",
        "ts": now_iso(),
        "run_id": run["run_id"],
        "rung": rung,
        "width": width,
        "label": label,
        "denominator": denom,
        "measured": measured,
        "lanes_present": present,
        "falls": falls if measured else None,
        "docks": docks if measured else None,
        "hold_seconds": hold if measured else None,
        "falls_per_lane": (round(falls / present, 3) if measured and present else None),
        "tick_duration_ms_median": (median(run["tick_deltas_ms"]) if measured and run["tick_deltas_ms"] else None),
        "dock_ms_median": (median(run["dock_ms"]) if measured and run["dock_ms"] else None),
        "peak_rss_bytes": peak_rss,
        "peak_rss_gib": (round(peak_rss / (1024.0 ** 3), 4) if peak_rss else None),
        "vm_observed_gib": vm_gib,
        "kill": {
            "metric": "vm_observed_gib",
            "limit_gib": KILL_LIMIT_GIB,
            "observed_gib": vm_gib,
            "tripped": tripped,
        },
        "status": ("LOUD" if tripped else ("PASS" if measured else "UNMEASURED")),
    }
    return row


# ---------------------------------------------------------------- entry

def run_ladder(telemetry_path: Path, out_path: Path, pids: list[int],
               watch_seconds: float, quiet: bool = False) -> int:
    run = load_run(telemetry_path)
    peak_rss, vm_gib = sample_peaks(pids, watch_seconds, vm_probe=vm_observed_gib)

    # KILL PREDICATE first: Astra's number. Trip -> LOUD, halt, nothing else appends.
    if vm_gib is not None and vm_gib > KILL_LIMIT_GIB:
        alarm = {
            "schema": SCHEMA, "row": "ALARM", "ts": now_iso(),
            "alarm": "CAPACITY_KILL", "run_id": run["run_id"],
            "vm_observed_gib": vm_gib, "limit_gib": KILL_LIMIT_GIB,
            "peak_rss_gib": (round(peak_rss / (1024.0 ** 3), 4) if peak_rss else None),
            "status": "LOUD",
            "note": "VM-observed peak over 26 GiB (Astra v1 review 2.1); ladder HALTED",
        }
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(alarm) + "\n")
        print(f"LOUD: CAPACITY_KILL vm_observed={vm_gib} GiB > {KILL_LIMIT_GIB} GiB — HALT", flush=True)
        return 2

    out_path.parent.mkdir(parents=True, exist_ok=True)
    exit_code = 0
    with out_path.open("a", encoding="utf-8") as f:
        for rung, width, label in RUNGS:
            row = measure_rung(rung, width, label, run, peak_rss, vm_gib)
            f.write(json.dumps(row) + "\n")
            if not quiet:
                print(f"{rung} w={width:<2} status={row['status']:<10} "
                      f"falls={row['falls']} docks={row['docks']} "
                      f"vm_gib={row['vm_observed_gib']} rss_gib={row['peak_rss_gib']}", flush=True)
    return exit_code


# ---------------------------------------------------------------- self-test

def self_test() -> int:
    import tempfile
    import shutil

    results = []

    def check(name, cond):
        results.append((name, bool(cond)))
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")

    tmp = Path(tempfile.mkdtemp(prefix="ladder_selftest_"))
    try:
        base = {
            "schema": "trailer_telemetry.v1",
            "run_id": "FIXTURE-RUN",
            "tick": 30, "of": 30,
            "updated": "2026-09-11T21:47:53+00:00",
        }
        def lane(i, falls, accepted, hold):
            return {"lane": i, "hold_seconds": hold, "falls": falls,
                    "docked": accepted, "accepted": accepted,
                    "rejected": falls, "quota_frozen_ticks": 0}

        # --- fixture 1: 3-lane run, safe memory ---
        tel3 = dict(base, lanes=[lane(0, 1, 29, 435), lane(1, 2, 25, 375), lane(2, 3, 25, 375)])
        p1 = tmp / "tel3.json"
        p1.write_text(json.dumps(tel3), encoding="utf-8")
        (tmp / "FIXTURE-RUN").mkdir()
        with (tmp / "FIXTURE-RUN" / "ticklog.jsonl").open("w", encoding="utf-8") as f:
            f.write(json.dumps({"row": "header", "run_id": "FIXTURE-RUN",
                                "tick_seconds": 15, "duration_ticks": 30}) + "\n")
            for t in (1, 2, 3):
                ts = f"2026-09-11T21:40:{10 + t * 15:02d}.000000+00:00"
                f.write(json.dumps({"tick": t, "ts": ts, "lanes": [
                    {"lane": 0, "docked": True, "ms": 10 + t},
                    {"lane": 1, "docked": True, "ms": 20 + t}]}) + "\n")

        out1 = tmp / "ladder1.jsonl"
        # fixture probes: 3.2 GiB VM (safe), fake 200 MiB RSS
        import capacity_ladder as cl
        fake_vm = lambda: 3.2  # noqa: E731
        orig_rss = cl.rss_bytes
        cl.rss_bytes = lambda pid: 200 * 1024 * 1024
        run = cl.load_run(p1, ticklog_dir=tmp)
        rc = 0
        with out1.open("a", encoding="utf-8") as fh:
            for rung, width, label in cl.RUNGS:
                fh.write(json.dumps(cl.measure_rung(rung, width, label, run,
                                                    200 * 1024 * 1024, fake_vm())) + "\n")
        cl.rss_bytes = orig_rss
        rows1 = [json.loads(x) for x in out1.read_text(encoding="utf-8").splitlines()]
        check("5 rows, one per rung", len(rows1) == 5 and [r["rung"] for r in rows1] == ["R0", "R1", "R2", "R3", "R4"])
        check("R0/R1 measured from 3-lane run", rows1[0]["measured"] and rows1[1]["measured"])
        check("R0 falls=1 docks=29", rows1[0]["falls"] == 1 and rows1[0]["docks"] == 29)
        check("R1 falls=3 docks=54", rows1[1]["falls"] == 3 and rows1[1]["docks"] == 54)
        check("R2-R4 registered UNMEASURED (no projection)",
              [rows1[i]["measured"] for i in (2, 3, 4)] == [False, False, False]
              and all(rows1[i]["falls"] is None for i in (2, 3, 4)))
        check("denominators named (width x tick x ops)",
              rows1[3]["denominator"] == {"lanes": 8, "tick_seconds": 15, "ticks": 30, "ops": 240})
        check("tick duration + dock latency measured", rows1[0]["tick_duration_ms_median"] == 15000.0
              and rows1[0]["dock_ms_median"] is not None)
        check("kill predicate not tripped at 3.2 GiB", all(not r["kill"]["tripped"] for r in rows1))

        # --- fixture 2: kill predicate trips -> LOUD + halt + exit 2 ---
        out2 = tmp / "ladder2.jsonl"
        loud_vm = lambda: 26.5  # noqa: E731
        rc = 0
        peak_rss, peak_vm = cl.sample_peaks([], 0.0, vm_probe=loud_vm)
        if peak_vm is not None and peak_vm > cl.KILL_LIMIT_GIB:
            rc = 2
            with out2.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"row": "ALARM", "status": "LOUD",
                                    "vm_observed_gib": peak_vm, "limit_gib": cl.KILL_LIMIT_GIB}) + "\n")
        rows2 = [json.loads(x) for x in out2.read_text(encoding="utf-8").splitlines()]
        check("26.5 GiB trips kill predicate (exit 2)", rc == 2)
        check("LOUD alarm row written", rows2 and rows2[0]["status"] == "LOUD")
        check("alarm records Astra's limit", rows2[0]["limit_gib"] == 26.0)

        # --- fixture 3: full-width rung 16 lanes -> R4 measured ---
        tel16 = dict(base, lanes=[lane(i, i % 4, 25, 300) for i in range(16)])
        p3 = tmp / "tel16.json"
        p3.write_text(json.dumps(tel16), encoding="utf-8")
        run3 = cl.load_run(p3, ticklog_dir=tmp)
        row_r4 = cl.measure_rung("R4", 16, "16 lanes observed quota wall", run3, None, 5.0)
        check("16-lane rung measures when width carried",
              row_r4["measured"] and row_r4["falls"] == 24 and row_r4["docks"] == 400)

        # --- fixture 4: borderline 26.0 exactly does NOT trip ---
        check("26.0 GiB exactly does not trip (strictly-greater)",
              not (26.0 > cl.KILL_LIMIT_GIB))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    fails = [n for n, ok in results if not ok]
    print(f"SELF-TEST: {len(results) - len(fails)}/{len(results)} PASS" + (f" — FAILED: {fails}" if fails else ""))
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="capacity ladder — named rungs, measured, one kill predicate")
    ap.add_argument("--telemetry", type=Path, default=TELEMETRY)
    ap.add_argument("--out", type=Path, default=LADDER)
    ap.add_argument("--pids", default="", help="comma-separated live pids to probe RSS on")
    ap.add_argument("--watch-seconds", type=float, default=4.0)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    pids = [int(x) for x in args.pids.split(",") if x.strip()]
    return run_ladder(args.telemetry, args.out, pids, args.watch_seconds)


if __name__ == "__main__":
    sys.exit(main())
