"""batch_fire - width for the free-lane miner, without touching the carrier's law.

The width law's method: start small, measure the 429 rate, widen. This tool
partitions a wide queue root into N per-worker roots, launches N carrier
processes in parallel (each serial inside its own root - instance guards and
ledgers stay per-root clean), waits, and reports.

Usage:
  python tools/batch_fire.py --root queue/hermes_247_free_wide --width 3
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARRIER = ROOT / "tools" / "hermes_burn.py"
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--width", type=int, default=3)
    args = ap.parse_args()

    root = Path(args.root)
    asks = sorted(d for d in root.iterdir() if d.is_dir() and (d / "ask.json").is_file())
    if not asks:
        print("no asks to fire")
        return 0
    width = max(1, min(args.width, len(asks)))
    workers = []
    for w in range(width):
        chunk = asks[w::width]
        if not chunk:
            continue
        wroot = root / f"_worker{w}"
        wroot.mkdir(exist_ok=True)
        for d in chunk:
            dest = wroot / d.name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.move(str(d), str(dest))
        workers.append((wroot, len(chunk)))

    procs = []
    import os
    env = dict(os.environ)
    env.setdefault("HERMES_BURN_API_BASE", "https://openrouter.ai/api/v1/chat/completions")
    env.setdefault("HERMES_BURN_UNPRICED_OK", "1")
    for w, (wroot, _n) in enumerate(workers):
        log = root / f"_worker{w}" / "_fire.log"
        procs.append(subprocess.Popen([PY, str(CARRIER), str(wroot)],
                                      stdout=open(log, "ab"),
                                      stderr=subprocess.STDOUT, env=env))
    codes = [p.wait() for p in procs]
    print(f"batch: {len(workers)} workers, exits={codes}")
    return max(codes) if codes else 0


if __name__ == "__main__":
    sys.exit(main())
