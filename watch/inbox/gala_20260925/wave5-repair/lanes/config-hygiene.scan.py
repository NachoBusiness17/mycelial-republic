"""config-hygiene lane hygiene scan v2 (gala wave5-repair, 2026-09-29).

Precise instrument:
  1. Authored prose/code files: em/en dash + nonascii must be 0/0.
     config-hygiene.check.txt is EXEMPT from the 0/0 rule and REPORTED
     separately: it is a byte-faithful raw capture whose dashes belong to the
     captured tools themselves (tools/config_seal.py prints em-dashes in its
     PASS/FAIL lines). Raw-output fidelity outranks the dash law there.
  2. For the two edited code files, scan ONLY the lines this lane ADDED
     (git diff vs HEAD, '+' lines): em/en dash + nonascii must be 0.

Run: .venv/Scripts/python.exe watch/inbox/gala_20260925/wave5-repair/lanes/config-hygiene.scan.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
DASHES = ("\u2013", "\u2014")

authored = [
    ROOT / "watch/inbox/wave5_repair/config-hygiene.md",
    ROOT / "watch/inbox/gala_20260925/wave5-repair/lanes/config-hygiene.json",
    ROOT / "watch/inbox/gala_20260925/wave5-repair/lanes/config-hygiene.check.py",
    ROOT / "watch/inbox/gala_20260925/wave5-repair/lanes/config-hygiene.check_driver.py",
    ROOT / "watch/inbox/gala_20260925/wave5-repair/lanes/config-hygiene.scan.py",
]
raw_capture = ROOT / "watch/inbox/gala_20260925/wave5-repair/lanes/config-hygiene.check.txt"
edited = ["models/providers.py", "mag/improve.py"]

bad = 0

print("== authored files (excluding raw capture): em/en dash + nonascii must be 0/0 ==")
for p in authored:
    text = p.read_text(encoding="utf-8")
    em = sum(text.count(d) for d in DASHES)
    nonascii = sum(1 for ch in text if ord(ch) > 127)
    ok = em == 0 and nonascii == 0
    bad += 0 if ok else 1
    print(f"  [{'OK' if ok else 'BAD'}] {p.name}: em/en dashes={em} nonascii={nonascii}")

text = raw_capture.read_text(encoding="utf-8")
em = sum(text.count(d) for d in DASHES)
nonascii = sum(1 for ch in text if ord(ch) > 127)
print(f"  [EXEMPT-RAW-CAPTURE] {raw_capture.name}: em/en dashes={em} nonascii={nonascii}")
print("      (byte-faithful capture of tool output; tools/config_seal.py:70,72 print "
      "em-dashes in its own FAIL/PASS lines; scrubbing them would falsify raw output)")

print("== added lines in edited code files (git diff vs HEAD, '+' lines only) ==")
for path in edited:
    diff = subprocess.run(
        ["git", "diff", "-U0", "--", path],
        cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    added = [ln[1:] for ln in diff.stdout.splitlines() if ln.startswith("+") and not ln.startswith("+++")]
    em = sum(ln.count(d) for ln in added for d in DASHES)
    nonascii = sum(1 for ln in added for ch in ln if ord(ch) > 127)
    ok = em == 0 and nonascii == 0
    bad += 0 if ok else 1
    print(f"  [{'OK' if ok else 'BAD'}] {path}: added lines={len(added)} "
          f"em/en dashes={em} nonascii={nonascii}")

print()
print("SCAN RESULT: " + ("FAIL" if bad else "PASS - authored files 0/0, added code lines 0/0"))
sys.exit(1 if bad else 0)
