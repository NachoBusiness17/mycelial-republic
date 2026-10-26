# WORK w-muse-spark-access

lane: openrouter model: meta/muse-glimmer-30b
ts: 2026-10-01T03:00:25.937709+00:00
finish: stop cached_tokens: 38
ask: OpenRouter meta/muse-spark-1.3 and 1.2 return 403 on free keys. Research: what is the muse-spark access model? Is it a contributor program (like muse-glimmer-contributor), a paid tier, or region-locked? How do we get access? Check OpenRouter docs, Discord, model page.

---

(1) FINDING
I could not verify the current access model for OpenRouter meta/muse-spark-1.3 and 1.2, including whether it is a contributor program, paid tier, or region-locked, and the specific reason for 403 errors on free keys. No verifiable source was retrieved in this session.

(2) STEALABLE idea worth keeping
If access is gated, treat model availability as a feature flag problem: maintain a fallback model map per model family and auto-fallback on 403/401 to the nearest public equivalent, with logging of gate reason codes.

(3) TESTABLE hypothesis
OpenRouter meta/muse-spark-1.3 and 1.2 require an allowlist / contributor tier and return 403 for free-tier keys, not for region lock.

(4) EVIDENCE or OWED
OWED. No OpenRouter docs, Discord posts, or model page content were accessed or cited in this session.
