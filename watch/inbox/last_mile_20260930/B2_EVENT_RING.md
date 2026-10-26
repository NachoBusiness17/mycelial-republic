# B2 — the event ring: writer side of AJ4's blindness (2026-09-30)

Lane: B2 (last_mile wave). Ownership held: `roblox_to_godot/scripts/game.gd`
(writer, where grep found the cap), `roblox_to_godot/scripts/hud.gd` (reader
mirror), `tests/test_event_ring.py`, one out-of-lane whitespace repair named
below, this receipt. **No commit.**

## Root cause and where it actually lives

Mission asked for `server/world.py` "or wherever last_events/the 6-cap
lives — grep it". Grep verdict: **the server has no cap anywhere.**
`server/world.py tick()` builds the full event list and chains ALL of it into
the tick row (`"events": events`, line ~285); `server/server.py pump_once`
broadcasts that payload raw; `server/innkeeper.py` relays the full list. The
6-cap was exclusively client-side: `game.gd _on_water_event`
(`while last_events.size() > 6: pop_front()`), the writer of the ephemeral
display feed. So the writer fix lands in game.gd; **world.py is untouched —
the hash-chained replay log and the determinism law are unaffected by
construction** (the ring is display state only; the `water_event` signal
fan-out from AJ4 stays exactly-once).

## What changed

1. **Writer (game.gd)**: `last_events` is a 64-slot drop-oldest ring —
   `const EVENT_RING_CAP := 64`, `var event_dropped := 0`; `_on_water_event`
   appends, pops the OLDEST past 64, and counts every drop. A tick carrying
   20+ strings (say bursts + physics lines) no longer decapitates itself
   before a feed-polling reader runs. Fix comments carry cause + receipt.
2. **Reader mirror (hud.gd)**: the two feed consumers (`_scan_greeting`
   rescan, `_draw_events` strip) already scan the full array — the ring
   growth is what makes their bursts visible (greeting window widens 6 -> 64
   by design). `_draw_events` now surfaces the tally: `"+N dropped"` is
   appended to the strip whenever `event_dropped > 0` — overflow is shown,
   never silent. Current-semantics comments updated ("6-event feed" -> ring).
3. **`tests/test_event_ring.py`** (6 tests): five structural laws (cap is 64
   not 6; drop-oldest shape pops AND tallies inside the while; no live
   `size() > 6` trim on code lines; hud reads + renders `event_dropped`;
   signal fan-out untouched) plus one EXECUTED law that drives the real
   game.gd headless (Godot 4.3 console exe, X8/W3 create-run-delete probe)
   whenever `tools/godot/` holds the binary, skip-with-reason otherwise.

## Verification (byte-run 2026-09-30, Godot 4.3 headless, final bytes)

- Probe (throwaway scene, deleted after): `B2_RING_PASS burst20=20/20
  ring64=64 dropped=6 head=burst6 tail=more49` — a 20-event burst in one
  tick is fully visible to a reader polling `last_events` the way hud does;
  70 pushed -> ring holds the newest 64, exactly 6 dropped, drop-OLDEST
  (head `burst 6`, i.e. burst 0-5 gone), newest kept.
- `pytest tests/test_event_ring.py` -> **6 passed** (three consecutive runs),
  including the executed headless burst test; gd-touching neighbors
  (`test_motion_rows.py test_flock_positive.py test_mountain_units.py`) ->
  91 passed.
- Full-suite numbers: filed below under Census.

## Out-of-lane repair (named, not smuggled)

- `roblox_to_godot/systems/water_graph.gd` lines 64-71 (sibling B1's
  `fracture_threshold` doc + return): 8 lines were TAB-indented inside a
  space-indented file — a hard GDScript parse error ("Used tab character for
  indentation", `water_graph.gd:63`) that killed ANY runtime `load()` of
  game.gd (it preloads water_graph.gd), i.e. every headless probe lane was
  dead on the working tree. Repair is whitespace-only (tab -> 4 spaces),
  zero semantic bytes changed. Evidence: `-s` diag load failed pre-repair,
  loads post-repair. Note: the plain main-scene smoke stays banner-only
  either way (scene-load path does not surface the parse error) — do not
  read a clean smoke as a parseable tree.

## Handoff notes (not this lane's ownership)

- `roblox_to_godot/network/net_client.gd` (sibling B3 netcode, untracked,
  in progress) fails compile: "The member `_buf` already exists in parent
  class res://scripts/net_client.gd" (`network/net_client.gd:57`). It prints
  two SCRIPT ERROR lines into any headless run of the current tree; the
  B2 probe asserts on its own PASS/FAIL markers and is robust to it, but the
  next smoke lane will want it fixed.
- Sibling working-tree edits (AJ4's four files, B1 fracture retune, server/
  protocol lanes) share the uncommitted diff; nothing here commits.

## Census (instrument + moment named per the denominator law)

Full-suite executed run, 2026-09-30, `pytest -q --timeout=180` (54:43 wall):

**16 failed, 3679 passed, 5 skipped, 3 deselected, 3 errors.**

- **3 deselected (environment wedges, named):** the only three tests that
  really invoke `doctor.examine()` — `test_doctor_provider_endpoints.py::
  test_wired_into_examine`, `test_doctor_scheduled_tasks.py::
  test_wired_into_examine`, `test_env_redirect_tripwire.py::
  test_doctor_examine_aggregates_redirect_warnings` — hang indefinitely on
  this box (a subprocess inside `check_tracked_secrets` never returns;
  confirmed standalone with `--timeout=25`, same wedge). Without the
  deselect they abort the whole run three times over (the thread-method
  timeout kills the process, not the test). Not this lane's code.
- **16 failures + 3 errors are all outside this lane's files.** Cluster:
  `test_server_persist` x5 (snapshot-vs-replay ValueError in sibling-owned
  server/persistence lanes), `test_healthz_status` x3 errors (AttributeError,
  sibling refactor), and one each in census_drift_patrol, container_setup,
  gods_number, headless_law, hook_prefix_pairing, k8s_water, oral_dedupe,
  organ_map x2, reconstruct, shared_surface_events. Diagnosed far enough to
  place them on sibling surfaces; this lane's delta (game.gd, hud.gd,
  water_graph.gd whitespace, tests/test_event_ring.py) touches none of them,
  and its own 6 tests + 91 gd-neighbor tests pass.
- Executed-vs-collected denominators named: this is an EXECUTED outcome sum
  (3,703 items run). The AGENTS census bullet's collected claim (2,303 /
  352 files, 2026-09-27) is far behind this tree — ~1,400 tests landed in
  sibling lanes since; refreshing that carrier is the census patrol's /
  operator's ritual (B2-246), not this lane's.

## Refire verification (2026-09-30 ~16:47-18:45 EDT, independent session)

Refired while the original close-out was landing. Every law re-verified on
final bytes, different moment than the runs above (denominator law):

- `pytest tests/test_event_ring.py` -> **6 passed**, incl. the executed
  headless law (no skip): probe printed `B2_RING_PASS burst20=20/20 ring=64
  dropped=6` — 20 events in one tick, reader sees 20+; drop-OLDEST holds.
- gd neighbors -> **91 passed**. `server/world.py` clean vs HEAD, no
  server-side cap (full read + grep); replay log untouched.
- water_graph.gd tab repair holding; B3's `_buf` shadow fixed in committed
  bytes (`network/net_client.gd:57`, renamed `_snap_buf`).
- Independent full-suite census (instrument `pytest -q --timeout=300
  --timeout-method=thread`, 17:44-18:38 EDT, SAME three doctor real-examine
  tests deselected by name — one bare `git grep <value> HEAD` measured 26s
  over the 14 GB object store, one real `examine()` measured 20m41s wall):
  **15 failed, 3680 passed, 5 skipped, 3 deselected, 3 errors in 54:19** —
  one failure fewer than the close-out's run above, same clusters
  (server_persist snapshot-replay ValueError at persistence.py:209,
  healthz `server.app` AttributeError; both reproduce in isolation on
  committed bytes — sibling-lane debt, not B2). No red touches this lane's
  files. `tests/test_event_ring.py` remains untracked by design.

## Commit note (this lane committed nothing)

This lane made no commit, per mission. Mid-run a sibling lane's tree sweep
(88ed0d729 "B7 healthcheck..." through e00fe8ffc, 2026-09-30 ~18:09) carried
the then-current working tree into history — including this lane's game.gd /
hud.gd / water_graph.gd edits and the first draft of this receipt (verified:
`git show HEAD:...game.gd` contains EVENT_RING_CAP). Still uncommitted on the
tree: `tests/test_event_ring.py` (untracked) and this receipt's census
section (the M). Named so nobody mistakes the sweep for this lane pushing.

