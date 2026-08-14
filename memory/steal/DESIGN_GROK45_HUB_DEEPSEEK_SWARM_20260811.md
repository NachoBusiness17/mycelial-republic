# DESIGN — CENTRALIZED GROK-4.5 POST → DEEPSEEK SWARMS → RIGHTSIZED FRONTIER QUERYING (2026-08-11)

Operator's architecture (canonical): "consult grok on the plan -> create frontier 4.5 agents as a
centralized swarm post to create the groupings -> they interact with those swarms using deepseek ->
use that system to rightsize our asks -> frontier-level querying at a fraction of the cost -> all recorded."

## The model (5 steps)
1. BRAIN-PLAN: consult grok 4.5 on the plan/approach for the ask.
2. HUB-GROUP: a small set of grok-4.5 agents act as a CENTRALIZED SWARM POST that creates the
   GROUPINGS (distill + route incoming asks into groups). grok 4.5 only ever groups + steers.
3. DELEGATE: the grok hub dispatches the groups to DEEPSEEK swarms, which interact/execute the volume.
4. RIGHTSIZE: every ask rightsized -> grok 4.5 ONLY for the grouping/steering step, deepseek for bulk.
   Net: frontier-level querying at a fraction of the cost.
5. RECORD: every call logged (transparent ledger + verkle knots) — measured, auditable, honest.

## Mapping to existing pieces
- grok 4.5 brain/plan: mag.grok_mirror.capture_plan (frontier compacts -> plan), grok_rightsize tier=orchestrate.
- Hub/grouping (grok 4.5): NEW — a router/reconciler that groups incoming asks (create groupings).
  Budget-gated via mag.grok_frontier_loop (rightsized to ~92% premium; resets 8/15; other grok 8/13 02:52Z).
- deepseek swarm: mag.cheap_swarm (expand+execute), mag.stateless_research, mag.flock_job, deepseek-v4-flash.
- Rightsize: mag.grok_rightsize.budget_for/classify_task + ghost_grok_task cost-gate (cheap first).
- Record: transparent usage ledger (aos_grok pattern: memory/embassy/AOS/grok_usage.jsonl) + verkle knots.

## Why it pays
- Cost: frontier quality without paying frontier price on volume (grok 4.5 only groups; deepseek executes).
- Quality: the grouping/hub preserves frontier-level routing/steering of the whole swarm.
- Honesty: full recording means every "frontier-level" result is traceable to its actual model + cost.
  grok_captured flag (grok_mirror pattern): never claim frontier output that didn't arrive.

## Build path (next session)
1. GROK-HUB: a grouping router — batch incoming asks, ask grok 4.5 to create groupings (one orchestrate
   call), then dispatch each group to the deepseek swarm. Record grouping + dispatch in the ledger.
2. Wire: grok_frontier_loop (budget gate) -> hub-group -> cheap_swarm/stateless_research dispatch -> fold.
3. Record: every grok 4.5 call + every deepseek dispatch in a transparent ledger + verkle knot.
4. Rightsize feedback: learn from outcomes (capture-rate, group quality) to tighten grok-vs-deepseek split.

## Memory
- /memories/repo/grok-central-hub-deepseek-swarm-design-20260811.md
- Built this session: mag/grok_frontier_loop.py (budget-gated frontier-steal loop).
