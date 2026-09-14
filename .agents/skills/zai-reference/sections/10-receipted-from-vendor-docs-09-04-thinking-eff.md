## 10. RECEIPTED FROM VENDOR DOCS 09-04 — THINKING/EFFORT SEMANTICS + CAMPAIGN SCOPING (8-page fold)

Sources: devpack/latest-model · guides/capabilities/thinking-mode (+ operator paste of live
page) · capabilities/{stream-tool, function-calling, cache, struct-output} ·
devpack/notice/event-glm-5.3-flash · llms.txt index. Complements the 09-03 addendum above
(cache/tool basics already folded there) — this section is what that sweep did NOT catch.

### 10.1 Thinking semantics per model
- **FORCED (cannot disable): GLM-5.3 + GLM-5.3-FLASH.** Verbatim: "GLM-5.3 and
  GLM-5.3-FLASH use forced thinking and cannot be disabled."
  **LIVED SCAR AGREES, and predates the docs**: 2026-08-26T02:38Z, z_ai lane, glm-5.3 →
  `HTTP 400 code 1210 "This model always engages in thinking and cannot be disabled;
  please use low, high, or max"` (memory/runs/alpha_zai/comparison.jsonl). The vendor's
  own error text receipts the 3-value effort set from production telemetry.
- Auto-decide (disable allowed): 5.2/5.1/5/4.6/4.5.
- **4.7/4.5V FORCED: UNPROVEN, CONFLICT ON FILE.** Operator paste says 4.7/4.5V are
  forced-enabled; the fetched render does not confirm it; lived production (§3 fleet
  finding, mag/fuel_feed.py 08-24 comment) runs 4.7-flash thinking-OFF for cache mining.
  Kill condition queued: §10.7 ping 1.
- **DOOR NUANCE (load-bearing):** native PAAS endpoint: `thinking.type="disabled"` on
  5.3 = 1210 ERROR. Coding-Plan door (/api/anthropic): disabled/false/none/off does NOT
  error — silently remaps to low ("still performs lightweight thinking"). Priority:
  "Explicit Effort > thinking toggle > default max"; default effort = max.

### 10.2 reasoning_effort tables
Native API:
| Model | Allowed values | Other values |
|---|---|---|
| 5.3 / 5.3-flash | **max, high, low ONLY** | ERROR (1210 family) |
| 5.2 | max, xhigh, high, medium, low, minimal, none | none/minimal = stops thinking; low/medium→high; xhigh→max |

Coding-Plan remap (what the plan door sends upstream when we steer it):
| Model | Mapping |
|---|---|
| 5.3 / 5.3-flash | none/minimal/low→low · medium/high→high · xhigh/max→max |
| 5.2 | none/minimal→stop · low/medium→high · xhigh→max |

latest-model page adds: light/ultra also accepted (light→low, ultra→max); unknown effort
string → max + logged hint. **MAX_DISTILL receipt**: "5.3 needs thinking=low" is now
vendor-receipted — low IS the model's floor, not a workaround.

### 10.3 reasoning_content shape
- Message: assistant msg carries `reasoning_content` beside content/tool_calls.
  Streaming: `delta.reasoning_content` chunks (hasattr-guard), same for stream-tool deltas.
- Preserved thinking: ON by default on the Coding-Plan endpoint, OFF on standard API.
  Opt-in via `clear_thinking:false` requires returning prior reasoning_content
  UNMODIFIED — "All consecutive reasoning_content blocks must exactly match the original
  sequence"; reordering/editing degrades performance + cache hit.

### 10.4 Stream-tool deltas
Tool-call args arrive as fragments keyed by `index`; assemble incrementally:
`final_tool_calls[index].function.arguments += frag` (arguments are a JSON STRING).
Docs self-contradiction: page says "limited to glm-5" while its own sample uses glm-5.3 —
treat the limit as untested. [1m] suffix + CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000 for 1M
on the Claude door (see addendum).

### 10.5 Structured output — honest limits
**NO json_schema parameter. NO strict mode. NO message.parsed.** Only
`response_format {"type":"json_object"}` + schema embedded in the system prompt +
`json.loads(content)` + own validation. Fleet output contracts CANNOT go native on z.ai —
keep prompt-schema discipline. (Docs-page absence ≠ proven API absence; probe queued §10.7.)

### 10.6 EVENT SCOPING — glm-5.3-flash nocturnal campaign (LIVE; sharpens addendum)
Vendor notice, exact scope: **Sep 3–20, 2026, DAILY 23:00–09:00 UTC+8 (15:00–01:00 UTC),
weekends included, automatic, all paid plans.** "Via ZCode: Zero quota consumption";
other supported agents: quota DOUBLED. **Applies ONLY to glm-5.3-flash** — 5.3-full bills
standard. Open items: notice's "ZCode" = this seat's CLI is name-collision-risk UNPROVEN
(prove via plan dashboard zero-burn in-window); stacking with off-peak 50% credits
unspecified.

### 10.7 QUEUED PINGS ($0-ordered; next seat executes cold)
1. **glm-4.7-flash + `thinking {"type":"disabled"}` + max_tokens=16** on ZAI_API_KEY —
   FREE model, $0. 200 → 4.7 still disableable, cache-mining doctrine intact, paste wrong.
   1210 → §4 row is DEAD, free-lane doctrine must rebuild on reasoning-bearing completions.
2. glm-5.3-flash native + `reasoning_effort:"medium"` → expect effort-error naming
   max/high/low (completes the 1210 receipt for the effort axis).
3. Plan dashboard read inside tonight's 23:00–09:00 SGT window → proves zero-quota
   campaign + settles the "ZCode" identity question.

### ADDENDUM 2 — CONCURRENCY TABLE FOUND (operator supplied the page my probes 404'd, 09-03)
Source: z.ai rate-limits page (pasted verbatim by operator; "API usage is limited by concurrency — in-flight requests").

FLEET-MEANING ROWS (concurrent in-flight):
- GLM-5.3-Flash: **50** — the free-lane king; intake/driver burst caps were conservative vs this.
- GLM-5.3: 15 · GLM-4-32B-0414-128K: 15 (B-lane engine confirmed at 15) · GLM-4-Plus: 20
- GLM-5.1/5.2: 10 · GLM-4.5V/4.6V: 10 · Web-Reader: 5 · Search-Prime(+Claude): 5
- GLM-4.7-Flash: **1** ← explains the historic "4.7 pool congested provider-wide"; 4.7: 2, 4.7-FlashX: 3
- GLM-4.5-Flash: 2 · 4.5-Air/AirX: 5 · GLM-5: 2 · 5-Turbo: 1 · GLM-Image/CogVideoX-3: 1
- THROTTLE LAW: >8K context on GLM-4-Flash (free trial) throttles to 1% of standard concurrency — long-context free-lane work dies silently; keep free-trial Flash calls short-context.
TRI-STATE: table = Supported (operator paste, primary source). Application to CODING-PLAN sessions (OAuth/anthropic door) = Unproven — table is titled for API usage; plan side may be credit-window-only. Router implications: 4.7-Flash lanes are 1-wide (retire/deprioritize), 5.3-Flash at 50 justifies bigger burst caps on API-credit lanes; fuel_feed FREE_LANES repoint = routed-plan item, not hot-patched.
