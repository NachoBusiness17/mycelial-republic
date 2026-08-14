# TOKENOMICS DEEP DIVE — the price of your interrupt, and under-explored cache levers
**Date:** 2026-08-10 · **Researcher:** ghost · **Grounded in:** cache_map.py, invariant.py,
renderman.py (COHERENCE STRATEGY), cost_learn.py, task_router.py, queue_learn.py, behavioral_analytics.py

## The one number that matters: 50×
DeepSeek caches by PREFIX. Verified-from-billing rates (cache_map.MODEL_RATES):
```
deepseek-v4-flash: input hit $0.0028/M · input miss $0.14/M · output $0.28/M  → 50× hit/miss
deepseek-v4-pro:   input hit $0.003625/M · miss $0.435/M · out $0.87/M      → 120× hit/miss
```
So the difference between a call that reuses the cache and one that doesn't is 50–120× on input.

## What happens to your DeepSeek price when you interrupt/adjust in VS Code
- The conversation/prompt **prefix** is what's cached (automatic, prefix-based, time-windowed).
- **You type/edit mid-context** → the prefix AFTER the first changed token becomes a **cache-miss**
  → that whole region re-bills at the 50× miss rate.
- **You edit early** (reorder, tweak an early file, add an early instruction) → nearly the whole
  context invalidates → a massive spike (e.g. 1M cached input tokens: $0.028 if hit, $1.40 if miss).
- **You edit late** (append the newest turn) → the earlier stable prefix STAYS cached (hits), only
  the tail re-derives → cheap. Position of the edit IS the cost.
- **You idle** between edits → DeepSeek's cache entry expires (minutes-ish window) → the next call is
  a full miss even with an identical prefix.
- **Every small adjustment compounds**: each interrupt that invalidates a big prefix re-pays the
  50× on the invalidated region. This is the hidden tax on "adjusting in the VS Code window."

## Should the terminal be stateless + learn behavioral routing? YES — and we have the parts
- **Stateless terminal**: the VS Code window should be a STATELESS CLIENT that emits immutable,
  content-addressed artifacts (knots) instead of holding one mutable shared prefix. Then an
  "interrupt" doesn't mutate a shared cache-prefix — each turn is a fresh hermetic artifact that
  SHARES the stable frozen prefix (system + invariant block) and only appends the delta. This is the
  stateless + versioning doctrine (schema_registry hermetic commit) applied to the token stream.
- **Behavioral routing**: behavioral_analytics (minute behavioral signals) + cache_map (which themes
  waste cache) + cost_learn/queue_learn (fold (shape, provider) cost) already exist. Extend to learn
  the OPERATOR's edit pattern: when you're mid-edit / likely to interrupt, route the volatile call
  to a cache-agnostic cheap path (local ollama, free frontends) and only pay DeepSeek's 50× when the
  prefix has stabilized.

## Under-explored tokenomics avenues (the deep dive)
1. **Cache-PREFIX discipline (the biggest 50× lever, barely exploited).** Order context so the STABLE
   prefix (system prompt + invariants + constants) is frozen and never changes → ALWAYS cache-hit;
   only the volatile tail changes. renderman.py's COHERENCE STRATEGY + invariant.py point at this but
   it's not wired as a router policy.
2. **Interrupt-aware routing.** Detect edit POSITION. Mid-context edit → debounce/defer the DeepSeek
   call until the prefix stabilizes, or route to a non-prefix-cached cheap provider. Don't burn 50×.
3. **Free-tier interleave for the volatile tail.** After an invalidating edit, the re-derived region
   is the expensive part → run it on local ollama / grok_free / deepseek free so the invalidated
   region is never paid at full rate.
4. **Frozen cache-preamble artifact.** Persist ONE immutable preamble (hermetic, versioned) that every
   call references; edits never touch it → the largest possible cache-hit surface.
5. **Cost-fold on edit position.** Extend queue_learn to fold (edit_position, provider) outcome+cost
   so the router learns which providers tolerate mid-context edits cheaply and routes accordingly.
6. **Session bucketization for waste.** cache_map already maps cache-waste onto verkle theme graph →
   route the cache-wasteful themes to cheaper/free paths.
7. **Keep the free tricks.** grok_free (grok.com browser), deepseek free tier, browser frontends, local
   ollama = the $0 leg. The goal is to make DeepSeek's 50× region as small as possible by keeping the
   cached prefix frozen and the volatile tail free.

## The framing
The operator is already "doing all this for free using our tricks." The remaining tax is the **50×
cache-miss on interrupts** — the one place we pay full price. The lever isn't a new model; it's
**prefix discipline + interrupt-aware routing + stateless turns**, reusing what we already built
(cache_map, renderman COHERENCE, cost_learn, behavioral_analytics, stateless versioning).

## Folds
Filed to memory/steal/. Highest-value next build: a cache-preservation router that (a) freezes a
stable preamble, (b) detects edit position, (c) routes volatile calls to cheap/free tiers — proving
the 50× region shrinks on real provider_usage.jsonl.
