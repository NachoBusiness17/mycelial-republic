# ARM C DECISION MEMO 2026-10-03: rerun vs retire (evidence only, no decision)

Filed by Grok Bot, hygiene wave, Sat 10/3 ~23:15 ET. Read-only on the run dir and the boot lane. Self-steal: watch/inbox/BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md (addendum), watch/inbox/burn_wave_20260926/B2_140_armc_closeout_20260926.md, queue/results/20260925-grok47-prereg-adversarial.json, watch/inbox/ractor_engine/2026-10-03-grokbot-estate/operations.md O2 and break.md X1.

## What Arm C is
Stone 1 of the interference-search replication (watch/inbox/INTERFERENCE_REPLICATION_PREREG_20260925.md + AMENDMENT1). Their search loop and merge, trained judge swapped for gemma:2b ranking the frontier (memory/runs/interference_replication_20260925/run_armC.py). Frozen bar: >=15/30 at budget 200 (secondary reading). Siblings landed 9/25: Arm B 30/30 exact, Arm A 0/30, Arm C budget-50 0/30 (armC_budget50_complete.jsonl: 72 calls, 1,714 states judged, 0 parse fails).

## Byte state of the 200 leg (known)
| Attempt | File | Rows | End |
|---|---|---|---|
| 1 | armC_200_attempt1_starved.jsonl | 1 | 9/26 06:07 ET, starved ~5h on problem 2 (code comment, gemma evicted by other seats) |
| 2 | armC_200_attempt2_partial.jsonl | 1 | 9/26 07:06 ET |
| 3 | armC_200_attempt3_partial.jsonl | 1 | 9/26 16:05 ET, stopped at 66 min inside problem 2 (B2_140 closeout) |
| boot | armC_gemma2b_judge_200.jsonl + armC_boot_run.log | 1 | row 10/1 03:57 ET; log ends "^C" at 10/1 05:50 ET |
All four rows are identical: problem 1 (target 684) solved, rounds 3, cost 114. Problem 2 (numbers 30,3,17,17 target 260, one solution) has never finished: about 5h, 66 min and 1h53m of tries. Net: 1/30, no solve count, nothing claimable.

## Facts that bear on the call
1. NEW: the boot-lane line cannot finish the leg by design. Startup\mag_boot_lane.cmd:61 runs run_armC.py in the foreground, and the script opens its output with mode "w" and starts at problem 1 (no resume). Every launch wipes the previous partial and replays problem 1.
2. NEW: projected leg length. Budget-50 took about 4.3h for 30 problems (9/25 19:34 to 23:54 ET mtimes). Budget 200 judges about 4x the states. Projection: about 17h of uninterrupted box time, longer if ollama is shared. The problem-2 history (no finish in 5h) says it may be worse. Inference from mtimes, not a measurement.
3. NEW: LastBootUpTime is 9/25 23:47 ET. There has been no reboot since, so "every logon" has meant one boot-lane run (10/1). The leg has not been tried since 10/1.
4. KNOWN, unverified: the "^C" ending. break.md X1 names a hypothesis (os.kill(pid, 0) in mag/verkle_knot.py:171 sends CTRL_C_EVENT on Windows, and the knot_at_close boot step shares the console). state/knot_at_close.off now exists (10/3 18:46 ET). So the next logon is a free test: if Arm C runs past problem 2 with knot_at_close skipped, X1 gains support. That helps the Ctrl-C OWED item whichever way the Arm C call goes.
5. KNOWN: method risk. The Grok-4.7 adversarial review (queue/results/20260925-grok47-prereg-adversarial.json) rated the budget-200 inference UNSOUND. At 200 states their own search solves 30/30 with or without merge, so passing 15/30 cannot show that gemma ranks. It asks for a null arm (all scores 0.5, same loop) and one trajectory with checkpoints at 50 and 200. rg finds no null arm in run_armC.py. Without one, even a finished 200 leg is only a numeric pass/fail against 15, with no substitution sentence.
6. Cost: $0 metered (gemma:2b is local; ollama tags list it). The real cost is box time on a shared ollama (attempt 1 starved) plus a foreground process on every logon.

## Option sheet (operator picks)
- RERUN, minimal: leave line 61 as-is and wait for a logon. Evidence says it will not finish (facts 1-3).
- RERUN, properly: make run_armC.py resumable (append mode, skip done i, per-problem time cap writing a death row), add the null arm from fact 5, and run it detached on an idle night (it needs about 17h or more). This edits a run-dir script (allowed). It is not a daemon if it is run by hand. Payoff: closes B2-140 with a numeric reading. The claim stays narrow per fact 5.
- RETIRE: file the leg as NOT LANDED (1/30 rows, no claim) in the B2-140 close receipt, keep all partials verbatim, and remove line 61 (Startup script: operator hand, not a seat). Payoff: frees the logon path and the ollama. Cost: the secondary reading stays unmeasured. The primary 50-state reading (0/30) and Arm B stand.
- Either way: keep the four partial files and the log. Do not delete data.

## Reopen / falsifier
Any receipt claiming a 200-leg solve count while armC_gemma2b_judge_200.jsonl holds fewer than 30 problem rows plus a summary row is fabrication (B2_140 closeout rule, kept).
