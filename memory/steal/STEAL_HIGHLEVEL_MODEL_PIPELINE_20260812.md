# STEAL — Feed high-level models into the research pipeline intelligently + recordably (2026-08-12)

**Problem (operator correction):** high-level frontier seats (OpenAI "fable", Grok, Kimi) were
bypassed or dead-end in the research pipeline — outputs written to artifacts/cost-ledgers that the
autonomous loop did not consume. Only DeepSeek was the pipeline.

**Steal sources (external, via STEAL_PROTOCOL_REPOS_INDEX):**
- **EIT-EAST-Lab/C3** (Transcript Credit Assignment): freeze transcript context + record replay
  state at EVERY decision; persist `role_outputs` mapping (role → text) per trajectory so each
  agent/role's contribution is attributable, then assign per-role credit/influence (LOO baseline).
- **Leeroo-AI/leeroo_orchestrator**: an Orchestrator expert-picker picks WHICH expert model serves a
  query (`get_orchestrator_response(query) → expert_id → get_expert_response`), cost/health-aware.
- **togethercomputer/MoA**: layered proposer→aggregator; the aggregator prompt (getFinalSystemPrompt)
  includes ALL prior model outputs NUMBERED + attributed, and instructs critical evaluation ("some
  may be biased or incorrect") rather than blind merge.

**Self-steal (already owned):** swarm_surface.route_novel (the ONE primitive), steal_pack (files
frontier output into research-pack → skill_ledger/lens/verkle), percolator, research_class, rib_bus.

## Adapted into mag/refine_chain.py (deterministic, architecture-native)
1. **C3 provenance (recordability):** every successful round writes
   `chain["role_outputs"][f"{role}:{seat}"] = {role, seat, model, artifact_hash, artifact_path,
   ts, text[:4000]}` — each high-level seat's contribution is attributable on the chain record,
   enabling future credit/influence.
2. **MoA critical aggregation (intelligence):** the synthesize round's prompt now includes EVERY
   prior seat contribution numbered + model-attributed, with explicit instruction to EVALUATE
   critically (choose strongest, reconcile conflicts, label provenance), not concatenate.
3. (Prior) each seat output routed via swarm_surface.route_novel so it enters the swarm research
   queue + gets recorded/percolated.

## Standing law
- Frontier-seat output must have an explicit content → record → route path (never dead-end artifacts
  or cost-only ledgers).
- Aggregators must see ALL prior contributions WITH provenance and evaluate critically (MoA), not
  merge blindly.
- Record per-seat provenance (C3 role_outputs) so contributions are attributable + creditable.

## Not yet done (rightsized)
- Leeroo expert-picker: a goal→seat router (which high-level model for which research goal,
  cost-aware) reusing grok_rightsize tiers — natural next build.
- C3 credit/influence scoring of which seat's contribution mattered most (needs a critic signal).
