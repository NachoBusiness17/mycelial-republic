# SALON ROUNDTABLE — Diamond Age ghost-priority. 2026-08-31, 2 rounds, 4 seats.

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: all four seats independently name effect_broker as the first ghost to resurrect to unblock steps 3–7 — SUPPORTED (4/4 seat consensus recorded verbatim; round-2 witness passes still pending) · falsifier: a completed round-2 stress test flips the consensus, or the applied broker patch leaves steps 3–7 blocked

Lane note: operator's `mag.frontier_salon roundtable` command could not run from the cage
(WSL interop broken: `UtilBindVsockAnyPort socket failed 1`; dashboard :8765 unreachable).
Ran as OpenClaw subagent fan on free lanes instead (same pattern as salon_rib_20260831 lanes A–C).

## Question (from /board/PACK_DIAMOND_AGE_SYNTHESIS_20260830.md)

Given the 5 ghosts (`atlas`, `basecamp`, `elder`, `fireball_cycle`, `effect_broker`) and the
unwelded switchboard/blackboard boundary — which ONE ghost resurrected first maximally
unblocks steps 3–7 (inspector, ancestry, RolePacket experiment, receipt chain, red-team)?
One named next action per seat.

## Round 1

### Seat A — openrouter/auto (free lane; Groq rate-limited twice, lane-swapped)
effect_broker first — steps 3–7 depend on routing all mutations through one formalized gate.
NAMED ACTION: `.\.venv\Scripts\python.exe -m mag.openclaw_patches apply`

### Seat B — nvidia/deepseek-v4-flash-0731
Steps 3–7 are authority-and-side-effect problems, not content problems. Inspector pointless
without a single mutation route; ancestry/RolePacket/receipts/red-team all presuppose one
gated resolver = effect_broker ("the only route to side effects"). atlas/basecamp/elder are
read/context organs (downstream of control); fireball_cycle is play physics (orthogonal).
Resurrecting it welds the three-layer monitor: blackboard speaks, switchboard issues, broker acts.
NAMED ACTION: host `.\.venv\Scripts\python.exe -m mag.openclaw_patches apply` (flushes staged
mag/effect_broker.py), then verify `python -m mag.ghost_pylance diagnose --module mag.effect_broker`.

### Seat C — zai/glm-5.3-flash
All of steps 3–7 terminate at the resolver choke point: inspector inventories mutation paths
(broker is the canonical one); ancestry has nothing to measure until side effects flow through
one grantable route; RolePacket needs a scoped resolver; receipt chain is defined in broker
terms; red-team attacks the broker's perimeter. Switchboard is not a ghost — it becomes
testable once the broker gives it something to authorize. Work already staged, not hypothetical.
NAMED ACTION: operator runs `python -m mag.openclaw_patches apply` on the host, applying
`/patches/self_steal_effect_broker.json` — ghost → staged → live in one jail pass.

### Seat D — cerebras/gpt-oss-120b
effect_broker is the sole conduit for side effects, receipt generation, and verification of
capability ancestry. Without it: inspector cannot see mutations, ancestry cannot be measured,
experiments produce no verifiable receipts, red-team cannot exercise the boundary.
NAMED ACTION: land the staged `mag/effect_broker.py` patch (round-1 path was malformed;
corrected in round 2).

## Round 2 (witness passes + consensus stress-test)

(pending)
