# UNTOUCHED_SURFACE_REPORT — 2026-08-31 (Economist seat, first job)

**Complaint answered:** operator's 18:13Z — "keys we pay for and don't call." Every claim below is pointer-backed. Receipts: `/mag/memory/runs/seat_corpus/latest.json` (ts 2026-08-29T17:46:06Z), `/board/water_windows.mjs` + `/board/water_ledger.jsonl` (mtime 08-31 14:07), `/root/.openclaw/workspace/MEMORY.md` lines 46–50 (rate card + telemetry), OpenClaw runtime line of this session (model=zai/glm-5.3-flash, default=deepseek/deepseek-v4-flash).

**Ledger reconciliation check:** water_ledger zai_credits burn = 0.75 + 2.65 = $3.40 → balance $20 − $3.40 = **$16.60** — matches the founding-wound number. The ledger now agrees with itself. Wound partially healed; still rate-receipt math, not a provider invoice.

## 1. LANE INVENTORY — all 23 named lanes (20 in prefer_order + 3 z_ai splits) + 4 desktop water seats

| lane | provider | what it offers | cost tier | last-use evidence | status | one-command activation |
|---|---|---|---|---|---|---|
| ollama | local | gemma:2b, qwen2.5:3b, qwen2.5-coder:7b, gemma4-desk — T0/T1 janitor | $0 (electricity) | capture "always-on janitor"; `janitor_report.jsonl` + `cache_watch.jsonl` mtimes 08-31 17:13 | **USED-THIS-WEEK** | `ollama run qwen2.5-coder:7b` |
| deepseek | DeepSeek API | v4-flash (default OpenClaw model), v4-pro; 1M window cache | PAID, measured: late-month avg $1.33/day, run-rate ~$40/30d (MEMORY L47) | this session's `default_model=deepseek/deepseek-v4-flash`; telemetry 998 req/$0.786/91.74% cache (08-31, MEMORY L47) | **USED-THIS-WEEK** | `model=deepseek/deepseek-v4-flash` |
| deepseek_overmind | DeepSeek API | failover key pool, same ids | PAID | `key_present: false` (seat_corpus) | **NEVER-CALLED** (no key — structurally dead) | import 2nd key, then `--provider deepseek_overmind` |
| z_ai | z.ai | glm-4.7-flash coding-plan key | PLAN-QUOTA; 1310 wall until 09-02 | fuel 56/72 ok (corpus 08-29) | **STALE** (2d) | opencode harness only (`opencode_only: true`) |
| z_ai2 | z.ai Pro | glm-4.7/5.3-flash; 97–99.9% cache-hit measured 08-26 | $0 marginal (plan cash sunk: Max $403.20/qtr, MEMORY L47) | **this session runs zai/glm-5.3-flash** ∈ its models | **USED-THIS-WEEK** | `model=zai/glm-5.3-flash` (this very report) |
| z_ai3 | z.ai Lite | glm-4.7/5.3-flash cache lane | $0 marginal (Lite $131.10/yr cash, MEMORY L47) | models ∩ this session model | **USED-THIS-WEEK** | `model=zai/glm-5.3-flash` via Lite key |
| z_ai4 | z.ai | coding-plan #2, glm-4.7/4.5-flash | PLAN-QUOTA; same 1310 wall | no fuel counter, opencode_only | **NEVER-CALLED** (no receipt either way — inference) | opencode only |
| groq | Groq | gpt-oss-120b free bulk, qwen3.6-27b, compound-mini | FREE (30 RPM/1K RPD/200K TPD, water mjs) | fuel 90/103 = 87.4% ok (corpus 08-29) | **STALE** (2d) | `model=groq/openai/gpt-oss-120b` |
| openrouter | OpenRouter | /auto + :free fleet — llama-3.3-70b, gemma-2-9b, r1:free; 50→1000 RPD | FREE lanes | no fuel counter; "18 free lanes if rotated" (corpus) | **NEVER-CALLED** this window (inferred — no receipt found) | `model=openrouter/meta-llama/llama-3.3-70b-instruct:free` |
| openai | OpenAI | gpt-4o-mini/4o (Mag), gpt-5.6-sol (OpenClaw catalog) | PAID, unmeasured | no receipt found in trails | **NEVER-CALLED** (inference — trails not exhaustively grepped) | `model=openai/gpt-5.6-sol` |
| xai | xAI API | grok-3-mini/3/4.5 — judgment lane | PAID, unmeasured | no receipt found (TUI seats ≠ API) | **NEVER-CALLED** (inference) | `model=xai/grok-4.3` (max_completion_tokens, not max_tokens) |
| together | Together | DeepSeek-V4-Flash-0731 same id as direct | trial/paid — **$0.14/$0.28 per 1M, cached $0.03, batch −50%** (MEMORY L46) | no receipt; "Mag pulled from $0 channel when key went paid" | **NEVER-CALLED** this window | `model=together/deepseek-ai/DeepSeek-V4-Flash-0731` |
| nvidia | NVIDIA NIM | 102 models; v4-flash-0731 verified 3.4s; llama 3.1/3.3, nemotron | FREE credits (billing UNVERIFIED → no spend, MEMORY L46) | fuel 59/77 = 76.6% ok (corpus 08-29) | **STALE** (2d) | `model=nvidia/deepseek-ai/deepseek-v4-flash-0731` |
| cerebras | Cerebras | gpt-oss-120b ~3000 tok/s; gemma-4-31b | FREE (5 RPM/30K TPM/1M TPD) | fuel 34/46 = 73.9% ok (corpus 08-29) | **STALE** (2d) | `model=cerebras/gpt-oss-120b` (browser UA in Mag) |
| google | Google/Gemini | gemini flash, adaptive thinking | free/paid | `key_present: false` ("empty in Mag .env", corpus) | **NEVER-CALLED** (no key) | fill GEMINI_API_KEY → `model=google/gemini-3.5-flash` |
| anthropic | Anthropic | claude-sonnet-4, haiku | PAID | `key_present: false` | **NEVER-CALLED** (no key) | fill ANTHROPIC_API_KEY → `model=anthropic/claude-sonnet-5` |
| github_models | GitHub | prefer_order only | — | no lane block in corpus | **NEVER-CALLED/UNCONFIGURED** | write lane block + token → then route |
| mistral | Mistral | prefer_order only | — | no lane block | **NEVER-CALLED/UNCONFIGURED** | same |
| moonshot | Moonshot | prefer_order only | — | no lane block | **NEVER-CALLED/UNCONFIGURED** | same |
| fireworks | Fireworks | prefer_order only | — | no lane block | **NEVER-CALLED/UNCONFIGURED** | same |
| cohere | Cohere | prefer_order only | — | no lane block | **NEVER-CALLED/UNCONFIGURED** | same |
| hf_router | HuggingFace | prefer_order only | — | no lane block | **NEVER-CALLED/UNCONFIGURED** | same |
| dashscope | Alibaba | prefer_order only | — | no lane block | **NEVER-CALLED/UNCONFIGURED** | same |
| grok_a | Grok TUI (nacho) | desktop seat, quota in subscription window | DESKTOP PLAN ($0 marginal) | water mjs: "idle seat — hook-tracked", no burn rows | **NEVER-CALLED** (idle desktop) | send prompt to seat / hook contract |
| grok_b | Grok TUI (sd) | desktop seat, grok2 alias | DESKTOP PLAN | same | **NEVER-CALLED** (idle desktop) | same |
| chatgpt_codex | Codex exec | long-horizon coding seat; jobs/codex-* contracts staged | DESKTOP PLAN ($0 marginal) | water mjs: "idle seat", no burn rows | **NEVER-CALLED** (idle desktop) | `codex exec "<task>"` |
| zcode | GLM Coding CLI | glm coding-plan CLI | DESKTOP PLAN | hands-off till 09-02 12:52Z (conservation law, MEMORY L13) | **POLICY-HELD** (deliberate, not waste) | after 09-02 12:52Z: route coding-plan work |

## 2. WATER WINDOWS vs burn ledger (receipt: `/board/water_windows.mjs`, `/board/water_ledger.jsonl`)

12 reservoirs defined: `deepseek_offpeak, zai_half_price, zai_credits, grok_a, grok_b, chatgpt_codex, zcode, deepseek_direct, ollama_local, groq_oss, cerebras, or_free`.
**Reservoirs WITH burn entries: 1 of 12** (`zai_credits`, 4 ledger rows 08-31: 0.75, rate-note 0, 2.65 correction, spend-policy 0 → $16.60 of $20 left).
**11 reservoirs carry no burn rows** — including all free tiers (groq_oss, cerebras, or_free) whose spend is invisible to the ledger by design (they burn quota, not dollars). Honest gap: quota-burn reservoirs are polled/trusted, never measured.

## 3. Rate-card anchors (measured, MEMORY L46–47)
- DeepSeek: 998 req/$0.786/91.74% cache-hit (08-31); month $93.34/69,335 req/98.01% cache; mid-month reprice ~Aug 16 (~2.28x effective); late-month $1.33/day; run-rate ~$40/30d.
- z.ai: glm-5.3-flash $0.075/$0.25/$0.015 per 1M in/out/cache — **cheapest measured interactive lane**; Lite $131.10/yr, Max $403.20/qtr cash; GLM family = $0-marginal backbone.
- Together: gpt-oss-120B $0.15/$0.60; DS-V4-Flash $0.14/$0.28 (cached $0.03, batch −50%).
- OpenAI/xAI/Anthropic/Google: **no measured receipts — marked unmeasured.**

## 4. TOP-5 HIGHEST-VALUE UNTOUCHED LANES (capability × cheapness × readiness)

1. **together** — cheapest measured paid path for bulk: DS-V4-Flash $0.14/$0.28, $0.03 cached, batch −50%; key in hand; one `model=` command; V4-eligibility inferred (flagged in MEMORY L46). Serves: batch-shaped bulk, swarm-scale overflow off direct DS.
2. **groq** — free 200K TPD bulk at 87.4% measured ok-rate; zero dollars; immediate. Serves: fast bulk scut that must not touch paid lanes.
3. **chatgpt_codex desktop seat** — already-paid subscription, $0 marginal, long-horizon coding; contracts staged (`jobs/codex-*`). This IS the operator-named GPT-utilization gap: capability present, zero calls this window, one `codex exec` away.
4. **openrouter** — free-lane fleet rotation (50→1000 RPD at ≥$10 bal); breadth play (llama-3.3-70b, r1:free); immediate.
5. **cerebras** — 1M TPD free at ~3000 tok/s (fastest measured class); 73.9% ok-rate; immediate.
*(Honorable: nvidia — free credits, 102-model catalog, 76.6% ok, held back only because billing is UNVERIFIED.)*

## 5. HONEST GAPS
- `MONEY_MAP_20260831.md` **does not exist on /board** (checked; referenced in MEMORY L46 as `staging/MONEY_MAP_20260831.md` — staging dir not found at /mag). The rate card lives only in MEMORY.md lines 46–47.
- 7 prefer_order lanes have no detail block — ambition without contracts.
- deepseek_overmind, google, anthropic: configured=true but key_present=false — dead weight in the order.
- Free-tier burn (groq/cerebras/OR quota) is invisible to the ledger — 11 of 12 reservoirs unmeasured.
- Trail grep for openai/xai/openrouter use was partial (two greps of large JSONL tails, not exhaustive).

## 6. SELF-ATTACK — inference vs measured
**MEASURED (billing/telemetry/counters):** DeepSeek $0.786/998req/91.74% + month-scale $93.34 (MEMORY L47); z.ai price points + plan cash ($131.10/$403.20) + $0.81/6d API (L47); Together price points (L46, fetched money-map page pre-reprice); fuel ok-rates groq 90/103, nvidia 59/77, cerebras 34/46, z_ai 56/72 (seat_corpus ts 08-29); water_ledger burn rows (this file §2).
**INFERRED (no receipt in hand):** every NEVER-CALLED status for openai/xai/openrouter/z_ai4/together is absence-of-evidence from partial trail greps; desktop seats grok_a/grok_b/codex "idle" rests on hook-tracked state + zero burn rows, not provider invoices; Together batch "≈19× cheaper" claim is arithmetic on measured price points, and its V4 batch eligibility is inferred; all rate caps (30RPM/1K RPD/200K TPD etc.) are operator receipts cited in water_windows.mjs, not re-verified today; the 7 unconfigured lanes' NEVER-CALLED is structural inference.
**Verdict:** cost *rates* are measured; *utilization* of 15+ surfaces is inferred. Next seat-job: provider billing exports for openai/xai to convert the two biggest inferences into receipts.
