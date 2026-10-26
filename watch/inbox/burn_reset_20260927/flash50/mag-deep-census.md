# mag/ deep census (item s2-05, 2026-09-28)

Census of every Python file under `mag/`. Every number below came out of a command
run during this ask; instruments and moments are named per the census denominator
law. Banked alongside: `_s2-05_census.py`, `_s2-05_stats.py`, `_s2-05_importers.py`
(the sweeps) and `_s2-05_raw.json`, `_s2-05_raw2.json` (raw outputs).

## Instruments

- Primary sweep: `.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/_s2-05_census.py`,
  completed 2026-09-28T22:50:03+00:00. AST parse of all 1,034 mag/ files plus the
  import graph over 24,187 repo `.py` files (dot-dirs, `node_modules`, `__pycache__` pruned).
- Stats sweep: `_s2-05_stats.py` (same venv, file/def distribution).
- Import pass 2: `_s2-05_importers.py` (live-tree vs repo-wide importer split),
  repo snapshot 24,200 `.py` files (13 files appeared outside mag/ between the two
  passes; concurrent lanes are active in this tree).
- Cross-checks: `find`, `wc -l`, `grep -lE`, `tail -c 1` (git-bash), each named inline.
- Stability re-pin at 2026-09-28T23:17:41Z: `find mag -name '*.py' | wc -l` = 1,034,
  `find mag -name '*.py' -print0 | xargs -0 cat | wc -l` = 294,316. mag/ did not move
  between passes.

## Headline counts

| Metric | Value | Instrument |
|---|---|---|
| Python files (modules) under mag/ | 1,034 | ast sweep + `find ... \| wc -l` |
| Non-`__init__` modules | 1,032 | ast sweep |
| `__init__.py` files | 2 (`mag/__init__.py`, `mag/cli/__init__.py`) | `find mag -name '__init__.py'` |
| Packages (dirs holding `__init__.py`) | 2 (`mag`, `mag/cli`) | ast sweep |
| Total lines | 294,323 (`splitlines`) / 294,316 (`wc -l`) | both, delta explained below |
| Total bytes | 12,637,868 | ast sweep |
| AST parse failures | 0 | ast sweep |
| Public defs (all, incl. methods) | 5,742 | ast sweep |
| Public non-method defs | 5,392 | ast sweep |
| Public methods (inside classes) | 350 | ast sweep |
| Top-level public defs | 5,233 | ast sweep |
| All defs incl. private | 10,057 | ast sweep |
| Files with zero public defs | 20 (18 have zero defs at all) | `_s2-05_stats.py` |
| Repo `.py` files scanned for the import graph | 24,187 (pass 1) / 24,200 (pass 2) | ast sweeps |

Definitions, stated once: a "public function" is any `def`/`async def` whose name
does not start with `_`, counted via `ast.walk` (so class methods are included;
the non-method and method splits above separate them). Line counts are physical
lines: `len(text.splitlines())` vs `wc -l`. The 7-line difference between the two
instruments is exactly the 7 mag/ files whose last line has no trailing newline
(`splitlines` counts it, `wc -l` does not; independent `tail -c 1` sweep counted
7 such files).

## Composition

| Where | .py files |
|---|---|
| mag/ top level | 1,028 |
| mag/cli/ | 3 |
| mag/tests/ | 2 |
| mag/ontology_compiler/ | 1 |
| mag/hermes_personas/, mag/watch/ | 0 |

Line distribution (`_s2-05_stats.py`): median 207, mean 284.6, p90 510, p99 1,357,
min 6, no zero-byte files.

## 10 largest by lines

| Lines | Bytes | Public defs | File |
|---|---|---|---|
| 4,838 | 218,080 | 17 | mag/game_campaign.py |
| 4,242 | 186,470 | 74 | mag/ghost.py |
| 3,139 | 128,163 | 32 | mag/agent_cli.py |
| 2,773 | 108,712 | 20 | mag/improve.py |
| 2,183 | 108,914 | 14 | mag/governor_autorun.py |
| 2,056 | 82,227 | 26 | mag/orchestrator.py |
| 1,777 | 71,404 | 5 | mag/voice_turn.py |
| 1,668 | 56,130 | 12 | mag/game_brawl.py |
| 1,362 | 54,863 | 6 | mag/context_pack.py |
| 1,361 | 67,315 | 12 | mag/doctor.py |

## 10 most-imported

Two scopes. "Live" counts importers under mag/, tools/, tests/, scripts/ plus
top-level `.py` files (the running system); "all" counts every repo `.py`
including archaeology snapshot trees (corpus/oral_history/..., dist_audit/,
_archaeology_out/) that carry duplicate copies of old mag/ code. Live is the
primary rank; the archived copies inflate "all" by 2x to 4x.

| Module | Live importers | All importers |
|---|---|---|
| mag.orchestrator | 85 | 303 |
| mag.training_events | 78 | 282 |
| mag.verkle_knot | 71 | 251 |
| mag.swarm_surface | 70 | 290 |
| mag.rib_bus | 48 | 199 |
| mag.operator_inbox | 40 | 122 |
| mag.skill_ledger | 36 | 113 |
| mag.game_world | 32 | 112 |
| mag.swarm_worker | 29 | 117 |
| mag.failure_kb | 25 | 94 |

## 10 never-imported

266 of 1,032 non-init modules (25.8 percent) have zero importers under both
scopes. The 10 largest of those:

| Lines | Entry-point flag | Module |
|---|---|---|
| 970 | yes | mag.fermat_ractor |
| 855 | yes | mag.republic |
| 847 | no | mag.renderman |
| 811 | yes | mag.research_director |
| 740 | yes | mag.decl_attention |
| 738 | yes | mag.dissector |
| 703 | yes | mag.falsifier_counter |
| 698 | no | mag.ga4_progression |
| 695 | yes | mag.refine_loop |
| 666 | yes | mag.transfer_gate |

Reading notes, all from commands run here:

- The entry-point flag means the module's leaf name appears as `python -m mag.<name>`
  somewhere in repo text (py/cmd/ps1/md/yaml/json/toml/txt/html scanned) or in an
  `import_module`/`__import__` string literal. 868 distinct `mag.*` leaf names are
  referenced that way repo-wide; 26 modules are pulled by dynamic string imports
  (agent_arena, ai_landscape, archetype_image, ask_router, coding_session_orchestrator,
  desk_timing, desk_tools, dirac_loop, ecosystem_surface, fireball_cycle, gap_frontier,
  guardrail_sentinel, harness, headless, health, invariant_ledger, knowledge_graph,
  local_scheduler, republic_governance, rib_cache, schema_registry, session_bridge,
  shader_bus, shadow_work, whisper_image, work_contract). Never-imported is a static
  import-graph fact, not a liveness verdict: most of the 266 are CLI entry points.
- 27 further modules are never imported by the live tree but only by archived
  snapshot copies (boot_check, chatgpt_desktop, chord_triangulate, claim_repair,
  code_map, data_refinery, grok_desktop, grok_route, grok_steer, grok_warm_rib,
  idea_flow, invariant_npcs, knot_at_close, loop_health, os_v2, ox_gap, rel_mem_eval,
  rightsize_api, saelis_room, saelis_world_brief, self_audit,
  self_test, session_overseer, swarm_test, tool_lifecycle, usage_digest,
  window_throttle). Live-tree-dead total is therefore 293 of 1,032.
- 0 `__init__.py` files are never-imported (both load with their package).

## Cross-checks run

1. `find mag -name '*.py' | wc -l` = 1,034, matching the ast sweep; re-pinned at
   23:17:41Z (still 1,034 / 294,316 wc-lines).
2. `find mag -name '__init__.py'` printed exactly the 2 files the sweep classified.
3. Line total: `find mag -name '*.py' -print0 | xargs -0 cat | wc -l` = 294,316 vs
   294,323 from the sweep; delta attributed above to the 7 trailing-newline-less files.
4. Import-count sanity on the top module: `grep -lE` over all repo `.py` (pruning
   .venv/.git/__pycache__) found 237 files with line-start `from|import mag.orchestrator`
   and 262 files containing the token `mag.orchestrator` anywhere; the ast count of
   303 importers is higher because the ast also sees `from mag import orchestrator`
   and parenthesized multi-import forms that line greps miss. Relative-form grep
   inside mag/ and tests/ returned 0, so no hidden relative-import mass.
5. Never-imported spot check on mag/renderman.py: a loose repo-wide grep for
   import-ish `renderman` references hit only `mag/grok_mirror.py:182`,
   `mag/grok_terminal.py:157`, `main.py:4090`, and every hit is
   `from mag.renderman_ask import ...` (a different module my loose pattern
   prefix-matched). mag/renderman.py has zero importers; the never-imported call holds.

## Caveats

- Repo-wide importer counts include archived duplicate trees; live-tree counts are
  the primary ranking for that reason.
- `splitlines` also splits on exotic Unicode line boundaries; none affected the
  totals (the wc reconciliation above would have exposed any).
- The import graph is a snapshot of a tree with concurrent lanes writing to it;
  mag/-scoped numbers were stable across two passes 27 minutes apart, the 13-file
  drift was outside mag/.

No em-dashes or en-dashes appear in this file (checked by scan after writing).
