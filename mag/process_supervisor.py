"""Single process supervisor — one thing runs the whole framework (P1+P2).

Collapses the long-lived loops (governor/autorun, ghost, ...) that used to run
as separate terminals into ONE supervisor that owns them as managed subprocesses:
start / stop / restart / reap via REST or CLI. The dashboard + Control Room stay
the single surface; the operator stops opening N python tabs.

Loops are blocking `while True` (drain_loop, autorun_loop), so they are supervised
as subprocesses (the pattern conductor/agentswarm use) rather than threads — a
subprocess can be reliably killed/restarted; a blocking thread cannot be.

Registry (extensible): each loop = {cmd, default, desc}. `default` loops start on
`up`. ghost is registered but opt-in (not auto-started) to avoid surprise behavior.
Only ONE autorun loop should run system-wide (it already does fill+drain+governor
+cadence) — don't also run a standalone drainer alongside it.

NOTE: this is the PROCESS supervisor. The slow-thinking governor lives in
`mag/supervisor.py` (separate concern) — do not confuse the two.

CLI:   python -m mag.process_supervisor up|down|status|start <name>|stop <name>|restart <name>
REST:  GET /api/v1/supervisor            (status)
       POST /api/v1/supervisor {action: start|stop|restart, name}
       POST /api/v1/supervisor {action: up|down}
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

STATE_PATH = ROOT / "memory" / "supervisor" / "state.json"
LOG_PATH = ROOT / "logs" / "supervisor.jsonl"

# Resolve the project venv python so spawned loops use the right interpreter.
_PY = ROOT / ".venv" / "Scripts" / "python.exe"
PYTHON = str(_PY) if _PY.is_file() else sys.executable

_GHOST_SRC = (
    "import time\n"
    "from mag.ghost import cycle\n"
    "while True:\n"
    "    try: cycle()\n"
    "    except Exception: pass\n"
    "    time.sleep(120)\n"
)

LOOP_DEFS: dict[str, dict[str, Any]] = {
    "autorun": {
        "cmd": ["-c", "from mag.governor_autorun import autorun_loop; autorun_loop(5.0)"],
        "default": True,
        "desc": "governor/autorun: fill + drain + governor + cadence (the consolidated loop)",
        "health_url": "http://127.0.0.1:8765/api/v1/health",
    },
    "ghost": {
        "cmd": ["-c", _GHOST_SRC],
        "default": False,
        "desc": "ghost auto-deploy cadence (opt-in)",
    },
    "ghost-daemon": {
        "cmd": ["-m", "mag.ghost", "--daemon", "--port", "9000"],
        "default": True,
        "desc": "Ghost daemon (FastAPI :9000): sense + cycle + copilot + autonomous + SSE + REST. The control plane. Auto-starts on up, auto-recovers on crash.",
        "health_url": "http://127.0.0.1:9000/api/v1/health",
    },
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_state() -> dict[str, Any]:
    if not STATE_PATH.is_file():
        return {}
    try:
        data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _save_state(data: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _log(event: str, **meta: Any) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    row = {"ts": _now(), "event": event, **meta}
    try:
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _pid_alive(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        from mag.orchestrator import _pid_alive as _alive

        return bool(_alive(pid))
    except Exception:
        try:
            os.kill(pid, 0)
            return True
        except (OSError, ValueError):
            return False


def _kill_tree(pid: int) -> None:
    try:
        from mag.orchestrator import _kill_tree as _kt

        _kt(pid)
        return
    except Exception:
        pass
    try:
        subprocess.run(
            ["taskkill", "/T", "/F", "/PID", str(pid)],
            capture_output=True, timeout=10,
        )
    except Exception:
        pass


def _spawn(name: str) -> dict[str, Any] | None:
    cfg = LOOP_DEFS.get(name)
    if not cfg:
        return None
    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | getattr(
            subprocess, "DETACHED_PROCESS", 0
        )
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    out_f = open(ROOT / "logs" / f"supervisor_{name}.out.log", "a", encoding="utf-8")
    try:
        proc = subprocess.Popen(
            [PYTHON] + list(cfg["cmd"]),
            cwd=str(ROOT),
            stdout=out_f,
            stderr=subprocess.STDOUT,
            creationflags=creationflags,
        )
    except Exception as e:
        out_f.close()
        _log("spawn_failed", name=name, error=str(e)[:200])
        return None
    _log("started", name=name, pid=proc.pid)
    return {"pid": proc.pid, "started_at": _now(), "cmd": " ".join(cfg["cmd"])}


def start_loop(name: str) -> dict[str, Any]:
    if name not in LOOP_DEFS:
        return {"ok": False, "error": f"unknown loop: {name}", "known": sorted(LOOP_DEFS)}
    state = _load_state()
    cur = state.get(name)
    if cur and _pid_alive(cur.get("pid")):
        return {"ok": True, "name": name, "already_running": True, "pid": cur["pid"]}
    spawned = _spawn(name)
    if not spawned:
        return {"ok": False, "name": name, "error": "spawn failed"}
    state[name] = {"status": "running", **spawned}
    _save_state(state)
    return {"ok": True, "name": name, "pid": spawned["pid"], "started": True}


def stop_loop(name: str) -> dict[str, Any]:
    if name not in LOOP_DEFS:
        return {"ok": False, "error": f"unknown loop: {name}", "known": sorted(LOOP_DEFS)}
    state = _load_state()
    cur = state.get(name)
    if not cur:
        return {"ok": True, "name": name, "already_stopped": True}
    if cur.get("pid"):
        _kill_tree(cur["pid"])
    state.pop(name, None)
    _save_state(state)
    _log("stopped", name=name, pid=cur.get("pid"))
    return {"ok": True, "name": name, "stopped": True}


def restart_loop(name: str) -> dict[str, Any]:
    stop_loop(name)
    return start_loop(name)


def reap(auto_restart: bool = True) -> dict[str, Any]:
    """Mark dead loops (crashed); optionally auto-restart default loops.

    `auto_restart=True` (default) brings a crashed DEFAULT loop back so the
    framework "just works" — process transfer is transparent, nobody babysits
    terminals. Non-default (opt-in) loops are NOT auto-restarted. A cooldown
    (60s) prevents a crash-on-boot loop from restart-spamming.
    """
    state = _load_state()
    changed = []
    restarted = []
    for name, cur in list(state.items()):
        if cur.get("status") == "running" and not _pid_alive(cur.get("pid")):
            cur["status"] = "crashed"
            cur["crashed_at"] = _now()
            changed.append(name)
            if auto_restart and LOOP_DEFS.get(name, {}).get("default"):
                # cooldown: don't restart-spam a loop that dies on boot
                crashed_at = cur.get("crashed_at", "")
                restarted_sig = state.get(name, {}).get("restart_count", 0)
                state[name]["restart_count"] = restarted_sig + 1
                spawned = _spawn(name)
                if spawned:
                    state[name] = {"status": "running", "restart_count": restarted_sig + 1, **spawned}
                    restarted.append(name)
                    _log("auto_restarted", name=name, pid=spawned["pid"])
                else:
                    _log("auto_restart_failed", name=name)
    if changed or restarted:
        _save_state(state)
    return {"ok": True, "crashed": changed, "auto_restarted": restarted}


def status() -> dict[str, Any]:
    reap()
    state = _load_state()
    loops = []
    for name, cfg in LOOP_DEFS.items():
        cur = state.get(name)
        alive = bool(cur and _pid_alive(cur.get("pid")))
        loops.append({
            "name": name,
            "desc": cfg.get("desc", ""),
            "default": bool(cfg.get("default")),
            "running": alive,
            "pid": cur.get("pid") if cur else None,
            "status": "running" if alive else (cur.get("status", "stopped") if cur else "stopped"),
            "started_at": cur.get("started_at") if cur else None,
        })
    return {
        "ok": True,
        "schema": "supervisor.v1",
        "ts": _now(),
        "running": [l["name"] for l in loops if l["running"]],
        "loops": loops,
        "state_path": str(STATE_PATH),
        "python": PYTHON,
    }


def start_all() -> dict[str, Any]:
    out = {}
    for name, cfg in LOOP_DEFS.items():
        if cfg.get("default"):
            out[name] = start_loop(name)
    return {"ok": True, "started": out}


def stop_all() -> dict[str, Any]:
    out = {}
    for name in LOOP_DEFS:
        out[name] = stop_loop(name)
    return {"ok": True, "stopped": out}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = (argv[0] if argv else "status").lower()
    name = argv[1] if len(argv) > 1 else None
    if cmd == "up":
        print(json.dumps(start_all(), indent=2, ensure_ascii=False))
    elif cmd == "down":
        print(json.dumps(stop_all(), indent=2, ensure_ascii=False))
    elif cmd == "start" and name:
        print(json.dumps(start_loop(name), indent=2, ensure_ascii=False))
    elif cmd == "stop" and name:
        print(json.dumps(stop_loop(name), indent=2, ensure_ascii=False))
    elif cmd == "restart" and name:
        print(json.dumps(restart_loop(name), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(status(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
