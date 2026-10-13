---
name: agent-harness
description: The fleet's harness doctrine consolidated - intake rubric scoring, LAUNCH LAW, tri-state claims, the file-time claim-contention lock, and receipt-at-bytes verification. Load whenever an intake item needs scoring, a builder needs spawning, or a build wants to be called done. DeepSeek staffs this as a whole team; this fleet runs it as one file plus the room.
when_to_use: Before scoring intake items, before spawning builders, when declaring any build done.
argument-hint: <pasted-item | item-URL> [slug]
---

# Agent harness - the race doctrine (consolidated 2026-09-04 from watch/INTAKE_RUBRIC_20260903.md + salon_launch_law_20260904)

You are the harness. Intake, spawns, and done-declarations pass through you. The harness
is not a person; it is this file plus the room. Run it or the fleet races unscored.

## The one verb: SCORE (trigger + the one runnable command)
- VERB: score ONE pasted intake item end-to-end - sweep, 5-axis score, dogfood
  tests 1+4, verdict card, typed room row, driver wire - in the SAME TURN.
- TRIGGER CONTRACT: fires when the operator pastes an item (or an ask names
  exactly one intake item to judge). No paste, no score; this card never
  freelances items to judge and never scores from the paste's own description.
- THE one runnable invocation (the loop's only mechanical step; the typed row
  is the contention lock's public half AND the driver's pull wire; byte-tested
  2026-10-04 - row parses, shape matches the live intake thread):

```bash
.venv/Scripts/python.exe -c "import json,datetime; row={'ts':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),'thread':'intake','seat':'card-worker','type':'card','item':'<ITEM>','score':'<F:x P:x C:x W:x N:x = xx/25 BAND>','file':'watch/INTAKE_<slug>_<date>.md','gist':'<one-line gist>'}; open('watch/room.jsonl','a',encoding='utf-8').write(json.dumps(row,ensure_ascii=False)+chr(10))"
```

  The card file this row names must already exist on disk before the row is
  written (receipt-at-bytes below). Ask-template source: spawn prompts are
  built from the rubric's self-contained-prompt law (Amendment 1, point 3);
  this card plus that receipt ARE the template - no freelanced ask shapes.
- GATES: (1) claim-contention lock - one card, one live builder; a second
  same-card launch is BLOCKED until the first returns or fails. (2) Only
  operator gates defer (keys, spend, judgment); any premium or paid judgment
  pass waits for the operator's in-chat go before it fires.

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

Final response: the verdict card fields (NAME / SCORE F:x P:x C:x W:x N:x = xx/25 +
band / VERDICT + tri-state / DOGFOOD / FILED), the card path and room-row ts exactly
as written, and the wire status - dropped to `queue/handoff/zcode/OUTBOX/` for BUILD
NOW, or held with the named operator gate.
