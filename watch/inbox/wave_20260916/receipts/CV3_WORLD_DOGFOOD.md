# CV3_WORLD_DOGFOOD — receipt (wave 20260916)

**Lane:** CV3 — make the fleet USE its own world (`mag/wow_world.py` atrium-ring chain: 12 green tests, zero real sessions carried world/room).
**Mission:** walk the world with a named traveler, resolve the boss through the kernels, write both durable receipts (player ledger + `wow_session.v1`), prove byte-identity across two same-seed runs, dogfood the deck, then run the wow-family tests.

## Log (append as I go)

- [2026-09-16] Receipt opened FIRST per wave-lane law.
- [2026-09-16] Interfaces read: `mag/wow_world.py` (WorldSession = BonesSession + room pointer + `go` gated by the room's exit table; receipt = wow_session.v1 with route/world binding; TURN_LIMIT 8, DRAW_TARGET 3), `mag/wow_bones_session.py` (kernels: Dispatch/Instance/Stream; AUTHED→LOGGEDIN promotion draws nothing), `mag/wow_player.py` (ledger, not a row: create/apply, hash-chained rows, no timestamps, resume-from-ledger).
- [2026-09-16] Orphan confirmed with eyes: only two receipts exist in `memory/runs/wow_world/receipts/` — seed `replay-check` (COMPLETE, 7 moves, pytest determinism residue) and seed `t-cli` (OPEN, 1 move, CLI test residue). Zero character-attached sessions. `memory/runs/wow_player/` does not exist at all.
- [2026-09-16] Route decided (8 turns = exactly TURN_LIMIT): look (promote) → go north (atrium→torch_hall) → **go west (the locked ash_gallery door — typed STATUS_NEVER refusal, room unchanged)** → go east (→vault) → look (load: TO_BE_DECIDED→IN_PROGRESS) → look ×3 (one draw each; guarded boss DONE on draw 3). Expected route ledger: atrium→torch_hall→vault, verdict COMPLETE. Bonus law exercised: the world refuses a locked door in a real session and still completes.
- [2026-09-16] Player design: traveler `lantern-01`, seed = `lantern-01` (character↔session binding is structural). On COMPLETE the walker grants one sigil item (`sigil-atrium-ring`) as ledger row 4. Replay law: walker re-derives the target ledger with wow_player's own pure reducers (`_new_row`/`_replay`/`verify_file`); existing file equal → no-op replay; divergent → typed LEDGER_CONFLICT (a ledger is history, never rewritten).
- [2026-09-16] **Walk run 1: FAILED, refused by its own falsifier** — `WALKER_BUG: public create/apply path diverged from target bytes`. Root cause: walker seeded ledger genesis from the *replayed final view* (room=vault) instead of row 1 (room=atrium) — it tried to create the character standing in the vault. The void player file written by the failed run was discarded (never consumed history; a failed settlement is void). Walker fixed: genesis reads `ledger[0]["data"]`. The incident stays in this receipt.
- [2026-09-16] **Walk run 1 (clean): COMPLETE.** Session `wworld-e924e95aadcd` (seed `lantern-01`, world `atrium-ring`, world_sha256_12 `44451fe6d884`): 8 turns (= TURN_LIMIT exactly), 3 draws, **1 typed refusal** (the locked `GO_WEST@ROOM:torch_hall` door — STATUS_NEVER, handler_ran false, room unchanged), route `atrium -> torch_hall -> vault`, boss 0 DONE, verdict COMPLETE. Traveler `lantern-01` (`ply-da9cfc91a7d7`): 4 ledger rows (create@atrium, move×2, grant `sigil-atrium-ring`), ends in vault carrying the sigil.
- [2026-09-16] **Walk run 2 (same seed): BYTE-IDENTICAL, the replay law holds with a character attached.** `player_replayed: true` — the walker resumed from ledger instead of appending duplicate rows. sha256 of all three durable files identical across runs: player `638b18791e2ac90125466e2e071046affe3d39947bee934777a52246bb7a7b57` · receipt `f9c97c51213529b72bec13bfba862c7d3513f0f8475f3ac83fad18503d994013` · session `12256487b64375a9a2af985fb434c4912163d109bcbaeb4ac69693baa13d855a`.
- [2026-09-16] **Dogfood: the deck now shows the world's first walked route.** `scripts/build_deck.py` patched (`mine_world()` mines `memory/runs/wow_world/receipts` + `memory/runs/wow_player`; a "walk" counts only when the session's seed names a real player ledger, so pytest residue can never pose as one; new `world` block in the embedded deck data + facts on the WORLD BUILD card). `dashboard/static/deck.html` regenerated (33,910 bytes) and now renders: `FIRST WALK: atrium -> torch_hall -> vault · seed lantern-01 · 8 moves · verdict COMPLETE · wworld-e924e95aadcd · receipt sha256:5b4592c8fbc7…` and `traveler lantern-01 (ply-da9cfc91a7d7) at vault · ledger 4 rows · inventory 1`. (Deck build telemetry printed the pre-existing grounding chain break at row 122 — known owed repair, not this lane's.)
- [2026-09-16] **Wow-family pytest after the walk: 64 passed, 0 failed, 0 skipped, 2.38s** (tests/test_wow_* — bones, bones_session, world, player, manifest, family). Trust bytes: this is the run's own count, not a hand-written one.

---

## Route taken

`atrium` → *(look: AUTHED→LOGGEDIN, promotion draws nothing)* → `torch_hall` (go north) → **refused: `go west` → STATUS_NEVER, handler_ran false — the locked ash_gallery door, typed, room unchanged** → `vault` (go east) → *(look: the load, TO_BE_DECIDED→IN_PROGRESS)* → look ×3 (draws 1–3; guarded boss DONE on draw 3). 8 turns = TURN_LIMIT exactly. Verdict **COMPLETE**, encounter DONE, draw_index 3, refusals 1.

## Artifacts + hashes (sha256, verified identical across both runs)

| File | Path | sha256 |
|---|---|---|
| world receipt (wow_session.v1) | `memory/runs/wow_world/receipts/wworld-e924e95aadcd.json` | `f9c97c51213529b72bec13bfba862c7d3513f0f8475f3ac83fad18503d994013` |
| session ledger (wow_world_session.v1) | `memory/runs/wow_world/sessions/wworld-e924e95aadcd.json` | `12256487b64375a9a2af985fb434c4912163d109bcbaeb4ac69693baa13d855a` |
| player ledger (wow_player.v1) | `memory/runs/wow_player/ply-da9cfc91a7d7.json` | `638b18791e2ac90125466e2e071046affe3d39947bee934777a52246bb7a7b57` |

Receipt self-hash inside the wow_session.v1 body: `5b4592c8fbc7308b5fd566aa788413a64003ccb8af1cc00e458c929bb1180ba6`. World binding: `atrium-ring` @ world_sha256_12 `44451fe6d884`, bones_digest `efeb905b4d17`.

## Byte-identity proof (the replay law, now with a character attached)

Run 1 (clean create) and run 2 (same seed `lantern-01`) produced **identical sha256 on all three durable files** (table above is run 2's `sha256sum` output). Run 2 reported `player_replayed: true` — the walker resumed from ledger instead of appending duplicate rows (still 4 rows), because the walker re-derives the target ledger with wow_player's own pure reducers (`_new_row`/`_replay`/`verify_file`) and no-ops on byte-equality, refusing `LEDGER_CONFLICT` if history ever diverges. A third safety held on run 1: the walker's own falsifier refused a buggy genesis (character created in the vault) before it could pass — see incident above.

## What the world needs next to be worth a second walk

1. **A boss that isn't a slot machine.** DONE lands deterministically on draw 3 — no decision, no risk, no FAIL/SPECIAL paths (Instance supports them; the world never asks). Encounters where draws carry consequences.
2. **Stamina that binds.** The player ledger has `stamina_max` and a `stamina` event, but nothing in the world ever decrements it — movement is free, so route choice is not a choice. Price doors in stamina.
3. **A key for the locked door.** `ash_gallery` sits behind STATUS_NEVER forever; `spend_item` exists in the ledger but no gate row can consume a key. Locks should be puzzles, not walls.
4. **More ring.** 5 rooms, 1 reachable dead end (unreachable, in fact), 1 encounter. Instance holds more bosses than boss 0; the world lists only `[0]` in one room.
5. **Native login.** Traveler↔session binding is currently the walker's convention (seed == character name); the wow_session.v1 schema can't carry a player_id. M2.5+ should let WorldSession take a player file so *any* surface, not this walker, can carry the character in.
6. **An inventory that matters.** The sigil is carried but no verb reads items yet — a second walk needs a reason to want the first walk's loot.

**Status: DONE** — the orphan has its first real session: a named traveler walked the atrium-ring, knocked on a locked door, resolved the boss through the kernels, banked a sigil in an append-only ledger, and the deck displays the route. Two runs, same seed, same bytes.
