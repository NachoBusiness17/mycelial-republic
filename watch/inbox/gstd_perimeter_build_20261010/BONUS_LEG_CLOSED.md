# GSTD BONUS LEG CLOSED - 2026-10-11 20:0x-21:5x ET (operator: "let's build our gstd and move")

**Verdict: the perimeter is complete end to end.** SettleTask taskId 53001101506 through SettlementMaster v3: TON splits paid, and the 25 GSTD bonus landed on DESKTOP's jetton wallet, first poll. Balance-reader law held: DESKTOP jetton 100,000,000 to 100,000,025 GSTD, pool 100,000 to 99,975 (getter reads, never txHash).

## v3 stack (all testnet, estate-deployed)

- SettlementMaster v3: EQBaW5BqIePGNstaJI8ECwoTMju_e6Ta-4NNrAlwfScYnePI
- v3 pool wallet: EQC8sX8b0880babuX31KcOC6W6uukg4TJXgbsHhpT-Gry2O7 (99,975 GSTD)
- Jetton v2 unchanged: EQCgvt0MRmJPl-zQ8rZaPXpQnQgDQMQ_21plPSeYF4-zSAf0
- baseRate on v3: 1e9 nano (1 GSTD per CU), set at deploy
- New scripts: deploy-settle-v3.ts, fund-v3.ts, bonus-v3.ts, set-base-rate-v2.ts, read-v3.ts, rebalance-bob.ts, print-wallet-addresses.ts

## The root-cause chain (three stacked bugs; the first report had one, wrong)

**Bug 1 - the baseRate cap (real, fixed on v2 and v3).** Deployed init: baseRate = 1,000,000 nanoGSTD per CU = 0.001 GSTD/CU (SettlementMaster.tact init). The settle path caps: maxAllowedBonus = baseRate x computeUnits, applied silently before the send. A 25 GSTD bonus with computeUnits 25 becomes 0.025 GSTD; the rail sends computeUnits 1, capping any bonus at 0.001 GSTD. No real bonus survives the default. Fix: SetBaseRate 1e9 (admin message, owner = deployer, no redeploy) - live-verified on v2 by getter, then set at v3 deploy. The original gas theory was WRONG; the cap alone explains "bonus never arrives."

**Bug 2 - the opcode mismatch (the killer after the cap was fixed).** The master hand-built the bonus body with the TEP-74 standard op 0xf8a7ea5 (2507683173). But GSTDJetton.tact declares `message Transfer` with no explicit opcode, so tact assigned its generated header: **1435380091** (GSTDJettonWallet.abi, both master and wallet ABIs agree). The pool wallet received three bonus transfers wearing 2507683173, matched no receiver, and tact silently ignored each: out_msgs 0, funds retained, no bounce. Byte-proof: pool wallet transactions show three accepts with zero outbound. Proof of the fix: v3 (rebuilt with storeUint(1435380091, 32)) lands the bonus on the first poll. Why the funding transfers always worked: they went through the tact TS wrapper ($$type Transfer), which serializes the generated header.

**Bug 3 - gas margin (real, hardening only, never the killer).** 0.12 TON on the TEP-74 send was too thin for a worker-wallet deploy; v3 uses 0.15. Kept SendIgnoreErrors as shipped - note for GB: with a wrong opcode SendIgnoreErrors turns any failure into total silence; bounce or a notify-on-fail would have surfaced this bug months earlier.

## GB gift, rewritten (replaces the "hardcoded gas" line in the message)

Three findings for your contract, all reproduced on your own testnet stack: (1) the SetBaseRate default (0.001 GSTD/CU) caps every real bonus to dust - set the rate at deploy; (2) your jetton wallet's Transfer receiver compiles to tact header 1435380091, not the TEP-74 standard 0xf8a7ea5, so any external wallet or contract sending a standard TEP-74 transfer is silently ignored - declare message(0xf8a7ea5) Transfer in GSTDJetton.tact and the wallet becomes actually compliant (one line, needs jetton migration); (3) the 0.12 bonus gas is thin if a worker wallet deploy rides the transfer - 0.15 clears it. We deployed the corrected master as v3 and the bonus lands first poll.

## Ops laws learned tonight (perimeter addendum)

1. Balance-gate before every send: a TON wallet silently DROPS external messages whose value plus fees exceed its balance - no error reaches the caller. The deployer was drained twice (0.0429, then 0.09); every "mystery failure" in the middle of the night was a dropped external. Cure: read balance, gate, then send; rebalance from device wallets (DESKTOP 0.4, then BOB 0.5 when DESKTOP hit its own floor at 0.33).
2. One trusted reader: the mnemonic-derived ts reader (toncenter via @ton/ton). A python toncenter getAddressInformation read on a UQ-form string returned a ghost balance (13.58 TON that does not exist). Cross-check instruments before believing a number.
3. Seqno gates between sequential fires, now including the funding step: the deploy script's own funding send was dropped in the deploy window - standalone scripts per step, read-confirm between.

## Falsifier

"Bonus leg proven" dies if DESKTOP's v2-jetton wallet getter stops reading 100,000,025 GSTD, if the v3 pool getter stops reading 99,975, or if a fresh settle to a cold (undeployed) worker wallet fails - the last one is exactly what the 0.15 gas fix claims to handle and should be the next probe.
