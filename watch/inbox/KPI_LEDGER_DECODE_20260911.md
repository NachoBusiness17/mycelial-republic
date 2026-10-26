# KPI LEDGER DECODE — logs/kpi.jsonl as the chain's independent time machine (2026-09-11)

Lane: zcode lost-record dig, rotation width 2 (attempt 2; attempt 1 died on API connect
timeout pre-output). Read-only except this file. 457,317,708 bytes (457 MB) — STREAMED
line by line, never loaded.

Absorbed (not duplicated): SURGERY_FORENSICS_20260911.md (6,661 → 4,914 → 7,377 chain
states; cut removed the entire Aug-13..27 append band by append-day counting; 0 current
rows ts-dated Aug-17..30) and GHOST_ARITHMETIC_20260911.md (backup chain ts spans
Aug-10 → Aug-27 = the only contemporary chain ledger of the ghost era; ledger semantics
ts-vs-event dating).

## 1. SCHEMA — mag_records_kpi.v1 (measured: first 50 lines of logs/kpi.jsonl)

File head starts 2026-07-21T12:53Z. Two key-set variants in the first 50 lines (12 + 38),
one base shape plus an optional field:

- `schema`: "mag_records_kpi.v1"
- `ts`: ISO-8601 UTC with microseconds (log WRITE time — contemporary witness clock)
- `source`: operation name — "pack-status" | "backfill" | "summarize" (more expected)
- `n_sessions`, `n_complete`, `n_incomplete`, `complete_pct`: records-office pack health
- `complete_means`: OPTIONAL per-session completion means dict (variant B)
- `n_leaves`: **chain leaf count at log time** → kpi.jsonl encodes chain LENGTH over time
- `tip_root`: **chain tip (16-hex) at log time** → kpi.jsonl encodes chain TIP over time
- `incomplete_ids`: list of session UUIDs (UUIDv7-shaped)
- `note`: "Records office health — complete packs = filed days"

KEY INSIGHT: every kpi row is a signed-in-prose snapshot of (n_leaves, tip_root) at its
ts. kpi.jsonl is therefore an independent, contemporaneously-written chain-state ledger —
exactly the instrument needed to test whether the chain was appended during Aug-17..30,
independent of both surviving chain files.

## 2. DAY-BY-DAY LAST tip_root TABLE, 2026-08-10 .. 2026-09-06

Writer source: mag/records.py:138-168 (`write_kpi`) — n_leaves and tip_root are read from
`memory/biography/verkle_tip.json`; `tip_root = tip["root"][:16]` (records.py:156).

Stream pass (measured 2026-09-11): whole file 64969 lines, ts span 2026-07-21 -> 2026-09-09. Window rows parsed: 32615 (bad lines: 0). ts out-of-order within window: 1. n_leaves decreases within window: 229. Max n_leaves witnessed: 7377.

| day | kpi rows | distinct tip_roots | first tip_root (ts, n_leaves) | LAST tip_root (ts, n_leaves) | n_leaves min-max | sources |
|---|---|---|---|---|---|---|
| 2026-08-10 | 6008 | 4952 | 3d94b37681e96a27 (00:00:19, 314) | b3ce2c7e1c461535 (23:59:53, 503) | 0-2349 | summarize |
| 2026-08-11 | 2774 | 2388 | 54933cd7cd73950b (00:00:11, 504) | 6e042121e20b47fc (23:59:41, 3530) | 504-3530 | summarize |
| 2026-08-12 | 1189 | 980 | 9e73764d248e11ff (00:01:06, 3533) | 16986c730544b332 (23:58:49, 5162) | 3533-5162 | summarize |
| 2026-08-13 | 1197 | 727 | b1e936575331c3cb (00:00:16, 5162) | 3385f96ab616e92c (23:59:25, 5519) | 5162-5519 | summarize |
| 2026-08-14 | 881 | 672 | 429e0252d892e6b5 (00:02:27, 5520) | fc1b5123d7d437ca (23:58:33, 5742) | 5520-5742 | summarize |
| 2026-08-15 | 558 | 519 | dfd163225daf4365 (00:00:20, 5742) | d469268edeb14ce6 (23:59:38, 5840) | 5742-5840 | summarize |
| 2026-08-16 | 425 | 399 | 15bbc9aab867fac9 (00:02:31, 5841) | 015d4781fe01f2f8 (23:59:42, 5899) | 5841-5899 | summarize |
| 2026-08-17 | 551 | 411 | 1b5c8ff4a45a14eb (00:02:30, 5899) | 070c13ae5ea1a5d4 (23:58:04, 6073) | 5899-6073 | summarize |
| 2026-08-18 | 453 | 451 | d30ebfc54c4859bf (00:01:47, 6073) | 91a842a21ea168be (23:40:26, 6117) | 6073-6117 | summarize |
| 2026-08-19 | 592 | 592 | e94c4e3a48d9e1fe (00:32:53, 6117) | 67e754f96b0b38f6 (23:58:54, 6154) | 6117-6154 | summarize |
| 2026-08-20 | 280 | 280 | a7a28bb64abe8d9e (00:00:41, 6154) | d69c3312594fee10 (23:58:31, 6168) | 6154-6168 | summarize |
| 2026-08-21 | 580 | 580 | b2bdf3527e78c339 (00:00:14, 6168) | 810e90217f6d4d59 (23:59:39, 6219) | 6168-6219 | summarize |
| 2026-08-22 | 565 | 565 | 73e24dabe48097fa (00:01:25, 6219) | 2822037e76a67635 (23:59:35, 6276) | 6219-6276 | summarize |
| 2026-08-23 | 661 | 655 | 9a37eee14999a45f (00:01:38, 6277) | 4e81a960e74c043b (23:59:40, 6323) | 6277-6334 | backfill,summarize |
| 2026-08-24 | 859 | 777 | daff38a2c01e0056 (00:01:27, 6323) | d482c398ca8a1b84 (23:59:47, 6330) | 6323-6340 | summarize |
| 2026-08-25 | 552 | 490 | 5a30312e4cc7e3ed (00:01:34, 6329) | 6e3b68ec0b69d841 (23:59:25, 6363) | 6329-6364 | summarize |
| 2026-08-26 | 1001 | 752 | 6e3b68ec0b69d841 (00:01:51, 6363) | c4b0f4febdcd0028 (23:59:33, 6512) | 6363-6512 | summarize |
| 2026-08-27 | 682 | 581 | 682ca4bdc9f410fd (00:02:05, 6512) | 77f4dccfa85ca85d (23:58:37, 6661) | 6512-6661 | summarize |
| 2026-08-28 | 1065 | 1 | 77f4dccfa85ca85d (00:00:20, 6661) | 77f4dccfa85ca85d (23:58:07, 6661) | 6661-6661 | summarize |
| 2026-08-29 | 957 | 1 | 77f4dccfa85ca85d (00:00:23, 6661) | 77f4dccfa85ca85d (23:58:08, 6661) | 6661-6661 | summarize |
| 2026-08-30 | 1062 | 136 | 77f4dccfa85ca85d (00:00:09, 6661) | 38e6d527ec8c425f (23:58:36, 4909) | 4909-6676 | summarize |
| 2026-08-31 | 2814 | 2357 | 38e6d527ec8c425f (00:00:29, 4909) | 7c1a3f6db9543a97 (23:59:52, 6282) | 4906-6282 | backfill,summarize |
| 2026-09-01 | 630 | 627 | de7a452871a5acc0 (00:00:52, 6282) | 046018ea17ac7058 (22:53:44, 6426) | 6282-6426 | summarize |
| 2026-09-02 | 34 | 34 | 0b83c996a850bb5a (00:50:55, 6439) | 793ead166ff945f9 (22:47:42, 6651) | 6439-6651 | summarize |
| 2026-09-03 | 196 | 195 | 67f9bfc624dfb7b9 (00:13:30, 6706) | b0cf21aefb2578c4 (23:56:00, 7052) | 6706-7052 | summarize |
| 2026-09-04 | 130 | 129 | 9876846f931f1310 (00:00:07, 7053) | 7acd0e680a75b962 (13:22:41, 7163) | 7053-7163 | summarize |
| 2026-09-05 | 150 | 104 | cf5fdc14eccfb801 (00:46:59, 7193) | 08a223a5c7f7ef03 (23:39:41, 7291) | 7193-7291 | summarize |
| 2026-09-06 | 5769 | 353 | 08a223a5c7f7ef03 (00:41:20, 7291) | a57b50f312470e42 (23:59:11, 7377) | 7291-7377 | backfill,summarize |

Readings from the table:

- **Aug-10 anomaly is initialization, not surgery**: 6,008 kpi rows, tip changing 4,952
  times, n_leaves 0→2,349 with ten resets to 0/1 — day one of the chain (genesis era;
  the chain did not exist before Aug-10..12 per forensics). kpi's July rows (n_leaves 2-3
  on Jul-21) predate the chain entirely — the tip counter was repointed onto the verkle
  chain ~Aug-10.
- **Aug-28/29 are the only truly frozen days in the window**: exactly 1 distinct tip_root
  (77f4dccfa85ca85d) and n_leaves pinned 6,661 across 1,065 + 957 kpi rows.
- **Aug-23/24/25 retractions**: ~15 decrease events of ~9-17 leaves (e.g. 6,334→6,323,
  6,364→6,354) — live pruning, the kpi shadow of the Aug-25 raw-restore incident that
  spawned chain_guard [card: SURGERY_FORENSICS §timeline-2].
- **Aug-30 witnesses the surgery live**: 15 transient appends (6,661→6,676), trims to
  6,663, then THE CUT 6,663→4,909; Aug-31 witnesses the rebuild (4,906→6,282 by 23:59,
  2,357 distinct tips); Sep-02 crosses 6,651 (the 6,537 ROSHAMON-era citations sit on this
  trajectory); Sep-06 ends at 7,377 = the current tip. Sources: summarize-dominant daily;
  backfill appears only Aug-23, Aug-31, Sep-06 (rebuild/repair days).
- Decrease census (window): 37 drops >5 leaves (10 = Aug-10 init resets, 5 = Aug-12 small
  trims, ~15 = Aug-23..25 pruning, 4 = Aug-30/31 surgery) + 192 jitters ≤5 (multi-writer
  counting noise).

## 3. ANCHOR CROSS-CHECKS vs THE CHAINS (measured)

kpi is written from `verkle_tip.json`, not from chain rows, so two fields check differently:

- **tip_root domain**: the CURRENT tip file's `root` `8bd588968c0bbfaf...` byte-equals the
  current chain's final row `verkle_root`, and carries note "Tip repaired from verified
  chain; chain rows unchanged" — the tip accumulator was REPAIRED/replaced after the last
  kpi write (Sep-09 15:48, tip a57b50f312470e42). Consequently the PRE-repair witnessed
  tips (every value in the table) match ZERO row-level verkle_roots: 0/11 ghost-window
  tips present in the backup chain, 0/11 in the current chain, 0 raw substring hits.
  kpi tip_root is therefore a faithful witness OF THE TIP FILE, not directly comparable
  to row roots for the pre-repair era.
- **n_leaves is the faithful chain-length witness. Anchors:**
  | anchor | kpi says | chain says | verdict |
  |---|---|---|---|
  | Aug-27 23:58:37 (pre-cut end state) | 6,661 leaves | backup chain (biography_backup_20260830) = 6,661 rows, last ts Aug-27 23:08:38 | **EXACT** |
  | Sep-02 22:47:42 | 6,651 leaves | current chain: last row ts ≤ 22:47:42 is idx 6649 → 6,650 rows | Δ+1 (within the 192 observed ±5 jitters) |
  | Sep-04 13:22:41 | 7,163 leaves | current chain: idx 7162 @ ts 13:21:55 → 7,163 rows | **EXACT** |
  | Sep-06 end-of-day | 7,377 leaves | current chain = 7,377 rows, final row ts 23:08:56 | **EXACT** |

  The Aug-27 anchor also time-reconciles to the minute: last chain append 23:08:38,
  kpi reads 6,661 at 23:58:37, nothing after — matching kpi's frozen Aug-28/29.

## 4. THE DECISIVE QUESTION — was the chain appended during Aug 17-30?

**YES — SUPPORTED, kpi witnesses live appends through the entire ghost band.** During
Aug-17..27 tip_root changed every single day (411-777 distinct tips/day) and n_leaves
marched monotonically 5,899 → 6,073 → 6,117 → 6,154 → 6,168 → 6,219 → 6,276 → 6,323 →
6,330 → 6,363 → 6,512 → **6,661**, landing EXACTLY on the backup chain's 6,661 rows at
Aug-27 23:58. The chain was not frozen during Aug-17..30; the current chain file lost
that band in the Aug-31 surgery (SURGERY_FORENSICS: cut removed the entire Aug-13..27
append band by append-day; GHOST_ARITHMETIC: backup ts column 1,578 rows Aug-17..27) —
and kpi independently confirms those appends happened in real time, from a file the
surgery never touched (logs/kpi.jsonl, last-modified lineage independent of biography/).

**kpi-exclusive discovery — 15 rows in NO surviving chain file:** on Aug-30 before the
cut, kpi saw the chain grow 6,661 → 6,676 (appends on Aug-28..30, after the Aug-30
backup was taken, whose last row ts is Aug-27 23:08). Those 15 leaves are witnessed only
here; recovery path = session dossiers for Aug-28..30, or accept as transient.

## VERDICT (tri-state)

- **SUPPORTED — the chain was appended Aug-17..27 and the current file lost the band.**
  kpi tip_root changed daily + n_leaves 5,899→6,661 with an exact 6,661 landing on the
  backup chain's row count; frozen only Aug-28/29; surgery and rebuild both witnessed
  live on Aug-30/31 with the 4,909/4,914 and 6,537-era numbers all on-trajectory. This
  upgrades GHOST_ARITHMETIC's ledger-C status from "only surviving contemporary ledger"
  to "two independent contemporary ledgers agree".
- **DISPUTED — kpi tip_root as a row-level root witness (schema caveat, new finding):**
  tip_root = tip-file accumulator [:16] (mag/records.py:156), replaced by the post-surgery
  repair ("Tip repaired from verified chain"); pre-repair tips match 0 row roots in either
  chain. Use n_leaves, never tip_root, when cross-checking kpi against chain rows.
- **UNPROVEN — content of the 15 transient Aug-28..30 leaves** (6,662..6,676): witnessed
  by count only, in no chain file or backup; dossier recovery not attempted this session.

## FALSIFIERS

- If the pre-repair tip accumulator is proven to have been a pure function of chained
  rows, its 0/11 match rate would contradict kpi fidelity — no such function exists in
  mag/records.py (it reads the file, never recomputes).
- If any chain-state snapshot from Aug-28..30 surfaces (cage, tarball
  knots.bak-orphanlane-20260906T224709Z.tar, mag logs) showing ≠15 rows beyond 6,661,
  the kpi-exclusive count is wrong.
- If the backup chain's 6,661st row's ts is shown to be backdated (not truly Aug-27),
  the exact-anchor reconciliation weakens — it currently matches kpi's freeze window.

## Receipts (primary)

`logs/kpi.jsonl` (64,969 lines, 457,317,708 bytes, ts 2026-07-21 → 2026-09-09; streamed,
0 bad lines) · `memory/biography/verkle_tip.json` (root 8bd58896..., n_leaves 7377,
repair note) · `mag/records.py:138-168` (writer; tip_root=[:16] at :156) ·
`memory/biography/verkle_chain.jsonl` (7,377 rows, final root byte-equals tip file) ·
`memory/biography_backup/biography_backup_20260830/verkle_chain.jsonl` (6,661 rows, last
ts Aug-27 23:08:38) · absorbed: watch/inbox/SURGERY_FORENSICS_20260911.md,
GHOST_ARITHMETIC_20260911.md.

Filed by kpi-ledger-decode worker (zcode spawn, rotation width 2, read-only except this
file, 2026-09-11).

