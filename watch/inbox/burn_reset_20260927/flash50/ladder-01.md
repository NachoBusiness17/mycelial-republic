# ladder-01 - DRIVING LADDER COMPLIANCE AUDIT (estate-wide model dispatch)

2026-09-28 · mirror-ladder-01 · audit-only session, read-only live checks, no model spend, no code or state changed.

## The law audited against

Read this session, bytes not reports:

1. `memory/rib/RIB_DRIVING_LADDER_20260928.md` (full read). Three invariants:
   - **I1 ONLY HERMES IS FUNDED.** $180 Nous credits (glm-5.3-prime, qwen3.8-max-prime, Hermes-4 class) is the only funded tier. Anthropic keys in .env exist but are NOT funded, no Opus rung. DeepSeek no longer the funded workhorse. Free stealth lanes not funded at all.
   - **I2 THE LADDER CLIMBS.** scut/sensing: free stealth lanes, opportunistically, outputs SENSED never trusted, banked as findings. workhorse/judgment: the funded Nous tier. Sensing is never substituted for judgment; an answer is not an answer until the funded tier or the bytes verify it.
   - **I3 REMEMBER BEFORE RUNNING** (boot order; adjacent, not dispatch).
2. `memory/rib/RIB_FREE_USAGE_POLICY_20260823.md` (full read): free = opportunistic sensing, never forced workhorse; its own routing ladder names "DeepSeek (funded)" as workhorse. The 09-28 rib explicitly supersedes that rung ("updates its funded rung, DeepSeek era -> Nous credits era"). Every DeepSeek-as-workhorse line below is therefore stale law, not active law.
3. `AGENTS.md` driving ladder bullet (workspace instructions): same three invariants, receipt `memory/rib/RIB_DRIVING_LADDER_20260928.md`.

Operator quote that minted the rib (cited in the rib itself): "those aren't funded only hermes". The second operator phrase in this ask, "stop defaulting to Chinese models", audited as: defaulting to UNFUNDED free Chinese-family lanes (z.ai cache lanes, moonshot, dashscope, free OpenRouter stealth rows) in place of the funded tier. Nuance recorded: the funded catalog itself is Chinese-family (z-ai/glm-5.3-prime, qwen/qwen3.8-max-prime) but rides metered Hermes keys, so model family is not the violation; lane funding is.

## Method

- Endpoint census: `git grep -Iil` over tracked `*.py *.json *.yaml *.yml *.ps1 *.js *.toml *.cmd *.sh` for API hosts. Host hit counts (tracked files, all dirs incl. receipts): api.z.ai 174, openrouter.ai 142, api.deepseek.com 100, api.groq.com 71, api.together.xyz 31, generativelanguage.googleapis.com 29, api.nousresearch.com 24, api.anthropic.com 21, api.openai.com 20, api.moonshot.ai 19, api.x.ai 2, api.mistral.ai 1, api.cohere.ai 1, api.cerebras.ai 1.
- Code-surface restriction: same grep over `mag/ tools/ scripts/ bridge/ harness/ agents/ backend/ dashboard/*.py main.py` returned 67 active-code files (full list inspected; the receipt-bearing dirs docs/, corpus/, memory/, watch/ excluded from verdicts).
- Full reads: `mag/auth_switchboard.py`, `mag/free_tier.py`, `mag/router.py` (route core 595-784), `tools/stealth_driver.py` (lanes + t_work + gates), `configs/providers.yaml` (defaults + nous/nous_api/deepseek blocks), `state/hermes_routing.json`, `mag/hermes_steering.py` (dispatch core), `mag/offerings.py` (z_ai/coding_plan/vision blocks), `mag/ox_swarm.py` (roster), `mag/aos_agent.py` (model default), `mag/seat_dispatch.py`, `mag/subscriptions.py`, `mag/nervous_system.py`, `mag/seat_corpus.py` (anthropic refs), `harness/glm_coder.py`, `harness/opencode_coder.py`, `models/providers.py` (anthropic adapter).
- .env: KEY NAMES read only (`grep -oE "^[A-Z_0-9]+=" .env`), values never printed except two non-secret model-default strings (AOS_AGENT_MODEL, OPENROUTER_MODEL). Secrets law honored.
- Telemetry censuses (stdlib json, no network): `memory/runs/hermes_dispatch_log.jsonl` (98 rows), `memory/runs/fuel_feed/lane_profile.jsonl` (542 rows), `memory/workflows/REGISTRY.jsonl` (30 rows).
- Live read-only probes (repo venv `.venv/Scripts/python.exe`, no network calls in these code paths: router.route and free_tier.status/route read configs/env/local telemetry only):
  - `mag.router.route('refactor the payment parser module and run the tests')` → `{"seat": "remote", "provider": "deepseek", "mode": "queue", "launch": true, "executable": true}`, why includes `execution=heavy, pick=deepseek`, hint "DeepSeek tool loop - multi-step coding."
  - `python -m mag.free_tier status` → 10 surfaces alive incl. `nous: key_present True, ok_rate None`.
  - `python -m mag.free_tier "reason deep frontier"` → `["ox", "coding_plan"]`.
  - `python -m mag.free_tier "strong bulk research judgment"` → `["z_ai3", "groq"]`.
  - (first attempt `python -m mag.free_tier route "reason deep frontier"` was a misfire: argv[1] is the intent, so it routed intent "route" → `["z_ai3","groq"]`; recorded so the numbers above are not confused with it.)
- Not run (stated, not guessed): no live balance probe of any provider (auth_switchboard probe hits api.z.ai only and was not executed; no Nous/DeepSeek/OpenRouter balance endpoint call was made), no live model dispatch, no pytest (audit has no code change).

## VERDICT: NOT COMPLIANT

The ladder exists as prose (AGENTS.md bullet, the rib) and is encoded in exactly ONE organ (`tools/stealth_driver.py`), but the estate's dispatch infrastructure contradicts it at the default layer, and the practice ledger shows the funded tier has never been climbed once.

## Findings

### F1. The default climb has no funded rung at all
`configs/providers.yaml:8-44` `defaults.prefer_order`: ollama → z_ai ("FREE cache-mined GLM ... the default for heavy agentic windows", lines 14-16) → openrouter → groq → together → github_models → moonshot → fireworks → cohere → hf_router → dashscope → **deepseek "PAID fallback" (line 37)** → deepseek_overmind (38) → **anthropic (39)** → openai (40) → xai (41). The word `nous` appears nowhere in prefer_order. The `nous` provider block exists at `configs/providers.yaml:150-168` (base_url inference-api.nousresearch.com/v1, keys HERMES_API_KEY_1/2, models z-ai/glm-5.3-prime, qwen/qwen3.8-max-prime, fireworks/ember-1) but is commented "the LAW-11 credits-over-failure RESCUE lane" - registered, never ranked. I1 violated at the config layer: the two rungs it explicitly defunds (DeepSeek workhorse, Anthropic) are exactly the paid rungs of the default climb.

### F2. Anthropic is a wired, ranked lane though unfunded
- `configs/providers.yaml:39` ranks anthropic in the default climb.
- `models/providers.py:418-419` routes `anthropic_messages` kind to `_chat_anthropic`; `models/providers.py:883-913` implements the live chat call to `https://api.anthropic.com/v1` with `anthropic-version: 2023-06-01` and ANTHROPIC_API_KEY. The key exists (`.env` names `ANTHROPIC_API_KEY`, `ANTHROPIC_API_KEY_2`; names read, values not echoed).
- `models/providers.py:747-748`: tool loop refuses anthropic with "use deepseek" - both sides of that message name retired or unfunded rungs.
- `mag/router.py:738` and `:742` put `anthropic` inside the heavy-execution prefer lists.
- `mag/subscriptions.py:132-134` already carries the honest row: "Key exists but NO usage in our ledger (claude CLI now points at GLM coding..." - the estate KNEW anthropic was unfunded and still ranks it as a dispatch lane.
I1 violated: the rib names these keys unfunded, no Opus rung.

### F3. The live router sends judgment work to DeepSeek today
`mag/router.py`:
- `:617-618` `heavy_code` → seat "deepseek" by default.
- `:698` / `:701` local-janitor preference ladders rank `deepseek, deepseek_overmind` as the conservative workhorse rung.
- `:734-742` heavy execution prefer `["vast", "deepseek", "deepseek_overmind", "anthropic"]` or `["deepseek", "deepseek_overmind", "anthropic", "vast"]`.
- `:764-768` failure hint literally instructs "Set DEEPSEEK_API_KEY (or vast/openrouter) - heavy work cannot run".
- `:1010-1031` heavy_design keywords → provider "deepseek".
- Hermes path exists (`:34-40` markers, `:605-607`) but `:673-675` parks it: mode `defer_hermes`, hint "Hermes is parked - explicit opt-in only".
LIVE PROOF (run this session): `route('refactor the payment parser module and run the tests')` returned provider=deepseek, executable=true, hint "DeepSeek tool loop". I1 and I2 violated in the live path on the day after the rib landed.

### F4. The funded tier is unreachable through the routing organ
`mag/free_tier.py`:
- `:86-93` classifies `nous` as a FREE surface (FREE_SURFACES list) with kind "aggregator", best_for strong_bulk/research.
- `:166-176` intent vocabulary has no "judgment"/"verify"/"workhorse" keyword; judgment intents fall into the cheap/daily/bulk branch (`:170-171`) or reasoning branch (`:168-169`).
- `:168-169` reasoning branch picks kinds `("reasoning","frontier","strong")` - "aggregator" is not in the tuple, so the alive, keyed nous surface can never be returned for a judgment intent.
LIVE PROOF (run this session): `route("reason deep frontier")` → `["ox", "coding_plan"]` (ox is the dying free stealth seat, `:75` "GOING AWAY (429 upstream)"; coding_plan is the z.ai Lite plan). `route("strong bulk research judgment")` → `["z_ai3", "groq"]` (cache-mining + fast free lanes). The funded tier is invisible to the climb. I2 violated at the router-of-last-resort.

### F5. stealth_driver's judgment rungs are Opus and GPT on OpenRouter
`tools/stealth_driver.py`:
- `:236-238` tier "judgment" → `anthropic/claude-opus-5.5` via OPENROUTER_API_KEY (account 1).
- `:240-242` tier "judgment" → `openai/gpt-6-astra` via OPENROUTER_API_KEY_2.
- `:208-209` states its own law: "The climb for judgment items: claude-opus-5.5 / gpt-6-astra on the funded OpenRouter account."
That "funded OpenRouter account" claim is the 08-23 era truth (nacho OpenRouter funded per RIB_FREE_USAGE_POLICY_20260823 lineage and providers.yaml:175-176 comment). The 09-28 rib supersedes it: ONLY Hermes/Nous funded, no Opus rung. The file carries the NEW law two paragraphs later (`:331-334` "THE LADDER (operator-corrected 2026-09-28)... items tagged judgment/scarce5 climb to those rungs" and `:486-489` the sensed-never-done gate citing RIB_DRIVING_LADDER_20260928) but kept the OLD rungs. Internal contradiction in the freshest driver in the estate.
Compliant parts of the same file: `:244-246` scarce5 = nous z-ai/glm-5.3-prime on HERMES key; `:331-344` tier-matched lane pick; `:483-492` rows flip to done only via funded-tier verification (sensed_ts + status "sensed"); `:495-503` POST host allowlist; `:272-278` subprocess spawn with `creationflags=CREATE_NO_WINDOW` on win32 (harness law honored).

### F6. Practice: the funded tier has never been climbed once
`memory/runs/hermes_dispatch_log.jsonl` census (98 rows, 2026-09-07 to 2026-09-26): 35 rows name a model and ALL 35 are `inclusionai/ling-3.0-flash-sante:free` (the $0 stealth test model, exits: 24 zero / 11 one); 63 rows carry empty model, which per `state/hermes_routing.json` lanes.default resolves to "custom (z.ai), glm-5.3-flash, cheap default for all hermes.exe jobs"; zero rows on glm-5.3-prime or qwen3.8-max-prime. Fuel telemetry `memory/runs/fuel_feed/lane_profile.jsonl` (542 rows): groq 202, cerebras 110, nvidia 95, ox 93, z_ai 76, openrouter-a1 34, openrouter-a2 18, together 2, z_ai3 2 - zero nous rows. Wiring says rescue-lane; practice says never climbed. I2 violated in fact, not just in code. (Most recent dispatches also exit=1: the 09-26 kabuki rows.)

### F7. Chinese-model defaulting is the estate norm (unfunded lanes)
- `configs/providers.yaml:14-16` z_ai GLM is THE default for heavy agentic windows; moonshot (`:30`) and dashscope (`:35`) hold standing free-lane slots.
- `mag/fanout.py:35` `DEFAULT_MODEL = "glm-5.3-flash"` (host allowlist `:39` = {api.z.ai, api.deepseek.com}).
- `mag/lane_runner.py:624` and `:664` cage lane pinned glm-5.3-flash on z_ai3 Lite.
- `mag/lite_scale.py:25` `MODEL = "glm-5.3-flash"`.
- `state/hermes_routing.json` lanes.default = z.ai glm-5.3-flash "cheap default for all hermes.exe jobs" (2026-09-07 authority, never updated).
- `.env` (values read, non-secret): `AOS_AGENT_MODEL=deepseek/deepseek-v4-flash`, `OPENROUTER_MODEL=stealth/ox-alpha`. `mag/aos_agent.py:82-88` reads exactly that pin: "routes through DEEPSEEK by default (meaningful, cheap, ~$0.00003/turn)".
- `mag/ox_swarm.py:76` fleet row: deepseek/deepseek-v4-flash fallback, plus `openai/gpt-5` and `x-ai/grok-4` as paid seats (`:78-84`) - none of those three are funded under I1.
- `mag/seat_dispatch.py:88-113`: three roster rows on deepseek/deepseek-v4-flash, justified "deepseek pennies ONLY - ZAI keys 2-4 are 429".
Nuance applied: family is not the crime (the funded catalog is glm/qwen on Hermes keys); unfunded-lane-as-default is. Every default above points at an unfunded or retired rung.

### F8. Stale funded-truth strings that will re-teach the violation
- `mag/ox_swarm.py:12` "deepseek : PAID, $50 balance ... <- reliable workhorse". The $50 balance claim has no receipt in the repo (state/hermes_routing.json explicitly records that the Nous balance endpoint is not exposed and mapping is by operator word; no DeepSeek balance receipt exists anywhere I grepped). OWED if ever cited as spend authority.
- `mag/seat_dispatch.py:88-113` deepseek pennies as standing roster.
- `mag/offerings.py:130-135` vision organ rides DEEPSEEK_API_KEY ("DeepSeek Vision deepseek-v4-flash-vision-exp") - the estate's only seeing-organ sits on a retired rung.
- `mag/offerings.py` coding_plan "best_for: frontier_coding, deep_work, reliable_pool" - z.ai Lite advertised as the reliable deep-work pool, the exact phrase the ladder reassigns to the funded tier.
- `configs/providers.yaml:11` comment "paid deepseek is the FALLBACK (reliable workhorse)".
- RIB_FREE_USAGE_POLICY_20260823 "DeepSeek (funded)" line is corrected only by the 09-28 rib's supersede note; the old rib's own body still says it.

### F9. z.ai coding-plan boundary case: needs an operator ruling (not adjudicated here)
The seat's own harness account is `account:zai-individual-coding-plan` (this session's host; `memory/workflows/REGISTRY.jsonl` 30 rows, none record a subagent_model, so workflow children ride the same account). Product-side, `harness/glm_coder.py:29` (api.z.ai/api/anthropic, GLM_CODING_API_KEY), `harness/opencode_coder.py:5` (api.z.ai/api/coding/paas/v4), `mag/free_tier.py:80-82` coding_plan "NOT free but cheap+cache-hit", `mag/auth_switchboard.py:52` probes api.z.ai for the seat's own identity. These are operator-paid plans that predate the rib and are not named by it. The rib defunds Anthropic and DeepSeek and free stealth lanes; it is silent on the z.ai coding plans. Flagged OWED: does "only Hermes is funded" retire the z.ai coding plans as a dispatch rung, or do they count as operator infrastructure (the coding seat itself) outside the ladder? This audit does not guess.

### F10. Sensing surfaces audited compliant (as sensing)
- `tools/stealth_fanout.py:40-53`: free stealth rows via OpenRouter + the two prime models via Nous keys (N1/N2), output banked with lane+model provenance.
- `tools/openrouter_free_gate.py:1-23`: B2-295 verify-then-add gate for :free ids, one live ALIVE probe per id (sensing of lane liveness, max_tokens 16).
- `mag/improve.py:446`: ~15 one-token pings per deduped (base_url, model, key) triple, bounded scouting.
- `tools/task_wall.py`, `tools/model_bakeoff.py`, `tools/stealth_sweep.py`: probe/bakeoff instruments (groq llama-3.3, nvidia glm/ds, deepseek-chat rows) - measurement seats, not trusted-output seats.
- `mag/lite_guard.py`: daily pacing ceiling on the z_ai3 Lite lane (operator emergency override only).
- `mag/auth_switchboard.py`, `mag/nervous_system.py:34`, `mag/seat_corpus.py:178-184`, `scripts/sync_env_from_scaffold.py`: credential/registry machinery, listing anthropic among tracked keys, no dispatch on its own.
- Workflows: 30 REGISTRY rows, dispatch shape on the harness account; `tools/workflow_gate.py` enforces dogfood laws, not model tier (no ladder enforcement in the gate - noted, not counted a violation since the gate's contract is shape, not spend).
- Scheduled tasks (AGENTS.md): MagCensusPatrolDaily, MagFtsIndexDaily, MagImproveDaily are local/FTS/bounded-probe; no metered model spend. Not re-verified live this session (schtasks not run; taken from AGENTS.md text only).

## Patterns (12)

1. **Default-layer ladder absence** - providers.yaml prefer_order ranks retired/unfunded paid rungs and omits the funded one entirely (F1).
2. **Live router violation** - router.py routes real heavy work to deepseek today, proven by execution, not by reading (F3).
3. **Funded tier registered but unreachable** - nous exists as a provider and a free_tier surface yet no intent path can return it; zero climbs in 98 dispatch rows and 542 telemetry rows (F4, F6).
4. **Hermes parked by default** - the one funded seat sits behind explicit opt-in markers while unfunded defaults fire (F3).
5. **Judgment rungs on the wrong keys** - stealth_driver judgment = opus/gpt on OpenRouter under a "funded OpenRouter account" claim the rib superseded (F5).
6. **Sensed-never-done gate exists and is correct** - stealth_driver :486-489 is the model the rest of the estate should copy (F5).
7. **Tier-matched lane pick exists in exactly one driver** - the 09-28 correction landed in one file only (F5).
8. **Stale funded-truth prose** - "$50 balance reliable workhorse", "deepseek pennies ONLY", "reliable_pool" advertise retired rungs to future seats (F8).
9. **Chinese-family defaults on unfunded lanes** - z.ai cache GLM, moonshot, dashscope, deepseek, free stealth rows as standing defaults across at least seven organs (F7).
10. **Unfunded adapter wired and ranked** - _chat_anthropic callable end to end; anthropic ranked in two prefer lists while the estate's own subscription ledger says no-usage (F2).
11. **Unreceipted balance claims** - spend authority asserted ("$50", "$220 armed") without a verifiable balance surface; OWED discipline required before any spend citation (F8, state/hermes_routing.json verified block).
12. **Boundary case left open by the law itself** - z.ai coding plans (seat harness + glm/opencode coders) neither funded nor defunded by the rib; needs one operator sentence (F9).

## Fix list (ordered, none applied this session)

1. `configs/providers.yaml`: insert `nous` into prefer_order as the paid/judgment rung above deepseek; mark `anthropic` dormant-unfunded citing RIB_DRIVING_LADDER_20260928.md; rewrite the line-11 free-first comment.
2. `mag/router.py`: heavy/judgment default → hermes/nous; drop anthropic from both prefer lists; repoint the `:768` hint from DEEPSEEK_API_KEY to HERMES_API_KEY_1.
3. `mag/free_tier.py`: split nous out of FREE_SURFACES into a FUNDED surface with kind "judgment"; add judgment/verify intents mapping to it.
4. `tools/stealth_driver.py`: swap judgment rungs claude-opus-5.5 / gpt-6-astra → nous z-ai/glm-5.3-prime + qwen/qwen3.8-max-prime; keep scarce5; update the :208-209 law line.
5. Rewrite the stale strings (F8 list) so the next seat reads funded truth.
6. One operator ruling on the z.ai coding-plan boundary (F9), then fold the answer into providers.yaml as code-as-law.
7. Fold RIB_DRIVING_LADDER_20260928.md into the boot-warm list check: any organ whose prefer list lacks nous after the fix fails a grep gate (one-line tool, owed).

## Verification debt (what this audit did not do)

- No provider balance was probed live (I1's "$180" figure taken from the rib and AGENTS.md text, not from an API).
- No ladder-compliant dispatch was exercised (the funded tier was not called; proving it works end to end is a separate live burn).
- schtasks statuses for the three daily tasks not re-run; AGENTS.md text trusted for the scheduled-surface row only.
- Untracked working-tree files were not grepped (git grep covers tracked files; the git-status snapshot lists many modified tracked files which ARE covered).
