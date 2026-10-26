# SWEEP: inference-efficiency via x (2026-10-06)

Area: inference-efficiency. Door: X via WebSearch + fxtwitter resolver (JSON, no login), plus a Twitter syndication-timeline harvester discovered this session. Stamp: source-fetched: 2026-10-06. Seat: sweep-inference-efficiency-x.

## Doors: what worked, what degraded (honest)

- WebSearch `site:x.com` queries mostly returned backend 429/1302 rate-limit errors or domain-root x.com links with no status ID (same failure mode yesterday's sweep recorded, `watch/inbox/frontier_olm_2026-10-05/sweep/inference-efficiency-x.md:8`). No banked item rests on a search snippet; every banked item below was resolved through the fxtwitter door and read end to end from its JSON.
- New door that worked: `https://syndication.twitter.com/srv/timeline-profile/screen-name/<handle>` (the public website-embed timeline, no login) returns Next.js HTML embedding recent tweets with id, created_at, and text. Raw dumps kept at `watch/inbox/frontier_olm_2026-10-06/sweep/_raw/bing/synd_*.html`; parser `parse_synd.py` in the same dir. This is how the candidate pool was built after WebSearch degraded.
- Syndication coverage is uneven: fresh timelines for @UnslothAI, @ollama, @togethercompute, @typesafeai, @Alibaba_Qwen; stale 2025-era embed data for @danielhanchen, @ggerganov, @vllm_project, @CloudflareDev, @rohanpaul_ai; 2KB error stubs for @kaboroevich, @RasvtNl, @reflectionai_labs, @main_horse. Stale accounts were triaged from what the embed carried; none of their stale rows is banked.
- nitter mirrors (poast, privacyredirect, tiekoetter, lightbrd, space, xcancel) all JS-challenge-walled: dead. Bing/DDG HTML search: Bing obfuscates links, DDG returns an anti-bot stub: dead.
- One fetch round of five fxtwitter calls 404'd because my loop dropped the `status` path segment (my bug, not the door's); corrected and refetched all ten posts cleanly, raw JSONs at `_raw/bing/fx_*_status_*.json`.

## Pass 1: candidate pool

Triaged 60+ in-window rows across eight account timelines (window 2026-09-06..2026-10-06, plus two decisive 09-02/09-04 posts): the Ollama decision-model cluster (Nimble, Tev1 0.8b/4b, /v1/systemone, Clef/Clef Flash, Beam, mischarge refund), the Unsloth cluster (GLM-5.3-Flash 3.3x, Qwen3.8-Flash MTP 1.7x, Laya 4GB, EmbeddingGemma 2, Qwen-Image-2.1 VRAM cuts, Docker/Colab lanes), the TypeSafe cluster (Jev reranker numbers, jev-permission-gate, calibrated confidence, $0.02/sweep risk agent, n8n, Claude Code mod), Together (Link auto-router, OpenRouter share, Qwen3.8-Flash 40% off, Jev-for-$17), Qwen (Qwen3.8-27B Nebius, Qwen-Image-2.1, Qwen-Audio-3.1 price cuts), plus stale embeds from the serving-side accounts. At least 30 distinct in-window candidates were considered; 11 were deep-read; 8 are banked.

## Pass 2: deep reads (11 posts fetched and read end to end via fxtwitter this session)

1. @UnslothAI 2095852388888522890 (2026-09-04, 233,348 views): GLM-5.3-Flash 3.3x faster locally, 1.6-3.4x via optimized decoding + bonus MTP, 3-bit on 128GB, guide unsloth.ai/docs/models/glm-5.3-flash#faster-inference-and-mtp-support.
2. @togethercompute 2107139875522879939 (2026-10-05): Together Link, Auto router picks model per task with spend tracking in a coding harness.
3. @MadisonJRickert 2106183706989953339 (2026-10-03): Jev-based classifier for Claude Code auto mode, 2x faster permission checks, repo github.com/madisonrickert/jev-permission-gate.
4. @togethercompute 2104965564368359681 (2026-09-29): OpenRouter token share across top open coding models: GLM 5.3 Flash 29.2%, DeepSeek V4.1 Flash 25.6%, Kimi K3 18.9%.
5. @johncrown 2105383804936626365 (2026-09-30): Jev reranker at 75% of previous cost, +30.64% matches per 200 candidates on real recruiter searches.
6. @ollama 2107186849370247235 (2026-10-05, 1,451,133 views): Beam by Reflection AI, 501B total / 23B active agentic open model, full weights this month.
7. @UnslothAI 2107505698531868941 (2026-10-06, today): EmbeddingGemma 2, 740M params, runs on 0.5GB RAM, text+vision+audio, GGUFs up.
8. @UnslothAI 2104592692072304916 (2026-09-28): Laya Decision models on 4GB RAM via Unsloth Desktop, Jev-compatible API, guide unsloth.ai/docs/models/decision-laya.
9. @ollama 2105152056382345544 (2026-09-30, 658,694 views): Jev-like decision models local (Nimble; Tev1 4b/0.8b per sibling tweets), local /v1/systemone API.
10. @ollama 2106186667543666841 (2026-10-03): Cloudflare Clef (27B) / Clef Flash (9B) decision models pullable from Ollama.
11. @edwardirby 2105695667486355848 (2026-10-01): risk agent without a frontier model at $0.02/sweep (youdotcom search + Jev typed judgments + Qwen synthesis + MCP).

## Answers to the five research questions (X-door slice)

- RQ1 (32 sweep items to register rows): the X door's contribution to the register is the external-confirmation set for the day-5 "decision models create a rung UNDER gemma:2b" find: within days of the estate's internal find, Ollama shipped local Jev-compatible decision models (09-30), Cloudflare's Clef landed pullable (10-03), and Unsloth packaged Laya at a 4GB RAM floor (09-28). The frontier independently minted the rung; those are register-row-grade receipts, already partially banked by yesterday's sibling doors (see dedup below).
- RQ2 (EMPTY_REASONING terminal classifier wiring): jev-permission-gate is the frontier's measured proof of the estate's own law (laws.md:91, EMPTY_REASONING terminal, classify once and never refire): a decision-model classifier wired into Claude Code's permission gate reads 2x faster than the LLM round-trip it replaces. The pattern transfers to the six unwired surfaces: classify-and-terminal at the lane entry, no prose generation, no reasoning-token contamination to re-measure.
- RQ3 (width 12-16 Task-agent rung): nothing on X measures agent-harness width curves or rolling account throughput; the closest public object is Together Link's per-task auto-routing (spend tracking included), which is per-task model choice, not per-window width. This rung remains internally measurable only; no public prior art found.
- RQ4 (route once per task, pin the model): two independent frontier confirmations that per-task routing is the productized shape: Together Link's Auto router ("low-cost models for quick fixes, more capable models for harder tasks") and OpenRouter's token-share data showing flash-class models (GLM 5.3 Flash #1 at 29.2%) dominating coding-agent traffic. Market structure matches the driving ladder's flash-first default; the pin survives as long as the task class is stable, which is the question-class law's job.
- RQ5 (in-session switch machinery): the X evidence is indirect but aligned: the frontier routes between tasks with cheap decision calls (Jev/Nimble/Clef for routing as a decision), not mid-generation model switches; nobody productizes in-session switching as a feature. No X source prices a forced in-session switch, so retire-or-keep stays an internal measurement.

## Dedup / overlap ledger (greps run this session against catalog/catalog.jsonl and memory/)

- GLM-5.3-Flash: 787 catalog rows (provider intake cards, watch/INTAKE_GLM53_HIGH_CONCURRENCY_20260904.md et al.), but the unsloth.ai/docs/models/glm-5.3-flash speed guide: 0 hits; yesterday's x.md:40 records siblings mention unsloth only re weight quants. The 3.3x local-speed artifact is NEW.
- Together Link / Auto router: 0 catalog, 0 memory. NEW.
- jev-permission-gate: 0 catalog, 0 memory. NEW. (Jev concept itself: 145 catalog rows; the estate calls api.typesafe.ai/v1/systemone per memory/research_packs/THE50_W3_T11_TYPED_DECISION_ORACLES.md.)
- OpenRouter flash-share stat: 0 memory hits (215 catalog OpenRouter rows are provider surfaces). NEW as a data point.
- Jev reranker 30.64%/75%: the number has no prior hit in memory (the bare "30.64" string matches 247 catalog rows of unrelated numeric data). NEW measurement on a known model.
- Beam/Reflection AI: not in catalog (91 "reflection" rows are WoW game code). NEW.
- EmbeddingGemma: 0 catalog rows. NEW.
- Laya: 28 catalog rows; yesterday's open-local-language-models-arxiv.md:19 banked the model (421M, 32.8ms p50). The 4GB Unsloth packaging is the new increment; banked low with overlap stated.
- Sibling-banked, NOT re-banked here: Ollama local decision models / systemone latency stack (inference-efficiency-hn.md:78-91, "Ollaya banked 09-30"), Clef/Clef-flash composition + BFCL numbers (finetuning-adaptation-hn.md:133-138), Clef license page already fetched as intake (_clef.html, catalog afca528a4b66; burns.md lists the license-page fetch OWED as satisfiable from it). The two Ollama X posts (items 9-10 above) and the Clef X post are therefore recorded as sibling-confirmed primary sources, not as new bank items.
- Estate-internal prior: Nimble held as sovereignty front-runner since 2026-09-19 (memory/continuity/seat_memory_20260927/jev-salon2-fold-20260919.md); calibrated confidence already formalized (memory/runs/jev_salon2/gate_builder.md, "confidence bands declared in syntax, judged at runtime"), so @typesafeai 2106197282274324846 is confirmation, not a bank item.

## Banked items (strongest first; verbatim quotes from the fxtwitter JSON fetched this session)

1. GLM-5.3-Flash 3.3x faster locally (UnslothAI, 2026-09-04). The funded seat model's own local speed path: optimized decoding + MTP in llama.cpp, flags at the guide anchor. Steals directly into the local-first DNA: same model, 1.6-3.4x cheaper locally.
2. jev-permission-gate (MadisonJRickert, 2026-10-03). Terminal decision-model classifier inside a coding-agent permission gate, 2x faster checks: the EMPTY_REASONING law's shape, measured by outsiders, wireable into the six unwired surfaces.
3. Together Link auto-router (togethercompute, 2026-10-05). Per-task model pick with spend tracking in a coding harness: route-once-per-task productized; the pattern the driving ladder's tier logic should be compared against.
4. OpenRouter flash dominance (togethercompute, 2026-09-29). GLM 5.3 Flash 29.2% / DeepSeek V4.1 Flash 25.6% / Kimi K3 18.9% token share: market-scale validation that flash-class is the coding-agent workhorse tier.
5. Jev reranker production numbers (johncrown, 2026-09-30). 75% of previous cost, +30.64% matches per 200 candidates on real recruiter traffic: a before/after template for wiring decision models into estate triage lanes.
6. Beam, 501B/23B active (ollama RT of reflectionai, 2026-10-05). The specialist tier's efficiency frontier claim ("frontier reasoning efficiency" at 4.6% active); weights due this month; watch for the estate's specialist seat.
7. EmbeddingGemma 2 (UnslothAI, 2026-10-06). 740M-param multimodal embeddings on 0.5GB RAM: sub-GB embedding lane for corpus semantic surfaces.
8. Laya on 4GB RAM (UnslothAI, 2026-09-28). The decision-model rung packaged below janitor hardware floor; candidate host for local EMPTY_REASONING-style terminal classifiers.

## Falsifier / caveat

Item 1 postdates the strict 30-day window start by two days (2026-09-04); kept because it is the estate's own seat model and unbanked anywhere in catalog or memory. Every quote above is verbatim from fxtwitter JSON fetched this session; raw files at `_raw/bing/fx_*_status_*.json`. No snippet-only claims are banked.
