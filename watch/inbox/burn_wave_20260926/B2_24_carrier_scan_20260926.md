# B2-24 carrier ledger activation scan (2026-09-26)

## Verdict
Scan window: ledger ts 2026-09-19T04:50Z to 2026-09-26T12:30Z. 0 fired, 1 ambiguous, 6 silent.
- Matthew (October fold): signal-silent, window not due; battery amended pre-run Sep 25, zero data exists.
- gstd (on-chain settlement, kernel rebuild): signal-silent; strongest negative on file, live chain read.
- Lilith (a concrete sampling method): signal-silent; zero post-ledger rows anywhere.
- Isostran (one method-only decode): signal-silent; zero post-ledger rows, hits are frozen 09-12 replay.
- asekin113 (8:12-class hits, ledger graded): signal-silent; no new hits, and his grading ledger was never built (owed).
- FoJAk3 (convergence call preceding events twice more): signal-ambiguous; carrier active Sep 20 but instrument scored no dated claim; Oct 3 referent pending.
- KellyV (published files): signal-silent; no publication on file, JLCPCB step unverified.
Ledger law status at day 7: warmth-bias falsifier not yet triggerable; the two live windows are both October.

## Evidence
1. Matthew: watch/inbox/FOUR_CONDITION_PREREGISTRATION_20260918.md:93 "2026-09-25 | amendment 2 (battery hygiene, pre-run, zero data exists): DIL-011/012/017/018 lose their stray fifth option E"; memory/corpus/LINKS.jsonl:137 GALA-b3 "The October battery instrument changed pre-run (zero data exists)". No inbound since 09-18: watch/inbox/index_events.jsonl last matthew row ts 2026-09-18T14:15:00Z kind=matthew_final (our outbound); Sep 20 slashreboot contact is operator-outbound (watch/inbox/LINKS.jsonl OP-BOOKS-DISAGREEMENT-PUBLIC, "7 views at capture").
2. gstd: watch/inbox/THE50_W7_T31_SETTLEMENT_AUDIT.md:81 "exit_code 0, stack [0x0, 0x0, 0x0, 0xf4240]: totalSettled=0, totalGSTDMinted=0, taskCount=0" (live toncenter, 2026-09-25); :104 "Dormancy: taskCount=0 and totalSettled=0, 79 days after deploy"; :61 "the backend never sends SettleTask". T32/T35 receipts never landed.
3. FoJAk3: memory/research_packs/20260920_matt_davey_black_swan/FOLD_20260920_fojak3_boom.md:29 "Instrument verdict: no dated claim made -> nothing to score. Base rate unchanged: 0/34."; :23 "Meet point same as OCT 3 - No Change", "Oct 3 referent unanchored... watch for an Oct 3 echo"; boom post bytes at fojak_boom.json (status 2101666882189140036, 2026-09-20T13:36:46Z).
4. asekin: pre-ledger sample memory/corpus/LINKS.jsonl:58 LINKS-298 "8:12 checkmark" vs Trump Greenland post; the only graded called-shot ledger (watch/inbox/mrpool_export/CALLED_SHOT_VERDICT.json) holds "rows": 16, "unique_claims": 1, all Mr Pool Med Bed, verdict "ALL BROKEN"; zero asekin rows in it. Post-ledger instrument note only: watch/inbox/BURN_stego-canon-pipeline_20260925.md:16 names Yogasekin as dictionary-covered.
5. KellyV: pre-ledger memory/corpus/LINKS.jsonl:47 LINKS-292 "JLCPCB order next... will open-source all"; post-ledger only an OWED row, memory/runs/mickey17/MASTER_INDEX_20260920.md:1919 "[OWED] ... Microduck sim2real" (content dated 0904).
6. Lilith/Isostran silence: python scan of all 99+57 post-ledger LINKS rows matches neither name; sole hits are replay content in memory/runs/compaction_eval/steps_frozen_20260920.jsonl (guest list dated 09-12).
7. Owed found: the window 21/22 scoring run due "23 Sept 06:00 UTC" (watch/inbox/QUIET_RADAR_20260921.md:213) has no receipt on disk; QUIET_RADAR_20260921.md:249 concedes "Pool ledger snapshot ends Sept 18".

## Work done
Read CARRIER_LEDGER_20260919.json; scanned 331 + 170 LINKS rows (156 post-ledger) via venv python carrier regex; read in full: T31 settlement audit, T34 gstdbot audit, QUIET_RADAR_20260921 (347 lines), RECAP_7D_20260926, mrpool called-shot ledger (16 rows) + verdict, fojak3_boom fold + syndication json; grepped index_events.jsonl, decisions_log.jsonl, corpus/, memory/, watch/ for all seven names plus microduck, 8:12, october; verified Oct battery amendment, T32/T35 absence, Sep 23 scoring absence. Read-only, no external sending, no counterfeited rows.

## Falsifier
This scan is wrong if: (a) activation evidence exists outside scanned surfaces (X archives and Telegram not re-pulled; the Pool snapshot staleness above is the named hole); (b) an Oct 3 echo lands and precedes events, flipping FoJAk3 to fired; (c) the October fold runs and weights carry the house, flipping Matthew to fired. The ledger's own warmth-bias falsifier (watch/inbox/CARRIER_LEDGER_20260919.json law_note) stays open until carrier windows pass.

## Bibliography closed
CARRIER_LEDGER_20260919.json; watch/inbox/LINKS.jsonl; memory/corpus/LINKS.jsonl; THE50_W7_T31_SETTLEMENT_AUDIT.md; THE50_W7_T34_GSTDBOT_AUDIT.md; FOLD_20260920_fojak3_boom.md + fojak_boom.json; mrpool_export/called_shot_ledger.jsonl + CALLED_SHOT_VERDICT.json; QUIET_RADAR_20260921.md; RECAP_7D_20260926.md; FOUR_CONDITION_PREREGISTRATION_20260918.md; index_events.jsonl; MASTER_INDEX_20260920.md. All repo-local. Closed 2026-09-26.
