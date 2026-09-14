# KPI LEAVES RECON — the 15 kpi-only leaves (idx 6,662-6,676) (2026-09-11)

Lane: zcode wave slot 2. Absorbed (not duplicated): KPI_LEDGER_DECODE_20260911.md (the
15-leaf discovery + its "UNPROVEN content" verdict), SURGERY_FORENSICS_20260911.md,
GHOST_ARITHMETIC_20260911.md. Read-only except this file. Question: are the 15 leaves
recoverable from any on-disk witness, or is dossier_commit re-knotting the only path?

## 1. DO THE LEAVES EXIST ANYWHERE BY INDEX? — NO (measured, 33 chain-like files)

Scanned every verkle*.jsonl + .bak on disk (33 files): 8 dated biography_backup dirs,
2 pre-flag backups, 3 flag backups, postrepair_20260825, repair_backups/verkle_20260831T0212Z,
5 memory/seals/ chains, 3 portable/blast lattices, current chain, AND 8 unindexed
`verkle_chain.jsonl.bak-orphanlane-20260906T2*` snapshots + `bak-batch-20260906T230013Z`
(nine witnesses the decode brief never opened).

Result: the 12 files that reach index 6,676 ALL carry the IDENTICAL rows at 6,661-6,676 —
ts 2026-09-02T23:15:52 → 23:45:01Z, sessions `work:seat:*` / `autonomous-auto-fkb-*`.
Rebuilt idx 6,661 is itself Sep-02: the Aug-31 rebuild renumbered the whole lineage, so
those indices belong to the new trajectory. **Zero files contain index 6662-6676 with an
Aug-28..30 ts.** Pre-cut witnesses all stop ≤6,661 (backup_20260830: 6,661 rows, last
ts Aug-27 23:08:38; orphanlane baks are post-rebuild). The original 15 rows are in no
surviving chain file — absence now measured, not assumed.

## 2. KPI AROUND THE ROWS — the overshoot is ONE 73-minute window, and it oscillates

Streamed logs/kpi.jsonl (ts-filtered; note: kpi lines start `{"schema"`, not ts —
line-prefix filters silently match nothing). All n_leaves transitions Aug-27..31:

- Aug-28 + Aug-29: ZERO transitions — 6,661 pinned, one tip (77f4dccfa85ca85d). Confirms
  the decode brief's freeze at transition granularity.
- **The entire 6,661→6,676 overshoot lives in 2026-08-30T19:18:04Z → 20:43:00Z**, ending
  7 minutes before THE CUT (20:49:56Z, 6,663→4,909). Peak 6,676 at 20:37:17Z.
- The window OSCILLATES: 6661↔6662↔6663 flapping within minutes, multi-leaf jumps
  (6665→6670, 6667→6674, 6674→6676, 6676→6663 in 4 s), repeated drops back to 6,661.
  This is tip-file multi-writer race under concurrent summarize load — the "15 leaves"
  is the MAX transient overshoot of the counter, not 15 durable, ordered rows.
- Session ids: `complete_means` in this era is a DESCRIPTIVE STRING ("residual + card +
  content_commit + chain_leaf"), not a session-keyed dict — refines the decode brief's
  schema note. `incomplete_ids` deltas name completers but the list flaps across writer
  snapshots (43 sessions re-enter 28x), so kpi cannot reliably name the leaf-owning
  sessions. Its n_sessions/n_complete counters rise monotonically through the window
  (2349→2396 / 1469→1529) while leaves flap — counters and chain-length see different
  writers. 18 single-exit `mag-agent-orc-*` sessions did complete in the window, but the
  ones traceable into the backup chain are OLD amended rows (e.g. orc-t3e82fd8a17 = idx
  307, ts Aug-23, amended:true) — dossier paperwork, not the lost appends.

## 3. THE NEW FINDING — the primary sources SURVIVE on disk: 217 ghost-band knots

`memory/biography/knots/` holds **217 knot files with mtime Aug-28..30**, filename-stamped
2026-08-30_1906Z → 2048Z — the same wall-clock window as the overshoot (plus 7 backdated
Aug-02 pytest knots rewritten in-band; no knots named Aug-28/29, matching the freeze).
Each knot carries `leaf_hash`, `session_id`, `dossier_commit`, full theme vectors —
the exact chain-input artifacts, stronger than dossiers.

Cross-check by leaf_hash/filename against both chains:
- **25/217 already re-chained** in the current rebuilt chain (recovered by the
  rebuild/backfill, unknown which pass).
- 0/217 in the pre-cut backup (expected — post-backup appends).
- **192/217 in NEITHER chain — orphaned primary sources sitting on disk right now.**

The 15 lost leaves' knots are a SUBSET of these 192 (exact membership indeterminable:
knot≠leaf 1:1 — the knots dir holds 28,910 files vs 7,392 chain rows; most knots are
never chained). But the recovery path is no longer "dossier_commit re-knotting only":
the chain-input knots themselves survived the surgery that killed their rows.

## VERDICT (tri-state)

- **SUPPORTED — the 15 original rows are unrecoverable as rows.** No chain file (33
  scanned, incl. 9 previously unindexed orphanlane/batch snapshots) holds idx 6,662-6,676
  with pre-Sep-02 ts; the rebuilt lineage owns those indices with Sep-02 content; kpi
  tip_roots are not row-comparable (decode brief's DISPUTED finding, unchallenged here).
- **SUPPORTED (upgraded from UNPROVEN) — the CONTENT of the ghost-band appends is
  recoverable: 217 knot files from the exact window survive at
  memory/biography/knots/ (2026-08-30_19*Z..20*Z), 192 of them in no chain.** A re-knot
  pass over the 192 orphans (dedupe against the 25 already chained by leaf_hash) would
  restore whatever the surgery dropped; the original index positions/roots do not
  survive and should not be faked.
- **DISPUTED — the brief's "appends on Aug-28..30".** Aug-28/29 are transition-silent at
  6,661 with zero new knots; all overshoot witnesses compress into Aug-30 19:18-20:43Z,
  and the counter's oscillation means "15 leaves" is a peak transient, not 15 verified
  durable rows. The honest count of lost durable leaves is UNPROVEN (0..15); the 6,676
  peak is a fact of the tip file, not proof 15 rows persisted.

## FALSIFIERS

- If any witness shows a STABLE n_leaves >6,661 for more than one consecutive kpi row
  span before 20:37Z (e.g. a backfill-source snapshot at 6,67x), the "transient peak"
  reading is wrong and ≥that-many durable rows existed.
- If the 192 orphaned knots' leaf_hashes are shown to hash-verify as already-chained
  content (duplicate knots of chained sessions), the "recoverable content" claim shrinks
  to near-zero.
- If the Aug-31 rebuild's dossier walk is shown to have consumed exactly these knots and
  rejected them (rejection log), they are evidence-tested orphans, not recoverables.

## Receipts (primary)

33 chain-like files scanned (paths in recon log; key: memory/biography/verkle_chain.jsonl
[7,392 rows now, growing], .bak-orphanlane-20260906T224709Z..225537Z x7 + bak-batch
[x2 shapes], memory/biography_backup/biography_backup_20260830/verkle_chain.jsonl
[6,661 rows, last ts Aug-27 23:08:38Z], memory/biography/repair_backups/verkle_20260831T0212Z/
[4,912 rows]) · logs/kpi.jsonl streamed window 2026-08-27..31 (6,580 rows parsed, 0 bad) ·
transitions table above · memory/biography/knots/ (28,910 files; 217 mtime Aug-28..30;
192 orphaned by leaf_hash cross-check; e.g. 2026-08-30_1943_untagged_memlang-_61ed8d4e.knot.json,
leaf_hash 61ed8d4e..., session memlang-daemon-194307729739) · absorbed:
watch/inbox/KPI_LEDGER_DECODE_20260911.md.

## CYCLE GENETICS

What worked: scanning by INDEX+TS across every backup (not just the named ones) turned
"exists in NO file" from an assumption into a measurement; the knots-dir mtime sweep was
the single highest-yield probe — the recovery witness was never in a chain file at all.
What to change: kpi line-prefix ts filtering silently matches nothing (kpi starts
`{"schema"`) — filter on the ts substring, and budget one schema-peek row before any
field-level parse (complete_means is prose, cost me one pass); next slot should inherit
the "enumerate witnesses beyond the named ones first" instinct as a standing move.

Filed by kpi-leaves-recon worker (zcode wave slot 2, read-only except this file, 2026-09-11).
