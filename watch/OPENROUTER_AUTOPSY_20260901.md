# OPENROUTER AUTOPSY — 2026-09-01

## Root cause: FREE TIER IS GONE (slug/auth, not outage)

Single probe to known-good free slug `meta-llama/llama-3.3-70b-instruct:free`:

- HTTP **404**
- Body: `"This model is unavailable for free. The paid version is available now - use this slug instead: meta-llama/llama-3.3-70b-instruct"`
- `user_id` returned in error → **key auth SHAPE IS VALID** (no 401/403)
- No rate-limit headers (404 short-circuits)

The 20 failures in lineage_genC were all `gemma-4-26b-a4b-it:free` → same class:
**PROVIDER RETURNED ERROR = 404, model not on free tier.** Not wrong slug (slug correct, tier gone), not outage (endpoint up, key authenticated), not auth shape (user resolved).

## Evidence chain
1. `lineage_genC` receipt: 20/20 failed "Provider returned error", http-ok 0 — matches 404-turned-error by harness.
2. Fresh probe: 404 + "unavailable for free" + user_id → proves key works, tier doesn't.
3. Root: OpenRouter free models are off/deprecated serverside for these slugs (availability churn).

## Does ladder-A stand ($10 top-up → 1000 RPD free fleet)?
**NO — as structured.** A $10 credit does NOT unlock the `:free` tier; free-tier availability is provider-side (`:free` slugs return 404 regardless of balance). The ledger reads "free fleet" — that specific assumption is dead.

## Path forward
- **Ladder-A-A′ (revised):** keep the $10 top-up but target **paid** slugs at `:free`-adjacent rates, or rely on credits with cost capping per request (OpenRouter gives ~$10 → hundreds of paid calls at small models, not 1000 RPD free).
- **Ladder-B:** swap to a provider with a real free tier (e.g. Groq, Cerebras, GitHub Models) and re-run lineage against a slug known live RIGHT NOW (verify before batch).
- Do NOT re-run the OpenRouter free-lane batch until a paid slug is confirmed live with one probe.

Verdict: cause = free-tier removal; ladder-A "$10 = free 1000 RPD" does not stand; path = A′ (paid slug + caps) or provider B.

## CORRECTION 07:30Z (operator funded key2, re-verified through fixed lens)
- **Auth-header bug found in shared probe pattern**: works on z.ai, not OpenRouter (needs strict `Bearer`). All earlier OR probes (S1 lane "down", part of this autopsy's evidence) ran through the broken header. Lens, not fleet.
- Validated via GET /api/v1/key with `Bearer`: **key1 valid** ($4.105 lifetime), **key2 valid** ($11 funded 06:58Z, no cap), paid gen gpt-oss-120b 200 OK @ $0.0000035.
- **Free-slug verdict UPHELD on honest evidence**: `:free` slugs 404 "unavailable for free" through the working header. Ladder-A stays dead; A′ (paid slugs + caps) is LIVE and now funded.
- OpenRouter battery lane re-run authorized: paid slugs on key2, cap ≤$0.02, receipt → lineage_genC_openrouter2_20260901.md.
