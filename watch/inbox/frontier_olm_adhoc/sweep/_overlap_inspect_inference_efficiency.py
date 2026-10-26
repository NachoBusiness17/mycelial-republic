"""Second-stage overlap inspection: show the actual catalog rows / memory cards
behind the pattern hits, so the overlap field is precise (2026-10-11 sweep).
"""
import json
import os
import re

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
CATALOG = os.path.join(ROOT, "catalog", "catalog.jsonl")
MEMORY = os.path.join(ROOT, "memory")

CAT_PATTERNS = [
    "planetscale",
    "dsv41flash",
    "deepseek-v4.1-flash",
    "cactus",
    "functiongemma",
    "tin: full-text",
    "better prompt caching",
    "magnitude (yc",
]


def catalog_rows():
    out = {}
    with open(CATALOG, "r", encoding="utf-8", errors="replace") as fh:
        for i, line in enumerate(fh):
            low = line.lower()
            for p in CAT_PATTERNS:
                if p in low:
                    out.setdefault(p, []).append((i + 1, line.strip()[:400]))
    return out


def leviathan_cards():
    hits = []
    for dirpath, _dn, filenames in os.walk(MEMORY):
        for name in filenames:
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            try:
                text = open(path, "r", encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            for m in re.finditer(r"[Ll]eviathan", text):
                s = max(0, m.start() - 100)
                snippet = text[s : m.end() + 160].replace("\n", " ")
                hits.append((os.path.relpath(path, ROOT), snippet))
                break  # one snippet per file is enough for the map
    return hits


if __name__ == "__main__":
    rows = catalog_rows()
    for p in CAT_PATTERNS:
        found = rows.get(p, [])
        print(f"=== catalog pattern {p!r}: {len(found)} rows")
        for ln, row in found[:4]:
            print(f"  line {ln}: {row}")
    print()
    cards = leviathan_cards()
    print(f"=== leviathan mentions in memory/*.md: {len(cards)} files")
    for rel, snip in cards[:12]:
        print(f"  {rel} :: ...{snip}...")
