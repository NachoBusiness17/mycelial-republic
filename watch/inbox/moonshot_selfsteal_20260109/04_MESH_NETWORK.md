# 04 THE MESH NETWORK - lane 4 of the moonshot self-steal (2026-10-09)

Asset: the mycelial mesh. Repo bytes only; every number cites its path.

## What it IS

Heterogeneous devices as one inference computer, memory carried as a torrent-style
standing wave instead of N processes greping one tree:
- The wire: tools/mesh_delta.py (docstring 1-39) - scan (snapshot index, sha256 per
  file), serve (/picture, /delta?since, /chunk verify-then-serve), pull (client that
  sha-verifies every byte), mcp (gps_mcp dialect: picture, delta, fetch, plant,
  witness, tally).
- The doctrine: index ONCE, serve MANY; no seat greps what an index answers. Born
  from a measured disease: four concurrent runs each greping the same tree, 16
  pythons (watch/inbox/MESH_DELTA_SEED_20261007.md).
- The frame: "CASTLE TURING = the mesh" - computation as an inhabited place, the
  Rokus its walls made visible (watch/inbox/ROLL_SHAPE_TURING_CASTLE_20261007.md).

## What we HOLD

- Indexed bytes: 561,386 files / 7.6GB in memory/ bootstrapped (proof round trip
  2026-10-07T01:40Z, MESH_DELTA_SEED); 562,232 on the scan that indexed the WoW
  knots (watch/inbox/WOWHEAD_MESH_P1_20261007.md).
- Device roster (docs/ref/GSTD_DOGFOOD_PLAN.md): desktop (14-core, tailnet
  100.96.161.76, Docker, estate home), bob laptop (100.125.103.60), Pixel 11 Pro
  (100.79.122.101), tablet, smashed-screen phone (headless always-on watcher), ~6
  Rokus (read-only display spiders).
- Tools: tools/mesh_delta.py, tests/test_mesh_delta_guard.py (5 green, SSRF fence),
  mag/wow_manifest.py, gps_ledger.db3 + catalog FTS + water_swarm + k8s lanes
  (inventory: watch/inbox/ONE_COMPUTER_MESH_STEAL_MAP_20261007.md).
- The memlance wire: plant/witness/tally in mesh_delta mcp (tools/mesh_delta.py:337-416);
  memory/mesh/lances/lances_ledger.jsonl holds the first cross-surface HIT
  (2026-10-08, latency 101864.2s).
- Prior-art steals, all mapped in ONE_COMPUTER_MESH_STEAL_MAP: exo (heterogeneous
  one-computer), llama.cpp RPC (layer split), cr-sqlite (CRDT multi-master sqlite),
  rqlite/dqlite, Mem0/Letta/Zep, vast.ai.

## STATE (honest tri-state)

- PROVEN (loopback only): scan -> serve -> pull dry -> chunk fetch sha-verified;
  tamper chunk refused 403; SSRF fence (loopback + tailnet CGNAT + RFC1918 allowlist,
  DNS pinned, redirects refused); WoW knots through the chunk door 6/6, ROUND TRIP
  MATCH True, 9 tests passed (WOWHEAD_MESH_P1).
- STAGED (runbook on disk, not fired): tailnet seeding (serve --bind 100.96.161.76),
  bob's first pull ON bob, node-lite on bob/Pixel, the GSTD wallet paste
  (watch/inbox/GSTD_WALLET_DOOR_20261007.md), Roku sideload, cr-sqlite twins, exo/RPC
  pooling. Blockers, byte-proven: Ollama binds 127.0.0.1 only; bob ssh needs key auth.
- OWED in the proven layer: picture chain_tip cursor reads null (code reads
  tip.index/tip.generated, verkle_tip.json carries n_leaves, updated_minute,
  last_filename - WOWHEAD_MESH_P1 finding 1); per-machine pull tasks (the clock
  side of the wave) unwritten.
- DAYDREAM (paragraph-only): N devices one live picture, phones earning while
  displaying, cr-sqlite merged ledgers, quorum attestations, other people's
  machines walking the light maze for pennies.
- Outside truth: GSTD census count 4, household-only, only the Pi earns (272 tasks,
  47.39141499999884 gstd, reputation 55) - swarm-growth falsifier NOT fired
  (watch/inbox/GSTD_NODE_CENSUS_20261007.md).

## COMPOSITION

- WITH WOW MACHINERY: world state is already content-addressed - WoW knots serve
  through the mesh chunk door UNCHANGED (P1 landed, $0). Next rung: the world as
  CRDT standing wave (cr-sqlite steal) so bob/Pixel play the same dungeon offline
  and merge writes instead of sharing one tree - kills the stash-sweep class for
  game state the way pull --apply kills it for memory. Multi-device play is
  multi-device PUBLISH: every device can seed what it rendered.
- WITH TOKEN ECONOMICS: the lance is a unit with a price and a hit rate -
  plant/witness/tally rows give cross-node steering a measurable P&L (first HIT
  latency 28.3h). The mesh generalizes the DESCENT PROTOCOL ledger across nodes:
  cheap scans/pulls on window-free local janitors, judgment on funded primes, every
  hop hash-verified and receipted.
- WITH THE 5H WINDOW: the window replenishes (99% remained after ~40M tokens,
  watch/inbox/GALA_20260925.md envelope table) and the mesh is what makes a
  replenishing budget compound: stagger device pull windows so indexing never
  contends with the burn, and push window-free scut (seed, serve, watchers) onto
  mesh silicon so the 5h window is spent only on judgment.
- WITH GSTD: the earning nodes ARE the mesh nodes - one roster, one tailnet
  backplane. node-lite on bob/Pixel points OLLAMA_URL at the desktop garden over
  tailnet; heartbeat uptime rewards bank every 30s with no public URL (cloudflared
  is only for task traffic - wallet door finding 4); per-device wallets make the
  GPS capability rows real. GSTD gets our R3 verification teeth (P4 quorum); the
  mesh gets an earning reason to stay powered.

## MOONSHOT

The republic made literal (compass pillar "Device fuels network... device is peer,
not client"; v5 GSTD DePIN seat, docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md).
Desktop seeds the 7.6GB memory picture on the tailnet; bob, Pixel, tablet, and the
smashed phone pull deltas on a clock, each keeping a tandem local copy - the
standing wave, 561k content-addressed cells with the same sha on every machine.
The same phones run node-lite and earn GSTD uptime while displaying the gauntlet
register; the ~6 Rokus poll estate URLs as the castle's read-only walls. cr-sqlite
twins merge the SQL ledgers the devices independently wrote; exo or llama.cpp RPC
pools desktop+bob inference as one endpoint; the GPS ledger + water_swarm route by
task_shape and load, vast.ai-style. Sellable edge: light mazes are measurement
instruments - other people's devices walk them for pennies and the estate reads
the walker's shape.

## SELF-STEAL

- Convergence: mesh_delta independently re-derived IPFS/Bitswap content addressing
  (named in the steal map). No second sync layer; the chunk door is the one door.
- The estate already holds the switchboard organs (FTS, GPS ledger, water_swarm, k8s
  lanes); the mesh's only NEW law is index-once-serve-many. Compose, do not rebuild.
- Steering across nodes already has a wire (plant/witness/tally, falsifier 2-of-5
  in .agents/skills/memlance/SKILL.md) - missing is the clock (per-machine pull
  tasks), not the mechanism.
- The GSTD P3 fleet lane (gstd provider in tools/free_lane_fleet.py, "the only one
  that PAYS us to burn") is the template for mesh-as-lane.

## FALSIFIER + PROBE

- FALSIFIER: a second device must hold the same picture. If bob's pull against the
  tailnet seed fails, sha-mismatches, or drifts while the desktop churns, the
  standing wave is a loopback demo and the one-computer claim dies by its own
  receipt. Republic falsifier: 4 weeks after the wallet paste, zero estate-earned
  gstd and zero non-desktop merged writes = display fleet, not a republic.
- PROBE (cheapest executable step, the standing OWED item, zero wallets, zero
  Docker): on the desktop, `.venv\Scripts\python.exe -m tools.mesh_delta serve
  --bind 100.96.161.76 --port 8767` (burners cage per the longrunners law); then
  ON bob `python -m tools.mesh_delta pull --peer http://100.96.161.76:8767` (dry
  first, --apply after). Success = bob's dry report returns the desktop picture's
  files/bytes/ts, every chunk sha-verified. Same sitting: wire the null cursor key
  (read n_leaves/updated_minute/last_filename) and append the receipt to
  MESH_DELTA_SEED's owed list.
