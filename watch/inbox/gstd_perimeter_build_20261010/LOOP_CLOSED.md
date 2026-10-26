# GB PERIMETER: THE LOOP CLOSED (2026-10-10/11 night, operator "Let's go")

GB's three asks, proven tonight on the estate's own hardware and GB's own contract:

1. "Different models generate a consensus answer" - consensus run
   consensus-20261011T000937Z: 5 heterogeneous models, 13 tasks, 8 distinct truths,
   consensus 69.23 pct vs dead-salmon null 25.5 pct = STRUCTURE verdict. Dates 5/5
   consensus AND 5/5 correct.
2. "Verification that the network will pay rewards to participants" - THREE real
   settlements through GB's own SettlementMaster on TON testnet
   (EQBRH9yC6trjOlLzOUuUIRJye7yxaEHf2diiDZQndncMekMw), one per device wallet,
   task ids 53001001101-103, deployer seqno confirmed x3.
3. "The network should learn on its own" - the consensus ledger accumulates per
   model per shape; every run banks rows (GPS-importable).

## THE PAYOUT ASSERTION (chain state, read from the chain)

| wallet | address (UQ, non-bounceable) | balance after |
|---|---|---|
| DESKTOP | UQBX4TEs0dCvV7CzDpUmj04niFPVd0jjbCfhquO8dPxxa3BJ | 0.899132488 TON |
| BOB | UQAW3wO8TwzoBuOjA-XwCivj80eKhRzGAWl_PgkzUUUlbe5m | 0.899132488 TON |
| T90 | UQBrE6BRPvZkBH47rHGfL7TmepeakX--unodq9I_K6f7BA3p | 0.899132488 TON |

Worker share = 85 pct of the 1.0 TON settle value (0.85) + 0.049 deploy stake -
receive fees = 0.899132488 each, identical, exactly as the contract's split
computes. Treasury got 10 pct, protocolFee 5 pct. Mnemonics: contracts/.env only
(gitignored, never printed - the key law held through the whole leg).

## The bug the probe caught (honest)

First settle round: all three payments BOUNCED - device wallets had keypairs but
no deployed contract code, and SettlementMaster's WorkerPayment is bounce:true,
which bounces off uninitialized accounts. Caught by reading chain state (the
instrument working as designed: nonexist status, zero tx). Cured by internal
deploy transfers from the deployer carrying each wallet's state_init (the
external-deploy route 500s on toncenter). Second settle round: confirmed x3,
balances landed. The perimeter's own probe found and fixed the failure before
any human asked.

## Infra state after tonight

- Tailscale perimeter: desktop 100.96.161.76 (models, live), bob 100.125.103.60,
  t90 tablet 100.72.38.3, pixel phone (joins on Termux install).
- Ollama serving on 0.0.0.0:11434, tailnet-reachable (firewall rule scoped to
  100.64/10 pending the operator's UAC click).
- Contracts (testnet, estate-deployed 10-07): Jetton, SettlementMaster,
  TreasuryGold, DAOVoting, AgentRegistry - all live addresses in
  deployment-testnet.json.
- New organs tonight: gen_perimeter_wallets.js, deploy_perimeter_wallets*.js,
  the settle-task rail exercised end to end.
- Dogfood receipts: MagNightCrew drained the swarm self-steal batch; gap-analysis
  on the event-substrate thesis riding; smith-chart series designed.

## What is still honest-not-done

- Jetton bonus leg: gstdBonusAmount sent 0 (SettlementMaster's jetton pool
  unfunded); the TON payment leg is proven, the GSTD bonus leg is the next rung
  (fund the master's jetton wallet from the testnet premint).
- Cross-device consensus RUNNERS: t90/bob hold payment identities; their harness
  executions wait on python/Termux installs (the coldest-vertex law says the
  phone run is the final proof of portability).
- The wallet law note: these are TESTNET-ONLY keys, zero real value, burnable.

## Falsifier

The claim "the network pays" dies if the balances above cannot be re-read from
the chain by an independent party (addresses are public; toncenter testnet is
the arbiter). The claim "different models reach consensus" dies if the
dead-salmon control ever matches the live rate on the banked runs.

## FUNDING LEG (2026-10-11, operator "Fund it"): the v2 stack

Findings that forced it (both real perimeter products):
1. v1 jetton: premint block commented out in the deploy script, mintAuthority
   locked to SettlementMaster, and SettlementMaster has no mint leg = zero
   testnet GSTD could ever exist. Caught by the funding attempt itself.
2. v1 SettlementMaster predates the ownJettonWallet feature (stale build vs
   .tact source): it cannot hold a jetton pool at all.

Deployed tonight (all testnet, public):
- Jetton v2: EQCgvt0MRmJPl-zQ8rZaPXpQnQgDQMQ_21plPSeYF4-zSAf0
- SettlementMaster v2: EQCfxtmiNx-D5kYFy2xWqlEIYYeU3hMpwY9fRo3ROaiKxF86
- Allocation: DESKTOP 100M GSTD (team), BOB 100M (liquidity), deployer 199M
  (ecosystem, after 2M to pools) - read from chain via tonapi.
- Pool: SettlementMaster v2's jetton wallet holds 2,000,000 GSTD (on-chain
  getter read; both funding transfers landed there).

## Leg status

- TON payment leg: PROVEN x2 rounds (0.899 then 0.909/0.994/0.984 across the
  three device wallets, chain-read).
- GSTD allocation leg: PROVEN (100M per device wallet on chain).
- GSTD bonus transfer leg: OPEN - settles confirm, TON splits pay, but the
  25 GSTD bonus does not reach the worker's jetton wallet with the pool
  funded (2M on-chain). Isolated to the deployed contract's bonus transfer
  gas margin (hardcoded 0.12 TON on the TEP-74 send, SendIgnoreErrors =
  silent loss if the worker jetton wallet deploy costs more). This is a
  GB-side contract parameter - the perimeter's first production finding
  FOR the contract, exactly what a closed perimeter is for.
- Deployer gas discipline: the treasury rebalanced itself mid-test (DESKTOP
  sent 0.4 TON back to the deployer) - the estate pays its own gas.
