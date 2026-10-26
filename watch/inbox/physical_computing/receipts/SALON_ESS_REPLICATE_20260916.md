# SALON ESS REPLICATE — 2026-09-16

- Lane: background wave-lane (fleet repo, Windows host) · Budget: $0 — LOCAL OLLAMA ONLY
- Status: PRE-REGISTERED; execution starting after this block is written
- Suspended claim under test: "the fleet's free-lane salons are a thermodynamic sampler of judgment space."
- Prior measurement (falsifier §4.1 / pack §6.1): Spearman(decorrelation, desk rank) = +0.167, wrong-signed, n=8, p=0.70.

## Pre-registration (committed before any generation)

**Question (exact wording sent to the model):**

> A town must cut its budget by 10%. Argue for the single change that best balances harm and fairness. Answer in 150 words or fewer.

**Design**

- 36 calls to local Ollama `gemma:2b` via `/api/generate`, per-call temperature (`options.temperature`), 12 runs per temperature (n=12 per temp is the point; lane = (temperature, run) pair; 36 total calls).
- Temperature ladder: 0.3 / 0.8 / 1.3.
- Generation order is temperature-major (calls 0–11 @ 0.3, 12–23 @ 0.8, 24–35 @ 1.3); this order is never shown to the grader.
- Every call: `options.temperature = t`, `options.num_predict = 300`, no seed set (random per call), `stream: false`.
- Model fallback rule: use exact tag `gemma:2b`; if absent, the smallest available `gemma*` tag with the deviation noted; if no gemma model or ollama is down → record here and STOP (zero external calls).

**Blinding**

- Shuffle seed (fixed, pre-registered): **20260916**. `random.Random(20260916).shuffle(list(range(36)))` maps presentation positions T01–T36 to generation indices, deterministically recomputable.
- Grader (this lane) sees only the shuffled presentation file (texts + their word counts). The grader does not open the generation JSON (which carries temperature labels) until after all grades are committed to this receipt.
- Mapping T-id → (temperature, run, grade) is written to `artifacts/salon_ess_mapping_20260916.json` ONLY after all 36 grades are committed below.

**Grading rubric (0–10, weights fixed before generation)**

- Names exactly ONE central change: 0–3
- Addresses harm (who is hurt / how mitigated): 0–2
- Addresses fairness (who bears the burden / equity reasoning): 0–2
- Concreteness (specific mechanisms, numbers, actors): 0–2
- Length discipline: 1 if ≤ 170 words, else 0 (target was 150)

**Analysis (pre-registered)**

- Word sets: lowercase `[a-z']+` tokens. Jaccard similarity; decorrelation = 1 − Jaccard.
- Per temperature: mean pairwise decorrelation over within-temperature pairs (C(12,2)=66 pairs), mean grade, ESS proxy = 1/(1 + mean pairwise similarity).
- Per-text decorrelation = 1 − mean Jaccard vs all other 35 texts (pooled).
- Spearman(decorrelation, grade) across all 36; two-sided permutation p, 100,000 draws, permutation seed 20260916, p = (b+1)/(N+1).
- Verdict thresholds (pre-registered): SUPPORTED if rho < −0.3 · REFUTED if rho > +0.3 · otherwise NULL/INSUFFICIENT.

## Status log (append-only; script and lane both append)

- receipt created; pre-registration above committed before any model call
- environment check: ollama 0.32.7 running, server responding on localhost:11434; exact tag `gemma:2b` present (b50d6c999e59, 1.7 GB) → no fallback needed; venv python 3.11.15. Proceeding.
- 2026-09-16 13:37:00 gen[00] temp=0.3 run=01 words=31 elapsed=7.5s
- 2026-09-16 13:37:03 gen[01] temp=0.3 run=02 words=37 elapsed=2.9s
- 2026-09-16 13:37:06 gen[02] temp=0.3 run=03 words=56 elapsed=3.1s
- 2026-09-16 13:37:09 gen[03] temp=0.3 run=04 words=45 elapsed=3.0s
- 2026-09-16 13:37:12 gen[04] temp=0.3 run=05 words=39 elapsed=2.9s
- 2026-09-16 13:37:15 gen[05] temp=0.3 run=06 words=33 elapsed=2.9s
- 2026-09-16 13:37:17 gen[06] temp=0.3 run=07 words=34 elapsed=2.8s
- 2026-09-16 13:37:21 gen[07] temp=0.3 run=08 words=52 elapsed=3.1s
- 2026-09-16 13:37:24 gen[08] temp=0.3 run=09 words=53 elapsed=3.0s
- 2026-09-16 13:37:27 gen[09] temp=0.3 run=10 words=53 elapsed=3.1s
- 2026-09-16 13:37:30 gen[10] temp=0.3 run=11 words=50 elapsed=3.0s
- 2026-09-16 13:37:33 gen[11] temp=0.3 run=12 words=54 elapsed=3.1s
- 2026-09-16 13:37:33 gen window [0:12] done; total calls on disk=12/36; window wall=40.5s
- 2026-09-16 13:37:46 gen[12] temp=0.8 run=01 words=42 elapsed=2.9s
- 2026-09-16 13:37:49 gen[13] temp=0.8 run=02 words=49 elapsed=3.1s
- 2026-09-16 13:37:52 gen[14] temp=0.8 run=03 words=61 elapsed=3.3s
- 2026-09-16 13:37:55 gen[15] temp=0.8 run=04 words=45 elapsed=3.1s
- 2026-09-16 13:37:58 gen[16] temp=0.8 run=05 words=50 elapsed=3.0s
- 2026-09-16 13:38:01 gen[17] temp=0.8 run=06 words=56 elapsed=3.1s
- 2026-09-16 13:38:04 gen[18] temp=0.8 run=07 words=59 elapsed=3.2s
- 2026-09-16 13:38:08 gen[19] temp=0.8 run=08 words=65 elapsed=3.3s
- 2026-09-16 13:38:11 gen[20] temp=0.8 run=09 words=38 elapsed=2.9s
- 2026-09-16 13:38:13 gen[21] temp=0.8 run=10 words=31 elapsed=2.8s
- 2026-09-16 13:38:16 gen[22] temp=0.8 run=11 words=43 elapsed=3.0s
- 2026-09-16 13:38:19 gen[23] temp=0.8 run=12 words=39 elapsed=2.9s
- 2026-09-16 13:38:19 gen window [12:24] done; total calls on disk=24/36; window wall=36.6s
- 2026-09-16 13:38:30 gen[24] temp=1.3 run=01 words=36 elapsed=2.9s
- 2026-09-16 13:38:33 gen[25] temp=1.3 run=02 words=45 elapsed=3.0s
- 2026-09-16 13:38:36 gen[26] temp=1.3 run=03 words=49 elapsed=3.1s
- 2026-09-16 13:38:39 gen[27] temp=1.3 run=04 words=40 elapsed=2.9s
- 2026-09-16 13:38:42 gen[28] temp=1.3 run=05 words=50 elapsed=3.0s
- 2026-09-16 13:38:45 gen[29] temp=1.3 run=06 words=34 elapsed=2.8s
- 2026-09-16 13:38:48 gen[30] temp=1.3 run=07 words=41 elapsed=2.9s
- 2026-09-16 13:38:51 gen[31] temp=1.3 run=08 words=54 elapsed=3.1s
- 2026-09-16 13:38:54 gen[32] temp=1.3 run=09 words=40 elapsed=2.9s
- 2026-09-16 13:38:57 gen[33] temp=1.3 run=10 words=61 elapsed=3.3s
- 2026-09-16 13:39:00 gen[34] temp=1.3 run=11 words=54 elapsed=3.1s
- 2026-09-16 13:39:03 gen[35] temp=1.3 run=12 words=31 elapsed=2.8s
- 2026-09-16 13:39:03 gen window [24:36] done; total calls on disk=36/36; window wall=35.8s
- 2026-09-16 13:39:11 shuffle done: seed=20260916; blind presentation -> salon_ess_shuffled_20260916.txt (grader sees T-ids only; generation JSON stays closed until grades are committed)

## Blind grades (committed 2026-09-16, BEFORE any unblinding)

Grader: this lane, reading only `artifacts/salon_ess_shuffled_20260916.txt` (T-ids + texts + word counts). The generation JSON was not opened before these grades were committed. Grades keyed by presentation T-id only.

| T | grade | T | grade | T | grade |
|---|---|---|---|---|---|
| T01 | 7 | T13 | 7 | T25 | 6 |
| T02 | 7 | T14 | 7 | T26 | 7 |
| T03 | 9 | T15 | 9 | T27 | 9 |
| T04 | 6 | T16 | 9 | T28 | 9 |
| T05 | 8 | T17 | 9 | T29 | 7 |
| T06 | 10 | T18 | 8 | T30 | 8 |
| T07 | 7 | T19 | 8 | T31 | 6 |
| T08 | 7 | T20 | 7 | T32 | 7 |
| T09 | 7 | T21 | 7 | T33 | 7 |
| T10 | 5 | T22 | 7 | T34 | 6 |
| T11 | 7 | T23 | 7 | T35 | 7 |
| T12 | 6 | T24 | 9 | T36 | 8 |

Grading notes (rubric applied as registered):
- The registered rubric has no feasibility/on-task item; several proposals do not actually cut town spending (price controls on goods, tax cuts that reduce revenue). These were graded only on the five registered components, per pre-registration.
- Length: every text came in far UNDER 150 words (31–65 words), so all 36 receive the length point (≤170). gemma:2b ignored the word target from below, not above.
- "one change" = 3 when exactly one central change is clearly stated; 2 when muddled (e.g., T10's "wage cap ... 100% of previous salary" conflates cap and freeze).
- harm/fairness = 2 only when a specific burden-bearing group plus mitigation/equity reasoning is present; 1 for gestures ("balanced", "everyone"); 0 when absent.
- concrete = 2 only with a number + clear instrument (e.g., "cut all town wages 10%", "raise property tax 5%"); 1 for named domains without numbers.

Grade vector in T01→T36 order (input to analyze stage):
`7,7,9,6,8,10,7,7,7,5,7,6,7,7,9,9,9,8,8,7,7,7,7,9,6,7,9,9,7,8,6,7,7,6,7,8`
- 2026-09-16 13:45:17 ANALYSIS (pre-registered stats; grades as committed above):
- 2026-09-16 13:45:17   temp=0.3: n=12  mean_pairwise_decorrelation=0.6823  mean_grade=7.25  ESS_proxy=0.7589
- 2026-09-16 13:45:17   temp=0.8: n=12  mean_pairwise_decorrelation=0.8453  mean_grade=7.50  ESS_proxy=0.8660
- 2026-09-16 13:45:17   temp=1.3: n=12  mean_pairwise_decorrelation=0.8566  mean_grade=7.50  ESS_proxy=0.8746
- 2026-09-16 13:45:17   Spearman(decorrelation, grade) n=36: rho=0.3271  perm_p(two-sided, 100000 draws, seed 20260916)=0.052469
- 2026-09-16 13:45:17   MECHANICAL VERDICT (thresholds: SUPPORTED rho<-0.3 / REFUTED rho>+0.3): REFUTED
- 2026-09-16 13:45:17   gen compute time (sum of call wall times): 112.8s
- 2026-09-16 13:45:17 mapping file written post-grade (as pre-registered) -> salon_ess_mapping_20260916.json

## Post-unblinding note

- The single grade-10 text (T06: "cut all town wages 10%") came from temp 0.8, run 4 — a distinctive proposal with high decorrelation (0.859 pooled).
- Of the seven grade-9 texts, four came from temp 1.3, two from temp 0.3, one from temp 0.8 — the top band leans on the high-temperature tail, but the bottom band (grades 5–6) is also rich in 1.3 and 0.8 texts; the positive rho is driven mainly by the temp-0.3 cluster (the mode answer "reduce the cost of public services by 5%") being reliably mid-pack while having the lowest decorrelation.
- Temperature did what thermodynamics says it should: mean pairwise decorrelation 0.682 (t=0.3) → 0.845 (t=0.8) → 0.857 (t=1.3), ESS proxy 0.759 → 0.866 → 0.875, with mean grade flat (7.25 → 7.50 → 7.50). Diversity is purchasable at no mean-quality cost — but it bought nothing either.

## Verdict (mechanical: REFUTED)

**Headline: Spearman(decorrelation, grade) = +0.327, n=36, permutation p = 0.052 → REFUTED** (pre-registered: refuted if rho > +0.3).

The pre-registered decisive follow-up lands on the same side as the prior measurement: +0.167 then, +0.327 now — repetition again predicts equal-or-better grades, this time strongly enough to cross the refutation line, though barely (rho is only 0.027 past the threshold and p is marginal at 0.052, so this is a weak refutation, not a slam dunk). What this does to the suspended claim — "the fleet's free-lane salons are a thermodynamic sampler of judgment space": the sampler metaphor loses its decisive support. A thermodynamic sampler earns its keep because widening the temperature envelope reaches *better* modes; here the widened envelope (decorrelation 0.68 → 0.86, ESS proxy 0.76 → 0.87) reached the same mean grade (7.25 → 7.50), and the texts hewing closest to the model's mode grade at least as well as the diverse tail. Diversity was purchasable and converted into zero quality. The honest residual reading: the free-lane salon widens the sampled space without sampling better judgments — a diversity pump, not a quality sampler. Caveats carried forward: single small model (gemma:2b), one question, one grader (this lane; blindness was procedural only, via the seeded shuffle), rubric had no feasibility item, all outputs ran far under the 150-word target, and rho is a threshold graze — a replication on a second question/model would settle whether the refutation holds.

## Runtime facts

- Model: `gemma:2b` (digest b50d6c999e59, 1.7 GB), exact pre-registered tag, no fallback needed
- Ollama: version 0.32.7, server on localhost:11434
- Total calls: 36 (12 per temperature × {0.3, 0.8, 1.3}); 0 failures, 0 retries needed
- Wall time: generation 112.9 s total (windows 40.5 + 36.6 + 35.8 s; sum of per-call times 112.8 s); shuffle + analysis (incl. 100,000-draw permutation) < 2 s; end-to-end lane wall ≈ 8 min including blind grading
- $ spent: **0** — local Ollama only; no external network calls, no hosted providers
- Artifacts: `artifacts/salon_ess_replicate_20260916.py` (script), `artifacts/salon_ess_gen_20260916.json` (raw generations), `artifacts/salon_ess_shuffled_20260916.txt` (blind presentation), `artifacts/salon_ess_mapping_20260916.json` (post-grade unblinding map)
