# Q-020 / FW-05 — Sampler closure receipt: SALON_ESS_REPLICATE formalized CONDITIONAL-REFUTED → REFUTED-ON-REPLICATE

- Date: 2026-09-28 · seat: queue-gopher2-Q-020 (workflow gopher) · cost: $0 (paperwork over already-run data; no model calls)
- Plan: `memory/plans/fifty_wide_20260917.md:16`
- The owed closure per `memory/continuity/seat_memory_20260927/salon-ess-refuted-conditional.md:20`: "one formal closure receipt with the threshold provenance and variable definitions filed together — then the word 'refuted' is earned." This is that receipt.

## Closure verdict (the formalized wording)

**REFUTED-ON-REPLICATE.** The claim "the fleet's free-lane salons are a thermodynamic sampler of judgment space" is refuted by its own pre-registered replicate arm — not "conditionally" refuted. The condition that held the word back (closure paperwork with threshold provenance + variable definitions filed together) is satisfied by this document; the pre-registered threshold was crossed by the data on 2026-09-16 and never un-crossed. Scope is carried in the word itself: refuted-on-replicate = refuted on this arm (36 trials, gemma:2b, one question, one blind-by-shuffle grader), with the receipt's own caveats attached (below) — it is a scoped refutation, not a universe-wide one.

## Threshold provenance (registered before the data)

- Registered in the pre-registration block of `watch/inbox/physical_computing/receipts/SALON_ESS_REPLICATE_20260916.md` ("Pre-registration (committed before any generation)"), declared before the first model call, and executed by the script's mechanical rule at `artifacts/salon_ess_replicate_20260916.py:210-215`: **SUPPORTED if rho < −0.3 · REFUTED if rho > +0.3 · otherwise NULL/INSUFFICIENT**. The script's analyze stage prints the verdict mechanically — the lane cannot hand-grade the threshold.
- Ordering evidence: the receipt's append-only status log shows pre-registration → environment check → gen[00] at 13:37:00 → … → gen[35] 13:39:03 → shuffle → grades committed → ANALYSIS at 13:45:17 ("pre-registered stats; grades as committed above"). Blindness was procedural: grader saw only the seeded-shuffle presentation (`artifacts/salon_ess_shuffled_20260916.txt`, shuffle seed 20260916); the mapping file was written LAST (`artifacts/salon_ess_mapping_20260916.json`).
- Honest note on the commit record: the script + receipt + data all landed in one checkpoint (`0f34a8f3e`, 2026-09-16 18:50:28 -0400, message itself says "sampler claim REFUTED by pre-registered replicate"), so the git history alone does not prove the ordering — the append-only receipt log is the ordering instrument, and that is what this provenance section rests on.

## Variable definitions (filed together with the threshold, as owed)

- n = 36 = 12 runs × 3 temperatures {0.3, 0.8, 1.3}, local Ollama `gemma:2b` (digest b50d6c999e59), one question (the 10%-budget cut), `num_predict` 300, 0 failed calls, $0 spent.
- Decorrelation of text i = 1 − mean Jaccard(word-set(i), word-set(j)) over the other 35 texts, word-sets = lowercase `[a-z']+` tokens.
- Grade = the grader's 0–10 rubric score (one-change 0-3 / harm 0-2 / fairness 0-2 / concrete 0-2 / length 1 if ≤170 words), joined back to (temp, run) via the seeded shuffle map only after all 36 grades were committed.
- rho = Spearman rank correlation between the 36 decorrelations and the 36 grades; p = two-sided exact-threshold permutation test, 100,000 draws, permutation seed 20260916, p = (b+1)/(N+1).

## The measurement (never re-computed by hand; read from the run's own artifacts)

- `artifacts/salon_ess_mapping_20260916.json`: `verdict: "REFUTED", rho: 0.32713353953033314, p: 0.05246947530524695, n: 36 mapping rows, model: gemma:2b` — read this session.
- Receipt analysis lines (2026-09-16 13:45:17): `Spearman(decorrelation, grade) n=36: rho=0.3271 perm_p(two-sided, 100000 draws, seed 20260916)=0.052469` → `MECHANICAL VERDICT …: REFUTED`.
- The replicate landed on the same side as the prior n=8 probe (+0.167): repetition again predicted equal-or-better grades. This time it crossed the kill line — by 0.027, at marginal p=0.052. The receipt's own characterization stands: a weak refutation by the pre-registered rule, not a slam dunk; the rule is the rule.

## Caveats carried forward (from the receipt's post-unblinding note, not softened here)

Single small model (gemma:2b); one question; one grader (this lane; blindness procedural only, via the seeded shuffle); rubric had no feasibility item; all outputs ran far under the 150-word target; rho is a threshold graze. A second-question/second-model replication remains the open settle-it move — absence of that replication is why the wording is REFUTED-ON-REPLICATE (scoped) rather than a bare universal REFUTED.

## Standing surfaces updated by this closure

- `memory/continuity/seat_memory_20260927/salon-ess-refuted-conditional.md` — closure addendum appended (the CONDITIONAL-REFUTED body preserved untouched, never rewritten); its status line now points here.
- `memory/continuity/seat_memory_20260927/MEMORY.md` index line for the memo — flipped from "CONDITIONAL pending closure receipt" to closed-with-pointer.
- Left untouched (frozen records of their own nights): `watch/inbox/THE_SESSION_RECORD_20260916.md:36`, `watch/inbox/wave_20260916/receipts/WARM_START_20260916.md:18` — the closure receipt supersedes them by pointer, not by edit.
