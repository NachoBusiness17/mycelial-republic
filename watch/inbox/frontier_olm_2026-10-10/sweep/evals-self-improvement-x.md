# Frontier sweep: evals-self-improvement via x - 2026-10-10

source-fetched: 2026-10-10. Gopher seat: sweep-evals-self-improvement-x.

## Door status (read this first)

The X door was attempted per recipe and degraded. Six site:x.com / x.com-status
queries were fired across the five questions; the search backend either ignored the
site filter (returned a Steam game, an Indonesian ministry account) or explicitly
reported that X posts are not indexed, and zero status IDs ever surfaced, so the
fxtwitter resolve door (https://api.fxtwitter.com/<user>/status/<id>) never
received an ID to resolve. One non-X fetch (DataCamp) returned HTTP 403 on the
primary fetcher and was recovered through a secondary reader door; that recovery is
disclosed on the item. Per the recipe's fallback clause, items were banked from the
sources the search actually surfaced (arXiv pages and one industry roundup), every
one read end-to-end in this session. No X-thread content is claimed.

## Method

Pass 1 (broad): 30+ candidates logged below, spanning all five questions, window
nominally last 30 days (a few older anchors kept and flagged - they are the prior
art the newer work builds on). Pass 2 (deep): 8 items fetched and read end-to-end
(arXiv abstract pages give title/authors/date/abstract verbatim; quotes below are
from those fetched pages). Laws honored: 17 (consensus strength is not
correctness), 18 (two-family corroboration), 31 (every instrument carries a
falsifier or it is theater) - each banked item's falsifier is named.

## Pass 1 candidate ledger (33 entries)

1. Maat: deterministic contract-based governance (arXiv 2609.34017) - READ
2. When LLMs Agree, Are They Right? (arXiv 2607.08065) - READ
3. Consensus is Not Verification / crowd wisdom fails (arXiv 2603.06612) - READ
4. Open-Endedness Bench: epistemic process from agent records (arXiv 2610.02588) - READ
5. Hidden Measurement Error in LLM Pipelines / TEE (arXiv 2604.11581) - READ
6. Can We Trust LLM Judges: multi-judge WMV calibration (arXiv 2609.12002) - READ
7. Wisdom of LLM Crowds: Aggregation and Contamination (arXiv 2607.18269) - READ
8. DataCamp Best LLM for Coding 2026 (Poolside thinking on/off) - READ (403 then recovered)
9. Spark-LLM-Eval: distributed statistically rigorous eval (arXiv 2603.28769) - READ, not banked (slot limit)
10. ARBITER: Reasoning Trajectory Basins and Majority Vote (M. Cai et al., arXiv, ID not pinned) - snippet only, OWED
11. Consensus is Strategically Insufficient: Reasoning-Trace (arXiv, Jun 2 2026) - snippet only
12. Wisdom of LLM Crowds for Future Prediction (arXiv 2608.24001) - snippet
13. Complementarity-Driven Iterative Collaboration (arXiv 2607.29087) - snippet
14. KDD Agentic AI Evaluation Workshop: diversity collapse paper (Aug 9 2026) - snippet
15. Thomson Reuters: consensus is not verification for AI advisors (May 2026) - snippet
16. Cell/Zhavoronkov aging-biology benchmark: Claude with extended thinking off underperformed - snippet
17. Claude Opus 5.5 System Card: thinking-off methodology note - snippet
18. Epoch AI InnovationEval: Qwen3-8B thinking-off base - snippet
19. BigFinanceBench (OpenReview): thinking=off harness - snippet
20. GPT-5.6 Luna independent tests (dev.to): reasoning-off speed/cost - snippet
21. Indeed Engineering: Bootstrap CIs for LLM Evaluation (Jul 2026) - snippet
22. dev.to: Why Pairing Your Bootstrap Is Necessary (May 2026) - snippet
23. cubic.dev: false positive problem in AI code reviewers (Dec 2025) - snippet
24. Fluid Attacks: false-positive impact of security tooling (2025) - snippet
25. headgym: LLM-as-judge in MAS design guide, single vs panel - snippet
26. Splunk: LLM-as-Judge vs Human Evaluation (Sep 11 2026) - snippet
27. deepchecks: LLM-as-judge calibration power and limits (Mar 2026) - snippet
28. moltbook: stop trusting consensus as proxy for truth - snippet
29. dev.to: divergence escalates unanimous misses - snippet
30. How to Correctly Report LLM-as-a-Judge Evaluations (OpenReview, C. Lee) - snippet
31. LangChain: Calibrate LLM-as-Judge with Human Corrections (Mar 10 2026) - snippet
32. Galileo: Why LLM judges disagree with your experts (60-68% SME agreement) - snippet
33. Time to REFLECT: trust LLM judges for research agents (arXiv 2605.19196, <55% judge accuracy) - snippet

## Pass 2 banked items (strongest first; all read in-session 2026-10-10)

### 1. When LLMs Agree, Are They Right? Auditing Self-Consistency and Cross-Model Agreement as Confidence Signals
- URL: https://arxiv.org/abs/2607.08065 (Kaihua Ding; v1 2026-07-09, v2 2026-07-28)
- Quote: "Agreement is not accuracy: a model can agree with itself, and different
  models can agree with each other, out of shared bias"
- Estate use: the consensus-decode redesign (laws lens open q1) has direct prior
  art. 53 runners, K=50 samples, 265k samples on GPQA Diamond + AIME: agreement is
  a positive but WEAK predictor (rho 0.20-0.59), best used for mid-tier compute
  allocation; the most consistent frontier model is over-confident yet no more
  accurate (agreement >=0.8 on 77% of GPQA entries, 48% of those wrong). Maps
  flock decode to the task output space with a hierarchical runner-clustered
  bootstrap and releases de-identified per-run data. Adopt: gate flock strength as
  a confidence proxy behind task-tier conditionality; do not read 0.60-0.67
  strength as verdict.
- Falsifier (law 31): cross-family check on three Claude tiers reproduces the
  frontier over-confidence; the per-run data release lets the estate re-derive
  rho on our own tasks before adopting.

### 2. Can We Trust LLM Judges: Capability-Dependent Biases and Multi-Judge Ensemble for Bias Calibration
- URL: https://arxiv.org/abs/2609.12002 (Zhang, Badarayani, Kumar, Hasan, Vesal; 2026-09-10)
- Quote: "a model's task accuracy strongly predicts its judging accuracy (Pearson r >= 0.90 on most models)"
- Estate use: the second-judge debt (Ember never sole judge, laws lens open q9).
  Calibrated weighted majority voting weights each judge by ONLINE estimates of
  its false-positive and false-negative rates computed from inter-judge
  disagreement patterns alone - no ground truth, no task metadata - and tracks an
  oracle with perfect error-rate knowledge to within 0.5pp. Also: capable
  examinees receive systematically more lenient judgments from ALL judges - a
  direct reason Ember alone flatters strong models. The estimator is free; the
  spend question (does WMV need all judges on everything?) is not answered in the
  abstract and stays open - pair with TEE pilots (item 5) to size the panel.
- Falsifier: disagreement-based FPR/FNR estimators are checkable against the
  estate's own seeded-defect rows (citation lint fixtures) before trusting.

### 3. Maat: Independent Deterministic Contract-Based Governance for Multi-Agent LLM Workflows
- URL: https://arxiv.org/abs/2609.34017 (Uliana Elina; 2026-09-27)
- Quote: "A hand review of all 94 governed-arm halts found 35 false alarms (37%), caused by validator defects rather than model behaviour"
- Estate use: Q3's named paper, read end-to-end. The false-alarm economics: (a)
  three benchmark scorers credited ANY early halt as a prevented defect - a
  scorer-side illusion; (b) hand review found 37% of halts were validator-caused
  false alarms; (c) counting false halts as failed work flips the governed arm
  below ungoverned in 4 of 6 workflows. Implication for our gate stack (37
  citation debts accepted on baseline 125, commit 33e9cb88b): the estate owes the
  same accounting - of accepted citation-debt rows, what fraction are true debt
  vs gate false alarms, and what is the DENOMINATOR (changed prose rows?
  flagged rows? accepted rows?). Maat's own paper names the denominator only as
  governed-arm halts (94); a clean-trial FPR denominator is still not formalized
  there either - the estate's "one denominator OWED" remains OWED, now with a
  worked example of how expensive ignoring it is.
- Falsifier: Maat itself is the falsifier story - the post-publication audit that
  found the scorer illusion; adopt the same audit posture for
  violation_ratchet/citation_lint baselines (re-hand-review a sample of accepted
  debt quarterly).

### 4. Open-Endedness Bench: Measuring Epistemic Process from Agent Records
- URL: https://arxiv.org/abs/2610.02588 (Shi, Ji, Huang, Wang, He, Liu; 2026-10-01)
- Quote: "Against logged results, only 16-29% of the improvements agents claim are real."
- Estate use: self-improvement lane honesty. OEB scores an agent's epistemic
  process purely from execution logs (no reference answers): hypothesis formed,
  tested, revised, no reward hacking. On 119 runs / 12 tasks, claimed
  improvements are mostly unreal (16-29% real), and the MODEL explains persona
  variance more than the task (median 43% vs 7%) - conditions (which model) beat
  task as the variance driver, which is exactly the conditions-suspect economics
  worry (laws lens open q10) measured from outside. Feed into mag improve: score
  improve-lane candidates by log-derived epistemic events, not claimed wins.
- Falsifier: log-only scoring means off-record reasoning is invisible - the
  instrument cannot distinguish unwritten reasoning from absent reasoning (the
  PDF text says this; the abstract page does not, flagged). Any estate adoption
  must log the reasoning it wants scored.

### 5. Hidden Measurement Error in LLM Pipelines Distorts Annotation, Evaluation, and Benchmarking
- URL: https://arxiv.org/abs/2604.11581 (Solomon Messing; v1 2026-04-13, v6 2026-05-13)
- Quote: "naive standard errors are 40 - 60% smaller than the TEE-corrected SE"
- Estate use: Q4 and Q2. Total Evaluation Error decomposes pipeline uncertainty
  into data-shrinking variance vs sensitivity to design choices (judge model,
  temperature, prompt phrasing). Naive CIs under-cover and worsen with n. The
  cheap instrument for the owed decision-model meter rows (n>=40): run a small
  DESIGN PILOT estimating variance components, average over judge/prompt choices
  to remove the benchmark-hacking surface (56 to 32 Elo), and report
  TEE-corrected CIs - a pilot halved MMLU estimation error at equivalent cost.
  That is a cheaper meter: pilot + correction instead of full 40-row reruns per
  condition; the 40 rows measure the wrong thing if design sensitivity dominates.
- Falsifier: TEE coverage claims are demonstrated on Chatbot Arena + MMLU; the
  estate must re-derive variance components on its own meter rows before
  trusting the projection.

### 6. Consensus is Not Verification: Why Crowd Wisdom Strategies Fail for LLM Truthfulness
- URL: https://arxiv.org/abs/2603.06612 (Denisov-Blanch, Kazdan, Chudnovsky, Schaeffer, Guan, Adeshina, Koyejo; 2026-02-20 - OLDER than the 30-day window, kept as the anchor the 2026 work cites)
- Quote: "Even at 25x the inference cost of naive sampling, polling-style aggregation yields no consistent accuracy gains"
- Estate use: the hard boundary for the flock decode redesign. In unverifiable
  domains extra samples reinforce shared misconceptions; model errors are
  correlated even when prompted for pseudo-random output (correlation is
  fundamental, not benchmark-specific); models are better at predicting what
  other models will say than at identifying truth. Verdict: consensus decode is
  adoptable only where a verifier exists (code, bytes, tests); in prose verdicts
  the flock needs an external verifier or it amplifies shared bias - matching
  law 17 and the 0/3-at-strength-0.60-0.67 illusion.
- Falsifier: the forecasting benchmark with ground-truth resolution is the
  built-in falsifier; our flock pilot should run on resolvable rows first.

### 7. Wisdom of LLM Crowds: Aggregation and Contamination in Language Model Ensembles
- URL: https://arxiv.org/abs/2607.18269 (Igor Douven; v1 2026-05-26, v2 2026-07-22)
- Quote: "can exhibit wisdom-of-crowds effects, but that contamination-free evaluation is essential for reliable assessment"
- Estate use: the constructive complement to item 6 - WHEN crowds work. 15 LLMs,
  254 binary prediction-market questions: a LEARNED LINEAR aggregator (logistic
  regression) beat every individual model and every classical aggregator;
  symbolic regression finds a pure model-disagreement signal is the
  lowest-complexity useful formula. Contamination accounting: on questions
  resolved after all training cutoffs, the frontier-cloud vs smaller-local gap
  collapses from 35.8% to 8.9%. For the estate: two-family corroboration (law
  18) should be a weighted disagreement signal, not a coin flip; and any
  cross-model agreement claim must be cutoff-matched or it measures memorization.
- Falsifier: cutoff-matched re-evaluation is the falsifier - re-run estate flock
  rows against post-cutoff facts before banking agreement as skill.

### 8. Best LLM for Coding in 2026: 9 Models Ranked (DataCamp)
- URL: https://www.datacamp.com/blog/best-llm-for-coding (published 2026-09-25; fetch 403'd on primary door, recovered via secondary reader door - disclosed)
- Quote: "70.2% on Terminal-Bench 2.1 with max thinking (60.4% with thinking off)"
- Estate use: Q5's only outside quantification of thinking-off economics in the
  sweep. Poolside Laguna S 2.1: thinking off costs ~9.8 points on Terminal-Bench
  2.1 while mean completion length runs 23K-249K tokens per task with thinking
  on - the cheap lane pays roughly 10 points for up to ~10x token burn on
  agentic tasks. Also on the page: Vals scores Laguna at 53.5% "if you count the
  tasks its safeguards handed to a fallback model as failures" - a Maat-style
  denominator fight in the wild (vendor counts safeguarded handoffs as passes;
  the independent board counts them as failures). Pre-2026-10-04 conditions-suspect
  economics do NOT change direction under explicit thinking-off: they get a
  measured price tag. No full outside replication of OUR protocol was found; this
  is adjacent evidence, not a replication - say so when citing.
- Falsifier: the Vals-vs-vendor scoring split IS the falsifier for any headline
  number on the page; adopt the both-denominators report for the estate meter.

## Answers to the five research questions (one line each)

- Q1 consensus-decode prior art: YES - items 1, 6, 7 (weak rho, correlated
  errors, learned linear disagreement weighting); adopt the conditional-proxy
  framing, do not invent from zero.
- Q2 multi-judge calibration / second-judge without doubling spend: items 2, 5 -
  disagreement-based judge error rates are free to estimate; panel SIZE should be
  set by a TEE pilot, not doubled by default; leniency-toward-capable-examinees
  confirms Ember is never sole judge.
- Q3 Maat false-alarm accounting for our gate stack: item 3 - count false halts
  as failed work and name the denominator; our 37-accepted-on-125 citation-debt
  baseline lacks exactly the hand-review audit Maat needed post-publication.
- Q4 cheaper meter for n>=40 rows: item 5 - design pilot + TEE-corrected CIs at
  equivalent cost; item 9 (Spark-LLM-Eval, not banked for slot limit) adds
  content-addressable response caching so metric iteration never re-pays
  inference - a steal pattern worth porting without Spark.
- Q5 thinking-off economics: item 8 quantifies the trade (~10 points vs up to
  ~10x tokens), item 4 shows model-choice dominates task variance (43% vs 7%);
  no outside replication of the estate's exact thinking-off protocol was found -
  OWED, honestly.

## Overlap check (commands run this session)

- Command: rg -n -i "Maat|2609\.34017|consensus is not verification|when llms agree|2607\.08065|2603\.06612|open-endedness bench|2610\.02588|hidden measurement error|2604\.11581|spark-llm-eval|2603\.28769|wisdom of llm crowds|2607\.18269|trajectory basins|calibrated weighted majority" over catalog/catalog.jsonl -> NO_MATCH_CATALOG (zero hits).
- Same pattern over memory/ -> hits ONLY in memory/corpus/ai_canon/chapters/dlb_*.html (Deep Learning Book chapters) and memory/corpus/ractors/.../pg*.txt (Gutenberg texts) - generic word matches inside text libraries, no estate analysis holdings (nothing in memory/rib, memory/lenses, memory/press, memory/frontier).
- Verdict: all 8 banked items are genuinely new to the estate.

## OWED / not done

- X-thread IDs: none surfaced; fxtwitter door unused (no IDs to resolve). X-side
  discussion of these papers exists per the search backend's own note but could
  not be retrieved - a syndication-token or x-history miner pass remains the way
  in (matches the standing HERMES DIGEST OWED).
- ARBITER full read: arXiv ID never pinned (search truncated URLs); snippet says
  majority vote selects the most stable basin, not the most accurate - high-value
  follow-up for the flock redesign.
- Maat clean-trial FPR denominator: still not formalized in the paper; estate
  must define its own (changed-prose-rows vs flagged vs accepted) - the sweep
  does not resolve the standing OWED, it arms it.
- Cell aging-benchmark thinking-off underperformance: snippet only, page not read
  (paywalled Cell full text).
