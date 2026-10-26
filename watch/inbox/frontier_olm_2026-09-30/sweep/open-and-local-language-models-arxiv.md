# frontier sweep: open and local language models via arxiv

source-fetched: 2026-09-30
Area: open-and-local-language-models via arxiv. Seat: sweep gopher, Mag Resource Harness.
Feeds: the driving-ladder funded set (memory/rib/RIB_DRIVING_LADDER_20260928.md:7-23), the free-lane sensing law (memory/rib/RIB_FREE_USAGE_POLICY_20260823.md:3-5, cited at watch/inbox/frontier_olm_2026-09-30/lens/laws.md:23), the free-resource-landscape burn lane state (watch/inbox/frontier_olm_2026-09-30/lens/burns.md:57-59), and the local janitor tier (gemma:2b, gemma4) in the queue lanes.

## Doors used and degradations (honest ledger)

- Door 1, arXiv export API: 4 WebFetch queries, all HTTP 200, Atom XML parsed. Queries: all:"small language model" (25 entries), all:"open-weight" (25), all:"distillation"+all:"language model" (20), ti:"Gemma"+OR+ti:"Qwen"+OR+ti:"Muse Glimmer" (20). All sorted submittedDate descending. Recipe per watch/inbox/frontier_olm_2026-09-30/lens/doors.md:14-18 (door re-verified live by the lens seat 09-30; my queries confirm with entries published 2026-09-29).
- Door 2, HN Algolia: 6 queries, all JSON 200. Relevance search "local llm" (nbHits 540 exact-phrase, 2916 unquoted, reproducing doors.md:29), Clippy lookup, "Gemma" + created_at_i>1785600000, "Muse Glimmer" (17 hits), search_by_date "open weights" (20), "GLM" (12).
- Door 3, direct pages: featherless.ai homepage, ollama.com/blog/muse-glimmer, felixrieseberg.github.io/clippy, sota.borgcloud.ai, plus 2 arXiv full-text HTML reads (2609.31540v1, 2609.37902v1). All answered.
- WebSearch ran twice: once for open-weight small-model releases (returned Muse Glimmer, IFM K2 Horizon 0.9B/3.7B/7B, PrismML, Gemma 3 270M with NO fetchable links), once for the Featherless counter gap (returned nothing relevant). The two unverifiable leads stayed unbanked; Muse Glimmer was independently verified through HN Algolia and the Ollama blog fetch.
- No door 403'd or degraded this ask. The reddit door was not attempted: it is closed with root cause verified at watch/inbox/frontier_olm_2026-09-30/lens/doors.md:31-45 (login/rate-limit wall, reason=lor2), and mirrors are the recorded route-around.

## Pass 1, broad sweep

Pool: 110 arXiv entries across the 4 API queries (all 2609.x = September 2026 except 12 July/August Qwen-Audio entries, excluded from the window), plus 66 HN story hits, plus 14 SoTA Feed September rows, plus 4 WebSearch leads. In-window candidates (2026-08-31..2026-09-30) exceed 100; 35 adjudicated explicitly below (id | date | verdict):

1. 2609.31540 | 09-25 | DEEP: checkability boundary for local LLM automation, the sensing/verification instrument
2. 2609.37902 | 09-29 | DEEP: market-aware routing for open-weight inference, the lane-churn instrument
3. 2609.36860 | 09-29 | DEEP: IronLLM-0.6B edge-native model, janitor-slot candidate
4. 2609.32642 | 09-26 | DEEP: local SLMs consult cloud LLMs task-privately, local-first protocol
5. 2609.35833 | 09-24 | DEEP(abs): neurosymbolic routing, deterministic-first on edge
6. 2609.30716 | 09-25 | DEEP(abs): behavioral eval of Gemma 4, our own janitor family
7. 2609.27581 | 09-23 | DEEP(abs): step-law recalibration below 59M params, janitor sizing
8. sota.borgcloud.ai | 09-21 | BANK: release tracker, answers the since-09-28 question
9. Muse Glimmer | 08-10 | BANK: 30B Apache-2.0 agent model, local slot above janitor
10. Clippy | 2025-05-06 | BANK: the RQ3 top hit, verified live with artifact quotes
11. 2609.33927 | 09-27 | hold: Phi-2 QLoRA PEFT chatbot tuning, we already tune locally
12. 2609.31291 | 09-25 | hold: output-head softmax reparameterization, sibling quantization area
13. 2609.30836 | 09-25 | hold: PTC-Decoder training-free SLM framework for offline edge
14. 2609.30578 | 09-24 | hold: RL of communication in a mesh of SLMs, lane-comms adjacent
15. 2609.35875 | 09-26 | hold: multi-agent debate in SLMs, hypothesis rejected on every axis
16. 2609.34292 | 09-28 | hold: pre-registered negative result, SLM-scale compression
17. 2609.37891 | 09-29 | hold: SYNTH fully synthetic single-stage recipe, 58,698 Wikipedia articles
18. 2609.38025 | 09-29 | hold: Dr. OPD on-policy distillation
19. 2609.37044 | 09-29 | hold: think-mode advantage via on-policy distillation
20. 2609.36742 | 09-29 | hold: SIPO unifying RLVR with on-policy self-distillation
21. 2609.36734 | 09-29 | hold: confidence-aware selective distillation
22. 2609.36695 | 09-29 | hold: selective self-distillation via internal information flow
23. MiMo-V2.6-Flash/Pro-MOPD | 09-27 | hold: 178-573 GB MoE, too big for the consumer host
24. MiMo-V2.6-Distill-Qwen-9B | 09-21 | hold: 18.8 GB dense distill, borderline 24 GB card
25. NV-Reason-CT | 09-08 | hold: 5.3B dense, 10.6 GB, NVIDIA release-tracker row
26. Qwen3.8-27B-NVFP4 | 09-04 | hold: 22 GB fp4, 24 GB card ceiling
27. whichllm (HN 48146369) | 05-15 | hold: ranked-by-your-hardware local LLM picker
28. LocalScore (HN 43572134) | hold: local throughput benchmark instrument
29. "The local LLM ecosystem doesn't need Ollama" (HN 47788385) | 04-16 | hold: 648 pts context signal
30. "Why your local LLM feels dumber than it is" (HN 49402232) | 08-22 | hold: 511 pts, 39 days old, outside window
31. "640tok/s on Gemma 4 with a megakernel" (HN 49897153) | 09-29 | hold: throughput ceiling signal
32. 2609.28653 | 09-23 | drop: predecessor hold then drop (0928 sweep #33), re-banking waste
33. 2609.28003 | 09-23 | drop: predecessor already holds it (0928 sweep #9)
34. 2609.36941 | 09-29 | drop: black-box secrets extraction, security-area overlap
35. IFM K2 Horizon, PrismML | n/a | drop: WebSearch-only leads, zero fetchable sources, never verified

## Pass 2, deep reads (7 arXiv abs pages read end to end; 2 full texts)

Read depths, honestly labeled. FULL TEXT = arxiv.org/html/<id>v1 fetched and read via structured extraction: 2609.31540, 2609.37902. ABS PAGE = arxiv.org/abs/<id> fetched via web reader and read whole (an abstract page is one screen; full-text HTML not fetched for these five): 2609.36860, 2609.32642, 2609.35833, 2609.30716, 2609.27581.

### The two full texts

- 2609.31540 Touchstone (Can You Check That?): defines a task as checkable when it exposes a cheap deterministic intrinsic check rejecting outputs that violate a NECESSARY (not sufficient) correctness condition; passing means survived-refutation with a measured false-accept rate. Seven off-the-shelf SLMs 1-8B (Llama-1B/3B/8B, Qwen-1.5B/3B/7B, SmolLM-1.7B) with GPT-5.5 as the escalation frontier. Headline: conflict detection 98.6% accuracy at 0.0% FAR (84.0% best single SLM without the pipeline); intent translation 93.8% / 5.6% FAR; log parsing accuracy 99.7/91.7/87.7% but FARs 27.7/14.4/30.0%; routing-code generation only 50% accuracy at 75% egress; the knowledge-only control (TeleQnA) shows checks cannot rescue knowledge gaps (78.2% vs 84.2% frontier). Mechanism: local-first admission control, offline per-model skill profiling, confidence-gated escalation (tau=0.6) that ships the check's diagnostic evidence to the frontier model as a repair hint.
- 2609.37902 (You Cannot Pick a Provider From the Price List): 43 days, three measurement waves, 93 endpoint-cells, 28,151 timed calls, 15-min price resolution, 6+ open-weight models, 16 named providers (DeepInfra, Novita, Cloudflare, DigitalOcean, Google, Parasail, Venice, AtlasCloud, Nebius, CoreWeave, SiliconFlow, Phala, Mara, Groq, Cerebras, SambaNova). Prices differ up to 8.8x, latencies up to 68x for the same model; median price-latency correlation -0.61. Measured-map router: cheapest provider within 5 accuracy points of best with >90% availability gives 94% accuracy at 1.57x cheapest cost with 0% below-floor; the online facet layer certifies (provider x task) pairs and never routes to uncertified facets; live 36-hour run moved Llama-3.3-70B traffic from $1.04/M to a $0.21/M certified endpoint, 63.7% serving-cost reduction.

### The five abstract reads

- 2609.36860 IronLLM: "We present IronLLM-0.6B, a 654M-parameter language model designed for efficient on-device inference" (from the fetched Atom XML). Edge-native, real-time embodied intelligence, 09-29. Self-reported numbers; no third-party benchmark found this ask.
- 2609.32642 PriCon (Ask Without Telling): local SLMs consult cloud LLMs without revealing task intent; "A local closed-loop refinement mechanism further maintains privacy and recoverability throughout consultation." 09-26.
- 2609.35833 Neurosymbolic Routing: "Many queries appearing to demand reasoning are in fact structurally deterministic" - a deterministic head answers first, the LLM only handles genuinely uncertain queries, on resource-constrained edge devices. 09-24.
- 2609.30716 (Words Speak Louder Than Order): behavioral evaluation of Gemma 4, "When a language model receives two conflicting documents as input, how does it decide which one to prioritize?" 09-25. Independent (non-vendor) evidence on the family holding the estate's gemma4 slot.
- 2609.27581 (Step Law Transfer): "We test whether Step Law transfers to small language models" - empirical recalibration below 59M parameters. 09-23. Scaling-law hygiene for anything smaller than the current janitor tier.

## The four research questions, answered from what was fetched

### RQ1: open-weight models since 2026-09-28 for the janitor/scut slots on a consumer Windows host

Honest window answer: NOTHING dated after 09-28 was found. The SoTA Feed's September listing ends at the MiMo-V2.6-Flash-MOPD / MiMo-V2.6-Pro-MOPD pair (Sep 27); StepFun's Step 5 Preview (600B/27B MoE) was teased 09-22 with open weights promised Oct 15 (HN 49796998). The strongest candidates found, all pre-cutoff:

- Muse Glimmer (Meta, 08-10): 30B multimodal, Apache 2.0, 128K+ context, "purpose-built for agent workloads that run locally"; Ollama blog confirms local serving (MLX on Apple Silicon, DFlash 1.5-1.8x speedup claim) and unsloth ships GGUF Q4/Q6/Q8 on HuggingFace (HN 49251771). A 30B Q4 is roughly a 24 GB card fit; this is a candidate for a local sovereign-AGENT slot ABOVE the janitor tier, not a gemma:2b replacement. All capability claims are Meta self-reports or blog-grade third parties: the funded tier would need to verify before any slot grant (laws.md:23).
- IronLLM-0.6B (09-29): the only sub-1B open model surfaced this window claiming real-time on-device inference; self-reported, needs a local re-run before touching the janitor slots.
- From the SoTA Feed: NV-Reason-CT (5.3B dense, 10.6 GB, 09-08) and Qwen3.8-27B-NVFP4 (22 GB, 09-04) are consumer-card-borderline; MiMo-V2.6 MoEs are not.
- The 0928 sweep already established (its bank, not re-derived here): nothing untuned under 2B beats a gemma-class 2B janitor per published numbers; wins come from narrow fine-tuned specialists (FunctionGemma 270M), harness/server repairs, and a 3-bit quantization floor.

Self-reported claims the funded tier should verify before action: Muse Glimmer's local-agent capability and DFlash speedups (vendor blog); IronLLM's real-time claims; GLM-5.3 open-weight "beat Anthropic/OpenAI for 1/5 cost" (reinvently.co.uk, HN 240 pts, blog-grade).

### RQ2: what replaced the dead Lightning lane and the dropped GLM-5.3-Flash rung; the Featherless gap

- No published "replacement" announcement was found. HN Algolia confirms GLM-5.3-Flash launched 2026-08-26 ("GLM-5.3-Flash", 1132 pts, z.ai/blog/glm-5.3-flash) and "GLM-5.3 is now open-weight" landed 2026-08-28 (806 pts, huggingface.co/zai-org/GLM-5.3); z.ai published "How GLM built its own inference infrastructure" 09-17 (411 pts, HN 49737922). The estate-side drop of the Flash rung (burns.md:57-59) has no public counter-announcement in anything fetched.
- The research-grade answer to lane churn is FACET (2609.37902, full text): provider price/quality maps decay fast enough that static per-model pricing is the wrong selection instrument; 16 providers measured, 8.8x price and 68x latency spread for identical models, live 63.7% cost cut by measured-map routing with certified-facet fail-safe anchoring. The estate's litellm checkout already carries a Featherless provider path at mine/raw/agent_platform/BerriAI/litellm/litellm/llms/featherless_ai/chat/transformation.py (catalog probe line 365410).
- Featherless counter gap: NO published explanation of the 22,059-served vs 28.6k-counter discrepancy was found (WebSearch returned nothing relevant). What I did verify live: the featherless.ai homepage now reads "Browse 40,000+ models" and "Test any of 40,000+ models effortlessly", so the marketing counter has moved past both numbers; the underlying served-vs-advertised gap question is superseded, not answered.

### RQ3: what the high-signal local-LLM wave says the local tier should adopt

The wave is real and current: nbHits 2916 for "local llm" (reproduced this ask; exact-phrase gives 540). The Clippy top hit is verified live (1122 points, 275 comments, created 2025-05-06, HN 43905942) and its own page carries the UX thresholds: "Offline, local, free: Everything runs on your computers. The only network request Clippy makes is to check for updates (which you can disable)." plus "Thanks to llama.cpp and node-llama-cpp, the app will automatically discover the most efficient way to run your models (Metal, CUDA, Vulkan, etc)". Read against the rest of the wave (AMD Lemonade local server 572 pts, whichllm hardware-ranked picker 283 pts, LocalScore benchmark 124 pts, "Why your local LLM feels dumber than it is" 511 pts), the adoptable thresholds are: (1) zero-setup with automatic backend/hardware discovery, (2) model choice ranked for YOUR hardware by benchmark, not by parameter count, (3) a local throughput benchmark (LocalScore-style) as the acceptance instrument, (4) offline-by-default. The estate's janitor tier already runs headless, so the transferable items are the hardware-ranked picker and a throughput acceptance gate; Touchstone adds the capability half: only route checkable chores local, and ship the check's diagnostic with every escalation.

### RQ4: the repeatable arXiv-door harvest for the frontier_thinking shelf, and state/arxiv staleness

- The shelf (11 files per CORPUS_CATALOG.md:19, counted at lens corpus.md:23) fills continuously from four doors, all proven live this ask: (1) the arXiv API recipe at lens doors.md:14-18 with this ask's query set (all:"small language model", all:"open-weight", distillation+language model, ti:"Gemma"+OR+ti:"Qwen"); (2) HN Algolia search_by_date "open weights" for release chatter; (3) sota.borgcloud.ai ("Every open-weights release from the labs that matter") as the release-truth tracker; (4) the bank file + receipts this ask produced. One pass is roughly an hour and yields 5-10 bankable items per window.
- Staleness: my census run (`find state/arxiv -type f | wc -l` = 3776, matching lens corpus.md:13; `ls state/arxiv` = 26 day folders spanning 2026-09-05 through 2026-09-30) shows the shelf is a ROLLING 26-day window, not an aging archive. No row is stale past usefulness by age: the oldest folder is 25 days old. The real limitation is depth, not age: rows are abstract-scale snapshots (the 0928 sweep measured one at 1,191 bytes), so they hold titles/dates/pointers but no full-text findings. Four of this ask's seven deep reads already had abstract snapshots on the shelf (see overlap census); the deep reads added the findings.

## Banked items (strongest first, mirrored in the SweepResult)

1. 2609.31540 Touchstone (2026-09-25) - the checkability instrument for the janitor tier
2. 2609.37902 market-aware provider routing (2026-09-29) - the lane-churn instrument
3. Muse Glimmer (2026-08-10) - 30B Apache-2.0 local agent model, candidate above the janitor tier
4. 2609.36860 IronLLM-0.6B (2026-09-29) - sub-1B edge-native candidate, self-reported
5. 2609.32642 PriCon (2026-09-26) - task-private local-to-cloud consultation protocol
6. sota.borgcloud.ai SoTA Feed (2026-09-21) - repeatable release-truth door; answers the since-09-28 window honestly
7. Clippy artifact + wave stats (2025-05-06, verified live 09-30) - the UX thresholds
8. 2609.30716 Gemma 4 behavioral eval (2026-09-25) - independent evidence on the slot holder

2609.35833 and 2609.27581 were deep-read and banked in prose above; displaced from the top-8 by the release-truth and RQ3 items the ask names directly.

## Overlap census (commands actually run this ask)

- Byte-precise probe of catalog/catalog.jsonl (691,788 lines) via .venv/Scripts/python.exe term scan over 12 terms: "Checkability Boundary" 1 hit = catalog line 581100, path local_sovereign_agent/state/arxiv/2026-09-28/2609.31540v1.txt (abstract snapshot, age_days 0). "Market-Aware Routing for Open-Weight" 1 hit = line 690781, state/arxiv/2026-09-30/2609.37902v1.txt. "Words Speak Louder Than Order" 1 hit = line 580910, state/arxiv/2026-09-28/2609.30716v1.txt. "Step Law Transfer to Small-Scale" 1 hit = line 445440, state/arxiv/2026-09-24/2609.27581v1.txt. "Touchstone" 1 hit = an unrelated estate file (memory/continuity/seat_memory_20260927/isfahan-1197-lock-touchstone.md). "IronLLM" 0, "Ask Without Telling" 0, "Neurosymbolic Routing for Reliable Reasoning" 0, "Muse Glimmer" 0, "borgcloud" 0, "MiMo-V2.6" 0.
- "Featherless" 5 hits, all litellm provider source under mine/raw/agent_platform/BerriAI/litellm/ (code support, no prior findings).
- rg -i -c "IronLLM" catalog/catalog.jsonl rerun standalone: exit 1, zero hits (settles an earlier ambiguous chained-grep reading; the probe and rg agree on 0). rg -i -c "task-private consultation": exit 1, zero.
- rg -l -i "Muse Glimmer|IronLLM|Checkability Boundary" memory/: zero files.
- Predecessor dedupe: watch/inbox/frontier_olm_20260928/sweep/open-and-local-language-models-arxiv.md read in full this ask; its 8 banked ids and 34-item consider list share ZERO ids with this ask's bank (its #9 2609.28003 and #33 2609.28653 were re-surfaced by my queries and deliberately dropped as re-banks).

## OWED / not verified

- IFM K2 Horizon (0.9B/3.7B/7B) and PrismML: WebSearch-only mentions with no fetchable page; unverified, never banked.
- Muse Glimmer's <20 GB VRAM local-run claim rides a 2-point HN post (49249632); the Ollama blog I fetched gives no VRAM figure. A local GGUF Q4 pull-and-run is the only honest verification.
- The Featherless 22,059 vs 28.6k gap: no published explanation found; homepage now reads 40,000+. Not resolved, superseded.
- Kimi/Qwen license texts: carried OWED from the 0928 sweep, not re-verified here.
- Full-text HTML for 2609.36860, 2609.32642, 2609.35833, 2609.30716, 2609.27581 not fetched; their deep reads are abs-page depth, labeled as such above.
- INDEX.json registration of this file: not performed (not asked; the workflow publishes).

## Receipts

All fetches this ask: WebFetch (arXiv API x4, HN Algolia x6, featherless.ai, ollama blog, clippy page, sota feed, arXiv HTML x2), web reader (7 arXiv abs pages), WebSearch x2, plus local instruments (python catalog probe, rg greps, find/ls census) run in this ask's transcript. No raw XML receipts were written to disk this pass; every quoted string above is copied from tool output in this transcript with its URL attached.
