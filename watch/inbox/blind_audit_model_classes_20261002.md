# BLIND AUDIT: MODEL CLASSES (premium autopsy corpus, 2026-10-02)

Question: do the model-class boundaries (frontier/flash/local tiers, the
9-family garden grid, the inference_budget recipes) predict output quality,
or are they taxonomy theater (4th specimen of the number-does-not-match-
distinction class)?

HEADLINE: HALF THEATER. The local/remote boundary is brutally real. The
flash-vs-frontier ladder among remotes is theater on totals (0.04 gap, SHAPE
tied, EVIDENCE inverted) with one honest residue: +0.15 CORRECTNESS and the
runtime-simulation column. The QUESTION axis predicts (36.3 percent of remote
variance); the FAMILY axis barely does (3.6 percent). A question taxonomy
wearing a model taxonomy.

## 1. METHOD

Corpus: 102 files watch/inbox/model_garden/PA-<QID>-<fam>.md (17 questions x
6 families, byte-identical asks; MANIFEST premium_autopsy/MANIFEST.json).
Protocol (blind, seed 20261002):
1. Stripper state/blind_strip_20261002.py: drops family-naming lines (regex
   glm|deepseek|ds|kimi|qwen|grok|gemma|nous, case-insensitive) from the top
   10 lines only (deeper mentions are question content; C1 names
   Llama/Qwen/Gemma lineages in the ask itself), shuffles, emits
   state/blind_model_sheet_20261002.json; secret map to %TEMP%, never into
   repo or receipt.
2. Grader state/blind_grade_20261002.py: fixed rubric, 0-2 each. EVIDENCE =
   citation density + quoted-byte specificity. CORRECTNESS = up to 6
   checkable claims (quotes, symbols) verified against the frozen evidence
   bytes and the repo tree (presence-anywhere = fabrication test). SHAPE =
   deliverable coverage from the 17 contracts (state/pa_contracts_20261002
   .json) + word limits + off-topic overlap. Hand adjudication of all 20
   flagged citation fails: 5 artifacts/paraphrases dropped, grep-verified
   resolves credited, ONE genuine fabrication kept (symbol `_series_point`,
   0 grep hits in the claimed frozen tail). Calibration: the 3 zero-scores
   hand-read, confirmed real; 6-scores spot-read, confirmed.
3. Rejoin state/blind_rejoin_20261002.py: secret map + statistics.
Caveats (named): EVIDENCE under-credits prose-native styles (kimik2 lowest E
but 1.0 C); CORRECTNESS audits anchored claims only.
Tier map (estate's own): local = gemma4 (providers.yaml:120-121 tier_max T1);
flash = glm53 + ds41 (RIB_MODEL_GARDEN_ROUTING.md:227-228 "mesh"); frontier =
kimik2 + qwen38max + grok47 (paid judgment lanes, RIB_DRIVING_LADDER per
AGENTS.md). Moving kimik2 to a middle rung changes nothing: it ties glm53.

## 2. BLIND SCORE TABLE (rejoined; totals 0-6)

| family | mean | sd | E | C | S | sixes | zeros | $/ask (receipt :147-151) | $/point |
|---|---|---|---|---|---|---|---|---|---|
| gemma4 (local) | 0.76 | 0.88 | 0.29 | 0.06 | 0.41 | 0 | 8 | 0 | n/a at shape |
| glm53 (flash) | 3.35 | 1.33 | 0.59 | 0.82 | 1.94 | 1 | 0 | 0.0012 | 0.00036 |
| ds41 (flash) | 3.94 | 1.73 | 1.00 | 1.12 | 1.82 | 5 | 0 | 0.0078 | 0.00198 |
| kimik2 (frontier) | 3.35 | 1.08 | 0.41 | 1.00 | 1.94 | 1 | 0 | 0.013 | 0.00388 |
| qwen38max (frontier) | 3.94 | 1.51 | 0.82 | 1.12 | 2.00 | 5 | 0 | prepaid | prepaid |
| grok47 (frontier) | 3.76 | 1.16 | 0.82 | 1.24 | 1.71 | 2 | 0 | 0.032 | 0.00851 |

QID x family grid (totals; rows by question mean):

| qid | gemma4 | glm53 | ds41 | kimik2 | qwen38max | grok47 | qmean |
|---|---|---|---|---|---|---|---|
| R2 | 0 | 2 | 1 | 3 | 2 | 2 | 1.67 |
| LENS1 | 1 | 1 | 2 | 2 | 2 | 3 | 1.83 |
| R1 | 0 | 2 | 3 | 2 | 3 | 3 | 2.17 |
| S5stores | 1 | 2 | 2 | 3 | 2 | 4 | 2.33 |
| S7mates | 3 | 3 | 2 | 2 | 3 | 2 | 2.50 |
| DG1 | 2 | 2 | 2 | 4 | 3 | 3 | 2.67 |
| S6docker | 1 | 3 | 3 | 3 | 3 | 3 | 2.67 |
| D1 | 0 | 3 | 6 | 3 | 3 | 4 | 3.17 |
| B2 | 0 | 3 | 5 | 3 | 6 | 3 | 3.33 |
| D2 | 0 | 4 | 4 | 3 | 4 | 5 | 3.33 |
| A1 | 0 | 5 | 5 | 4 | 4 | 4 | 3.67 |
| D3 | 1 | 5 | 6 | 3 | 3 | 4 | 3.67 |
| S8stealth | 2 | 3 | 3 | 5 | 6 | 4 | 3.83 |
| S4verkle | 0 | 4 | 5 | 3 | 6 | 6 | 4.00 |
| C1 | 1 | 5 | 6 | 6 | 5 | 3 | 4.33 |
| S1boot | 0 | 6 | 6 | 3 | 6 | 6 | 4.50 |
| S2surface | 1 | 4 | 6 | 5 | 6 | 5 | 4.50 |

## 3. CLASS-BOUNDARY VERDICTS

TIER LADDER (local < flash < frontier), per metric:
- TOTAL: local 0.76, flash 3.65, frontier 3.69. HOLDS at the local rung
  (collapse, 8/17 zeros, ctx-8192 contract-cut), COLLAPSES above it (gap
  0.04 of 6). SHAPE: 1.88 vs 1.88, EXACT TIE; contract-following does not
  know the tier. EVIDENCE: 0.79 vs 0.69, INVERTED (the cheap class cites
  more verifiable bytes). CORRECTNESS: 0.97 vs 1.12, WEAKLY HOLDS (+0.15,
  grok47 top at 1.24): the only metric residue of the quality ladder.
- Verdict: real as a LOCAL gate and a PRICE ladder (grok47 = 23.6x glm53 per
  blind point), not as an output-quality ladder.

9-FAMILY GRID (BATTERY.md:289-291): among the 5 remotes, family explains
3.6 percent of score variance, question 36.3, residual 60.2. Max pairwise
gap 0.59; two exact ties (glm53=kimik2=3.35, ds41=qwen38max=3.94). With
gemma4 in, family explains 41.7 percent, all of it the local rung. The 6
families are 2 effective classes: local-incapable vs remote-competent blob.

QUESTION-CLASS LAW (mesh reads / frontier simulates, rib :234-242):
blind-confirmed. On the rib-named simulation asks (S5stores, S4verkle):
frontier 4.00 vs mesh 3.25 (+0.75); on the 15 readable asks: mesh 3.70 vs
frontier 3.64 (tie). Family effects concentrate exactly where the rib says
the premium dollar belongs. Spread is widest on C1/S1boot/S2surface (5 pts,
evidence-heavy audits), narrowest on S7mates (1) and LENS1/R2.

## 4. CONTRADICTIONS VS DECLARED CLASSES

1. RIB_MODEL_GARDEN_ROUTING.md:227 "glm-5.3-flash WIN 17/17, mesh-convergent"
   vs blind C 0.82 and E 0.59: WIN 17/17 is a TRANSPORT verdict (content
   arrived) wearing a quality costume; blind scores rank glm53 last-but-one
   among remotes on anchored correctness.
2. Same rib :231 grok-4.7 "WIN 17/17 unique finds" vs blind total 3.76 (gap
   0.18 to ds41) at 4.1x ds41 price/ask and 4.3x/point: CHAMPION is a
   find-uniqueness claim, not superiority; read as quality it misroutes.
3. The "SENSING ONLY" flash label (rib :130-135, qwen3.7-flash row,
   generalized by RIB_FREE_USAGE_POLICY) does not transfer to the flash TIER:
   ds41 outscores 2 of 3 frontier families and beats frontier on EVIDENCE.
   Sensing-only is a SKU verdict; one bad SKU smears a whole rung.
4. mag/inference_budget.py:211-219 + classify_shape :247-249 split asks by
   SIZE only (18K small/review). The only quality boundary in the corpus is
   by QUESTION CLASS (36.3 percent of variance): the recipes have no knob
   for the axis that predicts. No recipe row is contradicted on fire
   mechanics (85/85 remote fires landed content, zero EMPTY_REASONING); the
   contradiction is scope, not wrongness.
5. PREMIUM_AUTOPSY.md:147-153 was graded by one author (its :184 admits no
   blind grader); the WIN/PARITY ordering (ds + qwen tops) survives
   blinding, the per-family EVIDENCE story does not: blind E ranks ds41 1.00
   vs glm53 0.59, a spread that receipt never names.

CONFIRMED (not theater): gemma4 DNF-BY-WINDOW (rib :232) reproduced, including
its escape hatch (best cells DG1=2, S7=3, the smallest bodies);
mesh-matched-on-14/17 (:81-97) reproduced independently; kimi row
(inference_budget.py:150-162) consistent.

## 5. THREE NAMED IMPROVEMENTS

1. RIB AMENDMENT (routing): at review shape, collapse the remote ladder to
   TWO verdict classes (LOCAL-INCAPABLE / REMOTE-COMPETENT) plus a
   SIMULATION-RESERVE flag on grok-4.7-high-effort only. Route by question
   class FIRST (readable -> cheapest competent remote, glm53 $0.00036/point;
   simulation -> reserve), family second. Rib :227-232 rows gain the blind
   C/E/S triplet beside every WIN.
2. RECIPE CHANGE (mag/inference_budget.py): add a SIMULATION shape to
   classify_shape() (keyword-gated: lock semantics, os/ntfs/cpython asks)
   that raises the floor and returns a route-to-reserve plan_call flag; add
   an EVIDENCE-DENSITY post-check to guard_terminal(): review-shape replies
   with under 2 anchored citations bank a thin-evidence row and sanction ONE
   cite-bytes retry (changed params, no terminal-marker conflict).
3. STANDING INSTRUMENT (blind gate): promote the stripper/grader pair to
   tools/blind_audit.py with the map-to-%TEMP% law; rib law 1 (instruments
   only, RIB_MODEL_GARDEN_ROUTING.md:47-53) should require a blind-grid run
   before any WIN/CHAMPION cell routes dollars (gap its :184-185 names).

## 6. FALSIFIER AND LIMITS

Falsified if: (a) a small-body rerun (under 12K chars) still shows
flash=frontier (then even the sim-reserve claim is shape-luck); (b) the sim
column flips on a second simulation question set (then +0.75 is noise, n=2
questions x 3 families). Limits: one moment (2026-10-01 fires), E-bias toward
citation-dense styles, correctness audits anchored claims only, kimik2 and
qwen38max $/point are prepaid upper bounds. Artifacts:
state/blind_model_sheet_20261002.json + blind_grades_20261002.json +
blind_rejoin_20261002.json. Mapping: TEMP only, not in this receipt.
