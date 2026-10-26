# D6 LANDED - monoculture agreement-rate proxy adapter (2026-10-05 night shift)

Door: D6-monoculture-proxy (eleven-doors ledger) - "monoculture
agreement-rate proxy as adapter. import mag/roshomon.py:140-176
primitives + reimplemented grouping loop (~15 lines, :205-214 shape);
NEVER compare() (_answers_for :179-186 welded to k8s PVC)". The door's
falsifier made law: "0.55 threshold groups all-or-nothing on the
24-wide lane chapters kills the estimate".

## What landed

**tools/monoculture_proxy.py** - the adapter:

- imports ONLY the door-named primitives (_invariant_statements,
  _clean, _tokens, _overlap); the grouping loop is reimplemented
  (~15 lines, same [representative, witnesses] shape, extended with an
  instance counter); compare()/_answers_for never touched (k8s-welded).
- SWEEPS thresholds 0.40/0.55/0.70 and reports sensitivity per
  threshold - no single-threshold estimate to kill.
- UNMEASURABLE verdicts, honestly: zero-core at every threshold
  (nothing recurs) or mass at every threshold (agreement > 0.9 with
  every witness merged) or < 10 statements. The falsifier's
  all-or-nothing case reports as a non-measurement, never a fake
  number.
- third agreement organ beside env_contract.run_legality and
  overmind_judge: agreement_proxy = statement INSTANCES in core groups
  (>= 2 witnesses) / all statement instances.
- history at memory/monoculture/history.jsonl (label-keyed); a
  core-size drop vs the last row for the label appends one line to
  memory/attention.md (the operator's triage board).

**tests/test_monoculture_proxy_20261005.py** - 6 tests (identical
witnesses = mass/unmeasurable, disjoint = zero-core/unmeasurable,
partial overlap = measurable, grouping overlap semantics, history +
alert-on-drop contract, no-alert-on-rise). The identical-texts test
caught a REAL module defect on its first run: the dominance metric
divided witness counts by statement totals (category error), and the
agreement denominator counted distinct (group, witness) pairs while
n_statements counted instances - tripled identical text read 0.4
instead of 1.0. Both fixed in the module (dominant_witness_share =
largest group's witness share; instance-counted agreement), which is
the falsifier doing its job before shipping.

## Production baseline (live lane surfaces, 2026-10-05T08:44Z)

7 witnesses (android_surface, bard_ledger, builder, day_work,
economist, elder, research), 929 statement instances:

    t=0.40: 505 groups, 53 core, agreement 0.308
    t=0.55: 658 groups, 28 core, agreement 0.117
    t=0.70: 737 groups, 12 core, agreement 0.048
    MEASURABLE: True; dominant witness share 1.0 with agreement 0.117
    (a few statements recur across all lanes; 88% of instances are
    single-witness)

THE READ: the estate's lanes are far from monoculture - at the
canonical 0.55, 88% of what lanes say is unique to one witness, and
the sensitivity sweep degrades smoothly (0.31 / 0.12 / 0.05), not
all-or-nothing. Baseline banked; future runs alert attention.md if the
0.55 core group count drops below 28.

Honesty note: two history rows banked during the build (08:33Z, 08:35Z)
under the pre-instance arithmetic were cleared when the instance fix
landed - they measured 73 (witness-pair sum) where the shipped
semantics counts 28 (core groups); keeping them would have fired a
false drop-alert on the first post-fix run. The 08:44Z row is the
baseline of record.

Caveat: the lane surfaces are different-job lanes (economist vs builder
write about different work), so low cross-lane agreement is partly
structural; the proxy's value is the TREND line + the attention alert
on drop, and running it on same-question corpora (--texts) when those
exist.

Banked by GLM-5.3 window (night shift), 2026-10-05.
