# MEMORY ORPHANS — gatherer run (memreg, 2026-09-06)

Operator order: "look deeply at our memories... gather all the orphans."
Scope: repo `memory/` READ-ONLY. Measurements only, $0, no network.
Method: python scans of `memory/MEMORY.md`, harness copy at
`C:\Users\foste\.zcode\cli\memories\projects\projects-0fb5e3041b59db21\memory\MEMORY.md`,
`memory/percolator/invariants.json` (+ both .bak), full recursive basename walk of `memory/`.

## Headline

**366 of 396 unique index targets in `memory/MEMORY.md` (92%) resolve to no file
anywhere under `memory/`.** The index is a map to rooms that were never built or
were moved without re-pointing. The 30 that do resolve live in
`memory/runs/codex_seat/fold/` (matched by basename, not by the relative path the
links claim). Two indexes exist (repo copy vs harness-loaded copy) and they have
diverged.

## The orphan table

| # | Orphan | Location | Evidence | Why it never made it in | Promotion path |
|---|--------|----------|----------|------------------------|----------------|
| 1 | Dangling index targets | `memory/MEMORY.md` (421 link rows, 396 unique targets) | 366 unique targets exist nowhere under `memory/`; 30 resolve only via `memory/runs/codex_seat/fold/` basename coincidence; 0 resolve at the literal relative path | Topic files were indexed by filename convention at `memory/` top level, but the files live in per-seat folds (`runs/codex_seat/fold/`) or were never materialized; index grew faster than the disk | One re-link pass: resolve each target by basename across `memory/`, rewrite links to real paths; mark never-materialized rows as `index-only` or delete |
| 2 | `user-letter-to-daughter.md` (L513 + L516) | `memory/MEMORY.md:513,516` | Target missing everywhere; the PAYLOAD EXISTS at `corpus/oral_history/LETTER_TO_DAUGHTER.md` (3,491 B, Sep 6 00:31) — link rot, not content loss | Index row written with an invented filename instead of the real deposit path | Rewrite both rows to `../corpus/oral_history/LETTER_TO_DAUGHTER.md` (delivery obligation, highest-stakes row in the index) |
| 3 | Catch-all aliasing: `project-vision-pipeline-self-steal-20260905.md` | `memory/MEMORY.md` cited 12x (repo) / 13x (harness) | One (missing) filename carries ~11 distinct topics: percolation-lean, xbatch2 verifier, astra round2/3, founding record, fleet atlas, human-atlas code, lock-1, audio microscope, chain voice calibration | Log-folding habit: new rows appended with a reused filename instead of new files | Split into per-topic files or accept the single file as canonical and dedupe rows |
| 4 | Invariant registry shrink: 45 generations → 5 | `memory/percolator/invariants.json` (current, 1,409 B, Sep 6 12:18) vs `invariants.json.bak` + `.bak-20260902` (11,984 B each, 45 gens / 15,896 counts, unchanged Sep 2 → Sep 6 01:04) | Current: 5 gens / 2,678 counts. **40 generations (~13,218 mined counts) live only in the .bak.** Operator's "45→58" signal is DISPUTED by disk: measured 45→5 | A writer rebuilt the registry from recent explore.jsonl (1.6 MB, Sep 6 07:56) without merging the prior generation set; no consolidation step in `mag/percolator.py` preserves history | Promote-or-prune pass over the 40 bak-only generations: fold survivors back in or seal them to the chain and retire; then make percolator merge, not replace |
| 5 | Invariants with no consumer | `memory/percolator/invariants.json` (all gens) | Only readers: `mag/lattice_logic.py` (mirror to `dashboard/static/lattices/`, write-free), `mag/seal.py` (seals the file), `scripts/vision_endowment.py` (existence probe). `memory/law/registry.json` (LAW-1..10) is a separate organ with no intake from invariants | The percolator compiles invariants but no promotion pipe connects them to the law lattice — compiled conclusions never become enforceable law | Wire a promotion gate: invariant survives N windows + salon contest → candidate LAW-N in `law/registry.json` |
| 6 | Index tail beyond the load window | harness `MEMORY.md` = 587 lines / 99,428 B; a ~200-line load window captures 26% of bytes; **345 of 457 entries (75%) sit beyond it** — including the newest 09-06 rows (audio microscope, chain voice calibration, agent_mock) | The newest memory is the least-loaded memory; the index loses its own head AND its own tail is what the boot never reads | Append-only index growth with no sliding-window or tiering | Tier the index: hot (last ~40 rows) / warm (digest per day) / cold (topic_index cards already exist — link to `mag/topic_index.py` output instead of inlining) |
| 7 | Dual-index drift | repo `memory/MEMORY.md` = 539 lines vs harness copy = 587 lines, DIFFERENT content, both modified Sep 6 | Repo `MEMORY.pre_trim_20260906.bak` = 521 lines — today's "trim" left the file LONGER than its own backup | Two writers (repo seat + harness memory dir) with no sync contract | Declare one canonical (harness copy is what windows actually load); repo copy becomes a build artifact, or add a sync step to boot_check |
| 8 | `narrative_corpus` husk | `memory/narrative_corpus/` = 4 items: `CATALOG_ONLY.md` (9-link table), `INDEX.md`, `PULL_STAMP.txt` (pull 2026-08-06), `rashomon/tavern_bar_fight_party.v1.md` (2,676 B) | Confirmed "empty husk": story quarter moved out; raw clones live at `mine/raw/narrative_corpus/` (ink, twinejs, redblob, tes5edit, public_domain...) — inside the repo but outside `memory/`; `memory/story/` holds only `THESIS_JOURNEY.md` + `story_latest.json` | Corpus is CAGE/catalog-only by law (copyright), so `memory/narrative_corpus` kept only pointers; nothing ever consumed the rashomon seed since Aug 6 | Either route `rashomon/tavern_bar_fight_party.v1.md` into the D&D/salon pipeline (Rashomon multi-voice is a standing product idea in INDEX.md) or mark the dir catalog-frozen |
| 9 | Memory-root scratch orphans | `memory/working_*.py` × 8 (Aug 2 theme/DNA tooling: annotate_high, apply_dna, backfill_theme, dna_theme, theme_check, theme_list, theme_remaining, unroll_threads), `_hermes_probe.txt` (Jul 24), `scratch_probe.txt` (Aug 9), `harvest_20260816.jsonl` (Aug 16) | Dead scripts + probe droppings sitting at the index's own level; sacred-cow check: the theme/DNA scripts are one draft of the biography-theme idea — steal the bones if biography theming ever revives | One-off runs landed at `memory/` root and stayed | Move to `memory/archaeology/` (dir already exists) or `trash/`; keep `harvest_20260816.jsonl` only if it feeds a knotted run |
| 10 | Biography backup strata | `memory/biography_backup/`, `biography_backup_20260825/`, `biography_backup_flag_20260826T142830Z/`, `...T143105Z/`, `...T145735Z/`, `biography_backup_postrepair_20260825/` | 6 parallel backup dirs from the Aug 25-26 repair nights, no registry of which is canonical | Backup-first law honored but no prune/merge after the repair was verified | Keep newest + the postrepair dir; seal the rest into the chain and delete |
| 11 | L252-286 zone (operator signal 5) | `memory/MEMORY.md` game/salon zone | Superseded by the full scan: every `project-*.md` target in that zone is index-only; none exist on disk | Same as #1 | Same as #1 |

## Signal scorecard (operator's 5 known signals)

1. **L513 dangling letter link** — CONFIRMED, and worse: 366 dangling targets total; payload safe at `corpus/oral_history/LETTER_TO_DAUGHTER.md`.
2. **invariants.json 45→58** — DISPUTED by disk: measured 45→5 generations (13,218 counts dropped from live registry today at 12:18; recoverable from `.bak`). Zero-to-one consumers either way (mirror only).
3. **narrative_corpus empty husk** — CONFIRMED: 4 catalog items + one unconsumed rashomon seed; raw clones intact at `mine/raw/narrative_corpus/`.
4. **MEMORY.md truncation** — CONFIRMED and quantified: harness copy 587 lines / 99,428 B; ~200-line window = 26% of bytes; 345/457 entries (75%) beyond it; dual-index drift repo(539) vs harness(587).
5. **L252-286 project-* files** — CONFIRMED via full scan: that whole zone is index-only.

## Falsifier for this card

Any single claimed-missing target shown to resolve via the literal relative path
`memory/<target>` — none did (0/396); the 30 "resolved" all required the fold
basename walk. Re-run: `python` scan in this card's history or re-run the walk.

---
Run by seat `memreg`, 2026-09-06. Tesuji cells posted under axis R.
