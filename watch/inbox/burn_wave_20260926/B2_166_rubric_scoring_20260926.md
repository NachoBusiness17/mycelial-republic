# B2-166 window 21/22 rubric scoring receipt (2026-09-26)

## Verdict

MISS on receipts on file: data point #35 scores 0, the called-shot ledger lineage moves 0/34 to 0/35, and Matt Davey's 21-22 convergent map closes quiet exactly as his own conclusion card pre-accepted, which files as a calibration credit per the rubric's MISS clause. The score is PROVISIONAL on one named evidence hole: the Mr Pool ledger snapshot ends 2026-09-18T14:27:47Z (byte-pinned below), so rubric item 5's Pool-channel arm and any in-window channel-silence telemetry cannot be confirmed fresh, and the Pool-harvest refresh the desk scheduled before scoring (QUIET_RADAR_20260921.md lines 248-251) was never executed. No HIT item and no PARTIAL item fires on any receipt on disk. The rubric's scoring clock was 2026-09-23 06:00 UTC; this run executed 2026-09-26 ~19:00Z, three days late, and the lateness is named rather than papered over. The victory-lap rule binds symmetrically: no telemetry (the 10:55Z watchlist post, the water-rhyme, the SaltyVet personnel action) is upgraded, and no hole is disguised as a clean MISS.

Per-arm score against watch/inbox/WINDOW_2122_SCORING_RUBRIC_20260920.md:

| rubric arm | fired? | basis |
|---|---|---|
| HIT 1: unscheduled G20 blackout/comms >1M customers and >6h | no receipt | zero boundary-true keyword hits in all 101 window-date inbox files; zero radar entries |
| HIT 2: national non-weather, non-test emergency-alert activation | no receipt | same sweep; zero radar entries |
| HIT 3: MOEX XRP futures launch halted/disrupted on 22 Sept | no receipt | no MOEX observation either way exists on disk; the launch itself is unwitnessed by the archive |
| HIT 4: G20 market-wide circuit breaker | no receipt | same sweep; zero radar entries |
| HIT 5: dated register-principal pre-claim on the window | not fired on file | FoJAk3: instrument verdict "no dated claim made" (window-eve fold); Assange: silent on file; BG123/Riddler/mirror: unmonitored surfaces, nothing on file; Mr Pool: UNVERIFIABLE, snapshot ends Sept 18 (the hole) |
| PARTIAL: blackout drill in-window | no receipt | zero hits |
| PARTIAL: sub-threshold outage amplified by register accounts | no receipt | zero hits; amplifier arms unverifiable post-Sept 18 for Pool |
| PARTIAL: MOEX launch delays under 2h | no receipt | no MOEX observation either way |
| PARTIAL: register victory-lap over an ambiguous event | no receipt | zero hits |

Cluster disposition of watch/inbox/WATER_WATCHLIST_20260921.json: institutional (items 1-4) no score; ripple_core no dated-before-event statement on file; prophecy_cluster not fired on receipts on file with the Pool arm unverifiable; chaos_commentary (watched-serious per the Sept 21 posture correction) no rubric-relevant statement on file. OCT 3 check stays PENDING, scoreable 2026-10-04 per the rubric's pre-registration.

## Evidence

1. The scored card: watch/inbox/WINDOW_2122_SCORING_RUBRIC_20260920.md, sha256 A76590AC441C96490EB29DF90BF4F42E751AD7A71CDE0CC1D2777D07B174DA11, byte-identical to its index_events.jsonl registration (seq 1790011211373993, 2026-09-21T17:20:11.373Z, class BACKFILL). Pre-registered before the window opened; window 2026-09-21 00:00 UTC to 2026-09-23 00:05 UTC; scoring time 2026-09-23 06:00 UTC, receipts only.
2. The owed premise verified: no scoring receipt existed. Filename sweep of watch/ and memory/ for scoring, WINDOW_21, and RUBRIC artifacts returns only the rubric card itself; grep for "0/35" and "data point #35" returns no scoring artifact anywhere; watch/inbox/INDEX.json carries only WINDOW_2122_SCORING_RUBRIC_20260920.md. First on-disk naming of the debt: watch/inbox/burn_wave_20260926/B2_24_carrier_scan_20260926.md Evidence item 7.
3. The scored instrument: watch/inbox/WATER_WATCHLIST_20260921.json, sha256 156CEF8F526AF3F3C717DF31C6A7B56D9A69357D38AD42BD2C96BFE9CF711603. Day-1 telemetry (ts 2026-09-21T11:10Z): Mr Pool channel silent day 1 per window QA; "NOT a rubric hit - no blackout, no EBS, no MOEX halt, no pre-claim"; channel-activity asymmetry logged as telemetry only; prophecy-cluster mirrors named "unmonitored until this list".
4. The standing sweep that ran through the window: watch/inbox/QUIET_RADAR_20260921.md, sha256 20F2002876699FA46F7627C408DEDE4FFEEE6A70296A4AAEE52AB0EFCE6B6027. Line 213: "rubric scoring 23 Sept 06:00 UTC unchanged." Lines 248-251 (WINDOW DAY-ONE LEDGER NOTE): "Pool ledger snapshot ends Sept 18 - day-one window silence CANNOT be confirmed fresh without a Telegram re-pull. Added to the scoring run: refresh the Pool harvest before the Sept 23 scoring." All in-window radar entries record zero HIT-class events (the SaltyVet pair explicitly scored "NO window hit"; the last in-window entry is the Sept 22 session comb).
5. Keyword sweep of every watch/inbox artifact dated 2026-09-21, 2026-09-22, or 2026-09-23 (101 files) for MOEX, blackout, circuit breaker, EBS, IPAWS, "emergency alert": an initial case-insensitive pass matched only the substring "ebs" inside "website"; a boundary-true recheck returned 0 matches in all 101 files. No on-disk receipt of any HIT-class external event exists.
6. The data hole, byte-pinned: watch/inbox/mrpool_export/ledger.jsonl and ledger_full.jsonl each hold 3,663 rows, min date 2023-05-02T10:36:53Z, max date 2026-09-18T14:27:47+00:00 (venv python scan over both files, sha256 of ledger_full 5FD228004F567342746CE4635418048125E3C8445AEC005B14DD1CDA03425B34). mrpool_export/HARVEST_COMPLETE.json confirms harvest date 2026-09-18 and no re-pull since. The entire scoring window postdates the snapshot.
7. Register principal surfaces on file: memory/research_packs/20260920_matt_davey_black_swan/FOLD_20260920_fojak3_boom.md (boom post 2101666882189140036, 2026-09-20T13:36:46Z, window-EVE): "Instrument verdict: no dated claim made -> nothing to score. Base rate unchanged: 0/34." and the Oct 3 referent pre-registered. FOLD_20260920_matt_reaction_157251.md closes the same way: "no dated claim, 0/34 stands."
8. Denominator lineage: memory/research_packs/20260920_matt_davey_black_swan/REPORT.md ("34 dated claims extracted, every one checkable") and PACK.md ("0/34 dated claims landed genre-wide"). The rubric's MISS clause defines data point #35 as the ledger move 0/34 to 0/35.
9. Discoverer's record: watch/inbox/burn_wave_20260926/B2_24_carrier_scan_20260926.md Verdict and Falsifier(a), which inherited this exact hole ("X archives and Telegram not re-pulled; the Pool snapshot staleness above is the named hole").

## Work done

1. Read in full: the rubric card, WATER_WATCHLIST_20260921.json, QUIET_RADAR_20260921.md (347 lines), B2_24_carrier_scan_20260926.md, the black swan pack folds and report heads.
2. Verified the rubric's bytes against its own registration seal (hash match, seq 1790011211373993), so the scoring ran against the pre-registered card, not a mutated one.
3. Ran the owed-premise check (no scoring receipt on disk) by filename sweep, full-text grep, and INDEX.json.
4. Swept all 101 window-date inbox artifacts with boundary-true HIT-class keywords; classified the only matches (case-insensitive "ebs" in "website") as substring artifacts.
5. Pinned the Pool snapshot hole with a venv python scan of both ledger files (row counts, min, max dates).
6. Scored all five HIT arms and all four PARTIAL arms per the table above; filed this receipt as the data-point-35 record; appended the memory/burns/LEDGER.jsonl row via .venv python json.dumps; self-fed three briefs to the board UNCHECKED.
7. Did NOT mutate mrpool_export/CALLED_SHOT_VERDICT.json or any called_shot_ledger.jsonl: those hold the Med Bed block (16 rows, unique_claims 1), a different ledger shape; the 0/34 count lives in the report lineage, and this receipt is the #35 record. Named-lateness law: the run is filed 2026-09-26 against a 2026-09-23 06:00Z clock, and the missed clock is itself recorded as a finding (B2-166 brief).

## Falsifier

1. Any dated in-window receipt of HIT items 1-4 (G20 blackout >1M customers and >6h, national non-weather alert, MOEX XRP launch halt on 22 Sept, G20 circuit breaker) flips this MISS to HIT and voids the receipt; the sweep is archive-bound, and a wire log or re-pull can still produce one.
2. A dated Mr Pool or mirror-channel in-window post constituting a "this is it" pre-claim on the 21-22 window flips HIT item 5 and voids the provisional arm; the Sept 18 snapshot makes this checkable only by a Telegram re-pull (mrpool_export/harvest.session exists for exactly that).
3. If a 35th pre-window dated claim turns out checkable in the genre corpora, the 0/34 denominator is wrong, the #35 ordinal moves, and the ledger move must be recomputed before any citation.
4. This scoring does not touch the OCT 3 pre-registration: a Mr Pool / FoJAk3 / mirror message event referencing Oct 3, or a documented real-world event they link to it, landing by 2026-10-04 scores separately per the rubric; silence there sends the coffee-protocol claim to the expired ledger.

## Bibliography (closed)

- watch/inbox/WINDOW_2122_SCORING_RUBRIC_20260920.md (full read, hashed)
- watch/inbox/WATER_WATCHLIST_20260921.json (full read, hashed)
- watch/inbox/QUIET_RADAR_20260921.md (full read, hashed, lines 213 and 248-251 cited)
- watch/inbox/burn_wave_20260926/B2_24_carrier_scan_20260926.md (full read)
- watch/inbox/mrpool_export/ledger.jsonl + ledger_full.jsonl (venv python scan) + HARVEST_COMPLETE.json + CALLED_SHOT_VERDICT.json
- memory/research_packs/20260920_matt_davey_black_swan/ (REPORT.md, PACK.md, MATT_QA_20260921.md, FOLD_20260920_fojak3_boom.md, FOLD_20260920_matt_reaction_157251.md)
- watch/inbox/index_events.jsonl (seq 1790011211373993 rubric registration)
- watch/inbox/INDEX.json, watch/inbox/burn_wave_20260926/QUEUE.md (B2-24 row line 156, B2-166 row line 250), memory/burns/LEDGER.jsonl
- 101 watch/inbox artifacts dated 20260921/20260922/20260923 (keyword sweep)

All repo-local. No external fetch was used; the scoring is receipts-only per the rubric's own law, which is also why the hole is a hole. Closed 2026-09-26.
