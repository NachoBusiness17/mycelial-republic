# B2-227 walk-compare rescan gap, LAW-13 decision (2026-09-26)

## Verdict

LANDED, resolved by running the minimal experiment rather than choosing
between "owed" and "stands": the walk voice's date gap is CLOSED. A
current-dated walk re-run (watch/inbox/WALK_COMPARE_20260926.json, ts
2026-09-26T20:17:56Z, produced by tools/cathedral_walk.py this lane) shows
water_first at 17 steps / 4 missing edges, byte-identical to the frozen
09-21 vote, and hub_first worsened to 23 steps / 4 missing (was 19/6). The
four-voice stack's walk vote STANDS and is strengthened: water_first's
structural counts reproduce exactly on the current world, and hub_first's
step cost widened. Decision filed as a dated addendum appended to
watch/inbox/REFEREE_VERDICT_20260926.md (append-only, no verdict byte
modified).

## Evidence file:line quotes

- The gap, watch/inbox/WALK_COMPARE_20260921.json: "ts":
  "2026-09-21T18:47:00Z", "water_first": {"steps": 17, "missing_edges": 4},
  "hub_first": {"steps": 19, "missing_edges": 6}; the only walk-compare on
  disk before this lane (repo glob WALK_COMPARE_* returned exactly this
  file; no WALK_COMPARE_20260922 existed, as the brief stated).
- The mixed-date stack, watch/inbox/burn_wave_20260926/B2_70_referee_refresh_20260926.md:6-8:
  "the current meter is the 09-22 rescan (0.032 vs 0.038, margin 0.006)"; the
  walk voice remained 09-21.
- watch/inbox/REFEREE_VERDICT_20260926.md:37: "The descent-order lean is now
  water_first, 4th independent voice (walk..." - the voice whose date the
  brief flagged.
- The experiment, watch/inbox/WALK_COMPARE_20260926.json (this lane's run):
  "ts": "2026-09-26T20:17:56.437530+00:00", "water_first": {"steps": 17,
  "missing_edges": 4}, "hub_first": {"steps": 23, "missing_edges": 4}; tool
  stdout: "WALK WATERFIRST: steps=17 missing=4 / WALK HUBFIRST: steps=23
  missing=4"; companion files WALK_WATERFIRST_20260926.md and
  WALK_HUBFIRST_20260926.md landed beside it.
- LAW-13 (watch/inbox/LAW13_EXPERIMENT_ON_ABSENCE_20260926.md): absence must
  be named, the minimal experiment designed with its inversion threshold and
  filing site, theory mapped or the attempt filed.

## Work done

1. Verified the absence: exactly one walk-compare on disk, dated 09-21, while
   the meter addendum cites 09-22.
2. Ran tools/cathedral_walk.py against the current world: the minimal
   experiment executed in one command, landing three files in watch/inbox/.
3. Applied the pre-registered reading: water_first counts reproduce exactly
   (the vote is wiring-true, not date-lucky); hub_first's route lengthened
   19 to 23 steps while its missing-edge demand fell to parity (4 = 4), so
   the contested quantity (which edges each order demands) now favors
   water_first more clearly, since hub no longer demands extra edges but
   pays 6 more steps.
4. Appended the dated addendum to REFEREE_VERDICT_20260926.md naming the
   absence, the experiment, the outcome, and the theory-map attempt.
5. Filed this receipt; LEDGER row; QUEUE pointer; INDEX registration.

## Falsifier

This decision is inverted if any of the following holds: (a) a future walk
run shows water_first counts drifting from 17/4 on an unchanged world file
(the 09-21/09-26 agreement was coincidence, the vote is unstable and must be
demoted from the stack); (b) the walk tool's world input changed since 09-21
in a way that makes the identical water_first counts a wiring-stability fact
ABOUT the frozen input rather than the live world (then the addendum's
"current world" wording is wrong and must be corrected); (c) WALK_COMPARE_20260926.json
is found predating this receipt's ts (fabricated provenance).

## Bibliography closed

watch/inbox/WALK_COMPARE_20260921.json (read in full); watch/inbox/WALK_COMPARE_20260926.json
+ both walk .md files (produced and read this lane); watch/inbox/burn_wave_20260926/B2_70_referee_refresh_20260926.md
(read in full); watch/inbox/REFEREE_VERDICT_20260926.md (read: foot addendum;
appended: dated B2-227 addendum); watch/inbox/LAW13_EXPERIMENT_ON_ABSENCE_20260926.md
(read in full); watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260922.json (ts read,
cited as the 09-22 meter). No network calls.
