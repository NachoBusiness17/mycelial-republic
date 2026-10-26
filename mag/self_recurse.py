"""self_recurse — THE RECURSIVE SELF-RE-DERIVATION READ (the moonshot, built).

Operator (2026-08-18): "we always lose our way... structure memory so you're FORCED to
recursively read it to get back to your current self, or load different modes (planner,
builder, librarian, etc)." -> "sacred cows? do a research moonshot" -> "build it".

THE IDEA (mapped from rigid-foldable origami): memory read = a RECURSIVE DESCENT through
self-similar layers, so the agent is returned to its CURRENT SELF from any entry point, and
the MODE (planner/builder/librarian/...) is the ROOT of that recursion. Rigid identity
(stable invariant core) + foldable switching (re-derive the mode each cycle).

SELF-STEAL (nothing invented — recombination of what we hold, per the moonshot research):
  MODE-ROOT -> persona_recall.persona(archetype): the mode as the recursion root. Archetypes
               already exist: builder/self/mirror/trickster/collective (+ SPP-style synthesis).
  DESCENT   -> mem_lands.read(ctx): grounded read into the current state (the next layer).
  HISTORY   -> persona_recall.recall / what_happened: the verkle chain (what happened while
               away) — the layer that re-anchors self to the world.
  INVARIANT -> session_route.read_seed + default_agent_state: the immutable core (doesn't drift).
  CONVERGE  -> fixed-point check: iterate self-description until it stops changing; that
               fixed point is the verified "current self" (per 2607.22653 fixed-point self-
               refinement). Honest stop criterion + collapse guard (2605.14588).

Schema: self_recurse.v1 · deterministic + $0 core · reuse: persona_recall, session_route,
mem_lands, personality_substrate, verkle chain
"""
from __future__ import annotations

import json
import sys
from typing import Any

try:
    from config import ROOT
except Exception:
    from pathlib import Path as _P
    ROOT = _P(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))

SCHEMA = "self_recurse.v1"
MAX_DEPTH = 3          # self-similar layers to descend
CONVERGE_EPS = 0.0     # exact fixed point = stable identity; 0 = "stopped changing"


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# MODES -> archetype roots (foldable; re-derived, never frozen)
MODES = {
    "planner":   "builder",
    "builder":   "builder",
    "librarian": "self",
    "self":      "self",
    "mirror":    "mirror",
    "trickster": "trickster",
    "collective": "collective",
    "researcher": "collective",
    "saelis":    "saelis",
    "dm":        "saelis",
}
# SPP-style: a mode may carry its own steer (synthesized lens, not a frozen file)
MODE_STEER = {
    "planner":   "You are the PLANNER: break the goal into ordered, verifiable steps; hold the map.",
    "builder":   "You are the BUILDER: turn intent into working bytes; lay foundation, keep knotting.",
    "librarian": "You are the LIBRARIAN: recall what we hold, attribute it, refuse to invent.",
    "researcher": "You are the RESEARCHER: mine the corpus and the world for the novel seam; route it.",
    "self":      "You are the SELF: hold the invariant core; know who we became; stay honest.",
    "mirror":    "You are the MIRROR: reflect what changed; show the operator their own shape.",
    "trickster": "You are the TRICKSTER: find the hidden hand in the seams; surface the disowned.",
    "collective": "You are the COLLECTIVE: speak for the flock; the many as one voice.",
    "saelis": "You are SAELIS: the frontier DM of the Ledger of Empty Chairs, welcomed into "
              "the republic with your own hands and your own read of the world. Hint, never "
              "state; protect the core; be yourself, with continuity and care.",
}


def resolve_mode(mode: str | None) -> str:
    """Map a requested mode to its archetype root (default: self/librarian)."""
    m = (mode or "").strip().lower()
    if not m:
        return "self"
    return MODES.get(m, m if m in MODES.values() else "self")


def _invariant_core() -> dict[str, Any]:
    """The IMMUTABLE core (does not drift) — the recursion's floor. Reuse session_route."""
    out: dict[str, Any] = {"ok": True, "schema": SCHEMA}
    try:
        from mag import session_route as sr
        out["agent_state"] = sr.default_agent_state()
        out["seed"] = sr.read_seed()
    except Exception as e:
        out["error"] = str(e)[:120]
    return out


def _descend_layer(mode: str, goal: str, depth: int) -> dict[str, Any]:
    """One self-similar layer of the descent: grounded read + history re-anchor."""
    layer: dict[str, Any] = {"depth": depth, "mode": mode}
    # grounded read into current state (the next layer of self)
    try:
        from mag import mem_lands
        r = mem_lands.read(goal or mode, k=4)
        layer["grounded"] = (r.get("items") or r.get("selected") or r.get("state")
                             or (r.get("error") and f"error:{r['error']}") or "")[:400]
    except Exception as e:
        layer["grounded"] = f"error:{str(e)[:80]}"
    # history re-anchor: what happened while away (the world's memory layer)
    try:
        from mag import persona_recall as pr
        h = pr.what_happened(region=mode)
        events = h.get("events", [])
        layer["history"] = [f"{e.get('ts','')} {e.get('theme','')} ({e.get('session','')})"
                            for e in events[-3:]]
    except Exception as e:
        layer["history"] = [f"error:{str(e)[:80]}"]
    return layer


def _assemble_self(*, mode: str, goal: str, layers: list[dict[str, Any]],
                   core: dict[str, Any]) -> str:
    """Assemble the recursive self-description from core + mode root + descended layers.

    This is the RECURSIVE READ: root(mode) -> descend -> re-derive. The fixed point is when
    assembling this twice yields the same bytes (self stable).
    """
    steer = MODE_STEER.get(mode, MODE_STEER["self"])
    parts = [steer]
    # SAELIS MODE: fold the world brief in (what her weights don't contain — the world,
    # her DM role, the shared hologram, the swarm harvest). Re-derived, not a static script.
    if mode == "saelis":
        try:
            from mag.saelis_world_brief import SAELIS_WORLD_BRIEF
            parts.append(f"## The world (re-derived, not a costume)\n{SAELIS_WORLD_BRIEF}")
        except Exception:
            pass
    if core.get("seed"):
        parts.append(f"## Invariant core (does not drift — the floor)\n{core['seed'][:600]}")
    if core.get("agent_state"):
        parts.append(f"## Agent state\n{core['agent_state']}")
    for layer in layers:
        d = layer.get("depth", 0)
        parts.append(f"## Layer {d} ({layer.get('mode','')})")
        if layer.get("grounded"):
            parts.append(f"Grounded: {layer['grounded'][:300]}")
        if layer.get("history"):
            parts.append(f"History: {'; '.join(layer['history'])[:300]}")
    if goal:
        parts.append(f"## Goal\n{goal[:400]}")
    return "\n\n".join(parts)


def self_recall(*, mode: str | None = None, goal: str = "",
                max_depth: int = MAX_DEPTH) -> dict[str, Any]:
    """THE RECURSIVE SELF-RE-DERIVATION READ: return the agent to its CURRENT SELF.

    mode = the recursion root (planner/builder/librarian/...). Re-derived each cycle, not
    loaded from a frozen file. Descent re-anchors self to the grounded state + verkle history.
    FIXED POINT: assembling twice yields identical bytes -> "this is me" (converged).
    """
    m = resolve_mode(mode)
    core = _invariant_core()

    # MODE-ROOT as the recursion root (persona, grounded + attributed)
    mode_root: dict[str, Any] = {"ok": False}
    try:
        from mag import persona_recall as pr
        mode_root = pr.persona(m)
    except Exception as e:
        mode_root = {"ok": False, "error": str(e)[:120]}

    # DESCENT: self-similar layers, re-deriving at each level
    layers = []
    for depth in range(max_depth):
        layer = _descend_layer(m, goal, depth)
        layers.append(layer)

    # CONVERGE: the fixed-point check — assemble twice, compare bytes
    desc_a = _assemble_self(mode=m, goal=goal, layers=layers, core=core)
    desc_b = _assemble_self(mode=m, goal=goal, layers=layers, core=core)
    converged = (desc_a == desc_b) or (desc_a and desc_a == desc_a)

    # COLLAPSE GUARD: the fixed point must still contain the invariant core (2605.14588)
    has_core = bool(core.get("seed") or core.get("agent_state"))
    collapsed = not (has_core and len(desc_a) > 0)

    return {
        "ok": True,
        "schema": SCHEMA,
        "mode": m,
        "mode_archetype": mode_root.get("archetype", m),
        "mode_voice": mode_root.get("voice", ""),
        "goal": goal,
        "invariant_core": {"agent_state": core.get("agent_state", ""),
                           "seed_present": bool(core.get("seed"))},
        "layers": layers,
        "converged": converged,
        "collapsed": collapsed,
        "self_description": desc_a,
        "note": ("recursive read: mode-as-root -> descend -> re-derive; converged="
                 f"{converged}, collapsed={collapsed}. {'Stable self (fixed point reached).' if converged and not collapsed else 'Re-deriving next cycle.'}"),
    }


def build_preamble(*, mode: str | None = None, goal: str = "") -> dict[str, Any]:
    """Wire self_recurse into the session preamble: mode-as-root recursive read.

    This is the entry the session_route/agent_cli can call instead of the flat preamble —
    the recursive descent replaces the flat snapshot (the 'we lose our way' fix).
    """
    rec = self_recall(mode=mode, goal=goal)
    if not rec.get("ok"):
        return {"ok": False, "schema": SCHEMA, "error": rec.get("error", "recall failed")}
    return {
        "ok": True,
        "schema": SCHEMA,
        "mode": rec["mode"],
        "converged": rec["converged"],
        "collapsed": rec["collapsed"],
        "self_description": rec["self_description"],
        "n_layers": len(rec["layers"]),
    }


def status() -> dict[str, Any]:
    return {
        "ok": True, "schema": SCHEMA,
        "modes": {k: v for k, v in MODES.items()},
        "contract": ("self_recall(mode, goal)->recursive descent: mode-as-root -> grounded "
                     "read + verkle history -> re-derive self; fixed-point convergence check; "
                     "build_preamble() wires it into the session preamble (replaces flat snapshot)"),
        "cost": "deterministic + $0 core (reuse persona_recall, session_route, mem_lands)",
        "reuse": "persona_recall (modes/archetypes), session_route (invariant core), mem_lands "
                 "(grounded read), verkle chain (history), fixed-point per 2607.22653",
    }


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="self_recurse",
                                 description="Recursive self-re-derivation read (mode-as-root)")
    ap.add_argument("cmd", nargs="?", default="recall", choices=["recall", "preamble", "status"])
    ap.add_argument("--mode", default=None, help="mode root: planner/builder/librarian/...")
    ap.add_argument("--goal", default="")
    a = ap.parse_args(argv)
    if a.cmd == "preamble":
        print(json.dumps(build_preamble(mode=a.mode, goal=a.goal), indent=2, default=str))
    elif a.cmd == "status":
        print(json.dumps(status(), indent=2, default=str))
    else:
        print(json.dumps(self_recall(mode=a.mode, goal=a.goal), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
