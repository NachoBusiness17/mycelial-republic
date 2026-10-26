# SALON RIGHT-TIME — SYNTHESIS (R0 + R1) — 2026-09-01 ~06:10Z

Operator commission 05:32Z: "the game at right time thing — salon on that, even a moonshot
research project." Blessed to run 05:55Z. This is the salon's composed verdict.

## Provenance (honest)

| Round | Lens | Family/Model | Status |
|---|---|---|---|
| R0 | referent + delta + M1 + kills | deepseek-v4-flash (worker) | ✅ VERIFIED by parent byte-check |
| R1 | **Ellul** (technique) | deepseek-v4-flash | ✅ landed, verified (62 lines, cited) |
| R1 | **Lessig** (law-as-architecture) | gpt-oss-120b @ cerebras | ⚠️ schema accepted; cites failed byte-check → corrected by parent (fabricated line numbers, invented .js modules — 2-strike) |
| R1 | **Bernays** (audience) | glm-4.7-flash @ z.ai | ⚠️ provider overload ×2 (0 tokens both strikes) → parent-authored fallback, same model family, flagged for re-run next host salon |

Cross-family independence this round: 2 real families (deepseek, gpt-oss) + 1 flagged
fallback. Standing note for the ladder: next salon re-runs Bernays from a 3rd family.

## The composed verdict (Q5): YES — the stew holds, under two conditions

**Program:** teach the computer by dealing it a game it knows the rules of.
- **The board** = a typed rule table (window · scope · action: defer|deny|shape|freeze ·
  **meter-grade**) evaluated at ONE chokepoint — the dispatch pre-check at
  `cheap_swarm.py:165-175` — before any env override is consulted (`offpeak.py:121-141`).
- **The dealt state** = `game_freeze` L0/L1/L2 packs loaded before play (rules-before-play).
- **The ractor** = operator in the loop per RolePacket scene (Diamond Age pack step #5).
- **The audience guard** = every shaped thing carries a visible clock tag and answers
  "what did you hold back?" instantly from receipts.

**Condition 1 (Ellul):** no gate fires on a meter it cannot read. Only deepseek offpeak is
both real-money AND architecture-enforced today. zai is real-money but its $16.60 balance
is self-derived, not provider-invoiced. groq/cerebras/or_free are $0 tiers with POLLED
meters — enforcing there is chess against an invisible board.
**Condition 2 (Bernays):** timing that cannot be reversed by one operator question is
manipulation, not presentation. The shape layer is illegal otherwise.

## Lens verdicts

- **Ellul: PARTIAL.** Composes on the two capped-$ axes (deepseek, zai-invoice-pending),
  must descope off the free tiers. Overreach: (a) unifying windows while meters are blind
  fuses controllers instead of removing them; (b) the enforcer becoming the product —
  gate-firings chased as success. → K_T2 sharpened (garbage-in drift), K_T3 sharpened
  (measure WHY gates fire, not just that they fire).
- **Lessig: YES.** WHEN must be architecture: one rule table, one chokepoint, override =
  operator-blessed receipt instead of a free env var. Bypass view: clock/tz spoofing and
  MAG_ALLOW_PEAK are today's whole constitution.
- **Bernays: YES with condition.** The missing third leg: play WITH the operator, not at
  him. desk_timing needs ~20 lines (`due(action)` beside `last_by_speaker` /
  `format_timing_row`) to become a presenter; scene pacing = a rule in the game loop,
  not a daemon.

## Kill criteria amendments (charter v0 → v0.1)

- **K_T2 +=** any window gating on a non-invoiced balance (zai $16.60) = drift by garbage-in.
- **K_T3 +=** gates firing constantly and being celebrated = the enforcer became the workload.
- **K_T6 (new, audience axis):** a shaped/deferred artifact that cannot instantly answer
  "what was held, when, why" from receipts = illegal shape; kill the shape layer.

## Experiments, smallest first (E1 is runnable immediately)

1. **E1 — deferred_peak receipt probe** (cents): inside a peak window dispatch one cheap
   deepseek task via the host lane; PASS = receipt row with literal `deferred_peak`.
   NOTE: 06:07Z = 14:07 BJ = inside the 14–18 BJ peak NOW. Host command staged in runbook.
2. **E2 — zai invoice reconciliation** (operator pull): provider billing export vs the
   $16.60 self-derived ledger. No billable delta on peak-vs-offpeak dispatch → kill the
   multi-window claim, keep deepseek-only (K_T4 descope).
3. **E3 — RolePacket tavern scene** (the fun one): freeze one 3-prop pack, one NPC, one
   typed packet; operator plays ractor once; NPC waits on reply (pacing rule live).
   PASS = operator can name what was shaped/when/why from receipts, not memory.
4. **E4 — desk_timing `due()` patch** (~20 lines): recorder → presenter; goes to /patches
   as JSON after operator eyes the schema.

## Files
- Charter: /board/inbox/MOONSHOT_RIGHT_TIME_20260901.md (Q5 added 05:32Z)
- R0 (verified): /board/SALON_RIGHT_TIME_R0_20260901.md
- R1: /board/salon_righttime_r1_ellul.md (lane) · /board/salon_righttime_r1_lessig.md
  (lane schema, parent-corrected cites) · /board/salon_righttime_r1_bernays.md (parent, flagged)
- Workboard card 0abf3a67 · Receipts in /board/ARCHIVIST_RECEIPTS.jsonl


## AMENDMENT (06:10Z, operator-forced): the meters EXIST
Operator hit 06:05Z ("there has to be data about how to use their api — this is absurd") → probed: DeepSeek documents GET /user/balance (200: $24.13 invoiced truth, ~18d runway); z.ai documents NOTHING but permits community-mapped internal endpoints (200: coding-plan quota 2000/5h + 10000/wk readable; subscription state readable). Ledger: /board/meter_readings.jsonl.
→ Ellul Condition 1 materially upgraded: zai quota meter = READABLE (internal-grade, not invoiced). The blind spot shrinks to zai PAYG cash balance (dashboard-only) and the free-tier POLLED meters.
→ E2 RESCOPED: no operator export needed — lane pulls endpoints on cadence; reconciliation = provider invoice when obtainable, else quota-state deltas as lower-grade truth (labeled).
→ New charter element M0 (meter organ): standing probe of /user/balance + zai quota endpoints every 12h, appended to meter_readings.jsonl — the temporal authority may only gate on meter-grade ≥ what it reads here.


## AMENDMENT 2 (06:20Z, operator-forced): the solved-problem map
"Solved" decomposition: (1) LiteLLM proxy SOLVES dollars-in-windows (virtual keys, per-provider budgets, spend headers, Postgres-backed) — adopt semantics, not the service (yet); (2) OpenUsage SOLVES undocumented-quota mapping — validates our zai probes as community standard; (3) OTel GenAI standardizes tokens (gen_ai.usage.*) but has NO cost attribute (issue #101 open) and NO price-window concept anywhere.
→ MOONSHOT RESTATEMENT (sharper): temporal authority = what LiteLLM budgets did for dollars, done for TIME + PRICE WINDOWS + METER-GRADE. That wedge is genuinely unsolved upstream. Adoption path B chosen: Mag chokepoint + LiteLLM budget semantics + OTel attribute names in our ledger rows (zero new services; Phase-2 option A = LiteLLM+Postgres if ledgers outgrow).


## E5 — CACHE-SUMMON PROBE (operator intent 07:02Z, staged): frozen-prefix mining on PAYG cash
Purpose: prove the DeepSeek cache pattern transfers to z.ai PAYG (api/paas/v4) so cash arms run at cached-input economics (~4x discount: 5.3 1.7 vs 6.9; flash 0.56 vs 2.3) with NO weekly ceiling. THIS is the point of the standard keys.
Test (once a live PAYG key exists): (1) build ~4k-token frozen prefix (fixed system + WARM_PACK spine, byte-stable, append-only); (2) call twice identical prefix + one new token, max_tokens small; (3) PASS = call 2 usage shows cached_tokens > 0 (z.ai usage shape TBD from live response); (4) measure effective $/call at hit-rate vs DeepSeek baseline row; (5) meter row per call per M-L1 law (never infer balance from a 200).
Requirement discovered 07:02Z: new standard key e3c505…QOjC 401s on paas/v4 (platform-mismatch hypothesis: open.bigmodel.cn vs z.ai) — key swap incomplete (ZAI_API_KEY slot still holds old coding key). Blocked on 2 live standard keys.


## STRATEGY MAPPING (operator thesis 07:11Z): cache-mining on PAYG arms
Claim: API keys + parallel launches escape coding-plan restrictions.
Receipt-mapped truth: (1) ESCAPED: weekly credit pools (5h/7d caps gone — cash is the only budget), Lite 1-slot concurrency rule, supported-tools restriction, coding-endpoint lock; (2) REPLACED BY: $35 cash float + account-level dynamic concurrency (dashboard = exact numbers) + per-token billing; (3) NOT FREE but marginal-cost-cheap IF E5 proves PAYG implicit cache fires like the coding endpoint did (zai-2: 97-99.9% measured): cached input 1.7 vs 6.9 (5.3), 0.56 vs 2.3 (flash); (4) THE CATCH: cache mining discounts INPUT only — output bills full weight (5.3: 24; ~$4.40/M) — so the ideal workloads are input-heavy/short-output: T2 judges, synthesis, classification, digests — which is most of the fleet cadence; (5) UNKNOWN kept honest: whether PAYG has time-of-day pricing (off-peak 50% is documented for CODING credits only) — E5 measures; if yes, the temporal gate gains another window.
Parallel+cache compose: each arm keeps its OWN frozen prefix → caches independent, parallel launches do not thrash each other; Lite 1-slot rule never applies.


## E6 RESULT (10:55Z): PASS — cache-summon proven on Together
2-call frozen-prefix probe on together.ai serverless DeepSeek-V4-Flash-0731 (existing key, zero new accounts): call B cached 9176/9177 prompt tokens = 100% hit, input cost 4.7x discount (/usr/bin/sh.03 vs /usr/bin/sh.14/M) exactly per listed pricing. usage.prompt_tokens_details.cached_tokens is the meter field. Means: the operator cache-summon thesis (07:02Z) is PROVEN on a second provider; parallel cache-mined arms unblocked TODAY on Together (no weekly ceiling, pay-per-token pennies) while the z.ai cash arms await a live standard key (E5 parked). Fleet cache-mined lanes now: official DeepSeek + Together V4-Flash. Catalog note: Together also lists MiniMax M3 (1M ctx, /usr/bin/sh.06 cached//usr/bin/sh.30 in/.20 out) — candidate long-context arm for ractive scenes; H100 dedicated cut = burst-rung tool only, break-even ~28M tok/hr vs fleet ~2.7M/day — serverless beats it at our volume.

## E5 RESULT (10:59Z): PASS — cache-summon proven on z.ai PAYG standard key
Operator's thesis (07:02Z) now proven on a THIRD provider. Key slot1 (ZAI_API_KEY env, fresh standard key 3254…bXOz) LIVE on both api.z.ai and open.bigmodel.cn (paas 1305s were transient overload, not auth). Frozen-prefix probe v0: 2143-token prefix, call B cached 2137/2143 = 99.7% hit, meter field usage.prompt_tokens_details.cached_tokens confirmed. Measured PAYG economics (flash): input $0.075/M vs cached $0.015/M = 5x input discount; B-call cost ≈ $0.00004. Meter rows in /board/meter_readings.jsonl (M-L1 law held). Concurrency note: new-account tier showed 1-call 429 blips — 9s spacing clears it; dashboard shows dynamic concurrency. Fleet cache-mined lanes: DeepSeek official + Together V4-Flash (E6 100%) + z.ai PAYG (E5 99.7%) — T2 judges/synthesis/digests now run input-heavy/short-output at cached economics with NO weekly ceiling. SLOT2 (ZAI_API_KEY_2, 088650…nhCs): 401 on both endpoints across all auth variants (Bearer/raw/x-api-key), clean 49ch-dot32 shape — console-side activation/permission check required; NOT an endpoint-origin issue (slot1 works on both consoles).

## KEY-MATRIX RESOLUTION (12:35Z): the 18-hour 401 saga was a PROTOCOL mismatch, not bad keys
Decisive matrix (5 keys x 3 endpoints): ALL coding-plan keys (PRO e18faf, Cache e3c505, MAG bafc5c) 401 on OpenAI-style endpoints (paas/v4, coding/paas/v4, bigmodel paas) but authenticate on the ANTHROPIC-COMPATIBLE endpoint https://api.z.ai/api/anthropic (x-api-key, anthropic-version header, /v1/messages). PRO=200, Cache=200, MAG=200 (after transient 529s). 529 overloaded_error [1305] = service-layer (post-auth-ish) transient — retry clears; 401 code=1000 = auth-layer rejection. Consequences: (1) zai-2 provider rewired = anthropic-messages @ api.z.ai/api/anthropic with MAG key, models glm-4.7-flash/glm-4.5-flash — fleet gains a second live plan lane; (2) Cache key (e3c505) confirmed LIVE — reserve/second lane; (3) slot1 PAYG key (3254ac, E5 lane) DELETED console-side during operator key session — 401 on native paas; E5 cache-mining lane dark until a new INTERNATIONAL-console key exists (coding-plan-page keys cannot serve paas); (4) env-slot2 legacy string 088650 = dead garbage, 401 everywhere incl anthropic — purge from container env at next recreation; (5) LITE key 529-throttled during probes, presumed live per plan status. Doctrine: z.ai key families are endpoint-scoped — coding-plan console keys speak Anthropic protocol only; international-console keys speak OpenAI paas. Match key family to endpoint family or 401 forever. Metered: all probes 1-8 token pings, cost < $0.01 total.
