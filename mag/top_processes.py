"""top_processes — the bug-hunt STARTS here: top CPU/memory processes for ghost sense.

Operator (2026-08-11): "in the past we bug hunted and never went to the top processes with ghost
sense so we should start that way moving forward." Standing rule: when errors appear (lower-right
toasts), check TOP PROCESSES FIRST via ghost sense, then descend into files.

Adapted from the standard process-monitoring pattern (psutil top). Deterministic + graceful:
if psutil is missing, returns an honest error (no crash). Schema: top_processes.v1
"""
from __future__ import annotations

from typing import Any

SCHEMA = "top_processes.v1"


def top_cpu(n: int = 8) -> list[dict[str, Any]]:
    """Top N processes by CPU percent (the 'top' view). Deterministic snapshot."""
    import psutil  # noqa: F401
    rows = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "cmdline"]):
        try:
            rows.append({"pid": p.info["pid"], "name": p.info["name"] or "?",
                         "cpu": round(p.info["cpu_percent"] or 0.0, 2),
                         "mem": round(p.info["memory_percent"] or 0.0, 2),
                         "cmd": " ".join((p.info["cmdline"] or [])[:3])[:60]})
        except Exception:
            continue
    rows.sort(key=lambda r: -r["cpu"])
    return rows[:max(1, int(n))]


def top_memory(n: int = 8) -> list[dict[str, Any]]:
    """Top N processes by memory percent."""
    import psutil  # noqa: F401
    rows = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "cmdline"]):
        try:
            rows.append({"pid": p.info["pid"], "name": p.info["name"] or "?",
                         "cpu": round(p.info["cpu_percent"] or 0.0, 2),
                         "mem": round(p.info["memory_percent"] or 0.0, 2),
                         "cmd": " ".join((p.info["cmdline"] or [])[:3])[:60]})
        except Exception:
            continue
    rows.sort(key=lambda r: -r["mem"])
    return rows[:max(1, int(n))]


def top_processes(n: int = 8) -> dict[str, Any]:
    """The bug-hunt entry surface: top CPU + top memory + host totals. Graceful if psutil missing."""
    try:
        import psutil  # noqa: F401
    except Exception as e:
        return {"ok": False, "schema": SCHEMA, "error": f"psutil required: {str(e)[:120]}"}
    cpu = top_cpu(n)
    mem = top_memory(n)
    return {"ok": True, "schema": SCHEMA, "n": len(cpu), "top_cpu": cpu, "top_memory": mem}


def main(argv: list[str] | None = None) -> int:
    import json, sys
    print(json.dumps(top_processes(), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
