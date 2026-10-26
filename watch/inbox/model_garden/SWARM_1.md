# SWARM 1 - the first codebase swarm-review run (2026-10-01)

**Schema:** swarm.review.v1 - **ts:** 2026-10-01 - **lane:** SWARM-1 (ZCode subagent, operator mission:
"we can launch swarms against our codebase like we do our 5.3 lanes")
**Instrument:** tools/code_swarm.py (new this lane, 363 lines) + tests/test_code_swarm.py (9 tests).
**Targets:** the 53 triple-violator files of DOLLAR_BURN_SWEEP.md (all three wiring organs NO),
selected by --triple-violators from dollar_burn_20261001/sweep_grid.json at stage moment.
**Families (near-free tier):** kimi (moonshotai/kimi-k2 @ Nous, HERMES_API_KEY_2 credits),
glm-flash (glm-5.3-flash @ api.z.ai/api/coding/paas/v4), deepseek (deepseek-chat @ api.deepseek.com).
All 159 asks rode the gated rail tools/model_garden.run_ask (inference_budget recipes, refusal +
EMPTY_REASONING terminals, usage ledger); DeepSeek rode the garden rail rather than the ds_workhorse
CLI because the rail applies the deepseek recipe (thinking-off, floors) and banks terminals; the
workhorse's fixed 2000 cap has no budget guard.

## Headline

- **53 files x 3 families = 159 asks; 153 landed; 6 kimi EMPTY_REASONING terminals**
  (the burn law held: markers minted, same params never refired; those files still carry
  glm + deepseek coverage, so no file lost 2-family convergence).
- **Fire window 23:37:21Z - 23:45:27Z main pass (8m06s)** + 2 catch-up passes at width 2/1 for
  4 glm 429 transport failures (asks that never landed; conditions changed = lower width, not a
  same-params refire; kimi terminals skipped on sight).
- **Cost: $0.218 metered of the $2.00 cap** (deepseek $0.1599, zai $0.0581, kimi $0.0 metered on
  Nous credits). Worst-case crosscheck with kimi priced at the OpenRouter list
  ($0.57/M in, $2.30/M out, KIMI1_RUN precedent): $0.525 total, 26 percent of cap.
  Tokens: in 809,302 / out 247,883 (kimi reasoning 54,996 + glm thinking 131,337 ride out).
- **Convergence rollup (claim-level, the CROSS_RACTOR_MATRIX law): 279 clusters total,
  50 REAL (2+ families, same line-window, lexical claim overlap), of which 22 carry all 3 families;
  35 CO-LOCATION (same window, different diagnosis - reported as co-location, never agreement);
  194 UNIQUE. 1 REAL cluster (mag/gpu_ghost.py:266/277) is a re-report of the KNOWN organ-c
  violation and is excluded from the feed below: 49 new REAL clusters.**
- Grading: cites_resolve 153/153, lines_in_range 153/153, zero sha drift between ask and rollup
  (every verdict below is stamped against the sha the families actually reviewed). Shape strict-pass
  120/153 (glm 19 + deepseek 14 replies added extra prose lines; the defect lines inside them still
  parsed), no_em_dash 150/153, max_lines 151/153.
- Raw per-family per-file replies: watch/inbox/model_garden/swarm1/raw/<family>/<file>.md (153
  files) + the carrier-contract originals at watch/inbox/model_garden/swarm1-*.md; machine rollup
  at watch/inbox/model_garden/swarm1/rollup.json; manifests at swarm1/manifest.jsonl (sha-stamped).

## Top of the converged feed (byte-verified by this seat at rollup)

Ranked by dollar damage first, security second, correctness third. Line cites are the families';
the seat verified the mechanism on current bytes for every row marked VERIFIED.

| # | file:lines | families | the converged defect | byte verdict |
|---|---|---|---|---|
| 1 | tools/ocean_v2_pilot.py:45,127,142 | kimi+glm (window w/ ds) | COST_CAP=0.25 is declared and printed into the receipt but NEVER enforced: spend accumulates (145, 167) with no brake, so a run can blow past the pre-registered cap | VERIFIED: only uses of COST_CAP are the receipt print (198) and stdout (203); no comparison against spend anywhere |
| 2 | tools/roblox_npc_gateway.py:72 | glm+deepseek (identical claims) | DNS-rebinding TOCTOU: assert_public_https validates one getaddrinfo pass, then _OPENER.open re-resolves independently, so a rebinding host passes the gate and reaches a private IP | VERIFIED: same defect class the matrix already byte-settled in hermes_burn (X01 kimi A3); this is a second carrier of the hole |
| 3 | tools/reverse_map.py:160,173 | kimi+glm (identical claims) | keys[hash((sid, attempt)) % len(keys)] for retry key rotation: str hash is PYTHONHASHSEED-salted, so key selection is nondeterministic across runs, unreproducible in the receipt | VERIFIED at fire_shard |
| 4 | mag/preload_selector.py:213,227 | glm+deepseek (window w/ kimi) | pick_model exact-membership matches PRIMARY/FALLBACK against ollama /api/tags names that carry tag suffixes (:latest), then falls through to next(iter(sorted(names))) = an arbitrary installed model | VERIFIED at pick_model |
| 5 | mag/desk_model_probe.py:36,45,49 | glm+deepseek (window w/ kimi) | _has_model treats any tag sharing the base prefix as a match ("qwen-desk-v2" satisfies "qwen-desk"); ensure_qwen_desk builds Modelfile FROM qwen2.5:3b-instruct that may not exist with pull=False | spot-checked mechanism shape (prefix match + unconditional FROM); full walk pending |
| 6 | scripts/handoff_escalation_watcher.py:59,66 | glm+deepseek | _load_seen accepts list-or-dict but _save_seen writes a bare sorted list and silently truncates to 200 ids, so saved ids can only round-trip one way and old escalations get evicted arbitrarily | mechanism claims consistent; full byte walk pending |
| 7 | tools/tier_probe.py:249,262 | kimi+glm | --cache warm-up API call is discarded AND its tokens never counted, so cache-hit cost columns undercount real spend and the cache-economics claim is biased | pending byte walk |
| 8 | tools/task_wall.py:217,227 | glm+deepseek (window w/ kimi) | chore["lane"] is set to the Lane object inside worker but dispatch/retry treat it as a string; done counts every historical ok line in LEDGER with no time filter, overcounting this run | pending byte walk |
| 9 | mag/gpu_ghost.py:174,181 | glm+deepseek | partition misroutes: learned_tier never set so unknown heavy tiers go LOCAL-GPU; gpu free=None (telemetry dark) treated differently by partition vs afk_train | pending byte walk |
| 10 | mag/gopher_lite.py:116,135 | glm (window w/ kimi+ds) | spend gate uses fixed est_tokens=4000 while chore_label_farm ships a 9000-char prompt; --loop indexes d["choices"][0] unguarded so one malformed provider response kills the loop | pending byte walk |

Remaining 39 REAL clusters: swarm1/rollup.json clusters[] with status REAL (each carries file,
lines, families, per-family claims; sha-stamped against the reviewed bytes).

## Tickets minted (TICKET_LEDGER format, watch/inbox/hermes_burn/TICKET_LEDGER.md row shape)

| # | Ticket | Source receipt | Verdict |
|---|---|---|---|
| SW1-01 | tools/ocean_v2_pilot.py: enforce COST_CAP against running spend (abort before dispatch when spend >= cap) | SWARM_1.md row 1 (kimi+glm converged, seat-verified) | LANDED 2026-10-02 night lane: cap_ok() gate before every dispatch + aborted_at_cap receipt flag; tests/test_sw1_tickets.py |
| SW1-02 | tools/roblox_npc_gateway.py: pin the validated IP (or re-validate per open) to close the DNS-rebinding TOCTOU at assert_public_https | SWARM_1.md row 2 (glm+deepseek converged, seat-verified) | LANDED 2026-10-02 night lane: _validated_pin + _PinnedHTTPSConnection (SNI/Host/cert stay on hostname, connect dials the validated IP); tests/test_sw1_tickets.py |
| SW1-03 | tools/reverse_map.py: replace hash((sid, attempt)) with a stable digest (sha256 of f"{sid}:{attempt}") for key rotation | SWARM_1.md row 3 (kimi+glm converged, seat-verified) | LANDED 2026-10-02 night lane: sha256(f"{sid}:{attempt}") rotation; tests/test_sw1_tickets.py |
| SW1-04 | mag/preload_selector.py: tag-suffix-aware match in pick_model + refuse instead of arbitrary next(iter(sorted(names))) fallthrough | SWARM_1.md row 4 (glm+deepseek converged, seat-verified) | LANDED 2026-10-02 night lane: base-tag suffix match + ValueError refusal (no arbitrary fallthrough); tests/test_sw1_tickets.py |
| SW1-05 | mag/desk_model_probe.py: exact-tag match in _has_model + verify base model exists before Modelfile FROM | SWARM_1.md row 5 (glm+deepseek converged) | LANDED 2026-10-02 night lane (second half: FROM-verification fail-closed; first half suffix-aware _has_model was already landed pre-ticket, pinned by test) |
| SW1-06 | scripts/handoff_escalation_watcher.py: one canonical seen format (write what you read) + no silent 200-id truncation | SWARM_1.md row 6 (glm+deepseek converged) | LANDED 2026-10-02 night lane: canonical plain-list seen (legacy dict migrates on read), no 200-id truncation; tests/test_sw1_tickets.py |
| SW1-07 | tools/tier_probe.py: count the discarded cache warm-up tokens (or reuse the warm result) | SWARM_1.md row 7 (kimi+glm converged) | LANDED 2026-10-02 night lane: warm-up tokens counted into row["warm"] (tokens + cost), measured call uncontaminated; tests/test_sw1_tickets.py |
| SW1-08 | tools/task_wall.py: settle chore["lane"] type (object vs name) + time-filter the done count | SWARM_1.md row 8 (glm+deepseek converged) | LANDED 2026-10-02 night lane: lane assigned once (Lane object, sha256 pick), done count filtered to run window; tests/test_sw1_tickets.py |
| SW1-09 | mag/gpu_ghost.py: partition learned_tier wiring + one None-telemetry policy shared with afk_train | SWARM_1.md row 9 (glm+deepseek converged) | LANDED 2026-10-02 night lane: telemetry_allows_local() shared by afk_train + partition (None no longer blocks local dispatch); learned_tier chain verified wired flock_scheduler->backlog_reform->partition; tests/test_sw1_tickets.py |
| SW1-10 | mag/gopher_lite.py: guard choices[0] parsing in --loop + size est_tokens from the actual prompt | SWARM_1.md row 10 (glm + window) | LANDED 2026-10-02 night lane: guarded choices parse, est_tokens sized from prompt length, --loop survives a bad cycle; tests/test_sw1_tickets.py |

## Honest caveats

1. **Instrument bug this lane paid for:** the first version of tests/test_code_swarm.py wrote its
   synthetic grid over the real dollar_burn_20261001/sweep_grid.json (the fixture patched GARDEN
   but not SWEEP_GRID). Recovery: regenerated byte-derived via the sweep's own aggregate.py from
   the intact results_01..08.jsonl + targets.jsonl; the regenerated aggregate matches
   DOLLAR_BURN_SWEEP.md's numbers exactly (391 files, 53 triple violators, $0.5193, organ counts
   a 147/2/242, b 122/31/238, c 295/4/92, worst-10 identical). The test now patches SWEEP_GRID in
   the fixture; 9/9 pass. Lesson banked: any test touching a module-level Path constant must patch
   every Path it writes through.
2. Kimi re-reported KNOWN organ violations in several replies despite the contract's do-NOT-re-report
   clause (gpu_ghost UA/budget, lane_probe atomic write); the rollup filters organ-language clusters
   from the REAL feed (1 excluded), but individual kimi defect rows still carry some known-violation
   claims - the per-family raw files keep them, the feed above does not.
3. Convergence is corroboration, not adjudication (the G2/GPS law): every ticket above marked
   seat-verified was byte-walked by this seat; rows marked pending need the byte walk before a fix
   lands. CO-LOCATION clusters are leads, not findings.
4. glm replies burn heavy output tokens (thinking-on, uncapped per the 1210 law): 152K out tokens
   for 53 files vs deepseek's 28K. The glm recipe is correct (empty-content disease otherwise) but
   it prices glm at ~2.6x deepseek for the same grid on out-tokens.
5. The 6 kimi terminals are ask-shape burns (content empty, finish=length): the sanctioned recovery
   is re-stage with the kimi recipe or switch family; SWARM-1 leaves them dead on purpose.

## Instrument registration (no tools/ README exists on this tree; this receipt is the register)

**tools/code_swarm.py is the standing swarm-review instrument.** Rerun shape:
`python tools/code_swarm.py --run <id> --triple-violators --stage --fire --rollup`
(or `--files f1 f2 ...` for an explicit list, `--families kimi glm-flash deepseek --concurrency 10
--cap 2.0`). Landed outputs skip on rerun; EMPTY_REASONING/REFUSED terminals never refire.

## What the instrument still lacks to be a standing daily lane

1. **A scheduler + drift gate:** nothing fires it daily (needs a MagSwarmDaily task shape like the
   census patrol) and nothing yet re-runs only files whose sha changed since the last swarm
   (a sha-indexed cache of swarmed files would cut the daily cost to the moving tail).
2. **Automatic byte adjudication:** convergence clusters still need a seat walk for truth; a cheap
   deepseek adjudicator pass over each REAL cluster (the X1 paste-bound pattern) would pre-settle
   verdicts and leave only intent questions for the operator.
3. **Ticket minting is manual:** rollup.json emits clusters but does not append rows to a ledger
   file; the daily lane wants --mint writing id'd rows (aging view per the TICKET_LEDGER verdict).
4. **Family-health telemetry per run:** the rollup banks per-family check pass rates but does not
   yet alarm on family rot (e.g. a family whose shape-pass rate collapses); the animal_profiles
   sync should ingest swarm rows as behavioral observations.
5. **glm shape discipline:** 19/53 glm replies broke the strict 6-line shape (extra prose); a
   one-shot revision turn (the rail already supports revision.md) triggered on shape-fail would
   raise machine-parse rate without a second full ask.

Lane SWARM-1 seat, 2026-10-01. No commits. Files: tools/code_swarm.py (new),
tests/test_code_swarm.py (new), watch/inbox/model_garden/swarm1/ (staged asks, manifests,
raw sidecars, rollup.json, fire_log.txt), 153 carrier outputs swarm1-*.md, this receipt.
