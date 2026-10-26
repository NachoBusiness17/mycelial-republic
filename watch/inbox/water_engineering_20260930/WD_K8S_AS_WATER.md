# WD - K8S AS WATER (ractor pass, lane 4/6, 2026-09-30)

## Archaeology
Original drive: operator quotes in `memory/living_map.json` ("communicate... through the shared ghost whisper tools via the kubernetes"). `mag/rib_k8s.py` (2026-08-10): "rib files as code instructions for our k8s... act smart for free" - invariants as desired-state policy. Nacho handoff `handoff/game_rib_coding_instructions.md`: "BUILD: emulator (MaNGOS/TrinityCore lineage) on k8s; MACHINE: k3s build + k8s deploy." `DELEGATION_RESEARCH_20260929.md`: k8s inference pools mature (KServe, LeaderWorkerSet, Gateway API InferencePool, llm-d, KubeAI). `watch/inbox/K8S3D_RACK_FIND_20260911.md`: webernetes - real open-source k8s simulator; "may reveal state, may not become authority."

## The Hydraulic lens
Pod = node (elev = PriorityClass, volume = pending requests); quota/limit = pipe cap; scheduler = the deterministic gravity tick; load shedding = sill junction (below threshold spills to waste = eviction); exclusive placement = xor; autoscaler burst-then-drain = siphon (primes at crest, runs until intake breaks); escalation/retry = boil (ignores pipes, condenses at highest cold node = top tier).

## The Operator lens
AI-as-operator no longer means an LLM inside reconciliation (nobody routes inference through MCP; rib_k8s proved invariants-as-policy at $0). It means gps_mcp's shape: router schedules, the ledger (G = 1 - delivered/claimed) is the pressure gauge; the AI only sets elevations, sills, and crests - physics dispatches.

## The Skeptic lens
It died of no consumer: kind cluster = museum, zero ollama refs, corpse = unstaffed orchestrator, Metal breaks CUDA-shaped k8s. Today: a real workload (gps_mcp routing, game platform) and a free simulator exist.

## Verdict
v0 = water_graph as a k8s scheduler simulator: feed webernetes metrics (or gps_mcp JSONL receipts) into a WaterGraph spec, tick, assert shed/starvation against tests/test_water_graph_campaign.py. $0, stdlib, no cluster.
