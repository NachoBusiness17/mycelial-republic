# VAST TEMPLATE V3 — current-practice (vast-native vLLM, 2026-09-01)

> **Provenance:** built from CURRENT sources per operator directive ("read the manual, look
> at how others do it"): docs.vast.ai/vllm-llm-inference-and-serving + vLLM official docs.
> Supersedes V1 (phantom image) and V2 (August ollama recipe evaluated: sovereignty rules
> and tunnel patterns remain sound; the ollama serving layer is superseded by vast-native
> vLLM with prefix caching + OpenAI-compat). No sacred cows: the August recipe was the best
> interpretation of its time; this is the current one.

## The vast-native pattern (how it's actually done)
1. **Image:** `vastai/vllm:@vastai-automatic-tag` (vast's official vLLM image — the
   `:latest` tag does NOT exist; that phantom caused 5 boot failures) or `vllm/vllm-openai:latest`.
2. **Config via ENV VARS, not onstart scripts:** `VLLM_MODEL` (HF repo), `VLLM_ARGS`
   (e.g. `--max-model-len 16384 --enable-prefix-caching`), optional `HF_TOKEN`.
   The template auto-runs `vllm serve` on boot. No fragile onstart line-continuations.
3. **Port 8000** (vLLM default) — map it, don't fight it.
4. **Endpoint auth:** `Authorization: Bearer <token>` (instance env / OPEN_BUTTON token).
5. **Search API:** JSON q with operators eq/gte/lte; price key `dph_total`; compute_cap
   decimal; AWQ needs cc ≥ 7.5 (V100 7.0 fails — filter cc ≥ 8.6 or use fp16).

## Dogfood ladder (each rung verified before the next — the 16:42 law)
1. search (read-only) ✓ verified: 64 offers, 3090s from $0.069/hr
2. rent with env-var config + poll /v1/models ✓ pattern per vast docs
3. cache probe (9k prefix ×2, latency delta + cached_tokens)
4. weight-bearing task (digest-fold patch, verified locally)
5. destroy + proof

## GPU ladder (3090 24GB verified available at $0.069-0.11/hr)
7B AWQ first (pipe proof) → 32B AWQ (~19GB, fits 24GB) → larger only via multi-GPU.

## Sovereignty rules retained from August (still correct)
Verkle tip / agent_state / private DNA never on vast disk. Access via port map or tunnel.
The node is hot inference only.

## E8 note (the actual prize)
With the template: farm-build runs become one PUT + env vars + a poll — the temporal
authority meters the WHEN (rent only during build windows), the meter rows carry
cached_tokens per call, and the whole session costs cents.
