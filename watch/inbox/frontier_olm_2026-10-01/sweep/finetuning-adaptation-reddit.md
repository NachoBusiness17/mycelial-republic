# SWEEP: finetuning-adaptation via reddit - 2026-10-01

source-fetched: 2026-10-01
Area: finetuning-adaptation (reddit door). Gopher: sweep-finetuning-adaptation-reddit (GLM-5.3-Flash seat in a dynamic workflow).

## DOOR FORENSICS (all direct reddit doors degraded - fallback used and recorded)

Ran in this session, in order:

1. `WebFetch https://old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` (and same for r/MachineLearning, r/LocalLLM, r/ollama): all four returned only the "Welcome to Reddit" shell, zero post data. old.reddit now requires an account ("Log in to use old Reddit" per web_reader read of the same URL).
2. `WebFetch https://www.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50`: HTTP 403 Blocked.
3. `WebFetch https://old.reddit.com/r/LocalLLaMA/top/?t=month` (HTML): welcome shell, no listing.
4. `WebFetch https://old.reddit.com/r/LocalLLaMA/comments/1sexdhk/...` (thread page): same login wall.
5. `mcp web_reader` on old.reddit listing and www thread: first read got the login wall, later reads got Reddit's "Please wait for verification" bot page, plus 1302 rate limits between attempts.
6. `WebFetch https://r.jina.ai/https://www.reddit.com/r/LocalLLaMA/comments/1sexdhk/...`: Reddit returned 403 Forbidden through the proxy.
7. `WebFetch https://api.reddit.com/r/LocalLLaMA/comments/1sexdhk`: HTTP 403 Blocked.
8. Redlib mirrors: redlib.catsarch.com -> HTTP 429 Too Many Requests; rl.bloat.cat -> ECONNRESET.

**Fallback actually used (the recipe's sanctioned fallback): WebSearch `site:reddit.com`** - 9 successful searches total (2 more died to 1302 rate limits and were re-run after backoff). Deep reads below are snippet-deep: the search index surfaces post/comment content verbatim in `content` fields, but I could NOT load full comment trees. Every quote below is copied verbatim from the snippet I actually received; nothing is reconstructed. Where a claim is the search tool's summary rather than a verbatim snippet, it is marked as such.

**Clean corroboration door:** `unsloth.ai/docs` fetched directly via WebFetch (works, no wall) - used to byte-corroborate the Gemma 4 fine-tuning claims and date the release era. A third-party AI Pulse article 302-redirected into Vercel SSO and was NOT followed (same 302-SSO disease AGENTS.md warns about for the estate's own Vercel URLs).

## PASS 1 CENSUS (broad sweep, ~50 candidates considered)

Candidates gathered across the searches (r/LocalLLaMA dominant; also r/MachineLearning, r/LocalLLM, r/Rag, r/deeplearning, r/MistralAI, r/AI_Agents, r/WebAfterAI, r/singularity, r/OpenAI, r/ArtificialInteligence, r/legaltech):

- Gemma 4 fine-tuning: 1sexdhk (8GB VRAM finetune + bug fixes); docs corroboration at unsloth.ai/docs/models/gemma-4 and /train
- 2026 local-FT framing: 1rwj60g "Local fine-tuning will be the biggest competitive edge in 2026"; 1re5qdy "Is 2026 the Year Local AI Becomes the Default?"; 1ro3zwu "2026 reality check: Are local LLMs on Apple Silicon legitimate?"
- FT vs RAG: 1mltedd, 1ld8gs4 "Fine-tuning may be underestimated", 1itkgwf, 1fhtl6c, 1hc1kyo, 1fntw4z, 1cfdbpf "RAG is all you need", 1ov7ogq "Stop fine-tuning your model for every little thing", 1rlt0su "Your RAG Benchmark Is Lying to You" (measured RAG-config numbers, not FT ablation)
- Data-quality / dataset prep: 1mqme6y (formatting hours, broken UTF-8), 1wu9zkn ("dataset prep is 99% of the work" - paraphrase, not verbatim-verified), 1ilkamr ("80% of your time on data"), 1pj7aih, 1fm59kg
- Tiny-model seats: 1qojhw3 (270M for sensitive-info obfuscation), 1r6gx75 (FunctionGemma 270M multi-turn tool calling), 1mxagp5, 1mz2di5, 1sexdhk
- Domain law/tax: 1vyl6yj Thomson-1.0-Small (+ r/legaltech 1vxd4qw crosspost)
- Continual learning / forgetting: 1w0198r Engrams main post (~1.3K upvotes, 343 comments), 1wis23s "Update: Small model + Engram", 1qjt08m "Sleeping on Engram", 1slv4ez "The decline in LLM reasoning and catastrophic forgetting", 1qd696s Nvidia end-to-end test-time training (r/MachineLearning), 1c8r7wq
- Secrets/PII in training data: 1bol0gl, 18s1lvj, 1pksdhr
- Practitioner guides: 1od0gw9 "LoRA/QLoRA: The most significant training parameters", 1t2jc34 "The Ultimate LLM Fine-Tuning Guide", 18o5u0k VRAM table, 1e07km4, 1bkvtib
- Toy/small-data: 17eo5mo (10 samples), 1oabtk1 "Can and should I train a LoRA?", 1ndjxdt Unsloth AMA, 1n2jraj gpt-oss 60k FT, 1ggaagw 16GB VRAM

**Window degradation, stated plainly:** the recipe asks for candidates from the last 30 days. With the listing doors down, I cannot enumerate a subreddit's last-30-days top list; search results are recency-uncontrolled. Several banked items are demonstrably 2026-current (Thomson dated 2026-08-26 by corroboration; Engrams thread has a newer reddit ID than Thomson; "biggest competitive edge in 2026" is 2026-titled). Others are undated because the door is down. Every banked item carries its date status honestly; none is claimed in-window without evidence.

## PASS 2 DEEP READS (8 threads, snippet-deep; strongest first)

### 1. "You can now fine-tune Gemma 4 locally, 8GB VRAM, + bug fix" (r/LocalLLaMA 1sexdhk) - Q1
Verbatim (search-indexed snippet): "You need 8GB VRAM to train. Unsloth trains Gemma 4 ~1.5x faster with ~60% less VRAM than FA2 setups: for Vision, Text, Audio and inference."
Corroborated byte-level by fetching https://unsloth.ai/docs/models/gemma-4/train directly this session: "Gemma 4 E2B trains on 8GB VRAM. E4B requires 10GB VRAM."; "Gemma 4 E2B LoRA works on 8-10GB VRAM. E4B LoRA requires 17GB VRAM."; "31B QLoRA works with 22GB"; "Unsloth trains Gemma 4 ~1.5x faster with ~60% less VRAM than FA2 setups (no accuracy loss)". Docs also fix named bugs (gradient-accumulation loss inflation; 31B/26B IndexError from `layer_types[:-0]` collapsing to `[]`; fp16 audio overflow from a -1e9 masked_fill) and note "High losses of 13-15 on E2B/E4B are described as normal for multimodal models."
Estate read: the tier ladder's local seats are `gemma:2b` scut and `gemma4` short worker. E2B LoRA on 8-10GB means the estate could train its own short-worker adapter on the consumer GPU it already has, feeding from room.jsonl/session tapes. The 13-15 initial-loss note is a free tripwire: a first QLoRA run on session rows that shows loss 13-15 is not necessarily broken.
Date: unknown (thread date unreadable, door down; docs date the fine-tuning release era to Apr-Jun 2026; docs screenshots dated 2026-04-07).

### 2. "No, Engrams won't let you run 1T models locally. It does something even better" (r/LocalLLaMA 1w0198r) - Q4
Verbatim (title as indexed): "No, Engrams won't let you run 1T models locally. It does something even better" (~1.3K upvotes, 343 comments per search result). Search-summary (not verbatim): the thread argues Engrams matter because a model can be trained further without forgetting, with commenters noting removing existing engrams could be catastrophic. Follow-up "Update: Small model + Engram" (1wis23s) reports positive results building the Engram table OUTSIDE the model while freezing it (search-summary).
Estate read: this is the external-memory-vs-weights question the estate is already working from the other side (memlance/memweave inject structures instead of training them in). The 1wis23s pattern - new knowledge in a frozen-external table, base weights untouched - is exactly the shape of a rolling estate-corpus "training loop" that never risks catastrophic forgetting because nothing is backpropagated. Q4's paper-level answer (forgetting under continual adaptation) has a practitioner-level answer here: don't put the rolling corpus in the weights at all.
Date: unknown; reddit ID sorts newer than 1vyl6yj (2026-08-26), so likely late Sep 2026, unverified.

### 3. "How many hours did you spend formatting data for fine-tuning?" (r/LocalLLaMA 1mqme6y) - Q1/Q3 data-quality gates
Verbatim (search-indexed comment snippet): "Needed to convert them to the chat format. Spent 4 hours writing Python to parse the tickets. Realized half had broken UTF-8 encoding. 2 more ..."
Estate read: this is the noisy-session-corpus gate problem in miniature and maps 1:1 onto the estate's 14,859 session rows (lens/corpus.md) and room.jsonl. The practitioner gate order is: source parse -> encoding check -> chat-format conversion - exactly the per-row provenance/gating the code-agent-data organ needs before a row becomes an instruction pair. The UTF-8 gate is cheap and should run first on room.jsonl if not already banked.
Date: unknown.

### 4. "Why aren't people using small llms to train on their own data?" (r/LocalLLaMA 1mltedd) - Q2
Verbatim (search-indexed top-comment snippet): "The problem is that 'tiny' models are still pretty big and fine tuning them costs money. They don't generalize anywhere near as well..."
Estate read: the counter-position to Q2's premise, and the honest one for 2B seats: community consensus (this thread plus 1qoyoty, 1ov7ogq per search summaries) is that RAG beats fine-tuning for personal/private KNOWLEDGE, and fine-tuning earns its keep only on narrow tasks where format/style/behavior matter more than facts. For estate law vocabulary specifically: bake the jargon's USE (drafting style, term handling) into weights; keep the jargon's FACTS behind retrieval.
Date: unknown (ID sits between early-2025 and mid-2025 era threads; unverifiable with doors down).

### 5. "Thomson Reuters releases Thomson-1.0-Small. A law and tax focused model" (r/LocalLLaMA 1vyl6yj) - Q2
Verbatim (title as indexed): "Thomson Reuters releases Thomson-1.0-Small. A law and tax focused model. New Model."
Search-corroborated details (two secondary sources, not verbatim from reddit): open-weight MoE, 35B total / 3B active, fine-tuned from Qwen3.6-35B-A3B, reported 79.9% Stanford LegalBench; posted ~2026-08-26 (AI Daily Digest dates it Aug 26, 2026).
Estate read: proof-of-landscape for Q2 - a major publisher ships a law-domain small-ACTIVE model rather than a dense small model, and measures it on LegalBench. The estate-law-vocabulary play at true 2B scale remains unclaimed territory; nobody in this sweep published a 2B law-jargon ablation. Slightly out of the 30-day window (36 days); kept for the LegalBench precedent.
Date: 2026-08-26 (per AI Daily Digest corroboration).

### 6. "Fine-tuning may be underestimated" (r/LocalLLaMA 1ld8gs4) - Q2
Verbatim (search-indexed snippet): "Fine tuning allows you to achieve the same results as RAG with smaller LLMs and fewer tokens."
Search-summary (not verbatim): adds that LoRA won't always be enough but gets part of the way there. This is the closest thing this sweep found to a measured FT-vs-RAG claim for small models; it is an assertion with community traction, NOT a published ablation. No rigorous 2B-scale FT-vs-retrieval ablation surfaced anywhere in the sweep; the estate could generate one cheaply on its own corpus (C1 program shape: same estate-law eval set, retrieval arm vs QLoRA arm).
Date: unknown.

### 7. "I'm finetuning a 270M parameter model for sensitive information" (r/LocalLLaMA 1qojhw3) - Q3
Verbatim (search-indexed snippet): "The obfuscation task is simple: the model receives a text, processes it and returns the same text with the sensitive data obfuscated using a tag."
Estate read: two Q3 lessons in one thread. (a) The pipeline shape for secrets: a tiny in-house model tags/obfuscates sensitive spans BEFORE rows become training pairs - a model-in-the-loop redaction gate, cheaper than regex walls. (b) The estate's own 270M-class seat could BE that redaction model (Gemma 3 270M family fine-tunes are a recurring r/LocalLLaMA theme this year: 1r6gx75 FunctionGemma for multi-turn tool calling, 1mxagp5, 1mz2di5). Related older threads (1bol0gl, 18s1lvj) push the same pattern: detect-PII model -> scrub -> train.
Date: unknown.

### 8. "Local fine-tuning will be the biggest competitive edge in 2026." (r/LocalLLaMA 1rwj60g) - Q1 framing
Verbatim (search-indexed snippet, truncated at its edge): "Fine-tuning significantly improved the speaker's style similarity compared to using zero-shot"
Estate read: the year's thesis post for Q1. The measured-ish claim is about STYLE (voice similarity), not knowledge - consistent with the whole sweep's consensus: fine-tuning moves style/format/behavior; retrieval moves facts. For the estate: the biographer's voice and the janitors' output format are the fine-tuning targets; the session FACTS stay in retrieval.
Date: unknown (2026 from title).

## ANSWERS TO THE FOUR RESEARCH QUESTIONS (sweep-grade, degraded door)

1. **QLoRA/LoRA practice for 2B-8B on a single consumer GPU (2026):** the Unsloth-centered path is current (E2B 8GB, E4B 10GB, 31B QLoRA 22GB - docs verified this session); named bug class to avoid (grad-accum loss inflation, `layer_types[:-0]` slice bug); multimodal small-model initial loss 13-15 is normal. Data-quality gates for noisy session corpora: practitioners report the cost is in parse -> encoding -> chat-format conversion (1mqme6y), and the community's standing ratio claims ("80% of your time is data", 1ilkamr; "99% of the work", 1wu9zkn - the latter paraphrase-only).
2. **FT vs retrieval/prompt-stuffing at 2B for domain jargon:** no measured 2B-scale ablation found. Community position splits: knowledge -> RAG (1mltedd and consensus), style/jargon-in-use -> fine-tune (1rwj60g, 1hc1kyo); 1ld8gs4 claims FT matches RAG at smaller model+fewer tokens but shows no numbers in the snippets I could read. 1rlt0su's measured numbers are RAG-config-only (LangChain default 0.535/0.202 vs naive+reranker 0.549/0.282 Hit Rate@5). The ablation the estate wants does not exist publicly at 2B - that is an open C1-shaped experiment.
3. **Session logs -> instruction pairs without leaking secrets:** strongest pattern is model-in-the-loop obfuscation: a small fine-tuned model tags sensitive spans before rows become pairs (1qojhw3; older 1bol0gl/18s1lvj). No thread in the sweep showed per-row provenance gating as a mechanism; the estate's hash+provenance registry instinct is ahead of the public practice surfaced here.
4. **Catastrophic forgetting under continual adaptation:** the loud 2026 practitioner thread is the Engrams family (1w0198r + 1wis23s): keep base weights frozen, grow knowledge in an external table - forgetting risk moves to table maintenance ("removing existing engrams could be catastrophic", search-summary). Direct weight-level continual-FT threads (1c8r7wq, 1slv4ez) remain pessimistic. For a rolling estate-corpus loop, the sweep's lesson is: rolling corpus -> retrieval/engram-table, frozen base; periodic distilled adapter re-trains, never naive continued SFT.

## OVERLAP GREP (run this session, not assumed)

- `grep -c -i "<phrase>" catalog/catalog.jsonl` for 16 phrases (Thomson, RAG Benchmark Is Lying, why aren't people using small llms, How many hours did you spend formatting data, LoRA catch on, Can and should I train a LoRA, Ultimate LLM Fine-Tuning, most significant training parameters, domain specific experts, seven kinds of agent memory, test-time training, Engrams, FinanceBench, ...): 0 catalog hits on every thread-specific phrase. The only catalog "Gemma 4" matches are an unrelated internal asset ("Gemma 4 Prompt Logs.zip", 146175 bytes, mtime 2026-04-16) - not these threads.
- `grep -r -l -i` over memory/: "Thomson" matched only incidental corpus substrings (memory/corpus/game_design_docs/nethack_guidebook_367.txt, memory/corpus/mycology_canon/*.xml); "RAG Benchmark Is Lying" matched only memory/trajectory/steps.jsonl:40278, which is this session's OWN grep command being logged (ts 2026-10-01T14:58:35Z) - self-noise, not a prior bank.
- Sibling sweeps in this same dir (open-local-language-models-*: arxiv/hn/reddit/x) cover OTHER Gemma 4 threads (1sgq19k, 1slcb4r, 1t3dfvp, 1uz2u9k, 1saxvw2) - none of the 8 items banked here appears in them.

## NOT BANKED (considered, rejected)

- 1rlt0su "Your RAG Benchmark Is Lying" - measured numbers but RAG-config-only, ~7 months old, not FT-vs-RAG.
- 1wu9zkn, 1ilkamr, 1od0gw9, 1t2jc34, 18o5u0k, 1e07km4, 1bkvtib - practitioner guides, older or paraphrase-only; content already represented by banked items 1/3.
- 17eo5mo, 1oabtk1, 1bol0gl, 18s1lvj, 1pksdhr, 1c8r7wq, 1slv4ez, 1qd696s - real signal but superseded by the banked item in the same question slot (max 8).
- 13qrdj6 (2023 QLoRA original), 137rxgw (2023 Leaked Moat) - historical, out of window.

## HONEST LIMITS

- No full comment tree was read for ANY item: every reddit page fetch path (old.reddit json/html, www json, api.reddit, web_reader, jina proxy, redlib mirrors) failed this session. Deep reads are snippet-deep via the sanctioned WebSearch fallback; quotes are verbatim from what the search index surfaced.
- Dates are mostly "unknown" because the door is down; two items carry corroboration dates.
- The last-30-days pass-1 constraint is degraded to "recency where verifiable"; stated per item.

## CORRECTION (post-submit, same session, from the completed background grep)

The overlap grep ran in the background and I read its partial output before submitting; the finished run adds one real overlap the submitted Engrams item's overlap field understated ("memory/ 0 hits" was true only of the phrases the partial run had reached):

- The estate holds its OWN engram design line: `memory/runs/engram_20260913/` (E01_template through E08_the_ponytail; E02 opens "Design - the engram architecture for this fleet" with verdicted-leaf, wave-engram Merkle tiers; E06_associative_recall and E07_decay_forget are directly adjacent to the reddit thread's Q4 territory of associative recall and forgetting).
- `memory/continuity/seat_memory_20260927/rashomon-surfacing-style.md` uses "engrams" as a scale-free-states metaphor (Asimov's property for weights).
- The reddit Engrams thread (item 2) is therefore NOT estate-new as a concept - it is independent 2026 community convergence on the architecture the estate sketched 2026-09-13. The estate delta is that its engram line is verdict/provenance-native (Merkle rollups over tri-state verdicts) while the reddit line is model-architecture-native. The submitted result stands except for that overlap sentence; this section is the corrected record.
- All other overlap verdicts verified unchanged in the full grep: catalog/catalog.jsonl 0 hits on every thread-specific phrase; steps.jsonl hits on multiple phrases are this session's own logged commands; no other real estate holdings matched the candidate titles.

