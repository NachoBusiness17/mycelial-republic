# swarm-orchestration arXiv sweep (frontier gopher, 2026-10-11, second mint)

source-fetched: adhoc. Area: swarm-orchestration via arxiv. This file supersedes the
2026-10-10 mint of this same path (read in full this sitting before overwrite); the
prior mint's six banked items are NOT re-banked below except where this run re-read
the paper end to end and the re-read carries a verdict or a correction the register
lacks. Every paper banked or verdict-issued below was fetched and read by this seat
this sitting; nothing is carried from the prior mint's word alone.

Doors status: the arXiv API (export.arxiv.org/api/query) worked all window (three
queries, no 429), unlike the 10-10 run's hard-429 wall. Full-body reads went through
arxiv.org/html/<id>v1; two fetches timed out at 60s and succeeded on immediate
retry, one v2 URL 404'd and v1 served. No door degraded enough to need the
WebSearch fallback for reads; the recipe's listing door was not needed (API covered
the sweep).

## Pass 1 (broad sweep, 55 unique candidates, last 30 days)

Three API queries this sitting: (a) id_list for the five named adhoc-register
papers; (b) cat:cs.MA AND abs:"large language model", 30 results by submittedDate
desc; (c) abs:"multi-agent" AND abs:"orchestration", 25 results. After dedup the
union is 55 unique items, all dated 2026-09-26 through 2026-10-08 (inside the
30-day window). Beyond the nine deep-read items below, the strongest remaining
candidates held for a future window: Theory of Scene 2609.32939 (symmetry trap in
homogeneous concurrent agents, DivvyBench 71.1 to 99.6), DEALS 2609.33768
(decentralized expertise-aware load serving, no central router), LLMs Trust Their
Own 2609.33495 (in-group consensus increases conformity to wrong answers across 12
models; CoT suppresses it), Absorbing State Phase Transitions 2609.38327 (critical
communication degree above which wrong hypotheses stop spreading), Recursive Social
Improvement 2609.38516 (copying makes peer learning cheaper but concentrates
discoveries), Population Physics 2609.33871 (phase transitions in LLM societies),
S1-MAS 2610.08155 (cheap coordinator + capable workers, up to 97.2 percent token
cut), MIRROR 2610.02349 (k-route quorum hashing, 0 percent attack success at 1x
cost), WorkflowOps 2610.07860 (collaboration priors cut routing calls 80 percent),
Humanize 2610.08900 (deterministic hooks + plan contracts + 72 gates, contest
scores). Full enumeration available in this session's API fetches; not re-listed
here at length to keep the record to what this run verified.

## Pass 2 (nine papers read end to end this sitting)

2610.12176 MASS, 2610.10126 MAScope, 2610.09037 Governor, 2610.12436 Ecology,
2610.10468 Society (the five named by the ask), plus 2609.39211 RHEON, 2609.34017
Maat, 2609.40303 minimal-harness, 2610.08647 SquidAgent.

## RQ1: can flock consensus become a correctness signal?

NEW FIND, the strongest of the window: arXiv 2609.39211 "Consensus and Factual
Dynamics in Large Populations of Interacting Language Models" (Ricco, Onofria,
Sammartino, Di Pietro; KAUST / U Pisa; 2026-09-30). They built exactly the
decode-to-output-space instrument our mindsweave rib owes: each agent carries a
factual spin tagged correct/hallucinated in the ANSWER space by an independent
judge (Qwen2.5-72B, human agreement 87.6 percent, kappa 0.76), plus a semantic
embedding spin. 2,160 runs, 4,767,840 LLM calls, geometry ladder ring/torus/MF,
temperatures 0.1 to 1.6, frozen Qwen3-14B population. Verdict against our redesign
hope: even with the decode mapped into the true output space, "semantic agreement
correlates positively with factual convergence, and interaction strengthens the
association, yet never enough for unanimity to certify correctness" (their
abstract). Their discussion sharpens it: "the most cohesive states we observe are
the confidently wrong ones." Cohesion-accuracy Pearson peaks at +0.36 (2D,
N=256). This is external, mechanism-grade validation of our law
(RIB_MINDSWEAVE_EVAL_CONSENSUS_ILLUSION: high-strength consensus wrong 3/3): the
redesign makes consensus a WEAK POSITIVE signal (r rising +0.09 to +0.15 pooled,
peak +0.36), never a certificate. Two extra steals: (1) temperature x topology
interaction: the hallucination-minimizing temperature depends on coupling (dense
mean-field wants T near 1.0 so noise lets a correct minority escape a wrong
consensus; large local lattices want T=0.1); cold + dense can freeze total shared
hallucination. If our flock ever re-tries consensus, the dial is sampling
temperature by topology, not prompt strength. (2) repair dominates: a hallucinated
majority is not stable, correct minorities pull populations back (unlike a voter
model); only ~5 percent of runs amplify error. Cheap: their whole campaign cost
~$540, truncation at t=4 saves 54.5 percent of calls.

## RQ2: does emergence compound (the longitudinal record)?

Two deep reads, opposite signs at two layers, and the estate's five-axis protocol
remains the right instrument. NULL SIDE: arXiv 2609.40303 "How Much of a Harness
Does a Strong Agent Need for Autonomous ML Engineering?" (Brilliantov,
Hernandez-Cano, Abbe; EPFL + Apple; 2026-09-30): "under an equal time budget and
the same frontier LLM backbone, open-source state-of-the-art harnesses provide no
advantages over a single session of a minimal-harness coding agent baseline,
pointing to the backbone as the primary driver for performance." Multi-agent
interventions on their ladder HURT: base Malena 66.51 percentile vs +Delegation
63.62 and +Broadcast+Parallel 58.91 (fixed14, 24h, medal rates 55.7 / 45.2 / 33.3
percent). Only the small backbone (Gemma 4 31B) benefited from hand-crafted
harness priors; parallelism raised the oracle ceiling (71.79) but widened the
self-selection gap, canceling the gain. That is the deterministic-arm-stays-flat
picture with the single session AS the flat arm, on 30 MLE-bench + 40 NatureBench
tasks, with CIs. POSITIVE SIDE (training layer, not runtime): MASS 2610.12176
re-read: the multi-agent student M+ (28.82M processed tokens, 68.3 percent win
rate) beats the single-agent S++ (42M tokens, 64.0 percent) with 31.4 percent
fewer tokens; multi-agent traces are more training-efficient even where runtime
scores decline (Terminal-Bench 37.5 to 35.2, SWE-bench Verified 62.6 to 61.1
across cycles). Synthesis for the estate: emergence does not compound at the
runtime-harness layer under a strong backbone (the null), but the BYPRODUCT
(multi-agent trajectory data) compounds at the weight layer. Our K8S
emergent-vs-deterministic A/B should measure both layers or it will answer the
wrong one. Note the null's own condition: same backbone, equal time; their cost
table has Malena at $12.12/run vs AiScientist $1.95, so cost-per-outcome axis
still favors some harnesses on cheap backbones.

## RQ3: do the adhoc register's five survive a read past the abstract? (all five read by this seat)

- 2610.12176 MASS: SURVIVES, and the register's corrected payload verifies. My
  independent read confirms: evaluator agreement 0.73 to 0.91 to 0.93 across
  cycles; score-per-output-token 1.2 to 1.6x on the four research benchmarks;
  win rates 53.9 / 69.9 / 60.8 percent; NO dead-salmon/random-workflow control
  anywhere (controls are single-vs-multi students and a generic-directive arm);
  the only external check is two withheld LLM judges (GPT-5.5, Claude Opus 4.8),
  still consensus-class evidence. Bottleneck claim verbatim: "our main claim is
  optimizer capacity, rather than the evaluator capacity, can be a bottleneck in
  the speed of RSI." The contracts-and-hops migration holds: "roles and
  instructions become less task-specific, while contracts and hops become more
  task-specific." Verdict: banked row 1 stands; the falsifier (random-workflow
  control) remains OUR test, not theirs.
- 2610.10126 MAScope: SURVIVES with one hygiene note: the paper has NO explicit
  limitations section (their caveats live inside results text: LOFO mixes
  framework and topology shift; Inject-Mix labels are injection-derived). The
  chi-square 409.9, dof 39, p = 1.2e-70 on 851 MAST-clean traces verifies, as do
  the per-topology residual modes and the cheap-judge economics ($0.63 vs $10.26
  per 1000 traces; gpt-mini 0.346 Macro-F1 with predicted topology = 94 percent
  of gpt-5.4 trace-only 0.372). Cross-framework transfer is the weak leg: Flat-GBM
  0.490 to 0.226 under LOFO; topology recovery on SMP is 56.9 percent. Steal
  stands: topology-conditioned priors make a cheap judge nearly frontier-grade
  for failure triage.
- 2610.09037 Governor: SURVIVES. The EWMA backoff rule verifies exactly: EWMA of
  induced failures with lambda 0.3 (r_new = 0.7*r_old + 0.3 on induced failure),
  regulation applied with probability p_apply = 1 - min(1, k*r), k in {1.5, 3,
  6}. Stochastic substrate: no-governance 0.31, cost-blind 0.19 (WORSE than no
  governance), cost-aware 0.40, rate-matched fixed 0.30. Gemini 2.5 Flash arm
  (576 episodes): blind 0.33 vs cost-aware k=3 0.75 at alpha=2. Oracle caveat the
  register under-weighted: the backoff consumes ORACLE labels of induced events;
  the paper's own limits say whether such costs arise naturally is open, one
  model, six related tasks, 8 repeats, no CIs, k=3 vs k=6 gap is two episodes of
  48. Estate replication must self-label induced failures (the gate's own
  regression tests are the label source) or the law imports an oracle.
- 2610.12436 Ecology: SURVIVES as a frame, with its own honesty intact: "toy"
  model, worked example Ncrit about 463 at N_ref=16 (p_ref 0.10, p_crit 0.20,
  beta 0.035), the deployment gap (published multi-agent cyber data tops out at
  16 agents while OpenAI reportedly ran ~10,000 concurrent agents on
  Navier-Stokes, Sept 2026), and population pacing (step width up while measuring
  capability-vs-N, re-estimate per model generation). Their own appendix warns
  the three-agent-count fits "should not be extrapolated to larger populations."
  Banked row 5 stands as the width-ceiling frame; no new mechanism.
- 2610.10468 Society of Researchers: SURVIVES and CLEARS THE NO-THRONE BAR by
  design. Re-read verbatim: "The mayor tells no principal investigator what to
  work on, and once a call is open, no human needs to act until results arrive."
  Allocation-not-assignment, declines as first-class records ("a decline is a
  complete document that argues against doing the work"), three independent
  single-question judge personas, skeptics never exchanging messages with the PIs
  they check, lottery band against cumulative advantage. The C5 episode (an agent
  adopted another lab's in-flight experiment as its own on shared compute) and C1
  admission ("We have not yet compared a society against a swarm or a planner
  under matched compute") both verify. Their compute claim is one lab's report
  (17 percent lower perplexity at ~30 percent less compute), not a controlled
  arm. Of the five, this is the one whose institutional grammar the estate can
  lift wholesale for the flock's claim/precommit layer.

## RQ4: do the banked EWMA width-shaping and width-pricing laws replicate on the estate's fan-out shape?

The estate's measured shape (given by this ask, per the gala/burn-wave receipts):
workflow children at max_concurrency 10, 50 children clean for hours, first
rate-limit contact is a HOLD signal, not a width cut. Three deep reads map onto
it: (1) Governor 2610.09037: the estate's HOLD-not-cut IS the cost-aware backoff
shape: intervene less as the measured disturbance (429/1302 rate) rises; the
cost-blind twin (cut width on first contact) is their 0.19-collapse arm. Replicates
qualitatively; the estate's version needs no oracle if the ledger's 429 events are
the label. (2) Maat 2609.34017 re-read (banked by the 09-30 swarm sweep as half
the EWMA pair; this is the first read past its abstract by any sweep seat): the
deterministic-governance optimism must be discounted: hand audit of 94 governed
halts found 35 false alarms (37 percent); v1 scorers "credited any early halt as a
prevented defect"; under lower-bound scoring "the governed arm [falls] below
ungoverned in four of six workflows" (paired gains +7.7 to +29.1 percent
otherwise); single model (Claude Haiku 4.5), synthetic workflows, small paired n.
Their own line is the law to steal: "determinism is not the same as correctness: a
wrongly configured deterministic rule can reproducibly produce the wrong verdict."
Our exit-2 gate needs its own halt audit the way Maat's v2 needed one. (3)
SquidAgent 2610.08647 (NEW; NeurIPS 2026; Sydney/MBZUAI/UTS): a width-PRICING
rule with numbers: parallelize a layer iff rho_hat = serial-token-sum / (critical
path + alignment cost) > alpha = 1.9; fork workers from the orchestrator session
so re-exploration cost ~0 (our frozen-prefix cache law is the same move); 2.2x
mean throughput and 2.6x wall-time over Claude Code at quality 98.2 +/- 2.1
percent; token budgets predict duration at rho = 0.77 vs wall-clock 0.16. The
estate's shape (independent per-item asks, forked from a shared frozen ask, low
cross-item alignment) sits deep in the parallelize regime of their rule, which is
consistent with 50-clean-children; their rule prices the boundary our
first-429-HOLD policy currently senses blind.

## RQ5: hidden ask bank from ~20 to 100+

No external paper grows our bank; this remains estate work (cheap-seat drafting,
operator review, hidden reveal). Adjacent signal from this window's Pass 1 (abstract
level only, not deep-read): the astronomy reproduction paper 2609.35900 warns
"matching published results doesn't validate reasoning reconstruction" (11 of 13
Nature papers had ambiguous methods), which is the contamination argument for why
the bank must be UNSEEN asks, not repackaged public benchmarks. Nothing banked.

## Overlap record (commands run this sitting)

Catalog + memory greps: for each of 2609.39211, 2609.40303, 2610.08647, 2609.34017,
2609.33495, 2609.38327: grep -c <id> catalog/catalog.jsonl; grep -rl <id> over
memory/frontier memory/press memory/lenses memory/rib memory/improve
memory/workflows memory/burns; plus grep -rl over watch/inbox and corpus/steal
for 2609.39211 and 2609.34017. Findings: 2609.39211 = ZERO holdings (catalog 0,
mapping dirs 0, corpus/steal 0, no state/arxiv stub; only hit anywhere is
memory/trajectory/steps.jsonl, a workflow instrument log naming it in a command
string, not a holding). 2609.40303 = catalog row 69b706a936df, the
state/arxiv/2026-10-01 abstract stub (1353 bytes) only. 2610.08647 = catalog row
07dc89e31665, the state/arxiv/2026-10-07 abstract stub (2067 bytes) only.
2609.34017 = NOT in catalog; banked by
watch/inbox/frontier_olm_2026-09-30/sweep/swarm-orchestration-arxiv.md (confirmed
by grep) and named in the 10-09 fold per the adhoc lens burns.md:89-91; this run's
Maat entry is the read-past-abstract verification, not a re-bank. The five named
papers = adhoc register.jsonl rows 1-5 + the prior mint of this file; my entries
below are verification verdicts on those rows, explicitly marked.

## Ranked items (the eight-or-fewer JSON cut)

1. 2609.39211 RHEON (new; RQ1 answered with a mechanism and 4.77M calls)
2. 2609.40303 minimal-harness (new; RQ2 null side, the strongest anti-emergence
   evidence this window)
3. 2610.08647 SquidAgent (new; RQ4 width-pricing rule with numbers)
4. 2609.34017 Maat (banked 09-30; first read past abstract: 37 percent false
   alarms, scorer flaws, determinism-is-not-correctness)
5. 2610.12176 MASS (register row 1; verdict survives, all register numbers
   re-verified, falsifier still ours)
6. 2610.10126 MAScope (register row 2; verdict survives, no-limitations-section
   hygiene note, LOFO weak leg named)
7. 2610.09037 Governor (register row 4; verdict survives, EWMA rule verified to
   the formula, oracle-label caveat elevated)
8. 2610.10468 Society of Researchers (register row 3; verdict survives, clears
   the no-throne bar by design)

Ecology 2610.12436 (register row 5) also re-read and verified but cut from the
eight by strength; its verdict stands in RQ3 above.
