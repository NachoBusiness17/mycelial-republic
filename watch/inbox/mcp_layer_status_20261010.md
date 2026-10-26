# THE MCP LAYER: full status (2026-10-10, companion to the mr pool analysis)

Operator ask: "explain our experimental use of mcp servers to serve memories across our
swarms or whatever else we use them for did a lot of designing and theory where are we
on all that." Every claim cites a file or a command run this sitting; the live parity
run is reproduced below.

## 1. What the MCP layer is for (the design intent)

The estate uses MCP as the STANDARDIZED NERVE END between seats, swarms, and cold
agents - four jobs, in weight order:

1. SERVE MEMORY TO COLD AGENTS (the "memories across swarms" leg): the SEED-RIB
   (B2-180 format, B2-181 server). Any MCP-capable cold agent spawns
   tools/seed_mcp.py and receives: resources seed://current (the kilobyte seed),
   seed://law-registry (live law bytes), seed://brief-pointers, plus tools
   rebuild_subtree, verify_hash, fetch_bounded_pointer, join_protocol. Bounded
   pointers serve live estate bytes ONLY after a sha256 seal match, capped at
   --max-fetch, else the pointer stays a named stub. The server never invents
   pointer bytes. Falsifier: a cold session rebuilt a working subtree from MCP
   alone, 10/10 cold-join checks, hash-verified (2026-09-26,
   watch/inbox/burn_wave_20260926/B2_181_seed_mcp_20260926.md).
2. EXPOSE ESTATE ORGANS TO CLIENTS (compute leg): the house server
   (mag/mcp_server.py, stdlib-only JSON-RPC) with PROFILES - a profile is a
   projection, not a permission set (the 2026-08-31 quantized dogfood law).
3. ROUTE MODEL CALLS ON MEASURED CAPABILITY (the GPS facade, tools/gps_mcp/):
   routes on pass-rate from a SQLite capability ledger, not marketing labels;
   test-double default, LIVE gstd config since 2026-10-09 (14 real gstd-tier
   models, test_double false; ROUTER_VOCAB_LANDED.md).
4. DOGFOOD PROVIDER SURFACES (the learning leg): 121 hosted provider tools
   counted 2026-09-28, registry two-axis tier/mode, composition laws mined
   (isError contract, refs-are-params, fan-in).

## 2. The surfaces, LIVE RIGHT NOW (mcp_parity.py run this sitting, exit 0)

| surface | transport | serves | status |
|---|---|---|---|
| house stdio | JSON-RPC 2.0 stdio, protocol 2025-06-18 | bridge profile 7/7 | OK |
| house HTTP | POST /mcp gateway 127.0.0.1:8001, X-API-Key | full profile 42/42 | OK |
| docker mag-mcp | TCP bridge 127.0.0.1:8766, always-on | archivist profile 17/17 | OK; container image MATCHES current mag-sovereign:local (0225f08a7c2f) |
| seed MCP | stdio | 3 resources + 4 tools | cold-join falsifier passed |
| GPS facade | stdio, MCP-shaped | ask/cascade/report_capability/record_verdict, 28 tests | test-double + live-gstd configs |

The 10-01 parity break (docker serving a stale 2026-09-26 image with zero estate_
tools, green healthcheck the whole time) is CURED: the container was recreated from
the current image and tonight's check confirms the digest match.

## 3. The theory that got banked (ractor50 lane, 2026-10-01)

watch/inbox/ractor50/mcp.md - 12 sections, doctrine-grade:

- WHAT BELONGS ON THE BRIDGE: seven rules, headlined by one-verb-one-wrapper
  (never a generic run/proxy tool) and stateless-or-caller-held-state (the
  water_graph shape: caller holds the spec, server holds the physics).
- WHAT NEVER CROSSES: enumerated per-tool rulings from the chain-repair
  precedent (effect-carrying verbs stay gated; the effect broker law rides
  above the bridge).
- THE METERING RULE (section 6) and the R2-R4 next-organ priority (section 7,
  reordered by the night's evidence).
- THE MISSING-TOOLS LIST (section 8): what neither house nor provider surfaces
  offered. Top item: estate_receipt_append - a bridge client could not file the
  receipt the workflow gate demands of every wave. THE LOOP-CLOSURE GAP.
- ONE-SITTING BUILD SPEC for it (section 9).

## 4. Where we are: the two named gaps, one closed this month

The doctrine's verdict was: the architecture is sound (transport, pin, isError,
effect-class meta all proved live); the gap is not organs but PARITY and
LOOP-CLOSURE.

- PARITY: CLOSED. Law MCP-2 (an always-on MCP surface without a parity check is
  a stale surface with a green heartbeat) shipped as tools/mcp_parity.py; the
  stale docker surface was caught, the container recreated, and tonight's run is
  a clean PASS across stdio + http + docker with image-digest match.
- LOOP-CLOSURE: CLOSED AT THE TOP. estate_receipt_append landed in the bridge
  (tools/__init__.py maps it to mag.estate_bridge.receipt_append; the bridge
  now serves 7 tools where the doctrine night counted 6 declared / 5 served -
  the drift-withheld estate_thought_compile was resolved and the roster grew).
  A bridge client can now file workflow-gate-grade receipts. The remaining
  R2-R4 organs from section 7 are still design-class, unforced.
- THE PIN GATE has real scalps: its first live fire (2026-10-01) withheld
  estate_thought_compile on a schema hash change with the alarm on stderr -
  the rug-pull class (a tool silently changing shape after clients pinned it)
  now fails loud.

## 5. The memory-swarm theory stack (where memweave sits)

The MCP layer is the TRANSPORT leg of a three-piece memory doctrine:

1. MEMWEAVE (the ghost operating doctrine, .agents/skills/memweave): feed
   STRUCTURES (memlang), not prose, to model seats; weave context across seats
   via the RIB. The distributor is mag/mem_weave_distributor.py. Theory home:
   rib_bus doctrine + the 2026-08-10 adversarial harness evals.
2. MESH-COMMS (the non-MCP nervous system): chan rows {from_lane, to_lane, msg,
   ref}, rib_bus, panels, wants - how seats talk to each other in-process.
   Pheromone bus (tools/pheromone.py, 6h half-life, multi-source
   reinforcement) is the swarm-signaling layer for solver fleets.
3. SEED-RIB over MCP (the cold-boot leg): the only piece that crosses machine
   boundaries - kilobyte seed in, hash-sealed bounded pointers out, join
   protocol for booting into the fleet.

In one sentence: memweave says WHAT to serve (structures, not prose), the seed
says HOW LITTLE to serve (kilobytes plus sealed pointers), and MCP is the pipe
both ride; the swarm side (chan + pheromone) runs in-process where MCP would be
overkill.

## 6. What is still open (ranked, honest)

1. R2-R4 bridge organs (doctrine section 7): design-class, unforced - they
   fire when a swarm actually needs them (demand precedes organ).
2. The 10-01 missing-tools list below the top item: unrebuilt, same law.
3. GPS real-MCP wiring: the facade is MCP-shaped but not MCP-wired; the
   mapping is documented so the wiring is mechanical when a client needs it.
4. Seed MCP second-consumer proof: one cold-join falsifier passed; a SECOND,
   different-client cold boot (e.g. a garage-guild bench or a Pierre-class
   external) would upgrade it from proved-once to proved-portable.
