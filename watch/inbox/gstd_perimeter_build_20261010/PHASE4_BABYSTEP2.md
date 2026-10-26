# PHASE 4 BABYSTEP 2 - reputation on-chain - 2026-10-11/12 (closed)

**Verdict: the reputation organ is live on-chain and getter-verified.** SettlementMaster v6 (EQDw9oXaR1lmwaVJdJFYA2heY11ktvdS0Jsdnee7Qqxur_g8) carries a per-worker reputation map updated on every SettleTask and readable by anyone: `worker_reputation(Address)`. Live proof in one settle: DESKTOP's jetton wallet 100,000,050 -> 100,000,075 GSTD (+25, first poll) AND `worker_reputation(DESKTOP) = 2` (1 from the prior settle on this master lineage + this one), both read by getter.

**Contract change (committed to PR #1 as ebb6121):** `workerReputation: map<Address, Int>` updated in SettleTask, getter `worker_reputation(Address): Int`, null-guarded for first-time workers. The PR (open since tonight) now carries two commits: the three bonus-leg fixes + the reputation organ.

**The night's honest arc (three deploys, each teaching):**
1. First reputation build used `??` - this repo's tact predates null-coalescing: compile error, codebase idiom is `== null` checks + `!!`.
2. Second build compiled but the FIRST settle on the fresh master self-refunded: my bare `!!` on a first-time worker's missing row aborted the whole SettleTask. Null-guard landed. (A real trap GB's own code would hit the same way - the receipt saves him the excursion.)
3. Third build: settle executed (reputation 1) but the bonus was skipped - the deploy script's SetOwnJettonWallet had landed LATE (after the settle; blind-fire sequencing under testnet load). Gated standalone re-wire, fresh taskId, settle: +25 first poll, reputation 2.

**Ops law, now triply-receipted and the night's headline lesson: blind-fire deploy scripts drop messages under testnet load.** The gated standalone pattern (one action per script, read-confirm between) executed flawlessly every time it was used. The deploy script stays as the anti-pattern receipt.

**Stack state:** v6 live (EQDw9oXa...), pool 99,950 GSTD, DESKTOP 100,000,075 GSTD / reputation 2, deployer rebalanced twice tonight (DESKTOP floor 0.33 hit, BOB wired 0.5, operator topped +2 TON - all consumed by real settles and deploys).

**Ladder after babystep 2:** reputation getter is readable by any node - next is the ROUTER reading it (reputation-gated task routing), bob/t90 remote runs (bob needs the authorized_keys line), and the GB PR set companion docs. PR #1 carries both commits now; GB's review is the open human gate.

## Falsifier

The reputation claim dies if worker_reputation(DESKTOP) stops reading 2 on v6, or if a settle executes without incrementing the getter. The gating claim dies if any settle fires without a STRUCTURE verdict having been passed explicitly.
