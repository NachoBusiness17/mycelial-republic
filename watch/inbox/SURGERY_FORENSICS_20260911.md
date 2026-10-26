# SURGERY FORENSICS — the 2026-08-31 verkle chain cut + rebuild

Date: 2026-09-11 · Lane: zcode research worker · Method: read-only byte-level diff of every
chain state that survives on disk. No claim below is taken from prose without a measurement
behind it; prose citations marked [card], measurements marked [measured].

## VERDICT (tri-state, up front)

- **DESTROYED vs RESHELVED: RESHELVED (SUPPORTED), with a bounded lost-file inventory.**
  The surgery removed 2,876 chain rows across two phases, but (a) 1,452 of the cut rows'
  knot files survive on disk today as the dated-orphan pile, (b) the rebuild re-knotted the
  same event periods into 3,586 fresh rows whose files exist (3,585/3,586 on disk), and
  (c) every removed row's full metadata (leaf_hash, session_id, dossier_commit, ts) survives
  verbatim in `memory/biography_backup/biography_backup_20260830/verkle_chain.jsonl`.
- **"Zero rows dated Aug 16-30": DISPUTED as stated, SUPPORTED under one reading.** True for
  `ts` (append-time) dating: 0 rows appended Aug-17→Aug-30 (1 row Aug-16). False for
  event-date (filename) dating: 249 current rows carry event dates Aug-16→Aug-30. The only
  hard event-date hole is **Aug-19..22** (4 days, 178 orphan files cover them) [measured].
- **Provably unrecoverable: nothing at the record level; ~304 knot files + 18 chained
  filenames absent from audited disk locations, all with surviving metadata** [measured].
- Prior record's numbers 6,661 → 4,914 → 6,537: **SUPPORTED** — 6,661 and 4,914 verified
  byte-exact on disk; 6,537 consistent with the rebuild finishing Sep-01/02 [measured+card].

## SOURCE STATES (all measured this session)

| State | File | Rows | Integrity |
|---|---|---|---|
| Pre-cut (Aug-30 backup) | `memory/biography_backup/biography_backup_20260830/verkle_chain.jsonl` | **6,661** (0 bad lines) | clean parse; matches ROSHAMON card's "6,661 rows" [card: ROSHAMON_REBUILD_20260902.md:61] |
| Mid-surgery snapshot | `memory/biography/repair_backups/verkle_20260831T0212Z/verkle_chain.jsonl` ≡ `memory/biography_backup/biography_backup_20260831/verkle_chain.jsonl` (sha256-identical, `1e0d5b66ec417590`) | **4,912 parsed + 2 truncated lines = 4,914** | 2 corrupt mid-write lines (idx ~2288, ~4901-4907); indices renumbered 0..4908, gap only at 2287-2290 (the corrupt zone) |
| Current chain | `memory/biography/verkle_chain.jsonl` | **7,377** (0 bad) | 7,376/7,376 parent links intact, 0 duplicate filenames, 0 duplicate leaf_hash, 0 duplicate verkle_root |

Cross-check: the Sep-01 audit measured 6,312 knots mid-rebuild at 02:29Z [card:
AUDIT_C_VERKLE_20260901.md §2]; the Sep-02 cards cite 6,537 [card: FOUR_STRATA_SELF_STEAL_20260902.md:29,
LINEAGE_WALL_20260902.md:17]. Trajectory 4,914 → 6,312 (Sep-01 early) → 6,537 (Sep-02) → 7,377 (Sep-06+) is monotone and consistent.

## TIMELINE (as the data supports it)

1. **Aug-10 → Aug-30, live appends.** The original chain grew one leaf per session, ts
   Aug-10..Aug-30 (4,914-state rows are ALL ts-dated in this window; event days span
   Aug-02..Aug-30). The Aug-10..12 mass (2,851 rows in the 6,661 state) is the MEGA-BUILD
   ("~4,200 knots in 3 days") [card: LOST_CIVILIZATION_5W_20260902.md:18].
2. **Aug-25 ~13:38 — prior incident, not this surgery.** A raw restore outside verkle_lock
   reverted the chain to a pre-repair lineage (1,039 evidence_lost flags → 0); this spawned
   `mag/chain_guard.py` [card: mag/chain_guard.py:1-11]. Repair state marked Aug-26 15:01Z,
   `evidence_lost_expected: 1031`, note "flag landed on 264d0ba3 (knot missing)" [measured:
   memory/biography/verkle_repair_state.json]. Knots were already going missing BEFORE Aug-31.
3. **Aug-30/31 — THE CUT (6,661 → 4,914).** 1,762 distinct filenames dropped (6,661 − 4,899
   kept; the record's "1,747 removed rows" [card: ROSHAMON_REBUILD_20260902.md §G] is the same
   event counted by rows vs filenames — 6,661 rows contain 3 byte-identical dup rows per the
   ROSHAMON fold's own measurement). Survivors renumbered 0..4908. Cut concentrated on event
   days Aug-11..17 and Aug-26..27 (e.g. Aug-12: 296, Aug-13: 309, Aug-14: 189, Aug-17: 176,
   Aug-26: 146, Aug-27: 151) [measured]. Snapshot frozen 02:12Z Aug-31 (dir name) and copied
   twice (repair_backups + biography_backup_20260831).
4. **Aug-31 → Sep-01 — THE REBUILD (4,914 → 6,537).** Dropped 1,114 more rows (event days
   Aug-03..12 + 2 on Aug-30; **83% amended (922), 602 evidence_lost (54%)** — this was the
   corrupted core) and appended 3,586 fresh rows (ts: 1,909 on Aug-31, 575 Sep-01, remainder
   through Sep-06), re-knotting event days Aug-02 → Sep-06 from source sessions. All 3,586
   new filenames distinct; 3,585/3,586 files on disk; **0 files pre-date the surgery** (0
   present in the Aug-30 backup knots/ dir) — they were created by the rebuild [measured].
5. **Sep-01..06 — live growth** to 7,377 by Sep-06 (last knot ts Sep-06, tip n_leaves 7377
   [measured: verkle_tip.json]).

Current chain composition: **3,791 rows (51.4%) are verbatim pre-cut survivors** (amended
flags byte-stable: 0 changes between states); **3,586 rows (48.6%) are rebuild re-knots.**
3,791 + 1,114 = 4,905 distinct = the mid-surgery state. Every number reconciles [measured].

## WHAT LEFT THE CHAIN (itemized, two phases)

**Cut phase, 1,762 rows:**
- 1,458 knot files survive in `biography_backup_20260830/knots/`; 1,452 survive in the
  CURRENT `memory/biography/knots/` — i.e. they are inside the dated-orphan pile today.
- **304 knot files found in neither knots dir** — file gone, row metadata intact in the
  6,661 backup (leaf_hash + session_id + dossier_commit give a recovery path).
- Cut-dropped rows: 631/1,762 amended, 420 evidence_lost.

**Rebuild phase, 1,114 rows dropped:**
- 1,106/1,114 knot files absent from disk; 8 remain.
- These were the sick rows: 922 amended, 602 evidence_lost — and the repair state expected
  exactly this class of damage (`evidence_lost_expected: 1031`, marked Aug-26) [measured].
- Their event periods were re-knotted: rebuild-added rows cover Aug-02..12 at equal or
  greater depth than what was dropped (e.g. Aug-10: 436 dropped → 440 added; Aug-12:
  16 dropped → 185 added) [measured].

## WHY THE ORPHAN PILE ENDS EXACTLY AUG-31 (the reshelving signature)

Dated orphan knot files (on disk, never referenced by any chain row): **13,693**, spanning
2026-07-10 → 2026-08-31 (only 3 on Aug-31), = 21,479 non-chain files in knots/ minus 7,786
by-session files [measured; reconciles the mission's 13,693 exactly]. After the surgery,
every dated knot written was chained (Aug-31 event-dated files: 310/313 chained). The pile
is the pre-surgery backlog: knots written Jul-10..Aug-31 that the old chain never indexed
(knot grammar indexed them later — 13,678 knots indexed per the concurrency-probe record),
plus the cut's 1,452 files. The pile ending at Aug-31 is the moment "write knot" and
"append chain" became one step — reshelving, not destruction.

## AMENDMENT ANALYSIS

- Current chain: **1,719 amended** rows [measured; matches mission context]. Of these,
  **1,698 are rebuild re-knots** (47% of the 3,586 added rows); only **21 are pre-cut
  survivors**. Amendment is a property the rebuild stamped, not a pre-surgery condition.
- By ts: 902 amended written Aug-31 + 440 Sep-01 = 78% of all amended rows were written in
  the 48h rebuild. By event day: concentrated Aug-08..11 (440+344+136+120) — the MEGA-BUILD
  band, i.e. the sessions that had already been summarized once before re-knotting.
- `evidence_lost`: 618 rows; 539 written Aug-31/Sep-01; event days Aug-06..11 (257+140+88+68
  on Aug-10..11...) [measured]. Code semantics: flag = "knot file missing", set under
  verkle_lock by `mag/_flag_dangling_264d0ba3.py:70-82`; guarded by `mag/chain_guard.py`
  against silent flag-loss.
- Structure of amended rows (sample of 50, seed 11): the chain is a strict linear hash
  chain — every row's `parent_verkle_root` = previous row's `verkle_root` (0 breaks
  chain-wide), so amended rows share exactly the parent pattern of non-amended neighbors;
  no sub-chain, no fork. In 50/50 samples the filename's 8-hex tag equals the prefix of
  `leaf_hash` or `dossier_commit` — chain row ↔ knot file binding is content-addressed.
  Genesis row (idx 0, Aug-12_1641): leaf_hash == verkle_root == filename tag `6bcba096`
  [measured; matches AUDIT_C_VERKLE_20260901.md §3]. `repaired_from_pointer` appears on
  exactly 5 rows (3 ts Aug-11, 1 Aug-12, 1 Sep-06 batch repair) [measured].

## UNRECOVERABLE INVENTORY (bounded, with recovery paths)

1. **304 cut-dropped knot files** absent from both audited knots dirs. Row metadata intact
   in the 6,661 backup; content possibly recoverable from session dossiers via
   `dossier_commit`/`session_id`. Not proven destroyed — proven absent from audited paths.
2. **18 current-chain filenames missing from disk** (event days Aug-07..12; one is a
   malformed filename containing a raw dict repr: `2026-08-11_1952_mem-invariant-map_mem_inva_{'ok': F.knot.json`)
   — chain asserts a knot the disk doesn't have.
3. **1 rebuild-added filename missing from disk** (3,585/3,586 present).
4. **2 truncated lines in the 4,914 snapshot** (mid-write corruption around idx 2288 and
   4901-4907) — partial fields only; the cut had already renumbered past them.
5. **1,106 rebuild-dropped knot files** absent — but this is the class the rebuild was
   curing (54% evidence_lost-flagged, expected count 1,031 set Aug-26), and their periods
   were re-knotted from source sessions. Reshelved by design, not lost by the surgery.

Nothing at the RECORD level is unrecoverable: every removed row's full JSON survives in
`biography_backup_20260830`, and the whole pre-surgery knot corpus (1,458 files) survives
in its knots/ dir. Backup-first was obeyed.

## PRIOR-CLAIM CORRECTIONS

- "Chain spans Aug-10 → Sep-06": DISPUTED — event dates span **Aug-02 → Sep-06** (earliest
  chained event Aug-02, idx-adjacent backfill; genesis knot's own filename-day is Aug-12
  because idx 0 was written Aug-12) [measured].
- "Zero rows dated Aug 16-30": DISPUTED for event dating, SUPPORTED for ts dating (see
  verdict). Real event-date hole: **Aug-19..22 only**.
- "13,693 dated orphans": SUPPORTED, exact.
- "6,661 → 4,914 → 6,537": SUPPORTED; 6,537 is a Sep-01/02 measurement, current tip is 7,377.
- ROSHAMON §G's open item — "1,009 [pruned rows] lack signature survivors... content-level
  survival still owes one check before calling it zero" [card: ROSHAMON_REBUILD_20260902.md
  §G-CORRECTION] — this card is that check: the rebuild re-knotted every pruned event period
  from source sessions into rows whose files exist; the pruned rows' own files mostly survive
  as orphans or in the Aug-30 backup. Verdict: prune obeyed the duplication-is-emphasis law.

## FALSIFIERS

- If any of the 304 absent files turns up under an unaudited path (cage, tarball
  `knots.bak-orphanlane-20260906T224709Z.tar`, 66.9MB), the lost-file inventory shrinks —
  the tar is the obvious next dig, deliberately not opened read-heavy this session.
- If a `leaf_hash` from the 6,661 backup is absent from all later states AND its
  `dossier_commit` no longer resolves, that row's content is then provably gone (none found).
- Root-reuse test returned negative chain-wide (0 duplicate verkle_roots) — any future
  duplicate would indicate re-knotting of identical content and should re-open this verdict.
