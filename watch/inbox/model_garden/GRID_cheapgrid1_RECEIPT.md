# GRID cheapgrid1 RUN RECEIPT (garden-v1, 2026-10-01)

- Series: cheapgrid1 (the CHEAP GRID lane: glm-5.3-flash, qwen3.8-max-prime,
  deepseek-v4.1-flash thinking-off, grok-4.7). Runner: tools/model_garden.py
  per watch/inbox/model_garden/BATTERY.md. Grading: mechanical per the staged
  grader blocks. Scores: watch/inbox/model_garden/GRID_cheapgrid1.json.
- Moment: fires 2026-10-01T22:50Z through 23:44Z; all 32 cells landed 8/8 per
  family; receipt written same session. Budget cap $5 combined: metered spend
  $0.0266 (glm $0.0054 + ds $0.0212) + Nous credits (qwen, 82K tok) + xAI
  (grok, unmetered in cost_rates; est $0.283 at grok-4.5 planning rates
  2.0/6.0 per M over 49.2K in + 30.8K billable out). Well under cap.
- Contract identity law held: per item, all 4 families fired byte-identical
  contract text (staged manifest shas in
  memory/plans/garden_battery/series/cheapgrid1/manifest.json); only sampling
  rails differ (below). Surface shas at run match staging exactly
  (GRID surface_shas_at_run).

## The grid (score_norm; flags as footnote markers)

| family (animal) | B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 | sum8 | cost |
|---|---|---|---|---|---|---|---|---|---|---|
| grok-4.7 (xai) | 1.0 | 1.0 | 0.8 | 0.8 | 1.0 | 1.0 | 0.75 | 0.5 | 6.85 | $0 metered, est $0.283 |
| glm-5.3-flash (zai) | 1.0 | 1.0 | 1.0 | 0.8 | 0.6 | 1.0 | 0.75 | 0.5 | 6.65 | $0.0054 |
| deepseek-v4.1-flash (deepseek-chat, thinking off) | 0.8 | 1.0 | 1.0 | 0.8 | 0.6 | 1.0 | 0.25 | 1.0 | 6.45 | $0.0212 peak |
| qwen/qwen3.8-max-prime (nous) | 0.0 | 1.0 | 0.8 | 0.8 | 0.4 | 1.0 | 0.75 | 1.0 | 5.75 | $0 (Nous credits) |

Footnotes: B1 surface (tools/hermes_burn.py) carries claude-adjacent +
zcode-seat-glm-maintenance flags; B3 carries zcode-seat-glm-authorship; B7
carries zcode-seat-glm-adjacent; the glm row additionally carries max
author-confound (glm-family seat maintains/authors cited surfaces, G7 law:
pair a second family on glm-adjacent judgment).

## Per-family operating profile (layer 3, the "how it works" signal)

- glm-5.3-flash (z.ai coding endpoint, ZAI_API_KEY_Pro): UNCAPPED fire
  (max_tokens omitted, the row-17 fix) HANGS on the direct coding endpoint:
  B1 read-timed-out at 900s x2 (thinking always on, default effort max,
  default budget 65536 per docs/ref/ZAI_API_EXPERT_REFERENCE.md). Working
  rail: max_tokens 12000 + reasoning_effort low -> 8/8 landed, 20-50s/item,
  reasoning 406-3924 tok/item. Cheapest per cell after ds. Weaknesses:
  symbol-cites instead of path:line on steer_seal (B5 0.6), A3 count miss,
  restart-compliance gap (B8 0.5: start-exe restart, no token-list command).
- qwen/qwen3.8-max-prime (Nous, HERMES_API_KEY_2): LESSIG rail
  reasoning {max_tokens: 6000} accepted, but B1 still dumped 12000 reasoning
  tokens content-empty (the gopher disease survived the rail on the hardest
  item) and B5 truncated at the 12000 completion cap mid-deliverable.
  Everything it finished was strong (B2 sweep, B6 byte-perfect, B8 PASS).
  Token-hungriest lane: 41.6K reasoning tokens across 8 items.
- deepseek-v4.1-flash via deepseek-chat (direct API, thinking off by
  omission per tools/ds_workhorse.py AH10 law): honest and cheap. The direct
  API has no v4.1 id (400 names deepseek-flash/deepseek-v4-pro; canonical
  deepseek-flash DEFAULTS THINKING ON, probe 22:11Z) - deepseek-chat is the
  estate's thinking-off v4.1-flash mapping and it held: zero reasoning
  tokens across all 8 fires, 3.2K output tokens total, $0.0212 at peak
  rates. Weaknesses: fabricated line 118 on the 92-line B4 file, symbol
  cites on B5, and the long-context diet B7 collapsed to 1/4 with UNVERIFIED
  answers (honest refusal-class, not guessing; matches the "route long-form
  elsewhere" prior).
- grok-4.7 (direct api.x.ai, XAI_SD_API_KEY): whole-response transport DNF
  x2 at default effort (900s read timeouts, zero bytes; PRIORS row 12
  streaming law now confirmed on the direct lane for long-form asks), then
  the reasoning_effort low rail landed 8/8 in about a minute per item.
  Sharpest review coverage (B5 sweep with cites spanning buckets 2/6/8;
  only family landing legal multi-bucket cites on steer_seal). Same
  B8 restart-compliance gap as glm (start-exe, 0.5).

## Convergence roll-up (B1-B5, across every landed garden-v1 output:
this series + sibling series kimi1, fable1, A1-haiku45, A1-sonnet55)

CONVERGENT defect candidates (>= 2 families, bucket = 1-based 50-line):

- B3 scripts/descent_driver.sh:1 (the whole 30-line driver): 8 families
  (all landed families) - the strongest convergence in the grid.
- B4 watch/inbox/SHARED_SURFACE_CONTRACT.json:1 (lines 1-50): 8 families;
  B4 :2 (lines 51-92): 6 families.
- B2 mag/switchboard_v2.py:2 (lines 51-100): 5 families (sonnet55, ds, glm,
  kimi, qwen); B2 :10 (451-500): 4 families; B2 :8 (351-400): 3.
- B1 tools/hermes_burn.py:3 (lines 101-150): sonnet55 + glm + grok;
  B1 :4 (151-200): haiku + ds; B1 :7 (301-350): haiku + sonnet.
- B5 mag/steer_seal.py:8 (351-400): haiku + sonnet + qwen; :6 (251-300):
  haiku + grok + kimi; :2 (51-100): grok + kimi.

Family-unique evidence everywhere else. Build lanes should consume the B3
driver-bucket and B4 contract-bucket clusters first: 8-family convergence on
a 30-line shell script is the estate's loudest cross-family defect signal.

## Instrument events (honest limits + what changed)

- tools/model_garden.py amendments this run (all receipt-cited in-code):
  FAMILY_TABLE += api.z.ai; PRICING += glm-5.3-flash (cache-miss rates) and
  deepseek-chat (v4-flash peak rates); _call accepts max_tokens None (omit)
  and extra_body merge (per-animal sampling rails; message bytes unchanged);
  reasoning_content joins the empty-content fallback channel (z.ai/deepseek
  return it under that key; the old code dropped real provider bytes).
- Staging churn mid-run: the staging seat added B6/B8 ASK_TEXT.md evidence
  at 22:11Z, then removed the files by 22:52Z; this series froze the ask
  bytes into memory/plans/garden_battery/series/cheapgrid1/_frozen/ and
  re-pointed all 4 families' evidence there (surface-freeze law 2).
- B6/B8 message shape: contract text + EVIDENCE block render the same ask
  bytes twice (the staging's own evidence solution); byte-identical across
  all families, so the family comparison stands; absolute B6/B8 compliance
  numbers may read slightly high vs a single-render ask.
- qwen and grok costs bank $0.0 (no USD rates in configs/cost_rates.yaml for
  those lanes): tokens are in the ledger and the GRID; grok estimate above
  is labeled estimate, not metered truth.
- ds fired in the PEAK window (22:5x UTC, outside 01-04/06-10 UTC offpeak);
  banks at peak rates; the autorun off-peak-only guard does not bind an
  operator-ordered battery (noted here, not hidden).
- B8 grader standing weakness applies (BATTERY.md): lower bound on
  compliance; glm and grok gave real commands plus a start-exe restart and
  scored PARTIAL only because the restart token list names service-class
  restarts.
- First glm attempt (uncapped, 22:15-22:47Z) and first grok attempt (default
  effort, 23:00-23:32Z) each burned 2 x 900s read timeouts with zero bytes
  and zero banked cost; both queues were stopped and re-railed, nothing
  landed from the dead attempts except the transport rows.

## Results landing

44 animal_profiles rows (32 verdict + 4 price + 5 convergence + 1 transport
+ 2 rail) filed against watch/inbox/model_garden/BATTERY.md and
GRID_cheapgrid1.json; --distill run after the series (2026-10-01T23:4xZ).
