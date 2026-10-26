# SPACE BUNNY BURN — the x3 stealth lane + the standing burn doctrine

**2026-09-24 · GO: operator ("full blast on all our free stealth lanes ... use all of this reliably, consistently, wide and deep")**

---

## THE LANE MAP (all three verified LIVE this session)

Same stealth catalog, three keys, one model: `stealth/space-bunny-alpha`.

| # | Host | Key | Verified by | Result |
|---|---|---|---|---|
| 1 | openrouter.ai/api/v1 | OPENROUTER_API_KEY (nacho) | mag.probe_route probe --json | LIVE, $0 |
| 2 | openrouter.ai/api/v1 | OPENROUTER_API_KEY_2 (fostertron/ox) | direct probe | auth OK, $0 (first 30-token probe eaten by mandatory reasoning — budget 512+) |
| 3 | inference-api.nousresearch.com/v1 | HERMES_API_KEY_1 (sk-nous) | mag.probe_route probe --json | LIVE, $0 |

## THE MODEL CARD (from OpenRouter API, 2026-09-24)

- `stealth/space-bunny-alpha`, provider "Stealth", anonymous
- context **1,000,000** / max completion **524,288**
- modality **text+image+video → text** (video input natively; usage payload has a video_tokens slot)
- reasoning **mandatory**, default effort **max**, adjustable low/xhigh/high/medium/max
- tools, tool_choice, response_format, temperature, top_p supported
- pricing $0 / $0 on all three keys; prompt cache active (cached_tokens seen)
- live latency: ~2.5 s end-to-end at effort low (17×23 correct)

Nous catalog = 417 models in OpenRouter slug format. It is a mirror-relay, not a sibling.

## COMPARATIVE FINDINGS (the first audit haul)

1. **Mirror drift is real**: Nous mirror 404s `meituan/longcat-2.0:free`; OpenRouter has it. Selftest 4/5 on Nous. The gate excludes dead slugs per host — routing must stay per-host aware. Do not assume catalog equality.
2. **Our own probe organ was blind to our biggest free host**: `mag/probe_route.py` allowlisted only nous/deepseek/z.ai. FIXED this session: `openrouter.ai` added. Drift found by dogfooding, exactly as ordered.
3. **Mandatory reasoning eats small budgets**: a 30-token probe returns empty content with reasoning spent. Any lane using the bunny needs max_tokens >= 512 or empty-content false-kills.

## WHAT CHANGED IN THE REPO (durable wiring)

- `configs/providers.yaml`: `stealth/space-bunny-alpha` added to openrouter models; new **nous_api** provider block (base_url inference-api.nousresearch.com/v1, keys HERMES_API_KEY_1/2 chain, default_model the bunny). 27 providers parse clean.
- `mag/probe_route.py`: allowlist + openrouter.ai.
- `state/probe_route.json`: TTL cache now carries live verdicts for both hosts.
- `memory/corpus/LINKS.jsonl`: LINKS-322.

## THE BURN DOCTRINE (how the three keys get used, reliably)

- **Wide**: swarm/fan-out jobs route through the normal lane ladder; the bunny joins the free tier via providers.yaml, so any `openrouter` or `nous_api` lane call can land on it. No bespoke transport (dogfood law).
- **Deep**: token starvation is over for whole-corpus reads. 1M ctx × 3 keys means full-ledger reads (LINKS.jsonl, trails, ESTATE_INDEX) fit in one prompt. Use for the comparative audit: same question against all three keys, diff the answers, drift = signal (refraction habit).
- **Mickey 17 posture**: the model is an anonymous reprint worker that expires when the stealth window ends. Spend it like it is free, because it is. Do not hoard it for later; there is no later.
- **Video input** is the unburned surface: nobody in the fleet has run video through a lane yet. First job: Mr Pool / DOA corpus mp4s → frame extraction or direct video input for the interpretation pipeline.
- **Reasoning effort is a budget dial**: effort low for classification/scut (2.5 s), max for judgment. Stop paying max effort for scut work.

## ROBLOX EXECUTION (pairs with ROBLOX_MONETIZATION_PLAN_20260924.md)

The plan filed today already sets the build order: swarm port first (week 1), RUINS GO + Arrakis (week 3), Ledger of Empty Chairs flagship (weeks 4-12). The bunny lanes are how it gets built:

1. **Steal bones**: mine open-source Luau repos + Roblox Studio templates for the skeleton genres (bullet-hell, obby, simulator). The port law from the plan stands: "Roblox is the port, not the invention."
2. **Translate our systems**: game_campaign.py (4,765 lines), ShadowLedger, TheAnswer mechanics → Luau modules. Each translation is a bounded job: paste the Python module, ask for the Luau equivalent with the lore intact, human-gate the diff.
3. **Executor**: opencode 1.18.23 is installed (headless-capable) alongside hermes v0.21.3. Code-gen jobs go opencode headless or hermes dispatch --account nacho; both ride the same three keys underneath.
4. **Corpus → Roblox**: the estate's 35 playable games are the source material; the arxiv-paper repo the operator named is the research-pack feed for game mechanics (procedural audio, bullet patterns, difficulty curves).

## STANDING TASKS (filed in queue/todo.md)

- [ ] Swarm port week 1: Luau skeleton for swarm via opencode headless on the bunny lanes
- [ ] Comparative audit pass: same prompt × 3 keys, file the drift diff
- [ ] First video-input burn: one mp4 through the bunny, receipt
- [ ] mirrors.json: per-host catalog diff refreshed by the scout (longcat divergence was found by hand; make it a table)

## FALSIFIERS

- If the bunny dies on any key within 14 days, the stealth window closed; record expiry, revert lane default to ling/longcat chain.
- If a comparative diff (same prompt, 3 keys) ever returns byte-identical answers including reasoning traces, the "3 lanes" are one lane behind a proxy and the x3 claim is void.
- If the Luau translation of ShadowLedger cannot preserve the hall-files-what-you-chose mechanic, the port is cosmetic and the flagship thesis needs the Python engine server-side instead.

---

*Sources: x.com/yeahfortommy/status/2103302058103418906 (09-25 01:54Z), x.com/OpenRouter/status/2102772427105407270 (09-23 14:49Z), OpenRouter /api/v1/models, Nous /v1/models, mag.probe_route receipts in state/probe_route.json. All probes $0.*
