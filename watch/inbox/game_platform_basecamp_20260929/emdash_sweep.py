#!/usr/bin/env python
"""em-dash sweep for house skill docs (census-law compliant: reports real counts)."""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HOME = Path.home()
ROOTS = [REPO / ".agents" / "skills", HOME / ".agents" / "skills", HOME / ".zcode" / "skills"]

fixed_files = 0
fixed_count = 0
for root in ROOTS:
    if not root.exists():
        continue
    for md in root.glob("**/SKILL.md"):
        t = md.read_text(encoding="utf-8", errors="replace")
        n = t.count("\u2014")
        if n:
            t = t.replace(" \u2014 ", " - ").replace("\u2014", "-")
            md.write_text(t, encoding="utf-8")
            fixed_files += 1
            fixed_count += n
print(f"files fixed: {fixed_files} | em-dashes removed: {fixed_count}")
