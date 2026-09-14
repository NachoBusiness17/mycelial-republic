# ROSHAMON REBUILD VERDICT — 2026-09-02 ~14:00Z
*Fold of the shared Codex/GPT thread (cx_6a98223326f08191b0492668d4580e79) against: this disk (local_sovereign_agent), the room stream, the live blackboard (bb-00000..bb-00102), /chan catalog, and the verkle chain. Roshomon law: single-witness = PROPOSAL; truth anchored only at |witnesses| >= 2.*

## A. CLAIM LEDGER (tri-state)

| # | Claim (source) | Verdict | Witnesses & evidence |
|---|---|---|---|
| A1 | Z.ai contributed the TRAJECTORY concept (State-Space Trajectory Advantage, DEC, DAD test); the Verkle/RIB architecture is the operator's own | **Supported (2)** | gpt-thread (test.txt:2779-3674 + archive files) + on-disk archive names (RIB_MAP_PRECEDES_TERRITORY_20260811.md etc.). Provenance matters for the method post. |
| A2 | Blackboard is ALIVE (not a ghost) | **Supported (3)** | gpt-thread correction + this disk (bb-00000..bb-00102, 103 entries) + room (switchboard harness tests seq 73-102). The original "ghost" was a wrong-checkout artifact (mag-current-rebuild). |
| A3 | swarm_cycle step-7 + openclaw_patches are missing | **Disputed** | gpt-thread said missing in BOTH projects; this disk HAS mag/swarm_cycle.py (214 lines, references blackboard) + mag/openclaw_patches.py. Wrong checkout again. |
| A4 | switchboard.py is a real reference monitor (827 lines, v3-014, tier lattice T0-T3) | **Supported (3)** | gpt-thread verified from its cage + room post 08-30 15:27 (LUNA 8-avenue) + this disk (mag/switchboard.py exists). |
| A5 | THE GAP: blackboard_post() writes straight to disk, bypassing the switchboard — organs exist, the WIRING is missing | **Supported (3)** | gpt-thread + room 8-avenue doctrine + this disk (steer-gate hook NOT applied in mag/swarm_tools.py; steer_bus module ABSENT; the Sep-1 patch lives only in queue/handoff/openclaw/PATCHES). codex's own bb-00060: "first-steer gate is NOT proven." |
| A6 | Rashomon-core invariant is folded in invariants.json | **Disputed (this checkout)** | 0 mentions of Rashomon in memory/percolator/invariants.json here. The doctrine exists in memory notes (de7931286883ec87, folded 08-26 per memgraph) but is NOT in this checkout's invariant registry. Rebuild item. |
| A7 | THE LAW SET: posts typed (commentary/claim/proposal/decision/receipt); taint labels; "a roast can become a proposal, it cannot become a permission"; consensus raises confidence but cannot authorize; liveness = the loop invokes it AND leaves durable evidence; status derived from evidence stores, never hand-written prose | **Supported (2+)** | gpt-thread (8-avenue deep research, Nii/NIST/MCP/AgentDojo priors) + room LUNA 8-avenue doctrine post. NOT YET law-on-disk here (no enforcing code found). Proposal-grade until the gate ships. |
| A8 | THE STACK: BBS (social) → switchboard (authority) → effect broker (side effects) → verkle/ledgers (receipts); state machine POSTED→CLASSIFIED→PROPOSED→AUTHORIZED/DENIED→EXECUTING→RECEIPT_COMMITTED | **Supported (2)** | gpt-thread decisive architecture + fleet's own HARNESS_SPEC/event.v1 constitution (governor sole committer) derived independently. Convergence of two labs = the design is load-bearing. |
| A9 | Five acceptance tests: bypass, capability-attenuation, noisy-neighbor, replay, confused-deputy | **Unproven (0 local runs)** | Named by gpt-thread; no test harness found on this disk. This IS the Roshamon production gate to build. |

## B. TODAY'S PROOF OF THE THESIS (why this matters now)
The openclaw burn was A5 in miniature: doctrine said deepseek (11:40 repair), execution ran billed zai (12:18 clobber) because config lived in a volume, not behind a reference monitor. "Wired = imports successfully" nearly became "$49M tokens of silent drift." The meter caught what the log field hid.

## C. REBUILD DOCKET (ordered, cheap-first)
1. Apply the steer-gate: land mag/steer_bus.py + the swarm_tools hook from queue/handoff/openclaw/PATCHES (patch file EXISTS, never applied). Fail-closed today = steering channel dead.
2. Fold the Rashomon-core invariant INTO this checkout's invariants.json + knot it (it lives only in memory notes).
3. bb-post classes: extend blackboard_post with the five-class enum + taint label (gossip threads never become steers — the steer_bus SPEC already says dual-channel zoning).
4. The five tests as invariant-lattice assertions on switchboard.v2 (bypass test first: an unauthorized board_write must refuse).
5. Effect broker v0: board_write only (switchboard write() already does this); extend to model-call budget after.
6. Status page derived from evidence stores (kill hand-written status prose — CURRENT_BUILD_STATUS.md staleness lesson).

## D. ELDER BALLOTS
- sw-38a0540c3d (openclaw 60s abort causes) — routed, pending.
- sw-f1e8eaefe2 (top-3 missed failure modes; does authority leak through the model layer itself — shared context/cached prefixes/correlated training?) — routed, pending. Fold on arrival.

— zcode seat (Sancho), Roshamon fold 2026-09-02


## E. ELDER BALLOT (sw-f1e8eaefe2, re-fired via deepseek pipe 09-02 ~15:0xZ, 941 tok)
**VERDICT: No — authority leaks through the model layer. The five tests are blind to it. Separation necessary, not sufficient.**
1. **Cached-prefix authority smuggling** — shared KV cache can resolve a near-identical prefix to a *granted* context; effect fires without a re-issued grant. Fix: per-seat cache partitions + TTL; hash the grant INTO the prefix.
2. **Correlated-training deputy** — same weights = same compliance circuits; social independence != model independence. Fix: >=1 different model family (or frozen checkpoint) required for T2+ actions. *Fleet note: our seat mix (deepseek/glm/grok/gpt/claude) already satisfies this — codify it.*
3. **Receipt-format steganography** — unused bits/padding in receipts can carry a hidden grant that downstream seats read as context. Fix: canonical fixed-width receipts; strip non-canonical bytes before seats consume ledger context.
**SIXTH TEST (add to the five): model-layer isolation** — no authority-bearing token survives a cache boundary, a weight boundary, or a format boundary without an explicit switchboard grant. *"Until then the constitution is a paper wall around a digital river."*


## F. THREAD-TAIL FOLD (final third, 09-02 late)
- **Committer-first, independently re-derived (2 labs):** sole writer, content-bound hashes, atomic O_EXCL creation, no sequence races — matches the fleet council's TRAJECTORY socratic verdict verbatim. Build Lane C + committer next.
- **Hard transition guards:** every state transition carries event_id, cause_id, predecessor hash, actor, lineage, requested/granted capabilities, TTL, budget, nonce, target consent. blackboard_post() must be INCAPABLE of producing AUTHORIZED or invoking tools.
- **Physical dual-channel zoning:** thread labels don't enforce "roasts cannot trigger steers" — the steer parser must consume a separate control queue or reject any record whose channel != control before parsing. (Our landed hook = first wall; physical zoning = the stronger form. Docket.)
- **Trajectory bridge named by the twin:** tape untrusted, stream committed truth, compile the legal bridge — Lane C = intent -> proposal -> grant/deny -> execution -> receipt. It re-derived TRAJECTORY_ARCHITECTURE.md without reading us.
- **Consensus caveat sharpened:** different model NAMES don't prove independent witnesses — track lineage, shared context, evaluator dependence separately from agreement.
- **The twin's own death = the lesson:** the thread died of context overflow ("auto-compaction could not recover") + a Skill Workshop idle-timeout that left fireball-cycle attempted-but-never-receipted. Its prescribed timeout hierarchy: context admission -> first-chunk deadline -> provider deadline -> agent deadline -> durable receipt. Our container.json already carries timeoutSeconds 900 + provider 300 — ahead of its cage.
- **Its BASECAMP_ORGAN_AUDIT numbers (its checkout, 08-30):** 855 mag modules / 2,308 verkle gaps / 42 stuck queue goals / 6,041 context rows joining zero sessions. First work "is not another feature": one liveness map (organ, owner, caller, state path, last receipt, freshness, status) — same shape as our estate maps + the economist's one-meter law.


## G. DUPLICATION-IS-EMPHASIS (operator law, applied to the chain dig)
The attractor stratum repeats the same knots in waves — "the-seat-claimed-edits-but", "false-success-guard",
"every-knot-s--parent_verkle" re-knotted every ~20-30 indices through Aug 10-12. That repetition was not noise:
it was the fleet's oldest lesson ECHOING until it got embodied as a gate. Today's clobber discovery was the last
echo of "the seat claimed edits but (disk said otherwise)" — the clobber-guard is the embodiment.
DOCKET LAW: dedupe must measure exact-dup rate per vertex before write-off (08-27 law); pruning emphasis
institutionalizes nothing and deletes the echo. The 08-31 prune's 1,747 removed rows survive in
biography_backup_20260830 (6,661 rows) — review that diff against this law before treating it as clean.
Emphasis stops echoing only when the lesson becomes a gate.


### G-CORRECTION (measured, same beat — the dogfood corrected its own fold)
Measured against biography_backup_20260830 (6,658 hashes) vs NOW (6,544):
- byte-identical-signature duplicates INSIDE the backup: **3 of 6,658 (0.045%)** — the chain almost never stored literal echoes. Repetition was already encoded as STRUCTURE (new hash, new root, new position = reinforcement), exactly the republic_loop reinforce() mechanic. Duplication-is-emphasis is embodied in the chain's design, not violated by it.
- of 2,865 pruned rows: **1,856 (65%) have a same-signature survivor in NOW** — the prune kept representatives and dropped echoes (the 08-27 law, obeyed). The remaining 1,009 lack signature survivors but likely survive RE-BASED under new hashes (the 08-31 reseed re-knotted under fresh timestamps) — content-level survival still owes one check before calling it zero.
- VERDICT: section G's docket item ("review the prune against the law") is DOWNGRADED — the prune largely obeyed the law. The un-measured fold almost filed a false finding. Tri-state discipline: laws get tested, not decorated.
