# B2-72 curvature keyword-order sensitivity · 2026-09-26

## Verdict

NOT ORDER-ROBUST. The settlement ("adventure_2d6 is the cheapest hill, 0.483,
+0.017 from the 0.5 bar") is an artifact of the as-shipped first-match
assignment order. Holding the order and varying keyword sets moves the cosine
at most 0.003 (settlement survives). Swapping water_computer ahead of
adventure_2d6 moves adventure by -0.276 (0.483 to 0.207) and hands "cheapest"
to water_computer at 0.482, margin 0.018. Full order reversal makes adventure
DARK (grok loses all 7 paragraphs) and hands "cheapest" to audit_dungeon at
0.039. What does survive every variant: both regions stay SADDLE (nothing
crosses 0.5), and "some region sits about 0.017 from the bar" holds, but WHICH
region is order-fragile. Any quote of 0.483 as builder agreement must name the
assignment order that produced it.

## Evidence

- `tools/curvature_scan.py:133-134`: `keys = {"adventure_2d6": ["2d6", "ford",
  "river", "adventure"], "water_computer": ["water", "cistern", ...]}`
  adventure declared first; `:142-144`: `for r, kws in keys.items():  #
  adventure first: 'river ford' paragraphs` / `if any(k in low ...):` /
  `break`.
- `REFEREE_VERDICT_20260926.md:28-30`: "The cheapest hill: adventure_2d6 is
  0.483, only +0.017 from the 0.5 HILL bar."
- Baseline gate: probe reproduces all six filed cosines bit-for-bit
  (0.483/0.358/0.129/0.134/None/0.124 vs CATHEDRAL_CURVATURE_SCAN_20260921.json).
  Unrounded adventure cos 0.48307382, margin 0.01692618.
- Contested boundary: 4 grok + 7 deepseek paragraphs match BOTH keyword
  families; these are exactly the paragraphs the swap moves (adventure paras
  7/11 to 3/4, water 4/7 to 8/14).

Run table (adv = adventure_2d6 cos (delta), wat = water_computer cos (delta),
cheapest region = gap to 0.5):

| variant | adv | wat | cheapest |
|---|---|---|---|
| baseline_as_shipped | 0.483 (+.000) SADDLE | 0.358 (+.000) | adventure (.017) |
| swap_water_first | 0.207 (-.276) | 0.482 (+.124) | water (.018) |
| full_reverse_order | DARK | 0.364 (+.007) | audit (.039) |
| kw_adv_minus_river | 0.483 (+.000) | 0.358 (+.000) | adventure (.017) |
| kw_adv_minus_river_ford | 0.480 (-.003) | 0.353 (-.005) | adventure (.020) |
| kw_adv_minus_adventure | 0.483 (+.000) | 0.358 (+.000) | adventure (.017) |
| kw_water_plus_river_ford | 0.483 (+.000) | 0.358 (+.000) | adventure (.017) |
| swap_plus_adv_minus_river_ford | 0.236 (-.247) | 0.482 (+.124) | water (.018) |

- River-only invariance explained: zero paragraphs in either normal match
  adventure only via "river", so dropping that keyword changes nothing.
- Mirror finding: under swap the claiming region sits at 0.482/0.483 either
  way; the contested 11 paragraphs carry nearly all shared signal.
- Side finding: `version_deepseek.md:515` ends mid-sentence "action: push
  right from (0," at byte 27594, no trailing newline; the deepseek normal is
  truncated (blob-double Level 3 cut off).

## Work done

Read tools/curvature_scan.py in full, version_grok.md (115 lines),
version_deepseek.md (515 lines) in full, B2_17 receipt + B2_17_verify.py,
both filed scan JSONs, TRIANGULATION_20260921.md, REFEREE_VERDICT_20260926.md.
Wrote B2_72_order_probe.py (independent reimplementation, parameterized
ordered config, baseline gate against filed bytes), ran 8 variants plus
paragraph-destination trace under .venv/Scripts/python.exe. Results in
B2_72_results.json.

## Falsifier

(1) A byte change to either normal or to build_sections that makes the swap
variant leave adventure above 0.5 or cheapest would invert "not order-robust".
(2) A filed scan whose cosines my baseline gate fails to reproduce.
(3) Proof that some paragraph matches adventure only via "river" (would break
the invariance explanation). Not tested: order permutations beyond the two
extremes (full space is 720 orders); interplay with other regions' keyword
sets varied simultaneously. Filed as owed.

## Bibliography

tools/curvature_scan.py; memory/runs/combined_game_triangulation/
version_grok.md + version_deepseek.md + TRIANGULATION_20260921.md; watch/inbox/
CATHEDRAL_CURVATURE_SCAN_20260921.json + _20260922.json; watch/inbox/
REFEREE_VERDICT_20260926.md; watch/inbox/burn_wave_20260926/
B2_17_adventure2d6_20260926.md + B2_17_verify.py; B2_72_order_probe.py +
B2_72_results.json (this lane). Closed 2026-09-26.
