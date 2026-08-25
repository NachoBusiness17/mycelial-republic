# DEEP STEAL — the room that remembers (2026-08-24)

**Date:** 2026-08-24
**Commitment:** `deep-steal-room-that-remembers-001`
**Method:** steal the INVARIANT from OUR OWN game (not an external field). The concept is ours;
this steal makes it a standing law + a build plan.
**Operator (verbatim):** "the room that can tell you about everything that ever happened in it
but has no idea what the next room has to say. Dig deep on that one." + "i think we need to
retire the old take what is useful and leave the rest in an archive so we can revisit it without
me stumbling upon it i'm pretty sure we talked about a museum and appending verkle history with
the current state of itself."

## Where the concept lives (all real, read this turn)

- `memory/steal/STEAL_PLACE_REMEMBERS_20260814.md`: "a place remembers what happened there. Not
  the player's log. THE ROOM." places/{room}.md ## happened = the dream. Deeds append. Glances do
  not. Knots remain ground truth; files are the visible diary.
- `mag/game_mud.py` ROOMS — each room IS a system: the World-Memory (verkle), the Mycelial
  Library (RIBs), the Forge-Hive (swarm), the Dungeon (tasks), the Gear (novel content), the Warm
  Springs (hot context), the Crystal Vault (VRAM), the Echo (voice), the Observatory
  (self-witness), the Shadowlands (neglected work). Each has a frontier QUESTION + prose + exits.
- THE HALL OF SHARED SUPPER (the mechanic): "the hall files which you chose" — the world observes
  what the player notices OR refuses to notice, and that becomes the record. `game.mud.hall_record`
  is a REAL verkle-committed fact (game_world.set_state), not flavor. Count -> filed. Eat past ->
  filed. The room keeps the choice forever.
- `mag/hall_shared_supper.py` — the deterministic slice: same start + same plays -> same
  content-addressed root on both seats. Play is the work; the state is the evidence.
- `mag/game_world.py` — server-authoritative world state, every change folded as a verkle knot
  (content-addressed leaf + recomputed root + changes log). A player action becomes true only
  when committed here.

## The invariant (the deep steal, one sentence)

**A room is a self-contained record of everything that happened in it — deeds only, glances never —
committed to the chain — and it has no knowledge of what the next room will say.**

Three laws unpack it:

1. **DEEDS APPEND, GLANCES DO NOT** (STEAL_PLACE_REMEMBERS). Only real state changes enter the
   room's record: talk, take, move, count, choose. Looking is free and leaves no trace. This is
   what separates a ROOM from a LOG — a log records everything, a room records what was DONE.
2. **THE ROOM FILES WHICH YOU CHOSE** (the Hall). Not just what happened — what the observer
   NOTICED or REFUSED to notice becomes the record. The empty chairs counted vs. eaten past are
   different histories. The world observes the choice, and the choice is the data. This is the
   noticing mechanic, and it is verkle-committed, not flavor.
3. **A ROOM HAS NO IDEA WHAT THE NEXT ROOM SAYS.** Each room is isolated from the FUTURE: it can
   tell you everything that happened in it, but cannot predict the next room's content. That is
   not a limitation — it is the honesty contract. No room overclaims the future; every room is
   only its own committed past. (Heisenberg in the maze: position in this room, momentum
   elsewhere; you do not get both sharp.)

## Why this is the museum

The operator's ask: retire the old surfaces (dashboard :8765, mirror desk :8743, the vis lab, the
hypervisor graphs) — take what is useful, leave the rest in an archive "so we can revisit it
without me stumbling upon it." That is EXACTLY the room-that-remembers applied to the stack:

- **A museum is a set of rooms.** Each retired surface becomes a ROOM: a self-contained,
  verkle-committed record of what that surface WAS and DID — its history, its useful invariants,
  its reason for retiring. Deeds appended (what it actually did), not a glossy description.
- **The museum room remembers itself, not the future.** An archived surface tells you everything
  about the surface as it was, and makes NO claim about what comes next. You can revisit it;
  it will not haunt the live stack.
- **"Appending verkle history with the current state of itself"** = the room commits its own
  terminal state to the chain as a leaf. The verkle chain already IS a museum of rooms: every
  session is a leaf that remembers that session. The new move: each retired surface gets a leaf
  that is the surface's own terminal self — so the chain can tell you everything that ever
  happened in it (including the retirement) without pretending to know the next room.

## Self-steal (already built — confirm, don't rebuild)

- The verkle chain IS the room-that-remembers backbone: every leaf = a session's committed
  history; prove_latest() + verify() = the room answering for itself.
- game_world.set_state = the "deeds append" writer (content-addressed leaf + root + changes log).
- hall_shared_supper = the deterministic slice (same start + plays -> same root on both seats).
- The Mirror desk's Mag stage already reads the living record; it is a museum VISITOR, not the
  museum itself.
- The dashboard is a room that remembers (2,511 sessions browsable) — the issue is it is STILL
  LIVE when the operator wants it RETIRED.

## The gap (what to build)

A **museum module** (`mag/museum.py`?): one deterministic, $0, verkle-committed archive action.

  retire(surface_name, *, kind, history, useful_invariants, why_retired, live_url)
    -> appends ONE leaf to the verkle chain (schema museum_room.v1) that IS the surface's
       terminal self: what it was, what it did, what we kept, why we retired it, where it was.
    -> moves/writes the surface's static + code pointer into memory/archive/<surface>/ so the
       operator no longer stumbles on it live (the dashboard/mirror processes stop; the archive
       is read-only, revisitable).
  visit(surface_name) -> read the archived room: everything that happened in it, no future claim.

The chain then answers: "what was the dashboard?" — the leaf tells you (a room that remembers
itself). And the NEXT room (the lane hypervisor) says only what IT is. No cross-room prophecy.

## Ordered adaptations (cheapest first)

1. THIS steal (memory) — deterministic + $0.
2. `museum.py` with retire()/visit() — appends museum_room.v1 leaves to the verkle chain; no
   process changes yet. Deterministic + $0.
3. Retire the OLD dashboard (:8765) and mirror (:8743) THROUGH museum.retire(): take what is
   useful (the mirror's lens stack, the dashboard's session browser, the fleet hypervisor's
   mermaid + bills), archive the rest, stop the live processes so the operator stops stumbling.
4. Point the live surface (lane hypervisor / work_loop) at the archive for "what happened" reads.

## Refuse

- Rebuilding the dashboard/mirror as new code. The museum is an ARCHIVE, not a rewrite.
- Deleting the old surfaces. They are sacred cows: archived, not slaughtered.
- A museum that predicts the future. The room's honesty is that it does NOT know the next room.

## Rope

Deeds append, glances don't; the room files which you chose; a room knows its own past and never
the next room's future. The chain is the museum; each leaf is a room; retiring is appending the
surface's terminal self.

## Fold with

STEAL_PLACE_REMEMBERS · game-hall-of-shared-supper-mechanic · WORLD_LEDGER_EMPTY_CHAIRS ·
verkle-knot (leaf = room) · game_world (deeds append) · surface_render (the hypervisor IS the
current room) · living-floorplan (the readable map of rooms) · ROCINANTE (bones = the rooms'
committed state, running = the stochastic life inside them).
