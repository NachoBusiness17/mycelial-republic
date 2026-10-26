# B2-295 openrouter :free rotation build-out 2026-09-26

## Verdict

LANDED. The verify-then-add rotation exists and ran live: tools/openrouter_free_gate.py fires one chat gate per candidate id (PASS = HTTP 200 with non-empty content; 200-empty retried ONCE at max_tokens 2000 so reasoning models are not falsely failed by the B2-62 thinking-ate-the-budget scar) and only PASSING ids earn a providers.yaml line. Live run 2026-09-26: 4 ids earned their lines and were appended to configs/providers.yaml openrouter models with dated gate comments (nvidia/nemotron-3.5-lightning:free, liquid/lfm-2.5-2.6b:free, poolside/laguna-xs-2.1:free, plus cohere/north-mini-code:free re-proven alive); yaml parses clean through load_providers(). The gate tool stays for every future candidate: no line without a gate PASS row.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/B2_295_gate_results.json (first run, pre-retry arm): cohere/north-mini-code:free http 200 EMPTY content, qwen/qwen3.8-27b:free 429 upstream shared pool (the B2-61 proof re-measured), google/gemma-4-31b-it:free 429, thinkingmachines/inkling-small:free 403 "only available on ag[ents]".
- watch/inbox/burn_wave_20260926/B2_295_gate_results2.json (with the retry arm): 4/5 PASS. The cohere flip is the receipt of the false-negative class: same id, same hour, 200-empty at 16 tokens then PASS at 2000, proving the 16-token gate alone would have wrongly denied the B2-61-verified lane.
- configs/providers.yaml openrouter models (post-edit, load_providers() output): [openrouter/auto, stealth/space-bunny-alpha, cohere/north-mini-code:free, nvidia/nemotron-3.5-lightning:free, liquid/lfm-2.5-2.6b:free, poolside/laguna-xs-2.1:free].
- tools/openrouter_free_gate.py: docstring law "CATALOG PRESENCE IS NOT LIVENESS"; gate_one() retry arm named with the B2-62 scar.

## Work done

1. Authored tools/openrouter_free_gate.py (stdlib, key from env/.env chain, --from-catalog for fresh :free id pulls, --spacing for the shared pool, --out JSON rows).
2. Live-gated candidates on both runs; the first run's 200-empty cohere FAIL exposed the gate's own false-negative class; fixed the gate (spec-first comment) BEFORE trusting it, then re-ran.
3. Claim law: configs/providers.yaml working-tree-modified, CLAIM B2-295 (20:44:49Z) before the edit; only the openrouter models list grew, existing lines untouched; yaml re-validated by import.
4. Appended the 3 new ids (cohere already had its line from B2-61; re-proven, not duplicated) with dated gate comments plus an explicit gate-FAILED no-line list (qwen 429, gemma-4-31b 429, inkling-small 403) so the next sweep re-tests only those.

## Falsifier

Dies if: (a) any providers.yaml :free line exists whose id has no gate PASS row in a B2_295_gate_results*.json or successor artifact (line without gate); (b) the gate passes an id on 200-empty content (the retry arm regressed); (c) a gate-FAILED id gets a line before a later gate run PASSes it (the failed-list comments name them); (d) the 3 new lanes go dead without a drift patrol naming it (this tool re-run is the check).

## Bibliography closed

Read whole: tools/openrouter_free_gate.py (authored), watch/inbox/burn_wave_20260926/B2_61_verify_results.json (17-id catalog, openrouter_repoint_probe), configs/providers.yaml openrouter block + ladder header purge comments. Bytes: two live gate runs on file, yaml parse via load_providers() observed. Nothing synthesized; 429/403 ids stay lineless.
