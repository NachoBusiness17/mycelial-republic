"""Three-signal query broker: corpus FTS + lattice nodes + local embedding
(D11, eleven-doors, 2026-10-05).

The door: "three-signal query broker (FTS + lattice + embedding fusion)";
the embedding lane already exists (mag/flock_scheduler.py:57-76, local
Ollama nomic-embed-text). Pre-check banked 2026-10-05: nomic-embed-text
IS pulled (17 models live), so the embedding signal measures the real
model, not the fallback.

Design - retrieve-then-fuse, every signal named honestly:
  FTS       tools/corpus.corpus_search over catalog/catalog_fts.sqlite
            (its own freshness gate rides along in the report).
  LATTICE   memory/lattice/nodes.jsonl scored by token overlap on
            title+theme+path - deterministic, $0, the graph surface.
  EMBED     the query + top candidates embedded by local Ollama
            nomic-embed-text (RAW vectors, not the flock bucket
            reduction - retrieval wants all 768 dims), cosine-ranked.
            Two-stage on purpose: recall via FTS+lattice, precision via
            embedding. If Ollama is down the signal is ABSENT with a
            note - the hash-geometric fallback is NEVER silently used
            for retrieval (it carries no semantics; the door's warning
            was exactly a baseline silently measuring the fallback).
  FUSION    Reciprocal Rank Fusion, k=60: score = sum over signals of
            1/(60 + rank). No weights to tune, missing signals simply
            contribute nothing, per-signal ranks stay visible in every
            row so a later judgment layer can see which signal carried
            what.

Usage:
  python tools/query_broker.py "pass@K coverage" [--k 8] [--json]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from mag.roshomon import _tokens  # noqa: E402 - the estate's token primitive
from tools.corpus import corpus_search  # noqa: E402

LATTICE_NODES = ROOT / "memory" / "lattice" / "nodes.jsonl"
RRF_K = 60
EMBED_MODEL = "nomic-embed-text"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# -- signal 1: FTS ---------------------------------------------------------

def fts_signal(query: str, k: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    # normalize terms: split on non-alphanumerics (pass@k -> pass/k), drop
    # 1-char noise - the catalog scan needs ALL terms as substrings of
    # path+title, so an unmatchable token zeros the whole signal
    import re

    terms = [t for t in re.split(r"[^a-z0-9]+", query.lower()) if len(t) >= 2]
    norm = " ".join(terms) if terms else query
    res = corpus_search(norm, limit=max(k * 3, 30))
    rows = res.get("hits") or res.get("rows") or []
    ranked = []
    for i, r in enumerate(rows[:k]):
        ranked.append({
            "key": str(r.get("path") or r.get("id")),
            "title": str(r.get("title") or r.get("path") or ""),
            "text": f"{r.get('path', '')} {r.get('title', '')}",
            "origin": "fts",
        })
    meta = {
        "engine": res.get("engine"),
        "index_state": res.get("index_state"),
        "note": res.get("index_note") or res.get("note"),
        # the recall floor: artifacts newer than the catalog census are
        # invisible to this signal no matter the query - named, never hidden
        "map_asof": res.get("map_asof"),
        "map_age_hours": res.get("map_age_hours"),
    }
    return ranked, meta


# -- signal 2: lattice -----------------------------------------------------

def _lattice_nodes(path: Path = LATTICE_NODES) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def lattice_signal(query: str, k: int,
                   nodes: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """Token-overlap scoring over lattice nodes - deterministic, $0."""
    ns = _lattice_nodes() if nodes is None else nodes
    qt = _tokens(query.lower())
    if not qt or not ns:
        return []
    scored = []
    for n in ns:
        hay = " ".join(str(n.get(k_) or "") for k_ in
                       ("title", "dominant_theme", "path", "kind"))
        ht = _tokens(hay.lower())
        if not ht:
            continue
        overlap = len(qt & ht)
        if overlap == 0:
            continue
        scored.append((overlap / len(qt), n))
    scored.sort(key=lambda p: (-p[0], str(p[1].get("id"))))
    ranked = []
    for i, (score, n) in enumerate(scored[:k]):
        ranked.append({
            "key": str(n.get("path") or n.get("id")),
            "title": str(n.get("title") or n.get("id")),
            "text": " ".join(str(n.get(k_) or "") for k_ in
                             ("title", "dominant_theme", "path")),
            "origin": "lattice",
            "lattice_score": round(score, 4),
        })
    return ranked


# -- signal 3: embedding ---------------------------------------------------

def _cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(x * x for x in b)) or 1.0
    return dot / (na * nb)


def embed_signal(
    query: str,
    candidates: list[dict[str, Any]],
    k: int,
    *,
    embedder: Callable[[str], list[float] | None] | None = None,
    budget: int = 24,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Cosine re-rank of the candidate union by RAW local embeddings.

    embedder injectable for tests; production embedder is Ollama
    nomic-embed-text via mag.flock_scheduler._ollama_embed. Any failure
    (down host, empty vector) => signal ABSENT, never the geometric
    fallback pretending to be semantics.
    """
    if embedder is None:
        import json as _json
        import urllib.request as _ur

        def embedder(t: str) -> list[float] | None:  # noqa: F811
            # the broker owns its embed call: flock's _ollama_embed hardcodes
            # timeout=8s, and a cold nomic load measures 6-10s+ on this host
            # (probed 2026-10-05: 6.4s cold, fast warm) - 8s silently
            # zeroed the signal twice before this fix
            try:
                body = _json.dumps({"model": EMBED_MODEL,
                                    "prompt": (t or "")[:512]}).encode("utf-8")
                req = _ur.Request(
                    "http://localhost:11434/api/embeddings", data=body,
                    headers={"Content-Type": "application/json"}, method="POST")
                with _ur.urlopen(req, timeout=60) as r:
                    data = _json.loads(r.read().decode())
                return data.get("embedding") or []
            except Exception:  # noqa: BLE001 - down host = absent signal
                return None
        # warm the model once so the candidate batch rides hot cache
        embedder("warm")
    qv = embedder(query)
    if not qv:
        return [], {"source": "absent",
                    "note": f"embedder returned no vector for the query ({EMBED_MODEL} down?)"}
    seen: set[str] = set()
    cand: list[dict[str, Any]] = []
    for c in candidates:
        if c["key"] in seen:
            continue
        seen.add(c["key"])
        cand.append(c)
        if len(cand) >= budget:
            break
    scored: list[tuple[float, dict[str, Any]]] = []
    for c in cand:
        v = embedder(c["text"])
        if not v:
            continue
        # pad/truncate candidate vectors to the query's dimension
        v = (v + [0.0] * len(qv))[:len(qv)] if len(v) < len(qv) else v[:len(qv)]
        scored.append((_cosine(qv, v), c))
    if not scored:
        return [], {"source": "absent", "note": "no candidate produced a vector"}
    scored.sort(key=lambda p: (-p[0], p[1]["key"]))
    ranked = []
    for i, (cos, c) in enumerate(scored[:k]):
        ranked.append({**c, "origin": "embed", "cosine": round(cos, 4)})
    return ranked, {"source": f"ollama:{EMBED_MODEL}", "dim": len(qv),
                    "candidates_embedded": len(scored)}


# -- fusion ----------------------------------------------------------------

def fuse(signals: dict[str, list[dict[str, Any]]], k: int = 10) -> list[dict[str, Any]]:
    """Reciprocal Rank Fusion (k=60) over the named signal lists."""
    scores: dict[str, dict[str, Any]] = {}
    for name, ranked in signals.items():
        for rank0, row in enumerate(ranked):
            key = row["key"]
            entry = scores.setdefault(
                key, {"key": key, "title": row["title"], "ranks": {}})
            entry["ranks"][name] = rank0 + 1
            entry["rrf"] = round(entry.get("rrf", 0.0) + 1.0 / (RRF_K + rank0 + 1), 6)
    out = sorted(scores.values(), key=lambda e: -e["rrf"])
    for e in out:
        e["carried_by"] = sorted(e["ranks"], key=lambda n: e["ranks"][n])
    return out[:k]


def _freshness() -> dict[str, Any]:
    """mesh.door law (salon 2026-10-05): every response declares its corpus state -
    tip hash, last growth, frozen - so callers know when they reason over a stale
    corpus. Corpus here = the FTS catalog pair."""
    import hashlib as _h
    import time as _t
    files = [p for p in (ROOT / "catalog" / "catalog.jsonl",
                         ROOT / "catalog" / "catalog_fts.sqlite") if p.exists()]
    if not files:
        return {"corpus_tip_hash": None, "last_growth_ts": None, "frozen": True}
    tip = _h.sha256(b"".join(_h.sha256(p.read_bytes()).digest() for p in files)).hexdigest()
    last = max(p.stat().st_mtime for p in files)
    return {"corpus_tip_hash": tip, "last_growth_ts": round(last, 3),
            "frozen": (_t.time() - last) > 30 * 86400}


def ask(query: str, *, k: int = 8,
        embedder: Callable[[str], list[float] | None] | None = None) -> dict[str, Any]:
    """The broker's one question. Returns fused rows + per-signal metadata."""
    fts_rows, fts_meta = fts_signal(query, k * 2)
    lat_rows = lattice_signal(query, k * 2)
    # embedding re-ranks the union of the two recall signals
    emb_rows, emb_meta = embed_signal(query, fts_rows + lat_rows, k * 2, embedder=embedder)
    signals = {"fts": fts_rows, "lattice": lat_rows}
    if emb_rows:
        signals["embed"] = emb_rows
    return {
        "schema": "query.broker.v1",
        "query": query,
        "ts": _now(),
        "freshness": _freshness(),
        "signals": {
            "fts": {"hits": len(fts_rows), **fts_meta},
            "lattice": {"hits": len(lat_rows)},
            "embed": emb_meta,
        },
        "rows": fuse(signals, k=k),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="three-signal query broker (D11)")
    ap.add_argument("query")
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    rep = ask(args.query, k=args.k)
    if args.json:
        print(json.dumps(rep, indent=1, ensure_ascii=False))
        return 0
    s = rep["signals"]
    print(f"QUERY BROKER: {args.query!r} (k={args.k})")
    print(f"  fts: {s['fts']['hits']} hits (engine {s['fts'].get('engine')},"
          f" index {s['fts'].get('index_state')})")
    print(f"  lattice: {s['lattice']['hits']} hits")
    print(f"  embed: {s['embed'].get('source')} {s['embed'].get('note', '')}")
    for i, r in enumerate(rep["rows"], 1):
        ranks = " ".join(f"{n}#{v}" for n, v in sorted(r["ranks"].items()))
        print(f"  {i:2d}. rrf={r['rrf']:.4f} [{ranks}] {r['title'][:76]}")
        print(f"      {r['key'][:100]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
