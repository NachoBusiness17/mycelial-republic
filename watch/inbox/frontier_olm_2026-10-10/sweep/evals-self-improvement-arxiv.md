# SWEEP: evals-self-improvement via arxiv - 2026-10-10

source-fetched: 2026-10-10. Seat: sweep-evals-self-improvement-arxiv. Doors: arXiv Atom API
(`https://export.arxiv.org/api/query`, 6 targeted queries, sortBy=submittedDate desc:
`all:"LLM as a judge"` 30 entries; `all:"self-consistency" AND cat:cs.CL` 25; reasoning
effort/adaptive/overthinking 25; cs.CL false positives/false alarm/citation verification 25;
consensus/agreement/answer aggregation decoding 25; multi-judge/judge ensemble/panel 25) plus
`arxiv.org/abs/` deep reads and one full-text `arxiv.org/html/2610.04575v1` read. No door 403'd;
the API stayed up, so the `/list/cs.CL/recent` fallback was never needed. Two abs fetches timed
out at 60s on first attempt (2605.23362, 2610.07109) and succeeded on immediate retry: reported,
not papered over.

Pass 1 considered ~155 feed entries (with cross-query duplicates), 35+ distinct candidates
in-window plus 4 out-of-window priors. Pass 2 read 11 items (1 at full-HTML depth, 10 at
abs-page depth): 2610.04575 (abs + full HTML), 2609.12002, 2610.05094, 2607.08065, 2605.23362,
2610.07109, 2609.13824, 2610.03894, 2610.02142, 2609.00576, 2610.01218 (abs pages). Banked 8;
3 read items dropped for overlap (receipts below).

## Grounding (what the ask's citations resolve to in our bytes)

- Flock verdict illusion, strength 0.60-0.67 agreeing 0/3: `memory/rib/RIB_MINDSWEAVE_EVAL_CONSENSUS_ILLUSION_20260810.md:14-26`, and the rib's own redesign demand, decode must map to the ACTUAL task output space, at `:40-43`. The laws lens restates it as open q1 (`watch/inbox/frontier_olm_2026-10-07/lens/laws.md:102`).
- Second-judge debt (Ember never sole judge): `watch/inbox/frontier_olm_2026-10-07/lens/laws.md:105` citing `memory/rib/RIB_MODEL_GATES_20261001.md:50-52` and `memory/rib/RIB_MODEL_GARDEN_ROUTING.md:150`.
- Conditions-suspect economics (unmeasured thinking-ON default): `watch/inbox/frontier_olm_2026-10-07/lens/laws.md:118` citing `memory/rib/RIB_DEEPSEEK_SHOULDERS_20261001.md:60-72` and `memory/rib/RIB_DEEPSEEK_ELDER_SEAT.md:179-196`; the measured-ON rule at `memory/rib/RIB_INFERENCE_BUDGET_20261001.md:119-131`.
- Maat 2609.34017 false-alarm accounting (one denominator OWED) was banked by the 10-08 sweep
  at `watch/inbox/frontier_olm_2026-10-08/sweep/evals-and-self-improvement-arxiv.md:150-166`
  (37% false alarms, governed arm below ungoverned in 4/6). The 37-citation-debt acceptance on
  baseline 125 is the ask's material (commit 33e9cb88b).

## Overlap instruments (exact commands, run this sitting)

- Per-ID: `grep -rE "<id>" catalog/catalog.jsonl watch/inbox/frontier_olm_2026-10-09 watch/inbox/frontier_olm_2026-10-10 memory/rib memory/improve` then title-phrase `grep -ric "<title>" catalog/catalog.jsonl` plus `grep -ril "<title>"` over memory/{rib,improve} and frontier_olm_2026-10-0{6,7,8,9} and 10-10 sweeps (both loops run in-session; the first also covered memory/corpus/LINKS.jsonl for the q4/q5 adds).
- Predecessor reads: I READ both area predecessors end to end
  (`watch/inbox/frontier_olm_2026-10-09/sweep/evals-self-improvement-arxiv.md` full file;
  `watch/inbox/frontier_olm_2026-10-08/sweep/evals-and-self-improvement-arxiv.md` full file) and
  the day-7 sweep's banked section (`watch/inbox/frontier_olm_2026-10-07/sweep/evals-self-improvement-arxiv.md:14-56`).
- Dropped on overlap, with the receipt: 2609.12002 (read-not-banked by 10-09 sweep `:47`, top of
  the gala acquisition queue `memory/corpus/LINKS.jsonl:264`); 2610.07109 JudgeMoE (banked 10-07
  sweep item 3, full-HTML, `:34-40`); 2609.36856 FinRegQA-EU (banked 10-07 sweep item 2, `:32`);
  2610.02142 Keyword Harnesses Fail Open (quote-confirmed and used by the finetuning lane 10-06,
  `watch/inbox/frontier_olm_2026-10-06/sweep/finetuning-adaptation-arxiv.md:48,284`); 2610.02267
  Fast Models Slow Evidence (banked day-8, per `watch/inbox/frontier_olm_2026-10-09/sweep/inference-efficiency-hn.md` cross-ref); 2610.12083 All Verdicts (banked 10-09 sweep item 3).
- A full recursive grep of `memory/` was not run (prior seats measured 714,759 files / 12GB);
  scope was catalog.jsonl + memory/{rib,improve,press} + LINKS.jsonl + all frontier_olm sweep
  dirs 10-06..10-10, stated as the same limitation the 10-09 seat recorded.

## Banked items (strongest first; quotes verbatim from pages fetched this sitting)

### 1. From Probe Scores to Alarm Policies: Operational Validity of Activation Monitors for Language-Model Agents - arXiv 2610.04575 (2026-10-03, DAI 2026) - ZERO overlap

Read at abs + FULL-HTML depth. The Maat denominator question generalized into formal machinery:
an Operational Validity Contract fixing target, observability, identity, timing, unit,
comparator, calibration, cost; a claim ladder (representation -> restricted predictive ->
alarm-policy validity) that "cannot be promoted up by renaming the target"; any-alarm risk
R0(t)=Pr(max safe-attempt score > t) with Proposition 1: "At p=.05 and n=10, unit FPR is .401",
an identification error "more row-level test data cannot repair". AgentDojo counterexample:
mean-activation AUROC 0.9215 detects 0 of 38 positives at the 5% lock; a 10% calibration UCB of
8.92% realizes 18.67-20.0% test FPR; 23 calibration negatives force mechanical abstention
("zero alarms are mechanical abstention, not successful transport"). Identifiability bound:
m >= log(delta)/log(1-alpha), 59 independent negatives at alpha=delta=.05.

Estate fit (Q3+Q4): our gate stack (citation_lint PHANTOM-NUMBER, violation ratchet, census
patrol) runs per-file row alarms inside one push = exactly the repeated-opportunity compounding
this paper formalizes; a 5% per-row false-positive class compounds toward 40% per-push. The 59-
negative bound prices the meter: the estate's n>=40 decision-model rows sit BETWEEN the 10%
(29 negatives) and 5% (59) identifiability bounds, so the meter cost is not arbitrary, it is
lower-bounded by the alarm budget we claim; and "mechanical abstention, not successful
transport" is the fail-closed posture citation_lint already takes on unreadable cites. Feeds
the GAP_REGISTER fill-ball dwfrun-6c87e51f gate-economics rows.

### 2. When LLMs Agree, Are They Right? Auditing Self-Consistency and Cross-Model Agreement as Confidence Signals - arXiv 2607.08065 (v1 2026-07-09, v2 2026-07-28) - ZERO overlap

53 runners, K=50 samples/case, ~265,000 samples on GPQA Diamond + AIME, majority-correctness as
deployment label, runner-clustered bootstrap. Agreement is a "positive but weak predictor"
(rho 0.20-0.59), best for unsaturated mid-tier models and compute allocation, worst for the
most consistent frontier model: agreement >=0.8 on 77% of GPQA case-result entries yet 48% of
those confident entries wrong. Models can agree "out of shared bias, a memorized heuristic, or
an option-position prior rather than truth." A cross-family check on Claude tiers confirms
frontier over-confidence with confident errors recurring across providers.

Estate fit (Q1): the flock-verdict illusion externally replicated at 265k-sample scale, WITH the
two-family wrinkle (laws lens law 18): cross-MODEL agreement fails for the same reason
self-consistency fails when families share training priors, and the cross-family check is what
exposed it. The adopt-not-invent piece: their audit protocol (majority-correctness as label +
clustered bootstrap + per-regime breakdown) IS the mapping of consensus onto the task output
space the rib demanded, as a measurement instrument; what remains ours to build is the decode
itself. OUT OF 30-DAY WINDOW (July): flagged, banked because it is the definitive q1 prior.

### 3. How Much Do LLM-as-a-Judge Design Choices Matter? - arXiv 2610.05094 (2026-10-04) - ZERO overlap

10 reasoning models, scalar sentiment/toxicity (500+ items each) + binary QA classification
(n=600). Judges broadly reliable (MAD 0.11 on 1-7; 96.5% classification accuracy), but "changing
the rating scale alone can shift measured bias by up to 0.93 points", detailed prompts cut
leniency 28.9 points, switching models moves leniency up to 56.1 points, "lower reasoning
effort affects neither accuracy nor leniency", and "model identity is the dominant source of
variance."

Estate fit (Q5+Q2): the closest outside replication the window offers for the thinking-off
protocol economics: on the JUDGE lane, reasoning effort is a free axis (no accuracy, no leniency
cost), while model identity dominates variance. For the conditions-suspect re-measure (laws
lens q10/17: shoulders economics measured on unmeasured thinking-ON default) this predicts the
explicit-off re-measurement will move little on judge-shaped work, and says judge2 spend should
buy a different FAMILY, not more thinking. Honest caveat: this is judge-design context, not
agent-task context; the estate re-measure stays owed.

### 4. Instance-Optimal Estimation with Multiple LLM Judges on a Budget - arXiv 2605.23362 (2026-05-22) - ZERO overlap

Formalizes "budgeted heteroskedastic multi-judge estimation": K prompt-response pairs, J judges
with known costs and unknown per-query variances; inverse-variance weighted estimator (IVWE)
with oracle allocation; EST-IVWE adaptive algorithm using "optimistically biased" variance
estimates matching the oracle rate; matching local minimax lower bound (Assouad-type); beats
naive uniform allocation on synthetic + HelpSteer2.

Estate fit (Q2): the second-judge debt does NOT require doubling spend, it requires allocation:
per-instance, per-judge variance weighting says spend the second judge only on the instances
where judge1's variance is high. This is the published math for "Ember never sole judge" at
partial budget, and the duel-ledger re-judge can adopt the estimator shape directly (bank judge
variance per ask-class, weight the second pass). OUT OF 30-DAY WINDOW (May): flagged, banked
because it is the only formal budget-allocation prior found for q2.

### 5. When Consistency Does Not Mean Reliability: Evaluating Local LLM Judges Against Human Ratings - arXiv 2609.13824 (2026-09-12) - ZERO overlap

LLaMA-3-8B and Qwen2.5-7B as judges over 300 GPT-2-124M responses, 9 human annotators, 3 judge
repetitions. Pearson with humans 0.275 / 0.340 (MAE 27.71 / 18.64) while exact self-consistency
runs 92.3% / 97.3%: "a judge may produce consistent scores without necessarily agreeing with
human evaluators."

Estate fit (Q1, law 17 on LOCAL judges): the flock is local, and this is law 17 (consensus
strength is not correctness) measured on exactly our judge class: near-perfect internal
consistency with r~0.3 human alignment. Kill rule for any future local-judge proposal: report
consistency AND an external anchor in the same row, or the row is theater (law 31).

### 6. Consistency Without Alignment: Item-Sensitive Language Models Indistinguishable From Random - arXiv 2609.00576 (2026-09-01) - ZERO overlap

Forced-choice signalling task (Deception: Murder in Hong Kong) where Bayesian-optimal and
random strategies are computable in closed form. All 21 model-by-rule combinations were
item-sensitive (answer "depends on the specific input rather than on its own output prior"),
yet 8 were indistinguishable from random and 5 worse than random; item-sensitivity correlated
with deviation-from-random at only r=0.30. Names the pattern "consistency without alignment".

Estate fit (Q1, law 31 falsifier): the sharpest single falsifier line for consensus instruments:
even item-sensitivity (a stronger condition than agreement strength) is nearly uncorrelated
with beating random; any consensus instrument without an external reference is unfalsifiable
theater. The closed-form-optimal-task design is also a cheap ask-bank pattern: generate tasks
where optimal and random are computable, so consensus can be graded against truth at $0.

### 7. Proxy Confidence: Auditing Black-Box LLM Agents with a Surrogate's Log-Probabilities - arXiv 2610.03894 (2026-10-02) - ZERO overlap

A low-cost open-weight surrogate reads the same context and scores the agent's tool call from
its own log-probabilities (teacher forcing, request-PMI, discriminative verdict, tool-choice
competition); training-free, one prefill pass per call. AUROC 0.825 on hard coding vs 0.598 for
the actor's stated confidence; "Against self-consistency it gains +0.14 to +0.19 on
near-deterministic actors, at 1/K the cost" because frontier models repeat the same call across
samples. Real-time gate mode: escalating the least-trustworthy 50% of calls lifts accepted-action
accuracy +0.05 to +0.30.

Estate fit (Q4): the cheaper instrument exists for the CONFIDENCE side of the meter: repeated
sampling (our n>=40 shape) is the expensive way, and it degrades exactly where frontier actors
are near-deterministic; a surrogate log-prob readout is one prefill per row. Honest limit: it
prices decision CONFIDENCE (which calls to escalate), not decision CAPABILITY (accuracy of the
decision model on the task), so the capability meter rows stay n>=40; the surrogate replaces the
confidence/consensus columns, not the accuracy column.

### 8. AGO AI Quality Gate: Evidence-First Release Decisions for Retrieval-Augmented Generation - arXiv 2610.01218 (2026-10-01, NFMCP @ ECML PKDD 2026) - catalog stub only (state/arxiv/2026-10-02/2610.01218v1.txt), no analytical holding; NEW as distillation

Industrial evidence-first release gate: four-state decision model, layered scoring, stratified
beta-binomial gate, and a MANDATORY meta-evaluation validating the LLM judge before use.
gpt-4.1-nano detects non-adherent answers "barely above chance (AUROC 0.603)" while producing
correct protocol output; gpt-4o 0.783 with per-domain AUROC 0.62-0.88. Fixed-seed gate study
across regression/no-change/improvement conditions "quantifies unsafe promotion, false-alarm
cost, and improvement throughput": decision-grade profile cuts unsafe promotion to 22.2-35.1%
vs 29.3-41.8% naive. "Point estimates alone are not a release decision."

Estate fit (Q3): the estate gate stack's own economics table: name unsafe-promotion and
false-alarm cost as columns on every gate (citation debts accepted vs defects caught), validate
the judge per-engagement (our per-ask-class judge variance), and prefer a stratified
beta-binomial gate over point counts. Maps 1:1 onto the promote-WARN-gate decision the Maat
item opened.

## Considered, not banked (trail for the census)

2609.20541 (training-free self-reported confidence: three-sample agreement much weaker than
verbalized confidence; self-consistency amplifies shared misconceptions: covered by items 2+5;
catalog stub 09-18). 2609.17708 XConf (experience-based confidence matching 10-sample SC at
1/10 cost; catalog stub 09-17; adjacent to item 7). 2609.33290 (hidden-state probes beat
self-consistency distillation; q4 second instrument, single coverage kept to item 7). 2606.22798
RAD (MoE routing states as answer-string-free rollout selector: q1 output-space-adjacent, out
of window). 2610.12061 RACE cross-turn when-to-think (catalog stub 10-09; q5, weaker fit than
item 3 for judge lanes). 2609.40284 cua-speedrun (higher reasoning effort sometimes FASTER:
q5 anecdote). 2610.03994 VeriContest (extra reasoning effort raised cost without more proofs:
q5 second anecdote). 2610.08026 Labeling Problem in Hallucination Detection (catalog stub
10-07). 2609.40103 JuryFlow (listed by 10-09 predecessor trail; catalog stub 10-01). 2609.37145
judgment-vs-downstream-utility. 2610.08675 Same-Number Citation Swaps (stub-banked 10-07 per
day-7 sweep `:12`). 2610.12083, 2609.12002, 2610.07109, 2609.36856, 2610.02142, 2610.02267:
dropped on overlap, receipts above. 2608.30156 consensus-guided ensemble (out of window,
matched SC at 8x lower sampling cost: q4/q1 adjacent).

## Cross-cutting take

Three convergences: (1) law 17 is now externally over-determined (items 2, 5, 6 from three
independent designs: 265k samples, local judges, closed-form-optimal tasks), so the estate
should stop re-proving it and spend on the decode-to-output-space redesign the rib named, where
item 2's audit protocol and item 6's closed-form task family are adoptable parts; (2) the
second-judge debt is an allocation problem, not a doubling problem (items 4, 8, 3: variance-
weighted allocation, per-engagement judge validation, family-identity spend); (3) false-alarm
accounting has formal teeth now (items 1, 8): compounding per-row rates, identifiability bounds
on calibration negatives (59 at 5%), and unsafe-promotion/false-alarm-cost as mandatory gate
columns. The n>=40 meter verdict: capability rows stay n>=40 (bounded below by the alarm budget
at 10%, not 5%), confidence columns can move to the surrogate readout at 1/K cost (item 7).

## Honest limits

- One full-text read only (2610.04575); the other 10 reads are complete abs pages with verbatim
  abstract sentences, same depth the 10-09 predecessor used; theorem/procedure bodies of items
  2-8 remain unread beyond the abstract layer (item 4's estimator mechanics are 53 pages).
- Items 2, 4, 6 sit outside the 30-day window (Jul/Jul... specifically 2026-07-28 v2,
  2026-05-22, 2026-09-01); flagged per item, banked as the best-matching priors for q1/q2.
- No estate instrument was run (no meter rows, no re-judge, no citation-lint pass): mining and
  dedup only; every claim above cites the fetched page or the named repo path.
- Untracked-memory full-tree grep not run (714,759 files / 12GB); scoped grep stated above.
