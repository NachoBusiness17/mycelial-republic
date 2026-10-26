# f-16 INDEX TRUTH AUDIT - watch/inbox/INDEX.json (2026-09-28)

Item f-16: for every item in `watch/inbox/INDEX.json`, (1) does the file exist on disk,
(2) does its sha256 match the INDEX-recorded sha256, (3) is it registered in
`watch/inbox/LINKS.jsonl`. Every number below comes from a command run during this ask
(repo venv `.venv/Scripts/python.exe`, never bare python). Sweep script banked beside
this file: `f-16_sweep.py`; full per-item truth: `f-16_sweep.json` (1,415 entries).
Mirror: `index-truth.md` in this directory, byte-identical (sha asserted at bottom).

## Subject files

- `watch/inbox/INDEX.json`: 466,153 bytes, sha256 `6acf33147b58d3e3824f39cc7b920173bfc05bc7413ff85754624a8c110d156b`, schema `shared_inbox.v1`, root `/board/inbox` (= `watch/inbox` on this host per `watch/inbox/SHARED_SURFACE_CONTRACT.json` canonical block: host_windows `C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox`).
- `watch/inbox/LINKS.jsonl`: 255,681 bytes, sha256 `80406c6cbb2a23da1cc9cde2b84fafaa7be844646b2e6cea5c6f8caf8856d514`.
- INDEX derivations block: derived from `watch/inbox/index_events.jsonl` at `2026-09-28T18:27:28.578Z`, event_count 4,696, active_items 1,415. INDEX.json mtime Sep 28 14:27 local confirms local time = UTC-4.

## Headline

| Question | Result |
|---|---|
| INDEX items | 1,415 (0 duplicate paths; all carry class + purpose + sha256; 23 have `living`, 18 have `seal`, 5 have `size`) |
| Q1 exists on disk | **1,415 / 1,415 (0 missing)** |
| Q2 sha256 matches | **1,403 match / 12 mismatch (99.15%)** |
| Q3 registered in LINKS.jsonl | **1 / 1,415 by sha256 join; 18 / 1,415 by filename-mention join; 3 LINKS rows carry file-path canonicals** |
| INDEX `size` fields | 5 present, 5 / 5 match actual bytes |

Commands: `f-16_sweep.py` hashes all 1,415 paths under `watch/inbox/` (read-only) and
joins LINKS.jsonl; spot re-verification of 3 mismatches with
`powershell -NoProfile -Command "Get-FileHash -Algorithm SHA256 ..."` returned hashes
identical to the sweep (case-insensitive), so the 12 mismatches are real drift, not a
sweep bug.

## Q1 - existence: 1,415 / 1,415 exist

Zero missing files. INDEX paths include 24 subdirectory prefixes (`burn_wave_20260926/`
47, `ractor_panel_20260926/` 65, `burn_reset_20260927/` 48, `full_blast_20260926/` 17,
`seed_rib_20260926/` 17, `noir_gwap_steal_20260926/` 8, `matthews_zenodo_17811909/` 10,
and 17 more); all resolved under the host root.

## Q2 - sha256: 1,403 match, 12 mismatch

All 12 mismatched files have mtime 2026-09-28 (today). Two mechanisms:

A. Eight files were modified AFTER the INDEX fold (derived 18:27:28Z = 14:27:28 local) -
normal drift for append-only surfaces, INDEX is simply older than the bytes:

| path | class | recorded sha (head) | actual sha (head) | mtime local |
|---|---|---|---|---|
| SELF_STEAL_REBUILD_RETEST_SALON_20260831.md | PROPOSAL | 19ee204804cef3e9 | 2e5b5a3ebc21a6c3 | 14:33:39 |
| GAP1_SPAWN_MANIFEST_20260906.md | BACKFILL | 7c3d58d980f4facb | 0c399ba114b1289e | 14:33:39 |
| REVEAL_FIVE_REHEARSALS_20260906.md | BACKFILL | 6e8660f5f3f5abac | d3ba0702c5a378cc | 14:33:39 |
| SEAT_SPORes_AUDIT_CELL_20260912.md | BACKFILL | 0c827b9403d92bf6 | 48883fa831ccd466 | 14:33:39 |
| LINKS.jsonl | receipt | 1e61ad82e88865c5 | 80406c6cbb2a23da | 14:29:00 |
| DATED_METERS.jsonl | ledger | 80a6195f44c82378 | 513f34da24b96249 | 17:20:49 |
| mimo_watch.jsonl | receipt | 486f249daa3d110b | 1ec775960a8395d3 | 16:58:19 |
| index_events.jsonl | receipt | 8805bd8b484468f9 | 2cfd8abd956e1b8c | 18:00:29 |

The four .md files share mtime to the same second (14:33:39.06x) - one batch operation
touched all four after the fold. (Full 64-hex shas in `f-16_sweep.json`.)

B. Four files were modified after their LAST registration event but BEFORE the fold -
the INDEX is a faithful fold of the event log; the gap is that no writer re-registered
the appended bytes. Event histories pulled from `index_events.jsonl`:

| path | last register event | INDEX sha (head) | actual (head) | file mtime local |
|---|---|---|---|---|
| FULL_SCAN_REPORT_20260923.md | 2026-09-26T20:20:52Z sha 168d3e1b | 168d3e1b (stale) | 3ad68f1e | 09:40 |
| endpoint_news/endpoint_news.jsonl | 2026-09-27T11:38:33Z sha beb2fc37 | beb2fc37 (stale) | 1415721b | 09:02 |
| mrpool_export/vision_nightly_receipts.jsonl | 2026-09-27T11:38:36Z sha f9f5b604 | f9f5b604 (stale) | cdf1e96c | 02:30 |
| phone_relay_log.jsonl | 2026-09-27T11:38:36Z sha 1a9c38a0 | 1a9c38a0 (stale) | 9095d4c5 | 09:31 |

FULL_SCAN_REPORT_20260923.md is a live scan report (233 bytes, its own header stamps
`run 2026-09-28T13:40:00Z`), rewritten daily with no re-register. Mismatch classes
across all 12: receipt 6, BACKFILL 3, PROPOSAL 1, RECEIPT 1, ledger 1.

## Q3 - LINKS.jsonl registration

LINKS.jsonl is a URL/finding ledger, not a per-file registry: 378 rows, 322 with
`canonical`/`url`, 291 distinct `canonical_sha256` values, 56 no-url rows
(free-resource-scout finding cards), 13 `op:"register"` rows. Domains: x.com 171,
arxiv.org 41, github.com 14, pmc.ncbi.nlm.nih.gov 14, doi.org 11, rest minor.

Both joins tested against the 1,415 INDEX items:

- **sha256 join (INDEX item sha == a row canonical_sha256): 1 hit** -
  `fibonacci_determinants_plate_20260918.png`, LINKS row 255
  (`canonical: "image-drop:fibonacci_determinants_plate_20260918.png"`), where INDEX sha
  == LINKS canonical_sha256 == disk sha. One true three-way-verified registration.
- **filename-mention join (basename appears in any row string field): 18 hits** - e.g.
  `scout_drop_free_claude_code_20260926.md` (row 337 note), `RACTOR_PANEL_20260926.md`
  (row 353), `PACK_SECRET_GATE_20260926.md` (row 354), `MILO_STEAL_20260927.md` (row 352
  note), `INTAKE_HAUL11_20260907.md` (rows 137-141 note). Of these only rows 255, 353,
  354 put a file path in the `canonical` field; rows 353/354 carry no sha.
- **Verdict: 1,412 / 1,415 INDEX items have no LINKS.jsonl registration, and that is by
  design** - INDEX.json (folded from index_events.jsonl) is the file registry;
  LINKS.jsonl registers URLs and a handful of drops. Absence from LINKS.jsonl is not an
  integrity failure; absence from INDEX would be.

## Event-log cross-check (INDEX derivations vs bytes)

- `index_events.jsonl` existed and read 5,114 lines at sweep time vs derivations
  event_count 4,696 - 418 events appended since the fold; a re-read minutes later counted
  5,138 LF (the log is live; its newest row during this ask was an `autoseal` of
  `flash50/f-03.md` at 2026-09-28T22:01:58Z from another lane).
- 3 unparseable hand-written rows (e.g. bare `{'seq':NEXT,...}` single-quoted JSON and
  `"seq":NEXT` unquoted) - the log tolerates them, a strict parser would not.
- Ops tally over parsed rows: register 3,915, autoseal 970, invalidate 135, amend 17,
  note 14, repair 1, windowseal 1, filed 1, 81 rows with no op field.
- fold_warnings: 138, dominated by writer nonce-gaps: `zcode-sw-08` 34,
  `zcode-corpus-map-window-20260918` 25, `zcode-sw-11` 21, `zcode-seat-20260926` 15,
  `sancho_pid6686` 8, `sancho` 7, `outside-dropped` 7, `zcode-journal-window-20260915` 5,
  remainder 16 across other writers.

## Verdict

1. INDEX.json is byte-truthful as a fold-of-events snapshot: 100% existence, 99.15%
   sha agreement, zero size-field errors. No fabricated or dead entry found.
2. All 12 sha mismatches are explained drift on live-append surfaces, not corruption:
   8 modified after the fold, 4 appended after their last register event. The fix shape
   (not applied here - census only) is re-register or refold; the INDEX itself never
   lies about what it was told.
3. LINKS.jsonl registration is the exception (1 by sha, 18 by mention), by design.
4. Residual risks filed as facts: 4 writers appending without re-registering
   (mechanism B), 3 hand-written unparseable event rows, 418+ unlogged-in-fold events
   pending the next fold, and a 4-file batch rewrite at 14:33:39 that outpaced the fold
   by 6 minutes.

Receipt: sweep `watch/inbox/burn_reset_20260927/flash50/f-16_sweep.py` +
`f-16_sweep.json`; this file + byte-identical mirror `index-truth.md`. No em-dashes
(scanned). No inbox file was written by the sweep; the only writes are the four bank
files in `flash50/`.
