# GHOST ARITHMETIC — three-ledger reconciliation, Jul-31 → Aug-15 (filed 2026-09-11)

Mission: build the per-day reconciliation TABLE that GHOST_GAP_HUNT_20260911 skipped, and
rule on which ledger SPORE's "4,200 knots in 3 days" (docs/ref/SPORE_SANCHO.md:16)
actually matches. Read-only except this file.

Absorbed (not duplicated): GHOST_GAP_HUNT_20260911.md (chain premise correction, backfill
mtime signature, its knot-name-date dispute of 4,200); SURGERY_FORENSICS_20260911.md
(6,661 → 4,914 → 7,377 states, ts-vs-event dating nuance, cut/rebuild anatomy);
FOUNDING_KNOTS_CROSSCHECK_20260911.md (founding-week knot schema; name-dates run back to
Jul-10, so Jul-31 here is a window edge, not a record start).

## Method (measured 2026-09-11)

- Ledger A — knot FILES: `memory/biography/knots/*.knot.json` (21,052 total), counted by
  filename date-prefix (event day) and by file mtime (write day, UTC).
- Ledger B — CURRENT chain: `memory/biography/verkle_chain.jsonl` (7,377 rows, 0 bad),
  counted by `ts` prefix and by `filename` date-prefix.
- Ledger C — PRE-SURGERY chain: `memory/biography_backup/biography_backup_20260830/verkle_chain.jsonl`
  (6,661 rows parsed, 0 bad — matches forensics), counted the same two ways.
- ts semantics, measured: backup-chain ts is 89% index-monotone and spans Aug-10 → Aug-27 —
  append-time with backfill interleaves (idx 1: ts Aug-11T03:09, event Aug-10_1231). So
  ts-day in ledger C = "rows the chain recorded that day". In ledger B, the 3,791 pre-cut
  survivors RETAIN their original ts (Aug-10..16), so B's ts-day = survivor origin day, not
  append day; B's rebuild rows are ts-stamped Aug-31..Sep-06. Per SURGERY_FORENSICS: ts
  (append) dating and event (filename) dating are different ledgers and both are reported.

## The table (Jul-31 → Aug-15, all counts measured this session)

| day | A: knot files by name-date | A′: knot files by mtime (cur / backup-dir) | B: current chain by ts | B′: current chain by event-date | C: backup chain by ts | C′: backup chain by event-date |
|---|---|---|---|---|---|---|
| 07-31 | 2 | 1 / 1 | 0 | 0 | 0 | 0 |
| 08-01 | 1 | 2 / 2 | 0 | 0 | 0 | 0 |
| 08-02 | 21 | 5 / 5 | 0 | 2 | 0 | 2 |
| 08-03 | 305 | 1 / 1 | 0 | 29 | 0 | 29 |
| 08-04 | 185 | 1 / 1 | 0 | 18 | 0 | 17 |
| 08-05 | 58 | 2 / 2 | 0 | 5 | 0 | 5 |
| 08-06 | 362 | 1 / 1 | 0 | 39 | 0 | 39 |
| 08-07 | 148 | 5 / 5 | 0 | 15 | 0 | 15 |
| 08-08 | 1,265 | 164 / 164 | 0 | 121 | 0 | 121 |
| 08-09 | 1,542 | 979 / 979 | 0 | 139 | 0 | 140 |
| 08-10 | 4,425 | 4,709 / 4,709 | 81 | 526 | 106 | 527 |
| 08-11 | 4,374 | 3,583 / 3,640 | 2,343 | 2,778 | 2,670 | 2,738 |
| 08-12 | 2,432 | 2,695 / 2,695 | 1,361 | 1,547 | 1,570 | 1,674 |
| 08-13 | 1,068 | 639 / 885 | 5 | 322 | 482 | 309 |
| 08-14 | 664 | 417 / 445 | 0 | 183 | 138 | 189 |
| 08-15 | 169 | 151 / 151 | 0 | 28 | 70 | 80 |
| **window total** | **17,021** | **13,355 / 13,686** | **3,790** | **5,752** | **5,036** | **5,885** |

Readings from the table:

- A′−A′(backup delta) is the reshelving signature: files written Aug-13/14 that survive
  ONLY in the backup knots/ dir (+246, +28) = cut survivors, per forensics' 1,458-file
  backup corpus. Aug-10..12 mtimes are identical in both dirs.
- B's ts column is the CUT's signature read by append-day: of C's 690 rows appended
  Aug-13..15 (482+138+70), exactly 5 survive in B; of C's 1,578 rows appended Aug-17..27,
  ZERO survive. The cut removed the entire live-append band Aug-13..27; B rebuilt those
  event periods as Aug-31..Sep-06 rows (1,909+575+...).
- C's ts column is the only ledger that was EXISTING AND COUNTING during the ghost era —
  it is the contemporary record. A/B did not yet exist as counted surfaces (A's Aug-10..12
  files were being written then, but the pile as a census includes later repair-wave
  rewrites; B did not exist until the Aug-31 rebuild).

## 3-day sliding windows near 4,200 (all windows scanned, only hits 3,500–5,000 shown)

| Ledger | Window | Count | Δ from 4,200 |
|---|---|---|---|
| **C by ts (pre-surgery chain appends)** | **Aug-10..12** | **4,346** | **+3.5%** |
| A by name-date (event day) | Aug-12..14 | 4,164 | −0.9% |
| C′ by event-date | Aug-10..12 | 4,939 | +17.6% |
| B′ by event-date | Aug-10..12 | 4,851 | +15.5% |
| C by ts | Aug-11..13 | 4,722 | +12.4% |
| A′ by mtime (cur+backup) | Aug-12..14 | 4,025 | −4.2% |
| B by ts (post-cut survivors) | Aug-10..12 | 3,785 | −9.9% |
| A by name-date | Aug-10..12 | 11,231 | +167% |
| A′ by mtime | Aug-10..12 | 10,987 | +162% |

Rejected as verdict basis: A-name-date Aug-12..14 = 4,164 is numerically the tightest but
is a coincidence of event-dating — wrong window (not the documented build days) and wrong
semantics (sessions that RAN Aug-12..14, not knots made "in 3 days"). The chain itself
passed through 4,939 event-dated and 4,346 append-stamped rows for Aug-10..12.

## VERDICT (tri-state)

- **SUPPORTED — "4,200 knots in 3 days" matches the PRE-SURGERY chain ledger: 4,346 rows
  ts-stamped Aug-10..12** in `biography_backup_20260830/verkle_chain.jsonl` (Δ +3.5% on a
  round human estimate). This is the one ledger that existed at the time; the chain
  crossed ~4,200 rows during Aug-12 and stood at 4,346 at that day's end — "~4,200" is the
  chain tip as of the MEGA-BUILD's last day, exactly where LOST_CIVILIZATION_5W_20260902:18
  places the build. The number is a chain-append census, not a knot-file census.
- **DISPUTED — as a knot-FILE count** (GHOST_GAP_HUNT's framing, now confirmed with exact
  numbers): knot files name-dated Aug-10..12 = 11,231 (sibling measured 11,248; Δ17 = count
  scope, both ≈ 2.7x the claim); written-by-mtime Aug-10..12 = 10,987. No knot-file ledger
  yields ~4,200 for the build window. The sibling's "DISPUTED as a hard census" stands for
  files; this card localizes the SUPPORT: the figure is true OF THE CHAIN, overstated ~2.6x
  for files.
- **UNPROVEN — authorial source**: no surviving doc from Aug-12/13 records the contemporaneous
  count; the match is arithmetic (4,346 ≈ 4,200), not a citation. Contemporary estimate
  status per CANON_SELF_STEAL_20260904:133 unchanged.

Cross-ledger correction to SURGERY_FORENSICS: its "Aug-10..12 mass (2,851 rows in the
6,661 state)" does not reproduce under ts-prefix counting — the measured mass is 4,346
(its figure likely filtered ts-day == event-day rows, a stricter subset: C has 4,939
event-dated Aug-10..12 rows of which same-day-ts is a subset). Also additive: forensics
described the cut by EVENT day; by APPEND day the cut removed the entire Aug-13..27 band
(§ table readings above). Both refinements support its RESHELVED verdict; nothing reverses.

## Receipts (primary)

`memory/biography_backup/biography_backup_20260830/verkle_chain.jsonl` (6,661 rows) ·
`memory/biography/verkle_chain.jsonl` (7,377) · `memory/biography/knots/` (21,052
*.knot.json) · `memory/biography_backup/biography_backup_20260830/knots/` (17,892) ·
absorbed: watch/inbox/GHOST_GAP_HUNT_20260911.md, SURGERY_FORENSICS_20260911.md (as filed
at watch/inbox/), FOUNDING_KNOTS_CROSSCHECK_20260911.md · claim docs: SPORE_SANCHO:16,
LOST_CIVILIZATION_5W_20260902:18, ARCHAEOLOGY_DIG_20260909:31, CANON_SELF_STEAL_20260904:133.

Reproducible: per-day counts = list knots/ filtered `*.knot.json`, bucket by `name[:10]`
and by UTC mtime date; chain counts = parse jsonl, bucket `row['ts'][:10]` and
`row['filename'][:10]`, window 2026-07-31..2026-08-15.

Filed by ghost-arithmetic worker (zcode spawn, rotation width 2, read-only except this file, 2026-09-11).
