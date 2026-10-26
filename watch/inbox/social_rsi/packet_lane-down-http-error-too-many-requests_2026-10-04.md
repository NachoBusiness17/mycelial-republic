# SOCIAL RSI PACKET - lane-down http error too many requests

Filed 2026-10-04 by tools/social_rsi.py v0 (pattern rank by windowed
count; day window 14d).

## Pattern (instrument-named)

- class (normalized detail key): `lane-down http error too many requests`
- count: 14 CYCLE_FAIL rows in the 14d window
- instrument: `queue/lanes/*/trail.jsonl` CYCLE_FAIL event rows,
  keyed by mag.lane_runner.normalize_detail (the mag/lane_runner.py
  CLUSTER_REPORT keying, so this cross-lane roll-up speaks the
  same class language as the per-lane reports)
- first-seen (window): 2026-09-20T12:00:15+00:00
- last-seen (window): 2026-10-03T12:00:10+00:00
- lanes affected: elder(14)
- example detail (verbatim from the newest matching row class):
  `lane-down: HTTP Error 429: Too Many Requests`
- failure_kb join: 0 matching rows in the windowed
  `logs/failure_kb.jsonl` (17841 rows scanned)
  no matching signature - the KB covers seat/session failures;
  a lane-cycle pattern absent from it is new evidence, not noise

## Evidence pairs (before/after)

- lane `elder`: CYCLE_FAIL at 2026-10-03T12:00:10Z ->
  CYCLE at 2026-10-04T08:20:40+00:00
  (gap 73230s); recovery detail: lens on 1 cards

## Matching receipts (watch/inbox grep, cap 3)

- `watch/inbox/burn_reset_20260927/flash50/deep-legibility.md` (matched: lane-down, requests, error)
- `watch/inbox/fillball/elder-salvage.md` (matched: lane-down, requests, error)
- `watch/inbox/frontier_olm_2026-10-03/DIGEST.md` (matched: lane-down, requests, error)

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
(`lane-down http error too many requests`) in its description so the falsifier can
measure it: a session with the card active should fail less on
this class than without (the arena/gwap instrument, per
watch/inbox/X_INTEL_PAPERS_20261004.md section 6's falsifier).

## Promote gate (the commit stays human)

This packet is the deliverable. Drafting the card is a separate
seated step BY DESIGN: the human promote gate (`mag.cmd promote
--apply`) stays the commit - autonomously drafted, humanly
promoted. The skill census law holds (the ractor50 verdict: waves
are the fuzzer, cards are the commits).
