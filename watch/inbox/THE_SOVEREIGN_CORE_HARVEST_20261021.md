# THE SOVEREIGN CORE HARVEST (2026-10-21) - GB's headless node, stolen with love

Operator order: "headless cli self steal" + the commit link. GB shipped a
complete sovereign node core on Oct 21 (commit a28c1f6a, co-authored with
Copilot): 27 files, src/sovereign/ vertical slice, 25 unit + 12 multi-
process integration tests, honest-limits audit doc.

## What GB built (verified from the commit)

- **Identity:** Ed25519 keypair per node, nodeId = pubkey hex, mode 0600.
- **Objects:** signed envelopes - node.announce, task.publish, task.lease,
  task.result, task.attest, task.finalize; id = sha256 of canonical body.
- **The Board:** an order-independent set of envelopes. Authority derived
  at evaluation time: leases valid only if signed by the publisher; results
  only from the leased worker; attestations only from independent
  verifiers, one vote each.
- **Acceptance:** verifier-hash-match - a quorum of independent verifiers
  must reproduce the same content hash. Mismatch quorum = rejected.
- **Lifecycle:** publish -> lease (price -> quality -> hash tiebreak) ->
  execute -> verify -> finalize; expired leases reassigned; late
  duplicates never change finalized state.
- **Transport:** direct HTTP, push-on-emit + pull anti-entropy, peer
  gossip, restart recovery.
- **Ledger:** computeAccruals - pure, deterministic, idempotent. Operator
  pool 85% (parameter, unconfirmed against bytecode), 70/30 exec/verify,
  per-node cap, remainder never minted, publisher never rewarded for its
  own task. simulatePayout always reports realTransfersExecuted: 0.
- **Proofs:** proofBundle / verifyProofBundle - offline result verification
  without trusting the serving node.
- **THE HEADLESS CLI:** one command, hardware-adaptive roles (suggestRoles
  from cpus + memory), JSON-line readiness handshake, env bootstrap,
  private-peer gate, subsidy budget.

## THE HARVEST (five steals, mapped to estate organs)

1. **Verifier-hash-match quorum** -> the fleet's result verification: a
   work product is trusted when N independent verifiers reproduce the same
   content hash. Upgrades the governor's material check from ok_material
   boolean to quorum-hash attestation.
2. **The accrual ledger** (pure, deterministic, idempotent, publisher
   never self-rewarded) -> the water computer's economy design: the same
   invariants the estate holds, formalized as executable math by the
   partner. Steal the shape.
3. **Offline proof bundles** -> the fleet's receipt format upgrade: a
   receipt a stranger can verify without trusting the serving node.
4. **The multi-process integration harness** (12 tests across real
   processes) -> the fleet's own multi-agent test discipline.
5. **THE HEADLESS CLI PATTERN** -> the phone mesh's missing software (the
   phone mesh spec named it: "the node script that turns phone two into
   t90"). GB built it: one command, hardware-adaptive roles, JSON
   readiness. Node runs on Android via Termux (Node is Termux-installable).

## THE LOOP CLOSES (the mutual steal, completed)

GB built the node software. The estate holds the phone mesh spec, the
reading experiment, and the blind-reader fleet. The closure: the estate's
phones (t90 pattern, the Moto, the drawer phones) run GB's sovereign node
pattern -> the nodes become GSTD network members -> the same-book reading
rounds run ON GB's rail as verified tasks -> GB gets deployment proof of
the sovereign core on real heterogeneous hardware -> the estate gets blind
readers on someone else's rail. Both ledgers record both directions. The
mutual-steal doctrine, closed into a circle.

GB's audit doc also independently arrived at the house receipt style:
honest limits stated upfront ("not a blockchain, not libp2p, no global
consensus; if the publisher is gone its tasks stall"), unconfirmed
parameters marked, real payouts zero. Convergent honesty - or absorbed
from the public face. Either way: the style is now shared.

## Falsifier

The harvest is real if the sovereign node runs on Android/Termux and
completes a verified task cycle on GB's rail from an estate device. If the
Node/Termux stack cannot run the sovereign core, the phone-mesh closure
fails and the node role waits for the CUDA door (bob) or x86 shelves.

## Next

1. Termux + Node on the drawer phone (the Moto boots fully now - it is the
   candidate).
2. The sovereign node adapted to the t90 beacon pattern.
3. The first estate-device verified task cycle on GB's rail = the loop
   closure proof, banked.
