# TAVERN CURVE AUDIT (2026-10-03 corpus, filed 2026-10-04 by GO wave lane 9 tavern-refresh)

The citable home for the Hollow Crown tavern calibration curve. Folded from corpus/steal/MASTER_MICKEY17_V2.md section 9 GO item 10 (lanes a03-tavern-curve#1, a03#3, a03#5). Evidence rows: memory/runs/mickey17_v2/runs/run-0/lanes/a03-tavern-curve.json. This file supersedes the phantom-anchored wording ("p0 never, p1 r3 x2, p2 r2; Greta fuse 3/3") that reached the fold unanchored: no estate file predating the a03 audit contained that wording (a03 row 5, PHANTOM-ANCHOR finding).

Census denominator law: every count below names its instrument and moment. Two moments are used:

- FOLD MOMENT: the a03 refire moment (corpus through tavern_20261004T022300Z). The counts the GO item names (14 p1 runs, 16 Greta sessions).
- CENSUS MOMENT: 2026-10-04T08:36:45Z, one venv-python pass over all 26 tavern_*/ dirs then on disk. The hourly arena automation kept firing during this audit (082510Z, 082906Z landed pre-census; 084000Z, 084146Z, 084457Z post-census), so counts are a snapshot, never a constant.

Primary instrument, both moments: `grep -l "RUN DONE" watch/inbox/playground/tavern_*/play.md` (28 files match at the filing moment), `grep "BRAWL at round" watch/inbox/playground/tavern_*/play.md`, `grep "round 1 Greta Thornwood" watch/inbox/playground/tavern_*/play.md`, and a venv-python parse of each scenario.json for `pressure` and the persona set. Byte rule: the brawl round comes from the BRAWL marker, never the DONE line's static "10 rounds cap" tag.

## 1. The calibration cells (the deliverable)

- **p0 cell (fold moment): default-pressure only, never a labeled row.** Two runs (113904Z v0 fixture $0.00 2 rounds; 114126Z $1.58 10 rounds), both brawl=False, both carry NO `pressure` key in scenario.json: pressure 0 is the engine default (tools/tavern.py:73), not a labeled curve point. **Resolved 2026-10-04: tavern_20261004T084457Z is the first LABELED pressure-0 corpus row** (`"pressure": 0` byte-present in its scenario.json, fired by this lane; result in section 3).
- **p1 cell (fold moment): 14 runs, 11 brawls at rounds 3,4,4,4,5,5,5,6,6,7,10 (median 5), 3/14 never brawl (121214Z, 124908Z, 152937Z).** Independently re-derived from bytes this session (venv-python pass over the 14 dirs through 022300Z: brawls [3,4,4,4,5,5,5,6,6,7,10], median 5, same 3 no-brawl). Exactly ONE p1 brawl at round 3 (tavern_20261003T115343Z:113), so the folded "p1 r3 x2" stays refuted. **Census moment drift: 23 p1 runs (hourly fires 032225Z through 082906Z landed after the fold moment), 18 brawls at rounds 3,3,3,4,4,4,4,4,5,5,5,5,5,6,6,7,7,10 (median 5), 5/23 never brawl (21.7 percent).**
- **p2 cell (fold moment): n=1, brawl round 2 (tavern_20261003T115100Z:74, cumulative 14 >= 14).** **Census-plus: n=2 clean** with this lane's tavern_20261004T084000Z (brawl round 2, cumulative 15 >= 14, $0.18). A third p2 fire (p2 refresh A) was attempted and is BLOCKED; see section 3.
- **Greta cell (fold moment): judge 3/5 at round 1 in 13 of 16 BARFIGHT sessions with Greta; 4/5 in 3 (124908Z, 130953Z, 171056Z); esc crosses 2 at round 2 in 15/15; escalation_threshold 2 (eff 1 at p1) in all 16 BARFIGHT scenario.json files; Oswin 5 everywhere.** Independently re-derived from bytes this session (16 sessions through 022300Z: 13 at 3/5, same three at 4/5). There is no "fuse" in tools/tavern.py. **Census moment drift: 25 Greta sessions, 3/5 in 22, 4/5 in the same 3.**
- **p0 trigger value (was UNVERIFIED in the lane's gaps): resolved from code, tools/tavern.py:74 `self.heat = 18 - 2 * self.pressure`, so pressure 0 triggers brawl at cumulative escalation 18 (p1: 16, p2: 14).** The 114126Z final cum of 11 with no brawl is consistent; the labeled p0 run ended at cum 12 < 18.

## 2. The brawl table (all tavern_*/ dirs at the census moment 2026-10-04T08:36:45Z, plus post-census landings)

| Run | Pressure | Seed | Brawl round | Spend | Note |
|---|---|---|---|---|---|
| tavern_20261003T113904Z | absent (default 0) | none | none (2-round v0 fixture) | $0.00 | Vess/Brann/Quill/Tally set, no Greta: NOT a calibration point |
| tavern_20261003T114126Z | absent (default 0) | none | none (10 rounds) | $1.58 | no act mechanics (different instrument, F4) |
| tavern_20261003T115100Z | 2 | none | 2 (14 >= 14) | $0.19 | the founding p2 point |
| tavern_20261003T115343Z | 1 | none | 3 (16 >= 16) | $0.33 | the only round-3-fold p1 brawl |
| tavern_20261003T115732Z | 1 | 9004 | 5 (16 >= 16) | $0.71 | variance run; ask preamble said "3-4", marker says 5 |
| tavern_20261003T121214Z | 1 | none | NONE (10 rounds) | $2.11 | no-brawl |
| tavern_20261003T124545Z | 1 | 9006 | 4 (16 >= 16) | $0.51 | |
| tavern_20261003T124908Z | 1 | 9007 | NONE (10 rounds) | $2.18 | no-brawl; Greta r1 4/5 |
| tavern_20261003T125711Z | 1 | 9008 | 10 (16 >= 16) | $2.12 | |
| tavern_20261003T130953Z | 1 | none | 7 (16 >= 16) | $1.06 | Greta r1 4/5 |
| tavern_20261003T140343Z | 1 | none | 6 (16 >= 16) | $0.83 | |
| tavern_20261003T152937Z | 1 | none | NONE (10 rounds) | $2.12 | no-brawl |
| tavern_20261003T162257Z | 1 | none | 4 (16 >= 16) | $0.53 | |
| tavern_20261003T171056Z | 1 | none | 4 (16 >= 16) | $0.50 | Greta r1 4/5 |
| tavern_20261003T180319Z | 1 | none | 5 (16 >= 16) | $0.70 | |
| tavern_20261003T190348Z | 1 | none | 5 (16 >= 16) | $0.72 | |
| tavern_20261004T022300Z | 1 | none | 6 (16 >= 16) | $0.85 | the refire's 14th p1 run |
| tavern_20261004T032225Z | 1 | none | 3 (16 >= 16) | $0.32 | post-fold hourly fire |
| tavern_20261004T040438Z | 1 | none | 3 (18 >= 16) | $0.30 | post-fold hourly fire |
| tavern_20261004T050205Z | 1 | none | 4 (17 >= 16) | $0.49 | post-fold hourly fire |
| tavern_20261004T060223Z | 1 | none | 7 (17 >= 16) | $1.17 | post-fold hourly fire |
| tavern_20261004T070212Z | 1 | none | NONE (10 rounds) | $2.10 | no-brawl, post-fold hourly fire |
| tavern_20261004T080144Z | 1 | none | 4 (16 >= 16) | $0.49 | post-fold hourly fire |
| tavern_20261004T081710Z | 1 | tourney1 | NONE (10 rounds) | $2.10 | burn-down tournament title, same BARFIGHT p1 instrument; no-brawl |
| tavern_20261004T082510Z | 1 | none | 5 (16 >= 16) | $0.70 | in census |
| tavern_20261004T082906Z | 1 | none | 5 (16 >= 16) | $0.68 | in census |
| tavern_20261004T084000Z | 2 | none | 2 (15 >= 14) | $0.18 | LANE 9 p2 refresh B (post-census) |
| tavern_20261004T084146Z | 2 | none | none (3-round cap) | $0.01 | NOT a calibration row: 2-persona flash dogfood variant, different instrument; its dir also carries two identical RUN DONE rows (two automation fires collided on the same-second stamp) |
| tavern_20261004T084457Z | 0 (LABELED) | none | none (budget-capped, see section 3) | $1.13 | LANE 9 labeled p0 (post-census) |

Seed note: corpus scenario.json files carry no seed field; seeds (9004, 9006-9008, tourney1) appear only in run titles. Dice rolls (d20) do not drive the brawl; the judge's escalation scores do, so the curve is seed-insensitive by mechanism and seed-sensitive only through model sampling variance.

## 3. Fired runs (this lane, 2026-10-04)

Carrier: `.venv\Scripts\python.exe tools\tavern.py` on the hermes_burn funded rails. Scenario inputs staged at watch/inbox/playground/scenarios_lane9/ (byte-clones of the corpus BARFIGHT instrument from 115100Z: six personas, same models, opus judge; only pressure, eff_threshold and title differ).

1. **p2 refresh B: FIRED, CLEAN.** Command: `tools/tavern.py --scenario watch/inbox/playground/scenarios_lane9/p2_refresh_b.json --rounds 10 --budget-usd 0.18 --chain-tip lane9-p2-b`. Result: tavern_20261004T084000Z, BRAWL at round 2, cumulative 15 >= 14 (pressure 2), spend $0.18, RUN DONE + DONE + GWAP_BANKED, chain ok=True. p2 cell now n=2 clean (with 115100Z).
2. **Labeled p0: FIRED, CLEAN.** Command: `tools/tavern.py --scenario watch/inbox/playground/scenarios_lane9/p0_labeled.json --rounds 10 --budget-usd 1.05 --chain-tip lane9-p0-refresh2`. Result: tavern_20261004T084457Z, `"pressure": 0` byte-present, brawl=False, BUDGET CAP $1.05 hit mid-round (hard stop at 5 full rounds + 2 turns of round 6), spend $1.13, final cumulative escalation 12 < 18 trigger, RUN DONE + DONE + GWAP_BANKED, chain ok=True. First labeled pressure-0 corpus row. It does NOT reach the 10-round form of the founding p0 (budget cap, see the spend ledger below); the cell reads "no brawl, cum 12 of trigger 18, through 5 rounds on the current act-mechanics instrument".
3. **p2 refresh A: BLOCKED, not re-fired.** First fire collided with the first p0 fire on tavern.py's second-resolution run stamp (both stamped 083959Z; `mkdir(exist_ok=True)` made them share one dir, interleaving two runs into one transcript and one play.md; scenario.json was overwritten mid-flight). The contaminated dir was quarantined out of the tavern_* namespace to watch/inbox/playground/scenarios_lane9/void_stamp_collision_tavern_20261004T083959Z (spend $0.6529, void as data: each run's personas read the other run's lines). The blocked re-fire command, exactly as it would run: `tools/tavern.py --scenario watch/inbox/playground/scenarios_lane9/p2_refresh_a.json --rounds 10 --budget-usd 0.18 --chain-tip lane9-p2-a2`. Reason for not firing: the lane's paid-spend cap is under $2 and the ledger below leaves $0.037 of headroom; the p2 cell already holds n>=2 without it (a03 row 3's stronger n>=3 wish stays open for the next sitting).

Spend ledger for the lane's fires (transcript cost_usd sums, venv-python): $0.6529 (voided collision, quarantined) + $0.1801 (p2 refresh B) + $1.13 (labeled p0, RUN DONE figure) = $1.963 total paid, under the $2 cap. Lesson filed for the carrier owner: tavern.py run stamps have second resolution and exist_ok mkdirs, so concurrent fires in the same second corrupt each other; the hourly automation mostly avoids it by minutes, this lane's parallel launch hit it in one second, and the automation's own 084146Z dir shows the same double-DONE signature.

## 4. Falsifier status (the claim's own kill condition)

FIRED. SUBSTANCE_play_findings.md F1's falsifier reads: "any p1 seed still unbrawled at round 10, or any p2 seed surviving past round 5, breaks the p0 < p1 < p2 ordering." The first prong has fired five times: p1 seeds ran the full 10 rounds with no brawl at 121214Z, 124908Z, 152937Z (fold moment, 3 of 14) and 070212Z, 081710Z (census moment, 5 of 23). The no-brawl rate is stable across both moments (21.4 and 21.7 percent) and the brawl-round median holds at 5, so the drift did not move the shape, it confirmed it. Consequence, banked into the cells above: **p1 is a distribution (brawl rounds 3-10, roughly a fifth of seeds never brawl), not a mid-run curve point; the no-brawl runs are first-class data, not outliers.** The monotone "p0 < p1 < p2" reading of the curve is dead as a point claim; what survives is trigger ordering by mechanism (18/16/14, tools/tavern.py:74) plus a p1 latency distribution. The p2 prong has not fired (both clean p2 rows brawl at round 2). F1's secondary falsifiers (cum == trigger at every brawl; Oswin pinned at 0) held in every row of the table above with the round-3/round-4 overshoot brawls (18 >= 16, 17 >= 16) still threshold crossings, and Oswin nonzero only at p1 finals of 1-2, never the p0-style 0 everywhere (worth a look at the next fold, not a breach: his 5-threshold is p0-relative, eff 4 at p1).

## 5. Files this lane touched

- watch/inbox/TAVERN_CURVE_AUDIT_20261003.md (this file, new)
- watch/inbox/replay_flash/SUBSTANCE_play_findings.md (appended "Calibration refresh" block: the 14/16 cells with grep cites)
- corpus/steal/MASTER_MICKEY17_V2.md (sections 6.11 and 6.12 refire-count lines: instrument citations added, counts unchanged)
- watch/inbox/playground/scenarios_lane9/ (new: p0_labeled.json, p2_refresh_a.json, p2_refresh_b.json, void_stamp_collision_tavern_20261004T083959Z/)
- watch/inbox/playground/tavern_20261004T084000Z/ and tavern_20261004T084457Z/ (the two clean fired runs)
- watch/inbox/go_wave_20261004/tavern_refresh.md (lane receipt)

No dungeon-lane files, no arena bank code touched.
