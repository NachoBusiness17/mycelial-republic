"""living_map — the whole project's thread, deduped and distilled to a reusable core.

The capstone (operator, 2026-08-16): "dedupe the asks, the tangents, the dropped work and we could
actually pull the whole thing into coherence... a living map of how we got here and our current
understanding of it, to pass onto future generations distilled to the very core for reuse."

Pipeline (each stage reuses an existing primitive — self-steal, no new core):
  HARVEST  stream of history items: {kind: ask|tangent|dropped|outcome, text, ts}
  DEDUPE   content-anchor hash (normalized text) -> swarm_surface-style dedupe
  WEAVE    order by ts into beads (focus_anchor thread shape) -> the coherent thread
  DISTILL  recurring keywords/themes -> the reusable core invariants
  ANCHOR   content-addressed hash of the distilled core (verkle-consistent, tamper-evident)

The output is a LIVING core: "how we got here + what we now understand + what's reusable."
Stateless-immortality: the distilled core survives any agent/session (workers die, wave persists).

Schema: living_map.v1 · deterministic $0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

SCHEMA = "living_map.v1"
MAP_PATH = ROOT / "memory" / "living_map.json"

# The VS Code Copilot session store — the project's full interaction history (weeks of sessions).
# Read-only; never written by us.
SESSION_DB = Path(r"C:\Users\foste\AppData\Roaming\Code\User\globalStorage\github.copilot-chat\session-store.db")

_KINDS = ("ask", "tangent", "dropped", "outcome", "correction")
_STOP = {
    "the", "and", "for", "then", "but", "not", "are", "was", "were", "will", "would",
    "could", "should", "this", "that", "these", "those", "with", "from", "have", "has",
    "had", "our", "your", "their", "its", "all", "any", "can", "you", "they", "them",
    "too", "also", "just", "like", "what", "when", "where", "which", "into", "out",
    "one", "get", "got", "make", "much", "more", "most", "very", "really", "we", "us",
}

# The republic's real domains (self-steal: agent_knot.EVO_DOMAINS + rib_bus/code_map taxonomy).
# Grouping the coherent braid by these = the map, the swarm, and the republic all speak one language.
DOMAIN_FINGERPRINTS = {
    "cache/economy":   ["cache", "hit", "miss", "cost", "token", "bill", "price", "spend",
                        "economic", "budget", "usage", "rate", "waste", "cheap", "expensive"],
    "verkle/truth":    ["verkle", "provenance", "anchor", "chain", "hash", "truth", "honest",
                        "ground", "prove", "verify", "ledger", "proof", "commit", "reconcile",
                        "audit", "root", "tamper", "bill"],
    "research/steal":  ["research", "steal", "frontier", "deep", "arxiv", "mine", "paper",
                        "corpus", "explore", "learn", "analy", "investigat", "study", "mining",
                        "discover", "survey", "synthes", "steal", "spore", "extract"],
    "game/world":      ["game", "player", "world", "npc", "dungeon", "quest", "campaign",
                        "adventure", "city", "build", "play", "room", "level", "battle",
                        "rogue", "mud", "simulat", "world", "village"],
    "swarm/k8s":       ["swarm", "k8s", "cluster", "worker", "drain", "queue", "parallel", "pod",
                        "distributed", "orchestrat", "deploy", "docker", "container", "flock"],
    "focus/braid":     ["focus", "tangent", "thread", "task", "track", "braid", "weave", "distract",
                        "return", "anchor", "lose", "thread", "goal", "attention"],
    "map/navigate":    ["map", "stochastic", "latent", "navigate", "coordinate", "region", "surface",
                        "space", "distance", "field", "graph", "topology", "lens", "vector"],
    "person/identity": ["player", "archetype", "persona", "shadow", "identity", "jung", "behavior",
                        "trait", "person", "psych", "guard", "personality", "self", "mind"],
}


def _classify_domain(text: str) -> str:
    """Deterministic: which republic domain this item belongs to (best keyword-overlap)."""
    tw = _toks(text)
    best, best_ov = "general", 0
    for dom, keys in DOMAIN_FINGERPRINTS.items():
        ov = len(tw & set(keys))
        if ov > best_ov:
            best, best_ov = dom, ov
    return best


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _norm(text: str) -> str:
    """Normalize for dedupe: lowercase, collapse whitespace, strip function words."""
    toks = [t for t in re.findall(r"[a-z0-9]{3,}", (text or "").lower()) if t not in _STOP]
    return " ".join(toks)


def _toks(text: str) -> set[str]:
    """Token set (stopwords stripped) for domain/overlap matching."""
    return set(re.findall(r"[a-z0-9]{3,}", (text or "").lower())) - _STOP


def _anchor(text: str) -> str:
    return hashlib.sha256(_norm(text).encode("utf-8")).hexdigest()[:16]


def _load_map() -> dict[str, Any]:
    try:
        if MAP_PATH.is_file():
            d = json.loads(MAP_PATH.read_text(encoding="utf-8", errors="replace"))
            if isinstance(d, dict):
                return d
    except Exception:
        pass
    return {"ok": True, "schema": SCHEMA, "items": [], "beads": [], "core": {}, "n_unique": 0}


def harvest(*, limit: int = 0, min_len: int = 12, db: Path | None = None) -> list[dict[str, Any]]:
    """Read the project's full history from the VS Code session store (read-only).
    Returns the real asks/tangents/dropped work as items for the living map.
    Filters out tool-call/system noise (messages containing '{')."""
    import sqlite3
    db = db or SESSION_DB
    items: list[dict[str, Any]] = []
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        con.row_factory = sqlite3.Row
        q = ("SELECT timestamp, user_message FROM turns "
             "WHERE user_message IS NOT NULL AND length(user_message) > ? "
             "AND user_message NOT LIKE '%{%' ORDER BY timestamp")
        args: list[Any] = [min_len]
        if limit:
            q += " LIMIT ?"
            args.append(limit)
        rows = con.execute(q, args).fetchall()
        con.close()
        for r in rows:
            text = str(r["user_message"] or "").strip()
            if not text:
                continue
            items.append({"kind": "ask", "ts": str(r["timestamp"] or ""), "text": text[:2000]})
    except Exception as e:
        return [{"kind": "ask", "ts": "", "text": f"HARVEST_ERROR: {e}"}]
    return items


def build_from_store(*, limit: int = 0, min_len: int = 12, write: bool = True) -> dict[str, Any]:
    """THE FULL LIVING MAP: harvest the real session store -> dedupe -> weave -> distill -> anchor."""
    items = harvest(limit=limit, min_len=min_len)
    return map_(items, write=write)


def dedupe(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Dedupe by content-anchor: same normalized text = same item, count it once (keep latest ts)."""
    seen: dict[str, dict[str, Any]] = {}
    for it in items or []:
        text = str(it.get("text", ""))
        if not text.strip():
            continue
        a = _anchor(text)
        prev = seen.get(a)
        if prev is None:
            seen[a] = dict(it)
            seen[a]["anchor"] = a
            seen[a]["repeats"] = 1
        else:
            prev["repeats"] = prev.get("repeats", 1) + 1
            if str(it.get("ts", "")) > str(prev.get("ts", "")):
                prev["ts"] = it["ts"]
    return list(seen.values())


def weave(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Order the deduped items into the coherent thread (braid beads)."""
    ordered = sorted(items, key=lambda x: str(x.get("ts", "")))
    beads = []
    for it in ordered:
        beads.append({
            "kind": it.get("kind", "ask") if it.get("kind") in _KINDS else "ask",
            "text": str(it.get("text", ""))[:500],
            "ts": it.get("ts", ""),
            "anchor": it.get("anchor", ""),
            "repeats": it.get("repeats", 1),
        })
    return beads


def distill(items: list[dict[str, Any]], *, top: int = 12) -> dict[str, Any]:
    """Extract the reusable core: the recurring themes AND the domain-grouped strands.
    Coherence = organized by the republic's real domains, not flat keywords."""
    if not items:
        return {"ok": True, "themes": [], "recurring": {}, "domains": {}}
    word_c = Counter()
    dom_c: dict[str, list[str]] = {d: [] for d in DOMAIN_FINGERPRINTS}
    for it in items:
        text = str(it.get("text", ""))
        word_c.update(re.findall(r"[a-z0-9]{3,}", _norm(text)))
        dom = _classify_domain(text)
        dom_c.setdefault(dom, []).append(text[:120])
    recurring = {w: c for w, c in word_c.most_common(top) if c >= 2}
    kinds = Counter(it.get("kind", "ask") for it in items)
    domains = {}
    for dom, texts in dom_c.items():
        if not texts:
            continue
        domains[dom] = {"n": len(texts), "sample": texts[:4]}
    return {"ok": True,
            "themes": [w for w in recurring],
            "recurring": recurring,
            "domains": domains,
            "kinds": dict(kinds),
            "n_unique": len(items)}


def map_(items: list[dict[str, Any]], *, write: bool = True) -> dict[str, Any]:
    """THE LIVING MAP: harvest -> dedupe -> weave -> distill -> anchor."""
    uniq = dedupe(items)
    beads = weave(uniq)
    core = distill(uniq)
    # anchor the whole distilled core (content-addressed, tamper-evident)
    core_text = json.dumps({"themes": core.get("themes"), "kinds": core.get("kinds")}, sort_keys=True)
    core_hash = hashlib.sha256(core_text.encode("utf-8")).hexdigest()[:16]
    result = {
        "ok": True, "schema": SCHEMA,
        "ts": _now(),
        "n_raw": len(items or []),
        "n_unique": core.get("n_unique", 0),
        "deduped_count": (len(items or []) - core.get("n_unique", 0)),
        "beads": beads,
        "core": {**core, "core_hash": core_hash},
    }
    if write:
        try:
            MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
            MAP_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError as e:
            result["write_error"] = str(e)[:120]
    return result


def status() -> dict[str, Any]:
    m = _load_map()
    return {"ok": True, "schema": SCHEMA,
            "contract": ("map(items)->dedupe by content-anchor, weave into the coherent thread, "
                         "distill the recurring core, anchor it (living map). HARVEST feeds session "
                         "history (asks/tangents/dropped work); the distilled core is what future "
                         "generations load and reuse. Deterministic $0."),
            "n_beads": len(m.get("beads", [])),
            "core_themes": (m.get("core") or {}).get("themes", [])[:8],
            "path": str(MAP_PATH)}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="living_map")
    p.add_argument("cmd", choices=["map", "status", "reset"])
    p.add_argument("--input", default="")
    a = p.parse_args(argv)
    if a.cmd == "status":
        print(json.dumps(status(), indent=2, ensure_ascii=False, default=str))
    elif a.cmd == "reset":
        if MAP_PATH.is_file():
            MAP_PATH.unlink()
        print(json.dumps({"ok": True, "reset": True}, ensure_ascii=False))
    elif a.cmd == "map":
        items = []
        if a.input and Path(a.input).is_file():
            for line in Path(a.input).read_text(encoding="utf-8", errors="replace").splitlines():
                if not line.strip():
                    continue
                try:
                    items.append(json.loads(line))
                except Exception:
                    pass
        print(json.dumps(map_(items), indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
