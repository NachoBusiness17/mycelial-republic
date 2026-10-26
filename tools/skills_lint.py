#!/usr/bin/env python
"""skills_lint — contract checker for every SKILL.md on the shelf.

The corpus-harvest bug class: skill files the harness cannot index (missing or
malformed frontmatter), name mismatches, empty descriptions, dead referenced paths.
Run: .venv/Scripts/python.exe tools/skills_lint.py [--house-only]
Exit 1 if any house skill has an ERROR-level violation.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HOME = Path.home()

ROOTS = [
    ("house-repo", REPO / ".agents" / "skills"),
    ("house-user", HOME / ".agents" / "skills"),
    ("zcode-user", HOME / ".zcode" / "skills"),
]
VENDOR = HOME / ".zcode" / "cli" / "plugins" / "cache"

FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
EMDASH = "\u2014"


def lint(md: Path) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    rel = md
    try:
        text = md.read_text(encoding="utf-8", errors="replace")
    except Exception as e:  # unreadable is fatal for an index
        return [("ERROR", f"unreadable: {e}")]
    m = FM_RE.match(text)
    fm_name = fm_desc = None
    if not m:
        issues.append(("ERROR", "no frontmatter block (harness cannot index name/description)"))
    else:
        for line in m.group(1).splitlines():
            if line.startswith("name:"):
                fm_name = line.split(":", 1)[1].strip()
            elif line.startswith("description:"):
                fm_desc = line.split(":", 1)[1].strip()
        if not fm_name:
            issues.append(("ERROR", "frontmatter missing name:"))
        if not fm_desc:
            issues.append(("ERROR", "frontmatter missing description: (skill invisible in any catalog)"))
        elif len(fm_desc) < 20:
            issues.append(("WARN", f"description too short ({len(fm_desc)} chars)"))
    if fm_name and fm_name != md.parent.name:
        issues.append(("WARN", f"frontmatter name '{fm_name}' != directory '{md.parent.name}'"))
    body_lines = len([ln for ln in text.splitlines() if ln.strip()])
    if body_lines < 5:
        issues.append(("WARN", f"thin body ({body_lines} non-empty lines)"))
    if EMDASH in text:
        n = text.count(EMDASH)
        issues.append(("WARN", f"em-dash count {n} (house law: 0 in filed docs)"))
    # referenced repo paths in backticks must exist
    for p in set(re.findall(r"`((?:docs|watch|mag|tools|configs|corpus|memory|state|scripts|tests)/[^`\s]+)`", text)):
        if not (REPO / p).exists():
            issues.append(("WARN", f"referenced path missing: {p}"))
    return issues


def main() -> None:
    house_only = "--house-only" in sys.argv
    total_files = errors = warnings = 0
    out: list[str] = ["# SKILLS LINT", ""]
    for label, root in ROOTS + ([("vendor", VENDOR)] if not house_only else []):
        if not root.exists():
            continue
        out.append(f"## {label}")
        for md in sorted(root.glob("**/SKILL.md")):
            total_files += 1
            issues = lint(md)
            if not issues:
                continue
            is_house = label.startswith("house")
            out.append(f"- `{md.parent.name}` ({label})")
            for sev, msg in issues:
                if sev == "ERROR":
                    errors += 1 if is_house else 0
                    out.append(f"  - ERROR: {msg}")
                else:
                    warnings += 1
                    out.append(f"  - warn: {msg}")
        out.append("")
    out.insert(1, f"files scanned: {total_files} | house errors: {errors} | warnings: {warnings}")
    report = "\n".join(out) + "\n"
    (REPO / "docs" / "SKILLS_LINT.md").write_text(report, encoding="utf-8")
    print(report)
    print(f"written to docs/SKILLS_LINT.md | house errors: {errors}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
