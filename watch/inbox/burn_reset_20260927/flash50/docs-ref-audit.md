# f-07 census: docs/ref audit (365 files)

Date: 2026-09-28. Item: f-07. Seat: fire-f-07 (census gopher).

## Method (commands actually run)

- File list: `find docs/ref -type f | wc -l` = 365; recursive listing via `find docs/ref -type f | sort`.
- Per-file size + disk mtime + git last-commit date: python os.walk + `git log --pretty=format:@%cI --name-only --no-renames -- docs/ref` (one pass, newest-first, first date seen per path = last touch). Raw data: inventory of 365 rows; every number below comes from that run.
- Staleness: >7d law (tools/freshness_check.py STALE_DAYS=7) against last-commit date; cutoff 2026-09-21 for today 2026-09-28.
- References: one `rg -F -i --hidden -f patterns.txt` pass over the repo (excluding .git/.venv/node_modules) with 2 path-form patterns per target (`docs/ref/<sub>`, `docs\ref\<sub>`) plus the bare basename for the 339 files whose basename is unique inside docs/ref (10 ambiguous basenames get path patterns only: README.md, INDEX.md, faq.md, introduction.md, overview.md, quick-start.md, stream-tool.md, web-search.md, LIGHT_OPERATOR_FOUNDATION_20260904.md, MAG_CHORD_V3_CANDIDATE_20260904.md). 10,057 raw matching lines post-processed; self-references excluded; weak-only = basename mentions with no path-form mention.
- Load-bearing: (a) rg `docs.ref` over mag/ tools/ scripts/ configs/ tests/ dashboard/ main.py mag.cmd githooks/ + boot docs; (b) targeted greps for path-BUILT readers (`'docs' / 'ref'` joins and dir globs) that string scans miss; (c) read mag/context_pack.py:884-909 and :1282-1293 directly.
- Git state of docs/ref: `git status --porcelain docs/ref` empty (all committed); `git check-ignore -v docs/ref/.mimosa/...` = .gitignore:190 `.mimosa/`.

## Headline numbers

| metric | n |
|---|---|
| files under docs/ref | 365 |
| committed + clean | 359 |
| stale (last commit > 7d, before 2026-09-21) | 349 (97.2% of committed) |
| fresh (commit within 7d) | 10 |
| never committed (gitignored .mimosa state) | 6 |
| BOOT-referenced (named in AGENTS.md / docs/FRAMEWORK_LOAD.md / README / RUNNING / CONSTITUTION / LOAD.md) | 38 |
| CODE-referenced (path or dir-read by code/config/tests under mag/ tools/ scripts/ configs/ dashboard/ githooks/ tests/) | 139 |
| SKILL-referenced (in-repo .agents/skills) | 7 |
| zero path-form references | 0 |
| weak-only (bare unique-basename mention, no path form) | 2 |

Verdict distribution: ESTATE+CORPUS=151, CODE=73, CODE+DIRREAD=31, BOOT+CODE=28, ESTATE=24, ESTATE+INT+CORPUS=23, BOOT+CORPUS=10, ESTATE+INT+DOC+CORPUS=8, ESTATE+DOC+CORPUS=8, CODE+SKILL=5, WEAK=2, SKILL+CODE+DIRREAD=2

## Load-bearing: the boot path and the context pack

1. Boot path (AGENTS.md:42-46,50 load-order table; docs/FRAMEWORK_LOAD.md:18-22,67-72,88). Every file the boot path names, with last-commit and staleness:

| boot-path file | last commit | age d | stale |
|---|---|---|---|
| docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md | 2026-09-27 | 1 | ok |
| docs/ref/MYCELIAL_SCIENCE_MAP.md | 2026-08-06 | 53 | STALE |
| docs/ref/MAG_DIRECTION_ARTIFACT_v2.md | 2026-08-06 | 53 | STALE |
| docs/ref/MAG_PROJECT_PROPOSAL.md | 2026-08-05 | 54 | STALE |
| docs/ref/OPERATOR_CARD.md | 2026-08-04 | 55 | STALE |
| docs/ref/MAG_VISION_AUTOMATION.md | 2026-08-06 | 53 | STALE |
| docs/ref/releases/VERSION_REGISTRY.md | 2026-09-27 | 1 | ok |

2. Context pack (mag/context_pack.py, what `mag.cmd context-pack` builds): it READS NO docs/ref file. It only embeds two strings: `"operator_path": "FIND → FILE → LOAD (docs/ref/OPERATOR_CARD.md)"` (mag/context_pack.py:892) and the docstring `Law: docs/ref/COORDINATION_ELIAS_ROPE.md` (mag/context_pack.py:1292). All `read_text` calls in the module target memory/, queue/, state/ artifacts (mag/context_pack.py:26,48,162,172,176,203,254,269,280,322,361,364,543,551,715,765,1065), none docs/ref.

3. Runtime code that actually READS docs/ref files (verified by reading the code):

- TREE (every .md or all files): scripts/corpus_packer.py:194-197 rglobs docs/ref/**/*.md into the corpus pack
- TREE (every .md or all files): dashboard/static/_build_scout_deck.py:173 iterates (WATCH, ROOT/'docs'/'ref')
- TREE (every .md or all files): tools/full_scan.py:37 includes ROOT/'docs'/'ref' in scan roots
- TREE (every .md or all files): main.py:1846 caveman-audit default --path is docs/ref
- DIR docs/ref/ractors/: tools/lens.py:44 BRIEFS = ROOT/'docs'/'ref'/'ractors'
- DIR docs/ref/ractors/: tools/letter_salon_20260920.py:59 reads ractors/<chair>.md
- DIR docs/ref/ractors/: tools/saturation_fourcond.py:50 BRIEFS ractors/BERNAYS.md
- DIR docs/ref/ractors/: tools/ocean_v2_pilot.py:42 BRIEFS ractors/BERNAYS.md
- DIR docs/ref/prompts/: scripts/build_vislab_catalog.py:246 globs docs/ref/prompts/*
- DIR docs/ref/canon/: scripts/build_knowledge_graph.py:35 includes docs/ref/canon as graph source
- DIR docs/ref/spores/mesh/: scripts/mesh_comm_ilap_run.sh:39 writes spore leafs to docs/ref/spores/mesh/
- FILE docs/ref/MAG_NEXT_CODING_RUN.md: mag/steward.py:22 `RUN_DOC = ROOT / "docs" / "ref" / "MAG_NEXT_CODING_RUN.md"`, read at :158-160 `RUN_DOC.read_text(...)`
- FILE docs/ref/STACK_V1.md + docs/ref/ZAI_API_EXPERT_REFERENCE.md: scripts/audit_bundle.py:26-27 bundle list
- FILE docs/ref/ractors/BERNAYS.md: tools/saturation_fourcond.py:50 and tools/ocean_v2_pilot.py:42 `BRIEF` constants

4. Labels only (string cites, no file read): dashboard/rest.py:1150-1151 + :1280 provenance labels for OPERATOR_CARD.md and MIRROR_PRESENTED.md; mag/context_pack.py:892 and :1292 above; tools/drift_pairs_stamp.py:321,344 `doc` fields pointing at docs/ref/releases/VERSION_REGISTRY.md.

5. Tests that consume docs/ref (run under pytest): tests/test_skill_seat.py:58 (`run_audit(paths=["docs/ref/PONYTAIL_CAVEMAN_AUDIT.md"])`), tests/test_virtual_desk_loop.py:41,47 (RESEARCH_MAG_VIRTUAL_DESK.txt brief), tests/test_pack_modes_steward.py:74 (monkeypatches steward RUN_DOC onto MAG_NEXT_CODING_RUN.md), tests/test_wow_bones.py:5 + tests/test_zai_backoff_floor.py:3 + tests/test_stealth_driver_effort_dial.py:64 (spec cites).

6. In-repo skill surfaces (.agents/skills, 8 reference instances): zai-reference SKILL.md:3,24 -> ZAI_API_EXPERT_REFERENCE.md; light-operator SKILL.md:3,23 -> canon/LIGHT_OPERATOR_FOUNDATION_20260904.md + canon/MAG_CHORD_V3_CANDIDATE_20260904.md; verb-genomes SKILL.md:11 -> verb_genomes/L0_contract.md + steal.md + self_steal.md; frontier-researcher SKILL.md:34,42 -> verb_genomes/research_socratic.md + SPORE_SANCHO.md; agent-harness SKILL.md:26 -> verb_genomes/research_socratic.md; operator-corrections SKILL.md:136 -> BIBLIOGRAPHY_MAP.md. NOTE: the .zcode skill mirrors under C:/Users/foste/.zcode/skills live OUTSIDE this repo and were not scanned (out of repo boundary).

## Findings

F1. STALENESS IS NEAR-TOTAL AND UNGATED: 349 of 359 committed docs/ref files (97.2%) last changed before 2026-09-21; only 10 are within 7d. tools/freshness_check.py:38-41 gates only BOOT_4_7.md + state/CURRENT.md + state/START_BRIEF.md + state/HANDOFF.md - docs/ref has NO freshness gate, so the >7d law never fires on this tree.

F2. THE BOOT PATH ITSELF IS MOSTLY STALE: of the 7 boot-named files, 2 are fresh (COMPASS and VERSION_REGISTRY, both 2026-09-27) and 5 are August-stale 53-55d (MYCELIAL_SCIENCE_MAP + MAG_DIRECTION_ARTIFACT_v2 + MAG_VISION_AUTOMATION 2026-08-06, MAG_PROJECT_PROPOSAL 2026-08-05, OPERATOR_CARD 2026-08-04). A new seat is booted through documents the freshness law would call STALE if they were watched.

F3. DANGLING BOOT REFERENCE: docs/FRAMEWORK_LOAD.md:114 cites `docs/ref/DECISION_LAYERS.md`; `ls docs/ref/DECISION_LAYERS.md` -> `No such file or directory`. The load-order doc points at a file that does not exist.

F4. CONTEXT-PACK LOAD-BEARING IS LABEL-ONLY: `mag.cmd context-pack` (mag.cmd:9 -> main.py) reads zero bytes from docs/ref; its only docs/ref content is a pointer string (mag/context_pack.py:892). The pack is not a docs/ref consumer; agents are.

F5. THE 6 NEVER-COMMITTED FILES ARE .mimosa STATE, NOT DOCS: docs/ref/.mimosa/** (finding-ledger, history, hook-state, 2 task-review reports) are gitignored via .gitignore:190 `.mimosa/`. The 2 task-review reports are also the only files in docs/ref with zero path-form references anywhere in the repo.

F6. TREE-LEVEL READERS MAKE EVERY .md CORPUS-FED: scripts/corpus_packer.py:194-197 rglobs docs/ref/**/*.md, so all 329 .md files in docs/ref are ingested by the corpus packer regardless of individual references; dashboard/static/_build_scout_deck.py:173, tools/full_scan.py:37 and main.py:1846 (caveman-audit default path) likewise sweep the whole tree. Per-file verdicts below therefore add +CORPUS to .md rows whose only code tie is tree-level.

F7. FRESH SET (all 10, last commit 2026-09-21 or later):

- docs/ref/KABUKI_STACK_20260905.md (2026-09-27, ESTATE+CORPUS)
- docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md (2026-09-27, BOOT+CODE)
- docs/ref/ZAI_API_EXPERT_REFERENCE.md (2026-09-27, CODE+SKILL)
- docs/ref/canon/LIGHT_OPERATOR_FOUNDATION_20260904.md (2026-09-27, SKILL+CODE+DIRREAD)
- docs/ref/canon/MAG_CHORD_V3_CANDIDATE_20260904.md (2026-09-27, SKILL+CODE+DIRREAD)
- docs/ref/canon/README.md (2026-09-27, CODE+DIRREAD)
- docs/ref/canon/CANDIDATE/LIGHT_OPERATOR_FOUNDATION_20260904.md (2026-09-27, CODE+DIRREAD)
- docs/ref/canon/CANDIDATE/MAG_CHORD_V3_CANDIDATE_20260904.md (2026-09-27, CODE+DIRREAD)
- docs/ref/canon/CANDIDATE/README.md (2026-09-27, CODE+DIRREAD)
- docs/ref/releases/VERSION_REGISTRY.md (2026-09-27, BOOT+CODE)

## Staleness by bucket

| bucket (dir under docs/ref) | files | stale |
|---|---|---|
| (root files) | 178 | 175 |
| zai_docs_mirror | 105 | 105 |
| canon | 16 | 10 |
| onepagers | 13 | 13 |
| ractors | 11 | 11 |
| releases | 8 | 7 |
| tesuji | 7 | 7 |
| .mimosa | 6 | 0 |
| verb_genomes | 6 | 6 |
| proposals | 4 | 4 |
| spores | 4 | 4 |
| prompts | 2 | 2 |
| weaves | 2 | 2 |
| skills | 1 | 1 |
| steals | 1 | 1 |
| templates | 1 | 1 |

## Per-file census (365 rows)

Columns: bytes; GIT-LAST = last commit date (disk mtime also captured, same row); AGE d from 2026-09-28; refs C=code/config/tests, B=boot docs, K=skills, E=estate notes (memory/ corpus/ watch/ queue/ state/ catalog/), I=internal docs/ref, O=other docs, W=weak-only basename mentions. Verdict: BOOT/CODE/SKILL/ESTATE/INT/DOC/WEAK/ZERO, +DIRREAD = member of a dir with a path-built reader, +CORPUS = tree-fed by corpus_packer (and not already CODE).

| file | bytes | git-last | mtime | age | C | B | K | E | I | O | W | verdict | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AGENTIC_LANDSCAPE_2026.md | 10226 | 2026-08-06 | 2026-08-06 | 53 | 0 | 1 | 0 | 16 | 3 | 1 | 13 | BOOT+CORPUS |  |
| AGENT_BLEEDING_EDGE_REPOS_INDEX.md | 14086 | 2026-08-06 | 2026-08-06 | 53 | 8 | 0 | 0 | 5 | 1 | 1 | 3 | CODE |  |
| AGENT_PLATFORM_REPOS_INDEX.md | 14628 | 2026-08-06 | 2026-08-06 | 53 | 8 | 0 | 0 | 4 | 2 | 1 | 6 | CODE |  |
| AGENT_UI_STEAL.md | 1487 | 2026-08-04 | 2026-08-04 | 55 | 0 | 0 | 0 | 2 | 0 | 0 | 4 | ESTATE+CORPUS |  |
| ANNALEA_STANDARD.md | 2641 | 2026-09-14 | 2026-09-12 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| BARE_METAL_PRIMITIVES.md | 2744 | 2026-09-14 | 2026-08-28 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 6 | ESTATE+CORPUS |  |
| BIBLIOGRAPHY_MAP.md | 65768 | 2026-09-14 | 2026-09-11 | 14 | 2 | 0 | 1 | 17 | 0 | 1 | 9 | CODE+SKILL |  |
| BOOT_PLAYBOOK.md | 3566 | 2026-09-14 | 2026-08-27 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| BUDDY_LETTER.md | 2448 | 2026-09-14 | 2026-09-04 | 14 | 0 | 0 | 0 | 5 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| BUILD-factory-audit-json-EXAMPLE.md | 2525 | 2026-08-05 | 2026-08-06 | 54 | 5 | 0 | 0 | 4 | 4 | 1 | 3 | CODE |  |
| BUILD-TEMPLATE.md | 1811 | 2026-08-05 | 2026-08-06 | 54 | 2 | 1 | 0 | 4 | 7 | 1 | 3 | BOOT+CODE |  |
| BUILD-v3-deepseek-run.md | 1617 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 4 | 1 | 1 | 2 | ESTATE+INT+DOC+CORPUS |  |
| BURST_DOCTRINE_20260903.md | 5266 | 2026-09-14 | 2026-09-04 | 14 | 14 | 0 | 0 | 10 | 1 | 1 | 3 | CODE |  |
| CACHE_CRAFT_LAWS_20260906.md | 1423 | 2026-09-14 | 2026-09-06 | 14 | 0 | 0 | 0 | 3 | 1 | 0 | 2 | ESTATE+INT+CORPUS |  |
| CHAIN_V2_ANCHOR_REGISTRY_SPEC.md | 5326 | 2026-09-14 | 2026-08-27 | 14 | 2 | 0 | 0 | 4 | 0 | 0 | 3 | CODE |  |
| CHAT_PLAY_LOOP.md | 1696 | 2026-09-14 | 2026-08-29 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| COMMON_LANGUAGE_SPEC.md | 3395 | 2026-09-14 | 2026-08-28 | 14 | 0 | 0 | 0 | 7 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| COORDINATION_ELIAS_ROPE.md | 7437 | 2026-08-04 | 2026-08-04 | 55 | 6 | 0 | 0 | 5 | 2 | 1 | 6 | CODE | mag/context_pack.py:1292 docstring cite (no read) |
| CORE_MEMORY_PROTOCOL.md | 3632 | 2026-09-14 | 2026-08-28 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| CUSTODY_AND_DISCLOSURE.md | 2605 | 2026-09-14 | 2026-08-27 | 14 | 0 | 0 | 0 | 4 | 0 | 1 | 4 | ESTATE+DOC+CORPUS |  |
| DASHBOARD_DESIGN.md | 3607 | 2026-08-05 | 2026-08-06 | 54 | 3 | 0 | 0 | 6 | 0 | 3 | 4 | CODE |  |
| DASHBOARD_PLUGIN_SURFACE.md | 2143 | 2026-08-07 | 2026-08-07 | 52 | 0 | 0 | 0 | 3 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| DATA_LAYERS.md | 4525 | 2026-08-07 | 2026-08-07 | 52 | 0 | 0 | 0 | 4 | 0 | 0 | 5 | ESTATE+CORPUS |  |
| DESK_GPU_HISTORY.md | 3519 | 2026-09-14 | 2026-08-28 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| DINNER_LOOP_REPORT.md | 1824 | 2026-08-06 | 2026-08-06 | 53 | 0 | 0 | 0 | 18 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| DM_MAG_TRANSFER.md | 1706 | 2026-08-07 | 2026-08-07 | 52 | 2 | 0 | 0 | 2 | 1 | 1 | 3 | CODE |  |
| DOGFOOD_PROGRAM.md | 3983 | 2026-09-14 | 2026-08-28 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| DUAL_PROGRESS_STATUS.md | 1246 | 2026-08-06 | 2026-08-06 | 53 | 0 | 0 | 0 | 6 | 1 | 0 | 6 | ESTATE+INT+CORPUS |  |
| ENV_SWITCHING.md | 1413 | 2026-08-06 | 2026-08-06 | 53 | 0 | 0 | 0 | 2 | 1 | 1 | 2 | ESTATE+INT+DOC+CORPUS |  |
| evidence_states_audit.md | 3888 | 2026-09-14 | 2026-09-12 | 14 | 1 | 0 | 0 | 2 | 0 | 1 | 2 | CODE |  |
| evidence_states_audit_prep.md | 2250 | 2026-09-14 | 2026-09-12 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| EXTROPIC_Z1T_DIGEST_20260904.md | 8192 | 2026-09-14 | 2026-09-04 | 14 | 0 | 0 | 0 | 9 | 1 | 0 | 2 | ESTATE+INT+CORPUS |  |
| FOREIGN_GSTD_DEEPDIVE_20260827.md | 3920 | 2026-09-14 | 2026-08-26 | 14 | 0 | 0 | 0 | 4 | 1 | 0 | 3 | ESTATE+INT+CORPUS |  |
| FORTRESS_AND_REPUBLIC.md | 4415 | 2026-08-09 | 2026-08-08 | 50 | 0 | 0 | 0 | 19 | 1 | 0 | 21 | ESTATE+INT+CORPUS |  |
| FRONTIER_PROMPT_V1.md | 6884 | 2026-09-14 | 2026-09-10 | 14 | 0 | 0 | 0 | 4 | 1 | 0 | 2 | ESTATE+INT+CORPUS |  |
| GAME_SALON_LOOP.md | 851 | 2026-08-07 | 2026-08-06 | 52 | 0 | 0 | 0 | 3 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| GAME_THEORY_PLAY_MAP.md | 4656 | 2026-08-07 | 2026-08-06 | 52 | 4 | 0 | 0 | 18 | 1 | 0 | 8 | CODE |  |
| GAME_VILLAIN_GUILD_DESIGN.md | 2528 | 2026-09-14 | 2026-08-27 | 14 | 2 | 0 | 0 | 4 | 0 | 3 | 3 | CODE |  |
| GLM53_ARCHITECTURE_PRO.md | 3476 | 2026-09-14 | 2026-08-28 | 14 | 1 | 0 | 0 | 3 | 1 | 0 | 6 | CODE |  |
| GLM53_FLASH_EXPLOITATION.md | 4717 | 2026-09-14 | 2026-08-28 | 14 | 2 | 0 | 0 | 3 | 0 | 0 | 7 | CODE |  |
| GLM_K8S_MCP_DEEP_RESEARCH_20260826.md | 17716 | 2026-09-14 | 2026-08-26 | 14 | 0 | 0 | 0 | 42 | 2 | 0 | 9 | ESTATE+INT+CORPUS |  |
| GRAYSWAN_ARENA_STEAL.md | 5235 | 2026-09-14 | 2026-08-28 | 14 | 1 | 0 | 0 | 7 | 1 | 0 | 3 | CODE |  |
| GSTDCOIN_REPOS_INDEX.md | 2284 | 2026-08-05 | 2026-08-06 | 54 | 4 | 0 | 0 | 10 | 2 | 1 | 3 | CODE |  |
| HARNESS_SPEC.md | 4050 | 2026-09-14 | 2026-08-28 | 14 | 6 | 0 | 0 | 9 | 0 | 2 | 9 | CODE |  |
| HOME_HARDWARE_ENVELOPE.md | 3430 | 2026-08-07 | 2026-08-06 | 52 | 0 | 0 | 0 | 5 | 2 | 0 | 5 | ESTATE+INT+CORPUS |  |
| HOME_PC_SYNC.md | 3039 | 2026-08-06 | 2026-08-08 | 53 | 4 | 1 | 0 | 4 | 1 | 0 | 3 | BOOT+CODE |  |
| HONEST_COST_LEDGER.md | 5543 | 2026-09-14 | 2026-09-02 | 14 | 2 | 0 | 0 | 4 | 1 | 1 | 2 | CODE |  |
| IDEA_GRAPH.md | 2910 | 2026-08-04 | 2026-08-04 | 55 | 4 | 0 | 0 | 16 | 0 | 0 | 2 | CODE |  |
| JONES_AGENT_FLEET_PACK.md | 8415 | 2026-08-05 | 2026-08-06 | 54 | 2 | 1 | 0 | 5 | 2 | 1 | 5 | BOOT+CODE |  |
| KABUKI_STACK_20260905.md | 3445 | 2026-09-27 | 2026-09-26 | 1 | 0 | 0 | 0 | 14 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| KV_CACHE_ECON.md | 5673 | 2026-09-14 | 2026-09-07 | 14 | 0 | 0 | 0 | 5 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| LAYMAN_OFFICE_VISION.md | 10211 | 2026-08-05 | 2026-08-06 | 54 | 0 | 1 | 0 | 5 | 3 | 0 | 4 | BOOT+CORPUS |  |
| lessig_1_6.md | 2081 | 2026-08-04 | 2026-08-04 | 55 | 4 | 0 | 0 | 8 | 2 | 1 | 4 | CODE |  |
| LEXICON.md | 2919 | 2026-09-14 | 2026-08-27 | 14 | 0 | 0 | 0 | 11 | 6 | 0 | 6 | ESTATE+INT+CORPUS |  |
| LINEAGE_AUDIT_PLAN.md | 3425 | 2026-09-14 | 2026-08-27 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| LINEAGE_POINTERS.md | 4172 | 2026-09-14 | 2026-09-04 | 14 | 6 | 0 | 0 | 12 | 0 | 4 | 3 | CODE |  |
| LING_API_REFERENCE.md | 3849 | 2026-09-14 | 2026-09-12 | 14 | 0 | 0 | 0 | 7 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| MAG_Activation.md | 1584 | 2026-08-05 | 2026-08-06 | 54 | 0 | 1 | 0 | 3 | 1 | 0 | 8 | BOOT+CORPUS |  |
| MAG_AGENT_ERROR_CATALOG.md | 10352 | 2026-08-05 | 2026-08-06 | 54 | 2 | 1 | 0 | 5 | 2 | 1 | 2 | BOOT+CODE |  |
| MAG_BEHAVIORAL_COMPOUNDING.md | 13436 | 2026-08-06 | 2026-08-06 | 53 | 6 | 1 | 0 | 17 | 3 | 0 | 11 | BOOT+CODE |  |
| MAG_BUILD_PIPELINE.md | 10928 | 2026-08-05 | 2026-08-06 | 54 | 4 | 1 | 0 | 4 | 8 | 2 | 5 | BOOT+CODE |  |
| MAG_Card.md | 938 | 2026-08-04 | 2026-08-04 | 55 | 0 | 1 | 0 | 4 | 2 | 0 | 10 | BOOT+CORPUS |  |
| MAG_DIRECTION_ARTIFACT_v2.md | 13682 | 2026-08-06 | 2026-08-06 | 53 | 7 | 2 | 0 | 13 | 5 | 0 | 7 | BOOT+CODE |  |
| MAG_FACTORY_PILOT.md | 3568 | 2026-08-06 | 2026-08-06 | 53 | 0 | 1 | 0 | 4 | 4 | 1 | 8 | BOOT+CORPUS |  |
| MAG_FULL_BLAST_PLAN.md | 12931 | 2026-08-05 | 2026-08-06 | 54 | 0 | 1 | 0 | 4 | 0 | 0 | 2 | BOOT+CORPUS |  |
| MAG_FUTURE_WALKTHROUGH.md | 15128 | 2026-08-06 | 2026-08-06 | 53 | 2 | 2 | 0 | 5 | 1 | 1 | 4 | BOOT+CODE |  |
| MAG_ILAP_PROTOCOL.md | 11819 | 2026-08-05 | 2026-08-06 | 54 | 5 | 1 | 0 | 6 | 7 | 0 | 5 | BOOT+CODE |  |
| MAG_LLM_FEED_PACK.md | 15003 | 2026-08-05 | 2026-08-06 | 54 | 0 | 1 | 0 | 7 | 1 | 1 | 6 | BOOT+CORPUS |  |
| MAG_LOCAL_STEWARD.md | 8208 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 2 | 1 | 0 | 6 | ESTATE+INT+CORPUS |  |
| MAG_LOOP_DISCIPLINE.md | 4838 | 2026-08-06 | 2026-08-06 | 53 | 6 | 0 | 0 | 5 | 3 | 0 | 6 | CODE |  |
| MAG_MOBILE_VOICE_SPEC.md | 11957 | 2026-08-07 | 2026-08-06 | 52 | 8 | 1 | 0 | 7 | 3 | 0 | 3 | BOOT+CODE |  |
| MAG_MYCELIAL_REPUBLIC_COMPASS.md | 13132 | 2026-09-27 | 2026-09-26 | 1 | 4 | 4 | 0 | 44 | 3 | 4 | 10 | BOOT+CODE |  |
| MAG_NEXT_CODING_RUN.md | 12812 | 2026-08-06 | 2026-08-06 | 53 | 7 | 1 | 0 | 17 | 4 | 2 | 10 | BOOT+CODE | mag/steward.py:22 RUN_DOC const, :158-160 runtime read_text |
| MAG_OS_v2.md | 2140 | 2026-08-05 | 2026-08-06 | 54 | 11 | 0 | 0 | 6 | 2 | 3 | 5 | CODE |  |
| MAG_PROJECT_PROPOSAL.md | 16216 | 2026-08-05 | 2026-08-06 | 54 | 9 | 4 | 0 | 12 | 3 | 1 | 9 | BOOT+CODE |  |
| MAG_SEAT_INTELLIGENCE.md | 8560 | 2026-08-07 | 2026-08-07 | 52 | 2 | 0 | 0 | 3 | 1 | 0 | 3 | CODE |  |
| MAG_STEAL_AUTOPILOT.md | 14169 | 2026-08-07 | 2026-08-06 | 52 | 4 | 1 | 0 | 5 | 1 | 2 | 8 | BOOT+CODE |  |
| MAG_SWITCHBOARD_VISION.md | 6225 | 2026-08-05 | 2026-08-06 | 54 | 2 | 1 | 0 | 3 | 1 | 0 | 3 | BOOT+CODE |  |
| MAG_TRAINING_DATA_SPEC.md | 13430 | 2026-08-05 | 2026-08-06 | 54 | 2 | 0 | 0 | 5 | 8 | 0 | 10 | CODE |  |
| MAG_v2_PLAN.md | 20612 | 2026-08-05 | 2026-08-06 | 54 | 10 | 1 | 0 | 6 | 3 | 2 | 9 | BOOT+CODE |  |
| MAG_v3_BACKLOG.md | 11914 | 2026-08-05 | 2026-08-06 | 54 | 4 | 1 | 0 | 4 | 3 | 1 | 9 | BOOT+CODE |  |
| MAG_V3_DISPATCH_PLAN.md | 13522 | 2026-08-05 | 2026-08-06 | 54 | 4 | 1 | 0 | 5 | 4 | 1 | 3 | BOOT+CODE |  |
| MAG_v3_RESEARCH_PLAN.md | 9564 | 2026-08-05 | 2026-08-06 | 54 | 6 | 1 | 0 | 3 | 3 | 1 | 6 | BOOT+CODE |  |
| MAG_v3_SWARM_VISION.md | 16695 | 2026-08-05 | 2026-08-06 | 54 | 2 | 1 | 0 | 16 | 3 | 0 | 7 | BOOT+CODE |  |
| MAG_V4_CONDUCTOR_LOOP_DRAFT.md | 14481 | 2026-08-05 | 2026-08-06 | 54 | 8 | 0 | 0 | 2 | 6 | 0 | 11 | CODE |  |
| MAG_v4_THEORY.md | 6284 | 2026-08-05 | 2026-08-06 | 54 | 0 | 1 | 0 | 3 | 1 | 1 | 5 | BOOT+CORPUS |  |
| MAG_v5_GSTD_FOREST.md | 6753 | 2026-08-05 | 2026-08-06 | 54 | 2 | 0 | 0 | 7 | 6 | 0 | 7 | CODE |  |
| MAG_v5_MESH_FOREST.md | 6875 | 2026-08-05 | 2026-08-06 | 54 | 1 | 0 | 0 | 2 | 1 | 0 | 6 | CODE |  |
| MAG_v5_PIPE.md | 5772 | 2026-08-05 | 2026-08-06 | 54 | 2 | 0 | 0 | 4 | 3 | 0 | 12 | CODE |  |
| MAG_v5_VAST_TRAINING.md | 5850 | 2026-08-05 | 2026-08-06 | 54 | 4 | 0 | 0 | 9 | 6 | 0 | 4 | CODE |  |
| MAG_v5_XRPL.md | 5376 | 2026-08-05 | 2026-08-06 | 54 | 2 | 0 | 0 | 4 | 3 | 0 | 5 | CODE |  |
| MAG_VISION_AUTOMATION.md | 23379 | 2026-08-06 | 2026-08-06 | 53 | 2 | 2 | 0 | 4 | 1 | 0 | 6 | BOOT+CODE |  |
| MCP_MANIFEST_SPEC.md | 11832 | 2026-09-14 | 2026-09-04 | 14 | 2 | 0 | 0 | 17 | 0 | 4 | 3 | CODE |  |
| memory_verkle_map.md | 2274 | 2026-08-04 | 2026-08-04 | 55 | 4 | 1 | 0 | 6 | 4 | 1 | 9 | BOOT+CODE |  |
| MESH_COMM_REPOS_INDEX.md | 7487 | 2026-08-05 | 2026-08-06 | 54 | 15 | 0 | 0 | 2 | 2 | 0 | 6 | CODE |  |
| MESH_LOCAL_AGENT.md | 4132 | 2026-08-05 | 2026-08-06 | 54 | 5 | 1 | 0 | 4 | 2 | 0 | 2 | BOOT+CODE |  |
| MESH_PIPELINE_20260903.md | 9316 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| MIRROR_PRESENTED.md | 1970 | 2026-08-04 | 2026-08-04 | 55 | 7 | 0 | 0 | 9 | 2 | 4 | 3 | CODE | rest.py:1151 provenance label (no read) |
| MYCELIAL_SCIENCE_MAP.md | 12875 | 2026-08-06 | 2026-08-06 | 53 | 2 | 3 | 0 | 22 | 3 | 0 | 5 | BOOT+CODE |  |
| NERVOUS_SYSTEM.md | 1224 | 2026-09-14 | 2026-08-28 | 14 | 0 | 0 | 0 | 9 | 2 | 0 | 29 | ESTATE+INT+CORPUS |  |
| NG_AISRP_RIGHTSIZED.md | 3691 | 2026-09-14 | 2026-08-28 | 14 | 1 | 0 | 0 | 2 | 0 | 0 | 2 | CODE |  |
| NNUE_ACCUMULATOR_DESIGN_20260904.md | 5439 | 2026-09-14 | 2026-09-04 | 14 | 2 | 0 | 0 | 6 | 1 | 0 | 2 | CODE |  |
| NNUE_SIDECAR_BRIEF_20260904.generator.js | 11106 | 2026-09-14 | 2026-09-04 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE |  |
| NNUE_SIDECAR_BRIEF_20260904.md | 10064 | 2026-09-14 | 2026-09-04 | 14 | 2 | 0 | 0 | 4 | 2 | 0 | 2 | CODE |  |
| ONTOLOGY_COMPILER_PHASE1.md | 3247 | 2026-09-08 | 2026-09-08 | 20 | 0 | 0 | 0 | 3 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| OPERATOR_CARD.md | 4888 | 2026-08-04 | 2026-08-04 | 55 | 21 | 2 | 0 | 19 | 4 | 6 | 10 | BOOT+CODE | context_pack.py:892 payload string, rest.py:1150/1280 provenance label (labels, no read) |
| OPERATOR_GATES_SCHEMA.md | 2643 | 2026-09-14 | 2026-09-12 | 14 | 0 | 0 | 0 | 5 | 0 | 2 | 2 | ESTATE+DOC+CORPUS |  |
| OPERATOR_SURVIVAL_EXTRACT.md | 5797 | 2026-08-05 | 2026-08-06 | 54 | 5 | 0 | 0 | 2 | 0 | 0 | 2 | CODE |  |
| PHYSICAL_ENFORCEMENT_TOOLKIT_20260904.md | 4971 | 2026-09-14 | 2026-09-04 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| PLANNING_MODE.md | 3026 | 2026-08-04 | 2026-08-04 | 55 | 0 | 0 | 0 | 4 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| PLATFORM_AUDIT.md | 4259 | 2026-08-04 | 2026-08-04 | 55 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| PLAY_BENCHMARK.md | 4306 | 2026-08-07 | 2026-08-06 | 52 | 2 | 0 | 0 | 3 | 3 | 0 | 3 | CODE |  |
| PONYTAIL_CAVEMAN_AUDIT.md | 3264 | 2026-08-05 | 2026-08-06 | 54 | 1 | 0 | 0 | 3 | 3 | 0 | 5 | CODE | tests/test_skill_seat.py:58 run_audit(paths=[...]) |
| PONYTAIL_CAVEMAN_SKILLS.md | 4854 | 2026-08-05 | 2026-08-06 | 54 | 0 | 1 | 0 | 3 | 1 | 0 | 3 | BOOT+CORPUS |  |
| PRODUCT_VISION_AUTORUN.md | 1929 | 2026-08-05 | 2026-08-06 | 54 | 2 | 0 | 0 | 3 | 0 | 0 | 12 | CODE |  |
| PROJECT_VERKLE_GROK_BUILD_HANDOFF.md | 4245 | 2026-08-06 | 2026-08-06 | 53 | 0 | 0 | 0 | 5 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| PROPOSAL_TO_THE_SWARM_20260905.md | 5542 | 2026-09-14 | 2026-09-06 | 14 | 0 | 0 | 0 | 7 | 0 | 2 | 3 | ESTATE+DOC+CORPUS |  |
| PROVIDER_LANE_MAP_20260902.md | 5471 | 2026-09-14 | 2026-09-02 | 14 | 2 | 0 | 0 | 4 | 0 | 1 | 2 | CODE |  |
| RESEARCH_MAG_VIRTUAL_DESK.md | 13640 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 5 | 2 | 1 | 2 | ESTATE+INT+DOC+CORPUS |  |
| RESEARCH_MAG_VIRTUAL_DESK.txt | 15380 | 2026-08-05 | 2026-08-06 | 54 | 9 | 0 | 0 | 5 | 0 | 1 | 6 | CODE | tests/test_virtual_desk_loop.py:41,47 brief_paths read |
| RESEARCH_NOTE_FLYWHEEL_BUDGET_PROJECTION.md | 3498 | 2026-09-14 | 2026-08-27 | 14 | 0 | 0 | 0 | 4 | 2 | 1 | 2 | ESTATE+INT+DOC+CORPUS |  |
| RETROSPECTIVE_V4_1.md | 5225 | 2026-09-14 | 2026-08-28 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| ROUTE_COVERAGE.md | 5384 | 2026-08-08 | 2026-08-08 | 51 | 0 | 0 | 0 | 3 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| RTFM_20260904.md | 27427 | 2026-09-14 | 2026-09-04 | 14 | 9 | 0 | 0 | 6 | 1 | 4 | 3 | CODE |  |
| RUN.md | 6865 | 2026-08-09 | 2026-08-09 | 50 | 0 | 1 | 0 | 4 | 0 | 0 | 94 | BOOT+CORPUS |  |
| run_trail_lattice.md | 3930 | 2026-08-04 | 2026-08-04 | 55 | 4 | 0 | 0 | 8 | 3 | 3 | 2 | CODE |  |
| SAELIS_DOSSIER.md | 6391 | 2026-09-14 | 2026-08-28 | 14 | 0 | 0 | 0 | 18 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| SEAT_AUDIT_SOCRATIC.md | 5863 | 2026-09-14 | 2026-08-28 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| SEAT_FARM.md | 3570 | 2026-09-14 | 2026-08-28 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| shadertoy_rule_lattice.md | 17952 | 2026-09-14 | 2026-09-03 | 14 | 17 | 0 | 0 | 7 | 0 | 0 | 2 | CODE |  |
| SHARED_STATELESS_SCRATCH.md | 11865 | 2026-08-06 | 2026-08-06 | 53 | 1 | 0 | 0 | 4 | 2 | 1 | 2 | CODE |  |
| SKILL_ECOSYSTEM_MAP.md | 10337 | 2026-08-07 | 2026-08-06 | 52 | 2 | 0 | 0 | 2 | 0 | 0 | 2 | CODE |  |
| SOVEREIGN_STACK.md | 4554 | 2026-08-04 | 2026-08-05 | 55 | 0 | 0 | 0 | 3 | 0 | 1 | 3 | ESTATE+DOC+CORPUS |  |
| SPORES.md | 3251 | 2026-08-07 | 2026-08-07 | 52 | 0 | 0 | 0 | 23 | 2 | 1 | 3 | ESTATE+INT+DOC+CORPUS |  |
| SPORE_CONTINUITY_SCHEMA.md | 6769 | 2026-09-14 | 2026-09-12 | 14 | 0 | 0 | 0 | 5 | 0 | 1 | 2 | ESTATE+DOC+CORPUS |  |
| spore_reading_guide.md | 1393 | 2026-09-14 | 2026-09-12 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| SPORE_SANCHO.md | 4695 | 2026-09-14 | 2026-08-26 | 14 | 4 | 0 | 1 | 23 | 2 | 1 | 7 | CODE+SKILL |  |
| SPORE_VNEXT_DELTA.md | 28107 | 2026-09-14 | 2026-08-27 | 14 | 0 | 0 | 0 | 5 | 0 | 0 | 6 | ESTATE+CORPUS |  |
| STACK_V1.md | 5960 | 2026-09-14 | 2026-09-10 | 14 | 9 | 0 | 0 | 8 | 0 | 5 | 14 | CODE | scripts/audit_bundle.py:26 bundle list |
| STEAL_MATRIX.md | 2501 | 2026-09-14 | 2026-08-27 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| STEAL_PROTOCOL_REPOS_INDEX.md | 2589 | 2026-08-06 | 2026-08-06 | 53 | 12 | 0 | 0 | 2 | 1 | 0 | 4 | CODE |  |
| strike_origin.json | 4427 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE |  |
| strike_origin.md | 6196 | 2026-08-04 | 2026-08-04 | 55 | 9 | 1 | 0 | 11 | 4 | 5 | 11 | BOOT+CODE |  |
| SURFACES.md | 5360 | 2026-09-14 | 2026-08-29 | 14 | 0 | 0 | 0 | 18 | 2 | 3 | 7 | ESTATE+INT+DOC+CORPUS |  |
| SURFACES_EXPLOITATION_MAP.md | 3414 | 2026-09-14 | 2026-08-27 | 14 | 2 | 0 | 0 | 6 | 1 | 0 | 4 | CODE |  |
| TABLE_DOGFOOD.md | 1526 | 2026-08-07 | 2026-08-07 | 52 | 2 | 0 | 0 | 3 | 1 | 0 | 2 | CODE |  |
| TABLE_SHELL_ARCH.md | 2032 | 2026-08-07 | 2026-08-06 | 52 | 2 | 0 | 0 | 2 | 1 | 0 | 2 | CODE |  |
| TAPESTRY_VERKLE_VISUAL.md | 2501 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 2 | 0 | 1 | 2 | ESTATE+DOC+CORPUS |  |
| THE_FENCE.md | 3785 | 2026-09-14 | 2026-09-10 | 14 | 2 | 0 | 0 | 5 | 0 | 0 | 3 | CODE |  |
| THE_FENCE_FINAL.md | 2694 | 2026-09-14 | 2026-09-10 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| THE_FENCE_PUBLISHED.md | 6020 | 2026-09-14 | 2026-09-10 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| THE_MOVING_WALL_FINAL.md | 3441 | 2026-09-14 | 2026-09-10 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| THE_MOVING_WALL_POST_20260911.md | 3485 | 2026-09-14 | 2026-09-10 | 14 | 0 | 0 | 0 | 6 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| THE_OS_THESIS.md | 13406 | 2026-09-14 | 2026-09-10 | 14 | 0 | 0 | 0 | 7 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| THE_PARABLE_OF_THE_MOVING_WALL.md | 3754 | 2026-09-14 | 2026-09-10 | 14 | 0 | 0 | 0 | 5 | 1 | 0 | 2 | ESTATE+INT+CORPUS |  |
| THE_TAPED_LAYER.md | 4284 | 2026-09-14 | 2026-09-06 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| TOKEN_CHAIN.md | 1520 | 2026-08-06 | 2026-08-06 | 53 | 0 | 0 | 0 | 3 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| TRAJECTORY_ARCHITECTURE.md | 3755 | 2026-09-14 | 2026-08-28 | 14 | 0 | 0 | 0 | 10 | 0 | 2 | 3 | ESTATE+DOC+CORPUS |  |
| TRAJECTORY_RIB_COMPILER_SPEC.md | 4549 | 2026-09-14 | 2026-08-27 | 14 | 5 | 0 | 0 | 14 | 0 | 0 | 5 | CODE |  |
| UTILIZATION_MAP.md | 3528 | 2026-09-14 | 2026-08-27 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| UX_UI_FOUNDATIONS.md | 4497 | 2026-08-14 | 2026-08-12 | 45 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| V3_DEEPSEEK_RUN.md | 4236 | 2026-08-06 | 2026-08-06 | 53 | 2 | 0 | 0 | 3 | 3 | 1 | 4 | CODE |  |
| V3_HOME_SHIP_CHECKLIST.md | 3014 | 2026-08-05 | 2026-08-06 | 54 | 2 | 0 | 0 | 2 | 2 | 0 | 2 | CODE |  |
| V4_BUILD_PLAN.md | 4150 | 2026-09-14 | 2026-08-27 | 14 | 0 | 0 | 0 | 5 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| V4_SPEC.md | 5986 | 2026-09-14 | 2026-08-27 | 14 | 2 | 0 | 0 | 6 | 0 | 2 | 3 | CODE |  |
| VAST_API_EXPERT_REFERENCE.md | 11658 | 2026-09-14 | 2026-08-28 | 14 | 0 | 0 | 0 | 3 | 3 | 2 | 4 | ESTATE+INT+DOC+CORPUS |  |
| VAST_DEEP_GROK_ECONOMICS.md | 40463 | 2026-09-14 | 2026-08-27 | 14 | 0 | 0 | 0 | 3 | 1 | 0 | 3 | ESTATE+INT+CORPUS |  |
| VAST_DEEP_GROK_SERVERLESS.md | 36026 | 2026-09-14 | 2026-08-27 | 14 | 0 | 0 | 0 | 3 | 1 | 0 | 2 | ESTATE+INT+CORPUS |  |
| VAST_DEEP_GROK_THROUGHPUT.md | 36966 | 2026-09-14 | 2026-08-27 | 14 | 0 | 0 | 0 | 3 | 1 | 0 | 3 | ESTATE+INT+CORPUS |  |
| VERKLE_KZG_BOUNDARY_20260901.md | 4641 | 2026-09-14 | 2026-09-01 | 14 | 0 | 0 | 0 | 3 | 1 | 0 | 2 | ESTATE+INT+CORPUS |  |
| VERKLE_REBUILD_COMPLETION_20260901.md | 6500 | 2026-09-14 | 2026-09-02 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| VOICE_DIG_LOOP.md | 2193 | 2026-08-07 | 2026-08-06 | 52 | 0 | 0 | 0 | 2 | 1 | 0 | 3 | ESTATE+INT+CORPUS |  |
| VSCODE_COPILOT_DEEPSEEK.md | 3973 | 2026-08-07 | 2026-08-07 | 52 | 2 | 0 | 0 | 3 | 1 | 0 | 2 | CODE |  |
| witness_sampling_primer.md | 1269 | 2026-09-14 | 2026-09-12 | 14 | 0 | 0 | 0 | 2 | 0 | 1 | 2 | ESTATE+DOC+CORPUS |  |
| WORLD_ROLES_AND_RIDDLE.md | 1813 | 2026-08-07 | 2026-08-06 | 52 | 0 | 0 | 0 | 2 | 1 | 1 | 4 | ESTATE+INT+DOC+CORPUS |  |
| WOW_ACORE_STEAL_MAP_20260915.md | 13574 | 2026-09-15 | 2026-09-15 | 13 | 1 | 0 | 0 | 7 | 0 | 0 | 2 | CODE | tests/test_wow_bones.py:5 falsifiable spec |
| WOW_FAMILY_LINEAGE_20260915.md | 8808 | 2026-09-15 | 2026-09-15 | 13 | 0 | 0 | 0 | 5 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| ZAI_API_EXPERT_REFERENCE.md | 30114 | 2026-09-27 | 2026-09-26 | 1 | 23 | 0 | 1 | 44 | 1 | 4 | 9 | CODE+SKILL | scripts/audit_bundle.py:27 bundle list; .agents/skills/zai-reference SKILL index; tests/test_zai_backoff_floor.py:3 |
| .mimosa/finding-ledger/v1/events/batch-stop-20260827T054854752Z-27484-dc741825c791.json | 1669 | NEVER | 2026-08-27 | n/a | 0 | 0 | 0 | 1 | 0 | 0 | 2 | ESTATE |  |
| .mimosa/history/run-20260827T054854752Z-27484-dc741825c791.json | 1211 | NEVER | 2026-08-27 | n/a | 0 | 0 | 0 | 1 | 0 | 0 | 2 | ESTATE |  |
| .mimosa/hook-state/sess_c5f7b48a-8764-4b0a-a49c-9b45084cefba.continue.json | 177 | NEVER | 2026-08-27 | n/a | 0 | 0 | 0 | 1 | 0 | 0 | 3 | ESTATE |  |
| .mimosa/hook-state/sess_c5f7b48a-8764-4b0a-a49c-9b45084cefba.json | 449 | NEVER | 2026-08-27 | n/a | 0 | 0 | 0 | 1 | 0 | 0 | 3 | ESTATE |  |
| .mimosa/reports/task-review-sess_c5f7b48a-8764-4b0a-a49c-9b45084cefba-20260827T054854752Z-27484-dc741825c791.json | 4335 | NEVER | 2026-08-27 | n/a | 0 | 0 | 0 | 0 | 0 | 0 | 2 | WEAK |  |
| .mimosa/reports/task-review-sess_c5f7b48a-8764-4b0a-a49c-9b45084cefba.json | 4335 | NEVER | 2026-08-27 | n/a | 0 | 0 | 0 | 0 | 0 | 0 | 3 | WEAK |  |
| canon/canon_bubbles_holographic_transfer.txt | 55576 | 2026-09-14 | 2026-09-01 | 14 | 0 | 0 | 0 | 4 | 1 | 0 | 6 | CODE+DIRREAD |  |
| canon/canon_gauntlet_tokenpilot_physical.txt | 16617 | 2026-09-14 | 2026-09-01 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 3 | CODE+DIRREAD |  |
| canon/canon_model_rib_boundary.md | 7843 | 2026-09-14 | 2026-09-04 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 2 | CODE+DIRREAD |  |
| canon/canon_spore_ledger_v5_v7.txt | 99662 | 2026-09-14 | 2026-09-01 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | CODE+DIRREAD |  |
| canon/canon_substrate_native_computing.txt | 251642 | 2026-09-14 | 2026-08-30 | 14 | 0 | 0 | 0 | 5 | 0 | 0 | 4 | CODE+DIRREAD |  |
| canon/canon_surveillance_let_them_watch.txt | 1985 | 2026-09-14 | 2026-09-04 | 14 | 0 | 0 | 0 | 6 | 0 | 0 | 2 | CODE+DIRREAD |  |
| canon/canon_tokens_as_spores_v8.txt | 224612 | 2026-09-14 | 2026-09-02 | 14 | 1 | 0 | 0 | 8 | 1 | 0 | 3 | CODE+DIRREAD |  |
| canon/canon_world_games_cache_farming_1.txt | 29818 | 2026-09-14 | 2026-09-01 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 3 | CODE+DIRREAD |  |
| canon/canon_world_games_cache_farming_2.txt | 48058 | 2026-09-14 | 2026-09-01 | 14 | 0 | 0 | 0 | 2 | 1 | 0 | 2 | CODE+DIRREAD |  |
| canon/LIGHT_OPERATOR_FOUNDATION_20260904.md | 534 | 2026-09-27 | 2026-09-26 | 1 | 0 | 0 | 1 | 16 | 0 | 0 | 0 | SKILL+CODE+DIRREAD |  |
| canon/MAG_CHORD_V3_CANDIDATE_20260904.md | 512 | 2026-09-27 | 2026-09-26 | 1 | 0 | 0 | 1 | 16 | 0 | 0 | 0 | SKILL+CODE+DIRREAD |  |
| canon/philbrick_opamp_applications_1964.png | 615974 | 2026-09-14 | 2026-09-02 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 3 | CODE+DIRREAD |  |
| canon/README.md | 2103 | 2026-09-27 | 2026-09-26 | 1 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | CODE+DIRREAD |  |
| canon/CANDIDATE/LIGHT_OPERATOR_FOUNDATION_20260904.md | 6625 | 2026-09-27 | 2026-09-26 | 1 | 0 | 0 | 0 | 14 | 1 | 0 | 0 | CODE+DIRREAD |  |
| canon/CANDIDATE/MAG_CHORD_V3_CANDIDATE_20260904.md | 9147 | 2026-09-27 | 2026-09-26 | 1 | 0 | 0 | 0 | 14 | 1 | 0 | 0 | CODE+DIRREAD |  |
| canon/CANDIDATE/README.md | 590 | 2026-09-27 | 2026-09-26 | 1 | 0 | 0 | 0 | 13 | 0 | 0 | 0 | CODE+DIRREAD |  |
| onepagers/01-v4-north-star.md | 1659 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 2 | 1 | 0 | 3 | ESTATE+INT+CORPUS |  |
| onepagers/02-loop-discipline.md | 1551 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 2 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| onepagers/03-seat-economics.md | 1442 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 2 | 1 | 0 | 3 | ESTATE+INT+CORPUS |  |
| onepagers/04-local-steward.md | 1419 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 2 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| onepagers/05-wiring-gaps.md | 1653 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 4 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| onepagers/06-layered-law.md | 1785 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 2 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| onepagers/07-engine-handoff.md | 2001 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 2 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| onepagers/08-seat-intelligence.md | 1310 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 2 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| onepagers/09-gstd-v5-pipe.md | 866 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 2 | 1 | 0 | 4 | ESTATE+INT+CORPUS |  |
| onepagers/10-vast-training-v5.md | 679 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 3 | 0 | 0 | 4 | ESTATE+CORPUS |  |
| onepagers/11-xrpl-v5-pipe.md | 559 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 2 | 0 | 0 | 4 | ESTATE+CORPUS |  |
| onepagers/12-v5-pipe-umbrella.md | 493 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 2 | 0 | 0 | 4 | ESTATE+CORPUS |  |
| onepagers/README.md | 1526 | 2026-08-05 | 2026-08-06 | 54 | 4 | 0 | 0 | 2 | 1 | 0 | 0 | CODE |  |
| prompts/adventure_passage.md | 704 | 2026-08-07 | 2026-08-06 | 52 | 4 | 0 | 0 | 2 | 0 | 0 | 2 | CODE+DIRREAD |  |
| prompts/local_usable_producer.md | 1921 | 2026-08-07 | 2026-08-06 | 52 | 4 | 0 | 0 | 3 | 0 | 0 | 2 | CODE+DIRREAD |  |
| proposals/ILAP-arena-steal-textarena.md | 7800 | 2026-08-06 | 2026-08-06 | 53 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| proposals/ILAP-beta1-definition.md | 6874 | 2026-08-06 | 2026-08-08 | 53 | 4 | 0 | 0 | 2 | 0 | 0 | 2 | CODE |  |
| proposals/ILAP-mesh-steal-001.md | 2115 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 2 | 2 | 0 | 2 | ESTATE+INT+CORPUS |  |
| proposals/ILAP-v3-entry.md | 3689 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 2 | 2 | 0 | 2 | ESTATE+INT+CORPUS |  |
| ractors/BAUDRILLARD.md | 2661 | 2026-09-14 | 2026-09-04 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | CODE+DIRREAD |  |
| ractors/BERNAYS.md | 2521 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 34 | CODE+DIRREAD | tools/saturation_fourcond.py:50 + tools/ocean_v2_pilot.py:42 BRIEF consts |
| ractors/ELLUL.md | 2772 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 18 | CODE+DIRREAD |  |
| ractors/FOUCAULT.md | 2607 | 2026-09-14 | 2026-09-04 | 14 | 2 | 0 | 0 | 4 | 0 | 0 | 8 | CODE+DIRREAD |  |
| ractors/FREUD.md | 2902 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 7 | CODE+DIRREAD |  |
| ractors/HALL.md | 2623 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 10 | CODE+DIRREAD |  |
| ractors/JUNG.md | 2755 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 7 | CODE+DIRREAD |  |
| ractors/MCLUHAN.md | 2322 | 2026-09-14 | 2026-09-04 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | CODE+DIRREAD |  |
| ractors/PLATO_KIRK.md | 2679 | 2026-09-14 | 2026-09-04 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 7 | CODE+DIRREAD |  |
| ractors/RACTORS.md | 4282 | 2026-09-14 | 2026-09-05 | 14 | 0 | 0 | 0 | 7 | 2 | 0 | 7 | CODE+DIRREAD |  |
| ractors/WALLAS.md | 3166 | 2026-09-14 | 2026-09-05 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | CODE+DIRREAD |  |
| releases/MAG_VERSION_SUBPROCESS_MAP.md | 9006 | 2026-08-05 | 2026-08-06 | 54 | 2 | 0 | 0 | 3 | 0 | 0 | 3 | CODE |  |
| releases/RELEASE_NOTES_TEMPLATE.md | 1939 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 2 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| releases/RELEASE_NOTES_v1.md | 3411 | 2026-08-05 | 2026-08-06 | 54 | 2 | 0 | 0 | 3 | 0 | 0 | 5 | CODE |  |
| releases/RELEASE_NOTES_v2.md | 3465 | 2026-08-05 | 2026-08-06 | 54 | 2 | 0 | 0 | 2 | 0 | 0 | 5 | CODE |  |
| releases/RELEASE_NOTES_v3.md | 3062 | 2026-08-06 | 2026-08-06 | 53 | 2 | 0 | 0 | 2 | 1 | 0 | 5 | CODE |  |
| releases/RELEASE_NOTES_v4.md | 1587 | 2026-08-06 | 2026-08-06 | 53 | 2 | 0 | 0 | 2 | 0 | 0 | 3 | CODE |  |
| releases/VERSION_REGISTRY.md | 6695 | 2026-09-27 | 2026-09-26 | 1 | 7 | 3 | 0 | 26 | 4 | 0 | 14 | BOOT+CODE |  |
| releases/WITNESS_SPINE.md | 2160 | 2026-08-05 | 2026-08-06 | 54 | 2 | 0 | 0 | 2 | 0 | 1 | 6 | CODE |  |
| skills/tabletop-dnd.md | 1974 | 2026-08-14 | 2026-08-10 | 45 | 2 | 0 | 0 | 3 | 0 | 0 | 2 | CODE |  |
| spores/mesh/bitchat-dual-transport-20260805.md | 4310 | 2026-08-05 | 2026-08-06 | 54 | 1 | 0 | 0 | 2 | 0 | 0 | 3 | CODE+DIRREAD |  |
| spores/mesh/briar-sync-no-server-20260805.md | 1748 | 2026-08-05 | 2026-08-06 | 54 | 1 | 0 | 0 | 2 | 0 | 0 | 3 | CODE+DIRREAD |  |
| spores/mesh/bridgefy-transmission-modes-20260805.md | 2842 | 2026-08-05 | 2026-08-06 | 54 | 1 | 0 | 0 | 2 | 0 | 0 | 3 | CODE+DIRREAD |  |
| spores/mesh/README.md | 872 | 2026-08-05 | 2026-08-06 | 54 | 0 | 0 | 0 | 3 | 1 | 0 | 0 | CODE+DIRREAD |  |
| steals/curveball_kol_stickmin.md | 531 | 2026-08-07 | 2026-08-06 | 52 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| templates/ILAP-PROPOSAL.md | 3838 | 2026-08-05 | 2026-08-06 | 54 | 2 | 1 | 0 | 3 | 2 | 0 | 2 | BOOT+CODE |  |
| tesuji/diary-verkle-train-2026-08-07.md | 1962 | 2026-08-07 | 2026-08-06 | 52 | 6 | 0 | 0 | 4 | 0 | 0 | 2 | CODE |  |
| tesuji/grok46-tui-organs-2026-08-28.md | 1242 | 2026-09-14 | 2026-08-28 | 14 | 0 | 0 | 0 | 5 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| tesuji/intention-fidelity-routing-2026-08-07.md | 3310 | 2026-08-07 | 2026-08-06 | 52 | 6 | 0 | 0 | 4 | 1 | 0 | 3 | CODE |  |
| tesuji/tonight-primer-feed-drummers-2026-08-30.md | 3073 | 2026-09-14 | 2026-08-29 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 2 | ESTATE+CORPUS |  |
| tesuji/voice-vad-end-of-turn-2026-08-07.md | 5264 | 2026-08-07 | 2026-08-06 | 52 | 0 | 0 | 0 | 2 | 1 | 0 | 2 | ESTATE+INT+CORPUS |  |
| tesuji/water-computer-day-for-night-2026-08-28.md | 1587 | 2026-09-14 | 2026-08-28 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| tesuji/zeitgeist-amish-plain-2026-08-05.md | 7668 | 2026-08-06 | 2026-08-06 | 53 | 0 | 0 | 0 | 2 | 0 | 0 | 3 | ESTATE+CORPUS |  |
| verb_genomes/L0_contract.md | 1208 | 2026-09-14 | 2026-09-02 | 14 | 3 | 0 | 1 | 10 | 0 | 0 | 16 | CODE+SKILL |  |
| verb_genomes/README.md | 845 | 2026-09-14 | 2026-09-02 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | ESTATE+CORPUS |  |
| verb_genomes/research_socratic.md | 2559 | 2026-09-14 | 2026-09-03 | 14 | 6 | 0 | 2 | 19 | 1 | 0 | 2 | CODE+SKILL |  |
| verb_genomes/self_steal.md | 2343 | 2026-09-14 | 2026-09-02 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 10 | ESTATE+CORPUS |  |
| verb_genomes/steal.md | 2778 | 2026-09-14 | 2026-09-02 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 56 | ESTATE+CORPUS |  |
| verb_genomes/_demo_target_vcache.txt | 1367 | 2026-09-14 | 2026-09-02 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE |  |
| weaves/W8-ponytail-ladder.md | 1200 | 2026-08-05 | 2026-08-06 | 54 | 4 | 0 | 0 | 2 | 1 | 0 | 2 | CODE |  |
| weaves/W9-caveman-prose.md | 1235 | 2026-08-05 | 2026-08-06 | 54 | 4 | 0 | 0 | 2 | 1 | 0 | 2 | CODE |  |
| zai_docs_mirror/INDEX.md | 21516 | 2026-09-14 | 2026-09-03 | 14 | 6 | 0 | 0 | 5 | 0 | 0 | 0 | CODE |  |
| zai_docs_mirror/openapi.json | 146793 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 20 | ESTATE |  |
| zai_docs_mirror/api-reference/api-code.md | 11753 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/api-reference/introduction.md | 8452 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | ESTATE+CORPUS |  |
| zai_docs_mirror/api-reference/rate-limit.md | 799 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 17 | ESTATE+CORPUS |  |
| zai_docs_mirror/api-reference/agents/agent-conversation.md | 5279 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/api-reference/agents/agent.md | 26208 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 46 | ESTATE+CORPUS |  |
| zai_docs_mirror/api-reference/agents/file-upload.md | 3871 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/api-reference/agents/get-async-result.md | 4496 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/api-reference/audio/audio-transcriptions.md | 6362 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/api-reference/image/generate-image-async.md | 5104 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/api-reference/image/generate-image.md | 6414 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 7 | ESTATE+CORPUS |  |
| zai_docs_mirror/api-reference/image/get-image-status.md | 4452 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/api-reference/llm/chat-completion.md | 44133 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/api-reference/tools/layout-parsing.md | 8240 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/api-reference/tools/tokenizer.md | 13451 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/api-reference/tools/web-reader.md | 5911 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/api-reference/tools/web-search.md | 6300 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | ESTATE+CORPUS |  |
| zai_docs_mirror/api-reference/video/generate-video.md | 9243 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/api-reference/video/get-video-status.md | 4452 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/credit-campaign-rules.md | 10273 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 7 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/faq.md | 8845 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/latest-model.md | 6257 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 7 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/overview.md | 8565 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/quick-start.md | 5670 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/teamplan.md | 10883 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 7 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/transition.md | 5999 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 11 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/usage-policy.md | 3785 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 18 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/extension/coding-tool-helper.md | 6708 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/mcp/reader-mcp-server.md | 8098 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/mcp/search-mcp-server.md | 7107 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/mcp/vision-mcp-server.md | 9835 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 7 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/mcp/zread-mcp-server.md | 8104 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 7 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/notice/event-glm-5.3-flash.md | 1530 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/notice/usage-revision.md | 10368 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 11 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/resources/best-practice.md | 19849 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 7 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/resources/memory-mechanism.md | 20083 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/devpack/tool/others.md | 5981 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/agents/slide.md | 4543 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 7 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/agents/translation.md | 13219 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 11 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/agents/video-template.md | 7339 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/audio/glm-asr-2512.md | 5283 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/capabilities/cache.md | 17788 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 25 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/capabilities/function-calling.md | 18911 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/capabilities/stream-tool.md | 5370 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/capabilities/streaming.md | 4781 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 7 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/capabilities/struct-output.md | 33913 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/capabilities/thinking-mode.md | 6890 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/capabilities/thinking.md | 11848 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/develop/http/introduction.md | 10110 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/develop/java/introduction.md | 14873 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/develop/langchain/introduction.md | 8376 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/develop/openai/python.md | 11410 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 9 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/develop/python/introduction.md | 14652 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/image/cogview-4.md | 10521 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 5 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/image/glm-image.md | 15806 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 5 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/llm/glm-4-32b-0414-128k.md | 11697 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 4 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/llm/glm-4.5.md | 27634 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 5 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/llm/glm-4.6.md | 15540 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 4 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/llm/glm-4.7.md | 25488 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 5 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/llm/glm-5.1.md | 19347 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 4 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/llm/glm-5.2.md | 25293 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 7 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/llm/glm-5.3.md | 23446 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 9 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/llm/glm-5.md | 19040 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 4 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/overview/concept-param.md | 10575 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/overview/migrate-to-glm-new.md | 7641 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 7 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/overview/overview.md | 13160 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/overview/pricing.md | 3704 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 21 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/overview/quick-start.md | 11309 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/tools/stream-tool.md | 5444 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/tools/web-search.md | 50693 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/video/cogvideox-3.md | 12440 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 5 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/vlm/autoglm-phone-multilingual.md | 7190 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 9 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/vlm/glm-4.5v.md | 15693 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 4 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/vlm/glm-4.6v.md | 41342 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 5 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/vlm/glm-5.3-flash.md | 23575 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/guides/vlm/glm-ocr.md | 9382 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 8 | ESTATE+CORPUS |  |
| zai_docs_mirror/help/faq.md | 1737 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | ESTATE+CORPUS |  |
| zai_docs_mirror/legal-agreement/privacy-policy.md | 29172 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 7 | ESTATE+CORPUS |  |
| zai_docs_mirror/legal-agreement/subscription-terms.md | 8875 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 7 | ESTATE+CORPUS |  |
| zai_docs_mirror/legal-agreement/terms-of-use.md | 53492 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 7 | ESTATE+CORPUS |  |
| zai_docs_mirror/release-notes/new-released.md | 9513 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 7 | ESTATE+CORPUS |  |
| zai_docs_mirror/scenario-example/develop-tools/claude.md | 9355 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 39 | ESTATE+CORPUS |  |
| zai_docs_mirror/scenario-example/develop-tools/cline.md | 3173 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 7 | ESTATE+CORPUS |  |
| zai_docs_mirror/scenario-example/develop-tools/cursor.md | 1864 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 13 | ESTATE+CORPUS |  |
| zai_docs_mirror/scenario-example/develop-tools/droid.md | 4398 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 5 | ESTATE+CORPUS |  |
| zai_docs_mirror/scenario-example/develop-tools/goose.md | 3135 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 5 | ESTATE+CORPUS |  |
| zai_docs_mirror/scenario-example/develop-tools/opencode.md | 5660 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 6 | ESTATE+CORPUS |  |
| zai_docs_mirror/_raw/build_index.py | 5034 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 3 | ESTATE |  |
| zai_docs_mirror/_raw/crawl_urls.txt | 3772 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 12 | ESTATE |  |
| zai_docs_mirror/_raw/fetch_log.txt | 3651 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 17 | ESTATE |  |
| zai_docs_mirror/_raw/fetch_log_fixed | 39 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE |  |
| zai_docs_mirror/_raw/home.html | 92878 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 45 | ESTATE |  |
| zai_docs_mirror/_raw/INDEX.md | 2258 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | ESTATE+CORPUS |  |
| zai_docs_mirror/_raw/index_paths.txt | 1960 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE |  |
| zai_docs_mirror/_raw/index_urls.txt | 2164 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE |  |
| zai_docs_mirror/_raw/link_closure.py | 1841 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 9 | ESTATE |  |
| zai_docs_mirror/_raw/link_closure.txt | 10602 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 3 | ESTATE |  |
| zai_docs_mirror/_raw/link_targets.txt | 0 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE |  |
| zai_docs_mirror/_raw/llms_full.txt | 647819 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 6 | 0 | 0 | 14 | ESTATE |  |
| zai_docs_mirror/_raw/llms_index.txt | 8777 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 13 | ESTATE |  |
| zai_docs_mirror/_raw/sitemap.xml | 8908 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 26 | ESTATE |  |
| zai_docs_mirror/_raw/sitemap_paths.txt | 1935 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE |  |
| zai_docs_mirror/_raw/sitemap_urls.txt | 3141 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 5 | ESTATE |  |
| zai_docs_mirror/_raw/unfetched.txt | 0 | 2026-09-14 | 2026-09-03 | 14 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | ESTATE |  |

## Caveats

- Reference detection matches path forms (case-insensitive) and bare unique basenames; stem-only mentions (`SPORES` without `.md`) are not counted.
- Estate references (watch/ receipts, memory/, corpus/) are historical citations, counted as references but not load-bearing evidence.
- References from outside the repo boundary (user-level .zcode skills, other projects) are not scanned; the in-repo .agents/skills copies are.
- Staleness uses git last-commit date, not disk mtime; both are recorded per row. The 6 .mimosa files are untracked (gitignored), so their git date is NEVER and staleness is reported as untracked; their disk mtimes are 2026-08-27 era.
- No file under docs/ref was modified by this census; state/CURRENT.md and the verkle chain tip were not touched.

