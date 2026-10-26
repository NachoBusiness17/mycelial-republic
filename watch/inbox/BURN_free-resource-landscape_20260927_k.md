## Verdict

steal

## Evidence

- Census, byte-backed: GET https://api.llm7.io/v1/models returned HTTP 200 (2026-09-27). Total 64 models. A top-level `tier` field splits 5 turbo / 59 pro, matching pass f. Marker drift found: `usage_based_only` is true on 60 rows and false on exactly 4, all four inside turbo. Pass f recorded "All five carry usage_based_only false"; today DeepSeek-V4-Flash-0731 carries usage_based_only true. No pro row reads false.
- Free-class roster after census (usage_based_only false, keyless candidate class): GLM-5.3-Flash, codestral-latest, minimax-m2.7, mistral-Nemo-Instruct-2407.
- Probes, byte-backed, POST https://api.llm7.io/v1/chat/completions, no Authorization header, max_tokens 5, prompt "reply ok": minimax-m2.7 HTTP 200, 40 prompt / 64 completion tokens (max_tokens not enforced as a hard stop, reasoning-style spill), service_tier null. mistral-Nemo-Instruct-2407 HTTP 200, content "Hello! How can I", 6 prompt / 5 completion tokens, service_tier "default". Probes this pass: 2, cap 3 respected.
- Schema note: the gate marker is a top-level field, not under metadata; parse corrected here. Cross count: turbo-false 4, turbo-true 1, pro-true 59.

## Steal or Vacuous

The turbo tier of 5 is now fully pinned. Four ids are probe-verified keyless across both passes: codestral-latest and GLM-5.3-Flash (pass f), minimax-m2.7 and mistral-Nemo-Instruct-2407 (this pass). The fifth, DeepSeek-V4-Flash-0731, flipped to the gated class (usage_based_only true) since pass f and leaves the freelane. The LLM7 burn-rotation keyless row is therefore 4 ids, not 5: GLM-5.3-Flash, codestral-latest, minimax-m2.7, mistral-Nemo-Instruct-2407, all hammerable now for scout and janitor-class grind. Burn hazard: on minimax-m2.7 a 5-token ask returned 64 completion tokens, so per-call token caps are not trustworthy on that id; it is the spill-prone member of the lane. Catalog churn is live: roster and gate flags moved within one day, so the freelane census is a snapshot; re-pull /v1/models before each wave. Web search thin, stated honestly: no dedicated 2026 turbo-tier lineup page surfaced, only search-summary mentions that LLM7.io remains a live free tier alongside Kluster AI and Hugging Face; nothing there contradicts the byte-backed census.

## Bibliography

- https://api.llm7.io/v1/models (fetched 2026-09-27, HTTP 200, byte-backed)
- https://api.llm7.io/v1/chat/completions (keyless probes 2026-09-27, HTTP 200 x2, byte-backed)
- watch/inbox/BURN_free-resource-landscape_20260927_f.md (read 2026-09-27)
- watch/inbox/LINKS.jsonl (tail -30, read 2026-09-27)
- WebSearch 2026-09-27, summaries only: Reddit mention (LLM7.io live free tier), docs.usecoeus.com tracker (not opened)
