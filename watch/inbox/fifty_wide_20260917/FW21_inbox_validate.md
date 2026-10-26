# FW-21 — Inbox validate: failure delta vs drift-patrol baseline, per-failure labels

- **class:** RECEIPT · **writer:** queue-gopher2-q023 · **board:** memory/plans/fifty_wide_20260917.md §D · **date:** 2026-09-28
- **command:** `.venv/Scripts/python.exe -m mag.shared_surface validate` (the machine-contract validate; exits 1 while any error stands)

## Baselines used

- **Retired drift-patrol baseline: 73 errors** (DRIFT_PATROL_20260915.md and _0916.md: "73 errors = baseline 73, delta 0"). Retired by DRIFT_PATROL_20260919.md: the 73 were "fossils (deleted files still indexed) plus convention noise"; new steady state **0**.
- **Current steady state: 0 errors** — 09-19 through 09-28 patrols (10 clean days; DRIFT_PATROL_20260928.md "0 errors, ok: True").

## First run (pre-burn, ~18:14Z): ok=false, 5 errors, 2 warnings — delta +5 vs steady state, −68 vs retired 73

| # | error | label | evidence |
|---|---|---|---|
| 1 | `NEW event-kind row in LINKS.jsonl (line 377, id 'SCOUT-QUIET-3', kind 'finding', writer 'free-resource-scout')` — B2-168 gate: post-marker kind row whose content sha is not in configs/links_kind_baseline.json (checked: absent) | **NEW** — appended TODAY 2026-09-28T13:05:46Z (file mtime; commit 0ef6fa748 dated 09-28T09:05:48-04:00, HEAD bytes = working tree, 377 rows), i.e. after the 08:00 patrol's clean validate. Row's own `ts` field reads 2026-09-22T15:20:00Z — writer-asserted and backdated; the append is what is new. 40 `finding` rows exist; only the 2 baseline-registered ones are legal post-marker. | sed -n 377p LINKS.jsonl; git log -1 0ef6fa748; baseline JSON |
| 2 | `hash mismatch: FIFTY_WIDE_BOARD_20260915.md` | **NEW** — last register 09-19T12:10:44Z (drift-patrol-cron, from index_events.jsonl); file mtime 09-28T18:13:58Z — bytes changed during this session, between my 18:13:14Z fold verify and this validate (explains why the fold verify missed it). Live-writer race, class (3) of the 09-17 itemization. | event log grep + statSync |
| 3 | `hash mismatch: STEALTH_SWEEP_LATEST.md` | **NEW** — registered 09-28T12:08:04Z, edited 13:50:15Z. Race drift, pre-existing at session start. | same |
| 4 | `hash mismatch: DRIFT_PATROL_20260928.md` | **NEW** — registered 09-28T12:10:54Z, edited 12:24:21Z (the patrol's own ADDENDUM appended post-fold). Self-inflicted patrol race. | same |
| 5 | `hash mismatch: burn_reset_20260927/queue/Q-041.md` | **NEW** — sealed 09-28T17:01:17Z by md-record-seal, edited 17:07:46Z (sibling lane writing its receipt after the seal). | same |

**None of the 5 is pre-existing** in the baseline sense: all postdate the 09-19 zeroing, and all but #1 postdate even this morning's 08:00 patrol. None belongs to the 09-17 +34 classes (1) or (2) — see FW19_patrol_debt_1_10.md census.

Warnings (not failures): 89 unindexed inbox files (today's BURN_* intake awaiting their lanes' self-registration — between-folds cadence, pre-existing pattern); 1 living downgrade `burn_wave_20260926/QUEUE.md` (known-living flag dropped by a plain re-register; LIVING_HASH_LAW §5 remedy named). events_log_malformed: 3 total, 3 grandfathered, 0 new. events_log_keys: 4,673 lines scanned, 0 unknown keys.

## Post-burn run (after FW-19's 5 re-registers): errors 5 → 1, warnings 2 → 1

- Errors #2-5 gone (fresh whole-file seals, seqs 1790458967636140351-354, writer queue-gopher2-q023).
- Living downgrade gone: QUEUE.md re-registered `--living` size-seal 483,723 (seq ...355); validate living census now `{ok:5, open:18, unverified:0, downgraded:0}`.
- Remaining error: #1 only — **left for its owner lane**: the B2-168 remedy (mirror the row into watch/inbox/EVENTS.jsonl with origin provenance, register its content sha in configs/links_kind_baseline.json) is the free-resource-scout lane's duty; a gopher blessing a free-lane scout row into the gate baseline would convert an untrusted finding into registered debt. Filed here as the finding.

## Honest limits

- The `verify` CLI's exit code is not a failure signal (always 0; scripts/index_fold_host.mjs:774-775) — recorded so the next reader doesn't misread exit 0 as clean.
- "The 12:07 patrol state" (FW-20's ask) has no clock stamp in DRIFT_PATROL_20260917.md; deltas there are taken against that receipt's recorded counts (174→176 events → 159 items), stated as such.
- The LINKS row 377 was not healed, not re-registered, not baseline-registered — owner-lane work, deliberately not done by this seat.
