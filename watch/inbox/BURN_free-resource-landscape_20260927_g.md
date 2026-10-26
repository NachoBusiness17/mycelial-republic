# BURN free-resource-landscape 20260927_g: LLM7 authenticity A/B

## Verdict

steal

## Evidence

- A/B byte-match 1, prompt "Which model are you? Answer with your exact model id only.": LLM7 keyless codestral-latest returned HTTP 200 (0.817s), content "llama-3.1-8b-instant", usage 16 prompt / 12 completion / 28 total, model field echoes "codestral-latest". Official https://api.mistral.ai/v1/chat/completions, same id, keyed: HTTP 200 (1.140s), content "llama-3.1-8b-instant", usage identical 16/12/28. Response id shapes differ: LLM7 "chatcmpl_" hex prefix, Mistral plain hex.
- Controls on api.mistral.ai: catalog with key returns "codestral-2508", "owned_by":"mistralai", aliases ["codestral-latest","mistral-code-latest","mistral-code-fim-latest"]; no key HTTP 401 {"detail":"Invalid API Key"}; bad key HTTP 401 same. Endpoint genuine, no interception in path.
- A/B byte-match 2, prompt "In one short sentence: what model are you and who trained you?": both endpoints HTTP 200, both content "I'm a model from Mistral AI and was trained by Mistral AI on a variety of publicly available datasets.", usage identical 17/24/41, created timestamps 1790518155 vs 1790518156 (one second apart).
- Churn vs f-pass: live /v1/models (HTTP 200, 64 ids) now flags DeepSeek-V4-Flash-0731 usage_based_only true; f-pass recorded all five turbo rows false. Keyless 401 "Missing API key" reproduced on it. Keyless-usable set is now GLM-5.3-Flash and codestral-latest only.
- Saturation: mistral-Nemo-Instruct-2407 HTTP 429 x3, minimax-m2.7 HTTP 429 x1, GLM-5.3-Flash timeout x2 plus 429 x1, all "Too many concurrent requests for this client. Retry after 10 seconds.", code concurrent_request_limit_exceeded.
- Web search: thin. llm7 self-describes as a gateway to "leading AI models from various providers"; third parties route through its anonymous tier as a backend. Nothing per-model on alias vs real.

## Steal or Vacuous

codestral-latest on LLM7 is a real backend. Two independent temperature-0 prompts produced byte-identical prose and identical token counts on both endpoints within one second; two different checkpoints cannot do that. The "llama-3.1-8b-instant" string is Codestral itself hallucinating a modal API id when asked for an id with no system context (genuine Mistral emitted the identical string), not evidence of a Llama swap. Fleet adoption: LLM7 codestral-latest stays in the freelane burn rotation as the byte-verified vendor-backed id; authenticity is per-id and does not transfer. Frontier-shaped pro ids (gpt-6-astra, claude-opus-5-5, grok-4.6, kimi-k3) stay unverified: usage_based_only true blocks keyless probes (401 reproduced), so they are owed until a keyed A/B. GLM-5.3-Flash, Nemo, minimax unverifiable this pass (timeouts, concurrency wall) = owed. The anonymous lane is concurrency-walled today; treat it as burst-only.

## Falsifier

Pre-registered: if a keyed A/B on any pro id returns mismatched output for the same temperature-0 prompt, that id is marked alias and dropped from rotation; if codestral-latest stops matching official Mistral byte-for-byte on the two archived prompts, re-probe and demote on one mismatch.

## Bibliography

- https://api.llm7.io/v1/models (fetched 2026-09-27, HTTP 200)
- https://api.llm7.io/v1/chat/completions (probes 2026-09-27, HTTP 200/429/401 as quoted)
- https://api.mistral.ai/v1/models and /v1/chat/completions (keyed A/B plus no-key and bad-key controls 2026-09-27, HTTP 200/401)
- WebSearch 2026-09-27 summaries: docs.llm7.io, ayautomate.com (not opened)
