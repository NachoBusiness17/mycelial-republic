"""u6_union_creative -- creative drafting bundle (wave 20260916, lane U6).

Witness: stealth/union-alpha on OpenRouter (time-boxed free lane
`or-union-alpha` in mag/research_fanout.py LANES). The stealth model is the
drafting PEN; the agent is the EDITOR (fleet craft rules applied after).
Two asks:
  ITEM 1 - Frontier Souls SIGNS: 10 candidate one-line road-sign texts
           (editor curates 8). Western-dry, technically true, half the story.
  ITEM 2 - Soul Castle NPC voices: 2 options per NPC x 4 NPCs (editor picks
           1 each, 3-4 sentences). Monk-doorkeeper, lamplighter, doubting
           knight, bell that speaks in questions.
Key via mag.flight_recorder.load_env, never printed, never written to a row.
Raw rows -> watch/salon_responses/u6_union_creative/raw.jsonl (append-only).
Schema: u6_union_creative.v1. $0 budget; 402/403 -> record and stop.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]  # .../watch/inbox/wave_20260916/u6_union_creative.py
sys.path.insert(0, str(ROOT))

from mag.flight_recorder import load_env, guard_endpoint  # noqa: E402

OUT = ROOT / "watch" / "salon_responses" / "u6_union_creative"
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "raw.jsonl"

MODEL = "stealth/union-alpha"
BASE = "https://openrouter.ai/api/v1"
ALLOWED_HOSTS = {"openrouter.ai"}
TEMP = 0.9
MAX_TOKENS = 4000

SYSTEM = ("You are a working writer with a dry, plain style. You write like an old "
          "sign painter and a storyteller who trusts the listener. No em-dashes ever. "
          "No modern slang. No adverbs you do not need. Short words carrying weight. "
          "You never explain the joke or the lesson; you let the reader finish it.")

SIGNS_PROMPT = """Draft 10 candidate road-sign texts for a western roguelike called Frontier Souls.

The world: Arizona desert, grays and browns, gritty but not cartoonish, family-friendly-dry. The player woke in a canyon pit with their soul half stolen; they walk outward, ring by ring, toward Death at the rim. Their life force drains every step. Rattlesnakes kill half the people who get close. Tumbleweeds cannot be fought and do not care. Coyotes hunt in packs. Cowboy gangs wait on the flats. There is a wishing well that grants one wish. There is a stranger's grave off the road. The world advances whether you walk or stand.

The SIGNS law (from the designer): each sign is ONE line, western-dry, and every sign must be TECHNICALLY TRUE BUT HALF THE STORY. Like a promise kept so narrowly it becomes a warning. The sign never lies and never tells the whole truth.

Examples of the register (do not reuse): "Free water. Bring your own bucket."

OUTPUT CONTRACT - exactly 10 lines, numbered 1-10, no preamble, no closing, one sign per line. Each sign reads like painted boards: brief, flat, certain."""

CASTLE_PROMPT = """Draft NPC introduction speeches for a book world called Soul Castle (author: Melissa Hallman). A visitor arrives at the castle gate for the first time. Write the first thing each character says to them.

The four characters:
1. THE MONK-DOORKEEPER - keeps the door; decides who may enter; has kept it a long time.
2. THE LAMPLIGHTER - walks the walls lighting lamps; sees everyone come and go.
3. THE DOUBTING KNIGHT - armored, capable, no longer sure what the castle is for.
4. THE BELL - the great bell in the tower, and it speaks only in questions.

VOICE LAW: 3 to 4 sentences each. No em-dashes anywhere. Plain words carrying weight. No AI tells (no "delve", no "tapestry", no "whisper of", no "testament to"). Parable method: the character states small true things and lets the listener draw the large conclusion. Each voice must be distinct from the others in rhythm and concern.

OUTPUT CONTRACT - for each character give TWO options (A and B). Format exactly:
1A. <speech>
1B. <speech>
2A. <speech>
2B. <speech>
3A. <speech>
3B. <speech>
4A. <speech>
4B. <speech>
No preamble, no closing."""


def call(tag: str, prompt: str, key: str) -> dict:
    t0 = time.time()
    rec: dict = {"lane": "or-union-alpha", "model": MODEL, "tag": tag}
    try:
        guard_endpoint(BASE + "/chat/completions", ALLOWED_HOSTS)
    except ValueError as e:
        rec.update({"ok": False, "error": f"guard: {e}"})
        return rec
    body = {"model": MODEL, "temperature": TEMP, "max_tokens": MAX_TOKENS,
            "messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": prompt}]}
    req = urllib.request.Request(
        BASE.rstrip("/") + "/chat/completions", data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "User-Agent": "mag-u6-union-creative/1.0",
                 "HTTP-Referer": "https://local-sovereign-agent.invalid",
                 "X-Title": "U6 Union Creative Bundle"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
        text = d["choices"][0]["message"]["content"]
        usage = d.get("usage") or {}
        rec.update({"ok": True, "latency_ms": int((time.time() - t0) * 1000),
                    "out_tok": usage.get("completion_tokens"),
                    "in_tok": usage.get("prompt_tokens"),
                    "text": text})
    except urllib.error.HTTPError as e:
        rec.update({"ok": False, "status": e.code, "error": e.reason,
                    "latency_ms": int((time.time() - t0) * 1000)})
    except Exception as e:
        rec.update({"ok": False, "error": f"{type(e).__name__}: {e}",
                    "latency_ms": int((time.time() - t0) * 1000)})
    with open(RAW, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def main() -> int:
    env = load_env()
    key = env.get("OPENROUTER_API_KEY")
    if not key:
        print("NO KEY: OPENROUTER_API_KEY absent from .env (value never printed)")
        return 2
    print(f"key: present, {len(key)} chars, not shown")
    stops = (402, 403)
    for tag, prompt in (("SIGNS", SIGNS_PROMPT), ("CASTLE", CASTLE_PROMPT)):
        print(f"--- firing {tag} ---", flush=True)
        rec = call(tag, prompt, key)
        if not rec.get("ok"):
            print(f"{tag}: FAIL status={rec.get('status')} error={rec.get('error')}")
            if rec.get("status") in stops:
                print("paid-wall signal -> record and stop per lane law")
                return 1
        else:
            print(f"{tag}: ok {rec['latency_ms']}ms in={rec['in_tok']} out={rec['out_tok']}")
            print(rec["text"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
