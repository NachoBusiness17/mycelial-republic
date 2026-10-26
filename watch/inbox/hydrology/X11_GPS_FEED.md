# X11 -- GPS feed: world ticks eat the meter's first production meal (2026-09-29/30)

The tie-it-all move's second leg. Leg 1 (`mag/gwap_to_gps.py`, Mickey17
Wave 1) built the fail-closed gwap -> gps bridge but only synthetic demo
sessions ever crossed it. Leg 2 (this) wires the RETURN leg: the estate's
own world server now feeds it.

## Landed

- `server/verdict_feed.py` (new) -- `VerdictFeed.feed_tick()`, called after
  each `MountainWorld.tick()`:
  - mints one gwap payload per tick: `scene_id` = the tick's own gwap
    session id `{session_id}.t{tick:04d}` (one session per tick, so a
    re-feed can never double-count a verdict); `claims` = the tick's action
    rows through the closed `gwap_mud` mapping (`join`->move on the board
    tile projection, `boil`/`valve`->attack, `tag`->kill; physics narration
    mints no claims -- no author); `verdict` = `VERIFIED_AGREE` iff
    `world.verify_log()` holds, else the engine itself returns `DISPUTE`
    (the report side files one disjoint "chain broke verify" claim; no
    verdict is ever overridden post-build).
  - drives it through `feed_session` into the gps ledger under
    model_id `mountain-world-v0`, task_shape `world-tick`; evidence =
    gwap `row_sha256`, and the payload's `replay_tape_ref.sha256` is the
    world tick row's own sha (auditor walks gps row -> gwap row -> world
    tick, offline).
  - collusion-proof ordering (documented proof, plus a `VERDICT_MISMATCH`
    refusal guarding it): report claims = reverse(dedup(intent)); a
    duplicate-free palindrome of length >= 2 cannot exist, so the
    fingerprint can never fire and a verified tick always scores 1.0.
  - fail-closed: `EMPTY_LOG` / `NOT_A_TICK_ROW` / `UNKNOWN_WORLD_VERB` /
    `UNKNOWN_NODE` / `TICK_SESSION_EXISTS` (one verdict per tick,
    structural); idle ticks skip (`IDLE_TICK`), scoring nothing.
- `tests/test_verdict_feed.py` (new) -- 13 tests.

## Tests (instrument: `.venv\Scripts\python.exe -m pytest -q`, 2026-09-30)

- `tests/test_verdict_feed.py`: 13 passed.
- Neighborhood rerun (`test_verdict_feed + test_server_v0 + test_gwap_payload
  + test_gwap_mud + test_gwap_to_gps + tools/gps_mcp/test_gps_mcp.py`):
  112 passed.
- Laws proven: played session -> 4 gps rows under
  `(mountain-world-v0, world-tick)` at pass_rate 1.0; tampered world chain ->
  `DISPUTE`, verdict 0 row, pass_rate 2/3, never a minted `VERIFIED_AGREE`;
  tampered gwap ledger file -> bridge refuses `BROKEN_CHAIN`, gps untouched
  by that walk; duplicate-claim tick (the palindrome case) still verifies;
  idle tick / double feed / unknown verb / unprojected node all refuse.

## Demo (real, no live server: `python -m server.verdict_feed`, 2026-09-30)

Five `MountainWorld.tick()` calls (boil spring, tag hollow, valve p_bypass,
join terrace, then one pure-physics tick) against the PRODUCTION ledger
`tools/gps_mcp/gps_ledger.db3`:

- ticks 1-4: `VERIFIED_AGREE`, fed=1 each; tick 5: `IDLE_TICK`, fed=0.
- gps verdict_log rows: 6 -> 10 total; `(mountain-world-v0, world-tick)`
  0 -> 4, all verdict 1, each carrying a byte-backed evidence_hash.
- capability row minted:
  `{model_id: mountain-world-v0, task_shape: world-tick, pass_rate: 1.0,
  sample_size: 4}`.

The meter has eaten its first production meal. Next debt: `server/server.py`
does not call the feed yet (file ownership kept this leg to verdict_feed +
tests); wiring the server loop is one line at the broadcast site.
