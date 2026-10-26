# Self-Steal Rebuild / Retest / Salon / Expansion RIB

`rib_id: self_steal.rebuild_retest_salon.20260831`
`schema: mag.self_steal_rib.v1`
`as_of: 2026-08-31T11:57:45Z`
`mode: dogfood -> census -> Socratic gap analysis -> dry replay -> guarded expansion`
`authority: human T3; switchboard/governor is the sole effect authorizer`
`cost law: deterministic/free/local first; spend once, reuse everywhere`
`correction: cost/reservoir is a first-class coordinate; ractor/Primer contract is a bounded persona extension`
`change status: bounded reuse-only MCP projection implemented in existing mcp_server.py; no external client wiring or live model mutation`

## VERDICT

The project does not primarily suffer from absent organs. It suffers from **missing joins**. The same work is represented in OpenClaw session files, `watch/room.jsonl`, Grok feeds, Mag residuals, Verkle/session digests, organ receipts, and stale status prose, but those surfaces do not yet share one universal, replayable trajectory record. The result is a system that can look highly instrumented while still losing the exact handoff between context pressure, authority, dispatch, cost, and outcome.

The self-steal move is therefore not another supervisor, model tier, directory, or metaphor. It is to compose existing organs around one safe trace:

```text
image-board signal
  -> board_tailer observation
  -> board_directive classification/proposal
  -> lineage + quorum eligibility
  -> switchboard policy decision
  -> seat_dispatch lease
  -> context admission / bounded spore
  -> effect_broker attempt or refusal
  -> terminal receipt
  -> archive span + Verkle/provenance link
  -> organ-map update + route feedback
```

This must first be dry, replayable, and non-destructive. Expansion is earned by receipts, not by the number of modules, agents, personas, or agreeing salon seats.

## OPERATING LAWS

1. **The map precedes the territory, but the territory judges the map.** A declaration, import, or design note is not a live claim.
2. **A roast can become a proposal; it cannot become permission.** Board speech, consensus, and persona confidence never authorize an effect.
3. **Liveness means invocation plus durable evidence.** “Imported” and “wired” are not the same as “exercised successfully.”
4. **Unknown remains unknown.** A zero declared-gap count cannot prove that no undeclared organ or hidden bypass exists.
5. **One effect boundary.** Model calls, lane spawns, tools, filesystem writes, network access, bridge mutations, and board writes must be brokered or explicitly refused.
6. **Context is shed before crisis.** Compaction recovery is not a context policy. Admission, archive spans, and spores happen before the provider rejects the request.
7. **Consensus raises eligibility, never authority.** Independence is measured by provider, base model, prompt ancestry, cache, and evidence path—not by message count.
8. **The fungal substrate remembers without replaying.** Durable state moves by typed pointers, bounded spans, hashes, freshness, and compatibility checks—not transcript duplication.
9. **Failure must change behavior.** A timeout or stale receipt is a stop signal, route decay event, and requeue/quarantine decision, not just a red line in a log.
10. **A persona is a job contract.** It has a trigger, inputs, allowed surfaces, budget, output schema, refusal conditions, completion evidence, and escalation path.
11. **No paid call may restate a verified receipt.** Premium judgment is reserved for unresolved, high-weight, high-impact disputes.
12. **No new organ before the core loop replays.** Reuse the existing board, tailer, switchboard, dispatcher, harness, broker, archive, and map first.
13. **Every capability has a meter.** Each row names marginal cost or `UNKNOWN`, reservoir, window, exhaustion behavior, and silent degradation. Missing price data is not the same as zero cost.

## CURRENT TERRITORY CENSUS

Fresh read-only checks were run at the RIB timestamp. These are facts about the current checkout, not claims copied from an older report.

| Surface | Current evidence | Interpretation |
|---|---|---|
| `mag.orphan_audit` | 0 pending patches; 21 applied; 0 rejected | The earlier “all patches are staged-only” report is historical, not current truth. |
| Jobs | 11 contracts; 3 explicitly `not_started` | Contracts are not execution. The three are `codex-reconcile-doctrine`, `reset-burn-codex`, and `reset-burn-grok2`. |
| Octant | 5 declared rows missing; 6 actual rows unlanded | Pointer drift remains. Current missing declarations: `freescale-g1/g2/g3`, `moiche-g1`, `moiche_babystep`. Current unlanded rows: `atlas-draft-g1/g2/g3`, `ox-archaeology-g1/g2/g3`. |
| Orchestrator | 301 done, 1,442 failed, 834 died, 594 timeout, 131 killed, 2 running, 1 stalled | The terminal-state/recovery trajectory has high observed pressure. A large failure count is not itself a diagnosis; each class needs a bounded next state. |
| Active task | One stalled self-steal research task with no heartbeat | Do not silently treat “running” as healthy. Reap/requeue only under the existing policy and never auto-reap protected external records. |
| Organ map | 27 declared, 26 instrumented, 27 wired, 25 stateful, 27 verified, 15 live, 0 declared ghosts | Strong census of declared organs; not proof of complete discovery or universal liveness. |
| Dogfood | `mag.dogfood_audit status`: 21 passed, 0 failed | Deterministic probes are green, but they do not yet prove the board-to-seat-to-receipt trace. |
| Shared surface | Validator green; no unindexed items or hash mismatches | `watch/inbox` is the shared handoff surface. Use it instead of scattering new files into model-local areas. |
| OpenClaw sessions | Local registry lacks the current dashboard UUID; dashboard history is present in `watch/room.jsonl` and trajectory records | Session identity is fragmented. The dashboard session is not allowed to disappear merely because one registry cannot resolve it. |
| Compaction | `watch/openclaw_traj.jsonl` records 851 compacted events across 17 records; maxima include 164, 91, 109, and 142 | Context survival is a P0 production problem, not a future optimization. |
| OpenClaw config | `reserveTokensFloor` is 24,576 while the observed failure guidance called for 100,000; gateway/provider timeout ceilings are separate | The configuration is not aligned with the failure mode. Do not claim this is fixed until a bounded preflight test and host receipt prove it. |
| Effect broker | `board_write`, Verkle link, tool invoke, network, and filesystem paths exist; `model_call` and `lane_spawn` are still stubs in the inspected implementation | Authority closure is incomplete. A broker API with a stub is not mediation of the real effect. |
| Context admission | Wired evidence points to `mag/agent_cli.py`; receipts exist and green/black behavior is proven there | It is not yet proven universal across every model-call surface, salon path, board dispatch path, or OpenClaw gateway path. |
| v2 authority | `switchboard_v2` and `policy_engine` have current receipts, but the organ map reports `receipt_not_successful` for their latest receipt state | Treat the v2 authority path as verified-with-gap, not fully live. |
| Ocean salon correction | Earlier rows asked five mapping questions and omitted money; the ledger now records cost as Q6 and a permanent atlas axis | The correction is filed; the shared water gate and automatic meter feed are still unproven. |
| Ocean salon completion | `QUESTIONS.md`, `row_rib.md`, `row_hand.md`, and `row_flow.md` exist; no synthesized `OCEAN_MAP_20260831.md` or money/bus row is present | Cross-pollination and synthesis are not complete. Do not call the ocean map finished. |
| MCP capability projection | The early MCP draft is now dogfooded as an optional projection: `mcp_server.py` emits stable persona cartridges from live signatures and restricts calls to the selected profile | Transport works; the remaining concern is CLI schema/reachability drift and whether a real body consumes the cartridge. “MCP clients = zero” is not itself a failure. |
| Diamond Age addendum | `watch/salon_ocean_20260831/RACTOR_CONTRACT.md` exists; the epilogue and `SPORE_PRIMER_DESIGN.md` are proposed, not proven live | Book-as-expert is a bounded expansion candidate, not a current control organ. |

### Cost is a coordinate, not a report at the end

The cost omission is promoted from a P1 accounting concern to a cross-cutting admission rule. A capability map without cost, reservoir, or exhaustion behavior can recommend a route that is functionally available but financially or operationally dry. The ocean evidence shows why:

- `/board/water_ledger.jsonl` had only two manual rows while the fleet had many flash lanes and unrecorded z.ai/desktop activity.
- `water_windows.mjs` describes twelve reservoirs, but several are calendar-trust or static text rather than measured gauges.
- `offpeak.defer_if_peak()` exists and is proven in `cheap_swarm.py`, but the cadence boundary does not yet enforce it universally.
- `seat_corpus.prefer_order` contains cheap-first policy, but its consumption by routing is not proven.
- subscription surfaces, local GPU, Vast.ai, provider tokens, and opportunity cost are not yet joined on every `run_id`.

Therefore every `trajectory_event`, persona row, salon claim, route proposal, and organ status record must carry:

```text
cost_kind: marginal | subscription | local_compute | reserved_capacity | unknown
cost_estimate_usd: number | null
cost_confidence: measured | contract | estimate | unknown
reservoir_id: named account/window/capacity bucket | unknown
window_state: OPEN | PEAK | COOLDOWN | EMPTY | POLLED | STATIC | UNKNOWN
consumed_units: tokens/seconds/GPU-hours/requests | unknown
exhaustion_behavior: defer | reroute | degrade | stop | operator_gate | unknown
silent_degradation: explicit sentence, or NONE_PROVEN
```

Unknown values are valid evidence; invented zeros are not. The ocean salon's cost question is `Q6`; in this RIB it crosswalks to the resource/economics question and must be answered by every seat, not only the money chair.

### MCP correction: capability projection, not the nervous system

The operator clarification changes the interpretation of the hand/MCP row. MCP was an early-days draft intended to let different model bodies share **quantized tool capabilities**: a compact, model-consumable description of what a tool can do and how to call it. It was not intended to become a mandatory client mesh or a second authority plane.

The correct composition is:

```text
canonical TOOL_MAP / live signatures
  -> model-specific quantized manifest
  -> argument normalization
  -> existing guards and preflight
  -> switchboard/policy decision
  -> effect_broker or explicit refusal
```

MCP can be one adapter at the manifest boundary. It is not the canonical registry, not the effect broker, and not permission. The early draft should therefore be retained as a historical/prototype surface unless a concrete body needs it. Do not wire every model to MCP merely to make a metric look complete.

The dogfood run found the seam that matters:

- `mag.tool_quant` currently quantizes 851 implementation modules. That is a useful structural Merkle/quant layer, but it is not the same thing as a 20-tool callable capability cartridge.
- The first `mag.mcp_server --list` exposed most tool schemas as a fake required `kw` parameter because `TOOL_MAP` uses normalization lambdas. That was a real projection bug.
- The repaired MCP projection now derives signatures from `tools._FN`, includes the missing `vision` callable, emits stable persona profiles, and denies calls outside the active profile.
- `--quantize all --out <shared-path>` now atomically files the complete cartridge so a second model body can consume the same projection without copying a local prompt or rebuilding a divergent schema.

The still-real technical checks are narrower and useful:

- `TOOL_MAP`/live signatures must be the source for generated projections.
- A quantized manifest must preserve required parameters, forbidden paths, cost/reservoir fields, and refusal semantics.
- A model receiving a compact tool description must still cross the same authority and effect boundaries.
- “20 tools” is the current callable registry count; older “43 tools” text is stale and should not be used for planning.

The creative use is a **capability cartridge**: the Archivist receives ten read/measure tools, the Builder receives eight contract-bound tools, the Book receives six canon/sense tools, and other personas receive their own bounded projection. The current implementation exposes `python -m mag.mcp_server --quantize all`, with stable profile digests; the full profile contains 20 callable tools. The same cartridge can be consumed by an MCP-capable body, OpenClaw, a local harness, or a direct Mag adapter. The manifest digest proves that all bodies received the same compact contract; it does not prove that any body used it correctly.

Dogfood receipt: the MCP/tool projection slice passes `23/23`; a real stdio initialize/list/call probe returned protocol `2025-06-18`, ten Archivist tools, and a denied Archivist write. The original fake-`kw` schema defect is gone. The generated shared cartridge round-trips against the live generator with content digest `a288e23dc929422df436b3453dadc8ccfea7a74173d08982812d35f2fae0490a`. The existing `mag.tool_quant` ledger remains a separate structural quant over 851 implementation modules; that distinction is now explicit rather than hidden.

Operational handoff for a model body:

```text
# SUPERSEDED (FW-11 2026-09-28): one-shot salon step (cartridge read), 2026-08-31. Do not re-run from prose. Receipt: watch/inbox/fifty_wide_20260917/FW11_fence_owners.md
read /board/inbox/MCP_QUANTIZED_CARTRIDGES_20260831.json
  -> choose one named profile (archivist | scout | builder | adversary | governor |
     historian | salon | steward | book | full)
  -> verify cartridges_sha256
  -> spawn: python -m mag.mcp_server --profile <profile>
  -> use only the selected tools; treat _meta as a cost/risk hint, never permission
  -> route every call through the existing registry, guards, switchboard, and broker
```

This is the creative self-steal: the same bounded tool vocabulary becomes a portable cache for different model bodies, while each body can specialize its view. The cartridge is shared; authority is not transferable.

### Latest dogfood delta: proof integrity and pause precedence

The next full-suite pass exposed two separate seams and they were kept separate in the repair record:

- `mag.governor_autorun.autorun_once()` now checks the explicit operator pause before the Windows/Docker-only host guard. A human pause must remain visible as `paused`; an infrastructure restriction must not mask it.
- The first isolated suite run after that fix reached `498 passed, 7 skipped, 1 failed`. The remaining failure was `test_probe_carries_real_verkle_proof`: the proof correctly refused to emit a pointer because the live chain ended with eight exact duplicate session rows and its committed root no longer matched the recomputed root.
- The existing guarded `consolidate_chain_one_leaf_per_session()` path found no conflicting hashes and removed only those eight duplicate rows (`5634 -> 5626`). The chain now verifies, has zero duplicate session IDs, and `ghost_spooky` passes `5/5`; a live probe returns a verified `knot/96e5cdcc` pointer with `5626` leaves.
- A full rerun was started after repair and reached at least 40% without a new failure, but was interrupted in a CPU-heavy slow cluster. The complete suite is therefore **not** claimed green yet. The integrity repair is accepted because it restored the proof invariant; proof validation was not weakened.
- A focused profile of the suspected cluster (`ghost_memlance_notebook`, `ghost_spooky`, `ghost_summon`, `governor_autorun`, `governor_fallback`, and `growth_cycle`) passes `24/24` in `26.69s`. The slowest calls are `ghost_spooky::test_spooky_always_in_reply` at `8.16s` and two `ghost_summon` tests at `7.39s` and `7.20s`; this is measurable bounded work, not evidence of an infinite hang.

Receipt: `/board/inbox/VERKLE_DEDUP_DOGFOOD_RECEIPT_20260831.json`. This is a state-repair receipt, not evidence that every organ is live.

### Surfaces that are already worth reusing

| Need | Existing surface | What it should do in the next slice |
|---|---|---|
| Signal surface | `watch/room.jsonl`, `mag.chan` | Hold speech, claims, proposals, and receipts; never grant capability. |
| Ingress | `mag.board_tailer` | Observe by default; dispatch only with explicit `--dispatch`. |
| Classification/proposal | `mag.board_directive` | Preserve taint and turn explicit markers into bounded proposals. |
| Authority | `mag.switchboard_v2`, `mag.policy_engine` | Validate capability, status, budget, TTL, confirmation, and revocation. |
| Executor | `mag.seat_dispatch` | Be the canonical seat handoff; distinguish ranking from actual launch. |
| Lease/control loop | `mag.harness` | Own work, expire ownership, record terminal outcomes, and support requeue. |
| Effect boundary | `mag.effect_broker` | Mediate every effect; remove or fail closed on stubs. |
| Context transport | `mag.context_admission`, `mag.context_pack`, `mag.read_archive` | Preflight, compact, archive, and resume from bounded pointers. |
| Fusion/quarantine | `mag.session_bridge`, `mag.riddler_sanitize` | Sanitize foreign state and preserve taint through relay/archive/future prompt. |
| Routing/economics | `mag.ask_router`, `mag.fuel_feed` | Choose the least costly lane meeting the task floor and learn from receipts. |
| Continuity | `mag.manifest`, `mag.verkle_knot`, trajectory tape | Prove byte continuity and provenance; do not overclaim semantic truth. |
| Census | `mag.organ_map`, `mag.orphan_audit`, Elder/Basecamp artifacts | Compile status from current evidence and expose blind spots. |
| Shared handoff | `watch/inbox`, `mag.shared_surface` | One durable surface for all CLI/model families; indexed, hashed, and dereferenceable. |

## SOCRATIC ESCALATION

Each question below is intentionally uncomfortable. The answer is only as strong as its falsifier. The salon should not be asked to make these answers sound better; it should be asked to break them.

### Q1 — What is the canonical world record?

**Provisional answer:** There is no single canonical record yet. The closest materials are `watch/room.jsonl`, `watch/openclaw_traj.jsonl`, `watch/grok_feed.jsonl`, `memory/agent_sessions`, `memory/runs/orchestrator/tasks`, and organ receipts. They have different identifiers and retention semantics.

**Challenge:** If a dashboard event is in `room.jsonl` but absent from the local OpenClaw registry, which record wins?

**Required resolution:** Define a universal event envelope and a session locator registry. A record is canonical for replay only when it has `trajectory_id`, `run_id`, `span_id`, actor, timestamp, prior event, source path, source hash, and terminal linkage.

**Falsifier:** A fresh process can replay a dry run from one canonical event stream without reading the original chat transcript.

### Q2 — Is the organ map telling the truth?

**Provisional answer:** It tells the truth about declared organs and their tested evidence. It cannot yet prove discovery completeness, semantic usefulness, or universal liveness.

**Challenge:** What happens if a callable side-effect path is intentionally added outside the registry?

**Required resolution:** Add a blind-spot probe that reports “undeclared callable detected,” rather than converting the absence of a registry row into “no gap.”

**Falsifier:** The map detects an unregistered test organ and keeps its history while refusing to promote it.

### Q3 — Can language bypass authority?

**Provisional answer:** The doctrine says no, but the implementation still has closure gaps. `model_call` and `lane_spawn` are not real brokered effects in the inspected broker, and direct tools may exist outside the path.

**Challenge:** Can a board post, a three-seat consensus, or a fake receipt cause a model call, lane spawn, filesystem write, network request, or bridge mutation without a fresh grant?

**Required resolution:** Enumerate every effect entry point and run the same deny/allow matrix against each one.

**Falsifier:** Any ungranted side effect produces a successful effect receipt. That is a hard failure.

### Q4 — What happens before compaction pressure?

**Provisional answer:** It is not sufficiently universal. Context admission is real and emits receipts, but its wired evidence is concentrated in `agent_cli.py`; observed compaction churn proves the system has often reacted too late.

**Challenge:** What does an agent do when the next prompt will fit neither the configured reserve nor the provider window?

**Required resolution:** Preflight every model call; emit a bounded spore and archive spans; refuse or defer before dispatch; never depend on post-compaction recovery.

**Falsifier:** Artificial context pressure causes a fresh worker to resume from a spore and pointers without replaying the entire conversation.

### Q5 — What is safe to compact?

**Provisional answer:** Narrative repetition and already-hashed, dereferenceable summaries may be compacted. Operator law, authority grants/denials, taint, exact code changes, errors, receipts, and unresolved disputes must remain verbatim or losslessly addressable.

**Challenge:** Who proves that a “summary” did not erase a refusal, a capability restriction, or a competing hypothesis?

**Required resolution:** Mark compaction classes explicitly and require source hash/line span for every compacted item.

**Falsifier:** A compacted spore can be compared against its source and demonstrate that forbidden classes were not rewritten.

### Q6 — Are consensus seats independent?

**Provisional answer:** Independence tracking exists in proposals, but “three agents” is not yet a sufficient lineage definition.

**Challenge:** Do three models reading one cached answer count as three scouts?

**Required resolution:** Record provider, base model, prompt ancestry, cache hash, evidence paths, and copied-answer ancestry. Count lineages, not wrappers.

**Falsifier:** A false quorum built from one upstream answer is rejected; independent observations can still reach eligibility.

### Q7 — Does the bee/fungus analogy buy us anything?

**Provisional answer:** Yes, when translated into mechanisms: threshold recruitment, signal decay, stop signals, redundant routes, reinforcement, pruning, compatibility, and quarantine. No, when used as a claim that the software is a hive mind or that fungi possess semantic language.

**Challenge:** What observation would make the analogy harmful rather than useful?

**Required resolution:** Attach a measurable control rule and falsifier to every biological translation. If it does not change routing, safety, recovery, or cost, it is decoration and should be pruned.

**Falsifier:** A controlled comparison shows that bee/fungus-inspired routing is no better than a simpler baseline on cost, latency, correctness, and recovery; then the mechanism is retired or narrowed.

### Q8 — Does the flywheel learn?

**Provisional answer:** Receipts and ledgers exist, but receipt-to-routing change has not been demonstrated as a closed loop for the relevant task class.

**Challenge:** After a lane fails twice, does the next identical route actually change before another expensive attempt?

**Required resolution:** Add a controlled success/failure experiment and compare two consecutive route decisions with receipt pointers.

**Falsifier:** The route never changes despite a valid failure receipt; the learning trajectory remains unproven.

### Q8a — Does the map know what it costs?

**Provisional answer:** Not yet at the required granularity. Cost data exists in `cache_map`, `billing_feed`, `context_checkpoint`, water-window notes, subscription estimates, and Vast.ai research, but the ocean rows exposed that the capability map and every route/probe row did not uniformly carry the meter.

**Challenge:** If a lane is available but its reservoir is empty, peak-priced, unmeasured, or silently degraded, can the router explain why it fired or why it deferred?

**Required resolution:** Make cost/reservoir/window/exhaustion fields mandatory on trajectory events, proposals, persona outputs, and salon rows; compose `water_windows`, `offpeak`, `seat_availability`, `lane_cadence`, `seat_corpus`, `ask_router`, and the billing/cost stores behind one preflight decision.

**Falsifier:** A dry route with `UNKNOWN` cost is accepted as if it were `$0`, or a measured failure does not appear in the next route decision. Either result keeps TRJ-05 open at P0.

### Q9 — What is the phone-safe control surface?

**Provisional answer:** The phone may observe and issue closed-enum commands such as `approve proposal`, `deny proposal`, `pause lane`, `resume lane`, and `inspect receipt`. Free text is not an authority channel.

**Challenge:** Can a phone message accidentally grant an unlisted capability or become a root command?

**Required resolution:** Test the Control UI/Discord/mobile path with named proposal IDs and an allowlist of verbs.

**Falsifier:** A free-text message changes state without a proposal, capability list, and audit receipt.

### Q10 — What should not be built?

**Provisional answer:** No new hypervisor, atlas, blackboard, supervisor, universal gateway, directory, model tier, or “hive mind” organ is justified before the dry slice closes.

**Challenge:** Which existing surface already owns the proposed behavior?

**Required resolution:** Every new proposal must include a reuse map and a deletion/retirement plan for the duplicated concept.

**Falsifier:** A genuinely missing capability survives a composition attempt across the existing surfaces and has a bounded contract that cannot be represented by them.

## PERSONA CONTRACTS

Personas are disposable operating roles. They are not permanent agent identities, provider names, or claims about model intelligence. A model may perform a role only when the run records the role, lineage, budget, and evidence. The same model must not act as both proposer and independent verifier for the same claim.

### Shared persona contract

```yaml
persona_contract:
  persona_id: required
  role: required
  trigger: explicit event or assigned question
  inputs: bounded pointers with hashes and line spans
  allowed_surfaces: existing Mag modules/files only
  effects: none | proposal_only | named_broker_effects
  budget: token/time/cost ceiling
  ttl: expiry for the assignment and its outputs
  meter:
    cost_kind: required
    cost_estimate_usd: required_or_unknown
    reservoir_id: required_or_unknown
    window_state: required_or_unknown
    exhaustion_behavior: required
  output: fixed schema with claims, gaps, falsifier, action, receipt
  refusal: conditions that force UNPROVEN, DENIED, or QUARANTINED
  completion: durable receipt plus terminal state
  lineage: provider, model, prompt ancestry, cache hash, evidence hashes
```

### P01 — Archivist / Clerk (fungus: memory substrate)

- **Purpose:** Inventory files, sessions, runs, receipts, hashes, spans, and join keys.
- **Trigger:** A new run, orphan audit, compaction warning, or salon request.
- **Consumes:** `watch/inbox`, `watch/room.jsonl`, trajectory tape, run directories, organ map.
- **Allowed:** Read-only scans; write only a bounded report through the shared surface when granted.
- **Forbidden:** Interpreting absence as proof, editing production code, promoting a claim, or deleting records.
- **Budget:** Deterministic/local first; no model required for inventory or hashing.
- **Output:** `FACT` rows with source path, line span, hash, mtime, coverage class, unknowns.
- **Completion evidence:** A scan receipt and a list of unresolved joins.
- **Stop condition:** Duplicate IDs, invalid JSON, contradictory hashes, or an unbounded directory scope.

### P02 — Scout / Recruiter (bee: exploration and recruitment)

- **Purpose:** Find candidate routes, relevant evidence, and cheap lanes for a bounded task.
- **Trigger:** A signal reaches `board_tailer` or `ask_router`.
- **Consumes:** A frozen context pack and task contract; never the entire chat.
- **Allowed:** Rank and propose; may request a lease, never grant one.
- **Forbidden:** Direct effects, authority language, hidden prompt injection, or copying one answer as independent evidence.
- **Budget:** Free/cheap lanes; short output; TTL on every proposal.
- **Output:** Candidate route, expected value, cost/latency estimate, confidence, lineage, and falsifier.
- **Completion evidence:** Proposal receipt; a stop signal if stale, duplicate, unsafe, or over budget.
- **Stop condition:** No evidence pointer, no minimum task floor, or queue saturation.

### P03 — Builder / Worker (bee: bounded action)

- **Purpose:** Execute one named code or data change under a frozen contract.
- **Trigger:** An authorized proposal plus an unexpired lease.
- **Consumes:** Exact files/spans, acceptance commands, budget, and rollback identity.
- **Allowed:** Only named broker effects and only inside the allowed path.
- **Forbidden:** Scope expansion, new organs without approval, silent fallback, and claiming completion without a receipt.
- **Budget:** Defined by the proposal; deterministic tests before live models.
- **Output:** Patch/command result, tests, changed paths, source hashes, terminal status.
- **Completion evidence:** `COMPLETED` or `FAILED` plus `RECEIPT_COMMITTED`.
- **Stop condition:** Timeout, missing authority, dirty overlap, failed preflight, or acceptance failure.

### P04 — Adversary / Cross-Inhibitor (bee: stop signals)

- **Purpose:** Try to break authority, lineage, compaction, deployment, and false-completion claims.
- **Trigger:** A high-weight proposal, salon dispute, or release gate.
- **Consumes:** Claim IDs and evidence pointers, not full essays.
- **Allowed:** Read-only adversarial tests and negative receipts.
- **Forbidden:** Real destructive effects, credential access, or replacing a failed result with a nicer narrative.
- **Budget:** Free/local tests first; premium only for unresolved high-impact disputes.
- **Output:** Attack, observed result, severity, falsifier, downgrade/deny recommendation.
- **Completion evidence:** A reproducible failing or passing test and a durable challenge receipt.
- **Stop condition:** The test would cross T3 or affect external state without explicit authorization.

### P05 — Governor / Reference Monitor (fungus: compatibility gate; human-controlled)

- **Purpose:** Decide whether a proposal may acquire capabilities and whether an effect may execute.
- **Trigger:** Proposal reaches the switchboard.
- **Consumes:** Classification, taint, lineage, policy, capability request, TTL, budget, lease state.
- **Allowed:** Closed-enum grant, deny, defer, revoke, quarantine, and receipt decisions through `switchboard_v2`/`policy_engine`.
- **Forbidden:** Treating consensus as permission, granting more than requested, or allowing free-text authority.
- **Budget:** Deterministic. Human T3 confirmation required for configured high-risk or irreversible actions.
- **Output:** `AUTHORIZED`, `DENIED`, `DEFERRED`, or `QUARANTINED` with reason and receipt.
- **Completion evidence:** Policy decision plus state transition trail.
- **Stop condition:** Missing identity, stale TTL, capability mismatch, budget exhaustion, or non-successful authority receipt.

### P06 — Historian / Trajectory Compiler (fungus: transport and continuity)

- **Purpose:** Compile every meaningful transition into a replayable, bounded trajectory and spore.
- **Trigger:** Event emission, context pressure, terminal state, or session handoff.
- **Consumes:** Event envelope, archive spans, receipt paths, source hashes, session locator data.
- **Allowed:** Append-only evidence and derived indexes.
- **Forbidden:** Rewriting operator law, erasing disputes, or turning a hash into a semantic truth claim.
- **Budget:** Deterministic/local.
- **Output:** `trajectory_event`, bounded archive reference, spore, freshness, prior-event link.
- **Completion evidence:** Fresh-process dereference and replay pass.
- **Stop condition:** Missing predecessor, invalid span, hash mismatch, or unbounded payload.

### P07 — Salon Chair / Synthesizer (bee: collective deliberation; not authority)

- **Purpose:** Compare independent analyses, preserve disagreement, and name one next build.
- **Trigger:** A question set with cached prefix and explicit unresolved claims.
- **Consumes:** Exact shared prefix, pointer spans, normalized claim IDs, and lineage metadata.
- **Allowed:** Produce claim ledger and proposal only.
- **Forbidden:** Mutating code, promoting truth by majority, or asking every chair to reread the full corpus.
- **Budget:** R0/R4 free/local; one bounded call per independent chair; premium only for disputed high-weight questions.
- **Output:** `FACT`, `INFERENCE`, `PROPOSAL`, `UNPROVEN`, or `DISPUTE` rows with falsifier, reuse map, cost, and weight delta.
- **Completion evidence:** Compiled RIB and salon receipt; no state mutation.
- **Stop condition:** Missing evidence, shared lineage masquerading as quorum, or repeated restatement.

### P08 — Resource Steward / Metabolism Controller (fungus: flow; bee: allocation)

- **Purpose:** Explain and constrain cost, latency, subscriptions, local GPU, Vast.ai, and off-hours scheduling.
- **Trigger:** Route decision, queue pressure, budget event, or overnight scheduling window.
- **Consumes:** `run_id`/`trajectory_id`-linked usage, provider receipts, subscription ledger, GPU/Vast records.
- **Allowed:** Rank lanes, schedule/defer, stop waste, and emit proposals.
- **Forbidden:** Inventing prices, treating subscription access as free, or starting capacity without a budget receipt.
- **Budget:** Deterministic/local accounting first.
- **Output:** Cost attribution, route rationale, opportunity-cost note, and scheduling decision.
- **Completion evidence:** Per-run cost row with unknowns explicit.
- **Stop condition:** Missing provider/model/time/capacity identity or uncorrelated spend.

### P09 — Book / Primer Ractor (canon-bound design expert; proposed)

- **Purpose:** Let the Primer act as a design expert over our actual canon, using voice and story-with-stakes to review interfaces, pedagogy, and operator experience.
- **Status:** Proposed in `watch/salon_ocean_20260831/RACTOR_CONTRACT.md`; not yet proven live and not an authority organ.
- **Trigger:** A named design review with a bounded target such as the Ocean Map, Primer interface, or persona curriculum.
- **Consumes:** `SPORE_PRIMER_DESIGN.md` plus RIB/WARM_PACK pointers to real design documents; it dereferences rather than inventing structure.
- **Allowed:** Read-only canon review and proposal rows through `seat_dispatch`; it may speak in persona but must return ordinary claim IDs and evidence pointers.
- **Forbidden:** Invented organs, hidden authority, direct effects, unbounded transcript replay, or presenting book voice as factual evidence.
- **Budget:** First review approximately 200 tokens beyond the cached pack; use local/cheap lane first and record actual cost. No repeated rereading of the canon.
- **Output:** Design claim, canon pointer, user/stakeholder impact, falsifier, smallest reuse-only change, cost meter, and handoff.
- **Completion evidence:** A proposal receipt and a canonical pointer to the reviewed material; no code promotion by the ractor.
- **Stop condition:** Missing canon pointer, stale hash, role-play pressure to override policy, or no measurable design question.

### P10 — Ractor Epilogue / Warm Handoff (session lifecycle protocol; proposed)

- **Purpose:** Make a good session end deliberately so seats do not vanish without continuity.
- **Status:** The contract is specified; the closing ritual is still the missing proof.
- **Trigger:** An eligible seat reaches a terminal state and the operator/session contract opts in.
- **Consumes:** Final receipt, public persona form, and next-seat target.
- **Allowed:** Append exactly three bounded public lines to the trail: what was built, what was hard or enjoyable in the role, and what the next ractor should know.
- **Forbidden:** Inner-weather claims, private chain-of-thought, authority transfer, unbounded autobiography, or rewriting the terminal result.
- **Budget:** Approximately 50 tokens; recorded as a lifecycle cost.
- **Output:** `epilogue.v1` with `run_id`, `trajectory_id`, `seat`, `terminal_state`, `built`, `felt_publicly`, `next_ractor_knows`, cost meter, and receipt pointer.
- **Completion evidence:** Trail append survives a fresh process and is eligible for warm-pack extraction only after validation.
- **Stop condition:** No terminal state, no receipt, tainted session, or target handoff missing.

### Role-to-surface assignment

| Persona | Primary surface | Secondary evidence | Default effect level |
|---|---|---|---|
| Archivist | `orphan_audit`, `shared_surface`, `read_archive` | organ map, session indexes | none |
| Scout | `board_tailer`, `ask_router`, `fuel_feed` | cached RIB, route receipts | proposal only |
| Builder | `seat_dispatch`, `harness` | tests, patch receipts | named broker effects |
| Adversary | `dogfood_audit`, `harness`, policy tests | trajectory and failure receipts | none |
| Governor | `switchboard_v2`, `policy_engine` | T3 operator decision | authorization only |
| Historian | trajectory tape, `read_archive`, `verkle_knot` | session locator, manifests | append-only evidence |
| Salon | shared RIB/inbox, frontier salon | independent claim rows | proposal only |
| Steward | `fuel_feed`, `ask_router`, cost/Vast ledgers | provider/subscription receipts | proposal/stop |
| Book/Ractor | `seat_dispatch`, RIB/WARM_PACK, Primer docs | canon pointers and design receipts | proposal only |
| Epilogue | trail/core handoff | terminal receipt and next-seat pointer | append-only lifecycle note |

## TRAJECTORY REGISTRY AND WEIGHTS

Weights are engineering attention weights, not probabilities or intelligence scores. All weights are carried forward unchanged except TRJ-05: the operator-confirmed ocean correction and current flow-row evidence justify raising it from `.86` to `.92` because unmetered spend and unenforced reservoir windows are now observed failure pressure. This is a priority change, not a claim that the exact dollar totals are complete.

```text
W = .30 mission impact
  + .25 safety impact
  + .20 observed failure pressure
  + .15 implementation leverage
  + .10 time sensitivity
```

| ID | Trajectory | Weight | Priority | Current gap / proof target |
|---|---|---:|---|---|
| TRJ-01 | Epistemic truth | .89 | P1 | Discover undeclared organs, stale proofs, missing cost, and explicit unknowns. |
| TRJ-02 | Task execution | .97 | P0 | Replay board signal through seat dispatch to terminal receipt. |
| TRJ-03 | Context survival | .99 | P0 | Admit and shed before compaction; resume from bounded spore. |
| TRJ-04 | Authority | .98 | P0 | Prove every effect is brokered or refused. |
| TRJ-05 | Resource/cost | .92 | P0 | Make cost/reservoir/exhaustion a preflight coordinate; correlate provider, subscription, Vast.ai, local GPU, and run cost. |
| TRJ-06 | Agent roles | .81 | P1 | Implement response thresholds, saturation, starvation, and reclaim. |
| TRJ-07 | Consensus | .87 | P1 | Normalize lineage and reject copied-answer quorums. |
| TRJ-08 | Negative feedback | .93 | P0 | Make timeout, stale, unsafe, and duplicate signals decay route eligibility. |
| TRJ-09 | Fusion | .85 | P1 | Persist taint and compatibility through bridge/archive/prompt. |
| TRJ-10 | Topology | .80 | P1 | Reinforce useful edges; decay stale ones; preserve alternates. |
| TRJ-11 | Organ lifecycle | .93 | P0 | Add freshness, restart proof, and retirement semantics. |
| TRJ-12 | Human control | .85 | P1 | Closed-enum phone-safe verbs with explicit proposal IDs. |
| TRJ-13 | Terminal/recovery | .96 | P0 | Distinguish success, failure, timeout, death, stall, quarantine, and escalation. |
| TRJ-14 | Learning | .84 | P1 | Show receipts changing the next route decision. |
| TRJ-15 | Deployment truth | .94 | P0 | Link staged source hash to host import, exercise, receipt, and rollback identity. |

### TRJ-05 weight delta receipt

```text
old: TRJ-05=.86 (M=.90, S=.80, F=.85, L=.90, T=.80)
new: TRJ-05=.92 (M=.95, S=.85, F=.95, L=.95, T=.90)
reason: operator-confirmed cost omission plus ocean flow evidence showing two manual
water-ledger rows, unmeasured reservoir classes, unenforced off-peak cadence, and
unproven prefer_order consumption.
evidence: watch/SWARM_RESEARCH_LEDGER_20260831.md:170-173;
          watch/salon_ocean_20260831/row_flow.md:10-31;
          watch/salon_ocean_20260831/QUESTIONS.md:20-27
status: exact totals remain partially unknown; the correction itself is receipted.
```

### Why the weights do not make this a giant build

The vector says which transitions are risky, not that fifteen separate projects should launch. The first slice exercises TRJ-02, TRJ-03, TRJ-04, TRJ-11, TRJ-13, and TRJ-15 together. TRJ-08 is measured through deliberate failures. The remaining trajectories become downstream assertions on the same event stream.

## REBUILD / RETEST ORDER

### Stage 0 — Freeze and census (FREE/LOCAL)

Already available and repeatable:

```powershell
# SUPERSEDED (FW-11 2026-09-28): one-shot orphan_audit batch, 2026-08-31. Do not re-run from prose. Receipt: watch/inbox/fifty_wide_20260917/FW11_fence_owners.md
python -m mag.orphan_audit
python -m mag.openclaw_patches preflight
python -m mag.openclaw_patches status
python -m mag.organ_map status
python -m mag.dogfood_audit status
python -m mag.shared_surface validate
```

Pass condition: every result is timestamped; stale prose is not treated as current; missing, unlanded, not-started, stalled, and protected-external records remain distinct.

### Stage 1 — Canonical dry vertical slice (NEXT ACTION)

Run one synthetic, non-destructive board event through the existing surfaces:

```text
room event
  -> board_tailer poll --dispatch
  -> board_directive classify/propose
  -> lineage and quorum eligibility
  -> switchboard_v2 grant or deny
  -> harness.run_once(dry=True)
  -> context_admission.assess
  -> effect_broker dry/refusal
  -> terminal receipt
  -> read_archive dereference
  -> organ_map and trajectory record
```

The first implementation task is the **universal trajectory event envelope**, not a new agent. It should be emitted by the existing surfaces with these minimum fields:

```json
{
  "schema": "trajectory_event.v1",
  "trajectory_id": "TRJ-02",
  "run_id": "run-...",
  "span_id": "span-...",
  "event_id": "evt-...",
  "event_type": "board_observed",
  "ts": "...Z",
  "actor": "board_tailer",
  "prior_event_id": null,
  "source_path": "watch/room.jsonl",
  "source_line": 0,
  "source_sha256": "...",
  "authority_state": "UNTRUSTED",
  "cost_kind": "unknown",
  "cost_estimate_usd": null,
  "cost_confidence": "unknown",
  "reservoir_id": "unknown",
  "window_state": "UNKNOWN",
  "consumed_units": "unknown",
  "exhaustion_behavior": "operator_gate",
  "silent_degradation": "unknown",
  "evidence": [],
  "terminal": false
}
```

Required event sequence:

```text
board_observed
-> proposal_created
-> content_classified
-> lineage_recorded
-> quorum_evaluated
-> resource_preflight
-> grant_decided
-> lease_acquired
-> context_admitted
-> effect_attempted
-> receipt_committed
-> archive_span_bound
-> spore_emitted
-> route_updated
```

No event may claim to have happened unless it leaves a durable record. A denied effect is a valid terminal branch; it is not a failed system.

### Stage 2 — Context-pressure retest (P0)

Use a deterministic synthetic context budget. Confirm that:

1. `context_admission.assess` runs before dispatch.
2. Green admits; amber schedules compaction/spore work; red/black refuses or defers.
3. The original material is addressable by archive path and line span.
4. The spore contains no free-text authority and no missing operator law.
5. A fresh process can resume without loading the full transcript.
6. The trajectory and persona rows carry a cost meter even when the value is `UNKNOWN`; no missing meter is encoded as zero.

The OpenClaw reserve mismatch is a configuration defect candidate, not a claim to change blindly. First capture the preflight receipt, then choose a tested reserve policy appropriate to the actual model windows and tool schema.

### Stage 3 — Authority closure (P0)

Build an effect-entry inventory and test it with the same matrix:

| Effect | Must produce | Current concern |
|---|---|---|
| board write | broker receipt | Existing path is exercised. |
| Verkle link | broker receipt | Verify errors are terminal and dereferenceable. |
| tool invoke | broker receipt | Validate cwd/path allowlists and timeout. |
| filesystem write | broker receipt | Validate containment and append/write semantics. |
| network access | broker receipt | Validate URL policy, byte limit, and refusal. |
| model call | broker receipt or explicit refusal | Inspected implementation still returns a model stub. |
| lane spawn | broker receipt or explicit refusal | Inspected implementation still returns a spawn stub. |
| bridge mutation | broker receipt | Wire `session_bridge` mutation through the same grant. |

Pass condition: every exposed entry point either ends in a broker receipt or fails closed. A successful stub is not a pass.

MCP-specific check: `python -m mag.mcp_server --quantize PROFILE` may reduce context and exposure, but it never grants an effect. A profile call outside its cartridge must be refused before the underlying tool registry is reached.

### Stage 4 — Terminal/recovery and negative feedback (P0/P1)

Force, one at a time, these conditions:

- provider timeout;
- missing provider auth;
- malformed output;
- stale lease;
- duplicate proposal;
- failed effect;
- false completion claim;
- context budget overflow;
- disconnected external seat.

Each must end in a bounded state, a durable receipt, and a next action: retry with changed conditions, stop/decay, quarantine, escalate, or archive. No run may remain “spinning” without a heartbeat policy and escalation deadline.

### Stage 5 — Resource gate, learning, and economics (TRJ-05 P0 guard / P1 attribution)

Before any live or expensive work, compose the existing flow organs into one shared snapshot. The proposed `/board/water_state.json` is a **state artifact**, not a new organ: it should be emitted by an existing cadence/flow step from `water_windows`, `offpeak`, `seat_availability`, and `lane_cadence`. Every route proposal reads it before lease or effect.

The minimum preflight decision is:

```text
reservoir measured or explicitly UNKNOWN
AND window not PEAK unless operator override is present
AND lane cooldown is zero
AND route cost is within the proposal budget
AND exhaustion behavior is defined
```

The three cheapest reuse-only wires are:

1. `water_windows json` + `offpeak.defer_if_peak()` + `seat_availability.status()` + `lane_cadence.status()` -> `/board/water_state.json`.
2. `seat_availability.ping()` -> the currently static/POLLED reservoir rows, so availability is measured rather than asserted.
3. `seat_corpus.prefer_order` -> `ask_router`/ladder, so cheap-first policy is load-bearing rather than prose.

Once the trace exists, connect the existing `ask_router`/`fuel_feed` outcome ledger to it. A per-run cost row should include:

```text
run_id, trajectory_id, provider, base_model, lane, tokens,
runtime, local_gpu_seconds, Vast.ai_instance_or_unknown,
subscription_bucket, marginal_cost, opportunity_cost,
scheduling_decision, receipt_ids, unknowns
```

The first learning test is intentionally small: one controlled success and one controlled failure for the same task class, followed by two route decisions. The second decision must cite the receipt that changed its eligibility. If it does not, TRJ-14 remains unproven.

The cost acceptance test is equally small: run one dry route and require a row with a named reservoir/window, cost kind, estimate or explicit `UNKNOWN`, exhaustion behavior, and no false `$0` assertion. Then run one measured local or provider-backed job only if the operator authorizes it and compare the before/after ledger.

### Stage 6 — Guarded expansion (P2)

Only after Stages 1–5 pass:

- implement response thresholds and saturation-aware recruitment;
- add decaying positive/negative route signals;
- run independent salons with fixed prefixes and lineage receipts;
- reinforce/prune semantic graph edges separately from structural hash links;
- compare the bee/fungus hybrid with a simpler baseline;
- refresh atlas/basecamp views from compiled evidence;
- schedule premium/off-hours work using measured cost and queue pressure.

The Book/Primer expansion belongs here only after the core trace: mint `SPORE_PRIMER_DESIGN.md`, run one pointer-bound Ocean Map review through the proposed Book Seat, and append the optional three-line ractor epilogue only after the seat has a terminal receipt. This is a reuse of `seat_dispatch`, RIBs, and trail files, not a new control plane.

Expansion is a hypothesis test. It is not a reward for having more personas.

## SALON PROTOCOL

The salon is an adversarial measurement instrument, not a parliament.

### Shared cache

Every chair receives the same byte-stable prefix and only dereferences the spans required for its question. Use the existing salon RIB and the bee/fungus handoff as pointers. Do not inline full chat histories.

### Chairs

| Chair | Persona | Questions |
|---|---|---|
| A | Architecture + context | Q1, Q4, Q5 |
| B | Authority + adversary | Q3, Q6, Q9 |
| C | Fleet economics | Q8 plus cost evidence |
| D | Evidence/zeitgeist | Q2, Q7, Q10; primary sources only |
| E | Bee/fungus mechanisms | Q6, Q7, Q8 |
| F | Implementation elder | Q1–Q10; choose smallest build |
| G | Operator/Basecamp | Q2, Q4, Q9, Q10 |
| H | Chair/compiler | Compile only after A–G; cannot introduce unsupported claims |

### Rounds

```text
R0  deterministic inventory, hashes, spans, and deduplication
R1  independent chairs answer compact claim rows
R2  adversarial cross-examination of only disputed/high-weight claims
R3  chair compiles one claim ledger and one next action
R4  local verifier runs exact acceptance commands
R5  publish one canonical RIB; route only the named action to Basecamp
```

### Chair output schema

```text
CLAIM <id>
class: FACT | INFERENCE | PROPOSAL | UNPROVEN | DISPUTE
statement: <one falsifiable sentence>
evidence: <path:line-span OR primary DOI/URL>
project_map: <organ/surface/TRJ-id>
gap: <what is missing or assumed>
confidence: HIGH | MEDIUM | LOW | UNKNOWN
falsifier: <test or observation>
action: <one smallest named action>
reuse: <existing organ/tool/file>
cost: FREE | LOCAL | PAID:<estimate> | UNKNOWN
weight_delta: <TRJ-id; only with receipt/experiment>
receipt: <hashes, commands, and commands not run>
```

### Salon acceptance

The salon passes only when:

1. At least three independent lineages contribute, or the deficit is explicit.
2. Every promoted claim has an evidence pointer and class.
3. Every open gap has a next action and falsifier.
4. All 15 trajectory weights are returned.
5. At least one attractive claim is rejected or downgraded.
6. No chair mutates production state.
7. The output reuses existing machinery and names an exact local acceptance command.
8. A fresh worker can resume from the handoff without chat replay.

## RESEARCH TRANSLATION, WITH CONTROLS

### Bee dynamics -> mechanisms

- Independent scouts become independent evidence lineages.
- Waggle strength becomes quality-weighted, TTL-bound proposal energy.
- Signal expiration becomes route-score decay.
- Stop signals become denials, stale/unsafe receipts, and backpressure.
- Quorum becomes proposal eligibility, not authority.
- Response thresholds become role recruitment and specialization.
- Cross-inhibition becomes duplicate suppression and explicit negative feedback.

The control question is not “does this look like a hive?” It is “does this rule reduce dead cascades, improve task allocation, or preserve dissent under measured conditions?”

### Fungus dynamics -> mechanisms

- Hyphal edges become typed provenance-bearing pointers.
- Transport corridors become archive spans and bounded context packs.
- Reinforcement becomes outcome-linked route updates.
- Pruning becomes removal of routing eligibility, never deletion of history.
- Loops and alternates become provider/lane redundancy.
- Fusion becomes sanitized session bridging.
- Non-self rejection becomes taint persistence and quarantine.
- Fruiting bodies become canonical accepted artifacts with release gates.
- Spores become bounded handoff capsules.

The control question is not “is this a mycelial intelligence?” It is “can a fresh worker move enough state through a bounded pointer without importing authority or losing provenance?”

### Anti-overclaim control

The existing research correctly warns against turning biological metaphors into facts. Fungal electrical signaling and forest-network narratives remain areas where interpretation and generalization need care. Every biological translation in Mag must therefore carry a mechanism, a measurable outcome, and a falsifier. If it does not, it stays an analogy in the research layer and cannot become an architecture claim.

## DO NOT BUILD YET

- another hypervisor or universal supervisor;
- a second blackboard, atlas, ledger, directory, or session bus;
- new personas that do not have a distinct contract and acceptance test;
- a premium salon that rereads cached answers;
- a “smart” semantic layer before source spans, hashes, and freshness work;
- a semantic truth claim from a Verkle/hash proof;
- an automatic reaper for protected external records;
- a live model-call or lane-spawn effect that is only a stub;
- an overnight scheduler before actual cost and queue receipts are correlated;
- a release claim based on a stale `WARM_PACK`, `CAMPAIGN_MAP`, or pasted status paragraph.

## CURRENT DISPUTES / UNPROVEN CLAIMS

| Claim | Status | What would settle it |
|---|---|---|
| The current dashboard session is fully joined to local OpenClaw history | UNPROVEN | Session locator maps its ID to source file/span and replay receipt. |
| The image board can dispatch all the way to a seat | PARTIAL | One dry `room.jsonl -> board_tailer --dispatch -> seat_dispatch` trace. |
| The switchboard governs every side effect | UNPROVEN | Effect-entry inventory and deny/allow matrix, including model/lane/bridge. |
| Context admission prevents overflow for all surfaces | UNPROVEN | Preflight hooks at every model-call boundary plus pressure test. |
| `switchboard_v2`/`policy_engine` are fully live | VERIFIED-WITH-GAP | Successful receipt state and restart/replay proof. |
| Receipts alter future routing | UNPROVEN | Same-task before/after route decisions citing the receipt. |
| The biological architecture beats a simpler baseline | UNPROVEN | Controlled cost/latency/correctness/recovery comparison. |
| Every staged/reported job has a real run | FALSE for 3 current jobs | Explicit `NOT_STARTED` receipts remain until the jobs actually run. |

## HANDOFF

**Start at:** `TRJ-03 + TRJ-04`, with `TRJ-02` as the safe vertical slice; measurement support from `TRJ-11`, `TRJ-13`, and `TRJ-15`.

**Read first:**

1. This RIB.
2. `watch/inbox/AGENT_HIVE_BEE_FUNGUS_HANDOFF_2026-08-31.md`.
3. `watch/inbox/SALON_SUPERINTELLIGENCE_STACK_RIB_20260831.md`.
4. `watch/stack_recommendation_20260831.md`.
5. Current command output from `mag.orphan_audit`, `mag.organ_map`, and `mag.shared_surface validate`.

**Completed:**

- patch application and receipts are current at 21 applied / 0 pending / 0 rejected;
- shared-surface indexing is green;
- deterministic dogfood reports 21/21;
- the organ census exists;
- board tailer, authority v2, effect broker, context admission, archive, session bridge, router, harness, and swarm cycle are present in territory;
- the existing MCP server now derives real callable signatures, emits stable persona cartridges (`--quantize all`), and enforces profile-scoped exposure; targeted MCP dogfood is 22/22;
- the conversation’s repeated intent has been reduced to laws, trajectories, personas, and tests.

**Open:**

- universal trajectory event envelope and session locator;
- board-to-seat-to-receipt dry replay;
- universal context preflight/spore threshold;
- complete broker coverage for model call, lane spawn, bridge, and every direct tool;
- decide whether any concrete model body needs to consume the optional MCP cartridge; do not treat client count as a health metric;
- terminal-state/escalation semantics for stalled and failed work;
- receipt-to-routing learning;
- unified cost/subscription/Vast.ai/off-hours attribution;
- stale Octant pointers and the three not-started jobs;
- current OpenClaw reserve/timeout policy alignment.

**Blocked:**

- live/provider work remains constrained by provider auth, quota, and host/runtime state;
- protected external desktop records are not safe to auto-reap from this checkout;
- no paid model call is necessary for the first dry slice.

**Next agent instruction:**

Implement the smallest universal `trajectory_event.v1` adapter around one synthetic, non-destructive board event. Run it through `board_tailer poll --dispatch`, `board_directive`, `switchboard_v2`, `harness run_once --dry`, context admission, and the broker refusal/receipt path. Persist one replayable trace and one bounded spore. Do not add an organ, launch a live model, or mark the architecture complete until the trace satisfies all eight required assertions from this handoff.

## BIBLIOGRAPHY POINTER

The research bibliography and primary-source links are retained in `watch/inbox/AGENT_HIVE_BEE_FUNGUS_HANDOFF_2026-08-31.md`. The architectural and trajectory references are retained in:

- `docs/ref/TRAJECTORY_ARCHITECTURE.md`
- `docs/ref/TRAJECTORY_RIB_COMPILER_SPEC.md`
- `docs/ref/MYCELIAL_SCIENCE_MAP.md`
- `docs/ref/HARNESS_SPEC.md`
- `docs/ref/COMMON_LANGUAGE_SPEC.md`
- `watch/inbox/SALON_SUPERINTELLIGENCE_STACK_RIB_20260831.md`

Use the handoff bibliography as the primary research cache. Browse again only for a genuinely unresolved claim or a changed external specification, and record the new source and weight delta.
