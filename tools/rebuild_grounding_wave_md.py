"""Rebuild dashboard/static/grounding_wave.md from watch/GROUNDING_WAVE.jsonl.

The jsonl chain is authoritative; the md view is a rendered convenience and
drifts when rows are appended by paths that skip the view. This script reads
the jsonl, keeps the md's existing header block verbatim, and regenerates the
rows newest-first (reverse chain order) in the view's established format:

    ## <ts> — <verdict> — <seat>
    - **claim:** ...
    - **evidence:** ...
    - **note:** ...            (omitted when the row has none)
    - hash `<hash[:12]>` ← prev `<prev[:12]>`

Field rules copied from the existing view + mag/grounding_wave.py:
- verdict fallback "UNLABELLED" (render()'s fallback, mag/grounding_wave.py:810)
- seat fallback: "v1-era" for the pre-2026-09-07 grandfathered rows, "zcode"
  otherwise (both observed in the pre-resync view)
- hash/prev truncated to 12 chars, as in every existing view row

NEVER writes the jsonl. Only writes dashboard/static/grounding_wave.md.

Usage: python tools/rebuild_grounding_wave_md.py [--check]
  --check  regenerate in memory and exit nonzero if the file on disk differs
           (no write) — for CI-style drift alarms.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAIN = ROOT / "watch" / "GROUNDING_WAVE.jsonl"
VIEW = ROOT / "dashboard" / "static" / "grounding_wave.md"

V1_ERA_CUTOFF = "2026-09-07"  # rows before this carry no `seat`; view labels them "v1-era"


def seat_label(row: dict) -> str:
    seat = row.get("seat")
    if seat:
        return str(seat)
    ts = str(row.get("ts", ""))
    return "v1-era" if ts and ts < V1_ERA_CUTOFF else "zcode"


def render_row(row: dict) -> list[str]:
    lines = [f"## {row.get('ts', '')} — {row.get('verdict', 'UNLABELLED')} — {seat_label(row)}"]
    lines.append(f"- **claim:** {row.get('claim', '')}")
    if row.get("evidence"):
        lines.append(f"- **evidence:** {row['evidence']}")
    if row.get("note"):
        lines.append(f"- **note:** {row['note']}")
    lines.append(f"- hash `{str(row.get('hash', ''))[:12]}` ← prev `{str(row.get('prev', ''))[:12]}`")
    lines.append("")
    return lines


def read_header() -> list[str]:
    """Keep the existing view's header block verbatim (everything before the
    first row heading)."""
    text = VIEW.read_text(encoding="utf-8")
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("## "):
            return lines[:i]
    raise SystemExit(f"no row headings found in {VIEW}; cannot locate header")


def build_md() -> str:
    header = read_header()
    rows = [json.loads(line) for line in CHAIN.read_text(encoding="utf-8").splitlines() if line.strip()]
    lines = list(header)
    for row in reversed(rows):  # newest-first = reverse chain order
        lines.extend(render_row(row))
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="verify only: exit 1 if the view on disk differs from a fresh rebuild")
    args = ap.parse_args()

    md = build_md()
    n_rows = md.count("\n## ")
    if args.check:
        current = VIEW.read_text(encoding="utf-8")
        if current == md:
            print(f"CHECK PASS: view matches jsonl exactly ({n_rows} rows, header kept)")
            return 0
        print(f"CHECK FAIL: view drifted from jsonl (rebuild carries {n_rows} rows)")
        return 1

    VIEW.write_text(md, encoding="utf-8")  # jsonl untouched by construction
    print(f"rebuilt {VIEW.relative_to(ROOT)} from {CHAIN.relative_to(ROOT)}: {n_rows} rows, header kept")
    return 0


if __name__ == "__main__":
    sys.exit(main())
