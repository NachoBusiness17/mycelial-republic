#!/usr/bin/env python3
"""prepush_golden_vector.py - known-answer tripwire for tools/dungeon.py FULL CAMPAIGN.

Lane row (cause + evidence): memory/runs/mickey17_v2/runs/run-0/lanes/
a11-commits.json row index 3, key cc33f22dcafe ("FULL CAMPAIGN holds"). That
lane byte-verified, against the blob committed in a7d7d313d (git show
a7d7d313d:tools/dungeon.py, scenes dict lines 362-392, loop line 414, win at
516-528), that campaign() carries: S2 Lexical Stair, S3 Wiping Vault, S4
Phantom Wyrm with its scroll hoard, and the root-anchoring win gate (three
[AUDIT root] successes at DC 15; dropping the Wyrm's HP to 0 does NOT win).

The disease this closes: the audit ran once and nothing stood watch after it,
so a later dungeon.py edit could silently drop the win gate or a scene and no
gate would name it. The golden vector below is the exact byte tokens the row
pinned; each one was verified present at landing in BOTH the working tree
(grep -cF) and the a7d7d313d blob, 11/11 both surfaces.

Why a token check and not a live `dungeon.py --full` run: campaign() calls
models through self._paid (tools/dungeon.py:489) and writes a session DONE
file (tools/dungeon.py:577), and a push hook must never write shared state or
spend budget (the B2-328 push-hook law, stated in the refold gate block of
githooks/pre-push). The row's known answers are byte facts, so bytes are the
vector.

WARN-ONLY first landing per the t40/B2-215 house pattern: the hook captures
this tool's output and prints it as a WARN; it never blocks a push. Flip to
enforce is an operator call.

Exit codes: 0 = every golden token present; 1 = one or more missing (the WARN
payload names each lost law and the state to restore from); 2 = cannot verify
(target file missing or unreadable).

Usage:
  .venv/Scripts/python.exe tools/prepush_golden_vector.py [--file tools/dungeon.py] [--list]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TARGET = "tools/dungeon.py"

# The golden vector, one (law name, byte token) per row. Each token is a
# single-line fixed string verified by grep -cF against the working tree AND
# git show a7d7d313d:tools/dungeon.py at landing (11/11 on both; receipt
# watch/inbox/go_wave_20261004/prepush_instruments.md). A token that stops
# matching means the law it pins left the bytes.
GOLDEN_VECTOR: list[tuple[str, str]] = [
    ("S2 scene: the Lexical Stair", "The Lexical Stair"),
    ("S3 scene: the Wiping Vault", "The Wiping Vault"),
    ("S4 scene: the Phantom Wyrm", "Phantom Wyrm"),
    ("S4 scroll hoard + regrowth law (campaign docstring)", "scroll hoard, regrowth,"),
    ("S4 unaudited scrolls feed the Wyrm", "scrolls feed the Wyrm"),
    ("root-anchor win gate: 3x [AUDIT root] at DC 15", "[AUDIT root] successes at DC 15"),
    ("win gate law: dropping Wyrm HP to 0 does NOT win", "Dropping it to 0 does NOT win"),
    ("win verdict: lattice re-hooks to the chain",
     "WON: root anchored, the lattice re-hooks to the chain"),
    ("--full flag wiring (additive over S0+S1)", 'add_argument("--full"'),
    ("campaign scene loop S2-S4", '("S2", "S3", "S4")'),
    ("root anchor counter (the 3-anchor win state)", "root_anchors"),
]

RESTORE_FROM = ("restore state: git show a7d7d313d:tools/dungeon.py is the blob the "
                "a11-commits row byte-verified")


def check_text(text: str, vector: "list[tuple[str, str]] | None" = None) -> list[str]:
    """Pure verdict core. Returns the law names whose token is absent."""
    vec = GOLDEN_VECTOR if vector is None else vector
    return [name for name, needle in vec if needle not in text]


def run(target: Path) -> int:
    if not target.is_file():
        print(f"GOLDEN-VECTOR: cannot verify, target missing: {target}")
        return 2
    try:
        text = target.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"GOLDEN-VECTOR: cannot verify, target unreadable: {exc}")
        return 2
    missing = check_text(text)
    head = (f"{len(GOLDEN_VECTOR) - len(missing)}/{len(GOLDEN_VECTOR)} golden tokens "
            f"in {target}")
    if not missing:
        print(f"GOLDEN-VECTOR: ok - {head}")
        return 0
    print(f"GOLDEN-VECTOR: MISS - {head}")
    for name in missing:
        print(f"  lost: {name}")
    print(f"  {RESTORE_FROM}")
    return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="golden-vector known-answer tripwire for dungeon.py FULL CAMPAIGN "
                    "(a11-commits row 3)")
    ap.add_argument("--file", default=DEFAULT_TARGET,
                    help=f"file to check (default: {DEFAULT_TARGET})")
    ap.add_argument("--list", action="store_true", help="print the golden vector and exit")
    args = ap.parse_args(argv)
    if args.list:
        for name, needle in GOLDEN_VECTOR:
            print(f"{name}\n  token: {needle}")
        return 0
    target = Path(args.file)
    if not target.is_absolute():
        target = Path.cwd() / target
    return run(target)


if __name__ == "__main__":
    sys.exit(main())
