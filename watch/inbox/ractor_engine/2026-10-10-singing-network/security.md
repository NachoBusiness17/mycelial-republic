# SECURITY LENS: THE SINGING NETWORK (GSTD closed perimeter + consensus + MCP toggle layer)

Ractor lens-security, 2026-10-10. Frame: lethal trifecta (private data +
untrusted content + communication) over Lessig's four modalities (law = the
Tact contracts, norms = receipt culture, markets = GSTD rewards,
architecture = MCP + consensus). Every claim below was read or run this
sitting; commands named inline. No em-dashes. No sacred cows.

The trifecta is fully present in this design: private data (estate law bytes
served by the seed MCP, TON wallet seeds on nodes), untrusted content (the
task bank is built from web-mined shapes: hermes gallery stories, openclaw
showcase, X threads, press digests - all attacker-influenceable channels),
communication (tailnet to rented hosts, staging endpoint, public node_url).
The design is Phase-1-tonight class and NO harness code has landed yet (find
for "*consensus*" newer than the distribution thesis: zero hits), so every
finding below is specced at the cheapest moment to fix it.

## F1 (CONVERGENT, live-verified): A2 "heterogeneous consensus" runs on a
## two-family garden; the dead-salmon control cannot catch correlated lineage

GB's requirement is the network's founding assertion: "Nodes must confirm the
ability of different models to generate a consensus answer" (ask brief, from
watch/inbox/gstd_perimeter_design_20261010/CARD.md:4-5). The perimeter's own
hardware cannot satisfy it as specced:

- Live zoo census this sitting (`ollama list`, 16 rows): 13 chat-capable
  models, of which 6 are qwen2-lineage (qwen2.5:7b, qwen2.5:7b-instruct-q8_0,
  qwen2.5:3b-instruct, qwen-desk, qwen2.5-coder:7b, deepseek-r1:1.5b - the
  r1 distill rides qwen2 arch per ROUTER_VOCAB_LANDED.md row 7) and 6 are
  gemma-lineage (gemma:2b, gemma2:2b, gemma4, gemma4-desk, gemma4-hermes,
  athena-class 30B). 12 of 13 chat models share TWO pretraining lineages; the
  13th is the unproven ternary bonsai (ROUTER_VOCAB_LANDED.md row 14: "zero
  verdicts anywhere", evidence-farm only).
- The A2 control arm is label-shuffle only: "consensus must beat a
  label-shuffled baseline before it counts as signal"
  (gstd_perimeter_design_20261010/CARD.md:18-20). A label shuffle detects
  chance agreement; it does NOT detect correlated error from shared
  pretraining. Six qwen2 variants agreeing is real agreement with roughly
  one effective independent witness, and it beats the shuffled baseline
  every time.

The lie waiting to be caught: we would hand GB a consensus number that is
correlated echo wearing a heterogeneity costume - the exact dead-salmon
class the estate's own epistemics forbid, one level up (the drop card says
it for interpretability; it holds for consensus: plausible-looking signal
from a structure that would produce it anyway).

Move (one sitting, spec-level): the harness aggregator gains a
family-partitioned agreement matrix (consensus reported per
family-partition, never pooled across lineages) and the dispatcher asserts
K-set family entropy: at least 3 distinct lineages per consensus set,
mixing API-tier out-of-family animals (grok, glm, claude, deepseek are all
in the 17-animal vocab, CENSUS.md prior-mines list) when the garden cannot
supply them. Falsifier: if a consensus set of 3+ families STILL agrees at
rates statistically indistinguishable from a same-family set on the same
shapes, then family concentration was not the confound and the partition
was decoration - publish that null.

## F2 (CONVERGENT, re-derived): A1 as instrumented verifies the theater's
## ticket counter, not settlement - and the "closes our audit's finding"
## claim in the card is currently false

The card claims A1 "closes our audit's settlement-theater finding on a
staging rail" (CARD.md:13-14) with the assert "the paying node's
balance/ledger delta lands as claimed" (CARD.md:13-14). But the audit's
finding is that the balance delta is itself the theater:
- token.ts:387-396 fabricates hash 'tx_'+randomBytes with status 'confirmed';
  /api/rewards/claim fabricates txHash (GSTD_TOKENOMICS_AUDIT.md:19-22).
- Platform-side settlement code is unobservable (audit :6-7); asserting the
  API counter against a platform that fabricates confirmations proves the
  counter moved, nothing more.
- I re-censused the phantom method myself this sitting (quantifier law):
  `grep -rn verifyQuorum reference/gstdcoin/contracts/` -> zero hits;
  `grep -rn SettleTaskWithProof reference/gstdcoin/contracts/` -> zero
  hits; while gstdbot node code targets it at four sites (attestation.ts:34,
  :80, identity.ts:11, agent.ts:694). The signed lane points at a contract
  method that does not exist in the repo. CONVERGENT with the audit's
  2026-10-09 finding, independently re-derived today.
- The gateway wallet is the top-earning node: 91% of emissions
  (audit :95-99); the deployed SettleTask trusts one address.

An API-delta assert would be satisfied by the same D1 counter the theater
maintains. What closes the finding is an ON-CHAIN read: after a completed
staging task, read the worker address's jetton balance or the
SettlementMaster emit history from a public TON API (toncenter/tonapi,
read-only, no key) and assert THAT delta. Move (one sitting): add the
chain-read arm to the A1 harness assert and amend the card line to "A1
asserts on-chain delta; API deltas are reported as theater telemetry, not
verification." Falsifier: if the staging platform settles on-chain, the
chain read will show the payout within blocks; if it cannot (because the
signed lane has no contract target), A1 fails loud on day one - which is
the finding staying open, honestly labeled, not closed by a proxy.

## F3: the vast.ai arm puts node identities and TON wallet seeds on
## untrusted hosts, and identity pinning makes it worse

Arm 1 rents vast instances to host node containers (CARD.md:27-48), with
IDENTITY PINNING per container (CARD.md:36-39). The node's wallet seed is
"protected" by an AES key derived from /etc/machine-id or the homedir
string (reference/gstdcoin/gstdbot/src/wallet/wallet.ts:43-51, read this
sitting). On a vast host, the lessor (or any snapshot/escape) can read both
the machine-id and wallet_seed.enc: the encryption is obfuscation against
honest co-tenants, not custody against the host owner. Persistent
identities = seeds at rest on a stranger's disk for the life of the
reservation. And the closed perimeter is only as closed as vast's host
isolation: a compromised lessor host sits INSIDE the tailnet, not outside
it. Architecture modality silently overrides the law modality here.

Move (one sitting, before any Phase 2 spend): write two laws into the
perimeter CARD. (1) KEY CUSTODY: vast nodes get fresh, zero-balance,
disposable identities generated per rental; the conf-demo wallet and any
real-balance key never leaves owned hardware (blade/desktop); keys are
generated where they live. (2) TAILNET ACL: vast-joined nodes may reach
ONLY the staging endpoint, never the estate desktop, blade, or other
benches - the mesh reach of a rented host is a one-way door. Falsifier: at
any point a vast container can be shown holding a key with nonzero balance
or reaching an estate node's port, the arm is paused until the law is
enforced in code (ACL + key template), not prose.

## F4 (live-probed): OUR toggle layer's cold-boot organ breaches the
## estate's own bridge rules - the gate that tests itself and nothing else

The seed-rib MCP is what the toggle layer offers new nodes for cold boot.
Two rule breaches verified against the live code this sitting
(`.venv/Scripts/python.exe -c` probe + source read):

- Caller-supplied write root, unpinned: tool_rebuild_subtree takes `into`
  raw (tools/seed_mcp.py:112) and writes bytes there (:130) with NO
  allowlist (probe: "into allowlist present: False"). The estate's own
  never-cross doctrine rule 4 says caller-supplied write paths are refused
  and the writer is pinned (watch/inbox/ractor50/mcp.md:147, the
  estate_bridge thought-compile precedent). is_void (:52-53) protects the
  ENTRY paths, not the caller's chosen root. Locally controlled; handed to
  a guild bench or an external cold agent it is an arbitrary-root writer
  that can overwrite any colliding subpath (memory/law/... style names)
  under any directory the caller can name.
- The fetch cap is caller-RAISABLE: `cap = max_bytes or self.fetch_cap`
  (tools/seed_mcp.py:187) means a caller passing max_bytes=10GB silently
  overrides the server's --max-fetch bound. The docstring advertises
  "capped at --max-fetch" (tools/seed_mcp.py:12-14). The seal check is the
  real gate so exposure is bounded by sealed estate files, but the flag is
  a lie as written - and it is exactly the class of gate that tests itself.

Move (one sitting, code): (a) `cap = min(max_bytes, self.fetch_cap) if
max_bytes else self.fetch_cap`; (b) pin rebuild_subtree's write root to a
server-owned temp/seed root (or an explicit operator-passed allowlist),
same shape as the receipt_append spec's one-directory law; (c) two tests:
cap-raise refused, out-of-allowlist into refused. Falsifier: any test that
shows a caller raising the served cap above --max-fetch or landing bytes
outside the pinned root after the fix means the pin is decorative.

## F5: the self-learning instrument is Sybil-gradable - the GPS ledger
## verifies consistency, never provenance, and it is about to become the
## network's memory

The acceptance bar is "the network should learn on its own as it grows";
the named instrument is the GPS capability ledger fed by consensus-contrib
rows (CARD.md:79-80). The write path today is single-writer-honest:
record_verdict's Q28 gate recomputes sha256 from cited bytes
(tools/gps_mcp/ledger.py:331-344) and stores "caller-named provenance"
(ledger.py:23); a hash-only or self-written-blob row is "legal, but
self-attested" (docstring, ledger.py:341-344). Nothing checks WHO authored
the bytes or whether the verdict reflects work. Routing trusts the result:
"1 candidate(s) pass constraints and pass-rate threshold 0.85; cheapest
wins" (ROUTER_VOCAB_LANDED.md:111). In a multi-node network every
participant grades itself: two colluding nodes can pump any model's
pass-rate to 1.0 with internally-consistent (hash-correct) fabricated
evidence, and the 0.85 threshold will route real work there. The dead
salmon arm does not cover this (it controls consensus luck, not ledger
poisoning), and the LM7 positive-floor clamp (ledger.py:358-369) is
anti-gaming within one writer's row, not against the writer. The network
would then be learning fiction, autonomously, which is the self-learning
law inverted.

Move (one sitting, spec): the harness aggregator's consensus-contrib rows
require provenance that survives strangers: grader_id != model_owner_id
(cross-node grading, task issuer is not the verdict recorder) or
ground-truth-seeded tasks (known answers the platform or the dispatcher
holds) before any row feeds a shared ledger. Single-writer self-grades
stay legal only in the local, owned-hardware ledger where one owner is the
trust root. Falsifier: run one red-team sweep where a node self-writes pass
evidence for a model that is actually broken (dead-salmon twin at the
ledger layer); if those rows survive into the agreement matrix or move the
pass-rate, the instrument fakes learning and the merge gate is the fix.

## The beauty beat

What would make it sing: this perimeter can be the first GSTD-scale claim
born with its negative controls attached - dead-salmon arm in the spec from
day one (norms), family-partitioned agreement (honest architecture), an
A1 that asserts on-chain rather than against the counter the theater
maintains (law), and rewards that only route on cross-graded capability
(markets). That network's consensus number would be the first one GB can
take to a skeptic. What is currently a lie waiting to be caught: A1's
"closes the settlement-theater finding" while instrumented against the API
counter the theater itself fabricates, and A2's "different models" while
the garden is two families deep.

## Blind spots (honest)

- GB's staging platform code is unobservable (the audit's label stands); I
  could not verify whether staging differs from the public codebase.
- vast.ai: no live rental was made; pricing and host-isolation claims rest
  on the card's estimate-class notes, not my own measurement.
- The consensus harness does not exist yet, so no finding was test-fired;
  all five aim at the spec and the two live organs (seed MCP, GPS ledger).
- The dead-salmon paper (arXiv 2512.18792) and the unisub paper are known
  via the estate's drop cards, not read first-hand this sitting.
- Tailscale/WireGuard ACL semantics were not lab-tested; the tailnet ACL
  move is a spec demand, not a verified enforcement.
- SettlementMaster.tact line-level cites beyond my greps ride the audit
  receipt (2026-10-09); my independent check covered the phantom-method
  absence across the full contracts tree only.

## Instrument register (self-learning law)

Instrument that makes the learning measurable: the family-partitioned
agreement matrix + cross-graded consensus-contrib rows in the GPS ledger.
Falsifier that catches it faking: the ledger-layer dead-salmon sweep (F5)
plus the family-null test (F1) plus the on-chain assert (F2). If all three
stay green across a phase, the network's learning is measured, not
performed.
