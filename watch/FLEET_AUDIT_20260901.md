# FLEET AUDIT — how the new structure maps to old attempts (2026-09-01 ~02:35Z)

**Question (operator):** how does the seat map map to our old system attempts? Ask the elder, check the verkle, full self-audit, fanned out parallel.
**Method:** 4 parallel worker lanes (A attempts-archaeology, B elder, C verkle, D seat-map-reconciliation) + direct deref of elder receipts + organ_map.py source. Every claim path-cited in lane drafts. Elder law in force: *contradictions resolve by evidence and hierarchy, not vote.*

## Verdict

The seat map is **not a new system attempt — it is the org chart for the 5th attempt of the one recurring idea**. Lane A proves the sovereign/autonomous-loop concept was rebuilt ≥4× (gate-test 07-27 → 12h-sovereign-run 08-03 → steer_router 08-10 → ask_router/governor 08-31). Lane D proves the new structure **refinances existing organs**: 5 CONTINUATIONS, 6 RENAMES, 1 genuinely-new slot (codex paste), **0 resurrections** — nothing dead is being rebuilt, nothing live is being duplicated as a corpse. The risk is routing, not invention.

## Seat/lane → prior organ mapping (lane D, /board/AUDIT_D_MAP_20260901.md)

| New | Prior organ that already does it | Category |
|---|---|---|
| Director | Grok TUI + 5.3-flash-high (existing lanes) | RENAME (role split) |
| Driver | this session (route fixed 01:21Z) | RENAME |
| Hands | DS-flash off-peak + codex desktop seat | CONTINUATION (codex paste = the 1 new slot) |
| Tail | glm-4.7-flash $0 + ollama dumb | RENAME |
| Swarm | cerebras/groq/together fan-out via sessions_spawn + seat_dispatch | RENAME (orchestrator exists) |
| Standing self | zai-2 frozen-prefix cache-mining (measured 97–99.9% tonight) | CONTINUATION |
| Harvest lane | archivist_feed_harvest cron 26046696 (v4 kit) | CONTINUATION |
| Smell lane | socratic intake + lensed shots (ractor doctrine) | CONTINUATION |
| Probe lane | seat_dispatch probes + LINEAGE_DIFF battery | RENAME (needs merge) |
| Coding lane | codex + DS-flash + Director review | CONTINUATION |
| Salon lane | lane_salon / salon_openclaw / frontier_salon | RENAME (needs merge) |

## Old-attempts census (lane A, /board/AUDIT_A_ATTEMPTS_20260901.md)

- **~33 named attempts** evidenced in /mag/memory/runs (450 entries): **9 LIVE** (governor, orchestrator, seat_steer, seat_spend, ask_router, session_bridge, board_tailer, party_subchain, republic_os), **16 DEAD** (every dated run.json carries `status:"closed"`), **~6 DORMANT** (fuel_feed, steer_router, lane_salon, riddler_coherence, seed_percolator, frontier_advice).
- **Rebuild patterns:** empty_recovery rebuilt in **3 waves** (25× 08-03, 1× 08-04, 19× 08-30 — same schema); sovereign-loop ≥4 attempts; continuity proven, binary not identical.
- Dead attempts carry their lessons in the failure ledger; none is being resurrected by the seat map.

## Elder verdict (lane B + direct deref, /board/AUDIT_B_ELDER_20260901.md)

- Standing audit 2026-08-31 04:55Z: **27 organs — DECLARED 27 / INSTRUMENTED 26 / WIRED 27 / STATEFUL 25 / VERIFIED 27 / LIVE 17 / GHOST 0; gap_count 0** (after a 7→0 repair loop 04:27–04:55).
- The elder audits a **hardcoded REGISTRY** (organ_map.py:46+): the fleet-structure files were **invisible to it** until now.
- **Dogfood fix applied:** `/patches/patch-fleet-structure-registry.json` adds a `fleet_structure` entry (source = watch/FLEET_STRUCTURE_20260901.md, state_paths = slot map + 4 lane drafts, receipt_paths = this synthesis). Honest levels it will earn: DECLARED + STATEFUL — **not** WIRED/LIVE, because the lanes are not wired yet. The elder ladder is now the structure's acceptance gate: no lane claims LIVE until the registry shows it.
- Evidence ladder (organ_map.py:9-15): DECLARED=source exists → INSTRUMENTED=callable imports → WIRED=caller exists → STATEFUL=state exists → VERIFIED=probe passes → LIVE=recent receipt ≤24h → GHOST=declaration only.

## Verkle verdict (lane C, /board/AUDIT_C_VERKLE_20260901.md)

- Chain **healthy**: **6,312 knots** (idx 0..6311), parent→prev-root chained 6311/6311, 0 orphans, 0 dup indices. Tip root `2670c7ea555c` at **2026-09-01T02:27:46Z** — the tip ticked *during* this audit.
- Milestones: genesis idx 0, first constitution idx 7, first fact_bus idx 1111, first memlang idx 2751.
- Correction to prior usage: event tie-in is `link --event --when` (not `tie_in`).
- Ready host commands:
  - `python -m mag.verkle_lance link --event "FLEET_STRUCTURE law filed" --when "2026-09-01T01:52:00Z"`
  - `python -m mag.verkle_lance link --event "fleet audit 2026-09-01: structure maps to attempt #5, refinances 9 live organs" --when "2026-09-01T02:35:00Z"`

## Collisions and merges (lane D)

1. **Salon lane vs 3 salon organs** — merge: Salon lane = router/clock over ONE canonical substrate (`lane_salon`); the other two become invocation aliases. UNKNOWN: shared room.jsonl — blocks dispatch until checked. Note: lane_salon last ran 08-29 → prepend a fresh heartbeat or the rename is a renamed-corpse.
2. **Probe lane vs 4 probe batteries** — merge: ONE frozen probe-battery ledger (LINEAGE_DIFF = canonical unit); probe lane = off-peak scheduler appending to it.
3. **Harvest lane vs OPS_RESEARCH_LOOP intake** — merge: one cron (26046696), two named gaps, one triage queue.

## Repeat-risks (from the failure ledger) and their meters

- **Write-ahead-of-reach** (the 13:33Z "salon fired" defect): the spec's "lanes live" lines are currently DECLARED-level. Meter: elder registry is the single source for LIVE claims; the better-by-default ladders ship inside each lane block.
- **Salon yield meter** (72h repetition cap + lens gate-runtime meter) must be inherited by the Salon lane, not re-invented.
- **empty_recovery pattern**: 45 instances across 3 waves = the cost of loops with no receipt discipline. Meter: every lane run appends a receipt (the archivist doctrine already does this).

## Host runbook (one pass, when ready)

```text
.\.venv\Scripts\python.exe -m mag.openclaw_patches apply   # applies fleet-structure registry patch
.\.venv\Scripts\python.exe -m mag.organ_map snapshot
.\.venv\Scripts\python.exe -m mag.elder                    # fresh audit incl. fleet_structure
.\.venv\Scripts\python.exe -m mag.verkle_lance self_check
python -m mag.verkle_lance link --event "FLEET_STRUCTURE law filed" --when "2026-09-01T01:52:00Z"
python -m mag.verkle_lance link --event "fleet audit 2026-09-01" --when "2026-09-01T02:35:00Z"
```

## Artifacts

- Lane drafts: /board/AUDIT_A_ATTEMPTS_20260901.md · AUDIT_B_ELDER · AUDIT_C_VERKLE · AUDIT_D_MAP
- Patch: /patches/patch-fleet-structure-registry.json
- This synthesis: /board/FLEET_AUDIT_20260901.md (+ mirrored /board/inbox/ per shared-surface law)
- Vault custody (background, separate thread): MXFP4 streaming; see MODEL_VAULT_PASSPORTS.jsonl
