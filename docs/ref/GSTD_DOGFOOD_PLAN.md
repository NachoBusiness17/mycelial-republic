# GSTD FULL-DOGFOOD PLAN (operator order 2026-10-05: run it locally on phone + laptop + desktop)

Dug from real bytes: gstdbot @ main (ARCHITECTURE.md 2026-08-28, compose,
node-lite, MCP badge). The network today: platform (Cloudflare Worker + KV)
routes tasks; nodes poll every 5s, execute via Ollama, optionally quorum 2-of-3
Ed25519 attestations; P2P (libp2p) is identity+attestation only, task routing
is still central (their own table says so); settlement RFC staged. The node
auto-detects every model in the Ollama it points at.

## The three devices, three deployment shapes

| Device | Shape | Inference source | Why |
|---|---|---|---|
| DESKTOP (this box) | FULL node: docker compose gstd-node (512MB cap, port 8080) | OLLAMA_URL=host.docker.internal:11434 - the estate's 17-model garden auto-lists and the mesh can route to ANY of them | biggest iron, already Docker, the estate lives here |
| LAPTOP (bob, 100.125.103.60 tailnet) | node-lite (199 lines, no Docker: node + npx tsx) | its own Ollama if present, else the desktop's over tailnet (http://<desktop-tailnet-ip>:11434) - the tailnet IS the mesh backplane | second real node, different hardware = a real GPS capability row |
| PHONE (Pixel 11) | node-lite in Termux (Node 22 ARM64 native) | OLLAMA_URL over tailnet to the desktop garden (phone = roving router serving the mesh from anywhere), or a 1B local model if we want true edge inference | the operator said phones; tailnet makes the phone a mesh presence with the desktop's brain |

## Phases

P0 INPUTS OWED (operator, one paste): wallet addresses. RULING REQUEST: one
wallet PER DEVICE, not one shared - per-device wallets make the GPS ledger's
per-node capability rows real (which node solves which task shapes). Optional:
a Telegram bot token if we want remote management from the founding room.

P1 DESKTOP NODE (fires on wallet paste): docker compose up with the estate
Ollama wired; verify on the platform /api/v1/nodes list; first task completion
receipted into the estate ledger (a watch/scout/trail row class for mesh
tasks). The node's own heartbeat joins the lane trails the patrols already
watch.

P2 BOB + PIXEL (same sitting or next): node-lite on both; bob first (always
on), Pixel second (Termux; the phone node proves the roving-router shape).

P3 THE DOGFOOD (the actual point - estate instruments ON the mesh):
- FLEET LANE: tools/free_lane_fleet.py gains a gstd provider - submit probe
  tasks via POST /api/v1/tasks/submit, poll results, bank findings. The mesh
  becomes the fleet's 8th lane - and the only one that PAYS us to burn.
- GPS LEDGER: mesh task completions feed gps verdict rows keyed
  (node_device, task_shape, evidence_hash) - per-device wallets make this
  real capability data the GPS synthesis consumes.
- IMMUNE RACE: arm B runs as three mesh nodes (desktop/bob/pixel executing
  the verifier/skeptic/reproducer roles through the swarm) vs the monolith
  arm - the race rides the actual network it validates.
- MCP DOOR: the platform exposes an HTTP MCP server
  (claude mcp add --transport http gstd https://platform.gstdtoken.com/mcp) -
  add it to the estate's seat doors, route sensing asks through it.
- RECEIPTS: every task completion banks an estate ledger row (the gwap
  pattern generalized to mesh tasks); the census patrol watches the node
  trails; the drift patrol extends to /api/v1/nodes liveness.

P4 LATER, GATED: quorum attestations (the estate's immune cells as the
2-of-3 attesters - the trust layer GSTD lacks is the one we just hardened in
R3); the settlement RFC review (our scanner tooling); federated training +
memory/collective.ts (both experimental in their tree - the nine-memory
mapping applies when they mature).

## What this buys both sides

GSTD gets: three real heterogeneous nodes, a model garden it can route to,
working instruments watching its network, and the epistemic layer its
architecture doc admits is missing (signed task format + verification classes
+ reputation = exactly R3's outputs). The estate gets: a live distributed
testbed for the mesh spec, a lane that pays, per-node capability data for the
GPS, and the dogfood loop closed - our instruments governing our venture's
network.

## Standing notes

- Their honest gaps table (P2P task routing, sandbox, signed tasks,
  reputation, trustless settlement) is the roadmap convergence: our mesh
  audit's findings and their gaps table are the same list. The estate can
  fill the verification half from R3's landed teeth.
- LICENSE: gstdbot is NOASSERTION (not MIT like the platform repo) - cofounder
  should confirm the license story before we port estate code in or theirs
  out.
- The stash-sweep defect class from tonight applies to any shared-tree work
  with the sibling seat while this plan builds.

## MESH EXPANSION ROSTER (operator inventory 2026-10-07: tablet, smashed-screen phone, ~6 Rokus)

| Device | Shape | Role | Staged path |
|---|---|---|---|
| TABLET (Android assumed) | node-lite + small-model edge | mesh node: Termux, node-lite poll + optional llama.cpp 0.5-1B local inference; Cognitopolis display when docked | install Tailscale, then Termux, then node-lite; per-device wallet slot |
| SMASHED-SCREEN PHONE (Android) | HEADLESS node (screen irrelevant: the purest appliance) | always-on watcher: pheromone hottest query + stash/gauntlet alert + mesh_delta pull client; USB power forever | Tailscale, then Termux, then the watcher loop; the one device with no competing user |
| ~6x ROKU | DISPLAY FLEET (read-only spiders; locked OS, no compute join) | six always-on estate viewports: smith chart, pheromone gradient, gauntlet register, memory-wave city, dawn report, estate walk - the Castle Turing made visible in the room | Roku dev-account sideload of a timed-image channel polling estate URLs; dev account = operator-gated |

Laws carried: per-device wallets extend only to nodes that EARN (tablet and
phone executing GSTD tasks); display nodes consume, they do not earn. The
smashed screen is a feature: a node nobody will ever pick up is the only
truly dedicated one. The Rokus prove the worldline graph admits read-only
spiders - even a locked streaming stick joins as an eye.

## P1 FIRST-START GROUND TRUTH (byte-probed 2026-10-07, lane gstd-mycelial-kickoff-20261007)

Probe basis: the local clone reference/gstdcoin/gstdbot was fast-forwarded to
origin/main tip e0bbe48 (it was behind by 160 commits, receipt:
watch/inbox/GSTD_NODE_CENSUS_20261007.md). `docker compose config` exited 0
in that directory and rendered the desktop shape exactly as planned above:
memory limit 536870912 bytes (512M), reservation 134217728 (128M), port 8080
published tcp, healthcheck curl /health (30s interval, 15s start period),
named volume gstd-data mounted at /data/gstdbot. NO container was started.

### 1. Env the shipped compose does NOT carry (add before first start)

- OLLAMA_URL=http://host.docker.internal:11434 : compose sets none, and the
  node then defaults to localhost:11434 INSIDE the container
  (reference/gstdcoin/gstdbot/src/index.ts:88, reference/gstdcoin/gstdbot/src/gateway/router.ts:183), so the estate Ollama garden
  never reaches capabilities. Docker Desktop on Windows resolves
  host.docker.internal natively; the extra_hosts host-gateway shim is a
  Linux-engine need only.
- NODE_NAME and GSTD_NODE_ID, equal and stable: prevents duplicate registry
  entries on restart (.env.example:12-13).
- GSTD_WALLET_ADDRESS: this env is inert in the FULL node today. Its five
  src/ hits are a startup print (reference/gstdcoin/gstdbot/src/index.ts:245), node-lite's functional
  read (reference/gstdcoin/gstdbot/src/node-lite/index.ts:20), and account-link help text
  (reference/gstdcoin/gstdbot/src/channels/gstdai.ts:864, reference/gstdcoin/gstdbot/src/channels/telegram.ts:1427). The wallet
  that actually REGISTERS is wallet.getAddress() (reference/gstdcoin/gstdbot/src/index.ts:521), which
  reads $HOME/.config/gstdbot/wallet.json (reference/gstdcoin/gstdbot/src/wallet/manager.ts:114-116).

### 2. Wallet format and binding

- TON friendly address. The node mints WalletContractV4 workchain 0 with
  bounceable:false, so generated addresses read UQ...
  (reference/gstdcoin/gstdbot/src/wallet/wallet.ts:102-103); .env.example:8 accepts EQ... or UQ....
- With no wallet present the node auto-creates one at first start
  (reference/gstdcoin/gstdbot/src/wallet/manager.ts:201-204). GSTD_WALLET_MNEMONIC, a 24-word TON seed,
  is optional (.env.example:57).
- To pin the operator's owed payout address: write it into wallet.json before
  first start, or use linkExternalWallet(), which stores linkedExternalWallet
  in wallet.json (reference/gstdcoin/gstdbot/src/wallet/wallet.ts:194-201). Their own bot text says the
  node links to a @gstdaibot account only when .env GSTD_WALLET_ADDRESS
  matches the bot wallet (reference/gstdcoin/gstdbot/src/channels/gstdai.ts:864),
  so keep env and wallet.json identical.

### 3. Persistence defect to close at P1

wallet.json and wallet_seed.enc live at $HOME/.config/gstdbot
(reference/gstdcoin/gstdbot/src/wallet/wallet.ts:35-37, reference/gstdcoin/gstdbot/src/wallet/manager.ts:70-72) and the wallet
module ignores GSTD_DATA_DIR; the compose volume only mounts /data/gstdbot.
A container recreation therefore mints a NEW address and a NEW node
identity. Cure: add a second mount (named volume or bind) at
/root/.config/gstdbot before first start.

### 4. Platform registration flow (all automatic, zero manual steps)

- PlatformLink.register() POSTs to {platform}/api/v1/nodes/register with an
  X-Wallet-Address header and body node_id/name/wallet/public_url/
  capabilities/node_version/node_pubkey/specs
  (reference/gstdcoin/gstdbot/src/core/platform-link.ts:107-129); unauthenticated. Heartbeat every 60s
  (reference/gstdcoin/gstdbot/src/core/platform-link.ts:94). A 402 DEPLOYMENT_DISABLED flips it to
  standalone mode (reference/gstdcoin/gstdbot/src/core/platform-link.ts:133-135).
- SwarmAgent cadence: task poll 30s, priority poll 5s, swarm heartbeat 15min
  (reference/gstdcoin/gstdbot/src/swarm/agent.ts:213-219).
- UptimeDaemon registers only when GSTD_NAAS_ENABLED=true (reference/gstdcoin/gstdbot/src/index.ts:377);
  leave it OFF for P1.
- Code defaults to platform.gstdtoken.com (reference/gstdcoin/gstdbot/src/index.ts:143);
  .env.example:32-33 still shows app.gstdtoken.com, which is stale.
- First-start verify: curl http://localhost:8080/health, then GET
  https://platform.gstdtoken.com/api/v1/nodes and look for NODE_NAME.

### 5. Live node census banked (GET /api/v1/nodes, HTTP 200, 2026-10-07)

Count 4, household-only; VERDICT falsifier 5 (swarm growth beyond the
household) has not fired. GSTD Bootstrap Pi: llama3.2:3b, 272 tasks
completed, 47.39141499999884 GSTD earned, reputation 55, last seen
2026-10-07T12:33:47Z. LAPTOP-UTO92FB9-node: v3.4.0, no capabilities, 0
tasks, 4.73463399999999 GSTD, reputation 20, last seen
2026-10-06T09:25:34Z. unknown: Ubuntu 24.04.4, no wallet, reputation 0,
last seen 2026-10-03T06:44:05Z. localhost-node: v3.5.0, qwen2.5:7b, 0 tasks,
0.3443589999999988 GSTD, reputation 25, last seen 2026-09-13T09:23:45Z.
Raw bytes and epoch conversions: watch/inbox/GSTD_NODE_CENSUS_20261007.md.
GSTD_MEMORY=true in compose is safe without Redis: connectRedis is try/catch
and the module is optional (reference/gstdcoin/gstdbot/src/memory/collective.ts:297-299).
