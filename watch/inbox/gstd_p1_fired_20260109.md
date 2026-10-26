# GSTD P1 FIRED - the trigger pulled - 2026-10-09

The moment the operator circled since 2026-10-08 ("almost afraid to pull the
trigger") landed this sitting. Sequence, byte-backed:

1. THE PASTE: desktop payout address pasted in-chat (public-address-only
   law held; no keys ever touched chat, repo, or disk).
2. PRECONDITION CURED: OLLAMA_HOST=0.0.0.0 (setx for future starts +
   headless `ollama serve` launched with the env in-process - the setx-only
   first attempt failed because the launcher inherited the old env; lesson
   banked). Ollama now answers on 127.0.0.1 AND tailnet 100.96.161.76
   ({"version":"0.34.3"} on both).
3. WALLET PIN + OVERRIDE: C:\Users\foste\.gstd_wallet_desktop\wallet.json
   (address/publicKey""/created shape per the runbook) +
   docker-compose.override.yml (NODE_NAME=gstd-desktop, GSTD_NODE_ID pinned,
   OLLAMA_URL=host.docker.internal:11434, wallet bind-mount).
4. FIRST FIRE: container up; ~3 heartbeats rode the FIRST address (loaded).
5. OPERATOR RULING (the small-fries question): fresh empty wallet wins -
   on-chain observability paints targets and merges identity clusters; a
   founder node streaming into a visible hoard reads as extraction
   plumbing; fresh-from-zero tells the honest earning story; per-device
   wallets were already estate law. Container STOPPED within minutes.
6. THE SWAP ("what would satoshi do"): second paste = fresh zero-balance
   address; wallet.json repinned, override rewritten, container
   force-recreated.
7. VERIFIED: platform.gstdtoken.com/api/v1/nodes reads 5 nodes (was 4),
   gstd-desktop present; /health = ok, v3.5.0, swarm.models=10 (garden
   wired), peers 0 (newborn).

## State now

- Node: gstd-desktop (docker, desktop FULL node, identity pinned)
- Payout: the FRESH address (vault address retired from the stream after
  ~3 heartbeats; never use the loaded wallet as a node payout again)
- Earning: uptime rewards via 60s heartbeats now; TASK traffic likely needs
  a public node_url (census: the only task-earner, the Pi, runs a
  trycloudflare URL) - cloudflared on the desktop is the next rung when
  task earning is wanted (operator call).
- P2 OWED (no rush): bob + pixel node-lite, EACH with its own fresh
  zero-balance wallet (same small-fries law); runbook P2 lines print with
  addresses baked; prereqs per GSTD_POOL_SETUP_20261001 (bob ssh key auth,
  pixel Termux).
- The longrunner law: gstd-node is a containerized long-runner (compose);
  patrol row owed at next census.

Runbook: watch/inbox/GSTD_WALLET_DOOR_20261007.md (executed as written,
with the wallet swap as the one operator-ordered deviation).
