## 3. THE CACHE (implicit, automatic)

- No API parameters for cache control
- Response field: `usage.prompt_tokens_details.cached_tokens`
- Cache hits: ~50% of standard input price
- Cache: implicit based on content similarity (not byte-exact, but identical = highest hit)
- Best practices: stable system prompts, long docs in system message, append-don't-rewrite history
- TTL: undocumented ("reasonable time limits")
- **FLEET FINDING**: 4.7-flash (thinking off) caches at 99%. 5.3-flash (thinking always on) did NOT cache on our test. Hypothesis: thinking generates variable reasoning tokens that break similarity matching.
- **OVERTURNED 08-29 (EXP-A, mag/_exp_a_cache_retrigger.py): 5.3-flash DOES cache — 99.52% hit (7040/7074) on a byte-stable ~7K prefix with thinking on; novel-prefix same-size controls: 0%.** The 08-26 miss was prefix instability, not thinking. Cache mining doctrine extends to the judgment lane: frozen prefix + append-only turns + max_tokens>=1536.
