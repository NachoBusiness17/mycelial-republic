# W3E — GRAPH HEAL v0 (Mickey17 W3, 2026-09-29)

Lane: Mickey17 W3 · ownership: `tools/graph_heal.py` (new) + `tests/test_graph_heal.py` (new) · NO COMMIT (per ask).

## What landed

The S9 ARC survivorship pass (ledger `watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md`): promotion requires ONE why-context edge; demotion emits forget-pointers; destination is the quantized_thought archive; nothing is ever deleted.

1. **CENSUS** — degree-0 nodes (in+out) by kind, plus duplicate-id byte truth.
2. **HEAL (cheap class)** — one inbound `why_context` edge (marker `heal: graph_heal.v0`) when the orphan's name tokens (alnum, len>=4, own kind-word dropped) match EXACTLY ONE module, OR its source file exists and exactly one other module owns the same basename. Candidates from both rules UNION first: 2+ competing stories heal nothing. Never self-heals.
3. **DEMOTE (pointer law)** — every unhealed orphan becomes a forget-event row `{name -> memory/corpus/quantized_thought/graph_ghosts/<kind>/<label>.md}` in `forget_events.jsonl`, append-only by id. No node removed, no archive file created, graph untouched by demotion.
4. **Idempotent** — rerun adds 0 edges; forget file append-only by id (reruns append 0 rows); heal log is a deterministic mirror of all `why_context` edges.

## Real numbers (instrument: `tools/graph_heal.py` on `memory/knowledge_graph.json`, graph_ts 2026-09-28T19:47:25Z; pre-pass sha256 `89a56bc4…79654`, snapshot kept at `memory/knowledge_graph.json.pre_graph_heal_20260929.bak`)

- CENSUS before: 2062 nodes / 817 edges / **1466 degree-0 orphans** (module 409, knot 400, case_law 300, doctrine 217, steal 140).
- The ask's "1167 orphans" does NOT byte-match any count on this file (1466 total; excluding case_law = 1166). Hand-copied headline suspicion; the tool recomputes, per the B2-69 census law.
- HEAL: **94 edges added** (doctrine 27, module 49, steal 18) — e.g. `leaked_prompt_mine.py` -> 21 vendor-leak doctrines, `diamond_mine.py` -> `steal:DIAMOND_AGE_STEAL`, sibling pairs `browser_driver`<->`browser_env`, `stale_sweep`<->`disposition_sweep`. Ambiguous (2+ modules, healed nothing): 539.
- Anchor cascade (named behavior): an orphan module that anchors another orphan's heal earns out-degree and stops being an orphan itself — 24 such anchors, which is why census-after reads 1348 orphans (1466 − 94 healed − 24 cascaded), not 1372.
- DEMOTE: **1372 listed, 1073 unique ids recorded** (`memory/corpus/quantized_thought/graph_ghosts/forget_events.jsonl`), deleted 0.
- Idempotency proven on the REAL graph: rerun = `RESULT: PASS healed=0 … graph_edges=911`, forget-file bytes unchanged (sha256 `6fc10145…f239a0`).
- Tests: `tests/test_graph_heal.py` — **10 passed** (census fixture, exact heal-edge set, demote-only-lists, idempotency, dry-writes-nothing, real-pass + rerun, pointer collisions, duplicate-id handling, fail-closed exit 2).

## Defect found (upstream, NOT fixed here)

The graph builder emits **300 byte-identical case_law nodes all with id `law:`** (label "law", empty summary, source `memory/improve/skill_ledger.jsonl`). The census now reports `duplicate_ids={'law:': 300}` instead of papering over it. Fix belongs to the graph builder's case_law extractor, not the compaction pass.

## Notes

- Full-suite line (2026-09-29, `pytest -q`, 34:40): **2 failed, 2886 passed, 12 skipped, 3 errors** (log `logs/pytest_full_w3e_20260929.log`). All 5 non-passes are other lanes' debt, none reference graph_heal: 3x `test_healthz_status.py` (`module 'server' has no attribute 'app'`), `test_census_drift_patrol.py::test_cli_collect…` (that file's uncommitted edit is another lane's), `test_headless_law.py` bare-spawn ratchet 22→33 whose 23-file offender list does not include `tools/graph_heal.py` or `tests/test_graph_heal.py`.
- `python tools/violation_ratchet.py check --changed` FAILs on `mag/corpus_selfsteal.py` and `tools/census_drift_patrol.py` — other lanes' uncommitted working-tree debt; `graph_heal.py`/`test_graph_heal.py` are absent from its output (clean).
- Pre-pass snapshot: `memory/knowledge_graph.json.pre_graph_heal_20260929.bak` (sha256 `89a56bc4…79654`). Post-pass forget list sha256 `6fc10145…f239a0`, stable across the idempotency rerun.
