# prereg-attack, candidate one: the cost-unit law's token clause is broken for Arm C

## Approach

Attack the prereg's cost-unit law, not its bars. The frozen claim, watch/inbox/INTERFERENCE_REPLICATION_PREREG_20260925.md:45-47: "## Cost-unit law (all arms) / Sequential steps and judged states recorded per problem. LLM tokens counted and reported for Arm A/C." Amendment 1 clause 3 (watch/inbox/INTERFERENCE_REPLICATION_PREREG_AMENDMENT1_20260925.md:31-33) reaffirms it: "Everything else in the original prereg stands unchanged." For Arm C this claim is false in the instrument, false in the data, false in every receipt, and unhealable for the owed 200-leg without editing the standing script. A third party breaks it by reading three estate files; no rerun is even needed.

Why this attack and not the obvious ones: the Grok 4.7 adversarial pass (watch/inbox/INTERFERENCE_PREREG_ADVERSARIAL_GROK47_20260925.md) already holds the five structural attacks (saturated-regime 200 PASS, 50-bar reinterpretation, two-budgets-second-life, unfrozen decoding/rank prompt, skip-later retrofit). Re-naming any of those dies as already-known. The prereg's own text pre-consumes the rescue-reading class ("no rescue interpretations", prereg line 6), so the close receipt's "0/30, matches their own trained judge's weakness at 50" (BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md:11-12) and queue/todo.md:196's "0/30 (frozen bar kept, = their own trained judge's 23% at 50)" are covered-class defects, not my attack. The cost-unit accounting was attacked by nobody: the Grok pass never touches it, the prereg text merely asserts it will happen, and the assertion is what breaks.

Why it is substantive, not clerical: the law is the prereg's comparability instrument. Arm C's design sentence, prereg line 36-37: "each batched state still counts against the same judged-state budget = the cost unit stays comparable". But the steal this prereg licenses (BOOT_LANE_INTERFERENCE_BURN_20260925.md:50-52, stone 1 step 3: the trained-judge shape ~100k params feeding the estate's judge-lane program, currently zero populated records) needs the LLM-tokens-per-judged-state number to argue a local-LLM judge is a viable substitute for a 100k-param judge that costs zero tokens. That number was frozen as a deliverable, the instrument never captured it, and the 200-leg fold demanded by B2-140 will violate the same law again because the script cannot produce it.

The break, as a third party executes it:

1. memory/runs/interference_replication_20260925/run_armC.py:35: `stats = {"calls": 0, "states_judged": 0, "parse_fails": 0}`. No token counter exists.
2. run_armC.py:59: `text = json.loads(r.read()).get("response", "")`. The ollama response dict carrying eval_count is discarded. `eval_count` appears in exactly one script in the run dir, run_armA.py:50 (grep, this session).
3. memory/runs/interference_replication_20260925/armC_budget50_complete.jsonl: 31 rows (30 problems + summary). Census run this session: `has tokens field: False`. Summary row verbatim: `{"budget": 50, "summary": "0/30", "calls": 72, "states_judged": 1714, "parse_fails": 0}`.
4. Receipts: BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md contains exactly one token mention, line 11, and it is Arm A's "~80 tok/problem"; grep for "parse" in that file returns nothing. B2_140_armc_closeout_20260926.md contains no token mention. queue/todo.md:196 reports Arm C with no tokens.
5. No recovery meter exists. logs/provider_usage.jsonl does meter gemma:2b per call with prompt_tokens/completion_tokens, but its gemma:2b rows span 2026-07-20 to 2026-09-19 and contain zero rows dated 2026-09-25/26 (checked this session), because run_armC.py bypasses the mag provider layer with raw urllib to 127.0.0.1:11434.

Contrast that keeps the attack honest: Arm A satisfies the same law. run_armA.py:50 captures eval_count per row; census this session: 30 rows, total tokens 2377, average 79.2, which byte-backs the receipt's "~80 tok/problem". The law was executable and executed for one arm and structurally impossible for the other, in the same run directory, under the same prereg.

Secondary frozen-report clause broken in the same receipts (folded into this attack as one pattern): amendment 1 clause 2, "parse-fail rate is reported in the close receipt" (AMENDMENT1:29-31). The completed 50-leg's rate (0 parse fails over 1714 judged states, 72 calls) sat in the jsonl before the close receipt was written, and the close receipt contains zero occurrences of "parse".

Verified clean while hunting, reported as negatives so the next attacker does not re-dig them:

- problems.json reproduces byte-exact from the vendored seed-11 generator. Ran regeneration under .venv Python 3.11.15 and PATH Python 3.12.10: both 0/30 mismatches (command and output in my session log; both interpreters named).
- Python-version fragility of the frozen one-liner is dead. The documented 3.11 changes to random.sample (sets no longer auto-converted) and random.shuffle (optional random parameter removed), docs.python.org/3/library/random.html fetched this session, do not alter the draw stream for sequence inputs, and the 3.11/3.12 empirical agreement confirms. No 3.10 interpreter exists on this box, so 3.10 stays untested; stated as not run, not as safe.
- Upstream generator stability holds across the entire public history. The vendored clone is shallow at 929dd0c of github.com/Badtheorylabs/interference-search. Web history shows interference_search/countdown.py was touched by exactly two commits (b635215 initial, cee1492 same-day tidy); I fetched b635215's countdown.py raw and diffed against HEAD with --strip-trailing-cr: the only change is a dead `used = list(leaves)` line in extract_attempts. gen_problem and gen_hard_problem are identical in both public commits.
- Arm identity holds: armA and armC budget-50 rows match problems.json numbers/targets in identical order (census, both True).
- Residual, not an attack: "Same seed, same generator, same order as their published run" (prereg:12-13) is unverifiable on the published side, because their published artifact results/countdown/countdown_benchmark.json holds aggregate rates only (one-line 0.7 at 200, interference 1.0; no per-problem records) and paper/CLAIMS.md cites that same aggregate file. No third party can contradict it either, since pre-b635215 history does not exist publicly, so it is a doubt, not a breakable claim. Filed here so nobody mistakes it for leverage.

## Moves with estate paths

1. The break itself: cite run_armC.py:35 and run_armC.py:59 (token counter absent, eval_count discarded) against memory/runs/interference_replication_20260925/armC_budget50_complete.jsonl (31 rows, no token field, summary `0/30, calls 72, states_judged 1714, parse_fails 0`) and watch/inbox/BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md:11 (single tok mention, Arm A only). This is the third party's three-file kill.
2. No-recovery proof: logs/provider_usage.jsonl gemma:2b date range 2026-07-20 to 2026-09-19, zero rows on 2026-09-25/26 (run_armC.py raw-urllib bypass, run_armC.py:26-31 loopback assert block names the path); B2_140_armc_closeout_20260926.md and queue/todo.md:196 contain no Arm C token report.
3. Amendment-1 clause 2 fold: parse-fail rate 0/1714 exists in the jsonl summary row yet BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md carries zero "parse" occurrences; same receipts, same pattern, one attack.
4. Pre-rerun instrument fix on the owed 200-leg (watch/inbox/burn_wave_20260926/B2_140_armc_closeout_20260926.md:21-23 reopen condition): patch run_armC.py to capture eval_count per call BEFORE the rerun, file the patch as prereg amendment 2 citing this attack, else the 200-leg fold violates the cost-unit law a second time. Timing is forced by the Grok-pass principle (INTERFERENCE_PREREG_ADVERSARIAL_GROK47_20260925.md:36: "Any later edit voids the arm"): edit before launch, never after rows exist.
5. Protect the identity claims I verified clean: write the regeneration receipt (both interpreters, 0/30 mismatches) and the b635215-vs-HEAD generator diff into the run dir so the "same generator" leg of prereg:11-13 stops being an unbacked assertion.

## Falsifier

My attack dies if any of these holds:

- Arm C token counts exist somewhere I did not find: a field in any armC jsonl, a line in any receipt under watch/inbox, or gemma:2b rows dated 2026-09-25/26 in logs/provider_usage.jsonl. I checked all three this session (census, grep "tok"/"parse" on the close receipt and B2-140, provider_usage date range); refuting me means producing the bytes.
- One argues the law's phrase "for Arm A/C" means Arm A only, or that judged states alone were the frozen unit. The text says "LLM tokens counted and reported for Arm A/C" verbatim and amendment 1 clause 3 froze "everything else... unchanged"; the slash reading is the only honest one, and Arm A's own compliance (2377 tokens, 79.2 average, byte-backing the receipt's ~80) proves the estate read it that way too.
- One reclassifies the break as already-covered: the prereg text asserts the counting, it does not hedge it; Grok's five attacks (INTERFERENCE_PREREG_ADVERSARIAL_GROK47_20260925.md:16-42) target decision structure and never the cost accounting. If the judge finds a prior filing that names the missing Arm C tokens, this candidate dies as already-known; I found none in the prereg, amendment, Grok pass, close receipt, B2-140, or queue/todo.md.

The third-party one-liner a hostile auditor runs: read run_armC.py lines 35 and 59, then grep for "tok" and "parse" in watch/inbox/BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md and watch/inbox/burn_wave_20260926/B2_140_armc_closeout_20260926.md, then open the armC_budget50_complete.jsonl summary row. Frozen claim, broken, no rerun required.

## Owed

- The instrument fix itself (move 4) is not landed by this candidate; it belongs to the lane that reruns the 200-leg. Amendment 2 drafting is theirs.
- The regeneration + upstream-diff receipt (move 5) is not written to the run dir by this candidate; this file holds the findings, the receipt is a five-minute follow-up for the same lane.
- 3.10-interpreter regeneration test not run (no 3.10 on this box); if one appears upstream ever claims 3.10 for the published run, rerun the frozen one-liner under it. Documented random changes say it should agree; untested stays untested.
- The "same as their published run" residual unverifiability (aggregates only, no per-problem record, invisible pre-b635215 history) is named above and left as a doubt; no estate action can settle it, only upstream publishing per-problem bytes could.
