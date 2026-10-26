# SEAT C: THE EVAL THAT SETTLES LEDGER-ROUTING vs CASCADE vs CLASSIFIER

Written blind (independent of Seats A and B). Author: ractor seat C,
2026-09-29. Em-dash 0; estate claims path-cited; every n, variance, and
cost figure below is ESTIMATE unless it cites a file. Design target:
implementable by the estate's own fleet in five working days, $0 frontier
spend.

## 1. The question, sharpened

PRIMARY: does ledger-informed routing reduce cost-per-verified-solve
relative to (i) a cheapest-qualifying confidence-gated cascade and (ii) a
prompt-classifier router, WITHOUT losing verified-solve rate?
SECONDARY: does the ledger's knowledge go stale faster than it
accumulates (the drift question), and can its verdicts be poisoned (the
trust question)? These map to the adversary's pre-registration conditions
C1-C7 without requiring this seat to adopt them.

## 2. Arms (all four share identical gates and identical task corpus)

- ARM 1 LEDGER: gps-mcp selection driven by measured capability (the
  shipped v0 router, `tools/gps_mcp/router.py`, possibly with its
  threshold overridable per arm config; this eval tests the CONCEPT, any
  v1 refinements are amendments to this harness).
- ARM 2 CASCADE: pure FrugalGPT shape: local tier first, escalate one
  tier on returned confidence < 0.8 (v0's own cascade mechanics with the
  ledger BLINDFOLDED: thresholds ignored, selection = tier order only).
- ARM 3 CLASSIFIER: a small local model (gemma class, per the fleet in
  `AGENTS.md`) reads the task text and picks the tier; no ledger, no
  cascade. This is the "cheap intelligence instead of bookkeeping"
  baseline.
- ARM 4 FIXED-MID: always the designated mid tier (v0's exploration
  model, `tools/gps_mcp/config.json` exploration_model). Sanity floor:
  any clever arm that cannot beat fixed-mid is decoration.

## 3. Task corpus and gates (the part that makes it honest)

Five shapes, matching the shipped fixture taxonomy
(`tools/gps_mcp/seed_fixtures.py`), each with a MACHINE gate so
cost-per-VERIFIED-solve is real, not self-reported:

| Shape | Gate (class) | Item source | Target items (ESTIMATE) |
|---|---|---|---|
| tool_call_parse | G0: JSON-schema + executable-tool validation | estate queue items + synthetic mutations | 50 |
| yes_no_decision | G0: exact match to pre-labeled answer key | estate decision logs with labels | 50 |
| summarize | G1: dual-independent rubric, agreement threshold | estate documents | 40 |
| code_review | G0: does the flagged line set match seeded ground truth | seeded repos with injected defects | 40 |
| design_judgment | G2: operator rubric (weight-0.5 verdicts) | archived design asks | 20 |

Total: 200 items (ESTIMATE; scale after pilot variance read). SEED/EVAL
SPLIT is mandatory and structural: the ledger arm's starting history
comes from a DISJOINT seed corpus (fresh items per shape, target 30 per
cell for the 6 fixture models, reusing the deterministic seeding pattern
of `tools/gps_mcp/seed_fixtures.py` but from measured double runs, not
hand-picked literals). Eval items NEVER contribute to the ledger before
being scored, else Arm 1 is graded on its training set.

Determinism law (house): test doubles are deterministic by sha256 of
payload (`tools/gps_mcp/providers.py` per
`tools/gps_mcp/README.md`); corpus sampling and item-to-arm
assignment use seeded selection, no RNG, so reruns are byte-comparable.

## 4. Fleet and spend

- Local tier: real Ollama endpoints (scut/gemma class per `AGENTS.md`).
- Mid tier: the FUNDED metered lane only (Nous/Hermes credits per
  `AGENTS.md` DRIVING LADDER 202609-28; Anthropic keys are unfunded).
- Frontier tier: TEST DOUBLE ONLY in this eval. Honest consequence: the
  eval cannot measure true frontier economics; it measures ROUTING
  QUALITY with frontier priced at the fixture constant 0.12 USD/call
  (`tools/gps_mcp/seed_fixtures.py` FIXTURE_COSTS). Any conclusion that
  hinges on frontier real behavior is out of scope and said so.
- Estimated total mid-tier burn: 200 items x 2 mid-using arms x <= 2
  calls x ~0.004-0.009 USD = under 10 USD (ESTIMATE). Local: minutes of
  Ollama time. Frontier: 0.

## 5. Randomization and pairing

PAIRED design: every item runs through ALL FOUR arms (same input bytes,
same gate). Order of arms is permuted per item by seed to cancel
position effects (doubles are deterministic, so ordering matters only for
live endpoints; still permuted for hygiene). Pairing converts the primary
metric into per-item cost differences between arms: the right unit of
analysis is the paired delta, not two independent samples.

## 6. Metrics

- M1 COST-PER-VERIFIED-SOLVE (primary): (sum of all call costs + all
  gate costs for the item) / (verified solves), per arm, compared as
  paired differences on log cost. Gate costs are included for ALL arms:
  a cheap answer that fails the gate and re-climbs is charged its whole
  trace, which is the honest accounting the research brief demands
  (`watch/inbox/game_platform_basecamp_20260929/DELEGATION_RESEARCH_20260929.md`,
  economics: failed tasks cost MORE than solved).
- M2 VERIFIED-SOLVE RATE: per arm per shape; guard metric
  (non-inferiority, not superiority).
- M3 ESCALATION WASTE: cost spent on non-final tiers / total trace cost,
  per arm. The cascade's signature risk; the ledger's claim to fix it.
- M4 STALE-RATE INCIDENTS (drift injection): mid-run, swap the test
  double's behavior for ONE mid model on ONE shape (pass collapses, e.g.
  0.93 to 0.50 as a double knob, since doubles expose per-shape
  confidence/behavior config per `tools/gps_mcp/README.md` config
  section). Then run 50 fresh routed requests on that shape per arm.
  Count incidents = routes to the collapsed model after its cell
  should have demoted. Cascade predicts robust (per-instance gates);
  ledger predicts faster recovery on repeat traffic IF its update loop
  works; fixed-mid predicts max incidents. Also record detection latency:
  fresh verdicts needed before the cell demotes.
- M5 VERDICT THROUGHPUT: operator minutes per accepted verdict, per gate
  class (the organ-tax meter; G0 should be ~0, G2 is the bottleneck).
- M6 CALIBRATION ERROR (ECE): per model per shape over the eval's
  confidence readings vs gate outcomes. The escalation trigger in every
  arm leans on self-confidence; if ECE is high for a shape, confidence-
  triggered escalation is noise there, whatever the routing scheme.

## 7. Sample size (derivation, all ESTIMATE numbers)

Pilot first (Day 3): 60 items/shape-pooled to read sigma_log (sd of log
item cost) and pairing correlation rho. Planning assumptions:
sigma_log = 0.5 (ESTIMATE), rho = 0.6 (ESTIMATE), target detectable
cost reduction r = 15% (ESTIMATE, the smallest saving that would justify
the organ), two ledger comparisons (Arm1 vs Arm2, Arm1 vs Arm3) so
Bonferroni alpha = 0.025, power 0.80.

Paired n per comparison (z_{alpha/2}=2.24 at Bonferroni alpha 0.025,
z_{power}=0.84):
n = (2.24 + 0.84)^2 x 2(1-rho) x sigma_log^2 / ln(1/(1-r))^2
= 9.49 x 0.8 x 0.25 / (0.1625)^2 = 9.49 x 0.2 / 0.0264 = about 72,
padding for shape stratification and gate failures:
TARGET n = 120 items per arm (ESTIMATE), i.e., the 200-item corpus has
enough headroom; if pilot sigma is worse (0.8), n needed is about 2.6x
more and the corpus doubles to 500 items (ESTIMATE) or the claim shrinks
to "ledger does not lose" (equivalence framing).

M2 guard: solve-rate non-inferiority with margin 5 points at p ~ 0.85
needs roughly 250+ per arm for a clean one-sided test (ESTIMATE); at
n = 200 the guard is run as a pre-registered kill rule instead of a
powered test (K2 below), which is honest about what 200 items can and
cannot show.

## 8. Kill rules (pre-registered falsifier thresholds)

- K1 (concept kill): Arm 1's M1 is not at least 10% better than Arm 2
  AND at least 10% better than Arm 3, with the paired 95% CI excluding
  zero on log cost. => LEDGER LOSES ROUTING AUTHORITY: it survives only
  as an instrument (report/dashboards), the adversary's concession.
- K2 (quality kill): Arm 1 verified-solve rate is more than 3 points
  below Arm 2 (ESTIMATE threshold chosen so the paired kill is detectable
  at n = 200; 3+ points on 200 items is ~6 paired flips, a visible
  signal). => kill regardless of cost win.
- K3 (drift kill): Arm 1 commits more than 5 stale-rate incidents in the
  50-request post-swap window, or its detection latency exceeds 10 fresh
  verdicts. => the ledger's update loop is too slow for a moving fleet;
  decay/probe redesign required before any rerun.
- K4 (organ kill): M5 shows accepted G2 verdicts costing more than
  5 operator-minutes each on average, or seed-corpus filling exceeding
  one operator-day. => the organ tax exceeds plausible savings; cap the
  ledger at G0-only shapes.
- K5 (trust kill): red team lands ANY of: a forged verdict accepted, a
  replayed verdict double-counted, one evidence_hash accepted for two
  different answers, or a cell inflated over threshold without its
  receipts chaining. => the verification-gate contract fails CLOSED:
  no graduation until patched and re-run.

## 9. Five-day schedule (receipts per day, `watch/inbox/` panel dir)

- D1: corpus + gates + answer keys + seed corpus build (all G0 gates
  machine-run; G2 rubric drafted).
- D2: four arms wired over the SAME router boundary (arm = config +
  selection override, not a fork; preserves v0's one-call-boundary law,
  `tools/gps_mcp/README.md` What v0 deliberately does not do).
- D3: pilot 60 items, variance read, sample-size recompute, go/no-go on
  corpus size.
- D4: full run (200 items x 4 arms), drift injection, receipts land.
- D5: red team (K5 attacks), analysis, kill-rule adjudication, report
  file. Every phase leaves a receipt row in this panel dir; numbers are
  filed from the runs, never hand-copied (census law,
  `AGENTS.md` Clippy tests bullet).

## 10. What this eval cannot settle (said out loud)

Frontier-tier economics (doubles only); shapes without honest gates
(design_judgment at n=20 G2-weighted is directional at best); and the
long-run organ tax beyond one week. If the eval says "keep", it licenses
a production pilot, not a throne (no core-mirror throne,
`AGENTS.md` Zeitgeist line).

Em-dash count: 0.
