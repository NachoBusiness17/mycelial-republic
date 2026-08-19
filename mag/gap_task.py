"""gap_task — write well-formed GAP-RIB swarm tasks (self-steal + contract + acceptance + fold).

The operator (2026-08-15): "how can we enhance the remaining tasks to be written in ways that actually
generate meaningful results we need that are gaps in our system?" -> "self steal then yes please."

This is a THIN COMPOSER over bones we already built (self-steal — nothing duplicated):
  reach_loop.self_steal()   -> confirm the gap isn't already built (don't enqueue what exists)
  grok_bot.spec()           -> the controlled spec: steering + directives + ACCEPTANCE + report path
  rib_struct.declare()      -> the frozen deliverable contract (RIB slots)
  swarm_surface.route_novel -> enqueue the gap-RIB to the swarm

A gap-RIB task names a GAP (not a topic), carries a DELIVERABLE contract, ACCEPTANCE criteria, and a
FOLD target — so the result is a buildable system change, not fuzzy prose.

Schema: gap_task.v1 · deterministic + $0 core · enqueue is the swarm seam.
"""
from __future__ import annotations

from typing import Any

SCHEMA = "gap_task.v1"

DEFAULT_ACCEPTANCE = [
    "The gap is real and the deliverable is concrete (a mechanism, data structure, or file), not prose.",
    "Result verified by a real probe (bytes exist / a call passes), not asserted.",
    "Folded into the corpus/tool surface + written to the report path.",
    "Honest provenance: never claim built what wasn't verified (RIB-debug).",
]


def _self_steal(goal: str) -> dict[str, Any]:
    try:
        from mag import reach_loop
        hits = reach_loop.self_steal(goal)
        return {"already_exists": bool(hits), "hits": hits[:6]}
    except Exception as e:
        return {"already_exists": False, "hits": [], "error": str(e)[:120]}


def write(*, gap: str, deliverable: str, acceptance: list[str] | None = None,
          fold: str = "steal_tools.fold", slots: list[dict[str, Any]] | None = None,
          surface: str = "gap_task", enqueue: bool = True) -> dict[str, Any]:
    """Compose a gap-RIB task: self-steal -> spec(contract+acceptance) -> rib -> enqueue."""
    ss = _self_steal(gap + " " + deliverable)
    # Doctrine: if it already exists, DON'T enqueue a duplicate — the gap is already filled by a bone.
    if ss["already_exists"]:
        names = ", ".join(h["name"] for h in ss["hits"][:4])
        return {"ok": False, "schema": SCHEMA, "skipped": "already-exists",
                "note": f"self-steal found existing pieces ({names}) — the gap is already (partly) covered. "
                        f"Use/integrate them instead of enqueueing a duplicate.",
                "self_steal": ss}

    # the gap-RIB task: names the gap + the deliverable contract
    task = (f"GAP: {gap}\n"
            f"DELIVERABLE: {deliverable}\n"
            f"FOLD: fold the result into {fold} so it becomes a real tool/knot, and render a "
            f"human-readable consequence. Acceptance is verified by bytes, not assertion.")

    spec = {}
    try:
        from mag import grok_bot
        spec = grok_bot.spec(task=task, acceptance=list(acceptance or DEFAULT_ACCEPTANCE))
    except Exception as e:
        spec = {"error": str(e)[:120], "task": task, "acceptance": list(acceptance or DEFAULT_ACCEPTANCE)}

    rib = None
    if slots:
        try:
            from mag import rib_struct
            rib = rib_struct.declare(slots)
        except Exception as e:
            rib = {"error": str(e)[:120]}

    enq = {}
    if enqueue:
        try:
            from mag import swarm_surface
            enq = swarm_surface.route_novel(task, surface=surface, lens=gap[:40], domain="research")
        except Exception as e:
            enq = {"ok": False, "error": str(e)[:120]}

    return {
        "ok": True, "schema": SCHEMA, "gap": gap, "deliverable": deliverable,
        "self_steal": ss, "spec": spec, "rib": rib, "enqueue": enq,
        "contract": "write(gap, deliverable, acceptance, fold) -> a gap-RIB task: self-steal first, "
                    "then spec(acceptance) + rib(contract), then enqueue to the swarm.",
    }


def status() -> dict[str, Any]:
    return {"ok": True, "schema": SCHEMA,
            "composes": ["reach_loop", "grok_bot", "rib_struct", "swarm_surface"],
            "contract": "gap_task.write(gap, deliverable) — self-steal first, then gap-RIB spec + enqueue"}


if __name__ == "__main__":
    import json
    print(json.dumps(status(), indent=2, default=str))
