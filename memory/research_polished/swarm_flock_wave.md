# SWARM_FLOCK_WAVE — polished research thread
Cluster: swarm_flock_wave (10 packs) · Polished: 2026-09-20 burn wave
Register: memory/runs/mickey17/digest_rp_*.jsonl · Packs: memory/research_packs/
Re-verified this polish against the live tree (mag/ line numbers re-checked 2026-09-20).

## 1. Thread essence

Can a leaderless, stateless, content-addressed swarm steer itself, verify its own
witnesses, and *prove* its own emergence with bytes instead of belief? The thread runs
from the naming act — the whole system is "archive-driven Quality-Diversity search
under geometric steering with bandit gating" (deep_research_architecture_synthesis) —
through leaderless coordination contracts (deep_research_stateless_swarm_edge), an
external protocol reality-check (THE50_W7_T33_A2A_VS_MESH), the flock's own gate
receipts (flock_steal_* x3), a $0 emergent-behavior curriculum (steal_shadertoy),
the honesty law for consensus (steal_gap_swarm_independence), the emergence meter
(steal_deep_research_emergence_grid), and the closed-loop control application
(hil-setpoint-flock-control). One spine: **legible self-measurement is the coordination
mechanism** — every pack either builds a meter or tries to cheat-proof one.

## 2. Merged findings (deduplicated)

**F1. The whole QD/swarm architecture is bottlenecked on semantic honesty of the
distance field.** sha256-space "novelty" is hash dispersion, not semantic surprise;
the archive can fill with orthographic diversity while signal looks healthy — "geometry
theater". Named kill criteria: semantic embed must raise holdout novelty-agreement and
diamond precision within 2 cycles; cross-run elite Jaccard proves stateless
reproducibility; reinforcement rising while external probe lift flat = self-licking
loop, halt autorun. **Criteria filed, never run.**
Cites: deep_research_architecture_synthesis.answer.remote.md; corroborated by
deep_research_stateless_swarm_edge.answer.remote.md ("no more steering primitives
until semantic distance is real"). Re-verified this polish: no embedder module in mag/
(grep for nomic/bert-mini/onnx/embedder hits only economics prose). Owed.

**F2. Eight leaderless contracts are specified, none wired.** Content-addressed
immutability + stateless workers enable orchestrator-free patterns, all defaulting to
$0/deterministic with anomaly-gated frontier entry: (1) tip-gated speculative prefetch
(fail-closed on merkle mismatch); (2) steal-fold bloom cascade (bloom as verkle leaf,
check-before-enqueue); (3) invariant-pressure self-shedding; (4) merkle-root epidemic
gossip; (5) skill-ledger residual mining; (6) deterministic shadow quorum voting on
hash equality (split-brain abort); (7) compact-frontier expand-swarm ladder; (8)
case-law tip pinning. Each carries its own fail condition (tip mismatch, split-brain,
tier violation = bug). **No execution receipts anywhere** — architecture-native paper
only. Cheapest two first: bloom cascade, tip-gated prefetch.
Cites: deep_research_stateless_swarm_edge.answer.remote.md.

**F3. A2A vs mesh: opposite trusts, no adoption, three rows stolen.** A2A v1.0.0
(Linux Foundation, opaque-agent interop between strangers) vs the filesystem mesh
(legible cooperation between known seats): opacity is a bug in this house; per-seat
HTTP servers solve a problem the fleet does not have (and A2A's own webhooks fall back
to plain HTTP/JSON). Adoptable: R1 task-state enum — terminal vs interrupted states,
with `input_required` as the honest name for operator-gated packets; R2 AgentCard-shaped
per-seat manifests filed in rib_bus (publish-once, no new plumbing); R3 at-least-once +
idempotent-consumer contract as law for bus folds, deduping on content ids. Evidence it
is needed: 50 writer nonce-gap fold_warnings in INDEX.json:16-65; the content-hash-id
half is already adopted (fleet commit 4ad6eb0d6, JEV-1). Re-verified this polish:
no `input_required` in queue/todo.md or mag/chan.py; no agent cards in rib_bus — R1/R2
and the R3 contract text still unadopted. Spec-level only (no A2A server/SDK run;
a2a.proto never fetched).
Cites: THE50_W7_T33_A2A_VS_MESH.md (3 live fetches).

**F4. Consensus honesty law: agreement only counts if witnesses are independent —
BUILT AND VERIFIED.** "Agreement = don't re-pay" is honest only if the agreeing cheap
witnesses cite non-overlapping sources; N witnesses on one source ≈ 1 opinion.
Adapted from agentswarm's evidenceOverlap/scaleK: scale aggregation by mean pairwise
source overlap (0.7·Jaccard(urls) + 0.3·Jaccard(domains)); fail-open — 0 independent
witnesses ⇒ NOT converged; frontier-budget exhaustion reported honestly, never silent
re-pay; unrepresentable states illegal (covered-with-divergence, escalate-with-zero-
budget). Re-verified this polish at exact lines: mag/gap_swarm_experiment.py
`independent_witnesses` L291, `decide_escalation` L340, `gap_map` L381,
`gap_map_precision` L487. **The cluster's strongest verified build.**
Cites: steal_gap_swarm_independence_20260811.answer.remote.md.

**F5. Emergence meter shipped, never switched on.** Genuine emergence = capability
grown from own folds, measured as real per-cycle deltas across five axes — compounding
(invariants/classified/facts/worlds up), efficiency (cost-per-request down, cache-hit
held), self-correction (false-positives, spikes caught), latent discovery (shadow_graph
nodes/edges), traceability (vertical origin pointers). mag/emergence.py implements
cycle() L161, track() L145, emergence() L195, GRID=memory/emergence/grid.jsonl L44 with
auto-mkdir L146. Re-verified this polish: **memory/emergence/ does not exist — zero
rows ever appended.** Shipped code holding no data.
Cites: steal_deep_research_emergence_grid_20260811.answer.remote.md.

**F6. Spatial hashing landed end-to-end — the cluster's best steal→build→wire chain.**
The ShaderToy corpus read as a parameterized curriculum for local-rules→global-emergence
yielded 5 invariants (boids local rules, data-parallel shared state, FBO ping-pong,
spatial hashing, flow fields). The unlock was grid-hash O(N) neighbor search replacing
O(N²) seams(): mag/flock_grid.py (96 lines, docstring cites the operator's boid-shader
steal) and memweave.py L72 calls `fg.seams_spatial(...)`. Re-verified this polish.
Contradiction carried honestly: the corpus fetch itself 403'd — techniques are
knowledge-grounded (marked SPECULATION in the pack), and the tuned parameter-regime
theft (sep/align/coh weights, radii, cell sizes) plus frontier elevation were never
done (unfunded API). The one concrete invariant was independently verified in code.
Cites: steal_shadertoy_flocking_training_corpus_20260811.answer.remote.md.

**F7. Flock-steal gate case law: refire→verify, with a suspected meter bug.** Three
receipts (mag/flock_steal.py, 225 lines, verified present): doctrine question
"memlang x RIB x weave sound?" first pass → unanimous refire (1.0) at phi_goal 9.938;
re-fired 18 min later → send (0.75) at phi_goal 0.0. The loop pattern (unanimous
reject → re-fire → accept) is the durable case law. Contradiction carried: phi_goal
0.0 more likely means phi was not recomputed on the verify pass than perfect
convergence — stub cannot disambiguate; suspect one-line fold bug. Second carried
limit: consensus verbs (send/cross/refire) are story-domain; the eval-flock receipt
(consensus cross 0.6 on the sha256-dedup question) decodes to no real decision —
dead-end case law unless the run's raw answer or decoded scratch is recovered.
Cites: flock_steal_memweave-test_20260810.answer.remote.md;
flock_steal_memweave-verify_20260810.answer.remote.md;
flock_steal_eval-flock_20260810.answer.remote.md.

**F8. HIL setpoint control: fully grounded design, zero build.** Constrained control
(hold CPU/mem setpoints AND throughput) can be flock-learned from a measured
(setpoint, error, actuation, throughput) trail instead of hand-tuned PID — learning-
based control (extremum-seeking + swarm optimization, honestly attributed). Loop:
SETPOINT→SENSE(system_telemetry)→ERROR→ACTUATE(resource_governor)→MEASURE→LOG→
FLOCK-LEARN; ghost_control is the surface, mem_invariant_map the multi-modal lance.
Re-verified this polish: all six referenced modules exist (system_telemetry,
resource_governor, ghost_control, mem_invariant_map, flock_field, gpu_lifecycle);
**no "setpoint" token anywhere in mag/** — unbuilt, buildable today from existing
parts. The trail columns are the whole evidence standard.
Cites: hil-setpoint-flock-control.md.

**Resolved vs carried contradictions**
- Mesh obsolete because of A2A? Resolved: no — opposite trust models (F3).
- memlang x RIB x weave doctrine sound? Resolved weakly: approved after refire at 0.75
  majority — case law, not proof (F7).
- phi_goal 9.938→0.0 between passes: carried as probable non-recompute bug (F7).
- ShaderToy corpus as live training data vs 403 fetch: carried — knowledge-grounded
  only; its one concrete invariant separately verified in code (F6).
- "Architecture is novel" (architecture_synthesis §4) vs nothing measured: carried —
  novelty claims (portable QD state, invariant-lens-conditioned QD) are untested until
  the kill criteria run (F1).

## 3. Verified/built vs unverified/owed

**Verified/built (receipts re-checked this polish)**
- gap_swarm_experiment.py: independence scaling, fail-open escalation table, gap maps —
  exact lines 291/340/381/487; invariants RIB-tested per pack (F4).
- flock_grid.py O(N) spatial hash + memweave.py L72 seams_spatial wiring (F6).
- emergence.py: cycle/track/emergence + GRID path with auto-mkdir — code real (F5).
- flock_steal.py exists; three gate receipts on disk with aligned-invariant headers (F7).
- A2A pack: 3 live spec fetches, row-by-row comparison; content-hash packet ids already
  fleet-adopted (4ad6eb0d6) (F3).
- HIL: all six referenced modules present (F8).

**Unverified/owed**
- Semantic embedder (Move #1) absent from mag/ — gates every QD claim and all new
  steering primitives (F1).
- Kill criteria unrun: no holdout novelty-agreement, diamond precision, cross-run elite
  Jaccard, or reinforcement-vs-probe-lift numbers exist anywhere (F1).
- 8 stateless-swarm contracts: zero wired, zero tested (F2).
- Emergence grid: never executed; memory/emergence/ has zero rows (F5).
- A2A R1/R2 unadopted (no state enum, no seat cards); R3 contract unwritten as law (F3).
- HIL setpoint loop: unbuilt, no setpoint token in mag/ (F8).
- ShaderToy: corpus unfetched (403), parameter-regime theft undone, frontier elevation
  not dispatched (F6).
- Flock-steal stubs carry no answer bodies; consensus-verb decode impossible from stub
  alone; suspected phi_goal non-recompute bug unfixed (F7).

## 4. THE FIVE NEXT ACTIONS

1. **Land the local semantic embedder** (nomic/bert-mini/ONNX, one interface) replacing
   sha256-geometric distance, then actually RUN the two-cycle kill check (holdout
   novelty-agreement + diamond precision). Everything else in the QD stack compounds
   only after this; "no more steering primitives until semantic distance is real" (F1).
2. **Execute one emergence cycle**: `mag.emergence.cycle(track_row=True)` to append the
   first real row to memory/emergence/grid.jsonl (auto-mkdir already handles it). Shipped
   meter, zero data — the first row converts five-axis emergence from belief to bytes (F5).
3. **Wire the two cheapest $0-deterministic swarm contracts with their fail conditions
   as tests**: Steal-Fold Bloom Filter Cascade (bloom as verkle leaf, check before
   enqueue) and Tip-Gated Speculative Prefetch (CAS-write only if merkle_verify(tip)) (F2).
4. **Adopt the three A2A rows**: task-state enum on queue/meter rows (input_required for
   operator-gated packets), one AgentCard-shaped manifest per seat in memory/rib_bus/,
   and the at-least-once + idempotent-consumer contract (dedupe on content ids) written
   as mesh law (F3).
5. **Build the HIL setpoint loop skeleton from existing modules** (the trail columns are
   the evidence standard) and fix the suspected phi_goal non-recompute on flock-steal
   verify passes (one-line) so refire→verify receipts become trustworthy (F7+F8).
