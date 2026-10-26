# W3F - Blind re-judge of the banked G1-vs-G3 duel - 2026-09-29/30

Mission (Mickey17 W3 follow-up): the v1.0 retro G1-vs-G3 verdict was judged
NAME-AWARE (judge saw model names); the W3 v1.1 honesty note priced a blind
re-judge at one ember call (~$0.02). This mission paid it.

## What ran

```
.venv/Scripts/python.exe tools/duel_harness.py \
  --ask-id retro-g1-vs-g3-blind-rejudge-20260929 \
  --from-jsonl watch/inbox/game_platform_basecamp_20260929/GOPHER_BURN_output3_healthy_20260929.jsonl \
  --a-id G1-adversarial-baseline-qwen --b-id G3-model-test-glm-prime
```

Same shape as the original retro run (ember judge `fireworks/ember-1`,
default rubric, default retro task text, no context file) so the only
deltas vs the name-aware row are: (1) names withheld from the judge ask
(v1.1 blind prompt), (2) presentation order swapped (ledger held 1 row ->
odd -> swap=true: slot A carried logical B/glm, slot B carried logical
A/qwen), (3) judge sampling (temp 0.4).

## Result

- ONE ember call, judge_cost $0.0176, 5.1s, no retry. Budget cap $0.10
  absolute respected (17.6% of cap).
- BLIND VERDICT: winner A = qwen/qwen3.8-max-prime (G1), rubric sum
  19-17 over glm's 17. Judge's slot-space vote was B; swap remap banks
  it as logical A. Raw rationale praises slot B, which held qwen's
  text - coherent with the remap. Per-criterion (logical terms):
  coverage 4-5 glm, severity 5-4 qwen, citations 5-4 qwen,
  actionability 5-4 qwen.
- FLIP: YES. Name-aware banked row said glm 19-16; blind re-judge says
  qwen 19-17. The two rows now sit side by side in the ledger.

## Honesty bounds on the flip

n=1 blind trial. The flip is real as a data point but does NOT isolate
its cause: name bias (the v1.0 leak favored glm), position bias (v1.0
showed qwen first; this run showed glm first), and judge sampling
variance (temp 0.4) all changed at once. Treat the pair as
name-aware-vs-blind, order-flipped, single-sample. The harness's parity
alternation + style signals (a_headers 13 vs b_headers 4 this run) are
the instruments for separating volume from content on future duels.

## Files

- Ledger row 2: `logs/duel/duels.jsonl`
  (ask_id `retro-g1-vs-g3-blind-rejudge-20260929`, ts 2026-09-30T02:14:55Z).
- Tool (unchanged this mission): `tools/duel_harness.py` v1.1.
- Source answers (already paid by the burn, not re-paid):
  `watch/inbox/game_platform_basecamp_20260929/GOPHER_BURN_output3_healthy_20260929.jsonl`.

Em-dash count in this file: 0.
