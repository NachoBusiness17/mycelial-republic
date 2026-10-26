# B2-129 receipt: capture the gemini Bearer 401 (2026-09-26)

## Verdict

LANDED, captured the same day instead of next run. The script fires generateContent twice (native x-goog-api-key vs Authorization: Bearer) with a synthetic "ping" and persists both full bodies to B2_129_gemini_auth_bodies.json. The Bearer 401 body PROVIDER_HEALTH quoted without proof is now on disk byte-for-byte ("Request had invalid authentication credentials. Expected OAuth 2 access token..."). Fresh drift found while capturing: the native-key arm now answers 404 (model retired for new users, roster points at gemini-3.8-flash), NOT the 401 "API keys are not supported by this API" that B2_04_probe_results2.json:64-74 recorded earlier today. Key masked (AQ.Ab...) in every persisted byte.

## Evidence file:line quotes

- watch/inbox/PROVIDER_HEALTH_20260926.md:24 (gemini row): "generateContent 401 as API key (\"API keys are not supported by this API\") and 401 as Bearer (\"invalid authentication credentials\")".
- watch/inbox/burn_wave_20260926/B2_04_probe_results2.json:64-74: "gemini_native_diag ... \"status\": 401 ... \"message\": \"API keys are not supported by this API. Expected OAuth2 access token ...\"" (the only gemini error body B2-04 persisted; no Bearer body anywhere in either results file).
- B2_129_gemini_auth_bodies.json (this lane, persisted): bearer arm `"status": 401` with `"message": "Request had invalid authentication credentials. Expected OAuth 2 access token, login cookie or other valid authentication credential. See https://developers.google.com/identity/sign-in/web/devconsole-project."`, `"status": "UNAUTHENTICATED"`.
- B2_129_gemini_auth_bodies.json: native_key arm `"status": 404` with `"message": "This model models/gemini-2.5-flash is no longer available to new users. Please update your code to use models/gemini-3.8-flash ... We recommend you to use the Interactions API"`, `"status": "NOT_FOUND"`.
- .env:84: `GEMINI_API_KEY=AQ.Ab8...` (full value never printed; script masks to AQ.Ab...).

## Work done

1. Wrote watch/inbox/burn_wave_20260926/B2_129_gemini_bearer_retry.py: reads GEMINI_API_KEY from .env, POSTs the identical synthetic body once per auth mode (x-goog-api-key vs Authorization: Bearer), persists status + full body + latency for both to B2_129_gemini_auth_bodies.json, masked key only, exit 0 when both bodies persist.
2. Ran it immediately (2026-09-26, synthetic prompt only): both bodies persisted in one pass, so "next run" is already satisfied and the health-doc quote is now byte-backed.
3. Named the drift: between B2-04's probe and this run the native-key failure class changed 401 (key rejected for this API) to 404 (model retired for new users). PROVIDER_HEALTH gemini row remains NO (inference) under either body; no doc edit made by this lane because the health row's verdict (NO) still holds and the Bearer cell is now proven.

## Falsifier

This capture dies if: (a) a rerun of B2_129_gemini_bearer_retry.py persists bodies that do not match the auth-mode headers claimed (e.g. bearer arm returning 200 would prove the key is an OAuth-capable token and the health row's "invalid authentication credentials" was a transient, filing an erratum against PROVIDER_HEALTH_20260926.md:24); (b) the persisted file ever carries the unmasked key (grep AQ.Ab8 must hit nothing); (c) the native_key arm flips back to the B2-04 401 body without a dated note, meaning the 404 drift was transient and the health row's API-key clause is again the live truth.

## Bibliography closed

All read this lane: watch/inbox/PROVIDER_HEALTH_20260926.md (line 24 gemini row), watch/inbox/burn_wave_20260926/B2_04_probe2.py (probe structure, header construction), B2_04_probe_results2.json (gemini_native_diag block), configs/providers.yaml gemini purge comment (lines 19-23, 42), .env line 84 (key name + masked head only).
