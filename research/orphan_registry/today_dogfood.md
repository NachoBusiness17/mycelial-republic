# TODAY DOGFOOD — 2026-09-06 · seat today

Operator: "we added a lot of research today so dogfood it all." Exercise, not stat:
parse everything, rerun the bench, sample claims against sources, then name the orphans.
$0, no network, no daemons. Swept 2026-09-06 (static sweep then bench rerun).

## 1. SWEEP TABLE

| surface | n | check | result |
|---|---|---|---|
| research/gaming_corpus/**/*.md (incl. marathon_terminals/INDEX.md) | 16 | UTF-8 decode + non-empty + no NUL/replacement chars | 16/16 PASS |
| research/corpus_triangulation/*.md (R1-R6) | 6 | same | 6/6 PASS |
| watch/inbox/** .md mtime >= 2026-09-05 | 36 | same | 36/36 PASS |
| research/surface_audit/df1..df6.json | 6 | json.load, non-empty dict | 6/6 PASS |
| state/shadow_work/volume.json | 1 | schema: points[] | PASS — points=9,305, n_slabs=50, axes x/y/z/c |
| state/shadow_work/weights_volume_qwen3b.json | 1 | schema: tensors[] | PASS — tensors=434 (Qwen2.5 3B Instruct, 36 layers) |
| state/shadow_work/projection_3d.json | 1 | schema: pca fields | PASS — 9,305 pts, pca1/pca2/pca3 + slab + law_hits |
| state/shadow_work/chunk_manifest.json | 1 | schema: 72 chunks | PASS — exactly 72 |
| state/perturbation_battery.json | 1 | json.load | PASS — schema/ts/salon/rules/cases/verdict (NOTE: lives in state/, not state/shadow_work/ as briefed) |
| watch/TESUJI_GRID_T1_20260906.json | 1 | json.load | PASS — grid/generated/charter/gate/pricing/cost/falsifier_hooks |
| state/shadow_work/slab_*.csv | 50 | csv module, row band 186-191 | PASS — 50/50 in band (min 186, max 191, 6 cols each, 0 outliers) |
| notebooks/shadow_work_physics.py | 1 | END-TO-END rerun | PASS — exit 0, "RUN OK"; eikonal BFS==\|grad T\|=1 CONFIRMED; 9,305 pts loaded; t-SNE 2,000 pts KL=0.7487 (999 iters); layer-gradient log-linear 1.52%/layer r=0.705 p=1.6e-6, verdict CONFIRMED on its own basis; focal set 1,184 pts in 50 slabs; re-emitted projection_3d.json (9,305 pts, 778 KB) |

Method note: no `markdown` lib in this env — ".md parses" = valid UTF-8, non-trivial
content, zero NUL/replacement bytes (markdown itself has no strict grammar to violate).

## 2. CROSS-CHECKS (3 sampled claims)

| # | claim (card) | source of truth | measured | verdict |
|---|---|---|---|---|
| 1 | R3_training.md: "configs/training_patterns.yaml carries **19 eval cases** (eval-001..010, economics-003, ilap-001..003, steward-001, desk-teaching-001)" | configs/training_patterns.yaml `eval_cases` | **16** cases; the enumerated id list matches exactly once you restore the yaml's `eval-` prefix (eval-economics-003, eval-ilap-001..003, eval-steward-001, eval-desk-teaching-001) — the card under-prefixed AND over-counted its own list (16 names, headline 19) | **DISPUTED** (actual 16) |
| 2 | R5_signals.md: "MrPool_Q **2,008** rows; median 1,438 chars; max 3,000; 2 empty texts" | corpus/telegram/MrPool_Q.jsonl | 2,008 rows; median 1,438; max 3,000; 2 empty — all four sub-claims exact | **SUPPORTED** |
| 3 | TRANSFER_TEST_20260906.md: "surface_B **176** units (= INDEX)" + INDEX "M1+M2: 176 terminals, 275,149 chars" | research/gaming_corpus/marathon_terminals/m1/*.txt + m2/*.txt, `^### .*(Terminal` sections | 176 sections exactly; 275,149 chars exactly; per-file counts match INDEX row-for-row (incl. m2/captured.txt = 0 stub) | **SUPPORTED** |

## 3. UNLINKED CARDS (today's orphans)

37 of 58 today-cards are referenced by NO tesuji cell (haystack: watch/TESUJI_MAP.jsonl
238 rows + watch/TESUJI_GRID_T1_20260906.json + watch/TESUJI_MAP.md render).
These are the research additions with no cell in the field:

RESOLVED 2026-09-07 (linker link37, salon LOOT verdict): 36 LINKED via R/linked/* cells
(seat link37), 1 DISPOSITIONED as pure aggregate. Per-card status:

```
research/corpus_triangulation/R1_gaming_canon.md — LINKED via cell R/linked/r1-gaming-canon #07549db17479
research/corpus_triangulation/R3_training.md — LINKED via cell R/linked/r3-training #205ff8081656
research/gaming_corpus/baroque_vs_fleet.md — LINKED via cell R/linked/baroque-vs-fleet #bbd259fb0b2b
research/gaming_corpus/basecamp_fulfilled.md — LINKED via cell R/linked/basecamp-fulfilled #5cb52669723b
research/gaming_corpus/berlin_interpretation_intake_004.md — LINKED via cell R/linked/berlin-interpretation-004 #9fc0bc8ecc9a
research/gaming_corpus/codex_ontology_proven.md — LINKED via cell R/linked/codex-ontology-proven #b828146afdb6
research/gaming_corpus/deadzone_internals_intake_006.md — LINKED via cell R/linked/deadzone-internals-006 #7405a7bbdddc
research/gaming_corpus/engines_race_sowing.md — LINKED via cell R/linked/engines-race-sowing #d472299ad315
research/gaming_corpus/l0_contract_crossmap.md — LINKED via cell R/linked/l0-contract-crossmap #07d6ae7fa4b8
research/gaming_corpus/marathon_archive_intake_005.md — LINKED via cell R/linked/marathon-archive-005 #68508e334699
research/gaming_corpus/primer_vs_fleet.md — LINKED via cell R/linked/primer-vs-fleet #3998a26a8669
watch/inbox/AGENT_MOCK_DOSSIER_20260906.md — LINKED via cell R/linked/agent-mock-dossier #60a18285ae87
watch/inbox/CITE_GATE_BUILD_20260906.md — LINKED via cell R/linked/cite-gate-build #5a508633fbe3
watch/inbox/ELEVATION_RICE_20260906.md — LINKED via cell R/linked/elevation-rice #a344c1446a4a
watch/inbox/FLEET_LIGHTMAP_V2_20260906.md — LINKED via cell R/linked/fleet-lightmap-v2 #01f1b4a86802
watch/inbox/FRONTIER_DISPATCH_001_20260905.md — LINKED via cell R/linked/frontier-dispatch-001 #7a92d6fdfc90
watch/inbox/FRONTIER_DISPATCH_001_20260905_COMPLETE.md — LINKED via cell R/linked/frontier-dispatch-001-complete #f14d9d42a0e7
watch/inbox/FRONTIER_SIGNAL_INCIDENT_SPACE_20260906.md — LINKED via cell R/linked/frontier-signal-incident-space #a39d52618c5e
watch/inbox/HOME_API_FIX_20260906.md — LINKED via cell R/linked/home-api-fix #a02335296e3d
watch/inbox/MARATHON_HARVEST_20260906.md — LINKED via cell R/linked/marathon-harvest #b61db7bb8221
watch/inbox/MAZE_ARENA_B1_20260906.md — LINKED via cell R/linked/maze-arena-b1 #cb4c4b0c16db
watch/inbox/NAV_WIRING_20260906.md — LINKED via cell R/linked/nav-wiring #9da784303a6c
watch/inbox/RESTFUL_WATCH_059_20260906.md — LINKED via cell R/linked/restful-watch-059 #d36220b5bf68
watch/inbox/REVEAL_FIVE_REHEARSALS_20260906.md — DISPOSITIONED: aggregate of the 5 unabridged receipt re-mints it carries verbatim (state/POWER_RESTORE_20260825.md, state/HOW_TO_RUN_THIS_20260826.md, state/SANITY.md, state/AUDIT_STACK.md, state/HANDOFF.md — none has a tesuji cell of its own; the reveal adds no new claim beyond the Law-2 unabridged correction)
watch/inbox/SALON_CONCURRENCY_CHAIR4_ASTRA_20260906.md — LINKED via cell R/linked/salon-concurrency-chair4-astra #fcaeafad313f
watch/inbox/SALON_LIGHTMAP_B2_20260906.md — LINKED via cell R/linked/salon-lightmap-b2 #7b3be22f3d10
watch/inbox/SHADOW_PHYSICS_LAB_20260906.md — LINKED via cell R/linked/shadow-physics-lab #c4ae73a3899e
watch/inbox/SHADOW_WALK_V2_RUN_20260906.md — LINKED via cell R/linked/shadow-walk-v2-run #4245c1fdf0a0
watch/inbox/SHADOW_WORK_WEIGHTS_VOLUME_20260906.md — LINKED via cell R/linked/shadow-work-weights-volume #4e2235576a7f
watch/inbox/SOWING_ROOM_20260906.md — LINKED via cell R/linked/sowing-room #37e44580fc6e
watch/inbox/TESUJI_A6_LOCAL_DIFF_20260906.md — LINKED via cell R/linked/tesuji-a6-local-diff #1c9186d55a2c
watch/inbox/TESUJI_GRIDDER_20260906.md — LINKED via cell R/linked/tesuji-gridder #374cd365a387
watch/inbox/TESUJI_PAGER_20260906.md — LINKED via cell R/linked/tesuji-pager #da55cee9b2f5
watch/inbox/TESUJI_T0_RECEIPTER_20260906.md — LINKED via cell R/linked/tesuji-t0-receipter #8b6a3cf87333
watch/inbox/TOPIC_INDEX_BUILD_20260906.md — LINKED via cell R/linked/topic-index-build #017f340b028b
watch/inbox/VISION_PASS_SWEEP1_20260906.md — LINKED via cell R/linked/vision-pass-sweep1 #7f2f22267a02
watch/inbox/bad_apple/PROVENANCE.md — LINKED via cell R/linked/bad-apple-provenance #28550da0b9f0
```

DISPUTED resolution (2026-09-07, seat link37): the "19 eval cases vs 16" dispute is
resolved by correction cell `R/training/eval-count` #70453072503c — counted
`configs/training_patterns.yaml` `eval_cases` precisely: **16** (eval-001..010,
eval-economics-003, eval-steward-001, eval-ilap-001..003, eval-desk-teaching-001).
R3's headline 19 was a miscount of its own 16-name list; §4 fix stands.

Linked today-cards (21): research/corpus_triangulation/R2_library.md · R4_oral_history.md · R5_signals.md · R6_swarm_apk.md · research/gaming_corpus/baroque_cycle_intake.md · deadzone_rogue_intake_001.md · diamond_age_primer_intake.md · engines_tile_card_constraint.md · engines_war_territory.md · mickey17_intake_002.md · marathon_terminals/INDEX.md · watch/inbox/CHAIN_INDEX_AUDIT_20260905.md · DOOR_VERIFIER_INTAKE_20260906.md · FREE_TIER_AUDIT_20260906.md · LITE_REARM_RUNBOOK_20260905.md · PERTURBATION_BATTERY_20260906.md · REFEED_GUARD_B1_20260905.md · SHADOW_WALK_20260906.md · TESUJI_T0_BANKER_20260906.md · TRANSFER_TEST_20260906.md (posts axis-G cells) · X_HARVEST_SCORECARD_20260905.md

## 4. BROKEN ADDITIONS

- **DISPUTED — research/corpus_triangulation/R3_training.md:38**: "19 eval cases" does not
  reproduce; configs/training_patterns.yaml holds 16 (the card's own enumeration is 16).
  Fix: change 19 -> 16 (and re-prefix the six non-eval-NNN ids). Everything else in the
  card's claim stands: all 16 carry fixtures; zero corpus-sourced eval cases.
- **Not broken, misplaced**: perturbation battery output is `state/perturbation_battery.json`,
  not `state/shadow_work/perturbation_battery.json` as briefed. Parser (mag/perturbation_battery.py)
  and data are healthy.
- Zero files failed to parse. Zero CSVs out of band. Bench rerun reproduces end-to-end.

## 5. CELLS POSTED

- `R/dogfood/today/parse-sweep` SUPPORTED — 58 md + 9 json + 50 csv exercised, all pass
- `R/dogfood/today/crosschecks` DISPUTED — R3 "19 eval" actual 16; MrPool 2,008 PASS; marathon 176 PASS
- `R/dogfood/today/orphans` SHADOW — 37/58 today-cards have no tesuji cell; this registry is the pointer

Chain verify after posting: **PASS — 252 cells, chain intact, tip=b43b925bc7be** (run twice, stable).
Note: at post time (16:28:51Z) verify transiently reported `row 245: EVIDENCE-MISSING law/registry.json` —
a FOREIGN row (seat memreg, mid-reorg of the law registry, canonical home `memory/law/registry.json` per
mag/law.py:21). Resolved by memreg within the minute; not a dogfood finding, logged here for the record.
Ledger was 238 rows at sweep time, 252 by verify — concurrent seats (maze-lineage, memreg) post to the same chain.
