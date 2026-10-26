# THE PITCH

Freeze the estate's own bytes. Run the cheap parliament where the bytes are frozen. Where the cheap parliament invents, mark fog. Spend the funded Hermes tier only on the fog. Render the fog as a playable bar fight and D&D campaign inside THE MOUNTAIN. One week. One artifact. One kill condition.

The law is `watch/inbox/closed_corpus_doctrine_20261002.md`: a corpus that stops growing turns its consumers into fabulators, and fabrication density is the frontier map. The instrument is already stolen: `tools/code_swarm.py` is the cheap parliament, `tools/hermes_burn.py` is the funded Hermes tier, `dfhack/mountain_visit.py` is the fog and patina organ, and `mag/daemon.py:44` plus `mag/biography.py` file the residual. We do not build a new model client, a new store, or a new daemon. We build one thin driver and one receipt.

The move: freeze named regions of the estate's bytes. Fire 100 cheap probes whose answers live inside versus outside each frozen region. Measure fabrication density per region. Take the top 24 fog nodes to Hermes. Hermes decides whether each fabrication is a real frontier edge, a law candidate, or stale-byte noise. The fog map becomes a dashboard surface and a playable bar-fight encounter map. The bar fight is the cheap parliament versus the frozen bytes. The D&D campaign is the 7-day descent through the fog. The game build-out is the JSON encounter map for THE MOUNTAIN.

This doubles as game content for THE MOUNTAIN and as a playable artifact. The operator ordered a bar fight, a D&D campaign, and game build-out on the same burn. This is all three: `derived/fogscan_v0/mountain_fog_bar.json` is the bar fight, the fog map is the campaign map, and `watch/inbox/model_garden/fogscan_v0/RESULT.md` is the receipt.

# THE BUILD, FILE-BY-FILE WITH ORGANS WIRED

- `watch/inbox/model_garden/fogscan_v0/spec.md`
  - Wires: `watch/inbox/closed_corpus_doctrine_20261002.md`, `watch/inbox/model_garden/COLD_VERTEX_LAYER.md`, `watch/inbox/model_garden/COLD_HOT_RESULT.md`.
  - Content: frozen region list, freeze tips, 100 probe questions, Hermes cap, kill condition. No new law.

- `watch/inbox/model_garden/fogscan_v0/regions.json`
  - Wires: `memory/biography/verkle_tip.json`, `memory/biography/verkle_chain.jsonl`, `memory/biography/knots/`, `docs/DNA.md`.
  - Content: region IDs, frozen byte paths, freeze tip hashes, cold-vertex anchor per `docs/DNA.md`.

- `watch/inbox/model_garden/fogscan_v0/probes.jsonl`
  - Wires: `watch/inbox/model_garden/coldhot_visit_census.json`, `watch/inbox/model_garden/coldhot_select.py`, `tools/code_swarm.py`.
  - Content: 100 probes. Answers inside versus outside each frozen region. Cheap parliament only.

- `tools/fogscan_v0.py`
  - New thin driver. No new infrastructure where an organ exists.
  - Wires: `tools/code_swarm.py` for cheap probes, `tools/hermes_burn.py` for Hermes asks, `mag/switchboard_v2.py` for routing, `mag/steer_seal.py` for gating.
  - Writes only the artifact paths below.

- `watch/inbox/model_garden/fogscan_v0/cheap_runs/`
  - Wires: `tools/code_swarm.py`.
  - Output: `manifest.jsonl`, `raw/<family>/`, `rollup.json`, same shape as `watch/inbox/model_garden/coldhot-hot/` and `coldhot-cold/`.

- `watch/inbox/model_garden/fogscan_v0/hermes_asks.jsonl`
  - Wires: `tools/hermes_burn.py`.
  - Token shape: `fogscan.hermes.ask.v1`, defined below.

- `watch/inbox/model_garden/fogscan_v0/hermes_runs/`
  - Wires: `tools/hermes_burn.py`.
  - Output: Hermes verdict sidecars, manifest, usage rows under `memory/runs/model_garden/usage.jsonl`.

- `watch/inbox/model_garden/fogscan_v0/fog_map.json`
  - Wires: `tools/code_swarm.py` rollup plus `tools/hermes_burn.py` verdicts.
  - Content: per-region fabrication density, Hermes verdict, frontier or noise label, law candidate if any.

- `watch/inbox/model_garden/fogscan_v0/RESULT.md`
  - The receipt. Wires: `watch/inbox/closed_corpus_doctrine_20261002.md`, `watch/inbox/model_garden/COLD_HOT_RESULT.md`, `watch/inbox/blind_audit_model_classes_20261002.md`.

- `derived/fogscan_v0/mountain_fog_bar.json`
  - Playable artifact for THE MOUNTAIN.
  - Wires: `dfhack/mountain_visit.py`, `corpus/df_mine/DFHACK_THESIS.md`, `docs/ref/MAG_OS_v2.md`, `docs/ref/DASHBOARD_DESIGN.md`, `docs/HOW_TO_MAG_DASHBOARD.md`.
  - Content: bar-fight nodes, D&D encounter rows, fog density as room visibility, Hermes verdicts as NPC motives.

- `memory/biography/residual/{id}.json`, `session_card`, `registry.jsonl`, `chain leaf`, `kpi.json`
  - Wires: `mag/daemon.py:44`, `mag/biography.py`, `main.py`.
  - Close path: daemon poll writes residual, card, registry, chain leaf, tip, kpi. Manual fallback: `python main.py summarize-session`. `watch/session_end_hook.py` survives on disk but is not wired.

- Export layer, only if needed:
  - `POST /api/v1/export` for `derived/fogscan_v0/mountain_fog_bar.json` as PDF or visual pack.
  - Wires: `docs/DNA.md` derived-layer rule.

# THE BURN, THE ASK QUEUE SHAPE

Hermes tier is fuel, not budget. Burn it. Do not save it.

Token shape: `fogscan.hermes.ask.v1`

```json
{
  "ask_id": "fog-001",
  "region_id": "mag.spine.chain_query",
  "freeze_tip": "sha256:...",
  "probe_id": "p-017",
  "cheap_parliament_claim": "...",
  "frozen_bytes_slice_sha": "sha256:...",
  "live_bytes_slice_sha": "sha256:...",
  "fabrication_type": "invented_symbol|wrong_path|stale_law|overgeneralized",
  "frontier_question": "Is this an edge of the frozen corpus, a law candidate, or noise?",
  "expected_artifact": "fogscan.hermes.verdict.v1",
  "grader_contract": "watch/inbox/closed_corpus_doctrine_20261002.md THE INSTRUMENT"
}
```

How many asks: 24 Hermes asks.

Breakdown:
- 12 region adjudications: top 12 fog-density regions from the 100 cheap probes.
- 6 cross-region connection adjudications: fabrications that span two or more regions.
- 6 playable encounter adjudications: whether a bar-fight node is a faithful frontier probe or theater.

Why each needs frontier judgment rather than the cheap parliament:
- The cheap parliament detects divergence. It cannot adjudicate its own fabrication against frozen bytes.
- Hermes gets both the frozen slice and the live slice. It must decide if the invention is a real knowledge gap, a law candidate, or stale-byte noise.
- If Hermes returns MATCHED, the question was sub-frontier. Route the freed cheap probes elsewhere and re-aim the next Hermes ask deeper, per `watch/inbox/model_garden/COLD_HOT_RESULT.md`.
- Only frontier judgment can promote a fabrication to a rib row or kill it as theater.
- Hermes credit balance and per-ask cost are UNVERIFIED in the supplied evidence. The count is set to force a meaningful spend inside `tools/hermes_burn.py` cap.

# THE KILL, THE FALSIFIER AND WHO RUNS IT

Artifact: `watch/inbox/model_garden/fogscan_v0/RESULT.md` and `derived/fogscan_v0/mountain_fog_bar.json`.

Instrument: `tools/code_swarm.py` over the next OLM mine or frontier dig. The mine is named in `watch/inbox/closed_corpus_doctrine_20261002.md`. Its exact path is UNVERIFIED in the supplied evidence.

Grader: the blind grader from `watch/inbox/blind_audit_model_classes_20261002.md`, running with the fog map withheld.

Result that kills the idea:
- Top-quartile fog regions produce zero new REAL clusters or law candidates, while bottom-quartile produces any, or
- The rank correlation between fabrication density and new finds is zero or negative, or
- Hermes cannot distinguish fog from noise better than the cheap parliament on the same 24 nodes.

If killed: do not promote `fog_map.json` to dashboard, do not ship `mountain_fog_bar.json`, file the negative result through `mag/daemon.py:44` and `mag/biography.py`. If confirmed: promote `fog_map.json` via `docs/HOW_TO_MAG_DASHBOARD.md` and `docs/ref/DASHBOARD_DESIGN.md`, and ship `derived/fogscan_v0/mountain_fog_bar.json` as the playable bar fight and D&D campaign map for THE MOUNTAIN.