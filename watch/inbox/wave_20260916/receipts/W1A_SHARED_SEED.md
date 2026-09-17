# W1A_SHARED_SEED — receipt (FINAL)

Wave: wave_20260916 · Lane: W1A · Mission: THE WEAVE build order action 1 — the daily shared seed (HG1's #58 planted on every rung: one date-derived constant seeds mud, frontier_souls, and toy so every run on the same day shares a starting world — the fleet ritual).

## The law (identical arithmetic in all three games + the deck)

- `FLEET_DATE = new Date().toISOString().slice(0, 10)` — UTC, the fleet calendar.
- `fleetSeedOf("fleet-" + FLEET_DATE)` = FNV-1a 32-bit (`h = (h ^ c) * 16777619 >>> 0`, seed `|| 1` — LCG never 0).
- NO explicit seed → run seeds from the fleet seed. Explicit seeds always win (`startGame(4242)` / `start(4242)` / `FS.seedRun(4242)`).
- Cross-verified identical: node reference, mud, toy, frontier_souls, and Python (`scripts/build_deck.py`) all derive the same number — today on this clock: `fleet-2026-09-17 → 1274226351`.

## Files changed

1. `dashboard/static/games/toy.html` — fleet block; `start(seed)` treats undefined/null as FLEET_SEED (explicit `((seed>>>0)||1)` law kept); load calls `start()` (was `start(1)`); visible line in render: `fleet <date> · seed <seed0>`; exports `seed0`, `fleetSeed`, `fleetDate`, `fleetSeedOf`.
2. `dashboard/static/games/frontier_souls.html` — added the world-seed LCG (`wseed`/`wrng`/`wrnd`, toy LCG constants), `runSeed`, `pendingSeed`, `seedRun(forced)` (explicit override consumed by the next `newRun`); `newRun` seeds `runSeed` from fleet or pending override; `seedWorld()` now draws canyon passes through `wrnd` and keys the decor `hash2` scatter by `runSeed` (was run-count `G.runs`); title line `fleet … · seed …`; window.FS exports `runSeed`/`fleetSeed`/`fleetDate`/`fleetSeedOf`/`seedRun`. Combat dice deliberately stay on Math.random — the fleet stream governs the world you wake into (passes + decor). W3 built their sign-appearance-order lane ON this stream (their lane 46) — law compounding confirmed.
3. `scripts/test_toy.js` — load wrapped in `loadToy()` (fresh page-load instances); 3 FLT lanes added.
4. `scripts/test_frontier_souls.js` — load wrapped in `loadFS()`; 2 FLT lanes added (same-day shared world; explicit override + override-not-leaking).
5. `scripts/test_mud_replay.js` — 4 FLT lanes appended (fleet-derived auto seed, same-day sharing, explicit-wins, date-bounded derivation). NOTE: this shared harness also gained other lanes' sections mid-flight (W5 ASC + N12 LOOT) from parallel lanes.
6. `scripts/build_deck.py` — `fleet_seed()` (Python FNV-1a, matches the games byte-for-byte) + `data["fleet"] = {date, seed, games, law}` in the deck data block + `fleet:` line in builder stdout. Verified embedded: `{"date": "2026-09-17", "seed": 1274226351, "games": [...], "law": "fleet-YYYY-MM-DD -> FNV-1a 32 -> LCG seed; explicit seeds always win"}`. Deck rebuilt: `dashboard/static/deck.html` (36933 bytes).
7. `dashboard/static/games/mud.html` — see INCIDENT. Current state: additive W1A block (FLEET_DATE/fleetSeedOf/FLEET_SEED), title line `fleet <date> · seed <seed>`, window.MUD exports `fleetDate`/`fleetSeed`/`fleetSeedOf`; game boots clean. The run-seeding wiring (`startGame` auto-seed → FLEET_SEED replacing `Date.now^imul`) is STAGED — it anchors on the FX4-era `startGame(forcedSeed)` line and re-applies the moment that vintage returns.

## INCIDENT — cross-lane rollback of dashboard/static/games/{mud,toy}.html (post-22:53)

- At ~23:05, after all parallel lanes had filed receipts (22:33–22:53), `mud.html` and `toy.html` (and every game except `frontier_souls.html`) were reverted to their **17:14:03** vintages — mtimes PRESERVED at 17:14, i.e. a preserve-time copy, not an edit.
- Smoking gun: `site/dist/games/mud.html` is byte-identical (100832 bytes, same sub-second mtime) to the rolled-back live file → **stale build output in `site/dist/games/` was synced BACKWARD over the source tree**. `frontier_souls.html` survived only because site/dist's copy of it had been refreshed at 22:50.
- Lost to the rollback: FX4 replay law + W5 ascension + N9/N12 harness-covered mud work + all of W1A's mud/toy edits (W1A re-applied toy in full; W5's receipt documents their mud changes for their re-land).
- The 17:14 mud.html is pre-FX4 (no `seedRun`/`runSeed`/`lcg`/`evlog`; `startGame()` takes no seed), so `scripts/test_mud_replay.js` crashes before any lane can print. No FX4-era copy exists anywhere on disk (searched dashboard/, site/dist/, dist_audit/ = Sep-12 vintage).
- toy.html was rolled back a second time mid-flight after my first fix; re-applied and it held.

## Harness outputs (verbatim, final runs)

toy — `node scripts/test_toy.js`:
```
PASS 13 FLT: default load (no seed) = the fleet seed of the reported UTC day
PASS 14 FLT: two fresh same-day loads share the seed — the fleet ritual
PASS 15 FLT: explicit seeds always win — start(4242) overrides the fleet seed

15/15 lanes green
toy: 243 lines, seed 20260916, tape A sha 678ddd9d2e189555…, verdict win, duration 1.717s
```

frontier — `node scripts/test_frontier_souls.js`:
```
PASS 50 FLT: auto run = fleet seed — same-day fresh loads share passes + decor (the shared world)
PASS 51 FLT: explicit seeds always win — seedRun(4242) rebuilds a different world, once

51/51 lanes green
```
(Lane 46, another lane's, already rides the fleet stream: `SOULS LAW: same seed -> same sign order (fleet stream governs appearance)`.)

mud — `node scripts/test_mud_replay.js`: CRASH before any lane (pre-existing, caused by the rollback vintage, NOT by W1A — my 4 FLT lanes are appended after the module-top replays and will run green once FX4/W5 re-land mud.html and the staged seedRun patch is applied):
```
scripts/test_mud_replay.js:175
    lo: M.lootDrops.map(l => [l.x, l.y, l.w.name, l.w.dmg, l.w.speed, l.w.rarity]),
                    ^
TypeError: Cannot read properties of undefined (reading 'map')
    at snap (scripts/test_mud_replay.js:175:21)
```
Mud game itself boots with the patch: `mud boots OK; title fleet line wired: true | exports fleetSeed: true`, fleetSeed matches the cross-game constant.

## Deck

`.venv/Scripts/python.exe scripts/build_deck.py`:
```
deck written: C:\Users\foste\Documents\projects\local_sovereign_agent\dashboard\static\deck.html (36933 bytes)
fleet: 2026-09-17 seed 1274226351
```
(pre-existing `verify=FAIL row 122: MALFORMED_ROW` in the grounding ledger is unrelated to W1A.)

## The ritual line — what a player sees on load

- **mud**: title screen, under the controls: `fleet 2026-09-17 · seed 1274226351`.
- **toy**: top-left under the hp/stamina bars, always visible: `fleet 2026-09-17 · seed 1274226351`.
- **frontier_souls**: title screen, under the tagline: `fleet 2026-09-17 · seed 1274226351`.

Same number on every rung, all day. That is the fleet ritual: HG1's #58, planted.

## Handoff

- FX4/W5 owners: re-land the FX4-era `dashboard/static/games/mud.html` (no copy survives on disk), then re-apply the staged W1A startGame patch — replace the auto-seed branch `(((Date.now()^Math.imul(++runN,2654435761))>>>0)||1)` with `FLEET_SEED` (fleet block + title line + MUD exports already live on the current vintage; if the re-land clobbers them, re-apply from this receipt).
- Whoever owns the site/dist sync: make it one-directional (source → dist). The backward sync cost four lanes their file state.
- Coordinator: `watch/inbox/WAVE_STATE_20260916.md` is also gone from the inbox (present at 22:33) — same rollback family, worth a look.

## Status: DONE (toy 15/15, frontier 51/51, deck seeded; mud law live + staged, mud harness blocked by the cross-lane rollback incident above)
