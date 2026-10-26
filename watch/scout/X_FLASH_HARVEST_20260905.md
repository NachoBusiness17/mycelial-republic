# X HARVEST — 5.3-FLASH NEWS — 2026-09-05 ($0, search + api.fxtwitter doors)

**Scope:** today's 5.3-flash timeline news, operator-ordered. Roots pulled verbatim via api.fxtwitter (x.com hard-walled). Web layer cross-receipted (docs.z.ai, unsloth, HF, Reddit).

## THE ROOTS (verbatim where quoted)

1. **@theo (t3.gg, 385K followers), Aug 27:** "Updated list with glm-5.3-flash! It's so good that I had to move other things around. Incredible model." — 4,248 likes / **613,620 views**, quoting his 4.0M-view Aug 22 tier list. CONSENSUS-PRICED: the timeline has adopted flash.
2. **@Adidotdev, Aug 26 release day:** "It's release day — Ox Alpha is officially GLM-5.3-Flash" — 320B-A18B MoE, native multimodal (text/image/video), 1M ctx, **MIT license**, $0.15/$0.50 API ($0.03 cached). Benchmarks: **Terminal-Bench 2.1 = 84.3 vs Opus 4.8's 85.0**, DeepSWE 63.4, AutomationBench 48.8 (up from 5.2's 26.2). Preview ran on domestic chips.
3. **@Zai_org announcement** (2092616204787626030): weights + local-run commitment "later today/early tomorrow" of release.
4. **Unsloth wave (Sep 3–5):** official GGUF repo (dynamic quants — **3-bit on 128GB RAM, 1-bit on ~100GB**), special llama.cpp PR REQUIRED (support not upstream), Unsloth Desktop runs it. Guide: unsloth.ai/docs/models/glm-5.3-flash.
5. **r/LocalLLaMA field test:** Unsloth Q4_XS + llama.cpp PR on **M2 Ultra: works; TTFT 3–4 MIN** (prompt processing is the Apple-Silicon bottleneck). Generation varies 40–130+ tok/s by quant/bandwidth.
6. **Sep 5 vendor layer:** @louszbd quota-doubling post (carded separately, watch/INTAKE_LOUSZBD_FLASH_QUOTA_20260905.md); 4 concurrent flash events retweeted by @Zai_org.
7. **Community:** Agentic Index 5th, "tying GPT-5.6-Sol," "runs on $8,000 of hardware at faster than API speeds" (@krunkosaurus, Sep 3). GMI Cloud: "the stealth model that became the talk of the timeline."

## FLEET HITS (the parts that move decisions)

- **ROCINANTE DAY-ONE RECIPE EXISTS, PINNED BY OTHERS:** Unsloth dynamic quants + their llama.cpp PR; 128GB unified = practical floor, Q4_XS field-tested. Our 68.7GB box CANNOT host even 1-bit (~100GB floor) — genuinely Rocinante-gated. UZU card's probe target gains a sibling: GLM-5.3-Flash GGUF day-one probe (tok/s AND TTFT).
- **OUR PRIMARY LANE IS MIT WEIGHTS:** the model this seat rides all week can be owned outright Oct 27 — the "own almost everything, rent frontier for judgment" doctrine has a concrete date and recipe.
- **HONEST NUMBER FOR PROJECTIONS:** TTFT 3–4 min on M2 Ultra (prompt-processing-bound). Interactive local = no; batch/long-horizon local = yes. Probe card must gate on BOTH numbers.
- **NO ANTIREZ POST FOUND** (search-level negative; his Sep 3 Q2/Q4 benchmark tweets from our 09-05 morning pass stand as the antirez receipt).

## DOORS/TRAJECTORY

Search (web_search_prime, $0) → x.com roots → api.fxtwitter verbatim pulls. Total burn: $0, 4 calls. Pro-deck enumeration door not needed today.
