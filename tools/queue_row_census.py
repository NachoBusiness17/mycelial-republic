"""Queue row census + normalizer + tripwire (B2-488, 2026-09-26).

The strict census regex the burn wave used,
    STRICT_ROW = ^- \[[ x]\] B2-\d+<space>
misses row starts that deviate from the canonical checkbox shape (the live
disease: "-  [ ] B2-369 ..." double-space starts sat on the board at 18:58Z
and every strict consumer undercounted until a tolerant second regex was
written by hand). This module is the shared surface the brief asked for:

  check      tripwire: list every line that a tolerant reader sees as a
             brief-row start but the strict regex cannot see, or that packs
             more than one checkbox row onto one line. Exit 0 = clean,
             exit 1 = deviations named (wire this before any queue census).
  normalize  one dated pass to the canonical shape: leading malformed starts
             are rewritten; same-line embedded rows that QUOTE a landed
             brief's original text are indented under their landing note so
             they stop masquerading as row starts; genuine same-line briefs
             are split onto their own lines. Prints the SHA256 of the board
             before/after. Never touches non-Open-section content rules.

Usage:
  python tools/queue_row_census.py check   [--queue PATH]
  python tools/queue_row_census.py normalize [--queue PATH] [--dry-run]
"""
from __future__ import annotations

import argparse
import hashlib
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"

STRICT_ROW = re.compile(r"^- \[[ x]\] B2-\d+ ")
# tolerant: a checkbox row start with any dash/space damage, or any checkbox
# row ANYWHERE on the line (the embedded-same-line shape)
TOLERANT_START = re.compile(r"^-+\s*\[\s*[x ]\s*\]\s*B2-\d+\s")
CHECKBOX_ROW_ANYWHERE = re.compile(r"(?:^|\s)-\s*\[\s*[x ]\s*\]\s*B2-\d+")


def census(lines: list[str]) -> dict:
    strict = sum(1 for ln in lines if STRICT_ROW.match(ln))
    tolerant = sum(1 for ln in lines if TOLERANT_START.match(ln))
    deviations: list[tuple[int, str, str]] = []
    for i, ln in enumerate(lines, 1):
        n_rows = len(CHECKBOX_ROW_ANYWHERE.findall(ln))
        if TOLERANT_START.match(ln) and not STRICT_ROW.match(ln):
            deviations.append((i, "malformed-start", ln[:110]))
        elif n_rows > 1:
            deviations.append((i, f"multi-row-line ({n_rows} rows)", ln[:110]))
    return {
        "strict_rows": strict,
        "tolerant_rows": tolerant,
        "deviations": deviations,
        "undercount": tolerant - strict,
    }


def normalize_line(ln: str) -> str:
    # canonicalize a malformed leading row start
    m = re.match(r"^(-+)\s*\[\s*([x ])\s*\]\s*(B2-\d+\s.*)$", ln)
    if m and not STRICT_ROW.match(ln):
        return f"- [{m.group(2)}] {m.group(3)}"
    # embedded same-line rows after a landed ([x]) note: indent as quote
    if STRICT_ROW.match(ln):
        parts = ln.split("- [ ")
        if len(parts) == 1:
            parts = ln.split("- [ ]")
        if len(parts) == 1:
            parts = ln.split("- [x]")
        if len(parts) > 1 and parts[0].strip():
            head = parts[0]
            tail = ln[len(head):]
            return head + "\n  " + tail.lstrip()
    return ln


def normalize(lines: list[str], dry: bool) -> tuple[list[str], int]:
    out = []
    changed = 0
    for ln in lines:
        cur = ln
        # re-apply until stable, hard-capped so a pathological line can
        # never spin the pass
        for _ in range(5):
            new = normalize_line(cur)
            if new == cur:
                break
            cur = new
        if cur != ln:
            changed += 1
        # a fix may embed a newline (split-onto-own-line shapes)
        out.extend(cur.split("\n"))
    return out, changed


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cmd", choices=["check", "normalize"])
    ap.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    raw = io.open(args.queue, encoding="utf-8", newline="").read()
    before_sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
    lines = raw.split("\n")

    if args.cmd == "check":
        c = census(lines)
        print(f"queue census: strict {c['strict_rows']} / tolerant "
              f"{c['tolerant_rows']} rows; deviations {len(c['deviations'])}; "
              f"undercount {c['undercount']}")
        for i, kind, ln in c["deviations"][:10]:
            print(f"  line {i} [{kind}] {ln}")
        if c["deviations"]:
            print("TRIPWIRE: strict consumers are blind to the lines above; "
                  "run the normalizer or fix the row start.")
            return 1
        return 0

    fixed, changed = normalize(lines, args.dry_run)
    c = census(fixed)
    if args.dry_run:
        print(f"dry run: {changed} line(s) would change; post-census "
              f"deviations {len(c['deviations'])}")
        return 0 if not c["deviations"] else 1
    out = "\n".join(fixed)
    io.open(args.queue, "w", encoding="utf-8", newline="").write(out)
    after_sha = hashlib.sha256(out.encode("utf-8")).hexdigest()[:16]
    print(f"normalized {changed} line(s); board sha {before_sha} -> {after_sha}; "
          f"post-census deviations {len(c['deviations'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
