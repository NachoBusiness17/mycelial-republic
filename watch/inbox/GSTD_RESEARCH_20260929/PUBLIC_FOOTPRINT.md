# GSTD (gstdcoin) PUBLIC FOOTPRINT

Date: 2026-09-29. Method: live WebSearch, WebFetch, and curl probes run 2026-09-29 ~13:50-14:15 UTC against public surfaces (tonapi.io, toncenter.com, api.dexscreener.com, api.coingecko.com, registry.npmjs.org, api.github.com, the gstdtoken.com domains, Telegram previews, X profile, GitHub). Companion to the local clone forensics (`watch/inbox/GSTD_FORENSICS_20260918.md`, `watch/inbox/GSTD_T0_PROBE_20260918.json`, `watch/inbox/THE50_W7_T34_GSTDBOT_AUDIT.md`). Verdicts are tri-state: Supported / Disputed / Unproven. Failed probes are recorded, not papered over.

---

## 1. Chain and contract

- GSTD is deployed on TON as a jetton named "Gold Standard" (symbol GSTD), 9 decimals, total supply exactly 1,000,000,000, mintable: false. Jetton master address `EQDv6cYW9nNiKjN3Nwl8D6ABjUiH1gYfWVGZhfP7-9tZskTO` (raw `0:efe9c616f673622a337737097c0fa0018d4887d6061f59519985f3fbfbdb59b2`). Supported. Source: https://tonapi.io/v2/jettons/EQDv6cYW9nNiKjN3Nwl8D6ABjUiH1gYfWVGZhfP7-9tZskTO (fetched 2026-09-29).
- Deployment date: the master account's first transaction is an account init (orig_status nonexist, end_status active) at 2025-07-04 13:29 UTC. Supported (init tx equals deployment). Source: https://toncenter.com/api/v3/transactions?account=0:efe9c616...&sort=asc&limit=1.
- Holder count: 206 holders as of 2026-09-29. Supported. Source: tonapi jetton endpoint above.
- Top-holder concentration: top 5 addresses hold 46.33 percent of supply, top 10 hold 67.98 percent (computed from the top-100 holders endpoint; 5th-ranked holder is the STON.fi DEX pool at 9.72 percent, which is effectively the entire liquid float). Two unrelated-looking wallets hold exactly 5.00 percent each, consistent with structured buckets. Supported. Source: https://tonapi.io/v2/jettons/EQDv6cYW.../holders?limit=100.
- Jetton metadata narrative is GOLD, not AI: description reads "Gold Standard is an innovative project in the TON ecosystem that combines the stability of tokenized gold with a decentralized blockchain architecture." Image is hosted on cdn.blum.codes (Blum ecosystem CDN). tonapi classifies the jetton verification as "whitelist". Supported. Source: tonapi jetton endpoint above.
- Same address is cited on the official site and wired into the STON.fi swap links. Supported. Source: https://gstdtoken.com and the dexscreener pair listing below.

## 2. Market reality

- Live but effectively dormant market. One DEX pair: STON.fi, GSTD quoted against GRAM, pair created 2025-07-31 17:24 UTC. Supported. Source: https://api.dexscreener.com/latest/dex/search?q=gstd (fetched 2026-09-29), pair https://dexscreener.com/ton/eqbakubvv_ppbcmcpnwqxkfv1iihtve5imya8-wg0hpmznh8.
- Current numbers at fetch time: price $0.00005643, market cap and FDV both $56,437, liquidity $10,462, 24h volume $1.26 across 2 transactions (1 buy, 1 sell), 6h 1 buy, price change h24 -0.85 percent. Supported. Source: dexscreener pair data above.
- Not listed on CoinGecko: API search for "gstd" returns empty coins/exchanges/categories. Supported. Source: https://api.coingecko.com/api/v3/search?query=gstd.
- Not listed on CoinMarketCap: https://coinmarketcap.com/currencies/gstd/ returns HTTP 404. Supported. Source: that fetch, 2026-09-29.
- Liquidity lock: DEX Screener's listing includes a tonraffles lock link (https://tonraffles.app/lock/EQDv6cYW9nNiKjN3Nwl8D6ABjUiH1gYfWVGZhfP7-9tZskTO, page returns 200), which implies an LP lock exists, but the lock terms are inside a JS app and could not be read. Unproven (lock existence implied by listing metadata; terms unverified).
- A "yieldo.me" token calculator page includes GSTD in an auto-scraped token list. Supported (barely: scraper artifact, not a listing). Source: search result surfaced via WebSearch, https://yieldo.me.

## 3. Team and narrative

- Team is anonymous. No names, photos, or legal entity anywhere on gstdtoken.com. Supported. Source: https://gstdtoken.com (fetched 2026-09-29).
- Public handles all read as the same small operation: GitHub user `gstdcoin` (bio "Open AI Compute Network", account created 2013-08-21, i.e. an aged account repurposed for this project; 6 followers, 9 public repos), X `@gstdtoken`, Telegram `@gstdtoken` and `@goldstandardcoin`. Committer identities in the repos are "GSTD Dev", "GSTD Coin", "GSTD Cleanup", "GSTD Pi Node" (same-person-appearing aliases, no other human contributors visible). Supported. Sources: https://api.github.com/users/gstdcoin, https://api.github.com/users/gstdcoin/repos, per-repo commit fetches 2026-09-29.
- X profile: "Gold Standard" (@gstdtoken), bio "Decentralized AI Compute & Fine-Tuning Network", 562 followers, 588 posts, joined November 2024. Recent posts: Jun 5 2026 (Solana/Ripple tag), May 25 (#GSTD #TON #DePIN), Mar 22 (Node-as-a-Service), Mar 3 (bot beta). Activity visibly thins after June 2026. Supported. Source: https://x.com/gstdtoken (rendered without login, 2026-09-29).
- Telegram: @gstdtoken 232 members; sibling channel @goldstandardcoin 142 subscribers. Both channels carry the identical description "Computational clarity, network reliability. Physical reserves protect system responsibility. GSTD powers verified distributed computation." The gold channel's recent content includes a chain diagram "GSTD - TON - UTILITY - SOLANA - XRPL - BRIDGE - COMMODITY - GOLD", a "GSDT DePIN & Gold Reserve (Q1 2026)" status post (note their own GSDT typo), "Node-as-a-Service" with a "Matryoshka" architecture, an AI hackathon submission link, and a beta announcement for @GstdAppBot (a bot the project's own web repo commit replaced with @gstdaibot on 2026-08-30, i.e. the channel promotes a stale bot). Post views run roughly 199 to 651. Supported. Sources: https://t.me/s/gstdtoken, https://t.me/s/goldstandardcoin (fetched 2026-09-29), https://api.github.com/repos/gstdcoin/web/commits.
- Narrative is genuinely split: the site and GitHub say decentralized AI compute (DePIN), the on-chain jetton metadata and the gold channel say tokenized gold with physical reserves. The site itself states the gold-reserve treasury contract is "written but not deployed" and that GSTD is not backed by reserves. Supported. Sources: https://gstdtoken.com, tonapi metadata, https://t.me/s/goldstandardcoin.
- The site (Russian language) is candid about defects: no audit ("Аудита не было"), Solana/XRPL bridges have no working vault, no cryptographic proof of correct computation yet, hardware reward tiers (Spark/Flame/Storm/Titan/Sovereign), 85/10/5 fee split via SettlementMaster, one-line node install via curl from raw.githubusercontent. Supported. Source: https://gstdtoken.com.
- Docs hub exists at https://gstdtoken.com/docs in Russian, sections: Обзор, Архитектура, Нода, Вычисления, Инференс, Платежи, Вознаграждения, Верификация, Казна, Токен, Безопасность, API, Разработчикам, FAQ. No whitepaper found anywhere. Supported (docs exist; whitepaper absent). Source: https://gstdtoken.com/docs.

## 4. Reputation surface

- No scam alerts, rug flags, regulator warnings, audit reports, or exchange listings/delistings found for this GSTD in search. Multiple search attempts partially failed on rate limits (429s recorded below), so this is absence of evidence from a degraded instrument. Unproven (no flags found; coverage itself is near zero).
- Risk signals that are byte-backed: 67.98 percent of supply in 10 addresses, $10.4k liquidity, $1.26 daily volume, anonymous team, no audit (self-admitted), gold narrative in metadata that the site itself disclaims. Supported. Sources: tonapi, dexscreener, gstdtoken.com as cited above.
- Mitigating facts the project published itself: jetton mintable is false (admin mint disabled), the bridges are labeled non-functional rather than sold as working, the site carries utility-token-not-investment language. Supported. Sources: tonapi, https://gstdtoken.com.

## 5. The dark-front-door question

- app.gstdtoken.com is now FULLY dark: root returns Vercel "DEPLOYMENT_NOT_FOUND" (HTTP 404, deployment id yul1::mjhrw-1790690478057). This is worse than the 2026-09-18 T0 probe (alive shell, 404 API paths): the Vercel deployment has since been deleted. Supported. Source: curl https://app.gstdtoken.com/ 2026-09-29.
- A DIFFERENT backend is alive: platform.gstdtoken.com, a Cloudflare-fronted JSON API. `/health` and `/api/v1/health` return 200 with body `{"status":"ok","service":"gstd-platform"}`. Supported. Source: curl 2026-09-29.
- The project's own commit messages confirm the migration and the death of the old door: A2A repo commit "fix: replace app.gstdtoken.com with platform.gstdtoken.com across all files" (2026-08-28), contracts repo commit "fix: settle-rewards.ts PLATFORM_API - platform.gstdtoken.com" (2026-08-30), web repo commit "fix: app/monitor - platform.gstdtoken.com (not dead Vercel)" (2026-08-30, their own words "not dead Vercel"). Supported. Source: https://api.github.com/repos/gstdcoin/{A2A,contracts,web}/commits.
- `/api/v1/nodes` is open and returns a LIVE node registry, 4 nodes, seen as recently as 2026-09-28 08:47 UTC (yesterday):
  - "GSTD Bootstrap Pi": wallet UQB03R2DuNR9LKkW1AxbWUDsegAjxCRVwRimZlyNQX2Gc8ve, node_url https://myspace-kurt-furniture-twice.trycloudflare.com, capability llama3.2:3b, Debian trixie, 168 tasks completed, 32.348 GSTD earned lifetime, avg response 40,942 ms, registered 2026-08-28, last seen 2026-09-18.
  - "node-LAPTOP-UTO92FB9" (an operator laptop hostname): registered 2026-09-18, last seen 2026-09-28, 0 tasks, 0.464 GSTD earned.
  - "localhost-node": qwen2.5:7b, last seen 2026-09-13, 0.344 GSTD earned.
  - "unknown": version field "24.04.4 LTS (Noble Numbat)" (an OS string, not a node version), last seen 2026-09-22, 0 earned.
  Total lifetime GSTD earned by the entire visible network: 33.157 GSTD, about $0.0019 at the current price. Supported. Source: curl https://platform.gstdtoken.com/api/v1/nodes 2026-09-29.
- The Bootstrap Pi's tunnel URL matches, byte for byte, the "Update seed peer URL" commits pushed to the ai repo by committer "GSTD Pi Node" on 2026-09-15. The node registry publicly ties the live backend to the same hands that push the repos. Supported. Sources: /api/v1/nodes response, https://api.github.com/repos/gstdcoin/ai/commits.
- So: the gateway/settlement backend is LIVE and serving real nodes, while the branded front door is deleted and the market is dormant. The answer to "brochure or backend" is: backend alive, brochure dead. Supported.

## 6. Repo activity (public GitHub view)

- Account: user `gstdcoin` (not an org; api.github.com/orgs/gstdcoin returns 404, users endpoint works), created 2013-08-21, 9 public repos, 6 followers, twitter_username gstdtoken. Supported. Source: https://api.github.com/users/gstdcoin, /users/gstdcoin/repos.
- Repos with created/pushed dates (all UTC, all non-archived, forks 0 across the board):
  - web (TypeScript): created 2025-09-15, pushed 2026-08-30, 1 star.
  - ai (TypeScript): created 2025-12-27, pushed 2026-09-15, 1 star. Last commits are seed-peer tunnel URL updates by "GSTD Pi Node".
  - A2A (Python): created 2026-02-02, pushed 2026-08-28, 2 stars.
  - gstdbot (TypeScript): created 2026-02-28, pushed 2026-09-01, 1 star. Last commits add an npm MCP package for "MCP Registry submission".
  - contracts (TypeScript): created 2026-03-03, pushed 2026-08-30, 1 star. Last commits: ClaimUptime voucher claim in SettlementMaster, gas bumps.
  - gstd-bridge (Rust): created 2026-03-13, pushed 2026-08-26, 1 star. Notable commit: "Strip fake MPC aggregation, forgeable votes, and fabricated withdrawal tx hashes" (2026-08-13), an in-repo admission that earlier code faked things.
  - awesome-mcp-servers, awesome-mcp-servers-1, awesome-mcp-servers-2: three forks created within one minute (2026-09-01 19:22-19:23 UTC, pushed 19:33), 0 stars, classic visibility-farming fork pattern.
  Supported. Source: https://api.github.com/users/gstdcoin/repos?per_page=100 and per-repo /commits fetches, 2026-09-29.
- Contributors: commit author aliases "GSTD Dev", "GSTD Coin", "GSTD Cleanup", "GSTD Pi Node" across repos; no external contributor commits surfaced in latest-commit sampling. Stars: 0 to 2 per repo. Forks: 0. Supported. Source: same fetches.
- npm: package `gstd-network-mcp` v1.0.0 published (author gstdcoin, Apache-2.0, points back to github.com/gstdcoin/gstdbot), marketing copy: "Run Llama 3, Mistral, CodeLlama, Qwen, DeepSeek and 50+ open-source models for free, no API key." Supported. Source: https://registry.npmjs.org/gstd-network-mcp.

## 7. Comparative existence check

- Invisible to aggregators: no CoinGecko entry, no CoinMarketCap page (404), no presence found in DePIN lists (CryptoTotem, DePINscan, awesome-depin) or TON ecosystem maps in searches. Supported (absence in checked surfaces). Sources: coingecko search API (empty), CMC 404, WebSearch queries 2026-09-29 (partially rate-limited, see failure log).
- The only third-party surfaces that mention it are auto-scrapers (yieldo.me token calculator) and its own self-seeded entries: an identityhub.app AI-hackathon listing carrying the exact Telegram description text ("Gold Standard. Computational clarity..." at https://identityhub.app/contests/ai-hackathon; the entry list itself would not render without JS, so submission details are Unproven), plus the #GSTDGrid hashtag with a single post. Supported (self-seeded), Unproven (hackathon participation details).
- A GitHub search hit independently shows the ai repo README marketed via the app subdomain. Supported. Source: WebSearch result for github.com/gstdcoin/ai.

## Failure log (attempts that returned nothing)

- WebSearch: multiple queries hit upstream 429 rate limits ("GSTD gstdcoin token" fully failed; several scam-check variants partially failed). Recorded as degraded evidence for the empty scam-flag finding.
- https://identityhub.app/contests/ai-hackathon: entry list is JS-rendered; project details not readable. Unproven.
- https://tonraffles.app/lock/EQDv6cYW9nNiKjN3Nwl8D6ABjUiH1gYfWVGZhfP7-9tZskTO: page 200 but lock terms JS-rendered; not readable. Unproven.
- X post bodies beyond profile metadata require login; post-level verification limited to what the profile page rendered.
- api.coinmarketcap.com/data-api search endpoint returned a 404 HTML page (instrument failed); CMC absence was instead established via the /currencies/gstd/ 404.

---

## PUBLIC VS CLONE DELTA

Where the public story is THINNER than the cloned codebase: the market. The cloned repos describe a sovereign-agent state machine with slash economics, buyback-and-burn, escrow and DAO; the public world using it is 4 nodes (3 of which are operator-adjacent: a laptop hostname, localhost, and the project's own Bootstrap Pi), 206 holders, 67.98 percent supply in 10 wallets, $10.4k of liquidity, $1.26 of daily volume, 232 Telegram members, and a lifetime network payout of 33.157 GSTD, roughly a fifth of a cent. The code promises a swarm; the registry shows one developer's devices talking to themselves.

Where the public story is THICKER than the local probe assumed: the backend. The 09-18 T0 probe found a dark front door and read that as decay. The public side shows the operation migrated, not died: platform.gstdtoken.com is a live settlement API (health OK, node registry open, nodes seen 2026-09-28), commits explicitly migrated all clients off the dead Vercel app in late August 2026, and development continued through 2026-09-15. The operation is alive and maintaining itself; only its storefront is gone.

Narrative layering (camouflage-relevant): one jetton carries three stories. On-chain metadata: tokenized gold. Telegram sibling channel: physical reserves and a gold-bridge commodity chain, plus a "Gold Reserve (Q1 2026)" promise. Site and GitHub: decentralized AI compute DePIN network. The site itself admits the gold treasury is not deployed and the bridges have no working vault. The gold story is the marketing skin; the AI compute story is the code reality; the on-chain reality is a $56k micro-cap with $10k of float.

Observations of image management: the gstd-bridge repo publicly deleted its own fake mechanisms ("fake MPC aggregation, forgeable votes, fabricated withdrawal tx hashes"), which is unusual candor, and simultaneously the account forked awesome-mcp-servers three times in one minute to farm visibility, and the npm MCP package advertises "50+ models for free, no API key", which the node registry contradicts (one Pi, one model capability listed, 41-second average responses).

## VERDICT on the camo hypothesis (public side alone)

The operator's thesis is that the pay/grift layer is camouflage over a more developed operation. From the public footprint, the thesis half-holds, with the polarity inverted from what a scam-hunt reading would predict. The developed operation is real: a live, Cloudflare-fronted settlement platform with an open node registry, recent continuous development, working TON settlement contracts being tuned in commits, and an honest self-documenting site. What is camouflage is not the grift covering the operation; it is the SCALE. The public surface is engineered to look both bigger and smaller than it is: bigger via the gold-reserve narrative, the 50+ models npm pitch, triple MCP-list forks, and DePIN hashtags; smaller via the candid disclaimers, deleted storefront, and near-zero market, which together keep the operation below the radar a $10k-liquidity token would normally attract. The single decisive public fact is the node registry: the entire "sovereign swarm" publicly resolves to four nodes, three of them the operator's own hardware, with a lifetime economy of 33 GSTD (about two tenths of a cent). That is not a hidden empire; it is a real but tiny single-operator (or very-small-team) machine whose elaborate agent-state codebase outruns its world by several orders of magnitude. Camo as plausible deniability: supported (gold skin over compute reality, self-documented). Camo as concealment of a large developed operation: unproven, and the public numbers argue against it. The local clone forensics and this public footprint now agree on the same object from both sides: a serious, live, self-aware micro-operation wearing two marketing stories over one dormant micro-cap jetton.
