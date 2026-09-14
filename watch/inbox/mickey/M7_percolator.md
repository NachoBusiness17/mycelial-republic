# M7 — THE FIVE NACHO NARRATIVE TESTS, PERCOLATED

**Lane:** mickey 7/7 · Perception OS · 2026-09-10 (operator date; box-clock skew noted)
**Deliverable:** `mag/narrative_tests.py` — schema `narrative_tests.v1`, deterministic, $0, stdlib only. Same lexicon-scoring discipline as `mag/percolator.py` (no LLM, no hallucination, evidence attached to every score).
**Entry point:** `run_tests(text_batch: list[str]) -> dict` — drop in a batch of related posts/threads from the same 48-hour window, get five 0-1 scores plus a verdict.

## THE POINT

The operator's Dec 11 2025 post asked one question: is this narrative being **GROWN** or being **PLANTED**? Organic consensus is sloppy and takes days. Manufactured consent is clean, synchronized, and fast. The five tests operationalize that:

| # | Test | Mechanism (text-only, deterministic) |
|---|------|--------------------------------------|
| 1 | **Tears & Trauma** | Suffering-imagery lexicon (kids, grief, "protect them"); hits in the opening two sentences count double — the rollout *leads* with the victim image |
| 2 | **Archetype** | Hero-charge + monster-charge vs nuance/hedge count. Clean hero + clean monster + zero messy middle = max score; a thin cast scores thin |
| 3 | **Phrase Clone** | Best normalized 3-8-gram coverage across documents (case/punct/whitespace collapsed = "near-identical"); all-stopword n-grams discarded — grammatical overlap is not a clone |
| 4 | **Speed & Volume** | Saturation proxies: top-8 content-token concentration (pumped volume has low diversity), urgency markers, and length-uniformity (organic virality is sloppy; campaigns are uniform) |
| 5 | **Punishment** | Guilt-as-enforcement lexicon ("complicit", "silence is consent", "wrong side of history", "anyone who questions"); spread across mouths compounds |

**Verdict:** 4-of-5 positive = MANUFACTURED CONSENT · 3-of-5 = SUSPECTED · <3 = ORGANIC. Flag threshold 0.5.

## TEST RESULTS (3 batches)

| Batch | tears | archetype | clone | speed | punish | Verdict |
|---|---|---|---|---|---|---|
| **A — propaganda rollout** | 1.000 | 1.000 | 1.000 | 0.783 | 0.847 | **MANUFACTURED CONSENT (5/5)** |
| **B — genuine community discussion** | 0.000 | 0.000 | 0.000 | 0.262 | 0.000 | **ORGANIC (0/5)** |
| **C — the fence parable** | 0.000 | 0.000 | 0.000 | 0.391 | 0.000 | **ORGANIC (0/5)** |

- **A** (tri-state: SYNTHETIC TEMPLATE — tonight's links were not piped into this lane, so batch A reconstructs the manufactured shape from the parable itself, clearly labeled in the module as `BATCH_A_PROPAGANDA_ROLLOUT_SYNTHETIC_TEMPLATE`; Supported for the *detector*, Unproven as a claim about any specific real event). Signature found: shared slogan `"protect the children"` in **100% of docs** (clone coverage 1.0), 9 monster hits vs 5 hero hits vs **zero** nuance, punishment spread over 4 of 6 mouths.
- **B**: 10 nuance hits, zero shared content n-grams, no suffering imagery, no enforcement language. The messy middle is exactly what the archetype test measures.
- **C** (fence parable — the counter-narrative control): scores LOW **as required**. Key falsifier evidence: all three posts are *thematically identical* (sit on the fence first, doubt before demolition) yet score **0.000 on phrase clone** — the test keys on lexical synchronization, not topic. Curiosity language ("maybe", "sometimes", "either way") zeroes the archetype test. The parable is the antidote and the detector knows the difference.

## HONEST LIMITS

- Text-only proxies: tests 3-4 are strongest with timestamps/author metadata, which the signature accepts but does not yet use (48h window is assumed by the batch boundary). Real link batches drop straight in.
- Lexicons are the seeded first draft; false-positive log pattern from `mag/percolator.py` (`false_positive()`) is the intended feedback path — not wired here yet, noted for the next lane.
- Batch A is synthetic (labeled). First real 48h window run should be recorded in this file.

## FOLD

Five probes, one question: grown or planted. The fence parable passes its own test — it teaches doubt and the detector reads doubt as organic. Runs on the free lane forever: deterministic, $0, stdlib.
