"""Repro: tools/stealth_driver.py _dispatch_hermes selffeed rc=1.

Byte-copies the resolution block from _dispatch_hermes
(tools/stealth_driver.py lines 261-278) and runs the exact subprocess it
runs, under the Mag venv python (what pythonw run_stealth_driver.py uses).
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")

# --- exact copy of the driver's resolution (lines 261-270) ---
hermes_python = sys.executable  # Hermes Python, already on PATH  (comment lies)
hermes_home = os.environ.get("HERMES_HOME", "")
if not hermes_home:
    hermes_home = str(Path(hermes_python).parent.parent)
hermes_agent = str(Path(hermes_home) / "hermes-agent")

os.environ["HERMES_HOME"] = hermes_home
os.environ["PYTHONPATH"] = hermes_agent
os.environ.pop("PYTHONHOME", None)

print("driver python (sys.executable):", hermes_python)
print("hermes_home:", hermes_home)
print("hermes_agent (PYTHONPATH):", hermes_agent)

r = subprocess.run(
    [hermes_python, "-m", "hermes_cli.main", "-z",
     "Reply with the single word OK."],
    capture_output=True, text=True, timeout=90,
    cwd=str(ROOT),
    creationflags=0x08000000,
    env=os.environ,
)
print("rc =", r.returncode)
print("stderr[:300]:", repr((r.stderr or "")[:300]))
print("stdout[-200:]:", repr((r.stdout or "")[-200:]))
