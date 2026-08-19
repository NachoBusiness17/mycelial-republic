"""reach_loop — the loop for creating the pieces you reach for, SELF-STEAL FIRST.

The operator (2026-08-15): "auto code the pieces you need when you reach for them after making sure
they're not already there, then find what was intended to be there from our corpus, and propose a couple
directions we could take it and why what that might do."

This is an ORCHESTRATOR that composes pieces we ALREADY built (self-steal — nothing duplicated):
  reach_protocol.reach()       -> the reach/search primitive
  steal_tools.tools()          -> the corpus-as-tools surface (SENSE)
  shared_context.context_for() -> lexical retrieval of INTENT from the corpus
  tool_lifecycle.run_tool()    -> the creation lifecycle (used ONLY if nothing already exists)
  swarm_worker / swarm_surface -> routing novel work to the swarm

reach(goal) -> {
  self_steal:    did we already have a piece that does this? -> if found, STOP (don't rebuild)
  corpus_intent: what the corpus says was INTENDED to be here (mechanism + invariant)
  directions:    2-3 proposals, each {direction, why, effect}
  auto_code:     ONLY if not already there -> route creation through tool_lifecycle, not ad-hoc
}

Schema: reach_loop.v1 · deterministic + $0 core · tool_lifecycle + swarm are the creation/routing seams.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SCHEMA = "reach_loop.v1"


def _tokens(s: str) -> set[str]:
    return set(w for w in re.split(r"[^a-z0-9]+", s.lower()) if len(w) > 2)


def self_steal(goal: str) -> list[dict[str, Any]]:
    """Step 1 — is it already there? Search mag/ modules + the steal-tools surface. If found, we STOP."""
    g = _tokens(goal)
    hits: list[dict[str, Any]] = []
    # modules in mag/
    for p in sorted((ROOT / "mag").glob("*.py")):
        name = p.stem.lower()
        if name.startswith("_"):
            continue
        nt = set(name.replace("_", " ").split())
        shared = len(nt & g)
        # require real overlap (>=2 shared tokens, or exact-name match) to cut false positives
        if name in g or shared >= 2:
            hits.append({"kind": "module", "name": p.stem, "file": f"mag/{p.name}"})
    # corpus-as-tools (steal_tools)
    try:
        from mag import steal_tools
        for t in steal_tools.tools():
            if g & _tokens(t["theme"]) or g & _tokens(t["invariant"]):
                hits.append({"kind": "steal_tool", "name": t["name"], "theme": t["theme"],
                             "file": t["file"]})
    except Exception:
        pass
    # dedupe by name, cap
    seen: set[str] = set(); out = []
    for h in hits:
        if h["name"] in seen:
            continue
        seen.add(h["name"]); out.append(h)
    return out[:12]


def corpus_intent(goal: str) -> dict[str, Any]:
    """Step 2 — what did we intend to be here? Lexical retrieval over the corpus-as-tools."""
    mechanism, invariant = "", ""
    best = 0
    try:
        from mag import steal_tools
        g = _tokens(goal)
        for t in steal_tools.tools():
            score = len(g & _tokens(t["theme"])) + len(g & _tokens(t["mechanism"])) * 2
            if score > best:
                best = score; mechanism = t["mechanism"]; invariant = t["invariant"]
    except Exception:
        pass
    return {"found": bool(mechanism), "mechanism": mechanism[:400], "invariant": invariant,
            "source": "steal_tools corpus surface"}


def propose(goal: str, hits: list[dict[str, Any]], intent: dict[str, Any]) -> list[dict[str, Any]]:
    """Step 3 — a couple directions, why, and what each would do."""
    if hits:
        # A piece already exists -> the direction is to USE/complete it, not rebuild.
        names = ", ".join(h["name"] for h in hits[:3])
        return [
            {"direction": f"Use what already exists ({names})",
             "why": "Rebuilding would duplicate real bytes — the loop says don't.",
             "effect": "The reach resolves to an existing piece; we integrate/verify it."},
            {"direction": "Wire it into the cadence if it's dormant (a built-but-unrun loop)",
             "why": "The most common failure is a piece that exists but isn't running (e.g. a drainer without a live governor).",
             "effect": "The existing piece actually runs and produces bytes."},
            {"direction": "Let the swarm deepen it if the goal is genuinely novel",
             "why": "If the existing pieces only partially cover the reach, route the gap to the swarm.",
             "effect": "The swarm returns a mechanism to fold in."},
        ]
    if intent.get("found"):
        return [
            {"direction": f"Auto-code it, seeded from the intended mechanism ({intent['invariant']})",
             "why": "The corpus already holds the design — we build the thin piece that matches it.",
             "effect": "A new tool appears that matches what we meant to have."},
            {"direction": "Route creation through tool_lifecycle (BORN->PROPAGATED), not ad-hoc",
             "why": "Creation itself should live the standing-wave lifecycle, not be built-and-dropped.",
             "effect": "The new tool is born, verified, and propagated like every other piece."},
            {"direction": "Ask the swarm for a second mechanism before committing",
             "why": "Novel pieces benefit from a frontier witness before we encode it.",
             "effect": "We avoid encoding a half-intended mechanism."},
        ]
    return [
        {"direction": "Reach the swarm for the mechanism first",
         "why": "The corpus has no intended mechanism yet — so we route the novel reach out.",
         "effect": "A mechanism comes back to seed the piece."},
        {"direction": "Write the intent into the corpus before building",
         "why": "The loop only works if the intent is findable; capture it first.",
         "effect": "Future reaches for the same goal resolve to the intended piece."},
    ]


def auto_code(name: str, invariant: str, need: str) -> dict[str, Any]:
    """Step 4 — create a piece, but ONLY through tool_lifecycle (never ad-hoc)."""
    try:
        from mag import tool_lifecycle
        return tool_lifecycle.run_tool(name, invariant, need)
    except Exception as e:
        return {"ok": False, "error": str(e)[:120], "note": "tool_lifecycle not reachable"}


def reach(goal: str) -> dict[str, Any]:
    hits = self_steal(goal)
    intent = corpus_intent(goal)
    directions = propose(goal, hits, intent)
    built = {}
    if not hits and intent.get("found"):
        built = auto_code("reach_" + (intent["invariant"] or "piece").lower().replace(" ", "_"),
                          intent["invariant"], goal)
    return {
        "ok": True, "schema": SCHEMA, "goal": goal,
        "self_steal": {"already_exists": bool(hits), "hits": hits},
        "corpus_intent": intent,
        "directions": directions,
        "auto_code": built if built else {"skipped": "already exists or no intent found — loop says don't build"},
        "contract": "reach(goal): self-steal -> corpus intent -> propose directions -> auto_code only if missing",
    }


def status() -> dict[str, Any]:
    return {"ok": True, "schema": SCHEMA,
            "composes": ["reach_protocol", "steal_tools", "shared_context", "tool_lifecycle", "swarm"],
            "contract": "reach(goal) — self-steal first, then corpus intent, then directions, then auto-code only if missing"}


if __name__ == "__main__":
    import json
    print(json.dumps(status(), indent=2, default=str))
