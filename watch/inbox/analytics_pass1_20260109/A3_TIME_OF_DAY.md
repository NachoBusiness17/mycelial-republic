# A3 TIME OF DAY vs OUTCOME - analytics pass 1

Lane A3. Read-only joins over three instruments, .venv python, moment 2026-10-08 session (EDT).

## Instruments + moments

- LEDGER: memory/burns/LEDGER.jsonl, 705 rows, ts 2026-09-25T10:05:50Z -> 2026-09-28T19:30:00Z (one burn wave, 4 dates), mtime 2026-10-07 08:09 local
- USAGE: memory/runs/hermes_burn/usage.jsonl, 3038 rows, ts 2026-10-01T13:11:41Z -> 2026-10-07T09:21:35Z, mtime 2026-10-07 05:21 local; total $94.74, ok 76.1%
- TRAILS: dashboard/static/trails/research.jsonl 3965 rows + day_work.jsonl 2683 rows, 2026-09-04 -> 2026-10-09T03:2xZ, mtime 2026-10-08 23:22 (still appending; counts are snapshots)
- ET = UTC-4 (EDT) across the entire span (DST ends 2026-11-02), so ET hour = UTC hour minus 4

## Hour-of-day vs outcome (USAGE, hourUTC; ET in parens)

- ok-rate best: 07Z (03ET) 97.1% (n=105); worst: 20Z (16ET) 34.8%, then 19Z (15ET) 53.1% and 22Z (18ET) 53.6%
- cost peak: 19Z (15ET) $15.56 of $94.74; single worst hour-date: 2026-10-01 19Z, 92 calls, $14.36, ok 40.2%
- the 19-20Z crater is a CLASS: both heavy dates crater there (10-01 20Z ok 35.5%, 10-03 20Z ok 34.5%), not one bad afternoon
- 08Z (04ET) spike: n=504 (498 on 10-04 alone = the night-shift batch), ok 71.2%, fail-cost only $0.04
- paid dispatch volume lives 04ET-18ET; 19ET-20ET is nearly dark (n=2, n=0) - the operator's evening has almost no paid calls at all
- LEDGER landing field: 705/705 rows carry a landing path, so landing-rate does not discriminate by hour; verdict class does (below)

## Verdict quality by hour (LEDGER, hourUTC)

- steals (210/705) are a night-ET shape: 01Z (21ET) 16/18 rows steal, 02Z 7/13, 04-06Z ~6/7-6/8, 10Z 15/17; afternoon 20Z (16ET) only 6/114 (5.3%) with 91 landed - volume hour, not steal hour
- steals at 00-02Z span all three later wave dates (09-26/27/28), so the night-steal shape is not a single-date artifact; but 20Z's 114 rows are 111 from 09-26, and the whole ledger is one wave whose opening barrage (09-25 10:05Z) was steal-shaped - hour and wave-phase are confounded, single-wave instrument
- vacuous (8 rows): 6 land 12-14Z (08-10 ET morning), 2 land 00-02Z; slugs: free-resource-landscape x3, world-models-multi-agent, stego-canon-pipeline, adversarial-self-probes, doctrine-owed-chase
- erratum rate peaks 17-18Z (13-14 ET): 6/30 and 7/33 rows

## Automation trails by hour

- research CYCLE_FAIL: worst 21Z and 23Z (21% each), 15Z-20Z all 16-20%; best 06Z (2%), 09Z/13Z (4%) - evening ET automation fails at roughly double the 02-08 ET rate
- day_work mean stalled lanes per CYCLE: floor 3.5 at 06-07Z (02-03 ET) and ~4.0 at 12-13Z, ceiling 6.0 (all 7 lanes) at 15-19Z (11:00-15:00 ET); STALLED: none appears in 3 of 1917 cycles

## Is the 03:00Z drain bug a class or a one-off

Verdict: CLASS, in two jackets (the one-bug law holds).

- Jacket 1, spend-absence (the rib's own shape, "hoarding funded budget while free lanes grind"):
  usage.jsonl has 03Z rows on only 2 of 7 nights (10-04: 36, 10-05: 51 - exactly the night-shift dates); 10-01/02/03/06/07 have ZERO paid calls at 03Z, and day_work CYCLE rows fire at 03Z every single night (2 per night, 35 consecutive dates, mostly reporting stalled lanes). 00-06Z paid rows exist only on 10-04 (207) and 10-05 (257).
- Jacket 2, spend-without-outcome: the empty-content class below - money left the account, nothing landed in the content channel, and the ok flag never noticed.
- Where 03Z itself is NOT anomalous: ledger 03Z rows (09-27) are 5 ordinary governance dispositions (done, applied, retired, amended, declined) and usage ok-rate at 03Z is 75.9% (mid-range). The drain is an absence pattern, not an outcome crater; the outcome craters live at 15-16 ET.

## Which hours produce steals vs vacuous vs empty-content

- steals: night ET, 21:00-06:00 ET (see LEDGER table above)
- vacuous verdicts: 08-10 ET morning (12-14Z)
- empty-content (channel = "reasoning (content channel empty)"): 82 rows, ALL ok=true, $28.75 = 30.4% of total spend; 77/82 on 2026-10-01; hours 18-21Z (14-17 ET) hold 69/82; opus-5.5 carries 62
- refused (89, all 2026-10-01): 18Z 14, 19Z 55, 20Z 20 - the 10-01 15-16 ET refusal storm
- content_filter (216 rows, $0.94, cheap): nights of 10-04 (151) + 10-05 (65), hours 01-06Z plus a 14Z pocket (66 on 10-04)
- finish_reason null + not ok (421 rows, $0.10): 411 have completion_tokens 0 - free transport-class empties, concentrated 10-03 (233) and 10-04 (177), worst hours 08Z and 20Z

## Strange findings (datum + join + confidence + falsifier)

1. DATUM: 82 empty-content rows are ALL ok=true and carry $28.75 (30.4% of the ledger's $94.74); the single most expensive call in the file ($1.72, T1W1_stranger_shared_surface, 10-01 19:09Z, opus-5.5) is one of them. JOIN: usage.jsonl channel field vs ok vs cost_usd, grouped by hour; 21Z on 10-01 posts ok=100% while 14 of its rows bought no content channel. CONFIDENCE: high (byte-backed in one file). FALSIFIER: find the consumer of the reasoning dump - if the harness harvests reasoning_tokens downstream (only 2 rows say "raw reasoning banked"), the money was not lost and ok=true is honest.
2. DATUM: the 15-16 ET (19-20Z) crater repeats on both heavy dates (ok 34.5-40.2% vs ledger-wide 76.1%) and hosts every refusal in the file plus the priciest hour. JOIN: usage ok-by-hour x date; refused x hour x date; cost x hour. CONFIDENCE: high for the two dates, medium for "afternoon is structurally bad" (only two afternoon-heavy dates exist). FALSIFIER: a third heavy afternoon at ok above 70% kills the class reading.
3. DATUM: paid calls exist at 03Z on only 2 of 7 nights while automation cycles fire there every night for 35 nights - the drain-bug falsifier text ("zero paid calls while free lanes grind") is satisfied on 5 of 7 nights post-cure. JOIN: usage 03Z rows by date x day_work 03Z CYCLE count by date. CONFIDENCE: medium (usage.jsonl cannot show whether judgment-class work was actually queued on the silent nights). FALSIFIER: night-shift receipts for those five dates showing judgment ran on free lanes by design, or evidence no judgment work existed.
4. DATUM: steals are nocturnal (21-06 ET, 01Z at 89% steal share) while the peak-volume hour 20Z is 5% steals. JOIN: LEDGER verdict x hour x date. CONFIDENCE: medium - single burn wave, hour confounded with wave phase (opening barrage was steals; 20Z volume is 111/114 from one date, 09-26). FALSIFIER: a second multi-week ledger where afternoon hours steal at parity.
5. DATUM: automation health inverts the paid-crater hours - trails are healthiest 02-03 ET (2% CYCLE_FAIL, 3.5 stalled lanes) exactly when paid spend is near zero, and worst 11:00-15:00 ET (6.0 stalled lanes, 16-20% fail) overlapping the paid ok-crater. JOIN: research/day_work hour tables vs usage hour table. CONFIDENCE: high for the trail side, medium for the coupling (no causal join available). FALSIFIER: the 15-19Z stall ceiling is a scheduler duty-cycle artifact (day lanes scheduled there by design) rather than degradation - check lane_runner schedules before acting on it.

## Caveats

- LEDGER hour-of-day rides one 4-date burn wave; wave phase and hour are confounded everywhere in that section
- usage.jsonl covers 7 dates only and 10-02/10-06 have near-zero rows; date-level conclusions outrank hour-level ones where n is thin (23Z n=2)
- trails were still appending at read moment; day_work STALLED text is scheduler prose, not an independent outcome instrument
