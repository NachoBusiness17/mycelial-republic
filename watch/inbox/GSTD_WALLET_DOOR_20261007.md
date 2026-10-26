# GSTD WALLET DOOR: the one-paste runbook (2026-10-07, lane g5-wallet-door)

Closes P0 INPUTS OWED of docs/ref/GSTD_DOGFOOD_PLAN.md: the operator fills
exactly three wallet addresses at the top of one PowerShell block and pastes
it. The paste fires P1 (desktop FULL node) end to end and prints the P2
commands for bob and pixel with the addresses already baked in.

Basis: byte-traced this day on reference/gstdcoin/gstdbot at tip
e0bbe4851b9c4ddcc0dd9956a8f258e8c1320280 (the same tree the P1 ground-truth
section of the dogfood plan probed), plus live probes run this session
(listed in section 7). GSTD_FORENSICS_20260918.md is the trust context: the
network pays through the platform gateway, so the payout address we paste is
what the gateway credits; the node itself never signs a TON transaction
(reference/gstdcoin/gstdbot/src/swarm/agent.ts:695-696 says this of its own
wallet).

## 1. THE ONE INPUT

Three TON friendly addresses, one PER DEVICE (the P0 ruling request; per-device
wallets are what make the GPS ledger's per-node capability rows real):

| slot | device | example placeholder used below |
|---|---|---|
| DESKTOP_WALLET | desktop (FULL node, docker compose) | UQDesktop... |
| BOB_WALLET | bob, the laptop (node-lite) | UQBob... |
| PIXEL_WALLET | Pixel 11 Pro (node-lite in Termux) | UQPixel... |

Format law: TON friendly (human-readable) form, `UQ...` or `EQ...` prefix
(.env.example:8 names both). Recommend `UQ...` (non-bounceable): it is what
the node mints itself (reference/gstdcoin/gstdbot/src/wallet/wallet.ts:103,
bounceable:false) and every wallet on the live platform reads `UQ...`
(watch/inbox/GSTD_NODE_CENSUS_20261007.md section 3: all four listed nodes
with wallets carry UQ-prefixed strings). Do not paste the raw form
(`workchain:hex`). No client-side regex validates the string anywhere: the
node-lite gate is only "is it nonempty"
(reference/gstdcoin/gstdbot/src/node-lite/index.ts:147-150). Platform-side
validation is UNREAD: the Cloudflare Worker that serves
platform.gstdtoken.com is not in the local clones (reference/gstdcoin/web is
the Next.js frontend; grep for nodes/register in its src found nothing), so
the format law above rests on .env.example plus observed live data, marked
honestly.

The three addresses must be three DISTINCT external wallet addresses you
control (Tonkeeper, @wallet in Telegram, any TON wallet). They are payout
destinations only; no keys go into this repo or the nodes.

## 2. The registration field, byte-exact (what the paste is FOR)

Two different code paths consume the address, per shape:

FULL node (desktop). The registering wallet is wallet.json's `address`
field, never the .env var. Trace: NodeWallet stores wallet.json at
`$HOME/.config/gstdbot/wallet.json`
(reference/gstdcoin/gstdbot/src/wallet/manager.ts:70-72), `getAddress()`
returns that address (reference/gstdcoin/gstdbot/src/wallet/manager.ts:114-116),
reference/gstdcoin/gstdbot/src/index.ts wires it into the
revenue engine at startup (reference/gstdcoin/gstdbot/src/index.ts:292-294),
the gateway's PlatformLink registers with it in both the body field
`wallet` and the header `X-Wallet-Address`
(reference/gstdcoin/gstdbot/src/core/platform-link.ts:111-116), and every
SwarmAgent register/heartbeat call carries the same header
(reference/gstdcoin/gstdbot/src/swarm/agent.ts:1357-1361). `GSTD_WALLET_ADDRESS`
as env is inert for the FULL node's registration; its only live reader is
the startup print (reference/gstdcoin/gstdbot/src/index.ts:245) and the
account-link help text. We still set it in the override, identical to
wallet.json, because the @gstdaibot link flow compares the env value
(reference/gstdcoin/gstdbot/src/channels/gstdai.ts:864) and identical
values keep the dashboard honest.

node-lite (bob, pixel). The registering wallet is the value of the
`--wallet` flag or the `GSTD_WALLET_ADDRESS` env
(reference/gstdcoin/gstdbot/src/node-lite/index.ts:20), and it lands in the
body field `wallet` of POST {SWARM_URL}/api/v1/nodes/register
(reference/gstdcoin/gstdbot/src/node-lite/index.ts:45-60). Node-lite has no
wallet.json at all; if the value is empty the process refuses to start:

    if (!WALLET) {
        console.error('Usage: gstd-node --wallet EQ... [--name my-node] [--port 8765]');
        process.exit(1);
    }

(reference/gstdcoin/gstdbot/src/node-lite/index.ts:146-150, byte-copied.)
The full lite registration body: node_id, name, wallet, node_url, cpu_cores,
ram_mb, ram_free_mb, gpu, capabilities, models, version ("1.0.0-lite"),
status; heartbeats every 30s carry wallet again
(reference/gstdcoin/gstdbot/src/node-lite/index.ts:73-93, 185).

Identity pins (both shapes, prevents duplicate registry rows on restart):
NODE_NAME and GSTD_NODE_ID equal and stable
(.env.example:12-13). node-lite would otherwise randomize the name every
restart (`lite-` plus 3 random hex bytes,
reference/gstdcoin/gstdbot/src/node-lite/index.ts:21). Pins chosen:
gstd-desktop (docker), lite-bob, lite-pixel.

## 3. Where each address lands

| device | lands in | registration reads it from |
|---|---|---|
| desktop | wallet.json `.address` at C:\Users\foste\.gstd_wallet_desktop\ (bind-mounted to /root/.config/gstdbot in the container) + the identical GSTD_WALLET_ADDRESS env in docker-compose.override.yml | wallet.json address via getAddress() |
| bob | GSTD_WALLET_ADDRESS env on the ssh command line (or --wallet) | body field `wallet` |
| pixel | GSTD_WALLET_ADDRESS env in Termux (or --wallet) | body field `wallet` |

Why a docker-compose.override.yml and NOT a .env file in the clone: compose
does not inject .env variables into containers (it uses them only for
interpolation, and the shipped docker-compose.yml interpolates nothing).
Proven this session: with .env carrying GSTD_WALLET_ADDRESS=EQTEST_interp_check,
`docker compose config` rendered no trace of the variable; with the same
value in docker-compose.override.yml environment it rendered as
`GSTD_WALLET_ADDRESS: EQTEST_interp_check` alongside NODE_NAME, OLLAMA_URL,
and `target: /root/.config/gstdbot` (exit 0). Both test files were removed
after the proof; the clone tree is clean.

Why the wallet.json bind mount (the persistence cure, plan P1 section 3):
the wallet module ignores GSTD_DATA_DIR and writes to $HOME/.config/gstdbot
(reference/gstdcoin/gstdbot/src/wallet/wallet.ts:35-37), the shipped volume
only covers /data/gstdbot, so an unmounted container recreation mints a NEW
address and a NEW node identity. The override adds
C:/Users/foste/.gstd_wallet_desktop:/root/.config/gstdbot so the pinned
address survives every recreation and stays inspectable from Windows.

Why wallet.json hand-pinning is safe for an external address: NodeWallet
init loads an existing wallet.json as-is when present
(reference/gstdcoin/gstdbot/src/wallet/manager.ts:81-90); the only field
registration touches is `address`; `getSeed()` degrades to null when
wallet_seed.enc is absent (reference/gstdcoin/gstdbot/src/wallet/wallet.ts:155-162)
and nothing at boot requires it; publicKey is stored but the registration
body's node_pubkey comes from the P2P identity module, not the wallet
(reference/gstdcoin/gstdbot/src/index.ts:271). The paste writes the
shape initWallet writes (address, publicKey, created;
reference/gstdcoin/gstdbot/src/wallet/wallet.ts:106-111) with publicKey "".

## 4. THE PASTE (fill three lines, paste into PowerShell on the desktop)

Idempotent: safe to re-paste after any abort; done steps are skipped or
rewritten with the same values. Abort paths print the fix and stop without
starting anything.

```powershell
function Gstd-Door {
  # ===== THE ONE INPUT: three addresses, one per device =====
  $DESKTOP_WALLET = "UQDesktop_paste_real_address_here"
  $BOB_WALLET     = "UQBob_paste_real_address_here"
  $PIXEL_WALLET   = "UQPixel_paste_real_address_here"
  # ==========================================================
  $REPO    = "C:\Users\foste\Documents\projects\local_sovereign_agent\reference\gstdcoin\gstdbot"
  $WDIR    = "C:\Users\foste\.gstd_wallet_desktop"
  $WDIRFWD = "C:/Users/foste/.gstd_wallet_desktop"
  $DESK_IP = "100.96.161.76"

  if ($DESKTOP_WALLET -match "_paste_real" -or $BOB_WALLET -match "_paste_real" -or $PIXEL_WALLET -match "_paste_real") {
    Write-Host "ABORT: fill the three wallet lines at the top first."; return
  }

  # Guard: Ollama must answer on the tailnet IP (proven broken 2026-10-07).
  try {
    Invoke-RestMethod -TimeoutSec 5 "http://${DESK_IP}:11434/api/version" | Out-Null
    Write-Host "OK: Ollama reachable on ${DESK_IP}:11434"
  } catch {
    Write-Host "ABORT: Ollama answers only on 127.0.0.1 (netstat-proven 2026-10-07)."
    Write-Host "FIX: setx OLLAMA_HOST 0.0.0.0  then QUIT and RESTART Ollama, then paste again."
    return
  }

  # P1 step 1: pin the desktop wallet BEFORE first start.
  New-Item -ItemType Directory -Force $WDIR | Out-Null
  $wfile = Join-Path $WDIR "wallet.json"
  if (Test-Path $wfile) {
    $existing = (Get-Content $wfile | ConvertFrom-Json).address
    if ($existing -ne $DESKTOP_WALLET) {
      Write-Host "ABORT: $wfile already pins $existing. Delete it first if that address is wrong."; return
    }
    Write-Host "OK: wallet.json already pins $DESKTOP_WALLET"
  } else {
    @{ address = $DESKTOP_WALLET; publicKey = "";
       created = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ") } |
      ConvertTo-Json | Set-Content -Encoding ASCII $wfile
    Write-Host "OK: wrote $wfile"
  }

  # P1 step 2: write the compose override (upstream compose.yml untouched).
  @"
services:
  gstd-node:
    environment:
      - NODE_NAME=gstd-desktop
      - GSTD_NODE_ID=gstd-desktop
      - OLLAMA_URL=http://host.docker.internal:11434
      - GSTD_WALLET_ADDRESS=$DESKTOP_WALLET
    volumes:
      - $WDIRFWD:/root/.config/gstdbot
"@ | Set-Content -Encoding ASCII (Join-Path $REPO "docker-compose.override.yml")
  Write-Host "OK: wrote docker-compose.override.yml"

  # P1 step 3: fire.
  Push-Location $REPO
  docker compose up -d

  # P1 step 4: verify (node registers within seconds of start; heartbeat 60s).
  Start-Sleep -Seconds 20
  Write-Host "== /health =="
  curl.exe -s -m 10 http://localhost:8080/health
  Write-Host ""
  Write-Host "== platform nodes (look for gstd-desktop and your UQDesktop address) =="
  curl.exe -s -m 20 "https://platform.gstdtoken.com/api/v1/nodes"
  Write-Host ""
  Pop-Location

  # P2 blocks, printed with real addresses (run when each device's prereq lands).
  Write-Host "== P2 BOB (prereq: ssh key auth per watch/inbox/GSTD_POOL_SETUP_20261001.md) =="
  Write-Host "ssh bob@100.125.103.60 ""git clone --depth 1 https://github.com/gstdcoin/gstdbot.git ~/gstdbot 2>/dev/null; cd ~/gstdbot && GSTD_WALLET_ADDRESS=$BOB_WALLET NODE_NAME=lite-bob GSTD_NODE_ID=lite-bob OLLAMA_URL=http://${DESK_IP}:11434 nohup npx -y tsx src/node-lite/index.ts >> ~/gstd_lite.log 2>&1 &"""
  Write-Host ""
  Write-Host "== P2 PIXEL (paste inside Termux; prereq: Termux from F-Droid) =="
  Write-Host "pkg update -y && pkg install nodejs-lts git -y"
  Write-Host "termux-wake-lock"
  Write-Host "git clone --depth 1 https://github.com/gstdcoin/gstdbot.git ~/gstdbot && cd ~/gstdbot"
  Write-Host "GSTD_WALLET_ADDRESS=$PIXEL_WALLET NODE_NAME=lite-pixel GSTD_NODE_ID=lite-pixel OLLAMA_URL=http://${DESK_IP}:11434 npx -y tsx src/node-lite/index.ts"
}
Gstd-Door
```

What fires the moment the paste lands (P1): wallet.json pinned; override
written; `docker compose up -d` starts gstd-node with the estate Ollama
wired (OLLAMA_URL host.docker.internal:11434) and the wallet volume
mounted; the container registers itself to
https://platform.gstdtoken.com/api/v1/nodes/register automatically
(PlatformLink, unauthenticated, heartbeat every 60s,
reference/gstdcoin/gstdbot/src/core/platform-link.ts:85-96, 107-129;
registration also retries on subsequent heartbeats after any failure,
reference/gstdcoin/gstdbot/src/core/platform-link.ts:147-148). Verification
curls then prove it. GSTD_NAAS
stays OFF (UptimeDaemon registers only when GSTD_NAAS_ENABLED=true,
reference/gstdcoin/gstdbot/src/index.ts:377).

P2 timing (honest deviation from "one paste fires everything"): the paste
PRINTS the bob and pixel commands rather than auto-firing them, because
the estate's own pool-setup doc marks both prereqs unmet: bob is "ONLINE
but SSH needs key auth" and the Pixel is "ONLINE but no SSH server"
(watch/inbox/GSTD_POOL_SETUP_20261001.md bodies table). The moment each
prereq lands, the printed line fires that device: no further inputs, the
addresses are already baked in. The one-paste door is therefore: paste
once for P1, then one ssh line for bob and one Termux paste for the Pixel.

## 5. Device prerequisites (checked, ordered)

Desktop: Docker running (compose config exited 0 on this tree,
watch/inbox/GSTD_NODE_CENSUS_20261007.md section 2); Ollama reachable on
the tailnet IP (see the Guard; currently BROKEN, section 6); port 8080 free
on the host (shipped compose publishes 8080).

Bob (laptop, 100.125.103.60): ssh key auth per the pool-setup doc; node
18+ and git present (`node --version`, `git --version`; node-lite needs
only npx tsx plus its 4 node builtins,
reference/gstdcoin/gstdbot/src/node-lite/index.ts:11-14). Its OS flavor is
UNVERIFIED (pool-setup table: specs TBD; hostname LAPTOP-UTO92FB9 smells
Windows): the printed P2 line is bash-flavored; if `ssh bob@100.125.103.60
"uname -a"` fails, run the same env-prefixed command in PowerShell on bob
instead (drop nohup and the trailing &, keep the log redirect).

Pixel (Termux, 100.79.122.101): Termux from F-Droid; `pkg install nodejs-lts
git` gives Node 22 ARM64 native; termux-wake-lock keeps the node alive with
the screen off. Cloudflared is optional on both lite devices (next section).

## 6. Negative findings, first-class (all byte-proven this session)

1. Ollama listens on 127.0.0.1 ONLY: `netstat -ano` shows
   `TCP 127.0.0.1:11434 ... LISTENING`; curl to the tailnet IP
   http://100.96.161.76:11434/api/version exits 7 / HTTP 000 (refused).
   Consequence: bob, the Pixel, AND the desktop container
   (host.docker.internal arrives on a non-loopback interface) all fail
   against today's Ollama. The paste's Guard fail-closes on this and prints
   the fix (setx OLLAMA_HOST 0.0.0.0 + restart Ollama). Ollama 0.34.3
   answered on 127.0.0.1 ({"version":"0.34.3"}).
2. A bare .env in the clone never reaches the container (section 3 proof).
   Any future "just put the wallet in .env" move is a no-op for the FULL
   node; doubly so because the FULL node's registration reads wallet.json,
   not the env (section 2).
3. Platform-side wallet validation UNREAD: the Worker serving
   platform.gstdtoken.com is not in the local clones. Format law rests on
   .env.example:8 and the live census's UQ-form wallets. If the platform
   rejects a pasted EQ form, switch that device's address to UQ form and
   re-paste (the override rewrites; delete wallet.json first if the desktop
   address changes).
4. node-lite earns two ways and the tunnel is one of them: heartbeats bank
   uptime rewards every 30s (reference/gstdcoin/gstdbot/src/node-lite/index.ts:185)
   with no public URL needed, but task traffic needs node_url, and node-lite
   silently skips the quick tunnel when cloudflared is missing
   (reference/gstdcoin/gstdbot/src/node-lite/index.ts:116, "skipping tunnel").
   Live evidence the tunnel is the earning path for lite shapes: the only
   real earner in the census (the Pi, 272 tasks) carries a
   .trycloudflare.com node_url (watch/inbox/GSTD_NODE_CENSUS_20261007.md
   section 3). Install cloudflared on bob/pixel when task-traffic earning
   is wanted; uptime rewards flow regardless.
5. Erratum to the plan's P1 ground truth: it cites
   reference/gstdcoin/gstdbot/src/index.ts:521 as "the
   wallet that actually REGISTERS". Line 521 is the P2P identity wire
   (`walletAddress: wallet.getAddress()` into GstdP2PNode); the PlatformLink
   registration feed is reference/gstdcoin/gstdbot/src/index.ts:292-294
   (revenue.setWalletAddress) plus
   reference/gstdcoin/gstdbot/src/gateway/server.ts:350 (PlatformLink
   construction). Conclusion unchanged
   (wallet.json's address registers); citation corrected here because this
   lane does not edit the census lane's section of the plan doc.

## 7. Provenance (commands run this session, 2026-10-07)

- git rev-parse HEAD in the clone: e0bbe4851b9c4ddcc0dd9956a8f258e8c1320280.
- git status --short in the clone: only `?? .mimosa/` (tree clean of my
  probes; both test artifacts removed after proving).
- tailscale ip -4: 100.96.161.76 (desktop, matches the pool-setup table).
- netstat -ano | grep ":11434.*LISTEN": 127.0.0.1 bind only.
- curl http://localhost:11434/api/version: {"version":"0.34.3"}.
- curl http://100.96.161.76:11434/api/version: exit 7, HTTP 000.
- docker compose config with throwaway .env then throwaway
  docker-compose.override.yml (values EQTEST_interp_check / gstd-desktop):
  bare .env rendered nothing; override rendered all four keys plus
  `target: /root/.config/gstdbot`, exit 0. Both files deleted after.
- grep nodes/register in reference/gstdcoin/web/src: no matches.
- Byte sources for every code citation: read in full this session
  (node-lite/index.ts 1-199, platform-link.ts 80-149, wallet/manager.ts
  60-209, wallet/wallet.ts 30-224, index.ts 238-300 + 512-531 +
  grep-located lines, swarm/agent.ts 295-335 + 1340-1380, .env.example,
  docker-compose.yml, lib/wallet-link-headers.ts).
