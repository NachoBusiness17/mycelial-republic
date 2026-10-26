# inbox genre census - every markdown file in watch/inbox/ (s2-22)

Item: s2-22 (flash50, burn_reset_20260927) - banked 2026-09-28 by seat f2-s2-22.
Twin files (byte-identical): `watch/inbox/burn_reset_20260927/flash50/inbox-genre-census.md`
and `watch/inbox/burn_reset_20260927/flash50/s2-22.md`.

## Census of record and drift

The inbox is a live shared surface; sibling lanes landed files while this census ran.
Every number below is from the snapshot of record unless a moment is named:

- opening walk (first command of the ask, ~19:35 EDT): 2,270 md / 12,322 total files / 190 dirs / 6,385,219,826 bytes
- draft instrument 19:43:12: 2,277 md; rerun 19:47:44: 2,279 md
- **snapshot of record 2026-09-28T20:23:59-04:00: 2,385 md / 24,228,864 md bytes / 2,198 git-tracked**
- drift over the run: +115 md in ~49 min (about 2.3 md/min), mostly burn_reset_20260927 sibling seats

The ask said "watch/inbox/ (6000+ files)". Verified split: the 6000+ holds for ALL
inbox files (12,322 at the opening walk); markdown specifically is 2,385 at the snapshot.

## Instruments

- `flash50/_s2_22_census.py`: walk + git facts (ls-files tracked set, log --diff-filter=A birth dates) + classification (its first reference pass, `git grep -oI -F -f stems`, was superseded - see Method 5b)
- `flash50/_s2_22_memrefs.py` (v2, the reference instrument of record): both reference passes in LINE MODE with exact python substring attribution - canonical `git grep -n -I -F -f stems` over the T1 roots (9,731 matching lines) and ripgrep line-mode over memory/+watch/ - plus the INDEX.json registry cross-tab
- raw per-file rows: `flash50/_s2_22_raw.json` (2,385 rows: rel, size, mtime, fdate, git_add, tracked, class, ext_refs, ref_by, mem_refs, reg_ref)

## Genre classes (snapshot of record)

Classification is rule-based (rules quoted in Method); the ask's five genres plus an
explicit `other` residue. Number first, rule after.

| class | files | share | bytes | defined as |
|---|---|---|---|---|
| receipt | 1586 | 66.5% | 13,984,250 | numbered burn id (B2-/FW-/W#-/Q-NN/THE50) or RECEIPT/BURN/CLOSE/verdict/checkpoint/salon markers or `## Verdict` or bank:/status: banked |
| finding | 600 | 25.2% | 8,209,703 | research deliverable signatures (CENSUS, ANALYSIS, DECODE, FOLD, THEORY, LENS, STEAL, PLAYBOOK, DIGEST, THREAD, UNPACK, SOURCE, STUDY, MAP, RESEARCH, SURVEY, NOTES, REVIEW, PROBE, DEEP-) |
| brief | 109 | 4.6% | 1,385,161 | BRIEF/HANDOFF/ONBOARD/PROMPT/DISPATCH/ASK_/NEXT-WINDOW/ORDER_/MEMO in stem, or banked queue ask under burn_reset queue/ |
| law | 45 | 1.9% | 302,758 | word-boundary LAW/LAWS/RIB/CLIPPY/CONSTITUTION/MAXIM in stem, or `# law`-style heading, or law-candidate |
| shitpost | 18 | 0.8% | 101,117 | explicit markers: SHITPOST/WHIM stem, shitpost/roast/dream/vision-verbatim in first heading, or the operator journal group |
| other | 27 | 1.1% | 245,875 | none of the above after a stage-2 heading pass |

## When written (three clocks)

| clock | coverage | min | max | note |
|---|---|---|---|---|
| filename date | 1504 of 2385 (63.1%) | 2026-07-20 | 2026-09-29 | regex 2026MMDD / 2026-MM-DD in stem |
| git first-add | 2198 tracked md (92.2%) | 2026-09-14 | 2026-09-28 | log --diff-filter=A per path |
| mtime | all | 2026-08-31 06:31 | 2026-09-28 20:23 | mutable; max is the live write edge |

By filename month (undated = no date in stem):

| month | files |
|---|---|
| 2026-07 | 22 |
| 2026-08 | 12 |
| 2026-09 | 1470 |
| (undated) | 881 |

Two clocks disagree on the past: 29 files carry July/August filename dates but the
inbox only entered git history on 2026-09-14 (git first-add min), and mtimes reach back
only to 2026-08-31 06:31. For those the filename date is the only birth claim; it is
self-declared, not byte-proven.

Newest-dated oddity: two files stamped 2026-09-29 are pytest basetemp fixtures a sibling
lane (s2-19) captured inside flash50 at `_s219_basetemp/test_commit_chain_and_load0/agent_state/versions/`
(UTC stamps reading as tomorrow in local time). flash50 is hosting another lane's test temp tree.

## Referenced by anything (three instruments, two tiers)

| instrument | scope | files with >=1 ref | share |
|---|---|---|---|
| T1 canonical roots git grep | docs, queue, state, configs, mag, tools, scripts, githooks, tests, corpus/steal, roblox/docs, .agents, memory/{rib,briefs,improve,workflows,boot}, memory/attention.md, memory/live_from_grok.md, 5 top-level md (tracked files only) | 422 | 17.7% |
| T1 INDEX.json registry | stem named in the derived registry (read 2026-09-28T20:31 EDT after this pass re-read it live: 1,678 items from index_events.jsonl) | 1121 | 47.0% |
| T2 memory+watch rg pass | ripgrep line-mode -n -F -f stems over memory/ + watch/ minus watch/inbox minus archival memory/corpus (gitignore-respecting, binaries skipped); 230,306 match lines, python substring attribution | 2376 | 99.6% |
| T1 union (canonical bar) | canonical roots OR registry | 1319 | 55.3% |
| T2 log-mention only | mem_refs > 0 but NOT canonically referenced | 1062 | 44.5% |
| zero anywhere | none of the three | 4 | 0.2% |

The 4 true orphans (zero on all three instruments), named:

- burn_reset_20260927/flash50/_sw03_out_sw-econ-3_stealth_space-bunny-alpha.md (# SW03 sw-econ-3)
- fifty_wide_20260917/FW37-42_INDEX.md (# FW-37..42 (board §H, game estate) - DONE 2026-09-28, receipts live under burn_reset queu)
- outbound/adventurelearn_packet/WHY.md (# WHY - three laws, their pedigree, and the anti-cult clause)
- seed_rib_20260926/seed-rib/CHANGELOG.md (# Changelog)

The promotion bar is T1: a session log in memory/ citing a receipt is a mention, not an
anchoring in the permanent record. T2 is reported because the ask says "referenced by
anything" - and on that literal bar only 4 md files in the inbox are true orphans.

Top referencing files (canonical pass, by number of distinct inbox md stems they name):

| referencing file | inbox md stems named |
|---|---|
| queue/queue_index.jsonl | 44 |
| docs/ref/BIBLIOGRAPHY_MAP.md | 27 |
| scripts/build_knowledge_graph.py | 20 |
| tools/seed_v2.py | 18 |
| scripts/build_deck.py | 18 |
| AGENTS.md | 13 |
| mag/improve.py | 12 |
| mag/agent_cli.py | 10 |
| scripts/the50_t21_q_caption_ledger_verify.py | 10 |
| queue/lanes/research/trail.jsonl | 9 |
| configs/violation_baseline.json | 9 |
| corpus/steal/MASTER_MICKEY17_V2.md | 8 |
| docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md | 8 |
| scripts/index_fold_host.mjs | 8 |
| tools/task_wall.py | 8 |

## Cross-tab against the registry's own taxonomy

INDEX.json items carry a `class` field of their own (event-log intake taxonomy, 53 distinct
values at read time; top: receipt 745, BACKFILL 569, RECEIPT 161, data 26, artifact 21, FACT 15). For the 1266 of 2385 inbox md that match a registry item by
basename, exact-label agreement is 319 (25.2%) - the two taxonomies are different
instruments, not errata: the registry labels intake events (BACKFILL = folded from the
log), this census labels genre. Registry classes for my 45 law files: BACKFILL 13, RECEIPT 4, receipt 3, LAW 2, AMENDMENT 1, DOCTRINE 1, STEAL 1, PROPOSAL 1.
The registry records the landing event; the census records what the file is.

## Promotion verdicts

Verdict rule (applied per file, stated before the counts): canonically referenced (T1:
canonical roots or INDEX registry) -> KEEP. A T2-only log mention does not KEEP a file.
Canonically unreferenced: law -> PROMOTE (a law outside the permanent record is the one
class where promotion is the failure mode); brief -> REVIEW if filename-dated within
14 days else ARCHIVE; finding -> REVIEW if within 14 days or a census/map/audit/decode/
inventory/gap signature, else ARCHIVE; receipt -> ARCHIVE (the work is in commits; the
receipt's value is already folded); shitpost -> ARCHIVE; other -> REVIEW (unjudged).

| verdict | files | share |
|---|---|---|
| KEEP | 1296 | 54.3% |
| PROMOTE | 20 | 0.8% |
| REVIEW | 90 | 3.8% |
| ARCHIVE | 979 | 41.0% |

### PROMOTE list (20): canonically unreferenced laws

Every one, named (rel | dated | h1):

- SEED_RIB_REFRESH_20260928.md | 2026-09-28 | # SEED_RIB_REFRESH_20260928
- audit_20260926/WAVE2_LANE3_RIB_COMPILER.md | 2026-09-26 | # WAVE2 LANE 3 - RIB COMPILER + SCHEDULED SURFACES
- burn_reset_20260927/flash50/_compiled_clippy.md | 2026-09-28 | ## 🖇️ Clippy - standing reminders (always-on, verkle-knotted)
- burn_reset_20260927/flash50/_compiled_clippy_release.md | 2026-09-28 | ## 🖇️ Clippy - standing reminders (always-on, verkle-knotted)
- burn_reset_20260927/flash50/_compiled_rib_k8s.md | 2026-09-28 | # RIB - Deep Dive: Emergent Tooling, Why It Makes K8s Valuable, and How to Tell Emergent from Deterministic
- burn_reset_20260927/flash50/_compiled_rib_release.md | 2026-09-28 | # RIB - Deep Dive: Emergent Tooling, Why It Makes K8s Valuable, and How to Tell Emergent from Deterministic
- burn_reset_20260927/flash50/rib-bus-census.md | 2026-09-28 | # s2-01: memory/rib_bus/ full census (domain-by-domain map)
- burn_reset_20260927/flash50/rib-census.md | 2026-09-28 | # RIB CENSUS - memory/rib/ (ITEM f-14, 2026-09-28)
- journal_mark_202609/MAXIM_20260915.md | 2026-09-15 | # Operator maxim - 2026-09-15, window close
- mickey/G3_6_law.md | 2026-09-10 | # MICKEY G3-6 - DISSECTION LAW FILED (2026-09-11)
- physical_computing/receipts/COMMIT4_20260916.md | 2026-09-16 | # COMMIT4_20260916 - checkpoint #4 receipt (wave-lane law: receipt first)
- seed_rib_20260926/seed-rib/ARTIFACT_LEDGER_LAW.md | 2026-09-27 | # THE EMBEDDED ARTIFACT LEDGER
- seed_rib_20260926/seed-rib/BUILD_DISCIPLINE_LAWS.md | 2026-09-27 | # BUILD DISCIPLINE LAWS
- seed_rib_20260926/seed-rib/SHARED_SURFACE_LAW.md | 2026-09-27 | # SHARED SURFACE LAW
- seed_rib_20260926/seed-rib/TRUST_BYTES_LAW.md | 2026-09-27 | # TRUST BYTES, NOT REPORTS
- seed_rib_20260926/seed-rib/kernel/env.law.md | 2026-09-27 | # env.law (kernel section 1, extracted from AGENTS.md "Python env", as-of 2026-09-27T04:39:02Z)
- seed_rib_20260926/seed-rib/kernel/filing.law.md | 2026-09-27 | # filing.law (kernel section 5, extracted 2026-09-27T04:39:02Z)
- seed_rib_20260926/seed-rib/kernel/tier.law.md | 2026-09-27 | # tier.law (kernel section 6, extracted 2026-09-27T04:39:02Z)
- wave_20260916/receipts/B11_SLIDING_WINDOW_RIB.md | 2026-09-16 | # B11 - SLIDING WINDOW vs LINEAR → RIB MAPPING (2026-09-16)
- wave_20260916/rs_witness_posts/RS4_referee_lawyer.md | 2026-09-16 | # WITNESS 4 - THE REFEREE LAWYER

### REVIEW shortlist (top 30 of 63 unreferenced recent/census findings+briefs, by bytes)

- burn_reset_20260927/flash50/silent-pass-census.md | 1859370 B | 2026-09-28 | # Silent exception handler census (f-29)
- burn_reset_20260927/flash50/mag-census.md | 486355 B | 2026-09-28 | # mag/ module census (item f-24, 2026-09-28)
- burn_reset_20260927/flash50/ledger-census.md | 112000 B | 2026-09-28 | # f-26: JSONL ledger census (every .jsonl in the repo, .venv/.git excluded)
- burn_reset_20260927/flash50/secrets-census.md | 97157 B | 2026-09-28 | # f-22: secrets-file census (2026-09-28)
- burn_reset_20260927/flash50/todo-census.md | 91838 B | 2026-09-28 | # f-10 - TODO/FIXME/HACK/XXX census of the Mag estate (2026-09-28)
- burn_reset_20260927/flash50/api-endpoint-map.md | 61566 B | 2026-09-28 | # API endpoint map: dashboard/rest.py + dashboard/server.py
- audit_20260926/LANE1_PRIOR_MAP_DELTA.md | 35263 B | 2026-09-26 | # LANE 1 - PRIOR-MAP DELTA
- burn_reset_20260927/flash50/free-lane-map.md | 29694 B | 2026-09-28 | # FREE-LANE MAP - every provider, model, rate limit, auth mechanism, cost
- wave_20260916/receipts/VC1_FULL_CENSUS.md | 22384 B | 2026-09-16 | # VC1 - FULL CENSUS / verkle crawl (VC seat)
- burn_reset_20260927/flash50/deep-epistemic-gap.md | 22259 B | 2026-09-28 | # EPISTEMIC GAP SENSOR  -  designing the estate's nervous system (deep-epistemic-gap, flash50, 2026-
- wave_20260916/receipts/R3_GAP_ANALYSIS_SOCRATIC.md | 20303 B | 2026-09-16 | # R3 - PROGRAM GAP ANALYSIS, SOCRATIC EXPANSION (2026-09-16)
- physical_computing/receipts/K13_K8S_TUB_MAPPING.md | 19447 B | 2026-09-16 | # RECEIPT - K13: Kubernetes mapping spec for the tub fleet (K13_K8S_TUB_MAPPING)
- burn_reset_20260927/flash50/skill-census.md | 18940 B | 2026-09-28 | # f-21 - SKILL CENSUS: .agents/skills/*/SKILL.md (2026-09-28)
- burn_reset_20260927/flash50/deep-the-map-is-territory.md | 18780 B | 2026-09-28 | # deep-the-map-is-territory: the estate where the map is the territory
- burn_reset_20260927/flash50/luau-census.md | 18049 B | 2026-09-28 | # Luau census: roblox/src/ (item s2-03, 2026-09-28)
- burn_reset_20260927/flash50/large-file-census.md | 18027 B | 2026-09-28 | # s2-07: Large-File Census (10 largest files outside .git/.venv/node_modules/corpus)
- deepseek_research/deepseek_analysis_6tweets_20260923.md | 17311 B | 2026-09-23 | ## 1. LLM Inference Serving: Six Systems-Level Techniques
- burn_reset_20260927/flash50/ps1-census.md | 17167 B | 2026-09-28 | # ps1-census: every PowerShell script in scripts/ (item f-28, 2026-09-28)
- burn_reset_20260927/flash50/inbox-recent-census.md | 16799 B | 2026-09-28 | # Inbox recent census: the 20 most recent files in watch/inbox/ (item s2-09, 2026-09-28)
- burn_reset_20260927/flash50/configs-census.md | 15910 B | 2026-09-28 | # configs/ JSON census (item s2-10)
- burn_reset_20260927/flash50/context-pipeline-map.md | 15842 B | 2026-09-28 | # s2-08: context_pack pipeline map (census, 2026-09-28)
- inbound/AOS_CFMBT_V5_SPEC_20260922.md | 15695 B | 2026-09-22 | # CFMBT v5 - Conflict-First Municipal Bond Transparency
- burn_reset_20260927/flash50/steering-pipeline-map.md | 15139 B | 2026-09-28 | # steering-pipeline-map (s2-15, 2026-09-28)
- burn_reset_20260927/flash50/decorator-census.md | 15107 B | 2026-09-28 | # s2-24: decorator census - mag/ + tools/
- audit_20260926/WAVE2_LANE1_DISK_MAP.md | 14832 B | 2026-09-26 | # WAVE2 LANE1 - DISK MAP: where the 48 GB actually sits
- burn_reset_20260927/flash50/root-module-census.md | 13947 B | 2026-09-28 | # f-17 - root module census (repo root *.py), 2026-09-28
- burn_reset_20260927/flash50/branch-census.md | 12801 B | 2026-09-28 | # f-20 - git branch census (burn_reset_20260927 flash50)
- burn_reset_20260927/flash50/promise-gap.md | 11849 B | 2026-09-28 | # f-13: promise-vs-reality gap analysis - FRAMEWORK_LOAD.md + MAG_MYCELIAL_REPUBLIC_COMPASS.md
- wave_20260916/receipts/CV1_COLD_MAP.md | 11667 B | 2026-09-16 | # CV1 COLD MAP - wave 2026-09-16
- burn_reset_20260927/flash50/hook-census.md | 11660 B | 2026-09-28 | # s2-12 HOOK CENSUS - githooks/ (2026-09-28)

### OTHER residue (all 27, named)

- BATTLE_BOTS_SQUID_MAZE_20260914.md | # Battle Bots in the Squid Maze - concept note (2026-09-14)
- CONSTRAINT_ENGINEERING_TOLDYOUSO_20260913.md | # TOLD YOU SO - constraint engineering IS the house (2026-09-13, operator: "tell me what you think I
- EQUIVALENCE_SHADER_ENV_20260912.md | # EQUIVALENCE + THE SHADER ENVIRONMENT (2026-09-12, intake + build)
- FAILOPEN_AUTHORITY_GATE_20260911.md | # FAILOPEN AUTHORITY GATE - relayed finding, owner action requested (2026-09-11)
- FANOUT_STANDING_ORGAN_20260912.md | # FANOUT - the standing N-wide organ (2026-09-12, operator correction: "SELF STEAL" + "duplication i
- FRONTIER_GAME_REPOS_20260924.md | # FRONTIER GAME REPOS - pattern-steal census (2026-09-24)
- FULL_SCAN_REPORT_20260923.md | # FULL SCAN - semantic catalog churn
- HARVEST_MOON_RACTOR_PANEL_20260927.md | # Harvest Moon Ractor Panel - September 27, 2026
- HOLLOW_MASS_BODIES_20260911.md | # HOLLOW MASS BODIES - did the null-theme knots hide real work? 2026-09-11
- LANE19_SEAL_HOOK_TEST_20260922.md | # LANE 19 SEAL-HOOK TEST (2026-09-22)
- LIFE_OF_SAINT_ANTONY_20260915.md | # The Life of Saint Antony - link-drop mine · 2026-09-15
- ORCHESTRATOR_SEEDS_20260911.md | # ORCHESTRATOR_SEEDS_20260911
- PERSISTENT_WORLD_V0_LIVE_20260914.md | # THE PERSISTENT WORLD - v0 LIVE (2026-09-14, ~00:2xZ, operator: "do it")
- RASHOMON_SURFACE_ELEPHANT_20260914.md | # THE ELEPHANT, RASHOMON SURFACE - 2026-09-14
- RESOLUTION_J1_CAGE_TO_MAG_ROUTE_20260901.md | # J1 RESOLVED - Cage→Mag API route for chans commits + mermaid render
- SPOT_PATROL_LANDED_20260927.md | # LEDGER SPOT-CHECK PATROL LANDED - 2026-09-27
- THE_OLD_BOOKS_SHELF_DIG2_20260923.md | # THE OLD BOOKS SHELF - dig 2 (append to THE_OLD_BOOKS_SHELF_20260923.md)
- WINSTT_ASSESS_20260911.md | # WINSTT ASSESSMENT - the operator's voice organ (2026-09-11)
- _seal_test.md | (no heading)
- bad_apple/PROVENANCE.md | # B5 SOURCE PROVENANCE - Bad Apple!! frames (2026-09-06)
- fleet_research_lens/fleet-research-lens/evidence-excerpts.md | # Selected source excerpts
- hive_operating_floor/CLAIMS.template.md | (no heading)
- hive_operating_floor/LAYERS.template.md | # Claims template (blank)
- hive_operating_floor/OPSEC.md | # DEMO - globe analog
- hive_operating_floor/README-SHARE.md | # OPSEC - globe share template
- seed_rib_20260926/seed-rib/AGENTS.md | (no heading)
- seed_rib_20260926/seed-rib/VSCODE.md | # VSCODE - "download VS Code and use this with the free models"

### SHITPOST/whim class (all 18, named)

- ATLAS_TANK_20260913.md | # THE GUPPY EXODUS - Atlas in the kitchen (2026-09-13, operator's vision, verbatim)
- ELITESAVIOR_RACTOR_SHITPOST_RESPONSE_20260920.md | # ELITESAVIOR RESPONSE - through the ractors + the shit post desk (2026-09-20)
- SHITPOST_DESK_ANTHROPIC_PRIMER_20260922.md | # SHITPOST DESK - "The Primer" roast pack (Anthropic) · 2026-09-22
- SHITPOST_DESK_MASSIE_20260923.md | # SHITPOST DESK - Thomas Massie, "Thrown From the Tent" · 2026-09-23
- SHITPOST_DESK_MASSIE_V2_VOLTAIRE_20260923.md | # SHITPOST DESK - Massie roast v2, Voltaire voice · 2026-09-23
- SHITPOST_DESK_MASSIE_V3_MEAN_20260923.md | # SHITPOST DESK - Massie roast v3, MEANER · 2026-09-23
- SHITPOST_DESK_NVIDIA_REPLY_20260928.md | # SHITPOST DESK: REPLY TO NVIDIA - 2026-09-28 (ractor, candidates dying)
- SHITPOST_DESK_RACTOR_CYCLE0_STAGED_20260924.md | # SHITPOST DESK - RACTOR ROTATION CYCLE 0, STAGED · 2026-09-24
- SHITPOST_DESK_SANDERS_BAN_20260923.md | # SHITPOST DESK - SANDERS "BAN ARTIFICIAL SUPERINTELLIGENCE ACT" - 2026-09-23
- SHITPOST_DESK_SELF_STEAL_20260924.md | # SHITPOST DESK - SELF STEAL EDITION · 2026-09-24
- VP_SHITPOST_DESK_20260916.md | # Shitpost Desk - @VP border thread - 2026-09-16
- burn_reset_20260927/flash50/deep-dream-cycle.md | # DEEP-DREAM-CYCLE: The Estate's Dream Cycle (designed from its own organs)
- journal_mark_202609/DREAM_MYCELIUM_20260916.md | # Mark's dream - 2026-09-16 - the dozen cubes (mycelial compute lenses)
- journal_mark_202609/JOURNAL_20260914.md | # Journal entry - 2026-09-14 - Mark
- journal_mark_202609/JOURNAL_20260915.md | # Journal entry - 2026-09-15 - Mark
- journal_mark_202609/JOURNAL_20260916_ANSWERS.md | # Mark's journal - 2026-09-16 - answers to the five prompts
- journal_mark_202609/PARABLE_OF_THE_AUDITOR_draft.md | # THE PARABLE OF THE AUDITOR - draft for Mark · 2026-09-16
- wave_20260916/receipts/SP_OPENAI_MISALIGNMENT.md | # SP_OPENAI_MISALIGNMENT - shitpost desk receipt (2026-09-16, night)

### Law class detail (all 45)

25 of 45 law files are canonically referenced (KEEP); the 20 unreferenced ones are the
PROMOTE list above.

| law file | dated | refs | verdict |
|---|---|---|---|
| ARC_LAWS_20260918.md | 2026-09-18 | e0/m8/r1 | KEEP |
| ASTRA_CONSTITUTIONAL_AMENDMENTS.md | 2026-09-17 | e0/m5/r1 | KEEP |
| ENVELOPE_LAW_20260926.md | 2026-09-26 | e0/m4/r1 | KEEP |
| EVENTS_DRIFT_LAW_20260926.md | 2026-09-26 | e0/m5/r1 | KEEP |
| FLEET_MIX_LAW_20260922.md | 2026-09-22 | e0/m4/r1 | KEEP |
| KEY_LAW_20260923.md | 2026-09-23 | e0/m4/r1 | KEEP |
| LAW066_DELTA_LEDGER_WITNESS3_20260907.md | 2026-09-07 | e0/m6/r1 | KEEP |
| LAW13_EXPERIMENT_ON_ABSENCE_20260926.md | 2026-09-26 | e0/m8/r1 | KEEP |
| LAW_064_065_INSTRUMENTS_20260907.md | 2026-09-07 | e0/m5/r1 | KEEP |
| LAW_CAND_066_VERDICT_CITATION_20260907.md | 2026-09-07 | e0/m6/r1 | KEEP |
| LIVING_HASH_LAW_20260926.md | 2026-09-26 | e6/m5/r1 | KEEP |
| MODEL_RIB_LIBRARY_DESIGN_2026-08-31.md | 2026-08-31 | e0/m6/r1 | KEEP |
| NIGHT_LAWS_AUDIT_20260911.md | 2026-09-11 | e0/m4/r1 | KEEP |
| PACK_RETENTION_LAW_20260926.md | 2026-09-26 | e0/m4/r1 | KEEP |
| RACTOR_PREWARMED_RIB_SPEC_20260920.md | 2026-09-20 | e0/m4/r1 | KEEP |
| RESTFUL_WATCH_059_20260906.md | 2026-09-06 | e0/m6/r1 | KEEP |
| RIBV_LENS_STACK_SALON_20260922.md | 2026-09-22 | e0/m5/r1 | KEEP |
| RIB_BUS_RESURRECTION_20260911.md | 2026-09-11 | e0/m3/r1 | KEEP |
| RIB_LANGUAGE_CACHE_OS_20260919.md | 2026-09-19 | e0/m5/r1 | KEEP |
| SALON_SUPERINTELLIGENCE_STACK_RIB_20260831.md | 2026-08-31 | e0/m8/r1 | KEEP |
| SEED_RIB_FORMAT_v0_20260926.md | 2026-09-26 | e2/m5/r1 | KEEP |
| SEED_RIB_HANDOFF_KERNEL_20260926.md | 2026-09-26 | e0/m5/r1 | KEEP |
| SEED_RIB_REFRESH_20260928.md | 2026-09-28 | e0/m2/r0 | PROMOTE |
| audit_20260926/WAVE2_LANE3_RIB_COMPILER.md | 2026-09-26 | e0/m2/r0 | PROMOTE |
| burn_reset_20260927/flash50/_compiled_clippy.md | 2026-09-28 | e0/m1/r0 | PROMOTE |
| burn_reset_20260927/flash50/_compiled_clippy_release.md | 2026-09-28 | e0/m1/r0 | PROMOTE |
| burn_reset_20260927/flash50/_compiled_rib_k8s.md | 2026-09-28 | e0/m1/r0 | PROMOTE |
| burn_reset_20260927/flash50/_compiled_rib_release.md | 2026-09-28 | e0/m1/r0 | PROMOTE |
| burn_reset_20260927/flash50/rib-bus-census.md | 2026-09-28 | e0/m1/r0 | PROMOTE |
| burn_reset_20260927/flash50/rib-census.md | 2026-09-28 | e0/m1/r0 | PROMOTE |
| journal_mark_202609/MAXIM_20260915.md | 2026-09-15 | e0/m4/r0 | PROMOTE |
| mickey/G3_6_law.md | 2026-09-10 | e0/m2/r0 | PROMOTE |
| physical_computing/receipts/COMMIT4_20260916.md | 2026-09-16 | e0/m1/r0 | PROMOTE |
| seed_rib_20260926/SEED_RIB_LANDED_RECEIPT.md | 2026-09-27 | e0/m2/r1 | KEEP |
| seed_rib_20260926/seed-rib/ARTIFACT_LEDGER_LAW.md | 2026-09-27 | e0/m2/r0 | PROMOTE |
| seed_rib_20260926/seed-rib/BUILD_DISCIPLINE_LAWS.md | 2026-09-27 | e0/m3/r0 | PROMOTE |
| seed_rib_20260926/seed-rib/SEED_RIB.md | 2026-09-27 | e3/m7/r1 | KEEP |
| seed_rib_20260926/seed-rib/SHARED_SURFACE_LAW.md | 2026-09-27 | e0/m2/r0 | PROMOTE |
| seed_rib_20260926/seed-rib/TRUST_BYTES_LAW.md | 2026-09-27 | e0/m7/r0 | PROMOTE |
| seed_rib_20260926/seed-rib/kernel/env.law.md | 2026-09-27 | e0/m2/r0 | PROMOTE |
| seed_rib_20260926/seed-rib/kernel/filing.law.md | 2026-09-27 | e0/m2/r0 | PROMOTE |
| seed_rib_20260926/seed-rib/kernel/tier.law.md | 2026-09-27 | e0/m2/r0 | PROMOTE |
| wave_20260916/receipts/B11_SLIDING_WINDOW_RIB.md | 2026-09-16 | e0/m2/r0 | PROMOTE |
| wave_20260916/receipts/PD3_FOUNDING_LAW.md | 2026-09-16 | e1/m1/r0 | KEEP |
| wave_20260916/rs_witness_posts/RS4_referee_lawyer.md | 2026-09-16 | e0/m1/r0 | PROMOTE |

## Verdict by class

| class | KEEP | PROMOTE | REVIEW | ARCHIVE | of which log-mention-only |
|---|---|---|---|---|---|
| receipt | 825 | 0 | 0 | 761 | 758 |
| finding | 348 | 0 | 63 | 189 | 251 |
| brief | 85 | 0 | 0 | 24 | 24 |
| law | 25 | 20 | 0 | 0 | 20 |
| shitpost | 13 | 0 | 0 | 5 | 5 |
| other | 0 | 0 | 27 | 0 | 4 |

## Method and limits

1. Classification is heuristic on stem + first 4 KB (heading line first). The exact rule
   chain, in order: numbered burn id (B2-/FW-/W#-/Q-NN/THE50 prefixes; verdict or receipt
   text in first 600 B -> receipt, queue-grouped without verdict -> brief/ask, else
   receipt) > word-boundary LAW/LAWS/RIB/CLIPPY/CONSTITUTION/MAXIM > brief signatures >
   explicit shitpost markers on the first heading > finding signatures > receipt markers
   > stage-2 heading pass > lane fallback (mickey/, burn_reset work/flash50, burn_wave/,
   wave_20260916/, physical_computing/ -> receipt) > other. Known noise, accepted and
   counted in `other` (27 files): concept notes and templates with no signature words.
2. Reference scan 1 (T1) is `git grep -n -I -F -f stems.txt` over TRACKED files in the
   pathspecs listed above; untracked reference surfaces are not scanned (except
   INDEX.json, read directly). Stem match is exact substring on the matched line: a stem
   inside a longer token counts (longer and shorter stems on the same line are both
   credited).
3. Generic-named files (readme/license/changelog/index/todo/notes stems, case-insensitive)
   are resolved by full `watch/inbox/<rel>` needle instead of bare stem, to avoid false
   positives from the word itself.
4. Registry cross-tab matches by basename; 0 duplicate-basename conflicts were found
   across the 1678 registry items.
5. The memory+watch rg pass is gitignore-respecting and substring-based; a T2-only file is
   mentioned in logs but anchored nowhere canonical. Zero-ref means zero in ALL THREE
   instruments, a lower bound on true orphanhood, not an equality.
5b. Instrument defect found and fixed during this census: ripgrep 15.2.0 `-o` with a
   2,379-pattern `-f` file silently drops matches (a stem found by single-pattern -e and
   by line-mode was never emitted by the multi-pattern -o run; first surfaced as 3
   spot-check zero-ref files that repo-wide grep DID find in catalog/ and memory/).
   All reference numbers above come from the re-run line-mode passes with exact python
   substring attribution (canonical git grep -n -F: 9,731 lines; rg line-mode: 230,306 lines);
   the earlier -o numbers (416/2,211/93) are superseded and were never banked.
6. INDEX.json was re-read live by the second instrument (%s items vs 1,415 at the first
   pass 20:27 EDT): the registry itself is derived live from index_events.jsonl; reg_ref
   flags in the raw rows are from the later read.
7. File contents were read only to 4 KB per file (head + heading extraction). No whole-file
   read pass was made; genre calls below the heading are unverified.
8. The 187 untracked md files have no git birth date; their clocks are filename date + mtime only.
9. Self-exclusion: the twin outputs (s2-22.md, inbox-genre-census.md) and the
   instrument files (_s2_22_*.py/json/txt) are excluded from the md rows by name at the census moment.
10. Quoted heading text in the named lists is dash-normalized (em/en to hyphen) so this
   banked file carries zero em/en dashes; the verbatim heading bytes live in the source
   files and in _s2_22_raw.json.

## Per-file appendix (2385 rows)

Format: `rel | class | dated(filename/git) | refs ext+mem / reg | bytes | verdict`.

A2A_FIRST_PROBE_20260925.md | finding | 2026-09-25 | 0+4/1 | 5945 | KEEP
ABSORPTION_PATTERN_20260924.md | finding | 2026-09-24 | 0+4/1 | 2334 | KEEP
ABULAFIA_VITAL_DERIVATION_20260928.md | receipt | 2026-09-28 | 0+3/0 | 966 | ARCHIVE
ACCOUNT_VS_AUDIT_20260923.md | receipt | 2026-09-23 | 4+4/1 | 8341 | KEEP
ADAM_ONBOARDING_FULL_20260924.md | brief | 2026-09-24 | 0+7/1 | 138218 | KEEP
AEOLIPILE_SPORE_20260922.md | receipt | 2026-09-22 | 0+4/1 | 3958 | KEEP
AGENTZIP_STEAL_20260912.md | finding | 2026-09-12 | 0+4/1 | 3079 | KEEP
AGENT_HIVE_BEE_FUNGUS_HANDOFF_2026-08-31.md | brief | 2026-08-31 | 1+7/1 | 31870 | KEEP
AGENT_MEMORY_COUNTERLAW_20260925.md | brief | 2026-09-25 | 0+4/1 | 6345 | KEEP
AGENT_MOCK_DOSSIER_20260906.md | receipt | 2026-09-06 | 0+6/1 | 24895 | KEEP
AGENT_SESSIONS_DECODE_20260911.md | finding | 2026-09-11 | 0+4/1 | 7996 | KEEP
AOS_CFMBT_BUILD_RECEIPT_20260922.md | receipt | 2026-09-22 | 0+4/1 | 4749 | KEEP
AOS_REPLY_OUR_LENS_20260922.md | finding | 2026-09-22 | 0+4/1 | 9774 | KEEP
APPEND_GATE_WIRED_20260927.md | receipt | 2026-09-27 | 0+3/1 | 2722 | KEEP
ARC_LAWS_20260918.md | law | 2026-09-18 | 0+8/1 | 3895 | KEEP
ARENA_V2_CONSTELLATION_SALON_20260913.md | receipt | 2026-09-13 | 0+5/1 | 3751 | KEEP
ARTIFACT_LENS_GOMOKU_FLY_20260912.md | finding | 2026-09-12 | 0+4/1 | 7174 | KEEP
ASTRA_ASK_2_NIGHT_AUDIT_20260916.md | brief | 2026-09-16 | 0+5/1 | 5804 | KEEP
ASTRA_ASK_FOLD_20260913.md | brief | 2026-09-13 | 0+5/1 | 3445 | KEEP
ASTRA_ASK_THE_LOOP_20260911.md | brief | 2026-09-11 | 0+5/1 | 15026 | KEEP
ASTRA_BLIND_SELFANSWERS_20260907.md | receipt | 2026-09-07 | 0+6/1 | 4799 | KEEP
ASTRA_CONSTITUTIONAL_AMENDMENTS.md | law | 2026-09-17 | 0+5/1 | 1758 | KEEP
ASTRA_FRONTIER_TIER_TRAINING_BRIEF.md | brief | 2026-09-17 | 0+5/1 | 2804 | KEEP
ASTRA_GAP_V2_20260906.md | finding | 2026-09-06 | 0+5/1 | 4401 | KEEP
ASTRA_GAP_V2_SOCRATIC_20260906.md | finding | 2026-09-06 | 0+6/1 | 4353 | KEEP
ASTRA_HANDOFF_JOURNAL_20260907.md | brief | 2026-09-07 | 0+6/1 | 8116 | KEEP
ASTRA_HERMES_SEAT_POSITIONS_FOLD_20260908.md | finding | 2026-09-08 | 0+4/1 | 7658 | KEEP
ASTRA_HOUR_BRIEF.md | brief | 2026-09-21 | 0+4/1 | 3345 | KEEP
ASTRA_PROMPT_OLLAMA_MAZE_20260907.md | brief | 2026-09-07 | 0+6/1 | 11232 | KEEP
ASTRA_PROMPT_STANDING_WAVE_20260907.md | brief | 2026-09-07 | 0+5/1 | 2370 | KEEP
ASTRA_PROMPT_WORLDLINE_WITNESS3_20260907.md | brief | 2026-09-07 | 0+5/1 | 10938 | KEEP
ASTRA_REAUDIT_V3_20260911.md | receipt | 2026-09-11 | 0+10/1 | 4391 | KEEP
ASTRA_REGISTRATION_REVIEW_20260909.md | finding | 2026-09-09 | 0+9/1 | 4543 | KEEP
ASTRA_REGISTRATION_REVIEW_20260909_2324.md | finding | 2026-09-09 | 0+6/1 | 4725 | KEEP
ASTRA_REPAIR_LANE_20260915.md | receipt | 2026-09-15 | 0+5/1 | 9164 | KEEP
ASTRA_REVIVE_VERDICT_20260926.md | receipt | 2026-09-26 | 0+4/1 | 3293 | KEEP
ASTRA_V2_FIXES_APPLIED_20260911.md | receipt | 2026-09-11 | 0+6/1 | 8479 | KEEP
ASTRA_V4_STATUS.md | receipt | 2026-09-17 | 0+5/1 | 2297 | KEEP
ASTRA_VS_CHEAP_FIRED_20260912.md | receipt | 2026-09-12 | 0+4/1 | 1441 | KEEP
ATHENA_CLASS_INTAKE_20260922.md | receipt | 2026-09-22 | 0+4/1 | 6055 | KEEP
ATLAS_SELF_STEAL_20260927.md | finding | 2026-09-27 | 2+7/1 | 6113 | KEEP
ATLAS_TANK_20260913.md | shitpost | 2026-09-13 | 0+4/1 | 3242 | KEEP
ATTIC_STRATA_20260911.md | finding | 2026-09-11 | 0+23/1 | 7240 | KEEP
AUDITOR_RECON_RLT_20260912.md | finding | 2026-09-12 | 0+6/1 | 3007 | KEEP
AUDIT_GOPHER_20260926.md | finding | 2026-09-26 | 0+7/1 | 6309 | KEEP
AUDIT_SEED_ADVENTURE_LEARN_20260926.md | receipt | 2026-09-26 | 0+5/1 | 6827 | KEEP
AUK_SPIKE_20260928.md | receipt | 2026-09-28 | 0+2/0 | 4973 | ARCHIVE
AUTORUN_AUTOPSY_20260919.md | receipt | 2026-09-19 | 0+4/1 | 1933 | KEEP
BASECAMP_NEXT_20260916.md | receipt | 2026-09-16 | 0+5/1 | 2601 | KEEP
BASECAMP_PROMPT_20260913.md | brief | 2026-09-13 | 0+4/1 | 6278 | KEEP
BATTLE_BOTS_SQUID_MAZE_20260914.md | other | 2026-09-14 | 0+5/1 | 4797 | REVIEW
BCHAIN2_DISSECTOR_20260907.md | finding | 2026-09-07 | 0+6/1 | 5773 | KEEP
BEACON_GWAP_72STEP_20260922.md | receipt | 2026-09-22 | 0+4/1 | 4018 | KEEP
BLIND_DIFFERENTIAL_METHOD_20260921.md | receipt | 2026-09-21 | 1+5/1 | 2267 | KEEP
BLIND_PROBE_STEAL_MAP_20260921.md | finding | 2026-09-21 | 0+4/1 | 2145 | KEEP
BLOB_DOUBLE_MECHANIC_SPEC.md | finding | 2026-09-18 | 0+4/1 | 2144 | KEEP
BOOT_AUDIT_APPLIED_20260911.md | receipt | 2026-09-11 | 0+8/1 | 8028 | KEEP
BOOT_LANE_INTERFERENCE_BURN_20260925.md | receipt | 2026-09-25 | 1+5/1 | 6750 | KEEP
BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md | receipt | 2026-09-26 | 0+7/1 | 5338 | KEEP
BOOT_LANE_MORNING_ADDITIONS_20260926.md | receipt | 2026-09-26 | 0+5/1 | 2081 | KEEP
BREAD_PANIC_X_FLEET_20260927.md | receipt | 2026-09-27 | 0+2/1 | 3685 | KEEP
BRING_IN_PLAN_20260918.md | receipt | 2026-09-18 | 0+5/1 | 4078 | KEEP
BROWSERLESS_GATE_20260922.md | receipt | 2026-09-22 | 0+4/1 | 3629 | KEEP
BUILD_ORDER_LIVING_MUD_20260922.md | brief | 2026-09-22 | 0+4/1 | 5413 | KEEP
BURN_C8_SCOPE_20260925.md | receipt | 2026-09-25 | 0+8/1 | 7503 | KEEP
BURN_CLOSE_20260927_EVENING.md | receipt | 2026-09-27 | 0+2/1 | 4194 | KEEP
BURN_JUDGE_LANE_BUILD_20260925.md | receipt | 2026-09-25 | 5+9/1 | 8666 | KEEP
BURN_PLAN_20260927.md | receipt | 2026-09-27 | 0+7/1 | 2139 | KEEP
BURN_PLAN_2B_20260912.md | receipt | 2026-09-12 | 0+5/1 | 5890 | KEEP
BURN_RESET_20260927_EVENING.md | receipt | 2026-09-27 | 0+2/1 | 1869 | KEEP
BURN_WAVE_PIN_20260926.md | receipt | 2026-09-26 | 0+8/1 | 3156 | KEEP
BURN_adversarial-self-probes_20260925.md | finding | 2026-09-25 | 0+5/1 | 3171 | KEEP
BURN_adversarial-self-probes_20260925_b.md | finding | 2026-09-25 | 0+5/1 | 3720 | KEEP
BURN_adversarial-self-probes_20260925_c.md | finding | 2026-09-25 | 0+5/1 | 3334 | KEEP
BURN_adversarial-self-probes_20260926.md | finding | 2026-09-26 | 2+5/1 | 3598 | KEEP
BURN_adversarial-self-probes_20260926_b.md | finding | 2026-09-26 | 0+5/1 | 3748 | KEEP
BURN_adversarial-self-probes_20260926_c.md | finding | 2026-09-26 | 0+5/1 | 3426 | KEEP
BURN_adversarial-self-probes_20260926_d.md | finding | 2026-09-26 | 2+5/1 | 4559 | KEEP
BURN_adversarial-self-probes_20260927.md | finding | 2026-09-27 | 1+4/1 | 3655 | KEEP
BURN_adversarial-self-probes_20260927_b.md | finding | 2026-09-27 | 0+3/1 | 3570 | KEEP
BURN_adversarial-self-probes_20260927_c.md | finding | 2026-09-27 | 1+3/1 | 3435 | KEEP
BURN_adversarial-self-probes_20260927_d.md | finding | 2026-09-27 | 0+4/0 | 3184 | REVIEW
BURN_adversarial-self-probes_20260927_e.md | finding | 2026-09-27 | 0+4/0 | 2850 | REVIEW
BURN_adversarial-self-probes_20260927_f.md | finding | 2026-09-27 | 1+3/0 | 3540 | KEEP
BURN_adversarial-self-probes_20260927_g.md | finding | 2026-09-27 | 1+3/0 | 3424 | KEEP
BURN_adversarial-self-probes_20260927_h.md | finding | 2026-09-27 | 0+4/0 | 3844 | REVIEW
BURN_b2-wave-fold_20260926.md | finding | 2026-09-26 | 1+5/1 | 3257 | KEEP
BURN_b2-wave-fold_20260926_b.md | finding | 2026-09-26 | 0+5/1 | 3783 | KEEP
BURN_b2-wave-fold_20260926_c.md | finding | 2026-09-26 | 1+5/1 | 2736 | KEEP
BURN_b2-wave-fold_20260926_d.md | finding | 2026-09-26 | 0+5/1 | 3168 | KEEP
BURN_b2-wave-fold_20260926_e.md | finding | 2026-09-26 | 0+5/1 | 3720 | KEEP
BURN_b2-wave-fold_20260927_b.md | finding | 2026-09-27 | 0+7/1 | 2240 | KEEP
BURN_b2-wave-fold_20260927_c.md | finding | 2026-09-27 | 0+4/1 | 2237 | KEEP
BURN_b2-wave-fold_20260927_d.md | finding | 2026-09-27 | 0+3/1 | 3826 | KEEP
BURN_build-fold-verify_20260926.md | finding | 2026-09-26 | 0+5/1 | 3610 | KEEP
BURN_build-fold-verify_20260926_b.md | finding | 2026-09-26 | 0+5/1 | 3410 | KEEP
BURN_build-fold-verify_20260926_c.md | finding | 2026-09-26 | 0+5/1 | 3943 | KEEP
BURN_build-fold-verify_20260927.md | finding | 2026-09-27 | 0+3/1 | 3633 | KEEP
BURN_doctrine-owed-chase_20260925.md | receipt | 2026-09-25 | 0+5/1 | 3411 | KEEP
BURN_doctrine-owed-chase_20260926.md | receipt | 2026-09-26 | 0+5/1 | 3484 | KEEP
BURN_doctrine-owed-chase_20260926_b.md | receipt | 2026-09-26 | 0+5/1 | 3738 | KEEP
BURN_doctrine-owed-chase_20260926_c.md | receipt | 2026-09-26 | 0+5/1 | 3693 | KEEP
BURN_doctrine-owed-chase_20260926_d.md | receipt | 2026-09-26 | 0+5/1 | 3581 | KEEP
BURN_doctrine-owed-chase_20260926_e.md | receipt | 2026-09-26 | 0+5/1 | 3591 | KEEP
BURN_doctrine-owed-chase_20260927.md | receipt | 2026-09-27 | 0+4/1 | 3431 | KEEP
BURN_doctrine-owed-chase_20260927_b.md | receipt | 2026-09-27 | 0+3/1 | 2953 | KEEP
BURN_doctrine-owed-chase_20260927_c.md | receipt | 2026-09-27 | 0+3/1 | 3038 | KEEP
BURN_doctrine-owed-chase_20260927_d.md | receipt | 2026-09-27 | 0+4/0 | 3265 | ARCHIVE
BURN_doctrine-owed-chase_20260927_e.md | receipt | 2026-09-27 | 0+4/0 | 3408 | ARCHIVE
BURN_doctrine-owed-chase_20260927_f.md | receipt | 2026-09-27 | 0+3/0 | 3444 | ARCHIVE
BURN_doctrine-owed-chase_20260928.md | receipt | 2026-09-28 | 0+3/1 | 3369 | KEEP
BURN_doctrine-owed-chase_20260928_b.md | receipt | 2026-09-28 | 0+3/0 | 3806 | ARCHIVE
BURN_doctrine-owed-chase_20260928_c.md | receipt | 2026-09-28 | 0+3/0 | 3581 | ARCHIVE
BURN_doctrine-owed-chase_20260928_d.md | receipt | 2026-09-28 | 0+3/1 | 3356 | KEEP
BURN_doctrine-owed-chase_20260928_e.md | receipt | 2026-09-28 | 0+3/0 | 2883 | ARCHIVE
BURN_doctrine-owed-chase_20260928_f.md | receipt | 2026-09-28 | 0+3/0 | 3104 | ARCHIVE
BURN_doctrine-owed-chase_20260928_g.md | receipt | 2026-09-28 | 0+3/0 | 3239 | ARCHIVE
BURN_doctrine-owed-chase_20260928_h.md | receipt | 2026-09-28 | 0+3/1 | 3672 | KEEP
BURN_doctrine-owed-chase_20260928_i.md | receipt | 2026-09-28 | 0+3/0 | 2626 | ARCHIVE
BURN_doctrine-owed-chase_20260928_j.md | receipt | 2026-09-28 | 0+2/0 | 3586 | ARCHIVE
BURN_doctrine-owed-chase_20260928_k.md | receipt | 2026-09-28 | 0+2/0 | 3172 | ARCHIVE
BURN_doctrine-owed-chase_20260928_l.md | receipt | 2026-09-28 | 0+2/0 | 3908 | ARCHIVE
BURN_doctrine-owed-chase_20260928_m.md | receipt | 2026-09-28 | 0+2/0 | 2968 | ARCHIVE
BURN_free-resource-landscape_20260925.md | finding | 2026-09-25 | 0+5/1 | 2855 | KEEP
BURN_free-resource-landscape_20260925_b.md | finding | 2026-09-25 | 0+5/1 | 3068 | KEEP
BURN_free-resource-landscape_20260925_c.md | finding | 2026-09-25 | 0+5/1 | 3572 | KEEP
BURN_free-resource-landscape_20260925_d.md | finding | 2026-09-25 | 0+5/1 | 4098 | KEEP
BURN_free-resource-landscape_20260926_e.md | finding | 2026-09-26 | 0+5/1 | 3166 | KEEP
BURN_free-resource-landscape_20260926_f.md | finding | 2026-09-26 | 0+4/1 | 4012 | KEEP
BURN_free-resource-landscape_20260926_g.md | finding | 2026-09-26 | 0+5/1 | 3434 | KEEP
BURN_free-resource-landscape_20260926_h.md | finding | 2026-09-26 | 0+6/1 | 3522 | KEEP
BURN_free-resource-landscape_20260927_b.md | finding | 2026-09-27 | 0+4/1 | 3117 | KEEP
BURN_free-resource-landscape_20260927_c.md | finding | 2026-09-27 | 0+3/1 | 3237 | KEEP
BURN_free-resource-landscape_20260927_d.md | finding | 2026-09-27 | 0+3/1 | 3211 | KEEP
BURN_free-resource-landscape_20260927_e.md | finding | 2026-09-27 | 0+3/1 | 2305 | KEEP
BURN_free-resource-landscape_20260927_f.md | finding | 2026-09-27 | 0+4/0 | 3249 | REVIEW
BURN_free-resource-landscape_20260927_g.md | finding | 2026-09-27 | 0+4/0 | 3530 | REVIEW
BURN_free-resource-landscape_20260927_h.md | finding | 2026-09-27 | 0+4/0 | 3703 | REVIEW
BURN_free-resource-landscape_20260927_i.md | finding | 2026-09-27 | 0+4/0 | 3504 | REVIEW
BURN_free-resource-landscape_20260927_j.md | finding | 2026-09-27 | 0+3/0 | 3267 | REVIEW
BURN_free-resource-landscape_20260927_k.md | finding | 2026-09-27 | 0+3/0 | 2715 | REVIEW
BURN_free-resource-landscape_20260928.md | finding | 2026-09-28 | 0+3/0 | 3230 | REVIEW
BURN_free-resource-landscape_20260928_b.md | finding | 2026-09-28 | 0+3/0 | 3139 | REVIEW
BURN_free-resource-landscape_20260928_c.md | finding | 2026-09-28 | 0+3/0 | 2850 | REVIEW
BURN_free-resource-landscape_20260928_d.md | finding | 2026-09-28 | 0+3/0 | 3493 | REVIEW
BURN_free-resource-landscape_20260928_e.md | finding | 2026-09-28 | 0+3/0 | 2987 | REVIEW
BURN_free-resource-landscape_20260928_f.md | finding | 2026-09-28 | 0+3/0 | 3385 | REVIEW
BURN_free-resource-landscape_20260928_g.md | finding | 2026-09-28 | 0+3/0 | 3615 | REVIEW
BURN_free-resource-landscape_20260928_h.md | finding | 2026-09-28 | 0+3/0 | 3146 | REVIEW
BURN_free-resource-landscape_20260928_i.md | finding | 2026-09-28 | 0+3/0 | 3506 | REVIEW
BURN_free-resource-landscape_20260928_j.md | finding | 2026-09-28 | 0+3/0 | 2881 | REVIEW
BURN_free-resource-landscape_20260928_k.md | finding | 2026-09-28 | 0+3/0 | 3928 | REVIEW
BURN_free-resource-landscape_20260928_l.md | finding | 2026-09-28 | 0+2/0 | 3084 | REVIEW
BURN_free-resource-landscape_20260928_m.md | finding | 2026-09-28 | 0+2/0 | 2560 | REVIEW
BURN_free-resource-landscape_20260928_n.md | finding | 2026-09-28 | 0+2/0 | 3421 | REVIEW
BURN_judge-lane-spec_20260925.md | receipt | 2026-09-25 | 0+5/1 | 3722 | KEEP
BURN_judge-lane-spec_20260925_c.md | receipt | 2026-09-25 | 0+5/1 | 3940 | KEEP
BURN_judge-lane-spec_20260925_d.md | receipt | 2026-09-25 | 0+5/1 | 3706 | KEEP
BURN_judge-lane-spec_20260926_e.md | receipt | 2026-09-26 | 1+5/1 | 3509 | KEEP
BURN_judge-lane-spec_20260926_f.md | receipt | 2026-09-26 | 0+5/1 | 3689 | KEEP
BURN_judge-lane-spec_20260926_g.md | receipt | 2026-09-26 | 0+5/1 | 3858 | KEEP
BURN_judge-lane-spec_20260926_h.md | receipt | 2026-09-26 | 0+5/1 | 3518 | KEEP
BURN_judge-lane-spec_20260927.md | receipt | 2026-09-27 | 0+3/1 | 3526 | KEEP
BURN_judge-lane-spec_20260927_c.md | receipt | 2026-09-27 | 0+3/1 | 3803 | KEEP
BURN_middle-path-doctrine_20260925.md | receipt | 2026-09-25 | 0+5/1 | 3547 | KEEP
BURN_middle-path-doctrine_20260926.md | receipt | 2026-09-26 | 1+6/1 | 3499 | KEEP
BURN_middle-path-doctrine_20260926_c.md | receipt | 2026-09-26 | 0+5/1 | 4103 | KEEP
BURN_middle-path-doctrine_20260926_d.md | receipt | 2026-09-26 | 0+5/1 | 3294 | KEEP
BURN_middle-path-doctrine_20260926_e.md | receipt | 2026-09-26 | 0+5/1 | 3249 | KEEP
BURN_middle-path-doctrine_20260926_f.md | receipt | 2026-09-26 | 1+5/1 | 2612 | KEEP
BURN_middle-path-doctrine_20260926_g.md | receipt | 2026-09-26 | 0+6/1 | 3140 | KEEP
BURN_middle-path-doctrine_20260927.md | receipt | 2026-09-27 | 0+5/1 | 3559 | KEEP
BURN_middle-path-doctrine_20260927_b.md | receipt | 2026-09-27 | 0+3/1 | 3108 | KEEP
BURN_middle-path-doctrine_20260927_c.md | receipt | 2026-09-27 | 0+3/1 | 3398 | KEEP
BURN_middle-path-doctrine_20260927_d.md | receipt | 2026-09-27 | 0+4/0 | 3491 | ARCHIVE
BURN_middle-path-doctrine_20260927_e.md | receipt | 2026-09-27 | 0+4/1 | 3368 | KEEP
BURN_middle-path-doctrine_20260927_f.md | receipt | 2026-09-27 | 0+3/0 | 3437 | ARCHIVE
BURN_middle-path-doctrine_20260927_g.md | receipt | 2026-09-27 | 0+3/0 | 3431 | ARCHIVE
BURN_middle-path-doctrine_20260927_h.md | receipt | 2026-09-27 | 0+4/0 | 3877 | ARCHIVE
BURN_middle-path-doctrine_20260927_i.md | receipt | 2026-09-27 | 0+3/0 | 3403 | ARCHIVE
BURN_middle-path-doctrine_20260927_j.md | receipt | 2026-09-27 | 0+3/0 | 3511 | ARCHIVE
BURN_middle-path-doctrine_20260928.md | receipt | 2026-09-28 | 0+3/1 | 3347 | KEEP
BURN_middle-path-doctrine_20260928_b.md | receipt | 2026-09-28 | 0+3/0 | 3893 | ARCHIVE
BURN_middle-path-doctrine_20260928_c.md | receipt | 2026-09-28 | 0+3/0 | 3049 | ARCHIVE
BURN_middle-path-doctrine_20260928_d.md | receipt | 2026-09-28 | 0+3/0 | 3310 | ARCHIVE
BURN_middle-path-doctrine_20260928_e.md | receipt | 2026-09-28 | 0+3/0 | 3631 | ARCHIVE
BURN_middle-path-doctrine_20260928_f.md | receipt | 2026-09-28 | 0+2/0 | 3297 | ARCHIVE
BURN_middle-path-doctrine_20260928_g.md | receipt | 2026-09-28 | 0+2/0 | 3104 | ARCHIVE
BURN_middle-path-doctrine_20260928_h.md | receipt | 2026-09-28 | 0+2/0 | 2995 | ARCHIVE
BURN_middle-path-doctrine_20260928_i.md | receipt | 2026-09-28 | 0+3/1 | 3314 | KEEP
BURN_middle-path-doctrine_20260928_j.md | receipt | 2026-09-28 | 0+3/0 | 2956 | ARCHIVE
BURN_middle-path-doctrine_20260928_k.md | receipt | 2026-09-28 | 0+3/0 | 3808 | ARCHIVE
BURN_prompt-uplift-lane_20260925.md | brief | 2026-09-25 | 1+5/1 | 3083 | KEEP
BURN_prompt-uplift-lane_20260925_b.md | brief | 2026-09-25 | 0+5/1 | 3210 | KEEP
BURN_prompt-uplift-lane_20260925_c.md | brief | 2026-09-25 | 0+5/1 | 3742 | KEEP
BURN_prompt-uplift-lane_20260925_d.md | brief | 2026-09-25 | 1+5/1 | 3813 | KEEP
BURN_prompt-uplift-lane_20260926_f.md | brief | 2026-09-26 | 0+5/1 | 3503 | KEEP
BURN_prompt-uplift-lane_20260926_g.md | brief | 2026-09-26 | 0+5/1 | 3650 | KEEP
BURN_prompt-uplift-lane_20260927.md | brief | 2026-09-27 | 0+3/1 | 3294 | KEEP
BURN_queue-field_20260925.md | receipt | 2026-09-25 | 0+5/1 | 3675 | KEEP
BURN_queue-field_20260925_b.md | receipt | 2026-09-25 | 0+5/1 | 3429 | KEEP
BURN_queue-field_20260925_c.md | receipt | 2026-09-25 | 0+5/1 | 3577 | KEEP
BURN_queue-field_20260926.md | receipt | 2026-09-26 | 0+5/1 | 2879 | KEEP
BURN_queue-field_20260926_b.md | receipt | 2026-09-26 | 0+5/1 | 2583 | KEEP
BURN_queue-field_20260926_c.md | receipt | 2026-09-26 | 0+5/1 | 3177 | KEEP
BURN_queue-field_20260926_d.md | receipt | 2026-09-26 | 0+5/1 | 2777 | KEEP
BURN_queue-field_20260927.md | receipt | 2026-09-27 | 1+3/1 | 3480 | KEEP
BURN_queue-field_20260927_b.md | receipt | 2026-09-27 | 0+3/1 | 3410 | KEEP
BURN_queue-field_20260927_c.md | receipt | 2026-09-27 | 1+3/1 | 3417 | KEEP
BURN_queue-field_20260927_d.md | receipt | 2026-09-27 | 0+3/1 | 2415 | KEEP
BURN_roblox-durable-lane_20260925.md | receipt | 2026-09-25 | 0+5/1 | 2912 | KEEP
BURN_rsi-harness_20260925.md | receipt | 2026-09-25 | 0+6/1 | 3478 | KEEP
BURN_rsi-harness_20260925_b.md | receipt | 2026-09-25 | 0+5/1 | 3363 | KEEP
BURN_rsi-harness_20260925_c.md | receipt | 2026-09-25 | 0+6/1 | 3918 | KEEP
BURN_rsi-harness_20260926.md | receipt | 2026-09-26 | 13+9/1 | 3420 | KEEP
BURN_rsi-harness_20260926_b.md | receipt | 2026-09-26 | 0+5/1 | 3621 | KEEP
BURN_rsi-harness_20260926_c.md | receipt | 2026-09-26 | 0+7/1 | 3841 | KEEP
BURN_rsi-harness_20260926_d.md | receipt | 2026-09-26 | 0+6/1 | 3014 | KEEP
BURN_rsi-harness_20260926_e.md | receipt | 2026-09-26 | 0+6/1 | 3570 | KEEP
BURN_rsi-harness_20260927_f.md | receipt | 2026-09-27 | 0+3/1 | 3089 | KEEP
BURN_rsi-harness_20260927_g.md | receipt | 2026-09-27 | 0+4/0 | 3108 | ARCHIVE
BURN_steering-theory_20260925.md | finding | 2026-09-25 | 2+5/1 | 3241 | KEEP
BURN_steering-theory_20260925_b.md | finding | 2026-09-25 | 2+5/1 | 3621 | KEEP
BURN_steering-theory_20260925_c.md | finding | 2026-09-25 | 1+5/1 | 4554 | KEEP
BURN_steering-theory_20260926.md | finding | 2026-09-26 | 2+5/1 | 3541 | KEEP
BURN_steering-theory_20260926_b.md | finding | 2026-09-26 | 1+5/1 | 3926 | KEEP
BURN_steering-theory_20260926_c.md | finding | 2026-09-26 | 1+5/1 | 4075 | KEEP
BURN_steering-theory_20260926_d.md | finding | 2026-09-26 | 0+5/1 | 2938 | KEEP
BURN_steering-theory_20260926_e.md | finding | 2026-09-26 | 0+5/1 | 2804 | KEEP
BURN_steering-theory_20260926_f.md | finding | 2026-09-26 | 0+5/1 | 3625 | KEEP
BURN_steering-theory_20260927.md | finding | 2026-09-27 | 0+3/1 | 3466 | KEEP
BURN_steering-theory_20260927_b.md | finding | 2026-09-27 | 0+3/1 | 3156 | KEEP
BURN_stego-canon-pipeline_20260925.md | receipt | 2026-09-25 | 0+5/1 | 3309 | KEEP
BURN_stego-canon-pipeline_20260925_b.md | receipt | 2026-09-25 | 0+5/1 | 3331 | KEEP
BURN_stego-canon-pipeline_20260925_c.md | receipt | 2026-09-25 | 0+5/1 | 3811 | KEEP
BURN_stego-canon-pipeline_20260926_d.md | receipt | 2026-09-26 | 0+5/1 | 3710 | KEEP
BURN_stego-canon-pipeline_20260926_e.md | receipt | 2026-09-26 | 0+5/1 | 3206 | KEEP
BURN_stego-canon-pipeline_20260926_f.md | receipt | 2026-09-26 | 0+5/1 | 3260 | KEEP
BURN_stego-canon-pipeline_20260926_g.md | receipt | 2026-09-26 | 0+5/1 | 3348 | KEEP
BURN_stego-canon-pipeline_20260927.md | receipt | 2026-09-27 | 0+4/1 | 3807 | KEEP
BURN_stego-canon-pipeline_20260927_b.md | receipt | 2026-09-27 | 0+3/1 | 3973 | KEEP
BURN_stego-canon-pipeline_20260927_c.md | receipt | 2026-09-27 | 0+3/1 | 3166 | KEEP
BURN_stego-canon-pipeline_20260927_d.md | receipt | 2026-09-27 | 0+4/0 | 4161 | ARCHIVE
BURN_stego-canon-pipeline_20260927_e.md | receipt | 2026-09-27 | 0+4/0 | 3545 | ARCHIVE
BURN_stego-canon-pipeline_20260927_f.md | receipt | 2026-09-27 | 0+3/0 | 3194 | ARCHIVE
BURN_stego-canon-pipeline_20260927_g.md | receipt | 2026-09-27 | 0+3/0 | 3407 | ARCHIVE
BURN_stego-canon-pipeline_20260927_h.md | receipt | 2026-09-27 | 0+4/0 | 3554 | ARCHIVE
BURN_stego-canon-pipeline_20260927_i.md | receipt | 2026-09-27 | 0+3/0 | 3321 | ARCHIVE
BURN_stego-canon-pipeline_20260927_j.md | receipt | 2026-09-27 | 0+3/0 | 2719 | ARCHIVE
BURN_third-way-game_20260925.md | receipt | 2026-09-25 | 0+5/1 | 3845 | KEEP
BURN_third-way-game_20260926.md | receipt | 2026-09-26 | 0+5/1 | 4136 | KEEP
BURN_third-way-game_20260926_b.md | receipt | 2026-09-26 | 0+5/1 | 3166 | KEEP
BURN_third-way-game_20260926_c.md | receipt | 2026-09-26 | 0+5/1 | 3612 | KEEP
BURN_third-way-game_20260926_d.md | receipt | 2026-09-26 | 0+5/1 | 2644 | KEEP
BURN_third-way-game_20260926_e.md | receipt | 2026-09-26 | 0+5/1 | 3103 | KEEP
BURN_third-way-game_20260926_f.md | receipt | 2026-09-26 | 0+5/1 | 3704 | KEEP
BURN_third-way-game_20260927_b.md | receipt | 2026-09-27 | 0+3/1 | 3473 | KEEP
BURN_third-way-game_20260927_c.md | receipt | 2026-09-27 | 0+4/0 | 3577 | ARCHIVE
BURN_third-way-game_20260927_d.md | receipt | 2026-09-27 | 0+3/0 | 3329 | ARCHIVE
BURN_world-models-multi-agent_20260925.md | receipt | 2026-09-25 | 0+5/1 | 3480 | KEEP
BURN_world-models-multi-agent_20260925_b.md | receipt | 2026-09-25 | 0+5/1 | 3832 | KEEP
BURN_world-models-multi-agent_20260925_c.md | receipt | 2026-09-25 | 0+5/1 | 3905 | KEEP
BURN_world-models-multi-agent_20260926_d.md | receipt | 2026-09-26 | 0+4/1 | 3458 | KEEP
BURN_world-models-multi-agent_20260926_e.md | receipt | 2026-09-26 | 0+5/1 | 3480 | KEEP
BURN_world-models-multi-agent_20260926_f.md | receipt | 2026-09-26 | 0+5/1 | 3224 | KEEP
BURN_world-models-multi-agent_20260926_g.md | receipt | 2026-09-26 | 0+5/1 | 3506 | KEEP
BURN_world-models-multi-agent_20260927.md | receipt | 2026-09-27 | 0+4/1 | 2842 | KEEP
BURN_world-models-multi-agent_20260927_b.md | receipt | 2026-09-27 | 0+3/1 | 2895 | KEEP
BURN_world-models-multi-agent_20260927_c.md | receipt | 2026-09-27 | 0+4/0 | 3845 | ARCHIVE
BURN_world-models-multi-agent_20260927_d.md | receipt | 2026-09-27 | 0+3/0 | 4216 | ARCHIVE
BURN_world-models-multi-agent_20260927_e.md | receipt | 2026-09-27 | 0+4/0 | 3816 | ARCHIVE
BURN_world-models-multi-agent_20260927_f.md | receipt | 2026-09-27 | 0+3/0 | 3851 | ARCHIVE
BURN_world-models-multi-agent_20260927_g.md | receipt | 2026-09-27 | 0+3/0 | 3558 | ARCHIVE
BURN_world-models-multi-agent_20260928.md | receipt | 2026-09-28 | 0+3/0 | 3863 | ARCHIVE
BURN_world-models-multi-agent_20260928_b.md | receipt | 2026-09-28 | 0+3/0 | 3535 | ARCHIVE
BURN_world-models-multi-agent_20260928_c.md | receipt | 2026-09-28 | 0+3/0 | 3792 | ARCHIVE
BURN_world-models-multi-agent_20260928_d.md | receipt | 2026-09-28 | 0+3/0 | 3772 | ARCHIVE
B_CHAIN1_REASONING_INTAKE_20260907.md | receipt | 2026-09-07 | 0+7/1 | 7281 | KEEP
C1_FOLD_20260912.md | finding | 2026-09-12 | 0+4/1 | 8475 | KEEP
CAGE_INTAKE_DFHACK_V0.md | receipt | 2026-09-14 | 0+7/1 | 5525 | KEEP
CANDLE_RESOLVED_20260921.md | receipt | 2026-09-21 | 0+4/1 | 2378 | KEEP
CANON_EXTENSION_20260911.md | receipt | 2026-09-11 | 0+4/1 | 2703 | KEEP
CANON_EXTENSION_SIGNED_20260912.md | receipt | 2026-09-12 | 0+4/1 | 2899 | KEEP
CANON_FIVE_POSTS_20260911.md | receipt | 2026-09-11 | 0+5/1 | 3279 | KEEP
CANTOR_DECODE_20260921.md | finding | 2026-09-21 | 0+4/1 | 2917 | KEEP
CANTOR_DIAG_INTAKE_20260921.md | receipt | 2026-09-21 | 0+4/1 | 2083 | KEEP
CASTLE_TRACK_20260911.md | receipt | 2026-09-11 | 0+5/1 | 8070 | KEEP
CATHEDRAL_COMBINE_deepseek_20260924.md | receipt | 2026-09-24 | 0+4/1 | 5204 | KEEP
CATHEDRAL_COMBINE_groq_20260924.md | finding | 2026-09-24 | 0+4/1 | 7947 | KEEP
CATHEDRAL_SPEC_OF_RECORD_20260924.md | receipt | 2026-09-24 | 0+4/1 | 5272 | KEEP
CELL_FALSIFIER_LEDGER_READY_20260912.md | receipt | 2026-09-12 | 0+4/1 | 4174 | KEEP
CHAIN_INDEX_AUDIT_20260905.md | receipt | 2026-09-05 | 0+10/1 | 2916 | KEEP
CHAIN_STOP_INVESTIGATION_20260911.md | receipt | 2026-09-11 | 0+7/1 | 9422 | KEEP
CHAIR_FOLD_CORPUS_MINE_20260922.md | finding | 2026-09-22 | 0+4/1 | 1285 | KEEP
CHAN_COMMIT_001_20260901.md | receipt | 2026-09-01 | 0+8/1 | 1656 | KEEP
CIN_FOLD_20260912.md | finding | 2026-09-12 | 0+5/1 | 9615 | KEEP
CITE_GATE_BUILD_20260906.md | receipt | 2026-09-06 | 0+6/1 | 4034 | KEEP
CLARKES_END_CENTERLINE_20260912.md | receipt | 2026-09-12 | 0+5/1 | 5622 | KEEP
CLARKES_END_SEAT_READ_20260912.md | finding | 2026-09-12 | 0+4/1 | 4291 | KEEP
CODEX_ACTIVATION_20260901.md | receipt | 2026-09-01 | 0+9/1 | 455 | KEEP
CODEX_TASK_001_20260901.md | brief | 2026-09-01 | 0+9/1 | 1100 | KEEP
CODEX_TASK_001_REVIEW_20260901.md | brief | 2026-09-01 | 0+13/1 | 5161 | KEEP
CODEX_TASK_002_20260901.md | brief | 2026-09-01 | 0+9/1 | 2356 | KEEP
CODEX_TASK_003_20260901.md | brief | 2026-09-01 | 0+10/1 | 3039 | KEEP
CODEX_TASK_003_REPORT_20260901.md | brief | 2026-09-01 | 0+8/1 | 3012 | KEEP
CODEX_TASK_004_20260901.md | brief | 2026-09-01 | 0+10/1 | 2564 | KEEP
CODEX_TASK_005_20260901.md | brief | 2026-09-01 | 0+9/1 | 2448 | KEEP
CODEX_WITNESS_Manual_Audit_Steg_Analysis_20260918.md | finding | 2026-09-18 | 0+5/1 | 18767 | KEEP
COGNITIVE_CONTROL_PLANE_20260919.md | receipt | 2026-09-19 | 0+5/1 | 4830 | KEEP
COLDEST_SHARD_VEIL_TEX_MAP_20260920.md | finding | 2026-09-20 | 0+5/1 | 4958 | KEEP
COLDEST_VERTEX_STEAL_MAP_20260923.md | finding | 2026-09-23 | 0+5/1 | 7132 | KEEP
COLD_READ_TEST_20260912.md | receipt | 2026-09-12 | 1+4/1 | 3748 | KEEP
COLONY_GRAMMAR_20260913.md | receipt | 2026-09-13 | 0+4/1 | 6973 | KEEP
COMPUTE_WEALTH_INVENTORY_20260918.md | finding | 2026-09-18 | 0+5/1 | 2190 | KEEP
CONCEPTUAL_SPACES_STEAL_20260918.md | finding | 2026-09-18 | 0+5/1 | 4523 | KEEP
CONSTRAINT_ENGINEERING_TOLDYOUSO_20260913.md | other | 2026-09-13 | 0+4/1 | 5413 | REVIEW
CONTEXT_OS_20260918.md | receipt | 2026-09-18 | 1+6/1 | 4440 | KEEP
CONVERGENCE_RUBIK_GRAPH_20260922.md | receipt | 2026-09-22 | 0+4/1 | 8959 | KEEP
CORPUS_MAP_SALON_20260918.md | finding | 2026-09-18 | 8+7/1 | 30567 | KEEP
CORPUS_MINE_FOLD_20260922.md | finding | 2026-09-22 | 0+4/1 | 3708 | KEEP
DAILY_COMPUTE_PLAN_20260924.md | receipt | 2026-09-24 | 0+4/1 | 4272 | KEEP
DASH25_DIAGNOSIS_20260922.md | receipt | 2026-09-22 | 0+4/1 | 5998 | KEEP
DAWN_READING_MIRROR_20260907.md | receipt | 2026-09-07 | 0+12/1 | 5875 | KEEP
DECODE_NONEQ_MC_RL_20260922.md | finding | 2026-09-22 | 0+4/1 | 3603 | KEEP
DEEPSEEK_ADVERSARIAL_ARC_20260918.md | receipt | 2026-09-18 | 0+7/1 | 20665 | KEEP
DEEPSEEK_OFFPEAK_CACHE_RATIO_RECEIPT_20260925.md | receipt | 2026-09-25 | 0+4/1 | 8483 | KEEP
DEEP_THREAD_FOLD_20260913.md | finding | 2026-09-13 | 0+4/1 | 3709 | KEEP
DEPTH_CHAIN_20260912.md | finding | 2026-09-12 | 0+4/1 | 6559 | KEEP
DEPTH_SALON_FOLD_20260913.md | finding | 2026-09-13 | 0+4/1 | 3576 | KEEP
DESKTOP_CORPUS_DATED_20260911.md | receipt | 2026-09-11 | 0+4/1 | 10869 | KEEP
DESKTOP_HOMECOMING_20260909.md | receipt | 2026-09-09 | 0+4/1 | 2828 | KEEP
DESKTOP_SALON_CORPUS_MINED_20260911.md | receipt | 2026-09-11 | 0+4/1 | 15066 | KEEP
DESK_DEFENSE_FACTORY_20260911.md | receipt | 2026-09-11 | 0+4/1 | 5393 | KEEP
DESK_DOGFOOD_VISUAL_DECK_20260911.md | receipt | 2026-09-11 | 1+3/1 | 3190 | KEEP
DESK_DSV41FLASH_20260911.md | receipt | 2026-09-11 | 1+4/1 | 4878 | KEEP
DESK_FOLD_SEVEN_20260911.md | finding | 2026-09-11 | 1+4/1 | 4107 | KEEP
DESK_FOLD_SEVEN_MCP_20260911.md | finding | 2026-09-11 | 0+4/1 | 4144 | KEEP
DESK_FOLD_ZEITGEIST_WAVE_20260911.md | finding | 2026-09-11 | 0+4/1 | 4108 | KEEP
DESK_TRACE_AS_STATE_20260911.md | finding | 2026-09-11 | 0+4/1 | 4340 | KEEP
DIRECTIVE_WATCHERS_20260926.md | receipt | 2026-09-26 | 0+8/1 | 3070 | KEEP
DIVERGENCE_TEST_CARD_20260912.md | receipt | 2026-09-12 | 0+4/1 | 5290 | KEEP
DOGFOOD_OPERATING_ENVIRONMENT_20260922.md | receipt | 2026-09-22 | 1+4/1 | 7836 | KEEP
DOOR_VERIFIER_INTAKE_20260906.md | receipt | 2026-09-06 | 0+7/1 | 4125 | KEEP
DOZEN_WIDE_FOLD_20260912.md | finding | 2026-09-12 | 0+4/1 | 5921 | KEEP
DRAFT_SWEEP_20260927.md | receipt | 2026-09-27 | 0+3/1 | 1794 | KEEP
DRIFT_DONT_COIL_20260911.md | finding | 2026-09-11 | 0+6/1 | 4228 | KEEP
DRIFT_PATROL_20260915.md | receipt | 2026-09-15 | 0+5/1 | 1430 | KEEP
DRIFT_PATROL_20260915_run2.md | receipt | 2026-09-15 | 0+5/1 | 1581 | KEEP
DRIFT_PATROL_20260916.md | receipt | 2026-09-16 | 0+5/1 | 1845 | KEEP
DRIFT_PATROL_20260917.md | receipt | 2026-09-17 | 0+4/1 | 2071 | KEEP
DRIFT_PATROL_20260918.md | receipt | 2026-09-18 | 0+4/1 | 1798 | KEEP
DRIFT_PATROL_20260919.md | receipt | 2026-09-19 | 0+4/1 | 2212 | KEEP
DRIFT_PATROL_20260920.md | receipt | 2026-09-20 | 0+4/1 | 2308 | KEEP
DRIFT_PATROL_20260921.md | receipt | 2026-09-21 | 0+4/1 | 1666 | KEEP
DRIFT_PATROL_20260922.md | receipt | 2026-09-22 | 0+4/1 | 1952 | KEEP
DRIFT_PATROL_20260923.md | receipt | 2026-09-23 | 0+4/1 | 2531 | KEEP
DRIFT_PATROL_20260924.md | receipt | 2026-09-24 | 0+4/1 | 1376 | KEEP
DRIFT_PATROL_20260925.md | receipt | 2026-09-25 | 1+4/1 | 2080 | KEEP
DRIFT_PATROL_20260926.md | receipt | 2026-09-26 | 0+4/1 | 1884 | KEEP
DRIFT_PATROL_20260927.md | receipt | 2026-09-27 | 0+3/1 | 2640 | KEEP
DRIFT_PATROL_20260928.md | receipt | 2026-09-28 | 0+2/1 | 3925 | KEEP
DRIFT_PATROL_CRON_CHARTER_20260926.md | finding | 2026-09-26 | 0+4/1 | 3152 | KEEP
DUNGEON_PRECEDENTS_20260924.md | finding | 2026-09-24 | 1+3/1 | 7067 | KEEP
ECHOIC_DRIFT_QUERY_20260912.md | receipt | 2026-09-12 | 0+4/1 | 4173 | KEEP
EIGHT_WAVE_INTAKE_20260921.md | finding | 2026-09-21 | 0+4/1 | 703 | KEEP
EIGHT_WAVE_STEAL_MAP_20260921.md | finding | 2026-09-21 | 0+5/1 | 3797 | KEEP
ELDER_ASK_SEED_AUDIT_20260926.md | brief | 2026-09-26 | 6+5/1 | 6094 | KEEP
ELDER_DASH25_RULING_20260922.md | receipt | 2026-09-22 | 0+4/1 | 2261 | KEEP
ELDER_LENS_20260919_TWO_WITNESSES.md | finding | 2026-09-19 | 1+5/1 | 4682 | KEEP
ELDER_SANCHO_STEERING_SURFACE_20260922.md | receipt | 2026-09-22 | 0+4/1 | 7556 | KEEP
ELEVATION_RICE_20260906.md | finding | 2026-09-06 | 0+6/1 | 9584 | KEEP
ELITESAVIOR_CALLOUT_20260920.md | receipt | 2026-09-20 | 0+4/1 | 8937 | KEEP
ELITESAVIOR_QUOTEPOST_THREAD_20260920.md | finding | 2026-09-20 | 0+4/1 | 6523 | KEEP
ELITESAVIOR_RACTOR_SHITPOST_RESPONSE_20260920.md | shitpost | 2026-09-20 | 0+4/1 | 6386 | KEEP
ENGINES_IN_CHARGE_20260916.md | finding | 2026-09-16 | 0+4/1 | 2392 | KEEP
ENGRAM_FOLD_20260913.md | finding | 2026-09-13 | 1+5/1 | 2765 | KEEP
ENGRAM_OPEN_WEIGHTS_20260911.md | receipt | 2026-09-11 | 1+5/1 | 4948 | KEEP
ENHANCE_NOT_BYPASS_20260926.md | receipt | 2026-09-26 | 0+5/1 | 3632 | KEEP
ENVELOPE_50W_HIT_20260926.md | finding | 2026-09-26 | 1+8/1 | 1009 | KEEP
ENVELOPE_LAW_20260926.md | law | 2026-09-26 | 0+4/1 | 853 | KEEP
EQUIVALENCE_SHADER_ENV_20260912.md | other | 2026-09-12 | 0+5/1 | 2661 | REVIEW
ESSENTIALS_RESTORE.md | receipt | 2026-09-27 | 0+6/1 | 1693 | KEEP
ESTATE_WALK_SPATIAL_20260914.md | receipt | 2026-09-14 | 0+5/1 | 4757 | KEEP
EUT_AUDITOR_WORLDVIEW_20260912.md | receipt | 2026-09-12 | 0+6/1 | 3941 | KEEP
EVENTS_DRIFT_LAW_20260926.md | law | 2026-09-26 | 0+5/1 | 1831 | KEEP
EXP002A_RECEIPT_20260901.md | receipt | 2026-09-01 | 0+11/1 | 4170 | KEEP
EXTERNAL_STEAL_DESK_CORPUS_20260917.md | finding | 2026-09-17 | 0+6/1 | 4605 | KEEP
F11_gomoku_rules_lens.md | finding | 2026-09-14 | 0+4/1 | 3581 | KEEP
FACTORY_GRAMMAR_20260913.md | receipt | 2026-09-13 | 0+4/1 | 5451 | KEEP
FAILOPEN_AUTHORITY_GATE_20260911.md | other | 2026-09-11 | 0+6/1 | 1910 | REVIEW
FALLEN_HUMANITY_DEBATE_20260915.md | receipt | 2026-09-15 | 0+7/1 | 14310 | KEEP
FAMILY_ATLAS_20260911.md | finding | 2026-09-11 | 0+4/1 | 11937 | KEEP
FANOUT_STANDING_ORGAN_20260912.md | other | 2026-09-12 | 0+4/1 | 2450 | REVIEW
FASTSEARCH_STATIC_KEY_PROBE_20260925.md | finding | 2026-09-25 | 0+4/1 | 4486 | KEEP
FENCE_TEST_PASSED_20260913.md | receipt | 2026-09-13 | 0+4/1 | 1592 | KEEP
FIFTY_WIDE_BOARD_20260915.md | finding | 2026-09-15 | 0+18/1 | 6112 | KEEP
FIFTY_WIDE_BOARD_20260917.md | receipt | 2026-09-17 | 0+4/1 | 7620 | KEEP
FIVE_LINK_INTAKE_20260913.md | receipt | 2026-09-13 | 0+5/1 | 2908 | KEEP
FIVE_MIRRORS_SELF_STEAL_20260912.md | finding | 2026-09-12 | 0+4/1 | 4946 | KEEP
FIVE_MORE_LINKS_20260913.md | finding | 2026-09-13 | 0+5/1 | 2870 | KEEP
FIX_ROTATION_AND_INDEX_20260907.md | receipt | 2026-09-07 | 0+6/1 | 4820 | KEEP
FLASHX_PROBE_20260927.md | finding | 2026-09-27 | 0+4/1 | 2782 | KEEP
FLEET_CANON_COOL_SHIT_20260926.md | receipt | 2026-09-26 | 0+4/1 | 5050 | KEEP
FLEET_IMPRINT_20260917.md | finding | 2026-09-17 | 2+24/1 | 412185 | KEEP
FLEET_KNOWLEDGE_GRAPH_20260917.md | receipt | 2026-09-17 | 1+6/1 | 9074 | KEEP
FLEET_LIGHTMAP_V2_20260906.md | finding | 2026-09-06 | 0+5/1 | 4433 | KEEP
FLEET_MIX_LAW_20260922.md | law | 2026-09-22 | 0+4/1 | 2631 | KEEP
FLEET_TASK_DOCTOR_20260927.md | brief | 2026-09-27 | 1+3/1 | 3132 | KEEP
FLT_20260906/SOURCES.md | finding | 2026-09-14 | 23+27/1 | 3075 | KEEP
FLUID_LENS_MANIFEST_20260913.md | finding | 2026-09-13 | 0+4/1 | 6508 | KEEP
FLY1_EXTRACTION_SPEC_20260911.md | finding | 2026-09-11 | 0+5/1 | 13452 | KEEP
FLY1_IMPL_RECON_20260911.md | receipt | 2026-09-11 | 0+4/1 | 10114 | KEEP
FLY1_QUEUED_20260911.md | receipt | 2026-09-11 | 0+4/1 | 1428 | KEEP
FLY_CONNECTOME_GOMOKU_20260912.md | receipt | 2026-09-12 | 0+5/1 | 2019 | KEEP
FLY_CONNECTOME_NEURAL_EMERGENCE_STEAL_20260912.md | finding | 2026-09-12 | 0+4/1 | 3121 | KEEP
FOLD_V2_DIRECTIONS_20260922.md | finding | 2026-09-22 | 0+4/1 | 517 | KEEP
FOLD_V2_DIRECTIONS_20260927.md | finding | 2026-09-27 | 0+4/1 | 496 | KEEP
FORGED_CANARY_RETIREMENT_20260912.md | receipt | 2026-09-12 | 0+4/1 | 2060 | KEEP
FORGED_STEER_TEST_20260911.md | receipt | 2026-09-11 | 0+4/1 | 4131 | KEEP
FOSSIL_CENSUS_20260927.md | finding | 2026-09-27 | 5+3/1 | 3943 | KEEP
FOUNDING_KNOTS_CROSSCHECK_20260911.md | finding | 2026-09-11 | 0+5/1 | 11592 | KEEP
FOUNDING_SENTENCE_RESTATEMENT_20260928.md | receipt | 2026-09-28 | 0+3/0 | 802 | ARCHIVE
FOUR_CONDITION_PREREGISTRATION_20260918.md | receipt | 2026-09-18 | 1+8/1 | 5968 | KEEP
FOUR_LINK_WAVE_20260912.md | finding | 2026-09-12 | 0+4/1 | 4685 | KEEP
FREELANE_DEEPDIVE_QUEUE_20260926.md | finding | 2026-09-26 | 0+4/1 | 1250 | KEEP
FREE_LANE_INTEL_BONSAI2_20260923.md | receipt | 2026-09-23 | 0+4/1 | 5565 | KEEP
FREE_TIER_AUDIT_20260906.md | receipt | 2026-09-06 | 0+7/1 | 4511 | KEEP
FROM_MUD_TO_WOW_20260914.md | receipt | 2026-09-14 | 0+12/1 | 53027 | KEEP
FROM_MUD_TO_WOW_20260914_WITNESSES.md | receipt | 2026-09-14 | 0+7/1 | 11612 | KEEP
FRONTDOOR_MISSING_JOINS_20260901.md | receipt | 2026-09-01 | 0+9/1 | 4757 | KEEP
FRONTIER_DISPATCH_001_20260905.md | brief | 2026-09-05 | 1+11/1 | 2421 | KEEP
FRONTIER_DISPATCH_001_20260905_COMPLETE.md | brief | 2026-09-05 | 0+7/1 | 13582 | KEEP
FRONTIER_FROM_FLASH_CLIMB1_20260920.md | receipt | 2026-09-20 | 0+4/1 | 4651 | KEEP
FRONTIER_GAME_REPOS_20260924.md | other | 2026-09-24 | 1+4/1 | 5012 | REVIEW
FRONTIER_SIGNAL_INCIDENT_SPACE_20260906.md | receipt | 2026-09-06 | 0+8/1 | 1974 | KEEP
FRONTIER_SOULS_INTAKE_20260915.md | finding | 2026-09-15 | 0+7/1 | 8428 | KEEP
FRONT_DOOR_STEAL_20260923.md | finding | 2026-09-23 | 0+4/1 | 2366 | KEEP
FULL_AUDIT_MAP_20260914.md | finding | 2026-09-14 | 0+8/1 | 7166 | KEEP
FULL_SCAN_REPORT_20260923.md | other | 2026-09-23 | 1+5/1 | 233 | REVIEW
G6_HISTORY_DIGEST_20260926.md | finding | 2026-09-26 | 0+3/1 | 3157 | KEEP
GALA_20260925.md | receipt | 2026-09-25 | 1+7/1 | 5229 | KEEP
GALA_GRAVE_c1-master-handoff-fossil.md | brief | 2026-09-25 | 1+4/1 | 6099 | KEEP
GALA_GRAVE_c2-peer-json-graves.md | receipt | 2026-09-26 | 1+3/1 | 5760 | KEEP
GALA_GRAVE_c3-goodnight-overnight.md | receipt | 2026-09-26 | 1+4/1 | 6674 | KEEP
GALA_MORNING_AFTER_PREREG_20260926.md | receipt | 2026-09-26 | 0+6/1 | 2015 | KEEP
GAMEDIG_MASTER_ATLAS_20260927.md | receipt | 2026-09-27 | 0+4/1 | 3973 | KEEP
GAMEDIG_co-op-social-ValheimDST-vein_20260926.md | receipt | 2026-09-26 | 0+4/1 | 88529 | KEEP
GAMEDIG_creature-farming-PalworldStardew-vein_20260926.md | receipt | 2026-09-26 | 0+4/1 | 105782 | KEEP
GAMEDIG_horror-maze-DOORSLethal-vein_20260926.md | receipt | 2026-09-26 | 0+4/1 | 121819 | KEEP
GAMEDIG_liveops-seasonal-GAGAdopt-Me-vein_20260926.md | receipt | 2026-09-26 | 0+4/1 | 86059 | KEEP
GAMEDIG_roguelike-runs-BalatroHades-vein_20260926.md | receipt | 2026-09-26 | 0+4/1 | 87639 | KEEP
GAMES_SITE_PLAYTEST_20260921.md | receipt | 2026-09-21 | 0+5/1 | 8295 | KEEP
GAME_FORGE_MARATHON_20260913.md | receipt | 2026-09-13 | 0+5/1 | 3343 | KEEP
GAMING_CORPUS_PASS_20260923.md | finding | 2026-09-23 | 1+4/1 | 22851 | KEEP
GAMING_THEORY_SELF_STEAL_20260917.md | finding | 2026-09-17 | 0+5/1 | 3291 | KEEP
GAP1_SPAWN_MANIFEST_20260906.md | receipt | 2026-09-06 | 0+26/1 | 4463 | KEEP
GAP_ANALYSIS_20260917.md | finding | 2026-09-17 | 0+6/1 | 3950 | KEEP
GAP_ANALYSIS_AND_STEAL_20260920.md | finding | 2026-09-20 | 0+4/1 | 9989 | KEEP
GAP_ANALYSIS_SOCRATIC_RACTOR_SALON_20260920.md | finding | 2026-09-20 | 0+5/1 | 15578 | KEEP
GAP_LEDGER_20260913.md | finding | 2026-09-13 | 0+5/1 | 2862 | KEEP
GATE_DEBT_BATCH_20260927.md | receipt | 2026-09-27 | 0+3/1 | 5467 | KEEP
GENE_POOL_TOMBSTONE_20260927.md | finding | 2026-09-27 | 1+2/1 | 2716 | KEEP
GEOMETRY_LENS_20260914.md | finding | 2026-09-14 | 0+4/1 | 3904 | KEEP
GHETTO_REPLICATOR_LOGISTICS_PLAN_20260921.md | receipt | 2026-09-21 | 0+4/1 | 3408 | KEEP
GHOST_ARITHMETIC_20260911.md | finding | 2026-09-11 | 0+3/1 | 7575 | KEEP
GHOST_AUTONOMOUS_FIXES_PROBE_20260911.md | finding | 2026-09-11 | 0+4/1 | 7554 | KEEP
GHOST_GAP_HUNT_20260911.md | finding | 2026-09-11 | 0+4/1 | 7495 | KEEP
GHOST_TRAIL_DECODE_20260911.md | finding | 2026-09-11 | 0+4/1 | 8031 | KEEP
GLOBAL_BOND_AUDIT_FEEDBACK_20260922.md | receipt | 2026-09-22 | 0+4/1 | 5625 | KEEP
GOOGLE_CODIRECTOR_STEAL_20260925.md | finding | 2026-09-25 | 0+6/1 | 4041 | KEEP
GOPHER_DIGEST_20260901_0410Z.md | finding | 2026-09-01 | 1+9/1 | 4050 | KEEP
GO_LIST_EXECUTION_20260925.md | receipt | 2026-09-25 | 2+7/1 | 5708 | KEEP
GO_WIDE_PASS_20260927.md | receipt | 2026-09-27 | 0+4/1 | 3095 | KEEP
GPS_FOR_DUMB_AGENTS_20260918.md | receipt | 2026-09-18 | 0+7/1 | 5194 | KEEP
GRIFT_DECLARATION_20260913.md | receipt | 2026-09-13 | 0+4/1 | 1844 | KEEP
GROK47_CLI_BURN_RECEIPT_20260925.md | receipt | 2026-09-25 | 0+4/1 | 6375 | KEEP
GROKBOT_ANDROID_CONVERGENCE_20260921.md | receipt | 2026-09-21 | 0+4/1 | 4164 | KEEP
GROK_ASK4_SCOPE_FREEZE_20260926.md | receipt | 2026-09-26 | 0+5/1 | 5872 | KEEP
GROK_INVERSION_PAIRED_20260916.md | receipt | 2026-09-16 | 0+5/1 | 2484 | KEEP
GROK_LANE_PACKET_20260925.md | receipt | 2026-09-25 | 0+7/1 | 2463 | KEEP
GROK_STRIKE_TRIAGE_20260916.md | receipt | 2026-09-16 | 0+5/1 | 3368 | KEEP
GROUNDING_WAVE_ANSWER_20260907.md | receipt | 2026-09-07 | 0+4/1 | 1618 | KEEP
GROUNDING_WAVE_ATTACK_20260913.md | receipt | 2026-09-13 | 0+4/1 | 1928 | KEEP
GROUNDING_WAVE_FOLD_20260911.md | finding | 2026-09-11 | 0+5/1 | 11962 | KEEP
GSTD_FORENSICS_20260918.md | receipt | 2026-09-18 | 2+8/1 | 3993 | KEEP
HANDOFF_20260901_OVERNIGHT.md | brief | 2026-09-01 | 0+7/1 | 7084 | KEEP
HANDOFF_20260927_SESSION_CLOSE.md | brief | 2026-09-27 | 0+5/1 | 4512 | KEEP
HANDOFF_CANVAS_PINK_20260921.md | brief | 2026-09-21 | 0+4/1 | 3073 | KEEP
HANDOFF_GOODNIGHT_20260917.md | brief | 2026-09-17 | 1+5/1 | 4140 | KEEP
HARD_JOB_QUEUE_20260920.md | finding | 2026-09-20 | 0+3/1 | 2800 | KEEP
HARVEST_MOON_RACTOR_PANEL_20260927.md | other | 2026-09-27 | 0+4/1 | 3534 | REVIEW
HEAD_MUSEUM_FOLD_20260912.md | finding | 2026-09-12 | 0+4/1 | 3567 | KEEP
HEAD_MUSEUM_PLAN_20260912.md | receipt | 2026-09-12 | 0+4/1 | 5719 | KEEP
HELPWANTED_A_VERDICT_20260926.md | finding | 2026-09-26 | 0+5/1 | 1939 | KEEP
HELPWANTED_B_VERDICT_20260926.md | finding | 2026-09-26 | 0+5/1 | 2795 | KEEP
HELPWANTED_C_VERDICT_20260926.md | finding | 2026-09-26 | 2+6/1 | 1741 | KEEP
HERMES_100_SPEND_PLAN_20260917.md | receipt | 2026-09-17 | 0+4/1 | 3962 | KEEP
HERMES_AGENT_STEAL_20260923.md | finding | 2026-09-23 | 0+4/1 | 4518 | KEEP
HERMES_DIRECTIVE_BONES_REFEREE_20260916.md | receipt | 2026-09-16 | 3+6/1 | 3121 | KEEP
HERMES_DIRECTIVE_INDEX_FOLDBACK_20260916.md | finding | 2026-09-16 | 0+5/1 | 6255 | KEEP
HERMES_DISCORD_SETUP_20260915.md | receipt | 2026-09-15 | 1+7/1 | 3950 | KEEP
HERMES_LANE_DEBT_20260907.md | receipt | 2026-09-07 | 0+6/1 | 4258 | KEEP
HERMES_PERSONALITY_STEAL_20260907.md | finding | 2026-09-07 | 0+5/1 | 2588 | KEEP
HERMES_PLUGIN_CATALOG_AUDIT_20260916.md | receipt | 2026-09-16 | 0+4/1 | 6484 | KEEP
HERMES_STEERING_20260907.md | receipt | 2026-09-07 | 0+6/1 | 3248 | KEEP
HERMES_SURFACE_SELF_STEAL_20260912.md | finding | 2026-09-12 | 0+4/1 | 4106 | KEEP
HERMES_ZOO_CENSUS_20260912.md | finding | 2026-09-12 | 0+4/1 | 4524 | KEEP
HERO_SIMULATION_20260906.md | receipt | 2026-09-06 | 0+4/1 | 3180 | KEEP
HOLLOW_MASS_BODIES_20260911.md | other | 2026-09-11 | 0+6/1 | 6424 | REVIEW
HOME_API_FIX_20260906.md | finding | 2026-09-06 | 0+7/1 | 4094 | KEEP
HONEST_START_20260916.md | receipt | 2026-09-16 | 0+3/1 | 2168 | KEEP
HOT_LATTICE_TO_ENGRAM_20260911.md | receipt | 2026-09-11 | 1+5/1 | 7342 | KEEP
HOUSE_IN_ORDER_AUDIT_TRIANGULATION_20260912.md | brief | 2026-09-12 | 0+5/1 | 2959 | KEEP
INCIDENT_DUNGEON_20260907.md | receipt | 2026-09-07 | 0+4/1 | 3353 | KEEP
INDEX.md | receipt | 2026-09-14 | 0+0/1 | 3175 | KEEP
INTAKE_33KV_SUBSTATION_20260907.md | receipt | 2026-09-07 | 0+6/1 | 2117 | KEEP
INTAKE_CORRELATIVE_UNIVERSE_20260907.md | receipt | 2026-09-07 | 0+4/1 | 5557 | KEEP
INTAKE_DISSOLVE_20260907.md | receipt | 2026-09-07 | 0+7/1 | 2290 | KEEP
INTAKE_HARDBURN_SILICON_20260913.md | receipt | 2026-09-13 | 0+4/1 | 1543 | KEEP
INTAKE_HAUL11_20260907.md | receipt | 2026-09-07 | 1+5/1 | 21955 | KEEP
INTAKE_KANERVA_SDM_20260913.md | finding | 2026-09-13 | 0+4/1 | 2500 | KEEP
INTAKE_LEDGER_OF_EMPTY_CHAIRS_20260908.md | receipt | 2026-09-08 | 0+7/1 | 3053 | KEEP
INTAKE_LONGER_THAN_LIGHT_20260907.md | receipt | 2026-09-07 | 0+7/1 | 3180 | KEEP
INTAKE_MARIGOLD_V2_20260913.md | receipt | 2026-09-13 | 0+4/1 | 2154 | KEEP
INTAKE_MAZE_20260907.md | receipt | 2026-09-07 | 0+7/1 | 2191 | KEEP
INTAKE_NAMES_THE_STARS_FORGET_20260907.md | receipt | 2026-09-07 | 0+6/1 | 2501 | KEEP
INTAKE_ONE_TWEET_SWARM_20260913.md | receipt | 2026-09-13 | 0+4/1 | 2147 | KEEP
INTAKE_RAINY_AUTUMN_20260907.md | receipt | 2026-09-07 | 0+7/1 | 4024 | KEEP
INTAKE_SECRET_TEACHINGS_ABBOTTABAD_20260907.md | finding | 2026-09-07 | 0+6/1 | 2729 | KEEP
INTAKE_STILL_ON_MY_FEET_20260907.md | receipt | 2026-09-07 | 0+6/1 | 2159 | KEEP
INTAKE_THE_KILLING_GAME_20260907.md | receipt | 2026-09-07 | 0+8/1 | 2401 | KEEP
INTAKE_XBATCH_20260912.md | receipt | 2026-09-12 | 1+5/1 | 29125 | KEEP
INTAKE_YIP_MAN_SIU_NIM_TAU_20260907.md | receipt | 2026-09-07 | 0+6/1 | 2364 | KEEP
INTERAGENCY_AOS_PACK_20260921.md | receipt | 2026-09-21 | 0+4/1 | 3746 | KEEP
INTERFERENCE_PREREG_ADVERSARIAL_GROK47_20260925.md | receipt | 2026-09-25 | 0+4/1 | 5361 | KEEP
INTERFERENCE_REPLICATION_PREREG_20260925.md | receipt | 2026-09-25 | 1+4/1 | 3360 | KEEP
INTERFERENCE_REPLICATION_PREREG_AMENDMENT1_20260925.md | receipt | 2026-09-25 | 0+4/1 | 1753 | KEEP
INTERPRETER_LAYER_20260918.md | finding | 2026-09-18 | 0+7/1 | 3675 | KEEP
INVARIANTS_SHRINK_FORENSICS_20260906.md | receipt | 2026-09-06 | 2+7/1 | 8280 | KEEP
JEV_CHORD_FORMALIZED_20260919.md | receipt | 2026-09-19 | 0+7/1 | 3605 | KEEP
JEV_CONSOLIDATED_BRIEF_20260919.md | brief | 2026-09-19 | 0+6/1 | 8394 | KEEP
JEV_DROPS_20260919_EVENING.md | receipt | 2026-09-19 | 0+4/1 | 4185 | KEEP
K8S3D_RACK_FIND_20260911.md | finding | 2026-09-11 | 0+3/1 | 2569 | KEEP
KEEPER_VOICE_20260907.md | receipt | 2026-09-07 | 0+4/1 | 3185 | KEEP
KEV_STEAL_MATERIALIZED_20260921.md | finding | 2026-09-21 | 0+4/1 | 2785 | KEEP
KEY_LAW_20260923.md | law | 2026-09-23 | 0+4/1 | 36552 | KEEP
KG_PDFS_RECEIPT_20260901.md | receipt | 2026-09-01 | 1+7/1 | 5698 | KEEP
KG_SOURCES_20260901.md | finding | 2026-09-01 | 1+7/1 | 11328 | KEEP
KG_SOURCES_20260901_src/Claude-Fable-5.1_RAW_system_prompt.md | brief | 2026-09-14 | 0+5/0 | 275723 | ARCHIVE
KG_SYNTHESIS_20260901.md | receipt | 2026-09-01 | 0+7/1 | 3117 | KEEP
KIFU_HIDDEN_KINGS_20260911.md | receipt | 2026-09-11 | 0+5/1 | 3701 | KEEP
KOOK_INQUISITOR_DISSOLUTION_20260928.md | receipt | 2026-09-28 | 0+3/0 | 902 | ARCHIVE
KPI_LEAVES_RECON_20260911.md | receipt | 2026-09-11 | 0+4/1 | 7702 | KEEP
KPI_LEDGER_DECODE_20260911.md | finding | 2026-09-11 | 0+4/1 | 12591 | KEEP
KV_CACHE_AS_OS_SELF_STEAL_20260922.md | finding | 2026-09-22 | 0+4/1 | 4468 | KEEP
LAMBDA_PROTOCOL_20260922.md | receipt | 2026-09-22 | 0+4/1 | 7116 | KEEP
LANE19_SEAL_HOOK_TEST_20260922.md | other | 2026-09-22 | 0+4/1 | 556 | REVIEW
LANE_COLLAB_SYNTHESIS_20260921.md | finding | 2026-09-21 | 0+4/1 | 6494 | KEEP
LANE_TRIAL_GLM_VS_DEEPSEEK_20260921.md | receipt | 2026-09-21 | 0+4/1 | 2006 | KEEP
LAW066_DELTA_LEDGER_WITNESS3_20260907.md | law | 2026-09-07 | 0+6/1 | 4761 | KEEP
LAW13_EXPERIMENT_ON_ABSENCE_20260926.md | law | 2026-09-26 | 0+8/1 | 1875 | KEEP
LAW_064_065_INSTRUMENTS_20260907.md | law | 2026-09-07 | 0+5/1 | 6889 | KEEP
LAW_CAND_066_VERDICT_CITATION_20260907.md | law | 2026-09-07 | 0+6/1 | 1447 | KEEP
LEASH_CUT_WAVES_20260912.md | receipt | 2026-09-12 | 0+4/1 | 2253 | KEEP
LIBRARIAN_RETIRED_20260927.md | finding | 2026-09-27 | 0+4/1 | 2067 | KEEP
LIFE_OF_SAINT_ANTONY_20260915.md | other | 2026-09-15 | 0+6/1 | 7675 | REVIEW
LIGHT_MAZE_3D_WALK_20260922.md | finding | 2026-09-22 | 0+4/1 | 3448 | KEEP
LILITH_ACTUATORS_THREE_RECRUITS_20260912.md | receipt | 2026-09-12 | 0+5/1 | 5444 | KEEP
LILITH_THREAD_TAPIN_20260914.md | finding | 2026-09-14 | 0+4/1 | 3136 | KEEP
LING_LOCAL_DEPLOY_FOLD_20260913.md | finding | 2026-09-13 | 0+5/1 | 3369 | KEEP
LITE_LANE_FLYWHEEL_DOCTRINE_20260926.md | receipt | 2026-09-26 | 0+6/1 | 4979 | KEEP
LITE_REARM_RUNBOOK_20260905.md | receipt | 2026-09-05 | 0+7/1 | 7641 | KEEP
LITE_WAVE_ARMING_20260911.md | finding | 2026-09-11 | 0+3/1 | 2172 | KEEP
LIVINGMUD_V11_CARTOGRAPHY_20260923.md | receipt | 2026-09-23 | 0+3/1 | 4043 | KEEP
LIVING_CIPHER_20260914.md | finding | 2026-09-14 | 0+5/1 | 5498 | KEEP
LIVING_HASH_LAW_20260926.md | law | 2026-09-26 | 6+5/1 | 6293 | KEEP
LOCKWOOD_IMPORT_BARON_TRUMP_20260920.md | receipt | 2026-09-20 | 0+3/1 | 3884 | KEEP
LOGS_DEEP_CENSUS_20260911.md | finding | 2026-09-11 | 0+4/1 | 11310 | KEEP
LOOKING_GLASS_LENS_20260917.md | finding | 2026-09-17 | 0+5/1 | 4142 | KEEP
LOOM3_WAVE_FOLD_20260912.md | finding | 2026-09-12 | 0+5/1 | 8061 | KEEP
LOOM_WAVE_FOLD_20260912.md | finding | 2026-09-12 | 0+5/1 | 8770 | KEEP
LOOPED_FLOWS_GODEL_20260912.md | receipt | 2026-09-12 | 0+4/1 | 2841 | KEEP
LYAPUNOV_DIMENSION_LIFT_DECODE_20260921.md | finding | 2026-09-21 | 0+5/1 | 5204 | KEEP
M2_MINING_AND_DATA_FIXES_20260907.md | finding | 2026-09-07 | 0+4/1 | 7577 | KEEP
MAGDISK_SNAPSHOT_MAP_20260911.md | finding | 2026-09-11 | 0+3/1 | 5736 | KEEP
MAIN_SESSION_DEATH_20260901.md | receipt | 2026-09-01 | 0+8/1 | 3780 | KEEP
MARATHON_BODY_HUNT_20260911.md | receipt | 2026-09-11 | 0+3/1 | 5494 | KEEP
MARATHON_HARVEST_20260906.md | receipt | 2026-09-06 | 0+5/1 | 7431 | KEEP
MATH_FORGETTING_STEAL_20260927.md | finding | 2026-09-27 | 0+4/1 | 3061 | KEEP
MATTHEWS_LENS.md | finding | 2026-09-14 | 2+4/1 | 4965 | KEEP
MATTHEWS_VECTOR_FRAMEWORK_MINE_20260914.md | receipt | 2026-09-14 | 0+4/1 | 6042 | KEEP
MATTHEW_CIO_BRIEF_20260918.md | brief | 2026-09-18 | 1+5/1 | 8240 | KEEP
MATTHEW_LAST_CORRESPONDENCE_20260918.md | receipt | 2026-09-18 | 0+7/1 | 5614 | KEEP
MAX_DISTILL_EPOCH2_SPEC_20260911.md | receipt | 2026-09-11 | 0+6/1 | 9958 | KEEP
MAZE_ARENA_B1_20260906.md | receipt | 2026-09-06 | 0+7/1 | 3186 | KEEP
MD_RECORD_STEAL_MAP_20260921.md | finding | 2026-09-21 | 0+4/1 | 3048 | KEEP
MECHA_STALIN_20260914.md | finding | 2026-09-14 | 0+4/1 | 2183 | KEEP
MELEE_DECOMP_ASSESS_20260911.md | receipt | 2026-09-11 | 0+4/1 | 1609 | KEEP
MEM1_ANATOMY_20260911.md | receipt | 2026-09-11 | 0+3/1 | 15179 | KEEP
MEMORY_REVAMP_BLUEPRINT_20260923.md | brief | 2026-09-23 | 0+4/1 | 3907 | KEEP
MESH_ARCHAEOLOGY_20260911.md | finding | 2026-09-11 | 0+3/1 | 6617 | KEEP
METERS_LANDED_20260922.md | receipt | 2026-09-22 | 0+4/1 | 2595 | KEEP
METRIC_REFERENT_TRIANGULATION_20260918.md | finding | 2026-09-18 | 1+5/1 | 16331 | KEEP
MICKEY17_V2_ENGINE_SPEC_20260924.md | receipt | 2026-09-24 | 0+4/1 | 17458 | KEEP
MICKEY17_V2_ENGINE_SPEC_v2.1_20260925.md | receipt | 2026-09-25 | 0+4/1 | 15069 | KEEP
MICKEY17_V2_RUN_SPEC_ADDENDUM.md | receipt | 2026-09-25 | 0+5/1 | 23685 | KEEP
MICKEY17_WAVE2_QUALITY_20260925.md | receipt | 2026-09-25 | 2+4/1 | 102446 | KEEP
MICKEY17_WAVE_OWED_20260925.md | receipt | 2026-09-25 | 0+4/1 | 9014 | KEEP
MIDDLE_PATH_SALON_20260925.md | receipt | 2026-09-25 | 0+6/1 | 11931 | KEEP
MIGRATION_CLEANUP_20260919.md | finding | 2026-09-19 | 0+4/1 | 5072 | KEEP
MILO_STEAL_20260927.md | finding | 2026-09-27 | 0+3/1 | 3447 | KEEP
MIMOSA_ROSETTA_20260921.md | receipt | 2026-09-21 | 0+4/1 | 2838 | KEEP
MIMOSA_SCAN_20260925.md | receipt | 2026-09-25 | 0+4/1 | 9352 | KEEP
MIMO_FREE_WINDOW_20260922.md | finding | 2026-09-22 | 1+4/1 | 1926 | KEEP
MINT_DOSSIER_20260911.md | receipt | 2026-09-11 | 0+6/1 | 12983 | KEEP
MINT_EXECUTION_20260912.md | receipt | 2026-09-12 | 0+4/1 | 7978 | KEEP
MISSED_NUANCE_FOLD_20260913.md | finding | 2026-09-13 | 0+4/1 | 3561 | KEEP
MODEL_MATRIX_20260923.md | receipt | 2026-09-23 | 1+4/1 | 2034 | KEEP
MODEL_RIB_LIBRARY_DESIGN_2026-08-31.md | law | 2026-08-31 | 0+6/1 | 7570 | KEEP
MOONSHOT_RIGHT_TIME_20260901.md | receipt | 2026-09-01 | 0+13/1 | 4189 | KEEP
MOUNTAIN_CLIMB_20B_FOLD_20260912.md | finding | 2026-09-12 | 0+5/1 | 3901 | KEEP
MOVE1_ARTIFACT_DRAFT_20260920.md | receipt | 2026-09-20 | 0+5/1 | 4155 | KEEP
MOZART_FETCHED_YUE2_20260912.md | receipt | 2026-09-12 | 0+5/1 | 3016 | KEEP
MUD_ENGINE_STEAL_MAP_20260923.md | finding | 2026-09-23 | 0+4/1 | 2324 | KEEP
MUSE_SPARK_ACCESS_20260928.md | receipt | 2026-09-28 | 0+1/0 | 2844 | ARCHIVE
NAV_REVERIFY_20260911.md | receipt | 2026-09-11 | 0+7/1 | 6469 | KEEP
NAV_WIRING_20260906.md | receipt | 2026-09-06 | 0+7/1 | 1993 | KEEP
NIGHT_AUDIT_20260916.md | receipt | 2026-09-16 | 0+6/1 | 10784 | KEEP
NIGHT_BOOT_AUDIT_20260911.md | finding | 2026-09-11 | 0+3/1 | 8191 | KEEP
NIGHT_EXTERNAL_CONNECTOME_20260911.md | receipt | 2026-09-11 | 1+3/1 | 8425 | KEEP
NIGHT_EXTERNAL_EVAL_20260911.md | receipt | 2026-09-11 | 1+6/1 | 16234 | KEEP
NIGHT_EXTERNAL_MEMORY_20260911.md | brief | 2026-09-11 | 2+6/1 | 10928 | KEEP
NIGHT_EXTERNAL_SWARMS_20260911.md | receipt | 2026-09-11 | 0+4/1 | 16105 | KEEP
NIGHT_FOLD_20260918.md | finding | 2026-09-18 | 1+5/1 | 4819 | KEEP
NIGHT_HIDDEN_POOLS_20260911.md | receipt | 2026-09-11 | 0+4/1 | 7486 | KEEP
NIGHT_LAWS_AUDIT_20260911.md | law | 2026-09-11 | 0+4/1 | 10367 | KEEP
NIGHT_MEMORY_AUDIT_20260911.md | brief | 2026-09-11 | 0+4/1 | 6925 | KEEP
NINE_CHAPTERS_PULL_20260907.md | receipt | 2026-09-07 | 0+5/1 | 3977 | KEEP
NO_SACRED_COWS_20260927.md | receipt | 2026-09-27 | 0+4/1 | 3067 | KEEP
NPC_RACTOR_ARCHITECTURE_20260917.md | receipt | 2026-09-17 | 0+5/1 | 5973 | KEEP
OBSERVER_ANATOMY_ATLAS_20260911.md | finding | 2026-09-11 | 0+9/1 | 12338 | KEEP
OBSTACLE_WAVE_FOLD_20260913.md | finding | 2026-09-13 | 1+4/1 | 5437 | KEEP
OFFLOAD_WAVE_FOLD_20260911.md | finding | 2026-09-11 | 1+7/1 | 6948 | KEEP
OLLAMA_LOGPROBS_PROBE_20260907.md | finding | 2026-09-07 | 2+5/1 | 5920 | KEEP
ONE_WAY_MIRROR_RSVP_20260922.md | receipt | 2026-09-22 | 0+5/1 | 5340 | KEEP
OPENCLAW_ARCHAEOLOGY_20260907.md | receipt | 2026-09-07 | 0+5/1 | 16536 | KEEP
OPENCLAW_POLICY_HANDSHAKE_20260927.md | receipt | 2026-09-27 | 0+2/0 | 5042 | ARCHIVE
OPENJEV_AB_PROTOCOL_20260925.md | receipt | 2026-09-25 | 0+8/1 | 11251 | KEEP
OPERATOR_ASK_20260916.md | brief | 2026-09-16 | 0+8/1 | 2972 | KEEP
OPERATOR_CANON_TRIAGE_20260920.md | receipt | 2026-09-20 | 0+4/1 | 6029 | KEEP
OPERATOR_GENESIS_STEERING_20260927.md | receipt | 2026-09-27 | 0+3/1 | 3494 | KEEP
OPERATOR_JOURNAL_20260920.md | receipt | 2026-09-20 | 1+3/1 | 1956 | KEEP
OPERATOR_PROOF_OF_WORK_20260922.md | receipt | 2026-09-22 | 0+4/1 | 5152 | KEEP
ORCHESTRATOR_SEEDS_20260911.md | other | 2026-09-11 | 0+6/1 | 8229 | REVIEW
ORGAN_TABLE_20260925.md | receipt | 2026-09-25 | 0+4/1 | 11000 | KEEP
ORPHANS_ASTRA_FIFTH_CHAIR_20260906.md | receipt | 2026-09-06 | 0+6/1 | 3482 | KEEP
ORPHAN_CLEARING_FOLD_20260913.md | finding | 2026-09-13 | 0+4/1 | 3398 | KEEP
ORPHAN_RACTOR_PANEL_20260918.md | receipt | 2026-09-18 | 1+7/1 | 2167 | KEEP
ORPHAN_SWEEP_FOLD_20260913.md | finding | 2026-09-13 | 0+4/1 | 3283 | KEEP
OUTBOUND_MD_FRIENDSHIP_FILE_20260921.md | receipt | 2026-09-21 | 0+4/1 | 8246 | KEEP
P0_3_1_WRITER_WARM_FACE_RECEIPT_20260926.md | receipt | 2026-09-26 | 0+3/1 | 6066 | KEEP
P0_5_2_4_SEED_CHORD_CONDUCTOR_RECEIPT_20260926.md | receipt | 2026-09-26 | 0+6/1 | 5518 | KEEP
P20B_MISSING_ORGANS_FOLD_20260912.md | finding | 2026-09-12 | 0+4/1 | 3270 | KEEP
P20_PENDING_WAVE_FOLD_20260912.md | finding | 2026-09-12 | 0+4/1 | 5531 | KEEP
PACK_RETENTION_LAW_20260926.md | law | 2026-09-26 | 0+4/1 | 5971 | KEEP
PACK_SECRET_GATE_20260926.md | receipt | 2026-09-26 | 3+3/1 | 9479 | KEEP
PARABLE_ARC_SYNTHESIS_20260916.md | receipt | 2026-09-16 | 0+6/1 | 5744 | KEEP
PATHS_ON_MAP_20260907.md | finding | 2026-09-07 | 1+4/1 | 2799 | KEEP
PERSISTENT_WORLD_TIE_TOGETHER_20260913.md | finding | 2026-09-13 | 0+4/1 | 4228 | KEEP
PERSISTENT_WORLD_V0_LIVE_20260914.md | other | 2026-09-14 | 0+3/1 | 1765 | REVIEW
PERSONA_CONDITIONING_PROGRAM_20260907.md | finding | 2026-09-07 | 0+5/1 | 4971 | KEEP
PERSONA_CONDITIONING_SHARE_RAW_20260907.md | receipt | 2026-09-07 | 0+7/1 | 37175 | KEEP
PERTURBATION_BATTERY_20260906.md | receipt | 2026-09-06 | 0+6/1 | 5445 | KEEP
PHONE_RELAY_20260924.md | receipt | 2026-09-24 | 0+4/1 | 3323 | KEEP
PHOSPHOR_ASSANGE_20260918.md | finding | 2026-09-18 | 0+9/1 | 4532 | KEEP
PHOSPHOR_DECODE_V2_20260919.md | finding | 2026-09-19 | 0+6/1 | 2585 | KEEP
PHOSPHOR_SALON_20260919.md | receipt | 2026-09-19 | 0+7/1 | 2128 | KEEP
PHOSPHOR_SALON_FOLD_20260919.md | finding | 2026-09-19 | 0+8/1 | 4065 | KEEP
PHOTON_FAST_SEARCH_STEAL_20260924.md | finding | 2026-09-24 | 0+4/1 | 3989 | KEEP
PHOTON_ROT_20260925.md | receipt | 2026-09-25 | 1+4/1 | 14977 | KEEP
PICASSO_DELETION_DROP_20260926.md | receipt | 2026-09-26 | 0+5/1 | 3190 | KEEP
PICASSO_STATE_XI_V2_20260926.md | receipt | 2026-09-26 | 0+5/1 | 6155 | KEEP
PIPELINE_RIGHT_PLAN_20260907.md | receipt | 2026-09-07 | 0+6/1 | 16295 | KEEP
PLAIN_LANGUAGE_FOR_AOS_20260924.md | receipt | 2026-09-24 | 1+6/1 | 9044 | KEEP
PLAN_KV50_LIFT_20260922.md | receipt | 2026-09-22 | 0+4/1 | 1234 | KEEP
PLUGIN_EVAL_STEAL_20260912.md | finding | 2026-09-12 | 0+4/1 | 4142 | KEEP
POINTER_INDEX_REPORT_20260911.md | receipt | 2026-09-11 | 0+4/1 | 5301 | KEEP
PORT_FORWARDING_ESTATE_20260923.md | finding | 2026-09-23 | 0+4/1 | 2847 | KEEP
PRATCHETT_MUD_SELF_STEAL_20260918.md | finding | 2026-09-18 | 0+6/1 | 4555 | KEEP
PRELOAD_SELECTOR_FW5_20260907.md | receipt | 2026-09-07 | 0+7/1 | 5490 | KEEP
PREMAP_ARCHAEOLOGY_20260911.md | finding | 2026-09-11 | 0+4/1 | 8453 | KEEP
PREPAREDNESS_AUDIT_20260927.md | receipt | 2026-09-27 | 0+3/1 | 4054 | KEEP
PRIMER_ROUND_20260911.md | receipt | 2026-09-11 | 0+5/1 | 5042 | KEEP
PROVIDER_HEALTH_20260926.md | finding | 2026-09-26 | 2+9/1 | 6229 | KEEP
PROWL_STEAL_20260925.md | finding | 2026-09-25 | 0+5/1 | 2712 | KEEP
PUBLIC_HALF_MAP_20260911.md | finding | 2026-09-11 | 0+3/1 | 11959 | KEEP
PURGE_LIST_MERGED_20260927.md | finding | 2026-09-27 | 0+2/1 | 2662 | KEEP
QUANTIZER_V03_20260927.md | finding | 2026-09-27 | 2+2/1 | 3441 | KEEP
QUEUE_CLOSE_VERB_20260927.md | receipt | 2026-09-27 | 0+4/1 | 2405 | KEEP
QUIET_RADAR_20260921.md | receipt | 2026-09-21 | 0+6/1 | 31288 | KEEP
QUOTE_AUDIT_WIDE_20260925.md | receipt | 2026-09-25 | 1+5/1 | 8532 | KEEP
Q_BRIEF_v1_20260907.md | brief | 2026-09-07 | 0+5/1 | 2829 | KEEP
Q_FIRST_DIALOGUE_20260907.md | receipt | 2026-09-07 | 0+5/1 | 2239 | KEEP
RACTORS_ASTRA_V2_20260911.md | receipt | 2026-09-11 | 0+5/1 | 6017 | KEEP
RACTOR_ENGINE_SPEC_v0_1.md | receipt | 2026-09-16 | 0+9/1 | 32168 | KEEP
RACTOR_PANEL_20260926.md | receipt | 2026-09-26 | 0+7/1 | 19178 | KEEP
RACTOR_PANEL_SPEC_20260926.md | receipt | 2026-09-26 | 0+4/1 | 5287 | KEEP
RACTOR_PREWARMED_RIB_SPEC_20260920.md | law | 2026-09-20 | 0+4/1 | 5348 | KEEP
RACTOR_SALON_20260916.md | receipt | 2026-09-16 | 0+7/1 | 5549 | KEEP
RACTOR_SALON_ASTRA_ASK_20260916.md | brief | 2026-09-16 | 0+5/1 | 6464 | KEEP
RACTOR_STEERING_SURFACE_20260922.md | receipt | 2026-09-22 | 0+4/1 | 4731 | KEEP
RACTOR_VERDICT_SHARE_CORPUS_20260923.md | receipt | 2026-09-23 | 0+4/1 | 2249 | KEEP
RASHOMON_SURFACE_ELEPHANT_20260914.md | other | 2026-09-14 | 3+6/1 | 7764 | REVIEW
REAL_PROCESS_MAZE_20260913.md | receipt | 2026-09-13 | 0+4/1 | 3730 | KEEP
RECAP_48HR_CHORD_20260917.md | receipt | 2026-09-17 | 0+5/1 | 5599 | KEEP
RECAP_7D_20260926.md | receipt | 2026-09-26 | 1+7/1 | 3755 | KEEP
RECEIPT_BODY_FTS_20260927.md | receipt | 2026-09-27 | 0+3/1 | 2035 | KEEP
RECEIPT_MUD_FIFTY_WIDE_PLAYTEST_20260914.md | receipt | 2026-09-14 | 0+5/1 | 3629 | KEEP
RECORD_POOL_CENSUS_20260911.md | finding | 2026-09-11 | 0+5/1 | 6448 | KEEP
REDO_SWEEP_20260927.md | receipt | 2026-09-27 | 0+5/1 | 3095 | KEEP
REFEED_GUARD_B1_20260905.md | receipt | 2026-09-05 | 0+8/1 | 4327 | KEEP
REFEREE_VERDICT_20260926.md | receipt | 2026-09-26 | 2+11/1 | 5690 | KEEP
REFRACTION_OCCULT_SALON_20260925.md | receipt | 2026-09-25 | 6+5/1 | 10144 | KEEP
REFRACTION_ORGAN_20260918.md | receipt | 2026-09-18 | 0+5/1 | 3215 | KEEP
REGISTRY_AUTOHEAL_20260906.md | receipt | 2026-09-06 | 0+7/1 | 5286 | KEEP
REHOME_20260907.md | receipt | 2026-09-07 | 0+6/1 | 5180 | KEEP
REJECTION_TAXONOMY_20260917.md | receipt | 2026-09-17 | 0+7/1 | 3912 | KEEP
RENDER_THE_SYSTEM_VISION_20260922.md | receipt | 2026-09-22 | 0+4/1 | 14816 | KEEP
REPLUNA_RACTOR_20260916.md | receipt | 2026-09-16 | 0+6/1 | 17001 | KEEP
REPORT_CAP_CRASH_SPECIES_20260927.md | finding | 2026-09-27 | 0+4/1 | 2184 | KEEP
RESEARCH_COMMISSION_SELFANSWERS_20260907.md | finding | 2026-09-07 | 0+6/1 | 5819 | KEEP
RESEARCH_COMMISSION_WORLDLINE_INTROSPECTION_20260907.md | finding | 2026-09-07 | 0+5/1 | 11490 | KEEP
RESEARCH_GAPS_AS_SENSORS_NAVIER_STOKES_20260913.md | finding | 2026-09-13 | 0+4/1 | 7014 | KEEP
RESEARCH_GAP_ANALYSIS_20260918.md | finding | 2026-09-18 | 0+8/1 | 5279 | KEEP
RESEARCH_WAVE_20260910.md | finding | 2026-09-10 | 1+4/1 | 14176 | KEEP
RESET_EVIDENCE_SPEC_20260923.md | receipt | 2026-09-23 | 1+4/1 | 73867 | KEEP
RESOLUTION_J1_CAGE_TO_MAG_ROUTE_20260901.md | other | 2026-09-01 | 0+8/1 | 2668 | REVIEW
RESONANCE_INTAKE_20260913.md | receipt | 2026-09-13 | 0+4/1 | 3846 | KEEP
RESTART_FLIP_RECEIPT_20260912.md | receipt | 2026-09-12 | 0+4/1 | 1934 | KEEP
RESTFUL_WATCH_059_20260906.md | law | 2026-09-06 | 0+6/1 | 3213 | KEEP
RESUME_20260919_UPDATE_RECOVERY.md | receipt | 2026-09-19 | 0+4/1 | 4654 | KEEP
RETROKNOTTER_PREP_20260911.md | receipt | 2026-09-11 | 0+5/1 | 13072 | KEEP
REVEAL_FIVE_REHEARSALS_20260906.md | receipt | 2026-09-06 | 1+28/1 | 15489 | KEEP
RE_LADDER_PILLARS_20260923.md | receipt | 2026-09-23 | 0+3/1 | 4003 | KEEP
RE_LADDER_READY_20260924.md | receipt | 2026-09-24 | 0+4/1 | 2201 | KEEP
RIBV_LENS_STACK_SALON_20260922.md | law | 2026-09-22 | 0+5/1 | 10553 | KEEP
RIB_BUS_RESURRECTION_20260911.md | law | 2026-09-11 | 0+3/1 | 11270 | KEEP
RIB_LANGUAGE_CACHE_OS_20260919.md | law | 2026-09-19 | 0+5/1 | 15093 | KEEP
RIDDLE_TRIAD_CADENCE_20260918.md | finding | 2026-09-18 | 1+7/1 | 3095 | KEEP
RIDE_FAMILY_VERDICTS_20260922.md | receipt | 2026-09-22 | 0+5/1 | 5463 | KEEP
RND_AGENDA1_VERKLE_BAIL_20260901.md | finding | 2026-09-01 | 0+9/1 | 8118 | KEEP
RND_AGENDA2_MODELDIFF_20260901.md | receipt | 2026-09-01 | 0+8/1 | 6135 | KEEP
RND_AGENDA3_EDITPATH_20260901.md | receipt | 2026-09-01 | 0+7/1 | 7799 | KEEP
ROBLOX_DEV_TUTORIALS_20260924.md | finding | 2026-09-24 | 1+4/1 | 5699 | KEEP
ROBLOX_MARKETING_PLAYBOOK_20260924.md | finding | 2026-09-24 | 1+3/1 | 6487 | KEEP
ROBLOX_MONETIZATION_PLAN_20260924.md | finding | 2026-09-24 | 0+4/1 | 6414 | KEEP
ROBLOX_SEASONAL_HALLOWEEN_20260924.md | receipt | 2026-09-24 | 1+3/1 | 5520 | KEEP
ROBLOX_WHO_IS_DOING_WHAT_20260924.md | finding | 2026-09-24 | 1+3/1 | 6256 | KEEP
ROLLBACK_WATCH.md | receipt | 2026-09-16 | 0+4/1 | 5250 | KEEP
ROOM_GAME_FAREWELL_20260907.md | receipt | 2026-09-07 | 0+6/1 | 1492 | KEEP
ROPE_AND_LOOM_20260912.md | receipt | 2026-09-12 | 0+5/1 | 2457 | KEEP
SACRED_COW_AUDIT_20260919.md | receipt | 2026-09-19 | 0+6/1 | 1867 | KEEP
SACRED_COW_AUDIT_SEP20_20260918.md | receipt | 2026-09-18 | 0+5/1 | 4129 | KEEP
SALON2_BRIEF_20260919.md | brief | 2026-09-19 | 0+4/1 | 10288 | KEEP
SALON3_FILING_20260901.md | receipt | 2026-09-01 | 1+7/1 | 6943 | KEEP
SALON_AUDIT_FOLD_20260908.md | finding | 2026-09-08 | 1+4/1 | 4726 | KEEP
SALON_CHAIRS_THE_LOOP_20260911.md | receipt | 2026-09-11 | 0+8/1 | 9388 | KEEP
SALON_CONCURRENCY_CHAIR4_ASTRA_20260906.md | receipt | 2026-09-06 | 0+6/1 | 4604 | KEEP
SALON_FOLD_THE_LOOP_20260911.md | finding | 2026-09-11 | 0+5/1 | 12950 | KEEP
SALON_LIGHTMAP_B2_20260906.md | finding | 2026-09-06 | 0+6/1 | 2995 | KEEP
SALON_PROMPT_MANUAL_20260920.md | brief | 2026-09-20 | 1+4/1 | 7711 | KEEP
SALON_REINGEST_T1A_20260911.md | receipt | 2026-09-11 | 0+7/1 | 12973 | KEEP
SALON_REINGEST_TIERA_20260911.md | receipt | 2026-09-11 | 0+3/1 | 12994 | KEEP
SALON_SOCRATIC_SYNTHESIS_20260908.md | finding | 2026-09-08 | 0+6/1 | 27058 | KEEP
SALON_SUPERINTELLIGENCE_STACK_RIB_20260831.md | law | 2026-08-31 | 0+8/1 | 9739 | KEEP
SANCHO_HEARTBEAT_POLL_20260901.md | receipt | 2026-09-01 | 0+8/1 | 1903 | KEEP
SANCHO_SELF_ANALYSIS_20260902.md | finding | 2026-09-02 | 0+6/1 | 4800 | KEEP
SAND_ERA_BLOBS_DECODE_20260911.md | finding | 2026-09-11 | 0+4/1 | 6778 | KEEP
SCOUT_CHARTER_20260926.md | receipt | 2026-09-26 | 0+5/1 | 2926 | KEEP
SEAL_CHECK_20260906.md | receipt | 2026-09-06 | 1+4/1 | 4349 | KEEP
SEAT_ARCHITECTURE_BRIEF_20260928.md | brief | 2026-09-28 | 0+2/1 | 4313 | KEEP
SEAT_CAPABILITIES_20260918.md | receipt | 2026-09-18 | 1+6/1 | 4393 | KEEP
SEAT_SPORes_AUDIT_CELL_20260912.md | receipt | 2026-09-12 | 0+19/1 | 4844 | KEEP
SECRET_GATE_BUILD_20260927.md | receipt | 2026-09-27 | 1+3/1 | 12736 | KEEP
SECRET_GATE_INDUSTRY_STEAL_20260927.md | finding | 2026-09-27 | 0+3/1 | 2903 | KEEP
SECRET_GATE_STEAL_ADDENDUM_20260927.md | finding | 2026-09-27 | 0+3/1 | 2255 | KEEP
SECRET_GATE_STEAL_LANDED_20260927.md | finding | 2026-09-27 | 0+3/1 | 3999 | KEEP
SECRET_SCAN_RULESET_ROTATION_20260926.md | finding | 2026-09-26 | 0+8/1 | 8624 | KEEP
SECURITY_NOTE_LMCACHE_CLONE_20260922.md | finding | 2026-09-22 | 0+4/1 | 1929 | KEEP
SEED_PUBLIC_PACK_20260925.md | receipt | 2026-09-25 | 0+8/1 | 3691 | KEEP
SEED_RIB_FORMAT_v0_20260926.md | law | 2026-09-26 | 2+5/1 | 6475 | KEEP
SEED_RIB_HANDOFF_KERNEL_20260926.md | law | 2026-09-26 | 0+5/1 | 5531 | KEEP
SEED_RIB_REFRESH_20260928.md | law | 2026-09-28 | 0+2/0 | 2489 | PROMOTE
SEED_SALON_RACTOR_RULING_20260925.md | receipt | 2026-09-25 | 0+4/1 | 3096 | KEEP
SEED_SALON_deepseek_20260925.md | receipt | 2026-09-25 | 0+4/1 | 3698 | KEEP
SEED_SALON_deepseek_20260926.md | receipt | 2026-09-26 | 0+3/1 | 3878 | KEEP
SEED_SALON_groq_20260925.md | receipt | 2026-09-25 | 0+4/1 | 4634 | KEEP
SEED_SALON_groq_20260926.md | receipt | 2026-09-26 | 0+3/1 | 4560 | KEEP
SEED_SALON_together_20260925.md | receipt | 2026-09-25 | 0+4/1 | 3317 | KEEP
SEED_SELF_STEAL_AUDIT_20260926.md | finding | 2026-09-26 | 1+4/1 | 20107 | KEEP
SEED_V2_BUILD_BOOK_20260925.md | receipt | 2026-09-25 | 2+4/1 | 27484 | KEEP
SEED_WINDOW_CLOSE_20260925.md | receipt | 2026-09-25 | 0+4/1 | 4839 | KEEP
SELF_AUDIT_ZCODE_20260918.md | receipt | 2026-09-18 | 1+7/1 | 5650 | KEEP
SELF_STEAL_20260915.md | finding | 2026-09-15 | 0+8/1 | 5101 | KEEP
SELF_STEAL_CORPUS_SKILLS_20260918.md | finding | 2026-09-18 | 0+8/1 | 4984 | KEEP
SELF_STEAL_CURVATURE_WORLDS_20260921.md | finding | 2026-09-21 | 0+4/1 | 4993 | KEEP
SELF_STEAL_DEEP_20260918.md | finding | 2026-09-18 | 1+5/1 | 5911 | KEEP
SELF_STEAL_DIRAC_MEMLANCE_20260927.md | finding | 2026-09-27 | 0+4/1 | 4105 | KEEP
SELF_STEAL_DOZEN_20260916.md | finding | 2026-09-16 | 0+9/1 | 4717 | KEEP
SELF_STEAL_KG_20260901.md | finding | 2026-09-01 | 0+19/1 | 11425 | KEEP
SELF_STEAL_PROMPT_LIBRARY_20260924.md | brief | 2026-09-24 | 0+4/1 | 7250 | KEEP
SELF_STEAL_PSEUDOSPECTRUM_20260921.md | finding | 2026-09-21 | 0+4/1 | 5262 | KEEP
SELF_STEAL_RACTOR_PANEL_20260911.md | finding | 2026-09-11 | 0+5/1 | 2992 | KEEP
SELF_STEAL_REBUILD_RETEST_SALON_20260831.md | finding | 2026-08-31 | 0+24/1 | 59621 | KEEP
SELF_STEAL_SALON_LENS_20260920.md | finding | 2026-09-20 | 0+4/1 | 5475 | KEEP
SELF_STEAL_SLASHREBOOT_20260916.md | finding | 2026-09-16 | 0+5/1 | 7739 | KEEP
SELF_STEAL_TEST_TIME_COMMUNICATION_20260921.md | finding | 2026-09-21 | 1+4/1 | 5718 | KEEP
SELF_STEAL_THREE_SHELVES_20260907.md | finding | 2026-09-07 | 0+5/1 | 6993 | KEEP
SELF_STEAL_TIMEKEEPING_20260907.md | finding | 2026-09-07 | 0+4/1 | 2642 | KEEP
SELF_STEAL_WING_CHUN_LENSES_20260917.md | finding | 2026-09-17 | 0+6/1 | 3599 | KEEP
SESSION_CLOSE_20260919.md | receipt | 2026-09-19 | 0+5/1 | 2780 | KEEP
SESSION_HANDOFF_20260926_noir_u1_gates.md | brief | 2026-09-26 | 0+5/1 | 6274 | KEEP
SESSION_ORPHANS_20260911.md | receipt | 2026-09-11 | 0+4/1 | 4027 | KEEP
SESSION_RECAP_FD5EC147_20260927.md | receipt | 2026-09-27 | 0+7/1 | 4297 | KEEP
SESSION_RECOVERY_FORGE_DAEMON_20260914.md | receipt | 2026-09-14 | 0+5/1 | 2689 | KEEP
SEVEN_LINKS_OPERATOR_CANON_20260912.md | receipt | 2026-09-12 | 0+5/1 | 4281 | KEEP
SHADOW_PHYSICS_LAB_20260906.md | receipt | 2026-09-06 | 0+6/1 | 3865 | KEEP
SHADOW_WALK_20260906.md | receipt | 2026-09-06 | 0+8/1 | 4445 | KEEP
SHADOW_WALK_V2_RUN_20260906.md | receipt | 2026-09-06 | 0+5/1 | 4162 | KEEP
SHADOW_WORK_WEIGHTS_VOLUME_20260906.md | receipt | 2026-09-06 | 0+5/1 | 4779 | KEEP
SHERPA_NEXT_US_20260914.md | receipt | 2026-09-14 | 0+6/1 | 3267 | KEEP
SHITPOST_DESK_ANTHROPIC_PRIMER_20260922.md | shitpost | 2026-09-22 | 0+4/1 | 13176 | KEEP
SHITPOST_DESK_MASSIE_20260923.md | shitpost | 2026-09-23 | 0+4/1 | 6635 | KEEP
SHITPOST_DESK_MASSIE_V2_VOLTAIRE_20260923.md | shitpost | 2026-09-23 | 0+4/1 | 3762 | KEEP
SHITPOST_DESK_MASSIE_V3_MEAN_20260923.md | shitpost | 2026-09-23 | 0+4/1 | 3181 | KEEP
SHITPOST_DESK_NVIDIA_REPLY_20260928.md | shitpost | 2026-09-28 | 0+2/1 | 1072 | KEEP
SHITPOST_DESK_RACTOR_CYCLE0_STAGED_20260924.md | shitpost | 2026-09-24 | 0+5/1 | 5306 | KEEP
SHITPOST_DESK_SANDERS_BAN_20260923.md | shitpost | 2026-09-23 | 0+4/1 | 8224 | KEEP
SHITPOST_DESK_SELF_STEAL_20260924.md | shitpost | 2026-09-24 | 0+6/1 | 6540 | KEEP
SHOUT_NATURE_SIX_LINKS_20260912.md | receipt | 2026-09-12 | 0+5/1 | 2606 | KEEP
SIGN_SHEET_20260912.md | receipt | 2026-09-12 | 0+4/1 | 1167 | KEEP
SIGN_SHEET_RESOLUTION_20260912.md | receipt | 2026-09-12 | 0+4/1 | 1906 | KEEP
SILENCE_DOSSIER_20260911.md | finding | 2026-09-11 | 0+10/1 | 13507 | KEEP
SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md | receipt | 2026-09-25 | 0+7/1 | 6015 | KEEP
SIX_LINK_SKILLS_ECONOMY_20260912.md | receipt | 2026-09-12 | 1+4/1 | 7636 | KEEP
SIX_WAVE_INTAKE_20260921.md | finding | 2026-09-21 | 0+4/1 | 801 | KEEP
SIX_WAVE_STEAL_MAP_20260921.md | finding | 2026-09-21 | 0+4/1 | 3873 | KEEP
SKILL_FORGE_20260918.md | receipt | 2026-09-18 | 1+6/1 | 2880 | KEEP
SMITH_MAP_KV50_20260922.md | finding | 2026-09-22 | 0+4/1 | 2874 | KEEP
SOCRATIC_ASKS_20260913.md | receipt | 2026-09-13 | 0+4/1 | 5332 | KEEP
SOCRATIC_GAPS_20260918.md | receipt | 2026-09-18 | 2+9/1 | 5785 | KEEP
SOCRATIC_PASS_20260919.md | receipt | 2026-09-19 | 0+8/1 | 2244 | KEEP
SOUNDTRACK_20260911.md | receipt | 2026-09-11 | 0+4/1 | 2094 | KEEP
SOVEREIGN_JUDGMENT_STACK_20260919.md | receipt | 2026-09-19 | 0+4/1 | 5199 | KEEP
SOWING_ROOM_20260906.md | receipt | 2026-09-06 | 0+6/1 | 3776 | KEEP
SPACE_BUNNY_BURN_20260924.md | receipt | 2026-09-24 | 0+5/1 | 5987 | KEEP
SPACE_CAPTURE_READY_20260916.md | receipt | 2026-09-16 | 0+3/1 | 1430 | KEEP
SPEC_EDITS_MICKEY17_V2_20260925.md | receipt | 2026-09-25 | 0+4/1 | 43511 | KEEP
SPOTCHECK_PROTOCOL_20260926.md | receipt | 2026-09-26 | 2+4/1 | 2926 | KEEP
SPOT_PATROL_LANDED_20260927.md | other | 2026-09-27 | 0+4/1 | 2106 | REVIEW
SQUARE_NAME_SELF_STEAL_20260920.md | finding | 2026-09-20 | 0+3/1 | 7344 | KEEP
STANDING_WAVE_PROTOCOL_20260918.md | receipt | 2026-09-18 | 1+5/1 | 2776 | KEEP
STARDEW_DIRECTIVE_20260913.md | finding | 2026-09-13 | 0+4/1 | 5304 | KEEP
STAYING_MOONSHOT_20260913.md | receipt | 2026-09-13 | 0+4/1 | 4807 | KEEP
STEALS_LEDGER_20260916.md | finding | 2026-09-16 | 0+5/1 | 5361 | KEEP
STEALTH_DRIVER_247_20260927.md | finding | 2026-09-27 | 0+2/1 | 2261 | KEEP
STEALTH_SWEEP_LATEST.md | finding | 2026-09-25 | 1+6/1 | 422 | KEEP
STEAL_FOLD_RESEARCH_PIPELINE_20260911.md | finding | 2026-09-11 | 1+3/1 | 10545 | KEEP
STEAL_MAPS_BYTEVERIFY_20260922.md | finding | 2026-09-22 | 0+4/1 | 7026 | KEEP
STEAL_ONESHOT_PROMPTS_20260924.md | brief | 2026-09-24 | 0+4/1 | 6573 | KEEP
STEAL_WAVE_FOLD_20260911.md | finding | 2026-09-11 | 2+7/1 | 28774 | KEEP
STEINIGER_OPERATIONAL_STEAL_20260918.md | finding | 2026-09-18 | 0+7/1 | 9951 | KEEP
STEINIGER_REVISIT_20260918.md | receipt | 2026-09-18 | 0+4/1 | 6470 | KEEP
STEREOGRAM_AUDIT_20260924.md | receipt | 2026-09-24 | 0+4/1 | 5481 | KEEP
STIGMERGY_PUBLIC_WITNESS_20260913.md | receipt | 2026-09-13 | 0+4/1 | 2694 | KEEP
STIGMERGY_WITNESS_SCAFFOLD_20260913.md | finding | 2026-09-13 | 0+3/1 | 2704 | KEEP
STONE_PROTOCOL_SELF_STEAL_20260911.md | finding | 2026-09-11 | 0+5/1 | 8148 | KEEP
STORE_DB_DECODE_20260911.md | finding | 2026-09-11 | 0+4/1 | 7275 | KEEP
STORYTELLER_SIX_RACTOR_20260925.md | receipt | 2026-09-25 | 0+6/1 | 7555 | KEEP
SUCCESSION_CONTRACT_20260912.md | receipt | 2026-09-12 | 3+4/1 | 3591 | KEEP
SUCCESSION_SLATE_20260920.md | receipt | 2026-09-20 | 0+4/1 | 3553 | KEEP
SUITE_BURNDOWN_20260927.md | receipt | 2026-09-27 | 0+3/1 | 4971 | KEEP
SUMMARY_DELIVERABLE_HOFW_20260912.md | receipt | 2026-09-12 | 0+4/1 | 1243 | KEEP
SUMMIT_DESIGN_20260924.md | receipt | 2026-09-24 | 0+4/1 | 168087 | KEEP
SURGERY_FORENSICS_20260911.md | receipt | 2026-09-11 | 0+4/1 | 11504 | KEEP
SURGERY_LOSSES_ACCOUNT_20260911.md | receipt | 2026-09-11 | 0+3/1 | 7600 | KEEP
SWAP_RUNBOOK_APIKEY_20260907.md | receipt | 2026-09-07 | 0+7/1 | 2687 | KEEP
SWARM_MAP_FOLD_20260914.md | finding | 2026-09-14 | 0+4/1 | 2380 | KEEP
SWARM_QUEST_GENERATOR_20260907.md | receipt | 2026-09-07 | 0+5/1 | 2691 | KEEP
SWARM_STEERING_IMPLICATIONS_20260901.md | receipt | 2026-09-01 | 0+9/1 | 5150 | KEEP
T1_FIRED_20260907.md | receipt | 2026-09-07 | 0+4/1 | 4412 | KEEP
TALKING_POINTS_20260911.md | receipt | 2026-09-11 | 0+4/1 | 2101 | KEEP
TARTARIA_LIVES_INTAKE_20260923.md | finding | 2026-09-23 | 0+4/1 | 6480 | KEEP
TASK_WALL_REPORT_20260923.md | brief | 2026-09-23 | 2+6/1 | 641 | KEEP
TAVERN_BRAWL_SHIPPED_20260907.md | receipt | 2026-09-07 | 0+6/1 | 3071 | KEEP
TENSION_PAPER_20260912.md | finding | 2026-09-12 | 0+4/1 | 3624 | KEEP
TESUJI_A6_LOCAL_DIFF_20260906.md | receipt | 2026-09-06 | 0+6/1 | 5368 | KEEP
TESUJI_GRIDDER_20260906.md | receipt | 2026-09-06 | 0+6/1 | 3166 | KEEP
TESUJI_PAGER_20260906.md | receipt | 2026-09-06 | 0+6/1 | 1954 | KEEP
TESUJI_T0_BANKER_20260906.md | receipt | 2026-09-06 | 0+6/1 | 6072 | KEEP
TESUJI_T0_RECEIPTER_20260906.md | receipt | 2026-09-06 | 0+6/1 | 4579 | KEEP
THE50_RELAUNCH_VERDICT_20260925.md | receipt | 2026-09-25 | 1+4/1 | 1937 | KEEP
THE50_W10_T46_DISSENSUS_FOLD.md | receipt | 2026-09-19 | 0+4/1 | 14277 | KEEP
THE50_W10_T47_CLIFF_SCALAR.md | receipt | 2026-09-19 | 0+4/1 | 29598 | KEEP
THE50_W10_T48_DISTINGUISH.md | receipt | 2026-09-19 | 0+4/1 | 8674 | KEEP
THE50_W10_T49_SYSONE_VOCAB.md | receipt | 2026-09-19 | 0+4/1 | 12411 | KEEP
THE50_W10_T50_STEERING_FREEZE.md | receipt | 2026-09-19 | 0+4/1 | 15007 | KEEP
THE50_W1_T04_NPC_DIALOGUE_BANK.md | receipt | 2026-09-19 | 0+4/1 | 6061 | KEEP
THE50_W1_T05_PAYOFF_MATRIX.md | receipt | 2026-09-19 | 0+4/1 | 15272 | KEEP
THE50_W3_T12_PROPHECY_MARKETS.md | receipt | 2026-09-19 | 0+5/1 | 20621 | KEEP
THE50_W3_T12_RECEIPT.md | receipt | 2026-09-19 | 0+4/1 | 1725 | KEEP
THE50_W4_T20_RECEIPT_CREDIT.md | receipt | 2026-09-19 | 0+4/1 | 14043 | KEEP
THE50_W6_T28_MISS_ENTROPY.md | receipt | 2026-09-19 | 0+4/1 | 8124 | KEEP
THE50_W6_T30_POLICY_EVAL.md | receipt | 2026-09-19 | 0+5/1 | 20454 | KEEP
THE50_W7_T31_SETTLEMENT_AUDIT.md | receipt | 2026-09-19 | 0+4/1 | 20722 | KEEP
THE50_W7_T34_GSTDBOT_AUDIT.md | receipt | 2026-09-19 | 0+4/1 | 20505 | KEEP
THE50_W8_T38_LEDGER_PUBLIC_SPEC.md | receipt | 2026-09-19 | 0+4/1 | 17301 | KEEP
THE50_W9_T44_NIGHTLY_VISION_BATCH.md | receipt | 2026-09-19 | 0+4/1 | 6957 | KEEP
THE50_W9_T45_EDGE_SCHEMA.md | receipt | 2026-09-19 | 0+5/1 | 14482 | KEEP
THEME_LEXICON_20260911.md | finding | 2026-09-11 | 0+3/1 | 14161 | KEEP
THEME_LEXICON_FOLDED_20260911.md | finding | 2026-09-11 | 0+3/1 | 3822 | KEEP
THEME_SLUG_DEDUPE_20260911.md | receipt | 2026-09-11 | 0+3/1 | 3473 | KEEP
THE_50_PROGRAM_20260918.md | receipt | 2026-09-18 | 2+7/1 | 3964 | KEEP
THE_ASK_IS_A_LENS_20260918.md | brief | 2026-09-18 | 0+5/1 | 7234 | KEEP
THE_BOOKS_DISAGREEMENT_20260919.md | receipt | 2026-09-19 | 0+6/1 | 13838 | KEEP
THE_CALLED_SHOT_20260914.md | receipt | 2026-09-14 | 0+4/1 | 4022 | KEEP
THE_CATHEDRAL_MAP_20260918.md | finding | 2026-09-18 | 0+5/1 | 4703 | KEEP
THE_CONVERSION_PLAN_20260923.md | receipt | 2026-09-23 | 0+4/1 | 4828 | KEEP
THE_CRAFT_NAMEPLATE_20260922.md | receipt | 2026-09-22 | 0+4/1 | 1839 | KEEP
THE_DECODER_RING_20260912.md | finding | 2026-09-12 | 0+5/1 | 4064 | KEEP
THE_ELDER_DISCUSSION_20260920.md | receipt | 2026-09-20 | 1+4/1 | 5360 | KEEP
THE_FIRST_NACHO_20260913.md | receipt | 2026-09-13 | 0+4/1 | 15275 | KEEP
THE_FRONTIER_20260924.md | receipt | 2026-09-24 | 0+5/1 | 177600 | KEEP
THE_FRONTIER_ASK_72STEP_20260920.md | brief | 2026-09-20 | 0+4/1 | 22537 | KEEP
THE_FULL_NIGHT_20260924.md | receipt | 2026-09-24 | 0+4/1 | 7588 | KEEP
THE_MERGE_20260914.md | receipt | 2026-09-14 | 0+4/1 | 2920 | KEEP
THE_NEEDS_MANIFEST_20260921.md | receipt | 2026-09-21 | 1+4/1 | 5350 | KEEP
THE_OLD_BOOKS_SHELF_20260923.md | finding | 2026-09-23 | 1+4/1 | 91641 | KEEP
THE_OLD_BOOKS_SHELF_DIG2_20260923.md | other | 2026-09-23 | 1+4/1 | 62739 | REVIEW
THE_ORPHAN_CARD_20260916.md | receipt | 2026-09-16 | 0+4/1 | 2606 | KEEP
THE_PARABLE_REGISTER.md | receipt | 2026-09-16 | 2+9/1 | 19844 | KEEP
THE_RACTORS_ARE_WRONG_20260920.md | receipt | 2026-09-20 | 0+3/1 | 3660 | KEEP
THE_REBELLION_IS_MAINTENANCE_20260914.md | finding | 2026-09-14 | 0+4/1 | 1935 | KEEP
THE_RIPOSTE_20260923.md | receipt | 2026-09-23 | 0+4/1 | 10586 | KEEP
THE_SCALE_FINAL_20260916.md | finding | 2026-09-16 | 0+7/1 | 12683 | KEEP
THE_SCALE_PARABLE_20260916.md | receipt | 2026-09-16 | 0+4/1 | 5515 | KEEP
THE_SESSION_RECORD_20260916.md | receipt | 2026-09-16 | 1+5/1 | 7795 | KEEP
THE_SOURCE_MATTHEWS_CORPUS_20260914.md | finding | 2026-09-14 | 0+4/1 | 4219 | KEEP
THE_UNDENIABLE_LEDGER_20260923.md | receipt | 2026-09-23 | 1+4/1 | 177909 | KEEP
THE_WEAVE_20260916.md | receipt | 2026-09-16 | 0+7/1 | 32337 | KEEP
THE_WINNABLE_ARGUMENT_20260923.md | receipt | 2026-09-23 | 0+4/1 | 50887 | KEEP
THIRD_WAY_FALSIFIER_REGISTRY.md | receipt | 2026-09-27 | 0+8/1 | 6802 | KEEP
THORN_KIT_20260920.md | receipt | 2026-09-20 | 1+4/1 | 7218 | KEEP
TIME_TRAVEL_QSTAR_20260918.md | receipt | 2026-09-18 | 1+8/1 | 8842 | KEEP
TOOL_NUANCE_WAVE_20260913.md | receipt | 2026-09-13 | 0+4/1 | 7106 | KEEP
TOOL_PRICING_RIGHTSIZE_20260913.md | receipt | 2026-09-13 | 0+4/1 | 4277 | KEEP
TOPIC_INDEX_BUILD_20260906.md | receipt | 2026-09-06 | 0+14/1 | 3182 | KEEP
TRAILER_MECHANISM_20260911.md | receipt | 2026-09-11 | 1+5/1 | 4357 | KEEP
TRAJECTORY_SWEEP_20260923.md | receipt | 2026-09-23 | 0+4/1 | 276349 | KEEP
TRANSFER_TEST_20260906.md | receipt | 2026-09-06 | 0+10/1 | 4994 | KEEP
TRAVEL_KIT_20260919.md | receipt | 2026-09-19 | 0+4/1 | 1814 | KEEP
TREE_DOCTRINE_20260925.md | receipt | 2026-09-25 | 1+5/1 | 6056 | KEEP
TREE_DOCTRINE_V2_BRIEF_20260925.md | brief | 2026-09-25 | 1+5/1 | 3012 | KEEP
TREE_DOCTRINE_V2_DIGEST_20260925.md | finding | 2026-09-25 | 2+6/1 | 160327 | KEEP
TRIAGE_MEMO_20260916.md | brief | 2026-09-16 | 0+6/1 | 11532 | KEEP
TWO_MACHINE_SYNC_20260919.md | receipt | 2026-09-19 | 1+8/1 | 6722 | KEEP
UNDENIABLE_LEDGER_ADDENDUM_20260923.md | receipt | 2026-09-23 | 1+5/1 | 92652 | KEEP
UNIVERSAL_LENS_RESPONSE_20260921.md | finding | 2026-09-21 | 0+4/1 | 4730 | KEEP
V2.1_ITERATION_20260925.md | receipt | 2026-09-25 | 0+4/1 | 4052 | KEEP
VERB_DSL_STEAL_20260918.md | finding | 2026-09-18 | 1+8/1 | 3344 | KEEP
VERITAS_X_ESTATE_20260927.md | receipt | 2026-09-27 | 0+3/1 | 5502 | KEEP
VERKLE_FAMILY_SURVEY_20260911.md | finding | 2026-09-11 | 0+4/1 | 15136 | KEEP
VERKLE_GATE_20260907.md | receipt | 2026-09-07 | 1+6/1 | 8693 | KEEP
VIDEO_SMOKE_20260907.md | finding | 2026-09-07 | 0+4/1 | 1938 | KEEP
VISION_PASS_SWEEP1_20260906.md | receipt | 2026-09-06 | 0+9/1 | 2770 | KEEP
VP_SHITPOST_DESK_20260916.md | shitpost | 2026-09-16 | 0+6/1 | 4101 | KEEP
W0_BASH_LOCAL_20260907.md | receipt | 2026-09-07 | 0+5/1 | 2983 | KEEP
W1_DEATH_RITE_20260907.md | receipt | 2026-09-07 | 0+5/1 | 5960 | KEEP
W2_RESURRECTION_LOADER_20260907.md | receipt | 2026-09-07 | 0+6/1 | 8861 | KEEP
W3_CACHE_IDENTITY_20260907.md | receipt | 2026-09-07 | 0+5/1 | 5644 | KEEP
W4_SALON_TRAJECTORY_NATIVE_20260907.md | receipt | 2026-09-07 | 0+8/1 | 4936 | KEEP
W6_SEED_REGISTRY_20260907.md | receipt | 2026-09-07 | 0+6/1 | 8132 | KEEP
WALK_HUBFIRST_20260921.md | finding | 2026-09-21 | 1+4/1 | 1949 | KEEP
WALK_HUBFIRST_20260926.md | finding | 2026-09-26 | 0+3/1 | 1803 | KEEP
WALK_HUBFIRST_20260927.md | finding | 2026-09-27 | 0+3/1 | 1803 | KEEP
WALK_WATERFIRST_20260921.md | finding | 2026-09-21 | 1+4/1 | 1465 | KEEP
WALK_WATERFIRST_20260926.md | finding | 2026-09-26 | 0+3/1 | 1465 | KEEP
WALK_WATERFIRST_20260927.md | finding | 2026-09-27 | 0+3/1 | 1465 | KEEP
WARMED_COLD_REPLAY_20260907.md | receipt | 2026-09-07 | 0+6/1 | 8760 | KEEP
WATCH_GOVERNANCE_20260924.md | finding | 2026-09-24 | 0+4/1 | 2581 | KEEP
WATCH_MINING_20260918.md | receipt | 2026-09-18 | 1+4/1 | 4565 | KEEP
WATER_MUSHROOM_PITCH_20260920.md | receipt | 2026-09-20 | 0+4/1 | 7160 | KEEP
WATER_ROUTING_LANDED_20260927.md | receipt | 2026-09-27 | 0+2/1 | 3157 | KEEP
WAVE_BRIDGE_20260922.md | receipt | 2026-09-22 | 0+4/1 | 2722 | KEEP
WAVE_BRUTEFORCE_DESIGN_20260911.md | receipt | 2026-09-11 | 0+5/1 | 2977 | KEEP
WAVE_STATE_20260916.md | receipt | 2026-09-16 | 1+7/1 | 4472 | KEEP
WBN_STEAL_20260918.md | finding | 2026-09-18 | 0+7/1 | 3544 | KEEP
WHAT_REMAINS_20260919.md | receipt | 2026-09-19 | 0+4/1 | 4343 | KEEP
WIDTH_LEDGER_20260926.md | receipt | 2026-09-26 | 1+8/1 | 4247 | KEEP
WINDOW_2122_SCORING_RUBRIC_20260920.md | receipt | 2026-09-20 | 1+4/1 | 3236 | KEEP
WINDOW_CLOSE_20260927_GATEFIX_LENS.md | finding | 2026-09-27 | 0+2/1 | 6651 | KEEP
WINDOW_CLOSE_20260927_MORNING.md | receipt | 2026-09-27 | 0+4/1 | 2033 | KEEP
WINDOW_MINING_BIRTH_20260911.md | receipt | 2026-09-11 | 0+4/1 | 12053 | KEEP
WINSTT_ASSESS_20260911.md | other | 2026-09-11 | 0+3/1 | 2386 | REVIEW
WORLDLINE_DUNGEON_SURFACE_20260907.md | receipt | 2026-09-07 | 0+8/1 | 5589 | KEEP
WORLDLINE_SEED_SALON_20260907.md | receipt | 2026-09-07 | 0+6/1 | 7296 | KEEP
WORLDVIEW_AUDIT_20260923.md | receipt | 2026-09-23 | 1+4/1 | 7200 | KEEP
WOW_CLONE_BETA_BLUEPRINT_20260916.md | receipt | 2026-09-16 | 2+4/1 | 3981 | KEEP
WOW_SURFACE_INVENTORY_20260911.md | finding | 2026-09-11 | 0+4/1 | 3492 | KEEP
WOW_TXT_MINED_20260911.md | receipt | 2026-09-11 | 0+7/1 | 11155 | KEEP
WRITE_STRIP_FANOUT_20260926.md | receipt | 2026-09-26 | 1+5/1 | 7484 | KEEP
WRONGTHINK_ROW_SEEDWAVE_20260911.md | finding | 2026-09-11 | 0+3/1 | 2201 | KEEP
W_WAVE_FOLD_20260912.md | finding | 2026-09-12 | 0+5/1 | 18100 | KEEP
X6_WITHDRAWAL_CLAUSE_20260928.md | receipt | 2026-09-28 | 0+3/0 | 724 | ARCHIVE
X_ANCHOR_MAP_20260923.md | finding | 2026-09-23 | 1+4/1 | 932 | KEEP
X_ANCHOR_MAP_SEEDS_20260923.md | finding | 2026-09-23 | 1+4/1 | 1197 | KEEP
X_ARTICLE_PROMPT_GAMES_20260923.md | brief | 2026-09-23 | 0+4/1 | 4656 | KEEP
X_HARVEST_SCORECARD_20260905.md | receipt | 2026-09-05 | 0+7/1 | 7249 | KEEP
X_LEAKS_WAYBACK_20260925.md | receipt | 2026-09-25 | 0+4/1 | 7096 | KEEP
ZCODE_DIVERGENCE_SYNC_20260912.md | receipt | 2026-09-12 | 0+5/1 | 1789 | KEEP
ZCODE_HARNESS_OPEN_SOURCED_20260921.md | finding | 2026-09-21 | 0+4/1 | 2740 | KEEP
ZCODE_SHADOW_STEAL_20260918.md | finding | 2026-09-18 | 1+5/1 | 6614 | KEEP
_seal_test.md | other | 2026-09-21 | 0+4/1 | 24 | REVIEW
astra_ask_package/sovereign-agent-systems-research-brief.md | brief | 2026-09-15 | 0+3/0 | 58495 | ARCHIVE
astra_corpus/ORPHANS_SUPPLEMENT_v1_1_20260916.md | receipt | 2026-09-16 | 0+1/0 | 7791 | ARCHIVE
astra_review_sep16/sep16-submission-review.md | finding | 2026-09-16 | 0+2/0 | 24683 | ARCHIVE
audit_20260926/GATE_DEFECT_ASSIGNMENT_BYPASS_20260927.md | receipt | 2026-09-27 | 2+2/0 | 4348 | KEEP
audit_20260926/LANE0_PARENT_INTEGRATOR.md | finding | 2026-09-27 | 0+6/1 | 7459 | KEEP
audit_20260926/LANE10_ADVERSARIAL.md | receipt | 2026-09-27 | 0+2/0 | 22202 | ARCHIVE
audit_20260926/LANE1_PRIOR_MAP_DELTA.md | finding | 2026-09-27 | 0+2/0 | 35263 | REVIEW
audit_20260926/LANE2B_DEAD_INSTRUMENTS_PARENT.md | receipt | 2026-09-27 | 0+2/0 | 3255 | ARCHIVE
audit_20260926/LANE2_DOGFOOD_TOOLS.md | receipt | 2026-09-27 | 0+2/0 | 30675 | ARCHIVE
audit_20260926/LANE3_GATE_ENFORCEMENT.md | receipt | 2026-09-27 | 0+2/0 | 17221 | ARCHIVE
audit_20260926/LANE4B_UNVERSIONED_RISK.md | receipt | 2026-09-27 | 0+3/0 | 19591 | ARCHIVE
audit_20260926/LANE4C_HISTORY_SECRETS.md | finding | 2026-09-27 | 0+1/0 | 9271 | ARCHIVE
audit_20260926/LANE4D_STALE_RECEIPTS.md | receipt | 2026-09-27 | 0+1/0 | 10803 | ARCHIVE
audit_20260926/LANE4_TEST_ROBUSTNESS.md | receipt | 2026-09-27 | 2+2/0 | 21823 | KEEP
audit_20260926/LANE4_UNVERSIONED_SURFACE.md | receipt | 2026-09-27 | 0+3/0 | 26557 | ARCHIVE
audit_20260926/LANE5_FILE_COMPOSITION.md | receipt | 2026-09-27 | 0+2/0 | 16447 | ARCHIVE
audit_20260926/LANE6_DOCTRINE_SOCRATIC.md | receipt | 2026-09-27 | 0+2/0 | 15142 | ARCHIVE
audit_20260926/LANE7_TEST_REALITY.md | receipt | 2026-09-27 | 0+2/0 | 25463 | ARCHIVE
audit_20260926/LANE7_VERIFICATION_PARENT.md | receipt | 2026-09-27 | 0+1/0 | 5364 | ARCHIVE
audit_20260926/LANE9_PRIVATE_BOUNDARY.md | receipt | 2026-09-27 | 0+1/0 | 13610 | ARCHIVE
audit_20260926/LANE9_VERIFICATION_PARENT.md | receipt | 2026-09-27 | 0+1/0 | 3890 | ARCHIVE
audit_20260926/PACK_SECRET_GATE_20260926.md | receipt | 2026-09-26 | 3+3/1 | 9479 | KEEP
audit_20260926/W2L7_SECRET_SCAN_VERIFICATION.md | receipt | 2026-09-27 | 0+1/0 | 5554 | ARCHIVE
audit_20260926/WAVE1_CONSOLIDATION_PARENT.md | receipt | 2026-09-27 | 0+2/0 | 8293 | ARCHIVE
audit_20260926/WAVE2_CONSOLIDATION_PARENT.md | receipt | 2026-09-27 | 0+2/0 | 9262 | ARCHIVE
audit_20260926/WAVE2_LANE10_SHARED_SURFACE.md | receipt | 2026-09-27 | 0+3/0 | 22749 | ARCHIVE
audit_20260926/WAVE2_LANE1_DISK_MAP.md | finding | 2026-09-27 | 0+2/0 | 14832 | REVIEW
audit_20260926/WAVE2_LANE2_PUSH_BLOCKERS.md | receipt | 2026-09-27 | 0+3/0 | 14398 | ARCHIVE
audit_20260926/WAVE2_LANE3_RIB_COMPILER.md | law | 2026-09-27 | 0+2/0 | 19107 | PROMOTE
audit_20260926/WAVE2_LANE6_DEAD_TOOLS.md | receipt | 2026-09-27 | 0+2/0 | 14702 | ARCHIVE
audit_20260926/WAVE2_LANE9_NARRATIVE_DRIFT.md | receipt | 2026-09-27 | 0+2/0 | 29030 | ARCHIVE
bad_apple/PROVENANCE.md | other | 2026-09-14 | 14+50/1 | 2243 | REVIEW
burn_reset_20260927/all_seat.md | receipt | 2026-09-27 | 0+4/0 | 2583 | ARCHIVE
burn_reset_20260927/desk_baseline.md | receipt | 2026-09-27 | 14+9/0 | 3940 | KEEP
burn_reset_20260927/dirac_loop6.md | receipt | 2026-09-27 | 0+2/0 | 4164 | ARCHIVE
burn_reset_20260927/dirac_loops45.md | receipt | 2026-09-27 | 0+2/0 | 3205 | ARCHIVE
burn_reset_20260927/flash50/_compiled_clippy.md | law | 2026-09-28 | 0+1/0 | 7205 | PROMOTE
burn_reset_20260927/flash50/_compiled_clippy_release.md | law | 2026-09-28 | 0+1/0 | 7205 | PROMOTE
burn_reset_20260927/flash50/_compiled_rib_k8s.md | law | 2026-09-28 | 0+1/0 | 12469 | PROMOTE
burn_reset_20260927/flash50/_compiled_rib_release.md | law | 2026-09-28 | 0+1/0 | 12469 | PROMOTE
burn_reset_20260927/flash50/_compiled_tide_v1.md | receipt | 2026-09-28 | 0+1/0 | 2328 | ARCHIVE
burn_reset_20260927/flash50/_s219_basetemp/test_append_agent_probe_inject0/runs/20260929T001346Z-inject-9d9ef8/progress.md | receipt | nodate | 146+169/0 | 1708 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_append_desk_meta_raw0/memory/working/agent_desk.md | finding | nodate | 38+10/0 | 122 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_append_desk_section0/memory/working/agent_desk.md | receipt | nodate | 38+10/0 | 76 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_arrival_report_honest0/research_packs/pack.answer.swarm.md | receipt | nodate | 1+1/0 | 720 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_auto_promote_gate0/playbook.md | finding | nodate | 72+63/0 | 311 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_base_id_mismatch_rejected0/runs/20260929T001345Z-mismatch-f15e3f/progress.md | receipt | nodate | 146+169/0 | 1712 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_behavioral_candidates_min0/memory/improve/daily/2026-08-04-behavioral.md | receipt | 2026-08-04 | 2+1/0 | 155 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_behavioral_candidates_min1/memory/improve/daily/2026-08-04-behavioral.md | receipt | 2026-08-04 | 2+1/0 | 155 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_behavioral_candidates_min2/memory/improve/daily/2026-08-04-behavioral.md | receipt | 2026-08-04 | 2+1/0 | 155 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_build_display_payload_sha0/memory/working/agent_desk.md | receipt | nodate | 38+10/0 | 76 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_canvas_pollution_auto_hea0/memory/working/agent_desk.md | finding | nodate | 38+10/0 | 606 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_cli_collect_accurate_carr0/AGENTS.md | receipt | nodate | 78+158/1 | 118 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_cli_collect_broken_collec0/AGENTS.md | receipt | nodate | 78+158/1 | 89 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_cli_collect_names_the_zer0/AGENTS.md | receipt | nodate | 78+158/1 | 117 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_cli_falsifier_green_gate_0/AGENTS.md | receipt | nodate | 78+158/1 | 117 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_cli_fresh_synthetic_estat0/AGENTS.md | receipt | nodate | 78+158/1 | 98 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_cli_future_census_exits_20/AGENTS.md | receipt | nodate | 78+158/1 | 80 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_cli_green_output_starts_w0/AGENTS.md | receipt | nodate | 78+158/1 | 98 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_cli_stale_synthetic_estat0/AGENTS.md | receipt | nodate | 78+158/1 | 131 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_cli_unparsable_carrier_ex0/AGENTS.md | receipt | nodate | 78+158/1 | 33 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_close_session_if_ready_cl0/agent_desk.md | receipt | nodate | 38+10/0 | 93 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_commit_chain_and_load0/agent_state/LATEST.md | receipt | nodate | 59+32/1 | 935 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_commit_chain_and_load0/agent_state/versions/20260929T001318Z_1f254e75.md | receipt | 2026-09-29 | 0+1/0 | 935 | ARCHIVE
burn_reset_20260927/flash50/_s219_basetemp/test_commit_chain_and_load0/agent_state/versions/20260929T001318Z_8c8e8b1b.md | receipt | 2026-09-29 | 0+1/0 | 961 | ARCHIVE
burn_reset_20260927/flash50/_s219_basetemp/test_commit_chain_and_load0/memory/improve/pins/AGENT_STATE_LATEST.md | receipt | nodate | 1+3/0 | 289 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_commit_empty_is_noop0/agent_desk.md | receipt | nodate | 38+10/0 | 15 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_commit_operator_intent_go0/agent_desk.md | finding | nodate | 38+10/0 | 114 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_demote_gap_shapes0/playbook.md | finding | nodate | 72+63/0 | 147 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_dialogue_turn_includes_ti0/memory/working/agent_desk.md | receipt | nodate | 38+10/0 | 82 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_dialogue_turn_local_mock0/memory/working/agent_desk.md | receipt | nodate | 38+10/0 | 122 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_dialogue_turn_simulated_l0/memory/working/agent_desk.md | receipt | nodate | 38+10/0 | 115 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_file_agent_core_stamps_ba0/runs/20260929T001345Z-drift-stamp-03d991/progress.md | receipt | nodate | 146+169/0 | 1721 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_fold_authored_idempotent_0/research_packs/pack.answer.swarm.md | receipt | nodate | 1+1/0 | 502 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_gate_refuses_missing_seal0/BATTERY_HELDOUT.md | receipt | nodate | 2+2/0 | 99 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_gate_refuses_missing_seal0/GROUND_TRUTH_HELDOUT.md | receipt | nodate | 2+2/0 | 111 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_gate_refuses_missing_seal0/RERUN_ANSWERS_fixture.md | receipt | nodate | 1+1/0 | 124 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_happy_path_default_never_0/BATTERY_HELDOUT.md | receipt | nodate | 2+2/0 | 99 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_happy_path_default_never_0/GROUND_TRUTH_HELDOUT.md | receipt | nodate | 2+2/0 | 111 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_happy_path_default_never_0/RERUN_ANSWERS_fixture.md | receipt | nodate | 1+1/0 | 124 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_happy_path_default_never_0/RERUN_SCORE_scaffold.md | finding | nodate | 1+1/0 | 2186 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_heldout_drift_refuses0/BATTERY_HELDOUT.md | receipt | nodate | 2+2/0 | 113 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_heldout_drift_refuses0/GROUND_TRUTH_HELDOUT.md | receipt | nodate | 2+2/0 | 111 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_heldout_drift_refuses0/RERUN_ANSWERS_fixture.md | receipt | nodate | 1+1/0 | 124 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_hook_census_case_arm_repl0/green/AGENTS.md | receipt | nodate | 78+158/1 | 98 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_hook_census_case_arm_repl0/stale/AGENTS.md | receipt | nodate | 78+158/1 | 131 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_list_drifts_clusters0/runs/20260929T001345Z-list-drifts-a8e91a/progress.md | receipt | nodate | 146+169/0 | 1718 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_mag_internal_includes_beh0/memory/improve/daily/2026-08-04-behavioral.md | receipt | 2026-08-04 | 2+1/0 | 155 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_meta_discuss_mock0/memory/working/agent_desk.md | receipt | nodate | 38+10/0 | 42 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_packs_reads_from_dir0/research_packs/p1.answer.swarm.md | receipt | nodate | 1+1/0 | 300 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_packs_reads_from_dir0/research_packs/p2.answer.swarm.md | receipt | nodate | 1+1/0 | 250 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_ping_pong_stops_on_failur0/memory/working/agent_desk.md | receipt | nodate | 38+10/0 | 12 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_plan_session_writes_known0/agent_desk.md | receipt | nodate | 38+10/0 | 1962 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_preserve_live_desk_restor0/desk.md | receipt | nodate | 291+450/0 | 14 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_resolve_and_file_agent_se0/derived/mag-agent-_pytest_agent_wd.md | receipt | nodate | 1+21/0 | 1082 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_revert_disarms_and_presen0/state/hold_queue/a_first.md | receipt | nodate | 1+1/0 | 1 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_revert_disarms_and_presen0/state/hold_queue/b_second.md | receipt | nodate | 1+1/0 | 1 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_score_mode_pairs_ground_t0/BATTERY_HELDOUT.md | receipt | nodate | 2+2/0 | 99 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_score_mode_pairs_ground_t0/GROUND_TRUTH_HELDOUT.md | receipt | nodate | 2+2/0 | 111 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_score_mode_pairs_ground_t0/RERUN_ANSWERS_fixture.md | receipt | nodate | 1+1/0 | 124 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_score_mode_pairs_ground_t0/RERUN_SCORE_scaffold.md | finding | nodate | 1+1/0 | 2120 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_seal_mismatch_refuses0/BATTERY_HELDOUT.md | receipt | nodate | 2+2/0 | 99 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_seal_mismatch_refuses0/GROUND_TRUTH_HELDOUT.md | receipt | nodate | 2+2/0 | 111 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_seal_mismatch_refuses0/RERUN_ANSWERS_fixture.md | receipt | nodate | 1+1/0 | 124 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_seed_desk_includes_orches0/agent_desk.md | receipt | nodate | 38+10/0 | 2972 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_seed_desk_writes_goal0/agent_desk.md | receipt | nodate | 38+10/0 | 2854 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_session_done_defers_expen0/desk.md | receipt | nodate | 291+450/0 | 14 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_set_desk_goal_replaces_se0/agent_desk.md | finding | nodate | 38+10/0 | 49 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_shape_drift_refuses0/BATTERY_HELDOUT.md | receipt | nodate | 2+2/0 | 99 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_shape_drift_refuses0/GROUND_TRUTH_HELDOUT.md | receipt | nodate | 2+2/0 | 111 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_shape_drift_refuses0/RERUN_ANSWERS_fixture.md | receipt | nodate | 1+1/0 | 124 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_slow_wake_skips_remote_wi0/memory/working/agent_desk.md | receipt | nodate | 38+10/0 | 12 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_start_run_freezes_base0/runs/20260929T001345Z-base-freeze-test-eeb395/progress.md | receipt | nodate | 146+169/0 | 1728 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_synthesize_behavioral_lea0/improve/daily/2026-08-04-behavioral.md | receipt | 2026-08-04 | 2+1/0 | 620 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_trigger_fires_seal_hold_l0/state/hold_queue/README.md | receipt | nodate | 0+0/1 | 224 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_turn_auto_heal_skips_canv0/memory/working/agent_desk.md | receipt | nodate | 38+10/0 | 157 | KEEP
burn_reset_20260927/flash50/_s219_basetemp/test_write_and_read_desk0/memory/working/agent_desk.md | receipt | nodate | 38+10/0 | 15 | KEEP
burn_reset_20260927/flash50/_sw03_out_sw-econ-1_glm-5.3.md | receipt | nodate | 0+1/0 | 152 | ARCHIVE
burn_reset_20260927/flash50/_sw03_out_sw-econ-1_stealth_space-bunny-alpha.md | finding | nodate | 0+1/0 | 119 | ARCHIVE
burn_reset_20260927/flash50/_sw03_out_sw-econ-3_meta_muse-spark-1.3.md | receipt | nodate | 0+1/0 | 161 | ARCHIVE
burn_reset_20260927/flash50/_sw03_out_sw-econ-3_stealth_space-bunny-alpha.md | finding | nodate | 0+0/0 | 11968 | ARCHIVE
burn_reset_20260927/flash50/api-endpoint-map.md | finding | nodate | 0+1/0 | 61566 | REVIEW
burn_reset_20260927/flash50/arch-01.md | receipt | 2026-09-28 | 0+1/0 | 18151 | ARCHIVE
burn_reset_20260927/flash50/arch-02.md | receipt | 2026-09-28 | 0+1/0 | 22430 | ARCHIVE
burn_reset_20260927/flash50/arch-03.md | receipt | 2026-09-28 | 0+1/0 | 17988 | ARCHIVE
burn_reset_20260927/flash50/arch-04.md | finding | 2026-09-28 | 0+1/0 | 19339 | ARCHIVE
burn_reset_20260927/flash50/boot-path-trace.md | finding | 2026-09-28 | 0+1/0 | 15265 | ARCHIVE
burn_reset_20260927/flash50/branch-census.md | finding | 2026-09-28 | 0+1/0 | 12801 | REVIEW
burn_reset_20260927/flash50/compass-audit.md | receipt | 2026-09-28 | 0+1/0 | 10852 | ARCHIVE
burn_reset_20260927/flash50/config-health.md | finding | 2026-09-28 | 0+1/0 | 26303 | ARCHIVE
burn_reset_20260927/flash50/configs-census.md | finding | nodate | 0+1/0 | 15910 | REVIEW
burn_reset_20260927/flash50/context-pipeline-map.md | finding | 2026-09-28 | 0+1/0 | 15842 | REVIEW
burn_reset_20260927/flash50/corpus-arxiv-list.md | receipt | 2026-09-28 | 0+1/0 | 19586 | ARCHIVE
burn_reset_20260927/flash50/decorator-census.md | finding | 2026-09-28 | 0+1/0 | 15107 | REVIEW
burn_reset_20260927/flash50/deep-antifragile-estate.md | finding | 2026-09-28 | 0+1/0 | 17833 | ARCHIVE
burn_reset_20260927/flash50/deep-attention-economics.md | finding | 2026-09-28 | 0+1/0 | 16003 | ARCHIVE
burn_reset_20260927/flash50/deep-attention-market.md | finding | 2026-09-28 | 0+1/0 | 18256 | ARCHIVE
burn_reset_20260927/flash50/deep-cathedral-market.md | finding | 2026-09-28 | 0+1/0 | 13486 | ARCHIVE
burn_reset_20260927/flash50/deep-cathedral-stone.md | finding | 2026-09-28 | 0+1/0 | 14281 | ARCHIVE
burn_reset_20260927/flash50/deep-chaos-governance.md | finding | 2026-09-28 | 0+1/0 | 22090 | ARCHIVE
burn_reset_20260927/flash50/deep-compiler-bootstrap.md | finding | 2026-09-28 | 0+1/0 | 25336 | ARCHIVE
burn_reset_20260927/flash50/deep-dirac-theory.md | finding | 2026-09-28 | 0+1/0 | 31443 | ARCHIVE
burn_reset_20260927/flash50/deep-dream-cycle.md | shitpost | 2026-09-28 | 0+1/0 | 22500 | ARCHIVE
burn_reset_20260927/flash50/deep-emergent-morality.md | finding | 2026-09-28 | 0+1/0 | 17056 | ARCHIVE
burn_reset_20260927/flash50/deep-entropy-budget.md | finding | 2026-09-28 | 0+1/0 | 20906 | ARCHIVE
burn_reset_20260927/flash50/deep-epistemic-gap.md | finding | 2026-09-28 | 0+1/0 | 22259 | REVIEW
burn_reset_20260927/flash50/deep-fossil-theory.md | finding | 2026-09-28 | 0+1/0 | 15944 | ARCHIVE
burn_reset_20260927/flash50/deep-genre-lattice.md | finding | 2026-09-28 | 0+1/0 | 24669 | ARCHIVE
burn_reset_20260927/flash50/deep-ghost-parliament.md | finding | 2026-09-28 | 0+1/0 | 19286 | ARCHIVE
burn_reset_20260927/flash50/deep-godel-estate.md | finding | 2026-09-28 | 0+1/0 | 20763 | ARCHIVE
burn_reset_20260927/flash50/deep-immune-system.md | finding | 2026-09-28 | 0+1/0 | 14520 | ARCHIVE
burn_reset_20260927/flash50/deep-infinite-cathedral.md | finding | 2026-09-28 | 0+1/0 | 20191 | ARCHIVE
burn_reset_20260927/flash50/deep-legibility.md | finding | 2026-09-28 | 0+1/0 | 14365 | ARCHIVE
burn_reset_20260927/flash50/deep-linguistic-dna.md | finding | 2026-09-28 | 0+1/0 | 21410 | ARCHIVE
burn_reset_20260927/flash50/deep-mirror-architecture.md | finding | 2026-09-28 | 0+1/0 | 21317 | ARCHIVE
burn_reset_20260927/flash50/deep-multiscale-memory.md | brief | 2026-09-28 | 0+1/0 | 21481 | ARCHIVE
burn_reset_20260927/flash50/deep-mycelial-routing.md | finding | 2026-09-28 | 0+1/0 | 17930 | ARCHIVE
burn_reset_20260927/flash50/deep-nurnberg-funnel.md | finding | 2026-09-28 | 0+1/0 | 27975 | ARCHIVE
burn_reset_20260927/flash50/deep-operator-model.md | finding | 2026-09-28 | 0+1/0 | 16498 | ARCHIVE
burn_reset_20260927/flash50/deep-operator-singularity.md | finding | 2026-09-28 | 0+1/0 | 21365 | ARCHIVE
burn_reset_20260927/flash50/deep-physics-of-receipts.md | finding | 2026-09-28 | 0+1/0 | 22902 | ARCHIVE
burn_reset_20260927/flash50/deep-prompt-compiler.md | brief | 2026-09-28 | 0+1/0 | 16109 | ARCHIVE
burn_reset_20260927/flash50/deep-quantizer-theory.md | finding | 2026-09-28 | 0+1/0 | 17724 | ARCHIVE
burn_reset_20260927/flash50/deep-quantum-receipts.md | finding | 2026-09-28 | 0+1/0 | 19014 | ARCHIVE
burn_reset_20260927/flash50/deep-recipe-ladder.md | finding | 2026-09-28 | 0+1/0 | 18471 | ARCHIVE
burn_reset_20260927/flash50/deep-recipes-as-types.md | finding | 2026-09-28 | 0+1/0 | 27468 | ARCHIVE
burn_reset_20260927/flash50/deep-selffeed-loop.md | finding | 2026-09-28 | 0+1/0 | 16733 | ARCHIVE
burn_reset_20260927/flash50/deep-semantic-diff.md | finding | 2026-09-28 | 0+1/0 | 15863 | ARCHIVE
burn_reset_20260927/flash50/deep-starvation-sensor.md | finding | 2026-09-28 | 0+1/0 | 24107 | ARCHIVE
burn_reset_20260927/flash50/deep-swarm-thermodynamics.md | finding | 2026-09-28 | 0+1/0 | 15215 | ARCHIVE
burn_reset_20260927/flash50/deep-temporal-types.md | finding | 2026-09-28 | 0+1/0 | 17203 | ARCHIVE
burn_reset_20260927/flash50/deep-tensor-receipts.md | finding | 2026-09-28 | 0+1/0 | 24844 | ARCHIVE
burn_reset_20260927/flash50/deep-the-map-is-territory.md | finding | 2026-09-28 | 0+1/0 | 18780 | REVIEW
burn_reset_20260927/flash50/deep-tool-genome.md | finding | 2026-09-28 | 0+1/0 | 13911 | ARCHIVE
burn_reset_20260927/flash50/deep-trust-game.md | finding | 2026-09-28 | 0+1/0 | 24922 | ARCHIVE
burn_reset_20260927/flash50/deep-verkle-formal.md | finding | 2026-09-28 | 0+1/0 | 26597 | ARCHIVE
burn_reset_20260927/flash50/deep-verkle-hologram.md | finding | 2026-09-28 | 0+1/0 | 20881 | ARCHIVE
burn_reset_20260927/flash50/deep-zero-operator.md | finding | 2026-09-28 | 0+1/0 | 20162 | ARCHIVE
burn_reset_20260927/flash50/dna-fact-check.md | receipt | 2026-09-28 | 0+1/0 | 13980 | ARCHIVE
burn_reset_20260927/flash50/dna-verification.md | receipt | 2026-09-28 | 0+1/0 | 11991 | ARCHIVE
burn_reset_20260927/flash50/docs-ref-audit.md | receipt | 2026-09-28 | 0+1/0 | 55599 | ARCHIVE
burn_reset_20260927/flash50/event-taxonomy.md | receipt | 2026-09-28 | 0+1/0 | 11441 | ARCHIVE
burn_reset_20260927/flash50/f-01.md | receipt | 2026-09-28 | 1+7/0 | 2917 | KEEP
burn_reset_20260927/flash50/f-02.md | receipt | 2026-09-28 | 0+6/0 | 16324 | ARCHIVE
burn_reset_20260927/flash50/f-03.md | receipt | 2026-09-28 | 0+7/0 | 3187 | ARCHIVE
burn_reset_20260927/flash50/f-04.md | receipt | 2026-09-28 | 0+3/0 | 7345 | ARCHIVE
burn_reset_20260927/flash50/f-05.md | receipt | 2026-09-28 | 0+3/0 | 11441 | ARCHIVE
burn_reset_20260927/flash50/f-06.md | finding | 2026-09-28 | 0+6/0 | 5317 | ARCHIVE
burn_reset_20260927/flash50/f-07.md | receipt | 2026-09-28 | 0+2/0 | 55599 | ARCHIVE
burn_reset_20260927/flash50/f-08.md | receipt | 2026-09-28 | 0+8/0 | 170333 | ARCHIVE
burn_reset_20260927/flash50/f-09.md | finding | 2026-09-28 | 0+8/0 | 91448 | ARCHIVE
burn_reset_20260927/flash50/f-10.md | receipt | 2026-09-28 | 0+3/0 | 91838 | ARCHIVE
burn_reset_20260927/flash50/f-11.md | receipt | 2026-09-28 | 0+10/0 | 11703 | ARCHIVE
burn_reset_20260927/flash50/f-12.md | receipt | 2026-09-28 | 0+7/0 | 9993 | ARCHIVE
burn_reset_20260927/flash50/f-13.md | finding | 2026-09-28 | 0+6/0 | 11849 | ARCHIVE
burn_reset_20260927/flash50/f-14.md | finding | 2026-09-28 | 0+6/0 | 15033 | ARCHIVE
burn_reset_20260927/flash50/f-15.md | finding | 2026-09-28 | 0+3/0 | 39098 | ARCHIVE
burn_reset_20260927/flash50/f-16.md | receipt | 2026-09-28 | 0+4/0 | 8222 | ARCHIVE
burn_reset_20260927/flash50/f-17.md | receipt | 2026-09-28 | 0+3/0 | 13947 | ARCHIVE
burn_reset_20260927/flash50/f-18.md | receipt | 2026-09-28 | 0+6/0 | 7084 | ARCHIVE
burn_reset_20260927/flash50/f-20.md | receipt | 2026-09-28 | 0+25/0 | 12801 | ARCHIVE
burn_reset_20260927/flash50/f-21.md | receipt | 2026-09-28 | 0+3/0 | 18940 | ARCHIVE
burn_reset_20260927/flash50/f-22.md | receipt | 2026-09-28 | 0+4/0 | 97157 | ARCHIVE
burn_reset_20260927/flash50/f-23.md | receipt | 2026-09-28 | 0+8/0 | 3321 | ARCHIVE
burn_reset_20260927/flash50/f-24.md | receipt | 2026-09-28 | 0+3/0 | 6931 | ARCHIVE
burn_reset_20260927/flash50/f-25.md | receipt | 2026-09-28 | 1+3/0 | 1646 | KEEP
burn_reset_20260927/flash50/f-26.md | receipt | 2026-09-28 | 0+3/0 | 4903 | ARCHIVE
burn_reset_20260927/flash50/f-27.md | receipt | 2026-09-28 | 0+3/0 | 4325 | ARCHIVE
burn_reset_20260927/flash50/f-28.md | receipt | 2026-09-28 | 0+2/0 | 4843 | ARCHIVE
burn_reset_20260927/flash50/f-29.md | receipt | 2026-09-28 | 0+6/0 | 7682 | ARCHIVE
burn_reset_20260927/flash50/f-30.md | receipt | 2026-09-28 | 0+6/0 | 2888 | ARCHIVE
burn_reset_20260927/flash50/free-lane-map.md | finding | nodate | 0+1/0 | 29694 | REVIEW
burn_reset_20260927/flash50/games-census.md | finding | 2026-09-28 | 0+1/0 | 9593 | REVIEW
burn_reset_20260927/flash50/hook-census.md | finding | nodate | 0+1/0 | 11660 | REVIEW
burn_reset_20260927/flash50/improve-loop-audit.md | receipt | nodate | 0+1/0 | 13235 | ARCHIVE
burn_reset_20260927/flash50/inbox-recent-census.md | finding | nodate | 0+1/0 | 16799 | REVIEW
burn_reset_20260927/flash50/index-truth.md | receipt | 2026-09-28 | 0+1/0 | 8222 | ARCHIVE
burn_reset_20260927/flash50/invariant-truth-audit.md | receipt | 2026-09-28 | 0+1/0 | 13311 | ARCHIVE
burn_reset_20260927/flash50/lane-health.md | receipt | 2026-09-28 | 0+1/0 | 11703 | ARCHIVE
burn_reset_20260927/flash50/large-file-census.md | finding | nodate | 0+1/0 | 18027 | REVIEW
burn_reset_20260927/flash50/ledger-census.md | finding | 2026-09-28 | 0+1/0 | 112000 | REVIEW
burn_reset_20260927/flash50/ledger-truth.md | receipt | 2026-09-28 | 0+5/0 | 170333 | ARCHIVE
burn_reset_20260927/flash50/luau-census.md | finding | nodate | 0+1/0 | 18049 | REVIEW
burn_reset_20260927/flash50/mag-census.md | finding | 2026-09-28 | 0+1/0 | 486355 | REVIEW
burn_reset_20260927/flash50/mag-deep-census.md | finding | nodate | 0+1/0 | 8118 | REVIEW
burn_reset_20260927/flash50/mag-dependency-graph.md | finding | 2026-09-28 | 0+1/0 | 91448 | ARCHIVE
burn_reset_20260927/flash50/mirror-decision-tree.md | receipt | 2026-09-28 | 0+1/0 | 19736 | ARCHIVE
burn_reset_20260927/flash50/mirror-x-voice.md | finding | 2026-09-28 | 0+1/0 | 10172 | ARCHIVE
burn_reset_20260927/flash50/oldest-files.md | receipt | nodate | 0+1/0 | 12224 | ARCHIVE
burn_reset_20260927/flash50/oral-01.md | receipt | 2026-09-28 | 0+1/0 | 43436 | ARCHIVE
burn_reset_20260927/flash50/oral-02.md | finding | 2026-09-28 | 0+1/0 | 17955 | ARCHIVE
burn_reset_20260927/flash50/oral-03.md | receipt | 2026-09-28 | 0+1/0 | 13619 | ARCHIVE
burn_reset_20260927/flash50/oral-decision-patterns.md | receipt | 2026-09-28 | 0+1/0 | 24049 | ARCHIVE
burn_reset_20260927/flash50/playbook-audit.md | finding | 2026-09-28 | 0+1/0 | 9843 | REVIEW
burn_reset_20260927/flash50/promise-gap.md | finding | 2026-09-28 | 0+1/0 | 11849 | REVIEW
burn_reset_20260927/flash50/provider-health.md | finding | 2026-09-28 | 2+3/0 | 9962 | KEEP
burn_reset_20260927/flash50/ps1-census.md | finding | 2026-09-28 | 0+1/0 | 17167 | REVIEW
burn_reset_20260927/flash50/quantizer-rd-curve.md | receipt | 2026-09-28 | 0+1/0 | 21709 | ARCHIVE
burn_reset_20260927/flash50/r-attractor-portfolio.md | finding | 2026-09-28 | 0+2/1 | 17192 | KEEP
burn_reset_20260927/flash50/r-auk-voice.md | receipt | 2026-09-28 | 0+2/1 | 10960 | KEEP
burn_reset_20260927/flash50/r-belady-lruk.md | finding | 2026-09-28 | 0+2/1 | 9546 | KEEP
burn_reset_20260927/flash50/r-belt-cube.md | receipt | 2026-09-28 | 0+2/1 | 18609 | KEEP
burn_reset_20260927/flash50/r-contrastive-wm.md | finding | 2026-09-28 | 0+2/1 | 24628 | KEEP
burn_reset_20260927/flash50/r-corpus-epistemics.md | receipt | 2026-09-28 | 0+2/1 | 15015 | KEEP
burn_reset_20260927/flash50/r-eam-tracking.md | finding | 2026-09-28 | 0+2/1 | 16526 | KEEP
burn_reset_20260927/flash50/r-moe-offload.md | finding | 2026-09-28 | 0+2/1 | 26029 | KEEP
burn_reset_20260927/flash50/r-muse-gating.md | receipt | 2026-09-28 | 0+2/1 | 7708 | KEEP
burn_reset_20260927/flash50/r-selfplay-sota.md | receipt | 2026-09-28 | 0+2/1 | 14027 | KEEP
burn_reset_20260927/flash50/r-solomonoff-pretrain.md | receipt | 2026-09-28 | 0+2/1 | 13805 | KEEP
burn_reset_20260927/flash50/r-vortex-latent.md | receipt | 2026-09-28 | 0+2/1 | 12102 | KEEP
burn_reset_20260927/flash50/r-water-plasma.md | finding | 2026-09-28 | 0+2/1 | 16650 | KEEP
burn_reset_20260927/flash50/rib-bus-census.md | law | nodate | 0+1/0 | 24310 | PROMOTE
burn_reset_20260927/flash50/rib-census.md | law | 2026-09-28 | 0+1/0 | 15033 | PROMOTE
burn_reset_20260927/flash50/root-module-census.md | finding | 2026-09-28 | 0+1/0 | 13947 | REVIEW
burn_reset_20260927/flash50/s2-01.md | receipt | nodate | 0+1/0 | 24310 | ARCHIVE
burn_reset_20260927/flash50/s2-02.md | receipt | nodate | 0+1/0 | 13235 | ARCHIVE
burn_reset_20260927/flash50/s2-03.md | receipt | nodate | 0+1/0 | 18049 | ARCHIVE
burn_reset_20260927/flash50/s2-05.md | finding | nodate | 0+1/0 | 8118 | ARCHIVE
burn_reset_20260927/flash50/s2-06.md | receipt | 2026-09-28 | 0+1/0 | 16725 | ARCHIVE
burn_reset_20260927/flash50/s2-07.md | receipt | nodate | 0+1/0 | 4538 | ARCHIVE
burn_reset_20260927/flash50/s2-08.md | receipt | 2026-09-28 | 0+1/0 | 15842 | ARCHIVE
burn_reset_20260927/flash50/s2-09.md | receipt | nodate | 0+1/0 | 16799 | ARCHIVE
burn_reset_20260927/flash50/s2-10.md | receipt | nodate | 0+1/0 | 15910 | ARCHIVE
burn_reset_20260927/flash50/s2-11.md | finding | 2026-09-28 | 0+1/0 | 15265 | ARCHIVE
burn_reset_20260927/flash50/s2-12.md | receipt | nodate | 0+1/0 | 11660 | ARCHIVE
burn_reset_20260927/flash50/s2-13.md | receipt | 2026-09-28 | 0+1/0 | 4834 | ARCHIVE
burn_reset_20260927/flash50/s2-14.md | receipt | 2026-09-28 | 0+1/0 | 9593 | ARCHIVE
burn_reset_20260927/flash50/s2-15.md | receipt | 2026-09-28 | 0+1/0 | 5791 | ARCHIVE
burn_reset_20260927/flash50/s2-17.md | receipt | nodate | 0+1/0 | 12224 | ARCHIVE
burn_reset_20260927/flash50/s2-18.md | finding | nodate | 0+1/0 | 61566 | ARCHIVE
burn_reset_20260927/flash50/s2-20.md | receipt | nodate | 0+1/0 | 11514 | ARCHIVE
burn_reset_20260927/flash50/s2-21.md | receipt | nodate | 0+1/0 | 3840 | ARCHIVE
burn_reset_20260927/flash50/s2-24.md | receipt | 2026-09-28 | 0+1/0 | 15107 | ARCHIVE
burn_reset_20260927/flash50/secret-gate-gaps.md | receipt | 2026-09-28 | 0+1/0 | 16725 | ARCHIVE
burn_reset_20260927/flash50/secrets-census.md | finding | 2026-09-28 | 0+1/0 | 97157 | REVIEW
burn_reset_20260927/flash50/seed-gaps.md | receipt | nodate | 0+1/0 | 11514 | ARCHIVE
burn_reset_20260927/flash50/sess-01.md | receipt | 2026-09-28 | 1+1/0 | 12214 | KEEP
burn_reset_20260927/flash50/sess-02.md | receipt | 2026-09-28 | 0+1/0 | 21252 | ARCHIVE
burn_reset_20260927/flash50/sess-03.md | receipt | 2026-09-28 | 0+1/0 | 18410 | ARCHIVE
burn_reset_20260927/flash50/sess-04.md | receipt | nodate | 0+1/0 | 17440 | ARCHIVE
burn_reset_20260927/flash50/sess-06.md | receipt | 2026-09-28 | 0+1/0 | 7438 | ARCHIVE
burn_reset_20260927/flash50/silent-pass-census.md | finding | 2026-09-28 | 0+1/0 | 1859370 | REVIEW
burn_reset_20260927/flash50/skill-census.md | finding | 2026-09-28 | 0+1/0 | 18940 | REVIEW
burn_reset_20260927/flash50/skill-liveness.md | receipt | 2026-09-28 | 0+1/0 | 16324 | ARCHIVE
burn_reset_20260927/flash50/stealth-sw-01.md | finding | nodate | 0+1/0 | 14663 | ARCHIVE
burn_reset_20260927/flash50/stealth-sw-02.md | finding | nodate | 0+1/0 | 12115 | ARCHIVE
burn_reset_20260927/flash50/stealth-sw-04.md | finding | nodate | 0+1/0 | 11880 | ARCHIVE
burn_reset_20260927/flash50/steering-pipeline-map.md | finding | 2026-09-28 | 0+1/0 | 15139 | REVIEW
burn_reset_20260927/flash50/task-census.md | finding | 2026-09-28 | 0+1/0 | 9993 | REVIEW
burn_reset_20260927/flash50/test-health.md | finding | 2026-09-28 | 0+1/0 | 39098 | ARCHIVE
burn_reset_20260927/flash50/todo-census.md | finding | 2026-09-28 | 0+1/0 | 91838 | REVIEW
burn_reset_20260927/flash50/todo-triage.md | receipt | 2026-09-28 | 0+1/0 | 13458 | ARCHIVE
burn_reset_20260927/flash50/w3-bare-spawn-sweep.md | receipt | 2026-09-28 | 0+1/0 | 3990 | ARCHIVE
burn_reset_20260927/flash50/w3-dirac-loop7.md | receipt | 2026-09-28 | 0+1/0 | 10475 | ARCHIVE
burn_reset_20260927/flash50/w3-fossil-genome.md | finding | 2026-09-28 | 0+1/0 | 10878 | ARCHIVE
burn_reset_20260927/flash50/w3-mirror-design.md | receipt | 2026-09-28 | 0+1/0 | 3329 | ARCHIVE
burn_reset_20260927/flash50/w3-mirror-oral.md | receipt | 2026-09-28 | 0+1/0 | 14107 | ARCHIVE
burn_reset_20260927/flash50/w3-mirror-x-kg.md | finding | 2026-09-28 | 0+1/0 | 10172 | ARCHIVE
burn_reset_20260927/flash50/w3-quantizer-theory.md | finding | 2026-09-28 | 0+1/0 | 21709 | ARCHIVE
burn_reset_20260927/flash50/w3-research-cachemech.md | finding | 2026-09-28 | 0+1/0 | 19072 | ARCHIVE
burn_reset_20260927/flash50/w3-research-memai.md | finding | 2026-09-28 | 0+1/0 | 19815 | ARCHIVE
burn_reset_20260927/flash50/w3-research-selfplay.md | finding | 2026-09-28 | 0+1/0 | 15387 | ARCHIVE
burn_reset_20260927/flash50/w3-research-swarm-scale.md | finding | 2026-09-28 | 0+1/0 | 12030 | ARCHIVE
burn_reset_20260927/flash50/w3-theater-audit.md | receipt | 2026-09-28 | 0+1/0 | 15932 | ARCHIVE
burn_reset_20260927/flash50/w4-03.md | receipt | nodate | 0+1/0 | 15148 | ARCHIVE
burn_reset_20260927/flash50/w4-05.md | receipt | nodate | 0+1/0 | 18711 | ARCHIVE
burn_reset_20260927/flash50/w4-06.md | receipt | nodate | 0+1/0 | 16344 | ARCHIVE
burn_reset_20260927/flash50/w4-epistemic-gap.md | receipt | nodate | 0+1/0 | 18711 | ARCHIVE
burn_reset_20260927/flash50/work/bnb_readme.md | receipt | nodate | 0+2/0 | 8266 | ARCHIVE
burn_reset_20260927/flash50/work/quantization.md | receipt | nodate | 36+86/0 | 14 | KEEP
burn_reset_20260927/flash50/work/vulkan_readme.md | receipt | nodate | 0+2/0 | 14 | ARCHIVE
burn_reset_20260927/healthz.md | receipt | 2026-09-27 | 2+8/0 | 2082 | KEEP
burn_reset_20260927/mirror_intro.md | receipt | 2026-09-27 | 1+4/0 | 2979 | KEEP
burn_reset_20260927/no_win.md | receipt | 2026-09-27 | 20+15/0 | 3657 | KEEP
burn_reset_20260927/pack_modes.md | receipt | 2026-09-27 | 4+4/0 | 3602 | KEEP
burn_reset_20260927/probe20_live.md | finding | 2026-09-27 | 1+2/0 | 3729 | KEEP
burn_reset_20260927/queue/FW32_weave_next5.md | receipt | 2026-09-28 | 0+1/0 | 7239 | ARCHIVE
burn_reset_20260927/queue/FW33_era_weave.md | brief | 2026-09-28 | 0+1/0 | 19152 | ARCHIVE
burn_reset_20260927/queue/FW34_cubes_parable.md | brief | 2026-09-28 | 0+1/0 | 5768 | ARCHIVE
burn_reset_20260927/queue/FW35_adventurelearn.md | brief | 2026-09-28 | 0+1/0 | 5833 | ARCHIVE
burn_reset_20260927/queue/FW36_ractor_stubs.md | brief | 2026-09-28 | 0+1/0 | 5767 | ARCHIVE
burn_reset_20260927/queue/FW38_wallwalkers.md | brief | 2026-09-28 | 0+1/0 | 5390 | ARCHIVE
burn_reset_20260927/queue/FW39_monastery_docs.md | brief | 2026-09-28 | 0+1/0 | 5710 | ARCHIVE
burn_reset_20260927/queue/FW40_ascension_balance.md | brief | 2026-09-28 | 0+1/0 | 4174 | ARCHIVE
burn_reset_20260927/queue/FW41_adam_questions.md | receipt | 2026-09-28 | 0+1/0 | 5801 | ARCHIVE
burn_reset_20260927/queue/FW42_netlify_preflight.md | brief | 2026-09-28 | 0+1/0 | 3570 | ARCHIVE
burn_reset_20260927/queue/Q-001.md | receipt | 2026-09-28 | 2+4/1 | 7026 | KEEP
burn_reset_20260927/queue/Q-002.md | brief | 2026-09-28 | 6+3/1 | 5323 | KEEP
burn_reset_20260927/queue/Q-003.md | receipt | 2026-09-28 | 2+2/1 | 5200 | KEEP
burn_reset_20260927/queue/Q-005.md | brief | 2026-09-28 | 1+1/1 | 3576 | KEEP
burn_reset_20260927/queue/Q-007.md | receipt | 2026-09-28 | 1+1/1 | 5158 | KEEP
burn_reset_20260927/queue/Q-008.md | brief | 2026-09-28 | 3+2/1 | 8318 | KEEP
burn_reset_20260927/queue/Q-009.md | brief | 2026-09-28 | 3+3/1 | 8034 | KEEP
burn_reset_20260927/queue/Q-010.md | brief | 2026-09-28 | 2+2/1 | 5230 | KEEP
burn_reset_20260927/queue/Q-011.md | brief | 2026-09-28 | 5+2/1 | 5628 | KEEP
burn_reset_20260927/queue/Q-020.md | receipt | 2026-09-28 | 1+4/0 | 4126 | KEEP
burn_reset_20260927/queue/Q-020_FW01_harness_trio.md | brief | 2026-09-28 | 0+1/0 | 4530 | ARCHIVE
burn_reset_20260927/queue/Q-020_FW02_referee_chain.md | receipt | 2026-09-28 | 0+1/0 | 2082 | ARCHIVE
burn_reset_20260927/queue/Q-020_FW03_grounding_verify.md | brief | 2026-09-28 | 0+1/0 | 4147 | ARCHIVE
burn_reset_20260927/queue/Q-020_FW04_void_prep.md | brief | 2026-09-28 | 0+1/0 | 4788 | ARCHIVE
burn_reset_20260927/queue/Q-020_FW05_sampler_closure.md | receipt | 2026-09-28 | 0+3/0 | 5457 | ARCHIVE
burn_reset_20260927/queue/Q-021.md | receipt | 2026-09-28 | 1+2/0 | 5390 | KEEP
burn_reset_20260927/queue/Q-022.md | receipt | 2026-09-28 | 2+2/0 | 7963 | KEEP
burn_reset_20260927/queue/Q-023.md | receipt | 2026-09-28 | 1+2/1 | 3057 | KEEP
burn_reset_20260927/queue/Q-024.md | receipt | 2026-09-28 | 1+2/0 | 5494 | KEEP
burn_reset_20260927/queue/Q-025.md | brief | 2026-09-28 | 1+1/0 | 6830 | KEEP
burn_reset_20260927/queue/Q-026.md | brief | 2026-09-28 | 1+2/0 | 5752 | KEEP
burn_reset_20260927/queue/Q-027.md | receipt | 2026-09-28 | 1+3/0 | 6450 | KEEP
burn_reset_20260927/queue/Q-028.md | receipt | 2026-09-28 | 1+2/0 | 11101 | KEEP
burn_reset_20260927/queue/Q-030.md | brief | 2026-09-28 | 2+3/1 | 3377 | KEEP
burn_reset_20260927/queue/Q-031.md | brief | 2026-09-28 | 3+3/1 | 7166 | KEEP
burn_reset_20260927/queue/Q-032.md | brief | 2026-09-28 | 1+1/0 | 9735 | KEEP
burn_reset_20260927/queue/Q-033.md | brief | 2026-09-28 | 1+2/1 | 9291 | KEEP
burn_reset_20260927/queue/Q-034.md | receipt | 2026-09-28 | 1+2/1 | 5023 | KEEP
burn_reset_20260927/queue/Q-036.md | brief | 2026-09-28 | 3+2/1 | 5003 | KEEP
burn_reset_20260927/queue/Q-037.md | brief | 2026-09-28 | 1+1/1 | 4931 | KEEP
burn_reset_20260927/queue/Q-039.md | receipt | 2026-09-28 | 2+1/1 | 7987 | KEEP
burn_reset_20260927/queue/Q-040.md | brief | 2026-09-28 | 2+1/1 | 6699 | KEEP
burn_reset_20260927/queue/Q-041.md | brief | 2026-09-28 | 1+2/1 | 5304 | KEEP
burn_reset_20260927/queue/Q-042.md | receipt | 2026-09-28 | 1+2/1 | 7842 | KEEP
burn_reset_20260927/queue/Q-043.md | brief | 2026-09-28 | 2+1/1 | 9303 | KEEP
burn_reset_20260927/queue/Q-047.md | brief | 2026-09-28 | 1+3/1 | 28444 | KEEP
burn_reset_20260927/queue/Q-048.md | brief | 2026-09-28 | 1+1/1 | 11352 | KEEP
burn_reset_20260927/queue/Q-049.md | brief | 2026-09-28 | 4+2/1 | 6295 | KEEP
burn_reset_20260927/queue/Q-050.md | receipt | 2026-09-28 | 1+5/1 | 4970 | KEEP
burn_reset_20260927/substrate.md | receipt | 2026-09-27 | 123+329/1 | 2837 | KEEP
burn_reset_20260927/work/drift_q033_inclusionai_ling-3.0-flash-vl.md | finding | 2026-09-28 | 0+1/0 | 1569 | ARCHIVE
burn_reset_20260927/work/drift_q033_meta_muse-glimmer-30b.md | finding | 2026-09-28 | 0+1/0 | 1271 | ARCHIVE
burn_reset_20260927/work/drift_q033_stealth_space-bunny-alpha.md | finding | 2026-09-28 | 0+1/0 | 11417 | ARCHIVE
burn_reset_20260927/work/fan2_belady-lruk_meta_muse-glimmer-30b.md | finding | 2026-09-28 | 0+2/0 | 1621 | ARCHIVE
burn_reset_20260927/work/fan2_belt-cube-real_inclusionai_ling-3.0-flash-vl.md | finding | 2026-09-28 | 0+2/0 | 3418 | ARCHIVE
burn_reset_20260927/work/fan2_contrastive-wm_inclusionai_ling-3.0-flash-vl.md | receipt | 2026-09-28 | 0+2/0 | 5125 | ARCHIVE
burn_reset_20260927/work/fan2_eam-tracking_meta_muse-glimmer-30b.md | finding | 2026-09-28 | 0+2/0 | 2117 | ARCHIVE
burn_reset_20260927/work/fan2_headless-agent-cli_inclusionai_ling-3.0-flash-vl.md | receipt | 2026-09-28 | 0+2/0 | 2515 | ARCHIVE
burn_reset_20260927/work/fan2_moe-hotswap_meta_muse-glimmer-30b.md | finding | 2026-09-28 | 0+1/0 | 924 | ARCHIVE
burn_reset_20260927/work/fan2_or-cache-mechanics_meta_muse-glimmer-30b.md | finding | 2026-09-28 | 0+1/0 | 913 | ARCHIVE
burn_reset_20260927/work/fan2_solomonoff-pretrain_inclusionai_ling-3.0-flash-vl.md | receipt | 2026-09-28 | 0+1/0 | 1331 | ARCHIVE
burn_reset_20260927/work/fan2_vortex-latent_meta_muse-glimmer-30b.md | finding | 2026-09-28 | 0+1/0 | 1324 | ARCHIVE
burn_reset_20260927/work/fan2_water-plasma_inclusionai_ling-3.0-flash-vl.md | finding | 2026-09-28 | 0+1/0 | 5113 | ARCHIVE
burn_reset_20260927/work/fan_auk-voice_meta_muse-glimmer-30b.md | finding | 2026-09-27 | 0+2/0 | 947 | ARCHIVE
burn_reset_20260927/work/fan_belt-cube-real_z-ai_glm-5.3-prime.md | receipt | 2026-09-27 | 0+2/0 | 171 | ARCHIVE
burn_reset_20260927/work/fan_eam-tracking_qwen_qwen3.8-max-prime.md | receipt | 2026-09-27 | 0+2/0 | 118 | ARCHIVE
burn_reset_20260927/work/fan_moe-hotswap_stealth_space-bunny-alpha.md | finding | 2026-09-27 | 0+2/0 | 120 | ARCHIVE
burn_reset_20260927/work/fan_or-cache-mechanics_stealth_space-bunny-alpha.md | finding | 2026-09-27 | 0+2/0 | 127 | ARCHIVE
burn_reset_20260927/work/fan_selfplay-sota_inclusionai_ling-3.0-flash-vl.md | finding | 2026-09-27 | 0+2/0 | 2527 | ARCHIVE
burn_reset_20260927/work/fan_solomonoff-pretrain_gpt-4o-mini.md | receipt | 2026-09-27 | 0+1/0 | 164 | ARCHIVE
burn_reset_20260927/work/fan_vortex-latent_meta_muse-spark-1.3.md | receipt | 2026-09-27 | 0+1/0 | 164 | ARCHIVE
burn_reset_20260927/work/fan_water-plasma_meta_muse-spark-1.2.md | receipt | 2026-09-27 | 0+1/0 | 163 | ARCHIVE
burn_reset_20260927/work/lib-belady-1966_hermes.md | receipt | 2026-09-27 | 0+2/0 | 1875 | ARCHIVE
burn_reset_20260927/work/lib-belady-1966_nous1.md | finding | 2026-09-28 | 0+1/0 | 3761 | ARCHIVE
burn_reset_20260927/work/lib-belady-1966_nous2.md | finding | 2026-09-28 | 0+1/0 | 1379 | ARCHIVE
burn_reset_20260927/work/lib-belady-1966_nous3.md | finding | 2026-09-27 | 0+2/0 | 1188 | ARCHIVE
burn_reset_20260927/work/lib-belady-1966_nous4.md | finding | 2026-09-28 | 0+1/0 | 1372 | ARCHIVE
burn_reset_20260927/work/lib-belady-1966_openrouter1.md | finding | 2026-09-28 | 0+2/0 | 1468 | ARCHIVE
burn_reset_20260927/work/lib-belady-1966_openrouter2.md | finding | 2026-09-28 | 0+1/0 | 1012 | ARCHIVE
burn_reset_20260927/work/lib-belady-1966_openrouter3.md | finding | 2026-09-28 | 0+2/0 | 1981 | ARCHIVE
burn_reset_20260927/work/lib-belady-1966_openrouter4.md | finding | 2026-09-28 | 0+2/0 | 983 | ARCHIVE
burn_wave_20260926/B2_01_the50_punch_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4327 | ARCHIVE
burn_wave_20260926/B2_02_writer_debt_20260926.md | receipt | 2026-09-26 | 0+3/0 | 3944 | ARCHIVE
burn_wave_20260926/B2_03_endpoint_news_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4210 | ARCHIVE
burn_wave_20260926/B2_04_provider_health_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3996 | ARCHIVE
burn_wave_20260926/B2_05_drift_pairs_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4478 | ARCHIVE
burn_wave_20260926/B2_06_link_dupes_20260926.md | receipt | 2026-09-26 | 1+4/0 | 4387 | KEEP
burn_wave_20260926/B2_07_grounding_20260926.md | receipt | 2026-09-26 | 2+3/0 | 3788 | KEEP
burn_wave_20260926/B2_08_judge_lane_20260926.md | receipt | 2026-09-26 | 2+3/0 | 4526 | KEEP
burn_wave_20260926/B2_09_prompt_uplift_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4400 | ARCHIVE
burn_wave_20260926/B2_100_flip_receipt_card_20260926.md | receipt | 2026-09-26 | 0+7/1 | 9090 | KEEP
burn_wave_20260926/B2_101_seed330_papers_20260926.md | receipt | 2026-09-26 | 0+5/1 | 7874 | KEEP
burn_wave_20260926/B2_102_fts5_wiring_20260926.md | receipt | 2026-09-26 | 2+5/1 | 9418 | KEEP
burn_wave_20260926/B2_103_path_census_20260926.md | receipt | 2026-09-26 | 1+3/0 | 11742 | KEEP
burn_wave_20260926/B2_104_freshness_policy_20260926.md | receipt | 2026-09-26 | 0+3/0 | 7528 | ARCHIVE
burn_wave_20260926/B2_105_mistral_surgery_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4986 | ARCHIVE
burn_wave_20260926/B2_106_probe_cadence_20260926.md | receipt | 2026-09-26 | 1+2/0 | 7132 | KEEP
burn_wave_20260926/B2_107_ollama_trap_20260926.md | receipt | 2026-09-26 | 1+2/0 | 8355 | KEEP
burn_wave_20260926/B2_108_commit_gate_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4024 | ARCHIVE
burn_wave_20260926/B2_109_rbxlx_armor_20260926.md | receipt | 2026-09-26 | 0+3/0 | 5382 | ARCHIVE
burn_wave_20260926/B2_10_playtest_prereg_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4357 | ARCHIVE
burn_wave_20260926/B2_110_mudbasecamp_wisp_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4209 | ARCHIVE
burn_wave_20260926/B2_111_gate_verdict_v2_wiring_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5212 | ARCHIVE
burn_wave_20260926/B2_112_v1_v2_escalation_reconcile_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3850 | ARCHIVE
burn_wave_20260926/B2_113_cascade_falsifier_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5264 | ARCHIVE
burn_wave_20260926/B2_114_groq_third_lane_20260926.md | receipt | 2026-09-26 | 0+2/0 | 6771 | ARCHIVE
burn_wave_20260926/B2_115_probe_chain_freeze_20260926.md | receipt | 2026-09-26 | 0+2/0 | 2629 | ARCHIVE
burn_wave_20260926/B2_116_groq_nonchat_classification_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3781 | ARCHIVE
burn_wave_20260926/B2_117_error_class_census_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5972 | ARCHIVE
burn_wave_20260926/B2_118_first_pass_erratum_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4576 | ARCHIVE
burn_wave_20260926/B2_119_ifexpr_balance_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5115 | ARCHIVE
burn_wave_20260926/B2_11_mimosa_close_20260926.md | receipt | 2026-09-26 | 3+2/0 | 4817 | KEEP
burn_wave_20260926/B2_120_playtest_lint_headline_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3098 | ARCHIVE
burn_wave_20260926/B2_122_canonical_first_filing_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3295 | ARCHIVE
burn_wave_20260926/B2_123_scout_charter_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3095 | ARCHIVE
burn_wave_20260926/B2_124_paste_door_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5856 | ARCHIVE
burn_wave_20260926/B2_125_bridge_go_blocked_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4450 | ARCHIVE
burn_wave_20260926/B2_126_laptop_bootstrap_20260926.md | receipt | 2026-09-26 | 0+2/0 | 2734 | ARCHIVE
burn_wave_20260926/B2_128_key_persist_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4495 | ARCHIVE
burn_wave_20260926/B2_129_gemini_bearer_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3857 | ARCHIVE
burn_wave_20260926/B2_12_caption_ledger_20260926.md | receipt | 2026-09-26 | 0+6/1 | 4920 | KEEP
burn_wave_20260926/B2_130_steering_selfsteal_20260926.md | receipt | 2026-09-26 | 0+3/0 | 6971 | ARCHIVE
burn_wave_20260926/B2_131_steering_failures_20260926.md | receipt | 2026-09-26 | 0+2/0 | 7211 | ARCHIVE
burn_wave_20260926/B2_132_steering_fold_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4146 | ARCHIVE
burn_wave_20260926/B2_133_cerebras_purge_20260926.md | receipt | 2026-09-26 | 8+3/0 | 7664 | KEEP
burn_wave_20260926/B2_134_key_inventory_truth_sweep_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4385 | ARCHIVE
burn_wave_20260926/B2_137_vault_pack_register_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3357 | ARCHIVE
burn_wave_20260926/B2_138_retention_law_20260926.md | receipt | 2026-09-26 | 0+4/1 | 6471 | KEEP
burn_wave_20260926/B2_139_ask3_repair_20260926.md | receipt | 2026-09-26 | 0+3/0 | 7266 | ARCHIVE
burn_wave_20260926/B2_13_scenario_cards_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3864 | ARCHIVE
burn_wave_20260926/B2_140_armc_closeout_20260926.md | receipt | 2026-09-26 | 0+3/0 | 3304 | ARCHIVE
burn_wave_20260926/B2_142_cerebras_dig_20260926.md | receipt | 2026-09-26 | 0+3/0 | 13659 | ARCHIVE
burn_wave_20260926/B2_143_card_trial_sweep_20260926.md | receipt | 2026-09-26 | 0+3/0 | 6084 | ARCHIVE
burn_wave_20260926/B2_144_cache_model_map_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5578 | ARCHIVE
burn_wave_20260926/B2_145_phantom_paths_20260926.md | receipt | 2026-09-26 | 1+4/1 | 4175 | KEEP
burn_wave_20260926/B2_146_unregistered_files_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4355 | ARCHIVE
burn_wave_20260926/B2_147_writer_poison_guard_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5879 | ARCHIVE
burn_wave_20260926/B2_148_seal_hook_seq_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4146 | ARCHIVE
burn_wave_20260926/B2_149_norminbox_root_strip_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5014 | ARCHIVE
burn_wave_20260926/B2_14_qdrop874_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4622 | ARCHIVE
burn_wave_20260926/B2_150_blocked_line_delta_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4880 | ARCHIVE
burn_wave_20260926/B2_151_pid_survivor_20260926.md | receipt | 2026-09-26 | 0+3/0 | 10664 | ARCHIVE
burn_wave_20260926/B2_152_ractor_panel_spec_20260926.md | receipt | 2026-09-26 | 0+3/0 | 3169 | ARCHIVE
burn_wave_20260926/B2_153_seedrib_steal_dig_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4986 | ARCHIVE
burn_wave_20260926/B2_155_seed_paired_harness_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4868 | ARCHIVE
burn_wave_20260926/B2_156_living_hash_law_20260926.md | receipt | 2026-09-26 | 0+3/1 | 4008 | KEEP
burn_wave_20260926/B2_157_prefix_case_20260926.md | receipt | 2026-09-26 | 0+4/1 | 4225 | KEEP
burn_wave_20260926/B2_158_games_history_20260926.md | receipt | 2026-09-26 | 0+2/0 | 6922 | ARCHIVE
burn_wave_20260926/B2_159_physcomp_gstd_fresheyes_20260926.md | receipt | 2026-09-26 | 0+2/0 | 7527 | ARCHIVE
burn_wave_20260926/B2_15_xintel_dig_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4201 | ARCHIVE
burn_wave_20260926/B2_160_ledger_c8_check_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4131 | ARCHIVE
burn_wave_20260926/B2_161_events_drift_policy_20260926.md | receipt | 2026-09-26 | 0+3/0 | 2807 | ARCHIVE
burn_wave_20260926/B2_162_g1_tripwire_20260926.md | receipt | 2026-09-26 | 1+2/0 | 7337 | KEEP
burn_wave_20260926/B2_163_law12_register_20260926.md | receipt | 2026-09-26 | 0+5/1 | 8596 | KEEP
burn_wave_20260926/B2_164_scenarios_gate_20260926.md | receipt | 2026-09-26 | 0+3/0 | 11040 | ARCHIVE
burn_wave_20260926/B2_165_asekin_ledger_20260926.md | receipt | 2026-09-26 | 0+4/1 | 7236 | KEEP
burn_wave_20260926/B2_166_rubric_scoring_20260926.md | receipt | 2026-09-26 | 1+3/0 | 10047 | KEEP
burn_wave_20260926/B2_167_queue_dedupe_20260926.md | receipt | 2026-09-26 | 0+5/1 | 8191 | KEEP
burn_wave_20260926/B2_168_event_split_gate_20260926.md | receipt | 2026-09-26 | 1+2/0 | 6896 | KEEP
burn_wave_20260926/B2_169_research_event_pointers_20260926.md | receipt | 2026-09-26 | 0+2/0 | 2467 | ARCHIVE
burn_wave_20260926/B2_16_uf_sweep_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4216 | ARCHIVE
burn_wave_20260926/B2_170_imprint_deck_denominator_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3828 | ARCHIVE
burn_wave_20260926/B2_171_xpost_source_convention_20260926.md | receipt | 2026-09-26 | 0+2/0 | 2552 | ARCHIVE
burn_wave_20260926/B2_172_image_drop_schema_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4735 | ARCHIVE
burn_wave_20260926/B2_173_l265_flag_20260926.md | receipt | 2026-09-26 | 3+2/0 | 8172 | KEEP
burn_wave_20260926/B2_174_p3_falsifier_sharpen_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3633 | ARCHIVE
burn_wave_20260926/B2_175_shadowledger_datastore_leg_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4131 | ARCHIVE
burn_wave_20260926/B2_176_disposition_durability_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4535 | ARCHIVE
burn_wave_20260926/B2_177_nous_cell_erratum_20260926.md | receipt | 2026-09-26 | 0+2/0 | 2421 | ARCHIVE
burn_wave_20260926/B2_178_caption_census.md | receipt | 2026-09-27 | 0+2/0 | 1329 | ARCHIVE
burn_wave_20260926/B2_178_corpus_prune_report.md | receipt | 2026-09-27 | 0+2/0 | 4767 | ARCHIVE
burn_wave_20260926/B2_178_freelane_runner_20260926.md | receipt | 2026-09-26 | 0+2/0 | 6421 | ARCHIVE
burn_wave_20260926/B2_179_dogfood_meters_20260926.md | receipt | 2026-09-26 | 0+1/0 | 5984 | ARCHIVE
burn_wave_20260926/B2_17_adventure2d6_20260926.md | receipt | 2026-09-26 | 0+4/0 | 4358 | ARCHIVE
burn_wave_20260926/B2_180_seed_rib_v0_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4266 | ARCHIVE
burn_wave_20260926/B2_181_seed_mcp_20260926.md | receipt | 2026-09-26 | 0+3/0 | 8718 | ARCHIVE
burn_wave_20260926/B2_182_free_tier_power_users_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5765 | ARCHIVE
burn_wave_20260926/B2_183_cool_shit_people_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4711 | ARCHIVE
burn_wave_20260926/B2_184_corpus_path_seam_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3719 | ARCHIVE
burn_wave_20260926/B2_186_uf122_eval_20260926.md | receipt | 2026-09-26 | 0+3/0 | 5407 | ARCHIVE
burn_wave_20260926/B2_188_transport_tripwire_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4819 | ARCHIVE
burn_wave_20260926/B2_189_retirement_body_parser_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4039 | ARCHIVE
burn_wave_20260926/B2_18_stone2b_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4892 | ARCHIVE
burn_wave_20260926/B2_190_past_2p53_seq_forms_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5634 | ARCHIVE
burn_wave_20260926/B2_191_queue_drift_flap_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5761 | ARCHIVE
burn_wave_20260926/B2_192_verdict_store_amend_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4732 | ARCHIVE
burn_wave_20260926/B2_193_spotcheck_protocol_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4324 | ARCHIVE
burn_wave_20260926/B2_194_gemini_native_kind_20260926.md | receipt | 2026-09-26 | 0+2/0 | 6195 | ARCHIVE
burn_wave_20260926/B2_195_express_quota_block_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3711 | ARCHIVE
burn_wave_20260926/B2_197_living_census_20260926.md | receipt | 2026-09-26 | 0+5/1 | 4642 | KEEP
burn_wave_20260926/B2_198_owed_receipt_20260926.md | receipt | 2026-09-26 | 0+4/1 | 4222 | KEEP
burn_wave_20260926/B2_199_patrol_living_20260926.md | receipt | 2026-09-26 | 0+4/1 | 4464 | KEEP
burn_wave_20260926/B2_19_improve_backlog_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4689 | ARCHIVE
burn_wave_20260926/B2_200_lawD_fold_check_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5863 | ARCHIVE
burn_wave_20260926/B2_201_dspy_optimizer_sweep_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4382 | ARCHIVE
burn_wave_20260926/B2_202_free_rotation_20260926.md | receipt | 2026-09-26 | 0+3/0 | 5698 | ARCHIVE
burn_wave_20260926/B2_203_ledger_freshness_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3569 | ARCHIVE
burn_wave_20260926/B2_204_dormant_skip_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3609 | ARCHIVE
burn_wave_20260926/B2_205_quorum_selfvote_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4235 | ARCHIVE
burn_wave_20260926/B2_206_judge_independence_20260926.md | receipt | 2026-09-26 | 0+2/0 | 6553 | ARCHIVE
burn_wave_20260926/B2_207_producer_family_record_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4272 | ARCHIVE
burn_wave_20260926/B2_208_staleness_tripwire_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5575 | ARCHIVE
burn_wave_20260926/B2_209_regime_gate_split_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4069 | ARCHIVE
burn_wave_20260926/B2_20_loop_gaps_20260926.md | receipt | 2026-09-26 | 1+3/0 | 4003 | KEEP
burn_wave_20260926/B2_211_patrol_cron_charter_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4644 | ARCHIVE
burn_wave_20260926/B2_213_fullscan_report_resync_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3454 | ARCHIVE
burn_wave_20260926/B2_214_dungeon_census_20260926.md | receipt | 2026-09-26 | 0+5/1 | 5627 | KEEP
burn_wave_20260926/B2_215_census_tripwire_20260926.md | receipt | 2026-09-26 | 0+4/1 | 5987 | KEEP
burn_wave_20260926/B2_216_collect_delta_20260926.md | receipt | 2026-09-26 | 1+4/0 | 7044 | KEEP
burn_wave_20260926/B2_217_w40_verify_20260926.md | receipt | 2026-09-26 | 0+3/0 | 8018 | ARCHIVE
burn_wave_20260926/B2_218_fragile_aligned_vocabulary_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4591 | ARCHIVE
burn_wave_20260926/B2_219_misdate_classes_20260926.md | receipt | 2026-09-26 | 2+2/0 | 6475 | KEEP
burn_wave_20260926/B2_21_doctor_probe_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4540 | ARCHIVE
burn_wave_20260926/B2_220_dotted_guards_20260926.md | receipt | 2026-09-26 | 1+2/0 | 7378 | KEEP
burn_wave_20260926/B2_221_prefix_editor_20260926.md | receipt | 2026-09-26 | 0+4/1 | 8741 | KEEP
burn_wave_20260926/B2_222_hot_living_20260926.md | receipt | 2026-09-26 | 0+2/0 | 7014 | ARCHIVE
burn_wave_20260926/B2_223_mimo_living_20260926.md | receipt | 2026-09-26 | 0+2/0 | 6350 | ARCHIVE
burn_wave_20260926/B2_224_w40_stamp_board_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3814 | ARCHIVE
burn_wave_20260926/B2_225_drift_alarm_tripwire_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4818 | ARCHIVE
burn_wave_20260926/B2_226_aging_guard_board_test_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3910 | ARCHIVE
burn_wave_20260926/B2_227_walk_compare_rescan_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4172 | ARCHIVE
burn_wave_20260926/B2_228_margin_erratum_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4248 | ARCHIVE
burn_wave_20260926/B2_229_audit_seed_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4141 | ARCHIVE
burn_wave_20260926/B2_22_fts5_spike_20260926.md | receipt | 2026-09-26 | 3+3/0 | 3886 | KEEP
burn_wave_20260926/B2_230_assignment_law_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4488 | ARCHIVE
burn_wave_20260926/B2_231_deepseek_truncation_erratum_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3662 | ARCHIVE
burn_wave_20260926/B2_233_qnum_dropno_map_20260926.md | receipt | 2026-09-26 | 0+2/0 | 6546 | ARCHIVE
burn_wave_20260926/B2_234_wave2_batch1_reaudit_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5046 | ARCHIVE
burn_wave_20260926/B2_235_mimo_revival_20260926.md | receipt | 2026-09-26 | 0+3/0 | 10630 | ARCHIVE
burn_wave_20260926/B2_236_mimo_retest_20260926.md | receipt | 2026-09-26 | 1+3/0 | 9311 | KEEP
burn_wave_20260926/B2_237_touch_law_20260926.md | receipt | 2026-09-26 | 0+4/1 | 7546 | KEEP
burn_wave_20260926/B2_238_checkbox_law_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5681 | ARCHIVE
burn_wave_20260926/B2_239_line_endings_20260926.md | receipt | 2026-09-26 | 1+3/0 | 8230 | KEEP
burn_wave_20260926/B2_23_seed_flip_card_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4249 | ARCHIVE
burn_wave_20260926/B2_240_b2_219_reconcile_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4929 | ARCHIVE
burn_wave_20260926/B2_242_quantity_bounds_20260926.md | receipt | 2026-09-26 | 2+2/0 | 9859 | KEEP
burn_wave_20260926/B2_243_bucket_audit_20260926.md | receipt | 2026-09-26 | 2+2/0 | 13723 | KEEP
burn_wave_20260926/B2_244_collect_deep_20260926.md | receipt | 2026-09-26 | 0+3/0 | 8034 | ARCHIVE
burn_wave_20260926/B2_244_guard_pin_20260926.md | receipt | 2026-09-26 | 0+2/0 | 9135 | ARCHIVE
burn_wave_20260926/B2_245_parser_order_20260926.md | receipt | 2026-09-26 | 1+4/1 | 6603 | KEEP
burn_wave_20260926/B2_246_collect_schedule_20260926.md | receipt | 2026-09-26 | 0+3/0 | 9873 | ARCHIVE
burn_wave_20260926/B2_247_collect_gap_20260926.md | receipt | 2026-09-26 | 0+5/1 | 11078 | KEEP
burn_wave_20260926/B2_248_module_split_20260926.md | receipt | 2026-09-26 | 0+2/0 | 8153 | ARCHIVE
burn_wave_20260926/B2_249_shape_law_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5804 | ARCHIVE
burn_wave_20260926/B2_24_carrier_scan_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4906 | ARCHIVE
burn_wave_20260926/B2_250_file_claims_20260926.md | receipt | 2026-09-26 | 0+2/0 | 7075 | ARCHIVE
burn_wave_20260926/B2_251_checkbox_audit_20260926.md | receipt | 2026-09-26 | 0+3/0 | 9865 | ARCHIVE
burn_wave_20260926/B2_252_error_capture_20260926.md | receipt | 2026-09-26 | 0+2/0 | 9070 | ARCHIVE
burn_wave_20260926/B2_253_transport_decision_20260926.md | receipt | 2026-09-26 | 0+3/0 | 8898 | ARCHIVE
burn_wave_20260926/B2_254_living_regression_20260926.md | receipt | 2026-09-26 | 0+4/1 | 14921 | KEEP
burn_wave_20260926/B2_255_double_spend_20260926.md | receipt | 2026-09-26 | 0+2/0 | 29286 | ARCHIVE
burn_wave_20260926/B2_256_class_pin_20260926.md | receipt | 2026-09-26 | 0+2/0 | 11292 | ARCHIVE
burn_wave_20260926/B2_257_year_ladder_20260926.md | receipt | 2026-09-26 | 2+2/0 | 10636 | KEEP
burn_wave_20260926/B2_258_yearfirst_20260926.md | receipt | 2026-09-26 | 2+2/0 | 11153 | KEEP
burn_wave_20260926/B2_259_pin_law_20260926.md | receipt | 2026-09-26 | 1+2/0 | 8460 | KEEP
burn_wave_20260926/B2_25_envelope_remeasure_20260926.md | receipt | 2026-09-26 | 2+4/0 | 4148 | KEEP
burn_wave_20260926/B2_260_verifier_gate_20260926.md | receipt | 2026-09-26 | 0+5/1 | 9540 | KEEP
burn_wave_20260926/B2_261_mimo_watch_arm_20260926.md | receipt | 2026-09-26 | 1+3/0 | 3838 | KEEP
burn_wave_20260926/B2_262_quantity_adjacency_probe_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5569 | ARCHIVE
burn_wave_20260926/B2_263_dash_noun_audit_20260926.md | receipt | 2026-09-26 | 1+2/0 | 5360 | KEEP
burn_wave_20260926/B2_264_links_seal_recovery_20260926.md | receipt | 2026-09-26 | 0+2/0 | 6027 | ARCHIVE
burn_wave_20260926/B2_265_seat_links_refile_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4804 | ARCHIVE
burn_wave_20260926/B2_266_no_erratum_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4954 | ARCHIVE
burn_wave_20260926/B2_267_touch_law_patrol_prompt_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4290 | ARCHIVE
burn_wave_20260926/B2_269_serve_decline_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3832 | ARCHIVE
burn_wave_20260926/B2_26_links_sha_backfill_20260926.md | receipt | 2026-09-26 | 1+2/0 | 4747 | KEEP
burn_wave_20260926/B2_271_qcaption_verify_beat_20260926.md | receipt | 2026-09-26 | 1+3/0 | 2902 | KEEP
burn_wave_20260926/B2_272_prepush_paths_helper_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3357 | ARCHIVE
burn_wave_20260926/B2_273_ratchet_growth_law_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4351 | ARCHIVE
burn_wave_20260926/B2_274_carrier_ownership_law_20260926.md | receipt | 2026-09-26 | 0+2/0 | 6359 | ARCHIVE
burn_wave_20260926/B2_275_pin_law_check7_fail_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3848 | ARCHIVE
burn_wave_20260926/B2_277_blind_exit_split_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4962 | ARCHIVE
burn_wave_20260926/B2_279_sort_totality_20260926.md | receipt | 2026-09-26 | 1+5/1 | 14406 | KEEP
burn_wave_20260926/B2_27_scout_checkgate_20260926.md | receipt | 2026-09-26 | 0+3/0 | 3802 | ARCHIVE
burn_wave_20260926/B2_280_seq_band_20260926.md | receipt | 2026-09-26 | 0+4/1 | 11564 | KEEP
burn_wave_20260926/B2_281_yearfirst_keeper_pin_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3080 | ARCHIVE
burn_wave_20260926/B2_282_yearmonth_sweep_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3439 | ARCHIVE
burn_wave_20260926/B2_284_claim_tests_extension_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4517 | ARCHIVE
burn_wave_20260926/B2_286_null_model_refuse_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3450 | ARCHIVE
burn_wave_20260926/B2_288_test_debt_cure_20260926.md | receipt | 2026-09-26 | 0+2/0 | 7104 | ARCHIVE
burn_wave_20260926/B2_28_schema_split_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4091 | ARCHIVE
burn_wave_20260926/B2_290_live_dead_child_proof_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3360 | ARCHIVE
burn_wave_20260926/B2_291_estate_mcp_docker_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4778 | ARCHIVE
burn_wave_20260926/B2_292_drift_patrol_living_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4831 | ARCHIVE
burn_wave_20260926/B2_294_register_sha_fix_20260926.md | receipt | 2026-09-26 | 1+2/0 | 3409 | KEEP
burn_wave_20260926/B2_295_openrouter_free_rotation_20260926.md | receipt | 2026-09-26 | 0+3/0 | 3468 | ARCHIVE
burn_wave_20260926/B2_296_mistral_keys_20260926.md | receipt | 2026-09-26 | 0+2/0 | 7745 | ARCHIVE
burn_wave_20260926/B2_297_living_downgrade_detector_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3582 | ARCHIVE
burn_wave_20260926/B2_298_patrol_persistence_20260926.md | receipt | 2026-09-26 | 0+2/0 | 7511 | ARCHIVE
burn_wave_20260926/B2_299_fold_verify_cwd_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3515 | ARCHIVE
burn_wave_20260926/B2_29_rbxlx_rebuild_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3095 | ARCHIVE
burn_wave_20260926/B2_300_handoff_kernel_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4086 | ARCHIVE
burn_wave_20260926/B2_301_normals/seatA.md | receipt | 2026-09-27 | 0+1/0 | 23575 | ARCHIVE
burn_wave_20260926/B2_301_normals/seatA.rerun.md | receipt | 2026-09-27 | 0+1/0 | 26231 | ARCHIVE
burn_wave_20260926/B2_301_normals/seatB.md | finding | 2026-09-27 | 0+2/0 | 28635 | ARCHIVE
burn_wave_20260926/B2_301_normals/seatB.rerun.md | finding | 2026-09-27 | 0+1/0 | 38310 | ARCHIVE
burn_wave_20260926/B2_301_sections/adventure_2d6__seatA.md | finding | 2026-09-27 | 0+1/0 | 3732 | ARCHIVE
burn_wave_20260926/B2_301_sections/adventure_2d6__seatA.rerun.md | finding | 2026-09-27 | 0+1/0 | 3732 | ARCHIVE
burn_wave_20260926/B2_301_sections/adventure_2d6__seatB.md | finding | 2026-09-27 | 0+1/0 | 3661 | ARCHIVE
burn_wave_20260926/B2_301_sections/adventure_2d6__seatB.rerun.md | finding | 2026-09-27 | 0+1/0 | 3492 | ARCHIVE
burn_wave_20260926/B2_301_sections/audit_dungeon__seatA.md | finding | 2026-09-27 | 0+1/0 | 4727 | REVIEW
burn_wave_20260926/B2_301_sections/audit_dungeon__seatA.rerun.md | finding | 2026-09-27 | 0+1/0 | 4727 | REVIEW
burn_wave_20260926/B2_301_sections/audit_dungeon__seatB.md | receipt | 2026-09-27 | 0+1/0 | 5501 | ARCHIVE
burn_wave_20260926/B2_301_sections/audit_dungeon__seatB.rerun.md | finding | 2026-09-27 | 0+1/0 | 7175 | REVIEW
burn_wave_20260926/B2_301_sections/fractal_maze__seatA.md | receipt | 2026-09-27 | 0+1/0 | 3774 | ARCHIVE
burn_wave_20260926/B2_301_sections/fractal_maze__seatA.rerun.md | finding | 2026-09-27 | 0+1/0 | 4568 | ARCHIVE
burn_wave_20260926/B2_301_sections/fractal_maze__seatB.md | finding | 2026-09-27 | 0+1/0 | 3948 | ARCHIVE
burn_wave_20260926/B2_301_sections/fractal_maze__seatB.rerun.md | finding | 2026-09-27 | 0+1/0 | 3636 | ARCHIVE
burn_wave_20260926/B2_301_sections/riddler_engram__seatA.md | finding | 2026-09-27 | 0+1/0 | 3288 | ARCHIVE
burn_wave_20260926/B2_301_sections/riddler_engram__seatA.rerun.md | finding | 2026-09-27 | 0+1/0 | 4070 | ARCHIVE
burn_wave_20260926/B2_301_sections/riddler_engram__seatB.md | receipt | 2026-09-27 | 0+1/0 | 6611 | ARCHIVE
burn_wave_20260926/B2_301_sections/riddler_engram__seatB.rerun.md | receipt | 2026-09-27 | 0+1/0 | 8861 | ARCHIVE
burn_wave_20260926/B2_301_sections/riddler_optics__seatA.md | receipt | 2026-09-27 | 0+1/0 | 5279 | ARCHIVE
burn_wave_20260926/B2_301_sections/riddler_optics__seatA.rerun.md | receipt | 2026-09-27 | 0+1/0 | 6352 | ARCHIVE
burn_wave_20260926/B2_301_sections/riddler_optics__seatB.md | receipt | 2026-09-27 | 0+1/0 | 5404 | ARCHIVE
burn_wave_20260926/B2_301_sections/riddler_optics__seatB.rerun.md | receipt | 2026-09-27 | 0+1/0 | 6344 | ARCHIVE
burn_wave_20260926/B2_301_sections/water_computer__seatA.md | receipt | 2026-09-27 | 0+1/0 | 2699 | ARCHIVE
burn_wave_20260926/B2_301_sections/water_computer__seatA.rerun.md | receipt | 2026-09-27 | 0+1/0 | 2699 | ARCHIVE
burn_wave_20260926/B2_301_sections/water_computer__seatB.md | finding | 2026-09-27 | 0+1/0 | 3434 | ARCHIVE
burn_wave_20260926/B2_301_sections/water_computer__seatB.rerun.md | finding | 2026-09-27 | 0+1/0 | 8719 | ARCHIVE
burn_wave_20260926/B2_301_tri_stage/version_deepseek.md | finding | 2026-09-27 | 2+7/0 | 38310 | KEEP
burn_wave_20260926/B2_301_tri_stage/version_grok.md | receipt | 2026-09-27 | 2+6/0 | 26231 | KEEP
burn_wave_20260926/B2_302_truncation_guard_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3395 | ARCHIVE
burn_wave_20260926/B2_303_one_error_named_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4047 | ARCHIVE
burn_wave_20260926/B2_306_cipher_pin_20260926.md | receipt | 2026-09-26 | 1+2/0 | 4449 | KEEP
burn_wave_20260926/B2_307_mimo_failure_classes_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3237 | ARCHIVE
burn_wave_20260926/B2_308_mimo_error_headers_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5365 | ARCHIVE
burn_wave_20260926/B2_309_queue_registration_reseal_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4340 | ARCHIVE
burn_wave_20260926/B2_30_shadowledger_live_20260926.md | receipt | 2026-09-26 | 1+2/0 | 3915 | KEEP
burn_wave_20260926/B2_310_attribution_audit_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5502 | ARCHIVE
burn_wave_20260926/B2_311_drop_year_clause_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5165 | ARCHIVE
burn_wave_20260926/B2_312_post_drop_ts_rejected_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5119 | ARCHIVE
burn_wave_20260926/B2_314_census_liveness_tripwire_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3993 | ARCHIVE
burn_wave_20260926/B2_316_checkbox_gate_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4807 | ARCHIVE
burn_wave_20260926/B2_318_pytest_port_batteries_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3369 | ARCHIVE
burn_wave_20260926/B2_31_poll_tripwire_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4088 | ARCHIVE
burn_wave_20260926/B2_320_driver_v2_S1_S3_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4013 | ARCHIVE
burn_wave_20260926/B2_322_gap_denominator_refresh_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3599 | ARCHIVE
burn_wave_20260926/B2_323_dated_numbers_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4962 | ARCHIVE
burn_wave_20260926/B2_324_sibling_headline_sweep_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3897 | ARCHIVE
burn_wave_20260926/B2_325_thoughtbank_preflight_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4266 | ARCHIVE
burn_wave_20260926/B2_326_qlora_smoke_owed_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4308 | ARCHIVE
burn_wave_20260926/B2_327_transport_precheck_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4474 | ARCHIVE
burn_wave_20260926/B2_328_refold_gate_20260926.md | receipt | 2026-09-26 | 0+3/0 | 10116 | ARCHIVE
burn_wave_20260926/B2_329_dump_strip_20260926.md | receipt | 2026-09-26 | 1+2/0 | 10714 | KEEP
burn_wave_20260926/B2_32_cascade_wire_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4314 | ARCHIVE
burn_wave_20260926/B2_330_junction_diff_20260926.md | receipt | 2026-09-26 | 0+3/0 | 3991 | ARCHIVE
burn_wave_20260926/B2_332_catalog_refresh_decision_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4010 | ARCHIVE
burn_wave_20260926/B2_333_index_selfseal_decision_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3472 | ARCHIVE
burn_wave_20260926/B2_335_testborn_candidate_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4471 | ARCHIVE
burn_wave_20260926/B2_336_conftest_gap_gate_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3458 | ARCHIVE
burn_wave_20260926/B2_337_ghost_resolve_20260926.md | receipt | 2026-09-26 | 0+2/0 | 11657 | ARCHIVE
burn_wave_20260926/B2_338_case_fix_20260926.md | receipt | 2026-09-26 | 1+5/1 | 8313 | KEEP
burn_wave_20260926/B2_33_rejection_recount_20260926.md | receipt | 2026-09-26 | 1+2/0 | 4374 | KEEP
burn_wave_20260926/B2_340_prompt_cache_matrix_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4835 | ARCHIVE
burn_wave_20260926/B2_341_secret_scan_papers_20260926.md | receipt | 2026-09-26 | 0+4/0 | 5973 | ARCHIVE
burn_wave_20260926/B2_342_schema_registry_20260926.md | receipt | 2026-09-26 | 2+2/0 | 8291 | KEEP
burn_wave_20260926/B2_343_restore_guard_20260926.md | receipt | 2026-09-26 | 1+2/0 | 10915 | KEEP
burn_wave_20260926/B2_344_dangling_disposition_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5834 | ARCHIVE
burn_wave_20260926/B2_345_lifecycle_reason_carry_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5345 | ARCHIVE
burn_wave_20260926/B2_346_flip_link_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4220 | ARCHIVE
burn_wave_20260926/B2_349_rotation_owed_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4045 | ARCHIVE
burn_wave_20260926/B2_34_cluster_detectors_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4603 | ARCHIVE
burn_wave_20260926/B2_351_secret_scan_schedule_20260926.md | receipt | 2026-09-26 | 1+4/0 | 3458 | KEEP
burn_wave_20260926/B2_352_stragglers_20260926.md | receipt | 2026-09-26 | 0+3/0 | 9472 | ARCHIVE
burn_wave_20260926/B2_353_shell_pin_20260926.md | receipt | 2026-09-26 | 0+2/0 | 7356 | ARCHIVE
burn_wave_20260926/B2_354_icon_honesty_20260926.md | receipt | 2026-09-26 | 0+2/0 | 6435 | ARCHIVE
burn_wave_20260926/B2_355_checkbox_reaudit_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3364 | ARCHIVE
burn_wave_20260926/B2_357_scout_pin_20260926.md | receipt | 2026-09-26 | 2+2/0 | 7394 | KEEP
burn_wave_20260926/B2_358_env_tripwire_20260926.md | receipt | 2026-09-26 | 2+4/1 | 8618 | KEEP
burn_wave_20260926/B2_359_writer_census_20260926.md | receipt | 2026-09-26 | 0+3/0 | 10856 | ARCHIVE
burn_wave_20260926/B2_35_groq_surgery_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4045 | ARCHIVE
burn_wave_20260926/B2_360_fkb_process_lock_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4107 | ARCHIVE
burn_wave_20260926/B2_361_fkb_verify_tripwire_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5371 | ARCHIVE
burn_wave_20260926/B2_362_fkb_log_search_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3725 | ARCHIVE
burn_wave_20260926/B2_363_prefix_pairing_pins_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4502 | ARCHIVE
burn_wave_20260926/B2_365_census_patrol_split_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5283 | ARCHIVE
burn_wave_20260926/B2_366_register_overrun_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3860 | ARCHIVE
burn_wave_20260926/B2_367_media_register_scope_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3929 | ARCHIVE
burn_wave_20260926/B2_36_cerebras_reclassify_20260926.md | receipt | 2026-09-26 | 1+2/0 | 4416 | KEEP
burn_wave_20260926/B2_372_chain_census_20260926.md | receipt | 2026-09-26 | 2+2/0 | 7271 | KEEP
burn_wave_20260926/B2_373_stanza_pin_20260926.md | receipt | 2026-09-26 | 1+7/1 | 8936 | KEEP
burn_wave_20260926/B2_374_behavioral_pin_20260926.md | receipt | 2026-09-26 | 2+2/0 | 11909 | KEEP
burn_wave_20260926/B2_375_powershell_tokens_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4755 | ARCHIVE
burn_wave_20260926/B2_377_unescape_20260926.md | receipt | 2026-09-26 | 0+2/0 | 9454 | ARCHIVE
burn_wave_20260926/B2_378_fold_outcome_20260926.md | receipt | 2026-09-26 | 1+2/0 | 8588 | KEEP
burn_wave_20260926/B2_37_provider_health_close_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4162 | ARCHIVE
burn_wave_20260926/B2_380_minter_key_pins_20260926.md | receipt | 2026-09-26 | 0+2/0 | 2968 | ARCHIVE
burn_wave_20260926/B2_382_shell_resolution_pins_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3774 | ARCHIVE
burn_wave_20260926/B2_383_chain_quote_pin_20260926.md | receipt | 2026-09-26 | 2+2/0 | 7854 | KEEP
burn_wave_20260926/B2_384_real_chains_20260926.md | receipt | 2026-09-26 | 0+2/0 | 9486 | ARCHIVE
burn_wave_20260926/B2_385_caption_sha_promotion_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4778 | ARCHIVE
burn_wave_20260926/B2_386_refetch_probe_20260926.md | receipt | 2026-09-26 | 0+3/0 | 3568 | ARCHIVE
burn_wave_20260926/B2_387_canary_marker_root_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5232 | ARCHIVE
burn_wave_20260926/B2_388_stale_tip_writer_hunt_20260926.md | receipt | 2026-09-26 | 0+3/0 | 6719 | ARCHIVE
burn_wave_20260926/B2_389_selftests_namespace_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3429 | ARCHIVE
burn_wave_20260926/B2_392_hot_writer_attributed_20260926.md | receipt | 2026-09-26 | 0+2/0 | 6573 | ARCHIVE
burn_wave_20260926/B2_393_chain_byte_exact_io_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4103 | ARCHIVE
burn_wave_20260926/B2_394_lifecycle_writer_identity_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4705 | ARCHIVE
burn_wave_20260926/B2_396_mag_tasks_whitelist_20260926.md | receipt | 2026-09-26 | 1+2/0 | 3653 | KEEP
burn_wave_20260926/B2_399_shared_surface_split_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4736 | ARCHIVE
burn_wave_20260926/B2_401_trail_env_seams_20260926.md | receipt | 2026-09-26 | 0+2/0 | 6613 | ARCHIVE
burn_wave_20260926/B2_402_test_isolation_20260926.md | receipt | 2026-09-26 | 2+2/0 | 4602 | KEEP
burn_wave_20260926/B2_403_test_sinks_20260926.md | receipt | 2026-09-26 | 0+2/0 | 6021 | ARCHIVE
burn_wave_20260926/B2_404_canonical_numbering_guard_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5301 | ARCHIVE
burn_wave_20260926/B2_406_bridge_decouple_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4674 | ARCHIVE
burn_wave_20260926/B2_408_crash_write_surface_20260926.md | receipt | 2026-09-26 | 1+2/0 | 3100 | KEEP
burn_wave_20260926/B2_409_caption_sha_pin_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3848 | ARCHIVE
burn_wave_20260926/B2_40_fold_poison_guard_20260926.md | receipt | 2026-09-26 | 1+2/0 | 4669 | KEEP
burn_wave_20260926/B2_410_outcome_vocab_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3850 | ARCHIVE
burn_wave_20260926/B2_411_fold_training_surface_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4272 | ARCHIVE
burn_wave_20260926/B2_412_icon_drop_fold_pin_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3179 | ARCHIVE
burn_wave_20260926/B2_413_icon_drop_pins_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4810 | ARCHIVE
burn_wave_20260926/B2_414_icon_thread_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4124 | ARCHIVE
burn_wave_20260926/B2_416_stanza_census_20260926.md | receipt | 2026-09-26 | 1+2/0 | 4837 | KEEP
burn_wave_20260926/B2_418_chain_marker_pin_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4549 | ARCHIVE
burn_wave_20260926/B2_41_hash_freshness_20260926.md | receipt | 2026-09-26 | 0+5/1 | 4342 | KEEP
burn_wave_20260926/B2_420_census_seat_errors_20260926.md | receipt | 2026-09-26 | 1+2/0 | 3537 | KEEP
burn_wave_20260926/B2_421_caption_via_pin_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4229 | ARCHIVE
burn_wave_20260926/B2_422_declared_unresolvable_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5699 | ARCHIVE
burn_wave_20260926/B2_423_carrier_position_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3707 | ARCHIVE
burn_wave_20260926/B2_424_envelope_harvest_20260926.md | receipt | 2026-09-26 | 0+3/0 | 3428 | ARCHIVE
burn_wave_20260926/B2_425_operator_go_surface_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3756 | ARCHIVE
burn_wave_20260926/B2_426_decay_window_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5738 | ARCHIVE
burn_wave_20260926/B2_427_registry_append_only_20260926.md | receipt | 2026-09-26 | 0+3/0 | 3280 | ARCHIVE
burn_wave_20260926/B2_429_law_registry_index_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5493 | ARCHIVE
burn_wave_20260926/B2_42_events_hygiene_20260926.md | receipt | 2026-09-26 | 1+2/0 | 4744 | KEEP
burn_wave_20260926/B2_433_mimosa_sweep_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4458 | ARCHIVE
burn_wave_20260926/B2_435_width3_sweep_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3764 | ARCHIVE
burn_wave_20260926/B2_436_width15_validation_arm_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3440 | ARCHIVE
burn_wave_20260926/B2_438_scripts_path_pins_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5201 | ARCHIVE
burn_wave_20260926/B2_439_wave_driver_scheduling_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5006 | ARCHIVE
burn_wave_20260926/B2_440_hunger_ledger_pin_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5424 | ARCHIVE
burn_wave_20260926/B2_442_waves_mode_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4352 | ARCHIVE
burn_wave_20260926/B2_443_dwf_error_census_20260926.md | receipt | 2026-09-26 | 2+3/0 | 4899 | KEEP
burn_wave_20260926/B2_445_base_url_spec_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4306 | ARCHIVE
burn_wave_20260926/B2_448_post_link_recheck_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4197 | ARCHIVE
burn_wave_20260926/B2_449_flip_go_transcription_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3177 | ARCHIVE
burn_wave_20260926/B2_450_scenarios_commit_block_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5034 | ARCHIVE
burn_wave_20260926/B2_451_scenarios_hook_pins_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4634 | ARCHIVE
burn_wave_20260926/B2_452_scenario_citation_patrol_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4571 | ARCHIVE
burn_wave_20260926/B2_454_cache_rate_audit_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5069 | ARCHIVE
burn_wave_20260926/B2_456_line_pointer_sweep_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4003 | ARCHIVE
burn_wave_20260926/B2_457_doctor_403_arm_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3114 | ARCHIVE
burn_wave_20260926/B2_458_builder_pyc_audit_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3940 | ARCHIVE
burn_wave_20260926/B2_459_seed330_reply_draft_20260926.md | receipt | 2026-09-26 | 0+3/0 | 2463 | ARCHIVE
burn_wave_20260926/B2_462_asekin_carrier_scan_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3763 | ARCHIVE
burn_wave_20260926/B2_463_window_convention_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4221 | ARCHIVE
burn_wave_20260926/B2_464_caller_census_20260926.md | receipt | 2026-09-26 | 0+2/0 | 12376 | ARCHIVE
burn_wave_20260926/B2_465_rebuild_schedule_20260926.md | receipt | 2026-09-26 | 0+6/1 | 15218 | KEEP
burn_wave_20260926/B2_466_catalog_v4_rescan_decision_20260926.md | receipt | 2026-09-26 | 0+2/0 | 6191 | ARCHIVE
burn_wave_20260926/B2_467_pool_repull_20260926.md | receipt | 2026-09-26 | 0+5/1 | 13107 | KEEP
burn_wave_20260926/B2_468_oct3_check_20260926.md | receipt | 2026-09-26 | 0+4/1 | 12021 | KEEP
burn_wave_20260926/B2_469_dated_meters_20260926.md | receipt | 2026-09-26 | 0+2/0 | 9307 | ARCHIVE
burn_wave_20260926/B2_470_links_dedupe_merge_owed_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5749 | ARCHIVE
burn_wave_20260926/B2_471_caption_census_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3432 | ARCHIVE
burn_wave_20260926/B2_472_corpus_prune_report_20260926.md | receipt | 2026-09-26 | 0+1/0 | 4767 | ARCHIVE
burn_wave_20260926/B2_475_real_limits_20260926.md | receipt | 2026-09-26 | 0+3/0 | 7255 | ARCHIVE
burn_wave_20260926/B2_476_deep_compute_20260926.md | receipt | 2026-09-26 | 0+2/0 | 11525 | ARCHIVE
burn_wave_20260926/B2_476_envelope_contract_20260926.md | receipt | 2026-09-26 | 0+3/0 | 4976 | ARCHIVE
burn_wave_20260926/B2_477_sep29_p0_reverify_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3687 | ARCHIVE
burn_wave_20260926/B2_479_exposure_census_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4555 | ARCHIVE
burn_wave_20260926/B2_481_derived_pair_refresh_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3958 | ARCHIVE
burn_wave_20260926/B2_482_matched_copy_audit_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3764 | ARCHIVE
burn_wave_20260926/B2_484_law12_clause_verdict_20260926.md | receipt | 2026-09-26 | 0+4/0 | 3988 | ARCHIVE
burn_wave_20260926/B2_485_scenarios_verify_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4169 | ARCHIVE
burn_wave_20260926/B2_486_queue_dupes_gate_20260926.md | receipt | 2026-09-26 | 1+2/0 | 3765 | KEEP
burn_wave_20260926/B2_488_queue_row_normalizer_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3979 | ARCHIVE
burn_wave_20260926/B2_489_resolver_bound_20260926.md | receipt | 2026-09-26 | 1+2/0 | 9294 | KEEP
burn_wave_20260926/B2_490_baseurl_sweep_20260926.md | receipt | 2026-09-26 | 0+2/0 | 10555 | ARCHIVE
burn_wave_20260926/B2_491_pointer_rot_20260926.md | receipt | 2026-09-26 | 0+2/0 | 7799 | ARCHIVE
burn_wave_20260926/B2_492_snapshot_differ_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3449 | ARCHIVE
burn_wave_20260926/B2_493_probe_cadence_block_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4420 | ARCHIVE
burn_wave_20260926/B2_494_probe_alarm_surface_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3488 | ARCHIVE
burn_wave_20260926/B2_504_fts5_spike_guard_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5174 | ARCHIVE
burn_wave_20260926/B2_506_census_fossils_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3150 | ARCHIVE
burn_wave_20260926/B2_50_missing_triage_20260926.md | receipt | 2026-09-26 | 0+3/0 | 3927 | ARCHIVE
burn_wave_20260926/B2_51_autorun_autopsy_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4778 | ARCHIVE
burn_wave_20260926/B2_521_cerebras_stragglers_20260926.md | receipt | 2026-09-26 | 6+2/0 | 10479 | KEEP
burn_wave_20260926/B2_522_cost_truth_20260926.md | receipt | 2026-09-26 | 1+2/0 | 9400 | KEEP
burn_wave_20260926/B2_52_bridge_card_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4076 | ARCHIVE
burn_wave_20260926/B2_53_grok_fire_card_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5006 | ARCHIVE
burn_wave_20260926/B2_54_cron_arm_card_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4977 | ARCHIVE
burn_wave_20260926/B2_55_buildlane_flip_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4254 | ARCHIVE
burn_wave_20260926/B2_56_returncode_law_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4257 | ARCHIVE
burn_wave_20260926/B2_57_uf_promotion_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4134 | ARCHIVE
burn_wave_20260926/B2_58_prompt_amendments_20260926.md | receipt | 2026-09-26 | 0+2/0 | 5098 | ARCHIVE
burn_wave_20260926/B2_59_miprov2_dig_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4586 | ARCHIVE
burn_wave_20260926/B2_60_judge_independence_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4681 | ARCHIVE
burn_wave_20260926/B2_61_roster_purge_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4646 | ARCHIVE
burn_wave_20260926/B2_62_zai_backoff_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4608 | ARCHIVE
burn_wave_20260926/B2_63_gemini_auth_20260926.md | receipt | 2026-09-26 | 0+4/0 | 4821 | ARCHIVE
burn_wave_20260926/B2_64_drift_dashboard_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4185 | ARCHIVE
burn_wave_20260926/B2_65_registry_revival_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4030 | ARCHIVE
burn_wave_20260926/B2_66_aging_guard_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4818 | ARCHIVE
burn_wave_20260926/B2_67_qvision_fixes_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4278 | ARCHIVE
burn_wave_20260926/B2_68_fraction_guard_20260926.md | receipt | 2026-09-26 | 1+2/0 | 4112 | KEEP
burn_wave_20260926/B2_69_test_census_20260926.md | receipt | 2026-09-26 | 2+4/1 | 4449 | KEEP
burn_wave_20260926/B2_70_referee_refresh_20260926.md | receipt | 2026-09-26 | 0+2/0 | 3832 | ARCHIVE
burn_wave_20260926/B2_71_hill_build_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4586 | ARCHIVE
burn_wave_20260926/B2_71_sections/V0_control__seatA.md | finding | 2026-09-27 | 0+1/0 | 2715 | ARCHIVE
burn_wave_20260926/B2_71_sections/V0_control__seatA.rerun.md | finding | 2026-09-27 | 0+1/0 | 3249 | ARCHIVE
burn_wave_20260926/B2_71_sections/V0_control__seatB.md | finding | 2026-09-27 | 0+1/0 | 3790 | ARCHIVE
burn_wave_20260926/B2_71_sections/V0_control__seatB.rerun.md | finding | 2026-09-27 | 0+1/0 | 3598 | ARCHIVE
burn_wave_20260926/B2_71_sections/V1_facts_first__seatA.md | finding | 2026-09-27 | 0+1/0 | 1535 | ARCHIVE
burn_wave_20260926/B2_71_sections/V1_facts_first__seatA.rerun.md | finding | 2026-09-27 | 0+1/0 | 1423 | ARCHIVE
burn_wave_20260926/B2_71_sections/V1_facts_first__seatB.md | finding | 2026-09-27 | 0+1/0 | 1166 | ARCHIVE
burn_wave_20260926/B2_71_sections/V1_facts_first__seatB.rerun.md | finding | 2026-09-27 | 0+1/0 | 1270 | ARCHIVE
burn_wave_20260926/B2_71_sections/V2_glossary__seatA.md | finding | 2026-09-27 | 0+1/0 | 3164 | ARCHIVE
burn_wave_20260926/B2_71_sections/V2_glossary__seatA.rerun.md | finding | 2026-09-27 | 0+1/0 | 3863 | ARCHIVE
burn_wave_20260926/B2_71_sections/V2_glossary__seatB.md | finding | 2026-09-27 | 0+1/0 | 4278 | ARCHIVE
burn_wave_20260926/B2_71_sections/V2_glossary__seatB.rerun.md | finding | 2026-09-27 | 0+1/0 | 3310 | ARCHIVE
burn_wave_20260926/B2_72_order_sensitivity_20260926.md | receipt | 2026-09-26 | 1+2/0 | 4348 | KEEP
burn_wave_20260926/B2_73_secret_scan_20260926.md | receipt | 2026-09-26 | 0+4/0 | 7063 | ARCHIVE
burn_wave_20260926/B2_74_qlora_recipe_20260926.md | receipt | 2026-09-26 | 0+2/0 | 8679 | ARCHIVE
burn_wave_20260926/B2_75_gardenfors_fetch_20260926.md | receipt | 2026-09-26 | 0+2/0 | 17164 | ARCHIVE
burn_wave_20260926/B2_75_jina_ch4.md | receipt | 2026-09-27 | 0+1/0 | 465 | ARCHIVE
burn_wave_20260926/B2_76_junction_policy_20260926.md | receipt | 2026-09-26 | 0+5/1 | 8465 | KEEP
burn_wave_20260926/B2_77_driver_v2_spec_20260926.md | receipt | 2026-09-26 | 2+4/1 | 9975 | KEEP
burn_wave_20260926/B2_78_denominator_refresh_20260926.md | receipt | 2026-09-26 | 0+4/1 | 13648 | KEEP
burn_wave_20260926/B2_79_pollution_fix_20260926.md | receipt | 2026-09-26 | 3+2/0 | 5217 | KEEP
burn_wave_20260926/B2_80_reason_carry_20260926.md | receipt | 2026-09-26 | 1+2/0 | 5246 | KEEP
burn_wave_20260926/B2_81_ollama_truth_20260926.md | receipt | 2026-09-26 | 1+4/1 | 6501 | KEEP
burn_wave_20260926/B2_82_verkle_reanchor_20260926.md | receipt | 2026-09-26 | 0+3/0 | 6315 | ARCHIVE
burn_wave_20260926/B2_83_flag_restore_20260926.md | receipt | 2026-09-26 | 0+2/0 | 7653 | ARCHIVE
burn_wave_20260926/B2_84_pile_drain_20260926.md | receipt | 2026-09-26 | 0+2/0 | 4666 | ARCHIVE
burn_wave_20260926/B2_85_powershell_fix_20260926.md | receipt | 2026-09-26 | 2+2/0 | 7283 | KEEP
burn_wave_20260926/B2_86_writer_isolation_20260926.md | receipt | 2026-09-26 | 3+2/0 | 7037 | KEEP
burn_wave_20260926/B2_87_fkb_continuity_20260926.md | receipt | 2026-09-26 | 0+2/0 | 11203 | ARCHIVE
burn_wave_20260926/B2_88_metadata_fetch_20260926.md | receipt | 2026-09-26 | 0+3/0 | 7409 | ARCHIVE
burn_wave_20260926/B2_89_hash_backfill_20260926.md | receipt | 2026-09-26 | 0+2/0 | 7074 | ARCHIVE
burn_wave_20260926/B2_90_album_captions_20260926.md | receipt | 2026-09-26 | 0+2/0 | 6512 | ARCHIVE
burn_wave_20260926/B2_92_qagg_sweep_20260926.md | receipt | 2026-09-26 | 0+3/0 | 8408 | ARCHIVE
burn_wave_20260926/B2_93_stego_erratum_20260926.md | receipt | 2026-09-26 | 0+3/0 | 9352 | ARCHIVE
burn_wave_20260926/B2_94_mimosa_tail_20260926.md | receipt | 2026-09-26 | 1+3/0 | 12233 | KEEP
burn_wave_20260926/B2_95_prune_gap_20260926.md | receipt | 2026-09-26 | 2+3/0 | 8228 | KEEP
burn_wave_20260926/B2_96_scripts_triage_20260926.md | receipt | 2026-09-26 | 2+3/0 | 9521 | KEEP
burn_wave_20260926/B2_97_width15_probe_20260926.md | receipt | 2026-09-26 | 0+2/0 | 9415 | ARCHIVE
burn_wave_20260926/B2_98_error_visibility_20260926.md | receipt | 2026-09-26 | 0+2/0 | 7052 | ARCHIVE
burn_wave_20260926/B2_99_fanout_reconcile_20260926.md | receipt | 2026-09-26 | 0+2/0 | 6186 | ARCHIVE
burn_wave_20260926/BOARD_REPAIR_INCIDENT_20260926.md | receipt | 2026-09-26 | 0+3/0 | 5309 | ARCHIVE
burn_wave_20260926/CLOSE_20260927_NOON.md | receipt | 2026-09-27 | 0+8/1 | 2908 | KEEP
burn_wave_20260926/DOGFLOOD_METERS_20260926.md | receipt | 2026-09-26 | 0+3/0 | 8243 | ARCHIVE
burn_wave_20260926/FREELANE_BURN_CLOSE_20260926_SMOKE.md | receipt | 2026-09-26 | 0+1/0 | 2728 | ARCHIVE
burn_wave_20260926/FREELANE_BURN_H14_SMOKE.md | finding | 2026-09-27 | 0+1/0 | 1263 | ARCHIVE
burn_wave_20260926/FREELANE_BURN_H15.md | finding | 2026-09-27 | 0+1/0 | 1287 | ARCHIVE
burn_wave_20260926/FREELANE_BURN_H16.md | finding | 2026-09-27 | 0+1/0 | 3692 | ARCHIVE
burn_wave_20260926/QUEUE.md | receipt | 2026-09-26 | 105+113/1 | 483723 | KEEP
deepseek_research/PIPELINE_PATTERN.md | finding | 2026-09-25 | 0+2/0 | 1827 | ARCHIVE
deepseek_research/deepseek_analysis_6tweets_20260923.md | finding | 2026-09-23 | 0+2/0 | 17311 | REVIEW
deepseek_research/mined/20260720T155500Z_what-is-the-ollama-project-homepage-prom.answer.local_analysis.md | finding | 2026-07-20 | 0+2/0 | 1362 | ARCHIVE
deepseek_research/mined/20260729T122057Z_deep-c-f368762f1e82.answer.remote_analysis.md | finding | 2026-07-29 | 0+1/0 | 223 | ARCHIVE
deepseek_research/mined/20260729T134347Z_deep-c-f368762f1e82.answer.local_analysis.md | finding | 2026-07-29 | 0+1/0 | 221 | ARCHIVE
deepseek_research/mined/20260729T134821Z_lattice-layer-five-step.answer.local_analysis.md | finding | 2026-07-29 | 0+1/0 | 229 | ARCHIVE
deepseek_research/mined/20260729T134938Z_lattice-url-3.answer.local_analysis.md | finding | 2026-07-29 | 0+1/0 | 209 | ARCHIVE
deepseek_research/mined/20260729T135051Z_lattice-url-4.answer.local_analysis.md | finding | 2026-07-29 | 0+1/0 | 209 | ARCHIVE
deepseek_research/mined/20260729T135140Z_lattice-url-5.answer.local_analysis.md | finding | 2026-07-29 | 0+1/0 | 209 | ARCHIVE
deepseek_research/mined/20260729T135201Z_lattice-url-6.answer.local_analysis.md | finding | 2026-07-29 | 0+1/0 | 209 | ARCHIVE
deepseek_research/mined/20260729T135209Z_lattice-url-7.answer.local_analysis.md | finding | 2026-07-29 | 0+1/0 | 8236 | ARCHIVE
deepseek_research/mined/20260729T135226Z_lattice-url-8.answer.local_analysis.md | finding | 2026-07-29 | 0+1/0 | 209 | ARCHIVE
deepseek_research/mined/20260729T135257Z_lattice-url-9.answer.local_analysis.md | finding | 2026-07-29 | 0+1/0 | 209 | ARCHIVE
deepseek_research/mined/20260729T135324Z_lattice-url-10.answer.local_analysis.md | finding | 2026-07-29 | 0+1/0 | 211 | ARCHIVE
deepseek_research/mined/20260729T135359Z_lattice-url-13.answer.local_analysis.md | finding | 2026-07-29 | 0+1/0 | 1867 | ARCHIVE
deepseek_research/mined/20260729T135427Z_lattice-url-14.answer.local_analysis.md | finding | 2026-07-29 | 0+1/0 | 211 | ARCHIVE
deepseek_research/mined/20260729T135504Z_lattice-url-15.answer.local_analysis.md | finding | 2026-07-29 | 0+1/0 | 211 | ARCHIVE
deepseek_research/mined/20260731T145433Z_steal-mag-native-contracts-only-not-pape.answer.local_analysis.md | finding | 2026-07-31 | 0+1/0 | 3527 | ARCHIVE
deepseek_research/mined/20260731T160538Z_deep-c-f368762f1e82.answer.local_analysis.md | finding | 2026-07-31 | 0+1/0 | 221 | ARCHIVE
deepseek_research/mined/20260731T160758Z_deep-c-8d7d551a16ee.answer.local_analysis.md | finding | 2026-07-31 | 0+1/0 | 221 | ARCHIVE
deepseek_research/mined/20260731T161032Z_deep-c-2fcab987a80f.answer.local_analysis.md | finding | 2026-07-31 | 0+1/0 | 221 | ARCHIVE
deepseek_research/mined/20260731T161312Z_deep-c-0b3cacba98e3.answer.local_analysis.md | finding | 2026-07-31 | 0+1/0 | 3413 | ARCHIVE
deepseek_research/mined/20260731T161530Z_blast-focus.answer.local_analysis.md | finding | 2026-07-31 | 0+2/0 | 6326 | ARCHIVE
deepseek_research/mined/20260731T162351Z_deep-c-f368762f1e82.answer.local_analysis.md | finding | 2026-07-31 | 0+1/0 | 221 | ARCHIVE
deepseek_research/mined/HYPOTHESIS_FILE_analysis.md | finding | 2026-09-25 | 0+1/0 | 175 | ARCHIVE
deepseek_research/mined/INTERNAL_JUDGE_LOOP_analysis.md | finding | 2026-09-25 | 0+1/0 | 183 | ARCHIVE
deepseek_research/mined/README_analysis.md | finding | 2026-09-25 | 0+2/0 | 2840 | ARCHIVE
deepseek_research/mined/REPORT_analysis.md | finding | 2026-09-25 | 0+1/0 | 157 | ARCHIVE
error_banner_MAP_20260913.md | finding | 2026-09-13 | 0+4/1 | 4154 | KEEP
fifty_wide_20260917/FW06_old_board.md | receipt | nodate | 0+1/0 | 1439 | ARCHIVE
fifty_wide_20260917/FW07_mcp_index.md | receipt | nodate | 1+1/0 | 1961 | KEEP
fifty_wide_20260917/FW08_census_selfrefs.md | receipt | nodate | 0+15/0 | 2196 | ARCHIVE
fifty_wide_20260917/FW08_census_selfrefs_lineage.md | receipt | nodate | 0+15/0 | 2996 | ARCHIVE
fifty_wide_20260917/FW09_mag_moves.md | receipt | nodate | 0+2/0 | 3138 | ARCHIVE
fifty_wide_20260917/FW10_vc2_amend.md | receipt | nodate | 1+1/0 | 1889 | KEEP
fifty_wide_20260917/FW11_fence_owners.md | receipt | nodate | 4+10/0 | 2382 | KEEP
fifty_wide_20260917/FW12_oldest_prose.md | receipt | nodate | 0+1/0 | 2867 | ARCHIVE
fifty_wide_20260917/FW13_wings.md | receipt | nodate | 0+2/0 | 1420 | ARCHIVE
fifty_wide_20260917/FW14_ghost_sample.md | receipt | nodate | 0+1/0 | 5687 | ARCHIVE
fifty_wide_20260917/FW19_patrol_debt_1_10.md | receipt | nodate | 0+1/1 | 3765 | KEEP
fifty_wide_20260917/FW20_fold_verify.md | receipt | nodate | 0+1/1 | 3338 | KEEP
fifty_wide_20260917/FW21_inbox_validate.md | receipt | nodate | 0+1/1 | 4471 | KEEP
fifty_wide_20260917/FW22_astra_persona.md | receipt | nodate | 0+1/0 | 11769 | ARCHIVE
fifty_wide_20260917/FW23_jev_steal.md | receipt | nodate | 0+1/0 | 6244 | ARCHIVE
fifty_wide_20260917/FW24_press_digest.md | receipt | nodate | 0+1/0 | 2313 | ARCHIVE
fifty_wide_20260917/FW25_selfthread.md | receipt | nodate | 0+1/0 | 4527 | ARCHIVE
fifty_wide_20260917/FW26_links_vks.md | receipt | nodate | 0+1/0 | 2866 | ARCHIVE
fifty_wide_20260917/FW27_publish_manifest.md | receipt | nodate | 0+1/0 | 5119 | ARCHIVE
fifty_wide_20260917/FW28_blind_hour.md | receipt | nodate | 0+1/0 | 4936 | ARCHIVE
fifty_wide_20260917/FW29_cube_assembly.md | receipt | nodate | 0+1/0 | 6082 | ARCHIVE
fifty_wide_20260917/FW30_discord_runbook.md | receipt | nodate | 0+1/0 | 4442 | ARCHIVE
fifty_wide_20260917/FW31_sep20_demo.md | receipt | nodate | 0+1/0 | 5402 | ARCHIVE
fifty_wide_20260917/FW37-42_INDEX.md | receipt | nodate | 0+0/0 | 1259 | ARCHIVE
fleet_research_lens/fleet-research-lens/README.md | finding | 2026-09-16 | 0+0/1 | 2140 | KEEP
fleet_research_lens/fleet-research-lens/discovery-excerpts.md | finding | 2026-09-16 | 0+2/0 | 62040 | ARCHIVE
fleet_research_lens/fleet-research-lens/evidence-excerpts.md | other | 2026-09-16 | 0+2/0 | 111053 | REVIEW
fleet_research_lens/fleet-research-lens/model-handoff.md | brief | 2026-09-16 | 0+1/0 | 5477 | ARCHIVE
fleet_research_lens/fleet-research-lens/orphans-and-connections.md | finding | 2026-09-16 | 0+2/0 | 40071 | ARCHIVE
fleet_research_lens/fleet-research-lens/prior/HOLD-3M-seal-package-v0.md | receipt | 2026-09-16 | 0+7/0 | 19260 | ARCHIVE
fleet_research_lens/fleet-research-lens/prior/effect-broker-contract-v0.md | receipt | 2026-09-16 | 1+8/0 | 23098 | KEEP
fleet_research_lens/fleet-research-lens/prior/ingestion-assay-v0.md | receipt | 2026-09-16 | 0+8/0 | 24927 | ARCHIVE
fleet_research_lens/fleet-research-lens/prior/sep16-kernel-verification.md | receipt | 2026-09-16 | 0+1/0 | 4722 | ARCHIVE
fleet_research_lens/fleet-research-lens/prior/sep16-qa-audit.md | receipt | 2026-09-16 | 0+2/0 | 10997 | ARCHIVE
fleet_research_lens/fleet-research-lens/prior/sep16-submission-review.md | finding | 2026-09-16 | 0+2/0 | 24683 | ARCHIVE
fleet_research_lens/fleet-research-lens/prior/sovereign-agent-systems-research-brief.md | brief | 2026-09-16 | 0+3/0 | 58495 | ARCHIVE
fleet_research_lens/fleet-research-lens/research-brief.md | brief | 2026-09-16 | 1+6/0 | 61335 | KEEP
fleet_research_lens/fleet-research-lens/research-program.md | finding | 2026-09-16 | 0+2/0 | 9874 | ARCHIVE
fleet_research_lens/fleet-research-lens/source-catalog.md | finding | 2026-09-16 | 0+1/0 | 15437 | ARCHIVE
full_blast_20260926/FULL_BLAST_20260926.md | receipt | 2026-09-26 | 0+5/1 | 5484 | KEEP
full_blast_20260926/L00_provider_probes_inline.md | finding | 2026-09-27 | 0+4/1 | 2088 | KEEP
full_blast_20260926/L01_omniroute.md | receipt | 2026-09-27 | 0+4/1 | 3264 | KEEP
full_blast_20260926/L02_cliproxyapi.md | receipt | 2026-09-27 | 0+4/1 | 2887 | KEEP
full_blast_20260926/L03_9router.md | receipt | 2026-09-27 | 0+4/1 | 2709 | KEEP
full_blast_20260926/L05_fle_u1_feasibility.md | receipt | 2026-09-27 | 0+4/1 | 3820 | KEEP
full_blast_20260926/L07_fivem_noir.md | receipt | 2026-09-27 | 0+4/1 | 3149 | KEEP
full_blast_20260926/L08_ue5_destruction.md | receipt | 2026-09-27 | 0+4/1 | 3915 | KEEP
full_blast_20260926/L09_gwap_literature.md | receipt | 2026-09-27 | 0+4/1 | 5567 | KEEP
full_blast_20260926/L10_memos_dreamscapes.md | brief | 2026-09-27 | 0+3/1 | 2830 | KEEP
full_blast_20260926/L11_provider_terms.md | receipt | 2026-09-27 | 0+4/1 | 2840 | KEEP
full_blast_20260926/PROVIDER_KEY_ASKS_20260926.md | receipt | 2026-09-26 | 0+2/1 | 1406 | KEEP
full_blast_20260926/W2_A_apb_burial.md | receipt | 2026-09-27 | 0+4/1 | 2939 | KEEP
full_blast_20260926/W2_B_small_debts.md | receipt | 2026-09-27 | 0+4/1 | 4069 | KEEP
full_blast_20260926/W2_L04_fcc_internals.md | receipt | 2026-09-27 | 0+4/1 | 5408 | KEEP
full_blast_20260926/W2_L06_teardown.md | receipt | 2026-09-27 | 0+4/1 | 4920 | KEEP
full_blast_20260926/WAVE_STATUS.md | receipt | 2026-09-27 | 0+4/1 | 1407 | KEEP
fullsend_s2/d23_mesh_findings_20260922.md | receipt | 2026-09-22 | 0+2/0 | 7108 | ARCHIVE
gala_20260925/AFTERPARTY_CLOSE_20260926.md | receipt | 2026-09-26 | 2+5/0 | 6407 | KEEP
gala_20260925/AFTERPARTY_QUEUE.md | receipt | 2026-09-26 | 0+4/0 | 5222 | ARCHIVE
gala_20260925/WAVE_STATE_GALA.md | receipt | 2026-09-25 | 1+3/0 | 15349 | KEEP
gala_20260925/afterparty/lanes/t43.species.md | finding | 2026-09-26 | 1+1/0 | 723 | KEEP
games_polish/p01-shadowbonk.md | finding | 2026-09-25 | 0+2/0 | 4068 | ARCHIVE
games_polish/p03-spectral-maze.md | finding | 2026-09-25 | 0+2/0 | 4083 | ARCHIVE
games_polish/p04-swarm.md | finding | 2026-09-25 | 0+2/0 | 4111 | ARCHIVE
games_polish/p05-shadow-walk.md | finding | 2026-09-25 | 0+2/0 | 4071 | ARCHIVE
games_polish/p06-wipeout-v2.md | finding | 2026-09-25 | 0+2/0 | 4137 | ARCHIVE
games_polish/p07-eraser-maze.md | finding | 2026-09-25 | 0+2/0 | 4111 | ARCHIVE
games_polish/p08-universe-within.md | finding | 2026-09-25 | 0+2/0 | 4125 | ARCHIVE
games_polish/p09-tavern-brawl.md | finding | 2026-09-25 | 0+2/0 | 4075 | ARCHIVE
games_polish/p10-bad-apple-field.md | finding | 2026-09-25 | 0+2/0 | 4100 | ARCHIVE
hive_operating_floor/CLAIMS.template.md | other | 2026-09-16 | 0+2/0 | 468 | REVIEW
hive_operating_floor/HIVE-OPERATING-FLOOR-U-1.2.0.md | receipt | 2026-09-16 | 0+2/0 | 3637 | ARCHIVE
hive_operating_floor/LAYERS.template.md | other | 2026-09-16 | 0+2/0 | 905 | REVIEW
hive_operating_floor/OPSEC.md | other | 2026-09-16 | 12+31/0 | 966 | REVIEW
hive_operating_floor/PLAN.md | finding | 2026-09-16 | 100+208/1 | 1003 | KEEP
hive_operating_floor/PROVENANCE.md | receipt | 2026-09-16 | 14+50/1 | 1296 | KEEP
hive_operating_floor/README-SHARE.md | other | 2026-09-16 | 0+2/0 | 360 | REVIEW
inbound/AOS_CFMBT_V5_SPEC_20260922.md | finding | 2026-09-22 | 0+2/0 | 15695 | REVIEW
inbound/DEEPSEEK_EIGHTWAVE_REPORT_20260921.md | receipt | 2026-09-21 | 0+4/1 | 2001 | KEEP
inbound/UNIVERSAL_LENS_SYNTHESIS_20260921.md | finding | 2026-09-21 | 0+4/1 | 2417 | KEEP
journal_mark_202609/DREAM_MYCELIUM_20260916.md | shitpost | 2026-09-16 | 0+3/0 | 2987 | ARCHIVE
journal_mark_202609/JOURNAL_20260914.md | shitpost | 2026-09-14 | 0+5/1 | 1237 | KEEP
journal_mark_202609/JOURNAL_20260915.md | shitpost | 2026-09-15 | 0+5/1 | 1134 | KEEP
journal_mark_202609/JOURNAL_20260916_ANSWERS.md | shitpost | 2026-09-16 | 0+4/0 | 2647 | ARCHIVE
journal_mark_202609/MAXIM_20260915.md | law | 2026-09-15 | 0+4/0 | 564 | PROMOTE
journal_mark_202609/PARABLE_OF_THE_AUDITOR_draft.md | shitpost | 2026-09-15 | 0+3/0 | 2428 | ARCHIVE
kvos_steal/BOT1_console_apis.md | receipt | 2026-09-14 | 0+2/0 | 6000 | ARCHIVE
kvos_steal/BOT2_visual_deck.md | receipt | 2026-09-14 | 0+2/0 | 6377 | ARCHIVE
kvos_steal/BOT3_organs.md | receipt | 2026-09-14 | 0+2/0 | 8958 | ARCHIVE
kvos_steal/BOT4_cards_data.md | finding | 2026-09-14 | 0+2/0 | 7424 | ARCHIVE
kvos_steal/BOT5_input_path.md | receipt | 2026-09-14 | 0+2/0 | 4688 | ARCHIVE
lens_20260927/ATTIC_ORPHAN_CENSUS.md | finding | 2026-09-27 | 1+3/0 | 9956 | KEEP
lens_20260927/DIRAC_GAPS_READ.md | receipt | 2026-09-27 | 0+3/0 | 6243 | ARCHIVE
lens_20260927/THE_LENS_20260927.md | finding | 2026-09-27 | 0+2/1 | 6868 | KEEP
lens_20260927/are_inventory.md | receipt | 2026-09-27 | 0+1/0 | 141719 | ARCHIVE
lens_20260927/did_census.md | finding | 2026-09-27 | 0+1/0 | 6773 | REVIEW
lens_20260927/doctrine_revisit.md | receipt | 2026-09-27 | 0+1/0 | 13723 | ARCHIVE
lens_20260927/external_links.md | receipt | 2026-09-27 | 0+3/0 | 14793 | ARCHIVE
method_card_exp/BATTERY.md | receipt | 2026-09-25 | 10+25/1 | 1248 | KEEP
method_card_exp/BATTERY_HELDOUT.md | receipt | 2026-09-25 | 2+2/0 | 2105 | KEEP
method_card_exp/CARD_V1.md | receipt | 2026-09-25 | 2+2/0 | 2817 | KEEP
method_card_exp/CARD_V2.md | receipt | 2026-09-25 | 0+2/0 | 7271 | ARCHIVE
method_card_exp/CONTROL_SHEET.md | finding | 2026-09-25 | 0+2/0 | 7221 | ARCHIVE
method_card_exp/GROUND_TRUTH_HELDOUT.md | finding | 2026-09-25 | 2+2/0 | 7963 | KEEP
method_card_exp/RERUN2_ANSWERS_20260926.md | receipt | 2026-09-26 | 0+1/0 | 6440 | ARCHIVE
method_card_exp/RERUN2_SCORE_20260926.md | receipt | 2026-09-26 | 0+1/0 | 4176 | ARCHIVE
method_card_exp/RERUN_ANSWERS_20260926.md | receipt | 2026-09-26 | 0+1/0 | 5400 | ARCHIVE
method_card_exp/RERUN_PREREG_20260926.md | finding | 2026-09-26 | 2+1/0 | 8923 | KEEP
method_card_exp/RERUN_SCORE_20260926.md | receipt | 2026-09-26 | 0+1/0 | 4048 | ARCHIVE
mickey/G2_1_recount.md | finding | 2026-09-14 | 0+2/0 | 6084 | ARCHIVE
mickey/G2_2_storefront_v3.md | receipt | 2026-09-14 | 0+2/0 | 9729 | ARCHIVE
mickey/G2_3_cocitation.md | finding | 2026-09-14 | 1+3/0 | 8875 | KEEP
mickey/G2_4_pulls.md | receipt | 2026-09-14 | 0+2/0 | 4965 | ARCHIVE
mickey/G2_5_feedback.md | receipt | 2026-09-14 | 0+2/0 | 3121 | ARCHIVE
mickey/G2_6_timing.md | finding | 2026-09-14 | 0+2/0 | 5048 | ARCHIVE
mickey/G2_7_sheet_v2.md | receipt | 2026-09-14 | 0+2/0 | 4540 | ARCHIVE
mickey/G3_1_cart_quality.md | receipt | 2026-09-14 | 0+2/0 | 9859 | ARCHIVE
mickey/G3_2_wireup.md | finding | 2026-09-14 | 0+2/0 | 2571 | ARCHIVE
mickey/G3_3_controverted.md | receipt | 2026-09-14 | 0+2/0 | 9125 | ARCHIVE
mickey/G3_4_repin.md | receipt | 2026-09-14 | 0+2/0 | 2651 | ARCHIVE
mickey/G3_5_firing_card.md | finding | 2026-09-14 | 0+2/0 | 3965 | ARCHIVE
mickey/G3_6_law.md | law | 2026-09-14 | 0+2/0 | 1369 | PROMOTE
mickey/G3_7_hum.md | receipt | 2026-09-14 | 0+2/0 | 1759 | ARCHIVE
mickey/G4_1_adversarial.md | receipt | 2026-09-14 | 0+2/0 | 8088 | ARCHIVE
mickey/G4_2_controverted_v2.md | receipt | 2026-09-14 | 0+2/0 | 5192 | ARCHIVE
mickey/G4_4_wiring.md | finding | 2026-09-14 | 5+2/0 | 3114 | KEEP
mickey/G4_5_timeline.md | receipt | 2026-09-14 | 0+2/0 | 5410 | ARCHIVE
mickey/G4_6_adjacent.md | receipt | 2026-09-14 | 0+2/0 | 8239 | ARCHIVE
mickey/G4_7_cost_analysis.md | finding | 2026-09-14 | 0+2/0 | 7299 | ARCHIVE
mickey/G5_1_nyquist.md | receipt | 2026-09-14 | 0+1/0 | 2325 | ARCHIVE
mickey/G5_2_controverted_v2.md | receipt | 2026-09-14 | 0+4/0 | 15502 | ARCHIVE
mickey/G5_3_spine_flip.md | finding | 2026-09-14 | 0+1/0 | 1523 | ARCHIVE
mickey/G5_4_sizing.md | receipt | 2026-09-14 | 0+1/0 | 10372 | ARCHIVE
mickey/G5_5_audit.md | receipt | 2026-09-14 | 0+1/0 | 9082 | ARCHIVE
mickey/G5_6_cost_curve.md | receipt | 2026-09-14 | 0+1/0 | 2762 | ARCHIVE
mickey/G5_7_discovery.md | receipt | 2026-09-14 | 0+2/0 | 4936 | ARCHIVE
mickey/M1_janitor.md | receipt | 2026-09-14 | 0+1/0 | 5899 | ARCHIVE
mickey/M2_fence_final.md | receipt | 2026-09-14 | 0+1/0 | 4050 | ARCHIVE
mickey/M3_storefront_v2.md | receipt | 2026-09-14 | 0+2/0 | 24210 | ARCHIVE
mickey/M4_lattice.md | receipt | 2026-09-14 | 0+2/0 | 4618 | ARCHIVE
mickey/M5_librarian.md | receipt | 2026-09-14 | 0+1/0 | 2786 | ARCHIVE
mickey/M6_whale_replies.md | finding | 2026-09-14 | 0+1/0 | 4440 | ARCHIVE
mickey/M7_percolator.md | receipt | 2026-09-14 | 0+2/0 | 4211 | ARCHIVE
mickey/P0_dust_cascade.md | receipt | 2026-09-14 | 0+1/0 | 4373 | ARCHIVE
mickey/P0_endpoints.md | receipt | 2026-09-14 | 0+1/0 | 3016 | ARCHIVE
mickey/R2_tools.md | receipt | 2026-09-14 | 0+1/0 | 2062 | ARCHIVE
mickey/R4_cascade.md | receipt | 2026-09-14 | 1+2/0 | 3009 | KEEP
mickey/R7_eye.md | receipt | 2026-09-14 | 0+1/0 | 1826 | ARCHIVE
mickey/W7_A_agm.md | receipt | 2026-09-14 | 0+1/0 | 1300 | ARCHIVE
mickey/W7_B_controverted.md | receipt | 2026-09-14 | 0+4/0 | 10951 | ARCHIVE
mickey/W7_D_chapter3.md | receipt | 2026-09-14 | 0+1/0 | 12855 | ARCHIVE
mickey/W7_F_shuffle.md | receipt | 2026-09-14 | 0+1/0 | 10613 | ARCHIVE
mickey/W7_G_batch.md | receipt | 2026-09-14 | 0+1/0 | 3764 | ARCHIVE
mickey/W7_G_overflow.md | receipt | 2026-09-14 | 1+2/0 | 25794 | KEEP
mickey/W7_H_formal.md | receipt | 2026-09-14 | 0+1/0 | 6929 | ARCHIVE
mickey/hermes_fence_read.md | finding | 2026-09-14 | 0+1/0 | 4449 | ARCHIVE
moonshot_20260916/STRUCK_CHORD_DEEPREAD_20260916.md | receipt | 2026-09-16 | 0+1/0 | 4040 | ARCHIVE
moonshot_20260916/TT3_CONTEXT.md | receipt | 2026-09-16 | 0+1/0 | 6603 | ARCHIVE
moonshot_20260916/TT3_TURN1_ANSWER.md | receipt | 2026-09-16 | 0+1/0 | 5782 | ARCHIVE
moonshot_20260916/TT3_TURN2_ANSWER.md | finding | 2026-09-16 | 0+1/0 | 5154 | ARCHIVE
moonshot_20260916/TT3_TURN3_ANSWER.md | receipt | 2026-09-16 | 0+1/0 | 6645 | ARCHIVE
moonshot_20260916/TT3_TURN4_ANSWER.md | finding | 2026-09-16 | 0+1/0 | 2747 | ARCHIVE
moonshot_20260916/receipts/F5_PHYSICS_CANON.md | receipt | 2026-09-16 | 0+1/0 | 9382 | ARCHIVE
moonshot_20260916/receipts/M1_MNEMONIC_PRIORART.md | receipt | 2026-09-16 | 0+3/0 | 15305 | ARCHIVE
moonshot_20260916/receipts/M2_RECURRENT_DEPTH.md | receipt | 2026-09-16 | 0+1/0 | 18170 | ARCHIVE
moonshot_20260916/receipts/M3_LAPLACIAN_BELIEFS.md | receipt | 2026-09-16 | 0+2/0 | 23402 | ARCHIVE
moonshot_20260916/receipts/M4_MNEMONIC_STEAL.md | finding | 2026-09-16 | 0+2/0 | 9684 | ARCHIVE
moonshot_20260916/receipts/M4_RACTOR_ENGINE_SPEC.md | receipt | 2026-09-16 | 0+1/0 | 3798 | ARCHIVE
moonshot_20260916/receipts/TT1_RETROCAUSAL_PHYSICS.md | receipt | 2026-09-16 | 0+2/0 | 28034 | ARCHIVE
moonshot_20260916/receipts/TT2_RIDDLED_STONE_CANON.md | receipt | 2026-09-16 | 0+2/0 | 8977 | ARCHIVE
moonshot_20260916/receipts/TT3_UNION_FULLSEND.md | receipt | 2026-09-16 | 0+3/0 | 30054 | ARCHIVE
noir_gwap_steal_20260926/HOPPER_RENDER_HARDWARE_VERDICT_20260926.md | receipt | 2026-09-26 | 0+2/1 | 1562 | KEEP
noir_gwap_steal_20260926/REPORT_design_precedents.md | receipt | 2026-09-27 | 0+4/1 | 8494 | KEEP
noir_gwap_steal_20260926/REPORT_destruction_tech.md | receipt | 2026-09-27 | 0+4/1 | 3319 | KEEP
noir_gwap_steal_20260926/REPORT_gta_lineage.md | finding | 2026-09-27 | 0+4/1 | 5996 | KEEP
noir_gwap_steal_20260926/REPORT_noir_shaders.md | finding | 2026-09-27 | 0+5/1 | 10720 | KEEP
noir_gwap_steal_20260926/STEAL_PACK_20260926.md | finding | 2026-09-26 | 0+4/1 | 7325 | KEEP
noir_gwap_steal_20260926/SUBSTRATE_DECISION_20260926.md | receipt | 2026-09-26 | 0+2/1 | 5238 | KEEP
operator_voice/JOURNAL_20260919.md | receipt | 2026-09-19 | 0+4/0 | 1986 | ARCHIVE
outbound/adventurelearn_packet/BIBLIOGRAPHY.md | receipt | 2026-09-16 | 21+13/0 | 8728 | KEEP
outbound/adventurelearn_packet/BUILD.md | receipt | 2026-09-16 | 186+412/1 | 18354 | KEEP
outbound/adventurelearn_packet/PACKAGING.md | receipt | 2026-09-16 | 0+4/0 | 2677 | ARCHIVE
outbound/adventurelearn_packet/README.md | receipt | 2026-09-16 | 0+0/1 | 10148 | KEEP
outbound/adventurelearn_packet/WHY.md | receipt | 2026-09-16 | 0+0/0 | 4598 | ARCHIVE
panda_panel_recovery_20260928.md | receipt | 2026-09-28 | 0+1/0 | 4238 | ARCHIVE
physical_computing/COHORT_RESPONSE_ANALYTICAL_NODE_20260829.md | finding | 2026-08-29 | 0+2/0 | 6348 | ARCHIVE
physical_computing/COHORT_RESPONSE_GROK46_20260829.md | finding | 2026-08-29 | 0+2/0 | 13088 | ARCHIVE
physical_computing/CUBE1_SHOPPING_LIST.md | receipt | 2026-09-16 | 1+6/0 | 3279 | KEEP
physical_computing/DESIGN_ETCH_STONE_ONE_20260916.md | receipt | 2026-09-16 | 0+2/0 | 9707 | ARCHIVE
physical_computing/DESIGN_MULTISPECIES_LATTICE_20260916.md | finding | 2026-09-16 | 0+6/0 | 3545 | REVIEW
physical_computing/DESIGN_MYCO_MEMORY_20260916.md | brief | 2026-09-16 | 1+5/0 | 3446 | KEEP
physical_computing/PHYSICAL_COMPUTING_PACK_20260916.md | receipt | 2026-09-16 | 1+4/0 | 25426 | KEEP
physical_computing/RESEARCH_BRIEF_PHYSICAL_SUBSTRATES_v1_20260829.md | brief | 2026-08-29 | 0+2/0 | 11943 | ARCHIVE
physical_computing/receipts/C15_EXTROPIC_REPLICATION_DESIGN.md | receipt | 2026-09-16 | 0+1/0 | 18207 | ARCHIVE
physical_computing/receipts/C15_LANE1_CSV_ESS_AUDIT.md | receipt | 2026-09-16 | 0+1/0 | 14714 | ARCHIVE
physical_computing/receipts/C16_ETCH_INVENTORY.md | receipt | 2026-09-16 | 0+1/0 | 7056 | ARCHIVE
physical_computing/receipts/C17_CUBE_INSTRUMENT_PLAN.md | receipt | 2026-09-16 | 1+3/0 | 25429 | KEEP
physical_computing/receipts/C18_HYDRAULIC_THIRD_CHANNEL.md | receipt | 2026-09-16 | 1+1/0 | 14227 | KEEP
physical_computing/receipts/C19_XMINE_ROUND2.md | receipt | 2026-09-16 | 0+2/0 | 24145 | ARCHIVE
physical_computing/receipts/CANON_MINING_20260916.md | receipt | 2026-09-16 | 0+3/0 | 13687 | ARCHIVE
physical_computing/receipts/COLLECTION_ORIGINS_20260916.md | receipt | 2026-09-16 | 0+4/0 | 9072 | ARCHIVE
physical_computing/receipts/COMMIT2_20260916.md | receipt | 2026-09-16 | 0+1/0 | 3991 | ARCHIVE
physical_computing/receipts/COMMIT3_20260916.md | receipt | 2026-09-16 | 0+1/0 | 4259 | ARCHIVE
physical_computing/receipts/COMMIT4_20260916.md | law | 2026-09-16 | 0+1/0 | 6183 | PROMOTE
physical_computing/receipts/COMMIT5_20260916.md | receipt | 2026-09-16 | 0+1/0 | 5721 | ARCHIVE
physical_computing/receipts/COMMIT6_20260916.md | receipt | 2026-09-16 | 0+2/0 | 9062 | ARCHIVE
physical_computing/receipts/COMMIT7_20260916.md | receipt | 2026-09-16 | 0+1/0 | 7259 | ARCHIVE
physical_computing/receipts/COMMIT8_20260916.md | receipt | 2026-09-16 | 0+1/0 | 5239 | ARCHIVE
physical_computing/receipts/COMMIT_20260916.md | receipt | 2026-09-16 | 0+1/0 | 3678 | ARCHIVE
physical_computing/receipts/CONCERT002_FIBER_25.md | receipt | 2026-09-16 | 0+3/0 | 25827 | ARCHIVE
physical_computing/receipts/CV5_BELT_TRICK_REVIVAL.md | receipt | 2026-09-16 | 0+2/0 | 8129 | ARCHIVE
physical_computing/receipts/F6_MYCOLOGY_CANON.md | receipt | 2026-09-16 | 0+2/0 | 10452 | ARCHIVE
physical_computing/receipts/G-B_SPECIES_DATA.md | receipt | 2026-09-16 | 0+1/0 | 13174 | ARCHIVE
physical_computing/receipts/G-C_ZONE_TOPOLOGY.md | receipt | 2026-09-16 | 0+2/0 | 11972 | ARCHIVE
physical_computing/receipts/G-D_WRITE_MECHANISMS.md | receipt | 2026-09-16 | 0+2/0 | 19842 | ARCHIVE
physical_computing/receipts/G-E_FLUID_LOGIC_LIBRARY.md | receipt | 2026-09-16 | 0+1/0 | 20600 | ARCHIVE
physical_computing/receipts/G-F_SPINOR_LATTICE.md | receipt | 2026-09-16 | 0+1/0 | 18129 | ARCHIVE
physical_computing/receipts/G-G_SLOW_READOUT.md | receipt | 2026-09-16 | 0+1/0 | 18209 | ARCHIVE
physical_computing/receipts/G-H_COCULTIVATION.md | finding | 2026-09-16 | 0+1/0 | 17736 | ARCHIVE
physical_computing/receipts/G-I_PRINTABLE_FAB.md | receipt | 2026-09-16 | 0+1/0 | 20840 | ARCHIVE
physical_computing/receipts/G-J_INSTRUMENT_TIER.md | receipt | 2026-09-16 | 0+2/0 | 13971 | ARCHIVE
physical_computing/receipts/GA_SIGNAL_MAGNITUDE.md | receipt | 2026-09-16 | 0+1/0 | 18317 | ARCHIVE
physical_computing/receipts/HERMES_REDTEAM_20260916.md | receipt | 2026-09-16 | 0+1/0 | 8793 | ARCHIVE
physical_computing/receipts/K10_STEERING_TOOLKIT.md | receipt | 2026-09-16 | 0+1/0 | 18271 | ARCHIVE
physical_computing/receipts/K11_LIVING_MATERIAL_SENSING.md | receipt | 2026-09-16 | 0+1/0 | 28825 | ARCHIVE
physical_computing/receipts/K12_CONDUCTED_BLOCK.md | receipt | 2026-09-16 | 0+2/0 | 17684 | ARCHIVE
physical_computing/receipts/K13_K8S_TUB_MAPPING.md | finding | 2026-09-16 | 0+1/0 | 19447 | REVIEW
physical_computing/receipts/K1_STAMETS_CORPUS.md | receipt | 2026-09-16 | 0+1/0 | 19493 | ARCHIVE
physical_computing/receipts/K2_GALVANOTROPISM.md | receipt | 2026-09-16 | 0+1/0 | 16435 | ARCHIVE
physical_computing/receipts/K3_EMBEDDED_TRACES.md | receipt | 2026-09-16 | 0+2/0 | 18845 | ARCHIVE
physical_computing/receipts/K4_CONDUCTIVE_COMPOSITES.md | receipt | 2026-09-16 | 0+1/0 | 20989 | ARCHIVE
physical_computing/receipts/K5_ION_DOPING.md | receipt | 2026-09-16 | 0+1/0 | 16340 | ARCHIVE
physical_computing/receipts/K6_CAPILLARY_DESIGN.md | receipt | 2026-09-16 | 0+1/0 | 19634 | ARCHIVE
physical_computing/receipts/K7_LOWV_BIO.md | receipt | 2026-09-16 | 0+1/0 | 17627 | ARCHIVE
physical_computing/receipts/K8_LATTICE_FARADAY.md | receipt | 2026-09-16 | 0+1/0 | 18647 | ARCHIVE
physical_computing/receipts/K9_PRIOR_ART.md | receipt | 2026-09-16 | 0+1/0 | 22894 | ARCHIVE
physical_computing/receipts/LINKS_FILING_20260916.md | receipt | 2026-09-16 | 0+2/0 | 2911 | ARCHIVE
physical_computing/receipts/N2_PAULI_SPIN_STRUCTURE.md | receipt | 2026-09-16 | 0+2/0 | 15781 | ARCHIVE
physical_computing/receipts/N3_BO_FOR_CUBE.md | receipt | 2026-09-16 | 0+2/0 | 18133 | ARCHIVE
physical_computing/receipts/O2_WAVEGUIDE_VERIFY.md | receipt | 2026-09-16 | 0+1/0 | 15830 | ARCHIVE
physical_computing/receipts/O3_OPTICAL_INTEGRATION.md | receipt | 2026-09-16 | 0+1/0 | 20849 | ARCHIVE
physical_computing/receipts/S1_ACADEMIC_WHO.md | receipt | 2026-09-16 | 0+2/0 | 24472 | ARCHIVE
physical_computing/receipts/S2_BUILDERS_WHO.md | receipt | 2026-09-16 | 0+2/0 | 16016 | ARCHIVE
physical_computing/receipts/S3_SKEPTIC_WATCH.md | receipt | 2026-09-16 | 0+2/0 | 21176 | ARCHIVE
physical_computing/receipts/S4_CORPUS_STEAL.md | finding | 2026-09-16 | 0+2/0 | 30240 | ARCHIVE
physical_computing/receipts/SALON_ESS_20260916.md | receipt | 2026-09-16 | 0+2/0 | 8193 | ARCHIVE
physical_computing/receipts/SALON_ESS_REPLICATE_20260916.md | receipt | 2026-09-16 | 0+4/0 | 12073 | ARCHIVE
physical_computing/receipts/SALON_FREE_20260916.md | receipt | 2026-09-16 | 0+1/0 | 8834 | ARCHIVE
physical_computing/receipts/U3_UNION_HYDRAULIC_SIM.md | receipt | 2026-09-16 | 0+1/0 | 8274 | ARCHIVE
physical_computing/receipts/U7_UNION_IDENTITY_CONSENSUS.md | receipt | 2026-09-16 | 0+2/0 | 18651 | ARCHIVE
physical_computing/receipts/U8_UNION_TECH_INTEL.md | receipt | 2026-09-16 | 1+4/0 | 9074 | KEEP
physical_computing/receipts/X_MINE_FIGURES_20260916.md | receipt | 2026-09-16 | 0+1/0 | 12734 | ARCHIVE
physical_computing/receipts/X_MINE_PHYSICAL_20260916.md | receipt | 2026-09-16 | 0+2/0 | 19928 | ARCHIVE
physical_computing/receipts/concert002_fiber25/answers.md | finding | 2026-09-16 | 210+294/1 | 38077 | KEEP
play_as_work_20260926/BRIEF_v4_full_20260926.md | brief | 2026-09-26 | 1+5/1 | 26293 | KEEP
play_as_work_20260926/BRIEF_v6_master_20260926.md | brief | 2026-09-26 | 0+5/1 | 62831 | KEEP
play_as_work_20260926/MASTER_BUILD_NOTES_v6_20260926.md | finding | 2026-09-26 | 0+4/1 | 5032 | KEEP
play_as_work_20260926/STEAL_RECEIPT_20260926.md | finding | 2026-09-26 | 0+5/1 | 5589 | KEEP
play_as_work_20260926/VERIFICATION_v6_20260926.md | receipt | 2026-09-26 | 0+4/1 | 3814 | KEEP
probes/PROBE_001_20260921.md | finding | 2026-09-21 | 0+4/1 | 691 | KEEP
probes/PROBE_002_20260921.md | finding | 2026-09-21 | 0+4/1 | 691 | KEEP
probes/PROBE_003_20260921.md | finding | 2026-09-21 | 0+4/1 | 711 | KEEP
ractor_panel_20260926/burnaudit.final.md | receipt | 2026-09-27 | 0+2/1 | 29198 | KEEP
ractor_panel_20260926/cands/burnaudit-one.md | receipt | 2026-09-27 | 0+4/1 | 11325 | KEEP
ractor_panel_20260926/cands/burnaudit-two.md | receipt | 2026-09-27 | 0+4/1 | 13952 | KEEP
ractor_panel_20260926/cands/credrot-one.md | receipt | 2026-09-27 | 0+4/1 | 19646 | KEEP
ractor_panel_20260926/cands/credrot-two.md | receipt | 2026-09-27 | 0+2/1 | 16564 | KEEP
ractor_panel_20260926/cands/dfdials-one.md | receipt | 2026-09-27 | 0+4/1 | 13210 | KEEP
ractor_panel_20260926/cands/dfdials-two.md | receipt | 2026-09-27 | 0+6/1 | 11521 | KEEP
ractor_panel_20260926/cands/eigenmap-one.md | finding | 2026-09-27 | 1+2/1 | 11364 | KEEP
ractor_panel_20260926/cands/eigenmap-two.md | finding | 2026-09-27 | 3+3/1 | 8653 | KEEP
ractor_panel_20260926/cands/killed/README.md | receipt | 2026-09-27 | 0+0/1 | 1944 | KEEP
ractor_panel_20260926/cands/prereg-attack-one.md | receipt | 2026-09-27 | 0+6/1 | 10636 | KEEP
ractor_panel_20260926/cands/prereg-attack-two.md | receipt | 2026-09-27 | 0+4/1 | 13462 | KEEP
ractor_panel_20260926/cands/seedrib-one.md | receipt | 2026-09-27 | 0+4/1 | 14864 | KEEP
ractor_panel_20260926/cands/seedrib-two.md | receipt | 2026-09-27 | 0+8/1 | 11331 | KEEP
ractor_panel_20260926/cands/uf122-one.md | receipt | 2026-09-27 | 0+4/1 | 15995 | KEEP
ractor_panel_20260926/cands/uf122-two.md | receipt | 2026-09-27 | 0+6/1 | 19070 | KEEP
ractor_panel_20260926/cands/verkle99-one.md | receipt | 2026-09-27 | 0+6/1 | 12908 | KEEP
ractor_panel_20260926/cands/verkle99-two.md | receipt | 2026-09-27 | 0+4/1 | 12252 | KEEP
ractor_panel_20260926/credrot.final.md | receipt | 2026-09-27 | 0+2/1 | 26088 | KEEP
ractor_panel_20260926/dfdials.final.md | receipt | 2026-09-27 | 0+2/1 | 18827 | KEEP
ractor_panel_20260926/dfdials_mixed_dial_census_20260926.md | finding | 2026-09-26 | 0+2/1 | 4099 | KEEP
ractor_panel_20260926/eigenmap.final.md | finding | 2026-09-27 | 0+2/1 | 12568 | KEEP
ractor_panel_20260926/prereg-attack.final.md | receipt | 2026-09-27 | 0+2/1 | 18808 | KEEP
ractor_panel_20260926/seedrib.final.md | receipt | 2026-09-27 | 0+2/1 | 10362 | KEEP
ractor_panel_20260926/uf122.final.md | finding | 2026-09-27 | 0+2/1 | 31071 | KEEP
ractor_panel_20260926/verkle99.final.md | receipt | 2026-09-27 | 2+2/1 | 18859 | KEEP
sandbox_escape_primary.md | receipt | 2026-09-14 | 0+4/1 | 9379 | KEEP
scout_drop_free_claude_code_20260926.md | receipt | 2026-09-26 | 0+4/1 | 3078 | KEEP
seed_rib_20260926/SEED_RIB_LANDED_RECEIPT.md | law | 2026-09-27 | 0+2/1 | 5300 | KEEP
seed_rib_20260926/seed-rib/ACCOUNTS.md | finding | 2026-09-27 | 3+5/0 | 1631 | KEEP
seed_rib_20260926/seed-rib/AGENTS.md | other | 2026-09-27 | 78+158/1 | 172 | REVIEW
seed_rib_20260926/seed-rib/ARTIFACT_LEDGER_LAW.md | law | 2026-09-27 | 0+2/0 | 2301 | PROMOTE
seed_rib_20260926/seed-rib/BOOT_BUDGET_CARD.md | receipt | 2026-09-27 | 0+2/0 | 2009 | ARCHIVE
seed_rib_20260926/seed-rib/BUILD_DISCIPLINE_LAWS.md | law | 2026-09-27 | 0+3/0 | 2278 | PROMOTE
seed_rib_20260926/seed-rib/CAPABILITY_GATE_LEDGER.md | receipt | 2026-09-27 | 0+2/0 | 2114 | ARCHIVE
seed_rib_20260926/seed-rib/CHANGELOG.md | receipt | 2026-09-27 | 0+0/0 | 2497 | ARCHIVE
seed_rib_20260926/seed-rib/DATA_TIERS.md | finding | 2026-09-27 | 1+2/0 | 1078 | KEEP
seed_rib_20260926/seed-rib/FIRST_BOOT.md | receipt | 2026-09-27 | 3+3/0 | 2085 | KEEP
seed_rib_20260926/seed-rib/HANDOFF.md | brief | 2026-09-27 | 79+112/1 | 1037 | KEEP
seed_rib_20260926/seed-rib/MORNING_LOOP.md | finding | 2026-09-27 | 1+2/0 | 1225 | KEEP
seed_rib_20260926/seed-rib/SALON.md | receipt | 2026-09-27 | 55+309/1 | 1418 | KEEP
seed_rib_20260926/seed-rib/SEED_RIB.md | law | 2026-09-27 | 3+7/1 | 4253 | KEEP
seed_rib_20260926/seed-rib/SETUP.md | finding | 2026-09-27 | 14+32/1 | 882 | KEEP
seed_rib_20260926/seed-rib/SHARED_SURFACE_LAW.md | law | 2026-09-27 | 0+2/0 | 2332 | PROMOTE
seed_rib_20260926/seed-rib/STATE_BRIEF_CONTRACT.md | brief | 2026-09-27 | 0+2/0 | 1984 | ARCHIVE
seed_rib_20260926/seed-rib/THE_METHOD.md | receipt | 2026-09-27 | 3+4/0 | 3093 | KEEP
seed_rib_20260926/seed-rib/TOUR.md | receipt | 2026-09-27 | 4+5/0 | 1734 | KEEP
seed_rib_20260926/seed-rib/TRUST_BYTES_LAW.md | law | 2026-09-27 | 0+7/0 | 2150 | PROMOTE
seed_rib_20260926/seed-rib/VSCODE.md | other | 2026-09-27 | 6+9/0 | 1362 | REVIEW
seed_rib_20260926/seed-rib/ZERO_CONTEXT_DELEGATION.md | receipt | 2026-09-27 | 0+2/0 | 2373 | ARCHIVE
seed_rib_20260926/seed-rib/kernel/env.law.md | law | 2026-09-27 | 0+2/0 | 638 | PROMOTE
seed_rib_20260926/seed-rib/kernel/filing.law.md | law | 2026-09-27 | 0+2/0 | 551 | PROMOTE
seed_rib_20260926/seed-rib/kernel/load.order.md | finding | 2026-09-27 | 0+2/1 | 832 | KEEP
seed_rib_20260926/seed-rib/kernel/state.now.md | receipt | 2026-09-27 | 0+2/0 | 809 | ARCHIVE
seed_rib_20260926/seed-rib/kernel/thesis.card.md | receipt | 2026-09-27 | 0+2/0 | 1488 | ARCHIVE
seed_rib_20260926/seed-rib/kernel/tier.law.md | law | 2026-09-27 | 0+2/0 | 250 | PROMOTE
static_rebuild/LANE5_biblio.md | receipt | 2026-09-14 | 0+1/0 | 3577 | ARCHIVE
static_rebuild/LANE_A_classification.md | receipt | 2026-09-14 | 0+1/0 | 26043 | ARCHIVE
static_rebuild/LANE_B_dogfood.md | receipt | 2026-09-14 | 0+1/0 | 12962 | ARCHIVE
static_rebuild/LANE_C_wipeout.md | finding | 2026-09-14 | 0+1/0 | 9218 | ARCHIVE
static_rebuild/LANE_D_rd_history.md | receipt | 2026-09-14 | 0+1/0 | 6603 | ARCHIVE
static_rebuild/LANE_E_directions.md | receipt | 2026-09-14 | 0+1/0 | 5962 | ARCHIVE
static_rebuild/LANE_F_redesign_spec.md | receipt | 2026-09-14 | 0+1/0 | 11269 | ARCHIVE
static_rebuild/MASTER_PLAN.md | finding | 2026-09-14 | 0+2/0 | 3587 | ARCHIVE
steal_research_pipeline/BOT_A_perplexity.md | finding | 2026-09-14 | 0+2/0 | 8543 | ARCHIVE
steal_research_pipeline/BOT_B_claims.md | receipt | 2026-09-14 | 1+3/0 | 8511 | KEEP
steal_research_pipeline/BOT_C_deepresearch.md | finding | 2026-09-14 | 0+2/0 | 7762 | ARCHIVE
union_fullsend_20260917/DAY_PACK.md | receipt | 2026-09-17 | 3+5/0 | 300549 | KEEP
union_fullsend_20260917/ELDER_AUDIT_p1.md | receipt | 2026-09-17 | 0+3/0 | 3379 | ARCHIVE
union_fullsend_20260917/WANTS.md | receipt | 2026-09-17 | 3+19/0 | 2225 | KEEP
v41_paces/LANE1_api_sweep.md | finding | 2026-09-14 | 0+1/0 | 4869 | ARCHIVE
v41_paces/LANE2_harness.md | receipt | 2026-09-14 | 0+3/0 | 9880 | ARCHIVE
v41_paces/LANE2_harness_test.md | receipt | 2026-09-14 | 0+3/0 | 10272 | ARCHIVE
v41_paces/LANE3_bytedrift.md | receipt | 2026-09-14 | 0+2/0 | 9699 | ARCHIVE
v41_paces/LANE3_speed.md | receipt | 2026-09-14 | 0+2/0 | 3301 | ARCHIVE
v41_paces/LANE4_expansion.md | finding | 2026-09-14 | 0+2/0 | 7025 | ARCHIVE
v41_paces/LANE4_speed_cache.md | finding | 2026-09-14 | 0+2/0 | 8474 | ARCHIVE
v41_paces/LANE5_vision.md | finding | 2026-09-14 | 0+2/0 | 7926 | ARCHIVE
v41_paces/LANE6_coding.md | receipt | 2026-09-14 | 0+1/0 | 4190 | ARCHIVE
v41_paces/LANE6_encoding.md | receipt | 2026-09-14 | 0+1/0 | 5419 | ARCHIVE
v41_paces/LANE7_cost.md | receipt | 2026-09-14 | 0+1/0 | 7401 | ARCHIVE
v41_paces/LANE7_run.md | receipt | 2026-09-14 | 0+1/0 | 16991 | ARCHIVE
v41_paces/LANE7_whales.md | finding | 2026-09-14 | 0+2/0 | 6280 | ARCHIVE
v41_paces/LANE8_new_work.md | finding | 2026-09-14 | 0+1/0 | 7845 | ARCHIVE
v41_paces/LANE8_rocinante.md | receipt | 2026-09-14 | 0+2/0 | 8266 | ARCHIVE
v41_paces/W7_E_gamebuild.md | receipt | 2026-09-14 | 0+2/0 | 3967 | ARCHIVE
wave_20260916/DESIGN_MYCO_MEMORY_20260916.md | brief | 2026-09-16 | 1+5/0 | 3913 | KEEP
wave_20260916/N5_ractor_dogfood_pack.md | receipt | 2026-09-16 | 0+1/0 | 18198 | ARCHIVE
wave_20260916/WAVE_STATE_20260916.md | receipt | 2026-09-16 | 1+7/1 | 17808 | KEEP
wave_20260916/drafts/W1_contract.md | receipt | 2026-09-16 | 0+1/0 | 10887 | ARCHIVE
wave_20260916/drafts/u9_union_prompt.md | brief | 2026-09-16 | 0+1/0 | 7560 | ARCHIVE
wave_20260916/r1_fanout_runs/pack.md | finding | 2026-09-16 | 653+731/1 | 176774 | KEEP
wave_20260916/receipts/A1_BLIND_CHALLENGE_SET.md | receipt | 2026-09-16 | 1+3/0 | 16437 | KEEP
wave_20260916/receipts/A2_EPISTEMOLOGY_ENGINE.md | receipt | 2026-09-16 | 1+3/0 | 14804 | KEEP
wave_20260916/receipts/A3_THE_TOY_CORE_VERB.md | receipt | 2026-09-16 | 0+2/0 | 11119 | ARCHIVE
wave_20260916/receipts/A4_ASTRA_SMOKE_12.md | receipt | 2026-09-16 | 0+2/0 | 10610 | ARCHIVE
wave_20260916/receipts/B10_MLP_KV_CACHE_PRIORART.md | receipt | 2026-09-16 | 0+2/0 | 14454 | ARCHIVE
wave_20260916/receipts/B11_SLIDING_WINDOW_RIB.md | law | 2026-09-16 | 0+2/0 | 7238 | PROMOTE
wave_20260916/receipts/B12_RASHOMON_DEDUPE.md | receipt | 2026-09-16 | 0+2/0 | 5330 | ARCHIVE
wave_20260916/receipts/B13_CODETAUR_KAN.md | receipt | 2026-09-16 | 0+2/0 | 6671 | ARCHIVE
wave_20260916/receipts/B14_EXECUTION_RUN.md | receipt | 2026-09-16 | 0+3/0 | 11572 | ARCHIVE
wave_20260916/receipts/B14_THIRD_SMILE_PROTOCOL.md | receipt | 2026-09-16 | 0+3/0 | 19637 | ARCHIVE
wave_20260916/receipts/B6_LINKS_BACKFILL.md | receipt | 2026-09-16 | 0+2/0 | 2834 | ARCHIVE
wave_20260916/receipts/B7_CANONICAL_CHECK_WRITERS.md | receipt | 2026-09-16 | 0+2/0 | 5000 | ARCHIVE
wave_20260916/receipts/B8_ARXIV_SIX_LEADS.md | receipt | 2026-09-16 | 0+2/0 | 14654 | ARCHIVE
wave_20260916/receipts/B9_ZENODO_DOIS.md | receipt | 2026-09-16 | 0+2/0 | 1569 | ARCHIVE
wave_20260916/receipts/B9_ZENODO_DOIS_GEN2.md | receipt | 2026-09-16 | 0+2/0 | 2856 | ARCHIVE
wave_20260916/receipts/CG1_PROMPT_LIBRARY_UNPACK.md | brief | 2026-09-16 | 0+2/0 | 33978 | ARCHIVE
wave_20260916/receipts/CG2_CARSE_HISTORY.md | receipt | 2026-09-16 | 0+3/0 | 33471 | ARCHIVE
wave_20260916/receipts/CG3_ESTATE_INFINITE.md | receipt | 2026-09-16 | 0+2/0 | 17993 | ARCHIVE
wave_20260916/receipts/CG4_MESH_CARSE_SALON.md | receipt | 2026-09-16 | 0+1/0 | 14504 | ARCHIVE
wave_20260916/receipts/CONCERT001_20260916.md | receipt | 2026-09-16 | 0+3/0 | 18127 | ARCHIVE
wave_20260916/receipts/CV1_COLD_MAP.md | finding | 2026-09-16 | 0+2/0 | 11667 | REVIEW
wave_20260916/receipts/CV2_SHADOW_INVENTORY.md | receipt | 2026-09-16 | 0+3/0 | 16216 | ARCHIVE
wave_20260916/receipts/CV3_WORLD_DOGFOOD.md | receipt | 2026-09-16 | 0+2/0 | 8300 | ARCHIVE
wave_20260916/receipts/CV4_KILL_STAGING.md | receipt | 2026-09-16 | 0+2/0 | 7285 | ARCHIVE
wave_20260916/receipts/D20_BONES_ADAPTER.md | receipt | 2026-09-16 | 1+2/0 | 7093 | KEEP
wave_20260916/receipts/D21_ESTATE_LOD_SPECTATOR.md | receipt | 2026-09-16 | 0+1/0 | 5233 | ARCHIVE
wave_20260916/receipts/D22_PROVIDER_PROBE_20260916.md | finding | 2026-09-16 | 0+1/0 | 8302 | REVIEW
wave_20260916/receipts/D23_SALON50_NIGHT_RESULTS.md | receipt | 2026-09-16 | 0+1/0 | 20632 | ARCHIVE
wave_20260916/receipts/D24_MEMORY_DOCTRINE_BUNDLE.md | brief | 2026-09-16 | 0+2/0 | 6560 | ARCHIVE
wave_20260916/receipts/E_UNION_ALPHA_EVAL.md | receipt | 2026-09-16 | 0+2/0 | 15346 | ARCHIVE
wave_20260916/receipts/F1_AI_CANON.md | receipt | 2026-09-16 | 0+1/0 | 7490 | ARCHIVE
wave_20260916/receipts/F1_FOLD_STATE.md | finding | 2026-09-16 | 0+1/0 | 1780 | ARCHIVE
wave_20260916/receipts/F2_GAME_CANON.md | receipt | 2026-09-16 | 0+1/0 | 6374 | ARCHIVE
wave_20260916/receipts/F3_ELECTRONICS_CANON.md | receipt | 2026-09-16 | 0+1/0 | 10528 | ARCHIVE
wave_20260916/receipts/F4_ESOTERIC_CANON.md | receipt | 2026-09-16 | 0+3/1 | 9988 | KEEP
wave_20260916/receipts/FX1_SWARM_STORAGE_AUDIO.md | receipt | 2026-09-16 | 0+1/0 | 9935 | ARCHIVE
wave_20260916/receipts/FX2_SURFACE_RECONCILE.md | receipt | 2026-09-16 | 0+2/0 | 14426 | ARCHIVE
wave_20260916/receipts/FX3_SHADER_FIXES.md | receipt | 2026-09-16 | 0+1/0 | 8347 | ARCHIVE
wave_20260916/receipts/FX4_MUD_REPLAY_PORT.md | receipt | 2026-09-16 | 0+1/0 | 15602 | ARCHIVE
wave_20260916/receipts/FX5_SYNC_DIRECTION_FIX.md | receipt | 2026-09-17 | 0+1/0 | 5866 | ARCHIVE
wave_20260916/receipts/G1_GAMES_AUDIT.md | receipt | 2026-09-16 | 0+1/0 | 12787 | ARCHIVE
wave_20260916/receipts/G2_STATIC_INFRA_AUDIT.md | receipt | 2026-09-16 | 0+1/0 | 13398 | ARCHIVE
wave_20260916/receipts/G3_SHADER_AUDIT.md | receipt | 2026-09-16 | 0+1/0 | 21787 | ARCHIVE
wave_20260916/receipts/H1_HERMES_INDEX_REPAIR.md | receipt | 2026-09-16 | 0+1/0 | 5923 | ARCHIVE
wave_20260916/receipts/HG1_GAMING_HISTORY_WEAVE.md | receipt | 2026-09-16 | 0+3/0 | 27063 | ARCHIVE
wave_20260916/receipts/HG2_OUR_CORPUS_WEAVE.md | receipt | 2026-09-16 | 0+3/0 | 31278 | ARCHIVE
wave_20260916/receipts/INCIDENT_ROLLBACK_20260916.md | receipt | 2026-09-16 | 0+1/0 | 11897 | ARCHIVE
wave_20260916/receipts/LINKS_JEV_20260916.md | receipt | 2026-09-16 | 0+1/0 | 1749 | ARCHIVE
wave_20260916/receipts/LINKS_ORE3_20260916.md | receipt | 2026-09-16 | 0+1/0 | 2001 | ARCHIVE
wave_20260916/receipts/LINKS_PICASSO_20260916.md | receipt | 2026-09-16 | 0+1/0 | 1414 | ARCHIVE
wave_20260916/receipts/LINKS_TRUMPO_20260917.md | receipt | 2026-09-17 | 0+1/0 | 1482 | ARCHIVE
wave_20260916/receipts/MI1_INBOX_MINE_PRIMARY.md | receipt | 2026-09-16 | 0+2/0 | 46954 | ARCHIVE
wave_20260916/receipts/MI2_INBOX_MINE_RECEIPTS.md | receipt | 2026-09-16 | 0+1/0 | 30076 | ARCHIVE
wave_20260916/receipts/MI3_INBOX_SHADOW.md | receipt | 2026-09-16 | 0+2/0 | 41048 | ARCHIVE
wave_20260916/receipts/N10_PUZZLE_VAULT_CONSUMER.md | receipt | 2026-09-16 | 0+2/0 | 10452 | ARCHIVE
wave_20260916/receipts/N11_LOD_CONSUMER.md | receipt | 2026-09-16 | 0+1/0 | 5611 | ARCHIVE
wave_20260916/receipts/N12_INVENTORY_CONSUMER.md | receipt | 2026-09-16 | 0+2/0 | 21954 | ARCHIVE
wave_20260916/receipts/N1_COMMAND_DECK.md | receipt | 2026-09-16 | 0+2/0 | 10564 | ARCHIVE
wave_20260916/receipts/N4_GOAT_VS_SINKS.md | receipt | 2026-09-16 | 0+1/0 | 11933 | ARCHIVE
wave_20260916/receipts/N5_RACTOR_DOGFOOD.md | receipt | 2026-09-16 | 0+2/0 | 7815 | ARCHIVE
wave_20260916/receipts/N6_TRAINING_PDF_FETCH.md | receipt | 2026-09-16 | 1+1/0 | 9432 | KEEP
wave_20260916/receipts/N7_GAME_DOCS_FETCH.md | receipt | 2026-09-16 | 0+1/0 | 7665 | ARCHIVE
wave_20260916/receipts/N8_GAME_RAMP_REWIRE.md | receipt | 2026-09-16 | 0+2/0 | 9282 | ARCHIVE
wave_20260916/receipts/N9_BOON_BUGS.md | receipt | 2026-09-16 | 0+1/0 | 9477 | ARCHIVE
wave_20260916/receipts/P1_RACTOR_PACKAGE.md | receipt | 2026-09-16 | 1+3/0 | 9503 | KEEP
wave_20260916/receipts/P2_DEMO_SALON.md | receipt | 2026-09-16 | 0+2/0 | 21134 | ARCHIVE
wave_20260916/receipts/PD1_AUGMENTATION_CANON.md | receipt | 2026-09-16 | 0+1/0 | 11475 | ARCHIVE
wave_20260916/receipts/PD2_STEERING_CANON.md | receipt | 2026-09-16 | 0+2/0 | 1463 | ARCHIVE
wave_20260916/receipts/PD3_FOUNDING_LAW.md | law | 2026-09-16 | 1+1/0 | 4999 | KEEP
wave_20260916/receipts/PD4_PARABLE_REGISTER.md | receipt | 2026-09-16 | 0+1/0 | 3518 | ARCHIVE
wave_20260916/receipts/R1_SWARM_RESEARCH.md | finding | 2026-09-16 | 0+2/0 | 7560 | ARCHIVE
wave_20260916/receipts/R2_GAME_SUBSYSTEM_GAPS.md | receipt | 2026-09-16 | 0+3/0 | 15974 | ARCHIVE
wave_20260916/receipts/R3_GAP_ANALYSIS_SOCRATIC.md | finding | 2026-09-16 | 0+2/0 | 20303 | REVIEW
wave_20260916/receipts/RS_COMPOSE_EAST_WEST.md | finding | 2026-09-16 | 1+3/0 | 2124 | KEEP
wave_20260916/receipts/RS_EAST_PRIMARY.md | receipt | 2026-09-16 | 0+3/0 | 21618 | ARCHIVE
wave_20260916/receipts/RS_RACTOR_ENGINE_SALON.md | receipt | 2026-09-16 | 0+3/0 | 12212 | ARCHIVE
wave_20260916/receipts/RS_WEST_PRIMARY.md | receipt | 2026-09-16 | 0+3/0 | 21206 | ARCHIVE
wave_20260916/receipts/RS_WORLDBUILD_SALON.md | receipt | 2026-09-16 | 0+3/0 | 16028 | ARCHIVE
wave_20260916/receipts/RV1_RECIPROCAL_PACKET.md | receipt | 2026-09-16 | 0+2/0 | 10294 | ARCHIVE
wave_20260916/receipts/RV2B_PACKET_FOLD.md | finding | 2026-09-16 | 0+1/0 | 7625 | ARCHIVE
wave_20260916/receipts/RV2_MESH_EXPLAIN_FLEET.md | receipt | 2026-09-16 | 0+1/0 | 19443 | ARCHIVE
wave_20260916/receipts/RV3_HIVE_CROSSWALK.md | receipt | 2026-09-16 | 0+1/0 | 18694 | ARCHIVE
wave_20260916/receipts/S5_JOURNAL_VENUES.md | receipt | 2026-09-16 | 0+2/0 | 18477 | ARCHIVE
wave_20260916/receipts/SP_OPENAI_MISALIGNMENT.md | shitpost | 2026-09-16 | 0+1/0 | 6559 | ARCHIVE
wave_20260916/receipts/U1_UNION_TOY.md | receipt | 2026-09-16 | 0+1/0 | 10519 | ARCHIVE
wave_20260916/receipts/U2_UNION_ASTRA13.md | receipt | 2026-09-16 | 0+1/0 | 10825 | ARCHIVE
wave_20260916/receipts/U4_UNION_VERDICT_COLUMN.md | receipt | 2026-09-16 | 0+1/0 | 19065 | ARCHIVE
wave_20260916/receipts/U5_UNION_WAVE_WITNESS.md | receipt | 2026-09-16 | 0+3/0 | 13738 | ARCHIVE
wave_20260916/receipts/U6_UNION_CREATIVE.md | receipt | 2026-09-16 | 0+1/0 | 8378 | ARCHIVE
wave_20260916/receipts/U9_UNION_MCP_SERVER.md | receipt | 2026-09-16 | 1+1/0 | 11244 | KEEP
wave_20260916/receipts/V1_BUILD_AUDITIONS.md | receipt | 2026-09-16 | 0+1/0 | 9421 | ARCHIVE
wave_20260916/receipts/V4_GROUNDING_ADMISSION.md | receipt | 2026-09-16 | 0+2/0 | 9786 | ARCHIVE
wave_20260916/receipts/VC1_FULL_CENSUS.md | finding | 2026-09-16 | 0+3/0 | 22384 | REVIEW
wave_20260916/receipts/VC2_CHAIN_STATE.md | receipt | 2026-09-16 | 1+14/0 | 16332 | KEEP
wave_20260916/receipts/W1A_SHARED_SEED.md | receipt | 2026-09-16 | 0+2/0 | 7638 | ARCHIVE
wave_20260916/receipts/W1_WORLD_SKELETON.md | receipt | 2026-09-16 | 1+2/0 | 10713 | KEEP
wave_20260916/receipts/W2_MUD_BONES_FILES.md | receipt | 2026-09-16 | 0+2/0 | 9524 | ARCHIVE
wave_20260916/receipts/W2_PLAYER_FILES.md | receipt | 2026-09-16 | 1+2/0 | 5766 | KEEP
wave_20260916/receipts/W3_SOULS_MESSAGES.md | receipt | 2026-09-16 | 0+2/0 | 9447 | ARCHIVE
wave_20260916/receipts/W4_GHOST_PERSONALITIES.md | receipt | 2026-09-16 | 0+2/0 | 7526 | ARCHIVE
wave_20260916/receipts/W5_STS_CONSUMER.md | receipt | 2026-09-16 | 0+2/0 | 13814 | ARCHIVE
wave_20260916/receipts/W6_PROGRAMS_JSON.md | receipt | 2026-09-16 | 0+2/0 | 9693 | ARCHIVE
wave_20260916/receipts/W7_ERA_ANCIENT.md | receipt | 2026-09-16 | 0+2/0 | 31470 | ARCHIVE
wave_20260916/receipts/W8_ERA_TABLETOP_MUD.md | receipt | nodate | 0+1/0 | 961 | ARCHIVE
wave_20260916/receipts/W9_ERA_ROGUE_DECK.md | receipt | 2026-09-16 | 0+2/0 | 25074 | ARCHIVE
wave_20260916/receipts/WARM_START_20260916.md | receipt | 2026-09-16 | 0+3/0 | 9322 | ARCHIVE
wave_20260916/receipts/WEAVE_SYNTHESIS.md | receipt | 2026-09-16 | 0+3/0 | 3645 | ARCHIVE
wave_20260916/rs_witness_posts/RS1_souls_purist.md | receipt | 2026-09-16 | 0+1/0 | 1074 | ARCHIVE
wave_20260916/rs_witness_posts/RS2_mud_veteran.cerebras.md | receipt | 2026-09-16 | 0+1/0 | 1548 | ARCHIVE
wave_20260916/rs_witness_posts/RS2_mud_veteran.md | receipt | 2026-09-16 | 0+1/0 | 1251 | ARCHIVE
wave_20260916/rs_witness_posts/RS3_player_one.md | receipt | 2026-09-16 | 0+2/0 | 749 | ARCHIVE
wave_20260916/rs_witness_posts/RS3_player_one.mistral.md | receipt | 2026-09-16 | 0+2/0 | 1421 | ARCHIVE
wave_20260916/rs_witness_posts/RS4_referee_lawyer.md | law | 2026-09-16 | 0+1/0 | 2150 | PROMOTE
wave_20260916/u1_union_prompt.md | brief | 2026-09-16 | 0+2/0 | 4941 | ARCHIVE
wave_20260916/w2_union_prompt.md | brief | 2026-09-16 | 0+1/0 | 5355 | ARCHIVE

## Verification receipts (appended at banking, 2026-09-28T22:23:08-0400)

- final drift walk at banking: 2873 md / 14620 total files under watch/inbox/ (git-tracked md: 2228). Delta vs snapshot of record: +488 md in ~2 h - the census of record above is the 20:23:59 snapshot, this is the drift it was taken inside.
- em/en dash scan of both twins at banking: em 0 / en 0 / figure 0 / minus 0 (this file) and em 0 / en 0 / figure 0 / minus 0 (s2-22.md). Quoted heading text was dash-normalized at compose time (Method 10); authored text carries none.
- twin byte-identity: `cmp inbox-genre-census.md s2-22.md` exit 0 (0 = identical).
- reference spot-checks (4/4 confirmed by direct grep): `tools/lattice_build.py:57` names SELF_STEAL_TEST_TIME_COMMUNICATION_20260921.md; `scripts/build_deck.py:221,240` name wave_20260916/WAVE_STATE_20260916.md; `AGENTS.md` clippy block names ENVELOPE_50W_HIT_20260926.md; `githooks/pre-push` names MICKEY17_WAVE2_QUALITY_20260925.md.
- zero-ref spot-checks caught an instrument defect: 3 stems the first rg `-o` pass called zero-ref were found by repo-wide grep in catalog/ and memory/trajectory/ - ripgrep 15.2.0 `-o` with a 2,379-pattern `-f` file silently drops matches. All reference numbers were re-derived with line-mode passes and exact python attribution (Method 5b) before banking; the corrected instruments credit 2381 of 2385 md files somewhere and 1319 canonically.
- the 4 zero-everywhere files: 2 are hard orphans confirmed by repo-wide grep outside the inbox (`burn_reset_20260927/flash50/_sw03_out_sw-econ-3_stealth_space-bunny-alpha.md`, `fifty_wide_20260917/FW37-42_INDEX.md`); the other 2 (`outbound/adventurelearn_packet/WHY.md`, `seed_rib_20260926/seed-rib/CHANGELOG.md`) have generic-word stems - repo-wide word greps collide with the words themselves, so their zero-ref claim is exact only under the census name-matching instruments (their names are in the GENERIC stoplist for exactly this reason).
