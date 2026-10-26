# B2-262 receipt (2026-09-26)

## Verdict

NOT CLEAN, NO EDIT LANDED (probe-then-edit per the B2_219 pattern; the probe decided). Both adjacency variants the probe built fail the bar. Naive strict adjacency (match-at unit token) fails the brief's own falsifier outright: it re-dates 7643939 "This yields a transfer rate of 22.7 megabytes per second." because the unit is a mega compound the touching-anchor cannot see. Token-level adjacency (unit anywhere inside the touching token, the strongest defensible reading) kills both pins correctly but RE-DATES 2 sites per 6,242 drops that the window correctly kills, each becoming a new wrong ledger row: 1169101 "CLAS - Sec 11A P 2.2 [important]" (a document section reference; only "Sec" in the window knows it) and 7039475 "Umbrella SURV (leapfrog [1-4] points of contact)." (bracket-separated range with its unit noun). The 12-char window stays. Zero of the pinned keeper rows drop under any variant (0 keeper deletions), and check7 remains byte-equal PASS because the ledger bytes are untouched.

## Evidence file:line quotes

- The window under test: scripts/the50_t21_q_caption_ledger.py:539 `near = sent[max(0, m.start() - 12): m.end() + 12]` / `if QUANTITY.search(near): continue` (NUM_NOY path) and :552-553 the same plus `or "$" in near` (DOT_NOY path).
- Probe population: watch/inbox/qdrop_export/qdrops.jsonl, 6,242 drops, 273 candidate sites (221 NUM_NOY + 52 DOT_NOY) swept through the module's own clean_text/sentences and both guard decisions (watch/inbox/burn_wave_20260926/B2_262_adjacency_probe.py, results watch/inbox/burn_wave_20260926/B2_262_adjacency_probe_results.json).
- Probe results (all variants): window kill vs strict adjacency differ on 4 sites; window vs token-level adjacency differ on exactly 2: 1169101 and 7039475, both window_kill=true token_adj_kill=false, both classified new_wrong_row_under_adjacency. 0 sites in the killing direction (no variant deletes an existing ledger row; the 19 pinned keepers and "by 11-11" are untouched by every variant).
- Pins: 1416139 "Why has it taken 1.5 yrs?" window_kill=true token_adj_kill=true (safe under both variants); 7643939 "22.7 megabytes" window_kill=true token_adj_kill=true but STRICT adjacency kill=false, i.e. the naive variant re-dates the drop the brief named as its own falsifier (ts places it, DOT_NOY would read 22.7 as 1970-07-22-class).
- Verifier baseline before the probe (untouched after): check7 guard pin "resurgent 0, keepers byte-equal 77/77 PASS", RESULT PASS - 267 rows, 163 drops.
- Why the window's "whole-word unit anywhere" over-kill is load-bearing at exactly these sites: 1169101 survives adjacency only because the killing unit is "Sec" (the \bsecs?\b alternative of QUANTITY, scripts/the50_t21_q_caption_ledger.py:212-220), a section-label abbreviation 8 chars before the number; adjacency by construction cannot see it, and extending adjacency to see it IS the window again. B2-242 already cured the window's proven false-kill class (inside-word matches: b-day, attack, coming) with boundary bounding, so the remaining over-kill is down to 2 sites in 6,242, both of which are true kills by misdate outcome.

## Work done

1. Read the guard block, the two window sites, and the B2-242/B2-219/B2-68 probe precedents; ran the verifier for the PASS baseline before any idea of an edit.
2. Built the probe (B2_262_adjacency_probe.py) with three adjacency variants (strict match-at, touching-span search, token-level), ran all over the full 6,242-drop corpus through the module's own sentence pipeline, diffed guard verdicts site by site, and cross-referenced every differing site against the live ledger ids.
3. Caught my own first-cut probe defect (anchor semantics hid compound units) which is itself a finding: the pin drop 7643939 kills naive adjacency variants.
4. Applied the brief's decision rule: the edit was conditional on a clean sweep; the sweep is not clean (2 new wrong rows on the best variant, 1 falsified pin on the strict variant), so the ledger script is untouched and the window stands. Receipt, probe, and results JSON are the landing.

## Falsifier

The brief's falsifier held in both directions: no variant re-dates 1416139 (token adjacency kills it) and no variant drops a pinned keeper row; but the strict variant re-dates 7643939, and the best variant re-dates 1169101 and 7039475, so the edit fails on the add-side even though the delete-side is clean. Reopen conditions, pre-registered: (a) a variant that keeps all 77 keeper rows byte-equal AND adds zero wrong rows on this corpus; the probe file re-runs as-is and must print diff_sites 0 with both pins killed; (b) the 1169101 class acquires its own properly-caused guard (a section-reference guard that fires on "Sec 11A P" before the number), at which point token adjacency plus that guard can be re-probed; that is a new brief, not a guard branch here.

## Bibliography closed

- scripts/the50_t21_q_caption_ledger.py (guard block 186-320, window sites 539-553; UNMODIFIED)
- scripts/the50_t21_q_caption_ledger_verify.py (baseline PASS run, check7 77/77)
- watch/inbox/qdrop_export/qdrops.jsonl (6,242 drops swept); watch/inbox/qdrop_export/q_caption_ledger.jsonl (267 rows, id set cross-reference)
- watch/inbox/burn_wave_20260926/B2_262_adjacency_probe.py + B2_262_adjacency_probe_results.json (artifacts)
- watch/inbox/burn_wave_20260926/B2_242_quantity_bounds_20260926.md (boundary-bounding precedent; the fixed class stays fixed)
- watch/inbox/burn_wave_20260926/B2_219_misdate_classes_20260926.md (probe-then-edit pattern)
