# X4 - DUEL SERIES: the n=1 fix (coverage gap 5) - 2026-09-29/30

Mission (COVERAGE_GAPS_20260930.md row 5): the blind rejudge flipped the
one banked duel verdict (qwen 19-17) and the router row was riding a coin
flip; S5 says n~30-60. This lane is the first installment: 10 live blind
duels, qwen/qwen3.8-max-prime (logical A) vs z-ai/glm-5.3-prime (logical
B), ember judge, under a $3.00 ABSOLUTE cap.

## What landed

- `watch/inbox/hydrology/x4_duel_series.py` (new driver): imports
  `tools/duel_harness.py` (v1.1: anonymized judge, parity slot swap,
  a_headers/b_headers style control) and fires 10 asks per the S5 task
  mix: 3 adversarial-review (mag/hydrology.py, mag/water_graph.py, the
  compass), 3 planning (hydrology rung 2, duel-to-n30 plan, gap
  closure), 2 schema-design (duel ledger row v2, hydrology.v2 spec), 2
  grading (hydrology vs its own docstring, the W3 v1.1 receipt as audit
  artifact). Every ask embeds a byte-true repo doc read at runtime plus
  the gopher LAWS line (no em-dashes, cite paths, UNPROVEN marking).
  Per-shape judge rubrics. Hard budget guard (no fire when spent +
  $0.25 projection exceeds $3.00), width-1 sequential firing, and
  idempotence: ask_ids already banked in the ledger are skipped, so a
  killed run resumes without double spend.
- 10 rows appended to `logs/duel/duels.jsonl` (ids `x4-*`, ledger now
  12 rows). Swap alternated perfectly across the series (false/true
  five times each). Zero em-dashes in all 12 ledger rows (byte check,
  chr(0x2014)).

## VERDICT: glm-prime 7, qwen 2, TIE 1 (n=10, blind)

| ask_id | winner | duel cost |
|---|---|---|
| x4-adv-hydrology-rung1 | B glm | $0.1016 |
| x4-adv-water-graph | B glm | $0.1353 |
| x4-adv-compass | TIE | $0.1170 |
| x4-plan-hydrology-rung2 | B glm | $0.0946 |
| x4-plan-duel-to-n30 | A qwen | $0.0993 |
| x4-plan-gap-closure | B glm | $0.0745 |
| x4-schema-duel-row-v2 | B glm | $0.0865 |
| x4-schema-hydrology-v2 | B glm | $0.1058 |
| x4-grade-hydrology-vs-docstring | B glm | $0.0930 |
| x4-grade-harness-receipt-v11 | A qwen | $0.0547 |

Per shape: adversarial-review B2/TIE1, planning B2/A1, schema-design
B2, grading B1/A1. glm-prime leads every shape it contested.

## Does the blind flip hold at higher n? NO

The n=1 blind flip toward qwen does not replicate: at n=10 fresh blind
duels glm-prime wins 7-2. Including the retro blind rejudge, blind-era
totals are glm 7, qwen 3, TIE 1 (n=11). The flip now reads as judge
variance on a single pair of fixed answers, not a blinding effect; the
name-aware v1.0 row (glm) and the blind majority agree. Honesty bar:
exact binomial P(>=7 of 9 | p=0.5, ties dropped) = 0.0898 one-sided,
so even now CI does not exclude zero. Keep sampling toward n=30 per the
T3 clause before any router row is called calibrated.

## Style control (why this matters)

qwen writes 37 percent more chars (mean 8,122 vs 5,928) and 2.4x the
markdown headers (114 vs 47 total), yet loses 7 of 10: volume is not
buying verdicts under the "depth beats prose" judge law. When qwen does
win, its header count averages 14.5 vs 9.9 in losses; the covariate is
logged per row (a_headers/b_headers) for the n=30 regression.

Caveat for future readers: judge rationales speak in SLOT terms; on
swap=true rows slot A is logical B (glm), so "A wins..." in a rationale
maps to the banked winner B. The banked winner/criteria fields are
already remapped to logical contenders by the harness.

## Costs (metered from usage.cost in the banked rows)

- Series total: $0.9623 of the $3.00 cap (mean $0.096/duel; qwen
  contender is the cost driver at roughly 2.4x glm per duel).
- No budget holds triggered; no failed or UNPARSED duels; exit 0.

## Next steps (gap 5 not closed, n=10 of 30)

1. Re-run the driver (idempotent) with ~10 fresh asks per next window,
   roughly $1.0 per window at this rate; add the ask bank split (70/30
   hidden) once n passes 20.
2. At n=30 compute the multinomial CI on (A, B, TIE) and only then
   rewrite the router row; until then the W3 consequence line stays
   flagged n=1-reversed.
3. Judged-not-by-ember sensitivity check owed at n=30 (one alternate
   judge over the same banked answers, retro mode, ~$0.03).
