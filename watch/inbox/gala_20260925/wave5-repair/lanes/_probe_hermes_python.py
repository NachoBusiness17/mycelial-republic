"""Probe: does the hermes-agent venv python return real stdout for -z?

This is the candidate hermes_python for the _dispatch_hermes fix.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
HERMES_HOME = Path(r"C:\Users\foste\AppData\Local\hermes")
AGENT = HERMES_HOME / "hermes-agent"

py = str(AGENT / "venv" / "Scripts" / "python.exe")
env = dict(os.environ)
env["HERMES_HOME"] = str(HERMES_HOME)
env["PYTHONPATH"] = str(AGENT)
env.pop("PYTHONHOME", None)

print("venv python:", py, "exists:", Path(py).is_file())
print("venv version:", subprocess.run([py, "--version"], capture_output=True,
                                      text=True).stdout.strip())
t0 = time.time()
r = subprocess.run(
    [py, "-m", "hermes_cli.main", "-z",
     "Reply with the single word OK. Use no tools."],
    capture_output=True, text=True, timeout=240,
    cwd=str(ROOT), creationflags=0x08000000, env=env,
)
dt = time.time() - t0
print(f"rc = {r.returncode}  dt = {dt:.1f}s")
print("stdout[:400]:", repr((r.stdout or "")[:400]))
print("stderr[:300]:", repr((r.stderr or "")[:300]))
