# STEAL — Mag's own self_steal organ
**Date:** 2026-08-14
**Commitment:** `self-steal-organ-001`
**Method:** ran the existing auditor. Did not `--cadence` (would enqueue). No new auditor. No new graph.
**Organs:**
- `mag/self_steal.py` schema `self_steal.v1` — capabilities exist but unused/stale; `$0`, no LLM
- Ghost already loads `memory/runs/self_steal/state.json` into surfaces (`ghost.py` ~241, 3035–3067)
- CLI: `python -m mag.self_steal` (audit) · `--cadence` (audit + leaf + enqueue NEW gaps)

**This pass:** Mag venv `python -m mag.self_steal` at 2026-08-14T15:23:03Z.
n_capabilities=22, n_findings=12. `state.json` still `ts=2026-08-10T04:45:18Z`, `seen=[]` (audit does not write state; cadence does).

## Live findings (auditor)
stale (wired): cache_map, cost_learn, usage_forecast, session_maze, dogfood_audit, whisper_image, shader_bus, guardrail_sentinel
absent (wired): archetype_image, sovereign_handshake, chatgpt_bot, frontier_advisor
research/launch named: sovereign_handshake, chatgpt_bot, frontier_advisor
Not in findings (evidence fresh enough): verkle_knot, surface_steal, ecosystem_surface, cache_router, moonshot_engine, arrival, shape_seed, frontier_council, game_emulator, seat_steer

## Self-steal of the auditor
The auditor is Mag's Huang gate for unused organs. It is itself under-utilized: last cadence Aug 10, seen empty, Ghost will print "close self_steal capability gaps" only if seen is a non-empty list.

**Blind spot (not in CAPABILITIES at all):**
- `skill_ledger` — jsonl n=1437, Ghost reads `n_decisions` from `progress()` which returns `decisions` (`skill_ledger.py` 157–175 vs `ghost.py` 3073)
- `mycelium` — 154 list / 127 unique ids, snapshot frozen 2026-08-10
- `comms_trail` — seen=72, last_capture 2026-08-09

`surface_steal` looks **ok** because `memory/steal/` mtime is today. That is folder morphology. Steals still have 0 mycelium stems and 0 `steal:` KG edges. The auditor cannot see consumption, only that markdown landed.

## TAKE
1. Use `mag/self_steal.py`. Do not write a second auditor.
2. Add three capabilities to the existing `CAPABILITIES` list: skill_ledger (`memory/improve/skill_ledger.jsonl`), mycelium (`memory/mycelium/graph_snapshot.json`), comms_trail (`memory/runs/comms_trail/state.json`). Report-only. Fresh mtime is not utilization if Ghost prints 0.
3. Ghost one-liner: `sl.get("decisions", sl.get("n_decisions", 0))`. Envelope = claim. Existing function, existing key.
4. `surface_steal` utilization must not be folder mtime alone. Evidence should be a graph edge or lingering=0, not `memory/steal` existing.

## REFUSE
- `--cadence` this week (would enqueue three RESEARCH-PACKs).
- A new self-steal markdown as the auditor (this file is the chord, not a replacement module).
- Treating 12 stale/absent findings as a mandate to revive shader_bus/whisper_image. Those are report-only. Chord first.

## TEST
Fail if a second `self_steal` module appears, or if cadence fires research packs for chatgpt_bot before the one-liner reads `decisions`.
Pass if CAPABILITIES contains skill_ledger+mycelium+comms_trail AND LATEST `skill_ledger` is nonzero while jsonl is nonempty.

## Rope
The self-steal organ already watches 22 surfaces and is blind to the three that struck the chord. Plant those three names into the list it already walks.
