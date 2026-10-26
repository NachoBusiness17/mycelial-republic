# DELEGATION RESEARCH BRIEF — SMART-DESIGNS / DUMB-EXECUTES + THE SMART GPS (2026-09-29)

External research lane, run 2026-09-29 on the operator's question: why would we have Claude Opus 5.5 build us a prototype, and what are the underlying theories? Full text with all URLs preserved in the session transcript; this file banks the load-bearing findings and the verdict.

## The theory, compressed

1. **Anthropic ships the pattern twice.** Their multi-agent research system: Opus orchestrates, Sonnet subagents execute — +90.2% over single-agent Opus on research breadth, with the economics line "upgrading to Sonnet 4 beat doubling the token budget on Sonnet 3.7" (model quality at decision points beats token volume). Claude Code OpusPlan: Opus for the plan pass, Sonnet for execution — smart-designs/dumb-executes, productized. Caveat: multi-agent fails on most coding work (shared context does not parallelize).
2. **The paper record converges from both directions.** W4S (arXiv:2504.04785): a 7B meta-agent DESIGNS workflows that strong models execute, beating the strongest baseline by up to 24.6% — the planning slot carries the leverage regardless of which side is cheap. SWE-Router (2607.00053): route on the trajectory (what happened), not the prompt (what it looks like). FrugalGPT lineage: cheap-first cascades at up to 98% cost reduction. RRSI (2609.24972) + the harness-effects paper (2609.32459): harness evolution is real but modest and regularization-hungry; optimal harness design varies per model strength and task class.
3. **The single most relevant 2026 result: Scrouting/SuperScout (arXiv:2608.04804).** A 7B scout produces a SANDBOX-VERIFIED handoff (false claims stripped), then a router dispatches to frontier fixers: 159/266 vs 158/266 for the best single model on SWE-bench Pro at ~1/5 cost per solve. And its own ablation is the estate's design constraint: a no-router ablation TIES the routed system — "the handoff rather than the routing decision carries the result."
4. **The economics:** frontier output tokens run ~5x Haiku, ~10x Flash-class, ~100x+ owned-local marginal cost. Where the tiered pattern inverts: shared-context tasks (most coding), weak verification (failed SWE-bench tasks cost MORE than solved: $0.48 vs $0.35, 51 vs 39 calls — cheap-first without hard gates burns money exactly where you hoped to save).

## The practice

- **Nobody serious routes inference through MCP** — routing lives at the OpenAI-compatible gateway tier (LiteLLM dominant self-hosted; Portkey/Helicone hosted; RouteLLM/NotDiamond router-ML; vLLM semantic router as sidecar on agentgateway). k8s inference pools are mature (KServe, LeaderWorkerSet, Gateway API InferencePool, llm-d, KubeAI).
- **The gap is real:** no shipped self-hosted system routes on the buyer's own eval-gated, receipt-backed pass-rates with cost-truth meters. That combination is open.
- **Terminology bonus:** "Jev clones" has a public referent — Jev, TypeSafe AI's System One model (typed values with probabilities, ~200x faster / 400x cheaper than LLMs on typed decisions; LangChain published "Building a Harness with Jev"). The estate's local decision models behind OpenAI-compatible endpoints are a local re-implementation of a pattern the industry just legitimized.

## The ask-shape laws (from Anthropic's own guidance)

Do not over-instruct a frontier model; one-shot multistep is now legitimate with structured context (long inputs first, query last, +30%); "think thoroughly" beats hand-written step plans; tests-first framing; the interview-to-spec-to-fresh-session pattern for big builds. What wastes money: frontier tokens reproducing commodity knowledge, no output contract, plan+build in one context, no pass/fail gate.

## VERDICT (confidence 0.7)

The operator's instinct is right in the large (tiered delegation is the most validated architecture of 2025-2026, and 95%-local is economically correct), wrong in the particular: **do not spend the Opus ask on routing code.** Spend it on the verification/handoff CONTRACT — the capability-ledger schema, the gate definitions, escalation boundaries, and an adversarial critique — then let the mid-tier/local fleet build gps-mcp against LiteLLM/KServe from that spec, reserving future frontier contact for judging decisions on receipts. The frontier's marginal token pays for choosing, refuting, and calibrating. Not typing.

Caveats preserved: Anthropic's 90.2%/15x are self-reported; LiteLLM's 45% is a 25-task vendor benchmark; prices from third-party trackers; "Octomapper/HAL" could not be located (likely conflation with OctoTools, arXiv:2502.11271 — the operator's name for the builder-mapper split maps to the real OctoTools planner/executor/verifier lineage).

Em-dash count: 0.
