# G4-4 — hum.html WIRING LANDED (the face now has nerves)

**TYPE:** wiring pass — G3-7's footer list executed where executable without admin.

**FILE TO:** dashboard/static/hum.html (updated; G3-7 static rows untouched — they are the floor)

## What got wired (4 rows touched)

| row | wiring | data source | status |
|---|---|---|---|
| EYES | live probe of the eye's `/api/tags` — renders model count + any vision-capable models | HOST ollama `127.0.0.1:11434` (`host.docker.internal:11434` when viewed in-cage; no eye container is BY DESIGN per watch/OLLAMA_EYE_TO_HOST_20260907.md) | LIVE probe, currently answering dark (see below) |
| EARS | dated repo sweep baked in: no `audio.cpp`/engine binary exists anywhere outside `.venv` (searched 09-11) | filesystem sweep, seat-side | PROBED — honest dark; stack is spec'd, not built |
| SPINE | direct fetch of `memory/biography/verkle_chain.jsonl` (3 candidate served paths), parses last knot: index / leaves / verkle_root / knot date. Falls back to the existing overseer.json chain_tip line with a stale-feed caveat. | chain file directly — independent of the stale overseer feed (frozen 09-07, still lists retired mag-openclaw) | LIVE when the server root reaches the repo; fallback otherwise. Verified truth at wiring time: knot index 7518, 7,519 leaves, root e7861efd… |
| HANDS | deliberately NOT page-wired — provider query needs the API key, and a key in a static page breaks the secrets law. Row now states this on-page plus the lane-truth pointer. | `mag/fuel_feed.py` + configs (cage env) | WIRED AS POLICY — cage-side by law, not dark by neglect |

BRAINSTEM + CONDUCTOR rows already wired by G3-7 via overseer.json — left as-is; the
existing staleness flag (>1h amber) now visibly applies, since the feed is 09-07-frozen.

## Probed and dark right now (the record)

- EYE: no answer from `127.0.0.1:11434` at seat probe 09-11 (ollama down from this
  surface, or the page hits CORS — ollama only reads cross-origin with `OLLAMA_ORIGINS`
  set). The probe stays wired; first successful answer turns the line green.
- Free lane: `ZAI_API_KEY` not on the seat shell (correct — env lives in the cage),
  so no live provider ping was possible from the seat either. Lane truth remains
  fuel_feed/configs until someone runs the probe in-cage.
- overseer.json: stale (ts 2026-09-07T06:16Z, pre-09-08-rebuild fleet list, chain tip
  d0a798c2/7,377 rows vs live 7,519). `python -m mag.overseer` refresh would fix the
  BRAINSTEM/CONDUCTOR lines — not run here (build-freeze-light; one command, no admin).

## What remains (footer updated to match)

All five footer items are BUILDS or GATES, not wirings — each now labeled as such:
1. eyes/ears → lane input format — BUILD (Lane 5)
2. hands contracts + verification gates — BUILD
3. conductor stop conditions + kill-one-agent — BUILD
4. flywheel valve — GATED on operator egress GO
5. effort budgets as first-class lane parameter — BUILD

From G3_7_hum.md NEXT STEP: kv_os.html remains the SPINE row's amber chip (Lane E gap
#2) — a build, out of this card's scope.
