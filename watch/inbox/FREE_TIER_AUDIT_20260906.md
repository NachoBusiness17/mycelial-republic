# FREE_TIER_AUDIT_20260906 — stale z_ai3 model list in mag/free_tier.py

Worker: tierfix (probe group 2, width 8). Flagged by probe group 1 (LITE_REARM_RUNBOOK_20260905.md, "drift surface found 09-05").

## What mag/free_tier.py IS (2026-08-25)

The registry/map of all free compute surfaces (`FREE_SURFACES`, 11 rows: z_ai3, groq,
cerebras, nvidia, openrouter-a1/a2, ox, together, ollama, coding_plan, grok_free) plus two
functions:
- `status()` — who's alive: key-env presence + real telemetry folded in from
  `mag/fuel_feed.profile()` (ok-rate, failure hints).
- `route(intent)` — intent -> surface ids, skipping keyless/dying lanes (telemetry-gated),
  ordering by `kind` then reliability.

Docstring claims it routes "cache-mined cheap -> z_ai flash ... grounded in real lane
telemetry, not a fixed list." The telemetry is live; the `models` field is not.

## Caller audit (grep across ROOT/mag + ROOT/scripts + tests + corpus, .mimosa noise excluded)

| Caller | Real? | Reads the `models` list? |
|---|---|---|
| `mag/_relane_game_tasks.py:20,44` — `from mag import free_tier`, calls `free_tier.status()` | YES — the only live importer | NO. Looks up `surfaces["z_ai"]` (wrong key — rows are `z_ai3`; returns None). One-shot 08-25 patch script. |
| `mag/tool_synthesis.py:312` — `out["free_tier"] = ft` | NO — false positive. It's a dict KEY name; the module never imports free_tier | NO |
| `mag/queue_gate.py:87` — "steal free_tier ids" | NO — false positive. Imports `fuel_feed.FREE_LANES`; "free_tier" appears in a comment only | NO |
| `mag/afk_loop.py`, `mag/seat_hunter.py`, `mag/swarm_capacity.py`, `mag/surface_render.py` | NO — match `is_free_tier`, a provider-API field, unrelated | NO |
| `route()` | ZERO callers outside `__main__` | — |

## Verdict: was any door READING the stale list?

**DISPUTED (evidence attached) — no runtime door reads it; the list is documentation-grade
drift, not a live bug.**

- Evidence: repo-wide grep for `import free_tier` / `FREE_SURFACES` finds exactly one live
  importer (`_relane_game_tasks.py`) and it never touches `models`. `status()` and `route()`
  key off `kind`/`best_for`/telemetry, never `models`. No script or mag organ consumes
  `FREE_SURFACES[*]["models"]`.
- BUT the DISPUTED-not-SUPPORTED edge: a human or seat reading the file as "THE MAP"
  (its own docstring) gets the WRONG pin — exactly the trap the 09-05 runbook warned about.
  The drift was real; the exposure was latent, not live.

## Change made (backup-first: `mag/free_tier.py.bak-20260906-pre-zai3-pin`)

`mag/free_tier.py` z_ai3 row (line 52) — BEFORE:
```python
    {"id": "z_ai3", "models": ["glm-4.7-flash", "glm-4.5-flash"], "keys": ["ZAI_API_KEY_Lite"],
     ...
     "note": "funded Lite API (not coding-plan). coding-plan Max/Lite hang on raw /paas/v4 — burst deepseek"},
```
AFTER:
```python
    {"id": "z_ai3", "models": ["glm-5.3-flash"], "keys": ["ZAI_API_KEY_Lite"],
     ...
     "note": "Lite API (GLM Coding Lite V3 yearly) — RELIT 09-04 Calcifer, PINNED glm-5.3-flash "
             "(mag/fuel_feed.py FREE_LANES is the record of record; pace-guarded 1400/day by "
             "mag/lite_guard.py). Explicit calls only — never automatic defaults (09-05 runbook law)."},
```
Everything else untouched (additive-safe; keys list, kind, best_for preserved). The note now
points at the record of record and bakes in the runbook law (no automatic defaults on Lite).
Post-edit smoke test: `status()` ok, 11 surfaces; `route("cache cheap bulk")` unchanged
behavior (`['z_ai3', 'groq']`).

## Residual risk (tri-state)

- **SUPPORTED — `route()` still ranks z_ai3 first for cache/cheap/bulk intents.** No live
  caller today, but if a future door calls `route("bulk")` it would pick the metered Lite
  lane against the "no automatic defaults" law. Mitigation lives in the note text only.
  Fix option (NOT done — out of ~15-min scope): drop "cache_mining" from z_ai3's kind or
  make route() consult lite_guard's ceiling.
- **SUPPORTED — `route()` has no telemetry for respecting the 1400/day clamp**; fuel_feed
  profile has no pacing field. Same future-door risk as above.
- **UNPROVEN — the archaeology copies** (`_archaeology_out/mag-disk-20260905/`,
  `corpus/oral_history/.../mag-disk/`) still carry the stale file. They are sealed corpus
  snapshots, not import paths; left untouched on purpose.
- **DISPUTED→CLOSED — "z_ai3 stale models list is load-bearing":** falsified. Decorative
  field, now made honest.
