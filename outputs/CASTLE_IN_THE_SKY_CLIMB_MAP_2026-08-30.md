# Castle in the Sky: Basecamp Climb Map

Date: 2026-08-30

Purpose: map the system we actually have, then climb toward the flywheel without promoting plans, names, or metaphors into organs.

This map uses the available machinery as instruments:

    organ_map       catalog and status
    dirac_loop      topology and open-bridge scan
    self_audit      probe freshness and health
    guard_registry  process-safety invariants
    manifest        narrow anchor verification
    verkle_knot     integrity verification
    switchboard     seat-mesh self-test
    swarm_worker    queue and executor status
    openclaw_patches pending-change inventory

The map was refreshed from the repository at 2026-08-30T22:10Z. No production code was changed.

## The doctrine

The castle in the sky is allowed to exist as a hypothesis. It is not allowed to masquerade as terrain.

An organ advances through these gates:

    named
      -> source exists
      -> import succeeds
      -> caller is identified
      -> invocation occurs
      -> durable receipt exists
      -> contract passes
      -> negative test passes
      -> edge is live

Short law:

    A filename is not an organ.
    An import is not an invocation.
    An invocation is not a receipt.
    A receipt is not a contract.
    A contract is not authority.
    A Verkle proof is integrity, not truth.

The next bridge is climbed only when the current bridge leaves evidence.

## Castle legend

| Symbol | Meaning |
|---|---|
| Stone | Source exists and imports |
| Scaffold | Declared wiring or state path exists |
| Footing | A recent invocation receipt exists |
| Walkable bridge | Contract and transition evidence pass |
| Red flag | Known failure, stale evidence, or bypass |
| Cloud tower | Named concept with no runtime implementation |

## Current skyline

The refreshed organ map reports:

    DECLARED 13
    INSTRUMENTED 12
    WIRED 13
    STATEFUL 11
    VERIFIED 12
    LIVE 2
    GHOST 5

This is a catalog result, not proof that 13 bridges are live. The map currently overstates wiring because wired status is primarily path existence.

### Lower castle: real rooms

| Room | Current evidence | Honest status |
|---|---|---|
| Water computer | Non-cheated proof passes | Verified probe surface |
| Chain manifest | Manifest hash matches anchored leaf | Narrow anchor verified |
| Context admission | Recent receipts; deterministic green/amber/red/black assessment | Live, bounded |
| Context pack | Importable pack builder with bounded modes | Verified component |
| Context checkpoint | Checkpoint implementation and checkpoint directory | Present; current-turn edge unproven |
| Swarm surface | Route implementation and state path | Present; pressure edge unproven |
| Swarm worker | Queue, claim, process, result paths | Operational, semantic completion weak |
| Dirac loop | Finds topology loops and open gaps | Observer, not repairer |
| OpenClaw policy | Config and hook parse/exist | Controlled runtime evidence still needed |
| Seat mesh | switchboard self-test passes | Real mesh/router |
| Blackboard | Direct JSON store with pinned kinds | Real store, not authority boundary |
| Self-audit | Seven probes and a passing last report | Real, stale |

### Cloud castle: named but not landed

| Cloud tower | Evidence |
|---|---|
| Atlas/lattice map | No runtime implementation found |
| Basecamp controller | Planning doctrine, no runtime organ |
| Elder audit seat | No runtime implementation found |
| Fireball cycle | No runtime implementation found |
| Effect broker | No runtime implementation found |
| RolePacket/ractor/WorldDelta | Design language/search hits, no implementation |
| ContributionReceipt/PostconditionEvidence | No generic runtime contract found |

## Basecamp instruments: latest readings

### Organ map

Current statuses:

    LIVE: context_admission, self_audit
    STATEFUL: verkle_knot
    VERIFIED: water_computer, manifest, context_pack, context_checkpoint,
              swarm_surface, swarm_worker, dirac_loop, openclaw,
              switchboard, blackboard
    GHOST: atlas, basecamp, elder, fireball_cycle, effect_broker

The status for context_checkpoint is especially important: its implementation is real, but the registry's declared agent_cli wiring is not invocation proof.

### Dirac topology

Latest operational scan:

    betti1=8
    n_loops=6
    closed_solved=0
    open_gaps=6

Open bridges include:

    context_pack -> swarm_surface       pressure_offload
    context_checkpoint -> context_pack restore
    verkle_knot -> manifest             commit
    context_admission -> openclaw       runtime_policy
    openclaw -> context_admission       runtime_receipt
    water_computer -> manifest           proof

The loop detector is doing its job: it reports that these are declared invariants without transition receipts.

### Verkle integrity

Direct prove_latest reading:

    ok=false
    verified=false
    error=last row root mismatch
    committed=f085695544ad676c...
    recomputed=d19857d7209bd900...
    n_leaves=0

The chain has 4914 physical lines, 4912 valid JSON lines, and 2 malformed lines. The parseable tail is also out of sequence. This tower is red and cannot currently serve as the castle's notary.

### Seat mesh

switchboard self-test:

    ok=true
    tier_gate=true
    n_seats=33
    mesh_peers=81
    dry_drop=true

This proves mesh behavior and tier gating. It does not prove classify/propose/grant/write authority mediation.

### Swarm elevator

Current queue:

    queued 143
    running 1
    done 58
    failed 463
    cancelled 572

The executor exists, but the elevator is congested and its completion bell means process success plus nonempty output. It does not yet mean goal satisfaction.

### Health bell

self_audit:

    last report passed=7 failed=0
    last report age approximately 5.96 hours

guard_registry:

    ok=false
    failing invariant=spawn_sites_no_window
    action=alert_backoff

openclaw_patches:

    pending ask_router.json, board_directive.json, swarm_cycle.json, x_auth_once.json
    applied_n=0

The castle has a health bell, but it is not ringing on a sufficiently current cadence.

## The actual bridge map

### Bridge A: transcript to admission

Status: partial and real.

Existing footholds:

- agent_cli estimates context pressure.
- admission bands and thresholds exist.
- repacking exists.
- context receipts exist.

Missing footing:

- a durable transition proving that pressure caused a checkpoint.
- a durable transition proving that the compact residual was handed to swarm_surface.
- a result receipt proving reintegration.

### Bridge B: admission to cheap-agent offload

Status: declared, not walked.

The intended bridge is:

    red/black pressure
      -> checkpoint
      -> compact PressureEvent
      -> swarm_surface
      -> swarm_worker
      -> result
      -> postcondition

Current evidence proves the components separately, not this sequence. The OpenClaw hook records compaction after it happens; it is not yet a pre-admission controller.

### Bridge C: blackboard to authority

Status: bypassed.

The blackboard writer and public tool dispatcher can write directly. The current switchboard is a mesh/router, not the reference monitor described in earlier plans.

The first safe authority bridge is intentionally narrow:

    classify
      -> proposal
      -> grant
      -> board_write
      -> effect receipt

No free-text post, roast, consensus score, or pinned kind may grant an effect.

### Bridge D: worker completion to truth

Status: absent.

Required foothold:

- declared goal predicate
- evidence requirements
- action or contribution receipt
- independently evaluated postcondition
- explicit failure when evidence is absent

### Bridge E: evidence to map

Status: partial.

manifest verification works for its own anchored leaf. Verkle global verification fails. organ_map records declared topology, but it does not yet derive wiring from call/invocation evidence.

## The climb route

### Camp 0: Freeze the terrain

Use the existing read-only probes to record:

- source-tree and dirty-worktree snapshot
- configuration hashes
- queue inventory
- raw blackboard and Verkle evidence counts
- current organ-map and Dirac outputs

Stop condition: a dated baseline exists and no cleanup or patch application is mixed into the measurement.

### Camp 1: Repair the notary

Quarantine the raw Verkle chain, tip, and knot files. Preserve malformed lines byte-for-byte. Produce a mismatch report. Rebuild only under a new chain identity and explicit recovery policy.

Stop condition: prove_latest fails closed on malformed/out-of-order evidence, and a new clean test chain verifies.

### Camp 2: Correct the signposts

Separate seat_mesh from reference_monitor in the organ registry and documentation. Mark old authority edges as unknown until receipts exist.

Stop condition: no status display can call the mesh a reference monitor.

### Camp 3: Walk one controlled bridge

Implement only mediated board_write. Require typed proposal, effect, capability, budget, TTL, grant, and receipt.

Stop condition: a direct model/tool blackboard write cannot bypass the boundary, while an explicitly granted dry write can complete with a receipt.

### Camp 4: Build the pressure elevator

Introduce a compact PressureEvent. On red/black:

    checkpoint first
    retain a residual pointer
    enqueue compact work
    record result
    record reintegration or failure

Stop condition: one synthetic pressure event traverses the sequence without sending the whole transcript to the cheap agent.

### Camp 5: Add the completion bell

Require postconditions and evidence for worker completion. Keep execution status separate from semantic verdict.

Stop condition: a deliberately empty or wrong result is marked failed even when the subprocess exits zero.

### Camp 6: Recompile the map

Change organ status from path-derived to evidence-derived:

    source -> import -> call -> receipt -> contract -> recent live edge

Stop condition: the map can show a real module with an unproven edge without calling it wired.

### Camp 7: Controlled OpenClaw return

Snapshot host configuration. Run a bounded frontend/gateway test. Measure provider limits and compaction behavior. Adjust reserve floors from evidence, not from a universal magic number.

Stop condition: a real compaction/pressure event produces a complete receipt chain.

### Camp 8: Bounded swarm drain

Classify existing failures before restarting any drainer. Drain small batches with caps, backoff, and the new postcondition contract.

Stop condition: failure causes trend down and every completed task has evidence.

## Stop rules

Stop the climb and return to basecamp when:

- an integrity source is unverifiable;
- a direct authority bypass is found;
- a worker result lacks a postcondition;
- a map edge has no receipt;
- queue growth exceeds the bounded drain budget;
- a stale health report is being used as current evidence;
- an implementation is being proposed solely because its name appears in a document or conversation.

## First climb action

The first implementation action is not “launch more agents.”

It is:

    quarantine Verkle evidence
    label the current switchboard as seat_mesh
    preserve the baseline

Only after those three footholds exist should the system build the first mediated board-write bridge. That gives the flywheel a floor before giving it more speed.

## Relation to the prior research

The Boxer material remains outside the architecture map and serves only as an uncertainty/provenance test. Gray Swan remains an adversarial testing lens. Blackboard remains a shared-state design pattern, not permission. Verkle remains an integrity notary, not truth or authority. The “castle” metaphor is useful for navigation only when each bridge has a receipt.
