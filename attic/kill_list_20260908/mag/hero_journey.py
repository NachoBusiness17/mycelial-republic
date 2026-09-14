"""hero_journey — overnight epic: one tale, beginning woven into the end.
C.S. Lewis meets Cervantes, woven from the night's play. Not a labeled hero's journey.

Reads: memory/game/campaign_runs/*.jsonl (the swarm-played corpus) + the saga (game_saga) + the
egregore roster (invariant_npcs) — so the epic is GROUNDED in what actually happened, not a blank
model. Emergent beats (the fireball, the fish, the recurring elephant) become the story's turns.

Method: the monomyth is 12 stages; each is one ~450-word chapter written through the creative DM
(deepseek, thinking on, temp high). Concatenated = 5k+ words. Then a prose-pass (grok if reachable,
else deepseek polish) tightens the voice. Written to memory/game/hero_journey.md.

Reuse: game_dm_llm._raw_call, game_saga, invariant_npcs, campaign_runs.
Schema: hero_journey.v1
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

SCHEMA = "hero_journey.v1"
OUT = ROOT / "memory" / "game" / "hero_journey.md"
RUNS_DIR = ROOT / "memory" / "game" / "campaign_runs"

MOVEMENT_ROOMS = {
    "lantern": {"tavern_lantern", "tavern_loft"},
    "road": {"road_to_keep", "farm_edge", "woods_trail"},
    "keep": {"keep_gate", "courtyard", "cellar_hatch", "cave_fork",
             "claw_hall", "great_hall", "barracks", "lord_solar"},
    "return": {"tavern_lantern", "tavern_loft"},
}
OPENING_OBJECTS = "Mira the dwarf, apron of faces, promise to come back breathing, fire elemental in that hearth (named Calcifer by the operator, not every flame), elephant twice, lock under the stairs, crate with keep seal and missing tool."

# The style the operator asked for: C.S. Lewis (meaning/allegory) meets Cervantes (picaresque
# comedy-adventure). Emergent + specific, never boring.
STYLE = (
    "Write like C.S. Lewis meets Cervantes: allegory you feel, and specific absurd things "
    "happening to a specific person. Close third, present tense, vivid, funny. "
    "NEVER call this a hero's journey. NEVER name Campbell stages. No chapter labels. "
    "People have Dwarf Fortress races in the body: Mira is a dwarf, goblins are goblins, "
    "the merchant is human, Calcifer is a fire elemental (one being, in Mira's hearth only). "
    "Other torches and campfires are ordinary fire. Do not name them Calcifer. "
    "Calcifer is a personal name for that one elemental, not a word for flame. "
    "ONE tavern (the Guttered Lantern). ONE crate (keep seal, missing tool). "
    "Do not pick the lock in every movement. Escalate the elephant, Mira's promise to come "
    "back breathing, the apron of faces. Weave the opening objects into the ending, changed. "
    "Richer per sentence. Show, don't tell. Dialogue. End each movement on a hook, not a label."
)

# Four movements of ONE tale. No Campbell labels. Return weaves the opening.
MOVEMENTS: list[dict[str, str]] = [
    {"key": "lantern", "brief": "Open in the Guttered Lantern. Mira the dwarf, her apron, the promise to come back breathing. A fire elemental in that hearth (some call him Calcifer; he is not every flame). Pick the lock ONCE. The crate is not opened here, or only a finger's width. Leave the tavern. Do not stay under the stairs."},
    {"key": "road", "brief": "Dusty road to the keep. Overturned cart, blood, no bodies. Keep smoke too black. Do not pick the lock. Do not reopen a tavern crate. The hatch at the empty gate is ahead."},
    {"key": "keep", "brief": "Empty gate, dice, hatch down, cave fork, claw-marked hall. Human merchant bound, goblins, crate with the keep's seal, shut because the tool was missing. Rope and wax. Do not return to Mira's stairs."},
    {"key": "return", "brief": "Return to the Guttered Lantern. Same dwarf, same promise, same hearth-elemental, same elephant's two visits. The opening objects are changed by what was carried back. The crate's secret is the keep-seal crate, not a new fish. Weave beginning into end. No hero's-journey announcement."},
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _load_context() -> str:
    """A LIGHT context slice — small enough that deepseek reliably writes prose (the empty-reply fix).
    Sample a few beats + a slice of the saga + a couple NPCs; never dump the whole corpus into a prompt."""
    bits: list[str] = []
    runs = sorted(RUNS_DIR.glob("*.jsonl")) if RUNS_DIR.is_dir() else []
    beats: list[str] = []
    for p in runs:
        try:
            for line in p.open(encoding="utf-8"):
                row = json.loads(line)
                nar = str(row.get("narration") or row.get("narrate") or row.get("speak") or "")[:160]
                if nar and len(nar) > 20:
                    beats.append(nar)
        except Exception:
            continue
    if beats:
        import random
        random.seed(_now())
        sample = random.sample(beats, min(4, len(beats)))
        bits.append("BEATS (what happened):\n" + "\n".join("- " + b for b in sample))
    try:
        from mag import game_saga, invariant_npcs
        bits.append("SAGA: " + (game_saga.recall("demo").get("text") or "")[:300])
        roster = invariant_npcs.roster().get("npcs") or {}
        npc_lines = [f"- {n}: {p.get('archetype')} — {p.get('physical','')[:70]}"
                     for n, p in list(roster.items())[:4]]
        bits.append("EGREGORES (to meet):\n" + "\n".join(npc_lines))
    except Exception:
        pass
    return "\n\n".join(bits)


def _world_bible(context: str) -> str:
    """ONE call: establish the named world (places, NPC-egregores, running gags) so every chapter
    coheres to a shared world instead of each drifting. The coherence seed for the whole epic."""
    from mag import game_dm_llm
    system = ("You are the world-builder. From the beats below, write a compact WORLD BIBLE "
              "(~120 words): the named places, the named NPC-egregores, and the running gags that "
              "must recur and escalate across the whole story. List them tersely, no prose.")
    try:
        res = game_dm_llm._raw_call(system, context)
        text = str(res.get("text") or "").strip()
        if res.get("ok") and len(text) >= 40:
            return text
    except Exception:
        pass
    return ""


def _write_movement(stage: dict[str, str], context: str, bible: str = "") -> str:
    from mag import game_dm_llm
    system = STYLE + ("\n\nYou are writing the next movement of one continuous tale. No title. No stage name.")
    world = ("WORLD BIBLE (recurring named things — keep them coherent and escalating):\n" + bible) if bible else ""
    rooms = MOVEMENT_ROOMS.get(stage.get("key") or "", set())
    scope = ("WRITE ONLY this geography: " + ", ".join(sorted(rooms)) +
             ". Do not move other rooms' people into this place. ")
    if stage.get("key") == "return":
        scope += "Reuse these opening objects, changed: " + OPENING_OBJECTS + " "
    user = (f"THE BEAT: {stage['brief']}\n\n" + scope + context + (("\n\n" + world) if world else "") +
            "\n\nWrite this movement, ~400 words. Ground it in the beats. Do not reprint earlier scenes. "
            "Escalate named things. End on a hook. No headers.")
    # iterate-don't-repeat: retry once on empty/short before stubbing (never silently stub the voice).
    for _ in range(2):
        try:
            res = game_dm_llm._raw_call(system, user)
            text = str(res.get("text") or "").strip()
            if res.get("ok") and len(text) >= 80:
                return text
        except Exception:
            pass
    return f"_(the movement {stage['key']} could not be written; the forgetting held it.)_"


def _polish_chapter(title: str, chapter: str) -> str:
    """Polish ONE chapter (fits the output budget) — lift the voice without collapsing the epic.
    Falls back to the original if polish fails (never shorten the work)."""
    from mag import game_dm_llm
    system = ("You are a master editor. Tighten this chapter to C.S. Lewis meets Cervantes: keep "
              "every emergent beat and every named thing; lift the voice; preserve length and "
              "structure. Output the polished chapter only.")
    try:
        res = game_dm_llm._raw_call(system, f"POLISH THIS CHAPTER ({title}):\n\n{chapter}")
        text = str(res.get("text") or "").strip()
        if res.get("ok") and len(text) >= 80:
            return text
    except Exception:
        pass
    return chapter


def compose(*, polish: bool = False) -> dict[str, Any]:
    """Write one continuous tale. Four movements. Beginning woven into the end."""
    context = _load_context()
    bible = _world_bible(context)
    chapters: list[str] = []
    word_total = 0
    for stage in MOVEMENTS:
        chapter = _write_movement(stage, context, bible)
        if polish:
            chapter = _polish_chapter(stage["key"], chapter)
        if "could not be written" in chapter and "forgetting held" in chapter:
            continue
        chapters.append(chapter.strip() + "\n")
        word_total += len(chapter.split())
    body = "\n".join(chapters)
    header = (f"# The Land of Forgetfulness\n"
              f"_woven from the night's play · {_now()}_\n\n")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(header + body, encoding="utf-8")
    return {"ok": True, "schema": SCHEMA, "file": str(OUT), "movements": len(MOVEMENTS),
            "words": len(body.split()), "polished": polish, "written": _now()}


def status() -> dict[str, Any]:
    runs = sorted(RUNS_DIR.glob("*.jsonl")) if RUNS_DIR.is_dir() else []
    return {"ok": True, "schema": SCHEMA, "corpus_runs": len(runs),
            "out": str(OUT), "exists": OUT.is_file(),
            "words": len(OUT.read_text(encoding="utf-8").split()) if OUT.is_file() else 0}


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(prog="hero-journey")
    ap.add_argument("cmd", choices=["compose", "status"], default="status", nargs="?")
    ap.add_argument("--no-polish", action="store_true")
    a = ap.parse_args()
    out = compose(polish=not a.no_polish) if a.cmd == "compose" else status()
    print(json.dumps(out, indent=2, default=str))
