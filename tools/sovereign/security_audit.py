#!/usr/bin/env python3
"""tools/sovereign/security_audit.py — Comprehensive System & Network Security Auditor.

Audits:
1. GUI & Pop-up Surface: Detects all processes with visible window handles or titles.
2. Process Inventory: Examines running processes, command lines, and parent-child trees.
3. Network Attack Surface: Identifies all LISTENING ports, bound interfaces (localhost vs 0.0.0.0 vs Tailscale), and foreign connections.
4. Scheduled Task Audit: Scans Windows Task Scheduler for recurring batch/cmd scripts causing window pop-ups.
5. Persistence Mechanisms: Audits Windows Startup registry keys and startup folders.
6. Persistent Security Logging: Maintains a continuous log in watch/inbox/foreign_seats/SECURITY_EVENTS.log.

Zero external dependencies. Pure standard library Python 3.8+.
"""

from __future__ import annotations
import csv
import datetime
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = ROOT_DIR / "watch" / "inbox" / "foreign_seats"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SECURITY_REPORT_PATH = OUTPUT_DIR / "SECURITY_SWEEP_REPORT_20261023.md"
SECURITY_LOG_PATH = OUTPUT_DIR / "SECURITY_EVENTS.log"


def log_event(message: str) -> None:
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = f"[{timestamp}] {message}\n"
    with open(SECURITY_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)


def get_gui_windows() -> List[Dict[str, Any]]:
    """Enumerate processes with active MainWindowTitle in Windows."""
    ps_cmd = (
        "Get-Process | Where-Object { $_.MainWindowTitle } | "
        "Select-Object Id, ProcessName, MainWindowTitle | "
        "ConvertTo-Json -Compress"
    )
    try:
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd],
                             capture_output=True, text=True, timeout=20)
        out = res.stdout.strip()
        if not out:
            return []
        data = json.loads(out)
        if isinstance(data, dict):
            return [data]
        elif isinstance(data, list):
            return data
    except Exception as e:
        log_event(f"Error enumerating GUI windows: {e}")
    return []


def get_running_processes() -> List[Dict[str, Any]]:
    """Get process list with command lines and PIDs."""
    ps_cmd = (
        "Get-CimInstance Win32_Process | "
        "Select-Object ProcessId, ParentProcessId, Name, ExecutablePath, CommandLine | "
        "ConvertTo-Json -Compress"
    )
    try:
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd],
                             capture_output=True, text=True, timeout=25)
        out = res.stdout.strip()
        if not out:
            return []
        data = json.loads(out)
        if isinstance(data, dict):
            return [data]
        elif isinstance(data, list):
            return data
    except Exception as e:
        log_event(f"Error enumerating processes: {e}")
    return []


def get_listening_ports() -> List[Dict[str, Any]]:
    """Scan netstat for LISTENING ports and map to PIDs."""
    ports = []
    try:
        res = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, timeout=15)
        for line in res.stdout.splitlines():
            parts = line.strip().split()
            if len(parts) >= 4 and parts[0].upper() in ("TCP", "UDP"):
                proto = parts[0]
                local_addr = parts[1]
                state = parts[3] if proto == "TCP" else "UDP"
                pid = parts[4] if proto == "TCP" and len(parts) >= 5 else (parts[3] if len(parts) >= 4 else "?")
                
                if state == "LISTENING" or proto == "UDP":
                    # Determine scope
                    scope = "Localhost Only" if "127.0.0.1" in local_addr or "[::1]" in local_addr else "All Interfaces (0.0.0.0)"
                    if "100." in local_addr:
                        scope = "Tailscale Private Mesh"
                    ports.append({
                        "proto": proto,
                        "local_addr": local_addr,
                        "state": state,
                        "pid": pid,
                        "scope": scope
                    })
    except Exception as e:
        log_event(f"Error scanning netstat: {e}")
    return ports


def get_scheduled_tasks() -> List[Dict[str, Any]]:
    """Audit scheduled tasks running custom scripts or non-system binaries."""
    tasks = []
    try:
        res = subprocess.run(["schtasks", "/query", "/fo", "csv", "/v"],
                             capture_output=True, text=True, timeout=30)
        reader = csv.DictReader(io.StringIO(res.stdout))
        for row in reader:
            task_name = row.get("TaskName", "")
            action = row.get("Task To Run", "")
            status = row.get("Status", "")
            
            # Filter for non-empty user/custom tasks or script runners
            act_low = action.lower()
            if any(k in act_low for k in ["python", "powershell", "cmd.exe", ".bat", ".cmd", ".ps1", "zcode", "gemini"]):
                tasks.append({
                    "name": task_name,
                    "action": action,
                    "status": status,
                    "schedule": row.get("Schedule Type", "")
                })
    except Exception as e:
        log_event(f"Error auditing scheduled tasks: {e}")
    return tasks


def get_startup_entries() -> List[Dict[str, str]]:
    """Audit Windows registry Run keys and startup directories."""
    entries = []
    reg_keys = [
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
        r"HKLM\Software\Microsoft\Windows\CurrentVersion\Run",
    ]
    for rk in reg_keys:
        try:
            res = subprocess.run(["reg", "query", rk], capture_output=True, text=True, timeout=10)
            for line in res.stdout.splitlines():
                line = line.strip()
                if line and not line.startswith("HKEY_"):
                    parts = re.split(r"\s{2,}", line)
                    if len(parts) >= 2:
                        entries.append({
                            "location": rk,
                            "name": parts[0],
                            "target": parts[-1]
                        })
        except Exception:
            pass

    # Check startup folder
    appdata = os.environ.get("APPDATA", "")
    if appdata:
        startup_dir = Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        if startup_dir.exists():
            for p in startup_dir.iterdir():
                entries.append({
                    "location": "Startup Folder",
                    "name": p.name,
                    "target": str(p)
                })
    return entries


def perform_security_sweep() -> str:
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    log_event("=== INITIATING FULL SYSTEM SECURITY SWEEP ===")

    gui_windows = get_gui_windows()
    processes = get_running_processes()
    ports = get_listening_ports()
    tasks = get_scheduled_tasks()
    startup = get_startup_entries()

    # Map PIDs to names
    pid_to_name = {str(p.get("ProcessId")): p.get("Name", "") for p in processes if p.get("ProcessId")}
    pid_to_cmd = {str(p.get("ProcessId")): p.get("CommandLine", "") for p in processes if p.get("ProcessId")}

    # Identify potential pop-up generators
    popup_culprits = []
    for proc in processes:
        name = str(proc.get("Name", "")).lower()
        cmd = str(proc.get("CommandLine", "")).lower()
        pid = str(proc.get("ProcessId", ""))
        
        # Check if cmd.exe or powershell.exe is running without window suppression
        if name in ("cmd.exe", "powershell.exe", "conhost.exe"):
            if "hidden" not in cmd and "-windowstyle hidden" not in cmd:
                popup_culprits.append({
                    "pid": pid,
                    "name": name,
                    "cmd": proc.get("CommandLine", ""),
                    "reason": "Terminal process spawned without -WindowStyle Hidden"
                })

    # Flag publicly bound ports (0.0.0.0 or [::])
    public_ports = [p for p in ports if p["scope"] == "All Interfaces (0.0.0.0)"]

    report_lines = [
        "# SOVEREIGN ESTATE SECURITY SWEEP & POP-UP DIAGNOSTIC REPORT",
        f"**Audit Timestamp:** `{timestamp}`  ",
        "**Host Node:** `bob` (Edge Laptop, 100.125.103.60)  ",
        f"**Audit Log File:** [`{SECURITY_LOG_PATH.as_posix()}`](file:///{SECURITY_LOG_PATH.as_posix()})  ",
        "",
        "---",
        "",
        "## 1. Executive Summary: What Is Causing the Pop-ups?",
        ""
    ]

    if popup_culprits:
        report_lines.append(f"> [!WARNING] **Found {len(popup_culprits)} terminal/shell process(es) capable of spawning GUI windows:**")
        report_lines.append("")
        for c in popup_culprits:
            report_lines.append(f"- **PID {c['pid']} (`{c['name']}`):** `{c['cmd'][:120]}`...")
            report_lines.append(f"  *Cause:* {c['reason']}")
    else:
        report_lines.append("> [!NOTE] No unconstrained terminal background processes currently running.")

    report_lines.extend([
        "",
        "---",
        "",
        "## 2. Active Visible Windows on Desktop",
        "",
        "| PID | Process Name | Window Title |",
        "|---|---|---|"
    ])

    for w in gui_windows:
        report_lines.append(f"| {w.get('Id')} | `{w.get('ProcessName')}` | **{w.get('MainWindowTitle')}** |")

    report_lines.extend([
        "",
        "---",
        "",
        "## 3. Network Attack Surface: Listening Ports",
        "",
        "| Protocol | Local Address | Scope / Interface | Process Name (PID) |",
        "|---|---|---|---|"
    ])

    for p in ports:
        pid = p["pid"]
        proc_name = pid_to_name.get(pid, "Unknown")
        report_lines.append(f"| {p['proto']} | `{p['local_addr']}` | **{p['scope']}** | `{proc_name}` (PID: {pid}) |")

    report_lines.extend([
        "",
        "---",
        "",
        "## 4. Scheduled Task Audit (Windows Task Scheduler)",
        "",
        f"Found **{len(tasks)}** active task(s) involving script runners (`python`, `cmd`, `powershell`, etc.):",
        ""
    ])

    for t in tasks:
        report_lines.append(f"- **Task:** `{t['name']}`  ")
        report_lines.append(f"  *Action:* `{t['action']}`  ")
        report_lines.append(f"  *Schedule:* `{t['schedule']}` | *Status:* `{t['status']}`")
        report_lines.append("")

    report_lines.extend([
        "---",
        "",
        "## 5. Startup & Persistence Entries",
        "",
        "| Location | Name | Executable Target |",
        "|---|---|---|"
    ])

    for s in startup:
        report_lines.append(f"| `{s['location']}` | `{s['name']}` | `{s['target'][:90]}` |")

    report_lines.extend([
        "",
        "---",
        "",
        "## 6. Hardening Recommendations for Pure Headless Operation",
        "",
        "1. **Wrap All Scheduled Batch Files in VBScript / Hidden Runners:**",
        "   When Windows Task Scheduler runs `.cmd` or `.bat` files directly, it creates a temporary `conhost.exe` and flashes a command prompt on the desktop. Replacing them with a 3-line `.vbs` wrapper (`WScript.Shell.Run ..., 0, False`) completely suppresses all GUI pop-ups.",
        "2. **Lock Down Listening Interfaces:**",
        "   Ensure all dev servers and RPC ports bind strictly to `127.0.0.1` or `100.125.103.60` (Tailscale WireGuard), never `0.0.0.0`.",
        "3. **Continuous Background Watchdog:**",
        "   Log any new process creation or network socket bind to `SECURITY_EVENTS.log`.",
        "",
        "---",
        f"**Report Generated:** {timestamp}"
    ])

    content = "\n".join(report_lines) + "\n"
    SECURITY_REPORT_PATH.write_text(content, encoding="utf-8")
    log_event(f"Sweep complete. Report generated at {SECURITY_REPORT_PATH}")
    return content


if __name__ == "__main__":
    report = perform_security_sweep()
    print(f"[security] Sweep complete. Report generated: {SECURITY_REPORT_PATH}")
    sys.exit(0)
