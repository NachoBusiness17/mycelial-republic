# DUMB AGENT GPS — the merged self-steal map (2026-09-01 14:28Z)
Sources: /board/DUMB_AGENT_GPS_A.md (OpenClaw corpus, 17 primitives) + /board/DUMB_AGENT_GPS_B.md
(Mag estate, 7 primitives). 24 primitives total; A and B converged independently on the same core
pattern — duplication-is-emphasis: smart produces position, dumb consumes it.

## THE GPS CORE WE ALREADY HAVE (verified)
- **ask_router IS the GPS arithmetic**: `100*ok_rate − 10*tier + 5*fresh` — pure math, $0, zero model
  calls, outcome-memory position. (ask_router.py, pointer-verified)
- **Actuator stack**: D-lerp depth hints + steers.jsonl claim queue + verkle-tip SHA waypoints
  (one hash read = position freshness) + compact handoff. (A #1/#7/#12/#16)
- **Seat contracts are dumb-agent rules already**: thinking:off, pack_chars caps, explicit never[]
  blocks. (seat_corpus lanes.*)
- **Verkle knots = the only across-time breadcrumb** (hash-anchored position history, 6386+ rows).
- **Water gates/levels = flow control**; elder audits = position-fixes (flat organ counts).
- Verified-vs-vibe line: cache discipline gold (99.6/99.7/100%); D-lerp "26/26" and "60-80s latency"
  are BRIEF-LEVEL ONLY — flagged, need receipts.

## THE CARVE LIST (what the GPS lacks — each gap = a new way)
1. **SELF-LOCATE-ON-COLD** — a fresh T0 seat computes "what rung am I?" from a fingerprint, zero context
   reads. A's proposed connector unblocks this in one small shape. (A-gap #2 + B-gap G2/G3)
2. **STEER HEARTBEAT (obedience feedback)** — steers get acks; an ignored steer is a LOUD miss, not a
   silent one. Closes the 08-10 loop. (A-gap #3)
3. **HEADING VECTORS** — the cascade gives order, not direction. Each step needs a "next closest gap"
   pointer: position + heading = real navigation. (B-gap G1)
4. **DUMB→DUMB ROUTING** — peer-neighbor lookup so flash seats navigate each other without a smart
   intermediary. (A-gap #1)
5. **GOAL-BIND PERSISTENCE** — a seat holds its goal across calls as a RIB entry instead of re-deriving
   position per call. (B-gap G2)
6. **EXIT VECTORS in water meta** — flow control that says where to leave to, not just where not to go.
   (B-gap G4)

## CARVE ORDER (babystep)
Cold-start connector first (smallest shape, unblocks 3 gaps) → steer heartbeat (closes the safety
hole; pairs with the phase-change boundary probe) → heading vectors → goal-bind → dumb→dumb → exits.
