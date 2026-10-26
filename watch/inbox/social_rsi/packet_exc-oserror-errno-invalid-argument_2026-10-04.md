# SOCIAL RSI PACKET - exc oserror errno invalid argument

Filed 2026-10-04 by tools/social_rsi.py v0 (pattern rank by windowed
count; day window 14d).

## Pattern (instrument-named)

- class (normalized detail key): `exc oserror errno invalid argument`
- count: 825 CYCLE_FAIL rows in the 14d window
- instrument: `queue/lanes/*/trail.jsonl` CYCLE_FAIL event rows,
  keyed by mag.lane_runner.normalize_detail (the mag/lane_runner.py
  CLUSTER_REPORT keying, so this cross-lane roll-up speaks the
  same class language as the per-lane reports)
- first-seen (window): 2026-09-25T14:51:58+00:00
- last-seen (window): 2026-10-04T10:15:17+00:00
- lanes affected: research(454), builder(344), night(26), prose(1)
- example detail (verbatim from the newest matching row class):
  `EXC OSError: [Errno 22] Invalid argument: '/app/queue/lanes/builder/runner_state.json'`
- failure_kb join: 0 matching rows in the windowed
  `logs/failure_kb.jsonl` (17841 rows scanned)
  no matching signature - the KB covers seat/session failures;
  a lane-cycle pattern absent from it is new evidence, not noise

## Evidence pairs (before/after)

- lane `builder`: CYCLE_FAIL at 2026-10-04T09:45:33Z ->
  CYCLE at 2026-10-04T09:46:36+00:00
  (gap 63s); recovery detail: drops gated=0; queue on surface
- lane `night`: CYCLE_FAIL at 2026-10-03T23:08:04Z ->
  CYCLE at 2026-10-03T23:10:55+00:00
  (gap 171s); recovery detail: night composite: monitor rc=0; march rc=1

## Matching receipts (watch/inbox grep, cap 3)

- `watch/inbox/MIGRATION_CLEANUP_20260919.md` (matched: argument, invalid, oserror)
- `watch/inbox/audit_20260926/LANE2_DOGFOOD_TOOLS.md` (matched: argument, invalid, oserror)
- `watch/inbox/audit_20260926/WAVE2_LANE2_PUSH_BLOCKERS.md` (matched: argument, invalid, oserror)

## SYNTHESIS ASK (seated step: a seat or free lane, not this tool)

Draft ONE skill card for `.agents/skills/<verb-slug>/SKILL.md` that
prevents or repairs this pattern, in the estate's winning shape per
`watch/inbox/IMAGE_BLASTER_GO_20261003.md` (the five card-editing
rules its lane measured) with `.agents/skills/image-blast/SKILL.md`
as the template:

1. argument-hint frontmatter - a real argument surface, not prose
2. exactly one verb per card
3. at least one runnable command with a verified (not phantom) path
4. gates written into the card text where the action happens
5. a `Final response:` line naming what the seat reports back

Synthesize from the evidence pairs above (what failed, what
greened after), the receipts above, and the failure_kb signature
if one matched. The card must name this pattern's class key
(`exc oserror errno invalid argument`) in its description so the falsifier can
measure it: a session with the card active should fail less on
this class than without (the arena/gwap instrument, per
watch/inbox/X_INTEL_PAPERS_20261004.md section 6's falsifier).

## Promote gate (the commit stays human)

This packet is the deliverable. Drafting the card is a separate
seated step BY DESIGN: the human promote gate (`mag.cmd promote
--apply`) stays the commit - autonomously drafted, humanly
promoted. The skill census law holds (the ractor50 verdict: waves
are the fuzzer, cards are the commits).
