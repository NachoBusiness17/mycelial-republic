# WORK w-muse-spark-access

lane: openrouter model: inclusionai/ling-3.0-flash-sante:free
ts: 2026-10-01T02:54:48.916494+00:00
finish: stop cached_tokens: 0
ask: OpenRouter meta/muse-spark-1.3 and 1.2 return 403 on free keys. Research: what is the muse-spark access model? Is it a contributor program (like muse-glimmer-contributor), a paid tier, or region-locked? How do we get access? Check OpenRouter docs, Discord, model page.

---

FINDING: meta/muse-spark-1.3 and 1.2 return 403 on free OpenRouter keys. Whether the block is from contributor gating, paid tier, or region lock is unverified.

STEALABLE: Hit the same endpoint with a paid or contributor OpenRouter key to see if the 403 clears; if it does, the model is gated and free keys cannot use it.

TESTABLE hypothesis: A request to meta/muse-spark-1.3 with a valid contributor token will return HTTP 200 instead of 403.

EVIDENCE or OWED: OWED. I could not verify muse-spark access rules from OpenRouter docs, Discord, or the model page. No sources exist in my training.
