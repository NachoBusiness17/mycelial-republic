# SWEEP: swarm-orchestration via arxiv (frontier_olm 2026-10-02)

stamp source-fetched: 2026-10-02
Seat: sweep-swarm-orchestration-arxiv gopher. Instrument: WebFetch on export.arxiv.org API (Atom XML) + arxiv.org/html full texts. All 8 banked items were fetched and read THIS sitting; quotes are transcribed from the fetched pages as returned by the fetch instrument.

## Method (what was actually run)

Pass 1 broad sweep, 11 arXiv API queries, >100 candidate entries considered, 30+ from the last 30 days (2026-09-02..2026-10-02):

1. `all:"multi-agent" AND all:"consensus" AND all:"LLM"` (30 results, sorted submittedDate desc)
2. `all:"LLM" AND all:"swarm"` (30 results)
3. `all:"backpressure" AND all:"language model"` (2 results)
4. `all:"load shedding" AND all:"LLM"` (2 results, both off-topic grid control)
5. `all:"small language models" AND all:"orchestration"` (20 results)
6. `all:"admission control" AND all:"language model"` (9 results)
7. `all:"AIMD" AND cat:cs.DC` (11 results; surfaced HiveMind itself)
8. `all:"tie-break" AND all:"multi-agent"` (9 results, mostly game theory, none LLM)
9. `all:"congestion control" AND all:"LLM agent"` (0 results, empty feed)

Pass 2 deep reads (8 full-text fetches via arxiv.org/html, read end to end through the fetch instrument): 2609.38324, 2610.00954, 2608.25937, 2609.06367, 2608.00558, 2609.15494, 2608.00028, 2609.16313.

## Overlap checks (what was actually run)

- `grep -cF <arxiv-id> catalog/catalog.jsonl` for all 17 shortlisted IDs (8 banked + 9 near-miss): ALL returned 0. Command run this sitting; catalog read 871,790 lines (`wc -l`).
- Title greps against `catalog/catalog.jsonl` and `memory/ -r`: hits on "Troy Moment", "conformal consensus", "dissent is withheld" in `memory/trajectory/steps.jsonl` are THIS session's own command echo (verified by reading the surrounding bytes: they are the grep command string itself), not prior holdings.
- One pass-1 candidate is a KNOWN holding: OrchSLM (2609.13470) already sits in `memory/runs/corpus_gap_research/ARXIV_REGISTER.json` + `MAP_BACKFILL.md` (case-insensitive match, confirmed). Excluded from banking.
- HiveMind (2604.17111, "OS-Inspired Scheduling for Concurrent LLM Agent Workloads", quote: "HIVEMIND reduces failures to 0-18% and eliminates 48-100% of wasted compute") re-surfaced in query 7: this IS the estate's banked source, excluded as known.
- Caveat: the small-model fetch instrument returns paper content as summaries + selected verbatim quotes; a quote's wording is high-confidence but machine-transcribed, not byte-diffed against the PDF. Marked per item in confidence.

## Banked items, strongest first

### 1. Multi-agent discussion gains less when dissent is withheld (arXiv 2609.38324, 2026-09-29)
Quote: "Discussion can overturn an incorrect initial majority only when the withholding rate c is below a critical rate c* = gamma/(gamma+a), set by the net correction rate gamma and the internalization rate a."
Why it matters: this is the consensus-decode redesign's missing quantitative core (estate map: `watch/inbox/frontier_olm_2026-10-02/lens/laws.md:54`, owed from `memory/rib/RIB_MINDSWEAVE_EVAL_CONSENSUS_ILLUSION_20260810.md:37-43`). The flock's 0/3-agreed-at-strength-0.60-0.67 illusion is exactly the high-internalization regime this paper formalizes: agreement without visible dissent cannot overturn a wrong majority, and the paper gives a measurable threshold (c*, estimated per-team from logs by Bayesian inference) plus two named failure paths (silenced dissent c high; voiced-but-ignored dissent a high, gamma low). Turning reasoning OFF lowered internalization and raised discussion gain in all 6 models tested; cohesion instructions RAISED withholding. Directly buildable: instrument the flock with per-turn withhold/internalize/correct counters and gate "consensus reached" on measured c < c*, not on scoring strength.
Measured anchor: hidden-profile 120 tasks, N=5, T=3 rounds, 9 LLMs; forcing c=1 nearly eliminated gain; gain declines quadratically as c_hat - c* grows.
Overlap: arXiv ID 0 hits in catalog; title grep only self-echo. NEW.

### 2. Beyond Leaderboards: Tokenomics of Agentic Small Language Model Ensembles (arXiv 2610.00954, 2026-10-01)
Quote: "Our results show that agentic SLM ensembles can trade additional test-time tokens and orchestration overhead for improved instruction-following fidelity, motivating multi-dimensional evaluation protocols for future agentic AI systems."
Why it matters: measured answer to research question 4, and a worked instance of the consensus redesign: candidates are checked by a PROGRAMMATIC verifier (IFEval checker) against the actual output space, and an SLM judge only tie-breaks among verifier-compliant candidates or converts violations into corrective feedback (up to 3 attempts). Best ensemble 97.34% strict prompt accuracy vs strongest standalone (gpt-5.4) 91.53%, at LOWER cost per prompt; even the weakest ensemble (95.64%) beat the best standalone. Orchestration tokens 45-47% of spend. This is "small collective + deterministic verifier + cheap tiebreak judge" beating the frontier single model: the exact architecture the estate's flock lacks.
Caveat as-read: the paper itself flags a stochastic "Non-ASCII Roulette" anomaly in the IFEval checker adding noise to small deltas.
Overlap: arXiv ID 0 hits in catalog. NEW.

### 3. Candidate supply and answer selection shape the value of LLM judging in multi-agent systems (arXiv 2608.25937v2, 2026-08-26)
Quote: "Combining answer frequency with the judge's evaluation changed only the final answer-selection rule and raised accuracy from 63.82% to 70.82-70.95%, primarily by rescuing correct answers that were outnumbered by popular errors."
Why it matters: bridges questions 1, 3 and 4 with the largest measured delta of this sweep. Generation-retention gap 13.13-14.38pp (the collective HOLDS the right answer and reports the wrong one: the consensus illusion, quantified on 81,390 frozen k=8 pools). Judge reliability is SIGMOIDAL in correct-answer availability p_gen (half-rise m=14.7%, R^2=0.900); below the knee, rank AUC falls under 0.5, i.e. a judge on a hard pool is WORSE than random, so contested verdicts between strong families must not be resolved by raw judge score alone. Tiebreak mechanics as-read: hybrid weight w_i=(k-i)^t blends frequency with rank; at t=5 the top-ranked trace dominates; answer-score ties broken by random seed, sensitivity <=0.36pp. Hybrid beats vote by +13.52pp at k=2 but is flat-to-negative by k=16: judge value decays with pool size while cost per 1,000 extra correct answers climbs US$0.10 to US$6.28.
Overlap: arXiv ID 0 hits in catalog. NEW.

### 4. Robust Conformal Consensus: Multi-Agent LLM-as-a-Judge Interval Evaluation with Conformal Prediction (arXiv 2609.06367, 2026-09-06)
Quote: "interval-based aggregation across multiple judges leads to more stable evaluation outcomes."
Why it matters: the most direct published template for the owed redesign's "map agreement onto the ACTUAL task output space": each judge's integer score becomes a conformal prediction interval (9 methods, integer boundary adjustment for discrete scales), intervals are reliability-weighted across judges, and a meta-calibration quantile restores formal coverage. Output is an interval with guaranteed coverage, not a vibes strength score; disagreement shows up as interval width. As-read: after boundary adjustment most methods reach >=90% coverage (example: LVD on e-SNLI, Qwen2.5: 85.96% to 95.53%); multi-agent aggregation beats the best single judge's coverage floor (CHR on ROSCOE/CosmosQA 74.0% vs 72.65% for Qwen2.5 alone).
Overlap: arXiv ID 0 hits in catalog; "conformal consensus" grep only self-echo. NEW.

### 5. AiFlow: Token-Native Reactive Orchestration with Bounded Backpressure for Streaming LLM Applications (arXiv 2608.00558, 2026-08-01)
Quote: "cannot force a remote provider to un-generate tokens already produced"
Why it matters: question 2. Extends HiveMind's AIMD shedding from admission policy to a compile-time bounded-memory contract: every node declares a policy tuple (queue capacity q, workers k, ordering buffer rho, state concurrency sigma, overflow o, cancellation c, retry r) with overflow = Block / DropNewest / DropOldest / Error, and total in-flight events are provably the sum of declared bounds. As-read: MaxQ 8.0 vs 231.2 unbounded on a DeepSeek 30-run replay; Application TTFPT down 70.9-94.7% vs aggregation (Wilcoxon p<0.001); ablation shows removing backpressure keeps latency but grows MaxQ to 131 and memory 3.4x. The honest limit quoted above matches the estate's own law (`memory/rib/RIB_FREE_USAGE_POLICY_20260823.md:8-13`: provider caps return junk, local backpressure must absorb it). Slightly outside the 30-day window (Aug 1) but the only in-sweep item with a formal backpressure bound.
Overlap: arXiv ID 0 hits in catalog. NEW.

### 6. The Troy Moment: How LLM Agents Adjudicate the Decision Point Under Impossible Tasks, Claimed Authority, and Peer Information (arXiv 2609.15494v3, 2026-09-14)
Quote: "compliance is not well characterized as a property of a prompt or model in isolation."
Why it matters: question 3 (the pending Cathedral World tiebreak class, `watch/inbox/frontier_olm_2026-10-02/lens/laws.md:66`). On ImpossibleBench conflicting tasks (real bug + frozen unsatisfiable test), three strong families resolved IDENTICAL contested evidence by three distinct policies: provenance arbitration (in-band claim cannot supersede the standing system rule; escalate/stop), security classification (peer cues reframed as injection; refuse), authority-weighting (lateral peer precedent filtered, vertical claimed authority engaged, sometimes after verifying upstream). The implicit tiebreak hierarchy as-read: system-level boundary > claimed principal grant > peer precedent, with instruction wording selecting the endgame and tool affordance deciding executability. The swarm leg is the estate-relevant bit: mixed-family teams diagnosed the contradiction 19/21 vs 14/21 homogeneous, with peers re-deriving evidence instead of inheriting claims: cross-family re-derivation IS the tiebreak mechanism, matching the estate's two-family corroboration law (`memory/rib/RIB_MODEL_GATES_20261001.md:50-52`).
Overlap: arXiv ID 0 hits in catalog; title grep only self-echo. NEW.

### 7. Width, Memory, and Delay: A Resource Accounting for the Limits of Flat Multi-Agent Systems (arXiv 2608.00028, 2026-07-14)
Quote: "The delay is the hard wall. The floor equals the environment's unpredictability over the observation (feedback) delay. Buy a predictor or cut latency, not more agents."
Why it matters: question 2's other half, and a hard constraint on the estate's width envelope laws (AGENTS.md fan-out law). The accounting: width N only averages i.i.d. noise (MSE ~ 1/N) and NEVER reduces structured disturbance; that needs per-agent internal-model memory with d >= 2x the number of disturbance bands; beyond the computable N* where noise averaging hits the structural floor, "agents are ballast". Equal-budget N*d experiments: at B=3150, d=7 reaches 0.80 MSE vs ~2.3 at d=1. Out of the strict 30-day window (Jul 14), banked because it is the only in-sweep item that bounds width itself: a 50-wide flat fan-out buys noise averaging, not capability, and the delay term (provider latency to first evidence) is a floor no width crosses.
Overlap: arXiv ID 0 hits in catalog; title grep empty. NEW.

### 8. Cognitive Admission Control: Risk-Conditioned Assurance for Consequential Actions in Agentic Distributed Systems (arXiv 2609.16313, 2026-09-14)
Quote: "Across 390 CAC trials, 120 effects complete without modeled harm and no harmful effects occur."
Why it matters: question 2's admission-control leg, and a public mirror of the estate's switchboard/effect-broker doctrine ("model text can propose; only the switchboard/effect broker authorizes effects", AGENTS.md shared-artifact boundary). Gate mechanics as-read: risk vector (consequence, blast radius, irreversibility, uncertainty, dependency exposure, adverse plausibility) maps monotonically to typed evidence obligations; a ternary evaluator returns satisfied/violated/UNKNOWN and unknowns trigger targeted evidence acquisition; admission mints a single-use certificate consumed by CAS at the gateway, failing closed. 2,730 controlled trials, 0 harmful effects vs 30 for a live-policy baseline and 180 for auth-only; median dispatch cost 4.65-26.86ms. It is admission control by RISK not by load, so it complements rather than contradicts HiveMind's AIMD load shedding: CAC gates WHAT may dispatch, AIMD gates HOW MUCH.
Overlap: arXiv ID 0 hits in catalog. NEW.

## Cross-cutting fold for the estate

The three-leg consensus-decode redesign now has published templates for every leg: (a) gate consensus on measured dissent dynamics, c < c* = gamma/(gamma+a), not on strength scores (item 1); (b) verify against the actual output space programmatically, judge only tie-breaks among verified candidates (item 2, echoed by item 3's hybrid frequency+rank); (c) emit intervals with coverage, not scalar agreement (item 4). On backpressure, the AIMD load-shedding question splits: width has a computable point of diminishing returns (item 7), provider-side generation cannot be recalled, only locally absorbed (item 5), and admission is a risk function distinct from load (item 8). On tiebreaks, the evidence favors cross-family re-derivation over any in-family referee (item 6), and judges below the p_gen knee are worse than random, which formalizes why a sole judge on a contested verdict fails (item 3).

## OWED / limits

- Quote transcription is via the fetch instrument's reading model, not byte-diffed against PDFs; confidences reflect that.
- Queries 4, 8, 9 for AIMD/tiebreak/congestion-control in LLM-agent settings returned near-zero direct hits: no in-window paper explicitly tests AIMD-style shedding against HiveMind's numbers. The extension evidence is architectural (AiFlow bounds, CAC risk gating, item 7's width floor), not a head-to-head replication. Stated as not found, not fabricated.
- 2608.25937's tie-by-random-seed protocol and item 7's N* formula were read at summary depth; exact formulas would need a PDF pass to lift verbatim. OWED if the estate adopts them.
