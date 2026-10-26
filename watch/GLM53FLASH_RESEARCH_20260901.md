# GLM-5.3-Flash — Capability + Fleet-Fit Research
Date: 2026-09-01 | Lane: research | Custody: UD-Q4_K_XL quant (~claimed 130GB, 6 parts)

Model IDs confirmed in sources: `zai-org/GLM-5.3-Flash` (aka "ox-alpha") / `glm-5.3-flash` API. 320B total / 18B active MoE, MIT-licensed, 1M ctx. NOTE: many benchmark classifiers in sources are 2026-era (Claude Opus 4.8, GPT-5.6 Terra). Benchmarks largely Z.ai self-reported unless labeled independent.

## Findings (VALID = 2+ independent sources; UNVERIFIED = single/secondary or suspected)

1. CAP | Intelligence index 57 (AA Intelligence Index v4.1.1) — near Claude Opus 4.8 level; independent (Artificial Analysis). ~95% of full GLM-5.3's index (60). SELF-REPORTED vs INDEPENDENT mixed. VALID. https://artificialanalysis.ai/models/glm-5-3-flash

2. CAP | Agentic/coding strength (self-reported Z.ai harnesses): Terminal Bench 2.1 84.3, DeepSWE v1.1 63.4, Toolathlon Verified 78.4, AutomationBench 48.8 — matches/beats Claude Opus 4.8 on several. Geared for long-horizon/tool-use. SELF-REPORTED (DeepSWE community-run partially). VALID(cap orientation)/UNVERIFIED(precise numbers). https://ollama.com/library/glm-5.3-flash

3. CAP | Creative long-form: no dedicated public "flash" creative-writing leaderboard found. Closest evidence is parent GLM-5 series eqbench long-form report (chapter plan-adherence, restrained prose). Flash arch (18B active) noted to favor coherence/utility over lyrical prose. UNVERIFIED (direct creative-writing quality). https://eqbench.com/results/creative-writing-longform/zai-org__GLM-5_longform_report.html

4. CTX+LIMITS | Native 1M-token ctx, 128K output; hybrid sparse+linear attention (KDA+DSA) cuts KV compute ~3-4x. Math/coding/reasoning strong; known weakness: verbose (slower tokens/sec ~41-49/s), and "utility over purple prose" creative ceiling. UNVERIFIED failure-modes-at-depth for creative (no repetition/drift long-form bench). https://docs.z.ai/guides/llm/glm-5.3.md

5. LOCAL | GGUF shipping via unsloth dynamic UD quants confirmed; llama.cpp requires fork/PR branch (mainline support rolling out late Aug 2026); Ollama currently only `:cloud` tag (local pending llama.cpp milestone). Serve `--jinja -c 8192` w/ `-fa on`. VALID. https://unsloth.ai/docs/models/glm-5.3-flash

6. LOCAL | SIZE WATCH: unsloth docs table lists 4-bit = 162-210GB (3-bit 128-150GB). Task states Q4_K_XL ≈130GB/6 parts — under the documented 4-bit floor; 320B×4bit ≈160GB weights alone. Flag: confirm shard byte-sizes before custody; ~130GB more consistent with a 3-bit/UD-IQ3 reading. UNVERIFIED(discrepancy). https://unsloth.ai/docs/models/glm-5.3-flash

7. LOCAL | Quant quality: unsloth UD pipeline calibrated+imatrix; 1-bit UD-IQ1_S ~93GB retains ~71% of acc, 3-bit ~87%. Q4_K_XL expected clearly above that (top-tier). No documented Q4_K_XL-specific failure for this family found. UNVERIFIED (no specific Q4_K_XL UD study). https://huggingface.co/6block/GLM-5.3-Flash-GGUF

8. FLEET | Flash-tier is defensible for gamedesigner/campaign-narration seat: strong instruction-following + long-context economics (1-1/40 cost) favor iterative narration at scale. BUT creative-depth risk: full GLM-5.3 (18B-active sibling family, AA 60 vs 57) is the choice if lyrical/long-form coherence is non-negotiable. UNVERIFIED (no flash-vs-full creative A/B found). https://the-decoder.com/the-chinese-ai-model-glm-5-3-flash-runs-without-nvidia-and-costs-a-fraction-of-what-the-competition-does/

9. QUIRKS | Chat template: thinking ALWAYS forced on (cannot disable); `reasoning_effort` = low/high/max (default max, injects "Reasoning Effort: Max"); MUST pass `clear_thinking=true` for multi-turn chat to avoid stale reasoning-state. VALID. https://huggingface.co/zai-org/GLM-5.3-Flash

10. QUIRKS | Sampling defaults: temperature 1.0 / top_p 0.95; ONLY tune one, not both; coding/agentic alt temp 0.95/top_p 1.0. Serve w/ `--jinja` for official template. VALID. https://docs.z.ai/guides/overview/migrate-to-glm-new

## Fleet recommendation (synthesis)
Use GLM-5.3-Flash (API twin) for tail seats (dedupe/formatting — perfect: high-volume, instruction-following). For gamedesigner seat, flash-tier is acceptable at ~95% of full-model intelligence and 1-1/40 cost, with strong long-context economics for campaign narration; keep full GLM-5.3 as fallback if creative long-form coherence or prose flair is rated a hard requirement. Local Q4_K_XL ~130GB — verify actual file bytes vs unsloth 4-bit floor before trusting the "130GB" figure.
