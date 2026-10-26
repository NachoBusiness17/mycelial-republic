# D10 LANDED - the beat-indexed ractive: capture + banking (2026-10-05)

Door: D10-weld-ractive - "beat-indexed ractive (capture + banking loop);
input + playback halves exist and tested (MAG_DANCE_V02 ESTATE_INDEX row
21376); banking half zero wiring (zero beat/damage hits in arena_gwap.py
+ gwap_payload.py); build capture+banking, read actor_payloads first, no
quoted hours before the instrument runs".

## The weld

The run's ruled transcript events ARE the beat grid: every row with a
roll_committed is one beat in transcript order, strength = roll_value
(the dice roll is the beat's strength - the dice-law carrier welded to
the damage map), downbeat = k%4==0 (the damage-map 4/4 measure).
tools/beat_map.damage_map decides zone/hp/imp deterministically - no
RNG, golden-angle impulses, rerun-byte-identical.

**tools/arena_beats.py** (the ractive module): beat_grid(rows) capture +
table(run_dir) instrument + CLI. Live readout on this morning's run
dnd0_20261005T060250Z (9 beats, 49 hp banked; dm's opening DC check =
beat 0, DOWN, head, hp 11; warden's nat-20 audits at strength 9 after
the clip).

**tools/arena_gwap.py v4-beat** (the banking half): every dungeon claim's
commit qualifier gains beat=<k> zone=<z> hp=<n> on BOTH sides (intent +
report), derived from the SAME post-roll record exactly like commit=
itself - so the agreement arithmetic is untouched, proven by
test_verdict_byte_stable_vs_v3 (v4 vs beat-lookup-emptied payloads give
identical decide_verdict on every actor). Tavern rows carry no
roll_committed: no beats, honestly unmeasured, never a guessed grid.
Engine version bumped arena-v3-independent-cop -> arena-v4-beat (the
cop suite's version pin updated with the reason).

## The ratchet bite (and the split it forced)

The weld pushed arena_gwap to 450 lines - the pre-push ratchet flagged
file-too-long (>400) as NEW debt. The fix was the right architecture,
not a fence shave: the FEED machinery (_quarantined_run_dirs,
_original_run_name, _quarantine_scene_map, feed_scene_map - the
quarantine-orphan law) moved to **tools/arena_feed.py** with its
evidence-bearing docstrings intact, lazy-imported to avoid the cycle,
re-exported on arena_gwap for existing callers (the cop suite's
monkeypatch home updated to the new PLAY_DIR). arena_gwap lands at 357
lines; ratchet PASS.

## Evidence

- tests/test_arena_beat_weld_20261005.py: 6 tests (grid order + the
  damage contract incl. the CLIP law - my own first draft forgot roll 14
  clips to strength 9 on offbeats; beat fields on both sides + qualifier
  identity; the v3/v4 verdict-stability falsifier; tavern no-beats; CLI
  table).
- The cop suite (9) + full arena/gwap sweep: 99 passed, RC captured.
- Live instrument: the --beats table reads real runs; "no quoted hours
  before the instrument runs" honored - the instrument IS the deliverable,
  hours get measured when the ractive consumes them.

Banked by GLM-5.3 window, 2026-10-05 (compute-grind block).
