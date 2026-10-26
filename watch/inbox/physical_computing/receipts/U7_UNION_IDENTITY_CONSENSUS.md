# U7 — Union Alpha: Identity Consensus + Benchmark Intel Sweep

- **Lane:** U7 (intelligence sweep, receipt-first)
- **Date:** 2026-09-16
- **Operator:** wave-lane agent (open web sweep; no git, no paid APIs; X via api.fxtwitter.com)
- **Seed:** https://x.com/opencode/status/2100236430890991782 — OpenCode (@opencode, ~180K followers), posted Wed 2026-09-16 14:52:40 UTC: "Union Alpha (stealth model) is free for the next week / - no data training / - built for agentic coding / - supports images / let's see what you can do". Stats at sweep time: 7,846 likes · 376 RT · 423 quotes · 488 replies · ~2,010 bookmarks · ~994,861 views. No media attached.

## Log (append as I go)

- [t0] Seed tweet pulled via fxtwitter — text, stats, zero media confirmed. Quote count 423 (mission said 417 — close, still climbing).
- [t0] Receipt stubbed. Beginning HN thread pull.
- [t1] NOTE: mission's HN id 49717558 is a DIFFERENT thread (typesafe.ai "System One Models and Jev", 1,765 pts) — wrong pointer. Real Union Alpha HN thread found via Algolia: id 49728468 "New stealth model: Union Alpha" (by jlaneve, 13 pts, 3 comments, created 2026-09-16T15:24:16Z, links https://openrouter.ai/stealth/union-alpha).
- [t1] HN 49728468 comments: (a) olafura — "Wonder if it's a Gemini model because it was getting stuck on a rebase command because of vim being a non-interactive editor" + follow-up "It keeps on being weird" (behavioral tell, weak evidence); (b) animan — "First domestic model (Union?)" (speculation, no evidence). No benchmarks, no claim checks in HN thread.
- [t1] HN site-wide: only 1 comment hit for "Union Alpha" and it's a false positive (2013 Rebol regex comment). OpenRouter page = bare API ref: no description, no pricing, no context length, no modality statement; tool params present (tools/tool_choice) implying tool use; "failed generations are not billed".
- [t2] Reddit JSON API 403-blocked to our fetcher; old.reddit login-walled. Workaround: scoped WebSearch renders threads. RICHEST THREAD = r/singularity/comments/1wi03f6 "New stealth model: Union Alpha". Identity guesses harvested (see §IDENTITY below).
- [t2] r/singularity behavioral evidence: cutoff early 2026 ~Jan (ThePostMelone); answers Tiananmen questions → "western model, or no guardrails yet" — countered by Illustrious_Grade608 "Pretty sure ox alpha also did that, and it's a glm model"; heavily censored elsewhere (NSFW refusals); slow, high TTFT, frequent errors/retries → "guessing a larger rather than smaller model"; multi-step coding weak, isolated Rust/backend drafting fine; crowd ranking vs known models: "muse noticeably ahead, v4.1 ahead, union alpha around luna territory or a bit below depending on the task" (Luna = GPT-5.6 Luna).
- [t2] Companion opencode tweet found: status 2100237891263668418 (reply to @theemreates, 14:58 UTC) carries the ANTICIPATED PRICING as an image (pbs.twimg.com/media/HSWLOfjXYAAesBb.jpg?name=orig) — 70 quotes. Redditors read pricing off this image.
- [t2] Thread census so far: r/singularity 1wi03f6 · r/opencode 1wi046r + follow-up "Union Alpha Model thoughts?" · r/openrouter 1wi04ij · r/MistralAI 1wi1xng ("New stealthmodel on openrouter") + 1wi3aev "(European) Union Alpha". NO dedicated r/LocalLLaMA thread surfaced.
- [t2] BENCHMARK LEAD: r/MistralAI "(European) Union Alpha" claims "beats Kimi K3, GLM 5.3 and GPT 5.6 Sol xhigh on DeepSWE Pro" — provenance not yet confirmed (possibly opencode Zen leaderboard). Verifying next.
- [t3] HARD SPECS from OpenRouter public API (https://openrouter.ai/api/v1/models): id stealth/union-alpha · context_length 262,144 · max_completion_tokens 131,072 · pricing $0/$0 · modality text+image→text (input_modalities [text,image]) · tokenizer "Other" · is_moderated false · supported_parameters [max_tokens, response_format, temperature, tool_choice, tools, top_p] — NO reasoning param exposed · created 1789569723.
- [t3] OrcaRouter forensics piece (orcarouter.ai/blog/union-alpha-leak, Sep 16): listing appeared 14:42 UTC Sep 16; provider field "Stealth"; no HuggingFace repo/license/param count/arch note; knowledge-cutoff field EMPTY; single endpoint no failover; "frontier-level performance" is operator-written, unreproduced. CRITICAL: **no benchmark, leaderboard entry, or third-party number for Union Alpha exists yet** per OrcaRouter; "Union" breaks the stealth animal-codename convention (Pony, Ox, Owl, Hunter, Elephant) → possibly a different operator than prior drops, or spec trimmed to avoid fingerprinting. "Union = consortium" has no evidence.
- [t3] CLAIM CHECK (no-training): OrcaRouter — Union Alpha has **no data terms at all** ("no data-processing agreement, no stated retention period, no jurisdiction and no one to escalate to"). The "no data training" promise lives ONLY in opencode's tweet, not in any enforceable policy. Contrast: Ox Alpha "retained prompts and completions at the provider". IMAGE SUPPORT: verified only at the API-metadata level (text+image→text modality); no independent functional test surfaced yet.
- [t3] PRECEDENT LEDGER (reported, not lab-confirmed, per OrcaRouter): Quasar/Optimus Alpha → OpenAI GPT-4.1 previews · Sonoma Sky/Dusk → xAI Grok 4 Fast · Pony Alpha → Zhipu GLM-5 · Hunter Alpha → Xiaomi MiMo-V2-Pro · Owl Alpha → Meituan LongCat-2.0 · Ox Alpha → Zhipu GLM-5.3-Flash (revealed 6 days after appearing; OrcaRouter predicts Union resolves in ~5-7 days). Ox Alpha lesson: ~99%-confident testers named the RIGHT LAB but WRONG MODEL; forensics came from tokenizer counts, video encoder, API error formats.
- [t3] Prior Ox Alpha "80% DeepSWE / beats GPT-5.6 Sol" claim = one dev passing 8/10 on a subset — not the real benchmark (self-serving inflation precedent).
- [t3] @nummanali tweet says "Union Alpha, a stealth model WE just launched... Works in every harness. $ ori ..." → launcher-affiliated promo; its DeepSWE/Index claims are SELF-SERVING pending the actual numbers.
- [t4] @unionalphaai account pulled via fxtwitter: bio "Free. Stealth. Zero data retention. Feedback welcome." — joined 2026-09-10 11:12 UTC (SIX DAYS BEFORE the opencode tweet), verified type "individual", 10 tweets, 2,027 followers. NOTE: bio claims zero RETENTION; opencode tweet claims no TRAINING — two different promises; OrcaRouter found no enforceable terms for either.
- [t4] r/SillyTavernAI has a Union Alpha model thread (NSFW-censorship crowd); r/MistralAI "Speculations on Union Alpha" (1wi5vgg) is a 3rd Mistral-side thread. Thread sizes: r/opencode 253↑/106c · r/openrouter 171-261↑/66-111c · r/singularity largest.
- [t4] X quote-tweet sample (of 423): mostly amplification/jokes — TestingCatalog (repost + GPT-6 Sol rumor context), Wes Bos "sketchers already distilling the union alpha model" quoting Stolinski "everyone is guessing...", Rohan Paul (3D-scene render test), filicroval (~764 likes), gaganghotra_, alexatallah (OpenRouter co-founder: "a stealth model we just launched"), nummanali (promo). Identity guesses on X are THINNER than Reddit's; the guessing-game mood dominates over forensic claims.
- [t5] Precedent timelines nailed (see §PRECEDENT). Alex Atallah "we just launched" phrasing → nummanali likely OpenRouter-affiliated, confirming SELF-SERVING flag on all launcher-side numbers. DeepSWE Pro: no independent leaderboard found anywhere — the r/MistralAI-cited stat traces back to operator graphics only.
- [t5] Search rate-limit hit once (-429); all claims below sourced before cutoff. Sweep complete — writing deliverable sections.

---

## §IDENTITY — who the crowd thinks trained it (ranked by independent voices)

**Ground truth available to anyone:** OpenRouter listing — "developed and operated by a third-party provider who has chosen to remain anonymous during this preview." Nobody has confirmed anything as of 2026-09-16 ~20:00 UTC (T+5h from launch).

| # | Guess | Voices (independent) | Evidence cited | Evidence quality |
|---|---|---|---|---|
| 1 | **Zhipu / GLM (Z.ai), maybe "GLM 5.5"** | r/singularity: csjfkma ("I'm guessing GLM again"), FlunkyGraphics ("if Ox Alpha, Omen Alpha and Union Alpha are GLM models, this would be crazy"), Sinogolarity ("Might be GLM 5.5"), Illustrious_Grade608 | Behavioral: answers Tiananmen questions yet is heavily censored elsewhere (NSFW refusals) — pattern matching Ox Alpha (= GLM-5.3-Flash) exactly; continuity bias from Ox Alpha's reveal | **WEAK-MIXED.** Vibes + inertia. Counter-evidence in-thread: 256K ctx is "weird for GLM"; OrcaRouter notes "Union" breaks Zhipu's animal-codename series (Pony/Ox/Owl/Hunter/Elephant). Ox Alpha lesson looms: right lab, wrong model is the classic failure mode |
| 2 | **OpenAI — GPT-6 Luna or GPT-6 Sol** | r/singularity: Sockand2 ("GPT-6 Luna"), rollfaster ("Cost would be much lower. Maybe gpt 6 sol?"), peakedtooearly ("GPT-6 Sol. We know it's coming very soon") | Rumor-timing: GPT-6 Sol leaks say imminent; 256K ctx fits OpenAI's sub-1M house style; lower-cost tier implied; Horizon precedent (OpenAI invented the free stealth-preview playbook: Quasar/Optimus/Horizon) | **MODERATE-circumstantial.** Naming convention actually supports it: "X Alpha" is OpenAI's codename grammar (Quasar Alpha, Optimus Alpha, Horizon Alpha) — no animal. No tokenizer/style forensics published by anyone |
| 3 | **Mistral / "European Union Alpha"** | r/MistralAI threads ×3 (1wi1xng, 1wi3aev, 1wi5vgg); bunny_warrior69 ("It's Mistral I tell you it's Mistral this time. Europe is back, baby.") | Pun ("Alpha in the (European) Union") + the "beats Kimi K3, GLM 5.3, GPT-5.6 Sol xhigh on DeepSWE Pro" stat + hope | **WEAK.** Wordplay + motivated reasoning; the DeepSWE Pro stat traces to operator-side promo graphics, not a third party; pun proves nothing (would also be trivially deniable) |

Also on the board (single voices): DeepSeek 4.1 Pro (AppealSame4367, "most obviously", zero evidence) · "Chinese model or Grok" (ObiWanCanownme) · **Gemini** — the ONLY HN guess (olafura, vim/non-interactive-editor rebase hang as the tell — behavioral, weak, n=1) · Meta Hy4 pre-release (HeavySink3303) · joke tier: "Geppe-T ASI Win-XP-98" (r/opencode).

**Meta-observation:** the guess distribution is driven mostly by WHICH SUBREDDIT you're in (r/MistralAI says Mistral, GLM-adjacent users say GLM, GPT-6-rumor followers say Sol). Venue-corrected, there is NO true majority — the honest consensus is "a big lab running the standard stealth playbook, identity unresolved."

## §BENCHMARKS — external eval intel (5 best, graded)

**OrcaRouter's flat statement, T+5h: "Union Alpha: none. No benchmark, leaderboard entry, or third-party number exists."** Everything numeric below is operator-side or crowd-impression. Graded accordingly:

1. **Launcher-side DeepSWE Pro claim** — "beats Kimi K3, GLM 5.3 and GPT 5.6 Sol xhigh on DeepSWE Pro" (cited in r/MistralAI 1wi3aev; source = operator graphics; echoed by @nummanali "Here's the DeepSWE result for Union Alpha, a stealth model we just launched"). **SELF-SERVING — high confidence**: phrasing "we just launched" + no independent DeepSWE Pro leaderboard found + zero methodology.
2. **Launcher-side AA Intelligence Index claim** — @nummanali: "behind only Claude Fable 5.1 and Claude Opus 5" on the (Artificial) Analysis Intelligence Index. **SELF-SERVING — high confidence**; Artificial Analysis has no public Union Alpha entry surfaced by any search.
3. **Launcher-side Terminal-Bench v4.0 "internal ~50%"** (Facebook-circulated repost of operator material). **SELF-SERVING**; "internal" = unauditable.
4. **Crowd blind ranking vs known models** (r/singularity, multiple testers): "muse noticeably ahead, v4.1 ahead, union alpha around luna territory or a bit below depending on the task" (GPT-5.6 Luna, DeepSeek v4.1, Muse Spark as anchors). **NOT self-serving, but anecdotal** — the closest thing to an independent eval that exists.
5. **LinkedIn hype datum** — (st-scottsun-inireland): results "mog both OpenAI and Anthropic". **UNQUANTIFIED HYPE** — zero numbers, recorded only to show the rumor floor.

Cautionary precedent on operator numbers: Ox Alpha's "80% DeepSWE" was one dev passing 8/10 tasks on a subset (OrcaRouter). Discount accordingly. Note also: LinkedIn/x post said "a stealth model WE just launched" appears in BOTH OpenRouter-co-founder and promo accounts' mouths — the "third-party provider" is at minimum deeply co-marketed with OpenRouter/opencode Zen.

## §CLAIM CHECKS

- **"no data training":** UNVERIFIED / effectively UNVERIFIABLE. The promise exists ONLY in the opencode tweet; the @unionalphaai bio upgrades it to "Zero data retention" (a different claim); the actual listing carries **no data terms at all** — "no data-processing agreement, no stated retention period, no jurisdiction and no one to escalate to" (OrcaRouter). Contrast: Ox Alpha retained prompts+completions at the provider while free. Nobody has disputed the promise either — there's simply nothing to check it against. Treat as marketing-grade until a named provider inherits it.
- **"supports images":** VERIFIED at the metadata level (OpenRouter API: modality text+image→text, input_modalities [text,image]) and one functional crowd test (@rohanpaul_ai 3D-scene rendering). No independent quality eval exists.
- **"built for agentic coding":** partially corroborated — tools/tool_choice exposed on the API; crowd UX: fine for isolated backend/Rust drafting, weak on multi-step "build it and actually finish it"; slow TTFT, frequent errors/retries (provider overload day one — OpenRouter "getting hammered"). No reasoning parameter exposed; knowledge-cutoff field empty; tokenizer filed as "Other".

## §PRECEDENT — stealth-model reveal pattern and timing

| Model | Appeared | Revealed as | Gap |
|---|---|---|---|
| gpt2-chatbot (LMSYS) | 2024-04-28/29 | OpenAI GPT-4o (self-leaked system prompt May 8 as "im-also-a-good-gpt-chatbot") | ~15 days to official launch |
| Quasar Alpha / Optimus Alpha | Apr 2025 | OpenAI GPT-4.1 (announced Apr 14) | Optimus IDed ~4 days after listing |
| Horizon Alpha / Beta | 2025-07-30 → retired ~08-07 (2 days after gpt-oss shipped) | never officially confirmed; community ties to gpt-oss/GPT-5 family — **community memory itself is contested** | ~1 week window |
| Sonoma Sky / Dusk | 2025 | xAI Grok 4 Fast | days-to-fortnight |
| Pony Alpha | 2025/26 | Zhipu GLM-5 | — |
| Hunter Alpha | 2026 | Xiaomi MiMo-V2-Pro | — |
| Owl Alpha | 2026 | Meituan LongCat-2.0 | — |
| Ox Alpha | Aug 2026 | Zhipu GLM-5.3-Flash | **6 days** |

Pattern: free anonymous preview → 1-2 week window → retirement coincides with the official launch event; reveal lands AT launch, not before. Census (Digital Applied): identity revealed "inside a fortnight" in 6 of 7 cases. Ox Alpha lesson: ~99%-confident testers named the right lab and the wrong model; the actual cracks came from tokenizer counts, video-encoder behavior, and API error formats. OrcaRouter's prediction for Union Alpha: resolves in ~5-7 days. Union Alpha appeared 14:42 UTC Sep 16; the free window ends ~Sep 23.

## §DELIVERABLES (per mission contract)

**Consensus ranking — top 3 identity guesses:**
1. **GLM/Zhipu (Z.ai), possibly GLM 5.5** — most voices, behavioral-vibe evidence (guardrail pattern matches Ox Alpha) — evidence quality WEAK-MIXED (context-window and codename-convention counters).
2. **OpenAI GPT-6 Sol/Luna** — rumor-timing + "X Alpha" naming grammar fits OpenAI's own Quasar/Optimus/Horizon series — evidence quality MODERATE-circumstantial.
3. **Mistral / European** — venue-driven (r/MistralAI ×3) + pun + operator stat — evidence quality WEAK (wordplay + self-serving benchmark).
Caveat: venue-corrected, no true majority exists; naming-forensics lean OpenAI, behavioral vibes lean GLM.

**5 best external eval numbers:** (1) launcher DeepSWE Pro "beats Kimi K3 / GLM 5.3 / GPT-5.6 Sol xhigh" — SELF-SERVING; (2) launcher AA-Index "behind only Claude Fable 5.1 and Claude Opus 5" — SELF-SERVING; (3) launcher internal Terminal-Bench v4.0 ~50% — SELF-SERVING; (4) crowd blind ranking "around GPT-5.6 Luna territory or a bit below" — anecdotal, best independent signal; (5) LinkedIn "mogs OpenAI and Anthropic" — unquantified hype. NO third-party eval exists as of T+5h. Anchor points for context: GLM-5.3-Flash AA Index 57; GLM 5.3 45/75 vs GPT-5.6 Sol 47/77 (AA Intelligence/Coding).

**What the crowd does NOT know that our instrumented battery adds (U2/U4 tie-in):**
- **Timing instrumentation:** crowd has only "slow, high TTFT, retries" vibes. Our U4 battery quantifies it (88-170s for 2K-char outputs) — running Union Alpha through the identical harness yields comparable tokens/sec, TTFT, retry counts, and timeout profile. Nobody else is measuring this.
- **Polarity inversion probe (U2):** crowd reports "struggles with multi-step" but nobody tested whether verdicts and evidence diverge — our polarity-inversion finding (verdict cells flipping relative to the evidence lines they cite) is exactly the fingerprint class that survives rebranding. If Union Alpha shows the same verdict/evidence polarity inversion and honest-citation signature as another model, that's a transferable style fingerprint the crowd hasn't thought to look for.
- **Citation honesty:** no crowd member has audited whether Union Alpha's citations are real. Our honest-citations metric (from U2/U4) applied here gives a falsifiable, model-comparable number.
- **Tokenizer/error-format forensics:** the exact tools that cracked Ox Alpha (tokenizer counts, API error formats) are unpublished for Union Alpha ("Other" tokenizer on the listing) — our instrumented runs log raw token counts and error shapes, which would directly feed the identity question within the free window.
- **Guardrail polarity map:** crowd anecdotes only (Tiananmen yes, NSFW no). A systematic sensitive-topic × refusal matrix is cheap for us and would grade evidence quality on guess #1.

---
*Sweep window: 2026-09-16 ~14:42-20:00 UTC. Sources: api.fxtwitter.com (seed 2100236430890991782, companion 2100237891263668418, @unionalphaai), openrouter.ai/api/v1/models, openrouter.ai/stealth/union-alpha, news.ycombinator.com item 49728468 (+ Algolia), reddit r/singularity 1wi03f6 · r/opencode 1wi046r · r/openrouter 1wi04ij · r/MistralAI 1wi1xng/1wi3aev/1wi5vgg · r/SillyTavernAI, orcarouter.ai/blog/union-alpha-leak, simonwillison.net (gpt2-chatbot), opencode.ai/data, x.com voices (@alexatallah @nummanali @testingcatalog @rohanpaul_ai @wesbos @stolinski @filicroval @gaganghotra_). No git operations. No paid APIs.*
