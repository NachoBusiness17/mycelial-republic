# STEAL ROUND - external mechanisms for the estate's four exposed gaps (2026-10-14)

Targets chosen from this window's own wounds: the fountain (no token
demand), the bridge (owner-as-sole-guardian), the reputation map (no
consequence for bad evaluation), and the rehearsal discipline. One steal
per wound, each with mechanism -> gap -> adoption path -> falsifier.

---

## STEAL 1: Helium's Burn-and-Mint Equilibrium -> closes the fountain

**Their mechanism:** Data Credits are a $0.00001-pegged utility token
produced ONLY by burning HNT at market rate; DC pays all network fees and
is non-transferable. Emission goes to operators; usage burns the token.
Usage demand directly offsets emission - "burn and mint equilibrium."

**Our gap:** GSTD is minted on certified work against ZERO demand - nothing
is priced in GSTD, nothing burns it. The fountain. Friedman flagged it; the
measured burn rate made it urgent.

**Adoption path (one sitting, contract change):** a GSTD burn-for-service
door on the settlement organ - posting a task (or the settle's own relay
gas) costs GSTD that is BURNED, while certification MINTS it. The 25 GSTD
bonus per settle then has a counterweight: every unit of network use
destroys supply. Later step: denominate the relay's real gas in a GSTD-equivalent debit (the Friedman price signal), settled by burning.

**Falsifier:** track supply vs cumulative certified work over 30 days
post-adoption. If supply grows while certified work is flat, the equilibrium
failed - the mint valve is loose, not the burn.

## STEAL 2: LayerZero DVNs / Hyperlane ISMs -> fixes the SwapIn guardian flaw

**Their mechanism:** post-Wormhole ($320M via a spoofed signature-set
account; $2B+ across 13 bridge hacks in 2022 - the fixed-verifier-set is
the recurring corpse), the industry moved to MODULAR verification: each
application configures WHICH independent verifier networks must sign
(LayerZero DVNs, AND/OR quorums; Hyperlane pluggable ISMs that intercept
inbound messages). No monolithic guardian set; trust is compartmentalized
per-app and per-message.

**Our gap:** GstdBridgeRouter's SwapIn is owner-only with a self-supplied
replay key - one compromised key unlocks everything (excluded from the
build set this window).

**Adoption path:** when the router is rewritten: replace requireOwner with
a quorum interceptor - N of M independent signers (the estate already runs
a five-model council; the same shape applies to bridge keys: deployer +
bob co-sign, or a small guardian set each holding a partial claim), with
the message hash pre-committed. Interim: keep the router excluded from the
build set until this lands.

**Falsifier:** a bridge rewrite passes only if a single compromised key
cannot move value (test: fire SwapIn with one leaked key, expect revert).

## STEAL 3: Yuma Consensus (Bittensor) -> the reputation map's missing teeth

**Their mechanism:** validators score miners' work; rewards aggregate by
STAKE-WEIGHTED MEDIAN (not mean), so manipulative outlier evaluations
earn nothing; validators whose weights deviate from consensus get slashed
bonds; repeated honest evaluation compounds bonding weight. Subjective
judgment becomes math without a single judge.

**Our gap:** the reputation map counts settles per worker (valuable) but
scores nothing about QUALITY drift, and nothing polices a certifying
council that drifts. The consensus battery is the judge with no judge.

**Adoption path:** reputation v2 - keep the settle counter, add (a) the
council's own agreement variance as a quality axis (high consensus + low
correct-rate = suspicious: the dead-salmon class), (b) each cell's scores
tracked as a vector the other cells implicitly cross-check (the drain
already runs the same battery on every cell - the cross-check is free),
(c) outlier batteries get re-run cold before credit. No staking at
testnet; the median-aggregation discipline alone is adoptable in the
harness this week.

**Falsifier:** inject a rogue cell (a model that always agrees). If
median-style aggregation catches it within one cycle where mean-style
would not, the steal is verified. The dead-salmon arm is already the
harness's control - this extends it to the scoring layer.

## STEAL 4: chaos engineering cadence -> the Abiff drill's operating system

**Their mechanism:** Netflix's Chaos Monkey class - faults injected ON A
SCHEDULE, deliberately, with a hypothesis written BEFORE each injection
and a rollback path armed, so failure is rehearsed rather than suffered.
Game days: the whole team practices the outage.

**Our gap:** the Abiff drill (banked this window) names the rehearsal;
chaos engineering supplies the CADENCE and the hypothesis discipline.
The estate already half-runs it: dead-salmon controls, the dry-gate
live-fire, the band bounces - all accidental chaos that taught real
lessons.

**Adoption path:** a monthly injected-fault game day, one hypothesis each:
kill ollama mid-battery; serve a stale master read; feed the drain a
NOISE-CLASS cell; replay a taskId (done - 54291 verified). Each with the
hypothesis filed before the fault and the amendment after.

**Falsifier:** a game day that produces no runbook amendment fails its own
purpose (the L2 Mason's rule, restated).

---

## The meta-steal

All four external systems solved their gap the same way the estate solves
everything: they made honesty cheaper than deception, measured the
outcome, and rehearsed the failure. The steal confirms the house style is
the industry frontier - we are not behind; we are under-instrumented in
exactly four places, and each now has a named, falsifiable fix.

Sources: [Helium token docs](https://docs.helium.com/tokens/hnt-token),
[tokenomics.com HNT analysis](https://tokenomics.com/articles/helium-tokenomics-how-hnt-distributes-100-of-network-fees-to-operators),
[Merkle Science on the Wormhole exploit](https://www.merklescience.com/blog/hack-track-analysis-of-wormhole-token-bridge-exploit),
[LayerZero V2 message security](https://docs.layerzero.network/v2/concepts/protocol/message-security),
[Chainalysis bridge-hack tally](https://www.chainalysis.com/blog/cross-chain-bridge-hacks-2022),
[Yuma Consensus docs](https://www.bittensor.com/docs/internals/consensus),
[arXiv 2507.02951 on Bittensor](https://arxiv.org/html/2507.02951v1).
