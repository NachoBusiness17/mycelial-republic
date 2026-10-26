# FAST SEARCH STATIC KEY PROBE — 2026-09-25

**VERDICT: NO.** `HERMES_API_KEY_1` does NOT expose Perplexity Fast Search via `inference-api.nousresearch.com`, and no `/search`-style route of any kind is reachable on the static-key surface. The free Fast Search endpoint (if it exists) rides Nous Portal tiers behind OAuth, which the fleet already knows is an operator hand (see `GO_LIST_EXECUTION_20260925.md` P2: "hermes proxy path blocked on Portal OAuth login"). Closes the OWED probe at `watch/inbox/GO_LIST_EXECUTION_20260925.md:24`.

## Setup

- Key: `HERMES_API_KEY_1` from `.env:47` (40 chars, `sk-n***` prefix). Value never printed; probe script reads it directly.
- Base: `https://inference-api.nousresearch.com/v1` (as wired in `mag/free_tier.py:86-94`, the `nous` lane).
- Probe script: `_probe_nous_search.py` (repo root), run with `.venv/Scripts/python.exe`. Budget honored: **5 HTTP probe calls total, ~$0.001 spend** (probe 4 reported its own cost: $0.0005496; probes 1-3 are 404/free; probe 5 hit the token cap at 100).

## Evidence per attempt (chronological, exact commands)

1. **GET `/v1/models` -> 200 OK.** 418 models returned. Regex sweep of catalog ids for `search|sonar|perplexity|pplx` matched exactly three:
   - `perplexity/pplx-embed-v1-4b`
   - `perplexity/pplx-embed-v1-0.6b`
   - `relace/relace-search`
   No Sonar chat models, no `sonar`/`sonar-pro`/`fast-search` style model anywhere in the catalog. The two `pplx-embed` models are embeddings, not search. Sample of catalog (first 20 ids): `perceptron/perceptron-mk1.5`, `fireworks/ember-1`, `z-ai/glm-5.3-prime`, `qwen/qwen3.8-max-prime`, `stealth/space-bunny-alpha`, `aion-labs/aion-3.5-mini`, `aion-labs/aion-3.5`, `upstage/solar-mini4`, `cohere/command-a-plus`, `openai/gpt-6-luna-pro(:batch)`, `openai/gpt-6-luna(:batch)`, `openai/gpt-6-sol-pro(:batch)`, `openai/gpt-6-sol(:batch)`, `anthropic/claude-opus-5.5(:batch)`, `xiaomi/mimo-v2.6-pro-ultraspeed`.

2. **POST `/v1/search` with `{"query": "what day is it in Perth right now"}` -> 404 Not Found.** No standalone search route.

3. **POST `/v1/tools/search` with the same body -> 404 Not Found.** No tools-scoped search route.

4. **POST `/v1/chat/completions` (`z-ai/glm-5.3-prime`) declaring a `web_search` function tool -> 200 OK, but NO server-side search.** Model id `gen-1790381436-hHpKHBsytLEn0do9EN1X`, `finish_reason: stop`, content `"I have a web search tool available."`, zero `tool_calls` in the response, `reasoning_tokens: 0`. That sentence is the LLM role-playing the declared tool, not the platform executing one; no `web_search_options`-style field exists in the response schema. Not evidence of a search capability.

5. **POST `/v1/chat/completions` (`relace/relace-search`, the only search-named model in the catalog) -> 200 OK, and the model itself disclaims web access.** `system_fingerprint: vllm-0.26.0-75b21d46` (plain vLLM host, no search middleware). Content begins: `"I can't browse the web or access real-time information..."`. So `relace-search` is an LLM for agentic codebase search, not a web-search route. It does not back Perplexity Fast Search.

## Corroborating docs check (free, no API spend)

Web search for Nous inference API documentation surfaced only OpenAI-compatible `/v1/chat/completions` usage; no `/search` endpoint documented anywhere in results. Sources:
- [NousResearch/Nous-Hermes-2-Mixtral-8x7B-SFT (Hugging Face)](https://huggingface.co/NousResearch/Nous-Hermes-2-Mixtral-8x7B-SFT)
- [Hermes Agent Skill docs (github.com)](https://github.com)

This is corroboration only; the verdict rests on the five live probes above.

## Not run / limits

- `HERMES_API_KEY_2` was not probed: key 1 authenticated cleanly (probes 1, 4, 5 all 200), so a second key on the same lane adds nothing.
- Portal-tier surface (browser OAuth at nousresearch.com) was NOT probed, per standing law: Portal login is an operator hand, blocked since 09-23 (`GO_LIST_EXECUTION_20260925.md` P2). If the operator ever logs into the Portal, that is where a Fast Search toggle would live, not on these static keys.

## Downstream

- `mag/free_tier.py:93-94` lane note should drop "search endpoint not yet probed" (now probed: negative). Not patched by this seat; leaving the lane-file edit to the caller-wiring seat named in the same OWED line.
- Fleet web-search remap for the Sonar sunset (`GO_LIST_EXECUTION_20260925.md` P0) gets no help from this lane: the `nous` lane remains chat-completions-only for research chores.
