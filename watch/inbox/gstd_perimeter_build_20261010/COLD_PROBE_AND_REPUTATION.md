# COLD-WORKER PROBE + PHASE 4 BABYSTEP 2 - 2026-10-11 late night (closed)

**Cold-worker probe: PASSED at 0.3 TON bonus gas.** A NEVER-DEPLOYED worker wallet (key discarded at generation, receive-only) received a settle at taskId 53001101602: the master's bonus send **deployed the worker's jetton wallet inside the TEP-74 transfer and landed exactly 25 GSTD, first poll.** The TON worker share bounced off the uninitialized account by design (bounce:true) - the probe measures the jetton leg, which is the one the fixes changed.

**The honest arc of this probe (three failures, each a different real lesson):**

1. **0.15 TON build: FAILED.** Worker jetton wallet undeployed after 4 min. At the time I read this as "0.15 too thin" - half right, and the deeper cause was hiding underneath.
2. **0.3 TON build, first probe: self-refunded.** The whole SettleTask bounced back to the deployer (0.1996 of 0.2) - because I reused taskId 53001101600 and the contract has **replay protection**: a settled taskId refunds the caller. New lesson: taskIds are single-use; the probe needed a fresh one. (Also the receipted finding: replay protection exists and works - good news for payout design, worth telling GB.)
3. **Root cause of failure #1 found in the same trace: the deploy script's SetOwnJettonWallet message was DROPPED in the deploy window** (fired blind in the same seqno/balance storm as the deploy messages, the ops law biting the deploy script itself). With ownJettonWallet == zero address, the master skips the bonus branch ENTIRELY - no message, no error, consistent with everything seen. Sent SetOwnJettonWallet standalone (scripts/set-pool-v4.ts), re-probed with a fresh taskId: PASSED first poll.

**Gas truth table (probe receipts):** 0.12 (shipped): unknown-never-reached (cap+opcode bugs upstream). 0.15: warm workers proven, cold workers FAIL. 0.3: cold workers PROVEN. GB's fix note upgrades to: "0.3 TON on the bonus send, or two-phase settle (deploy wallets, then bonus) - receipted both ways."

**Phase 4 babystep 2 - the reputation ledger exists:** reference/gstdcoin/contracts/reputation.jsonl - one row per settle (taskId, node, wallet, kind, verdict rates, worker delta, polls-to-land, verified-by). Seeded with the three proven settles (bonus close, consensus-certified settle, cold-worker deploy). Every future settle appends here; per-node reputation = reading the ledger. This is the roadmap's "node reputation" organ at babystep scale: a file before a getter, a getter before a contract.

**Remaining honest gaps:** bob/t90 remote harness runs blocked on manual bootstrap - bob needs estate_to_bob.pub added to his authorized_keys (one line, SSH port 22 is open and the keypair exists; estate keypair verified matching for all three device wallets), t90 has no door (Termux + sshd later). The GB PR set (tact diff + three findings + the bridge script) is staged as the next rung.

## Falsifier

The cold-worker claim dies if a fresh undeployed wallet settles to zero GSTD, or if the pool getter drifts from 99,950 (100,000 - 25 - 25 across two cold/warm settles on v4).
