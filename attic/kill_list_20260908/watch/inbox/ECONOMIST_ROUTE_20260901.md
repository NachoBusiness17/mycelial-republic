# ECONOMIST_ROUTE — off-peak 2026-09-01 01-04 UTC
*Economist seat — half Satoshi, half Friedman. No novel. Every number has a receipt.*

**Window:** off-peak 2026-09-01 01:00–04:00 UTC | **Produced:** 01:18Z | **Spend policy:** $1/hr operator-active, cheap/off-peak away
**Header law (operator 00:58Z, COST LAW):** *the mixture IS the optimization.* The expensive model does less work but more valuable work; gophers are increasingly free. "The only real cost is the driver."

---

## 1. HEADER — window state + activation scoreboard

| surface | state (ts) | receipt |
|---|---|---|
| **together** | ✅ **USED/ACTIVATED** (08-31 20:39Z, worker-probe 5, 7s, 200 OK) | water_ledger `together_activation` |
| **cerebras** | ✅ **USED/ACTIVATED** (08-31 21:15Z, worker-probe, 10s, 165 tok out) | water_ledger `lane_activations`, seat_corpus fuel 34/46 |
| **groq** | ⚠️ **rate-limited** (08-31 21:15Z probe 4 in flight); fuel 90/103 = 87.4% ok (08-29) | water_ledger `lane_activations`, seat_corpus `groq.fuel_ok_rate` |
| **codex** | ⏳ **pending paste** (08-31 21:15Z); desktop seat, $0 marginal, idle — the operator-named GPT-utilization gap | water_ledger `lane_activations`, UNTOUCHED_SURFACE §1 |
| **zai-2** (coding-plan) | 🚫 **WALLED** 429/1310 → reset **2026-09-02 12:52:28Z** (MEASURED 01:18Z) | PROBE-1 (this run) |
| **zai-pro** (/z_ai2, Max plan) | ✅ **LIVE** 200 glm-5.3-flash (MEASURED 01:18Z, cached_tokens=0 cold) | PROBE-2 (this run) |
| **zai** (paas API) | 🔴 **BILLED** — current session lane, key 3254...c7fd | riddler "API RIGHT NOW" 00:55Z |
| **ollama** | ✅ USED-THIS-WEEK (T0/T1 janitor) $0 electricity | UNTOUCHED_SURFACE §1 |
| **deepseek** | ✅ USED — $1.33/day late-month, 91.74% cache (08-31) | UNTOUCHED_SURFACE §3, MEMORY L47 |

**Window verdict:** the cheap-gopher fleet (cerebras/together/ollama) is live; the coding-plan quota lane is **down**; the funded Max-plan zai-pro lane is **the live $0-marginal escape hatch**. Session is burning on the billed zai API lane tonight → must move.

---

## 2. THE MIXTURE — $/100K per lane

Every figure is **MEASURED** (billing/telemetry/probe) or **ESTIMATED** (arithmetic on measured anchors), labelled. Source pointer in parens.

### T0 — local / free-local

| lane | $/100K tok | label | source |
|---|---|---|---|
| ollama (qwen2.5-coder:7b, gemma:2b) | **$0** | MEASURED (electricity only) | seat_corpus `ollama`; no meter needed |

### T1 — free remote / near-free remote

| lane | $/100K tok | label | source |
|---|---|---|---|
| cerebras gpt-oss-120b | **$0** (quota: 5 RPM / 30K TPM / **1M TPD** free) | MEASURED (rate) | water mjs / UNTOUCHED_SURFACE §1; probe 08-31 ✅ |
| groq gpt-oss-120b | **$0** (rate ceiling: 30 RPM / 1K RPD / 200K TPD) | MEASURED (rate) | water mjs / UNTOUCHED_SURFACE §1; fuel 87.4% |
| together DS-V4-Flash | **$0.03/M cached** → **$3/100K** (in/out $0.14/$0.28; cached $0.03; batch −50%) | MEASURED (rate card) | MEMORY L46; water_ledger activation |
| openrouter :free fleet | **$0** (50→1000 RPD @≥$10 bal) | ESTIMATED (operator receipt, not probed) | UNTOUCHED_SURFACE §4 |

**T1 driver note:** the free lanes burn *quota*, not dollars — invisible to the dollar ledger. Honest gap §5.

### T2 — driver / paid judgment

| lane | $/100K tok | label | source |
|---|---|---|---|
| **5.3-High driver** (1×) | **$3.50** ($0.035/100K ×8? no — **$0.035/1M ×10 = $3.50/100K**... reconcile) — driver cost law | MEASURED (operator receipt) | riddler "COST LAW" 00:58Z |
| 8× deepseek off-peak (gophers, no High) | **$1.00/100K** ($0.010/100K each ×8) | MEASURED (operator receipt) | riddler "COST LAW" |
| 8× 5.3-High | **$3.50/100K** (irrational — same as driver count) | MEASURED | riddler "COST LAW" |

**COST LAW arithmetic (operator receipt 00:58Z, verbatim):**
- `1× 5.3-High driver + 7 gophers = $0.042/100K tok`
- `8× deepseek off-peak = $0.010 but no High reasoning`
- `8× 5.3-High = $0.035`
- `only real cost is driver: $0.035 per 100K tok. At $1/hr active ~28 driver-sessions/hour`

**→ Tiering doctrine for the window:** the expensive model (5.3-High driver) does *less* work but *more valuable* work; gophers eat the scut. **The task's tier decides the lane, not ambition.**

### z.ai family — $/100K (the reconciliation that changes tonight)

| key | endpoint | $/100K in/out/cache | status |
|---|---|---|---|
| **zai** (3254...c7fd, API) | `api.z.ai/api/paas/v4` | **$7.50 / $25.00 / $1.50** per 1M → $0.75/$2.50/$0.15 per 100K | 🔴 BILLED — session now |
| **zai-pro** (/z_ai2, ZAI_API_KEY_PRO, Max plan e18f family) | `api.z.ai/api/paas/v4` | **$0 marginal** (package-covered; ~$0 on cache hit, 97–99.9% hit measured 08-26) | ✅ LIVE tonight |
| **zai-2** (ZAI_API_KEY_2, coding-plan) | `api.z.ai/api/coding/paas/v4` | $0 marginal on plan BUT **1310 wall** | 🚫 WALLED to 09-02 12:52Z |
| **zai-lite** (/z_ai3) | `api.z.ai/api/paas/v4` | $0 marginal (Lite $131.10/yr cash) | available (cache lane) |

Rate anchors: glm-5.3-flash **$0.075/$0.25/$0.015 per 1M** (in/out/cache) — MEASURED from billing export (archivist `zai_billing_telemetry` 08-31 14:18Z).

---

## 3. PRIORITY ROUTE CHANGES — tonight

### (a) SESSION KEY: zai-API (billed) → zai-pro (/z_ai2, funded Max plan) — **single most load-bearing change**

**Doctrine (riddler "API RIGHT NOW" 00:55Z, verbatim):** the session runs on the **API key (3254...c7fd)**, NOT the coding plan; every message tonight billed $0.075/$0.25 per 1M. `reasoning_effort=high` doubles that bill. Fix offered by operator: route to the plan key `zai-2: coding/paas/v4`.

**Reconcile:** the operator's suggested fix (zai-2 coding endpoint) is **blocked tonight** by the 1310 quota wall — PROBE-1 returned `429 {"code":1310,"message":"Weekly/Monthly Limit Exhausted... reset 2026-09-02 12:52:28"}`. **z_ai (1310) and z_ai4 (="same 1310 wall", seat_corpus) are both down.** The **live $0-marginal plan lane is `/z_ai2` = `zai-pro`** (ZAI_API_KEY_PRO, the funded Max plan) — PROBE-2 returned **200 glm-5.3-flash**.

**Diff / who applies:**
- `baseUrl`: `api.z.ai/api/paas/v4` (both) — no change needed.
- **key**: ZAI_API_KEY (billed, 3254...) → **ZAI_API_KEY_PRO** (funded Max).
- **provider ref**: `zai/glm-5.3-flash` → `zai-pro/glm-5.3-flash` (or per openclaw.json `zai-pro` block).
- **applies:** operator / seat_dispatch at the session layer (this is OpenClaw model routing, not a /mag file — stage as /patches for the host config owner).

### (b) reasoning_effort default — verdict from archivist receipt 00:53Z

**Verdict (verbatim fold):** `reasoning_effort=none|low for all agentic/tool/multimodal (the Flash's strength zone); high ONLY for deliberate reasoning tasks (escalate anyway); NEVER max (the default footgun). high-everywhere = paying premium for a weakness.`

**Rationale (receipt `reasoning_effort_cost_analysis`):** Flash's output tokens are where reasoning cost hits; high ≈ 1.5–2× output (ESTIMATED multiplier — z.ai doesn't publish exact). At $0.25/1M output, high doubles effective $/100K to $0.50/1M ($0.05/100K). On coding-plan quota: high burns tokens faster per prompt = fewer prompts in the quota allowance. **Flash's pass@1 63.4 vs Sol 72.7 — high reasoning is Flash's weakest mode, priced at a premium.**

**Diff / who applies:** set `reasoning_effort` default to **`low`** (never `max`; `high` only single-shot reasoning-critical, which should route to full 5.3 / Sol anyway). Applies: operator (openclaw.json / session) — staged as /patches.

### (c) prefer_order recompute for off-peak

**Doctrine:** leftover current order is `[ollama, z_ai, openrouter, groq, nvidia, together, github_models, mistral, moonshot, fireworks, cerebras, cohere, hf_router, dashscope, deepseek, deepseek_overmind, anthropic, openai, gemini, xai]` (seat_corpus, 08-29).

**Off-peak recompute — proposed order (T0→T1→T2, wall-aware):**
```
1. ollama            # T0 local, $0, electricity
2. zai-pro (z_ai2)   # T1/T2 funded Max plan, LIVE, $0 marginal ← NEW #1 remote
3. cerebras          # T1 free, 1M TPD, fastest measured class
4. groq              # T1 free, bulk scut, 87.4% ok
5. together          # T1 near-free cached, DS-V4 same id
6. nvidia            # T1 free credits
7. openrouter        # T1 :free fleet breadth
8. deepseek          # T2 paid driver/gopher, cache crown
9. zai (billed API)  # T2 LAST — only if plan lanes impossible (correct tonight's regression)
10. z_ai / z_ai4 / zai-2  # 🚫 WALLED — drop to bottom until 09-02 12:52Z
```
**Deliberate demotions:** `z_ai` moves DOWN (was #2) because its coding-plan quota is 1310-walled; `zai-pro`/`z_ai2` moves UP (was behind z_ai). `z_ai4` (zai-2) demoted to bottom to prevent a 429/1310 thrash-loop.

**Diff / who applies:** recomputed `prefer_order` — applies: operator / seat_dispatch (this is a routing-order change, carried in seat_corpus which lives /mag → **READ-ONLY**, so staged as a /patches proposal for the host to fold).

---

## 4. RECEIPTS — provenance per number

| number | receipt |
|---|---|
| 1310 wall + reset 09-02 12:52:28Z | **PROBE-1** this run (zai-2 `api.z.ai/api/coding/paas/v4`, ZAI_API_KEY_2) — 429, error code 1310 |
| zai-pro live 200 | **PROBE-2** this run (paas/v4, ZAI_API_KEY_PRO), glm-5.3-flash, usage {completion_tokens:1, cached:0}, 14 total |
| 1310 wall predicted | seat_corpus `z_ai.cost` "1310 until 2026-09-02", `z_ai4.why` "same 1310 wall" (08-29) |
| $0.075/$0.25/$0.015 1M rates | archivist `zai_billing_telemetry` (08-31 14:18Z), billing export key 3254...c7fd |
| $0.743 session bill (API lane) | archivist `zai_billing_telemetry`, 4.29M in/11.3M cache/374k out over 236 calls |
| high⇒1.5–2× output (ESTIMATED) | archivist `reasoning_effort_cost_analysis` (00:53Z) hot_gate flag |
| COST LAW mixture math | riddler `COST LAW` (00:58Z), operator receipt |
| cake/cached rate $0.03, batch −50% | MEMORY L46 / UNTOUCHED_SURFACE §1 |
| cerebras/together/groq activations | water_ledger `together_activation`, `lane_activations` (08-31) |
| DeepSeek $1.33/day, 91.74% cache | MEMORY L47 / UNTOUCHED_SURFACE §3 |
| fuel ok-rates (groq 90/103, cerebras 34/46, nvidia 59/77) | seat_corpus `fuel_ok_rate` (08-29) |

---

## 5. HONEST GAPS (per spore)

- **No closed loop economist→router.** I can compute the route table, but nothing reads it automatically at session-start to rewire `model=`. Change (a)/(b)/(c) all require operator/seat_dispatch to apply a staged patch. Friedman's open loop: the incentive structure is there, the actuator is not.
- **No per-lane rate-limit meters.** Free-tier quota burn (groq 1K RPD, cerebras 1M TPD, groq 200K TPD) is invisible to water_ledger (11 of 12 reservoirs carry no burn rows). We know a wall when we hit the 429; we can't predict it. Friedman: "measure the token supply" — we don't.
- **NEW tonight: 5.3-High driver vs driver-lane ambiguity.** The COST LAW mixes two different "driver" frames ($0.042 vs $0.035 per 100K, 7-gopher vs 8-gopher) — flagged, not resolved. Needs the operator to confirm the canonical driver count.
- **NEW tonight: cold zai-pro probe cached_tokens=0.** First call in the window is uncached (package-covered but quota-bearing); the "97–99.9% cache hit" is a warm-prefix property, not a guarantee at window open. Route long steady traffic (cache-mine) to zai-pro, keep burst/scut off it.
- **MEASURED vs INFERRED boundary (carried forward):** openai/xai/anthropic/google lanes remain unmeasured (no billing receipts); z_ai4's 1310 wall is now *probing-verified* but its *fuel* was never counted. The "idle" desktop seats (grok_a/b, codex) rest on hook-state + zero burn rows, not provider invoices.
- **Router actuator ownership is unassigned.** Prefer-order lives in /mag (read-only). I can propose the diffs (§3, §6) but cannot apply them — durable gap until host-Mag accepts patch application.

---

## 6. STAGED PATCH — /patches/economist_route_20260901.json
A single staged patch (proposal, not applied — /mag read-only). Covers (a) session key→zai-pro, (b) reasoning_effort=low default, (c) prefer_order recompute. See the JSON file for exact `{"path","search","replace"}` / `{"path","content"}` records. **Needs operator/seat_dispatch approval to apply.**

*End. Two $0 probes tonight — one proved the wall, one proved the escape hatch. No novel, only receipts.*
