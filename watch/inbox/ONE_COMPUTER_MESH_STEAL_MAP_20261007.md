# THE ONE-COMPUTER MESH: steal map (prior-art sweep, self-steal first)

- Operator order 2026-10-07: "how can we use this in our mcp memory server in
  conjunction with our wowhead clone and local sql across all surfaces to
  reroute requests as one computer across lanes sort of like a vast ai...
  would it be possible to virtualize 14 physical processors via dockers and
  do it even better? Who else is doing this - we should check what already
  exists and steal it."
- Sweep instrument: estate inventory (bytes) + targeted web search (this
  sitting). LINKS rows: exo 1791337946849904, cr-sqlite 1791337946864574.

## The estate already holds the organs (self-steal inventory)

- mesh_delta (built tonight): the memory standing wave - snapshot index,
  sha-addressed chunks, picture/delta/chunk doors, pull client, MCP dialect.
  Independently re-derived IPFS/Bitswap content addressing (the convergence
  count keeps rising).
- memlance (.agents/skills/memlance): the aimed seed - plant ONE memory in a
  target seat's boot path so a later decision bends without a command;
  hit-rate tallied (plant_ts/hit_ts/latency). This is the PyLance idea in
  memory: intelligence served into context before it is asked for.
- wowhead clone = mag/wow_manifest.py: the Turtle WoW/WoWHead foundation
  manifested as VERKLE KNOTS (content-addressed) + RIB interpretation +
  world_rib rendering. The game-database surface is ALREADY
  content-addressed - it serves through mesh_delta's chunk door unchanged.
- Local SQL across surfaces: catalog/catalog_fts.sqlite,
  catalog/receipt_fts.sqlite, tools/gps_mcp/gps_ledger.db3, the trail/flow
  JSONL ledgers, and the ESTATE_INDEX sqlite migration design (r04 lane).
- water_swarm: the swarm-as-water doctrine - the invariant lattice pre-shapes
  the swarm's flow. The operator's water-computer spec as a working organ.
- k8s water lanes + docker-compose 9 services (mag, worker cage, ollama
  sidecar retired-to-profile, openclaw stack, mcp).
- Prior art already mined: localfirst-memory drop-dig 10-01 (7/7 lanes, the
  PAM claim corrected), Uber MCP Gateway (intel batch 3, 10-05), ReFlux
  delta-not-state, NHA in-model memory tiering.

## The steals (who else is doing it)

1. exo (exo-explore/exo): heterogeneous devices into "one computer" for
   inference; topology-aware model splitting; frankenclusters (DGX+Mac)
   proven. STEAL: the split-by-topology contract for desktop+bob inference
   pooling - the 14-core box plus bob's silicon presented as one endpoint.
2. llama.cpp RPC backend: the second school - split ONE model's layers
   across hosts (RPC_SERVERS). STEAL: the simpler door when a model will not
   fit this box; pairs with the ALoDLM garden probe (1.7B first).
3. cr-sqlite (vlcn-io): CRDT multi-master SQLite merging for databases that
   took independent writes; offline-capable. STEAL: the local-SQL plane -
   gps_ledger.db3 + catalog FTS replicas per machine that merge instead of
   sharing one tree (kills the stash-sweep class for ledgers). The 2026
   local-first synthesis names a cr-sqlite-backed MCP memory server as where
   agent memory is heading - the mesh_delta + memlance composition converged
   on it independently.
4. rqlite / dqlite: the strong-consistency school (Raft, leader-based) where
   ledgers need ordering over availability. STEAL: the consistency taxonomy -
   CRDT peers for memory/catalog, Raft only where a ledger must not fork.
5. Mem0 / Letta / Zep: the 2026 agent-memory race - MCP-standardized hybrid
   vector+graph memory services. STEAL: their MCP tool surfaces as the
   memlance server's API sketch (and the prior-art check: memlance's aimed
   injection + hit-rate tally is a shape none of them center - they retrieve,
   the lance plants).
6. vast.ai: the framing steal - the mesh presents as ONE resource with a
   market; our bids are capability x load rows in the GPS ledger.

## The Docker / 14-core question, answered honestly

Docker cannot create compute across machines - containers share one kernel.
Per machine it buys: caps and pinning (the burners cage, cpuset per lane =
the 14 cores allocated like a market instead of a mosh pit), restart policy,
and the longrunners fence. Across machines it takes a SCHEDULER to present
one API: the k8s water lanes are that organ; Ray/Nomad are the generic
steals. And for inference specifically, exo/llama.cpp-RPC do the "one
computer" split without any scheduler. So: 14 cores virtualized via Docker
= capped and pinned (better than today's mosh pit); 14 cores PLUS bob
presented as one = exo/RPC for inference, k8s/water_swarm for lanes.

## The composed architecture (one paragraph)

Desktop seeds mesh_delta (memory standing wave) + serves wow_manifest's
verkle knots through the same chunk door; every surface's SQL gains a
cr-sqlite crfile twin so desktop/bob/Pixel merge independently-written
ledgers; memlance rides the MCP memory server as the aimed-injection tool
(plant/witness/tally next to picture/delta/fetch); inference pools across
desktop+bob via exo or llama.cpp RPC; the GPS ledger + water_swarm route
tasks by task_shape and load - requests reroute as one computer across lanes,
vast.ai-style, with every hop hash-verified and receipted.

## First probes (one seat one sitting each)

- P1: serve wow_manifest knots through mesh_delta's chunk door (the clone
  becomes a mesh surface, $0).
- P2: cr-sqlite spike on a COPY of gps_ledger.db3 - two replicas, independent
  writes, merge, verify (never the live ledger).
- P3: llama.cpp RPC spike: split a small model desktop+bob, measured
  tokens/sec vs single-host (the exo door opens if RPC proves the latency).
- P4: memlance server tool: plant/witness/tally as MCP tools beside
  picture/delta/fetch (the aimed throw gets a wire).
