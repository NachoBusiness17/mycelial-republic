"""_audit_modules.py — audit mag/*.py for redundancy + dead/orphan candidates.

Operator (2026-08-15): "can modules be deduped?" Ground it with bytes: how many modules, and how many are
referenced (imported/used) vs dead-or-orphan candidates. A dead module (never imported anywhere) is a
bone to retire, not a sacred cow. Read-only, deterministic + $0.

Schema: _audit_modules.v1
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAG = ROOT / "mag"


def main() -> None:
    mods = sorted(p.stem for p in MAG.glob("*.py") if not p.stem.startswith("_"))
    print(f"mag/ modules: {len(mods)}\n")

    # reference scan: build ONE combined code index once, then match each module against it (fast).
    code_dirs = [ROOT / d for d in ("mag", "scripts", "dashboard", "tools", "backend", "router", "configs", "deploy", "tests", "queue", "models")]
    code_files = [ROOT / "main.py", ROOT / "mag_launch.py", ROOT / "config.py", ROOT / "conftest.py"]
    for d in code_dirs:
        if d.is_dir():
            code_files += list(d.rglob("*.py"))
    index = []
    for p in code_files:
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        index.append((p, txt))

    def refcount(m: str) -> int:
        pattern = re.compile(rf"(?:import|from)\s+mag\.{m}\b|\b{re.escape(m)}\.py\b|\bfrom mag import .*\b{m}\b")
        n = 0
        for p, txt in index:
            if p.stem == m and p.parent.name == "mag":
                continue
            if pattern.search(txt):
                n += 1
        return n

    refs = {m: refcount(m) for m in mods}

    dead = sorted((m for m, c in refs.items() if c == 0))
    low = sorted((m for m, c in refs.items() if 0 < c <= 2))
    print(f"DEAD-OR-ORPHAN (0 references anywhere): {len(dead)}")
    print("  " + ", ".join(dead[:60]))
    print(f"\nLOW-REFERENCE (1-2 refs, likely one-off bones): {len(low)}")
    print("  " + ", ".join(low[:40]))
    print(f"\nREFERENCED (3+ refs, live): {len(mods) - len(dead) - len(low)}")


if __name__ == "__main__":
    main()
