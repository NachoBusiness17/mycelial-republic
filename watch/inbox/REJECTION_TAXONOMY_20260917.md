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
