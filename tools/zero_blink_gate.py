#!/usr/bin/env python3
"""ZERO-BLINK GATE - the headless law, enforced at the machine layer.

Law (operator, headless doctrine): a scheduled task that creates a
console window steals the operator's attention. The estate's product is
attention sovereignty; a popup is the Q inversion running INSIDE the
house. -WindowStyle Hidden does NOT count: Windows creates the console
first and hides it after - the blink survives. Only a wscript launch
wrapper (scripts/run_hidden.vbs pattern) never creates a window.

Audit mode (default): enumerate all non-Disabled scheduled tasks, flag
any action whose Execute is a console host not routed through
wscript.exe. Exit 0 clean, exit 2 violations (estate gate convention).
Prints the exact rewrap command per violation so the fix is paste-ready.

Falsifier: any violation present while this patrol runs green means the
gate is dead - the gate is the law's body, not the prose.

Consumer: task-registration discipline for every seat (self included);
wired as MagZeroBlinkPatrol (daily, itself zero-blink by construction).
Verifier: this file + the patrol task it registers.
"""
from __future__ import annotations

import subprocess
import sys

PS_SCRIPT = (
    "Get-ScheduledTask | Where-Object {$_.State -ne 'Disabled'} | "
    "ForEach-Object { $t = $_; foreach ($a in $t.Actions) { "
    "if ($a.Execute) { Write-Output ($t.TaskPath + '|' + $t.TaskName + "
    "'|' + $a.Execute + '|' + $a.Arguments) } } }"
)

CONSOLE_HOSTS = {
    "powershell.exe", "pwsh.exe", "cmd.exe", "python.exe",
    "node.exe", "conda.exe", "bash.exe", "wsl.exe", "cscript.exe",
}
# pythonw.exe is the GUI-subsystem python: windowless by design, same
# class as wscript - it is a compliant wrapper, not a violation
CONSOLE_EXT = {".cmd", ".bat", ".ps1", ".py", ".js"}
WRAPPERS = ("wscript.exe", "mshta.exe")

RUN_HIDDEN = (
    "C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent"
    "\\scripts\\run_hidden.vbs"
)


def audit() -> int:
    out = subprocess.run(
        ["powershell", "-NoProfile", "-Command", PS_SCRIPT],
        capture_output=True, text=True, shell=False, timeout=120)
    violations = []
    total = 0
    for line in out.stdout.splitlines():
        parts = line.split("|", 3)
        if len(parts) != 4:
            continue
        path, name, exe, args = parts
        if path.startswith("\\Microsoft"):
            continue  # windows-owned machinery, not the estate's
        total += 1
        base = exe.strip().strip('"').rsplit("\\", 1)[-1].lower()
        ext = ("." + base.rsplit(".", 1)[-1]) if "." in base else ""
        if base in WRAPPERS:
            continue
        if base in CONSOLE_HOSTS or ext in CONSOLE_EXT:
            violations.append((name, exe, args))
    print(f"zero-blink audit: {total} estate tasks scanned, "
          f"{len(violations)} violations")
    for name, exe, args in violations:
        print(f"  VIOLATION {name}: [{exe} {args[:80]}]")
        print(f'    fix: schtasks /Change /TN "{name}" /TR '
              f'"wscript.exe //B //Nologo {RUN_HIDDEN} {exe} {args}"')
    if violations:
        print("ZERO-BLINK FAIL: headed tasks exist; attention was stolen")
        return 2
    print("ZERO-BLINK PASS: the fleet is invisible")
    return 0


if __name__ == "__main__":
    sys.exit(audit())
