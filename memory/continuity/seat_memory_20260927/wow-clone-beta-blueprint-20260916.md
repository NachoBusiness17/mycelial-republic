---
name: wow-clone-beta-blueprint-20260916
description: Operator order "build our game using it full blast — beta of our wow
  clone" → bones-legal world blueprint filed; NOT a private server (GPL laws read,
  world ours); milestones M0-M5; Union Alpha drafts full blast, editor seat
  verifies, falsifiers bind; W1 (M0 world skeleton) + W2 (M2 player ledger) fired
metadata:
  node_type: memory
  type: project
  originSessionId: sess_f8f2909b-0ac5-4763-abba-fbd8ba748f54
---

2026-09-16 night, operator: "Build our game using it full blast — beta of our wow clone —
what would that look like via our current plans; self steal and think about what it would
entail." Blueprint filed at watch/inbox/WOW_CLONE_BETA_BLUEPRINT_20260916.md.

## The law (self-steal from our own bones)

NOT a WoW private server, ever. AzerothCore is GPL-2.0: we READ the laws (725 verbs, status
gate before the verb, encounter machine, seeded replay) and WRITE OUR OWN WORLD — the clone
clones design lessons, not content. Anti-goals hold (no C++, no MySQL, no client, no copied
content).

## What the beta IS (from our own plans)

The "second client" from [[from-mud-to-wow-article]], along its own organ map (deploy →
relay → player files → room server): Adam — player one — walks/fights/loots through Discord
(Mag#2124 front door, /bones grows into /play), every session leaves a wow_session.v1
receipt that replays byte-identical. The referee chain already exists end-to-end (kernels →
session runner → adapter, 52 tests) — see [[hermes-wow-bones-azerothcore-20260916]].

## Architecture (every piece already in the tree)

World = rooms as legality tables (verbs through the bones Dispatch gate; a door is a
legality row). Combat = souls grammar (telegraph ≥0.35s → rollable i-frames → punish;
P-LEGAL; every-enemy-can-kill — the toy verb grown up). RNG = Stream kernel (every damage
tick a recorded draw). Loot = receipted packs. Encounters = Instance kernel with guarded
DONE (raid-door law). **Player file = append-only receipts — a character is a ledger, not
a database row; login is resume-from-ledger** (anti-MySQL made structural). QA =
fifty-wide harness pattern (unwinnable-state hunts by width).

## Milestones M0-M5 (UA drafts / editor verifies / falsifier binds)

M0 bones-world skeleton (rooms + movement through the gate; falsifier: same seed+route →
byte-identical receipt) → M1 authoritative room server (relay graduates presence→state;
two clients one seed identical state) → M2 player files (cold-restart resume
byte-identical; no timestamps in the file) → M3 one zone/one enemy/one loot pack (honest
start; P-LEGAL sweep; kill possible-but-avoidable) → M4 /play Discord surface (gated on
the operator's channel click) → M5 fifty-wide playtest (zero unwinnable states, first
punish <60s). Scope frozen through Sep-20 per the witness's law — M0 only until the demo
ships.

## What it entails (honest)

Union Alpha's pen is fast, its self-grading is broken (grade B tonight: wrong-signed
checks, vacuous locals() filters — U3) → **the editor seat is the bottleneck and is
forever**. We do not compete on graphics/content volume; we compete on VERIFIABLE PLAY —
a world where every session is a receipt. The free week is the drafting sprint.

## Fired → LANDED

W1 = M0 skeleton **LANDED**: mag/wow_world.py + tests/test_wow_world.py (12 passed). Key
scheme VERB@ROOM:<id> — the gate keys rows by name alone, so per-room GO_NORTH rows would
silently overwrite; locked exit → STATUS_NEVER, missing → UNKNOWN_OPCODE, handler_ran
always False on refusals; sessions bind the world digest (table edit refuses resume).
M0 falsifier proven CROSS-PROCESS: same seed + same route in two interpreters →
byte-identical receipts. UNION-ALPHA GRADE B (two 429 waves from the saturating free pool,
attempt 4 succeeded, $0). FLAGGED DECISION for the operator (made alone, two-line revert):
encounters load on the first successful NON-MOVEMENT verb in a boss room — bones-verbatim
loading makes room encounter data decorative, and the naive room-conditional fix would let
a 3-draw DONE bypass the Instance guard as a "load". Every DONE is a guarded transition.
FULL-SUITE CENSUS (first of the night): 32 failed / 1,427 passed / 9 skipped in 911s — all
failures pre-existing in unrelated subsystems, nothing regressed.
W2 = M2 player ledger **LANDED** (mag/wow_player.py + tests/test_wow_player.py, 17 passed;
wow_player.v1 append-only hash-chained rows; load() replays rows through pure reducers and
refuses the file VIEW_MISMATCH if the view lies; typed refusal order BAD_SCHEMA→BAD_ID→
BAD_N→BROKEN_CHAIN→TAMPERED→VIEW_MISMATCH; double-create refuses ALREADY_EXISTS; no
timestamps — structurally impossible by exact key-sets). M2 falsifier proven CROSS-PROCESS:
one interpreter plays a life, a fresh interpreter resumes → identical canonical bytes.
Union Alpha pen-grade A- as drafter (contract-faithful; added an unrequested
LEDGER_CONFLICT history guard making append-only hold at file level); the editor's own
tamper was wrong first — the ledger's refusal order was correct.
Also landed for the game estate: U1 THE TOY (dashboard/static/games/toy.html + scripts/
test_toy.js, 12/12 — first telegraph 0.667s, P-LEGAL clean, fork at exact frame) and U3 the
hydraulic XOR sim kernel (mag/hydro_xor_sim.py 15/15; P7 protocol ambiguity found in C18;
siphon spec 200 mL in 9–11 s).

Operator approved the build ("we wanna build this thing, do it, sounds good") and ordered
the blueprint through the ractors first "tease it out for nuance" → RS_WORLDBUILD_SALON
**CLOSED: blueprint SURVIVES with 7 amendments, no milestone dies** (receipt
RS_WORLDBUILD_SALON.md, $0, 14 free-lane calls). The amendments, pending operator fold-gate:
(1) the alone-decision (encounter-load law) is UNDERSPECIFIED — does `inspect` wake the
boss, no atomicity, no instance scoping, DONE lacks a victory predicate; (2) the missing
abstraction for M1 is the DOOR as a first-class stateful legality object (receipts must
hash door/lock state, not just room id); (3) telegraph 0.35s is a delivery-and-input
TIMING CONTRACT problem in the Discord medium (latency counted — amends M3; souls purist
and referee lawyer converged on this independently); (4) typed refusals read as silent
blocks to player one — hint the legal path inline (`[locked: /unlock]`) (amends M0/M4);
(5) second verb (defend/counter) drafted but GATED on playtest-fatigue evidence; (6) packs
prove issuance not ownership; death has no durable transition; (7) M1 re-specified as a
sequenced world-event log as the authority, ledgers/receipts as projections. Strongest
signal: the purist/lawyer convergence. Player-one's delight finding: the signed loot
receipt itself is the first delight moment. Also flagged: no Soul Castle lore file exists
anywhere — the 4 NPC speeches are drafts offered to Melissa, not canon.
Related: [[union-alpha-free-window-20260916]], [[wave-protocol-20260916]],
[[hermes-wow-bones-azerothcore-20260916]], [[design-myco-memory-20260916]].
