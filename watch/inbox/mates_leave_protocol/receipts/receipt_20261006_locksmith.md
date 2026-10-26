# Receipt: locksmith cycle 2026-10-06 (INTERIM, cycle in progress)

Mate: THE LOCKSMITH (mission_20261006_02_locksmith.md, claimed sidecar 08:00:10).
Status: IN PROGRESS. This interim file honors the receipt-before-speech law
mid-road; it is rewritten with the final FINDINGS/COUNTS when the cycle ends
(resume-not-respawn: if this file still says INTERIM, the next cycle resumes me
by id and reads the JOURNEY below as the live road).

## FINDINGS (so far)

1. The seed thread premise is STALE. "WaterGraph.boil + cold condensation has
   zero production callers" was false on arrival today. The boil door is wired,
   tested, and has live traffic:
   - server/world.py:358 calls self.graph.boil(target, 1) in _apply; the verb
     row "boil" sits in the bound wire table (server/protocol_table.py:123-124,
     handler world_boil); validate() gates it (server/world.py:258).
   - Live proof this cycle: `python -m server.server --demo --tick-ms 40`
     printed "THE CROWN FILLS. WIN at tick 4; boiler boiled 4, tagger tagged
     30." (30 ticks, 2 clients, 34 actions staged, 0 rate-capped).
   - History: mates.yaml seed text born 2026-09-29 (commit 172279a2d); the
     same day's MICKEY17 commit (bd41b4062) already reported "our server v0
     formal (15/15, WIN at tick 4) included". WIN at tick 4 requires four
     boils (crown is fed only by steam condensation). The seed was likely
     stale within a day of being written; five locksmith packs (0930, 1002,
     1003, 1004, 1005) carried it unexecuted; no locksmith receipt exists for
     any of them (receipts dir held 0 locksmith files on arrival).

2. Real caller census of WaterGraph.boil (pattern `\.boil\(`, this tree):
   16 call sites in 15 files = 1 production (server/world.py) + 4 tools
   (rule_parity, legality_dataset, k8s_water_sim, field_experiment) + 7 tests
   + 1 archived experiment (watch/inbox v3_deepseek_test) + 3 GDScript mirrors
   (game.gd:698 SPACE->boil, terrain_loader.gd:188, rule_parity_runner.gd:264).
   One further match is an unrelated same-name method (tests/test_distill.py:28,
   the mag distill organ). Cold condensation runs inside every tick
   (mag/water_graph.py:229 via _condense_steam:204).

3. NEW LOCKED DOOR FOUND (self-chosen next thread, same family, one room over):
   server/ws_door.py is imported by NOBODY in production. Its own docstring
   (lines 12-18) defines "THE 3-LINE INTEGRATION (the server owner adds to
   server/server.py; this lane does not edit that file)" and the server owner
   never did it. The door is fully built and tested (tests/test_room.py, 557
   lines, RFC6455 byte-level) and the standalone heartbeat demo exists, but
   the world server never opens it: zero browsers have ever seen a Mountain
   tick. Worse, the docstring's mount seam is STALE: it says WorldServer.
   pump_once, but B15 (rooms.py, 2026-09-30) moved the encode+broadcast into
   GameRoom.pump_once (rooms.py:147-148). The fix is the B15-adapted mount:
   an on_broadcast hook on GameRoom (mirroring the Z1 on_tick weld precedent)
   + WsDoor started in WorldServer.start behind a default-off flag (the
   allow_plaintext_hello migration-flag shape), door stop in stop(), ws_clients
   count in stats() (the counts-are-filed honesty law).

## JOURNEY (threads in order, dead ends named, why each turn)

1. Read the pack; checked the claim sidecar + receipts dir: 0 prior locksmith
   receipts, 2 sibling receipts today (archaeologist, mariner). Turn: the seed
   is virgin, nobody ever rode it.
2. Grepped WaterGraph + condensation: engine at mag/water_graph.py read in
   full (boil:170, _condense_steam:204, V5 waste-basin law, R8 int domain).
   Turn: establish what the organ actually is before judging the claim.
3. Grepped `\.boil\(`: found server/world.py:358 calling it. Turn: the premise
   said ZERO production callers; one counterexample kills it, so verify the
   whole chain instead of assuming.
4. Read server/world.py in full: validate() gates boil (DRY_POOL law), _apply
   boils 1, tick() checks crown >= 4 (WIN). Read protocol_table.py head: the
   DEFAULT table carries the boil row. Turn: is the row on the live wire?
5. Read server/README.md + git log: server v0 formal 15/15 WIN at tick 4
   landed 2026-09-29 (bd41b4062), bytes committed 2026-09-30 (0b846c01f);
   Godot client SPACE->boil (B1.0 fix comment, game.gd:698); playtest commit
   (785b1b139) says "4-SPACE win". Turn: the door has had traffic since
   09-29; run the live proof myself.
6. DEAD END (named): the seed thread as a "door to open". Ran the demo:
   WIN at tick 4, live. The seed is a stale report, not a locked door. Why
   the turn: a locksmith who forces an open door is a burglar, not a
   locksmith; the honest deliverable is the verdict + evidence, then the
   next real door.
7. Grepped ws_door imports: only its own file + its test. Read ws_door.py,
   room.py, rooms.py, server.py seams: the mount never happened AND the
   documented seam moved under it (B15). Turn: this is a real locked door in
   the seed's own family; open it.
8. (in progress) B15-adapted mount: spec updates (ws_door docstring, rooms.py
   docstring, server README), then the on_broadcast hook + --ws flag + tests.

## COUNTS (real, this cycle so far)

- demo run: 30 ticks, 2 clients, 34 staged actions, WIN at tick 4, 0
  rate-capped, 0 stale nonces.
- WaterGraph.boil call sites: 16 in 15 files (1 production, 4 tools, 7 tests,
  1 experiment, 3 GDScript) + 1 unrelated same-name method.
- locksmith receipts before this cycle: 0 (receipts dir read 2026-10-06
  08:2x EDT: 2 files, both siblings).
- ws_door production importers: 0. ws_door test file: 1 (tests/test_room.py,
  557 lines). ws_door lines: 341. rooms.py lines: 331. server.py lines: 1025.
- Prior locksmith packs carrying this same stale seed: 5 (0930, 1002, 1003,
  1004, 1005); all unexecuted (no receipts).

## LAWS HONORED

- No env dumps anywhere in this cycle. No API keys used (all work local on
  this account, per the COMPUTE LADDER steer). Em-dash count in this receipt: 0.
