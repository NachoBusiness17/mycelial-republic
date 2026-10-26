# LAW-066 DELTA LEDGER — WITNESS #3 vs SEALED SELF-ANSWERS (2026-09-07)

First complete LAW-066 accounting. Self-answers sealed pre-witness (commission Q1–Q10:
watch/inbox/RESEARCH_COMMISSION_SELFANSWERS_20260907.md, step affc6258; pre-witness position:
"expect GAINED on Q1/Q3/Q6, CONFIRMED-ALREADY-HAD on Q2/Q4/Q5/Q7, Q8–Q10 not pre-registrable").
Verdict: memory/runs/salons/worldline_seed_20260907/ASTRA_WITNESS3_RESPONSE.md (18,337 B,
read-only audit: source inspection, independent arithmetic, prompt-hash reconstruction, tape
verification, synthetic counterexamples).

## VERDICT SUMMARY

| Question | Our sealed answer | Witness | Ledger |
|---|---|---|---|
| Q1 identity→workstate reframe | retire "identity," behavioral-continuity metric | "recovery of working state" + behavioral continuity as the frame | **CONFIRMED-ALREADY-HAD + GAINED** (L/R/C/S branch design operationalizes what we reframed — beyond our spec) |
| Q2 re-run battery | everything $0 re-runnable in 1 day | recompute-from-durations first; re-runs INSUFFICIENT — instrument repair needed first | **GAINED** (defects a re-run would have reproduced) |
| Q3 instrument reconciliation | interaction prediction + 2nd model; cut production claim | paradox DISPUTED entirely — different interventions, denominators; sign error dissolved it | **GAINED** (witness proved introspection cut C12: the paradox was a soothing story) |
| Q5 vertical consumer | re-scope to resurrection corpus, named consumer | "cost per successful resumed task" framing | **CONFIRMED-ALREADY-HAD** |
| Q7 diary-vs-memory | name the chain per reading; local-model logprobs feasible | W1 loader boundaries: growing-file check + death-checkpoint cutoff demanded | **GAINED (adjacent — concrete hardening we lacked)** |
| Blind retro A1–A4 | — | different commission (worldline, not maze) | **OPEN** — honest: not scored this run |

**WITNESS-WRONG rows: ZERO.** Rigorous throughout — recomputed, cited, hash-verified,
tolerances labeled as proposals. Per the law: no dissection warranted; the gain is real.

## THE GAINS (receipts of new capability — things we did not have)

1. **Sign error in our replay:** recorded `ppl = exp(mean_logprob)` is INVERSE perplexity
   (correct: exp(−mean)). Corrected: **+0.205% favoring the preload**, not −0.21% against.
   And fatal: at COLD ppl 1.0024, max possible improvement = **0.237% — the 3% threshold was
   mathematically unreachable.** The instrument could never have awarded its positive verdict.
2. **F-W5 stat demoted:** 112%/222% is an asymmetric ratio over matching-token subsets
   (12/48, 8/48 positions); absolute delta DECREASED in run 2 while the percentage doubled
   (denominator shrink). Cheapest falsifier fails: two entirely different outputs with equal
   logprobs → churn 1.0, delta 0 → "DECORATIVE." Absence of comparable positions ≠ absence of
   effect. Order-sensitivity: **Supported narrowly; Unproven as calibrated magnitude.**
3. **"Instrument paradox" dissolved:** not a contradiction — different interventions, tasks,
   denominators. Our §6 framing is DISPUTED; introspection cut C12 ("soothing story") is
   PROVEN.
4. **Honest economics:** 797× was premature-rounded; true prefill **813×**, whole-response
   **4.79×** — and the COLD arm benefits from caching too.
5. **Alignment bug:** offset-zero tokens skipped — "199/199" was 200 generated/199 scored.
6. **Receipt gap:** FOUR executions survive in tape rows 39/49/51/52, not "three passes
   append-only"; the initial marker-echo run is absent from the replay JSONL.
7. **W1 hardening demands (pre-row-320):** recompute historical hashes in the growing-file
   check; cut reconstruction at the seed's death checkpoint (post-death rows can enter).
8. **The row-320 bar:** L (uninterrupted) / R (restored) / C (cold) / S (sham) branches from
   frozen real checkpoints; hidden history-dependent acceptance checks; preregistered
   tolerances — R within **5pp of L**, **+10pp over C and S**, paired 95% CIs, zero critical
   violations, every failure published, cost per successful continuation. Plus the vLLM
   prompt-logprobs door for chosen-continuation scoring where weights are accessible.

## THE LAW'S OWN VERDICT

Prediction check: GAINED-on-theory as predicted; **wrong productively on engineering** — we
called Q2-class defects CONFIRMED-ALREADY-HAD and the witness found a sign bug, an alignment
bug, and a receipt gap inside them. Gain demonstrated: something we did not have, delivered.
The unattempted would have heard "your paradox is wrong" with no baseline to score it. The
seal made the delta attributable — including our own sign error, which the sealed assumption
pattern (declare, then measure) caught cleanly.
