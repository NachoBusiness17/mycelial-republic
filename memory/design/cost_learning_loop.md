# Cost/Learn Loop — marry provider telemetry to APIs → learning → routing (2026-08-09)

The operator asked: "marry this to their API's and interactions with them for their data
for a full learning analysis of it and all related surfaces." This doc maps the full loop,
what is BUILT, and the next steps.

## The loop (tesuji-everywhere: MEASURE → FOLD → APPLY)

```
 provider API call (grok / deepseek / codex-API / copilot-API / groq / gemini)
   │  models/providers.py  (the single chokepoint — every remote call routes here)
   ▼
 record_usage()  ── enriched row: ts, provider, model, key_idx, prompt, completion,
                    cache_hit/miss, ok, latency_ms, session_id   ← SEAM (BUILT)
   ▼
 logs/provider_usage.jsonl   (volume: prompt_tokens on ALL rows; split where API reports it)
   ▼
 mag/cache_map.py   ── per-provider/per-model + per-theme map, rates, billing_authoritative
   ▼
 mag/cost_learn.py  ── windowed analysis + daily leaf + skill_ledger decisions  ← FOLD (BUILT)
   ▼
 memory/improve/skill_ledger  (case law: "deepseek flash: 97% hit, $1.34/d, X ms")
   ▼
 router / model_pick / self_drive  (reads case law → cheaper routing)      ← APPLY
```

## Surfaces involved (the "all related surfaces")

| Surface | Role | Status |
|---|---|---|
| `models/providers.py` | provider seam — capture interaction data | ✅ cache split + latency + key_idx |
| `models/quota.record_usage` | telemetry write — every call | ✅ split + latency + session_id |
| `logs/provider_usage.jsonl` | raw interaction ledger | ✅ volume (prompt_tokens) + split |
| `mag/cache_map.py` | cost/cache map (all remote providers) | ✅ per-provider + per-theme + billing |
| `mag/ghost_ledger.py` | spend ledger + billing sync | ✅ sync from billing CSV (any provider) |
| `mag/cost_learn.py` | learning fold → leaf + skill_ledger | ✅ NEW, wired to autorun |
| `mag/governor_autorun.py` | cadence (`MAG_COST_LEARN_EVERY`) | ✅ NEW |
| `mag/skill_ledger.py` | case law the router reads | ⬜ consuming it (router already folds case law) |
| `mag/model_pick.py` / `self_drive.py` | routing that should consume cost case law | ⬜ follow-up |
| verkle knot / biography | session anchoring | partial (session_id now stamped, not yet joined) |
| Copilot chat / Codex CLI / Cursor | subscription/editor surfaces | ⬜ no per-call token API — fixed cost only |

## What is BUILT now
1. **Seam enrichment** — every provider API interaction now records cache hit/miss + latency +
   session_id (forward-compatible). This is the "marry to their APIs" foundation.
2. **`mag/cost_learn.py`** — deterministic windowed analysis (per-provider/model: calls, tokens,
   hit ratio, latency, priced cost) → daily leaf (`memory/improve/daily/cost-<date>.md`) + folds
   cost-learning decisions into the skill_ledger (`source=cost_learn`). Idempotent cadence.
3. **Cadence wired** — `MAG_COST_LEARN_EVERY` (default 600 ticks) folds automatically in the loop.
4. **`cache_map` generalized** to all remote providers; **`ghost_ledger.sync_deepseek_usage`** made
   provider-generic (ingest any provider's billing `amount-*.csv`).

## Next steps (ranked)

**P0 — close the data loop (make the analysis actually learn):**
- **Wire `session_id` threading**: `record_usage` accepts it; thread it from the agent turn /
  orchestrator spawn so rows join to verkle sessions exactly (kills the 83%-unmapped gap).
- **Consumer: route on cost case law**: make `model_pick` / `self_drive` read recent
  `cost_learn` skill_ledger decisions so the router prefers the cheapest-per-hit provider for
  exec-shaped work (currently the fold writes case law but nothing consumes it yet).

**P1 — richer interaction data:**
- Capture **goal/task_shape** at the seam (not just session_id) so cost is attributable to
  task type — enables "which task shape is expensive on which provider".
- Add **provider-key attribution** (Mag vs Overmind vs Swarm) to the row so per-key cost is visible.

**P2 — subscription/editor surfaces (Copilot chat, Codex CLI, Cursor):**
- No per-call token API exists; track as fixed/subscription cost in the map via `cost_rates`
  `fixed_per_call` + a manual/observed usage counter (e.g., approximate by editor activity),
  so they at least appear in the map rather than being invisible.

**P3 — fold into behavioral/training:**
- Emit the cost/cache leaf into the training pipeline (`pile_classify`/labeled rows) so the
  system's own economics become training signal, not just operational telemetry.

## Guardrails
- All new analysis is deterministic ($0, no LLM) — bytes, not vibes.
- The fold is idempotent and capped (≤6 skill_ledger rows) to avoid spamming case law.
- Never reads/prints secrets; keys stay in `.env` (Swarm now split to its own var).
