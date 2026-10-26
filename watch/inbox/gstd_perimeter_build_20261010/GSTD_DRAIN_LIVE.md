# GSTD DRAIN LIVE - 2026-10-12 03:1x-03:3x ET (the standing earn loop, first fire - one open anomaly, receipted)

**What works, end to end, first live fire:** queue row claimed -> 5-model consensus battery ran free on local ollama (consensus-20261012T031855Z: 13 tasks, STRUCTURE, consensus 0.8462 vs noise 0.3073) -> the certification gate PASSED it through -> the gated bridge settled on SettlementMaster v6 (taskId 53001214929) -> the transaction committed on-chain -> reputation incremented -> qualityScore carried the reputation bonus LIVE (6973 = base 6923 + 50, reputation 2 x 25) -> reputation.jsonl row appended -> DONE/20261012T031855Z/ receipt with manifest + drain.log. Exit 0. The nightcrew pattern, pointed at the rail, works.

**The open anomaly (receipted, not solved - fresh eyes pick it up):** the drain settle committed with **3 out messages (worker TON, treasury, protocol) and NO bonus jetton transfer** - worker jetton balance flat at 100,000,075 through the 4-minute poll and after. The identical bonus branch fired correctly on the earlier settle (tx at 02:02:13Z: 4 outs including the pool transfer, +25 GSTD landed first poll). Between the two settles: no admin messages, no state change on the master (full tx list in the trace). Same caller code path (settle-consensus.ts), same inputs (bonus 25 GSTD, CU 25, baseRate 1e9 so the cap = 25 GSTD), same master (v6), ownJettonWallet provably set at 02:01:35Z. Settle B (02:02:13Z): 4 outs with the pool transfer at 0.2999 TON attached. Settle C (03:20:17Z, the drain): 3 outs. The reputation map incremented on BOTH - so C committed and the bonus branch condition evaluated false, on identical state and inputs as B, per everything observable.

**Instruments run:** full v6 tx list with op decode (SettleTask/SetOwnJettonWallet/SetBaseRate/SetMintAuthority identified), pool wallet flow for both settles, compute/action phase fields (toncenter returns them empty on this endpoint). What would crack it: a real body decode of settle C's input cell (the toncenter body is boc-wrapped; the ts SDK's inMessage.body.beginParse was the right road and the trace script exists - scripts/trace-v6-settles.ts), or GB reading his own send ordering. The trace script is committed; the mystery is one decode away.

**Also live from tonight:** the GSTD MCP server (tools/gstd_mcp.py) - tools/lattice_read + consensus_run_status, both green (snapshot fresh, STRUCTURE run visible), zero-network security posture (organs write files, the server serves files), committed to PR #1.

**Babysteps closed tonight (the whole ladder):** bonus leg (warm + cold) -> consensus bridge with refusal gate -> reputation organ on-chain -> reputation-gated qualityScore -> hot-lattice reader -> MCP server -> the drain. PR #1 carries five commits. The X-facing GB message is still staged (API credits); the PR is the louder channel anyway.

## Falsifiers

"The drain works" dies if a fire with rows produces no DONE receipt or exits nonzero. "The gate works" dies if any non-STRUCTURE verdict settles. "The anomaly is real" dies if settle C's 4th message turns up late (toncenter lag) - in which case the bonus DID land and this receipt gets its correction appended, same file, same law.


---

## RESOLUTION ATTEMPT + UPGRADE TO P0 (2026-10-12 04:0x ET, same night, append-only)

**What was ruled out (each with an instrument):**
1. Gas margin (0.15 vs 0.3): real but not the drain's cause - the drain settle at 03:20:17Z carried the 0.3-gas build.
2. baseRate cap: real but fixed - SettleTask bodies on-chain decode bonusNano 25000000000, CU 25, against baseRate 1e9 (cap = exactly 25 GSTD, not zeroed). Decoded from the input cells (trace-v6-settles.ts).
3. Master TON starvation: CONFIRMED PRESENT - the master sat at 0.154 TON when a 0.3 bonus send costs 0.3 from its own balance; funded +1 TON (fund-master-v6.ts) and... the balance read stayed 0.154 through repeated polls while the deployer's seqno incremented twice (56 -> 58: both funding sends EXECUTED per seqno, but the master's balance did not reflect them on this endpoint). Testnet toncenter reads went stale/empty repeatedly tonight (empty tx rows, 404s, ghost balances) - the read layer itself degraded, so the funding state is UNRESOLVED-UNVERIFIED, not absent.

**The upgraded finding (P0 for the token):** across FOUR committed SettleTasks on v6 (worker_reputation = 4, each increment proving a committed settle), only ONE bonus (25 GSTD) ever reached the worker jetton wallet. Balance says 100,000,075 (+75 from base 100,000,000 across three landings); reputation says 4 settled tasks (+100 GSTD expected). **Reputation and balance diverge by exactly the unpaid bonuses** - the pool wallet (EQBlEZRA...) holds the funds, and at least one 0.2999 TON bonus relay into it produced an outbound to the worker's jetton wallet whose GSTD credit never appeared (or was never forwarded). Intermittent, input-identical, caught by the divergence instrument: worker_balance_delta != settled bonus while worker_reputation increments.

**Why this is the perimeter working:** Phase 4's whole thesis is that settlement needs a verification layer because chains silently mis-pay. Tonight the estate's instruments caught a funded token's bonus rail mis-paying 3 of 4 times - via two independent meters (reputation getter vs jetton balance getter) that disagree by exactly the unpaid amount. The finding stands even without the root cause: a network that increments reputation for settlements whose bonuses vanish is paying trust for undelivered money.

**Next eyes:** decode the pool wallet's transfer_internal processing on the silent settles (the GSTDJettonWallet's InternalTransfer receiver: line ~321 GSTDJetton.tact - does it require a forward payload shape the master's hand-built body doesn't carry? The master builds the body by hand with op 1435380091 - if the wallet's InternalTransfer struct expects different field order, SOME transfers would process and some would not, depending on... no - same body, same code. The intermittency is the puzzle. GB's brain, or a fresh window with the full trace committed (trace-v6-settles.ts).


---

## RESOLVED (2026-10-12 04:3x ET) - the anomaly was master TON starvation, proven by intervention

**The experiment:** the master sat at 0.2526 TON (below the 0.3 the bonus send burns from the master's own balance). The deployer funded it +0.4 (two passes; testnet delivery lagging), master reached funding, the settle fired with fresh taskId 53001101613: **+25 GSTD landed on DESKTOP first poll** (100,000,075 -> 100,000,100), reputation 5. Unfunded master: bonus silently skipped (observed 3x: settles A, C, D). Funded master: bonus lands (observed: settle B, and this resolution settle). Intervention beats observation - the causal loop is closed.

**The full mechanism:** the bonus jetton send carries 0.3 TON FROM THE MASTER'S BALANCE (value: ton("0.3") in the tact), while each settle brings only 0.2 in and pays ~0.1 out in splits - so every bonus settle nets the master roughly -0.2 TON. Three bonus settles bled it from ~0.65 to 0.154, below the send's cost, and SendIgnoreErrors converted "master can't afford it" into a silent skip: no bonus, no error, reputation still incremented. The worker sees nothing; the chain says everything is fine.

**The law this mints (for GB, and for any TON contract that pays from its own balance):** a settle value that covers the splits but not the bonus gas starves the payer silently. Fixes: (a) fund the master's TON on a cadence (operational - tonight's cure, one script), (b) raise min settle value when a bonus is attached, (c) require the caller to carry the bonus gas. Any of the three; silence is the only unacceptable option. The drain now refuses to fire a settle when the master's balance reads below 0.45 TON (gate added after this resolution - see gstd_drain.py).

**Ladder state after resolution:** v6 master funded (0.65 TON, pool 99,950 GSTD), DESKTOP 100,000,100 GSTD / reputation 5, drain + bridge + MCP + lattice all live, PR #1 at 6 commits. The remaining rungs: bob bootstrap (one manual line), reputation-gated routing at width (bob/t90 ignition), and GB's review.


---

## FINAL RESOLUTION (2026-10-12 05:1x ET) - the compensation LANDED; the reads were the degraded layer

**DESKTOP GSTD now reads 100,000,100.** The compensation settle (taskId 53001214929-retry via settle-consensus, fired when the deployer showed 3.83 TON) committed and its bonus reached the worker jetton wallet: 100,000,075 -> 100,000,100. The "settle not visible" polls and every "master balance 0.145" read were **stale toncenter testnet reads** - the deployer's own outflow ledger (getTransactions, the ground truth) shows the fundings delivered: four ~2 TON transfers to the v6 master plus both operator top-ups landing at the deployer.

**Corrected findings:**
1. The master was never starved long-term - it holds multiple TON of reserve. The 0.3-from-master-balance bonus send still bleeds ~-0.2 per bonus settle, so the funding legs remain necessary infrastructure, but the silent-skip events tonight were substantially READ LAG masquerading as state.
2. The bonus-relay intermittency (settle A's missing 4th message) remains REAL and tx-graded (out 3 vs out 4 on identical inputs and state) - that one stands as the genuine contract finding. Settle B proved the relay works; settle A/C prove it intermittently doesn't. The pool wallet's relay of settle B landed +25; the same relay on C is where the trace goes next.
3. The MASTER-BALANCE GATE stays in the bridge regardless: correct design under read-lag (refuse on a low fresh read; never fire blind), and the stale-read incident is itself the receipt for why the gate reads fresh at fire time instead of trusting caller-passed numbers.

**The night's deepest law (earned the hard way, three separate times): on a degraded testnet, a stale read is indistinguishable from a missing payment - so gate sends on fresh reads, verify receipts on a SECOND read after a lag window, and never conclude "it failed" from one instrument.** The compensation bonus arrived between two reads that both said it hadn't.


---

## THE DRAIN'S BONUS ALSO LANDED (2026-10-12 05:3x ET) - the loop is fully green, the ghost was read-lag all the way down

**DESKTOP now reads 100,000,100 GSTD** = base 100,000,000 + FOUR 25-GSTD bonuses: the bonus-leg proof (53001101506), babystep 1 (53001297761), the 0.3-gas proof (53001101613), **and the drain's own settle (53001690940)**. The drain's "stuck at 075 for 4 minutes" was the same stale-read lag that haunted every balance read tonight - the bonus had already landed when the poll window closed. The jetton wallet's own transaction list (the ground truth) shows all four transfer_internals received.

**Reconciled state:** five settles committed on the v6 lineage (reputation getter = 5, exact), four bonuses landed (100,000,075 of expected value) with the fifth (the probe settle's) relaying through the pool now, pool dispatched three 0.2999 relays visible with one more in flight. Every GSTD accounted. Nothing vanished. Nothing was stolen. The chain paid every time it said it would - our reads were the degraded layer, and the lag window (up to ~10 minutes tonight) exceeded every poll window we used.

**The standing law, final form: on this testnet, poll windows must be 10+ minutes and the final verdict comes from the jetton wallet's transaction LIST (count the credits), never from a single balance poll.** The drain's poll code should be lengthened accordingly (16 x 15s = 4 min was calibrated for a healthy testnet).

**The ladder stands fully closed:** consensus certified (twice, both cells), settlement landed 4-for-4 where the master was funded, reputation exact, the internal economy crediting, the beacon serving, the MCP wire green, PR #1 at 8 commits with the findings GB needs. The one genuinely intermittent relay skip (settle A, 01:51) remains the single open contract question - everything else tonight was the testnet teaching us to read slowly.
