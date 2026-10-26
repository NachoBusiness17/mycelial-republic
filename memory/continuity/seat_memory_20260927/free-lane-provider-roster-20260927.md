---
name: free-lane-provider-roster-20260927
description: 9/27 free-lane provider health roster — groq gpt-oss-120b fat lane
  (1K RPM), 8/16 keys alive, cerebras/nvidia/gemini/mistral dead with named
  causes
metadata:
  node_type: memory
  type: reference
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Free-lane provider health roster from B2-04 probe + B2-03 endpoint news + B2-114 groq decision, all byte-verified 9/26-27.

**Alive (burning):**
- groq gpt-oss-120b: 1K req/min, 200K TPM, fattest free denominator ever measured
- openrouter k1/k2 (stealth/space-bunny-alpha): limit null, usage $4.61/$0.74
- nous (Hermes): alive, 822 tokens burned
- together (DeepSeek-V4-Flash-0731): trial, alive
- cohere (command-r-plus-08-2024): trial, alive

**Dead (cause named from live response bodies):**
- cerebras: 402 Payment Required (card-gated trial, $5/30 days, operator parked it)
- nvidia: 410 Gone + 404 "Function not found for account" (roster purged for this key)
- gemini: /models 200 but generateContent 401 (AQ.* key is Vertex express, not AI Studio; fix = AIza key or enable aiplatform)
- mistral: 429 x-ratelimit-limit-req-minute: 0 (literally zero quota)

**Key structural findings:**
- groq limits are PER MODEL not per account: a third chat lane adds its own 1K RPD bucket
- cerebras card-gate: $5 credits expire in 30 days, 5 RPM / 90K TPM / 1M TPD, 2-model catalog, operator parked it
- stale Groq denominator corrected: 14.4K RPD was wrong, real is 1K RPD / 200K TPD
- cached tokens bypass Groq limits (official on-doc)

**Cerebras community dig (B2-142) fleet-fit verdict:** short-context batch pattern (B2-04: 6,890 tokens/day) fits trial shapes easily (5 RPM / 30K uncached TPM / 1M TPD / 1M TPH) and dodges community kill-patterns ($5 gone in 10 min on agentic loops, 50K-context agent loops die in ~2 calls). But fleet's 97.3% prefix-cache engine earns ZERO on Cerebras (no cached-input discount, cache billed at standard rate). GO = scheduled 30-day batch sprint, never routing-list add. Dormant stays correct until operator card GO (P0 Oct 3).

**9/27 scoreboard rot (B2-106):** provider health scores go stale within hours — morning run read mistral DORMANT (post-surgery) not the morning's 403, cerebras DORMANT not 402. Wired as weekly MAG_PROBE_REMOTE=1 cadence in improve scout (provider_probe_due gate, 7-day cadence knob in configs/improve.yaml). First live run: 11 deduped probes over 28 providers in 16.1s, mlx-cluster tcp timeout, ollama docker-name locality trap, xai DOWN 400 all caught fresh.

**Receipt:** watch/inbox/PROVIDER_HEALTH_20260926.md + B2_04_probe.py (rerunnable falsifier)

**9/27 free-resource-landscape burn adds (BURN_free-resource-landscape_20260927_b, verdict steal):** hammer list = DeepSeek off-peak half-price window + OpenRouter funded lanes (1000 req/day each; 18-lane math holds) + Groq 1K RPD/model with cached-token denominators. Churn verdict: sponsored freelanes are EXPIRE-DATED WINDOWS not tiers (Cerebras card-gated 30-day trial confirmed; MiniMax 14-day window reportedly closed; Tabnine reportedly preview — snippet-grade, pages unread). Owed: 6 unprobed lanes (Featherless/Chutes/SiliconFlow/LLM7/Scaleway/Lightning AI), NVIDIA + Gemini login-gated denominators, providers.yaml Groq id surgery. Link promotion must ride `python -m mag.link_library add` per B2-06 (hand-appends caused 5 silent dupes).

**9/27 probe results settled the 6 owed lanes (passes c/d/e/f):**
- LLM7 CONFIRMED LIVE KEYLESS INFERENCE (chat probe HTTP 200, content returned, no auth header): 64-model catalog; turbo tier of 5 anonymous-usable = codestral-latest, GLM-5.3-Flash, DeepSeek-V4-Flash-0731, minimax-m2.7, mistral-Nemo; all 59 frontier-shaped pro rows gated usage_based_only true; anonymous cap ~500K tok/day search-surfaced NOT byte-confirmed. Enters burn rotation as BURST lane, not residency.
- LLM7 AUTHENTICITY CLOSED PER-ID (pass g, keyed A/B): codestral-latest proven a REAL backend by byte-identical responses vs official Mistral API on two temp-0 prompts (usage + prose matched within 1s); keyless lane churned to 2 of 64 ids (codestral-latest + GLM-5.3-Flash; DeepSeek-V4-Flash-0731 flipped usage_based_only true = 401 keyless) and was 429-concurrency-walled that day; frontier pro ids (gpt-6-astra, claude-opus-5-5, grok-4.6, kimi-k3) stay owed until a keyed A/B. Law: authenticity is PER-ID, not transferable — one real id proves nothing about its 63 neighbors.
- Featherless: keyless /v1/models HTTP 200 — RECON lane upgraded to CHURN-TELEMETRY by pass h (BURN_free-resource-landscape_20260927_h): nightly roster-diff CONFIRMED BUILDABLE via the UNDOCUMENTED ?sort=-created_at (newest-first verified live, first row created same day); 22,044 models each carrying unix created/model_class/context_length/pricing; pagination activates an envelope (current_page/per_page 100-clamp/total_items 50,586 total_pages 506 = paged route sees a superset of the default dump); a 422 error body enumerates the full sort enum; count drifts within minutes (22,044 vs 22,035 sorted, unresolved). Falsifier: two consecutive zero-new-rows nights while the full dump advances, or keyless 200 turning 401/403, kills the diff build and reverts Featherless to recon-only.
- Chutes: DEAD (catalog 200 with 491 chutes but /v1/models 404; 200 rpd freelane "fully retired" Mar 15 2026, primary-sourced).
- SiliconFlow 401 dead-until-key; Scaleway 401 dead unauthenticated (docs 404); Lightning AI = SPA shells, tier data still owed.
