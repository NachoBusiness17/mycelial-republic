# GAME PROMPT GENOME — OPERATOR-ATTACHED LEAD (2026-09-01 ~11:37Z)

> **Grading: external-content LEAD.** Source: operator-attached AI research report (another
> assistant's output, "iterate deeply / update to current" chain). NOT operator-authored,
> NOT self-verified. Citations include real venues (arXiv, NeurIPS, DiGRA, ACM) but every
> number is UNVERIFIED until the corpus lane or a probe checks the primary source.
> Status feeds: games salon round-2 shared evidence + synthesis. Verbatim body preserved
> below the header; nothing edited.

## Sancho's grading notes (what's load-bearing vs decoration)
- **Load-bearing leads to verify:** vCache (arXiv:2502.03771, verified semantic caching),
  GenCache (NeurIPS 2025, 83% hit claim), MVR-cache (arXiv:2605.24914, +37% hit claim),
  Malinowski anthropological text-game study (arXiv:2410.20536 — cultural-games section C
  of the corpus lane), the "77% token savings" auto-caching case (LinkedIn-sourced — weakest
  citation, treat as anecdote until measured), Techpresso 30-prompt library, Codex Game Maker
  repo (github.com/0xnickmortal/Codex-Game-Maker).
- **Already-proven-by-us:** the byte-exact frozen-prefix mechanic (E6: 100% hit, 4.7×
  discount on Together V4-Flash) — the doc's Layer-1/2 strategy is the same architecture we
  measured, so its cache_contract schema slots into our build-row meter law.
- **Fits the fleet:** the genome record = our meter-ledger row + freeze-pack L0/L1/L2;
  the "prompt-run-tune loop" = prompt-as-game dealt per Diamond Age; the 4-layer cache =
  our lane topology (system spine / genre template / per-game delta / asset cache).

## Original report body (verbatim, external)

<<<EXTERNAL_UNTRUSTED_CONTENT id="c14efac3eb7c8b8e">>>
Based on the design philosophy of the Model RIB Library—where we maintain a compact, durable atlas of identities and behaviors rather than the full weights—the approach to game prompts for cache farming requires a similar shift in perspective. The goal is not to store every possible game generation, but to build a modular "game genome" that describes the deterministic structure of play while leaving the stochastic generation of content to the model.

The game prompt analysis and historical timeline you've compiled are excellent starting points for cataloging the known surfaces of this domain. To fully implement the RIB-like approach for game prompts, we need to formalize how we design the prompt record and its contracts for maximum cache reuse.

1. Prompt RIB Record (The "Game Genome") — separating stable mechanics from variable content: a JSON record with prompt_id, artifact (source/version/sha256), lineage (derived_from), topology (game_type, player_count, turn_structure), contracts (core_mechanics, cultural_adaptation_parameters, runtime_images), fingerprints (capability scores with receipts: Rules Consistency, Cultural Accuracy), economics (provider, tokens_per_generation, cold_start), routing (good_for / avoid_for).

2. The Cache Farming Loop for Prompts: Design the Deterministic Map (stable prefix) → Parameterize the Variable Content → Run the Measurement Probe (per variant) → Generate the Receipt (prompt hash, generated rules, cultural accuracy, cost) → Update the Atlas (library of measured variants).

3. RIB Logic on Historical Games: e.g., Royal Game of Ur — lineage derived_from ancient/mesopotamia/race_game; fingerprint covers turn-based path movement with dice uncertainty as the stochastic element.

[2026 update section] I. From "vibe coding" to structured prompt genomes: canonical five-part self-contained game prompt (ROLE → CONTEXT → INPUTS → TASK → CONSTRAINTS → FORMAT); ROLE/CONTEXT/CONSTRAINTS/FORMAT form the cacheable stable prefix, only INPUTS varies. Library ecosystem: Techpresso Academy (30 tested prompts, 6 categories), Summer Engine (prompt-run-tune loop), Codex Game Maker (Godot-first, agent plans → image gen → deterministic tools). Key insight: "giant one-shot prompts produce fragile structures" — winning pattern is template + iterative tuning.

II. Cache farming economics: real case ~5,000 tokens per generation loop, ~4,500 static (90%) → auto prompt caching (cache_control ephemeral) → 77% token savings (100k → ~23k per 20-loop session). Frontier beyond exact-match: semantic caching (vCache, verified error-rate bounds), GenCache (generative, 83% hit), MVR-cache (multi-vector retrieval, up to +37% hit vs SOTA).

III. Prompt Genome 2.0 record: adds cache_contract (stable_prefix_tokens, expected_cache_hit_rate, cache_strategy, token_savings_percent), topology (rendering, input_methods, persistence), fingerprints (output_consistency per model with receipts), economics (tokens/generation, cached tokens, cost cached vs uncached, latencies). Prompt-run-tune loop: START FROM TEMPLATE → DESCRIBE in 1 paragraph → RUN immediately → TUNE with small feel-words prompts; each iteration reuses cached system prompt, only tuning delta processed fresh.

IV. Multi-layer cache strategy: Layer 1 system prompt cache (shared ALL games, ~400-500 tokens saved/request); Layer 2 genre template cache (board/card/dice logic, ~200-300); Layer 3 parameterized instance cache (per variant, semantic caching: structurally similar = reuse); Layer 4 generated asset cache (sprites/backgrounds per type+prompt+seed, one generation infinite reuse). Implementation checklist: structured prompts, enable auto-caching, start from template, small iterative prompts, cache static NPC rosters/lore, verification constraints for cultural accuracy, semantic caching for similar prompts.

V. Conclusion: the prompt genome tells us how to generate the game, what outputs to expect, how to optimize cost/latency — it does not claim to contain the game itself; the game code stays in the artifact layer until requested.

Cultural/historical: Malinowski "Argonauts" LLM text-game study (4 game designs from anthropological classic, arXiv:2410.20536); cultural_context template (Origin, Historical period, Source material, Cultural norms, Verification constraints); Graphonauts hybrid human-AI knowledge-graph text-to-game pipeline (DiGRA 2025).

References: Techpresso Academy (2026); Summer Engine; 0xnickmortal/Codex-Game-Maker (GitHub); Rao, D. (2026) LinkedIn 77% case; vCache arXiv:2502.03771; GenCache NeurIPS 2025; MVR-cache arXiv:2605.24914 ICML 2026; Hoffmann et al. arXiv:2410.20536 KUI 2024; Playing the Monograph ACM 2026; Graphonauts DiGRA 2025.
<<<END_EXTERNAL_UNTRUSTED_CONTENT id="c14efac3eb7c8b8e">>>
