#!/usr/bin/env python3
"""game_module_dated_numbers.py - the dated-number tripwire for game-module lore.

B2-323 (2026-09-26). Cause: memory/game_modules/audit_dungeon.v1.json carries
about a dozen bare census numbers (665,131 files; 986 halls; 38,400 diaries;
205,991 backup copies; 42,249 in the annex; 102,759 in the ore shaft; 23
unpushed commits; 1.6GB packs; 3.2GB ore; $220 armed) with the as-of date
(2026-09-14) baked only into the title and license_note, so every one of them
can fossilize exactly the way the 1,341 test headline did (B2-214 landed the
librarian line fix; B2-69 filed the census denominator law).

THE RULE (one dated-number rule for the module):
  Any lore string that asserts a NUMBER ABOUT THE REAL ESTATE (counts, sizes,
  money, commit counts) must carry its as-of date IN THE SAME STRING, e.g.
  "... 665,131 files (as of 2026-09-14) ...". A number in a string with no
  date marker is a fossil waiting to happen. Pure in-fiction numbers that
  never touch estate facts (dice rolls, room counts inside the fiction) are
  exempt - the tripwire flags real-estate-shaped counts only: thousands-
  grouped numbers, GB/MB sizes, dollar amounts, and N-commit claims.

MECHANISM: this tripwire walks every string in a game module JSON and flags
real-estate-shaped numbers whose string carries no date marker (ISO date,
"as of", or a bare census year like 2026). Exit 1 when any are found, exit 0
when clean; `--module <path>` checks one module, default sweeps
memory/game_modules/*.json.

Fix convention: add the date in-string ("... (as of 2026-09-14) ...") or move
the number into a hook that carries an explicit as_of sibling key when the
schema supports one.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = ROOT / "memory" / "game_modules"

# real-estate-shaped numbers: thousands-grouped (665,131), sizes (1.6GB, 42MB),
# dollar amounts ($220), and commit/test counts
NUMBER_RE = re.compile(
    r"\d{1,3}(?:,\d{3})+|\b\d+(?:\.\d+)?\s?(?:GB|MB|KB)\b|\$\s?\d[\d,]*"
    r"|\b\d+\+?\s+(?:commits|tests|files)\b"
)
# a string is "dated" when it carries any of these markers
DATE_MARK_RE = re.compile(r"20\d\d-\d\d-\d\d|\bas of\b|\bas_of\b|\bcensus\b|\bdated\b")


def find_bare(module_path: Path) -> list[str]:
    """Return one human line per bare (undated) real-estate number found."""
    data = json.loads(module_path.read_text(encoding="utf-8"))
    out: list[str] = []

    def walk(node, path: str) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, f"{path}/{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")
        elif isinstance(node, str):
            if not NUMBER_RE.search(node):
                return
            if DATE_MARK_RE.search(node):
                return
            for m in NUMBER_RE.finditer(node):
                if m.start() > 0 and node[m.start() - 1] == ":":
                    continue  # file.py:153,191,242 = a line reference, not a count
                seg = node[max(0, m.start() - 50):m.end() + 50]
                out.append(f"{path}: [{m.group(0)}] ...{seg}...")

    walk(data, module_path.name)
    return out


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv] or sorted(MODULES.glob("*.json"))
    total = 0
    for p in paths:
        try:
            bare = find_bare(p)
        except Exception as e:  # noqa: BLE001
            print(f"{p.name}: unreadable ({e})")
            total += 1
            continue
        if bare:
            print(f"{p.name}: {len(bare)} bare number(s) with no date in the same string:")
            for line in bare:
                print("  " + line)
            total += len(bare)
        else:
            print(f"{p.name}: clean (every real-estate number carries its date)")
    if total:
        print(f"TRIPWIRE: {total} undated real-estate number(s); add the as-of date "
              "in-string per the module dated-number rule (B2-323).")
        return 1
    print("TRIPWIRE: clean.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
