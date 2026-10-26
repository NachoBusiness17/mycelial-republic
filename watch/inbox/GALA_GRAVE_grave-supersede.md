# GALA GRAVE RECEIPT: grave-supersede (division C gravedigger, ball 20260929)

- **Lane:** grave-supersede, division C (GRAVEDIGGER), ball 2026-09-29
- **Scope:** census of `queue/handoff/*.json` (38 files) for entries whose work verifiably landed elsewhere; one receipt per fossil
- **Action:** 19 graves filed as receipts. **No file was deleted, moved, or edited. Deletions are operator-gated; nothing was requested or performed.**
- **Instrument:** `tools/grave_classify.py` single-file runs with explicit canonical labels and disk-verified successors (README law: `queue/handoff/README.md`, adopted by gala lane a25 2026-09-25)
- **Evidence log:** `watch/inbox/ball2/graves/grave-supersede.check.txt` (includes a same-window ERRATUM on a wrong consumer count)
- **Machine rows:** `watch/inbox/ball2/graves/grave-supersede.jsonl` (19 rows, one per grave)
- **Per-grave receipts:** `watch/inbox/ball2/graves/grave-01..19-*.md`
- **Inputs honored:** f-13 (`watch/inbox/burn_reset_20260927/flash50/f-13.md`, the 133-entry handoff promise), `watch/inbox/FOSSIL_CENSUS_20260927.md`, and the three GALA_GRAVE receipts of 2026-09-25/26 as format precedent

## GRAVE TABLE (19)

| # | Buried entry | Class | Successor (resolving pointer) | Evidence |
|---|---|---|---|---|
| 1 | HANDOFF-2026-09-16-index-foldback.json | DONE-ELSEWHERE | watch/inbox/INDEX.json (1,943 items) + index_events.jsonl (6,557 rows) | closure block in the file itself: closed 2026-09-26T03:37:50Z by gala-lane-b5-index-foldback, verdict MET-WITH-DRIFT; b5 check log verified on disk (142,913 B) |
| 2 | HANDOFF-2026-09-16-bones-referee.json | DONE-ELSEWHERE | mag/bones_adapter.py | contracted artifacts landed 2026-09-16: mag/wow_bones_session.py (11,108 B), tests/test_wow_bones_session.py (6,356 B), adapter docstring cites the directive |
| 3 | HANDOFF-2026-08-08-SANCHO-SPIKE.json | SUPERSEDED-BY | main.py (autorun drainer + deliberate-ask) | c2 rows 7/8 (2026-09-25); mag/sancho_router.py, vscode-mag-map/sancho.js, direct.js all absent re-verified 2026-09-29 |
| 4 | HANDOFF-2026-08-08-5-item.json | SUPERSEDED-BY | queue/todo.md | return_path memory/runs/handoff/2026-08-08-5-item/ never existed; phases carried by research_packs/, quantized_thought/ (recompiled 2026-09-28), MAG_DIRECTION_ARTIFACT_v2.md; steer-telemetry item recorded NOT LANDED |
| 5 | cloud-925cb9b3ae.json | DONE-ELSEWHERE | dashboard/static/shell.js | mirror of peer a5c69a4520 (c2 row 1); shell.js + index.html present |
| 6 | cloud-09eadb5328.json | DONE-ELSEWHERE | mag/feature_lab.py | mirror of peer 56b8cc3c06 (c2 row 2); feature_lab.py + tests present |
| 7 | cloud-03d6edbb13.json | DONE-ELSEWHERE | mag/feature_lab.py | mirror of peer 735bae9a90 (c2 row 3), chained to row 2 which landed; CROSS_AGENT_VERKLE_HANDOFF.md on disk |
| 8 | cloud-a9feee5e19.json | SUPERSEDED-BY | watch/inbox/ARENA_V2_CONSTELLATION_SALON_20260913.md | mirror of peer 046de3834b (c2 row 4); salon receipt present (3,751 B) |
| 9 | cloud-4d13163024.json | SUPERSEDED-BY | mag/swarm_tools.py | mirror of peer 9cdc923dc6 (c2 row 5); memory/shared_scratch absent re-verified |
| 10 | cloud-226ac2d50f.json | SUPERSEDED-BY | mag/riddler.py | mirror of peer a6a4e4e9b0 (c2 row 6); riddler.py present |
| 11 | cloud-854d2f588b.json | SUPERSEDED-BY | main.py | mirror of peer 605e1df369 (c2 row 7); deliverables absent re-verified |
| 12 | cloud-653a5d4f14.json | SUPERSEDED-BY | main.py | mirror of peer 9646d6beec (c2 row 8); deliverables absent re-verified |
| 13 | cloud-760cc3471f.json | SUPERSEDED-BY | memory/rib/ (+ frozen-RIB deliberate-ask law) | mirror of peer 7bce5aea37 (c2 row 10); system.yaml/shader_lib.py/render_audit.py absent re-verified; c2's named carrier VERKLE_RIB.json is itself grave 19 |
| 14 | cloud-dfc6027bae.json | SUPERSEDED-BY | campaigns/sunless_citadel | mirror of peer a3c9880f05 (c2 row 9); session_state_protocol.py + world.yaml absent re-verified |
| 15 | cloud-75a0c7433c.json | DONE-ELSEWHERE (partial) | vscode-mag-map/control_room.js | mirror of peer a46efc8273 (c2 row 11); control_room.js present; direct.js never built |
| 16 | cloud-3b5553e28f.json | ABSORBED-BY | mag/lane_runner.py | mirror of peer 9ce633bb4a, CLOSED by afterparty t17 (closure block ABSORBED-BY, evidence watch/inbox/gala_20260925/afterparty/lanes/t17.check.txt); z_ai default_model gap stays recorded open |
| 17 | cloud-f82f9a1fb6.json | DONE-ELSEWHERE | mag/game_freeze.py | standalone (no peer mirror); game_freeze.py brawl-aware, game_brawl_perspectives.py, ghost_talk.py, memory/working/research/ all present |
| 18 | qwen-wire-test-20260807.json | FOSSIL | (none needed; ingest is standing code mag/handoff_inbox.py:19-29) | one-shot hello-world wire test, 2026-08-07, 53 days stale |
| 19 | VERKLE_RIB.json | FOSSIL | memory/biography/verkle_chain.jsonl (live, 8,390 knots, tip 2026-09-29T14:42:49Z) + regenerator mag/verkle_rib.py | derived export (writer RIB_OUT at mag/verkle_rib.py:38; documented VERKLE_REBUILD_COMPLETION_20260901.md:69 at 6,497 knots); 27 days stale, no reader in tracked code |

## CENSUS ROWS NOT GRAVED (13 files + 1 closed file, honest non-burials)

| Population | Count | Disposition | Evidence |
|---|---|---|---|
| 20260929-10xxxx-taskold-files-probe.json | 3 | STILL-RELEVANT: pending work created today 06:01-06:06Z; return_paths absent from queue/results/ (grep count 0) | batch run in check log section B |
| *.meta.json (DEEP_DIVE_VERKLE_SELFREPLICATION, DEEP_RESEARCH_FLOCKING_GA, STEAL_FREE_COMPUTE, STEAL_MEMLANG_QUANTIZER) | 4 | not work orders: run-cost stubs for sibling research .md files, all 4 siblings present on disk; not burials | batch run in check log section B |
| peer-9ce633bb4a.json | 1 | already CLOSED 2026-09-26 by afterparty t17 (closure verdict ABSORBED-BY in-file); not re-graved | grep in check log section C |
| peer-*.json (rest) | 11 | already dispositioned by GALA_GRAVE_c2-peer-json-graves.md (2026-09-25); out of scope | c2 receipt |
| peer handoffs still pointing at live obligations | 0 found | n/a | c2 row 12 (9ce633bb4a) was the only STILL-RELEVANT and is now closed (row 16 above) |

Population arithmetic: 38 JSONs = 12 peers (c2) + 13 cloud-*.json (all graved) + 4 HANDOFF-*.json (all graved) + 4 meta stubs + 3 probes + VERKLE_RIB.json + qwen-wire-test (both graved). 19 + 13 non-graves + 12 prior-lane = 44 rows over 38 files (peers counted once at c2).

## Classification counts

- DONE-ELSEWHERE: 7 (graves 1, 2, 5, 6, 7, 15, 17)
- SUPERSEDED-BY: 9 (graves 3, 4, 8, 9, 10, 11, 12, 13, 14)
- ABSORBED-BY: 1 (grave 16)
- FOSSIL: 2 (graves 18, 19)
- STILL-RELEVANT (not burials): 3 probes + 4 meta stubs

## F-13 linkage

f-13 (2026-09-28) recorded the docs' promise of a 133-entry `queue/handoff/`
and the 2026-09-29 census finds 38 JSONs (+~100 Aug-era .md notes) in the
same directory. This lane's graves retire 19 of the 38 JSON entries as dead
letters with named successors, which is the swamp-drain the README's
retirement path was adopted for (queue/handoff/README.md, gala lane a25).

## Burial terms

Receipts only. Every buried file stays on disk byte-identical. The register
appends live in `watch/inbox/index_events.jsonl` (writer
gala-grave-supersede-20260929). No git commands, no paid APIs, $0.

Filed 2026-09-29 by lane grave-supersede.
