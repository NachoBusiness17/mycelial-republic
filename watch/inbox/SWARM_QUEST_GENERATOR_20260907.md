# SWARM QUEST GENERATOR — THE RUN eats the real backlog (2026-09-07)

Builder: questgen · KNOCK-OUT #11 · R6 promotion #1 (research/corpus_triangulation/R6_swarm_apk.md §3) · $0, no network, no daemons, streaming reads.

## Files
- `mag/swarm_quests.py` — the bridge: swarm queue ledgers → RUN quests (stream, one task file at a time — never slurp).
- `dashboard/static/shadow_quests.json` — {schema swarm_quests.v1, quests[], boss: THE FORMATEATER, stats} — THE RUN's quest source. **shadow_walk.html NOT touched** (runner owns the page today); the page can consume this next pass.
- Tesuji cells: `R/swarm/quest-generator` + `R/swarm/format-eater-boss`, seat questgen (watch/TESUJI_MAP.jsonl).

## Ground truth (live bytes, 09-07 — drifted +5 from the R6 snapshot)
- Queue: **1,280** tasks (R6 measured 1,275 on 09-06; 5 landed since): **480 failed / 228 done / 572 cancelled**.
- Result files: results/ 748 + results_incoming/ 44. **706 of 1,280 tasks resolve to a REAL result file (55.2%)** — 478 failed + 228 done. (Results/queue drift: 42 result files have no live queue task.)

## The transform (format-eater law applied, not recited)
task → quest {quest_id=task_id, title (goal trimmed: fuel-pointers stripped, cut at em-dash, cap 80), biome by status: failed→dark-zone-boss-room / done→lit-loot-room / cancelled→fog-zone, verdict_source (the task's REAL result path, results/ then results_incoming/), reward (loot tier common→relic by backlog age/depth)}.

**THE FORMATEATER IS THE FIRST BOSS**: the 478 failed-format tasks ARE the boss encounter — hp = count, weakness = `goal+format+verdict`, defeat = restate its goal in contracted form. Every failed swarm task is one of its teeth.

## Falsifier (anti-hallucination rule)
- build: `PHANTOM_QUESTS=574` — tasks with NO result file are **excluded, never emitted as quests**. Emitted set: **0 phantom verdict_sources, every path EXISTS on disk** (self-check PASS).
- Honest structural finding: **fog-zone = 0 quests.** All 572 cancelled tasks carry no verdict file (they never ran) — the falsifier withholds them. Fog zone is the shape of *unproven*, and the generator refuses to fabricate loot where no verdict exists. The reap (R6 promotion #3: width-50 replay with goal+format+verdict grammar) is what would populate the fog.
- `python -m mag.swarm_quests verify` → PASS: 706 quests / 1280 tasks, phantom=0, boss hp=478, all verdict_sources exist.

## Next door
shadow_walk page consumes `dashboard/static/shadow_quests.json` (quest board, boss bar, loot tiers) — one fetch, zero deps, next pass. Re-run `build` any time the queue moves; quests are fleet state, verbatim, path-addressed.
