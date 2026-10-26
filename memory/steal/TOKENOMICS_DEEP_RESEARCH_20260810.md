# TOKENOMICS DEEP RESEARCH — the 50× lever is already built; here's what's left
**Date:** 2026-08-10 · **Researcher:** ghost · extends TOKENOMICS_CACHE_DEEP_DIVE_20260810.md

## 1. DeepSeek rates CONFIRMED + a warning
api-docs.deepseek.com (live):
```
deepseek-v4-flash: hit $0.0028/M · miss $0.14/M · out $0.28/M   (50×)
deepseek-v4-pro:   hit $0.003625/M · miss $0.435/M · out $0.87/M (120×)
```
⚠️ **DeepSeek explicitly warns: "We plan to raise the overall pricing for DeepSeek API services in
the near future, with a significant increase expected."** → cache discipline becomes MORE urgent, not
less. The 50× hit/miss is the single biggest controllable cost.
Feature note: **"Chat Prefix Completion (Beta)"** — a way to warm/complete a prefix explicitly; a
potential under-used lever for pinning the cache.

## 2. SELF-STEAL: the 50× lever is ALREADY BUILT — mag/invariant.py
`invariant.py` ("make the session prefix STABLE RELIABLY") implements the exact cache-preservation
mechanism the deep dive proposed:
  - SEPARATE: byte-stable prefix (SESSION_SEED.md + formatting block) vs VOLATILE tail (learned +
    model_hint + ask), split by the fixed `<<<STABLE-INVARIANT-END>>>` delimiter → cache hits on the
    prefix, only the tail is a fresh miss.
  - PIN: spec_gate.freeze(SEED) + verkle-anchor the prefix sha (provable/auditable).
  - VERIFY: `check()` before every session that the prefix bytes still match the pinned sha; if
    drifted, DON'T ship drifted bytes — re-freeze or escalate.
So "under-explored avenue #1" (cache-prefix discipline) is NOT unexplored — it exists. The 50× region
is already minimized by keeping the prefix frozen. **Good news for cost; the real gaps are elsewhere.**

## 3. Cross-provider prompt-cache landscape (for cache-aware routing)
- DeepSeek: automatic PREFIX cache, 50× hit/miss, time-windowed (~minutes), no explicit control.
- Anthropic: EXPLICIT prompt caching via `cache_control` breakpoints, TTL 5m/1h, ~90% off cached input.
- OpenAI: automatic prefix caching, ~50% off cached input, transparent.
Implication: **routing should be cache-aware PER PROVIDER** — DeepSeek rewards a frozen prefix most
(50×) but has the shortest implicit window; Anthropic lets you pin explicit breakpoints with longer
TTL; OpenAI is automatic. A cache-preservation router picks the provider by which one best tolerates
the operator's edit pattern at that moment.

## 4. What is ACTUALLY left (the refined gap list)
1. **Interrupt-aware routing** (the real gap): detect WHERE the operator edited (edit position) →
   if mid-context (would invalidate the frozen prefix), defer/debounce the DeepSeek call or route the
   volatile tail to a cheap/free tier. invariant.py keeps the prefix stable, but nothing yet decides
   WHEN to pay 50× vs route the tail away.
2. **Free-tier interleave for the volatile tail**: after an invalidating edit, run the re-derived
   region on ollama / grok_free / free tier — never at the 50× miss rate.
3. **Cost-fold on edit position**: extend queue_learn/cost_learn to fold (edit_position, provider,
   cache_effect) → the router learns which providers tolerate mid-context edits cheaply.
4. **Cache-waste bucketing → action**: cache_map already maps cache-waste onto verkle themes; make it
   feed the router (route cache-wasteful themes to free).
5. **Chat Prefix Completion**: investigate using DeepSeek's beta to warm/pin the prefix deterministically.

## 5. Recommendation
Build the **interrupt-aware cache-preservation router** that CONSUMES invariant.py (stable prefix) +
cache_map (waste) + behavioral_analytics (edit pattern): it decides, per turn, whether to call
DeepSeek at full cache-hit economics or route the volatile tail to a cheap/free tier based on the
operator's edit position — then proves the 50× region shrinks on real provider_usage.jsonl.

## Folds
Filed to memory/steal/. The lever is 80% built (invariant.py); the remaining 20% is the behavioral
router that decides WHEN to pay 50×. Repo memory: /memories/repo/tokenomics-cache-deep-dive.md.
