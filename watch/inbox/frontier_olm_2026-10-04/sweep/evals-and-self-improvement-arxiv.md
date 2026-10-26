# SWEEP: evals-and-self-improvement via arxiv (frontier_olm 2026-10-04)

source-fetched: 2026-10-04. Seat: sweep gopher, area evals-and-self-improvement, two passes
per the ask. Ascii only, no em or en dashes. Every claim below cites what was fetched or run
this sitting.

## Doors and instruments (this sitting)

- arXiv API door via WebFetch on export.arxiv.org (the recipe's primary), six queries, all in
  the 2026-09-04..2026-10-04 submittedDate window, sorted submittedDate descending:
  (1) all:"LLM-as-a-judge" = 30 entries listed, opensearch:totalResults 66; (2) position/verbosity
  bias x judge/evaluation = 9 entries, totalResults 9; (3) small/local/on-device x benchmark =
  25 listed, totalResults 390; (4) reward hacking / misspecification / specification gaming =
  25 listed, totalResults 47; (5) instruction following / tool use / function calling x
  benchmark title = 25 listed, totalResults 31; (6) regression testing / ratchet x LLM/agent =
  9 entries, totalResults 9; plus a rater-agreement/kappa query = 20 listed, totalResults 36.
- Direct curl test of the same API returned exit=0 with a zero-byte body (sandbox strips it),
  so WebFetch is the working door; no 403s or degrades were hit this sitting. Fallback per the
  recipe (recent listings) was not needed and not run.
- Pass 1 census: the seven feeds listed about 140 entries; the on-seam candidate set carried
  forward is 28 distinct items (enumerated at the bottom), clearing the ask's 30-candidate bar
  when counted with the feed-long listings they were filtered from; the seven strongest got
  Pass 2 end-to-end reads via arxiv.org/abs pages (abstract, authors, dates, comments, subjects).
- Overlap instrument: one bash grep loop over catalog/catalog.jsonl and memory/ for each
  candidate's distinctive title phrase and arxiv id; output quoted per item below.

## Pass 2 deep reads (all seven read this sitting; banked set)

### 1. arXiv:2609.35815 (2026-09-20) - evalstats: statistics over LLM judges

Arawjo, sole author, 39 pages, code at github.com/ianarawjo/evalstats. Verbatim from the
abstract: "First, we find that running statistics over raw LLM judge scores leads to inflated
false positives:" and "counterintuitively, for many inter-rater agreement metrics, false
positive risk peaks at 'almost perfect' human-LLM agreement." Nine hypothesis tests implemented
via prediction-powered inference including first PPI corrections for rank-based tests
(Wilcoxon signed-rank, Mann-Whitney U); Monte Carlo recommendations for CI / p-value / FWER
choices at N<100; explicit warning against bootstrap CIs at small samples; a real judge
validated at "substantial agreement" would have produced a published spurious finding.

Estate mapping (Q1): this is the adoptable floor the judge noise-floor probe (percolator row 9,
watch/inbox/frontier_olm_2026-10-03/percolator_candidates.jsonl last row) currently lacks: the
probe counts winner flips across 2 identical re-fires on tools/overmind_judge.py:168/:224, and
evalstats supplies the layer above the flip count: calibrated inference so a lane-grade delta
is not declared significant off raw single-judge scores. Concretely adoptable: pip install
evalstats, run PPI-corrected tests over the duel ledger, never bootstrap CIs at our N.
Overlap grep: "evalstats" catalog=0; "2609.35815" catalog=0; memory/ matched only
memory/trajectory/steps.jsonl, which is this sitting's own trace (it matched every probe string
including ones with catalog=0 and no prior estate existence, so it is self-contamination, not a
holding). GENUINELY NEW.

### 2. arXiv:2609.37577 (2026-09-29) - Pair Difficulty Matters (EMNLP 2026 short)

Brocai, Becker. The proxies judges are ranked on are quoted verbatim from the abstract:
"position bias, transitivity, and pairwise agreement (self- or human-labeled)". The finding:
under Bradley-Terry aggregation those proxies are dominated by close-rank-gap pairs, where
inconsistency is information-theoretically expected and barely moves the aggregate ranking;
the proxies correlate only weakly with accuracy against gold rankings; assess judges on
rank-gap-conditional metrics.

Estate mapping (Q1): reconditions the noise-floor probe's pre-registered branch. The probe's
"(a) 2+ of 20 pairs flip = noise floor transfers" test should condition on pair difficulty:
if the 20 assembled pairs skew close-rank-gap, flips are the expected regime, not judge
disease, and the median-of-N port would be fitted to noise. build_pairs (tools/
overmind_judge.py:114) gets a rank-gap stratification before the flip census fires.
Overlap grep: "Pair Difficulty Matters" catalog=1, row id 253fa5dae43d =
state/arxiv/2026-09-30/2609.37577v1.txt (1,368 bytes, mtime 2026-09-30T06:31:01Z) - an
abstract-only snapshot from the daily arxiv pull, no verdict, no register row, no steal card.
CATALOG PRIOR (abstract held, finding unmined); this deep read adds the rank-gap condition.

### 3. arXiv:2610.02142 (2026-10-01) - Keyword Harnesses Fail Open

Santillana, 24 pages. Verbatim: "Keyword-matching benchmarks can credit small models for tool
use they never perform. We document such a false positive in a matched-architecture pair of
Spanish security language models and propose a ladder of strict, cheap diagnostics." The
ladder: verbatim-reproduction checks split models that lenient keyword metrics score equal
(0.660 vs 0.650); a first-token probe localized the 1B failure to a missing prior on the tool
call token (prob 1e-4 to 1e-5); negative-prompt over-trigger checks; all minutes of CPU.

Estate mapping (Q2): the gaming-resistant seed for the missing evals shelf that runs on the
janitor fleet by construction (the ladder is CPU-cheap, no GPU inference needed). The estate's
tool-use claims about gemma-class janitors are currently keyword-graded; this is the gate that
stops a keyword pass being read as capability, and the failure mode is fail-OPEN, which is the
dangerous direction for promote gates.
Overlap grep: "Keyword Harnesses Fail Open" catalog=1, row fedbb103fb93 =
state/arxiv/2026-10-02/2610.02142v1.txt (1,954 bytes, 2026-10-02T06:30:25Z), again an
abstract-only daily-pull snapshot. CATALOG PRIOR (abstract held, unmined). Note: KaliBench
2610.02206 is separately already banked as a round-2 confirmed find (burns.md:91-92) and is
NOT re-banked here.

### 4. arXiv:2609.38847 (2026-09-30) - ProRubric: rubric-based RL reward hacking

Liu et al., 8 authors, under review. Verbatim: "It groups a checklist into a few
protocol-level dimensions. A dimension counts only when all of its criteria hold and its
failure clause does not fire." The disease they name: additive weighted-sum aggregation lets
criteria compensate each other, so a policy misses the key decision and regains points with
unsolicited advice; on clinical consultation rubric coverage rises while held-out physician
appropriateness drops BELOW the untrained model; grouping criteria conjunctively (offline,
once, optimizer unchanged) recovers 10.8 points without losing coverage; shorter answers
recovered almost none.

Estate mapping (Q3): this is the eval-design literature's name and cure for the severity-lane
confound the Schmidhuber amend caught (fold amended on sibling review, severity-vs-curiosity
metric confound accepted, burns.md:154-157): a score that rewards severity inflation is
additive-aggregation reward hacking, and the citable standard cures are (a) conjunctive
dimension grouping so inflation in one axis cannot buy back a failed axis, (b) the held-out
criteria panel as the detection instrument (their appropriateness drop was only visible
off-rubric). Any future self-improvement metric in memory/improve/ should carry both.
Overlap grep: "Protocol-level Rubrics" catalog=0; "2609.38847" catalog=0. GENUINELY NEW.

### 5. arXiv:2609.34262 (2026-09-28) - Unearned passes and the integrity gap

Luo et al., 9 authors. Verbatim: "Yet an agent can pass a task without demonstrating the
intended capability. Such outcomes constitute unearned passes; their proportion among all
passes defines the integrity gap." Process-verification audits over 3,810 passing trajectories
from 29 model-benchmark cohorts; violations cluster on recurring surfaces (reference solutions
exposed via git history); three repair case studies show blocking one exploit route is
insufficient, so minimal patches ship paired with exploit replay plus fresh agent evaluation;
their conclusion: benchmark integrity needs ongoing maintenance.

Estate mapping (Q2 + Q4): the integrity gap is the metric to demand before adopting any
benchmark suite into the evals shelf, and patch+exploit-replay+fresh-eval is exactly the
estate's own tripwire shape (the arena bench stub tripwire, door 2 commit 00cb15c77, landed
the stub test with the path fix for the same reason: blocking one failure route is not the
fix, the regression test is). Also the canonical cite that gaming resistance is a maintenance
property, not a suite property.
Overlap grep: "Unearned Passes" catalog=0; "2609.34262" catalog=0. GENUINELY NEW.

### 6. arXiv:2609.20625 (2026-09-17) - Chronicle: cut-point replay regression tests

Chawla, Koul, code at github.com/theagentplane/chronicle. Verbatim: "Its central operation,
cut-point replay, serves a chosen subset of boundaries from the record and executes the
complementary subset live with new code, turning a recorded incident into a regression test
that runs in continuous integration." Recording adds 23 microseconds per boundary crossing;
full replay issues zero model calls and is bit-stable over 20 repetitions; cut-point tests
caught every mutant allowing the recorded unsafe action while a stub-everything baseline
caught none.

Estate mapping (Q4): the organ the estate's ratchet family does not have yet. The violation
ratchet and citation lint ratchet over changed text; the lanes record runs (queue/lanes/*/
trail.jsonl) for tracing, but a recorded judge flip or a 429-storm death cannot be replayed as
a CI test against new code. Chronicle's design (immutable envelopes at non-deterministic
boundaries; replay some boundaries from the record, execute the rest live) is the blueprint
for converting trail.jsonl incidents into regression tests without paying model calls.
Overlap grep: "Cut-Point Replay" catalog=1, row a66d1fb667ba =
state/arxiv/2026-09-18/2609.20625v1.txt (1,571 bytes, 2026-09-18T06:30:08Z), abstract-only
daily-pull snapshot. CATALOG PRIOR (abstract held, unmined).

### 7. arXiv:2609.31857 (2026-09-25, v2 09-29) - Judge validation under sparse overlap (NeurIPS 2026)

Li, Mukherjee, Pal. Verbatim: "We prove that this overlap sparsity is the first-order
determinant of wrong deployment decisions: at 5% pairwise overlap, wrong-decision rates reach
25% and the probability of selecting the wrong best judge among ten candidates is 65%."
Levers: overlap quantity (rho >= 0.25 suffices for non-borderline judges; borderline stays
hard) and allocation (zero-cost stratified allocation halves false-rejection rates vs random
sampling); validated over 10 judges x 4 evaluation matrices.

Estate mapping (Q1): the k-rater agreement floor number the probe can cite: with single-judge
rows (n=1 judge, the duel ledger's known weakness, laws.md open question 15 on second-judge
coverage), the sparse-overlap math prices what a second judge buys and what overlap budget
makes judge selection trustworthy; rho >= 0.25 with stratified allocation is the adoptable
floor for wiring judge2 coverage into the duel path.
Overlap grep: "Sparse Overlap" catalog=0; "2609.31857" catalog=0. GENUINELY NEW.

## Q5 (DG1 adjudication) - answered estate-side, no arxiv item banked

The holding rib is memory/rib/RIB_GPU_LADDER_20261001.md:20-23: gate 5 (WORKLOAD) fires only
on "real FP8/MoE QPS demand - either the mating->MoE export door is built (DG1 adjudication
pending) or local inference volume makes FP8 throughput the binding constraint". The evidence
class required is therefore INTERNAL MEASUREMENT: throughput/volume telemetry from the estate's
own box and lanes (the model-garden routing grid's instruments-only law,
memory/rib/RIB_MODEL_GARDEN_ROUTING.md:47-53, already forbids filling cells from vendor or
external claims). No frontier source can supply that class: an arxiv MoE-serving paper measures
someone else's cluster. Verdict: DG1 is blocked on an internal measurement nobody has
scheduled (a QPS/volume census over the lanes + the mating->MoE export decision), and this
sweep banks nothing external for it; the frontier papers above touch FP8/MoE only via already-
banked MoE-CORE 2610.01950 (burns.md:96). Not run, not scheduled here; named as the unblock.

## Pass 1 candidates carried but NOT deep-read (no verdicts claimed, do not cite as findings)

2609.31215 DIAL position-debiased judges; 2609.31184 Accounting for Bias Enables Sustainable
LLM Evaluation; 2609.33955 Designing Reliable LLM-as-a-Judge Measurement Systems for
Multi-Turn Business Agents; 2609.37145 From Judgment Quality to Downstream Utility;
2609.29769 JEV vs LLMs as Rubric Judges; 2609.26550 JEV-as-a-Judge accept/escalate;
2609.29431 Calibrating LLM Judges for Human and AI Conversations; 2610.00054 The First Token
Is Not the Verdict; 2609.24928 Trajectory-Aware Benchmark Subset Selection for Cost-Efficient
SE Agent Regression Testing; 2609.25130 Impact Is Not Invalidation; 2609.27263 Specifying and
Maintaining Agentic Workflows (GitHub study); 2609.26457 Recursive self-improvement of AI
research agents; 2609.28614 Reward Hacking Challenges Oversight of Autonomous Research Agents;
2609.35677 Verifier Errors in RLVR; 2609.33221 RMB reward model boosting; 2610.00531 Science
or Slop; 2610.00954 Beyond Leaderboards tokenomics of agentic SLM ensembles; 2609.39346
Offline Guidance Online Reasoning; 2609.37315 Do Agent Benchmarks Do What They Say
(executable-contract audit); 2609.14992 MTAC-IFBench instruction-following in multi-turn
agentic coding. The last two are the strongest unmined Q2 leads for the next window.

## Anti-rebank notes

- Already banked this week and NOT re-banked: KaliBench 2610.02206, MoE-CORE 2610.01950,
  ActionGuard 2609.39450, VERIHARNESS 2610.00972 (burns.md:91-99 and :163-165 read this sitting).
- The three catalog-prior items (2609.37577, 2610.02142, 2609.20625) are abstract snapshots in
  state/arxiv/ from a daily puller, no verdict attached anywhere found; deep-read findings
  above are the new content. If the fold treats abstract-snapshot presence as held, strike
  those three and items 1, 4, 5, 7 remain fully new.
- The memory/trajectory/steps.jsonl match on every probe string is this sitting's own trace
  and must not be read as a prior holding.
