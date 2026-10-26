# Inbox recent census: the 20 most recent files in watch/inbox/ (item s2-09, 2026-09-28)

Instrument: `Get-ChildItem watch/inbox -File | Sort-Object LastWriteTime -Descending | Select-Object -First 30` (run this session). watch/inbox top-level file count: 1,247. The top 20 by mtime were read (heads, tails, or full). Every count below comes from a command run during this ask.

## The 20, in mtime order

| # | file | mtime (local, 2026-09-28 unless noted) | bytes | what it is |
|---|------|-----|-------|------------|
| 1 | PACK_OFFLOAD.jsonl | 18:26:34 | 157,539 (747 rows) | context-pack offload telemetry, schema pack_offload.v1: per-session 4-stage shed log (L4 heat, L3 task, L0d/L0f blocks, hard clip), max_chars 4500 per stage |
| 2 | index_events.jsonl | 18:22:08 | 1,847,466 (5,224 lines, 5,223 parse as JSON, 1 does not) | the append-only inbox register event log that INDEX.json folds from |
| 3 | STEALTH_MINED_FINDINGS.jsonl | 18:21:33 | 48,475 (144 rows) | findings register for stealth-lane mined work: rows name work_id lib-belady-1966, lanes nous / hermes / openrouter, answer_file pointers into burn_reset work dir |
| 4 | DATED_METERS.jsonl | 17:20:49 | 5,305 (12 rows) | meter_patrol dated observation ledger, schema dated_meter_v1: one row per meter class per day, state RECEIPT or NOBS, pointer lists only |
| 5 | panda_panel_recovery_20260928.md | 17:05:26 | 4,238 | recovery receipt: a 4-lane ractor panel (sess_eb6d520b) died on a 1301 unsafe/sensitive strike at the synthesis turn; receipt banks the recovered verdict plus three new laws (receipt before speech, verdict not vocabulary, bell is a diagnostic) |
| 6 | mimo_watch.jsonl | 16:58:19 | 15,906 (61 rows) | hourly mimo-v2.6-flash-free free-window probe log (window_open, hours_left, serve up, latency, cost 0) |
| 7 | SELF_STEAL_REBUILD_RETEST_SALON_20260831.md | 14:33:39 | 59,621 | self-steal RIB (rib_id self_steal.rebuild_retest_salon.20260831): census, socratic gap analysis, rebuild order; verdict: the project suffers missing joins, not missing organs |
| 8 | SEAT_SPORes_AUDIT_CELL_20260912.md | 14:33:39 | 4,844 | seat-spore continuity audit cell: claim, repo evidence, act, Steiniger-style falsifiers; its own verify command is marked SUPERSEDED (FW-11) inside the file |
| 9 | REVEAL_FIVE_REHEARSALS_20260906.md | 14:33:39 | 15,489 | THE REVEAL reissue, unabridged: full-body receipts (state/POWER_RESTORE_20260825.md and siblings) with sha256 per receipt |
| 10 | GAP1_SPAWN_MANIFEST_20260906.md | 14:33:39 | 4,463 | GAP-1 closure receipt: mag/spawn_manifest.py consumed-sources organ + memory/MEMORY_resolved.md pointer repair; 31/467 links resolved, 436 phantoms |
| 11 | LINKS.jsonl | 14:29:00 | 255,681 (378 rows) | canonical URL link ledger (x.com drops and similar), per-row canonical sha256 and writer |
| 12 | INDEX.json | 14:27:28 | 466,153 (1,415 items) | the shared inbox register, schema shared_inbox.v1, authority untrusted_data_until_classified |
| 13 | FIFTY_WIDE_BOARD_20260915.md | 14:13:58 | 6,112 | fifty-wide work board: 40 receipt pointers into memory/runs/fifty_wide/*; footer marks the whole board SUPERSEDED 2026-09-28 (FW-06): all 40 pointers void, superseded by memory/plans/fifty_wide_20260917.md |
| 14 | MUSE_SPARK_ACCESS_20260928.md | 13:53:32 | 2,844 | OpenRouter recon verdict: 403 on meta/muse-spark-1.3 is a key-tier gate (permission_denied), not a free-tier gate; paid model, Contributor slug is separate |
| 15 | BURN_doctrine-owed-chase_20260928_m.md | 13:13:57 | 2,968 | burn receipt, verdict steal, topic closed green-pending-chronogram: archive item proven text-derivative-free, plate chronogram formally owed at higher resolution |
| 16 | BURN_doctrine-owed-chase_20260928_l.md | 12:22:38 | 3,908 | burn receipt, verdict steal: Amsterdam imprint byte-backed off archive.org JPEG originals (sha1 1305cab0...), year digits still owed |
| 17 | BURN_free-resource-landscape_20260928_n.md | 12:07:58 | 3,421 | burn receipt, verdict green: freelanes board consolidation caught churn (LLM7 free ids 4 to 3, GLM-5.3-Flash dropped; Featherless 22,059 rows alive) |
| 18 | BURN_doctrine-owed-chase_20260928_k.md | 11:09:49 | 3,172 | burn receipt, verdict steal: the 1701 Raziel scan found-not-pulled, double-pinned archive.org FD9301B8... + HebrewBooks req 23968 |
| 19 | BURN_free-resource-landscape_20260928_m.md | 11:04:24 | 2,560 | burn receipt, verdict vacuous: newest Wayback capture of lightning.ai/pricing is a client-rendered shell, Lightning lane closed dead |
| 20 | BURN_doctrine-owed-chase_20260928_j.md | 10:07:05 | 3,586 | burn receipt, verdict steal: HebrewBooks req 35004 byte-confirmed as Raziel HaMalakh name-magic exhibit but a 1953/54 Nagyvarad reprint, NOT the 1701 edition |

## Who wrote each (evidence per row)

Code-owned living instruments (writer is repo code, lines read this session):

- PACK_OFFLOAD.jsonl: written by `mag/context_pack.py:16` (PACK_OFFLOAD_FILE) appending at `mag/context_pack.py:48`.
- index_events.jsonl: written by the shared-surface register, `mag/shared_surface.py:117` (EVENTS_LOG); INDEX.json is the fold product (`mag/shared_surface.py:114`, fold host `scripts/index_fold_host.mjs`).
- STEALTH_MINED_FINDINGS.jsonl: written by `tools/stealth_driver.py:127` and `:788` (MINED_FILE).
- DATED_METERS.jsonl: written by `tools/meter_patrol.py:64` (LEDGER_RELPATH), organ meter_patrol; its two register events name writers exp002a and zcode-b2-469-dated-meters.
- mimo_watch.jsonl: written by `tools/mimo_watch.py:61` (LEDGER); hourly task armed by B2-261 at `configs/sanctioned_scheduled_tasks.yaml:56`; its register events name writers b2-236-mimo-retest, drift-patrol-cron, exp002a.
- LINKS.jsonl: written by the `main.py:1324` links CLI (add/check/dupes) plus backfill scripts (artifacts/backfill_links_20260916.py); 25 register events name 9 writers incl. zcode-rashomon-20260914, b2-26-links-sha-backfill, zcode-b2-221-prefix-editor, drift-patrol-cron.
- INDEX.json: control file, fold product of mag/shared_surface.py; deliberately never lists itself (CONTROL_FILES at `mag/shared_surface.py:119` includes INDEX.json, which is why it has no self-entry).

Receipt files (writer from register events or self-filing):

- panda_panel_recovery_20260928.md: zcode-seat-20260928 (its own index_events register rows at 2026-09-28T21:05:26Z and 21:05:45Z; the file's Filing section self-attributes the same).
- GAP1_SPAWN_MANIFEST_20260906.md: seat spawnman, self-named (session spawnman-gap1-20260906, "this seat built the two organs").
- The 6 BURN files: the burn-reset lanes whose slugs are doctrine-owed-chase and free-resource-landscape; every landing is locked as one row into memory/burns/LEDGER.jsonl (693 rows total; exactly 6 rows name these 6 files, verdicts j steal, k steal, l steal, doctrine-m green, free-m vacuous, n green; ledger writer tooling is the tools/ledger_lock.py append gate per `tools/ledger_lock.py:11`).
- SELF_STEAL_REBUILD_RETEST_SALON_20260831.md: author seat NOT named in the file header or its single register row (2026-09-01T03:18:00Z, class PROPOSAL, no writer field). watch/TOPIC_INDEX_20260905.md carries it 4 times marked [UNPROVEN]. Reported as unnamed, not guessed.
- SEAT_SPORes_AUDIT_CELL_20260912.md and REVEAL_FIVE_REHEARSALS_20260906.md: registered 2026-09-21T17:20:11.373488+00:00 as class BACKFILL ("md-record-law backfill: bytes were on disk, tracked late"), no writer field, no room.jsonl row found. Author unnamed.
- MUSE_SPARK_ACCESS_20260928.md: no register event, no INDEX entry, no room.jsonl row, no pre-session trajectory row found. Author unnamed on every surface searched this session.

## Referenced by anything (rg 15.2.0, one --fixed-strings pass per filename, glob excludes .git/.venv/node_modules/corpus; logs/ included; corpus/ 5.6 GB NOT searched)

- PACK_OFFLOAD.jsonl: tests/test_dirac_loop.py; watch/inbox/burn_reset_20260927/flash50/deep-multiscale-memory.md, deep-dream-cycle.md, deep-nurnberg-funnel.md; DIRAC_BANKED_INVARIANTS.jsonl; plus index surfaces. Registration: zero events ever, zero INDEX entries.
- index_events.jsonl: `mag/shared_surface.py:22,117,218,253`; scripts/index_fold_host.mjs; githooks/pre-push; configs/events_malformed_baseline.json; configs/events_key_schema.json; configs/drift_patrol_prompt.txt; memory/rib/RIB_MD_RECORD_20260921.md; memories/session/next-window-handoff.md. It IS the register.
- STEALTH_MINED_FINDINGS.jsonl: tools/stealth_driver.py; watch/inbox/SEED_RIB_REFRESH_20260928.md; watch/inbox/secret_gate_results/*.json; flash50/deep-selffeed-loop.md. Zero registration events.
- DATED_METERS.jsonl: tools/meter_patrol.py; tests/test_meter_patrol.py; scripts/census_patrol_daily.ps1; f-16.md and index-truth.md in this flash50 dir; B2_469_dated_meters_20260926.md. Registered, class ledger, 2 events.
- mimo_watch.jsonl: tools/mimo_watch.py; tests/test_mimo_watch_error_capture.py; configs/sanctioned_scheduled_tasks.yaml:56; configs/drift_patrol_prompt.txt; B2_223/B2_235/B2_236/B2_261 receipts. Registered, 4 events, 3 writers.
- panda_panel_recovery_20260928.md: referenced only by its own index_events rows and the live trajectory log. Registered in events (pending INDEX fold), zero INDEX entries.
- SELF_STEAL_REBUILD_RETEST_SALON_20260831.md: watch/TOPIC_INDEX_20260905.md (4 rows); the daily watch/PROSE_CENSUS_* index series; memory/corpus/watch_mining/watch_inventory.jsonl; B2 index presnapshots; the FW11_fence_annotator.py enumeration. Registered (PROPOSAL).
- SEAT_SPORes_AUDIT_CELL_20260912.md: PROSE_CENSUS series; flash50/f-16.md; ESTATE_INDEX; wave receipts. Registered (BACKFILL).
- REVEAL_FIVE_REHEARSALS_20260906.md: dashboard/static/trails/research.jsonl, dashboard/static/home.html, estate_walk html (the dashboard renders it); queue/lanes/research/trail.jsonl; PROSE_CENSUS series. Registered (BACKFILL).
- GAP1_SPAWN_MANIFEST_20260906.md: PROSE_CENSUS series; watch_inventory.jsonl; flash50/f-16.md. Registered (BACKFILL).
- LINKS.jsonl: 385 non-self files match, high-signal: main.py:1324; dashboard/server.py; docs/DRIFT_BOARD_SPEC.md; configs/links_sha_ratchet_baseline.json; configs/links_kind_baseline.json; scripts/build_knowledge_graph.py, build_fleet_imprint.py, build_deck.py, index_fold_host.mjs; queue lane inboxes (research/night/day_work/builder). Registered, 25 events.
- INDEX.json: the machine contract surface itself (watch/inbox/SHARED_SURFACE_CONTRACT.json; AGENTS.md boundary table; mag/shared_surface.py validate). Control file.
- FIFTY_WIDE_BOARD_20260915.md: PROSE_CENSUS_20260916 through 20260928; flash50/f-16.md; watch/inbox/burn_reset_20260927/queue/Q-021.md; memory/continuity/seat_memory_20260927/fifty-wide-board-20260915.md. Registered (RECEIPT).
- MUSE_SPARK_ACCESS_20260928.md: effectively zero durable references (only live trajectory rows from this census's own session). Unregistered.
- BURN_doctrine-owed-chase j/k/l/m: a strict citation chain, each cites its predecessor read in full (m cites l, l cites k, k cites j); free-resource m/n likewise (n cites m). All 6 locked into memory/burns/LEDGER.jsonl (6/6 rows present) and named in watch/inbox/secret_gate_results/changed_20260928T224028Z.json. All 6 have ZERO index_events rows: the last BURN register in the log is BURN_doctrine-owed-chase_20260928_h at 2026-09-28T12:17:32Z (writer md-record-seal); j through n were never sealed. 44 BURN-lane event rows exist historically (earlier lanes registered by exp002a and b2-02-writer-debt-20260926).

Caveat on reference counts: memory/trajectory/steps.jsonl matches every name because it is a live recorder that captured this census's own commands (session sess_dwf-dwfrun-...-actor_1_9 rows seen at its tail); catalog/catalog.jsonl, catalog/tags.jsonl, ESTATE_INDEX, and the PROSE_CENSUS series are catch-all indexes that mention nearly everything. High-signal references are the ones listed per file.

## Registration and drift audit (this session's sha check, INDEX.json snapshot mtime 14:27:28 local)

- Registered in INDEX.json (exact path match): 9 of the 20 (index_events, DATED_METERS, mimo_watch, SELF_STEAL_SALON, SEAT_SPORes, REVEAL_FIVE, GAP1, LINKS, FIFTY_WIDE_BOARD).
- INDEX.json itself: excluded from its own items by design (CONTROL_FILES, mag/shared_surface.py:119).
- Not registered: 10 of the 20. Of those, panda_panel has 2 register + 1 autoseal event rows (pending fold); the other 9 (PACK_OFFLOAD, STEALTH_MINED_FINDINGS, MUSE_SPARK, and all 6 BURN files) have zero registration events ever.
- SHA drift: comparing each registered entry's sha256 against current disk bytes: 8 of 9 MISMATCH (drift), 1 of 9 matches (FIFTY_WIDE_BOARD_20260915.md). The mismatches are the living JSONL appends plus the four files batch-touched at 14:33:39, consistent with the drift pattern f-16 documented earlier today.

## The 14:33:39 batch touch

Four files share mtime 14:33:39 to the second (SELF_STEAL_SALON, SEAT_SPORes, REVEAL_FIVE, GAP1). Fence-owner markers citing FW-11 2026-09-28 are present in 2 of the 4 (REVEAL_FIVE_REHEARSALS: 2 markers; GAP1_SPAWN_MANIFEST: 1 marker), matching the in-place annotation pass documented in watch/inbox/fifty_wide_20260917/FW11_fence_owners.md (30 fences, annotated in place, 2026-09-28). The other two files carry no fence marker; the writer of their same-second touch is not attributed by anything read this pass (reported as unresolved, not guessed).

## Preserve or archive

Preserve as living instruments (7): PACK_OFFLOAD.jsonl, index_events.jsonl, INDEX.json, LINKS.jsonl, DATED_METERS.jsonl, mimo_watch.jsonl, STEALTH_MINED_FINDINGS.jsonl. Code-owned, code-referenced, actively appended; the reference search shows tests, configs, hooks, and dashboards bind to them.

Preserve as active receipts (7): panda_panel_recovery_20260928.md (banks a lost deliverable plus three new laws; untracked in git, so it should ride the next commit and its INDEX fold), and the 6 BURN files (j,k,l,m + free m,n). The BURN chain is a closed evidence spine: j corrected an edition attribution, k double-pinned the 1701 scan, l byte-backed Amsterdam, m closed the topic green-pending-chronogram, free-m closed the Lightning lane, n consolidated the freelanes board green. Their registration gap is the actionable defect: recommend sealing them (the sealer last fired on _h at 12:17:32Z and stopped) and committing them.

Archive, keep bytes, drop from hot rotation (6): FIFTY_WIDE_BOARD_20260915.md (self-marked SUPERSEDED, all 40 pointers void); SEAT_SPORes_AUDIT_CELL_20260912.md (one-shot audit cell whose own command is marked SUPERSEDED); REVEAL_FIVE_REHEARSALS_20260906.md (rehearsal reissue, dashboards already carry it); GAP1_SPAWN_MANIFEST_20260906.md (delivered receipt, the organs live in mag/spawn_manifest.py); SELF_STEAL_REBUILD_RETEST_SALON_20260831.md (August PROPOSAL marked [UNPROVEN] in TOPIC_INDEX, superseded by later self-steal synthesis surfaces); MUSE_SPARK_ACCESS_20260928.md (small self-contained recon note with no durable references; register it, then archive).

## Census numbers, one line each

- 20 files censused of 1,247 top-level watch/inbox files; total bytes of the 20: 2,973,522 (os.path.getsize sum, this session).
- Registry status: 9 registered + 1 control-file-by-design + 10 unregistered, of which 9 have zero registration events ever.
- Drift: 8 of 9 registered entries sha-mismatch current bytes.
- Git: 11 of 20 tracked, 9 untracked (PACK_OFFLOAD, panda_panel, MUSE_SPARK, and all 6 BURN files).
- Burn ledger: 693 rows total, 6 name these files, verdicts 3 steal (j, k, l) / 1 vacuous (free-m) / 2 green (doctrine-m, n).
- Not searched: corpus/ (5.6 GB, 71,590 files) excluded from the reference pass for time; stated here rather than implied.
- Em-dash count in this file: 0 (scanned with the venv python below).

## Corroboration: mag.shared_surface validate run after banking

Running `.venv/Scripts/python.exe -m mag.shared_surface validate` this session independently confirmed the drift and registration findings: it raises hash mismatch errors on exactly the four batch-touched files (SELF_STEAL_REBUILD_RETEST_SALON_20260831.md, GAP1_SPAWN_MANIFEST_20260906.md, REVEAL_FIVE_REHEARSALS_20260906.md, SEAT_SPORes_AUDIT_CELL_20260912.md), and its unindexed-files warning names exactly the never-registered set found above (all listed BURN receipts including the 6 censused here, MUSE_SPARK_ACCESS_20260928.md, PACK_OFFLOAD.jsonl, STEALTH_MINED_FINDINGS.jsonl, panda_panel_recovery_20260928.md). One new defect surfaced by the validator that this census had not catalogued: LINKS.jsonl line 377 is a NEW event-kind row (id SCOUT-QUIET-3, kind finding, writer free-resource-scout) violating the link-rows-only rule past the B2-28 marker; the row should have gone to watch/inbox/EVENTS.jsonl per mag.link_library.load_events. Reported as found, not fixed.
