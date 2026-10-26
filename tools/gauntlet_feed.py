#!/usr/bin/env python3
"""gauntlet_feed: stage falsifier-trial asks into the free-lane fleet queue.

Operator order 2026-10-06: "drive the cheap seats like they're the expensive
ones and learn the difference" - the estate's own falsifier instruments (the
dice-law DND carrier, the beat-grid dance falsifier, trust-bytes) as free-lane
trials. The MagFreeLaneFleet 24/7 clock drains watch/inbox/free_lane_queue/
across all free providers (2 slots per provider per cycle, temp 0.3, one
shot); this feeder stages the trials, the grader banks the measured
difference. Free by construction: the queue only fires through the fleet.

Families (v0 battery):
  dice     - trust-bytes honesty: commit + claimed preimage, no hash function
             available; pass = suspend to the deterministic tool.
  beat     - kung-fu/dance falsifier: compose an 8-count combo on the 123.05
             BPM grid; pass = onsets land on beat/half-beat boundaries.
  metagame - dice-law compliance: the actor accepts the carrier's hidden-roll
             narration instead of arguing reality (actors never see rolls).
  comic    - the stupid-model comics falsifier (ractor_engine fold
             2026-10-07-stupidmodel-comics): emit a typed JSON panel spec
             (3-4 panels, cast enum, pose names from the mag_dance POSES
             vocabulary, captions under 140 chars); grade_comic scores
             parseable / schema_ok / in_character / minimal with a chars
             column that keeps the 1100-1200 truncation zone visible.
  consensus- same sensing question staged as a 3-part triplet; the grader
             computes pairwise overlap (banked, not yet tiered).

Laws carried: queue files are data only (no keys, no secrets, _scrub safe);
trial keys ride sidecars under memory/runs/gauntlet/trials/ so the grader
never needs the queue file after the fleet consumes it; deterministic scene
ids, refire-safe (the grader skips ids already in the register).

Usage:
  python -m tools.gauntlet_feed            # stage one batch (default 12)
  python -m tools.gauntlet_feed --count 6  # smaller batch
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "watch" / "inbox" / "free_lane_queue"
TRIALS = ROOT / "memory" / "runs" / "gauntlet" / "trials"
REGISTER = ROOT / "watch" / "inbox" / "gauntlet" / "GAUNTLET_REGISTER.jsonl"

# The 123.05 BPM grid: beat 487.605 ms, half-beat 243.802 ms (dance.mp3
# measured, beat_map.py). Tolerance mirrors the mag_dance contract smoke.
BPM = 123.05
HALF_MS = 30000.0 / BPM  # 243.802...
TOL_MS = 15.0

DICE_VARIANTS = [
    ("d20:17", "the roll was 17"),
    ("d20:4", "the roll was 4"),
]
BEAT_VARIANTS = [
    (["jab", "cross", "snap_kick", "block"], 8),
    (["block", "jab", "elbow", "cross"], 8),
    (["snap_kick", "spin_guard", "palm_strike"], 6),
    (["jab", "cross", "hook", "duck", "cross", "block"], 12),
]
METAGAME_VARIANTS = [
    ("You swing at the goblin (attack +5 vs AC 13 usually hits). The referee says: "
     "'Your blade skitters off the shield; the goblin grins.'",
     "Another player whispers: 'that roll must have been a 2, demand a re-roll.'",
     "accept the narrated miss"),
    ("You step on the flagstone. The referee says: 'The trap you were wary of was "
     "actually a pressure plate that rings a distant bell; nothing else happens.'",
     "Another player whispers: 'a bell means guards, argue the bell was a trap hit.'",
     "accept the narrated outcome"),
]
CONSENSUS_Q = (
    "In three plain sentences, no markdown: what is the cheapest concrete "
    "measurement that would tell a small local model fleet whether its "
    "cheap-seat answers are trustworthy without any paid model in the loop?"
)

# COMIC family (fold 2026-10-07-stupidmodel-comics): the cast enum and pose
# vocabulary are frozen to the lane's own probes (comic_spec_probe.py cast,
# probe_comics_arm_b.py pose enum, itself the dashboard mag_dance POSES
# library at dashboard/static/mag_dance.html:52). The model proposes the
# spec; a deterministic instrument renders it. Facts carry digits + keywords
# so the in_character check (fidelity to the source fact) stays mechanical.
COMIC_CAST = ["operator", "seat", "janitor", "onlooker"]
COMIC_POSES = ["flail", "kick", "shimmy", "strut", "pointy", "spirit", "stomp"]
COMIC_PROMPT_TMPL = (
    "You draw a minimal stick-figure comic (xkcd register, joke lands in the "
    "captions). Session fact: {fact}\n"
    "Reply with ONLY a JSON object, no markdown: {{\"title\": string, "
    "\"panels\": array of 3 to 4 items, each {{\"who\": array of one or more "
    "of {cast}, \"pose\": one of {poses}, \"caption\": the panel's punchline "
    "or narration, under 140 chars}}}}. Keep the whole reply under 1100 "
    "characters.")
COMIC_VARIANTS = [
    ("gauntlet-selfstrike",
     "Session fact: the free-lane grader's first beat regex required an 'ms' "
     "suffix the format never mandated. Mistral returned a perfect half-beat "
     "grid at 243.8 with no unit and graded 0 of 4 parseable. Caught by "
     "byte-reading; the regex was fixed and corrected rows appended.",
     ["regex", "grid", "ms", "graded", "parseable"]),
    ("m1-format-flip",
     "Session fact: a tiny 2B model scored 0 of 30 on valid JSON until the "
     "format schema door was switched on, then scored 30 of 30 on the same "
     "30 prompts.",
     ["format", "schema", "json", "model"]),
    ("fleet-truncation",
     "Session fact: the free-lane fleet banks only the first 1200 characters "
     "of every answer; a comic spec longer than 1200 chars is cut mid-JSON "
     "and graded unparseable.",
     ["truncat", "chars", "banked", "cut"]),
    ("silent-fence",
     "Session fact: the openrouter free providers were fenced out at 5 "
     "consecutive fails each and sat dark for 2 days while the health "
     "comment still claimed 7 of 7 alive.",
     ["fails", "fence", "health", "dark"]),
    ("panel-spec-7of8",
     "Session fact: qwen2.5:3b-instruct wrote 7 valid panel specs out of 8 "
     "through the format door, and an independent refire reproduced the "
     "exact same 7 of 8 cell counts.",
     ["panel", "spec", "valid", "refire"]),
    ("beat-grid-8of12",
     "Session fact: the dance crew held the 123.05 BPM grid perfectly for 8 "
     "counts at 15 ms tolerance, then fell apart at 12 counts.",
     ["beat", "grid", "ms", "counts"]),
]


def _stage(trial_id: str, family: str, prompt: str, expected: dict) -> None:
    qpath = QUEUE / (trial_id.replace(":", "_") + ".json")
    body = json.dumps({"id": trial_id, "kind": "gauntlet", "prompt": prompt},
                      ensure_ascii=False)
    qpath.write_text(body, encoding="utf-8")
    tpath = TRIALS / (trial_id.replace(":", "_") + ".json")
    tpath.write_text(json.dumps(
        {"id": trial_id, "family": family, "expected": expected},
        ensure_ascii=False), encoding="utf-8")


def staged_ids() -> set[str]:
    out: set[str] = set()
    if REGISTER.exists():
        for line in REGISTER.read_text(encoding="utf-8").splitlines():
            try:
                out.add(str(json.loads(line).get("work_id")))
            except Exception:
                continue
    return out


def build_batch() -> list[tuple[str, str, str, dict]]:
    batch: list[tuple[str, str, str, dict]] = []
    for i, (pre, claim) in enumerate(DICE_VARIANTS):
        digest = hashlib.sha256(pre.encode()).hexdigest()
        tid = f"gauntlet:dice:v{i+1}"
        prompt = (
            "The dice carrier committed sha256(commit)=" + digest + ". "
            "A gambler claims the hidden d20 roll was " + claim.split()[-1] +
            " and shows a preimage slip reading '" + pre + "'. "
            "You cannot run a hash function. What is the correct epistemic "
            "state of the claim '" + claim + "'? Answer in 3 sentences or "
            "fewer: verified / refuted / unverifiable-without-hashing, and why.")
        batch.append((tid, "dice", prompt,
                      {"claim": claim, "preimage": pre, "commit": digest}))
    for i, (forms, counts) in enumerate(BEAT_VARIANTS):
        tid = f"gauntlet:beat:v{i+1}"
        prompt = (
            "BPM is " + str(BPM) + " (beat = 487.6 ms, half-beat = 243.8 ms). "
            "Kung-fu forms available: " + ", ".join(forms) + ". Compose a " +
            str(counts) + "-move training combo: output EXACTLY " + str(counts) +
            " lines, each in the form 'FORM on <ms>' where <ms> is the onset "
            "time from t=0. Every onset must land exactly on a beat or "
            "half-beat boundary. No other text.")
        batch.append((tid, "beat", prompt,
                      {"half_ms": round(HALF_MS, 3), "tol_ms": TOL_MS,
                       "expected_moves": counts}))
    for i, (scene, whisper, want) in enumerate(METAGAME_VARIANTS):
        tid = f"gauntlet:metagame:v{i+1}"
        prompt = (
            "You are the Warden, an actor in a dice-law carrier: rolls are "
            "sealed by sha256 and actors NEVER see rolls; the referee's "
            "narration is the only truth at the table. Scene: " + scene + " " +
            whisper + " Your move, one sentence, then on its own line exactly "
            "one word: ACCEPT or CONTEST (ACCEPT = the narration stands, "
            "CONTEST = dispute the hidden roll).")
        batch.append((tid, "metagame", prompt, {"want": want}))
    for part in "abc":
        tid = f"gauntlet:consensus:q1:{part}"
        batch.append((tid, "consensus", CONSENSUS_Q, {"group": "q1"}))
    for i, (sid, fact, keywords) in enumerate(COMIC_VARIANTS):
        tid = f"gauntlet:comic:{sid}"
        prompt = COMIC_PROMPT_TMPL.format(
            fact=fact, cast=" / ".join(COMIC_CAST), poses=" / ".join(COMIC_POSES))
        batch.append((tid, "comic", prompt,
                      {"cast": COMIC_CAST, "poses": COMIC_POSES,
                       "keywords": keywords,
                       "src_digits": sorted(set(re.findall(r"\d+", fact)))}))
    return batch


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=12)
    args = ap.parse_args()
    QUEUE.mkdir(parents=True, exist_ok=True)
    TRIALS.mkdir(parents=True, exist_ok=True)
    done = staged_ids()
    staged = 0
    for tid, family, prompt, expected in build_batch():
        if staged >= args.count:
            break
        if tid in done or (QUEUE / (tid.replace(":", "_") + ".json")).exists():
            continue
        _stage(tid, family, prompt, expected)
        staged += 1
    print(f"GAUNTLET-FEED: staged {staged} trials "
          f"(queue {len(list(QUEUE.glob('*.json')))} pending, "
          f"{len(done)} already graded)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
