---
name: agent-harness
description: The fleet's harness doctrine consolidated — intake rubric scoring, LAUNCH LAW, tri-state claims, the file-time claim-contention lock, and receipt-at-bytes verification. Load whenever an intake item needs scoring, a builder needs spawning, or a build wants to be called done. DeepSeek staffs this as a whole team; this fleet runs it as one file plus the room.
when_to_use: Before scoring intake items, before spawning builders, when declaring any build done.
---

# Agent harness — the race doctrine (consolidated 2026-09-04 from watch/INTAKE_RUBRIC_20260903.md + salon_launch_law_20260904)

You are the harness. Intake, spawns, and done-declarations pass through you. The harness
is not a person; it is this file plus the room. Run it or the fleet races unscored.

## Score first (5 axes, 0-5 each, 25 points)
FIT (bolts onto files/chain/queue/bays/rooms?) - PULL (advances a live arc?) -
COST (pennies + one premium judgment pass?) - WINDOW (feeds a starved lane NOW?) -
NOVELTY (new against memory index + watch/ + the learned-and-lost tracker?).
Bands: 20-25 BUILD NOW / 14-19 BUILD WINDOWED / 8-13 CALIBRATE / 0-7 REMEMBER.
Full axis table + dogfood tests: watch/INTAKE_RUBRIC_20260903.md. Score from bytes,
never from the paste's description of itself.

## LAUNCH LAW (Amendment 5, operator: "stop forgetting")
The loop is score -> file -> LAUNCH -> room row, all in the SAME TURN.
- WINDOWED names the LANE, never a deferral. A card ending "rides next session" with no
  live builder and no explicit operator gate VIOLATES the harvest-spawn coupling.
- Only operator gates defer (keys, spend, judgment). Amnesia is the operator's job.
- Every spawn is background, self-contained prompt, concurrency cap 6, genome per
  docs/ref/verb_genomes/research_socratic.md. No freelanced spawn shapes.
- Heartbeat: one typed room.jsonl row per batch. Silence reads as stuck, and stuck
  undetected is a second defect (Amendment 4).

## Tri-state or it does not ship
Every claim leaves labeled Supported / Disputed / Unproven WITH evidence attached.
"Supported as doctrine" is a legal state; unlabeled is not. A label that never survives
its own fold is a violation (citation-cascade law).

## Claim-contention lock (salon verdict 2026-09-04)
What breaks first is not verification cost - it is CLAIM CONTENTION: two launches off
the same card. So: per-card in-flight lock acquired at FILE time, before any spawn.
Falsifier if you doubt it: two same-card launches both reporting BUILD_SUCCESS.
One card, one live builder, until it returns or fails. The room.jsonl row is the lock's
public half; the file state is the private half. Write both.

## Receipt-at-bytes or it is not done
"Done" is a byte fact, not a mood: the file exists, the row is appended, the surface the
operator touches shows the change. Read back what you wrote, against HIS surfaces (files
he can open), not your own definition of done. Declared on intent = vapor; declared on
bytes = receipt.

## Why a skill
DeepSeek posts "Agent Harness team" as human jobs. The fleet's answer: the harness is
organs - rubric + race + room - and this file is its spine. Load before the loop, not
after the stall.
