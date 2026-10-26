# BURN free-resource-landscape 2026-09-27 d

## Verdict

green

## Evidence

- Chutes catalog, curl unauthenticated `https://api.chutes.ai/chutes/`: HTTP 200, 146,593 bytes, 0.87s. Body opens `{"total":491,"page":0,"limit":25,"items":[{"chute_id":"42ee92ba...","name":"google/gemma-4-31B-turbo-TEE",...,"public":true,...}]}`. 491 chutes total, 25 on page 0. Recon-only: this is the public catalog, no inference performed.
- Chutes models endpoint, curl unauthenticated `https://api.chutes.ai/v1/models`: HTTP 404, 146 bytes. No OpenAI-style models listing without auth.
- Lightning AI docs, curl -L `https://lightning.ai/docs/overview`: HTTP 200, 17,642 bytes, 0.31s. Title tag begins "Overview" and ends "Lightning AI". Page body is a JS app shell; grep for serverless, API key, free credits, LitServe, Pods returned zero matches.
- Lightning AI status, curl unauthenticated `https://api.lightning.ai/status`: HTTP 200, 17,699 bytes, but body is an HTML SPA shell (`<!doctype html>`, MonacoEnvironment bootstrap). Not a machine-readable status document.
- Env var names (names only, no values printed): no LIGHTNING and no CHUTES variable in this shell, so per probe rules no key-authenticated Lightning call was made. Lightning API tier state is unverifiable from this seat: owed.
- Chutes free-tier retirement, curl `https://chutes.ai/news/community-announcement-february`: HTTP 200, 107,044 bytes. Verbatim: "200 daily request quota will remain available for all non-TEE models until March 15" followed by "fully retired." Announcement dated February 27, 2026.
- WebSearch on the Chutes lane: chutes.ai "From Volume to Value" reports removal of roughly 10B tokens/day of the 200-requests-per-day free quota used by about 11,000 users. Snippet-grade, captured via search-tool text only.

## Steal or Vacuous

No steal. Chutes is confirmed dead as a freelane: the 200 rpd free tier was retired March 15, 2026, and what remains open unauthenticated is the 491-chute catalog, same recon-only class as the Featherless pass (22,032 models, no inference). Chutes moves from probeable-gap to recon-only/dead in the ledger; a funded key would make it a paid tier, not a free window, so no hammering. Lightning AI stays owed: both reachable URLs returned SPA shells with no tier, quota, or status payload, and no key env exists in this shell to run the sanctioned models-list probe. Fleet canon after this pass: hot freelanes remain OpenRouter funded (1000 rpd) and Groq cached-token RPDs from prior passes today; recon-only shelves gain Chutes (491 chutes); dead: SiliconFlow (401), Chutes freelane (retired); owed: Lightning AI (keyless-unverifiable), LLM7, Scaleway. Receipt closes the last two probeable gaps named at dispatch.

## Bibliography

- https://api.chutes.ai/chutes/ (curl HTTP 200, catalog JSON)
- https://api.chutes.ai/v1/models (curl HTTP 404)
- https://lightning.ai/docs/overview (curl HTTP 200, SPA shell)
- https://api.lightning.ai/status (curl HTTP 200, SPA shell)
- https://chutes.ai/news/community-announcement-february (curl HTTP 200, retirement quotes)
- WebSearch result text citing https://chutes.ai/news/from-volume-to-value-building-a-sustainable-ai-inference-platform-2 (snippet-grade)
