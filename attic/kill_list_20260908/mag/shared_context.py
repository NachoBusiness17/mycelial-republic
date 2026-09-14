"""shared_context — THE PROTOCOL for loading shared invariants + relative corpus into a model
(deepseek, grok, chatgpt — any seat), rightsized to each interaction, for emergent human-AI
collaboration. Turtles all the way down: INVARIANTS (the soul) -> RELATIVE CORPUS (retrieved
knowledge) -> THE INTERACTION.

THE POINT ("avoid cache hits", operator 2026-08-15): do NOT dump the whole corpus as a static prefix
every call — that's cheap cache hits but hollow (the model re-serves a stored blob, it doesn't reason
with our ideas). Instead RETRIEVE the slice RELEVANT to THIS interaction, so the context is fresh,
varied, and genuinely reasoned with — the model carries our ideas INTO its own systems, rightsized
to what it's doing. The same protocol applies to grok desktop, chatgpt, deepseek: load the shared
invariants + the relative corpus, right-sized.

Reuse: mag_soul (invariants), memory/steal (the corpus), repo memory.
Schema: shared_context.v1
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SCHEMA = "shared_context.v1"
STEAL_DIR = ROOT / "memory" / "steal"
_REPO_DIR = ROOT / "memory" / "learn"
_STOP = {"the", "and", "for", "our", "your", "this", "that", "with", "into", "about", "how", "what"}


def _tokens(text: str) -> set[str]:
    import re
    return {w for w in re.findall(r"[a-z][a-z0-9_'-]{2,}", (text or "").lower()) if w not in _STOP}


def corpus_index() -> list[dict[str, str]]:
    """Index the corpus (memory/steal + memory/learn) once: title + a snippet + its tokens."""
    entries: list[dict[str, str]] = []
    for base in (STEAL_DIR, _REPO_DIR):
        if not base.is_dir():
            continue
        for p in sorted(base.glob("*.md")):
            try:
                head = p.read_text(encoding="utf-8", errors="replace")[:600]
            except Exception:
                continue
            entries.append({"path": str(p), "title": p.stem, "snippet": head,
                            "tokens": " ".join(sorted(_tokens(head)))})
    return entries


def retrieve(query: str, *, k: int = 3, max_chars: int = 1600) -> list[dict[str, str]]:
    """Pick the corpus entries most relevant to the query by lexical overlap — the RELATIVE slice."""
    q = _tokens(query)
    scored = []
    for e in corpus_index():
        et = set(e["tokens"].split())
        score = len(q & et)
        if score > 0:
            scored.append((score, e))
    scored.sort(key=lambda x: x[0], reverse=True)
    out: list[dict[str, str]] = []
    used = 0
    for _, e in scored[:k]:
        if used + len(e["snippet"]) > max_chars:
            break
        out.append(e)
        used += len(e["snippet"])
    return out


def context_for(query: str, *, include_soul: bool = True, k: int = 3, max_chars: int = 1600) -> str:
    """The protocol output: INVARIANTS (soul) + RELATIVE CORPUS (retrieved for THIS interaction).
    Fresh, varied, right-sized — the model reasons with our ideas, not a cached blob."""
    parts: list[str] = []
    if include_soul:
        try:
            from mag import mag_soul
            parts.append(mag_soul.soul_context(include_state=True))
        except Exception:
            pass
    rel = retrieve(query, k=k, max_chars=max_chars)
    if rel:
        bits = ["RELATIVE CORPUS (our ideas, rightsized to this interaction):"]
        for e in rel:
            bits.append(f"- [{e['title']}] {e['snippet'][:200].strip()}")
        parts.append("\n".join(bits))
    else:
        parts.append("(no directly relevant corpus — rely on the invariants)")
    return "\n\n".join(parts)


def status() -> dict[str, Any]:
    return {"ok": True, "schema": SCHEMA,
            "corpus_files": len(corpus_index()),
            "note": "the protocol: load shared invariants + the RELATIVE corpus slice, rightsized "
                    "per interaction, so the model has our ideas as working context (not cache-hit "
                    "blobs). Applies to deepseek / grok / chatgpt alike — turtles all the way down."}


if __name__ == "__main__":
    import argparse
    import json

    ap = argparse.ArgumentParser(prog="shared-context")
    ap.add_argument("--query", default="the game and the land of forgetfulness")
    ap.add_argument("--k", type=int, default=3)
    a = ap.parse_args()
    print(json.dumps({"schema": SCHEMA, "context": context_for(a.query, k=a.k)}, indent=2, default=str))
