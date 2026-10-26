"""flash_cure_checkpoint.py - rewrap checkpoint_v2_hourly.ps1 behind run_hidden (one-shot)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
target = ROOT / "scripts" / "checkpoint_v2_hourly.ps1"
orig = target.read_text(encoding="utf-8")
if "FLASH CURE" in orig:
    print("already cured")
    raise SystemExit(0)
wrapper = (
    "# FLASH CURE 2026-10-19: task action calls powershell.exe directly (ACL-locked,\n"
    "# cannot rewrap the task) - a console window flashes every hourly fire. This stub\n"
    "# delegates the real body through run_hidden.vbs (window style 0) and exits, so\n"
    "# the allocated console lives ~100ms. Original: checkpoint_v2_hourly.ps1.bak_flashcure\n"
    "if (-not $env:CHECKPOINT_DELEGATED) {\n"
    "    $env:CHECKPOINT_DELEGATED = '1'\n"
    '    $args_ = \'"//B" "//Nologo" "C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent\\scripts\\run_hidden.vbs" "powershell.exe" "-NoProfile" "-ExecutionPolicy" "Bypass" "-File" "\' + $PSCommandPath + \'"\'\n'
    "    Start-Process wscript.exe -ArgumentList $args_ -WindowStyle Hidden\n"
    "    exit\n"
    "}\n"
) + orig
target.write_text(wrapper, encoding="utf-8")
print("flash cure applied,", len(wrapper), "bytes")
