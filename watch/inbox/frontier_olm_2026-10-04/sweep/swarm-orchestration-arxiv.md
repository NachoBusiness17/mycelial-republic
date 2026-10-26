# SWEEP: swarm-orchestration via arxiv - 2026-10-04

source-fetched: 2026-10-04
Sweeper: frontier gopher (sweep-swarm-orchestration-arxiv, today's invocation of this lane).

## Method (commands run this sitting)

- Doors: arXiv export API via WebFetch over
  `https://export.arxiv.org/api/query?search_query=...` (Atom XML), sorted
  `submittedDate desc`; plus `https://arxiv.org/list/cs.MA/recent`; deep reads over
  `https://arxiv.org/abs/<id>` and one full text over `https://arxiv.org/html/2609.34136v1`.
  All doors returned 200; nothing 403'd or degraded; WebSearch was not needed.
- Pass 1 queries (five fetches, 40/30/25/30/30 max_results): `cat:cs.MA AND all:"large
  language model"` (39 entries read); `(all:"LLM swarm" OR all:"swarm of LLM agents" OR
  all:"agent swarm")`; `(all:flocking OR all:"flock") AND all:"language model"`;
  `(all:"retry" OR all:"rate limit" OR all:"fault tolerance") AND (all:"LLM agent" OR
  all:"multi-agent" OR all:"agent framework")`; `(all:"parallel agents" OR all:"fan-out" OR
  all:"fanout") AND (all:"throughput" OR all:"scaling" OR all:"width")`; plus
  `(all:"role assignment" OR all:"leader election" OR all:"role allocation" OR all:"dynamic
  roles") AND all:"LLM"`, a cs.CL `(all:"mixture of agents" OR all:"repeated sampling" OR
  all:"collective decoding" OR all:"ensemble decoding")` query, and the cs.MA recent listing
  (140 new, 50 read). Candidate pool well past the 30 floor (I counted 100+ distinct in-window
  candidates across the eight query outputs; every entry each fetch returned was listed).
- Pass 2 deep reads this sitting (fetched and read myself): abs pages of 2609.34136, 2609.27374,
  2609.29095, 2609.38482, 2609.33768, 2609.06386, 2609.35719, 2609.27657, 2606.14882, 2609.32939
  (10 reads) plus the FULL TEXT of Waggle (arxiv.org/html/2609.34136v1) - 11 fetch-reads total.
- Overlap instruments: `rg 15.2.0`. Greps run: all 11 read IDs against
  `catalog/catalog.jsonl` + `memory/`; ID set against
  `memory/runs/corpus_gap_research/ARXIV_REGISTER.json` and `MAP_BACKFILL.json`; title phrases
  against catalog + memory/rib + memory/steal + memory/facts + memory/grok_batch; yesterday's
  sibling bank `watch/inbox/frontier_olm_2026-10-03/sweep/swarm-orchestration-arxiv.md` read in
  full and the 09-28 bank `watch/inbox/frontier_olm_20260928/sweep/swarm-orchestration-arxiv.md`
  grepped, both BEFORE banking (anti-rebank).
- RQ2 grounding check run this sitting:
  `rg -n -i -m 10 "backlog|leader|elect|role|threat|formation" mag/lane_runner.py` returned only
  an unrelated "derivation" line (312) and the LLM chat `role` message fields (674-675). The lane
  runners carry NO formation-keeping, threat-table, leader-election, or backlog-routing machinery.

## Anti-rebank census (what prior seats hold; none of it re-banked below)

From yesterday's (10-03) sibling bank: 2610.00349 (budget conservation), 2609.35875
(cognitive diversity), 2609.10964 (release budget), 2609.34215 (recovery symmetry), 2609.04749
(DCFA), 2609.34701 (ResonAct), C-MoA 2609.25959 (held-shell delta), Waggle 2609.34136
(ABSTRACT-ONLY, full text flagged OWED). From the 09-28 bank: LIMBO 2609.29095 (banked item 3,
abstract-level), plus PANDA 2609.38482 and DEALS 2609.33768 as registered finds (register rows
r1/r4 per the 10-03 file; both in ARXIV_REGISTER.json). Theory of Scene 2609.32939 is registered
(ARXIV_REGISTER.json:5540, cited_in the 09-28 sweep) but only as a feed-level candidate line; it
has NO banked row and was never deep-read until my read today.

## Banked items (strongest first)

### 1. Where Does Exactly-Once Live? Model, Harness, and Tool-Contract Effects on Duplicate Side Effects in LLM Agents (LIMBO) - DELTA
- arXiv 2609.29095, 2026-09-24. Abs page read this sitting.
- Quote: "no verification-only policy is exactly-once under late commits without a bound on
  in-flight time" (given as a proven result).
- Why (RQ3, the retry-as-orchestration vs retry-as-transport question): this is the paper's
  core split, measured. Where a read-back can reveal what happened, the model decides (explains
  53% of explained variance); where it cannot (request in flight, transport delivered twice),
  the tool contract dominates ("the contract explains 81%"), and the harness barely matters.
  Numbers my read adds to the 09-28 bank: frontier models duplicate lost-ack writes at 0.5% but
  the SAME models duplicate at 56% (in-flight) and 74% (duplicate delivery); idempotency keys
  cut duplicates 28% to 4%; "even an hour of waiting per episode falls short" of keys under
  heavy-tailed delay; agents "reported success in 90% of the episodes in which they had
  duplicated an effect"; 25,930 episodes, nine models, three harnesses, 15 recovery conditions.
  Estate consequence: the fan-out width law's maxAttempts 0 for workflow children (die on first
  429) is not merely a rate-limit accommodation, it is the CORRECT default on an estate with no
  broker-minted idempotency keys - transport-level retries without keys live in the 56/74%
  duplication regime and the duplicate reports success. Raising the child retry envelope is
  gated on the 09-28 steal actually landing: effect_broker minting idempotency keys.
- Overlap: catalog 0 ID hits; memory hits only Gutenberg "limbo" noise; HELD: banked 09-28
  (ARXIV_REGISTER.json:5288-5291, cited_in frontier_olm_20260928 swarm sweep as item 3;
  ttc-week lane had verified the 90% statistic). This row banks the variance-attribution and
  duplication-regime numbers that bank lacks. Delta, not a re-bank.

### 2. Waggle: Learning One Anonymous Local Law for Self-Organizing LLM Swarms - OWED FULL-TEXT NOW READ (delta)
- arXiv 2609.34136, 2026-09-28. Full HTML read end to end this sitting
  (arxiv.org/html/2609.34136v1) - the exact read yesterday's bank flagged as owed.
- Quote: "the shared law retains 96.8% and 97.6% of oracle quality on SwarmBench and
  Silo-Bench, respectively".
- Why (RQ1, flock-shaped generation; RQ2): the closest published thing to the estate's
  law-carrying mesh, now at mechanism depth. Each agent's view is six canonically serialized
  components (task contract q, private state/evidence, an adapter-provided candidate action
  which "is an input to the joint local decision, not a separate decision or language-model
  call", bounded incident traces with novelty/support/conflict/TTL fields, local commitment,
  remaining budget); "Serialization exposes neither persistent identities nor a global node
  ordering." One joint decode outputs task action + bounded semantic update (deposit/relay/
  challenge, relays "lose at least one TTL step") + commitment update. Trained by Swarm-
  Consistent Distillation: token-level NLL on GPT-4o teacher decisions (6,912 views) +
  orbit consistency over relabelings + a training-only next-field prediction head (14,256
  triplets); deployment keeps only the policy, Qwen3-4B + rank-32 LoRA on two H800s, pattern
  replicated on Llama-3.1-8B. Numbers: 86.3/79.0/58.2% Silo-Bench success at N=16/32/64
  (baselines ~15% at N=64); frozen N=128 retains 82.9% of N=64 success; orbit supervision adds
  22.3 points of anonymous-view agreement; 99.75% of first decodes executable. Stated limits:
  transport/validation/expiry stay fixed (not learned), anonymity is not privacy, and "removing
  conflict handling or commitment reversibility collapses recovery". This is the rib_bus
  doctrine (feed structures/laws, not prose) as someone else's measured artifact - including
  the TTL-and-conflict fields the estate's edges lack.
- Overlap: catalog 0; memory only Gutenberg "waggle"; HELD abstract-level by the 10-03 bank
  with full text OWED. This row is that owed read. Delta.

### 3. Planned Test-Time Scaling with Coordinated Reasoning Paths (PTTS)
- arXiv 2609.27374, 2026-09-23. Abs page read this sitting.
- Quote: "PTTS strictly generalizes repeated sampling".
- Why (RQ1, the flock question, directly): independent parallel branches from one policy are
  the flock shape the estate's width law assumes, and this paper measures their waste: branches
  drawn independently are redundant, and a planner that "generates a solution outline for each
  branch, steering the branches toward distinct reasoning paths" with an executor conditioning
  on each outline beats it. On Qwen3-1.7B/4B across five math benchmarks, pass@64 improves by
  up to 6.7 points zero-shot and 13.4 RL-trained. Published verdict for the estate's un-run
  instrument: at matched width, COORDINATED fan-out beats independent fan-out, i.e. the value
  lives in the dispatch shape (the laws.md claim), not in width alone. Composes with the 10-03
  cognitive-diversity verdict (budget-matched self-consistency beats debate): a flock must buy
  its keep with structure, not numbers.
- Overlap: catalog/catalog.jsonl:445399 holds ONLY the raw abs snapshot
  (state/arxiv/2026-09-24/2609.27374v1.txt, 2,014 bytes); absent from ARXIV_REGISTER.json,
  MAP_BACKFILL.json, and both prior sweep files. First banked row.

### 4. Are Verifier Errors Independent Within a GRPO Group? Evidence from Qwen2.5 Rollouts
- arXiv 2609.06386, 2026-09-06. Abs page read this sitting.
- Quote: "Analyses based on independent verifier errors may overlook dependence".
- Why (RQ4, the width-rung estimator): the only in-window quantitative law for discounting
  nominal width, and it transfers. Across 24,998 eight-completion GRPO groups, within-group
  verifier-error correlation is 0.530 (CI 0.500-0.560), so the design-effect-adjusted effective
  sample size of an eight-wide group is 1.70. That is the exact arithmetic the 15-16 rung
  estimate needs: effective width = n/(1+(n-1)rho). Children in one burst share fate (same
  account, same rolling-throughput window; AGENTS.md records 1302s after bursts), which is
  positive failure correlation rho>0, so the marginal 11th-16th child's expected yield must be
  discounted the same way before anyone arms it. Estate instrument: compute rho from
  queue/lanes/*/trail.jsonl co-failing children in a burst window, then ESS-discount. No
  published agent-swarm throughput-vs-width curve exists in-window to compare 109.4M tok/h
  against (checked; nearest are PTTS and FLEET, both accuracy-per-width not tokens-per-hour),
  so the envelope's width law stays the estate's own measured artifact and this paper is the
  estimator, not a corroborator.
- Overlap: zero hits across catalog, memory/, both registers, both sweep files. NEW.

### 5. AI Agent Swarms as Researchers: Progress, Challenges, and Open Questions
- arXiv 2609.35719, 2026-09-28. Abs page read this sitting.
- Quote: "make real, correct, useful progress, and do not stop" (given as the swarms' one
  standing instruction).
- Why (RQ1/RQ4, the mirror paper): Gusev and Bernal Neira ran swarms of off-the-shelf coding
  agents from a scope statement only ("humans supplied no scientific ideas") and got research
  notes, paper-length drafts, and formal proofs in five areas, corpus released 2026-09-25 on
  GitHub; full human review is estimated at "months", past reviewer capacity. Their open
  questions are the estate's banked laws arriving independently: "how to trust results when
  review, not production, is the scarce resource" is the estate's verification-is-the-bottleneck
  finding from dwfrun-5e9435bb, and "what credit and publication counts mean when the human
  input is a prompt" is the self-steal meter's question. Corroboration that the estate's shape
  (scope + standing instruction + gate) is now a published research object, with their caveat
  "We do not claim that all of it is correct or new" matching the estate's
  findings-are-not-done-work law.
- Overlap: zero hits across catalog, memory/, both registers, both sweep files. NEW.

### 6. FLEET: From Logits Entropy to Enhanced Trajectories in Text Generation
- arXiv 2609.27657, 2026-09-23. Abs page read this sitting.
- Quote: "FLEET achieves the same accuracy as the repeated sampling baseline, with a 3x
  speedup".
- Why (RQ4/Q1): the decouple-accuracy-from-width result. Instead of memoryless independent
  samples, FLEET "represents each generation as a sparse trajectory through states whose
  entropy exceeds a predefined threshold and uses these trajectories to infer per-token utility
  scores that adjust the logits", deterministic, one calibration pass. LiveCodeBench Pass@32
  rises 59.9% to 66.2% at the same budget. For the estate: the width ladder has a published
  substitute axis - trajectory memory buys the pass@k that raw width buys, at a third the
  cost - which is the cheap-first rung below any width increase, i.e. before testing 15-16,
  the falsifier is whether per-lane trajectory utility (the trails already bank every row)
  recovers more than the extra children would.
- Overlap: catalog/catalog.jsonl:445457 holds ONLY the raw abs snapshot
  (state/arxiv/2026-09-24/2609.27657v1.txt, 1,431 bytes); absent from registers and sweeps.
  First banked row.

### 7. Theory of Scene: Breaking the Symmetry Trap in Multi-Agent LLM Coordination - FIRST BANKED ROW (delta)
- arXiv 2609.32939, 2026-09-26. Abs page read this sitting.
- Quote: "homogeneous agents form the same prediction of one another and respond to it in the
  same way".
- Why (RQ2, roles/formation): the playerbot role table (tank/heal/dps) is the cure this paper
  formalizes for interchangeable agents. The symmetry trap: identical agents without
  communication "collide on targets they must split and diverge on targets they must take
  together", and Theory of Mind fails because symmetric agents predict symmetrically. Theory of
  Scene is training-free: each agent reads "its public role, the only difference between the
  agents, and the task context they all observe", with role gating (is ownership divided?) and
  task coupling (converge/divide/sequence?). Beats all six baselines: DivvyBench 71.1% to
  99.6%, GovSim 207 to 400, Overcooked 1.41 to 1.67. Estate mapping: the lanes already carry
  public roles (builder/day_work/research/night-shift), which is why they do not collide; the
  transferable bit is task coupling as an explicit gate check (does this ask need converged or
  divided lanes?) before fan-out.
- Overlap: registered 09-28 (ARXIV_REGISTER.json:5540, cited_in frontier_olm_20260928 swarm
  sweep) but ONLY as a feed-candidate line, with no banked row and no deep read (verified by
  reading that sweep's pass-2 list and banked-eight list). This is the item's first banked row.

### 8. DynaHMRC: Decentralized Heterogeneous Multi-Robot Collaboration for Dynamic Tasks with Large Language Models - OUTSIDE WINDOW, FLAGGED
- arXiv 2606.14882, 2026-06-12. Abs page read this sitting. NOT in the preferred 30-day
  window (four months old); banked only because it is the one paper found that names the
  playerbot-style mechanism set directly.
- Quote: "a four-stage closed-loop process: self-description, task allocation with leadership
  bidding, leader election, and reflective execution" (the paper names the stages; it does not
  detail them at abstract level).
- Why (RQ2): decentralized heterogeneous teams where "each robot acts as a role-aware LLM
  agent", allocating via leadership bidding then leader election, benchmarked over three task
  families, four dynamic variations, six team configurations, claiming higher success with
  fewer action and communication steps. Estate state: leader election is ALREADY
  reimplemented knowingly, not unknowingly - the flock_scheduler leader lease
  (memory/rib/RIB_EMERGENT_TOOLING_K8S_DEEP_DIVE_20260810.md:64, the L8 storm fix) - and my
  lane_runner grep this sitting found NO formation/threat/backlog machinery in the runners.
  So the playerbot-transfer ledger reads: role tables = landed (lane roles + ToS above),
  leader election = landed (flock lease), formation keeping and threat tables = absent from
  lane runners and absent from in-window literature as LLM mechanisms; DynaHMRC is the lead
  for a full-text read if formation transfer is ever demanded.
- Overlap: zero hits across catalog, memory/, registers, sweeps (memory "leader election" hits
  are the estate's own ribs and Gutenberg texts, not this paper). NEW but stale-dated.

## RQ synthesis

1. Flock-shaped generation (RQ1): no in-window paper presents a decode architecture that
   matches the estate's flock shape (independent children + shared law + gate). The nearest
   three triangulate it: PTTS says coordinated fan-out beats independent fan-out at matched
   width; Waggle says one anonymous local law executed by interchangeable agents reorganizes
   without roles or topology (the estate's shape, learned); yesterday's cognitive-diversity
   result says undifferentiated flocks lose to budget-matched self-consistency. Nothing
   published matches closely enough to steal wholesale; the steal is PTTS's planner outline
   (per-branch intents minted before dispatch) as the mechanism that makes width pay.
2. Playerbot transfer (RQ2): role assignment transfers and is landed (lane public roles; ToS
   gives the explicit role-gating/task-coupling formulation); leader election is landed as the
   flock_scheduler lease; formation keeping and threat tables have NO in-window LLM-literature
   analog (the flocking papers are robotics/control: COMPASS 2609.28247 flies commanded flocks
   to 1024 robots but its control layer is not a lane-orchestration shape) and NO accidental
   reimplementation in the runners (grep run this sitting, empty). The one lead is DynaHMRC.
3. Retry-as-orchestration vs retry-as-transport (RQ3): the literature's answer is LIMBO's
   location result - transport-layer retry is safe exactly where the tool contract carries
   idempotency, and catastrophic where it does not (56/74% duplication); orchestration-layer
   recovery (replan around failed components, PANDA, registered) is a different act that must
   carry generation numbers and settlement (2610.00349, banked 10-03) to avoid double-spend.
   The estate's maxAttempts 0 children / maxAttempts 11 Task split is thereby VALIDATED as a
   correctness split, not just a rate envelope, with the precondition for widening it named:
   broker-minted idempotency keys first.
4. Throughput-vs-width (RQ4): no published swarm throughput-vs-width curve exists in-window;
   the envelope (109.4M tok/h at width 10, 15-16 untested) remains the estate's own measured
   artifact. The estimator for the untested rung is the correlation discount: ESS =
   n/(1+(n-1)rho) from the GRPO-correlation paper (rho=0.53 turned 8 into 1.70); measure
   co-failure correlation among burst-mates from lane trails before arming 15-16, and treat
   FLEET's 3x trajectory-memory result as the cheaper alternative axis to test first.

## Falsifiers / limits

- Quotes are verbatim fragments as rendered inside quotation marks by this sitting's WebFetch
  extractions of the live pages; sentence spans are the extraction's, so boundary wording
  beyond the quoted fragments was not byte-verified against the PDF.
- Banked items 3 and 6 (PTTS, FLEET) were read at abstract depth; their full texts are unread,
  and their token-cost figures are absent from the abstracts (PTTS reports no token budget,
  FLEET no sample counts beyond Pass@32).
- Item 8 (DynaHMRC) is outside the 30-day preference window and abstract-level only.
- LIMBO, Waggle, and Theory of Scene are DELTA banks on held items, per the held-shell-delta
  pattern; their prior banks are cited in each overlap field.
- PANDA 2609.38482 and DEALS 2609.33768 were read this sitting (abs level) but are registered
  finds from prior seats; deliberately not re-banked.
- The lane-runner grep is one instrument (rg over mag/lane_runner.py, patterns
  backlog|leader|elect|role|threat|formation); absence of matches is evidence of absence of
  those NAMES, not of function under different naming.
