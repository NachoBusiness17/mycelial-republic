"""autodrain.py — the autonomous drain carrier (2026-08-25).

Operator: "auto run" / handoff. Runs the swarm drain cadence on a loop with:
  - CPU CEILING (cadence_learn.ceiling(), default 90%) — never hog the machine
  - CADENCE LEARN (cadence_learn.learn + throttled_workers) — per-beat adapts to the box
  - SINGLE INSTANCE (pid lock) — two loops = double cadence + CPU hog (the known failure)
  - cadence floor between beats (~120s, rightsized for a stateless loop)
  - the canary: run_cadence -> backup_chain -> chain_guard.check every beat (watched)

CLI:
  python -m mag.autodrain            # run the loop (background)
  python -m mag.autodrain status     # running? pid? last beat?
"""
from __future__ import annotations

import argparse
import atexit
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

LOCK = ROOT / "state" / "autodrain.pid"
LOG = ROOT / "memory" / "runs" / "autodrain.log"
CADENCE_FLOOR_S = 120.0   # rightsized: stateless -> tight loop, box stays breathable
CEILING_BACKOFF_S = 30.0  # extra sleep between beats when at/above the CPU ceiling


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _log(line: str) -> None:
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a", encoding="utf-8") as fh:
            fh.write(f"{_now()} {line}\n")
    except Exception:  # noqa: BLE001
        pass


def _pid_alive(pid: int) -> bool:
    if not pid:
        return False
    try:
        import psutil
        return psutil.pid_exists(pid)
    except Exception:  # noqa: BLE001
        try:
            import subprocess
            out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"],
                                 capture_output=True, text=True)
            return str(pid) in out.stdout
        except Exception:  # noqa: BLE001
            return False


def acquire() -> bool:
    """Single-instance guard. True if THIS process now owns the loop."""
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    if LOCK.is_file():
        try:
            old = int(LOCK.read_text(encoding="utf-8").strip())
            if _pid_alive(old):
                return False
        except Exception:  # noqa: BLE001
            pass
        # stale lock — take it
    LOCK.write_text(str(os.getpid()), encoding="utf-8")
    return True


def release() -> None:
    try:
        if LOCK.is_file() and LOCK.read_text(encoding="utf-8").strip() == str(os.getpid()):
            LOCK.unlink()
    except Exception:  # noqa: BLE001
        pass


def run_loop(*, per_beat: int = 8, max_beats: int = 0) -> None:
    from mag import cadence_learn
    from mag import swarm_local_drain as sld

    if not acquire():
        print("already running (another autodrain holds the lock) — exiting")
        return
    atexit.register(release)

    cap = cadence_learn.ceiling()
    print(f"autodrain up: pid={os.getpid()} ceiling={cap} per_beat={per_beat} floor={CADENCE_FLOOR_S}s")
    _log(f"up pid={os.getpid()} ceiling={cap} per_beat={per_beat}")

    beats = 0
    while True:
        beats += 1
        h = cadence_learn.headroom()
        cpu = h.get("cpu_pct")
        limit = max(1, cadence_learn.throttled_workers(per_beat)) if cpu is not None else per_beat
        try:
            r = sld.run_cadence(per_beat=limit)
            ok = bool(r.get("ok"))
            done = int(r.get("done") or 0)
            skipped = str(r.get("skipped") or "")
            line = f"beat#{beats} limit={limit} cpu={cpu} ok={ok} done={done} skip={skipped}"
            _log(line)
            print(f"[{_now()}] {line}")
            cadence_learn.learn({"cpu_pct": cpu, "workers": limit, "ok": ok})
        except Exception as e:  # noqa: BLE001
            _log(f"beat#{beats} ERROR {e}")
            print(f"[{_now()}] beat#{beats} ERROR {e}")

        if max_beats and beats >= max_beats:
            break
        hot = (cpu is not None and cpu >= cap)
        time.sleep(CADENCE_FLOOR_S + (CEILING_BACKOFF_S if hot else 0))


def status() -> dict:
    running, pid = False, None
    if LOCK.is_file():
        try:
            pid = int(LOCK.read_text(encoding="utf-8").strip())
            running = _pid_alive(pid)
        except Exception:  # noqa: BLE001
            pass
    last = None
    if LOG.is_file():
        lines = [l for l in LOG.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]
        last = lines[-1] if lines else None
    return {"ok": True, "running": running, "pid": pid, "last_beat": last}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    ap = argparse.ArgumentParser(prog="autodrain")
    ap.add_argument("cmd", nargs="?", default="run", choices=["run", "status"])
    ap.add_argument("--per-beat", type=int, default=8)
    ap.add_argument("--max-beats", type=int, default=0)
    a = ap.parse_args(argv)
    if a.cmd == "status":
        print(json.dumps(status(), indent=2))
        return 0
    run_loop(per_beat=a.per_beat, max_beats=a.max_beats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
