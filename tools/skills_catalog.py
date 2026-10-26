#!/usr/bin/env python
"""skills_catalog — generate docs/SKILLS_CATALOG.md from every installed SKILL.md.

Census law compliance: this catalog is GENERATED, never hand-written. Re-run after
installing/removing skills:
    .venv/Scripts/python.exe tools/skills_catalog.py
Skill roots scanned (house skills first, vendor plugins last):
    <repo>/.agents/skills          repo-owned skills (committed, shared across seats)
    ~/.agents/skills               user-level skills
    ~/.zcode/skills                user-level zcode skills
    ~/.zcode/cli/plugins/cache     vendor plugins (official plugin packs)
"""
from __future__ import annotations

import datetime
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HOME = Path.home()

ROOTS = [
    ("house (repo-committed)", REPO / ".agents" / "skills"),
    ("house (user-level)", HOME / ".agents" / "skills"),
    ("house (zcode user)", HOME / ".zcode" / "skills"),
    ("vendor plugins", HOME / ".zcode" / "cli" / "plugins" / "cache"),
]

FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def parse_skill(md: Path) -> dict:
    text = md.read_text(encoding="utf-8", errors="replace")
    name, desc = "", ""
    m = FM_RE.match(text)
    if m:
        for line in m.group(1).splitlines():
            if line.startswith("name:") and not name:
                name = line.split(":", 1)[1].strip()
            elif line.startswith("description:") and not desc:
                desc = line.split(":", 1)[1].strip()
    if not name:
        name = md.parent.name
    return {"name": name, "desc": desc, "path": md}


def scan(root: Path) -> list[dict]:
    if not root.exists():
        return []
    skills = [parse_skill(md) for md in sorted(root.glob("**/SKILL.md"))]
    return [s for s in skills if "plugins/cache" not in str(s["path"]) or True]


def main() -> None:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# SKILLS CATALOG (generated)",
        "",
        f"Generated {now} by `tools/skills_catalog.py` — re-run that to refresh; never hand-edit counts.",
        "",
    ]
    total = 0
    for label, root in ROOTS:
        skills = scan(root)
        total += len(skills)
        lines.append(f"## {label} — {len(skills)}")
        lines.append("")
        if not skills:
            lines.append("(none found)")
            lines.append("")
            continue
        for s in skills:
            rel = s["path"].relative_to(root) if s["path"].is_relative_to(root) else s["path"]
            invocable = f"/{s['name']}"
            lines.append(f"- **{invocable}** — {s['desc'] or '(no description)'} `({rel})`")
        lines.append("")
    lines.insert(4, f"**Total: {total} skills.**")
    out = REPO / "docs" / "SKILLS_CATALOG.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out} ({total} skills)")


if __name__ == "__main__":
    main()
