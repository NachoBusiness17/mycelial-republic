# Z2 - DUEL SERIES n=21 installment (gap 5 continuation) - 2026-09-29

Mission (X4_DUEL_SERIES.md next step 1): re-run the driver shape with ~10
fresh asks this window toward n=30. This lane fired 10 live blind duels,
qwen/qwen3.8-max-prime (logical A) vs z-ai/glm-5.3-prime (logical B),
ember judge, under a $2.50 ABSOLUTE cap. Blind-era tally entered at n=11
(glm 7, qwen 3, TIE 1) and exits at n=21.

## What landed

- `watch/inbox/hydrology/z2_duel_series.py` (new driver): exact X4 shape
  (imports tools/duel_harness.py v1.1 blind judge, parity slot swap,
  a/b chars + header style counts, idempotent ask_id skip, width-1
  sequential, hard budget guard). Fresh artifacts and shapes so the
  verdict is not overfit to the X4 ask bank: 3 adversarial-review
  (census_drift_patrol.py, workflow_gate.py, docs/DNA.md), 2 planning
  (chan steer wiring, n=30 closeout), 2 schema-design (ask-bank
  manifest, chan.v2), 1 grading (patrol vs its own docstring), 2
  code-analysis (duel_harness.py defect hunt, corpus_fts_rebuild.py
  failure modes). Code-analysis is a new shape this series.
- 10 rows appended to `logs/duel/duels.jsonl` (ids `z2-*`, ledger now
  22 rows). Swap alternated perfectly (F/T five times each, continuing
  the ledger parity). Zero em-dashes in all 22 rows (byte check,
  chr(0x2014)). One contender retry all series: z2-code-duel-harness-
  defects:A returned empty content, the harness retried same model next
  key per its no-rotation law and banked at $0.1522 (reasoning burn),
  no duel lost.

## VERDICT: this window 5-5, blind era glm 12, qwen 8, TIE 1 (n=21)

| ask_id | winner | shape | duel cost |
|---|---|---|---|
| z2-adv-census-patrol | B glm | adv | $0.1009 |
| z2-adv-workflow-gate | A qwen | adv | $0.0969 |
| z2-adv-dna | A qwen | adv | $0.0908 |
| z2-plan-chan-steer | B glm | plan | $0.0938 |
| z2-plan-n30-closeout | A qwen | plan | $0.0788 |
| z2-schema-askbank | B glm | schema | $0.0739 |
| z2-schema-chan-v2 | A qwen | schema | $0.1072 |
| z2-grade-patrol-vs-docstring | B glm | grade | $0.0967 |
| z2-code-duel-harness-defects | A qwen | code | $0.2071 |
| z2-code-fts-rebuild-modes | B glm | code | $0.1220 |

Blind-era per shape (live + retro rejudge): adv B3/A2/T1, plan B3/A2,
schema B3/A1, grade B2/A1, code B1/A1. glm still leads or ties every
shape it contested, but its X4 margins shrank.

## Does glm's lead hold? WEAKENED, still not significant

X4 ended glm 7-2 (live). This window is a dead 5-5 split, so the blind
era now reads glm 12, qwen 8 over 20 decided. Honesty bar: exact
binomial P(>=12 of 20 | p=0.5, ties dropped) = 0.2517 one-sided; the CI
still straddles zero and moved AWAY from significance versus X4's
0.0898. The X4 read (glm pulls ahead) does not replicate at higher n;
the honest current statement is a mild glm edge indistinguishable from
a coin at n=21. Keep sampling to n=30 before any router row.

## Style control and a new position-bias signal (running)

- Volume: qwen still writes 26 percent more chars (mean 7,653 vs 6,073
  over the 20 live blind duels) and 2.3x the markdown headers (218 vs
  95 total), and still does not convert volume into verdicts.
- The X4 covariate claim (qwen wins ride higher header counts) weakened
  at n=20: qwen win rows average 11.7 headers vs 10.0 in losses (was
  14.5 vs 9.9 at n=10). No longer a clean story; keep the covariate.
- NEW signal this window: the judge's slot A (answer presented first)
  won 13 of 20 live duels (slot B 6, TIE 1). glm in slot A went 8-2;
  glm in slot B went 4-5-1. Both contenders win more from slot A, so
  this reads as first-position favoritism (or an interaction with glm's
  style), not model skill. P(>=13 of 20 | p=0.5) = 0.1316 one-sided:
  not conclusive, but it is exactly the residue the parity swap exists
  to cancel, and it stays on the watch list for n=30. Banked winners
  are unaffected (always remapped to logical contenders).

Caveat carried from X4: judge rationales speak in SLOT terms; on
swap=true rows slot A is logical B (glm). Banked winner/criteria fields
are remapped by the harness.

## Costs (metered from usage.cost in the banked rows)

- Series total: $1.0681 of the $2.50 cap (mean $0.107/duel; the
  $0.2071 harness-defects duel includes the one retry). qwen remains
  the cost driver (~1.9x glm per duel this window).
- No budget holds triggered; no UNPARSED duels; exit 0.

## Next steps (n=21 of 30)

1. One more window: ~9 fresh asks (~$1.0) reaches n=30. Add the 70/30
   hidden ask-bank split at that point (schema landed this window as
   the z2-schema-askbank duel ask).
2. At n=30 compute the simultaneous CI on (A, B, TIE) per the
   z2-plan-n30-closeout ask; only then rewrite the router row.
3. Alternate-judge retro sensitivity check (~$0.03) over banked answers
   at n=30, plus a slot-A-vs-slot-B tally as the position-bias control.
