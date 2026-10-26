# Lane 9 tavern-refresh receipt (GO wave 2026-10-04, MASTER_MICKEY17_V2.md section 9 GO item 10)

Evidence rows: memory/runs/mickey17_v2/runs/run-0/lanes/a03-tavern-curve.json (all 7 rows read). Fold: GO item 10 = a03#1 + a03#3 + a03#5. Full deliverable: watch/inbox/TAVERN_CURVE_AUDIT_20261003.md.

## Sub-item 1: calibration cells updated to the 14-run / 16-session counts

- a03#1 (p1 cell): corpus/steal/MASTER_MICKEY17_V2.md line 141 (section 6.11 refire-count line) now cites its instrument: `grep "BRAWL at round" watch/inbox/playground/tavern_*/play.md` over the 14 p1 runs with RUN DONE at the 2026-10-04 refire moment, pointing at this receipt. Counts unchanged (already correct in the refire line): 11 brawls r3-r10 median 5, 3/14 no-brawl.
- a03#3/#5 (Greta cell): master line 148 (section 6.12 refire-count line) now cites `grep "round 1 Greta Thornwood" watch/inbox/playground/tavern_*/play.md` over the 16 BARFIGHT sessions with Greta. Counts unchanged: 3/5 in 13 of 16, 4/5 in 3 (124908Z, 130953Z, 171056Z).
- Both fold-moment counts independently re-derived from bytes this session (venv-python pass over the 14 dirs through 022300Z): brawls [3,4,4,4,5,5,5,6,6,7,10] median 5, no-brawl 121214Z/124908Z/152937Z; Greta 13 of 16 at 3/5. Zero contradiction with the lane rows.
- watch/inbox/replay_flash/SUBSTANCE_play_findings.md: appended a "Calibration refresh (2026-10-04...)" block carrying the 14/16 cells with grep cites, the resolved p0 trigger (tools/tavern.py:74, `heat = 18 - 2 * pressure`, so p0 trigger 18), and the falsifier-fired statement. Original n=4 text left untouched (dated replay deliverable).

## Sub-item 2: brawl table filed

watch/inbox/TAVERN_CURVE_AUDIT_20261003.md section 2: the full table, 29 rows (26 dirs at census moment 2026-10-04T08:36:45Z + 3 post-census landings), each row: pressure from scenario.json, seed from title, brawl round from the BRAWL marker, spend from RUN DONE. Summary at the census moment: p1 n=23 (18 brawls, rounds 3,3,3,4,4,4,4,4,5,5,5,5,5,6,6,7,7,10, median 5; 5/23 no-brawl = 21.7 percent), p2 n=1, default-p0 n=2 (unlabeled), Greta 3/5 in 22 of 25.

## Sub-item 3: fires (one labeled p0, two p2)

- **p2 refresh B: FIRED, CLEAN.** tavern_20261004T084000Z: BRAWL round 2, cumulative 15 >= 14, $0.18, chain ok=True. p2 cell n=2 clean with 115100Z. Command in the audit, section 3.
- **Labeled p0: FIRED, CLEAN.** tavern_20261004T084457Z: `"pressure": 0` byte-present (first labeled p0 corpus row, a03 row 1's deliverable), brawl=False, budget-capped at 5 full rounds + 2 turns (cap $1.05, spend $1.13), final cumulative escalation 12 < 18 trigger, chain ok=True.
- **p2 refresh A: first fire VOID, re-fire BLOCKED.** Cause: tavern.py stamps run dirs at second resolution with exist_ok mkdir; the parallel p0 + p2 A launches both stamped 083959Z and shared one dir (interleaved transcripts, scenario.json overwritten mid-flight). Quarantined to watch/inbox/playground/scenarios_lane9/void_stamp_collision_tavern_20261004T083959Z ($0.6529 paid, void as data). Re-fire command filed in the audit, section 3, not fired: spend ledger stands at $1.963 against the under-$2 cap (headroom $0.037), and the p2 cell already holds n>=2. The automation's own 084146Z dir shows the same double-DONE collision signature - carrier-owner note filed in the audit.

## Sub-item 4: falsifier status

Stated in the audit, section 4: FIRED. F1's "any p1 seed still unbrawled at round 10" prong fired 3 times by the fold moment (121214Z, 124908Z, 152937Z) and 5 times by the census moment (+070212Z, 081710Z). No-brawl rate stable at 21.4 / 21.7 percent across the two moments; brawl median holds at 5. p1 is a distribution (rounds 3-10, about a fifth never brawl), the no-brawl runs are first-class data, and the monotone p0 < p1 < p2 point-claim reading is dead; what survives is the trigger ordering by mechanism (18/16/14) plus the p1 latency distribution. The p2 prong has not fired (both clean p2 rows brawl at round 2).

## Files touched (disjoint ownership honored)

- watch/inbox/TAVERN_CURVE_AUDIT_20261003.md (new)
- watch/inbox/replay_flash/SUBSTANCE_play_findings.md (append-only refresh block)
- corpus/steal/MASTER_MICKEY17_V2.md (lines 141, 148: instrument citations added to the two a03-owned refire lines; no other bytes)
- watch/inbox/playground/scenarios_lane9/ (new: 3 scenario inputs + voided-run quarantine)
- watch/inbox/playground/tavern_20261004T084000Z/, tavern_20261004T084457Z/ (my fired runs)
- watch/inbox/go_wave_20261004/tavern_refresh.md (this receipt)

No dungeon files, no arena bank code touched. No commits (coordinator commits).

## Blockers

- p2 refresh A re-fire: blocked by the paid-spend cap (exact command + reason in the audit, section 3). p2 cell at n>=2 satisfies the GO item's stated bar; a03 row 3's n>=3 wish is the open tail.
- Labeled p0 reached 5 rounds, not the 10-round form (budget cap). A full 10-round labeled p0 is projected $1.58-2.10 on the corpus instrument and will not fit under a $2 lane cap alongside the other fires; next sitting can fire it alone for about $2.

## Spend

$1.963 total paid (transcript cost_usd sums: $0.6529 voided collision + $0.1801 p2 B + $1.13 labeled p0). Under the $2 cap.
