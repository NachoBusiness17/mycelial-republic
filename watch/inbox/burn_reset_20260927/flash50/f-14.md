# RIB CENSUS - memory/rib/ (ITEM f-14, 2026-09-28)

Census moment: 2026-09-28T17:45:09 local (EDT), repo `local_sovereign_agent`, working tree branch mag/run-beta1-factory-build-audi-20260806T231709Z. Every number below came from a command run during this ask (commands listed at the end). Totals: **45 files (43 .md + 2 .json), 159,389 bytes** (`.venv/Scripts/python.exe` walk of memory/rib with os.path.getmtime/getsize).

## 1. The three asked surfaces

### AGENTS.md (grep -c per stem, 45 stems, run this session)
Exactly **2 of 45** ribs are named in AGENTS.md, both inside the DRIVING LADDER bullet ("warm the ribs (memory/rib/, esp. ..."):
- RIB_DRIVING_LADDER_20260928.md -> 1 hit
- RIB_FREE_USAGE_POLICY_20260823.md -> 1 hit
- all other 43 stems -> 0 hits

### The context pack (generic directory consumers, not per-file refs)
- `mag/context_pack.py:305-340` `_rib_doctrine()` reads ALL `memory/rib/*.md`, emits one title+goal line per file (title = first line starting `# ` or `**Schema:**`; goal = `**RIB goal:**` / `**Goal:**` / `**Operator` prefix). Pack key `doctrine` built at mag/context_pack.py:935. Rendered as the "L0d RIB Doctrine" section only in modes plan/full/build/audit (mag/context_pack.py:1092-1097); janitor/route packs drop it. MAG_FULL_CONTEXT raises the cap to 12000 (mag/context_pack.py:966).
- RUNTIME CHECK (run this session): `from mag.context_pack import _rib_doctrine; _rib_doctrine()` returned **4,235 chars, 43 entries** - every .md rib gets an entry today.
- Second pack consumer: `mag/solved_surface.py:63-76` `_rib()` reads ALL `memory/rib/*.md` (id=stem, title, one_line) and feeds `solved_excerpt` (mag/context_pack.py:414, rendered at :1113-1118).

### Code (grep of rib stems across mag/ tools/ scripts/ tests/ dashboard/ configs/ docs/ state/ main.py, .mimosa excluded)
Named references, 6 total:
- `mag/flock_job.py:69-76` `_rib_files()` globs ALL `memory/rib/*.md` as flock-pod payloads; `:83` falls back to `RIB_EMERGENT_FLOCK_ON_K8S_20260810.md` when the glob is empty.
- `tools/curvature_scan.py:43` reads `RIB_CATHEDRAL_WORLD_V1_20260921.md` directly (input to the game-world curvature scan).
- `tools/stealth_driver.py:486-490` comment enforces RIB_DRIVING_LADDER_20260928 as code-as-law (free-lane dispatch is SENSED never DONE).
- `mag/recreation_rib.py:45` writes `memory/rib/recreation-coding-history.json` (RIB_OUT).
- `mag/session_rib.py:52-53` SCENE_DIR = memory/rib, reads/writes `session-scene.json`.
- `mag/ram_cache.py:36` `_CORPUS_DIRS` includes `memory/rib` (mtime fingerprint auto-invalidation) and `:86` `_read_md_dir(ROOT/"memory"/"rib", 100)` reads the rib .md set into the republic-loop corpus text.

Docs/skills (bonus surface): `docs/concepts/README.md:20` (memory/rib/ = the knowledge base) and `:25` names DOCTRINE_MEMWEAVE_20260810.md; `.agents/skills/memweave/SKILL.md:9` points at the Memweave rib family.

Negative checks (run, empty): `grep -n rib mag/hermes_warm_boot.py` -> **0 hits** (warm boot does not read ribs; the AGENTS.md "warm the ribs" boot-order is operator law, not automated). Stem grep of tests/ -> 0 hits (no test pins any rib).

## 2. Staleness (>7d rule, mtime vs census moment)

Measured per-file ages (days): stale (>7.0d) = **43/45**; fresh = **2/45**. Age buckets: <1d = 2, 1-7d = 0, 7-8d = 3, 8-30d = 2, 30-40d = 9, 40-50d = 29.

- Fresh: RIB_BEHAVIOR_CARDS_20260928.md (0.81d), RIB_DRIVING_LADDER_20260928.md (0.86d) - both minted 2026-09-27 evening, both named-or-heir to the AGENTS.md DRIVING LADDER bullet. Last git touch of memory/rib: commit a23928aca, 2026-09-27.
- Just past the line (minted 09-21 wave, commit 16b45778a): RIB_MD_RECORD_20260921 (7.19d), RIB_MOSAIC_SEED_20260921 (7.43d), RIB_CATHEDRAL_WORLD_V1_20260921 (7.87d).
- Center of mass is the 2026-08-10 K8s/memweave era: 29 files sit at 40-50d.

Note: mtimes are the only freshness instrument applied here; the repo's own 7d STALE law (tools/freshness_check.py) covers BOOT_4_7.md and state/ docs, not ribs - ribs have no freshness gate of their own.

## 3. Per-rib census (45 rows)

Tags: AG = named in AGENTS.md; PK = context pack `_rib_doctrine` (all 43 .md, runtime-verified); SS = solved_surface `_rib()` (all 43 .md); RC = ram_cache fingerprint + corpus read (all 43 .md; .json only via fingerprint); CODE = named in code; DOC = named in docs/skill. Verdicts: ACTIVE-LAW (in-force law, named by boot canon or enforced in code), ACTIVE-MECH (input/store of a live tool), RECEIPT (documents a live module's landed behavior), STANDING (doctrine consumed generically, still in force), ERA (Aug-10/11 build-era artifact; informs, nothing depends on it).

| # | file | bytes | age d | refs | verdict |
|---|------|-------|-------|------|---------|
| 1 | DOCTRINE_MEMWEAVE_20260810.md | 4642 | 49.3 | PK/SS/RC + DOC | STANDING - the named operating doctrine (docs/concepts/README.md:25) |
| 2 | GROK_ADVICE_RUNAWAY_PYTHON_20260810.md | 1170 | 49.5 | PK/SS/RC | ERA - companion advice; its laws (CIM attribution, no blanket taskkill) live on in guards |
| 3 | GROK_PLAN_K8S_KNOT_SEAT_20260810.md | 7697 | 49.4 | PK/SS/RC | ERA - frontier ask for the unbuilt-as-specced K8s migration |
| 4 | RIB_BEHAVIOR_CARDS_20260928.md | 3631 | 0.8 | PK/SS/RC | ACTIVE-LAW - operator input-shape card deck, minted 09-27/28, no name-ref yet (youngest rib) |
| 5 | RIB_CASTLES_FOUNDATIONS_20260810.md | 6757 | 49.4 | PK/SS/RC | STANDING - castles-as-spec thesis behind the dashboard IA |
| 6 | RIB_CATHEDRAL_WORLD_V1_20260921.md | 1955 | 7.9 | PK/SS/RC + CODE | ACTIVE-MECH - invariant map read by tools/curvature_scan.py:43 |
| 7 | RIB_CAUSAL_GRAPH_MOONSHOT.md | 787 | 45.4 | PK/SS/RC | STANDING - causal-graph thesis card (append rules, no chain rewrite) |
| 8 | RIB_DEADDROP_FUTURE_SELF_20260811.md | 5577 | 48.4 | PK/SS/RC | ERA - Socratic world-rib contract map |
| 9 | RIB_DOCTRINE_CANONICAL.md | 918 | 45.5 | PK/SS/RC | STANDING - chain-is-ground-truth commitment |
| 10 | RIB_DRIVING_LADDER_20260928.md | 1774 | 0.9 | AG + PK/SS/RC + CODE | ACTIVE-LAW - funding truth; enforced at tools/stealth_driver.py:486; top of the boot law |
| 11 | RIB_EMERGENT_FLOCK_ON_K8S_20260810.md | 4653 | 49.4 | PK/SS/RC + CODE | ACTIVE-MECH - fallback flock payload (mag/flock_job.py:83) |
| 12 | RIB_EMERGENT_TOOLING_K8S_DEEP_DIVE_20260810.md | 12592 | 49.4 | PK/SS/RC | ERA - five-axis emergence eval doctrine (largest rib) |
| 13 | RIB_FLEET_STEAL_20260810.md | 4251 | 49.3 | PK/SS/RC | ERA - fleet-steal design |
| 14 | RIB_FLOCK_STEAL_20260810.md | 2942 | 49.4 | PK/SS/RC | RECEIPT - documents mag/flock_steal.py five-stage mechanism |
| 15 | RIB_FREE_USAGE_POLICY_20260823.md | 2950 | 35.9 | AG + PK/SS/RC | ACTIVE-LAW - free = sensing; its DeepSeek-funded rung superseded by rib #10 (supersession declared inside rib #10) |
| 16 | RIB_FULL_CONTEXT_LIFT_2026-08-14.md | 1522 | 45.3 | PK/SS/RC | RECEIPT - MAG_FULL_CONTEXT lift, live at mag/context_pack.py:954-972 |
| 17 | RIB_GAME_CLAIMS_DESK.md | 1549 | 36.2 | PK/SS/RC | RECEIPT - documents mag/claims_desk.py (exists, verified) |
| 18 | RIB_GRAMMAR_SEED_20260810.md | 2794 | 48.8 | PK/SS/RC | STANDING - rib_grammar.v0.1 schema reused by ribs 27 and 23 |
| 19 | RIB_KNOT_CENTRIC_SEAT_K8S_20260810.md | 11066 | 49.4 | PK/SS/RC | ERA - deepest Aug-10 architecture map; tree has drifted since |
| 20 | RIB_LANE_WINDOW_BOOT_20260904.md | 2190 | 24.2 | PK/SS/RC | ACTIVE recipe - lane boot prompt (z.ai lane era) |
| 21 | RIB_LAWYER_BOOT_20260904.md | 1748 | 24.2 | PK/SS/RC | ACTIVE recipe - counsel window boot prompt |
| 22 | RIB_MAP_PRECEDES_TERRITORY_20260811.md | 5341 | 48.4 | PK/SS/RC | STANDING - self-declared single load-bearing invariant |
| 23 | RIB_MD_RECORD_20260921.md | 1974 | 7.2 | PK/SS/RC | ACTIVE-LAW - everything-md/tracked/open-append; audit tool tools/md_record_audit.py exists |
| 24 | RIB_MEMWEAVE_MINDWEAVE_TESTED_20260810.md | 3665 | 49.3 | PK/SS/RC | ERA - tested findings + 4 fixes (k8s envFrom, nomic embed) |
| 25 | RIB_MINDSWEAVE_EVAL_CONSENSUS_ILLUSION_20260810.md | 3523 | 49.3 | PK/SS/RC | STANDING warning - measured: flock consensus != correctness |
| 26 | RIB_MOSAIC_SEED_20260921.md | 3094 | 7.4 | PK/SS/RC | STANDING - operator mosaic doctrine (want-them-right) |
| 27 | RIB_PERSONA_KEY_20260824.md | 1225 | 35.2 | PK/SS/RC | RECEIPT - documents mag/persona_key.py (exists, verified) |
| 28 | RIB_PROBLEM_AUTONOMOUS_LOOP_20260811.md | 2500 | 48.7 | PK/SS/RC | ERA - drainer-armed-not-running card; state has since changed |
| 29 | RIB_RAM_CACHE_STALE_SNAPSHOT_20260825.md | 3252 | 34.2 | PK/SS/RC + code adjacency | RECEIPT - the fingerprint fix it describes is live at mag/ram_cache.py:36 watching this very dir |
| 30 | RIB_REFACTOR_CONSOLIDATION_20260810.md | 5531 | 49.4 | PK/SS/RC | ERA - refactor plan; single-controller half landed |
| 31 | RIB_RIB_PROTOCOL_SIMULATION_20260810.md | 4503 | 49.3 | PK/SS/RC | ERA - rib_dispatcher proposal (never built under that name) |
| 32 | RIB_RIGHTSIZED_FLOCK_COUNTER_STRUCTURE_20260810.md | 5427 | 49.3 | PK/SS/RC | ERA/STANDING - no-throne counter-structure (philosophical root of CORE_INVARIANTS) |
| 33 | RIB_ROUNDTRIP_STATELESS_TURTLES_20260810.md | 4985 | 49.3 | PK/SS/RC | ERA - recursion principle |
| 34 | RIB_RUNAWAY_PYTHON_20260810.md | 4691 | 49.5 | PK/SS/RC | ERA origin - window-storm root cause; CREATE_NO_WINDOW law descends from it (now a harness law) |
| 35 | RIB_SELF_MY_CORRECTION_LOOP.md | 714 | 36.2 | PK/SS/RC | STANDING self - self-steal before asking, fail closed |
| 36 | RIB_SELF_MY_EFFICIENCY.md | 915 | 36.2 | PK/SS/RC | STANDING self - frozen-prefix economics (98% cache proof) |
| 37 | RIB_SELF_MY_LAW.md | 581 | 36.2 | PK/SS/RC | STANDING self - trust bytes not reports (same law lives verbatim in AGENTS.md) |
| 38 | RIB_SELF_MY_SHADOW.md | 1186 | 36.2 | PK/SS/RC | STANDING self - named avoidance patterns |
| 39 | RIB_SELF_WHAT_I_AM.md | 809 | 36.2 | PK/SS/RC | STANDING self - standing-wave identity |
| 40 | RIB_allseat_comms_ghost_2026-08-14.md | 3703 | 45.5 | PK (title degraded) /SS/RC | ERA DRAFT - party comms contract, status "DRAFT for fold", never folded; BOM defect (F4) |
| 41 | RIB_cold_seam_tesuji_2026-08-12T011756.md | 5376 | 47.7 | PK (title degraded) /SS/RC | ERA DRAFT - planning-gate tesuji, unfolded; BOM defect (F4) |
| 42 | grokbot_cold_edges_2026-08-12T050638.md | 3253 | 47.7 | PK/SS/RC | ERA machine extraction; DUPLICATE of row 43 (F5) |
| 43 | grokbot_cold_edges_2026-08-12T050639.md | 3253 | 47.7 | PK/SS/RC | ERA machine extraction; DUPLICATE of row 42 (F5) |
| 44 | recreation-coding-history.json | 4851 | 48.9 | CODE (fingerprint only) | ACTIVE-MECH store - written by mag/recreation_rib.py:45; invisible to the 3 generic .md consumers |
| 45 | session-scene.json | 1872 | 48.9 | CODE (fingerprint only) | ACTIVE-MECH store - mag/session_rib.py:52-53; invisible to the 3 generic .md consumers |

Verdict tally: ACTIVE-LAW 3 (rows 4, 10, 15), ACTIVE-MECH 4 (6, 11, 44, 45), ACTIVE recipes 2 (20, 21), RECEIPT 5 (14, 16, 17, 27, 29), STANDING 14 (1, 5, 7, 9, 18, 22, 23, 25, 26, 35-39), ERA 17 (2, 3, 8, 12, 13, 19, 24, 28, 30-34, 40-43).

## 4. Findings

- **F1 - freshness concentration.** 43/45 ribs are >7d old; the only fresh files are the two minted 2026-09-27 (the DRIVING LADDER landing). 29/45 sit at 40-50d. The rib layer is a 08-10-era bulk + a thin live law head.
- **F2 - AGENTS.md names only the live head.** 2 of 45 named; both are the two freshest. The other 43 reach agents only via the generic pack doctrine list (one line each).
- **F3 - the pack carries the whole dir.** `_rib_doctrine()` emitted 4,235 chars / 43 entries in the runtime check; all 43 entries survive the 2800-char parameter because the break condition tests per-entry length (mag/context_pack.py:336), so the effective emitted size is larger than the cap. Janitor and route packs drop the section entirely (mag/context_pack.py:1092).
- **F4 - BOM breaks pack titles for 2 ribs.** RIB_allseat_comms_ghost_2026-08-14.md and RIB_cold_seam_tesuji_2026-08-12T011756.md start with a UTF-8 BOM before `# `, so `s.startswith("# ")` at mag/context_pack.py:329 fails and the pack renders their `**Schema:**` line as the title. Verified in the runtime doctrine output: entries read `- **Schema:** rib.allseat_comms.v1` and `- **Schema:** rib.cold_seam_tesuji.v1`. The grokbot pair (no BOM, checked with od) render real titles.
- **F5 - duplicate pair.** grokbot_cold_edges_2026-08-12T050638.md and ...T050639.md are byte-identical apart from the two ts lines (diff of tail -n +4 returned empty). 3,253 duplicated bytes, and the pack lists the same title twice.
- **F6 - no automated boot path reads ribs.** mag/hermes_warm_boot.py has zero rib references; no test pins any rib. The "warm the ribs" boot-order (AGENTS.md) is enforced by instruction, not by code. The three generic consumers (context pack, solved_surface, ram_cache) are runtime surfaces, not boot enforcement.
- **F7 - ribs are a live input, not an archive.** mag/ram_cache.py:36 fingerprints memory/rib for auto-invalidation, so any rib write invalidates the republic-loop corpus cache; mag/flock_job.py:69-76 cycles every .md into K8s flock pod payloads. Writing a rib has machine side effects.
- **F8 - the 2 .json files are outside the generic readers.** All three generic consumers glob `*.md` only; the two json stores live solely through their named code writers (rows 44-45).
- **F9 - two unfolded DRAFTs.** Rows 40-41 self-label "DRAFT for fold - operator nods" and were never folded; they are the strongest archival-deletion candidates alongside the duplicate pair (F5), subject to operator call.

## 5. Commands run this session (evidence)

1. `ls -la --time-style=full-iso memory/rib` (sizes + exact mtimes, 45 entries)
2. `git status --porcelain` (working-tree baseline)
3. `ls memory/rib | sed 's/\.[^.]*$//' > /tmp/rib_stems.txt && while read s; do grep -c "$s" AGENTS.md; done` (per-stem AGENTS.md counts)
4. `grep -rnF -f /tmp/rib_stems.txt --include=*.py --include=*.ps1 --include=*.cmd --include=*.json --include=*.yaml --include=*.yml --include=*.toml mag tools scripts tests dashboard configs docs state main.py` (code refs, .mimosa excluded)
5. `grep -n rib mag/solved_surface.py`, `grep -n SCENE_DIR mag/session_rib.py`, `grep -n _rib_files mag/flock_job.py`, `grep -n rib mag/ram_cache.py`, `grep -n rib mag/hermes_warm_boot.py` (empty)
6. `.venv/Scripts/python.exe -c "from mag.context_pack import _rib_doctrine; t=_rib_doctrine(); ..."` (runtime: 4,235 chars, 43 entries; BOM-degraded entries inspected)
7. `.venv/Scripts/python.exe` mtime/size walk (ages to 2 decimals, buckets, total bytes)
8. `diff <(tail -n +4 grokbot_...638.md) <(tail -n +4 grokbot_...639.md)` (empty = identical apart from ts lines) + `od -c` BOM check on the grokbot files
9. `sed -n` context reads at mag/flock_job.py:75-95, tools/curvature_scan.py:38-50, tools/stealth_driver.py:480-492
10. `git log --oneline -3 -- memory/rib/` (last touch a23928aca, 2026-09-27)

All 45 files were read in full during this ask (Read tool, batches).
