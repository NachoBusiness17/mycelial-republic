# HERMES SETUP — 2026-09-07 (Nous Portal wired as the control-surface body)

> **[AUDIT-TYPED 2026-09-08]** status: LIVE · claims: hermes.exe is wired to Nous Portal via the v12 providers dict + UA header, and NOUS HELM dispatch is receipted end-to-end at $0 — SUPPORTED (receipt #4 session 20260907_080147_66313a, both keys HTTP 200) · falsifier: a hermes dispatch via the nous-<account>/<model> prefix fails, or resolve_startup_model_route returns None on the wired config

**Verdict:** LIVE + RECEIPTED. `NOUS HELM LIVE` end-to-end: Mag helm → hermes.exe →
Nous inference API (S:D account, $0 free model). Hermes is the incoming control
surface as OpenClaw retires (plan: watch/inbox/PIPELINE_RIGHT_PLAN_20260907.md §C).

## The operator's state (grounded)

- **Two Nous Portal accounts:** S:D = **$220** (armed work budget), Nacho Business =
  **$10** (petty). Keys in repo .env as HERMES_API_KEY_1 (= Nacho $10) and
  HERMES_API_KEY_2 (= S:D $220) — mapping by operator word; the API exposes no
  balance endpoint (probed: /models 200 both keys, balance paths 404).
- Hermes = Nous Portal's Hermes Agent + local hermes.exe v0.21.0 body
  (C:\Users\foste\AppData\Local\hermes), already a Mag seat (NACHO MASK persona,
  helm organ mag/hermes_steering.py from 09-07 morning).

## The wiring (final shape — after stealing hermes's own tests)

- **hermes config.yaml**: `model.provider: custom` + Nous base_url +
  `api_key: ${NOUS_SDD_API_KEY}` + **`model.default_headers: User-Agent:
  hermes-agent/0.21.0`** (clears the Cloudflare 1010 wall the SDK default UA hits);
  **`providers:` v12 dict** (nous-sdd / nous-nacho, `key_env` names) AND legacy
  `custom_providers:` list — the dict is what startup routing consumes. Backup:
  config.yaml.bak-nouswire-20260907.
- **hermes .env**: NOUS_SDD_API_KEY / NOUS_NACHO_API_KEY added (its own secret
  store; key material never in config.yaml or logs).
- **helm (mag/hermes_steering.py)**: `--account sdd|nacho` (default sdd) injects
  NOUS_<ACCOUNT>_API_KEY and prefixes the model `nous-<account>/<model>` —
  **selection is by MODEL PREFIX, never --provider** (the flag makes
  resolve_startup_model_route return None). $0 default model:
  inclusionai/ling-3.0-flash-sante:free; big brains pass --model (catalog: 390
  models incl. openai/gpt-6-astra, anthropic/claude-fable-5.1, google/gemini-3.8-flash).
- **Routing authority:** state/hermes_routing.json (accounts, budgets, lanes,
  spend rules).

## Receipts

1. API probe: both keys HTTP 200 on /v1/models (390 models), UA hermes-agent/0.21.0.
2. Free-lane direct call: HTTP 200, content "Hi there", **cost: 0** (BYOK :free model).
3. Body smoke (z.ai-era config): "HERMES READY", exit 0, 26s — but note below.
4. **Wired Nous dispatch: "NOUS HELM LIVE", exit 0, 28.8s, session
   20260907_080147_66313a** (memory/runs/hermes_jobs/20260907T120214Z.md).
5. Handshake (LAW-14): gate = hermes-nous-$220, unlocked 2026-09-07 ~10:30Z by the
   operator's top-up + screenshots, first_use = receipt #4 same hour.

## The five attempts that failed (steal-lesson, per operator: "steal what other
people do — ponytail and lessig")

1. `--provider nous-api` → unknown (example newer than binary).
2. `--provider nous` + env key → "not logged into Nous Portal" (OAuth-gated).
3. Pooled api-key credential → same OAuth gate.
4. `--provider custom:nous-sdd` / bare `nous-sdd` → Unknown provider (the gate
   checks the registry; named custom providers don't live there).
5. Legacy `custom_providers:` list + `custom:<name>/<model>` prefix → route not
   consumed oneshot; fell through to OpenRouter (404 their catalog).

**Lessig lens:** the executable law was `resolve_startup_model_route` all along —
"an explicit --provider returns None"; "provider/model strings are consumed only
for providers present in user config" where **user config = the v12 `providers:`
dict**. **Ponytail lens:** the hypothesis that finally taught was stolen, not
derived — hermes's own test file carried the working shape
(tests/agent/test_auxiliary_user_default_headers.py: custom_providers list +
model.default_headers). Steal the tests, not the docs.

## Honest notes

- **The pre-Nous "HERMES READY" smoke rode OpenRouter, not z.ai**: this binary
  doesn't know `provider: custom`'s old meaning in the MENU (chat path accepts
  it) and had auto-fallen back to OpenRouter. Yesterday's "Lite key wired" was
  therefore not the live lane. Now moot: default = Nous S:D. If a z.ai lane for
  hermes is wanted later, the source ships a native `zai` provider plugin.
- Portal **OAuth login** (hermes model → Nous Portal) remains undone — only
  needed for portal-managed cloud agents ("DEPLOY AN AGENT"); the API-key lane
  covers dispatch/steer/jobs. Operator finger-step when wanted.
- Named-provider duplication (providers: dict + custom_providers list both
  define nous-sdd/nous-nacho) is deliberate: the dict feeds startup routing, the
  list feeds the interactive menu; get_compatible_custom_providers() dedups.

## OpenClaw succession (what Hermes absorbs)

Control-surface body: DONE (this card). Board/4chan hooks + PATCHES queue + the
tailscale surface: owned by PIPELINE_RIGHT_PLAN_20260907.md §C — retire openclaw
behind a compose profile only after those rehome or are declared retired.
