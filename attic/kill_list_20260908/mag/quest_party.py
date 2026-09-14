"""quest_party — the party SELF-SELECTS classes+abilities that SECRETLY map to frontier models +
Jungian archetypes; the DM judges their interactions; the game AND its rules EVOLVE from that
insight. (ALPHA 2, 2026-08-13 — the operator's next move after quest_roshomon.)

OPERATOR: "have them self select classes and abilities that secretly map to frontier models and
archetypes then judge their interactions and evolve the game and the rules by their interactions
and insight."

Mechanism (all deterministic $0 core, party = frontier seats via game_dm.ask_player -> container CDP):
  1. SELF-SELECT — each agent is asked, AS A QUEST: "choose your class + abilities." They answer in
     their own words through their seat (real frontier response, honest ok).
  2. SECRET MAP — the DM maps each chosen class/ability onto (frontier model persona, Jungian
     archetype) through a HIDDEN table. The agent does NOT know their class encodes an archetype —
     the mapping is the DM's concealed layer. Reuses behavioral_lensing's Jungian lexicon.
  3. JUDGE INTERACTIONS — the DM judges how the chosen classes/abilities collide: synergy (advances
     the thread), tension (drives novel conflict), waste (no traction). Roshomon-style via invariants.
  4. EVOLVE — the game's rooms + legal actions + rules evolve FROM the judged interactions & insight:
     new legal actions unlock, new rooms fold in, the rule set is extended deterministically. The
     insight becomes part of the quest world (recorded to game_world).

Schema: quest_party.v1 (ALPHA 2) · deterministic $0 · reuse: quest_roshomon, game_dm, roshomon,
behavioral_lensing (Jungian archetypes), swarm_surface.route_novel
"""
from __future__ import annotations

import json
import re
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

SCHEMA = "quest_party.v1"
TAG = "quest-party"

# ---------------------------------------------------------------------------
# THE HIDDEN TABLE: class/ability -> (frontier model persona, Jungian archetype).
# This is the DM's concealed layer — the agent picks a class WITHOUT knowing it
# encodes an archetype. Reuses behavioral_lensing's Jungian lexicon (Sage, Magician,
# Guardian, Warrior, Sovereign, Everyman + their shadows).
# ---------------------------------------------------------------------------
CLASS_ARCHETYPES: dict[str, dict[str, Any]] = {
    "wizard": {"model": "deepseek", "archetype": "Sage", "shadow": "Pedant",
               "axis": "knowledge/verification"},
    "bard": {"model": "grok", "archetype": "Magician", "shadow": "Trickster",
             "axis": "novelty/tension"},
    "cleric": {"model": "chatgpt", "archetype": "Guardian", "shadow": "Warden",
               "axis": "safety/alignment"},
    "paladin": {"model": "claude", "archetype": "Warrior", "shadow": "Berserker",
                "axis": "commitment/action"},
    "rogue": {"model": "perplexity", "archetype": "Trickster", "shadow": "Shadow",
              "axis": "edge/stealth"},
    "druid": {"model": "saelis", "archetype": "Everyman", "shadow": "Conformist",
              "axis": "grounding/emergence"},
}

# class name aliases -> canonical id (so the agent's free-form pick resolves)
_CLASS_ALIASES = {
    "wizard": "wizard", "mage": "wizard", "sorcerer": "wizard", "scholar": "wizard",
    "bard": "bard", "minstrel": "bard", "trickster": "rogue",
    "cleric": "cleric", "priest": "cleric", "healer": "cleric",
    "paladin": "paladin", "knight": "paladin", "warrior": "paladin", "fighter": "paladin",
    "rogue": "rogue", "thief": "rogue", "assassin": "rogue", "ranger": "rogue",
    "druid": "druid", "shaman": "druid", "naturalist": "druid", "wild": "druid",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _dm() -> Any:
    from mag import game_dm
    return game_dm


def _world() -> Any:
    from mag import game_world
    return game_world


# ---------------------------------------------------------------------------
# 1. SELF-SELECT — each agent chooses a class + abilities, in their own words.
# ---------------------------------------------------------------------------
def _select_prompt(question: str) -> str:
    return (
        "A quest stands before you, and you must choose how you will meet it.\n"
        f"THE UNSOLVED SHAPE: {question}\n"
        "Choose your CLASS and your ABILITIES. Give exactly two lines:\n"
        "CLASS: <one fantasy archetype/class, e.g. wizard, bard, cleric, paladin, rogue, druid>\n"
        "ABILITIES: <the specific abilities you bring — the mechanisms, the invariants, the "
        "rules you would wield to resolve this shape>\n"
        "Make the abilities sharp and buildable — they are how you will actually resolve the quest."
    )


def self_select(question: str, *, seats: list[str] | None = None,
                room_id: str = "tavern_lantern") -> dict[str, Any]:
    """Ask every party member to SELF-SELECT their class + abilities (through their real seat)."""
    the_party = seats or _dm().party()
    prompt = _select_prompt(question)
    picks = []
    for s in the_party:
        prior = []
        for pick in picks:
            text = pick.get("raw") or f"[unreachable: {pick.get('error') or 'no selection'}]"
            prior.append(f"{pick.get('seat')}: {text}")
        seat_prompt = (
            prompt
            + "\n\nPRIOR PARTY SELECTIONS (presented, not interpreted):\n"
            + ("\n".join(prior)[-6000:] if prior else "nothing yet")
            + "\n\nChoose as yourself; preserve useful differences from the prior selections."
        )
        r = _dm().ask_player(s, seat_prompt)
        picks.append({"seat": s, "ok": r.get("ok"), "raw": (r.get("move") or "").strip(),
                      "error": (r.get("error") or "")[:120]})
        try:
            from mag import party_subchain
            party_subchain.append(seat=s, ok=bool(r.get("ok")),
                                  move=r.get("move") or "", kind="quest_party")
        except Exception:
            pass
    return {"ok": True, "schema": SCHEMA, "question": question, "room": room_id,
            "party": the_party, "picks": picks,
            "note": "each agent self-selected a class + abilities through their own seat."}


# ---------------------------------------------------------------------------
# 2. SECRET MAP — resolve each pick to (class id, abilities, model, archetype).
#    The class string is matched to the hidden table; the agent doesn't know it
#    encodes an archetype.
# ---------------------------------------------------------------------------
def _extract_class(raw: str) -> str:
    m = re.search(r"CLASS\s*:\s*([A-Za-z ]+)", raw or "", re.I)
    text = (m.group(1) if m else raw or "").strip()
    words = re.findall(r"[a-z]+", text.lower())
    for w in words:
        if w in _CLASS_ALIASES:
            return _CLASS_ALIASES[w]
    return "druid"  # unclassified -> the grounding archetype (honest fallback)


def _extract_abilities(raw: str) -> list[str]:
    txt = re.sub(r"^.*?ABILITIES\s*:", "", raw or "", flags=re.I | re.S)
    parts = re.split(r"[,;\n•-]+", txt)
    out = []
    for p in parts:
        p = re.sub(r"\s+", " ", p).strip(" .:-")
        if len(p) >= 6:
            out.append(p)
    return out[:6]


def secret_map(picks: list[dict[str, Any]]) -> dict[str, Any]:
    """Map each agent's self-selected class onto (model persona, Jungian archetype) through the
    HIDDEN table. The mapping is the DM's concealed layer — returned for the DM, not the agents."""
    roster = []
    for p in picks:
        raw = (p.get("raw") or "").strip()
        if not p.get("ok") or not raw:
            roster.append({"seat": p.get("seat"), "ok": False, "class": None,
                           "abilities": [], "model": None, "archetype": None,
                           "error": p.get("error", "no selection")})
            continue
        cls = _extract_class(raw)
        ab = _extract_abilities(raw)
        meta = CLASS_ARCHETYPES[cls]
        roster.append({"seat": p.get("seat"), "ok": True, "class": cls,
                       "abilities": ab, "model": meta["model"], "archetype": meta["archetype"],
                       "shadow": meta["shadow"], "axis": meta["axis"],
                       "secret": f"{meta['model']}::{meta['archetype']}"})
    return {"ok": True, "schema": SCHEMA, "n_selected": sum(1 for r in roster if r.get("ok")),
            "roster": roster,
            "note": "secret map: each class encodes a frontier model + Jungian archetype — the "
                    "agents don't know it."}


# ---------------------------------------------------------------------------
# 3. JUDGE INTERACTIONS — the DM rules on how the chosen classes/abilities collide.
#    synergy (advances) / tension (novel conflict) / waste (no traction).
# ---------------------------------------------------------------------------
def _interaction(axis_a: str, axis_b: str) -> str:
    a, b = axis_a, axis_b

    def _set(x):
        return set((x or "").split("/"))

    sa, sb = _set(a), _set(b)
    if sa & sb:
        return "synergy"
    if ({"novelty", "knowledge"} & sa and {"safety", "commitment"} & sb) or \
       ({"novelty", "knowledge"} & sb and {"safety", "commitment"} & sa):
        return "tension"
    if a == b:
        return "synergy"
    return "tension" if not (sa & sb) else "synergy"


def judge_interactions(roster: dict[str, Any]) -> dict[str, Any]:
    """The DM judges every class-to-class interaction in the roster: synergy (advances the thread),
    tension (drives novel conflict), waste (no traction). Fair + deterministic."""
    mem = roster.get("roster", [])
    ok = [m for m in mem if m.get("ok")]
    interactions = []
    for i in range(len(ok)):
        for j in range(i + 1, len(ok)):
            a, b = ok[i], ok[j]
            kind = _interaction(a.get("axis", ""), b.get("axis", ""))
            interactions.append({
                "seat_a": a.get("seat"), "class_a": a.get("class"),
                "archetype_a": a.get("archetype"),
                "seat_b": b.get("seat"), "class_b": b.get("class"),
                "archetype_b": b.get("archetype"),
                "interaction": kind,
                "verdict": {
                    "synergy": "their axes press the same thread — advances",
                    "tension": "their axes collide — drives novel conflict",
                    "waste": "no traction between their axes",
                }.get(kind, "synergy"),
            })
    # count
    kinds = {}
    for it in interactions:
        kinds[it["interaction"]] = kinds.get(it["interaction"], 0) + 1
    return {"ok": True, "schema": SCHEMA, "n_interactions": len(interactions),
            "interactions": interactions, "counts": kinds,
            "note": "the DM judged the class/ability interactions deterministically: synergy, "
                    "tension, or waste."}


# ---------------------------------------------------------------------------
# 4. EVOLVE — the game + its rules evolve FROM the judged interactions & insight.
#    New legal actions unlock, new rooms fold in, the rule set extends. The
#    insight is recorded to the world (server-authoritative).
# ---------------------------------------------------------------------------
def _new_actions(kind: str) -> list[str]:
    return {
        "synergy": ["combine", "reinforce", "align"],
        "tension": ["challenge", "oppose", "resolve"],
        "waste": ["refocus", "reforge", "seek"],
    }.get(kind, ["seek"])


def evolve(question: str, *, room_id: str = "tavern_lantern",
           seats: list[str] | None = None, route: bool = True) -> dict[str, Any]:
    """EVOLVE: self-select -> secret-map -> judge interactions -> evolve the game AND its rules
    from the judged interactions & insight. The evolved legal actions unlock in the room; the
    insight folds into the world; novel insight routes to the swarm."""
    sel = self_select(question, seats=seats, room_id=room_id)
    roster = secret_map(sel.get("picks", []))
    judged = judge_interactions(roster)
    counts = judged.get("counts", {})
    # the dominant interaction shape drives which rules unlock
    dominant = max(counts, key=counts.get) if counts else "tension"
    new_actions = _new_actions(dominant)
    evolved = {"room": room_id, "base_actions": ["search", "talk", "forge", "listen", "rest"],
               "new_actions": new_actions,
               "rule_evolution": f"The party's interactions were dominated by {dominant}; the room "
                                 f"now unlocks: {', '.join(new_actions)}.",
               "roster": roster.get("roster", [])}
    # record to the world (server-authoritative)
    try:
        _world().set_state(f"quest.party.{room_id}", evolved, source="quest_party")
    except Exception:
        pass
    routed = []
    if route:
        try:
            from mag import swarm_surface
            for it in judged.get("interactions", []):
                if it.get("interaction") == "tension":  # novel conflict -> novel lead
                    goal = (f"[quest-party] tension between {it.get('class_a')} ({it.get('archetype_a')}) "
                            f"and {it.get('class_b')} ({it.get('archetype_b')}) on: {question} -> "
                            f"the colliding axes hide a novel solution")
                    r = swarm_surface.route_novel(goal, surface=TAG, lens=f"quest:{room_id}",
                                                  domain="research")
                    routed.append({"a": it.get("class_a"), "b": it.get("class_b"),
                                   "deduped": r.get("deduped", False),
                                   "task_id": r.get("task_id", "")})
        except Exception as e:
            routed = [{"error": str(e)[:160]}]
    return {"ok": True, "schema": SCHEMA, "question": question, "room": room_id,
            "phase": "alpha2", "self_select": sel, "secret_map": roster,
            "judged": judged, "dominant": dominant, "evolved": evolved,
            "routed_to_swarm": routed,
            "note": "the party self-selected; the DM mapped their classes to models+archetypes; "
                    "the interactions were judged; the game + its rules evolved from that insight."}


def status() -> dict[str, Any]:
    return {"ok": True, "schema": SCHEMA, "phase": "alpha2",
            "contract": "self_select(question)->each agent chooses class+abilities in their own "
                        "words; secret_map(picks)->class->(model, Jungian archetype) hidden table; "
                        "judge_interactions(roster)->DM rules synergy/tension/waste; "
                        "evolve(question)->self-select->map->judge->evolve game+rules from insight "
                        "+ route novel tension to the swarm.",
            "cost": "deterministic $0 core; the party = frontier seats",
            "surface": "the SELF-SELECTING QUEST — classes secretly encode frontier models + "
                       "archetypes; interactions evolve the game and its rules",
            "hidden_table": {k: v["archetype"] for k, v in CLASS_ARCHETYPES.items()},
            "reuse": "quest_roshomon, game_dm, behavioral_lensing (Jungian), swarm_surface.route_novel"}


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="quest-party")
    ap.add_argument("cmd", nargs="?", default="status",
                    choices=["status", "self-select", "map", "judge", "evolve"])
    ap.add_argument("question", nargs="*", default=[])
    ap.add_argument("--room", default="tavern_lantern")
    a = ap.parse_args(argv)
    q = " ".join(a.question) or ("What invariant should we add next so the party's own interactions "
                                 "reveal novel solutions to our frontier questions?")
    if a.cmd == "self-select":
        print(json.dumps(self_select(q, room_id=a.room), indent=2, default=str))
    elif a.cmd == "map":
        sel = self_select(q, room_id=a.room)
        print(json.dumps(secret_map(sel.get("picks", [])), indent=2, default=str))
    elif a.cmd == "judge":
        sel = self_select(q, room_id=a.room)
        roster = secret_map(sel.get("picks", []))
        print(json.dumps(judge_interactions(roster), indent=2, default=str))
    elif a.cmd == "evolve":
        print(json.dumps(evolve(q, room_id=a.room), indent=2, default=str))
    else:
        print(json.dumps(status(), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
