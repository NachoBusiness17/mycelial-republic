# A2 novelty rate - fresh_failure_mode over time - analytics pass 1

- Seat: lane A2, read-only over small files. Written 2026-10-08 ~23:40 local.
- Instruments: memory/burns/LEDGER.jsonl (705 rows, zero bad lines, parsed with .venv\Scripts\python.exe json.dumps-compatible json.loads, read moment 2026-10-08 ~23:30 local; file mtime 2026-10-07 08:09); memory/burns/MANIFEST.json (topic roster, mtime 2026-09-26); memory/burns/LEDGER.lock.log (write-activity trace).
- Coverage: ts 2026-09-25T10:05:50Z through 2026-09-28T19:30:00Z, four days. ISO week 39 holds 687 rows, week 40 holds 18, so a weekly view is degenerate; daily buckets are reported instead.

## KPI: fresh failure mode rate over time

- Field is boolean in 269 of 705 rows (38.2 percent), missing in 433, a string in 3. All rates below use boolean rows only.
- Daily rate, all boolean rows: 09-25 = 91.3 (21/23), 09-26 = 66.3 (57/86), 09-27 = 25.2 (26/103), 09-28 = 10.5 (6/57).
- Manifest 15 topics only: 91.3, 70.6, 27.5, 10.5. Identical collapse, so it is not contamination from non-fire rows.
- Weekly wrap for the record: week 39 = 49.1 (104/212), week 40 = 10.5 (6/57), whole ledger 40.9 (110/269).

## Denominator integrity (two populations share one file)

- The 433 missing-field rows are 423 B2-prefixed slugs plus 10 strays; 346 carry verdict "landed". That is the B2 work-tracking population, which never carried the field: it must stay out of the KPI denominator rather than silently count as not-fresh.
- Three rows hold prose inside the boolean field (LEDGER.jsonl lines 36, 46, 50, all 09-26): width-3 folklore scope fix, 1302 ceiling at width 15-16, provider denominator withdrawal. Strict boolean parsing drops three genuine discoveries from the numerator; a schema note field (fresh_failure_mode_note) exists in exactly 1 of 705 rows.

## Topics: genuinely new failure modes vs re-learning

- Top novelty producers (fresh true / false): judge-lane-spec 9/1, queue-field 9/2, stego-canon-pipeline 10/9, free-resource-landscape 13/22, world-models-multi-agent 8/11, steering-theory 6/5, prompt-uplift-lane 5/2.
- Top re-learners: doctrine-owed-chase 29/9, middle-path-doctrine 24/6, free-resource-landscape 22/13, third-way-game 12/5.
- The two doctrine topics alone hold 53 of 159 false rows, 33 percent of all re-learning in the ledger.
- Exactly one slug is all-stale with 2+ fires (atlas-fix-queue, 0/4). No slug is all-fresh with 2+ fires: even judge-lane-spec re-learned once.

## Correlation with verdict class (boolean rows)

- steal 46.8 (94/201), vacuous 50.0 (4/8), landed 41.7 (5/12), green 14.3 (3/21), erratum 0 (0/2), correction 0 (0/2).
- Join: green means confirmed-working, so a low green rate is semantically expected; the surprise runs the other way (finding F3).
- Caveat: the verdict field holds 90+ distinct strings, many whole sentences (classified here by prefix fold), so class correlation inherits that noise.

## Trend: is discovery accelerating

- No. Fresh rate fell 91.3 to 10.5 in three days (8.7x) while boolean volume held at 57 to 103 rows per day: true counts fell 21 to 6 while false counts grew 2 to 77 then 51. The fleet kept firing and stopped finding.
- The collapse is fleet-wide, not one pathological topic: excluding doctrine-owed-chase entirely, 09-27 reads 24/96 = 25.0 and 09-28 reads 3/32 = 9.4.
- Day-one base-rate caveat: first contact with a topic is fresh by construction, so part of the 91.3 is novelty of first look, not discovery skill.
- Past 09-28 the question is unmeasurable on this instrument: zero October ts values exist despite continued machinery activity (finding F2).

## Strange findings (datum + join + confidence + falsifier)

- F1, the novelty collapse. Datum: daily fresh rates 91.3 / 66.3 / 25.2 / 10.5 across 09-25 to 09-28 at constant fire volume. Join: MANIFEST pat_rerank promises "fresh failure modes beat repeated ones" and solved topics demote, yet doctrine-owed-chase was fired 25 times on 09-28 alone (44 percent of that day's rows) at a 30-minute cron cadence, 22 of them fresh=false. Confidence: high (269 boolean rows; collapse survives excluding the top re-learner). Falsifier: re-score the 09-27/28 false rows against their one_lines; if a third are mislabeled repeats of laws already banked in MANIFEST self_steal_fold (19 methods), the collapse is label inflation, not discovery decay.
- F2, the instrument outlived its data. Datum: last ts-bearing row 2026-09-28T19:30Z, but LEDGER.jsonl mtime is 2026-10-07 08:09 and LEDGER.lock.log shows lock acquire/release through 2026-10-07T12:09Z; watch/inbox holds exactly one burn artifact dated after 09-28 (NIGHT_BURN_DESIGN_20261007.md) against 54 dated 09-28. Join: MANIFEST orders 24x7 fires, so 9 days of locked-but-empty activity means the novelty KPI went dark while its machinery stayed alive, and the single late artifact is a redesign doc, suggesting a rebuild was drafted instead of rows landing. Confidence: high on the gap (byte-proven), medium on intent. Falsifier: locate a successor ledger; SPOT_PATROL.jsonl also stops 09-27, and if burns continued under receipts outside the BURN_ naming law, only the ledger was abandoned, not the fires.
- F3, green and fresh at once. Datum: 3 rows are verdict green with fresh_failure_mode true (09-27 05:40Z build-fold-verify, 06:20Z b2-wave-fold, 08:40Z judge-lane-spec); each one_line confirms work closed green and simultaneously banks a new failure mode (the judge-lane row corrects a zero-emitter claim because a real V2 emitter had landed). Join: under ledger semantics green should mean nothing new was learned, so these are either the healthiest pattern in the file (verified closure that still finds novelty) or evidence the two fields are scored by different seats against different rubrics. Confidence: medium (n=3). Falsifier: read the three receipts; if the fresh flag was template-copied from the prior row, the pairing is clerical, not semantic.
- F4, minor, the boolean that became prose (lines 36, 46, 50). Join: writers hit discoveries too rich for a boolean and the schema had almost no note field (one row uses fresh_failure_mode_note). Confidence: high. Falsifier: none needed; the schema already grew the escape hatch once and these rows bypass it.

## Verdict for the KPI owner

- Discovery is decelerating hard inside the measured window and has been unmeasured for the 10 days since. The levers the data names: demote doctrine-owed-chase and middle-path-doctrine (33 percent of re-learning), split the ledger's two populations before charting any weekly KPI, and resolve the post-09-28 dark period before trusting a trend line in either direction.
