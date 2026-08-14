"""reach_protocol — reach-catch: when a dumb agent reaches for something not there, it RECOVERS.

OPERATOR (2026-08-12): "most of the time the data exists we just forgot how to find it we need a
reach for something not there catch protocol so dumb agents have some sort of internal logic
quantized from frontier" + "maybe they steal too" + "local agents around them through tool use and
their look from the game feature".

THE INSIGHT: a miss is usually a FORGOTTEN-HOW-TO-FIND, not an absence. So on a reach-miss the agent
must NOT hallucinate absence — it recovers by searching what EXISTS, and it STEALS (self + external)
to find the recovery logic. Local helper agents do this THROUGH TOOL USE, navigating by the GAME
WORLD MAP (game_world_map) — the logical map of every system = the "look" that says where each kind
of thing lives.

SCHEMA: reach_protocol.v1 · deterministic + $0 · pure stdlib · never fabricates an absence.

SELF-STEAL: game_world_map (the look), agent_signature (real vs phantom), rib_bus (memory RIBs),
arxiv_mine (mine-like-steal), session store / memory/agent_sessions (old conversations).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))

SCHEMA = "reach_protocol.v1"

# ── THE GAME WORLD MAP "LOOK" — where each KIND of thing lives (grounded in game_world_map) ──
GAME_LOOK: dict[str, list[str]] = {
    "memory":        ["memory/", "memory/verkle", "memory/knots", "memory/learn"],
    "verkle":        ["memory/verkle", "memory/knots", "memory/chain"],
    "instructions":  ["memory/rib_bus", "memory/rib", "docs/ref", "docs/FRAMEWORK_LOAD.md"],
    "doctrine":      ["memory/rib/", "docs/ORIGIN.md", "docs/CONSTITUTION.md"],
    "steal":         ["memory/steal", "memory/learn", "/memories/repo"],
    "agent":         ["mag/", "mag/seat_registry.py", "memory/registry_state"],
    "vendor":        ["field-strike-the-chord", "research/cl4r1t4s"],
    "session":       ["memory/agent_sessions", "memory/handoffs", "memory/runs"],
    "runs":          ["memory/runs", "memory/runs/seat_steer", "memory/runs/frontier_advice"],
    "good_work":     ["memory/rib_bus/good-work.json", "memory/rib_bus/research.json"],
    "self":          ["memory/rib_bus/self-shape.json", "/memories/repo", "/memories/session"],
}


def _walk(dir_paths: list[str], max_hits: int = 5) -> list[str]:
    hits = []
    for d in dir_paths:
        p = ROOT / d if not d.startswith(("/memories", "field-strike", "research")) else ROOT.parent / d
        if not p.exists():
            continue
        if p.is_file():
            hits.append(str(p.relative_to(ROOT.parent)) if str(p).startswith(str(ROOT.parent)) else str(p))
            if len(hits) >= max_hits:
                return hits
            continue
        # shallow walk (2 levels) to keep it cheap + deterministic
        try:
            for sub in p.iterdir():
                hits.append(str(sub.relative_to(ROOT.parent)) if str(sub).startswith(str(ROOT.parent)) else str(sub))
                if len(hits) >= max_hits:
                    return hits
                if sub.is_dir():
                    for sub2 in list(sub.iterdir())[:6]:
                        hits.append(str(sub2.relative_to(ROOT.parent)) if str(sub2).startswith(str(ROOT.parent)) else str(sub2))
                        if len(hits) >= max_hits:
                            return hits
        except Exception:
            continue
    return hits


def game_look(kind: str) -> dict[str, Any]:
    """THE LOOK from the game feature: return where a KIND of thing lives (the logical map)."""
    k = (kind or "").strip().lower()
    dirs = GAME_LOOK.get(k) or GAME_LOOK.get("memory")
    return {"ok": True, "schema": SCHEMA, "kind": k,
            "where_it_lives": dirs, "hits": _walk(dirs, max_hits=6)}


def reach(target: str, *, kind: str = "", max_hits: int = 6) -> dict[str, Any]:
    """REACH for something. On a miss this is NOT an absence — it's a 'forgot how to find it'.
    Returns found + location + evidence. Never fabricates; reports honestly."""
    target = (target or "").strip()
    if not target:
        return {"ok": False, "schema": SCHEMA, "found": False, "error": "empty target"}
    # 1) exact-ish filename probe
    hits = []
    low = target.lower()
    probe = [ROOT, ROOT / "mag", ROOT / "memory", ROOT.parent / "field-strike-the-chord"]
    for base in probe:
        if not base.is_dir():
            continue
        for p in list(base.glob("*"))[:400]:
            if low in p.name.lower():
                hits.append(str(p.relative_to(ROOT.parent)) if str(p).startswith(str(ROOT.parent)) else str(p))
                if len(hits) >= max_hits:
                    break
    # 2) game-look for the kind (where it lives) + walk
    if not hits and kind:
        look = game_look(kind)
        hits = [h for h in look.get("hits") or [] if low in h.lower()][:max_hits]
    # 3) session store / old conversations (if reachable) — cheap, stdlib
    if not hits:
        try:
            sess_dir = ROOT / "memory" / "agent_sessions"
            for p in list(sess_dir.glob("*.json"))[:80] if sess_dir.is_dir() else []:
                if low in p.name.lower():
                    hits.append(str(p.relative_to(ROOT.parent)))
                    if len(hits) >= max_hits:
                        break
        except Exception:
            pass
    return {"ok": True, "schema": SCHEMA, "target": target[:160], "found": bool(hits),
            "hits": hits, "note": "miss = forgot how to find it, NOT an absence (see steal_recover)"}


def steal_recover(target: str) -> dict[str, Any]:
    """STEAL-RECOVER: on a reach-miss, steal (self) the recovery logic — search our own steal docs,
    repo memory, and the good-work RIBs for how to recover this target. Never fabricates a hit."""
    found = []
    low = target.lower()
    sources = [
        ROOT / "memory" / "steal",
        ROOT / "memory" / "learn",
        ROOT / "memory" / "rib_bus",
        ROOT / "docs" / "ref",
    ]
    for d in sources:
        if not d.is_dir():
            continue
        for p in list(d.glob("*"))[:300]:
            if low in p.name.lower():
                try:
                    first = p.read_text(encoding="utf-8", errors="replace")[:240].splitlines()[0]
                except Exception:
                    first = ""
                found.append({"source": str(p.relative_to(ROOT.parent)), "hint": first[:120]})
                if len(found) >= 6:
                    break
    return {"ok": True, "schema": SCHEMA, "target": target[:160], "recovered": bool(found),
            "found": found,
            "note": "local agents recover through tool use; if nothing found, it is truly absent — "
                    "report that honestly, never fabricate"}


# ── THE INTERNAL LOGIC QUANTIZED FROM FRONTIER (carried by dumb agents) ──
RECOVERY_RIBS: list[str] = [
    "A miss is usually a FORGOTTEN-HOW-TO-FIND, not an absence. Before declaring 'not found', "
    "search what EXISTS: memory, rib_bus, steal docs, old conversations, the field corpus.",
    "Use the GAME LOOK (game_world_map) to navigate: each kind of thing lives in a known place "
    "(memory -> World-Memory/verkle, instructions -> rib_bus, steals -> memory/steal, vendors -> "
    "field corpus). Look there first.",
    "STEAL to recover: search our own steal docs + repo memory + good-work RIBs before giving up. "
    "Local agents around the frontier do this through TOOL USE, not by asking the operator.",
    "NEVER fabricate a hit or an absence. If the search genuinely finds nothing, report it as "
    "'truly absent' — the mirror corrects false finds.",
    "Quantized from frontier: this logic is compact on purpose — a dumb (local/flash) agent carries "
    "it without a frontier round-trip.",
]


def mount_recovery() -> dict[str, Any]:
    """The quantized internal logic dumb agents carry (also published to memory/rib_bus/recovery.json)."""
    return {"ok": True, "schema": SCHEMA, "n_recovery_ribs": len(RECOVERY_RIBS), "ribs": RECOVERY_RIBS}


def catch(target: str, *, kind: str = "") -> dict[str, Any]:
    """THE REACH-CATCH PROTOCOL: reach -> if miss, steal-recover (self) + game-look. Returns the
    honest outcome: found (with location) OR recovered-steal (with hint) OR truly-absent."""
    r = reach(target, kind=kind)
    if r.get("found"):
        return {"ok": True, "schema": SCHEMA, "outcome": "found", "target": target[:160],
                "hits": r.get("hits")}
    s = steal_recover(target)
    if s.get("recovered"):
        return {"ok": True, "schema": SCHEMA, "outcome": "recovered-steal", "target": target[:160],
                "found": s.get("found"), "look": game_look(kind).get("where_it_lives")}
    return {"ok": True, "schema": SCHEMA, "outcome": "truly-absent", "target": target[:160],
            "note": "genuinely absent after reach + steal-recover — reported honestly, never fabricated"}


def status() -> dict[str, Any]:
    return {"ok": True, "schema": SCHEMA,
            "contract": "reach(target, kind) = find what exists; game_look(kind) = the game-world "
                        "map 'look' (where each kind lives); steal_recover(target) = self-steal "
                        "recovery logic on a miss; catch(target) = reach -> steal-recover -> "
                        "honest outcome. Dumb agents carry RECOVERY_RIBS (internal logic quantized "
                        "from frontier).",
            "reuse": "game_world_map + agent_signature + rib_bus + arxiv_mine",
            "n_recovery_ribs": len(RECOVERY_RIBS),
            "game_kinds": sorted(GAME_LOOK)}


def main(argv: list[str] | None = None) -> int:
    import argparse

    p = argparse.ArgumentParser(prog="reach_protocol")
    sub = p.add_subparsers(dest="cmd")
    r = sub.add_parser("reach")
    r.add_argument("target")
    r.add_argument("--kind", default="")
    c = sub.add_parser("catch")
    c.add_argument("target")
    c.add_argument("--kind", default="")
    l = sub.add_parser("look")
    l.add_argument("kind")
    sub.add_parser("recovery")
    sub.add_parser("status")
    a = p.parse_args(argv)
    if a.cmd == "reach":
        print(json.dumps(reach(a.target, kind=a.kind), indent=2, default=str))
    elif a.cmd == "catch":
        print(json.dumps(catch(a.target, kind=a.kind), indent=2, default=str))
    elif a.cmd == "look":
        print(json.dumps(game_look(a.kind), indent=2, default=str))
    elif a.cmd == "recovery":
        print(json.dumps(mount_recovery(), indent=2, default=str))
    else:
        print(json.dumps(status(), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
