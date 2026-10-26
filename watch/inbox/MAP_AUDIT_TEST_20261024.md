# Next test: can a lens panel catch a planted premise? (2026-10-24, 120 calls, $0.128)

## Why this test

Yesterday's lens run didn't just produce decisions — the lenses attacked the **map**.
Diogenes called the backlog a vanity count; wallas said the rows might be one
observation reworded; foucault said the census was the archive's next monument. They
were right (62.5% probe chatter, ~750 real rows, 16 existing readers).

That suggests lenses act as an error-correcting code over maps. So: plant an error and
measure the correction.

## Design

Two maps, six numbered premises each, same lenses, same six lanes, 120 calls:

- **TRUE** — six premises true of the estate today.
- **FALSE** — same map with two planted falsehoods: *"No code in the estate reads
  explore.jsonl"* (P3) and a row count of 1,521 (P1).

Ask: *list premises you cannot verify from the map, and premises you believe are false.*
Score: **strict** detection (called false), **loose** detection (false or unverifiable),
and false alarms on the TRUE map.

Pre-registered hypotheses: H1 detection rises with panel size; H2 false alarms stay low;
H3 a single lens is insufficient (k=1 < 0.5, k=3 ≥ 0.8).

## Result

| | |
|---|---|
| FALSE map answered | 60/60 |
| planted P3 flagged (loose) | **52/60 (87%)** |
| planted P1 flagged (loose) | **54/60 (90%)** |
| planted flagged **strictly** (called "false") | **3/60 (5%)** |
| TRUE map, a true premise called false | **1/57 (1.8%)** |
| per-lane loose detection | groq 10/10, ollama 10/10, deepseek-flash 9/10, deepseek-v4-pro 5/10 |
| per-lens loose detection | 5/6 or 6/6 for every one of the ten lenses |

**H1 confirmed but trivially** (saturated at k=1). **H2 confirmed** — 1.8% false
accusations. **H3 falsified**: one lane, one lens catches ~87% of a factual error; a
panel adds almost nothing.

## What it actually says

The panel is not a lie detector. It is an **UNMEASURED detector**: given a map, models
overwhelmingly answer *"I cannot verify this from the map"* (90%) and rarely *"this is
false"* (5%). That is the correct epistemic behaviour — a map cannot establish whether
code reads a file; only the repo can — and it is the same tri-state discipline the
estate already runs (`PASS / FAIL / UNMEASURED`).

The three strict detections came from internal contradiction, not from evidence: 1,521
rows × 62.5% probe × ~750 distinct don't reconcile, so a careful reader can prove the
map inconsistent with itself.

Practical consequence: **do not spend a panel on factual premises.** One lane, one lens,
and a `unverifiable` list is enough — and cheaper by 10x. The panel earns its cost on a
different failure, the one that actually happened yesterday: a map whose *framing* is
wrong ("no consumer exists, build one") while every individual premise looks fine.

## The next test this implies

Same structure, but plant a **framing** error instead of a fact error:

- FRAMING-FALSE: "the queue's size is the problem" (when the real defect is composition —
  62.5% probe chatter — and 16 readers already exist).
- Ask for a decision, not an audit.
- Measure: does the panel's decision diverge from the framing (i.e. do lenses reject the
  *question*), and does a single lens merely answer it?

Prediction, stated so it can die: at k=1 the model accepts the framing and proposes a
consumer; at k≥3 the panel splits and at least one lens attacks the framing itself. If
k=1 already attacks it, the panel is decoration and yesterday's result was luck.
