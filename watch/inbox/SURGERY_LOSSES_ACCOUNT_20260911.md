# SURGERY LOSSES ACCOUNT — the tar dig + last unrecoverable-candidates check

Date: 2026-09-11 · Lane: zcode research worker · Method: read-only. Tar opened LIST-ONLY
(tarfile.getnames + 2 small members read into memory for schema check; nothing extracted
to disk). No quarantine path touched. This card is the bounded-losses account the
recovery vote was waiting on. Companion to `watch/inbox/SURGERY_FORENSICS_20260911.md`.

## HEADLINE VERDICT

**The tar recovers NOTHING from the bounded-loss inventory: 0/304 + 0/18 + 0/1 + 0/473
member-name hits [measured].** `knots.bak-orphanlane-20260906T224709Z.tar` is a third copy
of the orphan pile, not a lost-knot trove. Its only marginal content is **151 orphan files
that exist nowhere else on audited disk — and none of them is referenced by any chain
state (backup, mid-surgery snapshot, or current)** [measured]. Every loss class keeps its
recovery path via `dossier_commit`/`session_id` metadata; none gets a new one from the tar.

## 1. THE TAR (located + inventoried)

- Path: `memory/biography/knots.bak-orphanlane-20260906T224709Z.tar` (66,918,400 bytes =
  66.9 MB, matches the forensics card's description). Made 2026-09-06 22:47Z, during the
  orphan-lane cleanup that also produced 9 chain/tip `.bak-orphanlane-*` siblings in
  `memory/biography/` (chain snapshots 5,168,308–5,169,074 B, 22:47–22:55Z) [measured].
- **21,042 members** (all unique names, flat — no directory prefixes), spanning
  **2026-07-10 → 2026-09-06** across 51 distinct days [measured].
- Schema check (2 smallest members, read to memory only): standard knot JSON — keys
  `Q_proxy, chord_commitment, chord_root, date, dirichlet_energy_proxy, dominant_theme,
  dossier_commit, duration_minutes, engine, filename, gap_proxy, inspiration,
  lambda2_proxy, ...` — same grammar as the live knots [measured].
- Relation to disk: tar ≠ current `knots/` (tar-only: 151; disk-only: 7,984 — the tar
  predates later writes and skips much of the current corpus). It contains **5,234 of the
  6,661 pre-cut chain's filenames** — redundant safety copy of files that mostly also
  survive in the Aug-30 backup knots dir [measured].

## 2. THE 18 MISSING CHAIN-REFERENCED FILENAMES (recomputed exactly)

Current chain `memory/biography/verkle_chain.jsonl`: 7,377 rows, 0 bad lines, 7,377 unique
filenames; 18 absent from `memory/biography/knots/` [measured — matches forensics card]:
1. `2026-08-07_0612_mag_mag-agen_1d4a1797.knot.json`
2. `2026-08-08_1519_biography_mag-agen_ba182078.knot.json`
3. `2026-08-08_1831_biography_mag-agen_0bf6a10f.knot.json`
4. `2026-08-08_2011_mirror_mag-agen_a7b83063.knot.json`
5. `2026-08-09_1125_biography_mag-agen_4357f0aa.knot.json`
6. `2026-08-10_1219_session_mag-agen_8d2b2149.knot.json`
7. `2026-08-10_1253_harness_mag-agen_411ad3b3.knot.json`
8. `2026-08-10_1801_mag_mag-agen_f9120f5d.knot.json`
9. `2026-08-10_1856_biography_mag-agen_597e7917.knot.json`
10. `2026-08-10_2211_biography_mag-agen_1e9253c5.knot.json`
11. `2026-08-11_0945_untagged_work:mem_7a8f565c.knot.json`
12. `2026-08-11_0947_untagged_work:mem_7ddd7c9a.knot.json`
13. `2026-08-11_0949_untagged_work:mem_a2aeeaf3.knot.json`
14. `2026-08-11_0950_untagged_probe:st_ac41e1a7.knot.json`
15. `2026-08-11_0950_untagged_work:mem_2cc1d0fa.knot.json`
16. `2026-08-11_0950_untagged_work:mem_d52f3706.knot.json`
17. `2026-08-11_1952_mem-invariant-map_mem_inva_{'ok': F.knot.json` (malformed: raw dict repr)
18. `2026-08-12_0012_biography_mag-agen_81742491.knot.json`

New sub-finding: **7 of the 18 contain raw colons** (`work:mem`, `probe:st`, and the
dict-repr one) — NTFS-illegal characters. Those 7 names can never exist as ordinary
Windows files; any restore needs name-mangling, and their absence from disk is partly a
filesystem constraint, not only loss [measured].

## 3. OVERLAP ANALYSIS (18 vs 304, and the rest)

- **18 ∩ 304 = 0** [measured]. The classes are structurally disjoint: the 304 are
  cut-dropped filenames no longer referenced by any chain; the 18 are names the CURRENT
  chain still asserts.
- **The forensics card's class-3 "1 rebuild-added file missing" is INSIDE the 18**:
  `2026-08-10_1219_session_mag-agen_8d2b2149.knot.json` is a rebuild re-knot (cur-only,
  not in the 6,661 backup) whose file never hit disk. Distinct current-chain missing
  files = 18, not 19. The card's inventory double-counts by 1 [measured correction].
- Class-5 refinement: "1,106 rebuild-dropped files absent" is absent-from-CURRENT-knots
  only; **633 of them survive in the Aug-30 backup knots dir. Truly absent from both
  audited dirs: 473** [measured]. The 473 (467 snap-only + 6 snap-not-in-backup) are
  disjoint from the 304 and the 18 [measured].
- Reconciliation of "absent everywhere incl. the tar": 788 backup-chain filenames are in
  neither tar nor either knots dir = **304 (class 1) + 467 (class-5 snap-only) + 17
  (of the 18 that also sit in the backup chain)**. Arithmetic closes exactly [measured].

## 4. PER-CLASS RECOVERABILITY VERDICT (from the tar)

| Class | Size [measured] | In tar | Verdict (tri-state) |
|---|---|---|---|
| 1. Cut-dropped knot files (304) | 304 | **0** | **DISPUTED that the tar recovers them.** Metadata (leaf_hash, session_id, dossier_commit) intact in the 6,661 backup; content path remains dossier re-knot (SUPPORTED as path, Unproven until one dossier_commit resolves). |
| 2. Current-chain missing files (the 18) | 18 | **0** | **DISPUTED for tar recovery.** Full chain-row metadata intact in the live chain. 7/18 NTFS-illegal names — partly unwritable by construction. Content path: dossier re-knot. |
| 3. Rebuild-added file missing | 1 (⊆ the 18) | **0** | Same file as class 2 row 6. No separate loss. |
| 4. Truncated lines in 4,914 snapshot | 2 | n/a | Chain-line corruption, not knot files; only path is re-knot from source sessions. Unchanged. |
| 5. Rebuild-dropped files absent (card: 1,106) | 473 truly absent (633 survive in Aug-30 backup) | **0** | **DISPUTED for tar recovery** — but this class was reshelved by design (re-knotted at equal/greater depth); forensics card's verdict stands, now with the smaller truly-absent count. |

**Tar's actual marginal value: 151 unreferenced orphan files (archival only, no chain
row wants them) + redundant copies of 5,234 already-preserved filenames.** KEEP the tar
as belt-and-suspenders, but the recovery vote should not count it as a recovery source.

## BOTTOM LINE FOR THE VOTE

Distinct knot files absent from every audited location including the tar: **795**
(304 cut-dropped + 473 rebuild-dropped truly-absent + 18 chain-referenced − 1 double-count
already inside the 18... = 304 + 473 + 18 = 795; the classes are pairwise disjoint
[measured]). Zero are in the tar. All 795 have surviving row metadata somewhere (6,661
backup / 4,914 snapshot / live chain). Record-level loss remains ZERO; file-level loss is
now bounded exactly, and the only recovery path for content is
`dossier_commit`/`session_id` re-knotting from source dossiers — Unproven until one
dossier_commit is test-resolved.

## FALSIFIERS

- If a copy of this tar exists elsewhere (cage, attic backups — outside this session's
  read scope) with DIFFERENT members, re-run the member-set diff before closing.
- If a dossier_commit from any of the 795 resolves to a source dossier whose re-knot
  reproduces the lost content, class 1/2/5 shift from Unproven to recoverable.
- If any of the 151 tar-only files is later found referenced by a chain state that this
  session did not audit (e.g. a fourth chain snapshot), the "unreferenced" claim reopens.
