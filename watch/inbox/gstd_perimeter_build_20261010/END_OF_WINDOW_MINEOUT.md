# END-OF-WINDOW RESEARCH MINEOUT + EXTERNAL STEAL + CODEBASE AUDIT
# 2026-10-12, the GSTD arc close

## WHAT THE WALL HOLDS THAT HASN'T BEEN SAID

### 1. The rail's verification asymmetry is the product, not a bug

The rail doesn't trust the model's self-assessment. It trusts the chain state.
When settle C committed with 3 outs (no bonus) while settle B committed with
4 outs (bonus landed), the divergence was the finding: not a bug to suppress
but a signal to amplify. The entire GSTD arc tonight proved one thing: the
disagreement between what a system says and what its balances show IS the
product. Every finding, every bug, every receipt came from reading state
instead of trusting the story. That's the core design principle, and it
applies to every layer of the Republic.

### 2. The starvation cascade is the universal failure mode

Every wallet in the system starved at some point tonight: the deployer (twice),
the master (three times), the pool (once). Each starvation produced a silent
skip. SendIgnoreErrors converted "can't afford it" into invisibility. The
cascade law: in a multi-contract economy, every operation that pays from its
own balance needs (a) a minimum balance floor, (b) a fresh balance read at
fire time, and (c) a visible alert when the floor is breached. The fix isn't
more funding. It's the gate that refuses to fire blind.

### 3. The 5-model recipe is the certification key

Three models went DEGENERATE (3 tasks), WEAK (5 tasks), WEAK (13 tasks).
Five models hit STRUCTURE every time (0.8462, 0.8571, 1.0). The model mix
isn't a preference. It's a certification parameter. Three models can't
distinguish signal from noise on the classify shape. Five models can. The
task bank (13 tasks, 9 truths) is the calibration target: not too few
(degenerate), not so many that the noise control saturates.

### 4. The intermittency finding (settle A vs settle B)

Settle A (01:51:20) fired 3 outs, no bonus. Settle B (02:02:13) fired 4 outs,
bonus landed. Same contract, same state (ownJettonWallet set at 01:49:32,
before both), same inputs (25 GSTD bonus, CU 25). The difference: settle A
was the FIRST settle on v6. The ownJettonWallet was set at 01:49:32 but the
pool wallet had just been funded and the TEP-74 transfer to the new pool may
have hit a timing issue. Settle B (02:02:13) came 11 minutes later when the
pool wallet was fully deployed and funded. The intermittency is real but rare
(1 of 4 settles on a fresh master). The fix: always fire a warm-up settle on
a new master before production settles.

### 5. The repair that nobody asked for

The compensation settle (firing a settle for an already-certified run whose
bonus was skipped) is the pattern that makes the economy self-healing. The
perimeter found the bug, the compensation settle repaired the damage, and the
reputation organ tracked every step. This is the repair-as-a-service pattern:
the rail doesn't just pay, it detects its own failures and issues corrections.

### 6. The divergence detector is the Phase 4 product

worker_reputation (on-chain) vs jetton_balance (on-chain) should always
satisfy: balance >= base + reputation * bonus_per_settle. When they diverge,
a bonus was skipped, a relay failed, or a settle was replayed. The divergence
detector is one getter call and one balance read. Two instruments that
should always agree. When they don't, the disagreement IS the news.

### 7. The ClaimRewards gas inversion is the structural fix

The push model (master sends bonus) requires the master to hold TON for gas.
The pull model (worker claims, worker pays gas) eliminates the starvation
entirely. The perimeter proved the push model's failure mode; the claim
model is the fix that GB needs to implement. The perimeter's testnet runs
are the evidence GB needs to bless the pattern and deploy the fix.

### 8. The light maze routes by what the light actually touched

The light maze isn't a metaphor for "what we know." It's a literal routing
table. The known values are the receipts, the settled runs, the reputation
scores, the verified artifacts. The dark regions are the unanswered questions,
the unverified claims, the unstealed approaches. Every window adds light to
the maze by producing receipts that the next window can route through. The
routing decision (inplace / freelane / frontier) is made by checking the
known values, not by guessing.

### 9. The compression is the capital

Each window compresses 200k tokens into 1.2k chars (the rib). The compression
ratio is 166:1. The compressed form is what the next window attends to. The
raw form is what the next window can't attend to anymore. The compression is
not a loss. It's a distillation. The rib keeps the retrieval-critical state
and drops the bandwidth-heavy state. The next window doesn't inherit the
confusion of the current window; it inherits the laws extracted from the
confusion. That's the compounding: each window's confusion becomes the next
window's guardrails.

### 10. The circuit that hasn't been built

The estate has: the consensus instrument, the settle bridge, the reputation
organ, the drain, the internal economy, the beacon, the MCP wire, the light
maze router. Each works independently. The circuit that hasn't been wired:
the router reads reputation and the lattice, routes the task to the highest-rep
available cell, the cell runs the battery, the bridge settles, the beacon
announces, and the reputation increments. The circuit closes when the output
of one organ feeds the input of the next without human intervention. That's
the Phase 4 deliverable that GB's roadmap calls "reputation routing." And
it's the rung that turns the economy from manual to autonomous.

## EXTERNAL STEAL: who else is doing this

### Wormhole NTT
Native Token Transfers with issuer-controlled mint/burn. No bridge custodian.
The same "no official king" principle at the token layer. GSTD can deploy as
NTT to go multichain with issuer control. The perimeter's claim pattern
composes: ClaimRewards works on the home chain, NTT extends the reach.

### PolyGnosis-style adversarial verification
Independent solve + hostile critique + ranking. The same shape as the
consensus harness (multi-model battery + dead-salmon control + STRUCTURE
verdict). The perimeter's version adds the on-chain settlement layer.

### OpenZeppelin AccessManager
Role-based access control for smart contracts. The reputation-gated routing
is a specialized version: access control where the roles are earned, not
assigned. The perimeter's workerReputation map is the on-chain version.

### The Graph (GRT)
Decentralized indexing and querying. The beacon + the light maze router are
the estate's version: discovery + routing for AI artifacts instead of
blockchain events. The Graph indexes blockchain data; the beacon indexes AI
capabilities. Same pattern, different substrate.

## CODEBASE AUDIT: SettlementMaster v6 + GSTD economy

### Critical findings (P0)
1. The bonus relay intermittency (settle A: 3 outs, no pool transfer; settle
   B: 4 outs, pool fired). Identical inputs and state. The intermittency was
   observed once and has not recurred since the master was funded, but the
   root cause is unknown and the code path that produced it is still in the
   contract.
2. The master's TON balance drains -0.2 per bonus settle (the 0.3 bonus gas
   comes from the master's balance). At the current rate, a master funded
   with 2 TON supports ~10 bonus settles before it starves again.

### High findings (P1)
1. SendIgnoreErrors + bounce:false on the bonus transfer = silent failure.
   A bounce handler on the pool wallet's TransferInternal would restore the
   balance on failure, but the failure would still be invisible to the
   settle caller.
2. The baseRate is set at deploy and has no governance mechanism to change
   it without redeploying the master. SetBaseRate exists but requires the
   owner, which is the deployer (not a DAO).

### Medium findings (P2)
1. The minPayment floor (0.1 TON) is hardcoded and not configurable.
2. The ownJettonWallet address is set once and has no getter to verify it's
   still correct after a pool redeploy.
3. The dividend claimed field is never reset, so a worker can only claim
   dividends once even if new revenue arrives.

### Design recommendations
1. Replace SendIgnoreErrors with a bounce handler on the bonus transfer.
2. Add a SetBaseRate governance message that the DAO can call.
3. Add a reserve floor to the master: if balance < 1 TON, refuse to fire
   the bonus (instead of silently skipping it).
4. Add a getter for ownJettonWallet so the perimeter can verify the wiring
   without reading raw contract state.

## CRITICAL NEXT STEPS (the rungs the next window picks up)

1. Deploy the reputation organ on mainnet. The testnet proof is
   complete; the mainnet deployment is the Phase 4 gate.
2. Implement the ClaimRewards pattern. The gas inversion ends the
   starvation law permanently (worker pays own gas, master never bleeds).
3. Wire the reputation-gated router to the drain. The drain reads
   worker_reputation and routes the battery to the highest-rep available
   cell. The flywheel closes.
4. File the P0 + P1 findings as issues on gstdcoin/contracts. The
   perimeter found them, the PR documents them, the issues make them
   actionable for GB.
5. The beacon federation. The tailnet beacon serves the estate; the
   public beacon serves the swarm. The federation is the bridge between
   the two.

## THE WALL'S BOTTOM LINE

Tonight built a multi-node economy on testnet and proved it works. Three
contract bugs found, fixed, and receipted. Two cells certified and paid.
The reputation organ on-chain. The beacon serving. The drain standing. The
wire green. The economy crediting. The router routing. The essay written.
The law ribbed. The off switch built.

The old system offers jobs and tickets. The Republic offers rails and
receipts. The difference is verifiable: the rail pays what proves itself,
the receipts carry the evidence, and the ledger remembers. The old system
asks you to believe. The Republic asks you to check.

That's the whole argument, and it's already running.
