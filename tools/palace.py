"""palace - the operator's ideation method as an estate organ.

The operator's own words (2026-10-13): "i read all of these minds... when i
think i remember what it is i know about a person and use empathy basically
their ocean model filtered through what i know about them and their demeanor
and life to make up a plausible story that helps me understand what they might
have done. i do this around shit all the time, sort of like a memory palace.
i want you to do this as well somehow."

This is that, as machinery. A person-model is an OCEAN vector + demeanor notes +
life context + sources, stored MACHINE-LOCAL under state/palace/ (gitignored,
same discipline as state/riddler/). The plausible-story generation is a lane:
the tool formats a story-ask from a model; a sensing-grade or better judge runs
it; stories rank by consistency with the known bytes. Every model carries
confidence and a falsifier field: what byte would update it.

Ethics (riddler protocol alignment): models of private parties exist for
interaction-safety and honest forecasting only; outputs are estate-internal
unless passed through the veil. No model is committed to any public tree.

Usage:
  python tools/palace.py init
  python tools/palace.py show <id>
  python tools/palace.py list
  python tools/palace.py story <id> --question "what did they do and why"
      [--grade sensing|certified]  (prints the story-lane prompt; certified
      still requires a banked consensus receipt, same truth law as the veil)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PALACE = ROOT / "state" / "palace"

OCEAN = ("openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism")


def _registry() -> dict:
    path = PALACE / "models.json"
    if not path.is_file():
        raise SystemExit("setup error: no palace at state/palace/models.json; run init (exit 3)")
    return json.loads(path.read_text(encoding="utf-8"))


def _save(reg: dict) -> None:
    PALACE.mkdir(parents=True, exist_ok=True)
    (PALACE / "models.json").write_text(json.dumps(reg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def _fmt_model(m: dict) -> str:
    o = m.get("ocean", {})
    lines = [f"PERSON-MODEL: {m.get('id')} (confidence: {m.get('confidence', 'low')})"]
    lines.append("  OCEAN (0-100, estimate): " + ", ".join(
        f"{k}={o.get(k, '?')}" for k in OCEAN))
    if m.get("demeanor"):
        lines.append("  demeanor: " + m["demeanor"])
    if m.get("life"):
        lines.append("  life context: " + m["life"])
    for fact in m.get("known_facts", []):
        lines.append("  fact: " + fact)
    if m.get("falsifier"):
        lines.append("  falsifier (byte that updates this model): " + m["falsifier"])
    return "\n".join(lines)


def _story_ask(m: dict, question: str) -> str:
    return ("You are running the palace method: given a structured empathy model of a "
            "person (OCEAN estimate, demeanor, life context, known facts) and a question, "
            "generate plausible stories of what they did or will do. Rules: every story "
            "must be consistent with ALL known facts; rank stories by consistency with the "
            "OCEAN estimate; state what evidence would distinguish the top two stories; "
            "mark anything speculative as SPECULATIVE. The model is an estimate, not a "
            "verdict. No em-dashes.\n\n"
            "QUESTION: " + question + "\n\n" + _fmt_model(m))


def _load_palace(mid: str) -> dict | None:
    p = PALACE / "palaces" / f"{mid}.json"
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _fmt_palace(p: dict) -> str:
    lines = [f"MEMORY PALACE: {p.get('id')} (built {p.get('built', '?')})"]
    for room in p.get("rooms", []):
        lines.append(f"  ROOM: {room.get('name')} - locus: {room.get('locus', '?')}")
        for obj in room.get("objects", []):
            heat = obj.get("heat", "?")
            ptr = obj.get("pointer") or "no pointer"
            lines.append(f"    object: {obj.get('mem')} [heat {heat}; {ptr}]")
    walk = p.get("walk", [])
    if walk:
        lines.append("  WALK (route a story-ask traverses): " + " -> ".join(walk))
    if p.get("falsifier"):
        lines.append("  palace falsifier: " + p["falsifier"])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    a = list(sys.argv[1:] if argv is None else argv)
    if not a:
        print(__doc__)
        return 0
    cmd = a[0]
    if cmd == "init":
        PALACE.mkdir(parents=True, exist_ok=True)
        p = PALACE / "models.json"
        if not p.is_file():
            p.write_text(json.dumps({"version": 1, "note": "machine-local person-models; never committed", "models": []}, indent=1) + "\n", encoding="utf-8")
        print(f"palace initialized at {PALACE}")
        return 0
    reg = _registry()
    models = reg.setdefault("models", [])
    if cmd == "list":
        for m in models:
            print(f"{m.get('id')}  (confidence {m.get('confidence','?')}, {len(m.get('known_facts',[]))} facts)")
        return 0
    if cmd in ("show", "story", "palace") and len(a) > 1:
        mid = a[1]
        m = next((x for x in models if x.get("id") == mid), None)
        if m is None:
            print(f"no model '{mid}' in the palace"); return 3
        if cmd == "show":
            print(_fmt_model(m))
            p = _load_palace(mid)
            if p:
                print()
                print(_fmt_palace(p))
            return 0
        if cmd == "palace" and len(a) > 1:
            p = _load_palace(a[1])
            if p is None:
                print(f"no palace built for '{a[1]}' (state/palace/palaces/{a[1]}.json)")
                return 3
            print(_fmt_palace(p)); return 0
        question = " ".join(a[2:]) if len(a) > 2 else " ".join(
            a[i + 1] for i, x in enumerate(a) if x == "--question") or "What did they do, and why?"
        ask = _story_ask(m, question)
        p = _load_palace(mid)
        if p:
            ask += "\n\n" + _fmt_palace(p) + ("\nWalk these rooms in order; every story must "
                                               "not contradict an object's pointer.")
        print(ask)
        return 0
    print(f"unknown command: {cmd}"); return 3


if __name__ == "__main__":
    sys.exit(main())
