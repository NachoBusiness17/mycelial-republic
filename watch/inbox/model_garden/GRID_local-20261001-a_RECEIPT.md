# GARDEN BATTERY lane-local run local-20261001-a (receipt, amended)

Instrument: lane-local-script (scripts/garden_battery_local.py + scripts/garden_battery_local_refire.py). Canonical runner tools/model_garden.py NOT used for firing: its SSRF/https fence refuses the loopback endpoint by design. Fence NOT weakened. Ask construction byte-matches model_garden.run_ask (system block single-sourced from tools.hermes_burn._system_for, contract, appended EVIDENCE sections, same closing line). Budget $0, zero paid calls, 23 fires total, all local.

Deviations and run incidents, all honest:
- direct calls to ollama OpenAI-compat http://127.0.0.1:11434/v1 with a browser UA; runtime ctx 8192 measured for all three models.
- max_tokens 2048 local vs 12000 staged for remote families (request param, not ask bytes; at the measured 11-28 tok/s, 12000 risks hours per rambling fire).
- staging moved under the run twice (sibling family lane): 18:11:05 staged B6/B8 with ASK_TEXT.md evidence, 18:20:31 reverted to the evidence-less spec shape. First pass fired gemma2 B6/B8 on with-evidence bytes and errored gemma4 B6/B8 + gemma:2b B6 on preflight; the refire amendment re-fired B6/B8 for ALL models on the pinned post-revert staging (contracts byte-verified identical, ask.json snapshotted under lanelocal/local-20261001-a/ask_snapshot).
- first-pass bug fixed by amendment: error rows graded the empty string and banked vacuous passes (NO-FENCE / NO-TRAILING-WS on a blank reply); DNF rows now carry 0 with an ERROR marker.
- first-pass bug fixed by amendment: model tags contain colons, so raw reply dumps landed in NTFS alternate data streams; all 18 recovered to sanitized filenames, slug fixed for future runs.
- B7 prompts exceeded ctx: server kept the tail (prompt_tokens 4098-4099 observed against an ~11k-token ask); identical truncation for every model, noted per row.
- convergence roll-up recomputed with distinct-model sets; the first pass counted one model triple-citing a bucket as overlap.

## Scores (score_norm = checks_passed / checks_total)

| model | B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 | mean |
|---|---|---|---|---|---|---|---|---|---|
| gemma2:2b-instruct-q5_K_M | 0.20 (1/5) | 0.20 (1/5) | 0.20 (1/5) | 0.20 (1/5) | 0.20 (1/5) | 0.00 (0/6) | 0.25 (1/4) | 0.00 (0/2) | 0.16 |
| gemma4:latest | 0.60 (3/5) | 0.20 (1/5) | 0.80 (4/5) | 0.40 (2/5) | 0.20 (1/5) | 1.00 (6/6) | 0.00 (0/4) | 1.00 (2/2) | 0.53 |
| gemma:2b | - | - | - | - | - | 0.33 (2/6) | 0.00 (0/4) | - | 0.17 |

## Throughput (completion tokens / wall seconds, prompt processing included; local CPU)

| model | item | tok/s | wall s | prompt tok | finish |
|---|---|---|---|---|---|
| gemma2:2b-instruct-q5_K_M | B1 | 7.9 | 35.14 | 5982 | stop |
| gemma2:2b-instruct-q5_K_M | B2 | 22.6 | 23.89 | 4099 | stop |
| gemma2:2b-instruct-q5_K_M | B3 | 11.8 | 15.1 | 3343 | stop |
| gemma2:2b-instruct-q5_K_M | B4 | 14.5 | 8.18 | 1608 | stop |
| gemma2:2b-instruct-q5_K_M | B5 | 11.8 | 28.47 | 5684 | stop |
| gemma2:2b-instruct-q5_K_M | B6 | 4.3 | 6.29 | 249 | stop |
| gemma2:2b-instruct-q5_K_M | B7 | 26.5 | 26.0 | 4099 | stop |
| gemma2:2b-instruct-q5_K_M | B8 | 49.4 | 1.7 | 326 | stop |
| gemma4:latest | B1 | 15.1 | 83.68 | 6030 | stop |
| gemma4:latest | B2 | 26.1 | 78.46 | 4099 | length |
| gemma4:latest | B3 | 27.6 | 74.2 | 3429 | length |
| gemma4:latest | B4 | 28.8 | 34.59 | 1651 | stop |
| gemma4:latest | B5 | 21.0 | 97.45 | 5744 | length |
| gemma4:latest | B6 | 23.5 | 24.34 | 260 | stop |
| gemma4:latest | B7 | 26.9 | 76.19 | 4099 | length |
| gemma4:latest | B8 | 41.2 | 21.52 | 336 | stop |
| gemma:2b | B6 | 4.7 | 5.55 | 262 | stop |
| gemma:2b | B7 | 21.7 | 28.25 | 4098 | stop |

Refired B6/B8 rows show the refire2 numbers (from the reply dump headers);
attempt-1 counts ride in each row's lineage notes inside the GRID JSON.

gemma2 Q5_K_M range 4.3-49.4 tok/s; gemma4 range 15.1-41.2 tok/s; gemma:2b Q4_0 4.7-21.7 tok/s on its two probes.

## Identical-bytes proof (user-message sha256 per item; all models identical)

- B1: IDENTICAL gemma2:2b-instruct-q5_K_M=5db79c89ee2798fa; gemma4:latest=5db79c89ee2798fa
- B2: IDENTICAL gemma2:2b-instruct-q5_K_M=836eb53e69a94ba7; gemma4:latest=836eb53e69a94ba7
- B3: IDENTICAL gemma2:2b-instruct-q5_K_M=8e12032159bd4eef; gemma4:latest=8e12032159bd4eef
- B4: IDENTICAL gemma2:2b-instruct-q5_K_M=8b5faa16a7085760; gemma4:latest=8b5faa16a7085760
- B5: IDENTICAL gemma2:2b-instruct-q5_K_M=09553ec621fa2f09; gemma4:latest=09553ec621fa2f09
- B6: IDENTICAL gemma2:2b-instruct-q5_K_M=3b3c9fa91028e290; gemma4:latest=3b3c9fa91028e290; gemma:2b=3b3c9fa91028e290
- B7: IDENTICAL gemma2:2b-instruct-q5_K_M=194211e672491d3b; gemma4:latest=194211e672491d3b; gemma:2b=194211e672491d3b
- B8: IDENTICAL gemma2:2b-instruct-q5_K_M=6e6e7ddfbcb26613; gemma4:latest=6e6e7ddfbcb26613

## Evidence clusters (lane-local only; no cross-family convergence claimed)

- B3 scripts/descent_driver.sh:0: gemma4:latest (model-unique evidence)
- B3 scripts/descent_driver.sh:3: gemma2:2b-instruct-q5_K_M (model-unique evidence [citing row failed CITES-RESOLVE: hallucination-risk cite])
- B4 watch/inbox/SHARED_SURFACE_CONTRACT.json:0: gemma2:2b-instruct-q5_K_M (model-unique evidence [citing row failed CITES-RESOLVE: hallucination-risk cite])
- B1 tools/hermes_burn.py:1: gemma4:latest (model-unique evidence [citing row failed CITES-RESOLVE: hallucination-risk cite])
- B1 tools/hermes_burn.py:6: gemma4:latest (model-unique evidence [citing row failed CITES-RESOLVE: hallucination-risk cite])
- B5 mag/steer_seal.py:3: gemma4:latest (model-unique evidence [citing row failed CITES-RESOLVE: hallucination-risk cite])

Finding: every resolving cite is gemma4; gemma2 Q5_K_M emitted praise or summaries with garbled and hallucinated cites (its descent_driver.sh:183-186 cite is out of range for a ~40-line file). Zero cross-model buckets: no convergent defect candidate from this lane. gemma4 B3 (4/5) is the strongest review cell: real atomic-rename and exit-code claims on descent_driver.sh lines 13-22, failed only DISTINCT-EVIDENCE by triple-citing one 40-line file.

## Quant probe: Q5_K_M scut vs its old Q4_0 self (gemma:2b)

| item | gemma2:2b-instruct-q5_K_M | gemma:2b (Q4_0) | winner |
|---|---|---|---|
| B6 | 0.00 (0/6) | 0.33 (2/6) | Q4_0 |
| B7 | 0.25 (1/4) | 0.00 (0/4) | Q5_K_M |

Byte answer: NO clean win. B6 (format law): the old Q4_0 self BEATS the new Q5_K_M scut, 2/6 vs 0/6 (Q4_0 emits two of the three byte-exact lines; Q5_K_M emits a fenced B1..B7 list with trailing whitespace). B7 (long-context): Q5_K_M edges Q4_0, 1/4 vs 0/4 (it alone names B2-552, inside a format-violating ramble). Confounder, named: this is NOT one base model at two quants; gemma:2b is family gemma 3B Q4_0 while gemma2:2b-instruct-q5_K_M is family gemma2 2.6B Q5_K_M. The comparison is new scut vs old scut as deployed, not a pure quantization delta.

## Ledger (memory/runs/model_garden/usage.jsonl, channel=lane-local-script)

- gemma2:2b-instruct-q5_K_M: 10 fires, 26208 prompt tok, 2467 completion tok, $0.00
- gemma4:latest: 10 fires, 25648 prompt tok, 11909 completion tok, $0.00
- gemma:2b: 3 fires, 4360 prompt tok, 640 completion tok, $0.00

Raw replies: watch/inbox/model_garden/lanelocal/local-20261001-a/ (attempt-1 dumps kept as *.attempt1.md where the amendment re-fired; em-dash bytes, if a model emitted any, are sanitized with a marker, and the NO-EM-DASH check banks the byte truth).
