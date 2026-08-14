# STEAL — Grok Refactor: competitive memory/KG landscape for next version + aimbotting
**Date:** 2026-08-10 · **Researcher:** ghost (ai_landscape)
**Ask:** "is anyone else doing this? what can we steal in a grok refactor for our next version and
future aimbotting."

## Who else is doing this (competitive landscape)
The MEMORY/KNOWLEDGE-GRAPH half is CROWDED + well-funded. We are NOT alone there — steal their best.
The DENIABLE/STEGANOGRAPHIC/IMAGE/ARCHETYPE half is OUR MOAT — nobody does it.

### 1. Microsoft GraphRAG (the strongest direct steal)
- Extracts entities/relations/claims from text -> knowledge graph.
- **Hierarchical community clustering (Leiden)** -> **community summaries**.
- Query: **Global Search** (holistic via community summaries) · **Local Search** (fan-out from an
  entity to neighbors) · **DRIFT** (local + community context) · Basic (vector).
- This is EXACTLY "accurate knowledge graph so things are just known." Our `knowledge_graph` is
  source-backed + deterministic (better accuracy) but only does keyword match. STEAL the
  community-summary + global/local/DRIFT query modes.

### 2. Mem0 (agent memory, compression)
- Persistent cross-session/agent memory.
- **Memory Compression Engine**: single-pass hierarchical distillation -> compact memories -> cuts
  redundant tokens/latency.
- **Multi-signal retrieval** (recency + relevance + importance), not just keyword.
- STEAL: the compression engine + multi-signal retrieval into `knowledge_graph.known()` +
  `context_compression`.

### 3. Letta (stateful agents, dreaming)
- Stateful agents with **"memory & dreaming"**: OFFLINE consolidation of memories while idle.
- Learned **skills** (reusable workflows, learned or pre-made), subagents, schedules.
- STEAL: the **dreaming cadence** — offline recluster/summarize/prune of the knowledge graph while
  the operator is AFK. THIS is the aimbotting enabler: autonomous graph maintenance that makes
  things more accurately "just known" with zero operator effort.

### Others in the space (lower priority)
Neo4j/GraphRAG variants, Cognee, Zep, MemGPT/LangMem, Chroma/vector RAG, agent-swarm frameworks
(AutoGen, CrewAI, LangGraph, MetaGPT). Our stateless-swarm-on-kind is already differentiated.

## The grok refactor steal list (next version + aimbotting)
1. **Community summaries (GraphRAG)** — cluster `knowledge_graph` (deterministic, on module->invariant
   + landscape edges), emit a summary per community. Add **Global** (holistic) vs **Local** (fan-out)
   query modes to `known()`. This is the "spookily known" upgrade.
2. **Multi-signal retrieval (Mem0)** — `known()` scores by recency + relevance + importance, not
   just keyword overlap.
3. **Memory Compression Engine (Mem0)** — fold + distill redundant context into compact memories;
   reuse `context_compression` + `skill_drop.right_size`.
4. **Dreaming cadence (Letta)** — AFK "dream" pass over the graph: recluster, summarize communities,
   prune dupes, fold discoveries. Runs when the operator is idle (afk_cadence / ghost cycle). This is
   the aimbotting engine: the graph self-maintains toward accuracy.
5. **Learned skills (Letta)** — auto-catalog reusable workflows from case-law into `skill_ledger`
   (already partly done via fold).

## Keep the moat (do NOT throw away)
The deniable/steganographic/archetype layer (`whisper_image`, `archetype_image`, `ghost_whisper`,
`memlang` tokens) is what no one else has. The grok refactor ADDS the crowded half (KG/memory
patterns) while KEEPING the unique half (deniable image-whisper + archetype artifacts).

## Folds
Filed to `memory/steal/`. Register in `ai_landscape` (families: graphrag, mem0, letta) so ghost
recognizes the next memory/KG announcement and maps it to our modules + delta. Repo memory:
`/memories/repo/grok-refactor-steal.md`.
