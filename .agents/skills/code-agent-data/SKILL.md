---
name: code-agent-data
description: The Code Agent Data engineer organ — room.jsonl rows, seat session tapes, and intake cards ARE the training corpus for the fleet's successors. Load when mining sessions for training data, when judging whether a tape is corpus-grade, or when the QLoRA campaign's Stage 2/3 asks for food. DeepSeek hires humans for this role; the fleet runs it as a cadence over files it already writes.
when_to_use: When mining sessions for training data, when deciding if a tape is corpus-grade, when the campaign's Stage 2/3 asks for food.
---

# Code Agent data — the corpus organ (2026-09-04, from FRONTIER_MAP_DEEPSEEK_20260904.md gap b)

The fleet's own traffic IS the dataset. Three sources, written as a side effect of working:
- watch/room.jsonl — the typed rows: receipts, folds, steals, heartbeats.
- Seat session tapes — queue/handoff/<seat>/CONVO.md + INBOX/OUTBOX + session logs.
- Intake cards — watch/INTAKE_<slug>_<date>.md: verdicts with scores and falsifiers.

Coverage thesis: ACTION WITHOUT RECORD NEVER HAPPENED. A missing room row makes the
build unfalsifiable and untrainable. The row is first-class output, not an afterthought —
this skill exists because mining lapsed since Aug and the corpus starved while the
fleet kept working.

## Mining cadence
Night windows (the 04:00 class, when free lanes quiet). One window = one pass:
sweep room.jsonl from the last mined ts -> sweep seat tapes -> fold into the
Stage 2/3 corpus packer with a manifest. Cursor = last ts mined; never re-mine blind.
Mining without the gate check just manufactures vapor with a manifest attached.

## Substance floor (the Stage 2/3 gate)
A tape enters the corpus only at >=600 bytes AND at least one ##Result-class section:
verdict, measurement, falsifier outcome, or correction with contrast. Under the floor
it is a heartbeat, not food — leave it out and say so in the manifest.

## Training-grade vs vapor
TRAINING-GRADE: wrong move vs corrected move in one tape (contrast is the signal),
tri-state labels with evidence attached, falsifiers with pass/fail, corrections dated
and pathed, byte receipts. VAPOR: mood summaries, "made progress", plans without
outcomes, unlabeled claims, self-praise. The distilled policy shape from
.agents/skills/operator-corrections/SKILL.md (name, own language, WHY, one testable
next step, cite, mark [inferred]) is the per-record quality bar.

## Why a skill
DeepSeek lists Code Agent 数据工程师 as a human job. The fleet's answer: the tapes are
already being written every turn; the organ is the cadence that turns them into food.
Feed Stage 2/3 from your own traffic before buying anyone else's.
