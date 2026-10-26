# STEAL — grok_free bones (free surfaces · project handoff · private idea space)

**Stolen:** 2026-08-09 · sources: steal-protocol repos (agentswarm, blackboard-core, flock, leeroo, conductor, ollama-harness, subagent-router, bmas) + local docs/memory.

## Stolen patterns applied to grok_free
1. **Router-as-proxy with surface failover + budget** (subagent-router) → `grok_free.route_surface(goal)` picks cli|com|api deterministically, $0.
2. **Small-model classifier → route** (leeroo orchestrator) → `route_surface` is the deterministic "orchestrator model" that picks the surface before any token is spent.
3. **Priority-order context under token budget** (blackboard-core `to_context_string`) → free calls still token-budgeted + cache-aware (SYSTEM_PROMPT_CACHE).
4. **Blackboard artifact-subscription handoff** (flock scheduler) → `grok_free.handoff()` writes a frozen `queue/handoff/BUILD-grokfree-*.md` + spawns the cheap DeepSeek executor (plan@free-frontier → build@cheap).
5. **BUILD-spec pipeline** (local MAG_BUILD_PIPELINE) → handoff mirrors plan@Grok → build@DeepSeek → audit.
6. **Typed control channel + timeout→autonomous** (agentswarm ControlMsg / operator-input-contracts) → deferred to cadence layer.
7. **Concept-cell / graph memory recall** (ollama-harness ccmem / mycelium) → `save_idea` writes an `idea_graph` open_loop node (recallable topology, not isolated leaf).
8. **Self-referencing prior-block injection** (agentswarm memoryBlock "PRIOR RUNS") → `capture()` auto-injects a "PRIOR GROK-FREE IDEAS" block from `research_lens.retrieve_prior(lens="grok_free")` and folds the answer back (compounding).
9. **Pinned decisions + keyword recall** (blackboard) → reuses `research_lens.retrieve_prior`.
10. **Declarative skill registry + discovery** (conductor skills/) → a grok-free SKILL.md is the future model-native descriptor.
11. **Coordinated scheduling** (conductor workflow/router) → ghost.sense_surfaces + route_surface is the coordinator leaf.
12. **Cadence / scheduled automation** (ollama-harness scheduler / steward.run_job) → a `grok_free_cadence` job is the future scheduled loop.

## Verified live
- `route_surface(goal)` → `surface=cli` (deterministic pick, $0).
- `capture("...")` → ok=True, harness=True, **cost=0.0**, **folded=True** (self-referenced a prior idea + folded answer back to the lens corpus).
- `save_idea(...)` → writes private `memory/ideas/grok_free/*.md` AND an `idea_graph` open_loop node (`n_717f3ba254`).
- `handoff(goal)` → writes frozen `BUILD-grokfree-*.md` + spawns the cheap DeepSeek executor.

## Gaps (deferred, layer on top)
- grok-free SKILL.md + references/ (conductor skills pattern)
- control.jsonl + global kill-switch + timeout→autonomous for the free path
- `steward.run_job("grok_free_cadence")` scheduled loop over the private idea backlog
- free-vs-paid metering ledger (fallback_count) for cost learning
