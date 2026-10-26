# f-11 lane-health census (2026-09-28)

Item: read `configs/lanes.yaml` fully; for each lane: model, provider, rate limits, last used (from logs), alive?
All numbers below come from commands run in this session on 2026-09-28. No number is hand-copied.

## Source read

`configs/lanes.yaml` (159 lines, read in full). It defines four lanes (`lanes:` block, lines 7-25):
L0 local (backend ollama), L1 free_remote (backend openrouter), L2 specialist (backend grok_harness),
L3 human (backend wait). `default_lane: L0` (line 3). Plus a `local_models` role map (lines 27-40),
a `hermes` block (lines 49-54), a `grok_budget` block (lines 71-74), and a `gate_verdict_v2` judge
block (lines 110-158, judge seats `[local, flash, frontier]` - a verdict cascade, not a provider lane).

## Commands run (instruments)

1. `./.venv/Scripts/python.exe main.py probe-lanes` - the repo's own lane probe (`models/probe.py`):
   real L0 chat roundtrip, real L1 OpenRouter chat if key present, L2 binary-presence check (`harness_available()`), no L3 probe exists.
2. `./.venv/Scripts/python.exe -m mag.lane_probe --once` - the dedicated 3-provider pinger
   (`mag/lane_probe.py:22-41`: deepseek / zai / groq, 8-token pings, appends to `watch/lane_probe.jsonl`).
3. Full scan of `logs/usage.jsonl` (163,102 lines; 163,092 parse as JSON: L0 89,572 rows, L1 73,520 rows,
   L2 0 rows, L3 0 rows, 10 lines unparseable) - per-lane and per-provider last-use/success/failure tallies.
4. `models/registry.py inventory()` - Ollama up check and role-to-model presence.
5. Presence checks: `.env` key names (values never read), Windows User/Machine env var presence (bool only).
6. `memory/runs/hermes_dispatch_log.jsonl` scan (98 rows).
7. `watch/lane_probe.jsonl` history read (3 pre-existing rows, last run before today was 2026-09-02).

## Lane table

| Lane | Backend / provider | Model(s) | Rate limits (as configured) | Last used (log evidence) | Alive? |
|---|---|---|---|---|---|
| L0 local | ollama (`lanes.yaml:8-11`) | Role map `lanes.yaml:27-40`: clerk/router/orchestrator/voice `gemma:2b`; worker `qwen2.5-coder:7b`; desk_orchestrator/desk_conductor/critic/biographer `qwen-desk:latest`; embed `nomic-embed-text`. All 10 roles resolve and are present in Ollama (inventory run: `ollama_up: True`, every role `present=True`; 17 tags on the daemon) | No API rate limit. Hardware caps: `load_policy` sequential, `max_resident: 1` (`lanes.yaml:43-47`); envelope `ollama_context: 8192`, `ollama_max_loaded: 1`, never `35b+`/`70b` (`lanes.yaml:56-69`) | 89,572 rows since 2026-07-20T14:25:07Z. Today (2026-09-28 UTC): 25 rows, all ok. My probe-lanes run logged `role=router model=gemma:2b ms=18309` PONG at 21:44:22Z | ALIVE - PONG roundtrip today, 25/25 ok today |
| L1 free_remote | `lanes.yaml:12-17`: backend openrouter, `default_model: openrouter/auto`, `model_env: OPENROUTER_MODEL`, `never_tiers: [T0, T1]`. In practice the L1 slot carries a 15-provider fanout (see sub-table below; `action=provider_chat`) | Config model `openrouter/auto`; env override `OPENROUTER_MODEL=stealth/ox-alpha` (read from `.env`) shadows it and is DEAD | No numeric rate limit in `lanes.yaml`. Policy caps: `never_tiers: [T0, T1]` (line 16); `effort_tiers` block commented out (lines 104-108) so fanout admission uses built-in defaults; AGENTS.md DRIVING LADDER (2026-09-28) demotes free lanes to sensing-only, verification climbs to funded Hermes tier | 73,520 rows since 2026-07-20T15:33:04Z. Today: 77 rows, all ok (deepseek + z_ai3). Last row 2026-09-28T18:05:59Z deepseek ok | SPLIT: fanout ALIVE (today), but the lanes.yaml OpenRouter path is BROKEN as configured (see finding F1) |
| L2 specialist | `lanes.yaml:18-22`: backend grok_harness, `require_priority: true`. Escalation exec: `configs/mag.yaml:7 use_grok_harness: true`; binary probe `probe_l2()` in `models/probe.py:92-105` | n/a (harness runs the specialist CLI, no model id in lanes.yaml) | `grok_budget` (`lanes.yaml:71-74`): `max_escalations_per_day: 2`, `require_priority: true` (markers `[priority]`,`[grok]`,`[L2]`, lines 76-79), `attach_brief: true`. Adjacent cap on a separate surface: `configs/aos_grok.yaml:19 max_asks_per_day: 3` | 0 rows in `logs/usage.jsonl` ever (log born 2026-07-20; the escalate path writes `escalate_harness`/`handoff` rows at `mag/act.py:175-204` - none exist). Budget never consumed | ARMED BUT NEVER FIRED through the logged path: binary present (probe-lanes L2 `ok: true` today), 0 escalations in 70 days of log |
| L3 human | `lanes.yaml:23-25`: backend wait | none | none | 0 rows; no code writes `lane="L3"` anywhere (grep over `mag/*.py` + `main.py`: 0 hits) | NOT AN ACTIVE LANE - by design a wait state |
| hermes block (`lanes.yaml:49-54`) | code-team tool loop, `parked: false`, `not_router: true` | Dispatch log records e.g. `inclusionai/ling-3.0-flash-sante:free` via account `sdd`; `nous` provider rides `HERMES_API_KEY_1` and ran `z-ai/glm-5.3-prime` | Dispatch log has no rate limit in lanes.yaml; funding per AGENTS.md: $180 Nous credits, the only funded lane | `memory/runs/hermes_dispatch_log.jsonl`: 98 rows, 84 exit-0; last success 2026-09-19T09:02:27Z (kabuki); last activity 2026-09-26T09:03:28Z (exit 1 x3). Nous-provider success 2026-09-26T04:25:31Z glm-5.3-prime | ALIVE (idle 2-9 days): keys `HERMES_API_KEY_1/2` present in `.env`; last 3 kabuki dispatches exited 1 |

## L1 provider fanout sub-table (from `logs/usage.jsonl`, 73,520 `provider_chat` rows)

| Provider | Key env (evidence) | Rows / ok | Last success (UTC) | Last failure (UTC) | Verdict today |
|---|---|---|---|---|---|
| deepseek | `DEEPSEEK_API_KEY` (in `.env`) | 70,824 / 70,416 | 2026-09-28T18:05:59Z (deepseek-v4-flash) | 2026-09-20T08:49:11Z | ALIVE - carries 96.3% of all L1 traffic; fresh ping 562 ms OK today |
| z_ai3 | `ZAI_API_KEY_Lite` (in `.env`) | 613 / 246 | 2026-09-28T15:16:38Z (glm-4.5-flash) | 2026-09-26T13:46:57Z | ALIVE - success today; 40% row ok-rate |
| z_ai | `ZAI_API_KEY` (in `.env`) | 570 / 338 | 2026-09-16T02:08:13Z | 2026-09-22T04:46:30Z | ALIVE but idle 12 days - fresh ping of this exact key returned OK 969 ms today |
| groq | `GROQ_API_KEY` + `GROQ_API_KEY_2` (in `.env`) | 536 / 271 | 2026-09-26T13:38:04Z (key_idx 0, multi_key true) | 2026-09-26T13:35:20Z | UNRESOLVED - last success 2 days ago, but the direct `mag.lane_probe` ping of `GROQ_API_KEY` got HTTP 403 both on 2026-09-02 and today; which of the two keys is valid is not determinable from these runs |
| openrouter | `OPENROUTER_API_KEY` (+ `_2`) in `.env` | 185 / 152 | 2026-09-26T19:55:57Z (`openrouter/auto`) | 2026-09-18T00:47:32Z | KEY VALID, CONFIG MODEL DEAD - `openrouter/auto` worked 2 days ago; `OPENROUTER_MODEL=stealth/ox-alpha` 404s today (F1) |
| cerebras | `CEREBAS_API_KEY` + `_2` in `.env` | 165 / 155 | 2026-09-07T07:30:13Z | 2026-09-26T13:37:14Z | IDLE 21 days, last contact a failure |
| nvidia | `NVIDIA_API_KEY` - ABSENT from `.env` and Windows User/Machine env (presence check false; only unrelated `NVIDIABuild`/`NVIDIABuild2` exist) | 100 / 86 | 2026-08-24T23:01:00Z | 2026-08-24T22:55:30Z | DORMANT - no key configured, cannot fire |
| xai | `XAI_API_KEY` present in Windows User env only (not `.env`); `GROK_API_KEY`/`GROK_API_KEY_2` also in `.env` | 93 / 47 | 2026-08-09T16:03:02Z | 2026-08-23T21:54:33Z | IDLE 50 days, last contact a failure |
| z_ai2 | `ZAI_API_KEY_2` in `.env` (mapping inferred from sibling naming; row meta carried no key_env) | 202 / 74 | 2026-09-07T07:25:08Z | 2026-09-16T17:10:59Z | IDLE 21 days |
| deepseek_overmind | `DEEPSEEK_OVERMIND_API_KEY` - ABSENT from `.env` and Windows env | 156 / 156 | 2026-08-09T17:12:42Z | never failed | DORMANT - no key configured |
| together | `TOGETHER_API_KEY` (+ `TOGETHER_API_KEY2`) in `.env` | 12 / 11 | 2026-09-07T00:32:53Z | 2026-08-25T12:21:12Z | IDLE 21 days |
| openai | `OPENAI_API_KEY` in `.env` | 21 / 0 | never succeeded | 2026-08-28T23:31:41Z | DEAD - 0/21 ever |
| nous (Hermes-funded) | `HERMES_API_KEY_1` (row meta) | 3 / 3 | 2026-09-26T04:25:31Z (z-ai/glm-5.3-prime) | never failed | ALIVE, tiny sample - the funded workhorse path |
| z_ai4 | `ZAI_API_KEY_3` in `.env` (mapping inferred; meta carried no key_env) | 5 / 2 | 2026-08-26T15:57:54Z | 2026-08-27T11:15:04Z | IDLE 32 days |
| gemini | `GEMINI_API_KEY`/`GOOGLE_API_KEY` in `.env` | 5 / 0 | never succeeded | 2026-07-28T09:50:47Z | DEAD - 0/5 ever |
| test_provider | test fixture | 30 / 30 | 2026-08-05T01:28:16Z | never | Not a real lane (test harness rows) |

## Findings

- **F1 - L1's configured OpenRouter model is a corpse.** `OPENROUTER_MODEL=stealth/ox-alpha` (`.env`)
  shadows `default_model: openrouter/auto` (`lanes.yaml:18`). probe-lanes today: HTTP 404, body:
  "Thank you for participating in the Stealth Ox Alpha testing period. This model was ZAI's GLM-5.3 Flash.
  Use it now: https://openrouter.ai/z-ai/glm-5.3-flash". The key itself is valid (152/185 historical ok,
  last success 2026-09-26T19:55:57Z). Fix is one env line; nothing in the repo warns that the env override
  beats the yaml default.
- **F2 - L2 has never been used through its own instrumented path.** 70 days of usage log, zero L2 rows,
  while `use_grok_harness: true` (`configs/mag.yaml:7`) and the harness binary answers present. The 2/day
  budget (`lanes.yaml:72`) has never been spent. Either the escalate node never fires, or escalation happens
  on surfaces that bypass `mag/act.py` logging; both readings say the L2 lane's usage telemetry is dark.
- **F3 - lane_probe.py and the fanout disagree on groq.** The dedicated pinger (`GROQ_API_KEY`) got 403 on
  09-02 and today; the fanout logged key_idx-0 successes as recent as 09-26 with `multi_key: true`. One of
  the two groq keys is dead and the fleet's two instruments do not agree which.
- **F4 - two providers are configured in code but keyless on this machine** (nvidia, deepseek_overmind):
  their env key names exist nowhere (checked `.env` names, Windows User and Machine scopes). They cannot
  fire; their rows are all pre-2026-09.
- **F5 - gemini and openai lanes never worked** (0/5 and 0/21). They are config-weight without a single
  success in the log's lifetime.
- **F6 - the real L1 is deepseek + z.ai.** 96.3% of L1 rows are deepseek; the only two providers with
  successes today are deepseek and z_ai3. `ZAI_API_KEY_Pro` sits in `.env` with zero logged rows.
- **F7 - L0 is fully healthy but the probe surfaces differ.** Router roundtrip is `gemma:2b` per config and
  per my probe (PONG, 18.3 s cold). A separate `role=probe` surface (only call site: `mag/territory_solver.py:98`)
  logged `model=gemma4:latest ms=69719` at 19:01:38Z today - a different model than the lanes.yaml router,
  on a role name the registry does not define (`models/registry.py:14`), so it resolves through fallbacks.

## Caveats / not run

- Aliveness for openrouter/auto, cerebras, together, xai, z_ai2, z_ai4 was judged from log recency and key
  presence, not a live ping (the repo's pinger covers only deepseek/zai/groq; probe-lanes covers only the
  configured OpenRouter model). No spend-heavy live checks were invented for them.
- The 404/403 bodies are quoted from the probes' own outputs; I did not otherwise contact OpenRouter or Groq.
- `z_ai2`/`z_ai4` key-env mapping is inferred from sibling naming (their row meta carried no `key_env`);
  marked as inferred, not read.
- L2 "armed" claim rests on the binary-presence probe (`which/path probe via harness_available()`), not on a
  real escalation (which would spend the 2/day budget).

## Bank

This file: `watch/inbox/burn_reset_20260927/flash50/f-11.md`.
Byte-identical mirror per the ask's named table path: `watch/inbox/burn_reset_20260927/flash50/lane-health.md`.
