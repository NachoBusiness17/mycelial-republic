# INTERFERENCE SEARCH REPLICATION — PRE-REGISTRATION (frozen before first run)

Filed 2026-09-25, boot lane interference burn. Repo vendored at
corpus/library/interference-search (Apache-2.0, Badtheorylabs). Bars below are
frozen BEFORE any arm runs. No bar moves after results exist. A failed bar files
as FAIL/DISPUTED with numbers; no rescue interpretations, no rerolls, no
bar-shopping. One seed. Every arm reports honest n (deaths counted as deaths).

## Problems (identical across arms)

The exact 30 hard four-number problems from experiments/countdown/benchmark.py:
`rng = random.Random(11); sets = [gen_hard_problem(rng) for _ in range(30)]`.
Same seed, same generator, same order as their published run.

## Arms and frozen bars

**Arm B — their system on our hardware (vendored code, shipped judge, zero LLM).**
`search(dom, p, budget=200, width=b//12, merge=True)` exactly as benchmark.py.
Their claim: 30/30 at 200 judged states.
- PASS >= 27/30 (allows 1-2 hardware/env deltas).
- 20-26: PARTIAL, file per-problem diff vs their results/.
- < 20: FAIL on our stack; do not proceed to Arm C judgment claims.

**Arm A — fleet baseline: gemma:2b (ollama) thinking in text.**
prompt_text(p), greedy, temperature 0, 1500 generated token cap, fresh context
per problem, NO failure-feedback in prompts (their negative result: failure notes
made retries worse). Graded by their check_answer. 1500 generated tokens is the
honest cap on a model with no thinking mode; recorded as a scope difference.
- Expectation ~3/30 (their Qwen3-1.7B result).
- No pass/fail bar; report as-is. > 8/30 = SUSPICIOUS vs their claim, flagged
  in the receipt, not celebrated.

**Arm C — the fleet extension (the actual steal test): gemma:2b as the judge.**
Their search loop, their merge, but the trained 100k-param judge is REPLACED by
gemma:2b ranking the live frontier each step (batched: one ollama call judges
the whole frontier batch; each batched state still counts against the same
judged-state budget = the cost unit stays comparable).
- Budget 50 judged states per problem (their linear arm at 200 solved 21/30;
  their hidden-state probe solved 15/30).
- PASS >= 15/30 at 50 states.
- < 15/30: a dumb local LLM cannot substitute the trained judge; file FAIL with
  numbers. Either outcome feeds the estate judge-lane program (currently zero
  populated records) and the mickey17 fold-dedup steal.

## Cost-unit law (all arms)

Sequential steps and judged states recorded per problem. LLM tokens counted and
reported for Arm A/C. No arm gets a second chance on a problem.

## Canon carry (file with the receipt regardless of outcome)

- Merge dominance: 831,176 paths -> 13,229 states at six numbers (63 paths/state).
  We will measure OUR duplicate rate: mickey17 wave lane outputs screened for
  behavioral duplicates before fold. Their code-domain number was 83%.
- Negative results reproduced or not: prompted-judge AUC (theirs 0.58), hidden-
  state probe weaker than feature probe (0.87 vs 0.94), failure-feedback harm,
  resample-identical-line loop. Each gets a replicate/skip decision in the close
  receipt, none retrofitted.
- "Parallel streams seeing each other learned nothing" (0.511 vs 0.508) is
  training-from-scratch, not inference-time salons. Tension with refraction
  doctrine recorded as a domain question, NOT resolved by this lane.
