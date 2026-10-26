# Runs the events-door check battery and banks raw output (command, stdout,
# stderr, exit) into events-door.check.txt.
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
LANES = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(LANES, "events-door.check.txt")
PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")

out = []


def run(label, args):
    out.append("$ " + label)
    p = subprocess.run(args, capture_output=True, text=True, cwd=ROOT)
    out.append(p.stdout)
    if p.stderr:
        out.append("[stderr]")
        out.append(p.stderr)
    out.append("[exit %d]" % p.returncode)
    out.append("")
    return p.returncode


exits = {}
exits["finishline"] = run(
    ".venv\\Scripts\\python.exe watch\\inbox\\gala_20260925\\wave5-repair\\lanes\\events-door.finishline.py",
    [PY, os.path.join(LANES, "events-door.finishline.py")])
exits["tests"] = run(
    ".venv\\Scripts\\python.exe -m pytest tests\\test_link_library.py -q",
    [PY, "-m", "pytest", "tests\\test_link_library.py", "-q"])
exits["ratchet"] = run(
    ".venv\\Scripts\\python.exe tools\\violation_ratchet.py check --changed",
    [PY, "tools\\violation_ratchet.py", "check", "--changed"])

with open(CHECK, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("exits:", exits)
print("banked ->", CHECK)
