# INTAKE CARD — Z.AI VENDOR DOCS FOLD: THINKING/EFFORT SEMANTICS + 4 CAPABILITY PAGES + LIVE FLASH CAMPAIGN (item 13, 2026-09-03)

[SOCRATIC] assumption attacked: "the operator's paste and the live page agree, and our
lived knowledge is still current." instrument: WebFetch renders of 8 pages + corpus grep
(fuel_feed, reference, alpha_zai telemetry, max_distill). survives: all load-bearing
claims EXCEPT two — the paste's "4.7/4.5V forced thinking" (contradicts lived production)
and "ZCode"-identity in the campaign notice (name collision risk). Both Unproven, kill
conditions written (§10.7 of the reference).

## ITEM
Multi-URL vendor-docs drop, 8 pages (5 operator-named + 3 coordinator addendum):
1. docs.z.ai/devpack/latest-model — Coding-Plan model switch page (5.3/5.3-flash live all
   tiers; `/effort` default max; effort mapping table; glm-5.3-flash[1m] 1M suffix)
2. docs.z.ai/guides/capabilities/stream-tool — tool-call streaming (stream + tool_stream)
3. docs.z.ai/guides/capabilities/thinking-mode — content ALSO pasted inline by operator
   (key facts: 5.3/5.3-flash cannot disable thinking — errors; 5.3 effort = max/high/low
   only; Coding-Plan remap tables; reasoning_content in message + deltas)
4. docs.z.ai/llms.txt — full docs index (master key; noted devpack/notice pages, pricing,
   rate-limit, migrate-to-glm-new, usage-revision — not boiled, item was the five)
5. docs.z.ai/devpack/notice/event-glm-5.3-flash — VENDOR NOTICE on a free-lane-adjacent
   model: NOCTURNAL ZERO-QUOTA CAMPAIGN (details in RECEIPTS — flagged prominent per item)
Addendum: 6. capabilities/function-calling · 7. capabilities/cache (doctrine-critical) ·
8. capabilities/struct-output. Stream-tool folded briefly per coordinator.

## RECEIPTS
All 8 fetched via WebFetch (docs.z.ai renders clean). Exact quotes on file:
- **THE 1210 SCAR (MEASURE, $0, pre-dates the docs):** memory/runs/alpha_zai/
  comparison.jsonl — 2026-08-26T02:38Z, lane z_ai, model glm-5.3:
  `HTTP 400 code 1210 "This model always engages in thinking and cannot be disabled;
  please use low, high, or max"`. Vendor error text receipts BOTH the no-disable claim
  AND the 3-value effort set from our own production telemetry, 8 days before the fetch.
- thinking-mode page verbatim: "GLM-5.3 and GLM-5.3-FLASH use forced thinking and cannot
  be disabled." Effort tables + Coding-Plan remaps: from the operator's inline paste of
  the live page (fetch render did not surface them — tri-stated, cross-confirmed by the
  1210 text + latest-model mapping table).
- latest-model verbatim mappings: disabled/none/off→low ("still performs lightweight
  thinking"); minimal/light/low→low, medium/high→high, xhigh/max/ultra→max, unknown→max
  + logged hint; "Explicit Effort > thinking toggle > default max"; default = max.
- **EVENT (PROMINENT — free-lane wire):** devpack/notice/event-glm-5.3-flash — campaign
  Sep 3–20, 2026, DAILY 23:00–09:00 UTC+8 (= 15:00–01:00 UTC), weekends included,
  automatic for all paid plans, NO migration, NO new error codes. "Via ZCode: Zero quota
  consumption" (unlimited); other supported agents: quota DOUBLED. "applies only to
  GLM-5.3-Flash" — 5.3-full bills standard. NOT a rename/removal/deprecation — the model
  is unchanged. CONVERGENCE: the 09-03 addendum already in the reference had independently
  caught the window ("our locked campaign window 15:00-01:00Z IS 23:00-09:00 SGT") — two
  lanes, same organ; this pass adds dates, end-date, only-flash scoping, zero-custody.
- cache page: implicit only ("no manual configuration required"); hits "usually 50% of
  standard price"; worked example 2000-in/1200-hit → "saves 24%"; reporting field
  `usage.prompt_tokens_details.cached_tokens`; TTL still unnumbered ("reasonable time
  limits"). Matches reference §3 + EXP-A (99.52% hit) — receipted, not overturned.
- function-calling: `tool_choice` "default is auto (only supports auto)" — no forced/none.
  `function.arguments` is a JSON STRING (json.loads in every example); tool result =
  {"role":"tool","content":<json>,"tool_call_id":<id>}; branch on `if message.tool_calls:`
  (finish_reason not documented).
- struct-output: ONLY `response_format {"type":"json_object"}` — NO json_schema param, NO
  strict mode, NO message.parsed. Schema rides the system prompt; parse = json.loads.
- stream-tool: stream=True + tool_stream=True; deltas carry reasoning_content/content/
  tool_calls; args assembled per-index (`final_tool_calls[index].function.arguments += frag`).
  Self-contradiction on file: "limited to glm-5" while its own sample uses glm-5.3.

## SCORE — F:4 P:5 C:5 W:5 N:2 = 21/25 → **BUILD NOW** (docs-update; campaign window live)

## READ
This is a receipts-drop, not a discovery: most of the thinking semantics were lived
knowledge ("5.3 can't disable thinking", "needs thinking=low + >=1536 max_tokens") that
now carries vendor paper — and, better, carries OUR OWN paper: the 1210 scar in
comparison.jsonl is the vendor's exact error text captured in production on 08-26. The
genuinely NEW operational facts: (a) the Coding-Plan door does NOT error on disabled —
it silently remaps to low, so the claude-zai-style plan door and the native PAAS endpoint
have DIFFERENT failure modes for the same bad input; (b) the effort remap tables mean
churn/steer tails sending Claude-style effort strings get silently re-leveled on 5.3
(no current churn/steer sender found in mag/ — wire is NOTES-level, not a breakage);
(c) tool_choice is auto-only, so any future forced-tool steering on z.ai is impossible
by API; (d) struct-output has NO native json_schema — output contracts stay prompt-schema,
coordinator's "could go native" hope answered NO, honestly; (e) the campaign: the plan
lanes' frontier-VISION model is zero-quota nightly through Sep 20 — the free-lane story
gains a nocturnal 5.3-flash arm IF the notice's "ZCode" means this seat's CLI (name
collision risk — vendor sells to many agent CLIs; prove tonight on the dashboard, never
assume). The one OPEN CONFLICT: the paste claims 4.7/4.5V are now forced-thinking — if
true, the 4.7-flash $0 cache-mining lane (the standing wave's engine) is dead as
configured; lived production says it still ran thinking-off as of 08-24, and the fetch
render does not confirm the paste. That is the highest-stakes unknown in the drop and it
costs $0 to settle (free model ping) — queued, not fired, per lane-burn law.

## TRI-STATE
- 5.3/5.3-flash forced thinking; disabled errors on native API: **Supported** — thinking-
  mode page quote + lived 1210 scar (comparison.jsonl, message names "low, high, or max").
- Native effort set {max,high,low} only, others error; 5.2 ladder + mappings: **Supported**
  — operator paste of live page + 1210 text (names the triple) + consistent with §4.
- Coding-Plan remap tables (5.3: low-level→low, med/high→high, xhigh/max→max; 5.2:
  none/minimal→stop...): **Supported** — latest-model fetch rendered the mapping table.
- Plan door disabled→low (no error on /api/anthropic): **Supported** — latest-model page,
  explicit mapping + "still performs lightweight thinking".
- 4.7/4.5V now forced-thinking: **Disputed** (lean Unproven) — paste asserts; fetch render
  does not confirm; lived production ran 4.7-flash thinking-off through 08-24. $0 ping
  queued settles it.
- Cache 50% / implicit / cached_tokens field / TTL unnumbered: **Supported** — cache page,
  matches reference §3 and EXP-A.
- tool_choice auto-only; arguments-as-JSON-string: **Supported** — function-calling page.
- No native json_schema/strict on z.ai: **Supported as "no documented support"**; "API
  lacks it entirely" **Unproven** — docs-page absence is weak evidence of true absence.
- Stream-tool "limited to glm-5": **Unproven** — page contradicts its own sample (glm-5.3).
- Campaign exists as documented (Sep 3–20, nightly, automatic, only 5.3-flash): 
  **Supported** — vendor notice. "Via ZCode" = THIS seat's CLI: **Unproven** until a plan
  dashboard shows zero burn in-window.

## DOGFOOD
- INVARIANT PASS: receipts-over-claims (8 primary sources fetched before scoring; lived
  scar cross-receipted against vendor paper); tri-state throughout; cheapest-lane routing
  reinforced (the campaign literally widens the $0 channel nightly); zero-custody (no key
  touched, no lane burned — MEASURE ran on files alone). No law contradicted.
- STOCKFISH PASS: compute-inventory-routing gets the campaign as a time-boxed lane
  enrichment (nocturnal 5.3-flash, pending dashboard proof); provider reference upgraded
  from lived-knowledge to vendor-receipted on the params that gate every 5.3 call.

## VERDICT
**BUILD NOW** (21/25, docs-update). Done in this pass: reference §10 appended (thinking
semantics, native + Coding-Plan effort tables, 1210 lived-scar cross-receipt, door nuance,
reasoning_content shape, stream-tool assembly, struct-output honest limits, campaign
scoping, queued-ping list) + §4 pointer. Two counters: this work FORBIDS sending
thinking.type="disabled" to 5.3/5.3-flash on the native endpoint (1210, receipted twice)
and FORBIDS assuming native json_schema on z.ai output contracts; it PAID RENT on the
no-burn MEASURE — the falsifier lived in our own telemetry, so premium lanes stayed cold.

## ROUTE
- DONE: docs/ref/ZAI_API_EXPERT_REFERENCE.md §10 + §4 pointer (this pass).
- WIRE to driver (fuel_feed/driver): campaign brief — nightly 23:00–09:00 SGT zero-quota
  5.3-flash window through Sep 20; tonight's dashboard read proves both the campaign and
  the "ZCode"-identity question (§10.7 ping 3).
- QUEUED $0 pings (reference §10.7): (1) 4.7-flash thinking=disabled on ZAI_API_KEY —
  settles the paste-vs-production conflict, decides whether the cache-mining doctrine
  survives; (2) 5.3-flash native reasoning_effort:"medium" error-text receipt.
- CHURN/STEER note: no raw effort-string sender found in mag/ today; if churn ever steers
  effort through the plan door, values re-level per the §10.2 table (NOTES-level wire).
- Typed room.jsonl intake row owed by the main thread per Amendment 1 (schema not in
  this spawn's brief). Companion: the 09-03 addendum already resident in the reference —
  read together; two lanes, same window, independent catch (signal, not coincidence).

## THE CROP
This pass did NOT see: (a) the raw *.md sources behind the renders (llms.txt exposes
them; byte-verify the effort tables next seat — the tables rode the operator's paste);
(b) pricing.md + rate-limit.md — campaign-vs-off-peak stacking (zero-quota vs 50%-off)
unverified; (c) devpack/usage-revision.md + transition.md — sibling plan-structure
notices unread, could re-shape the credit tables §2 rides; (d) whether glm-4.5-flash
(the pinned z_ai3 lane) shares the 4.7 forced-thinking question; (e) any live lane —
zero pings fired by design. Next lens: a driver-lane $0 probe night settles (a-e ping 1)
and (campaign proof) in one dashboard read.

— Receipt: this card + reference §10. Falsifiability: the 4.7-flash disabled-ping result
(200 vs 1210) decides the card's one open Disputed row either way.
