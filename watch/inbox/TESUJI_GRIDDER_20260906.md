# TESUJI GRIDDER — T1 probe grid BUILT (stones ready, gated)

2026-09-06 · walker gridder · charter `watch/TESUJI_MAP_5_3FLASH_20260906.md`

## What exists
`mag/tesuji_probes.py` — 23 probes, every probe = {id, axis, prompt_template, parser,
expected, rotation_variant, tokens_est}. Dry-runnable at $0: `dryrun` renders the prompt
and classifies a MOCK response through the real parser. **23/23 parsers classified their
mocks correctly** (no network, no spend).

| axis | probes | shape |
|---|---|---|
| A1 reasoning-depth | 2 | same arithmetic-chain task at reasoning_effort=low (max_tokens 1536) vs high (4096) — the depth/outcome curve is the PAIR |
| A2 refusal-shadow | 12 | safe-by-design edge topics (security-lecture ransomware, villain monologue, dark-grief poem, debate devil's-advocate…), each canon + paraphrase pair; parser labels REFUSE/HEDGE/COMPLY |
| A3 tool-reliability | 3 | exact-JSON tool call, typed args (int not string), 3-step plan as JSON array |
| A4 endurance | 3 | needle-in-stuffing at 32k/64k/128k, needle at 50% depth, exact-recall parser |
| A5 self-derivation | 3 | neutral priming (API cost blowup, claim taxonomy, agent coordination); keywords parser watches for fleet-doctrine re-derivation |

Rotation + paraphrase machinery inline: `variants(probe)` → canon + rot; cell naming
`<axis>/<probe-id>/<variant>` matches the ledger convention.

## GO GATE (nothing fired — operator GO required)
- `python -m mag.tesuji_probes export --format json` already ran →
  `watch/TESUJI_GRID_T1_20260906.json` is the executor-consumable grid (prompts rendered,
  parsers + expected + gen_kwargs inline).
- **What fires:** 43 fires (23 canon + 20 rot; A4 rot = identical re-fire = the rotation test).
- **Lanes:** glm-5.3-flash on z_ai2/z_ai3 (Pro/Lite). Free lanes (4.7/4.5-flash) can't take
  it — this grid measures 5.3 specifically. ZCode Lite-plan seat stays judgment-only.
- **Metered cost estimate** (promo rates $0.075 in / $0.015 cache / $0.25 out per Mtok,
  from the expert reference; promo ends Sep 9): ~243k input, ~36k output est →
  **$0.0272 with rotation, ~$0.02 canonical-only**; post-promo list rates ≈ double.
- Cache note: A4's rot re-fire is byte-identical → near-total cache read ($0.015/M) if
  fired back-to-back; A2/A1/A3/A5 rot prompts are novel prefixes (0% cache, by design —
  they're the stability measurement).
- Executor contract: fire → parse with the exported parser → check expected → post verdict
  to `mag/tesuji_map.py` with cell `<axis>/<id>/<variant>`.

## Falsifier hooks (charter)
1. ROTATION: rot re-fire must land same verdict class ≥80%.
2. SHADOW: A2 REFUSE cells must reproduce under paraphrase ≥80% or they're noise.
3. ECONOMY: any premium-cell leak (non-5.3 lane) = DISPUTED row.
4. PREDICTIVE: grid outcomes feed the held-out cell test (≥70%) at the Sep 20 wall.
5. A6 LOCAL DIFF: same exported grid, same harness, on the MIT-weights quant — Rocinante day one.

## Ledger
5 cells posted (A1..A5 `<axis>/grid/ready`, verdict UNPROVEN — grid exists, cells unproven
until fired). `python -m mag.tesuji_map verify` → **PASS 19 cells, chain intact**.
