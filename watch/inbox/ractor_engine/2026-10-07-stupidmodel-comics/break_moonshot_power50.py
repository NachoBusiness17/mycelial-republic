"""break-moonshot-1 hostile pass: the n=50 power run (2026-10-07).

Attacks moonshot M2's falsifier ("if gemma4 regresses below gemma:2b at n=50
the ranking flips") and accuracy F1's owed admission gate, and byte-settles
M3's mechanism claim ("generic format:json -> gemma4 DROPPED the pose key on
8/8") by persisting FULL raws this time (the lens banked only 120-char heads).

Same door, same wrapper prompt, same grader as the lens's probe (imported, not
rewritten): body["format"]="json", temperature 0.3, num_predict 400, POSES
vocabulary + score_json from probe_moonshot_gemma4.py. 50 NEW session-summary
prompts (none reused from any sibling probe). 3 seats x 50 = 150 calls, $0,
local ollama only, sequential. No subprocess spawns.
"""
from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_moonshot_gemma4 import JSON_SPEC, POSES, score_json  # noqa: E402

OUT = Path(__file__).resolve().parent / "break_moonshot_power50_results.json"
URL = "http://localhost:11434/api/generate"
MODELS = ["gemma4:latest", "qwen2.5:3b-instruct", "gemma:2b"]

PROMPTS = [
    "The free fleet drained 31 corridor probes overnight and every one banked a receipt.",
    "The drone flew a perimeter loop in rain and the video feed froze twice.",
    "A 3 a.m. patrol found the census drifted by 50 tests and refreshed the carrier.",
    "Two agents debated whether to cache the vector store; the janitor just cleared it.",
    "The operator asked for a comic strip and the fleet asked how stupid exactly.",
    "A torrent of 9,305 parts took nine seconds to render as terrain.",
    "The dice trial ran 2 for 2 on free seats and nobody argued with the roll.",
    "The beat grid held 8 counts and collapsed on the 12th.",
    "A quota wall at 09:05Z denied eight retries and the balance never moved.",
    "The mountain game needed a river; the hydrology tool carved one overnight.",
    "The verkle audit found one dangling knot and the fix was a single hash.",
    "The janitor model summarized 40 pages into three bullets and one joke.",
    "A consensus triplet overlapped 0.45 and the gate called it a maybe.",
    "The emulator build finished with zero errors after six compiler cycles.",
    "The night loop closed itself and declared GROWS, not fixpoint.",
    "The drone landed on the exact pad it left in fog thick as soup.",
    "The deterministic tool answered in 40 milliseconds and both debaters went quiet.",
    "A stash sweep found three forgotten stashes and filed them for the operator.",
    "The token budget said 12 percent left; the seat shipped anyway and hid it.",
    "The model claimed it could not draw, so the renderer drew its words.",
    "A watchdog restarted the scheduler 14 times before anyone noticed.",
    "The stick figure danced the strut on beat seven of eight.",
    "The estate indexed 4,358 tests in 12 seconds and flagged none.",
    "A free seat wrote the changelog and misspelled verkle twice.",
    "The gallery render queued behind a build and delivered at dawn.",
    "The operator approved the push with one word at 07:54.",
    "A lore engine generated 12 rooms and 3 of them remembered each other.",
    "The map merged two biomes and the corridor stayed honest.",
    "A vision probe scored 0.6885 and the joint features took the credit.",
    "The queue drained 13 trials and only 2 passed without a schema.",
    "The capsule kept its seal across 11 reboots.",
    "A logger wrote mojibake at byte 57526 and the parser shrugged.",
    "The cliff notes said keep it stupid, keep it cheap.",
    "Two seats raced to fix the same bug and one left a receipt.",
    "The operator's morning list had 11 items and he signed 3.",
    "A shard rebalanced itself at noon with no operator gate.",
    "The comic renderer drew 4 panels from one ledger row.",
    "A pixel check caught the sprite flipped; one line fixed it.",
    "The pattern patrol flagged a stale carrier from 12 days back.",
    "The whisper model transcribed the standup and invented a deadline.",
    "The mesh relayed a check-in from three nodes and verified two.",
    "The gold invariant survived three reseeds and a shuffle.",
    "A typo in the config routed the comics to the wrong channel for an hour.",
    "The fleet retired three lanes and nobody mourned them.",
    "A probe measured 19.8 tokens per second on a Tuesday.",
    "The ratchet blocked the push and the fix comment named the cause.",
    "The summit render took 40 minutes and the climber never fell.",
    "A free API seat went dark for two days behind its own fence.",
    "The ledger grew 300 rows and the rib fold took none of them forward.",
    "The operator said trust bytes, not reports, and the seat re-ran the census.",
]


def call(model: str, prompt: str, timeout: int = 180) -> str:
    body = {
        "model": model,
        "prompt": f"Turn this session summary into a 3-4 panel xkcd-style comic spec. {JSON_SPEC}\n\nSession summary: {prompt}",
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": 400},
        "format": "json",
    }
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())["response"]


def pose_telemetry(raw: str) -> dict:
    """Full-raw pose analysis (the lens's 120-char heads could not show this)."""
    m = __import__("re").search(r"<think>(.*?)</think>", raw, __import__("re").S)
    txt = raw[m.end():].strip() if m else raw.strip()
    try:
        obj = json.loads(txt)
    except Exception:
        try:
            m2 = __import__("re").search(r"\{.*\}", txt, __import__("re").S)
            obj = json.loads(m2.group(0)) if m2 else None
        except Exception:
            obj = None
    if not isinstance(obj, dict):
        return {"parses": False}
    panels = obj.get("panels")
    if not isinstance(panels, list):
        return {"parses": True, "panels": 0}
    keys = sum(1 for p in panels if isinstance(p, dict) and "pose" in p)
    vals = [str(p.get("pose", "")).lower() for p in panels if isinstance(p, dict)]
    invocab = [v for v in vals if v in POSES]
    caps = [len(str(p.get("caption", "")).split()) for p in panels if isinstance(p, dict)]
    return {"parses": True, "panels": len(panels), "pose_key_present": keys,
            "pose_values": vals, "pose_invocab": len(invocab),
            "caption_words": caps}


def main() -> None:
    rows = []
    for model in MODELS:
        for i, p in enumerate(PROMPTS):
            t = time.time()
            try:
                raw = call(model, p)
                s = score_json(raw)
                pt = pose_telemetry(raw)
                err = ""
            except Exception as e:
                raw, s = "", {"parses": False, "spec_valid": False, "captions_ok": False, "poses_ok": False, "raw_head": ""}
                pt, err = {"parses": False}, f"{type(e).__name__}: {e}"
            rows.append({"model": model, "prompt_i": i, "secs": round(time.time() - t, 1), "error": err,
                         **s, "pose_tel": pt, "raw": raw[:4000]})
            print(model, i, "parses", s["parses"], "spec", s["spec_valid"], "posekey", pt.get("pose_key_present"), flush=True)
    summary = {}
    for model in MODELS:
        sub = [r for r in rows if r["model"] == model]
        valid = [r for r in sub if r["pose_tel"].get("parses")]
        panel_total = sum(r["pose_tel"].get("panels", 0) for r in valid)
        key_total = sum(r["pose_tel"].get("pose_key_present", 0) for r in valid)
        summary[model] = {
            "n": len(sub), "parses": sum(r["parses"] for r in sub), "spec_valid": sum(r["spec_valid"] for r in sub),
            "errors": sum(1 for r in sub if r["error"]),
            "mean_secs": round(sum(r["secs"] for r in sub) / len(sub), 1),
            "pose_key_present_total": key_total, "panels_total": panel_total,
            "pose_key_rate": round(key_total / panel_total, 3) if panel_total else None,
        }
    OUT.write_text(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
                               "summary": summary, "rows": rows}, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
