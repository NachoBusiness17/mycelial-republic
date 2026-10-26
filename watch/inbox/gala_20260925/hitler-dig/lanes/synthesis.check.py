"""synthesis lane (division A, hitler-dig): byte-check the mined quotes.

Tiers follow the estate's cross_ractor_bytecheck discipline
(watch/inbox/gala_20260925/ouroboros/lanes/cross_ractor_bytecheck.py):
T0-exact  : exact byte substring of the named source.
T1-wsnorm : whitespace-collapsed match (byte-true modulo line wraps).
Any MISS -> exit 1. The verdict is the exit code, not opinion.
"""
import re
import sys
from pathlib import Path

ROOT = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")

QUOTES = [
    {
        "law": "verdicts-carry-their-conditions",
        "source": "memory/rib/RIB_DRIVING_LADDER_20260928.md",
        "quote": "Law, generalizing B2-216 from counts to all instruments: A VERDICT WITHOUT ITS CONDITIONS IS NOT A VERDICT.",
    },
    {
        "law": "apophenia-until-the-grammar-does-work",
        "source": "memory/runs/salons/unified_fold_20260906/SALON_ARTIFACT.md",
        "quote": "If the protocol needs a new verb per surface, **the grammar is poetry.**",
    },
    {
        "law": "phantom-number-lint",
        "source": "tools/citation_lint.py",
        "quote": 'Founding fixture: the 191.8M phantom (STORY.md:240 stated 191.8M tokens; its named source watch/inbox/frontier_olm_20260928/DIGEST.md carries zero "191" hits).',
    },
    {
        "law": "memory-written-citations",
        "source": "watch/inbox/ractor50/accuracy.md",
        "quote": "Citations written from dig memory at doctrine-authoring time, never byte-checked against the named file at the granularity claimed (path wrong, predicate imprecise, one missing entirely).",
    },
    {
        "law": "depth-dilutes-while-volume-compounds",
        "source": "watch/inbox/gala_20260925/ouroboros_RECEIPT.md",
        "quote": "receipts grew +1,457 in 2 days while effective dimensionality D fell 4.3 to 4.0 and the laws-to-ribs edge froze at 2 citing ribs. Raw counts are the wrong weekly metric",
    },
]


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s)


fails = 0
for q in QUOTES:
    p = ROOT / q["source"]
    if not p.exists():
        print("MISS  %s  source missing: %s" % (q["law"], q["source"]))
        fails += 1
        continue
    raw = p.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()
    tier = None
    line_no = 0
    if q["quote"] in raw:
        tier = "T0-exact"
    elif norm(q["quote"]) in norm(raw):
        tier = "T1-wsnorm"
    # locate first matching window (6-line span, whitespace-collapsed)
    for i in range(max(len(lines) - 5, 0) + 1):
        window = norm(" ".join(lines[i : i + 6]))
        if norm(q["quote"]) in window:
            line_no = i + 1
            break
    if tier:
        print("PASS  %-42s %s  line~%d  %s" % (q["law"], tier, line_no, q["source"]))
    else:
        print("MISS  %-42s %-10s %s" % (q["law"], "no-tier", q["source"]))
        fails += 1

print("TOTAL: %d quotes, %d PASS, %d MISS" % (len(QUOTES), len(QUOTES) - fails, fails))
sys.exit(1 if fails else 0)
