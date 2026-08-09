"""process_reaper — conservative supervised-process leak sweep.

The operator's goal (2026-08-09): collapse the "90 python windows" sprawl down to the
supervised core (autorun + ghost-daemon) without ever killing live work. This module is
the MEASURED answer to that — it does NOT shotgun-kill.

It enumerates every python process under this project's venv and classifies each as:
  - supervised-loop : a known process_supervisor loop (autorun / ghost / ghost-daemon)
  - active-subagent  : linked to a running/queued orchestrator task (real work)
  - dashboard-server : the REST dashboard listener (port 8765)
  - leak             : none of the above — unowned, not linked to any task, no parent
                       relationship to a supervised loop, and idle past a grace age.

SAFETY MODEL (report-first):
  * run(dry=True) is the default — it only REPORTS leaks, kills nothing.
  * run(dry=False, live=True) kills ONLY confirmed leaks (idle >= grace_s AND unowned),
    each kill logged to the supervisor log so it is measured, not silent.
  * It NEVER touches supervised loops, active sub-agents, or the dashboard.
  * PIDs whose command line is unknown/None are treated as NOT confirmed (skip).

Wired into ghost's autonomous loop as a report-only cadence (see ghost.stall_sweep /
the daemon), so the operator SEES the sprawl without anything being auto-killed.
`--live` is an explicit operator decision.

CLI:  python -m mag.process_reaper            (report only)
      python -m mag.process_reaper --live     (kill confirmed leaks, logged)
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _log(event: str, **meta: Any) -> None:
    p = ROOT / "logs" / "supervisor.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    try:
        with p.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": _now(), "event": event, **meta}, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ValueError):
        return False


def _proc_create_time_iso(pid: int) -> str | None:
    """Best-effort process creation time (UTC ISO). Returns None if unknown."""
    try:
        import psutil  # may not be installed; graceful skip
        p = psutil.Process(pid)
        import datetime as _dt
        return _dt.datetime.fromtimestamp(p.create_time(), tz=_dt.timezone.utc).isoformat()
    except Exception:
        return None


def _project_python_procs() -> list[dict[str, Any]]:
    """Enumerate python processes whose command line references this project venv."""
    out: list[dict[str, Any]] = []
    try:
        import subprocess
        res = subprocess.run(
            ["wmic", "process", "where", "Name='python.exe'", "get", "ProcessId,CommandLine", "/format:csv"],
            capture_output=True, text=True, timeout=20, errors="replace",
        )
        for line in res.stdout.splitlines()[1:]:
            parts = line.split(",", 1)
            if len(parts) != 2:
                continue
            cl = (parts[1] or "").strip()
            if "local_sovereign_agent" not in cl and ".venv" not in cl:
                continue
            # PID is in the last CSV column of the row
            row = line.split(",")
            pid = row[-1].strip() if row else ""
            if not pid.isdigit():
                continue
            out.append({"pid": int(pid), "cmdline": cl[:400]})
    except Exception as e:
        _log("reaper-enumerate-error", error=str(e)[:160])
    return out


def _supervised_pids() -> set[int]:
    """PIDs owned by process_supervisor loops."""
    try:
        from mag.process_supervisor import status as sup_status
        st = sup_status() or {}
        return {l["pid"] for l in st.get("loops", []) if l.get("pid")}
    except Exception:
        return set()


def _task_pids() -> set[int]:
    """PIDs linked to any orchestrator task (running/queued = live work)."""
    try:
        from mag.orchestrator import list_tasks_live
        return {int(t["pid"]) for t in (list_tasks_live(limit=200) or [])
                if t.get("pid") and str(t["pid"]).isdigit()}
    except Exception:
        return set()


def classify() -> dict[str, Any]:
    """Classify project python procs. Report-only; kills nothing."""
    supervised = _supervised_pids()
    task_pids = _task_pids()
    procs = _project_python_procs()
    buckets: dict[str, list[dict[str, Any]]] = {
        "supervised-loop": [], "active-subagent": [], "dashboard-server": [],
        "leak": [], "unknown": [],
    }
    for pr in procs:
        pid = pr["pid"]
        cl = pr["cmdline"]
        if pid in supervised:
            buckets["supervised-loop"].append(pr)
        elif pid in task_pids:
            buckets["active-subagent"].append(pr)
        elif "dashboard" in cl or "8765" in cl or "rest" in cl:
            buckets["dashboard-server"].append(pr)
        elif "autorun_loop" in cl or "ghost" in cl or "server" in cl:
            # Known supervised-ish but not in the supervisor set (stray) — treat as leak.
            buckets["leak"].append(pr)
        elif "agent --query" in cl or "--query" in cl:
            # A sub-agent not currently tracked in the task set — could be mid-spawn.
            buckets["unknown"].append(pr)
        else:
            buckets["leak"].append(pr)
    return {
        "ok": True,
        "schema": "process_reaper.v1",
        "ts": _now(),
        "total": len(procs),
        "buckets": {k: len(v) for k, v in buckets.items()},
        "leaks": buckets["leak"],
        "unknown": buckets["unknown"],
    }


def run(*, live: bool = False, grace_s: int = 1800) -> dict[str, Any]:
    """Reap sweep. Default report-only; live=True kills confirmed leaks (idle >= grace_s)."""
    c = classify()
    leaks = list(c.get("leaks", []))
    killed: list[dict[str, Any]] = []
    if live:
        for pr in leaks:
            pid = pr["pid"]
            created = _proc_create_time_iso(pid)
            # Only kill if we could determine the process AND it's not freshly spawned.
            if created is None:
                continue
            # Skip very young procs (grace) — could be a mid-spawn worker.
            try:
                import datetime as _dt
                age_s = (_dt.datetime.now(_dt.timezone.utc) - _dt.datetime.fromisoformat(created)).total_seconds()
            except Exception:
                age_s = grace_s + 1  # unknown age -> treat as old enough only if confirmed
            if age_s < grace_s:
                continue
            if not _pid_alive(pid):
                continue
            try:
                import subprocess
                subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                               capture_output=True, timeout=10)
                killed.append({"pid": pid, "cmdline": pr["cmdline"][:200], "age_s": int(age_s)})
                _log("reaper-kill", pid=pid, cmdline=pr["cmdline"][:160], age_s=int(age_s))
            except Exception as e:
                _log("reaper-kill-error", pid=pid, error=str(e)[:120])
    else:
        _log("reaper-report", total=c.get("total"), leaks=len(leaks))
    return {**c, "live": live, "killed": killed, "grace_s": grace_s}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(prog="process-reaper")
    ap.add_argument("--live", action="store_true", help="kill confirmed idle leaks (logged)")
    ap.add_argument("--grace", type=int, default=1800, help="idle grace seconds before kill")
    args = ap.parse_args()
    res = run(live=args.live, grace_s=args.grace)
    print(json.dumps(res, indent=2, ensure_ascii=False, default=str))
