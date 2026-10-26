# SOCIAL RSI PACKET - exc httperror http error too many

Filed 2026-10-04 by tools/social_rsi.py v0 (pattern rank by windowed
count; day window 14d).

## Pattern (instrument-named)

- class (normalized detail key): `exc httperror http error too many`
- count: 10 CYCLE_FAIL rows in the 14d window
- instrument: `queue/lanes/*/trail.jsonl` CYCLE_FAIL event rows,
  keyed by mag.lane_runner.normalize_detail (the mag/lane_runner.py
  CLUSTER_REPORT keying, so this cross-lane roll-up speaks the
  same class language as the per-lane reports)
- first-seen (window): 2026-09-21T06:30:33+00:00
- last-seen (window): 2026-10-02T06:30:27+00:00
- lanes affected: harvest(10)
- example detail (verbatim from the newest matching row class):
  `EXC HTTPError: HTTP Error 429: Too Many Requests`
- failure_kb join: 0 matching rows in the windowed
  `logs/failure_kb.jsonl` (17841 rows scanned)
  no matching signature - the KB covers seat/session failures;
  a lane-cycle pattern absent from it is new evidence, not noise

## Evidence pairs (before/after)

- lane `harvest`: CYCLE_FAIL at 2026-10-02T06:30:27Z ->
  CYCLE at 2026-10-03T06:30:21+00:00
  (gap 86394s); recovery detail: fetched=300 new=0 hits=0

## Matching receipts (watch/inbox grep, cap 3)

- `watch/inbox/FREE_LANE_INTEL_BONSAI2_20260923.md` (matched: httperror, error, http)
- `watch/inbox/GAMING_CORPUS_PASS_20260923.md` (matched: httperror, error, http)
- `watch/inbox/STIGMERGY_WITNESS_SCAFFOLD_20260913.md` (matched: httperror, error, http)

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
(`exc httperror http error too many`) in its description so the falsifier can
measure it: a session with the card active should fail less on
this class than without (the arena/gwap instrument, per
watch/inbox/X_INTEL_PAPERS_20261004.md section 6's falsifier).

## Promote gate (the commit stays human)

This packet is the deliverable. Drafting the card is a separate
seated step BY DESIGN: the human promote gate (`mag.cmd promote
--apply`) stays the commit - autonomously drafted, humanly
promoted. The skill census law holds (the ractor50 verdict: waves
are the fuzzer, cards are the commits).
