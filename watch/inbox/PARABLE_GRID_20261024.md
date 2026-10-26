# Parable grid: the lens boundary, measured (2026-10-24, 40 calls, $0.06)

**Order:** prove capability across all live windows using the parables research.

## What ran

10 live lanes × 4 lens briefs = 40 calls, 5 workers, ~7 minutes.
Lanes: deepseek-flash, deepseek-v4-pro, zcode-1/2/3 (z.ai coding plans),
or-liquid / or-flint / or-nemotron (OpenRouter :free), nous-longcat / nous-beam (free).
Scored on: word window 80-170, English, a `mechanism:` line, the lens's required
signal present, **and the other lens's vocabulary absent**.

## Result

| task | valid | clean | failure |
|---|---:|---:|---|
| jung-no-freud | 10/10 | **4/10** | 6 lanes wrote "repress"/"symptom" (Freud's vocabulary) |
| freud-repetition | 10/10 | **9/10** | 1 lane wrote "grief" (Jung's ending) |
| ellul-autonomy | 9/10 | **9/9** | 0 boundary leaks |
| mcluhan-medium | 9/10 | **9/9** | 0 boundary leaks |

**38/40 produced a usable parable; 31/40 kept the boundary.**

## The finding, in one line

**Ellul and McLuhan are cleanly separable by an instruction; Jung and Freud are not.**
Twenty calls across four providers produced **zero** Ellul/McLuhan crossings, while
six of ten lanes collapsed Jung into Freud — always in the same direction, always
with the same words. The 2026-10-23 grid found the same asymmetry (5 of 21 errors);
this run reproduces it on different models with a direct prompt, which makes it a
property of the *lens*, not of one writer.

Per-lane, Jung:

```
deepseek-flash      clean        deepseek-v4-pro   clean
or-liquid           clean        or-nemotron       clean
nous-beam           leak repress nous-longcat      leak symptom
or-flint            leak symptom zcode-1           leak repress
zcode-2             leak repress zcode-3           leak repress
```

The two free Nous lanes and all three z-code lanes leak; DeepSeek (both tiers) and two
of three OpenRouter free models hold. Cost of the whole grid: **$0.06**, all of it on
DeepSeek and z.ai; the OpenRouter/Nous calls were free.

## Why this matters beyond the parables

The brief forbids the wrong word explicitly, and 6/10 models still used it. That is the
same failure the estate fights everywhere: **a prohibition in the prompt is not a gate**.
The instruction is not the control; the scorer is. Which is why the boundary has to be
checked at the output (as `tools/parable_score.py` does), not assumed at the input.

## Artifacts

- `tools/parable_score.py` — boundary scorer (need/forbid sets per lens).
- `memory/runs/burn/burn_20261024T015859Z.jsonl` — 40 raw calls with latency/tokens.
- `tools/burn_lanes.py` — 6 claimable lanes pre-registered (llm7, ollama-cloud,
  sambanova, google-studio, groq-new, mistral-new) so a pasted key is burnable with no
  further edit.

## Next

The gap is now specific: **Jung needs a gate, not a sentence.** Two options —
(a) a two-pass brief (write, then a self-audit that must name the mechanism in the
model's own words and reject Freud vocabulary before returning), or
(b) route Jung tasks only to the four lanes that held the boundary here.
Option (a) is testable in one more 40-call grid for ~$0.06.
