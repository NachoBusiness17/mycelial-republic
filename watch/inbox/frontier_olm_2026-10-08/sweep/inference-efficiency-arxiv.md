# Sweep: inference-efficiency via arxiv (2026-10-08)

source-fetched: 2026-10-08. Gopher seat: sweep-inference-efficiency-arxiv (dynamic workflow child).

## Method (instrument + moments)

Pass 1 broad sweep, six arXiv API queries via WebFetch against export.arxiv.org
(date-ranged submittedDate 202609080000 TO 202610082359, sortBy submittedDate desc)
plus one WebSearch (site:arxiv.org reasoning tokens overhead):

1. abs:"inference cost" (40 shown of 195 reported matches)
2. abs:"test-time compute" (39 entries)
3. abs:"reasoning tokens" (27 entries)
4. abs:"prompt caching" OR "context caching" OR "prefix caching" (30 of 32)
5. abs:"LLM routing" OR "model routing" OR "LLM cascade" (25 of 29)
6. abs:"token cost" OR "API cost" OR "cost per query" AND "language model" (30)
7. WebSearch keyword sweep (9 results, several pre-window, noted not banked)

Total surfaced ~350 entries; ~60 screened as on-topic for the five research
questions; 11 deep-read end to end on their arxiv abs pages (full title, authors,
abstract, quantitative results extracted); 8 banked as new; 3 dropped as already
in the estate catalog (documented below). All doors answered HTTP 200; no 403s,
no fallback needed.

## Banked items (strongest first)

### 1. What Does a Harness Repair? A Preregistered Study of Visibility, Baseline Adequacy and Evaluation Defects
arxiv.org/abs/2610.05533, 2026-10-04, Bowen Xu, Boyu Chen. 43pp preregistered
study, 47 primary endpoints, three small models x three benchmarks, GEPA search
arm, six injected evaluation defects.
Quote: "Turning thinking off raised accuracy over a capped thinking setting in 5
of 9 model-benchmark cells"
Estate mapping (Q1, lens/laws.md:149-153): the estate owes an off-state re-measure
of the pre-2026-10-04 DeepSeek rows ($0.0024 triangulations, $0.005 assembly,
$0.00077/ask) because they rode thinking-ON by omission. This paper is the
external preregistered proof of the estate's exact suspicion: thinking-off beat
capped thinking mostly on questions where the capped setting produced NO readable
answer (truncation, not reasoning quality); a serving-engine thinking budget
lowered truncation and raised parse rate in 6 of 9 cells. The steal for the d4
three-arm shape (lens/laws.md:28-30): record parse-rate/truncation as the
mechanism column next to dollars, and treat "no readable answer" as a first-class
cost driver, not a quality regression. Also: same-pipeline replication reproduced
an injected defect's distortion in 6 of 15 pairs, so replication alone is not an
audit.
Overlap: exact title grep over catalog/catalog.jsonl + memory/ + lens/: zero hits. NEW.

### 2. How Much Can Language Models Gain from Test-Time Computation? (SELF-POT)
arxiv.org/abs/2610.01110, v1 2026-10-01, v2 2026-10-06, Yang et al. 350 sealed
tasks, five low-cost reasoning models, Claude Opus 5.5 Direct as reference.
Quote: "charges every model call, including selection and critique, in dollars"
Estate mapping (Q3, lens/laws.md:41-45): cost-per-blind-point is the estate's
champion metric; SELF-POT is the published instrument shape for it: selection
rules replayed over IDENTICAL retained candidate pools swung logical API cost
12-49 percent (programming) and voting vs judged-fallback traded 182 vs 186
correct at 12-21 percent cost difference (math). The steal: the estate's
routing-class table (14/17 at 2-4 percent of dollars) can be re-scored by replaying
selection rules over logged candidate pools instead of refiring paid lanes, and
every judging/critique call must land in the burn ledger (memory/runs/hermes_burn/
usage.jsonl) as charged dollars, per the SPEND amendment (lens/laws.md:49-51).
Overlap: "SELF-POT" matched only Project Gutenberg texts (pg75871, pg55618), no
paper match. NEW.

### 3. Fast Models, Slow Evidence: A Paired and Self-Audited Evaluation of System-1 Decision Models for LLM Agent Harnesses
arxiv.org/abs/2610.02267, 2026-10-01, Jiawei Li. 11 decision points, 7,283 base
cases + 6,640 robustness variants, paired byte-identical inputs.
Quote: "Three analysis errors and one design confound distorted headline deployment claims"
Estate mapping (Q2+Q3): the estate is wiring a classifier inference-budget guard
into six hand-rolling fire surfaces (lens/laws.md:154-158). This paper evaluates
exactly that class of fast gate models: on zero-shot model routing "Neither model
beats chance"; the author self-audit found "reported 23.9% saving, actual 4.3%"
(an omitted pre-screen cost), gate accuracy misreported as end-to-end quality
(58 vs 98), and in-sample threshold tuning hitting 17 percent held-out misses
against a 5 percent target. The steal: before trusting any guard's savings claim
on the fire surfaces, pair it with a held-out audit that charges the guard's OWN
token and error costs; option-order instability (one model flipped 30 percent of
answers on option reversal) is a direct warning for the estate's classifier
prompts. Converges with the estate law "trust bytes, not reports".
Overlap: exact title grep: zero hits. NEW.

### 4. Identical Runs, Different Results: Benchmarking AI Coding Agents on Open-Weight Models
arxiv.org/abs/2609.33812, 2026-09-27, Arino de la Rubia (CEU), Pafka (Epoch).
584 runs, six agents x six open-weight endpoints, six pairings x 52 runs each.
Quote: "differed more than twentyfold between two agents on the same model, mostly through the prompt cache"
Estate mapping (Q1+Q3): two laws for the re-measure. First, within-pairing
run-to-run variance EXCEEDED between-pairing differences; resolving agent
differences needs tens to 100+ runs, so single-pass triangulations (the $0.0024
rows) are noise-exposed and the superseding rows should carry n and spread.
Second, the >20x cost spread between agents on the SAME model was driven mostly
by the prompt cache: any thinking OFF vs ON economics re-measure that does not
pin cache-hit state measures the cache, not the mode. Also: under 5 percent of
runs broke data rules yet took the top scores (compliance filter before scoring),
and delivered models kept only a third of their gain on later-year data.
Overlap: exact title grep: zero hits. NEW.

### 5. Harness Tokenomics: A Router for the Enterprise Agentic Control Plane
arxiv.org/abs/2609.28919, v1 2026-09-24, v2 2026-09-26, Kwartler, Aqrawi, Abbasi.
~10,000 real public sessions, simulated 10,000-seat enterprise.
Quote: "the router recovers 13 to 21% of model spend at Anthropic's list prices of 21 September 2026"
Estate mapping (Q2+Q3): the router only shifts work where "no running conversation
has to rebuild its cache" (session start, side lanes, subagent launch) and uses
price-sheet math for when a mid-task switch pays; ~$3.3M-5.1M/yr at list prices.
This is the mechanism behind the estate's routing-class rows: the cache-rebuild
tax, not model quality, is what makes evidence-readable asks cheap-forever at 2-4
percent of dollars; the estate's per-animal gates (lens/laws.md:60-62) should add
cache-affinity as a routing key before family or price. A noted crossover where
the priciest model beats the next tier on long tool-heavy sessions mirrors the
estate's "transport is not quality" line.
Overlap: exact title grep: zero hits. NEW.

### 6. Do Tool Calls Execute as Intended? Measuring and Repairing Intent-Execution Correspondence in LLM Agents
arxiv.org/abs/2610.04375, 2026-10-03, Yang et al. 47,828 production shell calls,
10 harnesses, IEC-Bench; commercial deployment of the IntAct repair.
Quote: "On IEC-Bench, the path raises the token cost per passed task 2.4 times (up to 12.3 times)."
Estate mapping (Q2): today's highest-probability token-bleed shape on the estate's
own fire surfaces: intermediate harness hops silently mutate emitted calls
(Claude Code's Bash tool modified 12.0 percent of calls containing code, escapes,
or long text; 80.7 percent of backslash-altered calls ran the wrong action
silently), forcing retrial bleed that trajectory judges misattributed to the LLM
in 95.1 percent of failures. The estate's win32 cmd quoting/escape paths
(creationflags law, nul-reserved-name artifacts) are exactly this class; the
measured number to beat when naming the highest token-bleed surface is 2.4x
average / 12.3x worst per passed task. Repair shape: deliver calls in a form the
offending hop cannot modify, or refuse (79.2 percent failure recovery).
Overlap: "IEC-Bench" grep: zero hits. NEW.

### 7. AgentLoop: Runtime Control of Slot-closed Execution Loops for Tool-augmented LLM Agents
arxiv.org/abs/2609.33315, 2026-09-27, Zheng et al. (cs.DC).
Quote: "total token cost reduced by up to 88.44% and average service invocations reduced by up to 76.85% against baselines"
Estate mapping (Q2): the published guard shape to wire into the six unwired
carriers (stealth_driver, duel_harness, tesuji_fire, lane_runner, lite_scale,
wave_fire; lens/laws.md:154-158): maintain compact runtime state, verify answer
completeness against required information slots, track bounded-stability and
low-gain signals across neighboring LLM/tool rounds, then choose Continue
Invocation / Answer Synthesis / Terminate Iteration. Ablation: removing the
slot-centered control raised execution depth and hurt accuracy, i.e. the guard
pays for itself rather than being overhead (same finding as SaveRouter
2609.37402's break-even framing, screened in pass 1).
Overlap: "AgentLoop", "slot-closed", "Slot closure" greps: zero hits. NEW.

### 8. State of Thought Enables Endogenous Reasoning
arxiv.org/abs/2609.16055, v1 2026-09-13, v2 2026-09-25, Gong et al. 3 LLMs x 16
datasets, 2 VLM scales, 3 API models.
Quote: "We propose State of Thought (SoT), a new reasoning paradigm that enables endogenous reasoning in LLMs"
Numbers: 582-parameter controller on frozen models, generated tokens cut 62.6
percent, end-to-end latency cut 44.6 percent (VLMs: 74.9 / 73.5), accuracy UP
across quantitative/general/symbolic/long-context.
Estate mapping (Q5, lens/laws.md:64-66): EMPTY_REASONING is terminal per (ask,
family) with two recoveries (re-stage or switch family); SoT is a third shape
worth stealing: condition on a compact internal reasoning-state readout and
reactivate only relevant past reasoning evidence instead of regenerating traces.
For the free-lane drip-not-burst question (lens/laws.md:52-54): state-conditioned
reuse of prior reasoning is the drip-shaped complement to burst refire; a 582-param
controller is cheap enough to run as an estate-local gate.
Overlap: "State of Thought" matched only Gutenberg texts (pg42931, pg55262);
"Endogenous Reasoning": zero hits. NEW.

## Dropped as already-held (dedup receipts)

- You Cannot Pick a Provider From the Price List (arxiv 2609.37902): catalog row
  id ba63d26946fa, state/arxiv/2026-09-30/2609.37902v1.txt, mirrored 2026-09-30.
  It was the best Q4 fit (FACET provider certification for cool-pool composition);
  the estate already holds it, so not re-banked.
- Reasoning-Token Spikes Under Prompted Untruthful Responding (arxiv 2610.10405):
  catalog row id bc75e163725e, state/arxiv/2026-10-08/2610.10405v1.txt, mirrored
  TODAY 2026-10-08T06:30Z. Not re-banked.
- RATIO: Reasoning Analysis and Token-level Inference Optimization (arxiv
  2609.39801): catalog rows state/arxiv/2026-10-01/2609.39801v1.txt AND a prior
  sweep raw q_2609.39801.txt (2026-10-04). Not re-banked; it converges with the
  estate's marker-penalty logit_bias profile (P6).
- ReFold (arxiv 2610.07863): catalog + memory/zknot + memory/burns hits; banked
  by the day-7 OLM MINE per repo commit c7d364ab6. Not re-banked.

## Per-question coverage honesty

- Q1 (thinking OFF vs ON re-measure): items 1 and 4 give the design law (parse
  rate and truncation as mechanism; pin cache state; repeated runs with spread).
  The re-measure itself is estate instrument work, not runnable from this gopher
  seat; no paper substitutes for firing the d4 three-arm probe.
- Q2 (budget guard wiring + highest token-bleed surface): items 3, 6, 7 give the
  guard shape, the audit discipline, and the 2.4x-12.3x retrial-bleed mechanism.
  Naming the estate's own highest-bleed surface with a fresh measured number
  requires reading the estate's burn trails, which this seat did not run.
- Q3 (cost-per-blind-point, routing table): items 2, 3, 5. The table's 14/17 at
  2-4 percent is consistent with all three papers' mechanisms but none re-proves
  the estate's specific grid; grid law says re-measure via estate instruments.
- Q4 (Featherless 28.6k roster gap, cool-pool composition): NO new arxiv item
  found; provider-roster facts live off-arxiv. Nearest research fit (FACET,
  2609.37902) is already in the catalog, so nothing new to bank this window. This
  question is better served by the estate's own paged re-pull than by any paper.
- Q5 (EMPTY_REASONING incidence, drip vs burst transfer): item 8 plus screened
  pass-1 context (Request Order Matters 2610.05833, cache-history sensitivity for
  rolling agents, answer variation 69.0 to 26.1 percent, no estate overlap; Settle
  2609.38997, learned end-of-reasoning stop, 40 percent token cut). The funded
  vs free lane incidence measurement itself is estate ledger work.

## Instrument notes

- All fetches via WebFetch of arxiv.org abs pages and export.arxiv.org API; all
  quotes are verbatim fragments as rendered by those fetches; abstract-only depth
  for items 2-8, full-record depth (endpoints, defect injections, addenda) for
  item 1 via its abs page render. No page 403ed; no fallback recipe used.
- Overlap greps ran with ripgrep over catalog/catalog.jsonl + memory/ + lens/
  (sqlite/pyc/dashboard-static excluded), 2026-10-08 this session.
