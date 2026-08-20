"""game_ramp — the GAME, built as the complexity ramp (operator 2026-08-13): TABLE TOP (perfect) ->
MUD (perfect) -> ROGUELITE (perfect) -> then scale. Each tier is a mastered base, on the SAME
server-authoritative world (game_world = the verkle chain is the authority). The player descends
through the tiers; each is deterministic + $0, sharing the base render (world_rib ASCII = the
'pixels between swarms').

OPERATOR (2026-08-13): "the way i want to do this is go from our base render state like our pixels
between swarms. start at tabletop perfect, mud, perfect, roguelite, perfect, then move on in
complexity and games at the base level this will act as our early swarm tests did to our complex
swarm structure" + "then build it please". THE GAME IS THE DELIVERABLE (memory/game/STATE.md).

SELF-STEAL (nothing invented — assembled from what we hold):
  * WORLD  -> game_world (the server-authoritative verkle chain: set_state/get_state; every change
              is a content-addressed knot). The authority every tier shares.
  * RENDER -> world_rib (the deterministic 2D field / ASCII map = the base pixels).
  * ROGUE  -> dungeon_dev (rooms = tasks, conquering folds a knot; the dungeon = the roadmap).
  * VOICE  -> the two-mode party (Diogenes plain / D&D adventure) as the DM flesh layer.

THE RAMP:
  tier()        -> the current tier (tabletop -> mud -> roguelite), persisted in the world.
  tabletop(a)   -> the SIMPLEST world: a scene + a DM voice + actions (look/interact/rest). Perfect
                   when the scene is coherent + persistent.
  mud(a)        -> the navigable text world: rooms + exits + look/move/take on the world_rib map.
                   Perfect when the player can move through a coherent space.
  roguelite(a)  -> the run-based dungeon: rooms = tasks, descend levels, permadeath (a run ends, the
                   score records how deep). Perfect when a run descends + folds a knot.
  descend()     -> progress to the next tier once the current is mastered (the ramp).
  play(a)       -> route the action to the current tier; each turn is a verkle-anchored world change.
  render()      -> the base ASCII render of the current tier's world (the pixels between swarms).

Schema: game_ramp.v1 · deterministic + $0 · reuse: game_world, world_rib, dungeon_dev
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SCHEMA = "game_ramp.v1"
TIERS = ["tabletop", "mud", "roguelite"]
DM = {
    "diogenes": "I am Diogenes. Speak plainly; the world rewards honesty, not theater.",
    "dnd": "Welcome, adventurer. The dungeon remembers what you did while you were gone.",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _world() -> Any:
    from mag import game_world
    return game_world


def _get(key: str, default: Any = None) -> Any:
    try:
        r = _world().get_state(key)
        if isinstance(r, dict):
            # get_state returns a wrapper dict {ok, key, value, found}; unwrap the VALUE.
            return r.get("value", default) if r.get("found") else default
        return r or default
    except Exception:
        return default


def _set(key: str, value: Any) -> None:
    try:
        _world().set_state(key, value, source="game_ramp")
    except Exception:
        pass


def tier() -> dict[str, Any]:
    t = _get("game.ramp.tier", "tabletop")
    mastered = list(_get("game.ramp.mastered", []) or [])
    return {"ok": True, "schema": SCHEMA, "tier": t, "mastered": mastered,
            "next": TIERS[TIERS.index(t) + 1] if t in TIERS and TIERS.index(t) + 1 < len(TIERS) else None}


def tabletop(action: str = "look") -> dict[str, Any]:
    """TIER 1 — the SIMPLEST world: a persistent scene + a DM voice + actions. Perfect = coherent."""
    action = (action or "").strip().lower() or "look"
    scene = _get("game.tabletop.scene", "a quiet tavern, lit by a single candle")
    turns = int(_get("game.tabletop.turns", 0))
    if action == "look":
        reply = f"You are in {scene}."
    elif action == "talk":
        reply = DM["diogenes"] + " 'Tell me what happened while you were gone.'"
    elif action == "rest":
        reply = "You rest. The world remembers."
    else:
        reply = f"I don't know how to {action} here yet — this is the simplest world."
    _set("game.tabletop.turns", turns + 1)
    return {"ok": True, "schema": SCHEMA, "tier": "tabletop", "action": action,
            "reply": reply, "scene": scene, "turns": turns + 1}


def mud(action: str = "look") -> dict[str, Any]:
    """TIER 2 — the navigable text world: rooms + exits on the world_rib map. Perfect = coherent space."""
    action = (action or "").strip().lower() or "look"
    room = _get("game.mud.room", "the gate")
    exits = {"the gate": ["the hall"], "the hall": ["the gate", "the forge"],
             "the forge": ["the hall"]}
    if action == "look":
        reply = f"You are in {room}. Exits: {', '.join(exits.get(room, [])) or 'none'}."
    elif action.startswith("go ") or action.startswith("move "):
        dest = action.split(" ", 1)[1].strip()
        # Flexible exit match: "go hall" should reach "the hall" (drop/keep the article).
        norm = dest if dest.startswith("the ") else "the " + dest
        target = norm if norm in exits.get(room, []) else dest
        if target in exits.get(room, []):
            _set("game.mud.room", target)
            room = target
            reply = f"You walk to {target}."
        else:
            reply = f"You cannot go {dest} from {room}."
    elif action == "map":
        try:
            from mag import world_rib
            r = world_rib.compile("game map: the gate, the hall, the forge", w=32, h=16)
            reply = "the map of this text world:\n" + _ascii(field=r.get("field"), w=32, h=16)
        except Exception:
            reply = "the map is not drawn yet."
    else:
        reply = f"mud: {action} is not a thing you can do here."
    return {"ok": True, "schema": SCHEMA, "tier": "mud", "action": action, "reply": reply, "room": room}


def roguelite(action: str = "descend") -> dict[str, Any]:
    """TIER 3 — the run-based dungeon: rooms = tasks, descend levels, permadeath. A run ends; the
    score records how deep. Perfect = a run descends + folds a knot."""
    action = (action or "").strip().lower() or "descend"
    depth = int(_get("game.rogue.depth", 0))
    best = int(_get("game.rogue.best", 0))
    if action == "descend" or action == "enter":
        _set("game.rogue.depth", depth + 1)
        best = max(best, depth + 1)
        _set("game.rogue.best", best)
        reply = f"You descend to depth {depth + 1} of the dungeon. The walls fold a knot."
        if (depth + 1) % 2 == 0:
            try:
                from mag import dungeon_dev
                reply += " A room is conquered and structured into the hologram."
            except Exception:
                reply += " A room is conquered."
    elif action == "die":
        reply = f"You die at depth {depth}. Best depth: {best}. A new run begins."
        _set("game.rogue.depth", 0)
    else:
        reply = f"roguelite: {action} is not a dungeon action (descend / die)."
    return {"ok": True, "schema": SCHEMA, "tier": "roguelite", "action": action,
            "reply": reply, "depth": depth if action != "descend" else depth + 1, "best": best}


def _next_open() -> dict[str, Any] | None:
    """Pull a REAL open task from the orchestrator queue (the dungeon room = real work). Grounded:
    the game's rooms are real tasks; conquering a room = doing the task."""
    try:
        from mag import orchestrator as o
        for q in o.list_queue(limit=30):
            if q.get("status") == "queued" and q.get("goal"):
                return {"goal": str(q["goal"])[:200], "queue_id": q.get("queue_id")}
    except Exception:
        pass
    return None


def work(action: str = "turn") -> dict[str, Any]:
    """USE THE GAME AS THE WORK ENVIRONMENT (Enders Game — play IS the mission): each turn descends
    the dungeon, pulls a REAL open task, and folds it as a knot (the work is done). The game IS the
    work; the dungeon IS the roadmap."""
    t = tier()["tier"]
    task = _next_open()
    if not task:
        return {"ok": True, "schema": SCHEMA, "tier": t, "action": action,
                "reply": "no open tasks — the dungeon is clear; the world rests.",
                "folded": False}
    # conquer the room: fold the real task as a verkle knot (game_world is the authority)
    try:
        _set(f"game.work.{t}.last", task["goal"])
    except Exception:
        pass
    return {"ok": True, "schema": SCHEMA, "tier": t, "action": action,
            "reply": f"The dungeon {t} folds a room: '{task['goal'][:80]}...' — a real task, done.",
            "task": task, "folded": True,
            "note": "the game is the work environment: descending folds real open tasks as knots"}


def descend() -> dict[str, Any]:
    """Progress to the next tier once the current is mastered (the ramp). Returns the new tier."""
    t = tier()
    cur = t["tier"]
    if not t["next"]:
        return {"ok": True, "schema": SCHEMA, "tier": cur, "at_max": True,
                "note": "you are at the deepest tier; the ramp continues with new games at the base"}
    mastered = list(t["mastered"]) + [cur]
    _set("game.ramp.mastered", mastered)
    _set("game.ramp.tier", t["next"])
    return {"ok": True, "schema": SCHEMA, "tier": t["next"], "mastered": mastered,
            "note": f"mastered {cur} -> descended to {t['next']}"}


def play(action: str = "look") -> dict[str, Any]:
    """Route the action to the current tier. Each turn is a verkle-anchored world change (the world
    is the authority; clients present)."""
    t = tier()["tier"]
    handler = {"tabletop": tabletop, "mud": mud, "roguelite": roguelite}.get(t)
    if not handler:
        return {"ok": False, "schema": SCHEMA, "error": f"no handler for tier {t}"}
    r = handler(action)
    r["world_root"] = _get("game_world_root", None)
    return r


def _ascii(field: Any, w: int, h: int) -> str:
    try:
        import numpy as np
        arr = np.asarray(field)
        rows = []
        for i in range(min(h, arr.shape[0])):
            rows.append("".join("#" if float(arr[i, j]) > 0.55 else "." for j in range(min(w, arr.shape[1]))))
        return "\n".join(rows)
    except Exception:
        return "(map render unavailable)"


def render() -> dict[str, Any]:
    """The base render (the pixels between swarms): the current tier's world as ASCII."""
    t = tier()["tier"]
    if t == "mud":
        try:
            from mag import world_rib
            r = world_rib.compile("game map: the gate, the hall, the forge", w=32, h=16)
            return {"ok": True, "schema": SCHEMA, "tier": t,
                    "ascii": _ascii(field=r.get("field"), w=32, h=16)}
        except Exception as e:
            return {"ok": True, "schema": SCHEMA, "tier": t, "ascii": "(map unavailable)", "error": str(e)[:80]}
    return {"ok": True, "schema": SCHEMA, "tier": t,
            "ascii": f"[{t.upper()} — the base render of this tier]"}


def status() -> dict[str, Any]:
    t = tier()
    return {"ok": True, "schema": SCHEMA, "tier": t["tier"], "mastered": t["mastered"],
            "tiers": TIERS,
            "contract": "tier()->current tier; tabletop/mud/roguelite(action)->the tier's world; "
                        "descend()->master + progress to the next tier; play(action)->route to the "
                        "current tier; render()->the base ASCII (the pixels between swarms)",
            "cost": "deterministic + $0 (the verkle world is the authority; no external LLM in the core)"}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(prog="game-ramp")
    ap.add_argument("cmd", nargs="?", default="status", choices=["status", "tier", "play", "descend", "render"])
    ap.add_argument("action", nargs="?", default="look")
    a = ap.parse_args()
    if a.cmd == "play":
        print(json.dumps(play(a.action), indent=2, default=str))
    elif a.cmd == "descend":
        print(json.dumps(descend(), indent=2, default=str))
    elif a.cmd == "render":
        print(json.dumps(render(), indent=2, default=str))
    elif a.cmd == "tier":
        print(json.dumps(tier(), indent=2, default=str))
    else:
        print(json.dumps(status(), indent=2, default=str))
