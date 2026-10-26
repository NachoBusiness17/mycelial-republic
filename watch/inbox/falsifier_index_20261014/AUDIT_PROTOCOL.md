# THE AUDIT PROTOCOL - how to kill (or keep) a "decentralized" claim

Theses 61 and 63 claim: a node holds its own keys, its own memory, its own
weights, and settles in public, with no permission anywhere in the path;
"truly" is the falsifier - find the permission and the claim dies. This
protocol is the method. It is written so a stranger can run it against ANY
vendor's "decentralized" marketing, including ours.

For each of the four possessions, walk the path from the holder to the
thing and record every step where a third party can refuse, revoke, gate,
or price the holder's access. One recorded permission anywhere in a
possession's path fails that possession. A vendor passes with four
clean paths. Anything else is a percentage of decentralized, which is
another word for rented.

## POSSESSION 1: KEYS

1. Who generated the key material? (holder-generated vs provider-issued)
2. Where does the private key live at rest? (holder device vs provider vault)
3. Can the provider reset, freeze, or rotate the key without the holder's
   signature? (any yes = permission)
4. Is withdrawal self-served end to end - no review queue, no business-hours
   window, no re-verification step, no fee above the raw network cost?
5. Record each step's answer with a screenshot or a clause quote.

Fail example (public record): a New York exchange froze a holder's balance
in 2026 without a prior request; steps 3 and 4 both answered yes.

## POSSESSION 2: MEMORY

1. Where does the agent's state live at rest? (holder machine vs provider
   cloud)
2. Can the holder export ALL state in an open format, machine-readable, with
   no provider mediation?
3. Does state survive the provider's billing decision? (suspend the card -
   does the memory die?)
4. Does the provider read the memory for its own purposes (training,
   profiling)? (any undisclosed read = permission)
5. Does state survive the PROVIDER's death? (company folds - who holds the
   copy?)

## POSSESSION 3: WEIGHTS

1. Can the holder run the full model on the holder's own hardware, offline,
   forever? (a no at any clause = permission)
2. Is the weight file itself obtainable - not a demo, not an API slot?
3. Does any agreement survive the download (usage restrictions, callback
   checks, license revocation)?
4. Can the holder modify the weights (fine-tune, merge, quantize) without
   the provider's approval?

## POSSESSION 4: SETTLEMENT

1. Is payment for the work settled on a public chain, verifiable without
   the provider?
2. Can the provider reverse, censor, or reorder a settlement? (any yes =
   permission)
3. Is the settlement's price formation public - or set unilaterally?
4. Does the worker's reputation/history survive outside the provider's
   private database?

## SCORING

- Four clean paths: the claim "truly decentralized" is earned. The vendor
  may call its node a node.
- Any permission in any path: the vendor's claim is checkably partial, and
  the partial list is the marketing's debt.
- Refusal to disclose any step: scored as a permission at that step.
  Unauditable is unaudited.

## OUR OWN SCORE (run against the estate, same protocol, 2026-10-14)

- Keys: holder-generated (testnet mnemonics in machine-local .env,
  regenerate-refusal; mainnet keys staged with a custody runbook and the
  holder's paper-backup drill owed before funding) - clean at generation
  and storage; the runbook drill is the open line.
- Memory: machine-local palace + memory trees, no cloud copy - clean.
- Weights: local ollama models (open weights), holder-modifiable - clean.
- Settlement: GSTD on public testnet, settlements chain-verifiable - clean
  at settlement, with the honest caveat that the estate's contract suite is
  under review as PR #1 and unmerged (the theses say so on the door).

Open lines are recorded, not hidden. That is the difference between an
audit and an advertisement.
