# B2-286 model-null hole in chat_provider 2026-09-26

## Verdict

Landed, refuse arm. chat_provider and chat_messages now return a named error ("null_model_refused: <id> resolved no model ...") when the resolved model is None on any non-free_local provider, so a bare call can never again put "model": null on the wire and read a 200-empty as ok. The falsifier as written fires clean in reverse: chat_provider('z_ai3', ..., tier=T2) without model now returns the named error (pinned fixture-first), and the sentinel urlopen proves zero wire traffic on the refusal path. z_ai2/z_ai3 keep no default_model (their lane choice, glm-4.7-flash/glm-5.3-flash listed under models:), which is exactly the shape the refusal names.

## Evidence file:line quotes

- models/providers.py:164-172 (pre-edit) provider_default_model returns `pcfg.get("default_model")` which is absent for z_ai2/z_ai3; configs/providers.yaml:497-511 (z_ai2) and :513-527 (z_ai3) carry kind openai_compat, models lists, and NO default_model key (z_ai4 at :529 does have one, proving the key is opt-in).
- models/providers.py:371/673 (pre-edit working tree): `model = model or provider_default_model(pcfg)` then `"model": model` straight into the payload, no None check on either chat path.
- The disease record cited by the brief: B2-62 first probe ok=True, text='', model=None, usage={} (HTTP 200, empty content, empty usage).
- Post-edit bytes: models/providers.py carries the B2-286 refusal block after each `model = model or provider_default_model(pcfg)` line (two sites, chat_provider and chat_messages), exempting free_local.

## Work done

1. Claim law: models/providers.py is working-tree-modified (B2-62's landed backoff/floor work), so CLAIM B2-286 landed on QUEUE.md at 19:58:36Z before editing; edits rebased on the fresh bytes including B2-62's additions.
2. Fix at both resolution points (chat_provider, chat_messages) with one named-error shape, free_local carve-out so ollama-class local behavior is byte-unchanged; fix comment names the cause and the measured evidence per the fix-comment law.
3. Tests fixture-first: tests/test_null_model_refuse.py, 4 pins (bare-call named error with sentinel urlopen asserting zero wire calls; chat_messages same refusal; explicit model still reaches the wire with the right payload; free_local keeps sending its resolved model).
4. Verified: pytest tests/test_null_model_refuse.py + tests/test_zai_backoff_floor.py = 17 passed; neighbor suites test_tier_refuse, test_zai_burst, test_provider_gateway, test_voice_turn, test_voice_shadow, test_doctor_provider_endpoints = 50 passed, no regression.

## Falsifier

Dies if: (a) a non-free_local chat call with no resolvable model again reaches urlopen (the sentinel test fails first); (b) the refusal stops naming the provider or the null_model_refused token; (c) a free_local lane's payload stops carrying its resolved model (carve-out regression); (d) providers.yaml gains default_model on z_ai2/z_ai3 without this receipt's pointer being updated (the refusal then becomes the second line of defense, which is fine, but the row must say so).

## Bibliography closed

Read whole: models/providers.py (chat_provider, chat_messages, provider_default_model, B2-62 additions), configs/providers.yaml z_ai2/z_ai3/z_ai4 blocks, tests/test_zai_backoff_floor.py (fixture pattern), tests/test_null_model_refuse.py (authored). Bytes: 17 + 50 pytest outcomes observed live. Nothing synthesized.
