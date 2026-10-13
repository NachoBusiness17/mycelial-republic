# Research-Informed Organ Audit

Date: 2026-08-30

Scope: local_sovereign_agent / OpenClaw integration, organ map, context admission and offload, blackboard, switchboard, swarm worker, Verkle evidence chain, provenance, and the claimed flywheel.

This is an evidence audit. It does not treat names, documentation, generated maps, or prior agent claims as proof that an organ is live.

## Executive verdict

The system has real working pieces, but the claimed flywheel is not currently a closed loop. It is a set of live or partially live islands with several declared bridges that have not been proven by invocation receipts.

The most important map correction is semantic:

- mag/switchboard.py is a seat mesh, peer registry, orphan reaper, and tier-bounded steering router.
- It is not currently the reference monitor or effect broker described in the switchboard proposal.
- mag/swarm_tools.py and the public tool dispatcher can write to the blackboard without passing through an authority boundary.
- The effect broker is not implemented.
- The global Verkle chain is not currently verifiable.
- Local context repacking exists, but automatic pressure-to-offload is not proven end to end.
- The organ map overstates wiring because it checks whether declared paths exist, not whether those paths invoke the claimed organ.

The system therefore has a useful basecamp, but not yet a trustworthy mountain map.

## What the Boxer detour means

The accidental Boxer Rebellion material is not evidence for an organ, a harvesting operation, or an architecture claim. It is retained only as a provenance and uncertainty-handling test:

1. Separate historical facts from analogy.
2. Separate analogy from executable system claims.
3. Require primary evidence before escalating a claim.
4. Do not let an emotionally salient or bizarre narrative acquire authority merely because it appears in a shared board or model conversation.

The audit found no basis for treating the Boxer material as an OpenClaw subsystem. It is out of the architecture map.

## Research rules applied

### A blackboard is a communication surface, not an authority boundary

Nii's blackboard architecture supports a shared problem-solving workspace. It does not, by itself, decide who may cause an external effect. The current blackboard is real and useful, but a pinned decision is still a posted record, not an authorization.

### A reference monitor must mediate every protected operation

The NIST reference-monitor model requires complete mediation, tamper resistance, and a small auditable mechanism. Direct blackboard writes and direct tool dispatch violate complete mediation for the operations they expose.

### A Verkle proof is integrity evidence, not truth or permission

A valid Verkle commitment can show that bytes fit a commitment. It cannot prove that a claim is true, that a model's goal was satisfied, or that an action was authorized. The current chain also has integrity failures, so even its narrower notary role is presently unavailable.

### Reward and specification gaming require postconditions

An exit code, nonempty output, or a model saying “done” is not evidence that the intended goal was achieved. Worker completion must carry a typed postcondition and independently checkable evidence.

### Human agency is not represented by metaphors alone

The Diamond Age / ractor / role language is useful as a design lens for human agency and social roles. The runtime does not currently contain a RolePacket, ractor, WorldDelta, ContributionReceipt, or effect-broker implementation. Those names must remain planned concepts until code and receipts exist.

### Gray Swan is an adversarial lens, not a conspiracy premise

The Gray Swan material is useful for red-teaming agent boundaries, prompt injection, and unsafe authority transfer. It is not evidence of a hidden chain of control in this repository.

## Current organ map

The fresh organ-map summary reports:

    DECLARED 13
    INSTRUMENTED 12
    WIRED 13
    STATEFUL 11
    VERIFIED 12
    LIVE 2
    GHOST 5

Those numbers are useful as a catalog, but the labels are too optimistic because wired currently means that a declared path exists.

| Organ or surface | Evidence-backed status | What can be safely claimed |
|---|---|---|
| context_admission | Live, but narrow | Deterministic preflight/repack assessment exists and writes receipts |
| context_pack | Real and tested | Produces bounded packs and preserves selected scope/heat |
| context_checkpoint | Real, used outside agent_cli | Checkpoint code exists; current-turn automatic use is not proven |
| swarm_surface | Real, integration incomplete | Surface and route concepts exist |
| swarm_worker | Real, operationally stressed | Queue, claim, execute, and result paths exist; semantic success is weak |
| dirac_loop | Real observer | Finds open graph gaps and loops; does not make edges live |
| openclaw | Config and hook present | Config parses; current live frontend/gateway behavior was not tested |
| switchboard | Real seat mesh | Mesh, peer, orphan, tier, steer, and route functions exist |
| blackboard | Real direct store | JSONL-style shared notes exist; direct writes bypass authority mediation |
| water_computer | Real test/probe surface | Negative-test/proof concepts exist |
| manifest | Real narrow anchor | Manifest anchor verifies; this does not verify the global Verkle chain |
| verkle_knot | Integrity degraded | Latest proof fails due malformed/out-of-order/root-mismatch evidence |
| self_audit | Real but stale | Last report passed, but it is about 5.9 hours stale |
| atlas | Ghost | No runtime implementation found |
| basecamp | Ghost as runtime organ | A planning metaphor and audit method, not a verified module |
| elder | Ghost | No runtime implementation found |
| fireball_cycle | Ghost | No runtime implementation found |
| effect_broker | Ghost | No runtime implementation found |

## Critical findings

### F1 — CRITICAL: the Verkle evidence chain is not currently verifiable

Evidence:

- Physical chain lines: 4914.
- Valid JSON lines: 4912.
- Malformed lines: 2.
- Recomputed root begins d19857d7209bd900.
- Last valid row commits a different root beginning f085695544ad676c.
- The latest valid tail is out of sequence and contains stale-looking rewrites.
- prove_latest returns ok=false with last-row root mismatch and n_leaves=0.
- test_ghost_spooky.py::test_probe_carries_real_verkle_proof fails because the proof has no knot pointer.

The loader silently skips JSON-decode failures. That makes the displayed parseable chain look healthier than the physical evidence actually is.

Safe first repair:

1. Stop treating the chain as authoritative.
2. Copy the raw chain, tip, and related knot files into a dated quarantine directory.
3. Preserve malformed lines byte-for-byte.
4. Produce a forensic report of sequence, parent, leaf, and root mismatches.
5. Rebuild only under an explicit recovery policy, with a new chain identity.
6. Add tests that fail closed on malformed or out-of-order evidence instead of silently skipping it.

Do not delete malformed rows or rewrite the chain in place before the quarantine copy exists.

### F2 — CRITICAL: authority semantics are aliased and bypassable

The live switchboard source identifies itself as:

    Switchboard — unified seat mesh, orphan reap, tier-bounded steer drops

It contains mesh, peers, orphan reaping, steer drops, route intent, status, and self-test. It does not contain the proposal's classify, propose, grant, write, reconcile, execute, capability issuance, or action-receipt implementation.

The blackboard path is direct:

- mag/swarm_tools.py blackboard_post creates the directory, scans sequence numbers, writes the file, and performs best-effort eviction.
- tools/__init__.py dispatches blackboard_post directly through TOOL_MAP.
- mag/agent_cli.py exposes blackboard_post as a model tool.
- There is no general reference-monitor check around dispatch.

Current inventory: 61 blackboard JSON files, 36 pinned decisions, 22 findings, 2 open questions, and 1 claim. “Pinned” means durable/canonical pressure; it does not mean authorized.

Meaning:

    a roast can be a proposal
    a proposal is not permission
    a pinned decision is not proof
    consensus is not authorization

The first authority implementation should be deliberately small: classify -> propose -> grant -> board_write, with typed receipts and no free-text permission payload.

### F3 — HIGH: context admission is not yet a closed offload loop

Real:

- agent_cli has local token estimation, admission bands, repacking, bounded history, post-tool admission, provider-context-error recovery, and context receipts.
- context_pack has deterministic modes and clipping.
- OpenClaw config has compaction, transcript limits, a mid-turn precheck, and a memory-flush threshold.
- The OpenClaw hook records room and trajectory events, including session:compact:after.

Not proven:

- agent_cli pressure calls swarm_surface.route_novel.
- agent_cli pressure enqueues a compact pressure task to swarm_worker.
- agent_cli pressure writes a current checkpoint before discarding context.
- the OpenClaw hook pre-admits or routes pressure; it is observational after the event.
- a worker result is reintegrated with a postcondition receipt.

Concrete prior pressure exists:

- Ollama rows reached estimated 23748 against a 27000 window, with a 22950 threshold, and were marked red/allowed=false.
- Groq provider-context errors occurred while the local estimate was green, showing that local estimates and provider acceptance are not equivalent.

The repo config has reserveTokensFloor 30000, while the reported runtime error suggested 100000 or higher. That suggestion must not be copied blindly: it is a provider/runtime configuration decision that needs a measured context budget, not a magic number.

### F4 — HIGH: the organ map confuses path existence with invocation

mag/organ_map.py computes wired_paths by checking whether each wired_by path exists. It does not inspect imports, calls, runtime registration, or invocation receipts.

Example:

- context_checkpoint is declared wired by mag/agent_cli.py.
- Actual checkpoint calls were found in mag/ghost.py and mag/copilot_bridge.py.
- No current agent_cli call path was found for checkpoint_turn, restore_pointer, or the pressure-to-checkpoint edge.

This creates exactly the “we assumed the organ existed” failure mode the water-computer method is meant to expose.

Required map distinction:

- declared: named in the registry
- present: implementation file exists
- imported: caller imports it
- invoked: caller executes it
- evidenced: invocation leaves a receipt
- live: a recent receipt satisfies the organ's contract

### F5 — HIGH: worker completion is not goal satisfaction

swarm_worker has queued, claimed, running, done, failed, and result-file states. For agent tasks, success is effectively process exit code zero plus nonempty output. run_rightsized_once also uses deterministic/local completion rules.

There is no generic postcondition evidence, contribution receipt, action receipt, or independently checked goal predicate. This is specification gaming territory: the system can report a successful run while failing the intended job.

### F6 — HIGH: the offload backlog and maintenance loop are not healthy

Current queue status:

    queued 143
    running 1
    done 58
    failed 463
    cancelled 572

The queue has 1237 JSON files in total. Recent results include model timeouts after 360 seconds.

autodrain reports running=false and a stale last beat from 2026-08-26. self_audit's last report is stale. Four patches remain pending in openclaw_patches status:

    ask_router.json
    board_directive.json
    swarm_cycle.json
    x_auth_once.json

This is not a reason to turn on an unbounded drainer. It is a reason to freeze the backlog, classify failure causes, and drain bounded batches only after the authority and evidence contracts are repaired.

### F7 — MEDIUM: headless process invariants are red

guard_registry check reports spawn sites missing CREATE_NO_WINDOW for eight listed sites and recommends alert_backoff. One visible fallback in mag/autodrain.py invokes tasklist without that invariant.

This is an operational hygiene issue, but it matters because a hidden worker fleet can produce duplicate, orphaned, or unobservable work.

### F8 — MEDIUM: provenance exists as a slice, not a system property

mag/provenance_gate.py is a real stdlib gate with evidence records, citations, claims, grounding, and verdicts. Broad search found no end-to-end integration from agent_cli, tools, blackboard, or worker completion into ProvenanceGate.

The current system therefore has provenance code, but not provenance mediation.

## Closed-loop reality check

The intended loop appears to be:

    OpenClaw transcript
        -> admission
        -> context pack/checkpoint
        -> pressure handoff
        -> swarm worker
        -> model result
        -> verified postcondition
        -> blackboard/ledger receipt
        -> Verkle integrity anchor
        -> map/status update

Evidence currently supports this narrower shape:

    OpenClaw transcript
        -> after-the-fact room/trajectory logs
        -> local agent_cli admission/repack

    swarm queue
        -> claimed worker process
        -> result file

    blackboard tool
        -> direct pinned JSON file

    seat mesh switchboard
        -> peer/steer/route behavior

    manifest
        -> narrow anchor verification

The missing or broken bridges are:

    admission -X-> automatic checkpoint + compact pressure handoff
    worker result -X-> postcondition evidence
    blackboard -X-> reference monitor
    reference monitor -X-> effect broker
    Verkle chain -X-> currently valid global integrity proof
    evidence receipt -X-> truthful derived organ status

## Basecamp climb: first steps, in order

### Step 0 — Freeze the map

Record a source-tree snapshot, configuration hashes, raw evidence-store hashes, and the current dirty-worktree classification. Do not clean, reset, or bulk-apply pending patches. Separate source, generated artifacts, inbox patches, and runtime evidence.

### Step 1 — Quarantine and repair Verkle evidence

Make a dated, read-only forensic copy. Preserve malformed records. Add fail-closed tests. Establish a new chain identity if recovery requires reconstruction. Until this is complete, label Verkle status integrity-degraded and do not use it as a canonical receipt.

### Step 2 — Split the switchboard names

Rename the current semantic concept in the map to seat_mesh or steering_mesh. Reserve reference_monitor for the planned authority component. This is a map repair and prevents a real mesh from being mistaken for a security boundary.

### Step 3 — Implement one minimal mediated effect

Use board_write as the first narrow effect. Require a typed proposal, explicit requested effect, capability, budget, TTL, grant, and receipt. Ensure model-facing free text can never directly grant it. Make direct blackboard writes fail or route through the same boundary.

### Step 4 — Add the pressure handoff contract

On a red or black admission event, emit a compact PressureEvent containing session identity, provider, estimated tokens, window, threshold, residual pointer, and the chosen action. Checkpoint before discard. Enqueue only the compact event or pointer, not the entire transcript. Require a result receipt.

### Step 5 — Add postconditions to worker tasks

Every task must declare a goal predicate and evidence requirements. “Process exited zero” remains an execution fact, not a success verdict. A task can be complete only when its postcondition evidence is present and independently checkable.

### Step 6 — Make the organ map evidence-derived

Replace path-existence wiring with call-graph or registration evidence plus recent invocation receipts. Mark every edge with last invocation, receipt path, contract version, and failure state. Generate the status document from those receipts.

### Step 7 — Re-test OpenClaw under a controlled configuration

Only after the local contracts are stable, start a controlled OpenClaw run. Snapshot the host config first. Measure actual provider limits and compaction behavior. Adjust reserve floors based on those measurements; do not assume the 100000 recommendation is universally valid.

### Step 8 — Drain in bounded batches

Do not start the stale autodrain blindly. Classify the 463 failures and 572 cancellations, select a small batch, record before/after queue state, and require the worker/postcondition contract for each batch.

## Safe claims now

The following are real enough to use with caveats:

- deterministic local context admission and repacking
- context-pack generation
- a swarm queue and worker executor
- a seat mesh with tiered steering
- a direct blackboard store
- a self-audit probe
- a narrow manifest anchor check
- a Dirac-style topology observer

The following are not proven:

- a closed flywheel
- automatic context offload through the swarm
- a complete reference monitor
- a general effect broker
- authority mediated by the blackboard
- semantic success of worker tasks
- current global Verkle integrity
- live Atlas, Basecamp, Elder, or Fireball organs
- end-to-end provenance enforcement
- current OpenClaw frontend/gateway liveness

## Verification receipts

Focused deterministic slice:

    45 passed in 42.54s

OpenClaw/config/switchboard/context slice:

    15 passed in 7.90s

Bounded full-suite first-failure run:

    495 passed, 7 skipped, 1 failed

First reliable failure:

    tests/test_ghost_spooky.py::test_probe_carries_real_verkle_proof
    AssertionError: prove block must carry a knot pointer

Dirac operational scan:

    betti1=8
    open_gaps=6
    closed_solved=0

Switchboard self-test:

    ok=true
    tier_gate=true
    n_seats=33
    mesh_peers=81
    dry_drop=true

The passing focused tests show that several components are internally coherent. They do not establish cross-organ liveness.

## Bibliography and design anchors

- Nii, H. Penny. Blackboard systems: https://onlinelibrary.wiley.com/doi/abs/10.1609/aimag.v7i2.537
- NIST, Reference Monitor: https://csrc.nist.gov/glossary/term/reference_monitor
- W3C, PROV Primer: https://www.w3.org/TR/prov-primer/
- DeepMind, Specification gaming: https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/
- Skalse et al., Reward hacking: https://arxiv.org/abs/2209.13085
- Gray Swan AI Proving Ground: https://www.grayswan.ai/news/introducing-the-gray-swan-ai-proving-ground
- NIST CAISI agent security red teaming: https://www.nist.gov/blogs/caisi-research-blog/insights-ai-agent-security-large-scale-red-teaming-competition
- Diamond Age / education research context: https://www.tandfonline.com/doi/full/10.1080/00131857.2025.2494589
- U.S. State Department, historical Boxer/Tianjin materials: https://history.state.gov/historicaldocuments/frus1870/d223 and https://history.state.gov/historicaldocuments/frus1870/d225

These sources support the architectural principles and historical/adversarial framing. They do not prove claims about this repository. Repository claims above are based on the local code, tests, runtime inventories, and evidence files inspected during this audit.

## Audit boundary

No production code was changed during this audit. Existing worktree modifications and generated artifacts were preserved. The next safe implementation turn should begin with Step 0 and Step 1, not with a broad patch application or an unbounded worker drain.
