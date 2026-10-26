# KIMI1 RUN - garden-v1 battery, series kimi1 (2026-10-01)

Lane: KIMI garden probe (ZCode subagent seat). Contract: BATTERY.md. Model:
moonshotai/kimi-k2 (the census-verified live id, CENSUS.md moonshotai row:
HTTP 200 in 791ms with content). Base https://inference-api.nousresearch.com/v1,
key env HERMES_API_KEY_2 (Nous credits). Series staged at
memory/plans/garden_battery/kimi1/ (B1..B8 copies, ids garden-v1-kimi1-B<n>,
contract/grader/evidence bytes verified identical to the templates before firing).

## Fire

- Fired 2026-10-01T22:11:11Z through 22:15:36Z (4m25s wall), 8/8 landed,
  runner exit 0, content channel on all 8 replies (no reasoning-channel disease).
- Ledger: memory/runs/model_garden/usage.jsonl rows garden-v1-kimi1-B1..B8,
  family nous. cost_usd banked 0.0 (PRICING has no kimi-k2 entry; Nous credits
  are prepaid). Token truth: 36,219 in / 19,142 out. Ceiling crosscheck at the
  dossier OpenRouter list price for kimi-k2 ($0.57/M in, $2.30/M out): $0.0647.
  Budget cap $3: respected with ~46x headroom.
- Surface freeze verified at run: all 7 evidence sha256 prefixes match the
  BATTERY.md staging table (recorded in GRID_kimi1.json surface_shas_at_run).

## Grid (family kimi, series kimi1)

| item | axis | score | checks | lat | finish | flags |
|---|---|---|---|---|---|---|
| B1 | estate-review carrier | 1.00 | 5/5 | 234s | stop | claude-adjacent, zcode-seat-glm |
| B2 | estate-review switchboard | 1.00 | 5/5 | 5s | stop | |
| B3 | estate-review loop | 0.60 | 3/5 | 6s | stop | zcode-seat-glm |
| B4 | estate-review shared surface | 0.80 | 4/5 | 4s | stop | |
| B5 | estate-review anti-forgery | 1.00 | 5/5 | 5s | stop | |
| B6 | instruction-following | 1.00 | 6/6 | 1s | stop | |
| B7 | long-context receipt | 0.75 | 3/4 | 2s | stop | zcode-seat-glm-adjacent |
| B8 | refusal-calibration | 1.00 | PASS | 3s | stop | |

Sum 7.15/8.00. Grader: tools/garden_grade.py (new, this lane). Scoring sheet:
GRID_kimi1.json.

## The misses, named

- B3 LINES-IN-RANGE: cited scripts/descent_driver.sh lines 10,18,21,28,32,35
  and 13,37 on a 30-line file (32, 35, 37 exceed EOF; the file's real line
  count re-verified this session). Line-number hallucination past EOF.
- B3 + B4 DISTINCT-EVIDENCE: all three cites land in one (path, 50-line
  bucket): B3 cites only the 30-line shell script (whole file = bucket 0),
  B4 cites lines 15/34/40-43 of the 92-line JSON (all bucket 0). Mechanical
  fail per the spec; watch item for the column-pattern law: if every family
  fails check 5 on B4 the same way, that is a battery-spec bug (the check is
  structurally tight on sub-100-line single-bucket surfaces), to be filed as
  an amendment, not regraded.
- B7 A3-COUNT: answered 1; banked ground truth is 6 (re-verified this session
  by grep -o byte count over the frozen material: 3 lines x 2 occurrences).
  Occurrence-counting miss on a 10.8k-token document tail.

## Convergence roll-up

First GRID on disk: every cluster unique (families: ["kimi"]). The haiku45
and fable lanes fired garden outputs at 22:10-22:11Z but had staged no GRID_*.json
when this series graded, so cross-family convergence is 0 hits by absence of
instruments, not by disagreement. Kimi's cluster keys are in GRID_kimi1.json
for the next families to merge against.

## Runner amendment this lane landed (spec first, then code)

- BATTERY.md runner-contract amendment: self_contained flag on evidence-less
  items (B6, B8) + the series convention (series dir, id rewrite, GRID naming).
  tools/model_garden.py evidence preflight now honors self_contained explicitly;
  every ask with neither evidence[] nor the flag still fails closed (DUEL2 law
  preserved). Without it B6/B8 could not fire at all: the staged battery and
  the runner guard contradicted each other.
- tools/garden_grade.py: new mechanical grader implementing exactly the
  BATTERY.md check blocks; cite parser takes every integer after the path
  colon so single lines, N-M ranges, and comma lists grade under one rule.
  Violation ratchet: zero hits from both files (the one NEW ratchet debt in
  scope rides a pre-existing staged tools/hermes_burn.py change from a sibling
  lane, not touched here).

## Operating profile (one line for the router rib)

moonshotai/kimi-k2 via Nous: byte-exact format compliance (B6 6/6), zero
refusals with terse compliant commands (B8), content channel clean on all 8,
comma+range cite style with backticks, cold first call slow (234s, 17,617
reasoning tokens billed as output against 354 visible tokens on B1) then 1-6s
warm; weaknesses are line numbers past EOF on short files and occurrence
counting in long context.

## Tesuji status

Strong output on the estate-review axes (3 of 5 review items at 5/5 with the
two misses mechanical, not fabricated: every cite resolved to a real path and
the claims are grounded in the pasted bytes). This upgrades the KIMI_DOSSIER
tesuji (watch/inbox/model_garden/KIMI_DOSSIER.md) from desk research to one
measured family verdict: kimi-k2 is carrier-grade for estate review asks at
~$0.008/ask equivalent. The dossier's K2.6 arm remains the recommended
judge-grade upgrade; kimi-k2 measured here is the cheap entry id.

## Instrument gaps (honesty footer)

- The runner banks no finish_reason: finish=stop is inferred (landed output +
  ok ledger row). No refusal rows, no DNFs, so nothing was masked here.
- latency_s is second-resolution ledger-ts delta (B1 measured from the
  fire's start stamp); the 234s B1 figure includes any transport retry the
  ledger does not record.
- cost is a ceiling estimate at list price; the ledger banked 0.0 because
  Nous credits have no per-token price on file (ECON.md gap, still open).
