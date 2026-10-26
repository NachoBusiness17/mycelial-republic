# The prohibition is the problem (2x2, 10 lanes, 2026-10-24)

Follow-up to the grid where 6/10 lanes used Freud's vocabulary inside a Jung brief
that explicitly forbade it. The guess was "a prohibition is not a gate". The 2x2 says
something sharper: **the prohibition is what caused the leak.**

## Design

Same 10 lanes (deepseek-flash, deepseek-v4-pro, zcode-1/2/3, or-liquid/or-flint/
or-nemotron, nous-longcat/nous-beam). Same Jung brief. Two switches:

- **prohibition** - the brief ends with "FORBIDDEN: cellar, symptoms,
  repetition-compulsion, 'cured/repressed' ending - that is FREUD's mechanism."
- **gate** - a second pass: "audit your draft for those stems; if present, rewrite
  keeping the Jung mechanism; output only the final parable."

Scored on the same rule as the grid: `cellar|symptom|repress|repetition-compulsion|
unconscious wish|neurosis` absent from the final text.

## Result

| | no gate | gate |
|---|---|---|
| **no prohibition** | **8/10 clean** ($0.009) | **9/10 clean** ($0.024) |
| **prohibition** | **4/10 clean** ($0.076) | **9/10 clean** ($0.022) |

Reading it:

1. **Forbidding the word made it appear.** 4/10 clean with the prohibition, 8/10
   without. The forbidden token is *mentioned* in the brief; mentioning it raises its
   salience, and half the models reach for it. Classic negative priming - and it is
   stronger than the model's ability to follow the instruction not to.
2. **A gate removes the problem regardless of framing.** 9/10 in both cells. The gate
   costs one extra call and repairs the damage the prohibition created.
3. **The gate is not free of failure**: one empty rewrite in each audited cell (a model
   that audited itself into silence). 9/10, not 10/10, twice.

## The rule this buys

Do not write prohibitions into a brief. Write the **positive mechanism** and gate the
output. A negative instruction is a token you injected; a gate is a check you can
actually run.

This also explains the estate's own recurring pattern: rules that list what not to do
(the forbidden-path list, the "never force-remove lock" line) work only because
something else checks them. The instruction is never the control.

## Cost of the whole experiment

$0.13 across 60 calls, every lane free or near-free.

## Side fix landed in the same window

`MagBreathReplayHourly` was running `fsck --connectivity-only` **every hour** with a
1800 s ceiling against a 20 GB / 228k-object store. One run took 30+ minutes and
starved the sweeper for hours (HEAD frozen at 01:20 while 614 files queued).
`chk_fsck` now caches its verdict for 24 h per HEAD and caps at 900 s, returning
UNMEASURED on timeout. Verified: replay check now completes in **31 s** with
`"cached": true`.

## Addendum: the four new lanes (groq ×2, ollama ×2)

The first gated run asked for 14 lanes but only 10 executed - the groq/ollama lanes
were registered after that job started. Re-run on the four:

| cell | result |
|---|---|
| no prohibition, no gate | 3/4 clean, 1 leak |
| no prohibition, + gate | 3/4 clean, 0 leaks, **1 silence** |

Across all 14 lanes with no prohibition: **11/14 clean without a gate, 12/14 with one** -
but the gate's failures are *silences*, and the ungated failures are *leaks*.

That distinction matters more than the one-call difference: a leak is silently wrong
(a Freud word inside a Jung parable, shipped as if fine); a silence is visible (no text
at all, caught by any consumer). The gate does not mainly raise quality - it converts
invisible wrongness into visible absence, which is the trade a gate should make.
