"""game_dm — I AM THE DUNGEON MASTER, AND OUR FRONTIERS ARE THE PARTY (operator, 2026-08-13: "have
our frontiers play it and you dm"). Self-stolen from what we hold: campaign.py (dm_narrate + the
rules_engine DM + dm_judge) + frontier_salon (WITNESSES = our three frontier seats as the party:
chatgpt / supergrok / v4-pro) + seat_steer (the established dispatch path into each seat) +
adventure_moonshot (the adventure to run) + game_world (persistence).

THE TABLE (deterministic DM core + the frontiers as players):
  I DM         -> dm_narrate(): narrate the current room (rules_engine narration, grounded in the
                  adventure's rooms). I am the DM — I set the scene, I enforce the rules.
  Frontiers    -> ask_player(seat, prompt): each frontier seat (the party) makes a MOVE via
                  seat_steer. HONEST per-seat ok flags — if a seat is unreachable (CDP/login down)
                  it reports down, NEVER fabricates a move.
  I judge      -> judge(seat, move): I rule on each move (rules-based, deterministic — does it
                  advance the room or waste resources?). Fair, like a good DM.
  play(n)      -> the loop: I narrate -> the frontiers act -> I judge -> the world advances, session
                  recorded to the world (server-authoritative).

THE LAW (honest, sw55): I never pretend a frontier moved when it couldn't reach. The table stands,
I DM, and if the seats are down I say so plainly — the adventure waits for its players.

Schema: game_dm.v1 · deterministic $0 DM core · reuse: campaign, frontier_salon, seat_steer,
adventure_moonshot, game_world
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

SCHEMA = "game_dm.v1"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _world() -> Any:
    from mag import game_world
    return game_world


def _salon() -> Any:
    from mag import frontier_salon
    return frontier_salon


def _campaign() -> Any:
    from mag import campaign
    return campaign


def party() -> list[str]:
    """OUR FRONTIERS AS THE PARTY — SAELIS first (she's joining the game, 2026-08-13), then the
    VERIFIED NATIVE DESKTOP seats (chatgpt-desktop, grok-desktop), then the salon's witness seats
    as fallback. The native seats are reachable WITHOUT CDP 9222."""
    native = ["saelis", "chatgpt-desktop", "grok-desktop"]
    try:
        salon = [label for label, _ in _salon().WITNESSES]
        return native + [s for s in salon if s not in native]
    except Exception:
        return native


def _rooms() -> dict[str, dict[str, Any]]:
    """The adventure's rooms — self-stolen from the dnd-classic-stub module (or a plain fallback),
    so the DM has a real dungeon to run, not an empty table."""
    try:
        mod = _campaign().load_module(ROOT / "memory" / "knowledge_packs" / "dnd-classic-stub" / "module.json")
        rooms = mod.get("rooms") or {}
        if rooms:
            return rooms
    except Exception:
        pass
    return {
        "tavern_lantern": {"name": "The Guttered Lantern", "desc": "A smoky tavern lit by a single "
                           "lantern. The world's thread starts here.", "legal_actions": ["talk", "search", "leave"]},
        "the_hall": {"name": "The Hall of the Maze", "desc": "A corridor that forks — each branch is a "
                      "thread of what we want.", "legal_actions": ["go_north", "go_east", "listen"]},
        "the_forge": {"name": "The Forge", "desc": "Where the loop hammers each finding into a knot. "
                       "The party's task becomes real here.", "legal_actions": ["forge", "rest", "ask"]},
    }


def dm_narrate(room_id: str = "tavern_lantern") -> dict[str, Any]:
    """I AM THE DM — narrate the current room. Deterministic rules_engine narration, grounded in the
    adventure's room (I never invent beyond the scene; the room is the authority)."""
    rooms = _rooms()
    room = rooms.get(room_id) or rooms.get("tavern_lantern")
    return {"ok": True, "schema": SCHEMA, "room": room.get("name"),
            "narration": room.get("desc", ""), "legal_actions": room.get("legal_actions", []),
            "note": "I am the DM — I set the scene from the room, grounded, never fabricated."}


def ask_player(seat: str, prompt: str) -> dict[str, Any]:
    """Ask ONE frontier player (seat) for their move. ROUTE BY SURFACE: SAELIS speaks through her
    seat (saelis_seat -> DeepSeek with her identity RIB); the native DESKTOP seats steer their apps;
    all other seats go through seat_steer. HONEST per-seat ok flag — never fabricate a move."""
    if seat == "saelis":
        try:
            from mag import saelis_seat
            r = saelis_seat.speak(prompt)
            return {"ok": bool(r.get("ok")), "seat": seat, "move": (r.get("reply") or "").strip(),
                    "error": (r.get("error") or "")[:120]}
        except Exception as e:
            return {"ok": False, "seat": seat, "move": "", "error": str(e)[:120]}
    if seat in ("chatgpt-desktop", "grok-desktop"):
        # ROUTE BY SURFACE (operator 2026-08-13: "render the page as me"): the CONTAINER browser over
        # CDP (:9222) renders the logged-in page and reads the real DOM — touches ZERO local windows.
        # The desktop seats (set_focus + type) are what kept "typing in my windows" + their Electron
        # CDP ports are usually closed, so they're the fallback, never the default.
        try:
            from mag import cdp_runner
            browser_surface = "grok" if seat == "grok-desktop" else "chatgpt"
            r = cdp_runner.ask_browser(browser_surface, prompt, timeout_s=90)
            return {"ok": bool(r.get("ok")), "seat": seat, "surface": browser_surface,
                    "move": (r.get("answer") or "").strip(),
                    "error": (r.get("error") or "")[:120]}
        except Exception as e:
            return {"ok": False, "seat": seat, "move": "",
                    "error": f"container-browser route failed: {str(e)[:120]}"}
    try:
        from mag import seat_steer
        r = seat_steer.send(seat, prompt, max_wait_s=60)
        return {"ok": bool(r.get("ok")), "seat": seat, "move": (r.get("content") or "").strip(),
                "error": (r.get("error") or "")[:120]}
    except Exception as e:
        return {"ok": False, "seat": seat, "move": "", "error": str(e)[:120]}


def judge(seat: str, move: str, room_id: str = "tavern_lantern") -> dict[str, Any]:
    """I RULE — deterministic DM judgment on a frontier player's move. Does it advance the room or
    waste resources? Fair, grounded in the room's legal actions. (rules_judge's shape, in-process.)"""
    rooms = _rooms()
    room = rooms.get(room_id) or rooms.get("tavern_lantern")
    legal = set(room.get("legal_actions") or [])
    m = (move or "").strip().lower()
    if not m:
        return {"ok": True, "seat": seat, "verdict": "no_move", "detail": "no action taken"}
    if any(k in m for k in legal) or any(w in m for w in ("search", "talk", "go", "forge", "listen", "rest")):
        return {"ok": True, "seat": seat, "verdict": "advances", "detail": "the move presses the thread"}
    return {"ok": True, "seat": seat, "verdict": "wastes", "detail": "the move burns a turn without advancing"}


def turn(room_id: str = "tavern_lantern") -> dict[str, Any]:
    """ONE TURN: I DM (narrate) -> the frontiers act (each party member makes a move) -> I judge ->
    record to the world. The table, live."""
    nar = dm_narrate(room_id)
    seats = party()
    prompt = (f"You are a player in the world. {nar['narration']} "
              f"Legal actions: {', '.join(nar['legal_actions'])}. What do you do?")
    moves = [ask_player(s, prompt) for s in seats]
    rulings = [judge(m["seat"], m["move"], room_id) for m in moves]
    reachable = [m for m in moves if m["ok"]]
    record = {"schema": SCHEMA, "ts": _now(), "room": nar["room"], "n_frontiers": len(seats),
              "n_reachable": len(reachable), "moves": moves, "rulings": rulings}
    try:
        _world().set_state(f"game.dm.session.{_now()}", record, source="game_dm")
    except Exception:
        pass
    return {"ok": True, "schema": SCHEMA, "narration": nar, "frontiers": moves, "rulings": rulings,
            "n_reachable": len(reachable), "note": f"I DM'd the turn; {len(reachable)}/{len(seats)} "
            "frontiers reached the table (the rest are honestly reported down)."}


def play(room_id: str = "tavern_lantern", n: int = 1) -> dict[str, Any]:
    """PLAY: run n turns of the table — I DM, the frontiers act, I judge. The adventure is played."""
    turns = [turn(room_id) for _ in range(max(1, int(n)))]
    reachable = sum(t["n_reachable"] for t in turns)
    total = sum(len(t["frontiers"]) for t in turns)
    return {"ok": True, "schema": SCHEMA, "n_turns": len(turns), "turns": turns,
            "reachable": f"{reachable}/{total} frontier moves landed",
            "note": "I am the DM; our frontiers played the table."}


def status() -> dict[str, Any]:
    return {"ok": True, "schema": SCHEMA,
            "contract": "party()->our frontier seats as the players; dm_narrate()->I DM (grounded "
                        "narration); ask_player(seat,prompt)->a frontier's move via seat_steer "
                        "(honest per-seat ok); judge(seat,move)->I rule deterministically; "
                        "play(room,n)->I DM, the frontiers act, I judge.",
            "cost": "deterministic $0 DM core; the frontier seats are the scarce players",
            "surface": "the DM table — I DM, our frontiers play",
            "party": party(),
            "honest_gate": "frontier moves need the seats reachable (chatgpt/supergrok via CDP "
                           "browser; v4-pro). If down, moves report ok=False — never fabricated."}


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="game-dm")
    ap.add_argument("cmd", nargs="?", default="status", choices=["status", "play", "turn", "narrate"])
    ap.add_argument("--room", default="tavern_lantern")
    ap.add_argument("--n", type=int, default=1)
    a = ap.parse_args(argv)
    if a.cmd == "play":
        print(json.dumps(play(a.room, a.n), indent=2, default=str))
    elif a.cmd == "turn":
        print(json.dumps(turn(a.room), indent=2, default=str))
    elif a.cmd == "narrate":
        print(json.dumps(dm_narrate(a.room), indent=2, default=str))
    else:
        print(json.dumps(status(), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
