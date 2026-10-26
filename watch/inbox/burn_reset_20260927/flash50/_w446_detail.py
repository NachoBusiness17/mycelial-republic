#!/usr/bin/env python3
"""_w446_detail -- follow-ups for w4-46.md. Read-only, no subprocess, no writes."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def load(rel):
    return [json.loads(l) for l in (ROOT / rel).read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]


burns = load("memory/burns/LEDGER.jsonl")
have = Counter()
for k in ("lane", "failure_class", "landing", "restore", "fresh_failure_mode", "fresh_failure_mode_note"):
    have[k] = sum(1 for r in burns if k in r)
print("burns.key_presence:", dict(have))

reg = load("memory/workflows/REGISTRY.jsonl")
by_digest = defaultdict(list)
for r in reg:
    by_digest[r.get("digest", "?")].append((r.get("ts", ""), r.get("name", ""), r.get("verdict", "")))
for d, lst in by_digest.items():
    if len(lst) > 1:
        print("registry.repeat_digest:", d, "x", len(lst), lst)

wave = load("watch/GROUNDING_WAVE.jsonl")
hashes = [r.get("hash") for r in wave if r.get("hash")]
for r in wave:
    kind = r.get("kind")
    if kind in ("void", "contest", "witness"):
        key = {"void": "voids", "contest": "contests", "witness": "signs"}[kind]
        tgt = r.get(key)
        targets = tgt if isinstance(tgt, list) else ([tgt] if tgt else [])
        for t in targets:
            ok = any(t and (h == t or (h and h.startswith(str(t)))) for h in hashes)
            if not ok:
                row = json.dumps({k2: r.get(k2) for k2 in ("ts", "kind", key, "seat", "evidence", "hash")})[:400]
                print("wave.unresolved_target:", row)
