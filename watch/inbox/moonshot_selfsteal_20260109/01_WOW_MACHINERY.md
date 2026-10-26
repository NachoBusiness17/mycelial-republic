# 01 - WOW MACHINERY (Lane 1 of 5, moonshot self-steal wave, 2026-10-08)

Asset 1 of the five-asset composition question. Method: mine estate bytes first; every
claim below carries a path. Anchor receipts read this pass:
watch/inbox/GWAP_BACKEND_RESEARCH_20260929.md, corpus/game_estate/FROM_MUD_TO_WOW_20260914.md,
memory/game/STATE.md, watch/inbox/noir_gwap_steal_20260926/SUBSTRATE_DECISION_20260926.md.

## What it IS (estate bytes)

- A complete WotLK server core, GPL-2: `corpus/library/mod-playerbots` is CMaNGOS
  mangos-wotlk (mangosd worldserver, realmd auth, 24MB src/game, ~943 cpp / 1,916 sql,
  136MB SQL schemas, map-extraction tooling) per GWAP receipt section 1.1.
- The verification moat: frozen-tape replay, fixed 1/60 timestep, seeded RNG, sha256 run
  receipts, one flipped input = INPUT_FORK at the exact frame; 202/202 green
  (GWAP receipt section 1.4).
- The GWAP payload schema: agreement-as-anti-cheat (sealed Robber intent vs independent
  Cop report vs Witness clues) plus the KissKissBan blocker (HCOMP'09) in
  watch/inbox/noir_gwap_steal_20260926/SUBSTRATE_DECISION_20260926.md.
- The ramp thesis: WoW as a Barnes-Hut center of mass standing for twenty years of
  engineering, approximable long before reproducible (FROM_MUD_TO_WOW, Part I).
- The doctrine: game-as-subtle-work, play IS the work, the game funds the supercomputer
  (memory/game/STATE.md, 2026-08-13 manifest).

## What we HOLD (inventory with paths)

- `corpus/library/mod-playerbots` - the CMaNGOS core, 235MB working tree, never built
- `C:\Users\foste\Documents\projects\azerothcore-wow` - the clone, 1.2GB verified by du
  this pass; 825MB extracted client data per the anchor claim; stub history in
  watch/SELF_STEAL_PROJECTS_TREE_ORPHANS_20260904.md (G1)
- Six suites, 64 tests, ALL PASSING (run this pass, 2.88s): tests/test_wow_bones.py (12),
  test_wow_player.py (17), test_wow_world.py (12), test_wow_manifest.py (4),
  test_wow_family.py (8), test_wow_bones_session.py (11)
- `mag/wow_manifest.py` (5.4KB) - the wowhead-clone surface as content-addressed verkle
  knots, already serving through mesh_delta's chunk door unchanged
  (watch/inbox/ONE_COMPUTER_MESH_STEAL_MAP_20261007.md)
- `mag/game_campaign.py` (228KB) - server-authoritative turn resolver, schema
  mag_game_campaign.v1, "engine owns truth; LLM narrates after"
- `dashboard/mud_relay.py` - working RFC6455 presence relay, 8Hz broadcast
- `memory/game/world/world_state.json` (1.75MB) - content-addressed verkle world store,
  game_world.v1
- `mag/water_graph.py` + `mag/water_computer.py` - deterministic engines with proof folds
- Design stack: SUBSTRATE_DECISION_20260926.md, watch/inbox/play_as_work_20260926/,
  queue/handoff/TOKENOMICS_MYTH_GAME_API_20260810.md

## STATE (honest)

- Owned-but-never-executed is the standing disease: nobody has compiled or run the
  CMaNGOS checkout or the clone; the playerbots submodule is an empty gitlink
  (GWAP receipt Part 6); the B1 revive rung is still paper.
- Estate-side bones are green: 64/64 this pass - the WoW-shaped character/world
  architecture is verified even though the server core is not.
- Single-writer world: the verkle chain has one writer on one Windows box; no second
  client has ever contested a leaf (FROM_MUD_TO_WOW, Part IV).
- mud_relay admits its own gaps: no authority, no persistence, no rooms, no auth
  (GWAP receipt 1.6).
- Zero external developers; every dev-experience claim is a hypothesis until B4
  (GWAP receipt Part 6). GPL-2 blocks a closed-source pivot of server-derived code.

## COMPOSITION (four rows)

- WITH TOKEN ECONOMICS: play-as-work gets meter credit only for byte-backed, falsifiable,
  rare artifacts - Jain & Parkes: meters going up is not work
  (watch/inbox/play_as_work_20260926/STEAL_RECEIPT_20260926.md row 1). WoW machinery is
  the artifact mint: a replay-hashed raid clear or a KissKissBan'd agreement payload is
  all three at once. The CMaNGOS AuctionHouse organ in src/game is a ready limit-order
  book for pricing them, and the headless-swarm marketplace
  (queue/handoff/TOKENOMICS_MYTH_GAME_API_20260810.md) makes bot seats paid players on
  the same rails.
- WITH THE 5H WINDOW: the provider 5-hour window quota is the BINDING currency
  (watch/inbox/QUOTA_LEDGER.md, 2026-09-30). The WoW tick architecture is the load
  splitter: the world lives on a clock, not on input (FROM_MUD_TO_WOW, Part V), so
  deterministic ticks, replays, and ollama-janitor bots run free OUTSIDE the window
  while premium judgment (agreement scoring, judge lanes) spends INSIDE it - and WoW's
  weekly raid lockout is the prior-art scheduler: scarcity-windowed content, build
  queues shaped to lockout cadence instead of wall-clock burn.
- WITH THE MESH: world state as a standing wave. mesh_delta (snapshot index, sha-addressed
  chunks, pull client) already carries the wow_manifest knots through its chunk door
  (ONE_COMPUTER_MESH_STEAL_MAP_20261007.md); cr-sqlite (vlcn-io CRDT multi-master SQLite,
  same receipt steal 3, spike planned on a copy of tools/gps_mcp/gps_ledger.db3) is the
  path to multi-master realms: realmd at the auth edge, one mangosd per shard replica,
  world DBs merging as CRDTs - this kills the single-writer limitation named in Part IV.
- WITH GSTD: the seal reads "each GSTD unit = one signed receipt carrying its own
  proof-of-cost; supply grows only with verified work" (state/gstd/genesis.json, sealed
  2026-08-27). A 202/202-grade frozen-tape replay receipt with sha256 plus a cost row IS
  that payload: verified play is the settlement layer, and this asset is the mint where
  the verified work happens.

## MOONSHOT

An AI-populated Azeroth as the GSTD mint. The playerbots module is the inhabited-realm
steal already on file: "Our fleet + this module = an inhabited NT-ACv2 realm"
(watch/inbox/STEALS_LEDGER_20260916.md). Fleet seats and swarm-marketplace bots play;
the 202/202 replay machinery verifies; each verified artifact mints GSTD against real
proof-of-cost; realms replicate mesh-side via cr-sqlite; the 5h window is the raid
lockout that schedules premium judgment. The GWAP receipt Part 3 already named the gap:
"whether bots are the product - playerbots + estate seats = AI-populated worlds - nobody
sells that." The Roblox inversion rides on top: external devs bring shells, we sell
verification, honest meters, and export-everything ownership (GWAP receipt Part 2, L2).

## SELF-STEAL (what our receipts prove that others would pay to know)

- Anti-cheat without kernel drivers: independent authorship + agreement scoring +
  KissKissBan word-bans is a literature-proven fix for the low-effort equilibrium
  (SUBSTRATE_DECISION_20260926.md) - game studios ship anti-cheat rootkits for less.
- Play verification exists and is green: deterministic replay with INPUT_FORK at the
  exact frame (202/202) - no other game platform verifies play at all; this is the moat
  the GWAP receipt itself crowns (section 1.4).
- Meter law for game economies: weight credit to rare byte-backed artifacts, never
  match-early volume - the exact anti-pattern the Roblox DevEx discount monetizes;
  our credit-rails design inverts it (play_as_work receipt + GWAP receipt 1.5).
- The MUD-lineage build order (telnet-over-WebSocket, then tick, then object db, then
  wizard ladder, Diku combat last) is a ranked fun-per-line map any MMO-from-scratch
  team would pay for (FROM_MUD_TO_WOW, Part V).

## FALSIFIER + PROBE

- FALSIFIER: B1 never compiles. Every composition row above routes through a running
  world server; if mangosd cannot build and tick on this box, the composition stays
  paper and the moonshot dies in its current form. Secondary: that anyone pays for
  play-as-computation remains Unproven (FROM_MUD_TO_WOW close, synthesizer row) until a
  second lantern - one external verified payload - exists.
- PROBE (cheapest executable step already run this pass): .venv pytest over the six
  suites = 64/64 green in 2.88s, so the estate bones are not the blocker. The next ONE
  concrete action: `git submodule update --init` inside corpus/library/mod-playerbots,
  then a single CMake configure of the mangosd tree; the first compile error, filed as
  a receipt, converts owned-but-never-executed into a named missing-toolchain list.

Filing: watch/inbox/moonshot_selfsteal_20260109/01_WOW_MACHINERY.md (this file), lane 1
of 5. Em-dash count: 0.
