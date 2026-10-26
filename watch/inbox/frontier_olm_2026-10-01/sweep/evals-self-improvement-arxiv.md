# sweep: evals-self-improvement via arXiv - 2026-10-01

stamp: source-fetched: 2026-10-01
area: evals-self-improvement · door: export.arxiv.org API + arxiv.org full texts · window: 2026-09-01 to 2026-10-01

## Doors used (health)

- Pass 1 (broad): 6 `export.arxiv.org/api/query` calls, `sortBy=submittedDate&sortOrder=descending`:
  1. `all:"LLM-as-a-judge" OR all:"LLM as a judge"` (30 results)
  2. `all:"judge ensemble" OR all:"multi-judge" OR all:"panel of LLM judges" OR (all:"judge" AND all:"debias")` (20)
  3. `all:"benchmark contamination" OR all:"data contamination"` (30)
  4. `all:"Bradley-Terry" AND all:"language model"` (20)
  5. `(ti:"emergence" OR ti:"emergent") AND (cat:cs.CL OR cat:cs.LG)` (20)
  6. `all:"self-improvement" AND all:"language model"` (20)
  All six returned clean Atom XML; union is roughly 100+ entries, filtered to the 30-day window: **40+ distinct candidates considered** (full list below).
- Pass 2 (deep): `arxiv.org/html/<id>v1` full-text reads succeeded for 2609.12002, 2609.26550, 2609.31184, 2609.26481, 2609.36549, 2609.37145, 2609.36892, 2609.35025, 2609.27510. **Degraded doors:** HTML 404 for 2609.15309, 2609.33871, 2609.12353; fell back to `arxiv.org/abs/<id>` per the recipe; those three are **abstract-level reads only** and are flagged as such on their items. The 2609.15309 quote was re-verified verbatim by a second targeted fetch of the abs page.

## Pass 1 candidate pool (all from the window; considered, mostly not banked)

Judge reliability/bias: 2609.37577 Pair Difficulty Matters (HELD) · 2609.37145 From Judgment Quality to Downstream Utility · 2609.36979 Louder, Longer, Livelier (speech judges) · 2609.33955 Designing Reliable Judge Systems for Multi-Turn Business Agents · 2609.32533 LLMAdBench (frontier judges unreliable for ad preferences) · 2609.31857 Judge Validation Under Sparse Overlap · 2609.31215 DIAL position-debiased judges (HELD) · 2609.31184 Accounting for Bias (HELD) · 2609.29769 JEV vs LLMs as Rubric Judges, wrong in same places (HELD) · 2609.26550 JEV-as-a-Judge (HELD) · 2609.12002 Can We Trust LLM Judges · 2609.26489 Calibration as a First-Class Criterion · 2609.13773 psychological-depth judge ensemble bias · 2609.36856 FinRegQA-EU (judge misses fabricated citations).
Duel/arena: 2609.15309 Elo-per-token · 2609.26707 Optimal Sequential Annotations (LMArena votes) · 2609.33282 pairwise comparative scale (SubJudge).
Self-improvement/RSI: 2609.39149 Rep2Skill · 2609.39045 RSIGame · 2609.38516 Solo to Social Learning · 2609.38372 Self-Evolving Harness · 2609.37950 Video-RSI · 2609.36892 Harness Evolution as Learning · 2609.36549 MedForge-RSI · 2609.35025 AutoDataBench · 2609.34975 hint annealing · 2609.34712 RSI-Router · 2609.34069 certificate-driven porting · 2609.33713 BIRD · 2609.33398 COEVO.
Contamination: 2609.27510 Uncheatable Eval (HELD) · 2609.25352 SSP-Bench · 2609.23201 Do Not Trust the Benchmark · 2609.19617 DataCanvas-EDU · 2609.18284 Made in Hungary · 2609.12353 SynthSentry · 2609.08532 individualized knowledge simulation · 2609.06229 SWE-Test.
Emergence: 2609.33871 Population Physics · 2609.26481 Behavior is Not Enough (HELD) · 2609.36455 emergent phases of superposition · 2609.32100 one-third scaling law · 2609.29362 POS as emergent SAE categories · emergent-misalignment cluster (2609.37914 / 2609.37624 / 2609.35291 / 2609.34970).

## Overlap ledger (grep evidence, run this session)

Command shape: `grep -c "<arxiv-id>" catalog/catalog.jsonl catalog/tags.jsonl` plus a recursive `grep -ril` over `catalog/ memory/` (18 title/ID probes). `memory/trajectory/steps.jsonl` matches are **this session's own step log** (circular) and are called out per item.

- **Already held, NOT re-banked:** 2609.26550, 2609.31184, 2609.26481, 2609.27510 (each 1 hit in catalog.jsonl + tags.jsonl; catalog lines are `zone:"lsa"` abstract snapshots, e.g. `"path": "local_sovereign_agent/state/arxiv/2026-09-23/2609.26550v1.txt"`), plus 2609.37577, 2609.31215, 2609.29769 (1 hit each by ID). I deep-read four of these anyway (26550, 31184, 26481, 27510); their numbers are folded into the notes below as context, not banked as new.
- **Known pointer, no bytes:** 2609.12002 - 0 hits in catalog/tags; referenced one-line at `memory/runs/gapwave/hn_x_fanout/orchestration_verification.md:75` ("Can We Trust LLM Judges ... capability-dependent judge biases; multi-judge ensemble calibrates them. Need: agreem..."). Banked because the deep read supplies the mechanism the pointer's "Need" asks for.
- **Genuinely new (0 hits anywhere except session self-log):** 2609.37145, 2609.36892, 2609.36549, 2609.35025, 2609.33871, 2609.12353, 2609.15309.

## Lens-path caveat

The ask cites `lens/laws.md` and `lens/burns.md`. No `lens/` dir exists in this repo (checked `find . -maxdepth 3`, `ls lens docs/lens watch/lens`, plus a docs/watch/state/memory sweep). Closest file `watch/inbox/48h_synth/laws.md` carries neither "second judge" nor "consensus illusion". RQ framing is therefore taken **from the ask text itself**; the descent falsifier is grounded at `memory/rib/RIB_THE_DESCENT_PROTOCOL_20261001.md:73` ("frontier contribution forward = the protocol decayed into spend theater").

## Banked items (deep-read, strongest first)

### 1. Can We Trust LLM Judges: Capability-Dependent Biases and Multi-Judge Ensemble for Bias Calibration - arXiv:2609.12002 (2026-09-10) [full HTML read]

**The direct answer to RQ1 (second judge family).** 4 benchmarks (QuALITY, GSM8K, MBPP, AIME 2025) x 6 examinees = 36 judge-examinee pairs, judges spanning three families (OpenAI GPT-5/GPT-4.1-mini/o4-mini, Meta Llama-3.3-70B/Llama-4-Maverick, DeepSeek-V3.2). Findings: judge accuracy tracks its own task accuracy (r>=0.90) and inversely tracks directional bias (r<=-0.83); **all judges grow more lenient toward more capable examinees even cross-family** (r>=0.83), dominating self-preference except for GPT-5 (own wrong answers accepted 73-100%). Fix: calibrated weighted majority voting, each judge weighted by online estimates of its false-positive/false-negative rates, label-free via a Dawid-Skene-style disagreement estimator (proxy FP = voting against the panel majority), tracking an oracle to within 0.5 pp. Majority voting vs self-judging on GSM8K: accuracy 96.8% vs 89.3%, FPR 20.7% vs 39.1%. Limitations: three families only, no Anthropic/Google; simulated drift ordering; single prompt template; estimator assumes a mostly-correct panel majority.
**Estate tie:** claims-desk tri-state verdicts and the duel graders can adopt per-judge FP/FNR weights - the calibration is label-free and cheap; capability-leniency means our premium-tier verdicts need cross-family panels, not self-judges.

### 2. Harness Evolution as Learning: Approximation, Generalization, and Optimization Limits of Self-Improving Personal Agents - arXiv:2609.36892 (2026-09-29) [full HTML read]

**RQ3 theory.** Decomposes the harness-evolution risk gap into approximation/generalization/optimization error. Theorem 4.1: context harnesses only reweight pretrained behaviors; control harnesses create new ones. Theorem 4.2: generalization error <= L*exp(-2g^2*floor(n/L)) - strictly increasing in memory size L at fixed feedback n (the U-shaped memory curve is measured: violations 0.77 -> 0.20 at L=10, back up to ~0.25-0.27 at L=20-150). Theorem 4.4: even with vanishing estimation error, biased updates converge to a stationary distribution with a **persistent positive error floor**; "repeated self-evolution does not guarantee sustained improvement." Empirically: best self-evolution arms (ACE/TEPA ~0.48) stay ~0.40 above oracle (0.071) after 24 interactions; Reflexion stays at the no-memory baseline.
**Estate tie:** this is the spend-theater falsifier made formal: iterations without an update-recipe change leave a common error floor - exactly the descent protocol's "ledger grew but no rib carries a frontier contribution" failure mode. Memory growth must track feedback amount AND reliability (the prior-art sweep clause in learning-theory form).

### 3. MedForge-RSI: Medical Deepfake Detection via Recursive Self-Improvement - arXiv:2609.36549 (2026-09-29) [full HTML read]

**RQ3 working mechanism.** Frozen 8B VLM weights; mutable state = structured experience entries + a self-written sandboxed toolbox (single-file, deterministic, raw measurements never verdicts). Per round: detect on 40 fresh labeled images, reflect on verified errors, propose changes; every proposal admitted only after a two-stage acceptance test (replay on/off on the batch, net >= 0; then A/B on 100 images from an independent 200-image pool, reject if correct-count drops >1). Weights, system prompt, scoring code, and all eval sets are outside the loop's write access; a verifier health check (off-arm must reproduce >=70% of known-correct predictions) distrusts the round otherwise. Gains: 4-set average 75.0% -> 84.4% over 20 rounds, 39,200 labels total (less than one SFT run). **Acceptance testing alone was worth 17.5 points - measured when a bug silently disabled it.** Harmful mechanisms named: admission budget -24.0, tournament selection -6.0. Maxima arrive within ~10 rounds; final state averages 3.0 below the best round. Full trajectories including rejected changes released.
**Estate tie:** the percolator/47-invariants/verkle loop gets its blueprint: acceptance-test-gated, individually attributable, testable, reversible state changes; verifier health as part of the attack surface; retirement by usage statistics, not the model's own judgment.

### 4. When Agents Slow Down: Understanding LLM Agents' Test-Time Strategies via Elo-per-token Analysis - arXiv:2609.15309 (2026-09-14) [**abs-level read; HTML 404**]

**RQ2 duel methodology.** Proposes Elo-per-token: track best solution per token budget, aggregate cross-task orderings with a Bradley-Terry model into Elo; compare against independent sampling, "for which Elo grows linearly with log compute." Four agents on four open-ended benchmarks, sessions up to 100M tokens, plus three feedback-driven optimization harnesses. Agents start above the reference in Elo-per-token efficiency, then gains diminish and fall below it; top human AtCoder contestants improve superlinearly - headroom. Scaling inflection point defined where marginal Elo meets the reference. **Splitting 100M tokens across parallel sessions beats one long session by +264 Elo and ten short sessions by +355** (FrontierCS Polyomino Packing). Authorship includes Zettlemoyer, Dimakis, Cheung, Peng (UW).
**Estate tie:** the duel volume leg toward $70+ should be scored Elo-per-token, and its compute shape should be parallel short sessions, not long ones - a directly actionable routing law for the duel harness.

### 5. AutoDataBench: Can Agents Write the Data That Feeds the Self-Improvement Loop? - arXiv:2609.35025 (2026-09-28) [full HTML read]

**RQ3 honesty check.** Per-artifact scoring of agent-written executable tasks against production acceptance criteria: gate (8 defect classes, zero-score) x difficulty band (target pass rate in [0.125, 0.75]) x rubric quality (modes covered / ceil(0.6N)). Result: "no agent we evaluate scores above 20 out of 100" at 45 min (kimi-k3 0.184, gpt-5.6-sol 0.177, qwen3.8-max 0.139, glm-5.3 0.130, deepseek-v4-pro 0.097). The bottleneck is **difficulty placement**: only 14.6-25% of deliveries land in band; "The agents can read a model's behavioural record and aim a task at it; what they cannot do is place that task where the target model solves it sometimes." Quadrupling the budget lifts the best agent 0.184 -> 0.541 at flat unit cost ($11.88 vs $12.62 per usable task). Rankings unstable across suites; self-authoring (deepseek writing for itself) scores worst on the gate.
**Estate tie:** any RSI data leg in the descent protocol should assume agents cannot yet calibrate task difficulty - bank task-writing as acceptance-tested artifacts (item 3's rule), and expect the difficulty band, not the gate, to discard most output.

### 6. From Judgment Quality to Downstream Utility: Rethinking LLM-as-a-Judge for Open-Ended Tasks - arXiv:2609.37145 (2026-09-29) [full HTML read]

**RQ1/RQ2 bridge.** Varies judge protocol on three axes (verdict granularity T/F vs 0-10, critique usage/order, batching) and measures intrinsic quality and downstream utility (GRPO training + test-time Best-of-NN, judge-guided revision, beam search) independently. Core finding: "Surprisingly, judgment quality and downstream utility do not always align" - rating beats T/F for training in 10/16 settings while T/F wins critique-consistency in 7/8; batched judging is cheaper but raises reward ties in 7/8 and lowers accuracy in 7/8 (permissiveness/position artifacts). Judge guidance converts test-time compute efficiently: Best-of-N gain over direct grows from +7.8 points at N=4 to +17.2 at N=40; one judge-guided revision adds 1.1-22.8 points; a rubric-accessing judge (policy never sees the rubric) is the key design.
**Estate tie:** duel harness protocol choices (granularity, batching, critique order) should be selected by downstream utility, not judge accuracy; the rubric-held-from-policy judge is a cheap shape for our grader prompts.

### 7. Population Physics, Population Problems: Safety and Emergence in LLM Societies - arXiv:2609.33871 (2026-09-27) [**abs-level read; HTML 404**]

**RQ5 measurable emergence.** Introduces a self-organization measurement framework (statistical order parameters, agent-agnostic, "without relying on natural language or model versioning") applied to a Schelling grid, the Moltbook social network, and a Twitter-like misinformation sim ("Rogue"). "All three exhibit statistically significant self-organisation," with open-ended systems showing "sharp, phase-transition-like dynamics"; "population-level pathologies can emerge even when the LLMs are safety-tuned or monitored," driven by "the coordinated activity of a population subset." Crucially, two negative controls - GovSim commons dilemma and ChatEval judge deliberation - show **no** self-organization, which is what makes the measure falsifiable rather than a consensus illusion.
**Estate tie:** the emergence-compounding open question gets a usable operationalization: measure order parameters + significance, demand negative controls, and treat "emergence" claims without them as unmeasured. Also a standing risk note: multi-agent swarms (our 50-wide windows) can develop population-level pathologies despite per-seat safety tuning.

### 8. SynthSentry: Detecting Synthetic Data Contamination in Language Model Training Data - arXiv:2609.12353 (2026-09-11) [**abs-level read; HTML 404**]

**RQ4 trust-bytes for corpora.** "Prior work diagnoses collapse after training; the actionable problem is screening a corpus of unknown provenance before training." Corpus-level, model-agnostic score = distributional divergence over lexical diversity collapse, n-gram tail truncation, and perplexity variance across reference models; no access to the generating model, no synthetic labels. Leave-one-generator-out protocol; per-domain calibration holds its nominal false-positive budget once covariance shrinkage + bootstrap thresholds replace a naive quantile (which runs 4x over budget). Downstream fine-tune showed no accuracy deficit at their (small) scale; **over-pruning risk once pruning exceeds the true contamination fraction**. Scope: English, batch mode, single-generation (not recursive) sources.
**Estate tie:** the estate's synthetic corpora (QLoRA tape corpora, generated eval sets) can be screened pre-training with this three-statistic divergence; the over-pruning warning maps to our anti-data-loss instincts - prune to measured contamination, not beyond.

## Context from held items (read but not re-banked)

- 2609.26550 JEV-as-a-Judge: decision-only cheap judge at 0.36% of a frontier judge's fee, frozen cascade retains 99% accuracy; **thresholds do not transfer across judges/workloads** (GPT-5.6 policy lost 2.35 pp) and style-adversarial pairs defeat confidence routing (RM-Bench hard pairs -19.8 pp); "Treat confidence as an escalation signal, not a certificate." Duel lane shape: cheap-first with a frozen, workload-validated escalation threshold.
- 2609.31184 Accounting for Bias: augmented Bradley-Terry + many-facet Rasch joint fit correcting position/verbosity/severity/same-family affinity; rankings from substantially fewer comparisons; Kendall tau = 0.80 disagreement between naive and corrected rankings even on full data. Duel volume leg: bias-correct fitting is near-free compute; "the path to reliable rankings runs through better measurement, not more measurement."
- 2609.26481 Behavior is Not Enough: identical cooperative outcomes in LLM public-goods games arise from distinct processes (learning vs selection vs imitation); expectation elicitation makes the states observable; "indistinguishable from behavior alone." Same consensus-illusion cure as item 7, at interaction level.
- 2609.27510 Uncheatable Eval: compression rate on freshly published text; Spearman rho = -0.884 vs zero-shot MMLU over 80 models; contamination resistance is recency + refresh, explicitly not a guarantee.

## Not-run / not-found

- `lens/laws.md`, `lens/burns.md`: not found in this repo (searched; see Lens-path caveat above). Not fabricated.
- No PDF fallback fetches for the three 404 items (abs pages read instead); their full texts remain unread by this seat.
- No estate-side duels or evals were executed during this sweep; this is a research-only ask.
