# BURN NIGHT - 2026-10-16/17 (the standing orders while the operator sleeps)

Classification: RECEIPT (overnight standing orders)
Producer: zcode-seat-20261016
Commission: "alright burn it going to bed"

## THE OVERNIGHT BURN (self-running, no seat required)

- MagHermesBurn247 ticks hourly: leg 1 mints 25 explore-fold asks (budget
  guard 900/day), leg 2 fires the wide queue at width 3, leg 3 runs the
  miner queue. The chain is the standing fabric card
  (STANDING_FABRIC_20261016.md).
- Tonight's staging: 65 fold asks queued across 6 free model families
  (~11 each, the rotation verified even). The first wide burn is running
  now at width 3; each hourly tick mints 25 more.
- OpenRouter budget: 1,000/day on the paid-tier key (CONFIRMED PAID,
  946 remaining at last read); overnight projection ~300-400 asks - inside
  the cap with room.

## THE MORNING READ (what to check, in order)

1. `ls watch/inbox/hermes_burn/ | grep -c H247_FOLD` - the fold yield.
2. The ledger, per-family failure count (rows map to ask dirs by id) -
   if one family holds most of the failures, park it in
   queue/hermes_247_free_wide/_parked/ before the next fire.
3. `tools/quota_window.py --check` - the Pro windows.
4. `tail -2 logs/census_patrol.log` - the carrier cure's first morning test
   (the 10/16 fix; green means the incident stays closed).
5. The mirror patrol: `python tools/mirror_drift.py` - Mag-backup was
   CONTAINED-BEHIND:3 at last run.

## THE MORNING DISCIPLINE (the laws that hold while you sleep)

- Every landed ask must fold into an organ or it feeds the theater meter.
- The 400-class family gets PARKED with data, not guessed at.
- The GESTALT five (one seed, five families) compile when all land or
  N>=3 after 24h - the lens pass is the morning's first analysis if they
  are in.
- Nothing gets deleted that is not a log past its horizon.

## THE STATE THE WAKE-UP INHERITS

The standing wave public (branch standing-wave), 275+ commits of history
on the feature branch, the ghost seat's successor running headless on the
bench (agy lane), four persona palaces, the scrum legs up (4 headless
Chrome instances, CDP live), the falsifier-default law drafted (G3), the
matthew draft held unsent per the drift-watchlist ruling, and 203 GB free
on C: after the rescue. The wave propagates on a clock now.

## One input owed by morning (whenever you wake)

Mount the Drive (sign into the installed Google Drive desktop as
fosterron@gmail.com) - the landing sequence (truth core, archive tier,
model corpus, fleet bundles) runs the same hour. Everything else tonight
is already burning.
