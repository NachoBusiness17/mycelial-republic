# Frontier sweep: finetuning-adaptation (X door) - 2026-10-10

source-fetched: 2026-10-10. Seat: sweep-finetuning-adaptation-x. Instrument: WebSearch (Z.ai web_search_prime backend) + WebFetch + mcp web_reader + arXiv export API.

## Door status (say it straight)

- X door DEGRADED from this seat, per the recipe fallback: the search backend ignores `site:x.com` (returned unrelated pages: Wiley "Small" journal, Wikipedia "Khat", Spotify "Fine"); parallel searches 429/1302-stormed until paced one-at-a-time; nitter/xcancel mirror returned HTTP 451; no x.com status URL/ID ever surfaced in any result block, so the fxtwitter door (api.fxtwitter.com/<user>/status/<id>) had nothing to resolve - it was never fired with a guessed ID because inventing one is fabrication. This matches the estate's standing X-surface OWED (commit f06008308: syndication mirror needs page-derived token).
- Fallback used: general-web search snippets + direct fetches of publisher pages (pytorch.org, arxiv.org, unsloth.ai). Every banked item below was fetched and read end-to-end by this seat, quote verbatim from the fetched page.
- unsloth.ai 403'd the standard WebFetch; read through the web_reader MCP door instead (front page + description meta only).

## Pass 1 ledger (50 candidates considered; 30+ inside the last-30-days window)

Clusters swept: single-host LoRA/QLoRA tooling (Unsloth ecosystem, 6 items), test-time training (arXiv API, 12 items inside the window), agent distillation (arXiv API, 9 items), QAT/compression (6 items), production finetuning case studies (3), ICL-vs-weights theory (7), decision guides (4), steering-via-LoRA (1), TTS/misc (2). Notable rejects and why:

- OnlineQAT (arXiv 2610.09346, Oct 7 2026, 3-bit Qwen3-1.7B 57.28 avg) - ALREADY BANKED day-9 prior art per the ask; catalog grep confirms 3 hits on "OnlineQAT"/"2610.09346". Not re-banked.
- qTTT "Let's (not) just put things in Context" (arXiv 2512.13898, Dec 15 2025; Qwen3-4B +12.6/+14.1 pp LongBench-v2/ZeroScrolls) - read via arXiv API, strong, but 10 months old; context only.
- "LoRA vs Full Fine-tuning: An Illusion of Equivalence" (arXiv 2410.21228, 2024) - foundational context; Shopify cites it as ref [4] for their retrain-on-old+new drift control.
- Gemma 4 QAT checkpoints (blog.google, Jun 5 2026; ~66% vLLM VRAM reduction per search snippet) - snippet-tier only: both guessed primary URLs 404'd (ai.google.dev/gemma/docs/qat, /tune/qat, blog.google and developers.googleblog.com paths) and search returns domains without full paths. OWED as a fetch; numbers NOT asserted beyond this line.
- Universal TTT (2610.05484), DeltaTTT (2610.08553), ActFirst-OPD (2609.36608, ~5x faster OPD), GC-OPD (2609.37522, ~2x student success), TRACE FP4 MoE RL (2610.07767, rollout 5.4x), QUASAR (2608.13966, INT2 +13.3 pts), CanonQ W2A4KV2 (2610.09202), SkillSandbox (2610.10088), Red-TTT (2610.05282), ProTTT (2609.32564), AuxMark (2609.34597), StageGuard (2609.20791) - arXiv-API-feed one-liners, context tier, not banked as reads.

## Pass 2: the 8 banked items (strongest first; every quote verbatim from the page this seat fetched)

### 1. How Shopify built a continual learning loop with PyTorch (production receipts -> weights, measured)
- URL: https://pytorch.org/blog/how-shopify-built-a-continual-learning-loop-with-pytorch-and-vllm/ - Last updated 2026-09-22. Read in full.
- Quote: "a continual learning loop that compresses production experience into the continuous space of the model's weights"
- Estate answer (q1, the living-weights falsifier): Shopify states the exact lesson-class boundary we keep circling: first "improvements accumulate in the discrete artifacts around it: prompt edits, retrieval examples, routing rules, and harness code" and only "once harness improvements plateau, we begin optimizing in parameter space" by mining hard negatives into daily full-parameter SFT + GRPO with a calibrated judge as reward. Measured: frontier serving ~$27M/yr est. vs ~$1M fine-tuned (96% cut) at up to 2,000 req/min; gist-token prompt compression 6,000 -> ~1,500 tokens, TTFT -19%, e2e -38%, ~14% fewer GPUs. The class of lesson that NEEDS weights is the compounding behavioral residue after the harness plateaus - not the laws themselves.
- Overlap: catalog "Shopify" hits are litellm source files named shopify.* (4 rows) and MEMORY.md:235 is a commerce-agents card - unrelated. Genuinely new.

### 2. ASCENT: Online Test-Time Training of Long-Horizon Agents via Self-Distillation of Verified Experience
- URL: https://arxiv.org/abs/2610.05303 - submitted 2026-10-04 (Lu & Gong). Abstract read in full.
- Quote: "trains the LLM's weights on its own execution trajectories during deployment"
- Estate answer (q1 mechanism): the exact instrument the living-weights falsifier describes, already built: frozen base model sees the VERIFIED trajectory as privileged info and hindsight-predicts next-token distributions along it; those distributions distill into persistent LoRA fast weights; invalid-action turns stripped; "the agent executes each task once, in one pass over the stream" - no teacher, no retrieval. Verified receipt -> weight delta, online, at small-model scale (ALFWorld/WebShop/AppWorld). This is the SHERPA-cheap-first shape for a gemma janitor.
- Overlap: raw deep-read HTML already in intake from the 10-06 sweep (catalog id b90bf5a1748e, watch/inbox/frontier_olm_2026-10-06/sweep/raw/deep_2610.05303.html); no distilled finding row found in catalog/memory subset - banking the analysis, flagging the raw-duplicate.

### 3. Distilling Agentic Systems: A Roadmap across Models, Artifacts, and Harnesses
- URL: https://arxiv.org/abs/2609.36630 - submitted 2026-09-29 (Luo et al.). Abstract read in full.
- Quote: "the persistent transfer of task-solving knowledge from a teacher agent to a student agent"
- Estate answer (q1 vocabulary): the field now names our ribs-vs-weights split: competence "extends beyond model parameters" and the taxonomy of WHERE knowledge is retained is model / artifacts / harness / substrates, with an eval framework linking retention to "causal contribution and deployed utility". That is the laws-lens q11 question stated as a survey; steal the taxonomy as the estate's register-schema language.
- Overlap: zero hits on title and id in catalog + memory subset. New.

### 4. Recursive Harness Distillation across Agents for Robot Manipulation
- URL: https://arxiv.org/abs/2609.33378 - submitted 2026-09-27 (Kim et al.). Abstract read verbatim.
- Quote: "reuse accumulated intervention knowledge in new task instances without updating model parameters"
- Estate answer (q1 boundary, the other side): measured proof the rib/playbook path is not a compromise - a strong agent's intervention experience distilled into a textual playbook, recursively refined by the light agent's execution feedback: real-world 37.3% -> 64.0%, SimplerEnv 41.7% -> 66.7%, and the SAME playbook lifts the strong agent to 79.2%. Register rows that transfer across agent classes without touching weights: that is our ribs, with numbers. Weights are for residue; playbooks compound for both janitors and primes.
- Overlap: zero hits. New.

### 5. Quantization-Aware Healing (QAH) -> Hypernova-60B open-weight
- URL: https://arxiv.org/abs/2608.20953 - submitted 2026-08-21 (Ryskulov et al.). Abstract read verbatim.
- Quote: "it reaches a comparable peak about 7 times faster and stays stable under continued training, without hand-tuned early stopping"
- Estate answer (q2, measured): against a matched QAT baseline, QAH (distill the 4-bit student directly from the ORIGINAL uncompressed model, skip the compressed bf16 middleman) reaches comparable peak ~7x faster, matches-or-beats its bf16 source on 7/9 benchmarks at ~4x less weight memory, and names a reproducible quality gap between distributed-training backends. Note the shape: healing distills from source-of-truth, exactly what our rib path does with receipts. Caveat: 60B scale, not janitor scale, and v1 is Aug 21 (outside 30d window, kept because q2 demanded measured cost numbers and almost nothing else has them).
- Overlap: zero hits on title and id. New.

### 6. Using Context Is Not Enough: Test-Time Training for Personalized Reward Modeling (P-TTT)
- URL: https://arxiv.org/abs/2609.35109 - submitted 2026-09-28 (Wang et al.). Abstract read in full.
- Quote: "fail to capture the preference relations conveyed by contextual pairs"
- Estate answer (q3 boundary): in-context adaptation demonstrably does NOT cover relational/preference knowledge: ICL-based personalization loses exactly the pairwise relations; P-TTT writes them into user-specific fast weights "within a single forward pass without inference-time backpropagation". Abstract claims "large margin" over SOTA without printing numbers on the page - numbers OWED to the PDF. Middle rung confirmed between rails and finetunes.
- Overlap: zero hits. New.

### 7. Test-Time Adaptation of Reasoning Strategies with Bayesian Nonparametric Memory (Bayesian Cheatsheet)
- URL: https://arxiv.org/abs/2610.06516 - submitted 2026-10-05 (Ramji et al.). Abstract read in full.
- Quote: "shares components across domains while allowing domain-specific mixing weights"
- Estate answer (q3 coverage): a growing HDP-GMM cheatsheet over behavior embeddings, softly updated per sample, retrieves past reasoning insights with no weight updates and no fine-tuning; gains on AIME'25, Omni-MATH, PhysReason incl. cold start (numbers not in abstract). This is the steering-free competitor to our rail engineering for the reasoning-strategy class specifically - and it is basically a probabilistic rib cache with posterior retrieval.
- Overlap: raw arXiv daily-dump text already mirrored in state (catalog id e72504d869a3, state/arxiv/2026-10-06/2610.06516v1.txt, zone lsa) - the mirror caught the bytes, no distilled row exists; banking the analysis on top.

### 8. Unsloth desktop app - "Run and Train Models Locally" (product-shape change)
- URL: https://unsloth.ai/ - front page read live 2026-10-10 via web_reader (WebFetch 403'd).
- Quote: "Unsloth is an open-source, no-code deskot UI for training and running open models on your local hardware." [sic - typo in their meta]
- Estate answer (q1 single-host reality): the cheap finetuning path has collapsed into a no-code local desktop app (built-in quantization model hub; OpenAI-compatible local API), i.e. the marginal operator cost of TRYING a finetuned janitor is now near zero - the ASTRA-successor question is no longer blocked by tooling, only by eval discipline. Front-page tier only; the Oct 8 "Decision models" post appeared in search snippets but not in the fetched page - not asserted further.
- Overlap: estate knows Unsloth as LoRA accelerator (memory/frontier/scout_findings.jsonl f-004, 2026-08-09, verdict WATCH, plan to wire into train_ghost.py); the desktop-UI pivot + agent hookup is the delta being banked.

## Research-question verdicts (only from the above reads)

- q1: The receipt-statable classes are prompts/retrieval/routing/harness-code (Shopify's discrete artifacts); the class needing weight changes is the post-plateau behavioral residue, and ASCENT shows the minimal instrument (verified-trajectory hindsight self-distillation into LoRA fast weights, single pass). Recursive Harness Distillation proves some classes should STAY in the playbook even when weights are available. The roadmap survey hands us the taxonomy to state this as law.
- q2: Cheapest measured path for scut lanes is now distillation-based healing, not vanilla QAT: QAH ~7x-to-peak vs matched QAT baseline (60B scale); OnlineQAT (banked) covers 3-bit at 1.7B. NOTHING public measures cost against a record/rib adaptation path - babelfish's 2,778 claim lines -> 151 invariant/109 instrument/2,058 register rows has no external rival benchmark; that comparison is an estate instrument to build, not a number to cite.
- q3: Coverage is real but sliced: reasoning-strategy reuse (Bayesian Cheatsheet, no weights), preference relations (P-TTT fast weights), long-horizon task-solving (ASCENT), long-context (qTTT, prior art). Persistent harness-level law remains outside all of them.
- q4: Not blocked. 8/8 banked items came through the arXiv export API + vendor blogs; the estate's state/arxiv daily mirror already ingests the raw abstracts (proven by the 2610.06516v1.txt row) - the gap is distilled rows, not corpus volume. 30,751 course rows + arXiv door cover this delta for this area.

## OWED
- Gemma 4 QAT primary page fetch (all guessed URLs 404'd; snippet-tier only).
- X door resolution: zero x.com posts banked this run; token-derived X surface remains the estate's standing OWED.
- P-TTT numeric gains (PDF-tier), Bayesian Cheatsheet numeric gains (PDF-tier).
