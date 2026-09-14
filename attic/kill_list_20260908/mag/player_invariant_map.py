"""player_invariant_map — map a player's revealed game behavior onto OUR invariant lattice.

THE BRIDGE (operator, 2026-08-16): "we watch how people let their guard down in games and map
our own invariance to theirs." In a game people drop their guard and reveal stable problem-solving
traits they can't hide. We watch that (game moves), extract the stable character, and map it onto
our OCEAN invariant lattice (ocean_persona) so a person's revealed character becomes a navigable,
content-addressed coordinate — the same way cache_field maps a model's stochastic region.

Reuses (self-steal, no new core):
  * arena_learning.PROFILES_PATH   -> the game move surface (low-guard problem-solving)
  * ocean_persona.OCEAN_INVARIANTS -> OUR trait->archetype->invariant lattice
  * cache_field._coord pattern     -> content-addressed coordinate in invariant space
  * (behavioral_lensing available for the full Jungian profile if wired)

Ethics (capture_guard / epistemic_guard doctrine): consensual in-game self-revelation, deniable
(only the player's own map), used for individuation — never covert surveillance.

Schema: player_invariant_map.v1 · deterministic $0
CLI: python -m mag.player_invariant_map map <player> | mirror <player> | status
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

SCHEMA = "player_invariant_map.v1"

_REPEAT = re.compile(r"(?:again|same|repeat|retry|retreat|stand|wait|stay)\b", re.I)
_RISK = re.compile(r"(?:charge|rush|attack|gamble|bet|bluff|all.?in|dive|leap|storm|fight)\b", re.I)
_COOP = re.compile(r"(?:help|join|share|guard|protect|trust|ally|aid|heal|follow)\b", re.I)
_EXPLORE = re.compile(r"(?:look|explore|open|enter|search|investigate|go|north|south|east|west|check)\b", re.I)


def _coord(key: str) -> tuple[float, float, float]:
    """Deterministic content-addressed coordinate (same shape as cache_field)."""
    h = hashlib.sha256(key.encode("utf-8")).hexdigest()

    def u(i: int) -> float:
        return (int(h[i:i + 4], 16) % 1000) / 100.0 - 5.0

    return (u(0), u(4), u(8))


def _read_moves(player: str = "") -> list[dict[str, Any]]:
    """Read game moves from arena_learning's move log. Filter by player/seat if given."""
    try:
        from mag.arena_learning import PROFILES_PATH
        path = PROFILES_PATH
    except Exception:
        path = ROOT / "memory" / "training" / "arena_profiles.jsonl"
    out = []
    if path.is_file():
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("kind") != "move":
                continue
            if player and player.lower() not in str(r.get("seat", "")).lower():
                continue
            out.append(r)
    return out


def _metrics(moves: list[dict[str, Any]]) -> dict[str, Any]:
    """Deterministic behavioral metrics from game moves (the low-guard signals)."""
    n = len(moves)
    if not n:
        return {"n": 0}
    illegal = sum(1 for m in moves if m.get("illegal"))
    timings = [m.get("timing_ms") for m in moves if isinstance(m.get("timing_ms"), (int, float))]
    text = " ".join(str(m.get("move", "")) for m in moves).lower()
    return {
        "n": n,
        "illegal_rate": round(illegal / n, 3),
        "avg_timing_ms": round(sum(timings) / len(timings), 1) if timings else None,
        "repeat_idx": round(len(_REPEAT.findall(text)) / max(1, n), 3),
        "risk_idx": round(len(_RISK.findall(text)) / max(1, n), 3),
        "coop_idx": round(len(_COOP.findall(text)) / max(1, n), 3),
        "explore_idx": round(len(_EXPLORE.findall(text)) / max(1, n), 3),
    }


def _ocean_vector(met: dict[str, Any]) -> dict[str, float]:
    """Derive an OCEAN vector from move metrics (deterministic, 0..1)."""
    if not met.get("n"):
        return {"openness": 0.5, "conscientiousness": 0.5, "extraversion": 0.5,
                "agreeableness": 0.5, "neuroticism": 0.5}
    n = met["n"]
    return {
        "openness": min(1.0, met.get("explore_idx", 0) * 3 + 0.2),
        "conscientiousness": max(0.0, 1.0 - met.get("illegal_rate", 0) - met.get("repeat_idx", 0) * 0.5),
        "extraversion": min(1.0, n / 20.0),
        "agreeableness": min(1.0, met.get("coop_idx", 0) * 3 + 0.2),
        "neuroticism": min(1.0, met.get("repeat_idx", 0) + met.get("risk_idx", 0) * 0.3),
    }


def _archetype_lattice() -> dict[str, dict[str, Any]]:
    try:
        from mag import ocean_persona as op
        return dict(op.OCEAN_INVARIANTS)
    except Exception:
        return {}


def map_(player: str = "player", moves: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Map the player's revealed game behavior onto our OCEAN invariant lattice."""
    moves = moves if moves is not None else _read_moves(player)
    met = _metrics(moves)
    if not met["n"]:
        return {"ok": True, "schema": SCHEMA, "player": player, "moves": 0,
                "note": "no game moves found for this player yet — play to reveal character"}
    ocean = _ocean_vector(met)
    lattice = _archetype_lattice()
    dominant = max(ocean, key=lambda k: ocean[k])
    arch = (lattice.get(dominant) or {}).get("archetype", dominant)
    inv_hash = hashlib.sha256(f"player:{player}:{dominant}".encode()).hexdigest()[:16]
    return {
        "ok": True, "schema": SCHEMA, "player": player,
        "moves": met["n"],
        "metrics": met,
        "ocean": {k: round(v, 3) for k, v in ocean.items()},
        "dominant_trait": dominant,
        "archetype": arch,
        "invariant_hash": inv_hash,
        "coord": _coord(inv_hash),
        "note": ("the player's revealed game character, mapped onto our OCEAN invariant lattice — "
                 "the game let their guard down and their stable problem-solving shape surfaced."),
    }


def mirror(player: str = "player", moves: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """MAP OUR INVARIANTS TO THEIRS: compare the player's revealed invariant to our own core
    invariants — what does this character mirror back to us?"""
    m = map_(player, moves)
    if not m.get("ok") or not m.get("moves"):
        return m
    lattice = _archetype_lattice()
    our_arch = (lattice.get(m["dominant_trait"]) or {}).get("archetype", m["dominant_trait"])
    return {**m, "mirror": {
        "our_invariant": m["dominant_trait"],
        "our_archetype": our_arch,
        "player_revealed": m["archetype"],
        "mirror_note": (f"the player's revealed character ({m['archetype']}) maps onto OUR invariant "
                        f"'{m['dominant_trait']}' (archetype {our_arch}) — a coordinate in our lattice."),
    }}


def status() -> dict[str, Any]:
    return {"ok": True, "schema": SCHEMA,
            "contract": ("map(player)->revealed character onto our OCEAN invariant lattice (moves->"
                         "metrics->ocean->archetype->invariant_hash->coord); mirror(player)->compare to "
                         "our core invariants. Reuses arena_learning moves + ocean_persona + cache_field "
                         "coord pattern. $0. Ethics: consensual in-game self-revelation, deniable, "
                         "individuation not surveillance."),
            "moves_source": "memory/training/arena_profiles.jsonl (arena_learning)"}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="player_invariant_map")
    p.add_argument("cmd", choices=["map", "mirror", "status"])
    p.add_argument("player", nargs="?", default="player")
    a = p.parse_args(argv)
    if a.cmd == "map":
        print(json.dumps(map_(a.player), indent=2, ensure_ascii=False, default=str))
    elif a.cmd == "mirror":
        print(json.dumps(mirror(a.player), indent=2, ensure_ascii=False, default=str))
    elif a.cmd == "status":
        print(json.dumps(status(), indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
