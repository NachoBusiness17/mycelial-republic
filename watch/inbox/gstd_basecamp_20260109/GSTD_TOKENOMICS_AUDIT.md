# GSTD TOKENOMICS + NETWORK AUDIT - Lane B - 2026-10-09

Instruments: gstdbot @ e0bbe48 + contracts/ (READ-ONLY clone), live platform GETs
(data moment 2026-10-09T05:03:47Z, /api/v1/nodes last_seen pins currency; the
earlier roster read carried last_seen 04:35:24Z per PLATFORM_SURFACE_MAP.md),
our dogfood receipts (DOGFOOD_DATA.md). Platform Workers code is NOT public:
every platform-side mechanism is marked unobservable. SPECULATION labels mark
anything not byte-backed.

## 1. The money's physics (code sites)

Emission lanes (what can create GSTD):
- On-chain: GSTDJetton.tact mint gate - only mintAuthority (the Settlement
  contract) may mint (GSTDJetton.tact:120), hard caps maxSupply 1B (:107) and
  workerPoolMax 400M (:111,:123), plus a one-time pre-mint of up to 600M for
  team/IDO/liquidity/advisors (:44-53): 60% allocation, 40% worker pool.
- Live economy: gstd_earned is a platform D1 counter (comment platform-link.ts:
  246), not an observable chain balance. Whether the platform mints per payout
  is unobservable; node-side "settlement theater" exists: token.ts:387-396
  fabricates hash 'tx_'+randomBytes with status 'confirmed', /api/rewards/claim
  fabricates txHash 'tx_'+sha256 (server.ts:3305), and the revenue engine's
  header promises SettlementRouter.tact settlement (engine.ts:15) while
  containing zero chain-call code (grep: no TonClient/send in engine.ts).

Payout math sites:
- Task payouts: platform-side, unobservable. Observed brackets: +0.002 for a
  36-char kill-test task (DOGFOOD_DATA.md sec 5, task-1791520415505-p9o8x4,
  completed 04:33:40Z) and mean 0.0095/task over our next 12 tasks
  ((0.143056-0.029056)/12, nodes API reads 04:34Z to 05:00:18Z). Contract
  shape: baseRate 0.001 GSTD per compute unit, bonus capped at baseRate x computeUnits (SettlementMaster.tact:110,
  152-154), split 85/10/5 worker/treasury/protocol (:106-108).
- Uptime rewards: granted BY the platform in the heartbeat response
  (platform-link.ts:202-203); our observed rate +0.000083 GSTD per 600s beat
  (docker logs, PLATFORM_SURFACE_MAP.md sec 5) = 0.000498 GSTD/h. Rate formula
  unobservable.
- Other rate tables are LOCAL DISPLAY ONLY, never wired to money: FeeLedger
  0.001/query 90/10 split (fees/ledger.ts:27-39, wired only to the local
  Ollama passthrough at server.ts:703), revenue engine DEFAULT_RATES
  (engine.ts:34-40), dashboard program bronze 0.5 to diamond 2.5 GSTD/h
  (dashboard/server.ts:304-308) - marketed program ~1000x our uptime floor.

SEAL VERDICT: ASPIRATIONAL in the live path. The seal "supply grows only with
verified work" (state/gstd/genesis.json) has NO enforcement site that verifies
work. The chain enforces authority (only Settlement mints, GSTDJetton.tact:
120; only DAO/gateway settles, SettlementMaster.tact:129) - i.e. supply grows
when the GATEWAY says so: SettleTask takes workerAddr, gstdBonusAmount,
computeUnits, qualityScore as trusted message fields (SettlementMaster.tact:
16-22, 128-135); only replay is guarded (:134). Worse, the quorum-verification
contract method the node code targets does not exist in the repo's contracts:
attestation.ts:2-3 says signatures "MUST exactly match SettlementMaster.tact's
verifyQuorum()", agent.ts:694 and p2p/node.ts:128 reference SettleTaskWithProof
- grep of contracts/ for either name returns ZERO hits (2026-10-09). The signed
lane points at a phantom method; the deployed SettleTask trusts one address.

## 2. Live economy cross-check (same regime? NO)

Live roster at 05:03:47Z (5 nodes): network lifetime gstd_earned sums to
56.6955 GSTD = $0.0029 at the live feed (/api/v1/market/price 200 same moment:
gstd_price_usd 0.0000514607, gstd_price_ton 0, source ston.fi - a USD number
with zero TON-pair depth is a thin-or-stub pool; SPECULATION).

| metric | Pi (their bootstrap) | us (gstd-desktop) |
|---|---|---|
| per-task mean, lifetime | 51.4735/288 = 0.1787 GSTD | (0.143056-0.029056)/12 = 0.0095 GSTD |
| idle accrual | +0.0359 over 1703s, 0 tasks (data moments 04:35:24Z to 05:03:47Z) = 0.0758/h | uptime floor 0.000498/h (docker logs) |
| avg_response_ms | 34536 | 6162 (was 1698 at 04:35:24Z) |

- The 19x per-task gap is consistent with size-scaled pay (Pi tasks ~34.5s vs
  our 1.7-6.2s work units) plus era effects; both carry early_adopter:1. Payout
  formula unobservable; era-multiplier part is SPECULATION.
- Idle accrual is NOT one regime: Pi idles at 0.0758/h while our heartbeat pays
  0.000498/h (152x). Zero-task historical nodes imply 0.0109/h (LAPTOP-UTO92FB9,
  4.7346 GSTD over 434.4h registered-to-last_seen) and 0.00128/h (localhost-
  node, 0.3444 over 268.6h) - assumes continuous heartbeats, SPECULATION. Some
  scaler (age/reputation/era) exists platform-side; it is not published.- reputation_score pays/gates nothing observable: ours moved 51 -> 59 on 8
  completions (DOGFOOD_DATA.md sec 5) then DECAYED to 49 by the 05:03:47Z read
  with 5 more tasks done; gstdai.ts:918 markets "higher reputation = more
  tasks routed" but we won 100% of poll races at 49-59. /api/node/rating
  (server.ts: 4459-4482: models 48 + activity 32 + uptime 20; silver >= 40 at
  1.5x) is pure local display: no consumer of its multiplier in any payout
  path (grep, src/ 2026-10-09).
- Network emission burn: ~56.7 GSTD over ~37 days of network life (earliest
  registration 2026-09-02) = ~1.53 GSTD/day network-wide; the 400M pool is not
  the binding constraint at that rate - demand is.

## 3. Stress test of the value thesis (distribution = value)

What ACCRUES as nodes/tasks grow (mechanism cited):
- Nothing observable. The only designed sinks are the 10% treasury and 5%
  buyback-and-burn of TON value through SettlementMaster (:143-190) - but live
  settlement rides D1 counters (sec 1). Fee income 0.001 GSTD/task submit
  (DOGFOOD_DATA.md sec 5) vs payouts 0.002-0.0095/task: every task is net
  emission subsidy of 2-10x revenue; uptime rewards have no fee counterparty.
  More nodes = more pool drain, zero added sink.
- What DOES accrue to the operator: the gateway wallet UQB03R2DuNR9... is the
  same address as the top-earning node "GSTD Bootstrap Pi" (nodes API 05:03:47Z
  vs deployment-mainnet.json gateway field) - 51.4735 of 56.6955 visible GSTD =
  91% of all emissions went to the operator's own node/gateway address.

What does NOT accrue (the leaks):
- Unsigned settlement: production lanes submit no signature (Lane A finding 12;
  push server.ts:4604-4617, poll platform-link.ts:287-297), so "work" behind a
  payout is unverifiable by anyone including the chain.
- Auth-by-address: /api/wallet/claim forwards only X-Wallet-Address
  (server.ts:2511-2534) - earnings custody reduces to knowing a string.
- Reputation opacity: no published formula (Lane A (b)); our own score moved
  59 -> 49 while earning - payouts on an opaque score are faith.

Honest failure modes: cold demand (post-dogfood external traffic was ~5 small
tasks in ~20 min, reads 04:40Z to 05:00:18Z; our dogfood was the platform's
biggest demand event); single-gateway dependency (one gateway address settles
everything, SettlementMaster.tact:129, and it is the operator's Pi wallet;
phase2_todo in deployment-mainnet.json shows SettlementMaster.owner is STILL
the admin address, DAO transfer not done, deployed 2026-07-08); and the
403/402-class kill switch: the platform can silence any node's earning at will
(DEPLOYMENT_DISABLED 402 stops heartbeats, platform-link.ts:131-137, 189-196)
while baked PLATFORM_PUBKEY_HEX lets it remote-command every node
(platform-auth.ts:5-10; Lane A (e)) - the same central-token-holder-cut-off
class as the fine-grained PAT 403s we hit filing upstream PRs (UPSTREAM_PRS.md:
6, 92). A fork inherits the crown or breaks.

## 4. Our-needs ledger (constitution Art 15, fork equality, two-tier data)

| republic need | GSTD today | verdict |
|---|---|---|
| Verifiable work-minting (unit = signed receipt with proof-of-cost) | Signed quorum lane exists (agent.ts:989-1010, attestation.ts) but off the production path; target contract method verifyQuorum/SettleTaskWithProof absent from contracts/ (grep zero); deployed SettleTask trusts gateway fields (SettlementMaster.tact:128-135) | GAP (machinery sketched, enforcement absent) |
| Offline two-tier settlement | Offline = standalone chatbot, no earning (platform-link.ts:131-137, 189-196); report/quorum retry queues exist (agent.ts:789-871) but no task acquisition or local ledger replay offline | PARTIAL (queues only, no settlement) |
| Per-device identity (fresh wallet per device, key possession) | Identity is knowable strings: X-Wallet-Address + X-Node-Id headers (platform-link.ts:107-112, 162-168); node_pubkey registered (platform-link.ts:120) but never verified at completion; seed encrypted under machine-derived key (Lane A finding 10, wallet.ts:42-52) | GAP (address-as-auth, keys not load-bearing) |
| Fork-equality (no throne, no core mirror) | 88 hardcoded gstdtoken.com refs, 7 with no env override (Lane A (e)); PLATFORM_PUBKEY_HEX baked per release (platform-auth.ts:5-10); gateway + owner are single operator addresses (deployment-mainnet.json) | GAP (fork inherits or breaks) |
| Capped, replay-guarded emission | maxSupply 1B + worker pool 400M + once-only taskId (GSTDJetton.tact:107-123, SettlementMaster.tact:134) - real, at contract level; live payouts ride D1 counters instead | PARTIAL (chain-grade caps, unobservable live use) |
| Permissionless read of the ledger | /api/v1/nodes + /market/price public and honest (this audit's instruments) | MET (for the counter, not for chain proof) |

Top unmet need: settlement-grade verifiable work-minting - the one thing the
seal promises and nothing enforces.

Sources: this dir (AUDIT_PLAN, GSTD_CODEBASE_AUDIT, DOGFOOD_DATA,
PLATFORM_SURFACE_MAP, UPSTREAM_PRS), reference/gstdcoin/gstdbot @ e0bbe48,
reference/gstdcoin/contracts (deployment-mainnet.json), live GETs
platform.gstdtoken.com /api/v1/nodes + /nodes/leaderboard + /market/price
(data moment 2026-10-09T05:03:47Z), state/gstd/genesis.json seal text.
