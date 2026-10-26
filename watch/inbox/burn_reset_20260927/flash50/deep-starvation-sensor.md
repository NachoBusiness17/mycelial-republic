# deep-starvation-sensor: the STARVED event generalized to any resource-flow DAG

- Item: deep item, flash50 wave, 2026-09-28. Companion prototype banked alongside: `starvation_sensor.py` (this directory).
- Grounding: every code line cited below was read this session; every check reported was executed this session with the repo venv (`.venv/Scripts/python.exe`). Literature anchors in section 8 are cited from model knowledge and flagged as not fetched this session.
- The ask: water_graph.py's STARVED event detects starvation in a directed water graph. Generalize to a starvation sensor for ANY resource-flow DAG (tokens, attention, compute, API budget). Name the universal starvation patterns. Deliver design + prototype.

## 1. What the estate already has (receipts, first-hand)

The sensor under generalization is not a hypothetical. It exists, it was born 2026-09-28, and it has a test contract:

1. **The STARVED event.** `mag/water_graph.py:180-186`: a gated junction (xor/sill) holding pooled volume spills it and emits `Junction {name} STARVED: {spill} pooled units spilled to waste ({why}; no inflow reached the gate).` The comment block at `mag/water_graph.py:141-150` records the law and its origin: the operator's "this whole starve-out thing is bullshit and our water computer spec should have picked it up", plus the two-part fix: under-gate inflow HELDS rather than spills (`water_graph.py:170-174`), and a pool dying with zero new inflow spills AND is NAMED.
2. **The test contract.** `tests/test_water_graph_starvation.py:33-62` pins the three-state semantics: pooling with live inflow is NOT starvation (`test_starved_junction_pools_instead_of_eating`), a pool dying with no inflow IS and must be named (`test_starved_event_fires_when_pooled_water_dies`), and pooling must still be able to reach the gate later (`test_pool_can_still_reach_the_gate`). Executed this session: `python -m pytest tests/test_water_graph_starvation.py -q` -> `4 passed in 0.52s`.
3. **A second, older starvation sensor mode: the budget verdict.** `mag/hydro_xor_sim.py:88-98` classifies a siphon run by wall-clock bands: `FAIL 131-169 (siphon primed but did not break)` and `FAIL >=170 (siphon never primed)`. That is a time-boxed non-delivery detector: when no witness predicate exists, a deadline is the sensor.
4. **Attention as a starvable resource, already modeled.** `mag/invariant_npcs.py:10`: the invariant NPCs "are NOURISHED by attention (cadence) and starve without it". The estate already treats attention as a flow that keeps entities alive.
5. **Token-budget starvation, already annotated.** `mag/max_distill_arms.py:214`: "reasoning tokens consume the budget, so C gets 1536 (512 starves it empty)". Sibling flow-starve annotations exist at `mag/swarm_worker.py:385` (gated old tasks starving fresh queueing) and `mag/lattice_loop.py:657` (a URL queue starving the stack after 2 knots). The pattern is endemic; it just never had a named sensor outside water.
6. **The live silent-starvation census.** `watch/inbox/burn_wave_20260926/B2_443_dwf_error_census_20260926.md` (read this session): 896 `model.network.failed` events across 375 `sess_dwf-*` actor sessions in 27 workflow runs (CLI logs 09-20..09-26), 850 with 429 retryable:true, 817 of those the z.ai plan rate-limit statusMessage "[1302][Rate limit reached for requests]"; 11 terminal actors (no completion after their last failure) across 2 runs that no receipt or tally named. The structural cause is first-hand verified this session: `tools/provider_error_tally.py:75-81` `_belongs()` only matches a line whose sessionId equals or prefix-extends the queried session, or whose parentSessionId equals it. A workflow child's `sess_dwf-dwfrun-<runid>-actor_1_13` satisfies none of the three, so the tally cannot see child starvation at all. Per AGENTS.md (fan-out width law), workflow children run `maxAttempts 0`: they die on first 429/1302 with zero retry budget. That is the hold-and-spill shape of `water_graph.py:170-186` with the STARVED line deleted.

## 2. New finding, proven this session: the estate engine can create resources out of nothing

While porting the flow laws into the generic engine, the deferral shape exposed a latent double-spend in the estate engine itself. `water_graph._available()` (`mag/water_graph.py:198-214`) reads `src.volume` and returns `min(cap, src.volume)` WITHOUT committing; the commit happens later in the gate phase (`water_graph.py:160-174`). When one source feeds TWO or more gated junctions, each deferral reads the same un-decremented balance:

Repro executed this session (repo venv, `mag.water_graph`):

```
src volume=2, pipes p1->j1 cap=2, p2->j2 cap=2, both j* sill=2
tick -> events: ['Junction j1 holds 2 below gate (1 < sill 2); pooling.',
                 'Junction j2 holds 2 below gate (1 < sill 2); pooling.']
src.volume after tick: -2     j1.volume: 2   j2.volume: 2
```

The source held 2 units; the engine debited 4. Two units were created from nothing, the event stream looks perfectly healthy ("holds ... pooling" twice), and no STARVED or error line fires. Existing tests never exercise a shared source (`tests/test_water_graph_starvation.py:20-30` uses two distinct sources), so this is invisible to the current suite. The general lesson is the core design principle of this item: **event-stream health is not ledger health**. A sensor that reads events alone sees two polite holds; only a per-node conservation audit sees the impossible balance. The generic engine fixes it by reserving at read time (debit the source when the deferral is queued); section 6 carries that into the design.

## 3. Theory: starvation is a liveness property, and that dictates the sensor's shape

Starvation is not a state you can point at; it is a claim about all futures ("this demand is never served"). In the safety/liveness partition of concurrent-systems theory (Lamport 1977; flagged as from-knowledge, section 8), starvation sits on the liveness side, like deadlock-freedom's weaker sibling. Coffman's four conditions (Coffman, Elphick, Shoshani 1971) characterize DEADLOCK (nobody moves); starvation is its asymmetric cousin: others move while one waits forever. Liveness cannot be decided by inspecting one snapshot, which is exactly why the estate needed a *law* (the operator had to order it) rather than a check. Any starvation sensor therefore needs one of three detection modes, and all three already exist in the estate in miniature:

- **M1 static (conservative, zero ticks).** Prove starvation POSSIBLE-BY-CONSTRUCTION from the graph shape alone: a demand node with no live route from any source; a gate whose input shape can never satisfy it. Safety-style: sound but incomplete (finds possibilities, not occurrences).
- **M2 witness (online, state-based).** A per-tick predicate whose persistence names a starvation in progress. The STARVED line is M2: the witness is `pool > 0 AND inflow == 0` at a gated node. Witness-based detection is how model checkers discharge liveness with fairness constraints.
- **M3 budget (time-boxed).** When no witness predicate is expressible, a deadline is the sensor: `hydro_xor_sim.py:98` `FAIL >=170 (siphon never primed)` generalizes to "a demand node owes a delivery receipt every B ticks".

## 4. The universal starvation patterns (derived from the flow laws, not invented)

Each pattern below is a flow LAW of `water_graph.py` plus the failure mode that law enables. This is the claim of the item: these seven are universal because any resource-flow DAG that has direction, capacity, thresholds, gates, sinks, and an out-of-band medium will exhibit exactly these failures, whatever the units are.

| # | Pattern | Flow law (water line) | Signature |
|---|---------|----------------------|-----------|
| P1 | Topological starvation | direction: flow only downhill, `src.elev > dst.elev` (:203, :223, :233-234) | demand node unreachable from any live source; static, detectable at build time |
| P2 | Gate starvation (hold-and-spill) | gating + hold+spill: xor exactly-one / sill >= N (:156-157), HOLD (:170-174), STARVED (:180-186) | pool > 0 with zero new inflow at a gated node; the witness strike |
| P3 | Threshold split (crest deadlock) | crest: a siphon primes only at crest volume (:204-211) | fed every tick, volume never rises toward the threshold; dribble + competing drain pin the buffer below the batch |
| P4 | Collision loss | xor both-inlets: the docstring shape (:15-17) records overflow-to-waste when 2 inlets arrive; current code HOLDS both (:170-174) | k > gate-arity arrivals in one tick; work arrived in the wrong tick shape and is deferred or destroyed |
| P5 | Out-of-band drain | steam: lifts out of the pipe medium, condenses at the highest cold node, falls back if none (:95-105) | units leave the metered DAG; every metered edge reads healthy while the demand starves |
| P6 | Supply cut | source/waste: production stops, waste swallows silently (:237-239) | all sources dry while demand stays enabled; downstream balances decay monotonically |
| P7 | Unnamed loss (the meta-pattern) | conservation: NEW law L7 in the prototype | debits at a node with no matching named event; silent starvation ANYWHERE, including resource creation (section 2) and resource destruction (B2-443) |

P7 is the one the water engine did NOT need until section 2 proved otherwise: water_graph's events are named per move, so event-readers were safe, until the deferral gap let the LEDGER diverge from the EVENTS while both stayed internally consistent. P7 is also the pattern B2-443 measured at fleet scale: units (asks, retries, actor lifetimes) destroyed with no tally line, because the tally's attribution predicate cannot see the node class where the losses happen (`tools/provider_error_tally.py:75-81`).

## 5. Media mapping: the same seven patterns on tokens, attention, compute, API budget

- **Tokens (context as the fluid).** Node = a seat's context window; pipe = prompt assembly (context-pack, rib injection); cap = per-source injection budget; sill = the minimum viable context (a seat below it produces flabby or empty output, the gemma EMPTY class of Q-022); crest = the batch threshold of a summarizer; steam = compaction/summarization lifting content out of the window (P5: condensed at the wrong node, the seat that needed the detail never sees it); P7 = the context tax paid in tokens that no per-seat ledger records.
- **Attention.** Node = a token position or a head; the resource is softmax mass. P2 is attention collapse (a sink absorbs mass, positions downstream starve; StreamingLLM's attention-sink finding, section 8). P3 is a head that needs a minimum activation to fire and never accumulates it under normalization pressure. P6 is a pruned upstream layer cutting supply. The estate's own formulation: invariants "NOURISHED by attention (cadence) and starve without it" (`mag/invariant_npcs.py:10`), where cadence is the rate and neglect is the cut.
- **Compute.** Node = a worker/GPU/queue slot; pipe cap = scheduler quantum; sill = minimum viable batch (Orca's iteration-level scheduling exists precisely to lower that crest, section 8); crest = burst-buffer warmup; elevation = affinity and data-locality constraints (a job cannot run "uphill" of its data); P4 = two jobs arriving for one exactly-once slot; P2 = the batcher that holds a partial batch and discards it on shutdown.
- **API budget.** Node = a lane or account (the DRIVING LADDER's funded Hermes lanes vs unfunded free lanes, per AGENTS.md); pipe cap = rate limit; source = the rolling window; P6 = the window decay; P2 = the child that holds a dispatched ask and dies on first 429/1302 with maxAttempts 0; P5 = retries routed outside the metered tally; P7 = B2-443's 896 invisible failures. The case C1/C2 demo in section 7 replays exactly this shape and shows the named-vs-silent difference: same physics, one sensor line versus zero.

## 6. The design: `FlowNet` + `StarvationSensor`

Prototype: `starvation_sensor.py` in this directory (22,253 bytes, stdlib-only, deterministic, integer volumes, no floats, no RNG, no subprocesses, so the win32 CREATE_NO_WINDOW law is trivially satisfied).

Contracts:

1. **Model.** `FNode(name, kind, elev, volume, rate, demand_rate, batch_min, gate, sill, oob_to, oob_rate, silent_spill)`; `FEdge(name, src, dst, cap)`. The laws L1-L7 in the module docstring map 1:1 to the water lines cited in sections 1 and 4, plus the new conservation law L7. Gates live on a `gate` attribute rather than node kind, so any junction kind can be gated (the generalization over water, where kind IS the gate).
2. **Engine emits an op ledger, not just events.** Every volume change is an `Op(node, delta, kind, named, detail)`. Named ops surface as event lines; the pre-law `silent_spill` junction emits an UNNAMED op and NO line. This is what makes P7 detectable on engines the sensor does not control: audit the ledger, compare to the snapshot delta.
3. **`StarvationSensor.observe(before_snapshot, ops)` runs after every tick** and maintains: per-(node) unnamed-loss totals (P7), per-demand unmet-tick counters with receipt clearing (M3, P2/P6), crest-split strike counters keyed to a progress baseline (P3), source-dry counters (P6), out-of-band drain flags (P5). Findings are `Finding(tick, pattern, node, units, detail)` and every finding names the node, the units, and the tick: the water law's own contract (`water_graph.py:149-150`, "the sensor the spec lacked").
4. **The strike-vs-progress rule (the subtle one, learned by breaking it).** The first cut fired CREST_SPLIT after N fed ticks below the crest. The demo then exposed a false positive: a demand fed 1/tick toward a batch of 5 IS below crest for 4 ticks and then serves. Delay is not starvation. The fix: a strike only accumulates while the node's volume never EXCEEDS its level at strike start; any rise resets the strike. Starvation witnesses must be trajectory claims (no progress across the window), not level claims (currently below). Symmetrically, a receipt (serve op) this tick clears the unmet counter even though serving empties the buffer back below the batch: the deadline measures receipts, not balances.
5. **`static_check(net)` is M1.** BFS from sources over live edges (an edge is live iff `src.elev > dst.elev`), flags demand nodes with no live route (P1) and xor gates with more than one live inlet (P4 possible), at zero ticks. Deliberately does NOT attempt static crest analysis: threshold reachability depends on scheduling, which is liveness; M1 stays conservative by design.
6. **Reservation at read.** The engine debits a source when its flow is deferred into a gated node (the section 2 fix). Any DAG engine feeding this sensor should do the same, or the conservation audit will (correctly) scream UNNAMED_LOSS on every shared-source tick: the sensor is what turns the estate engine's latent -2 into a filed finding instead of a silent impossibility.

## 7. Verified run

Command (this session): `./.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/starvation_sensor.py` -> EXIT 0. Full output:

```
=== CASE A: gate starvation (sill pools 4, pool dies) ===
t1 jx holds 4 below gate (sill); pooling.
t2 jx STARVED: 4 pooled units spilled (sill).
t3 (no movement)

=== CASE B: crest split (batch_min never crossed under a drip-leak) ===
t1 src produces +1.
t1 feed: 1 src->bat.
t1 serve: 1 bat->out.
t1 drip: 1 out->leak.
t2 src produces +1.
t2 feed: 1 src->bat.
t2 serve: 1 bat->out.
t2 drip: 1 out->leak.
t3 src produces +1.
t3 feed: 1 src->bat.
t3 serve: 1 bat->out.
t3 drip: 1 out->leak.
[t3] CREST_SPLIT    node=out units=0 :: fed 3 ticks, volume never rises toward batch_min 5
t4 src produces +1.
t4 feed: 1 src->bat.
t4 serve: 1 bat->out.
t4 drip: 1 out->leak.
t5 src produces +1.
t5 feed: 1 src->bat.
t5 serve: 1 bat->out.
t5 drip: 1 out->leak.
[t5] BUDGET_EXPIRED node=out units=5 :: unmet 5 ticks; largest pool: src (99)
t6 src produces +1.
t6 feed: 1 src->bat.
t6 serve: 1 bat->out.
t6 drip: 1 out->leak.

=== CASE C1: API-budget storm, pre-law gate (silent spill) ===
t1 child_1 holds 1 below gate (sill); pooling.
t1 child_2 holds 1 below gate (sill); pooling.
t1 child_3 holds 1 below gate (sill); pooling.
t1 child_4 holds 1 below gate (sill); pooling.
t1 child_5 holds 1 below gate (sill); pooling.
t2 child_1 holds 1 below gate (sill); pooling.
[t2] UNNAMED_LOSS   node=child_2 units=1 :: units removed with no named event (silent starvation witness)
[t2] UNNAMED_LOSS   node=child_3 units=1 :: units removed with no named event (silent starvation witness)
[t2] UNNAMED_LOSS   node=child_4 units=1 :: units removed with no named event (silent starvation witness)
[t2] UNNAMED_LOSS   node=child_5 units=1 :: units removed with no named event (silent starvation witness)
t3 (no movement)
[t3] UNNAMED_LOSS   node=child_1 units=2 :: units removed with no named event (silent starvation witness)
t4 (no movement)
t5 (no movement)
t6 (no movement)

=== CASE C2: API-budget storm, STARVED-law gate (named spill) ===
t1 child_1 holds 1 below gate (sill); pooling.
t1 child_2 holds 1 below gate (sill); pooling.
t1 child_3 holds 1 below gate (sill); pooling.
t1 child_4 holds 1 below gate (sill); pooling.
t1 child_5 holds 1 below gate (sill); pooling.
t2 child_1 holds 1 below gate (sill); pooling.
t2 child_2 STARVED: 1 pooled units spilled (sill).
t2 child_3 STARVED: 1 pooled units spilled (sill).
t2 child_4 STARVED: 1 pooled units spilled (sill).
t2 child_5 STARVED: 1 pooled units spilled (sill).
t3 child_1 STARVED: 2 pooled units spilled (sill).
t4 (no movement)
t5 (no movement)
t6 (no movement)

=== CASE D: static mode (starvation by construction, zero ticks) ===
[t0] STATIC         node=need units=0 :: no live (downhill) route from any source: starvation by construction
[t0] STATIC         node=x units=2 :: xor gate fed by 2 live inlets: collision-loss possible (water_graph.py:15-17)

=== CROSS-CHECK: the real estate engine names the same starve ===
cross-check vs mag.water_graph.WaterGraph: PASS :: Junction jx STARVED: 4 pooled units spilled to waste (0 < sill 2; no inflow reached the gate).
```

Reading the run: Case A is the water test shape rebuilt generically and cross-checked against the real engine (both name the same 4-unit starve). Case B shows both strike disciplines working: the demand never rises toward its crest (genuine split) and the deadline names the largest pool (the source hoarding 99 while the drip lane eats 1/tick). Case C1 versus C2 is the whole argument in one picture: identical physics (six units in, zero served, six spilled across five children), the pre-law gate produces ZERO event lines at the spill ticks and is caught only by the conservation audit's UNNAMED_LOSS findings, while the STARVED-law gate names every spill itself. Case D proves starvation at build time before a single tick runs. The estate suite stayed green throughout: `python -m pytest tests/test_water_graph_starvation.py -q` -> `4 passed in 0.52s` (run mid-session; the estate engine was not modified).

## 8. Literature anchors

Flagged honestly: the following are cited from model knowledge and were NOT fetched or verified this session. They are chosen as the canonical anchors for each design claim, and the fleet should pull bytes before quoting them further (OWED, section 10).

- Safety vs liveness: Lamport, "Proving the Correctness of Multiprocess Programs", IEEE TSE 1977 (the partition that puts starvation on the liveness side and forces the three detection modes).
- Deadlock vs starvation: Coffman, Elphick, Shoshani, "System Deadlocks", Computing Surveys 1971 (the four conditions characterize deadlock; starvation is the asymmetric remainder).
- Queueing: Little, "A Proof for the Queuing Formula L = lambda W", Operations Research 1961 (a demand node's backlog, arrival rate, and wait are one constraint; sustained unmet demand with a fat upstream pool is a Little's-Law contradiction visible to M2).
- Backpressure/stability: Tassiulas, Ephremides, "Stability properties of constrained queueing systems and scheduling policies for maximum throughput in multihop radio networks", IEEE Trans. Automatic Control 1992 (stability = every queue stable under a routing policy; starvation is the per-node negation, and differential backlog across an edge is the routing signal, the same signal my strike counters measure).
- Fairness: Demers, Keshav, Shenker, "Analysis and Simulation of a Fair Queueing Algorithm", SIGCOMM 1989 (max-min fairness gives the formal definition: a flow is starved iff its allocation is below its bottleneck fair share).
- Congestion: Chiu, Jain, "Analysis of the Increase and Decrease Algorithms for Congestion Avoidance in Computer Networks", Computer Networks and ISDN Systems 1989 (AIMD: the 429/1302 storm domain, where the fan-out width law is the additive-increase knob and the first 429 is the multiplicative-decrease signal).
- Worst-case injection: Borodin, Kleinberg, Raghavan, Sudan, Williamson, "Adversarial Queueing Theory", JACM 2001 (universal patterns must hold under adversarial arrival, not stochastic arrival; a sensor tuned to average load misses exactly the storms B2-443 censused).
- LLM serving: Yu et al., "Orca: A Distributed Serving System for Transformer-Based Generative Models", OSDI 2022 (iteration-level scheduling = lowering the batch crest); Kwon et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention", SOSP 2023 (KV-cache as the scarce fluid; preemption under pressure = hold-and-spill of running requests, the P2 shape at production scale).
- Attention as resource: Xiao et al., "Efficient Streaming Language Models with Attention Sinks", arXiv:2309.17453 (2023) (initial tokens absorb disproportionate attention: the anti-starvation concentrate, whose shadow side is P2 for every other position).

## 9. Where this lands in the fleet

1. **The owed B2-443 build is a P7 sensor.** The census names the owed `--dwf-run` tally mode (attribute by `sess_dwf-<runid>` prefix). Generalized per this design: the workflow run is a FlowNet (account -> children -> actor completions), serves are `model.network.completed`, spills are terminal actors, and the conservation audit (asks dispatched minus receipts minus named failures) IS the starvation line. It would have named runs dd7232ea and 6d7af824 at first contact instead of after an ad-hoc sweep.
2. **The water engine's section 2 gap deserves a reservation fix upstream** (debit at deferral) plus one regression test with a shared source feeding two gated junctions. Not done by this seat (estate code, sibling-lane surface risk); filed here as the finding with a runnable repro.
3. **Threshold parameterization is per-medium:** water needs one strike (a dead pool is unambiguously dead), API budgets want strikes-before-spill > 1 (a window can refill), attention cadences want M3 deadlines in days, not ticks. The sensor already parameterizes `split_patience`, `cut_patience`, `deadline`; the spill strike count is engine-side today and should become a node parameter if ported onto water_graph.
4. **FKB/ratchet hook:** UNNAMED_LOSS findings are exactly the class of signal the FKB indexer should escalate at count>=1 severity=error (the fake-success/collapse class), since an unnamed loss is by definition invisible to every other surface.

## 10. Not done / OWED

- Literature bytes not pulled this session (section 8 flags each as from-knowledge): fetch before external quoting.
- The estate `water_graph.py` was NOT modified (finding in section 2 is report-only, with repro output above). A fix plus shared-source regression test is proposed, not landed.
- The prototype's `oob_to`/`oob_rate` (P5) path is implemented but only exercised indirectly (no dedicated OOB case in the demo run); its `kind == "sink"` drain flag is code-read, not demo-proven.
- No full `pytest -q` run: this item touched no estate code paths beyond reading them; the named suite (`tests/test_water_graph_starvation.py`, 4 passed) is the full touched-surface check, per the census denominator law run at file scope.
