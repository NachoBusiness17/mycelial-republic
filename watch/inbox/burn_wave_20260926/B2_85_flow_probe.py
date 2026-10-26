"""B2-85 flow probe: re-run the calling flows of every module whose bare
"powershell" call was fixed (tools/shell.py + 8 mag modules, 10 sites).
Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_85_flow_probe.py
Writes B2_85_flow_probe_results.json next to itself. Read-only flows only,
except one drop_shortcut probe whose .lnk is created then deleted (disclosed).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

results: dict[str, object] = {}


def check(name: str, fn):
    try:
        results[name] = {"ok": True, "value": fn()}
    except Exception as e:
        results[name] = {"ok": False, "error": f"{type(e).__name__}: {e}"[:300]}


# 1. root tool: tools/shell.py run_shell (the sig run_shell:e566037def80 source)
def _run_shell():
    from tools.shell import run_shell
    r = run_shell("echo B2_85_PROBE_OK")
    return {"ok": r.get("ok"), "exit_code": r.get("exit_code"),
            "marker_in_output": "B2_85_PROBE_OK" in (r.get("output") or ""),
            "error": r.get("error")}
check("tools_shell_run_shell", _run_shell)


# 2. mag/gpu_ghost.py _amd_windows + gpu_status (read-only telemetry)
def _amd():
    from mag.gpu_ghost import _amd_windows, gpu_status
    return {"amd": _amd_windows(), "status_source": gpu_status().get("source")}
check("gpu_ghost", _amd)


# 3. mag/offerings.py status() (read-only)
def _offerings():
    from mag.offerings import status
    s = status()
    return {"ok": s.get("ok"), "n_bodies": s.get("n_bodies")}
check("offerings_status", _offerings)


# 4. mag/saelis_room.py _live_processes (read-only)
def _saelis():
    from mag.saelis_room import _live_processes
    rows = _live_processes()
    errs = [r for r in rows if isinstance(r, dict) and "error" in r]
    return {"rows": len(rows), "errors": errs}
check("saelis_room_live_processes", _saelis)


# 5. mag/power.py both fixed sites (read-only pid reads)
def _power():
    from mag import power
    return {"mag_pids": sorted(power._mag_python_pids()),
            "self_ancestor_contains_pid": os.getpid() in power._self_ancestor_pids()}
check("power_pid_reads", _power)


# 6. mag/platform_kill.py kill_all(dry=True) (plan only, kills nothing)
def _pk():
    from mag.platform_kill import kill_all
    out = kill_all(dry=True)
    return {"dry": out.get("dry", True), "targets": len(out.get("targets", out.get("kills", []) or [])),
            "keys": sorted(out.keys())[:8]}
check("platform_kill_dry", _pk)


# 7. mag/loop_breaker.py detect() + break_loop(dry=True) (read-only / dry)
def _lb():
    from mag.loop_breaker import break_loop, detect
    d = detect()
    b = break_loop(dry=True)
    return {"detect_keys": sorted(d.keys())[:8], "break_dry": b.get("dry", True)}
check("loop_breaker", _lb)


# 8. mag/legacy_audit.py scan() (read-only)
def _la():
    from mag.legacy_audit import scan
    s = scan()
    return {"keys": sorted(s.keys())[:8] if isinstance(s, dict) else str(type(s))}
check("legacy_audit_scan", _la)


# 9. forced psutil-ImportError branches (the code paths that hold 3 fixed sites)
def _forced_import_error():
    import mag.gpu_ghost as gg  # noqa: F401  (import check only)
    saved = sys.modules.get("psutil")
    sys.modules["psutil"] = None  # forces ImportError at "import psutil"
    try:
        from mag import legacy_audit, loop_breaker, platform_kill
        la = legacy_audit._enum_procs()
        pk = platform_kill._enum_host_pids()
        lb = loop_breaker._enum()
    finally:
        if saved is None:
            sys.modules.pop("psutil", None)
        else:
            sys.modules["psutil"] = saved
    blob = json.dumps({"la": la[:3], "pk": pk[:3], "lb": lb[:3]}, default=str)
    return {"la_rows": len(la), "pk_rows": len(pk), "lb_rows": len(lb),
            "errno2_in_output": "Errno 2" in blob}
check("forced_import_error_branches", _forced_import_error)


# 10. mag/icon_drop.py drop_shortcut end-to-end (lnk created then deleted)
def _icon():
    from mag.icon_drop import drop_shortcut
    row = drop_shortcut("B2_85_probe_lnk", str(ROOT / ".venv" / "Scripts" / "python.exe"),
                        desc="B2-85 probe, self-removing")
    lnk = Path(row.get("path") or "")
    existed = lnk.is_file()
    if existed:
        lnk.unlink()
    return {"status": row.get("status"), "lnk_existed": existed,
            "cleaned_up": not lnk.is_file()}
check("icon_drop_shortcut", _icon)


out_path = Path(__file__).with_name("B2_85_flow_probe_results.json")
out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
all_ok = all(r.get("ok") for r in results.values() if isinstance(r, dict))
print(json.dumps({"all_ok": all_ok, "checks": {k: v.get("ok") for k, v in results.items()}},
                 indent=2))
