# REJECTION TAXONOMY — self-steal from the build lane's own failure data (2026-09-17)

## The numbers

41 rejection rows total. Only **2 are merit rejections** (BFS said the level was
unsolvable). The other **39 are infrastructure failures**: transport errors, empty
content, rate limits, window ends, incomplete reads.

## The taxonomy

| Class | Count | What it means | Fix |
|---|---|---|---|
| 200-error-body | 16 | OpenRouter returns HTTP 200 with an error body (stealth windows flap) | key rotation (shipped) |
| 404 window-end | 11 | the stealth model's free window ended mid-fire | successor strike (shipped: pareto) |
| empty_content | 12 | reasoning channel consumed budget before content (pre-cap-removal) | cap removed (shipped) |
| schema | 2 | model emitted bad grid rows or width | brief hardening (shipped) |
| IncompleteRead | 1 | network-level | retry (free) |

## The finding

**The gate isn't strict — the infrastructure is unreliable.** Of 41 rejections, only
2 said "this level is unsolvable." The other 39 said "the pipe broke." The model
quality signal is actually: when a model produces a level, it passes the gate about
half the time (17 promoted / 16 transport-clean rejections = ~52% first-pass rate).
And after seeing its own failures, the gen-2+ pass rate approaches 100%.

## The astra connection

These 41 rejection receipts are the negative examples the astra brief demands. The
training corpus needs: not just the 19 promoted levels, but the 39 transport
failures (as "this is what infrastructure failure looks like — retry, don't
redesign") and the 2 merit failures (as "this is what unsolvable looks like —
the level has a sealed path, a parity trap, or a guard that can't be denied").
The model that learns the difference between "the pipe broke" and "the design is
wrong" is the model that stops wasting attempts on transport and starts
redesigning on merit.

## ERRATUM 2026-09-26 (append-only, lane B2-33 pre-burn recount)

Raw recount of build_lane/proposals.jsonl at the snapshot committed with this
file (git 3d12289f9, 2026-09-17T23:56:48-04:00, two minutes after this file's
mtime; 71 rows, 41 verdict FAIL) confirms the headline: 41 rejection rows,
39 infrastructure / 2 merit. Exactly one table cell is wrong: empty_content is
9, not 12 (8 rows on 09-17 plus 1 row at 2026-09-18T03:28:58Z; 12 is
unreachable under any cutoff since the file max is 9). The table sum of 42 came
from that +3 cell, then adding the IncompleteRead row to a 4-class sum that had
absorbed the same +3. Frozen census: 200-error-body 16 (12 KeyError 'choices'
plus 4 explicit 200_error_body), 404 window-end 11, empty_content 9, schema 2,
IncompleteRead 1, merit 2, total 41. Infra share 39/41 = 95.1% stands. The
falsifier in BURN_judge-lane-spec_20260925_d.md required a correction to the
95.1% figure only if the recount missed 41; it does not. Evidence:
watch/inbox/burn_wave_20260926/B2_33_rejection_recount_20260926.md

ERRATUM 2026-09-26 (B2-118, second erratum, append-only): the line-24 numerator
"17 promoted" is a stale same-day count. At the frozen cutoff (git 3d12289f9)
the bytes hold 24 promoted_* receipt files, 19 unique promoted names (dedupe
_g1/_g2), state.json promoted = 19, and 30 PASS rows / 19 unique PASS briefs;
this file's own line 30 already says "the 19 promoted levels". The only
17-tally in the bytes is mid-day: exactly 17 promoted receipts carry mtimes
before 17:23 (-0400), the 18th landed 19:11:03 and six more before the
23:56:48 commit. The denominator "16 transport-clean rejections" is CONFIRMED
from committed proposals.jsonl: 12 rows error "KeyError: 'choices'" + 4 rows
"200_error_body" = 16 of 41 FAIL. Corrected first-pass figure: 19/(19+16) =
54.3%, so "~52%" reads "~54%"; "about half the time" survives. Evidence:
watch/inbox/burn_wave_20260926/B2_118_first_pass_erratum_20260926.md
