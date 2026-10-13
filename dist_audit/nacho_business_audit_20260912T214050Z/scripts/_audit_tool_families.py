"""_audit_tool_families.py — collapse the 116 steal tools into distinct capability-families.

The operator (2026-08-15): memweave the tools? -> first prove the dedupe case with bytes. This buckets
the 116 tools by dominant family keyword (name/theme), showing how many DISTINCT capabilities there are
vs. how many labels. Deterministic + $0, read-only.

Schema: _audit_tool_families.v1
"""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# dominant family keywords, checked in order (first match wins) against name+theme
FAMILIES = [
    ("roshomon", r"roshomon|witness|consensus"),
    ("flock", r"flock|boid|shader|renderman|field"),
    ("memweave", r"memweave|mem_weave|weave|distribut"),
    ("verkle", r"verkle|knot|chain|merkle|dirac"),
    ("rib", r"\brib\b|rib_|standing.?wave"),
    ("gpu", r"gpu|vram|roc|nvidia|quantiz|int[48]"),
    ("grok", r"grok|x\.?ai|grokbot"),
    ("egregore", r"egregore|republic|myceli|swarm-mind"),
    ("castle", r"castle|foundation|formula|invariant"),
    ("gap", r"gap|frontier|escalat|moonshot|deep.?research"),
    ("swarm", r"swarm|worker|drain|queue|orchestrat|seat"),
    ("steal", r"steal|gene|hgt|horizontal|import"),
    ("persona", r"persona|mirror|npc|voice|dm|game|narrative"),
    ("budget", r"budget|cost|economy|token|rightsize|price"),
    ("browser", r"browser|cdp|fetch|web|page|native"),
    ("stateless", r"stateless|headless|no.?window|windowless"),
    ("shadow", r"shadow|prion|drift|babel|riddler|fish.?ear"),
    ("game", r"game|mud|dnd|wow|dungeon|rogue|quest"),
]


def _family(hay: str) -> str:
    h = hay.lower()
    for name, pat in FAMILIES:
        if re.search(pat, h):
            return name
    return "misc"


def main() -> None:
    from mag import steal_tools
    tools = steal_tools.tools()
    fam = defaultdict(list)
    for t in tools:
        key = _family(t["name"] + " " + t["theme"])
        fam[key].append(t["name"])
    counts = Counter({k: len(v) for k, v in fam.items()})
    distinct = len(counts)
    print(f"TOTAL TOOLS: {len(tools)}  |  DISTINCT FAMILIES: {distinct}  |  collapse {len(tools)} -> {distinct}")
    print(f"if every family weaves to ONE node (dedupe), the armory goes from {len(tools)} to ~{distinct} tools.\n")
    print("== FAMILY -> tool count ==")
    for k, c in counts.most_common():
        print(f"  {k}: {c}")
    print("\n== per-family tool names (to see the redundancy) ==")
    for k in sorted(fam, key=lambda x: -len(fam[x])):
        print(f"  [{k}] ({len(fam[k])}) " + ", ".join(x.replace('_', ' ') for x in fam[k][:12]))


if __name__ == "__main__":
    main()
