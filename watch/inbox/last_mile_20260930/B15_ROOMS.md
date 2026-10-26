# B15 ROOMS — minimal multi-room v0 (2026-09-30)

Fence: `server/rooms.py` (new) + `server/server.py` wiring + `tests/test_rooms.py`. No commit.

Closes MC3's gap-dossier row (watch/inbox/mountain_climb/GAP_ANALYSIS.md system 1):
"One room (`room.py`); no multi-room". Naming law: `server/room.py` stays the
TRANSPORT Room; `server/rooms.py` owns the GAME room.

## What landed

1. **A Room = one MountainWorld + its own tick pump + its peers.**
   `GameRoom` (server/rooms.py): `world`, per-room `peers` dict, its own
   `_tick_loop` task (`ensure_pump`/`stop_pump`), `broadcast()` fan-out
   scoped to its own peers (encode-once law preserved per room).
   `RoomBook` keys rooms by short id (`^[a-z0-9][a-z0-9_-]{0,15}$`).
2. **The join surface gains a room argument, default "summit".**
   - `hello` gains optional `"room"` (absent/None = default room; existing
     clients byte-identical). `welcome` now states `"room"`.
   - The `action` op gains optional `"room"`: the join verb literally takes
     a room argument (`action(sid,"join","terrace",room="basecamp")` acks,
     applies in that room's world). Routing law: no room field = the sid's
     own room (roster scan; fallback default so an unknown sid keeps the v0
     UNKNOWN_SID bytes); named room must exist (born-at-hello) else
     UNKNOWN_ROOM; malformed id BAD_ROOM; a sid from another room meets that
     world's own UNKNOWN_SID.
3. **Innkeeper per-room, memories scoped per room.** Every room with a
   durable root gets its own `Innkeeper` + `attach()`; memories at
   `<stem>.players.json` (default) / `<stem>.<room>.players.json` (side
   rooms). Its gated say rows are staged back into ITS world via the
   ordinary `say` channel (zero new wire ops) and apply at that room's next
   tick: two visits to summit earn "Welcome back"; the first visit to
   basecamp still hears "Welcome" (test-proven).
4. **Cross-room isolation, structural.** `GameRoom.pump_once` ticks its own
   world and fans out to its own peers only; a peer sits in exactly one
   room. Tested hard: room B's raw broadcast bytes are byte-identical to a
   solo `MountainWorld` run; each client times out silent when only the
   other room pumps; `srv.pump_once()` (both rooms) yields each client
   exactly one line.
5. **Capacity law.** Soft cap per room (`DEFAULT_ROOM_CAPACITY = 8` seats,
   `WorldServer(room_capacity=...)`); a full room refuses hello with
   ROOM_FULL BEFORE a sid is issued; the refused connection keeps its old
   binding and can seat elsewhere. Seats count peers, not sessions
   (re-hello never self-fills).
6. Extra laws: side rooms sleep when the last peer leaves (pump stops,
   world stays open; default room never sleeps); side rooms born at hello
   get durable roots beside the standing log (`world_log.<room>.jsonl`);
   the Z1 verdict-feed weld moved onto the DEFAULT room's `on_tick` hook,
   fail-open preserved verbatim.

## Compatibility

- `srv.world` = default room's world (test_chat/test_anticheat read it).
- `WorldServer.pump_once()` ticks every live room, returns the default
  room's payload (v0 contract); per-room manual drive `srv.rooms[<id>].pump_once()`.
- `stats()` keeps every key ("ticks" = default room clock) + additive
  "rooms"; `--demo` unchanged (WIN at tick 4 on smoke).

## Tests (instrument + moment + numbers)

- NEW `tests/test_rooms.py`: 7 passed, 2026-09-29 (venv pytest -q).
  Laws: independence, byte-hard isolation, join/default compat (default log
  lands at the exact log_path), action room vocabulary, per-room innkeeper
  scoping, capacity, sleep law.
- Server family: `test_server_v0 test_chat test_anticheat test_innkeeper
  test_rooms test_protocol_table test_motion_rows test_verdict_feed
  test_room` = 161 passed (2026-09-29, same interpreter).
- Sibling-lane `tests/test_auth_srp6.py` (B4, landed mid-flight): 12 passed
  against the rooms wiring (my `_grant_session` change is signature-compatible).
- `--demo --tick-ms 25 --ticks 30`: WIN at tick 4, exit 0.
- KNOWN PRE-EXISTING RED, NOT MINE: `tests/test_server_persist.py` = 5
  failed / 2 passed at CLEAN HEAD (all working-tree changes stashed,
  byte-verified) — "snapshot row disagrees with replayed state". Belongs to
  the tree before B15/B4; flagged for the persist lane.

## Raced with B4 (SRP6)

B4 edited server/protocol.py, protocol_table.py, server/server.py
concurrently. All B15 edits rebase on their `_grant_session` seam (both
auth doors grant through it; room binding rides the hello door, SRP6 lands
default-room v0 — rooms+SRP6 interplay filed as v1 debt).

## v1 debt (not scope creep, filed)

Rooms+SRP6 interplay (srp_proof carries no room yet), live session travel
between rooms, per-room capacity overrides, a rooms-listing op, side-room
verdict-feed metering.
