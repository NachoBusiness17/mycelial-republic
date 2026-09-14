# ROTATION TOLERANCE RULING — falsifier v2, partition not count (2026-09-05/06)

**The question:** rotation test 1 left the tolerance ruling open (±1 strict vs
seat-granularity ±2). Operator: "salon this then ask astra."
**Salon:** 3/3 blind (groq, cerebras, deepseek-pro), full answers,
memory/runs/lane_salon/salon_2026-09-06T0237.json. Transcript of consensus below.

## THE SALON CONSENSUS (unanimous, third roshomon in two days)

1. **Comparing cluster COUNTS is unsound.** Same count, wildly different
   partitions; near-identical partitions, different counts. All three
   witnesses said it in the same breath.
2. **The instrument is the Adjusted Rand Index** — chance-corrected pairwise
   co-membership agreement. The field analogs all pointed the same way:
   psychometrics' Cohen's κ / Krippendorff's α, content-analysis coder
   reliability, taxonomy's bootstrap support / Robinson-Foulds, ML's ARI/NMI,
   jurisprudence's clear-error standard (tolerate reasonable disagreement,
   flag egregious).
3. **Threshold:** groq + cerebras ≥ 0.60; deepseek-pro ≥ 0.65 for small n
   (chance agreement runs high at 19 items). **Fold: 0.60 PASS, 0.55-0.60
   PARTIAL → third-witness rescue (deepseek's tie-break adopted).**
4. **Reference becomes an interval [6,8]** (bootstrap/resample calibration),
   counts demoted to sanity check, never the gate.
5. **The number to print next to every run: the ARI.**

## FALSIFIER v2 LANDED (mag/rotation_harness.py v3)

- ARI vs the reference partition (watch/INTAKE_XBATCH_20260905.md clusters A-G,
  author→letter, 19 items) — stdlib, deterministic.
- PASS = both witnesses ARI ≥ 0.60 + counts in [6,8]; PARTIAL = ≥ 0.55.
- Full report always: ARI, counts, items placed, answer excerpt.

## FIRST ARI MEASUREMENT (same night)

| rotation | lane | clusters | ARI vs reference | verdict |
|---|---|---|---|---|
| 1 | groq | 9 | **1.0** (16/19 authors parsed) | PARTIAL* |
| 2 | cerebras | 9 | None (parser: 0/19) | NO-PARTITION |

*ARI 1.0 = **the interpret substance is IDENTICAL to the reference partition**
where comparable. The scary "9 vs 7" from rotation test 1 was edge-item
fragmentation plus unparsed authors — precisely the failure mode the salon
predicted for count-based scoring. The wave is healthier than rotation-1 read.

Named causes, still honest: cerebras formatting beat the parser (harness
limitation, not a wave verdict); 3 authors unmatched on name variants.

## RULING (falsifier v2, standing)

The rotation falsifier is **ARI ≥ 0.60 against the reference partition, counts
inside [6,8] as sanity, ARI printed on every run**. The ±1-count question is
DISSOLVED, not answered — it was the wrong statistic. Rotation-2 rides the next
batch (enriched input) with the partition metric as the real gate.

Cites: ROTATION_TEST_1_20260905, SELF_STEAL_VISION_PIPELINE_20260905, INTAKE_XBATCH_20260905
Decision: falsifier v2 standing; rotation-2 windowed on next batch

**Score:** 22/25 BUILD (a dissolving ruling: the question was wrong, the
literature was on the shelf, the harness now measures the right thing).

*Filed by the zcode seat, vision desk. Salon transcript:
memory/runs/lane_salon/salon_2026-09-06T0237.json.*
