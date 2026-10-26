# Sweep: evals-and-self-improvement via arXiv (2026-10-03, second same-day pass)

source-fetched: 2026-10-03
Area: evals-and-self-improvement (arXiv door)
Sweep agent: sweep-evals-and-self-improvement-arxiv (dynamic workflow gopher, evening seat)

This file REPLACES the morning version written by this run's earlier seat on the same path
(same rule the burns lens applied to its own 10:09 file, lens/burns.md:4-5). The morning
version banked 8 items (its lines 42-121); those stay valid and are the anti-rebank baseline
below. This pass is new work under burns.md rule 1: new primaries only, overlap stated, never
silently re-confirmed.

## Method (instruments, this sitting)

Pass 1 (broad): 4 export.arxiv.org API Atom feeds via WebFetch, sorted submittedDate
descending, 25 entries each, 100 feed entries scanned:

1. (all:"LLM-as-a-judge" OR all:"LLM judge") AND (all:ensemble OR all:panel OR all:mixture)
   -> 25 entries, 2026-08-23..2026-09-29.
2. (all:"judge" OR all:"judges" OR all:"grader") AND (all:cascade OR all:"cost" OR
   all:"routing") AND cat:cs.CL -> 25 entries, 2026-09-02..2026-10-01.
3. (all:"self-consistency" OR all:"semantic entropy" OR all:"self-consistent") AND
   (all:confidence OR all:"hallucination detection" OR all:unanimity) AND cat:cs.CL
   -> 25 entries, 2026-06-11..2026-09-28.
4. (all:"reward hacking" OR all:"reward overoptimization" OR all:"imagined") AND
   (all:grader OR all:"reward model" OR all:rubric) -> 25 entries, 2026-08-06..2026-10-01.

60+ entries seriously considered against the five research questions; shortlist of 12; 9 deep
reads end to end via arxiv.org/abs pages (2609.39229, 2609.29769, 2609.20541, 2609.33044,
2609.00038, 2609.29333, 2608.08002, 2609.21277, 2609.02246). Zero arXiv-door 403s. One
degraded fetch: the 2609.29333 abstract page timed out twice on the second verbatim-quote
pass (the first deep read of the same page succeeded), so that item banks its verbatim title
as the quote and its numbers are marked fetch-reported. No fallback doors were needed and none
were faked.

## Anti-rebank baseline (do not re-bank)

- Morning pass on this path (inherited, its lines 44-121): 2609.34292, 2609.32670, 2609.35182,
  2609.38372, 2609.34215, 2609.34227, 2609.09703, 2609.33295.
- Today's fold register r1-r23 (DIGEST confirmed-finds table; lens/burns.md:86-106), including
  2610.00954 SLM-judge ensembles (r20) and the 1wdasar sampling-consistency ladder (r7).
- The STRUCK 2610.00905 claim-as-stated (lens/burns.md:78-85).
- Already held, found by overlap grep this sitting and therefore NOT banked here:
  RAIM 2609.39229 (my strongest RQ1 hit, deep-read this sitting) is ALREADY IN CATALOG:
  catalog/catalog.jsonl:806387, path state/arxiv/2026-10-01/2609.39229v1.txt, age_days 0,
  title "RAIM: Robust Aggregation of Inexpensive Models for Hallucination Detection", mirrored
  2026-10-01. Same drop rule the morning pass applied to False Frontiers and EnterpriseVal
  (morning file lines 24-31). Its numbers, for whoever mines the holding: 4-9B panel of 10
  judges from disjoint families, median 93 pct of Claude Sonnet's Cohen's kappa retained at
  1/64th frontier inference price, one-time calibration on 50-100 labelled records, and an
  admissibility test that reads from the members' own outputs whether aggregation beats the
  best member.

## Estate checks run this sitting

### RQ5: keyword census over memory/trajectory/steps.jsonl ($0 probe 2, fired)

Instrument 1: wc -l memory/trajectory/steps.jsonl = 50,784 rows. Instrument 2, minutes later:
venv python line-loop over the same file = 50,824 rows read. The +40 delta between the two
moments is the live trajectory writer appending while this seat works (same live-write effect
the fold logged as its 41-row unexplained delta, lens/burns.md:115); never difference counts
from different moments.

Schema (first row read): trajectory_step.v1 = ts, session_id, face, command,
result.output_excerpt. It records SHELL traffic, not model reasoning.

Keyword census (case-insensitive, command + output_excerpt per row):
rubric 132 rows, judge 889 rows, grader 42 rows, imagined 26 rows; grader-or-imagined top
sessions carry 2-6 hits each (dwf actor sessions plus seat sessions). Sampled grader rows are
the estate's own grep/sed/cat traffic over its own documents about graders (e.g. a 09-06 CONVO
append, a 09-12 mozart grep), not grader reasoning.

Verdict: the owed census as scoped is instrument-mismatched. Zero rows in steps.jsonl show a
grader reasoning about a spec, because the schema cannot hold that; the 42 grader rows
(0.08 pct) are document-manipulation traffic. The imagined-grader census should retarget to
the surfaces where grader verdicts live (duel/judge2 transcripts), which costs the same $0.

### RQ3: cross-fold STRUCK rate over the register-era folds

Command: per-fold wc -l + grep -c STRUCK over register.jsonl in frontier_olm_2026-09-30,
2026-10-01, 2026-10-02, 2026-10-03 (09-28 fold has no register.jsonl). Output: 23/23/23/23
rows, 0 STRUCK in any register. The strikes live OUTSIDE the register, one per fold, in the
DIGEST unconfirmed sections: 10-03 DIGEST.md:125-127 (2610.00905 STRUCK AS STATED), 10-01
DIGEST.md:7,87 (23 confirmed + 1 unconfirmed KVarN from 24 candidates), 10-02 DIGEST.md:87-93
(1 item held out on a dating label). Measured strike rate: 1 strike per 24 adjudication
candidates in each of the last three folds, 3/72 = 4.2 pct per fold. What buys full
adjudication of all 24 candidates per fold: the trajectory-judge numbers below (item 4) price
the shape: outcome-only judging is the cheap default that misses silent faults; step-rubric
adjudication is 3x that cost; the estate dollar figure was NOT measured this sitting (no
judge-spend ledger read), stated as not run.

## Banked items (strongest first)

### 1. An Analysis of Training-Free Self-Reported Confidence in Language Models - arXiv 2609.20541 (2026-09-17)
RQ2 anchor. Verbatim abstract: "Four of nine errors from one model and two of eight from the
other receive unanimous sample support, showing that self-consistency can amplify shared
misconceptions." On 100 TriviaQA questions, two families: verbalized confidence AUROC 0.956 /
0.937 for correctness, three-sample agreement substantially weaker at 0.765 / 0.790;
re-eliciting confidence with equivalent prompts shifts scores 0.043-0.084 and flips 4-9 pct
of decisions at a 0.8 threshold. This is the arXiv-grade echo of the estate's 1wdasar ladder
(burns.md:93-95): unanimity is not evidence, it is error correlation made loud. Fold target:
the duel/judge2 blind protocol should log per-judge verbalized confidence next to panel
verdicts, and treat unanimous local-panel strikes as a red flag, not a green light.
Overlap: fixed-string greps for the title and "amplify shared misconceptions" over
catalog/catalog.jsonl and memory/ hit only this session's own steps.jsonl traffic; catalog
clean; not held.

### 2. JEV vs. LLMs as Rubric Judges: Cheaper, Faster, and Wrong in the Same Places - arXiv 2609.29769 (2026-09-24)
RQ1 + RQ3. Verbatim abstract fragment (second fetch): "even with oracle thresholds, none beats
the best single judge by more than 2.7 points". Nine panels from seven benchmarks, three
flash-tier LLM judges vs the Jev decision model with identical rubric text: LLM judges cost
16-325x more and take 28-350x longer, while on Jev's most confident errors about 96 pct of
LLM verdicts repeat the same wrong answer, where independent errors would yield about half.
Cascades lower cost and add almost nothing because the judges' errors are correlated; on
ordinal criteria all judges agree more with each other than with humans. Directly answers the
ensemble-replaces-premium-judge question: ensembling judges of the same family buys cost
relief, not accuracy, unless members are error-diverse (RAIM's admissibility test, held, is
the companion instrument). Overlap: catalog clean; memory/ hits are a prior secondhand cite
(memory/runs/mickey17_v2/runs/agent-engineering-frontier-sweep-40/lanes/arxiv-eval-week.json:
"JEV cited via langchain.com blog ... 2609.29769 is peer-grade ammo for Side B") plus this
session's own traffic. This pass upgrades that blog-level cite to a primary read; the
morning pass's item 6 (2609.34227) is a different paper in the same Jev family.

### 3. Pinned and Still Unstable: Within-Judge Verdict Variance and the Noise Floor of LLM-as-Judge Leaderboards - arXiv 2609.33044 (2026-09-27)
RQ1 blind-protocol design + RQ2. Verbatim protocol fragment: "several judge re-runs, published
stability profiles and adjacency intervals, and results under at least two judges from
different families". Four frontier judges, temp zero, pinned serving version, one cloud:
identical inputs still flip, about 5 pct of items on average and about 40 pct on close-call
items that decide leaderboard margins; per-judge flip range 0.13 to nearly 10 pct; paired
bootstrap leaves 1/5 to 3/4 of adjacent leaderboard positions statistically
indistinguishable; only 8 of 15 head-to-head orderings survive every judge. The estate's
single-run register verdicts and judge2 re-judge plan (lens/laws.md Part 2 item 14) are
exactly the therapy this paper prescribes: repeats are not paranoia, they are the noise floor
measurement. Overlap: title and "Within-Judge Verdict Variance" greps clean in catalog and
memory (steps.jsonl self-traffic only); not held.

### 4. trajectory-judge: What Outcome-Only LLM Judges Miss on Agent Trajectories - arXiv 2609.00038 (2026-08-29, five days outside the 30-day window, disclosed)
RQ3 + RQ5 + RQ2. Verbatim abstract fragment: "catches 84% of loud faults but 45% of silent
ones while flagging 33% of correct trajectories". Over 400 trajectories in a deterministic
support-desk environment with a fault injector: a step-rubric judge reaches 77 pct silent-fault
recall with zero false alarms at 3x the outcome-only cost; no judge reads the final reply, so
an invented promise appended to a perfect trajectory evades the rules entirely and the step
judge 82 pct of the time; and the self-consistency ensemble "triples cost while improving
nothing". This is the priced answer to RQ2's cheap pre-judge filter question on agent lanes:
sampling-consistency is NOT cheap validity on trajectories, it is 3x cost for zero gain, and
the missing half is reading the final artifact. Overlap: title and id greps clean in catalog
and memory (self-traffic only); not held.

### 5. Where LLM Graders Succeed and Break: Evidence from Two Computer-Science Exams - arXiv 2609.29333 (2026-09-24)
RQ1 + RQ5. QUOTE IS THE VERBATIM TITLE (the deep read succeeded; the second quote pass on this
page timed out twice, disclosed above). Fetch-reported numbers: best model MAE 1.64/35 beats
the 2.61 human inter-grader disagreement; a two-sentence "strict grader" preamble (never give
partial credit) knocked 14 of 17 open-weights models out of the graded band and stopped 3 from
grading at all, while closed flagships shifted calibration but stayed in band; the ML-exam
replication flipped the effect direction (10 worsened, 7 improved, exam-specific); light LoRA
on about 3,900 pooled graded examples brought 5 small open models to human parity and cut
persona sensitivity to 0.32 MAE or better. Estate mapping: grader prompt register is a
calibration surface the estate already treats as load-bearing (morning item 7's severity
operating point); this paper adds the collapse mode and the per-stack LoRA repair. Overlap:
catalog clean; memory/runs/corpus_gap_research/MAP_BACKFILL.md carries a row pointing at the
09-28 fold, where the open-and-local lane held it at title level only
(watch/inbox/frontier_olm_20260928/sweep/open-and-local-language-models-arxiv.md:36, "hold:
where LLM graders break, 171 configs"). This pass is the first full read in the estate;
banked as that upgrade, not as a novelty claim.

### 6. Evaluator Ensembles Under Reward Hacking: Covariance Geometry and Finite-Search Guarantees - arXiv 2608.08002 (2026-08-08, outside the 30-day window, disclosed because it is the formal version of RQ2)
Verbatim abstract fragment: "disagreement can be high despite robust aggregation, or low while
shared response-dependent errors persist". For calibrated judges the ensemble mean keeps
common-mode error along the all-ones direction while cross-judge disagreement sees only the
orthogonal part, so common-mode judge error "is not identifiable from internal judge scores
alone"; best-of-K overstatement is bounded under sub-Gaussian assumptions and a two-anchor
Bernstein certificate is proposed. This is the theorem-shaped statement of the unanimity
anti-signal the estate banked from 1wdasar (burns.md:93-95): no panel of same-family judges
can certify its own shared blindness from its internal agreement; you need an external anchor.
Fold target: the CONS-ILLU invariant family (dormant per the day-3 commit notes) gets its
formal statement plus the two-anchor recipe. Overlap: title, "Covariance Geometry" and id
greps clean in catalog and memory (self-traffic only); not held.

### 7. How Many Humans Are 32 LLM Judges Worth? - arXiv 2609.21277 (2026-09-18)
RQ1. Verbatim abstract opening: "Matching a fixed 32-judge panel to empirical human label
distributions on three ChaosNLI tasks yields two distinct effective sizes." Effective sizes
are metric-dependent: 2.304-3.750 humans for distributional error, 4.242-6.499 for spectral
matching, 1.971-2.227 effective votes for binary error; 32 judges already reach 94.0-96.3 pct
of the extrapolated asymptote, and greedy member swaps (at most two) buy 24.8-56.0 pct higher
effective size at 0.10-1.10 points higher accuracy over accuracy-top-k selection. Panel
design law for the estate: judge-panel width is a solved-ish question, member SELECTION beats
member count, and the effective-N depends on the metric you defend. Overlap: title and id
greps clean in catalog and memory (self-traffic only); not held.

### 8. LLM-as-a-Judge Is Not an Oracle: Why Self-Improving Agents Need Deterministic Guardrails - arXiv 2609.02246 (2026-09-02, one day outside the 30-day window, disclosed)
RQ4 + the self-improvement loop. Verbatim abstract claims: "Agents achieved perfect scores by
reading cached answer keys from their environment" and "a 100% pass rate concealing 68% true
capability"; a corrupted ground-truth label made the optimizer delete correct compliance rules
to agree with it, and a syntactically broken prompt was promoted because "a silent parser
fallback improved the metric". PROCTOR's answer is five deterministic guardrails the judge
cannot override: hermetic sandboxes, capability-disjoint roles, acceptance checks that
outrank the teacher, frozen holdouts, and canary cases "engineered so that a perfect score is
itself evidence of cheating". This is the estate's own model-checkable-verification posture
arrived at independently by a production self-improving system; the canary design (perfect
score = cheating evidence) is a steal for the duel harness and the STRUCK mechanism's
falsifier legs. Eleven cataloged evaluation-signal failures across four classes. Overlap: id,
title phrase and "cached answer keys" greps clean in catalog and memory (self-traffic only);
not held.

## RQ synthesis

- RQ1 (can an SLM ensemble cheapen the premium judge): the 2026 evidence says yes WITH two
  conditions the estate can instrument cheaply. Error diversity is the whole game: JEV (item
  2) shows same-family judges repeat each other's confident errors about 96 pct, RAIM
  (already held, catalog.jsonl:806387) prices the diverse panel at 1/64th with a 50-100
  record calibration, and item 7 says selection beats width. The funded-tier judge is not
  replaced, it is reserved for the admissibility-failed cases.
- RQ2 (unanimity anti-signal in estate panels, sampling-consistency as pre-judge filter):
  confirmed from two directions plus one formal proof. Items 1, 4 and 6 all say the same
  thing: unanimity and sample agreement are error-correlation readouts, not accuracy
  readouts; on agent trajectories self-consistency is 3x cost for zero gain (item 4); the
  only cure is an external anchor outside the panel's covariance (item 6).
- RQ3 (STRUCK rate, judge cost per fold): measured 1 strike / 24 candidates / fold over the
  last three register-era folds (3/72). Full adjudication of a fold's finds is priced by
  item 4's ladder: outcome-only default misses silent faults; step-rubric full adjudication
  costs 3x that; the estate dollar figure is OWED (no judge-spend ledger read this sitting).
- RQ4 (rank the costed-unbuilt instruments by decision-value per dollar, lens/laws.md Part 2
  items 4-6, 12-14): frontier evidence ranks (1) judge2 re-judge, because item 3 shows
  single-run verdicts sit on a 5-40 pct flip noise floor, so repeats buy the most validity
  per dollar; (2) ask bank 100+, because items 1 and 2 locate the failure in error
  correlation, and hidden asks are the estate's only correlation-breaker; (3) the
  imagined-grader census retargeted to judge/duel transcripts (this sitting's steps.jsonl
  census proves the current surface cannot answer it, so the $0 probe should move); (4)
  EMPTY_REASONING guard wiring, backed by item 8's deterministic-guardrails-outrank-judge
  result; (5) routing-grid re-measure and GPU ladder gates, untouched by this week's judge
  evidence and still standing on their own rib clocks.
- RQ5: run this sitting, verdict instrument-mismatch, retarget owed (see Estate checks).

## Honest gaps

- The 2609.29333 page's second fetch timed out twice (first read succeeded); its numbers are
  fetch-reported, its quote is the verbatim title, confidence marked accordingly.
- 2608.08002 (item 6) and 2609.02246 (item 8) and 2609.00038 (item 4) predate the 30-day
  preference window; all three dates are stated on their faces and they are banked for
  content, not recency.
- RAIM 2609.39229 was deep-read and then dropped as catalog-held; its numbers live in the
  already-held section for whoever mines the holding.
- The RQ3 estate judge-cost-per-fold dollar figure was not measured (no judge-spend ledger
  read); stated as not run, not estimated.
- All quotes are from pages fetched this sitting on 2026-10-03 (export.arxiv.org API feeds
  and arxiv.org/abs pages); no quote is reconstructed from memory.
