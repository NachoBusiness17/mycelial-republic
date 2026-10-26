"""ledger_close_check -- B2-203 one_line freshness re-check for LEDGER closes.

The disease (B2-203, 2026-09-26): memory/burns/LEDGER.jsonl row 110 (B2-156,
13:41:16Z) asserted "owed: missing B2-41 receipt filed as B2-198" 11m23s after
that receipt registered (index_events.jsonl seq 1789823567015749402,
13:29:52.864Z), minting a phantom owed brief that spun lane B2-198. The
convention lives in memory/burns/MANIFEST.json protocol.ledger_one_line_freshness.

Usage:
  python tools/ledger_close_check.py --one-line "..."
  python tools/ledger_close_check.py --row memory/burns/LEDGER.jsonl --line 110

Behavior: extracts repo-relative-looking path tokens from the one_line, finds
the missing/owed assertions, and re-checks each asserted-missing path against
disk bytes at run time. Exit 1 if any asserted-missing/owed path EXISTS (stale
assertion: the close would be a lie if appended now). Exit 0 when nothing is
asserted missing or every assertion still matches disk.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# path-like tokens: repo-relative segments with an extension or a known dir
PATH_RE = re.compile(
    r"(?:watch|memory|docs|configs|tools|scripts|mag|tests|queue|corpus|catalog)"
    r"(?:/[\w.\-]+)+")
# brief-id tokens: "B2-41 receipt" style assertions name the id, not the path;
# the receipt convention maps id -> watch/inbox/**/B2_<id>_*_<date>.md
ID_RE = re.compile(r"\bB2-(\d+)\b")

MISSING_RE = re.compile(
    r"(?:missing|owed|does not exist|not (?:been )?filed|absent|no receipt (?:exists|on disk)|never landed)",
    re.IGNORECASE)


def _receipt_candidates(brief_id: str) -> list[Path]:
    base = REPO / "watch" / "inbox"
    hits = sorted(base.glob(f"burn_wave_20260926/B2_{brief_id}_*.md"))
    hits += sorted(base.glob(f"B2_{brief_id}_*.md"))
    return hits


def check_one_line(one_line: str) -> dict:
    paths = sorted(set(PATH_RE.findall(one_line or "")))
    asserted_missing = []
    clean = []
    stale = []
    for p in paths:
        # only paths sitting in the same sentence/clause as a missing-assertion
        for chunk in re.split(r"[;.]", one_line):
            if p in chunk and MISSING_RE.search(chunk):
                asserted_missing.append((p, chunk.strip()[:160]))
                break
        else:
            clean.append(p)
    # brief-id assertions inside missing-clauses resolve to receipt globs
    ids = sorted(set(ID_RE.findall(one_line or "")), key=int)
    for bid in ids:
        for chunk in re.split(r"[;.]", one_line):
            if f"B2-{bid}" in chunk and MISSING_RE.search(chunk):
                asserted_missing.append((f"B2-{bid} (receipt glob)", chunk.strip()[:160]))
                break
    for p, ctx in asserted_missing:
        if p.startswith("B2-"):
            bid = p.split()[0].split("-")[1]
            cands = _receipt_candidates(bid)
            exists = bool(cands)
            rel = str(cands[0].relative_to(REPO)).replace("\\", "/") if cands else ""
        else:
            exists = (REPO / p).exists()
            rel = p
        (stale if exists else clean).append(
            {"path": rel or p, "exists_on_disk": exists, "assertion_context": ctx})
    stale_rows = [s for s in stale if isinstance(s, dict)]
    return {"ok": not stale_rows, "paths_seen": paths,
            "asserted_missing": [s[0] for s in asserted_missing],
            "stale_assertions": stale_rows}


def main() -> int:
    ap = argparse.ArgumentParser(prog="ledger_close_check")
    ap.add_argument("--one-line", default="")
    ap.add_argument("--row", default="")
    ap.add_argument("--line", type=int, default=0)
    args = ap.parse_args()

    if args.row and args.line:
        lines = Path(args.row).read_text(encoding="utf-8").splitlines()
        rec = json.loads(lines[args.line - 1])
        one_line = rec.get("one_line", "")
    else:
        one_line = args.one_line
    verdict = check_one_line(one_line)
    print(json.dumps(verdict, indent=1))
    if not verdict["ok"]:
        print("STALE ASSERTION: a path claimed missing/owed exists on disk; "
              "do not append this row as written (or append a CORRECTION row instead).")
        return 1
    print("close check green")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
