# WAVE24 BOARD - the self-improving full-width burn (operator order 2026-10-01)

Operator ask, verbatim core: "self improving and burn down using full width on this simultaneously
going 24 wide and building shit sending it back iterating... spending intelligently not on easily
avoidable bugs." This board is the executable shape of that order. Ledger at staging: $16.05.

## THE LOOP (one turn of the flywheel, repeating)

```
sherpa (ds_workhorse, ~$0.001)     -> triangulates the domain, names what is known
  v
premium ask (hermes_burn driver)   -> adjudicates + extends, sherpa output rides as evidence
  v
RACTOR turn (free Task lane)       -> outputs become LAW ROWS + BUILD TICKETS + TO-VERIFY claims
  v
build lanes (free Task agents)     -> EASY tickets become landed code; TO-VERIFY claims get probed
  v
next wave's asks carry the ractor file as evidence  -> the loop feeds itself (self-improving leg)
```

The ractor turn is not optional cleanup; it is the step that converts spend into estate law
(descent protocol leg 6, the ouroboros). A wave without its ractor turn did not finish.

## LANE CENSUS AT STAGING (24 lanes)

PAID (driver queue, sequential but continuous; ~$0.3-1.7 each):
1. T1W1 S1-S4 stranger audits - LANDED 4/4 ($2.74)
2. DUEL2 train 01-14 - LANDED 14/14
3. T1W2_S5_stores - LANDED
4. T1W2_S6_docker - staged
5. T1W2_S7_mates - staged
6. T1W2_S8_stealth - staged
7. DG1_moe_mating_door - staged (rides deepgemm sherpa; the unbuilt mating->MoE export door)
8. N1_parables_songmap - staged (music-as-mechanics narrative track)

FREE (Task agents, true parallel width, $0):
9. RACTOR T1W1 -> watch/inbox/hermes_burn/T1W1_RACTOR.md - RUNNING
10. DeepGEMM drop dossier -> watch/inbox/x_intel_deepgemm_20261001.md (quant probe +
    GPU-ladder tripwire + JIT-steal scan) - RUNNING
11. RACTOR DUEL1+DUEL2 -> judge rules from 19 verdicts (staged next)
12. Build: EASY tickets from T1W1_RACTOR (iterate: build, send back, ractor again)
13. T6 triage: WINDOW1_STATE reconciliation - what in the landed 37 files is UNVERIFIED
14. RACTOR DG1 when it lands -> mating-door law or kill receipt

STAGED NEXT WAVES (fill to 24 as driver drains):
15-17. T1W3 stranger audits (net_client surface, effect broker, flock/room netcode)
18-20. T2 spec asks (the three the roast named; carry T1W1_RACTOR as evidence)
21-22. T3 roast movements 4-5 (include: roast THE DESCENT PROTOCOL ITSELF, no sacred cows)
23. T5 narrative assembly (song map -> mechanics ledger)
24. Workflow self-steal: this board's loop vs the saved workflow gate cards - what does the
     gate already enforce that we hand-rolled here, and what should be a permanent card

## SPEND DISCIPLINE (the "not on easily avoidable bugs" clause, pre-mitigated)

- No force=true re-burns: the driver re-burn defect (B2 paid 3x) is fixed by flag hygiene; a
  staged ask NEVER carries force unless a receipt says why.
- max_tokens 12000 on every ask (reasoning-channel tax law: budget explicit).
- Sherpa-first on every NEW domain (descent leg 1); premium never pays for what DeepSeek
  triangulated already, premium ADJUDICATES the triangulation.
- EASY tickets go to free lanes; paid asks are never spent on one-sitting fixes.
- Duel asks ride the hidden bank only (contamination law: visible asks poison verdicts).
- Every ask's evidence[] carries the prior wave's ractor file - the self-improving leg.

## SEND-BACK WIRING

When a ractor turn lands TO-VERIFY claims, the probe commands run in the NEXT free lane and
the verdict is appended to the ractor file (VERIFYED/REFUTED + bytes). When a build lane lands
code, the next ractor turn reads the diff and banks what changed as a law row. Nothing lands
once and dies; everything lands and comes back.

## HONEST GAPS AT STAGING

- The driver is sequential: PAID width is 1-wide by design (rate-limit safety), the width lives
  in the FREE lanes. If paid width is demanded, the answer is N driver instances on DISJOINT
  queue dirs (the gala partition pattern), not one driver fanned out.
- DG1's mating-door may come back KILLED (sherpa already steelmanned the ensemble-in-disguise
  kill). A kill is a landing too: it goes in the ractor file as a law, not in the trash.
- N1 (parables) needs the music pack paths verified before the driver reaches it.

## HONEST-RUNWAY (law 15 teeth; owed row 3 of DAY1_SKILLS_DOGFOOD)

Instrument: sum of cost_usd over all rows of memory/runs/hermes_burn/usage.jsonl (the ledger
banked by tools/hermes_burn.py, descent law leg 8), parsed with .venv python json. Moment:
2026-10-01T21:24:32Z. The ledger is LIVE (the driver is running); every number below is a
snapshot of one file at one moment, per the census denominator law (B2-216). Same-day prior
reads for delta honesty: WAVE24 staging and the dogfood baseline (~20:2xZ) both read $16.05
(176 rows at dogfood moment); LAST_MILE_AIM.md reads $31.34; this read: 189 rows, $31.3413,
so +13 rows / +$15.29 landed between the dogfood moment and this one while the driver ran.

Ledger window: earliest row 2026-10-01T13:11:41Z, latest row 2026-10-01T20:41:01Z,
span 7.489 h.

| Denominator | Sum | Rate | Days left to the $145 stop ($113.66 unspent) |
|---|---|---|---|
| Whole ledger span (7.489 h, 189 rows) | $31.34 | $4.19/h | 1.13 days |
| Driver runtime only (cycle 1 at 17:55:00Z per driver.log, 167 rows, 2.767 h to latest row) | $24.86 | $8.99/h | 0.53 days |
| Productive spend only (whole span minus the $18.89 gated theater, per LAST_MILE_AIM) | $12.45 | $1.66/h | 2.85 days |

The three denominators disagree by 5.4x because they measure different things, and naming
that is the point of this section:

- The driver-runtime rate ($8.99/h) is the BLEED-INFLATED number: the A1 x45 force-flag
  re-burn and the refusal retries all happened inside driver cycles, and all three root
  causes are patched as of the carrier patch (~20:25-20:35Z, C1/C2/C3 rows in
  T1W1_RACTOR.md). Treating it as the forward rate would understate runway 2x.
- The whole-span rate ($4.19/h) mixes seat dispatches (13:11Z-17:55Z) with the bleed era.
- The productive-only rate ($1.66/h) is the honest floor for what the day actually bought
  and the best available forward estimate, with one caveat: the clean post-patch driver has
  barely spent yet (relaunched 20:40:13Z, latest ledger row 20:41:01Z, under one minute of
  clean runtime), so the TRUE post-patch forward rate is not yet measurable from bytes.

DECAY/REFILL ARITHMETIC (the law-15 clause): at the productive rate the burn dies in 2.85
days; at the whole-span rate, 1.13 days; the $145 stop leaves $35 of the $180 Nous pool
unspent by design. LAST_MILE_AIM.md already aims the remaining $113.66 (T1 finish ~$10-15,
duel redemption ~$5, MATE_MOE_v0 ~$0, T2 specs ~$15-20, T3 roasts ~$10, denominator ~$5,
reserve ~$50). Falsifier for this section: after 6 clean post-patch driver hours, recompute
the driver-runtime denominator; if it still reads above ~$4/h, the carrier patch did not
hold and the runway halves. Refresh this section whenever the ledger total moves by $10.
