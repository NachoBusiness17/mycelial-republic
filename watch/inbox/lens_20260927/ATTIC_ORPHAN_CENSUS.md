# ATTIC ORPHAN CENSUS — structural half of archive salvage (2026-09-27)

Operator split 2026-09-27: structural orphans are the fleet's to measure; valued orphans stay
with the operator. Audit basis: `mag/shape_map.py` REGISTRY has 9 subsystems and NO archive
subsystem — anything in the archives reducing to none of the claimed shapes is an orphan BY
DEFINITION (receipt `watch/inbox/audit_20260926/LANE4B_UNVERSIONED_RISK.md`).

Method: TOC-ONLY. Every number below came from a command run in this session
(`find -printf` for sizes; `tar -tf | awk` full-table-of-contents classification per tar —
NO tar was extracted, NO bulk content read). Directory entries inside tars (trailing `/`)
are counted separately as `dir-entries` and are NOT counted as orphans or matches.

## The 9 claimed shapes (mag/shape_map.py REGISTRY, one line each)

| # | Subsystem | Matcher / shape rule (path + element form) |
|---|-----------|--------------------------------------------|
| 1 | rib | lines `- [domain] invariant…` of `queue/handoff/DISTILLED_INVARIANTS.md` (via `mag.emergent_harvest._load_invariants`); rib artifacts also live under `memory/rib/` |
| 2 | corpus | file stems of `memory/research_packs/*.answer.*.md` |
| 3 | skill_ledger | JSONL rows of `memory/improve/skill_ledger.jsonl` |
| 4 | one_sizer | JSONL rows of `memory/learn/sizing.jsonl` |
| 5 | verkle_chain | JSONL rows of `memory/biography/verkle_chain.jsonl` |
| 6 | steal_pack | JSONL rows of `memory/runs/steal_pack/filed.jsonl` |
| 7 | pro_library | JSONL rows of `memory/pro/pro_library.jsonl` |
| 8 | mycelium | JSONL rows of `memory/mycelium/nodes.jsonl` + `memory/mycelium/edges.jsonl` |
| 9 | research_lens | items of `memory/lenses/corpus_index.json` |

Strict matcher used by this census: a tar member matches iff its path equals one of the
registry source paths (or the rib/corpus path families above). Anything else = structural-orphan
candidate. One family annotation is reported separately (verkle-knot-family: `*.knot.json`,
`verkle_chain.jsonl`, `verkle_tip.json` at ANY depth — the operator's dispatch hint names
"verkle/knot paths → verkle_chain"; the strict registry claims only the live chain file, so
these are counted as orphans in the strict column and as family in the annotation).

## Archive surfaces enumerated

- `attic/` — exactly **17 tars**, 3,103,631,360 bytes total (~2.89 GiB), plus `MANIFEST.jsonl`
  and two non-tar dirs (`kill_list_20260908/`, `secrets_quarantine_20260908/` — directories,
  not tars, out of this tar census's scope; noted for the valued-orphan half).
- `watch/inbox/ESSENTIALS_PACK_20260926.tar.gz.enc` — 1,706,469,664 bytes (1.59 GiB),
  **ENCRYPTED-OUT-OF-SCOPE** (unreadable without the key; recorded, not counted).

## Per-tar census (all counts = full `tar -tf` table of contents, not a 50-sample)

| Tar | Bytes | Members | Matched | Dir-entries | Orphan files | Dominant orphan classes (count, 5 examples each in log) |
|---|---|---|---|---|---|---|
| cards_backup_20260908.tar | 1,054,720 | 192 | 0 | 0 | 192 | `watch/*` 161 (ex: `watch/ADAM_CALL_BRIEF_20260907.md`, `watch/AUDIT_C_VERKLE_20260901.md`); `watch/inbox/*` 31 (ex: `watch/inbox/CHAN_COMMIT_001_20260901.md`, `watch/inbox/CODEX_ACTIVATION_20260901.md`) |
| biography_backup_20260825.tar | 189,808,640 | 42,302 | 0 | 53 | 42,249 | `…/biography/*` 22,462 (ex: `…/biography/019f4d15-….md`, `.pdf`, `.dossier.json`); `…/knots/*` 17,386 (ex: `…/knots/2026-07-10_1731_mirror_….knot.json`); `…/derived/*` 2,311 (ex: `…/derived/019f4d15-….md/.pdf`); `diary_nodes/*` 29; `cards/*` 9; backup-root 43 (incl. `verkle_chain.jsonl`, `verkle_tip.json`); 9 uuid/`mag-agent-orc-*` asset dirs of 1 each |
| biography_backup_20260914.tar | 62,822,400 | 30,552 | 0 | 2 | 30,550 | `…/knots/*` 30,548 = 21,875 `DATE_TIME_*.knot.json` + 8,637 `by-session_*.json` + 36 no-ext `…_untagged_work` markers; backup-root 2 (`verkle_chain.jsonl`, `verkle_tip.json`) |
| biography_backup_20260915.tar | 63,180,800 | 30,741 | 0 | 2 | 30,739 | `…/knots/*` 30,737 (same two families); backup-root 2 |
| biography_backup_20260916.tar | 63,692,800 | 31,014 | 0 | 2 | 31,012 | `…/knots/*` 31,010; backup-root 2 |
| biography_backup_20260917.tar | 64,040,960 | 31,198 | 0 | 2 | 31,196 | `…/knots/*` 31,194; backup-root 2 |
| biography_backup_20260919.tar | 64,542,720 | 31,466 | 0 | 2 | 31,464 | `…/knots/*` 31,462; backup-root 2 |
| biography_backup_20260920.tar | 65,105,920 | 31,761 | 0 | 2 | 31,759 | `…/knots/*` 31,757; backup-root 2 |
| leak_reports_2026-09-09.tar | 2,416,640 | 2,354 | 0 | 0 | 2,354 | bare filenames, no dir: `report-2026-09-09T000002.json` etc. |
| leak_reports_2026-09-10.tar | 2,426,880 | 2,366 | 0 | 0 | 2,366 | bare `report-2026-09-10T*.json` |
| leak_reports_2026-09-11.tar | 2,211,840 | 2,150 | 0 | 0 | 2,150 | bare `report-2026-09-11T*.json` |
| leak_reports_2026-09-12.tar | 2,242,560 | 2,179 | 0 | 0 | 2,179 | bare `report-2026-09-12T*.json` |
| leak_reports_2026-09-13.tar | 1,802,240 | 1,757 | 0 | 0 | 1,757 | bare `report-2026-09-13T*.json` |
| leak_reports_2026-09-14.tar | 1,976,320 | 1,914 | 0 | 0 | 1,914 | bare `report-2026-09-14T*.json` |
| leak_reports_2026-09-15.tar | 1,914,880 | 1,861 | 0 | 0 | 1,861 | bare `report-2026-09-15T*.json` |
| leak_reports_pre_2026-09-16.tar | 156,631,040 | 123,723 | 0 | 0 | 123,723 | bare `report-2026-08-*.json` (August remainder; ex: `report-2026-08-09T041329.json`) |
| hook-state_stale_baselines.tar | 2,357,760,000 | 160,429 | 0 | 68 | 160,361 | 68 classes `sess_<uuid>.baseline/` (ex: `sess_cc461d2f-….baseline/0207324b….source`), sha256-named `.source` files, avg ~2,358 per baseline dir |

Prefix `…/` = `biography_backup_<date>/` inside the tar. Full per-class output with 5 examples
per class lives in this session's command log (batch runs of 2026-09-27).

## SUMMARY

- **Total members sampled (full TOC of all 17 tars): 527,959** (527,826 file members + 133 dir entries).
- **Matched members across ALL 17 tars: 0.** Not one attic member sits at a path any of the 9
  registry shapes claims. **Structural-orphan candidates: 527,826 = 100.0% of file members.**
- Verkle-knot-family annotation: 167,343 of those orphans (31.7%) are `*.knot.json` (167,327) +
  relocated `verkle_chain.jsonl`/`verkle_tip.json` (8+8) — the verkle_chain subsystem's backing
  store snapshotted under `biography_backup_*/` roots instead of its live `memory/biography/` path.
  Family-adjusted orphan count (if the operator grants knots to verkle_chain): **360,483 (68.3%)**.
- **Top 3 orphan classes by volume (strict):**
  1. `biography_backup_*/knots/**` — 204,094 members (38.7% of orphans; 167,327 `.knot.json` +
     ~36,700 `by-session_*.json` + untagged markers; by-session split byte-verified in
     biography_backup_20260914: 21,875 knot + 8,637 by-session + 36 no-ext).
  2. `sess_*.baseline/<sha256>.source` (Mimosa hook-state) — 160,361 members (30.4%), the single
     largest tar (2.36 GB).
  3. bare `report-*.json` ghost leak reports — 138,304 members (26.2%) across 8 tars
     (123,723 pre-09-16 + 14,581 dailies).
  - Top-3 subtotal: 502,759 = 95.2% of all orphans. Remainder: biography dossier tree of the
    0825 backup (~24,863: biography/derived/cards/diary_nodes/uuid-assets), 12 relocated verkle
    chain/tip files in the six daily bio backups, 192 watch cards.
- Manifest cross-check (`attic/MANIFEST.jsonl`): measured member counts equal manifest
  `files` for 15/17 tars (dailies 2,354/2,366/2,150/2,179/1,757/1,914/1,861; pre 123,723; bio
  42,249/30,550/30,739/31,012/31,196/31,464/31,759 — the +2 per bio tar over manifest = the 2
  dir entries). hook-state manifest row says `files: 68` because it counted the 68 baseline
  DIRS; the tar holds their contents: 160,361 files. `cards_backup_20260908.tar` has NO
  manifest row (only tar in the attic with none).
- Leak-report tars store members as bare filenames with no `memory/ghost/leak_reports/` prefix,
  and hook-state stores baseline dirs at tar root with no `.mimosa/hook-state/` prefix — so even
  path-family extensions of the 9 shapes would not claim them; only filename/content-level
  matchers would.

## Verdict — is the attic mostly held shapes or mostly orphans?

**The attic is, by the strict structural definition, 100% orphans: across 527,826 file members
in 17 tars not a single one reduces to a path any of the 9 registered shapes claims — the
registry has no archive subsystem, and every archived family was snapshotted at relocated or
flattened roots (backup-dir prefixes, bare leak-report filenames, root-level baseline dirs).**
The honest qualification is concentration, not doubt: 95.2% of the orphan mass is three
families, and one of them (167,343 members of biography verkle knots and chain/tip snapshots,
31.7%) is the verkle_chain subsystem's own backing store one root-relocation away from its
claimed shape — grant that family extension and the attic drops to 68.3% orphan. What remains
unclaimed under any reading is the Mimosa hook-state baseline blob (160,361 hash-named sources,
30.4%, and 76% of the attic's bytes), the ghost leak-report stream (138,304 unversioned JSON
reports, 26.2% — the LANE4B unversioned-risk class), and the biography dossier/cards/watch
document tree (~25,000). Structural conclusion for the operator's half: the attic is not a
museum of held shapes; it is three unclaimed blobs plus the verkle knot store wearing a backup
costume — a shape_map `archive` subsystem (or explicit family rules) is the only thing that
would make any of it held.

---
Laws honored: no extraction (TOC only); every count/size from a command run this session;
encrypted pack recorded, not read; no existing file modified; only this output file created.
Classification instrument: GNU tar `-tf` + awk over full member lists, matchers fixed before
counting; dir entries excluded from both matched and orphan columns and reported separately.
