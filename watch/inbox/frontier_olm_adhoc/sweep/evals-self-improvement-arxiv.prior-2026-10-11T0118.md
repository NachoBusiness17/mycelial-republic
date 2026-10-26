# Sweep: evals-self-improvement via arxiv - 2026-10-11

source-fetched: adhoc

Door: arXiv (export.arxiv.org Atom API + arxiv.org abs pages) via WebFetch. Door status: the API answers reliably on single and paired calls; a 5-way parallel burst timed out at 60s five-for-five and is not the shape to use on this door. Seven API queries and ten abs-page reads completed this session; nothing 403ed. No fallback door was needed, so none is claimed.

## Pass 1 (broad)

Queries run against `https://export.arxiv.org/api/query` with `submittedDate:[202609110000 TO 202610112359]`, sorted by submittedDate descending:

1. `abs:"LLM-as-judge"` (25 entries)
2. `abs:"agent benchmark"` (25)
3. `abs:"data contamination" AND cat:cs.CL` (25)
4. `abs:"LLM routing"` (11 of 12)
5. `abs:"long-horizon" AND abs:"agent"` (25)
6. `abs:"position bias" AND abs:"judge"` (8)
7. `abs:"self-improving" AND abs:"agents"` (20)

Total candidate entries considered: 139 (with cross-query duplicates removed by eye, still well over the 30-item floor; every entry above was seen in a fetched result this session). Strongest veins: judge reliability (Q1), certified automation of agent eval (Q1/Q2 bridge), concurrency failure modes (Q2), interventional contamination designs (Q3), behavior-not-identity routing (Q4).

## Pass 2 (deep reads; every banked item read end to end on its abs page this session)

Read in full: 2610.11116, 2610.12083, 2609.34320, 2610.10263, 2609.27176, 2610.05982, 2610.11464, 2609.33044, 2610.05140, 2609.37362. Ten papers. Eight banked below; 2610.11464 dropped for catalog overlap (see Overlaps); 2610.05982 read but not banked (weakest RQ4 fit, superseded by RouteFM; near-miss note below).

## Banked items (strongest first)

### 1. BayesJudge: Uncertainty-Aware Bayesian Meta-Evaluation of Human and LLM Judgments (arXiv 2610.11116, 2026-10-08, stat.AP, NeurIPS 2026)

Quote: "We propose BayesJudge, an online Bayesian meta-evaluation layer for conflicting human-LLM judgment streams."

Why: This is the validated 2026 judge protocol for the owed judge number two. Order-swapped paired judge calls separate true response quality from position bias (the exact defect in ember's dossier, `memory/rib/RIB_MODEL_GARDEN_ROUTING.md:150` "position-bias flip at n=1"); tie-open labels keep ambiguity mass observable instead of forcing win/loss; rater-specific confusion matrices let one layer distinguish judge families without metadata. Posterior uncertainty correlates with human disagreement, i.e., the quorum knows when it is unsure. Seat ember's replacement protocol on this design: two orders per verdict, ties allowed, per-judge confusion estimated online.

### 2. All Verdicts are Not Equal: Rethinking LLM Judge Reliability (arXiv 2610.12083, 2026-10-08, AACL IJCNLP Main 2026)

Quote: "Finally, we demonstrate that shifting from pairwise win-rate to holistic rubric scoring improves trustworthiness more than any single-format prompting intervention, offering an actionable framework for robust NLP evaluation."

Why: Six models stress-tested across four benchmarks, five prompt formats, two orders, three temperatures, ten repetitions; the trustworthy verdict rate T (joint probability a verdict is reproducible AND order-invariant AND accurate) is the metric our judge dossier rows should carry instead of bare accuracy. Two findings restructure the judge-two decision: reliability is item-specific, not model-level (judge selection per item class, matching our question-class routing law), and the most deterministic judge agreed with ground truth only 51 percent of the time (determinism is not correctness; do not seat judge two by stability alone). Format beats prompting: rubric scoring first, family second.

### 3. Pinned and Still Unstable: Within-Judge Verdict Variance and the Noise Floor of LLM-as-Judge Leaderboards (arXiv 2609.33044, 2026-09-27)

Quote: "identical inputs to the same temperature-zero judge, at a constant serving-reported model version, produce different verdicts across re-runs"

Why: The measured case for n-judge agreement designs. Four frontier judges on Arena-Hard/AlpacaEval 2/MT-Bench: per-item flip rates around 5 percent average, around 40 percent on close-call items that decide margins, varying 40x across judges (0.13 to nearly 10 percent). Of 15 re-judged head-to-head orderings, 12 survive every re-run of the principal judge but only 8 survive every judge (Kendall tau 0.42-0.64 between Gemini and Sonnet judges). Their minimal reporting protocol is what our model-gates rib should adopt verbatim: several judge re-runs, published stability profiles and adjacency intervals, and results under at least two judges from different families. That last clause is the independent literature grounding for the second-judge-owed row.

### 4. Certified Selective Automation of LLM Agent Evaluation (arXiv 2609.34320, 2026-09-28)

Quote: "We ask the operational question: what fraction of agent evaluation can a judge take over, with a certificate that the error rate among auto-decided trajectories stays below a budget alpha?"

Why: The error-budget design for automating checker verdicts at our workflow gate. Task-level bootstrap resampling stays valid under correlated trajectories (agents attempt the same tasks); the naive i.i.d. certificate claimed 98 percent automation but blew its budget in 17.5 percent of task resamples. A 4B judge (SFT + reject-weighted GRPO, logprobs) certifies 0.30-0.59 of evaluation at alpha = 0.1, the only judge among frontier baselines certifying on both corpora; coverage is predictable pre-training from base rate and discrimination alone (leave-one-corpus-out R squared 0.96); pseudo-label contamination in self-training is bounded by alpha by construction (realized 0.000-0.041). Direct steal shape: cheap janitor-grade checkers auto-decide the bounded class of gate rows, humans and primes keep the rest, and the certificate (not vibes) sets the split.

### 5. LeakScale: Estimating the Causal Effect of Benchmark Exposure (arXiv 2609.27176, 2026-09-23)

Quote: "provenance can establish contact, but only a counterfactual can quantify the performance attributable to that contact."

Why: The design template for the owed 100+ hidden ask bank (currently ~20 asks, 6 hidden). Interventional: construct fresh executable tasks that depend on private, family-specific details not inferable from the public task, control access to that private information, and measure the control-adjusted accuracy shift. Across 2,048 unique families, two model families, two executable domains, 262,144 generations, exposure raised accuracy in every model-by-domain combination by +7.17 to +27.31 points. Lesson for the bank: "hidden" must mean counterfactually hidden (private variants plus access control with the shift measured), not merely unlisted. This is also the honest instrument for the 30-day cell-rot question: rot is only justified to the degree exposure shifts outcomes, and this design measures that degree.

### 6. When Sub-Agents Work in Parallel: The Promises and Pitfalls of Dynamic Concurrency in Long-Horizon Coding Tasks (arXiv 2610.10263, 2026-10-07)

Quote: "we evaluate its end to end effects and scheduling behavior, and analyze matched trajectories to characterize 13 concurrency specific failure modes"

Why: External failure taxonomy for the fan-out width law and the max-concurrency standing law (AGENTS.md; receipts gala/burn-wave). Controlled matched-execution comparisons across Codex, Claude Code, and Kimi Code on 354 tasks and 2,124 executions: 13 concurrency-specific failure modes plus 28 observable patterns; model capability largely governs short-task outcomes while orchestration becomes central in long-horizon work. The 13-mode taxonomy is the cross-check to run against our 50-wide envelope receipts before climbing to the untested 15-16 rung: which of their modes did our 429-storm and 1302 census already encode, and which are missing.

### 7. AutoSciBench: Autonomous Benchmark Generation for Evaluating Scientific Agents (arXiv 2610.05140, 2026-10-04)

Quote: "Agents attempt to solve each task, producing solver trajectories and corresponding judge feedback which AutoSciBench uses to revise the recipe or concept"

Why: The growth mechanism for scaling the hidden ask bank from ~20 to 100+. High-level concept plus low-level recipe per task; solver trajectories and judge feedback revise the recipe to close shortcuts; distilled refinement experience guides future generation. Generated benchmarks cut average solver accuracy by 22.4 points (computational biology) and 25.5 points (materials science) versus human-curated, with higher quality ratings in all three domains. Estate wiring: keep the operator-review gate (the bank is owed as operator-reviewed; AutoSciBench replaces the authoring bottleneck, not the review), and pair with LeakScale's private-variant discipline so generated asks are contamination-blind by construction.

### 8. Pretrain Once, Route Anywhere: Towards a Foundation Model for LLM Routing (arXiv 2609.37362, 2026-09-29)

Quote: "Experiments demonstrate transfer across changes in domains, modalities, candidate pools, and context budgets."

Why: Best 2026 directional evidence on RQ4. RouteFM routes from behavioral context, characterizing anonymous candidate models and inferring target-specific capabilities from as few as eight observations; decisions are driven by task-specific behavioral evidence, not fixed model identities, and the router transfers frozen across domains, modalities, candidate pools, and context budgets, beating the strongest baseline by 2.23 quality points on MMR-Bench held out from pretraining. This is consistent with the estate's 36.3-pct question-class law (`memory/rib/RIB_ROUTING_CLASSES_20261002.md:12`: question class explains 36.3 pct of score variance, family 3.6 pct): when routing signal lives in task behavior rather than model identity, family is a weak feature. It is NOT an effect-size replication: no variance decomposition by class versus family is reported. The falsifier stays OWED, agreeing with the sibling X sweep's verdict (watch/inbox/frontier_olm_adhoc/sweep/evals-self-improvement-x.md:31).

## Overlap check (commands run this session)

`grep -c` per candidate phrase against `catalog/catalog.jsonl`; scoped `grep -rl` over memory/frontier, memory/improve, memory/rib, memory/lenses, memory/press, memory/zknot/LATEST.md, CORPUS_CATALOG.md. Results: BayesJudge 0, trustworthy verdict 0, Pinned and Still Unstable 0, Certified Selective Automation 0, LeakScale 0, routing collapse 0, RouteFM 0, AutoSciBench 0, Sub-Agents Work in Parallel 0, inspectable grader 0. Three candidates found already held and DROPPED from banking: "Who Verifies the Verifier? Co-Evolving Inspectable Graders with Self-Improving Agents" (catalog row, zone lsa, age_days 1; deep-read this session, excellent, sibling lane already banked it), "Uncheatable Eval: Dynamic Compression-Based Evaluation of Language Models" (catalog, age_days 16), "SWE-Journey: Towards More Realistic Evaluation of Coding Assistants..." (catalog, age_days 1). A full recursive grep over memory/ hung and was stopped; the scoped grep above is the recorded evidence. No overlap with sibling sweep banked IDs (they hold 2602-2607 era items; mine are 2609-2610).

## Near-misses (pass 1, not banked, why)

- 2610.05982 Breaking the Tie (CASLR): deep-read; "routing collapse" from overlapping model capabilities is replication-directional for RQ4 but the fix is a router-training detail (masked softmax soft labels); RouteFM carries the question better.
- 2609.37577 Pair Difficulty Matters: position-bias proxies dominated by close-rank pairs; rank-gap-conditional metrics. Good second-order refinement for judge scoring, below the eight banked.
- 2609.31184 Accounting for Bias Enables Sustainable LLM Evaluation: latent-variable bias correction recovers rankings with fewer comparisons; relevant to cheap-quorum sampling but no agent-work validation.
- 2610.11559 SWE-Journey, 2610.11655 Harness Evolution Hits a Ceiling, 2610.08364 Transect, 2610.07557 CheckerBench, 2610.10942 StoreBench, 2610.02994 Sentry, 2610.08722 compaction-harm: all pass-1 candidates for the long-horizon shelf; SWE-Journey already cataloged, the rest deferred to the next sweep rather than shallow-banked.
- Self-improvement core: 2610.11464 (dropped, overlap), 2610.12176 MASS, 2610.08902 Agent Plasticity, 2610.10611 Verification and Self-Improvement foundations, 2610.10310 RSIGym, 2610.04087 DUET: a whole recursive-self-improvement vein surfaced; recommend a dedicated follow-up sweep.

## OWED after this sweep

- RQ4 falsifier UNBANKED: no independent 2026 variance decomposition replicating task-class-dominates-family at anything like 36.3 vs 3.6 pct. RouteFM and CASLR are directional only. Still owed: a mixed-agent-workload study reporting class and family variance components side by side.
- Judge-two seat: protocol now evidence-backed (items 1-3); the seat itself (which family, which rubric) remains an estate decision with the ember dossier as the negative case.

## Estate wiring

Feeds: the evals shelf of corpus/CURRICULUM.md; model-gates and routing ribs (judge-two protocol, hidden-bank growth + rot instrumentation, 36.3 pct replication watch); workflow-gate grader/checker dogfooding (certificate-shaped automation, alpha as the budget dial); fan-out width law cross-check (13-mode taxonomy).
