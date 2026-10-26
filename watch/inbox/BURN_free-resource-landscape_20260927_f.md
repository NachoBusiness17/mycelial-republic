# BURN free-resource-landscape 20260927_f: LLM7 census + keyless probe

## Verdict

steal

## Evidence

- Census, byte-backed: GET https://api.llm7.io/v1/models returned HTTP 200 (2026-09-27). Total 64 models. Families by prefix: gpt 8, claude 15 (8 as anthropic/claude + 7 bare), gemini 6, deepseek 4, glm 3, kimi 3, mistral 3 plus codestral 1, grok 2, llama-family 2 (llama-4-maverick, l3), media/generative remainder (seedance 3, inkling 2, voxtral 2, kling 2, whisper 2, gpt-image 2, chroma, dark, gemma4:31b, jev, minimax, seed).
- Tier split: turbo 5, pro 59. Turbo roster: DeepSeek-V4-Flash-0731, GLM-5.3-Flash, codestral-latest, minimax-m2.7, mistral-Nemo-Instruct-2407. All five carry usage_based_only false; all 59 pro rows carry usage_based_only true. No zero-priced rows; cheapest is codestral-latest at 0.01 in / 0.02 out per 1M.
- Frontier-shaped ids present: gpt-6-astra, gpt-5.6-sol/terra/luna, claude-opus-5-5, claude-sonnet-5, gemini-3.8-flash-high, grok-4.6, kimi-k3, deepseek-v4-pro, glm-5.3, mistral-large-3:675b. Provenance unverified: the list reads as a proxy/alias catalog, model authenticity owed.
- Probe, byte-backed: POST https://api.llm7.io/v1/chat/completions, model codestral-latest, max_tokens 5, no Authorization header. HTTP 200, choices[0].message.content was "ok", usage 9 prompt / 2 completion tokens, service_tier "standard". Free tier is inference-usable keyless.
- Rate shape, search-surfaced only: llm7.io text via WebSearch states "anonymous access up to 500,000 tokens/day with" no key or signup, and a free token from token.llm7.io raises limits while reaching the same turbo models. My direct fetch of llm7.io returned only the tagline (SPA shell), so the 500K/day figure is owed byte confirmation.

## Steal or Vacuous

LLM7 enters the freelane burn rotation as the keyless lane: anonymous, no signup, OpenAI-shaped schema, live inference confirmed on turbo tier. Fleet fit: scout and janitor-class grind, cheap drafts, dedupe-caption-class work; not specialist inference. Everything frontier-shaped sits in pro tier behind usage_based_only true, which the keyless probe did not test, so treat turbo's 5 models as the whole freelane until a probe proves otherwise. Assume the 500K tok/day anonymous cap until byte-verified; the lane is a burst lane, not a residency. Companion facts: it is one of the six lanes from the free-claude-code drop (LINKS row, scout_drop receipt), and it is the first of the six to come back HOT after Chutes, SiliconFlow, and Scaleway died and Lightning AI owed tier data.

## Falsifier

Pre-registered: if a follow-up probe completes keyless on a pro-tier (usage_based_only true) model, widen the rotation row; if measured anonymous burn lands far below 500K tok/day, correct the cap; if the same probe starts returning 401, retire the lane and refile.

## Bibliography

- https://api.llm7.io/v1/models (fetched 2026-09-27, HTTP 200, byte-backed)
- https://api.llm7.io/v1/chat/completions (keyless probe 2026-09-27, HTTP 200, byte-backed)
- https://llm7.io/ (fetched 2026-09-27, tagline only, SPA shell)
- WebSearch summaries 2026-09-27 quoting llm7.io limits text; github.com/mnfst/awesome-free-llm-apis; wotai.co/blog/best-free-llm-apis (not opened, search summary only)
