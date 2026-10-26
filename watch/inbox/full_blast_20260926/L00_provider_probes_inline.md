# L00: six-provider liveness probes (inline, seat-run)

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 · **Class:** RECEIPT / scout probe
**Method:** curl HTTP status probes, landing page + /v1/models at root and api. subdomain, 10-15s timeouts, no auth, no keys. Follow-up catalog fetches where open. Lane L11 (background) is closing terms/quotas; this file is the byte-level edge check.

## Results

| Provider | Landing | API edge | Reading |
|---|---|---|---|
| featherless.ai | 200 | api.featherless.ai/v1/models = **200 OPEN** | catalog fetchable unauthenticated |
| chutes.ai | 200 | api.chutes.ai/v1/models = 404; /api/v1/models = 502 | alive landing, API path shape unknown/auth-gated |
| siliconflow.com | 308 (www move) | api.siliconflow.com/v1/models = **401** | alive, auth required |
| llm7.io | 200 | api.llm7.io/v1/models = **200 OPEN** | catalog fetchable unauthenticated |
| scaleway.com | 301 | api.scaleway.com/v1/models = **401** | alive, auth required (generative API may live at api.scaleway.ai, unverified) |
| lightning.ai | 200 | lightning.ai/v1/models = **401** | alive, auth required (may be GPU-credits not inference, L11 checks) |

## Open-catalog intel (fetched byte samples)

- **LLM7:** model list includes `DeepSeek-V4-Flash-0731`, 400K context, tier "turbo", $0.02/M input and $0.04/M output, tools + reasoning + JSON mode + streaming. That is a serious lane candidate regardless of free tier: DeepSeek V4 Flash at 2 cents in.
- **Featherless:** RWKV-family catalog (`recursal/EagleX_1-7T`, rwkv5-7b class), 16K context, $0.10/M in and $0.20/M out pricing fields, `is_gated: false`. Niche: non-transformer architectures, cheap background lanes.

## Verdicts (edge tier; terms tier owned by L11)

All six ALIVE at the edge. PROBE-next tier: LLM7 (open catalog + V4-Flash pricing), Featherless (open catalog, niche arch). WAIT tier: Chutes (endpoint shape unknown), SiliconFlow, Scaleway, Lightning (auth required, terms pending L11). No lane decisions taken at this seat; this feeds providers.yaml only through the operator-gated promote path.
