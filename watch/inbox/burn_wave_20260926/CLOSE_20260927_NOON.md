# Flash-lane burn close receipt — 2026-09-27 noon close (fired 18:07 local -0400)

Close gate: dispatcher fire at 2026-09-27 18:07 local, past the noon close line.
No dispatch this fire. Numbers below are byte-derived: the landed array in
memory/burns/BURN_WAVE_STATE.json was re-derived from the LANDED RULE
(a dispensed B2-NN is landed iff B2_NN_*.md exists on disk, regex B2_(\d+)_ so
zero-padded single-digit lanes count), not from lane self-report.

## Final numbers

- 488 unique B2 lane ids dispensed (STATE dispensed array, deduped; 506 raw
  rows including known double-claims from the concurrent self-feed era)
- 402 LANDED by rule: 5-section receipts on disk in watch/inbox/burn_wave_20260926/
- 86 outstanding (dispensed, no receipt on disk): window-spent 1302 deaths and
  the self-fed B2-507..553 tail; carried to the reset-day window
- memory/burns/LEDGER.jsonl: 642 rows appended across the burn

## Verdict tally (642 ledger rows, exact field values)

- LANDED family: 352 (310 LANDED + 19 landed + 11 LANDED-* variants + LANDING,
  LANDED bounded, LANDED with incident/owed-alarm disclosures)
- steal: 161 (self-feed bookkeeping rows, not verdicts)
- green: 16, built: 6, done: 3, PROVEN/CONFIRMED/resolved/HOLDS/applied/
  adopted/backfilled/accept/wired: 9
- corrections and errata: 26 (every one names the prior row it supersedes)
- OWED family: 16 (each names its gate: operator, charter, Sep-29, W40, dormant)
- BLOCKED family: 2, vacuous: 2, misc singletons: the rest

## Token estimate from ledger rows

The ledger schema (ts, slug, verdict, landing, one_line) carries no token
field; estimate is derived from the lane contract, not claimed as measured.
402 landed lanes each contracted 1M+ tokens of real reading and verification:
floor approximately 400M tokens on the flash-lane receipts alone. Prior
session estimate across all surfaces stood near 1.1B witnessed; this receipt
attests only the 400M+ receipt-backed floor.

## Peak and envelope experiment

- Peak measured: 109.4M tok/h at width 10
- Width-24 experiment: 8 surfaced 1302 deaths (holds log 2026-09-26T21:45Z
  through 2026-09-27T07:02Z), ceiling confirmed depth-dependent, amendment
  recorded in BURN_WAVE_STATE.json holds
- Swarm: 12 deep lanes, 9 completed full slices, 3 died to 1302 and requeued

## What carries into the reset-day window (opens this afternoon)

- 86 outstanding dispensed briefs (ids in BURN_WAVE_STATE.json outstanding)
- Self-fed tail B2-507..553 unchecked in QUEUE.md
- the-50 pattern fullsend on fresh quota per watch/inbox/BURN_PLAN_20260927.md,
  SEED-RIB at the head of the line
- Five operator GOs pending: Drive bridge, Cerebras card (Oct 3), width-15
  probe, Grok packet refire, weekly pack cron

## The burn's one-line legacy

488 lanes dispensed, 402 landed with receipts on disk, every correction and
erratum filed by name, and the envelope law now rests on measured deaths.
