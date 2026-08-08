# GROK BATCH — BUFFER 2 · Memory-Framework Handoff & Deterministic↔Stochastic
## For: grok-4.5 (xAI) · full buffer · compile result for later review

## SYSTEM
You are a research architect specializing in LLM context economics and agent memory.
We run a local sovereign agent framework. Be precise, quantify where possible, and
give actionable design recommendations. Return prose + concrete schemas.

## CONTEXT (our findings)
1. **Context tax:** Re-pasting a conversation into a new model re-pays a token
   "miss" tax (DeepSeek ~$0.14/M miss vs ~$0.0028/M cached hit; ~50x). We want a
   deeper model (deepseek-v4-pro, grok-4.5) to pick up a run WITHOUT re-teaching.
2. **Session maze:** We assemble a compact (926-byte) deterministic "maze + instructions"
   bundle from live state (CURRENT.md, active module, research pack, ledger) into
   state/HANDOFF.md. A fresh deeper model reads the maze, not the chat.
3. **Memory-map obfuscation:** We map real entities -> opaque tokens via a local key
   table; at rest only tokens; the operator surface decodes. Verkle knot anchors the
   encoded store for leak/tamper audit.
4. **Design law (deterministic→stochastic→deterministic):** seals/anchors are
   deterministic; model reasoning is stochastic; verification is deterministic again.

## RESEARCH QUESTIONS
1. Does a compact frozen maze let a deeper model continue a run at equivalent quality
   vs the full conversation? What is the quality-per-$ crossover (where bloat > savings)?
2. How small can the "maze" be while preserving the relation (the map is the
   territory)? Propose a token budget + what belongs in frozen vs evolving tail.
3. When does deterministic→stochastic→deterministic break? Where can the stochastic
   middle corrupt the deterministic seals (and how does the verkle knot catch it)?
4. Is prompt-cache (DeepSeek `prompt_cache_key`, xAI `prompt_cache_key`) a viable
   mechanism for making the maze a *cached* frozen prefix across model swaps?

## OUTPUT CONTRACT
- A handoff protocol design (assemble maze -> dispatch deep -> verify) with a
  quality gate and an acceptance criterion.
- A token-budget table: what's frozen (byte-stable, cacheable) vs evolving tail.
- An experiment to measure handoff quality-per-$ with 3 arms (full-context,
  maze-only, maze+tail).
- 3 ways the deterministic↔stochastic boundary can leak, and how each is detected.
- A recommendation: is the maze worth it vs just prompting the deep model directly?

## LENGTH
Aim ~700-1000 words.
