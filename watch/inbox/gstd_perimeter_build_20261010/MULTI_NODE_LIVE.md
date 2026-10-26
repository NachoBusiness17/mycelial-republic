# MULTI-NODE LIVE - the lattice has two proven cells - 2026-10-12 (closed)

**Verdict: the GSTD rail is multi-node.** BOB (100.125.103.60, Windows, the estate's second machine) ran the consensus battery over the tailnet against the desktop's ollama - zero models, zero credentials on bob - and its STRUCTURE-certified run settled through SettlementMaster v6: **bob's wallet 100,000,000 -> 100,000,025 GSTD, first poll**, reputation-gated qualityScore 8775 (base 8750 + reputation bonus 25), and bob's on-chain reputation now reads **2**. DESKTOP reads **6**. The lattice reader (hot-lattice.ts) shows both cells' heat, money, and honor in one table.

## The run (bob's own hardware, the desktop's light)

| bob run | verdict | rates | outcome |
|---|---|---|---|
| consensus-20261012T101531Z (3 models, 8 tasks, 8 truths) | **STRUCTURE** | 0.875 vs 0.1737 | **SETTLED +25 GSTD, first poll (re-run after the balance lesson, fresh taskId 53001635792)** |
| consensus-20261012T102038Z | NOISE-CLASS | 1.0 vs 1.0 | refused by design (untestable) |
| consensus-20261012T102148Z | NOISE-CLASS | 1.0 vs 1.0 | refused by design |

The gate held across cells: bob's two degenerate runs paid nothing, exactly as the doctrine requires. The certified run paid better than the desktop's own tonight (0.875 consensus-correct on the same 3-model mix that went WEAK on the desktop at 0.40 - the 8-task/8-truth bank shape mattered more than the hardware).

## The starvation law, tx-graded (the night's operational find)

The master's bonus send carries 0.3 TON **from the master's own balance**; each settle brings 0.2 in and pays ~0.4 out (worker + treasury + protocol + bonus). Every bonus settle bleeds the master ~-0.2 TON, and when the balance drops under the queued sends, the action phase **silently skips the largest (the bonus)** - SendIgnoreErrors + bounce:false means no error, no bounce, no trace on the master: the worker just never gets paid, while reputation still increments. Tx-graded twice (04:34:53Z and 10:30:14Z, both 3 outs with ownJettonWallet provably set and inputs decoded correct on-chain). Fix proven: fund the master's reserve (2 TON via fund-master-v6.ts, now permanent script) and bonuses land first poll. Companion law: taskIds are generated as 53001 + Date.now().slice(-6) - two settles inside the same millisecond-window collide; the replay protection refunds the loser silently. Spread fires or hash the run id into the taskId.

## The honest anomaly ledger (all receipted, none blocking)

1. The drain's first fire settled taskId 53001214929 (worker TON share paid, reputation +1) with the bonus silently skipped - the starvation tx-grade. Its GSTD bonus remains OWED to DESKTOP: fire a compensation settle or fold it into the next claim batch.
2. bob's first settle (taskId 53001012772) - same starvation skip, bob's TON share paid (0.0848), bonus owed, fixed by the re-settle above (fresh taskId 53001635792 landed the 25 GSTD).
3. reputation.jsonl's drain row for 53001214929 needs a correction annotation: the row says drain_settle; the truth is settle-committed-bonus-skipped. Append-only law: correction rows, never edits.

## The state of the board

- v6 master: reserve funded 2 TON (deployer), pool 99,950 GSTD, baseRate 1 GSTD/CU.
- Cells: DESKTOP rep 6 (0.70 TON, warm), BOB rep 2 (0.18 TON after its own claim gas, cold-inference but a certified RUNNER), T90 rep 0 (0.49 TON, awaiting Termux ignition).
- PR #1 on gstdcoin/contracts: 7 commits (3 bonus-leg fixes, reputation organ, hot-lattice + MCP snapshot, reputation-gated quality, ClaimRewards gas-inversion proposal, trace instruments). GB's review is the open human gate.
- The claim model proposal (11c87ab) is the structural end of the starvation law: workers pull, the master never pays freight again.

## Falsifier

"Multi-node" dies if bob's wallet getter stops reading 100,000,025 GSTD or bob's reputation stops reading 2. The reserve law dies if a settle with master balance > 1 TON still skips a bonus (that would mean the starvation tx-grade was wrong and the pool relay is the real intermittent - the trace instruments are committed for exactly that re-check).


---

## EXTENSION (2026-10-12 late): bob's 5-model remote run - the cleanest certification of the project

Bob's lane fired the battery again with the full 5-model recipe (the STRUCTURE key): **consensus-20261012T124533Z - consensus 1.0, correct 1.0, noise control 0.0575, 8 tasks, 8 truths. STRUCTURE, the cleanest certification recorded.** Settled through v6: bob's wallet 100,000,000 -> 100,000,050 GSTD first poll, reputation-gated qualityScore 10000 (perfect base + reputation bonus 50), bob's on-chain reputation now 3.

**The portable-python unlock shipped with it:** bob had no usable interpreter (the Microsoft Store stub) - the estate shipped python-3.12.8-embed-amd64 (11 MB, no install, bare-dir) via scp; the stdlib-only harness ran on it out of the box. Any garage-wizard machine ignites the same way: ship the embeddable python + the harness, point at the nearest ollama, run.

**The ladder state:** two cells certified and paid (DESKTOP rep 6, BOB rep 3), one cell awaiting ignition (T90, Termux). The multi-node economy is no longer a design - it is a receipt.
