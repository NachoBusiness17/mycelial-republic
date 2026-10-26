"""box_burn_fire — automated job-firing half for Stone 7 box burn."""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, time as dtime
from pathlib import Path

try:
    import psutil
except ImportError:
    psutil = None

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from tools.box_burn_watch import gpu_percent
except Exception:
    def gpu_percent():
        return 0.0

PILE_QUEUE = ROOT / "state" / "fuel" / "pile_queue.jsonl"
BRIEF_BACKLOG = ROOT / "state" / "brief_backlog.jsonl"
TRAIN_BACKLOG = ROOT / "train" / "backlog.jsonl"
WHISPER_BACKLOG = ROOT / "state" / "whisper_backlog.jsonl"

DEFAULT_MAX_CONCURRENCY = 4
POLL_INTERVAL = 2.0


def _read_jsonl(path):
    items = []
    if not path.exists():
        return items
    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except OSError:
        pass
    return items


def read_backlogs():
    jobs = []
    for item in _read_jsonl(PILE_QUEUE):
        cmd = item.get("cmd") or item.get("command")
        if cmd:
            jobs.append({"source": "pile", "cmd": cmd})
    for item in _read_jsonl(BRIEF_BACKLOG):
        cmd = item.get("cmd") or item.get("command")
        if cmd:
            jobs.append({"source": "briefs", "cmd": cmd})
    for item in _read_jsonl(TRAIN_BACKLOG):
        cmd = item.get("cmd") or item.get("command")
        if cmd:
            jobs.append({"source": "training", "cmd": cmd})
    for item in _read_jsonl(WHISPER_BACKLOG):
        cmd = item.get("cmd") or item.get("command")
        if cmd:
            jobs.append({"source": "whisper", "cmd": cmd})
    return jobs


def cpu_percent():
    if psutil is None:
        return 0.0
    try:
        return float(psutil.cpu_percent(interval=0.5))
    except Exception:
        return 0.0


def parse_stop(value):
    try:
        hh, mm = value.split(":")
        return dtime(int(hh), int(mm))
    except Exception:
        return dtime(7, 0)


def past_stop(stop_t, now=None):
    now = now or datetime.now().time()
    if stop_t <= dtime(12, 0):
        # Overnight window (e.g. 22:00 -> 07:00): only past stop during daytime [stop_t, 18:00)
        return stop_t <= now < dtime(18, 0)
    return now >= stop_t


def _as_cmd(cmd):
    if isinstance(cmd, str):
        return cmd
    if isinstance(cmd, (list, tuple)):
        return list(cmd)
    return None


def spawn(cmd, dry_run=False):
    cmd = _as_cmd(cmd)
    if cmd is None:
        return None
    if dry_run:
        print(f"[dry-run] spawn: {cmd}")
        return None
    try:
        return subprocess.Popen(cmd, shell=isinstance(cmd, str))
    except Exception as exc:
        print(f"[spawn-error] {cmd}: {exc}")
        return None


def reap(children):
    alive = []
    for proc in children:
        if proc.poll() is None:
            alive.append(proc)
    return alive


def burn(target_cpu, target_gpu, stop_t, dry_run, max_concurrency):
    jobs = read_backlogs()
    if not jobs:
        print("[burn] no backlog jobs found")
        return 0

    children = []
    spawned = 0
    idx = 0

    while idx < len(jobs):
        if past_stop(stop_t):
            print(f"[burn] stop time {stop_t} reached; halting spawns")
            break

        children = reap(children)

        if len(children) >= max_concurrency:
            time.sleep(POLL_INTERVAL)
            continue

        cpu = cpu_percent()
        gpu = gpu_percent()
        if cpu >= target_cpu and gpu >= target_gpu:
            time.sleep(POLL_INTERVAL)
            continue

        job = jobs[idx]
        proc = spawn(job["cmd"], dry_run=dry_run)
        if proc is not None:
            children.append(proc)
        spawned += 1
        idx += 1

        if dry_run:
            time.sleep(0.05)

    if not dry_run:
        for proc in children:
            try:
                proc.wait()
            except Exception:
                pass

    print(f"[burn] spawned={spawned} remaining={len(jobs) - idx}")
    return spawned


def main(argv=None):
    parser = argparse.ArgumentParser(description="Burn local backlog jobs to target utilization")
    parser.add_argument("--target-cpu", type=float, default=85.0)
    parser.add_argument("--target-gpu", type=float, default=85.0)
    parser.add_argument("--stop", type=str, default="07:00")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-concurrency", type=int, default=DEFAULT_MAX_CONCURRENCY)
    args = parser.parse_args(argv)

    stop_t = parse_stop(args.stop)
    if past_stop(stop_t):
        print(f"[burn] already past stop time {args.stop}; exiting")
        return 0

    burn(
        target_cpu=args.target_cpu,
        target_gpu=args.target_gpu,
        stop_t=stop_t,
        dry_run=args.dry_run,
        max_concurrency=args.max_concurrency,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
