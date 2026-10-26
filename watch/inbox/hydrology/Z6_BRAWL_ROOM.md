# Z6 — brawl-first Room integration (2026-09-29)

**Lane:** hydrology, Z6 · **Verdict executed:** Y3 (`Y3_MUD_ROOM.md` — game_brawl first; game_mud stays blocked on its world-key split) · **Files owned:** `mag/game_brawl.py` (additive) + `tests/test_room.py` (amendment). No commit.

## What landed

`server/room.py`'s Room is now the tavern's spectator fan-out, wired per
Y3's spec. The engine keeps authority (initiative/HP/hit never moved); the
room moves bytes only.

- **One Room per brawl_id** — module registry `_BRAWL_ROOMS` +
  `brawl_room(brawl_id, create=…)` (lazily created on first seat),
  `join_brawl_room(...)` for player seat + spectators (live loop required:
  Room.join spawns the writer task), `close_brawl_room(brawl_id)` async
  shutdown (drops every seat, reaps writers, clears the registry entry).
- **`handle_brawl_voice` is the inbound-frame handler** — new optional
  `member_id` param (backward compatible; `mag/voice_turn.py` callers use
  keywords and are untouched). Per frame: `_touch_brawl_member` →
  `room.touch(member_id)` (presence refreshed on receipt), then the engine
  runs with full authority.
- **publish() broadcasts the advance/react lines** — `_room_wire_result`
  runs post-engine on every handled frame: takes the result's `events`
  (fallback: `speak` splitlines), encodes ONE canonical frame via
  `server.protocol.encode` (`{"op":"brawl","brawl_id","status","lines"}`),
  `room.publish(frame)` hands the same bytes object to every seat
  (encode-once law; no seats → 0 delivered, no-op).
- **sweep() expires a silent awaiting_player** — when a handled frame
  leaves the brawl `awaiting_player`, the room sweeps seats silent past
  `expire` (default 6.0s); the frame sender's own touch keeps their seat
  alive.

## Test (tests/test_room.py amendment)

`test_brawl_room_two_spectators_publish_touch_sweep` — fixture brawl
(`awaiting_player` at the pc seat, campaign linked by session, dirs
monkeypatched to tmp, dice pinned to total-2 so all attacks miss and the
engine loop is deterministic):

- player seat + two spectators; `brawl_room(create=True) is room` (one
  room per brawl_id).
- frame 1 = real player line ("punch vex"): all three seats receive the
  published lines, and `player.got[0] is ada.got[0] is bog.got[0]` (same
  bytes object); frame parses as op `brawl` with brawl_id + lines.
- frames 2-3: the slow spectator (drained one frame, then parked in send,
  maxsize=1) is dropped reason `"slow"` on the third publish — the frame
  handler still returns ok (never blocked), fast seats lose nothing.
- sweep: both remaining seats backdated 7s; next frame touches only the
  sender → silent spectator expired (`dropped["expired"]==1`), sender
  survives by touch, keeps receiving.
- `close_brawl_room` reaps everything; registry entry gone.

## Numbers (real, named instrument)

- `pytest -q` (executed, full suite, 2026-09-29 this run, 2452s):
  **7 failed, 3039 passed, 12 skipped, 3 errors.** All failures/errors
  sit in other lanes' in-flight working-tree files — visible:
  `test_rollup_delta` ×3 (`tools/rollup_delta.py` carries a pre-existing
  syntax error, flagged by the ratchet NEW before this lane touched
  anything), `test_reconstruct` (OSError 22), `test_party_subchain`
  (concurrency), `test_behavioral_awareness` (unresolved `<<<<<<<` merge
  conflict markers at line 70). No test in the tree imports
  `mag.game_brawl` except the amendment; none of the failures touch
  brawl/room/server/game paths.
- Neighborhood (executed): `test_room.py test_room_tags.py
  test_server_v0.py test_protocol_table.py test_game_entry.py
  test_game_live.py test_game_dm.py` → **66 passed** (includes the new
  brawl-room law; `tests/test_room.py` alone: 6 passed).
- Ratchet (`tools/violation_ratchet.py check --changed`): FAIL — 2 NEW,
  both in `tools/rollup_delta.py` (another lane's uncommitted file, parse
  error + file-too-long); zero hits in this lane's files.
