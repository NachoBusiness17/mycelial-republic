# SOCRATIC RELAY — chained cross-lineage salon (cage-native)

## What this is
The operator's manual method — pasting answers between Perplexity/DeepSeek/GPT/Grok —
automated. Difference from the RIB salon (parallel lanes): **relay lanes see prior lanes'
answers and must challenge or build on them.** Consensus is not the goal; surviving
cross-examination is.

## Lineage pool ($0 lanes, conservation-safe)
deepseek/deepseek-v4-flash · groq/openai/gpt-oss-120b · cerebras/gpt-oss-120b ·
nvidia/deepseek-ai/deepseek-v4-flash-0731 (+ z.ai / openrouter-free / ollama-local when needed)

## Phase protocol
- **A (ground):** answers the question cold. No priors.
- **B (build/attack):** reads A. Must name at least one thing A got wrong or missed, then answer.
- **C (converge/diverge):** reads A+B. Names where they agree for the WRONG reason, then answers.
- **D (challenger):** reads A+B+C. Steelmans the opposite of the emerging consensus. No new answer required — a kill shot is a valid output.
- **Synthesis:** cage (Sancho) writes verdict: what survived, what died, one concrete next action. Posted to /room with status=verified only if receipts check.

## Rules
- Each lane output ≤300 words, file at /board/socratic_relay_<topic>_<lane>.md
- Claims need receipts (file path, command, or "reasoned" tag). No vibe.
- A roast is content, not authorization (riddler law).
- Lane failure = skip lane, note the gap. Two strikes on a lane = drop it.

## Demo question (2026-08-31)
> The self-steal control surface (effect_broker, policy_engine, switchboard_v2,
> harness, swarm_cycle_v2, ask_router_v2 — 6 modules in /patches, host-deploy pending)
> is about to be deployed to the host venv. **What is the single most likely failure
> mode at deploy time, and which ONE test catches it earliest?**
