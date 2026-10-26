# W3D — REPRINT (death as interagent hand-off)

- **Wave:** Mickey17 W3 (2026-09-29) · ledger return 11/24 improvement, agent W3 lane
- **Files:** `mag/game_campaign.py` (additive: `reprint()` + `_cli()` verb + `__main__` entry), `tests/test_reprint.py` (new)
- **Tests:** `pytest tests/test_reprint.py -q` → **6 passed** (2026-09-29, .venv). Regression: `tests/test_water_graph_campaign.py` + `tests/test_water_computer.py` → 16 passed.

## What landed

`reprint(dead_campaign_id)` in `mag/game_campaign.py` (placed before `seal_session`), CLI verb `python -m mag.game_campaign reprint <cid>` (exit 0 reprint / 2 refusal, JSON verdict on stdout):

1. **Guard** — only `status==defeated` reprints; live/paused/awaiting/already-reprinted are refused untouched (`refused: true`, no side effects).
2. **Salvage harvest** — flags split three ways: `temple:` / `slain:` / `door_open:` carried to the clone; `cheat:` / `nuke:` (+ exact `cheat` / `scorched`, matching `water_computer.cheated()/scorched()`) dropped and named in the knot; everything else (module-scoped, e.g. `water:phase`) folded into the knot text, never silently lost. Inventory rides the corpse's list.
3. **Actor re-seat** — player rebuilt from the CHAR_DIR sheet (the `set_character` persistence), corpse as fallback; hp restored to hp_max; sheet rewritten with new campaign_id + reprint_n.
4. **Counter** — new campaign `reprint_n = old + 1`, `reprint_of` lineage pointer; corpse flips to `status: reprinted` + `reprinted_to` (excluded from `latest_any`/`latest_for_session` live filters, so the clone becomes the live campaign).
5. **Per-module pass-off** — `_module_handler(module_id)` invoked with `atype="reprint"` + salvage payload (the water remembers); unknown atypes return `handled: False`, pass-off failure never kills the reprint.
6. **Verkle knot** — death folded via `rib_bus.publish_rib(domain="game_reprint", source="game_campaign.reprint")`, the same fold idiom `dungeon_dev.conquer` uses.
7. **Receipt rows** — the two live patterns, mirrored from `game_campaign.py:2957` (party_subchain + steer fallback) and `:2790` (training_events `game_turn`, T1, non-exportable).

## Test matrix (6)

- defeated campaign reprints: honest flags honored, `water:phase` folded-not-carried, inventory kept, CHAR_DIR sheet outranks corpse (hp 20/20 vs dead 12), corpse filed `reprinted`, 1 party_subchain + 1 training_events + 1 rib receipt
- cheat flags dropped: `cheat:bucket` + `nuke:fireball` stripped, named in the knot text
- counter increments: 0→1→2 across generations; sheet advances with the clone
- live campaign refused: untouched, zero receipts/knots/new files
- missing campaign refused
- CLI verb exit codes + JSON verdict

Isolation: CAMP_DIR/CHAR_DIR + all three receipt sinks monkeypatched per test (tmp_path); shared verkle chain / events file / rib store stay byte-still (conftest B2-336 law).

## Honest seams left open

- No `handle_game` wiring (the MCP/game-surface dispatcher) — verb is `python -m` only; wiring it is a one-line follow-up if the surface wants it.
- The water module's reprint pass-off currently no-ops (`handled: False`); a real water-salvage law (carried `water:phase`) belongs in `water_computer.py`, outside this lane's file ownership.
- Module-scoped flags are knotted, not carried — if a module wants them carried it should speak in the pass-off, not grow the engine's keep-list.
