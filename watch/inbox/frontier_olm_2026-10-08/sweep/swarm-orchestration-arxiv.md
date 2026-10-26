# Frontier sweep: swarm-orchestration via arxiv (2026-10-08)

source-fetched: 2026-10-08. Doors used: arXiv API Atom feeds (export.arxiv.org/api/query, 7
queries rendered as text, zero 403s), arXiv abs pages (9 fetched and read end to end), 2
WebSearch queries (both returned rows; the pheromone query surfaced only an out-of-window
item). No door degraded this sitting.

## Pass 1 census

115 feed rows enumerated from 7 Atom feeds, all sorted submittedDate descending over
2026-09-08..2026-10-08 (the 30-day floor of 30 candidates is passed 3.8x):

1. all:"multi-agent" + all:"large language models": 25 entries (2610.10184 back to 2610.03010)
2. all:"majority voting": 20 entries (2610.09865 back to 2609.33855)
3. all:"LLM-as-a-judge": 20 entries (2610.09820 back to 2609.37145)
4. cat:cs.MA recent: 30 entries (2610.10527 back to 2610.07491)
5. all:stigmergy in-window: ZERO ENTRIES (feed totalResults 0)
6. all:"consensus" + cat:cs.MA: 20 entries (2610.10527 back to 2609.19208)
7. all:"swarm intelligence" + all:"language model" in-window: ZERO ENTRIES (totalResults 0)
Plus 2 WebSearch rows: pheromone/stigmergy+LLM (1 hit, arXiv 2601.08129, Jan 2026,
OUTSIDE the window); judge identity bias / blind evaluation (5 hits, all dated 2604-2608,
all outside the window).

The two zero-result feeds are a finding, not a failure: the pheromone-bus law
(tools/pheromone.py, lens/burns.md:145-147 ask-supplied) has NO fresh external analog in the
last 30 days anywhere I could reach. Nearest neighbor is 4 months old.

## Overlap gate (run before banking)

Instrument: grep over catalog/catalog.jsonl (id + distinctive-phrase patterns per item) and
over every sibling sweep file watch/inbox/frontier_olm_2026-*/sweep/swarm-orchestration-arxiv.md,
plus a full-tree grep over memory/ launched in background (title fragments, first four items
and DEFER1/JuryFlow/STEP-GATE patterns, second four). Catalog and sibling-tree results are
complete; the memory/ full-tree scan is filesystem-bound and its verdict is recorded per
item below where it finished, otherwise stated as partial.

- Clean (0 hits anywhere checked): 2609.39211 RHEON, 2609.38829 Diversity Combining,
  2610.06192 Copies or Sources, 2609.39912 TRACE, 2610.07816 STEP-GATE.
- Catalog-mirror only (abstract text held at state/arxiv/, never analyzed by any lane):
  2609.40103 JuryFlow (row 7f5fb871513a, state/arxiv/2026-10-01/2609.40103v1.txt, 2,074
  bytes), 2609.40190 Certifying Test-Time Scaling Curves (row 58fe109f8fbe,
  state/arxiv/2026-10-01/2609.40190v1.txt, 2,049 bytes), 2610.07657 Where Rules End and
  Judges Begin (row 6795b44920ba, state/arxiv/2026-10-07/2610.07657v1.txt, 1,359 bytes).
  The 10-07 lane explicitly listed 2610.07657 as mirror-held and did not bank it; no
  analysis of any of the three exists in the estate. I bank the deep reads with this
  overlap declared rather than silently.
- Excluded as already banked: 2610.04686 When Debate Helps carries a full section in the
  10-07 lane (frontier_olm_2026-10-07/sweep/swarm-orchestration-arxiv.md:30-32). I read it
  this sitting and fold its mechanism into the Q2 verdict below, but do not re-bank it.
  Also excluded on its one-line feed gist: 2610.02702 Silent Dissent (day-7 held-and-read)
  and 2610.03010 Engineering Sustainable Agents (day-7 item 5).
- False-positive overlap note: the phrase grep "DEFER" hits INTAKE_DEFERRED_SDF_20260918.md
  rows in catalog; those are unrelated (substring DEFER in a filename). "DEFER1" itself: 0
  hits.

## Pass 2: the 8 banked items (strongest first, all read via abs pages this sitting)

### 1. arXiv 2609.39211 Consensus and Factual Dynamics in Large Populations of Interacting Language Models (2026-09-30)
RHEON: a frozen model's population as an O(n) spin system, 432 configurations over prompt,
population size, topology (1D ring to mean-field), and temperature, swept into a 4.7
million-response tagged corpus (Eraclitus-4.7M). Semantic agreement correlates positively
with factual convergence and interaction strengthens the link, but it is "never enough for
unanimity to certify correctness". Initial state alone does not predict whether a
configuration reaches correct or hallucinated consensus, and the hallucination-minimizing
temperature depends on the coupling structure, so the near-greedy default is "not
automatically the safest".
Estate mapping: external, large-scale confirmation of the consensus-illusion law (0/3
wrong-at-high-strength, lens/laws.md:81-84 ask-supplied) AND a hard caveat on the Q10 decode
redesign (lens/laws.md:176-178): even a decode that maps consensus onto the task output
space cannot make unanimity a certificate; correctness prediction needs topology and
temperature context, not the vote alone. For the flock instruments this predicts the
consensus-strength meter needs a topology column before its readings mean anything.

### 2. arXiv 2609.38829 Diversity Combining for Multi-Path LLM Reasoning (2026-09-30, NeurIPS 2026)
Exact abstract text captured: "the pairwise correlation of path correctness caps the
design-effect effective sample size of the vote at a finite ceiling". GLS analysis shows
that under exchangeability the optimal symmetric linear combiner is uniform, so majority
vote is the natural default, while weighting or pruning pays only under heterogeneous
prompt-template branches. Prompt-template diversity reduced path correlation in 55 of 57
valid model/benchmark cells, strongest on open-ended QA. The Adaptive-K rule uses a
four-path pilot to select K*, retaining 96-103% of MV@32 accuracy across Math, QA, NLU.
Estate mapping: this is the missing design law for the gated width A/B (day-6 counter-
evidence, lens/burns.md:72-74 ask-supplied, DIGEST.md:17,:43): width is the wrong axis to
sweep alone. Correlation among siblings, not width, caps what a wider arm can buy; two
shapes at the same (model, prompt) correlation may be indistinguishable, and a decorrelated
narrow arm can match a wide one. Amendment the A/B should carry: fix or vary prompt-template
diversity explicitly across arms, and add a K-pilot (Adaptive-K shape) arm; without that,
the 1.25x/1.5x band measures correlation, not width.

### 3. arXiv 2610.06192 Copies or Sources? Measuring How LLM Aggregators Count Restated Evidence in Multi-Agent Systems (2026-10-05)
The aggregator "should count sources, not statements". Across three testbeds (message logs
with a Bayesian oracle, web documents with appended copies, agent-written logs under four
protocols), four models from three providers counted a restated copy as 0.06-0.42 of a fresh
reading, and on 5-40% of logs stating one reading three times the reported belief implied an
earlier commitment than the oracle makes. A one-paragraph declaration of what a copy
contributes drops copy weight to <=0.08 on controlled logs; a rule of referring to readings
instead of restating them cuts premature commitment from 11.2% to 1.1% while preserving real
corroboration.
Estate mapping: the MECHANISM under the consensus anti-signal (lens/laws.md:81-84): a flock
that relays one strong-remote verdict through three seats shows strength 3, not evidence 1.
"Count sources, not statements" is directly portable to the pheromone bus and the flock
reconcile stage: a mark re-read or relayed must carry its provenance so the tally counts
independent sources only, which is also the convergence bar the mosaic law already states
(sybil-form surfaces are ancestry, not convergence, lens/laws.md:111-113 ask-supplied).

### 4. arXiv 2610.07657 Where Rules End and Judges Begin: Measuring the Judgment Boundary in Multi-Agent Systems Security (2026-10-06)
DEFER1: "DEterministic-First Enforcement with Residual judgment" - five defense principles
as a 28-check deterministic cascade that blocks what it can and refers the residue to a
panel of four judges. Across four domains, attack success fell from about 30% to roughly 3%,
with 78% of blocked attacks handled deterministically; in the security-operations domain
only about a quarter of proposals reached the judges at all.
Estate mapping: the strongest published numbers for the Q3 probe-first port (probe monitors
97-99% recall vs judge 9, kappa 0.15, lens/burns.md:95-96 ask-supplied): a deterministic
first pass resolves most traffic and reserves the paid judge for the residue, and the
measured residual rate (~25%) is the sample-size denominator for what judge2 re-judging
costs. The 28-check cascade shape matches the estate's existing deterministic gates
(citation lint, ratchet, workflow gate) more than any new instrument.
Overlap declared: catalog mirror row 6795b44920ba at state/arxiv/2026-10-07/2610.07657v1.txt
(abstract bytes only); the 10-07 lane listed it mirror-held without banking; the deep read
and the Q3 mapping are new this sitting.

### 5. arXiv 2609.40103 JuryFlow: Disagreement-Guided Human-in-the-Loop Multi-Agent Evaluation (2026-09-30, HAI '26)
Treats judge disagreement "not as noise to be averaged away, but as a precise, claim-level
signal". Responses decompose into atomic claims, heterogeneous judges vote per claim, and a
disagreement graph (nodes scored by verdict entropy, edges by claim similarity) routes
minimal human (or automatic entropy-ranked) resolution; corrections propagate along the
graph and crystallize into rubric entries all judges inherit. Beats single-judge and
majority-vote panel baselines on MT-Bench and LLMBar gold-label agreement.
Estate mapping: the Q3 architecture, named: keep judge2 (second family, lens/laws.md:165-169
ask-supplied) only for probe-flagged disagreements. The disagreement graph is the missing
piece between "probe recall 97-99" and "judge for the flagged set": it decides WHICH
disagreements are worth a paid re-judge and lets the verdict generalize via rubric entries
instead of per-row re-judging. Dogfoodable on the next sweep's own review pass at $0: rank
this sweep's register rows by cross-seat verdict entropy before any judge2 spend.
Overlap declared: catalog mirror row 7f5fb871513a at state/arxiv/2026-10-01/2609.40103v1.txt
(abstract bytes only, never analyzed); no prior lane read it.

### 6. arXiv 2609.39912 TRACE: Trajectory Selection for Parallel Scaling of Search Agents (2026-09-30)
TRACE is "a lightweight learned selector that ranks completed trajectories using the search
evidence behind their answers": it links rollouts through shared content or document
identity, propagates evidence across those links, and each candidate answer reads its own
trajectory's updated state. On FRAMES, GAIA, BrowseComp it reaches 78.6% average accuracy,
"exceeding majority voting by 3.1 percentage points", comes within 0.4 points of 64-rollout
majority voting using 8 rollouts, and runs >=10x the throughput of generative aggregators
(SolAgg, SummAgg, AggAgent). One selector transfers across rollout policies and backbones.
Estate mapping: the Q10 decode redesign has a concrete published form: readout that uses
per-candidate evidence (provenance), not vote frequency. For the flock, the analog is a
selector over per-seat answers conditioned on each seat's cited sources, which is exactly
the material the party-turn provenance contract already preserves. Also a width result:
evidence-aware selection of 8 beats naive voting of 64, the same correlation-ceiling
conclusion as item 2 from the selection side.

### 7. arXiv 2609.40190 Cheap to Draw, Expensive to Trust: Certifying Test-Time Scaling Curves (2026-09-30)
"Sampling several answers and keeping the one a verifier scores highest is one of the
simplest ways to buy accuracy at test time", but scaling curves are "cheap to draw and
expensive to trust". The paired-audit design (exponential inequality on two independent
draws at the same question, no pilot needed) certifies the full curve across all budgets
simultaneously; a fixed exact-binomial design needs 192,000 generated answers to certify 64
budgets to +/-1/32 at 95% on 100 questions, with about 75% of the variance between
questions at budget 64. The paired audit uses 0.74x the answers of the cheapest competing
certified audit at 64 budgets and 0.53x at 1,024; on a fresh MMLU-Pro study it certified
the curve with 79,133 answers, within 0.6% of a pre-fitted cost law.
Estate mapping: the measurement design for BOTH the width A/B (Q1) and the G2 A/B (Q5):
differences of aggregate rates across arms are dominated by between-question variance (~75%),
so the 1.25x/1.5x band rule as written (DIGEST.md:43 ask-supplied) can read as signal what
is actually between-question noise. Pair the arms per question (same corpus items through
width 3 vs width 10) and certify the difference before amending or retiring the row.
Overlap declared: catalog mirror row 58fe109f8fbe at state/arxiv/2026-10-01/2609.40190v1.txt
(abstract bytes only); no prior lane read it.

### 8. arXiv 2610.07816 Do I Need the Cloud? (STEP-GATE) (2026-10-06, NeurIPS 2026 workshop: SLMs for Agentic Systems)
STEP-GATE is "an uncertainty-aware handoff framework that scores each local SLM action and
selectively escalates" difficult steps to a stronger cloud model, instead of routing once
per query. Single-step: Qwen2.5-1.5B/7B reaches 82.7% task success with 30.8% escalation vs
67.3% local-only and 75.4% random escalation. Multi-turn: 69.0% trajectory / 84.0% action
success with only 30.0% cloud actions, vs 48.0%/70.5% local-only, 60.0%/78.2% random, and
57.0%/77.1% for query-level routing; strong-only gets 82.0% trajectory at 100% cloud
actions. Limitations stated: one model family, one stronger backend, scripted tasks, small
test sets, risk tiers are research annotations.
Estate mapping: the driving ladder's escalation law got a per-STEP form: gate the climb on
per-step uncertainty, not on the ask. On the estate, the same shape says the lane runners
should escalate individual steps to primes while janitors hold the rest, and that
query-level routing (the current dispatch unit) measurably underperforms step-level
escalation at matched cloud share. The 30%-cloud-share number is a concrete target for a
ladder A/B on this account.

## Per-question verdicts (the five research questions)

- Q1 width A/B (workflow max_concurrency 3 vs Task agents 10-12): NOT run here (sweep scope
  is research, not the estate instrument run). Design inputs banked: items 2, 6, 7. The A/B
  should be per-question paired, correlation/diversity-controlled, and should record an
  Adaptive-K-style pilot arm; otherwise the 1.25x/1.5x band cannot separate width effects
  from between-question noise. Day-7's item 5 (2610.03010, 6.36x energy) already predicts
  the narrow arm owns the cost-normalized front.
- Q2 flock decode onto the task output space: three independent published mechanisms banked
  (items 1, 3, 6) plus the day-7-held readout mechanism (verification-aware readout,
  recoverable headroom, 2610.04686). Dogfoodable at $0 on this or the next sweep's own
  review pass: score recoverable headroom (was a correct proposal in the pooled sweep at
  all) and cross-seat verdict entropy BEFORE any consensus readout or judge spend; that
  directly tests whether consensus strength is measuring proposal coverage instead of
  correctness.
- Q3 probe-first vs paid judge: the published architecture converges on deterministic/probe
  first, judge only for flagged residue (items 4, 5, 8). DEFER1's ~25%-reaching-judges rate
  gives the expected judge2 load; JuryFlow's disagreement graph gives the routing rule;
  STEP-GATE shows step-level beats query-level escalation at matched cloud share.
- Q4 pheromone bus p1a L0d: NO in-window external analog exists (stigmergy feed: 0 results;
  swarm-intelligence+language-model feed: 0 results; nearest hit Jan 2026, out of window).
  Confirmation must come from the estate's own next natural swarm run, as the ask frames.
  MAG_POSITION_BOUND_LEAVES flipping the [a,b,c] vs [a,b,c,c] falsifier is on-box law per
  lens/burns.md:145-147 (commits d475824df, 633b884ad as named there); nothing read this
  window contradicts or confirms it externally. Item 3's count-sources-not-statements rule
  is the one transferable hardening for the bus: a relayed or re-read mark must not
  re-count as fresh evidence.
- Q5 G2 blind-sweep placement law (WARN, lens/burns.md:120-121): no in-window paper measures
  enforcement-vs-outcome-quality across two runs of the same cards. Nearest in-window leads
  (NOT deep-read, listed as leads only): 2609.33495 LLMs Trust Their Own (in-group
  conformity raises agreement with wrong in-group consensus) and 2610.09554 (visible labels
  collapse judge discrimination; label-free protocols recover it). Measurement design
  banked via item 7: the WARN-to-enforce A/B must pair the two runs per scenario card and
  certify the difference; a plain two-run comparison cannot resolve the question at
  realistic card counts. Flip remains an operator call; this sweep contributes the design,
  not the verdict.

## Door health and honest gaps

- arXiv export API green on all 7 queries; abs pages clean on all 9 fetches; WebSearch
  usable on both queries (its pheromone hit and all 5 identity-bias hits are out-of-window
  and used only as leads). No 403s, no degraded doors this sitting.
- Not run: the width A/B, the pheromone L0d confirmation, the G2 two-run A/B, and any
  pytest. This sweep informs their designs; it executed none of them.
- Deep reads: 9 abs pages read end to end (the 8 banked items plus 2610.04686, folded but
  not re-banked). Pass-1 leads held for a future confirmation pass, not banked here:
  2610.00991 Adapter Thickets (splitting an RLVR budget decorrelates voters and out-votes a
  concentrated one), 2609.38324 (discussion gains less when dissent is withheld),
  2609.35885 (aggregate agreement mischaracterizes coordination regimes), 2609.33495 and
  2610.09554 (Q5 leads above), 2610.07274 (only 22.6% of recorded agent-benchmark passes
  cleared four trust checks), 2609.39211's companion corpus Eraclitus-4.7M availability.
- Overlap-gate final state (both background scans stopped after their catalog hit bands
  cleared): catalog.jsonl fully checked (ids + phrases); sibling sweep trees fully checked;
  the memory/ tree scans surfaced exactly one file, memory/trajectory/steps.jsonl, with 1
  hit per phrase and a latest ts of 2026-10-08T18:00:36Z (this window's own steps: my grep
  commands and my Read of the day-7 sweep file are themselves the matches). The
  catalog-side hits are the three state/arxiv/ mirror rows already declared per item plus
  the DEFER substring false positive (INTAKE_DEFERRED_SDF filename). No real prior holding
  of any of the 8 items exists anywhere the gate reached; the un-scanned remainder of
  memory/ (scan stopped, filesystem-bound) is the one caveat carried forward.
