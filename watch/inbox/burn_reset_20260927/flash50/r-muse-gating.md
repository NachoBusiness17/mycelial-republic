# r-muse-gating: OpenRouter muse-spark 403 recon (2026-09-28)

## Verdict first

The 403 is NOT a contributor-tier membership gate and NOT a paywall. All four
`meta/muse-spark-*` slugs (1.2, 1.3, and both `-contributor` variants) are served by a
single Meta-direct endpoint and sit behind OpenRouter's provider attestation gate. The
blocker on a fresh/standard key is one missing attestation: **18+ age confirmation**,
done at https://openrouter.ai/settings/preferences. That is the entire "access program"
as reachable from OpenRouter's side.

## What was run and what it returned

### 1. Catalog check (primary)

    curl -s https://openrouter.ai/api/v1/models -o or_models.json

Muse family in the live catalog (6 ids):

- `meta/muse-glimmer-30b`
- `meta/muse-spark-1.1`
- `meta/muse-spark-1.2`
- `meta/muse-spark-1.2-contributor`
- `meta/muse-spark-1.3`
- `meta/muse-spark-1.3-contributor`

Pricing from the same catalog (USD per token):

| model | prompt | completion | cache read |
|---|---|---|---|
| muse-spark-1.1 / 1.2 / 1.3 (standard) | 0.00000125 ($1.25/M) | 0.00000425 ($4.25/M) | 0.00000015 ($0.15/M) |
| muse-spark-1.2-contributor | 0.0000001 ($0.10/M) | 0.0000002 ($0.20/M) | 0.000000002 ($0.002/M) |
| muse-spark-1.3-contributor | 0.0000001 ($0.10/M) | 0.0000002 ($0.20/M) | 0.000000002 ($0.002/M) |
| muse-glimmer-30b | 0.0000003 ($0.30/M) | 0.0000012 ($1.20/M) | 0.00000004 ($0.04/M) |

Contributor tier = 12.5x cheaper input, 21.25x cheaper output, 75x cheaper cache read
than the standard slugs. All are PAID models; there is no free spark slug.

### 2. Live probes (repo key from .env, this session, max_tokens 16)

Command shape:

    curl -X POST https://openrouter.ai/api/v1/chat/completions \
      -H "Authorization: Bearer $OPENROUTER_API_KEY" \
      -d '{"model":"<slug>","max_tokens":16,"messages":[{"role":"user","content":"Say OK"}]}'

Results:

- `meta/muse-spark-1.3` → HTTP 403:
  `{"error":{"message":"This model requires you to complete the following before use:
  18+ age confirmation. Confirm at https://openrouter.ai/settings/preferences.","code":403,
  "metadata":{"missing_attestation_types":["age_18plus"],
  "routing_funnel":[{"step":"Initial Endpoints","endpoint_count":1}],
  "failed_routing_step":"Gate Endpoints with Attestations"}}}`
- `meta/muse-spark-1.3-contributor` → HTTP 403, identical message and metadata.
- `meta/muse-spark-1.2` → HTTP 403, identical message and metadata.
- `meta/muse-spark-1.2-contributor` → HTTP 403, identical message and metadata.
- `meta/muse-glimmer-30b` → HTTP 200, served by DeepInfra (real completion returned,
  cost $0.0000366).

The ask's premise is verified byte-exactly, and the 403 body names the exact fix.

### 3. Why glimmer works but spark does not (endpoint topology)

    curl -s https://openrouter.ai/api/v1/models/meta/<slug>/endpoints

- muse-spark-1.3: exactly ONE endpoint, provider `Meta` (baseUrl `https://api.meta.ai/v1`).
- muse-spark-1.2 / 1.2-contributor / 1.3-contributor: same, single Meta-direct endpoint each.
- muse-glimmer-30b: open-weight ("dense, open-weight multimodal model from Meta
  Superintelligence Labs, distilled from Muse Spark"), served by many providers
  (Phala, DeepInfra, ...) with no Meta attestation required.

Glimmer works on a stock key because it routes to non-Meta hosts. Spark cannot route
around Meta's own endpoint, so the Meta endpoint's requirements bind: from the
muse-spark-1.3-contributor page JSON (fetched page HTML, ms13c.html):

- `moderationRequired: true`
- `requiredAttestationTypes: ["age_18plus"]`
- `requiresUserIDs: true`
- Meta provider TOS: `https://ai.developer.meta.com/legal/terms-of-service`

### 4. The contributor tier: what it is and its terms

It is a pricing-for-data tier, not a separate qualification program. From the
OpenRouter model page FAQ (openrouter.ai/meta/muse-spark-1.3-contributor, quoted):

- Q: What is Muse Spark 1.3 Contributor?
  A: "Muse Spark 1.3 Contributor is the cost-efficient contributor tier of Meta's
  multimodal reasoning model for experimentation, learning, and early-stage agentic,
  multi-agent, and coding workflows. It is designed to track information across
  extended tasks, work through conflicting inputs, and request clarification or
  confirmation when needed. Prompts and outputs may be used to improve Meta's products."
- Q: How much does it cost?
  A: "$0.10/M input tokens and $0.20/M output tokens, with separate rates for Cache
  Read at $0.002/M tokens and Web Search at $2.50/1K calls."
- Released September 2, 2026 (permaslug `meta/muse-spark-1.3-contributor-20260902`).
  Muse Spark 1.2 Contributor permaslug is `-20260805`.

Data policy difference, from the provider JSON embedded in the same page:

- contributor endpoints: `data_policy.training: true` (Meta may train on your
  prompts/outputs), `retainsPrompts: true`, `retentionDays: 30`, `canPublish: false`,
  `trainingOpenRouter: false` (OpenRouter itself does not train on it).
- standard endpoints: same shape but `data_policy.training: false`.

So the trade is: ~12-21x cheaper tokens in exchange for Meta's training use of
prompts and outputs. Standard tier costs full price and Meta's recorded policy for it
on OpenRouter is training:false, 30-day prompt retention either way.

### 5. How to qualify (the actual steps on OpenRouter)

1. Confirm 18+ age attestation at https://openrouter.ai/settings/preferences (this is
   what the 403 names; `missing_attestation_types: ["age_18plus"]`).
2. Hold credits: all spark slugs are paid (no `:free` variant exists). After the
   attestation a zero-credit key gets 402 insufficient-credits, not 403.
3. Pick the slug: `meta/muse-spark-1.3-contributor` or `meta/muse-spark-1.2-contributor`
   for the cheap tier (accepting the training-on-prompts data policy), or the standard
   slugs at $1.25/$4.25 per M. There is no separate signup, application, or approval
   step anywhere on OpenRouter's side; OpenRouter's docs index
   (https://openrouter.ai/docs/llms.txt, grepped) has no attestation page at all, the
   gate surfaces only via the 403 body and the settings UI.

## OWED (not verifiable this session, do not trust until checked)

1. Meta's own contributor program terms in full: `ai.developer.meta.com/legal/terms-of-service`
   is a JS-rendered app; plain curl returned a Facebook error shell and WebFetch got
   only the string "Model API". Whether the contributor tier requires a separate
   Meta-side agreement acceptance (beyond the OpenRouter data-policy choice) is OWED.
2. Whether Meta runs any qualification outside OpenRouter (developer-account tiers,
   application, region limits) for direct `api.meta.ai/v1` access: no reachable primary
   page found; OWED.
3. The framing that Meta's 18+ attestation stems from prior Llama license terms
   (13+/18+ requirements): search backend rate-limited during this ask; OWED.
4. muse-spark-1.1 was not probed live (ask scoped 1.2/1.3); its catalog entry shows the
   same standard pricing and it presumably shares the gate, but that is inference, not
   a run check.
5. Web search during this ask was degraded (the backend returned 429 errors and one
   secondary hit on vecbase.com claiming an account/permissions/balance requirement);
   the vecbase claim was not corroborated by any primary source and is discarded here.

## Receipts

- Catalog + endpoints + probes: commands and outputs above, run 2026-09-28 with the
  repo's `.env` OPENROUTER_API_KEY (values redacted in this file).
- Contributor page JSON/FAQ: https://openrouter.ai/meta/muse-spark-1.3-contributor
  (curl, 529,106 bytes HTML, extracted embedded RSC payload).
- Model ids and pricing: https://openrouter.ai/api/v1/models (751,967 bytes).
