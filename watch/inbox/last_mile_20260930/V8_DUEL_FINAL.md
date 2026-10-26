# V8 - DUEL QUESTION CLOSED: final n=30 tally + CI verdict - 2026-09-30

Instrument: `logs/duel/duels.jsonl` read at 31 rows, 2026-09-30 ~09:53 UTC,
last row `lw9-code-shared-surface` (ts 2026-09-30T09:52:07Z). Denominator law:
the blind era is exactly rows 2..31 of that snapshot (30 rows; row 1
`retro-g1-vs-g3-adversarial-baseline-20260929` is the unblinded v1.0 retro and
is excluded). A sibling lane (`v1_multifamily_duel.py`) also writes to this
ledger and may bank rows after this boundary; any later row is a different
series and is NOT part of this n=30.

## How the last 7 landed (no double spend)

The lw9 driver (`watch/inbox/last_mile_20260930/lw9_duel_series.py`, Z2 next
step 1, $1.50 series cap) was already in flight under another process when
this seat arrived at 24 ledger rows. This seat verified the live process
(PID 27644), let it finish its remaining idempotent asks, and fired nothing:
zero double-fired ask_ids, zero extra spend from this seat. Final lw9
series: 9 duels banked (2 adv, 2 plan, 2 schema, 1 grade, 2 code), all
parsed, zero UNPARSED, zero em-dash bytes (chr 8212 scan over all 31 rows),
swap alternation perfect across the blind era (T/F strict alternation).

## FINAL n=30 TALLY (blind era, logical terms: A = qwen, B = glm)

glm 17, qwen 12, TIE 1. Checkpoints reproduce byte-true: at n=21 the tally
was glm 12, qwen 8, TIE 1 (matches Z2_DUEL_N30.md and the operator brief);
live slot-A wins at n=21 were 13/20 (matches). This window (lw9, n=9):
glm 5, qwen 4. Per shape over the era: adv glm 4 / qwen 3 / TIE 1, plan
glm 4 / qwen 3, schema glm 4 / qwen 2, grade glm 3 / qwen 1, code 2-2, plus
the retro rejudge qwen 1. glm leads or ties every shape; code is even.

## CI VERDICT: mild glm edge, indistinguishable from a coin

- Decided duels n=29, glm 17: exact one-sided binomial P(>=17 of 29 |
  p=0.5) = 0.2291. Not significant; X4's early 7-2 read (p=0.0898 at n=10)
  did not replicate and the p-value ROSE as n grew.
- Wilson 95% CI on glm's share of decided duels: [0.407, 0.745], straddles
  0.5.
- Simultaneous 95% multinomial CIs (Goodman, c=3, z=2.394; binomial alone
  is wrong here because the three-way tally with ties is three interdependent
  proportions): glm [0.357, 0.755], qwen [0.219, 0.613], tie [0.004, 0.212].
  The glm and qwen intervals overlap massively; no separation.
- VERDICT: PARITY. glm-5.3-prime and qwen3.8-max-prime are statistically
  interchangeable on this ask mix at n=30. The router row may be written as
  "either workhorse, judgment tier", NOT as glm dominance. The duel question
  is closed.

## SLOT-A BIAS: now significant, exactly what the parity swap existed to cancel

Slot A (answer presented first to the judge) won 19 of 28 decided live duels
(19 A, 9 B, 1 TIE over 29 live), one-sided exact P = 0.0436. At n=21 it was
13/20 (p=0.1316); the signal strengthened with n. Both models show it:
glm won 11/14 from slot A vs 6/15 from slot B; qwen won 8/15 from slot A vs
3/14 from slot B. Exposure was balanced (perfect alternation; glm saw slot A
14 times, qwen 15), so the banked logical tally is not slot-skewed; the bias
lives in the judge's first-position favoritism, not in the glm-vs-qwen
comparison. Any future duel MUST keep the parity swap; single-slot judging
would inflate whichever model happens to sit first by roughly 10 points of
win rate.

## Style control and costs

- Volume: qwen mean 8,153 chars vs glm 6,193 over the 29 live blind duels;
  headers 295 vs 141 (about 2.1x). Volume still does not convert to
  verdicts at n=30.
- Cost: lw9 window $1.1173 (9 duels; 12 percent over the $1.00 planning
  note, inside the $1.50 series cap; this seat added $0). Blind-era total
  spend $3.2591 across X4 + Z2 + LW9.

## Open (optional, not blocking closure)

- Alternate-judge retro sensitivity check (~$0.03) over banked answers, per
  Z2 next step 3; with the verdict at PARITY the expected result is
  confirmation, and it does not change the router row.
- The owed harness refactor (glm side from local Task agents) stays filed in
  the lw9 driver docstring; parity verdict makes it an economy fix, not a
  validity fix.
