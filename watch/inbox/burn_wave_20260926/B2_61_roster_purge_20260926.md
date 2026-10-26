# B2-61 receipt: providers.yaml roster purge, live-probe set (2026-09-26)

## Verdict

STEAL. All four dead lanes from B2-04 were re-verified live today with one call
per change BEFORE writing, then purged in configs/providers.yaml (config-only):
openrouter stale :free ids dropped with one chat-verified repoint; nvidia
dormant with the 18-id roster dropped; gemini dormant with both roster ids
dropped; mistral dormant with its default repointed to the catalog-present id.
B2-63 landed a gemini auth verdict mid-lane; preserved verbatim and built on,
not overwritten. Validation green: yaml parse, estate load_providers (28
providers), doctor check_provider_endpoints classifies all four DORMANT.

## Evidence

- openrouter (configs/providers.yaml:144-156): "- cohere/north-mini-code:free
  # 2026-09-26 repoint (B2-61): chat 200, content "ALIVE", on
  OPENROUTER_API_KEY". Live gate: GET /api/v1/models 200, 458 models,
  old_ids_absent all true for meta-llama/llama-3.3-70b-instruct:free,
  google/gemma-2-9b-it:free, deepseek/deepseek-r1:free
  (B2_61_verify_results.json). qwen/qwen3.8-27b:free is catalog-present but
  live 429 "temporarily rate-limited upstream ... limit_source":
  "upstream_provider_shared_pool", so it was NOT chosen.
- nvidia (providers.yaml nvidia block, dormant: true): live 410 body "The model
  'deepseek-ai/deepseek-v4-flash-0731' has reached its end of life on
  2026-09-21T08:00:00Z and is no longer available."; B2-04 had 404 "Function
  '23bd454d-...': Not found for account". Roster dropped, none guessed.
- gemini (providers.yaml gemini block, dormant: true after B2-63's comment):
  live 404 "This model models/gemini-2.0-flash is no longer available. Please
  update your code to use models/gemini-3.8-flash"; live catalog GET 200, 61
  ids, contains neither gemini-2.0-flash nor gemini-1.5-flash; native
  generateContent 401 UNAUTHENTICATED "Expected OAuth 2 access token...".
- mistral (providers.yaml mistral block, dormant: true): old default
  mistral-large-latest live 403 "This model is not available in your
  subscription tier" (code 1910) and absent from the live catalog (46 ids);
  mistral-small-latest chat 429 with "x-ratelimit-limit-req-minute: 0" (code
  1300), reproducing B2-04 byte for byte. Default repointed to
  mistral-small-latest.
- Routing enforcement: pick_provider (models/quota.py:382-397) never reads
  dormant, so nvidia/mistral/gemini were pulled from prefer_order and all
  routing lists (scut, public_summarize, hard_code, hard_reason, default).
- Fact filed: .env spells the mistral key Mistral_API_KEY (mixed case); the
  lane only resolves because Windows env lookup is case-insensitive.

## Work done

1. Read B2-04 receipt + raw probe JSONs; enumerated the four purge targets.
2. Wrote B2_61_verify.py (keys from .env, never printed, synthetic prompt
   only) and ran it: openrouter catalog + repoint probe, nvidia chat, gemini
   chat. Raw-body re-probes settled the repoint (qwen 429 vs cohere 200).
3. Follow-up live calls: mistral chat x2 + catalog (mixed-case key name found),
   gemini native 401 + catalog id dump. All results in
   B2_61_verify_results.json.
4. Applied 7 edits to configs/providers.yaml (openrouter roster, prefer_order
   x2, gemini, mistral, nvidia, routing). Two concurrent lane landings
   (B2-62 retry_overload, B2-63 gemini comment) hit mid-edit; re-read and
   preserved both.
5. Validation: yaml.safe_load + models.providers.load_providers pass; purge
   assertions pass; mag doctor check_provider_endpoints: all four DORMANT,
   openrouter REMOTE-UNVERIFIED, only alarm is the pre-existing mlx stub.
6. Ledger row appended via .venv python json.dumps; self-fed 3 briefs.

## Falsifier

Dies if: (a) rerunning B2_61_verify.py today does not reproduce the quoted
statuses (410 nvidia, 404/401 gemini, 403/429 mistral, 458-model openrouter
catalog); (b) any purged id answers 200 with content on the exact same id and
key; (c) providers.yaml fails load_providers or doctor shows any of the four
as anything but DORMANT; (d) cohere/north-mini-code:free stops answering while
still listed (its own comment carries the verification date; the stealth lane
note precedent applies).

## Bibliography closed

configs/providers.yaml (edited) · watch/inbox/burn_wave_20260926/
B2_61_verify.py + B2_61_verify_results.json (live bytes) ·
B2_04_provider_health_20260926.md + B2_04_probe_results*.json (prior causes) ·
B2_63_gemini_auth_20260926.md (concurrent gemini verdict, preserved) ·
models/quota.py pick_provider · mag/doctor.py check_provider_endpoints ·
memory/burns/LEDGER.jsonl (row appended) · QUEUE.md (B2-197..199 self-feed)
