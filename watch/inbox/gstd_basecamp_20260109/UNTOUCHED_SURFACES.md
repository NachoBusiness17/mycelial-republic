# UNTOUCHED SURFACES - staleness census (GSTD basecamp, STALENESS lane)

Instrument: .venv/Scripts/python.exe mtime scan (glob + os.walk), stat-level only, no content walks.
Moment: 2026-10-09T04:30Z. Stale bar: last touch older than 2026-09-18 (~21d). 2195 files censused.
Machinery pages (LIVE_REPORT / REDBOARD / START_BRIEF) excluded from state/ per load-order row 0a.

## Surface staleness table

| Surface | Stale / total | Pct | Oldest touch | Verdict |
|---|---|---|---|---|
| docs/ref/*.md | 171 / 190 | 90% | 2026-08-04 | worst wide surface; includes mandated boot rows 3-6 |
| queue/** (all) | 615 / 691 | 89% | 2026-07-24 | largest unsummarized mass, never ledgered by age |
| configs/*.yaml | 35 / 45 | 77% | 2026-08-04 | includes version_roadmap.yaml, the cited "machine arc" |
| memory/improve/* | 36 / 49 | 73% | 2026-07-24 | daily face fresh, deep trove frozen July-Aug |
| memory/game/** | 16 / 24 | 66% | 2026-08-14 | world_state live 10-08 but campaign history dead |
| state/*.md (authored) | 15 / 23 | 65% | 2026-08-08 | SANITY + PAUSE_PROTOCOL 42d old while fleet grew |
| tools/*.py | 29 / 346 | 8% | 2026-08-07 | July-Aug toolbelt tail, mostly superseded |
| .agents/skills/*/SKILL.md | 1 / 31 | 3% | 2026-09-02 | only verb-genomes stale; healthy surface |
| corpus/game_estate/** | 0 / 15 | 0% | 2026-09-22 | fresh, no action |

## Oldest 15 regardless of bar (grouped where same class)

| Last touch | Path | Purpose (from head) | Data-value guess |
|---|---|---|---|
| 2026-07-24 | memory/improve/hermes_self_improve_report.md (+STARTED.txt, result.json) | "Hermes self-improve report (STOPPED early - operator cut)" | HIGH: founding self-improve run, why cut, never resumed |
| 2026-07-24 | memory/improve/triage-2026-07-25.md | "Improve triage 2026-07-25" | MEDIUM: baseline for what improve still owes |
| 2026-07-24 | queue/results/20260725-0031/0031/0035*-hermes.json (3 files) | hermes probe results | HIGH as a class: unexamined result ledger |
| 2026-07-24 | queue/results/tmpvlnnejkn.txt | tmp scratch | ZERO: delete candidate |
| 2026-07-24..27 | memory/improve/daily/2026-07-2[4-6].md, evals/2026-07-2[4-5].json, daily/2026-07-25-field.md | early daily scout + eval records | LOW alone: series only matters as trend baseline |
| 2026-07-27 | memory/improve/evals/models/kimi-k3-2026-07-27.md | model eval note | LOW: one model, pre-fleet era |

## Stale beyond the oldest 15, by surface (the >21d highlights)

- state/: PAUSE_PROTOCOL.md + SANITY.md (08-27, host stop/resume order and what-runs-loose registry), HOW_TO_RUN_THIS_20260826.md (08-25), m12_README.md (09-11, operator-load baseline), T1_GO_20260906.md, 08-08/08-10 closeout set (MAG, DIRECTION, WHAT_REMAINS, SESSION_SEED, AUDIT_STACK). SANITY is the one with real decision power: scheduled tasks, crons and emulators multiplied since 08-27.
- docs/ref/: 171 stale. The mandated boot load-order rows are themselves the stale class - OPERATOR_CARD.md (row 6, 08-04, 65d), MYCELIAL_SCIENCE_MAP.md (row 3, 08-06), MAG_DIRECTION_ARTIFACT_v2.md (row 4, 08-06), MAG_PROJECT_PROPOSAL.md (row 5, 08-06). Also HONEST_COST_LEDGER / STEAL_MATRIX / UTILIZATION_MAP (08-28, 41d) and DATA_LAYERS, GAME_SALON_LOOP, TABLE_SHELL_ARCH (08-06/07).
- configs/: version_roadmap.yaml + releases.yaml (08-06, cited by AGENTS.md as machine arc), blast.yaml / data_tiers.yaml / features.yaml / lanes_vast_rtx8000.yaml (08-04; the lanes_vast file self-describes as a pending merge into lanes.yaml, 65d pending).
- tools/: 29 stale - the 08-07 pipe/probe set (autopilot, one_pipe, smoke_import), ghost_tournament (08-10), coordinate_fleet (08-14), sense_tools (08-28). Unknown whether anything still imports them.
- memory/game/: campaign_runs jsonl set (08-14/15) + adventure/state.json (08-18) - the August self-play campaign, never mined.
- skills/: verb-genomes/SKILL.md (09-02, 36d) - the only stale skill; never usage-counted against skill_ledger.jsonl.

## TOP 5 "deserve data" - ranked, one-lane mining plans

1. queue/ ledger census (615 stale of 691). Plan: mtime histogram + join queue/handoff asks (peer-*/cloud-*) against queue/results by name, run tools/queue_row_census.py, land QUEUE_AGE_LEDGER.md. Decision it informs: archive-vs-keep for the 89% dead mass, and whether any ask from July-Aug still has an unclaimed result.
2. docs/ref boot-order four (rows 3-6 of the load order). Plan: one lane reads the 4 docs (plus HONEST_COST_LEDGER) against current canon (state/CURRENT.md, VERSION_REGISTRY) and files a still-true / drifted verdict per doc. Decision: rewrite the AGENTS.md load order or freeze each doc with reason. This is the literal disease class - docs that outrank their bytes.
3. state/SANITY.md + PAUSE_PROTOCOL.md re-enumeration (42d). Plan: enumerate what actually runs now (schtasks Mag*, ollama list, cron/patrol log tails) and diff against the 08-27 registry. Decision: what tonight's lanes may safely run alongside; the registry predates the scheduled-task boom.
4. memory/improve July-Aug goal trove (36 entries). Plan: read GOAL.md, MIRROR.md, roadmap_gap_report.json, gstd_probe_report.json, meta_graph_plan.md; score each goal hit / missed / obsolete by the October estate. Decision: whether the improve promotion ladder (auto_promote, candidates.jsonl) still points at real gaps.
5. configs consumer census (35 stale). Plan: grep mag/ + tools/ + scripts/ for each stale yaml name; anything with zero live consumers is a dead-config prune candidate; lanes_vast_rtx8000.yaml is a 65d pending merge to close. Decision: shrink config ambiguity at boot.

Runner-up: memory/game campaign_runs mining - what the August campaign proved vs the live world_state.

## Machinery cross-check (tools/freshness_check.py) - blind spots

What it meters: CRITICAL_DOCS only - BOOT_4_7.md, state/CURRENT.md, state/START_BRIEF.md, state/HANDOFF.md (freshness_check.py:60-65). Of those, BOOT_4_7 + HANDOFF sit in FROZEN_OK and START_BRIEF is machinery-regen excluded. Net: exactly ONE live doc (state/CURRENT.md) is freshness-metered, by last-commit age with a heartbeat-scaled 1-7d bar.

Blind spots this census found:
- 22 other authored state/*.md pages (15 stale) unmetered, incl. SANITY and PAUSE_PROTOCOL.
- queue/ (89% stale) has no freshness surface at all; queue_row_census is content-row counting, not age.
- docs/ref/ (90% stale) unmetered, including four docs the load order MANDATES every session - the meter guards the front door while the required reading rots.
- configs/ (77% stale) unmetered, including the cited machine-arc roadmap.
- memory/improve + memory/game stale troves unmetered (census_drift_patrol watches only the AGENTS.md test-count line; FTS + census tasks watch corpus + tests).
- The meter reads git commit age, falling back to mtime only for untracked files - a committed-but-drifted doc whose bytes moved in the working tree is invisible to it.

Receipt: this file. Raw scan output in the lane transcript; no content walks performed.
