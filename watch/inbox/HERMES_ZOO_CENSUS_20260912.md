# HERMES ZOO CENSUS + RIGHTSIZING MAP v0 (2026-09-12)

Operator question: "we have access to hundreds of models in hermes why arent we rightsizing them?"
Answer at the bytes: the zoo was armed 09-07 (390 models, both keys verified 200) and never
probed — rightsizing needs a registry, and the organ table (the registry) is the known missing
build (L06, dozen-wide fold). Meanwhile every dispatch rode one default. This card is the
census + the tier map + the routing amendment.

## THE CENSUS (probed 2026-09-12, HERMES_API_KEY_1, names only)

**403 models, 47 families, 7 free.** Raw: memory/runs/hermes_zoo/census_raw.json.

Families by width: openai 97 · qwen 53 · google 36 · anthropic 27 (opus through **opus-5**,
sonnet through **sonnet-5**) · mistralai 25 · z-ai 20 · deepseek 18 (incl.
**deepseek-v4-flash-vision-exp** and v4-pro) · moonshotai 9 · minimax 7 · bytedance-seed 6 ·
x-ai 6 · amazon 5 · meta 10 · **embedding families: sentence-transformers 5, voyageai 5,
intfloat 3** · nvidia 4 · poolside 4 · thinkingmachines 4 · sakana 3 · stepfun 3 · tencent 3 ·
long tail 20+.

**Variant suffixes already in the catalog:** `:batch` (deferred-tier variants exist for opus,
sonnet, deepseek and others) · `:US` (regional) · `:free` (7: ling-3.0-flash-fin/sante,
longcat-2.0, laguna-s/xs-2.1, step-3.7-flash, solar-pro4).

PRICING: UNPROVEN — model ids carry no prices; per-family price probe is the next census pass.
No routing decision may assume a number (W7 law: measured Pareto, not assumed tiers).

## WHY WE WEREN'T RIGHTSIZING (the honest finding)

1. **The fence predates the arsenal.** `lanes.yaml` (08-14): hermes `not_router: true,
   Residual never` — written before the Nous arming (09-07) and before the organ-table
   doctrine. It fences hermes-as-DEFAULT-router, not the catalog.
2. **The organ table doesn't exist.** No registry, no classifier at dispatch seams — every
   lane routes by habit and key availability (L06, dozen-wide, 09-12).
3. **The zoo probe was staged and never run.** ractor_dna.yaml: "v0 pin; v1: probe hermes
   zoo per voice" — v1 never happened. 74 dispatches since 09-07, all on the default.
4. **No demand model.** Chair 5's finding stands: supply-side routing with no demand meter
   optimizes a question nobody asked. Tier map below is a HYPOTHESIS until the task-suite
   probes run (n≥40/model, W7 honest-tier spec).

## THE TIER MAP v0 (hypothesis rows for the organ table — each row needs its probe)

| request class | zoo rows (cheapest-sufficient first) | note |
|---|---|---|
| bulk | `:free` 7 · deepseek-v4-flash(:batch) · z-ai glm rows · qwen flash rows | $0 first, batch tier second, Lite lane unchanged |
| research | deepseek-v4-pro · sonnet-5(:batch) · gemini-3 family · qwen big rows | batch suffix = the T4 batch-tier build item, already live in catalog |
| advisory | sonnet-5 · opus-4.x · gpt-5 family | mid-tier; probe before trusting |
| judgment (seal-grade) | opus-5 · opus-4.8 · gpt-5 flagship | metered against the $220 S:D budget, receipted per dispatch |
| senses (vision) | deepseek-v4-flash-vision-exp · gemini vision rows · qwen-vl rows | needs the vision probe before any claim |
| embeddings (engram) | voyageai · intfloat · sentence-transformers | corpus-engram v0's encoder choice lives HERE — the zoo supplies the embedder |

## THE ROUTING AMENDMENT (respects the fence, needs nothing flipped)

- z.ai glm-5.3-flash stays the hermes default lane (`not_router` fence untouched — the zoo
  enters as organ-table ROWS, not as the default).
- The classifier (6 classes) picks the row; every zoo dispatch rides the existing
  hermes_steering receipt (memory/runs/hermes_dispatch_log.jsonl) — metering is already built.
- Spend rules already sanctioned 09-07: $220 S:D = fleet work budget, $10 Nacho = petty +
  free-lane probes. Zoo tier probes ride Nacho/:free until a class earns the metered tier.
- Falsifier for the map: each row must beat or match the default lane on its class's task
  suite at lower realized cost, n≥40, before it replaces the default in production routing.
  A row that can't show the delta dies.

## NEXT (in order, on the standing order)

1. Per-family price probe (models endpoint metadata or one-token calls) — pricing UNPROVEN.
2. Class probes: bulk row vs default on a fixed 40-task suite (rides :free/$0).
3. Wire rows into the organ table v1 registry when it lands (the L06 build).
4. Vision + embedding probes (senses class + engram encoder pick).
