# BURN b2-wave-fold 20260926_b

## Verdict

steal

## Evidence

- memory/burns/LEDGER.jsonl: 451 rows now vs 178 sweep-time; act rows: 74 (B2-24), 84 (b2-30), 86 and 90 (b2-53), 89 (b2-54), 104 (B2-59).
- B2_53_grok_fire_card_20260926.md:82-88 (B2-425 note): "FIRE executes only on exit 0" of `python tools/operator_go.py grok-lane-packet`. Executed this pass: "NO-GO-on-file", exit 1.
- B2_54_cron_arm_card_20260926.md:5: "Arming is one operator step: open a FRESH chat and paste Prompt A"; FLEET_IMPRINT_20260917.md:1231: "a session owning a scheduled task CANNOT CronCreate a second".
- B2_166_rubric_scoring_20260926.md:5: "MISS on receipts on file: data point #35 scores 0 ... 0/34 to 0/35"; ledger line 247 "LANDED" 19:03:30Z.
- B2_467_pool_repull_20260926.md:3: "MISS STANDS and lifts to closed on the Pool main-channel arm"; ledger line 268: "B2-467 has no receipt and no LEDGER row ... checked unearned".
- B2_30_shadowledger_live_20260926.md:57: "Filed as owed: Studio publish + two-client crossing on real DataStores".
- B2_59_miprov2_dig_20260926.md:23-25: F1 fires if dspy "moves ReAnchor-style keep-if-beats-else-restore onto prompt text, or ships signature-level protected fields"; "amendment D untestable until the paired harness lands".

## Steal or Vacuous

(a) b2-53: fire-ready, three amendments in card (scope Asks 2-4; memory/corpus/LINKS.jsonl:32 as Ask 3 source; Ask 4 dated to the 37 20260925 files). Fires via harness/grok_cli.py. Operator fires first: the canonical gate reads NO-GO-on-file, so a GO row (operator_go.v1, gate grok-lane-packet, source_transcript) must land in OPERATOR_GO.jsonl before any lane executes.

(b) b2-54: card only, nothing armed, operator-gated: only a fresh operator chat can paste Prompt A (CronCreate weekly Sundays 06:30 local, the steps.jsonl:22162 pipeline with roundtrip gate, INDEX registration and the never-print pack_key law); an owning session cannot arm it (one-automation law). First fire 2026-09-27 06:30 if armed tonight, else 2026-10-04.

(c) B2-24: resolved after the sweep. Reconstructed from bytes and filed as B2-166: scored against the seal-verified rubric (sha A76590AC.., index seq 179001121373993) plus 101 window-date files; MISS, 0/34 to 0/35, three days late, lateness named. B2-467 closed the Pool main-channel arm via the no-auth preview door (30 fresh rows). Still owed: B2-467's own receipt (B2-511) and the never-harvested mirror @looP_rM311_7211 (B2-515).

(d) b2-30 live proof: publish the 08:28-or-newer rbxlx, then two real clients cross one portal, stop, rejoin on real DataStores and every "took the portal" row survives; probes are same-uid same-day cross-server double write (S2/S3) and mixed-fleet late-SetAsync clobber (S4b). Owed to the Sep-29 P3 run. HEAD is still pre-fix; worktree only.

(e) B2-59: resolves two ways. (1) Read the five owed dspy teleprompt files; zero protection there settles the hold, a protected field fires F1 and demotes to interop note. (2) Land the B2-58 paired harness so amendment D is testable; ReAnchor's 5-fold keep-or-restore is the filed steal candidate.

## Falsifier

This chase is wrong if: `tools/operator_go.py grok-lane-packet` exits 0 on a GO row filed after my read; or B2_166's seal hash fails against index_events.jsonl seq 179001121373993 (not byte-backed then).

## Bibliography

Closed. memory/burns/LEDGER.jsonl (lines 74, 84, 86, 89, 90, 104, 247, 263, 268); watch/inbox/burn_wave_20260926/: B2_53_grok_fire_card, B2_54_cron_arm_card, B2_24_carrier_scan, B2_166_rubric_scoring, B2_30_shadowledger_live, B2_59_miprov2_dig, B2_467_pool_repull (all _20260926.md); watch/inbox/OPERATOR_GO.jsonl; tools/operator_go.py (executed); watch/inbox/QUIET_RADAR_20260921.md:248-251. Nothing fired, nothing armed, no file edited except this report.
