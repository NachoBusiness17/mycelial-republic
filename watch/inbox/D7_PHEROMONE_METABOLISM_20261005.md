# D7 LANDED - GPS capability metabolism (2026-10-05 night shift)

Door: D7-pheromone-metabolism (eleven-doors ledger) - "alpha-decay +
dispute-streak slashing + drift-patrol-keyed reset on the GPS capability
table". Substrate the door verified: verdict_log 593 append-only rows
(now 703), capability 30 rows (the whole mutation surface), momentum
floor already law at ledger.py:433-443, all stored rows tainted-era (max
ts 2026-10-04T09:36:09Z) so decay is curative now, promoted with NO
backfill wait.

## What landed

**tools/gps_mcp/metabolism.py** - read-only over the same sqlite file;
the stored running mean stays the audit surface, the module computes the
ROUTING-FACING effective rate:

- alpha-decay: decayed = 0.5 + (stored - 0.5) * exp(-age_days/14).
  Decay measures ABSENCE of fresh evidence, never merit (the Z15
  decay-measures-absence gap this cures operationally).
- dispute-streak slashing: effective *= 0.85 ** min(fail_streak, 3) -
  a live dispute streak carries information the lifetime mean dilutes;
  the cap keeps a 3-fail night from nuking a 100-sample row.
- drift-patrol-keyed epoch reset: reset_epoch() stamps a marker
  (explicit act, never automatic); rows last measured BEFORE the marker
  collapse to the 0.5 prior until re-measured. load_epoch() treats a
  corrupt marker as no marker (fail-open to no-reset, never a silent
  wipe).
- CLI: `python tools/gps_mcp/metabolism.py [--task-shape ...]
  [--epoch none|PATH] [--set-epoch REASON|TS] [--json]`.

**tests/test_gps_metabolism_20261005.py** - 7 tests (fresh row
unchanged, 2-tau decay math, streak slash + cap, pass breaks streak,
epoch collapses pre-marker rows only, epoch roundtrip + corrupt-marker
ignore, tau constant pinned against silent retune). First run failed 2
on my own fixture math (nested approx; a 12h-old row decays slightly) -
the module was right both times. Coverage suite still 10/10; combined
17 passed RC=0; ratchet PASS.

## Production proof (no epoch stamped)

Fresh arena rows (age 0.0d) keep their rates. The 4.4-day-stale rows
(the 09-30/10-01 waves, untouched since) decay 1.000 -> 0.866. Live
streaks bite where the mean dilutes: glm-5.3-prime adversarial-review
stored 0.435 with a 7-fail streak -> effective 0.278; haiku
arena-agreement stored 0.047 with a 10-fail streak -> effective 0.030.
The zero-tier (grok-4.3 / qwen-4.7-flash / gemini-flash-safeguard,
stored 0.000) sits at the floor.

## Epoch demo (curative view, marker NOT stamped)

With a demo marker at 2026-10-04T12:00:00Z (the gps-dedupe cure moment;
the .bak-20261004-gpsdedupe backup names it): 26/30 rows collapse to
the 0.5 prior as tainted-era; the 4 survivors are exactly the
arena-agreement rows measured TODAY (post-marker). The marker is an
operator/patrol act by design - this receipt demonstrates it works and
leaves the stamping decision to the operator (stamping it now would
flatten every non-arena routing row to uninformative until re-measured;
with the mates parked and arena the only live feeder, that is the
operator's call, not the night shift's).

## What it changes

The router still reads stored pass_rate (wiring the router to effective
rates is a separate act - the door asked for the metabolism, not the
rewire). When wired: stale evidence stops routing dollars, dispute
streaks demote live, and any named drift event can mint a fresh epoch
without touching one stored byte.

Banked by GLM-5.3 window (night shift), 2026-10-05.
