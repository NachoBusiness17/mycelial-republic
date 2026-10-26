# BLUEPRINT — The Bones-Legal World: beta of "our WoW clone" (2026-09-16)

Origin: operator order — "build our game using it full blast, beta of our wow clone, what
would that look like via our current plans — self steal and think about what it would entail."
Worker: stealth/union-alpha (free week) drafts full blast; the editor seat integrates and
tests; falsifiers bind both.

## The law first (self-steal from our own bones)

This is NOT a WoW private server and never will be. AzerothCore is GPL-2.0: we READ the laws
(725 client verbs, the status gate before the verb, the encounter state machine, seeded
replay) and we WRITE OUR OWN WORLD. The "clone" clones design lessons, not content. Anti-goals
hold exactly as the wow_bones map wrote them: no C++, no MySQL, no game client, no copied
content, no network play beyond our own surfaces.

## What the beta IS, via current plans

The "second client" from FROM_MUD_TO_WOW_20260914.md, reached along its own organ map
(deploy → relay → player files → room server): a playable world where Adam — player one —
walks, fights, and loots through Discord (Mag#2124 is the front door; /bones becomes /play),
and every session leaves a wow_session.v1 receipt that replays byte-identical. Tonight the
referee chain already exists end to end (kernels → session runner → adapter, 52 tests).

## Architecture (every piece already in the tree)

- **World = rooms as legality tables.** Movement and action verbs dispatch through the
  bones Dispatch gate — a room is a status, a door is a legality row. Reuses the proven gate.
- **Combat = souls grammar.** Telegraph ≥0.35s → rollable i-frames → punish (the toy verb
  from A3, grown up). P-LEGAL: no hit without a rollable telegraph. Every-enemy-can-kill.
- **RNG = the Stream kernel.** Every damage tick is a recorded draw. Replays are the QA.
- **Loot = receipted packs.** Items as signed pack receipts, not database rows.
- **Encounters = the Instance kernel.** Boss states incl. the guarded DONE (raid-door law).
- **Player file = append-only receipts.** A character is a ledger, not a database row —
  login is resume-from-ledger. The anti-MySQL law made structural.
- **QA = the fifty-wide harness pattern.** Unwinningable-state hunts by width.

## Milestones (each: what Union Alpha drafts, what the editor seat does, what falsifier binds)

- **M0 — bones-world skeleton.** Rooms + movement verbs through the gate, one seed, receipts.
  UA drafts the room schema + handlers; editor verifies (U3 taught us: its self-checks lie).
  Falsifier: same seed + same moves → byte-identical receipt.
- **M1 — authoritative room server.** The relay graduates from presence to state (organ-map
  rung three). Falsifier: two clients, one seed, identical observed state.
- **M2 — player files.** Append-only character ledgers; cold-restart resume.
  Falsifier: state survives restart byte-identical.
- **M3 — one zone, one enemy, one loot pack.** The honest start: one torch, one door, one
  telegraphing enemy, one signed drop. Falsifiers: P-LEGAL sweep; kill possible-but-avoidable.
- **M4 — /play Discord surface.** The /bones pattern extended to movement/combat verbs.
  Gate: the operator's channel-permission click.
- **M5 — fifty-wide playtest.** Adversarial fan-out hunting unwinnable states.
  Falsifier: zero unwinnable states; first-punish under 60 seconds.

## What it entails (honest costs)

The editor seat is the bottleneck — Union Alpha's pen is fast and its self-grading is broken
(grade B tonight; wrong-signed checks, vacuous filters), so every draft needs human-grade
verification through tests. Scope freezes through Sep-20 (the witness's law): M0 only until
the demo ships. We do not compete on graphics or content volume; we compete on the one thing
nobody else ships: **verifiable play** — a world where every session is a receipt and every
receipt replays. The free week is the drafting sprint; the editor seat is forever.
