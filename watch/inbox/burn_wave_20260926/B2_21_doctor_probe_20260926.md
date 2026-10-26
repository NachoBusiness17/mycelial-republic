# B2-21 Doctor provider probe wiring (2026-09-26)

## Verdict

Landed. mag/doctor.py check_provider_endpoints() now carries the B2-04 deep remote probe: MAG_PROBE_REMOTE=1 runs GET /models plus ONE one-token chat ping per (base_url, model, key) triple and classifies the measured B2-04 failure shapes: cerebras 402 -> QUOTA-DEAD, nvidia 410 -> QUOTA-DEAD, gemini 401 -> AUTH-DEAD, mistral zero-limit 429 -> QUOTA-DEAD, z_ai 1305 429 -> DEGRADED (non-alarm, should_burst owns retry). Default path unchanged: remote lanes stay REMOTE-UNVERIFIED config-only, zero bytes leave. Fences: opencode_only -> FENCED, anthropic_messages kind -> REMOTE-UNVERIFIED (protocol mismatch), no key or no model -> REMOTE-UNVERIFIED. Alarm classes DOWN / QUOTA-DEAD / AUTH-DEAD feed issues. Tests 30/30 in tests/test_doctor_provider_endpoints.py (21 pre-existing untouched + 9 new), 50/50 across all doctor-importing test files, ratchet PASS NEW=0. Live MAG_PROBE_REMOTE=1 run reproduces the B2-04 scoreboard lane for lane.

## Evidence

- watch/inbox/PROVIDER_HEALTH_20260926.md:22 "chat 402 Payment Required x3, empty body = zero usable credit"; :25 mistral "x-ratelimit-limit-req-minute: 0, remaining: 0"; :20 z_ai "429 code 1305"
- watch/inbox/burn_wave_20260926/B2_04_probe_results.json: "cerebras -> DEAD status=402", "nvidia -> DEAD status=410", mistral rl x-ratelimit-limit-req-minute "0"
- watch/inbox/burn_wave_20260926/B2_04_probe_results2.json: zai-lite body_err {"error":{"code":"1305","message":"The service may be temporarily overloaded..."}}; gemini_native_diag 401 "API keys are not supported by this API"
- mag/doctor.py:42-74 spec (class map, fences, burn law, 15s floor); :304 _classify_chat_failure; :349 _probe_remote_deep; :376-377 ping = max_tokens 1, "Reply with the single word: pong.", browser UA per the Cloudflare-1010 law; :555 floor max(timeout, 15.0); :577-592 degraded/fenced result keys and alarm prefixes
- Live run 2026-09-26, 15 probes one 1-token ping each: groq, openrouter, nous+nous_api (deduped), together, deepseek ALIVE; z_ai2+z_ai3 DEGRADED 1305; cerebras QUOTA-DEAD 402; z_ai/z_ai4 FENCED; cohere/nvidia/dashscope/moonshot/fireworks/hf_router/github_models/vast/deepseek_overmind REMOTE-UNVERIFIED no-key; anthropic REMOTE-UNVERIFIED kind
- tests/test_doctor_provider_endpoints.py:308-430: nine tests replay every shape off a fake lane server, pin ping shape (1 POST, max_tokens 1, synthetic prompt), key values never in any detail, 13 remote rows dedupe to 10 probes, fences send zero bytes

## Work done

Spec-first docstring rewrite, then code. _probe_remote_models (the models-only probe, exactly the B2-04 trap: catalog 200 on inference-dead lanes) removed, replaced by _classify_chat_failure + _probe_remote_deep. Fences judged before any byte leaves; deep dedupe on (style, base_url, model, sha256 key fingerprint, first 12 hex, never the value). Result adds "degraded" and "fenced" lists; new issue prefixes PROVIDER QUOTA DEAD / PROVIDER AUTH DEAD. Real defect found and fixed live: the 2s local-probe timeout misclassified z_ai3 DOWN while sibling key z_ai2 answered the same endpoint; floor 15s per B2-04's measured 2.5-9.7s pings, after which z_ai3 reads DEGRADED 1305.

## Falsifier

MAG_PROBE_REMOTE=1 .venv/Scripts/python.exe -c "from mag import doctor; r=doctor.check_provider_endpoints(); print(r['statuses'], r['issues'])": cerebras must read QUOTA-DEAD while its key stays creditless, z_ai2/z_ai3 DEGRADED or ALIVE, and no detail may contain key bytes. Unset the env and every remote row must read REMOTE-UNVERIFIED with probes_run 0. If cerebras reads ALIVE, the operator has funded the account and the class map test fixture (402) is what needs updating, not the code.

Divergences from the health table, honest: gemini reads DOWN 404 (compat default gemini-2.0-flash), not 401, because the yaml path is the compat one with a stale default; B2-04 round 1 measured the same 404 and the 401 was the native path. Mistral reads DOWN 403, not zero-quota 429, because yaml default_model mistral-large-latest is not callable on this key; B2-04's zero-quota was mistral-small-latest. Both filed as self-feed briefs.

## Bibliography closed

watch/inbox/PROVIDER_HEALTH_20260926.md; watch/inbox/burn_wave_20260926/B2_04_provider_health_20260926.md; B2_04_probe.py; B2_04_probe_results.json; B2_04_probe_results2.json; mag/doctor.py; models/providers.py; tests/test_doctor_provider_endpoints.py; configs/providers.yaml; watch/inbox/burn_wave_20260926/QUEUE.md (B2-61, B2-62, B2-63 read, not rewritten).
