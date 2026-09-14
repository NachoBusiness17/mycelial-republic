# AUDIT D — seat-map reconciliation (fleet → doctrine)
2026-09-01 02:27Z · evidence-only, bounded · rule: cite path:line; UNKNOWN stays UNKNOWN.

Sources: /board/FLEET_STRUCTURE_20260901.md (FS), /board/LANE_SLOT_MAP_20260901.md (LSM),
/root/.openclaw/workspace/MEMORY.md (MEM). Collision refs: /board/*.md on disk.

## A. SEAT → PRIOR ORG MAP

| New seat | Category | Prior Mag system / organ (cite) |
|---|---|---|
| **Director** | RENAME | Grok TUI grok-a/b — already a live seat (`gap_moonshot_20260831.md:18` nearby seat_dispatch; FS:5 "Grok TUI (scarce, judgment only)"). Director = the boundary that grok-a/b already enforced; renamed, not new. |
| **Driver** | RENAME | operator session + session_bridge (`MEM:38` session_bridge + riddler_sanitize = cross-session bus; `MEM:33` ask_router = outcome-memory routing). FS:6 "operator session, idea play". Driver = the live interactive ribbon, renamed. |
| **Hands** | CONTINUATION | DS-flash worker spawns + GOPHER law (`MEM:31` "mechanical fetch/grep/verify → disposable DS-Flash spawns"). Codex desktop seat = pending paste (`FS:16`) = the ONE genuinely new slot; rest re-routes existing keys. |
| **Tail** | RENAME | glm-4.7-flash $0 + ollama local-dumb (`LSM` Tail slot ~70%; `MEM:45` glm-4.7-flash FREE). Tail = the LSM Tail slot reified as a seat; mechanism identical. |
| **Swarm** | RENAME/CONT | swarm_cycle + ask_router (`MEM:33` "swarm_cycle + ask_router = thin ribs"); SWARM_DOCTRINE_20260901 economics (`SWARM_DOCTRINE_20260901.md:3 "when to swarm"`). Swarm = the k8s-pattern ambition on the EXISTING swarm_cycle org; renamed wrap, no new organ. |
| **Standing self** | CONTINUATION | z_ai2 frozen-prefix cache-mine (`MEM:45` cache discipline / run-rate; zai-pro frozen prefix `FS:19` "97–99.9% measured"). Same mechanism, standing identity surface. |
| **second supervisor** | N/A (none) | Explicit red line honored — orchestrator = sessions_spawn + workboard + seat_dispatch (`FS:4`). No new supervisor. Good. |

Seat verdicts: 0 genuinely new, 2 continuation, 0 resurrection, 4 rename. (Codex seat = the only new slot, a pending paste, not a lane.)

## B. LANE → PRIOR ORG MAP

| New lane | Category | Prior Mag system (cite) | Note |
|---|---|---|---|
| **1. Harvest** | CONTINUATION | archivist_feed_harvest cron 26046696 (`MEM:41` "Standing harvest archivist_feed_harvest (cron 26046696, every 8h)"), v3 follow-kit `X_RESEARCH_KIT_20260831.md`, v4 ladder (`MEM:42`). | FS:23 "calls re-slotted per map" — same cron, calls re-slotted. No new organ. |
| **2. Smell** | CONTINUATION | socratic intake + operator-dropped links (`MEM:50` SOCRATIC DISCOVERY LAW; `MEM:55` smell lanes as Creed automation; operator inbox lane `MEM:41`). | lensed shots on operator-dropped links = existing inbox lane + lens protocol. |
| **3. Probe** | RENAME/CONT | probe batteries VERIFIED live: LINEAGE_DIFF frozen 20-probe battery (`LINEAGE_DIFF_DEEPRESEARCH_20260831.md:23`), seat_dispatch probes, economist probes, $0 probe-before-adoption (`OPS_RESEARCH_LOOP_20260901.md:11`). | FS:3 "probe loops — real work". Same probes, now a named lane. |
| **4. Coding** | CONTINUATION | Hands seat = DS-flash + codex (`FS:16`); director reviews diffs. GOPHER fetch/verify already coded. | No new model; new = codex review pairing (pending paste). |
| **5. Salon** | RENAME | frontier_salon + salon_openclaw + lane_salon ALL live (`gap_moonshot_20260831.md:20-22`; `FRONTDOOR_MISSING_JOINS_20260901.md:15`); ractor cast 3/3 (`MEM:34`). | FS:5 "persona-lens shots (ractor)". Salon lane = re-label of existing salon family. |

Lane verdicts: 3 continuation, 2 rename, 0 resurrection, 0 genuinely new.

## C. TOTAL COUNTS
- CONTINUATION: 5 (Hands, Standing self, Harvest, Smell, Coding)
- RESURRECTION: 0 (nothing in FS/LSM points at a dead system; all refs are live organs on disk)
- RENAME: 6 (Director, Driver, Tail, Swarm, Probe, Salon)
- GENUINELY NEW: 1 slot, not a system — codex desktop paste (a seat slot, and it's idle/pending, FS:16)

## D. SHARPEST COLLISIONS (two systems now claiming one lane) 

1. **Salon lane vs three salon organs.** FLEET Salon lane (FS:5) vs `frontier_salon` (host), `salon_openclaw` (host), `lane_salon` (`rows/mag_runs.row.md:34`) — 3 live salon implementations. Merge: FS Salon lane should be the *router/clock*, not a 4th organ — it wires windows onto ONE canonical salon surface (rag: `lane_salon` as the durable lane, `frontier_salon` roundtable as the scheduled form, `salon_openclaw` as the harness shell). Pick lane_salon as the single substrate; the other two become invocation aliases. UNCHECKED: whether all three write/read the same room.jsonl — if not, they're 3 blackboards.

2. **Probe lane vs existing probe batteries.** FS Probe lane (FS:3) vs `seat_dispatch` probes + economist route probes (`ECONOMIST_ROUTE_20260901.md:13-15,154`) + LINEAGE_DIFF 20-probe battery (`LINEAGE_DIFF...md:23`) + OPS_RESEARCH_LOOP dogfood probes (`OPS_RESEARCH_LOOP...md:11 §3`). Four probe families already run. Merge: ONE frozen probe-battery ledger (the LINEAGE_DIFF battery is the canonical frozen unit) as the shared registry; probe *lane* = the down-time scheduler that dispatches batteries off-peak and appends to that ledger. Otherwise probes re-fire anonymously.

3. **Harvest lane vs OPS_RESEARCH_LOOP external-intake reuse + archivist inbox.** FS Harvest lane (FS:1) is the archivist_feed_harvest cron, but OPS_RESEARCH_LOOP ALSO claims "External intake → archivist_feed_harvest cron" (§2) for fleet-ops SOTA. Same cron, two command lanes. Merge: harvest lane adds a named standing gap "fleet-ops SOTA" (`OPS_RESEARCH_LOOP:8`) into the existing v3 follow-kit tier stack instead of a parallel intake — one cron, two named gaps, one triage queue. No second harvester.

4. (watch) **Tail seat vs LSM Tail slot** — cleaner, single source (`LSM` Tail ~70%). Flag but NOT a collision: LSM already fixes it. Closed-loop actuator remains the UNASSIGNED owner (`ECONOMIST_ROUTE...md:147,142` "no closed loop economist→router"; FS night-3 "economist → water_windows gate").

## E. REPEAT-RISK (past failure patterns the new lanes could replay)

1. **Write-ahead-of-reach** — the 13:33Z "salon fired" claim that never spawned lanes; self-check caught it 13:44Z, fired 13:46Z (`MEM:30`). FS Salon/Probe/Smell lanes are described as "to wire" (FS:22 "lanes live" is the seat, lanes themselves are night-2/3 wiring). If wiring posts a status line before the lane spawns, same write-ahead gap. METER: each lane's hello must log a handoff receipt (lane spawned + window clock ticked + first work item), not a status message.

2. **Salons that fired without lanes / with no meter** — gate-runtime meter on lens usage is standing (`MEM:34` "gate-runtime meter on lens usage"), and 72h repetition cap is standing (`MEM:42` digest v1.1). FS Salon lane must inherit BOTH or it re-fires persona shots without a yield meter. METER: per-run lens hit-rate + dedupe vs SALON_RACTOR_SYNTHESIS; no PASS → quarantine (riddler gate, `MEM:35`).

3. **Empty_recovery loops** — better-by-default self-tuning ladder is LAW for every standing system (`MEM:30` "must carry a self-tuning loop... prune/promote at stated thresholds"). OPS_RESEARCH_LOOP has the ladder (`OPS_RESEARCH_LOOP:15-18` demote/promote). Harms: if Probe/Codex/Salon lanes are wired without an evolution ladder, they're incomplete standing systems (defect). METER: each lane files its ladder in its wiring proposal before going live (FS:22 sequences this — enforce the gate).

4. **Refresh staleness** — `rows/mag_runs.row.md:34` lane_salon last = 2026-08-29T2239 (2+ days dead) while the salon organs are labeled "live". RENAMED lane must not inherit a stale-runs corpse. METER: FS Salon lane first action = prepend a fresh heartbeat to lane_salon runs, else it's a renamed corpse.

## F. NET
Fleet is REFINANCING existing organs, not acquiring (consistent with FS:3 doctrine + red line). Risk is not duplicate invention — it is *routing*: four probe families, three salon surfaces, one reused harvest cron. Wire the merges in D as the clock/router over single canonical blackboards, attach the E meters, and FS lands as a router, not a new fleet. UNKNOWN: whether salon organs share one room.jsonl (D1) — required before Salon lane dispatch.

*End — evidence-only, no novel, receipts cited above.*
