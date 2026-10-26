# LW6 — CHAT V1: SAY RIDES THE TICK, WHISPER BYPASSES IT (2026-09-30)

Lane: last-mile wave (S19's spec: chat v1). No commit (operator's fence).
File ownership held: `server/protocol_table.py` + `server/world.py` + `tests/test_chat.py` only.

## What landed

| File | Change |
|---|---|
| `server/protocol_table.py` | CHAT dialect: `CHAT_SPEC`/`CHAT_TABLE`/`CHAT_DIGEST`/`CHAT_DISPATCH` — the four v0 rows plus `say`/`whisper` (`world_say`/`world_whisper` handlers), `BAD_TEXT` added to the closed reject vocabulary |
| `server/world.py` | `say` branch in `validate`/`_apply` (rides the ordinary stage→tick channel); `whisper` delivered at receipt onto `world.direct` (per-sid outbox + `drain_direct(sid)`), one `kind:"whisper"` audit row; `VERBS` now bound to `CHAT_TABLE.verbs`; `MAX_SAY = 240` |
| `tests/test_chat.py` | NEW. 17 tests: table superset law, say-in-next-tick, arrival-order interleave, determinism replay, text law (240/241 boundary), whisper target-only + per-user fanout + never-in-events, audit row shape, bot path, real-wire TCP for both verbs, v0 no-collateral |

## The dialect (the S19 spec, landed)

- **say** `{verb: say, target: <text>}` — zero new ops: it rides the existing
  `{"op":"action"}` line and the existing stage→tick machinery. Validated at
  receipt (empty or >240 chars → `BAD_TEXT`; 240 itself legal), staged in
  arrival order, applied at the next tick, event exactly `"user: text"`.
  Determinism untouched: the tick is still the only mutator, no RNG, no new
  log machinery (an action row like every other verb's).
- **whisper** `{verb: whisper, target: 'user|text'}` (first pipe splits; text
  may contain pipes) — the one verb applied at receipt: it mutates no world
  state, so it lands on `world.direct` as `{"op":"whisper","from":user,
  "text":text}` for every sid registered to the target user, OUTSIDE the
  canonical tick: readable before any tick, never staged, never broadcast,
  never in tick events. Unknown user → `UNKNOWN_TARGET`; malformed/empty/
  over-length → `BAD_TEXT`; unauthed sid → `UNKNOWN_SID` before text is read.
  One `kind:"whisper"` chained row (with `tick` field — the every-row-carries-
  a-tick law) keeps the server-side audit trail.
- **bot path** — any registered session speaks the same channel: a bot (a
  fish, the innkeeper) registers via `register_session` and stages `say`/
  `whisper` identically to a player. Tested with `innkeeper` + `fish_scout`.

## Contract law held

`CHAT_TABLE` follows the X9 law (receipt `watch/inbox/hydrology/X9_MOTION.md`):
a NEW contract version compiled from the DEFAULT rows, never an edit of the
bound v0 wire. Byte-verified against `git show HEAD:server/protocol_table.py`
compiled in a temp module (trust bytes, not test self-consistency):

- `PROTOCOL_DIGEST d41f7cba…9cf` — unchanged from HEAD (v0 wire byte-identical)
- `MOTION_DIGEST ce259465…637` — unchanged from HEAD
- `CHAT_DIGEST 3ce934f5a2ab56623b685f6ec6b7aab830ab05122a2372f92f2296d86b367574` — the new version

`server/protocol.py` was NOT touched (not this lane's fence): its pinned
`VERBS == ("boil","valve","join","tag")` surface stands; `world.py` binds to
`CHAT_TABLE.verbs` instead — a strict superset, so all four v0 paths are
byte-identical (the 138-test collateral run is the proof).

## Debt (named, not hidden)

- **Server-side whisper routing**: `world.direct` is the integration point;
  `server.py`'s writer queues do not drain it yet (server.py outside this
  lane's fence). The TCP test proves the world-side law today: the line
  waits in the outbox for the target sid alone.
- Whisper to a user with zero live sessions rejects `UNKNOWN_TARGET`; a
  "user offline" mailbox concept is v2 debt.

## Tests (real counts, this tree, this moment)

- `pytest tests/test_chat.py -q` → **17 passed** (1.11s; re-run after LF normalization with
  `tests/test_server_v0.py tests/test_protocol_table.py`: **57 passed**, 5.64s)
- Collateral (all MountainWorld/protocol consumers): `pytest tests/test_server_v0.py
  tests/test_protocol_table.py tests/test_motion_rows.py tests/test_verdict_feed.py
  tests/test_gods_number.py tests/test_chain_contract.py
  tests/test_ledger_registry.py tests/test_room.py
  tests/test_cast_server.py tests/test_wow_world.py -q` → **138 passed** (23.53s)
- Full suite: **attempted 3x, NOT claimed green.** Instrument + moment, honestly:
  (a) started ~05:45 EDT, `pytest -q` interrupted at collection — pre-existing
  unresolved merge conflict `UU tests/test_behavioral_awareness.py` (line 70
  `<<<<<<< Updated upstream`, SyntaxError; not this lane's fence, not touched by LW6);
  (b) started ~06:01 EDT, `pytest -q --ignore=tests/test_behavioral_awareness.py`
  killed externally at ~57% (no summary; a few unnamed F/E progress markers were
  observed before the kill — unattributed: sibling-lane pytest contention on this
  shared tree, dozens of concurrent python processes; the 09-27 close-out itself
  registered 31 pre-existing failures across 17 files, so unnamed markers prove
  nothing either way); (c) started ~06:08 EDT, same command redirected directly to a
  log: truncated at 38% (last write 06:23:38 EDT) with an unreliable exit code.
  Census instrument for scale only:
  `pytest --collect-only -q` → **3,089 tests collected, 1 error** (the UU file), vs the
  AGENTS.md 2026-09-27 census of 2,303/352 — the tree grew ~786 collected via sibling
  lanes landing test files (test_innkeeper.py, test_field_flow.py, test_rollup_delta.py,
  test_ldt_train.py, test_percolator_z15.py, test_section_stream.py among the untracked),
  not via LW6 alone (+1 file, +17 collected). No count here differences two instruments
  or two moments. Full-suite green is the standing pre-push gate's call, on a quiet tree.
