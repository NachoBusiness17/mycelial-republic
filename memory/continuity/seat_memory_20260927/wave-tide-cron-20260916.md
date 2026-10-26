---
name: wave-tide-cron-20260916
description: Wave tide cron created (automation-b0ebbbb9, daily 06:15) — the Lite seat
  repurposed as the fleet's nightly compaction organ (99% asleep, 2/10K weekly); tide reads
  all new receipts → writes the warm brief → feeds a context card to local gemma → refreshes
  the deck; everything through lite_guard
metadata:
  node_type: memory
  type: project
  originSessionId: sess_f8f2909b-0ac5-4763-abba-fbd8ba748f54
---

Operator question 2026-09-16 with the Lite usage dashboard (weekly 2/10K credits = 1% used,
5h bucket 0/2K, peak 286.54M tokens on 2026-09-08, 731M cumulative lifetime): "what can we
use our lite key for? cron jobs? that tie everything we are scattershotting together that
then feed our local ollama?"

**Answer built: the tide.** The Lite seat is the compaction and synthesis organ — the one
metered, paced, strong-enough brain that reads the scattershot nightly and folds it small
enough for the local janitors to carry. ~0.5–1 credit/day against the 1,400/day ceiling;
weekly pool ≈ 530M tokens of glm-5.3-flash currently evaporating each Tuesday 10:19 reset.

**AUTOMATION LIVE:** automation-b0ebbbb9-e629-417f-aef5-a503e80a12ec, daily 06:15
("Wave tide: nightly scattershot compaction"). The tide: (1) reads all receipts modified
since the last tide (state/fuel/tide/); (2) writes tide_<date>.md — 10-bullet changelog,
top 3 next stones, 3 Socratic questions, stub/contradiction flags; (3) distills a 200-word
context card → memory/corpus/tide_cards/card_<date>.md; (4) if local ollama is up, feeds the
card to gemma:2b for the 3-sentence morning brief; (5) runs scripts/build_deck.py (deck
refresh); (6) budget law: lite_guard.check/record if any model call, else read-and-write only.

**Heavier Lite-seat uses queued (in value order):** desk grading (blind-grading salon
outputs and the third-smile transcripts — the operator's hour becomes review), morning
Socratic question generation for the lanes, and the weekly canon synthesis riding the
Tuesday 10:19 pool reset (one strong pass over the week's entire output = the standing
wave's chapter). Designed rules: everything through lite_guard; tide work is read/write —
prefer zero model calls; heavy weekly jobs ride the reset, never the dregs.

**UPDATE (Carse quartet, same night): the Amendment Obligation is wired into the tide
prompt** (operator "steal it" on CG4's unanimous mechanic) — every tide now proposes
exactly ONE amendment to a fleet rule/doctrine/mechanism, appended to
state/fuel/amendments.jsonl as {"schema":"amendment.v1", day, target, change, reason,
falsifier}; an unexamined no is a silent skip. Seed row = the obligation itself,
self-booted. This makes the tide an infinite game (rules mutate in-course) instead of a
chore log.

**FIRST FIRE, 2026-09-17 06:15:** card landed (`memory/corpus/tide_cards/card_2026-09-17.md`) with night recap, owed list, and the three Socratic questions. Two honest gaps: (1) `state/fuel/amendments.jsonl` holds ONLY the boot row — the tide's own first amendment has not been appended yet, so the self-void falsifier (three consecutive no-amendment tides) is now ticking; (2) the gemma:2b leg came back thin — "GEMMA: EMPTY" first pass, then a loose 3-sentence summary ("fixed immediately", "requests he has not yet tested" = flabby). Check both on the next tide.

Related: [[lite-key-seat-glm53flash]], [[wave-20260916-standing-wave]],
[[command-deck-20260916]], [[third-smile-ladder-ready]], [[carse-finite-infinite-20260916]].
