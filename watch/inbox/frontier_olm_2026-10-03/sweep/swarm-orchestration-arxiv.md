# SWEEP: swarm-orchestration via arxiv - second same-day pass - 2026-10-03

source-fetched: 2026-10-03
Sweeper: frontier gopher (sweep-swarm-orchestration-arxiv, second invocation of this lane today).
This pass REPLACES the earlier same-path file written by this lane's first invocation: that file's
content was not read or verified by this seat, and the no-fabrication law banks only what the
sitting seat read itself. Anti-rebank rules (lens/burns.md section 5) were applied: nothing below
re-confirms the day's 23 register-confirmed finds; the one already-held shell re-read here (C-MoA)
is banked as a delta with its overlap named.

## Method (commands run this sitting)

- Doors: arXiv export API (Atom XML, urllib from `.venv\Scripts\python.exe`, never bare python per
  AGENTS.md) and arxiv.org/html full texts. All fetches succeeded; no door 403'd. Scripts kept at
  `sweep/_arxiv_sweep_swarm_r2.py` and `sweep/_arxiv_deep_swarm_r2.py`; raw outputs under
  `sweep/_raw/` (pass-1 list `swarm_r2_pass1.txt`; seven `*_fulltext.txt` files, 47k-269k chars each,
  plus `2609.38482_fulltext_r2.txt` and `2609.33768_fulltext_r2.txt` for the two RQ-named held papers).
- Pass 1: 8 queries (fault-tolerant mesh, queue/scheduling, retry/limits, collective failure,
  consensus/diversity, swarm, orchestration, resume/checkpoint), window
  `submittedDate:[202609030000 TO 202610042359]`, max_results 15 each, sorted submittedDate desc.
  Script printed `TOTAL unique candidates: 89` (well past the 30 floor). 16 re-hits against the
  day's banked IDs were flagged in-line by the script's BANKED map, not silently re-read.
- Pass 2 deep reads (full HTML fetched and read this sitting): 2610.00349, 2609.35875, 2609.34215,
  2609.10964, 2609.04749, 2609.34701 (six new papers, read at mechanism-section depth end to end)
  plus held-shell reads of PANDA 2609.38482 and DEALS 2609.33768 for the RQ1/RQ2 mechanism answers.
  C-MoA 2609.25959 was deep-read AFTER the overlap grep found it already registered (see item 7).
- Estate census run this sitting (the fold's owed $0 probe 1, lens/burns.md:118-120):
  `./.venv/Scripts/python.exe` over all 12 `queue/lanes/*/trail.jsonl` (7,492 rows total). Results:
  limit-class rows (429/1302/quota/too-many-requests/lane-down patterns) = 752, of which 722 are
  research-lane MONITOR rows (the monitor OBSERVING upstream 429s on its own sensing sources, not
  lane deaths), 26 are fatal lane CYCLE_FAILs: elder 14 consecutive daily 429s (2026-09-20 through
  2026-10-03, `queue/lanes/elder/trail.jsonl`) and harvest 12 (`queue/lanes/harvest/trail.jsonl`,
  2026-09-17 through 2026-10-02). Every fatal 429 is followed by a fresh next-day CYCLE: the lane
  model re-does from scratch, never resumes. Zero code-1005 rows in any lane trail (the BUILD-IT-ALL
  quota wall lived in the workflow runner, not the lane runners; commit af9aa05f6 message is its
  record). The research lane's own 387 CYCLE_FAILs are all `EXC OSError: [Errno 22] Invalid argument:
  '/app/queue/lanes/research/runner_state.json'` - an environment defect, not limits. Builder trail:
  283 CYCLE_FAILs, zero limit-class.

## Banked items (strongest first)

### 1. Fault-Tolerant Budget Conservation in Distributed Multi-Agent Delegation
- arXiv 2610.00349, 2026-09-29. Full text read this sitting (269,045 chars flattened).
- Quote: "Recovery may query, settle, or permanently retire the obligation; elapsed time alone
  cannot make the right spendable again."
- Why (RQ1+RQ2): this is the missing mechanism under the estate's quota wall. It proves the
  timeout-refund/late-completion double spend: a controller that refunds a dead child's budget and
  re-dispatches elsewhere can consume n+1 units of an n-unit authorization when the "dead" child's
  effect completes late. Its protocol: reserve before dispatch, terminal-evidence settlement
  (receipt or no-effect proof, never elapsed time), epoch fencing that returns recorded results for
  old idempotency keys but rejects new old-generation effects, exclusive escrow credits per branch,
  and lineage-scoped reissues. Directly the shape lane_runner's starvation failover
  (mag/lane_runner.py:637-666, one paced retry then openrouter overflow) needs next: the re-dispatch
  must carry a generation number and the original must stay quarantined until settled, else a
  429-failed child that later completes double-spends the Lite tank. Also names the boundary the
  estate's per-animal budget meters already live at: issuer-level escrow is required for an
  aggregate cap; per-branch equations do not give you an account-level cap.
- Overlap: catalog/catalog.jsonl 0 hits for "Fault-Tolerant Budget Conservation"; single-pass grep
  over memory/ (10 patterns, one traversal) hit only false positives (Gutenberg "waggle"); not in
  ARXIV_REGISTER.json, MAP_BACKFILL.json, state/arxiv snapshots, or today's register.jsonl. NEW.

### 2. Beyond Symmetric Agents: Cognitive Diversity and Multi-Agent Debate in Small Language Models
- arXiv 2609.35875, 2026-09-26. Full text read this sitting (92,995 chars).
- Quote: "at matched budget conditions it ties or even loses to self-consistency sampling at 1.6
  times the wall-clock and 3.4 times the token cost" (sentence context: debate beats single-agent
  3-7 points where tasks have headroom, but loses the budget-matched comparison).
- Why (RQ5): the strongest post-bank evidence on the flock question, and it cuts AGAINST debate
  flocks, not for them. Across 23 models, 11 vendor families, 5 tasks, 5,500+ debate and control
  runs, the cognitive-diversity hypothesis is REJECTED on every axis: persona prompting reduces
  accuracy (a persona tax), temperature and model diversity add nothing at matched budget
  (mixed-model teams lose to majority votes over their own rosters), nearly all debate benefit
  comes from the first exchange, and a measurement hazard (debate transcripts silently overflowing
  serving context windows) alone moved debate-vs-sampling from -1.8 points to parity once
  corrected. For the estate: the consensus-illusion law's valid use "open-ended divergent sampling"
  is NOT moved off the list - the authors explicitly exclude "domains valuing novelty or synthesis"
  from their claims - but any flock-vs-one-seat A/B on verifiable tasks must now clear a
  budget-matched self-consistency baseline, which the estate's flock has never run against.
- Overlap: catalog 0; memory single-pass grep 0; not in registers or today's register. NEW.

### 3. Decoupling Readiness from Release for Tail-Aware Scheduling of Agentic LLM Workflows
- arXiv 2609.10964, 2026-09-10. Full text read this sitting (47,467 chars).
- Quote: "substantially reduces the P95 of workflow flow time under contention, achieving up to a
  3.50 times speedup" (with comparability to eager release at light load, ratio 0.99-1.00x).
- Why (RQ2): the preventive queue shape for quota-wall lane deaths, named precisely. Eager release
  (dispatch a turn the moment it is ready) creates "committed work" that "can no longer be reordered
  by the workflow-level policy" - exactly the BUILD-IT-ALL failure, where 8 lanes released into a
  capped account and 2 died with their work committed and unrecoverable. The fix is a release
  budget: decouple readiness from release, maintain a bounded quantity of released-but-unfinished
  work, prioritize by mean-CVaR tail risk, and adapt the budget to observed queue pressure. This is
  the formal version of the estate's "first 429 is HOLD not a width cut" law (max-concurrency
  standing law) and composes with DEALS (banked, re-read this sitting: per-type FIFO queues,
  backpressure forwarding on backlog differentials, hop limit H against forwarding storms, split
  action returning unfinished work to the queue): hold below the wall, re-route on measured
  backlog, never re-fire into a saturated lane.
- Overlap: catalog 0; memory 0; not in registers or today's register. NEW.

### 4. Same Winners, Different Success Rates: Evaluating How LLM Agents Recover from Failures
- arXiv 2609.34215, 2026-09-28. Full text read this sitting (198,219 chars).
- Quote: "creating an illusion of stability that masks near-zero recovery success" (sentence
  context: when all actions fail they tie at zero reward and independent runs produce the same tied
  set with high probability).
- Why (RQ3): the census instrument the redo-vs-resume question must use. It proves set-path
  symmetry: for equal-cost Bernoulli actions, success probabilities (0.9, 0.8) and (0.2, 0.1) yield
  identical best-action-set distributions at every sample size - agreement alone cannot distinguish
  universal success from universal failure - and permuting checkpoint-to-action bindings changes 8
  to 13 percent of cell-level conclusions on 864 frozen RecoveryBench episodes plus 3,456 planning
  responses. The estate's banked agent-limit-retry census (438 redone vs 8 resumed, resumed all
  died) is a pooled-success-zero regime wearing an agreement costume; this paper prescribes
  reporting four diagnostics (agreement, all-zero fraction, held-out success, pooled success) with
  no extra data collection. The trail.jsonl census run this sitting should be extended with exactly
  those four columns before its redo-vs-resumed fraction is treated as a verdict: the count
  (26 fatal limit-class lane deaths, 0 resumed, 26 re-done next cycle) is Supported; its success
  interpretation needs the pooled-success column.
- Overlap: catalog 0; memory 0; not in registers or today's register. NEW.

### 5. DCFA: Dual-view Causal-inspired Attribution for Failure Reasoning in LLM-based Multi-agent Systems
- arXiv 2609.04749, 2026-09-04. Full text read this sitting (106,332 chars).
- Quote: "improves step-level accuracy by up to 8.27% over state-of-the-art baselines" (Who&When
  benchmark, six LLMs; average improvements 12.51% algorithm-generated / 4.02% hand-crafted vs
  strongest baselines).
- Why (RQ4): the mesh-diagnosis shape rib_bus can adopt without re-running blind. Training-free:
  a global module builds a structured causal dependency graph over the natural-language agent trace
  to find the decisive error (the earliest action whose correction reverses failure), then a local
  module runs counterfactual refinement via bidirectional greedy search over the dependency
  neighborhood. Cost is 2 full-context LLM calls - the same complexity as the strongest baseline
  ECHO - with ~400-token prompt overhead and 3k-10k-token traces. Estate mapping: memory/mycelium/
  edges.jsonl and the rib_bus arrival stream already ARE the message graph; a DCFA pass is a
  post-hoc instrument over rows the mesh already stores, and its named limitations (degrades on
  very long traces; weaker with smaller judge models; cannot attribute intrinsic hallucinations)
  match the estate's judge-tier laws.
- Overlap: catalog 0 ("DCFA"); memory 0; not in registers or today's register. NEW.

### 6. ResonAct: Streaming Metrics for Runtime Diagnosis and Self-Healing in Multi-Agent Systems
- arXiv 2609.34701, 2026-09-28. Full text read this sitting (48,242 chars).
- Quote: "improves task completion rates by up to 10.00 percentage points, with detection precision
  ranging from 70.59% to 82.91%, recall from 63.09% to 100%" (plus recovery 10.48-46.67%, runtime
  overhead -0.25% to 14.12%).
- Why (RQ4): the runtime complement to DCFA's post-hoc attribution, and the concrete rib_bus
  adoption candidate. An EXTERNAL control plane (no agent or orchestrator modification) ingests
  execution traces, agent interactions, and tool invocations as an event stream, derives streaming
  metrics at query/agent/tool granularity (count-based, embedding-based, judge-based), detects
  anomalies before task termination with a stability filter, and selects remediation policies
  (retry, re-plan, guidance injection) keyed to a failure taxonomy of common/silent/critical
  classes - silent failures (context decay, state divergence, redundant execution) are the class no
  retry envelope catches. Built on langfuse + kafka; the estate's equivalent spine is rib_bus +
  trail.jsonl. The elder lane's 14-day 429 streak (census above) is exactly a case where a
  streaming detector with a remediation policy (the openrouter overflow failover lane_runner
  landed 10-03) should have fired days earlier instead of re-failing daily.
- Overlap: catalog 0 ("ResonAct"); memory 0; not in registers or today's register. NEW.

### 7. Calibration Is Not Verification: Falsifiability-Aware Conformal Routing for Mixture-of-Agents (C-MoA)
- arXiv 2609.25959, 2026-09-22. Full text read this sitting (77,035 chars) - HELD SHELL, banked as
  delta only.
- Quote: "heterogeneous agents can jointly repeat an unsupported claim or omit a correct specialist
  fact."
- Why (RQ5): converts the consensus-illusion verdict from a ban into a calibration protocol.
  Agreement is decomposed to atomic claims, semantic inter-agent support becomes a claim-level
  nonconformity score, and an example-level conformal threshold gives distribution-free within-
  domain retention control: retained-claim precision on long-form generation nearly doubles (0.41
  to 0.75), transfers across domains without recalibration, and its one measured failure mode is
  short-form answering "where consensus is cheap and the score is left near chance." The CONTRA-MoA
  extension (blinded near-miss tournament, leave-one-agent-out stability) helps only when the
  verifier holds domain knowledge (half of false medical claims dropped at 0.940 precision) and is
  near chance with a memory-only judge (AUC 0.531 / 0.511); naive max fusion DEGRADES the
  agreement signal (0.687 to 0.652). This is the estate's cheap-judge law measured by someone else:
  a flock CAN produce grounded verdicts if its agreement is claim-level calibrated by a competent
  verifier - and the counterfactual arm must not run on a judge that lacks the domain.
- Overlap: ALREADY HELD - id 2609.25959 registered in memory/runs/corpus_gap_research/
  ARXIV_REGISTER.json and MAP_BACKFILL.json/md (frontier_olm_20260928 swarm lane) and mined by
  mickey17 (swarm-econ-week lane). NOT re-banked as new; this row banks the measured numbers the
  held shell lacks, per the burns lens's held-shell-delta pattern. Quote verified against the full
  HTML fetched this sitting.

### 8. Waggle: Learning One Anonymous Local Law for Self-Organizing LLM Swarms
- arXiv 2609.34136, 2026-09-28. Read at abstract level only (export API id_list fetch this
  sitting) - FLAGGED, full text not read.
- Quote: "the same learned law remains effective as populations and interaction budgets change,
  retains over 96% of substrate-specific oracle quality, and transfers without retraining".
- Why (RQ4/RQ1): the closest in-window paper to the estate's law-carrying mesh. Instead of learned
  roles, hierarchies, or routing topologies, one anonymous local law (jointly selecting task
  actions, semantic communication, and local commitment updates) executed repeatedly by
  interchangeable agents yields coordination that forms, persists, and reorganizes online -
  learned by Swarm-Consistent Distillation with anonymous-orbit consistency, no added inference-time
  components. That is the rib_bus doctrine (feed structures/laws, not prose; no throne) as a
  learned artifact, and its population/budget-shift robustness claim is the property the estate's
  width law needs when the envelope moves. Full-text read owed before any mechanism port.
- Overlap: catalog 0; memory single-pass grep hit only Gutenberg texts (the ordinary English word
  "waggle"); not in registers or today's register. NEW at abstract level.

## RQ synthesis (answers, grounded in this sitting's reads)

1. **PANDA port vs contradict (RQ1):** PANDA mechanisms re-read first-hand this sitting. PORT: the
   swap protocol (reassign a dead vertex's subtask to a compatible agent already in the team before
   recruiting - the estate's pending sibling-takeover probe is this), monotonic generation numbers
   on reissues (kills zombie duplicates of re-done work; pairs with item 1's epoch fencing), and
   checkpointing plan state to a peer for warm orchestrator restart (lane trails already are that
   checkpoint; the research lane's 387 OSError-on-runner_state failures show the checkpoint file is
   the fragile point to harden). CONTRADICTS: redundant execution (dispatch each subtask to n
   agents, accept first success, cancel the rest) spends n-1x tokens by design and presumes
   cancellation is real - on a quota-walled account that multiplies 429/1302 contact probability
   and, per item 1, cancelled children may still complete and settle. PANDA's assumption is
   capability-elastic compute; the estate's measured envelope is a rolling-throughput cap.
2. **Quota-wall queue policy (RQ2):** the census names the gap (0 in-lane retry on elder/harvest
   daily 429s before the 10-03 starvation failover; redo-only recovery), DEALS names the routing
   half (backpressure on measured backlog differentials, hop limits, split-and-requeue), and item 3
   names the admission half (release budget: cap committed-but-unfinished work below the wall, so
   the first 429 is a HOLD that re-prioritizes ready work rather than a wall that kills committed
   lanes). The preventive shape is the composition, plus item 1's settlement rule so a re-route
   cannot double-spend.
3. **Redo-vs-resume replication (RQ3):** the estate's own census ran this sitting: 26 fatal
   limit-class lane deaths (elder 14, harvest 12), 0 resumed, 26 re-done next cycle (100 percent
   re-done-not-resumed at the lane level, on a 7,492-row trail corpus), matching the banked HN
   census's direction (438 redone vs 8 resumed, resumed all died). Measured caveat per item 4: the
   fraction is a count, not yet a quality verdict; the four-diagnostic columns are owed before
   calling resumed-work hopeless. Workflow-level quota deaths (code 1005) leave no lane-trail row
   at all - they are invisible to this corpus, which is itself a finding: the workflow runner needs
   its own trail.
4. **Mesh-level diagnosis for rib_bus (RQ4):** two adoptable shapes, post-hoc (DCFA: causal
   dependency graph + counterfactual refinement over the already-stored message graph, 2 LLM calls)
   and runtime (ResonAct: external control plane over the event stream, streaming health metrics,
   policy-keyed remediation including the silent-failure class). Both re-use data rib_bus already
   carries; neither requires modifying agents - which fits the no-throne/no-orchestrator laws.
5. **Flock vs one seat (RQ5):** post-bank evidence TIGHTENS the valid-uses list rather than moving
   divergent sampling off it. Item 2 shows debate flocks must beat budget-matched self-consistency
   to justify themselves on verifiable tasks (they did not, at 5,500+ runs), and C-MoA shows the
   one measured way a flock's agreement becomes usable on grounded claims: claim-level conformal
   calibration with a competent verifier. The estate's un-run instrument is now precisely defined:
   a flock-vs-self-consistency A/B at matched tokens, scored by the four diagnostics of item 4.

## Falsifiers / limits

- All quotes verified verbatim against files fetched this sitting (the two Q1/Q7 quotes span my
  tag-flattening line breaks; the sentences are continuous in the fetched pages).
- Item 8 is abstract-level, flagged as such; its mechanism claims are the authors' own and unread.
- The census is one instrument at one moment (2026-10-03 sitting, venv python, glob over
  queue/lanes/*/trail.jsonl); per the counts law, do not difference it against counts taken by
  other instruments at other moments. Its limit-pattern match is substring-based; the prose lane's
  "stale=1005" row showed how a false positive looks, and row-level reading (not counts) backs
  every number above.
- PANDA and DEALS deep reads served the RQ synthesis only; both are banked finds (register rows r1,
  r4) and are NOT counted as new banks here.
- WebSearch was not needed this sitting (the export API answered all queries); no door degraded.
