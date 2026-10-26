# MOONSHOT-2: THE SINGING NETWORK, ridden hard (2026-10-10)

Lens: no sacred cows, every swing grounded in one real estate organ. Frame: Lessig's
four modalities, operator's "lessig ponytail" order. Topic: HIS spec (GB: closed
perimeter, TON/Tact work, gas, reward verification, heterogeneous-model consensus)
folded with OURS (the suggestion-toggle layer: seed-rib cold boot, GPS capability
ledger as network memory, profiles-as-projections, pin gate + parity law, memweave
structures-not-prose). Acceptance bar: the network learns on its own as it grows.

What would make it SING, in one sentence before the findings: a network that only
mints what heterogeneous strangers agree on (law), that treats a model agreement
claim the way a coroner treats a dead salmon (norms), that discloses every payout
split to any grepper (markets), and that eats its own disagreements as curriculum
(architecture). Anything short of those four instruments is a network that works;
these four are the ones that sing.

What is a lie waiting to be caught, in one sentence: A1 as written would stamp a
green check on top of settlement theater, A2's "K DIFFERENT models" is two families
wearing five name tags, "learns on its own" currently ends at a pile of banked
receipts, the never-silent-mining law has no byte instrument, and node identity is
pinned while model identity is self-reported. Five findings, five fixes, all
one-sitting-class.

## FINDING 1 (LAW): A1 verifies the theater's bookkeeping, not settlement; the 10x is consensus-proof-as-mint-condition

The perimeter CARD defines A1 as "the paying node's balance/ledger delta lands as
claimed (GB ask #4; closes our audit's settlement-theater finding on a staging
rail)" (watch/inbox/gstd_perimeter_design_20261010/CARD.md:13-14). But the
settlement-theater finding our own audit convicted is precisely that the ledger
delta and the chain disagree. I re-derived the conviction first-hand this sitting
from the clone, CONVERGENT with the 10-09 audit receipt
(watch/inbox/gstd_basecamp_20260109/GSTD_TOKENOMICS_AUDIT.md:20-23,47-54):

- reference/gstdcoin/gstdbot/src/blockchain/token.ts:388-398, read this sitting:
  recordEarning() fabricates `hash: 'tx_' + randomBytes(16).toString('hex')` with
  `status: 'confirmed'`. The node-side "settlement" is a random hex string.
- reference/gstdcoin/contracts/SettlementMaster.tact:128-135, read this sitting:
  SettleTask requires only `sender() == self.owner || sender() == self.gateway`;
  workerAddr, gstdBonusAmount, computeUnits, qualityScore arrive as trusted message
  fields; the only guard is the taskId replay latch.
- `grep -c "verifyQuorum|SettleTaskWithProof" reference/gstdcoin/contracts/SettlementMaster.tact`
  returned 0 this sitting, while gstdbot/src/p2p/attestation.ts:3 and
  swarm/agent.ts:694 and p2p/node.ts:128 (grep output above) all target those names.
  The signed quorum lane points at a phantom method.

So if GB's staging platform runs the same D1-counter code path (platform Workers
code is not public; audit marks every platform-side mechanism unobservable), A1's
"delta lands as claimed" PASSES while zero chain events occur. We would have
banked a receipt that certifies the theater's consistency with itself.

The swing that makes it beautiful: the perimeter's A2 output IS the missing message
schema. The consensus receipt (task, per-node model digests and answer hashes,
agreement matrix slice, dead-salmon delta, family-stratified delta, payout split)
is exactly what the phantom SettleTaskWithProof must consume: quorum = K-of-N
heterogeneous-model consensus, not gateway say-so. Then the genesis seal "supply
grows only with verified work" (audit line 43-44) gets its first enforcement site:
no consensus receipt, no mint. HIS spec and OURS stop being side-by-side documents;
the consensus receipt is literally the contract between them.

FALSIFIER: after an A1 "pass", pull the paying wallet on TON testnet. If zero
SettleTask or mint events correspond to the ledger deltas, A1 passed on theater
and the finding stands. Equally: any A1 receipt that asserts only ledger deltas
with no chain-event reference is the tell. If staging DOES emit verifiable chain
events (observable, contrary to the public-code read), then A1-as-written is fine
and this finding downgrades to "name the chain leg in the receipt".

MOVE (60-90 min): draft the consensus-receipt schema as one JSON block the harness
emits and the Tact method consumes: task_id, task_shape, per-node {node_id,
model_id, model_digest, answer_sha256, latency_ms}, K, majority_rule,
consensus_rate, shuffled_baseline_rate, dead_salmon_delta, family deltas,
payout_deltas with destination wallets and pct. Bank it beside the CARD. This is
the single artifact that turns the perimeter from GB's test rig into the behavioral
spec for his missing contract method.

## FINDING 2 (NORMS): the dead-salmon control cannot see family correlation; the garden supplies about 3 real lineages for "K DIFFERENT models"

A2 says: same task to K nodes running K DIFFERENT models, consensus must beat a
label-shuffled baseline (CARD.md:15-20). The label shuffle destroys the answer-key
association. It does NOT destroy shared priors: two siblings can agree on the same
wrong answer far above chance, and the estate's own celebrated paper predicts it.
The unisub card's own words: models trained on DISJOINT data collapse into the same
parametric subspace WITHIN shared architectures
(watch/inbox/unisub_drop_20261010/CARD.md:9-14). The perimeter CARD calls itself
"the behavioral analog of today's unisub paper claim" (CARD.md:22-23). Careful:
that analogy cuts both ways. If unisub is true, high agreement among same-family
models is lineage echo, the thing the paper predicts, not evidence the models are
right. A reviewer who reads both cards catches this in one pass: your consensus is
what your own citation predicts for siblings.

And the fleet as configured IS mostly siblings. I censused the live gstd config
this sitting (`.venv/Scripts/python.exe` over tools/gps_mcp/config.gstd.json):
20 providers, of which 5 are test doubles; the real-iron families group as
gemma-line (gemma, gemma2, gemma4, gemma4-desk, gemma4-hermes, gemma-worker-4b,
athena-class: 7 providers), qwen-line (qwen2.5 x3, qwen2.5-coder, qwen2.5vl,
qwen-desk, plus deepseek-r1:1.5b which ROUTER_VOCAB_LANDED.md:49-50 itself maps as
qwen2-arch: 7 providers), and ternary-bonsai (1, experimental, quality unproven).
So "K=5 different models" from the desktop garden is realistically 2 families and
an experiment. The dead-salmon arm passes, the consensus number is real, and it is
still substantially family correlation.

The beautiful fix is cheap and makes A2 stronger than GB asked for: a THIRD arm,
family-stratified agreement. The agreement matrix gets grouped by lineage pair;
within-family and between-family agreement rates are banked separately; consensus
counts as heterogeneous signal only when between-family agreement beats ITS shuffle
arm. And this is precisely the argument for the vast arm over mini PCs: elastic
rents vendor diversity (one llama, one mistral, one phi alongside the garden), the
one dimension a box of same-garden hardware cannot buy at any price. Diversity per
dollar is the elastic arm's real product.

FALSIFIER: run the sweep with family-blocked K-sets. If within-family minus
between-family agreement is near zero, the heterogeneity claim stands and this
finding dies. If the gap is large (say >0.2), every unstratified consensus number
in the receipts is inflated and must be re-labeled family-correlated agreement.

MOVE (45-60 min): amend the harness spec: lineage field on every node manifest row,
a lineage map table in config.gstd.json, K-set assembly rule (>=4 distinct vendor
lineages per sweep), aggregator emits the matrix grouped by lineage pair plus the
between-family shuffle arm. Spec-class, no spend.

## FINDING 3 (the acceptance bar): "the network learns on its own as it grows" has no instrument as written; the divergence curriculum is the missing loop and every organ for it already exists

The CARD's loop currently ends at banking: "divergence cases banked as receipts"
(CARD.md:18). A pile of divergence receipts changes nothing downstream unless
something consumes them. The estate already owns the law for this disease in
magatama form: "Feeding that stops producing ability deltas... means it is a pile,
not a Mag" (watch/inbox/mag_magatama_primer_20261010/CARD.md:72-74). Verbatim
applies to the network.

The swing: divergence IS the curriculum. Cases where the fleet splits near 50/50
are maximum-information tasks; auto-promote them into the task bank with provenance
origin=divergence:<receipt-id>, so the network's disagreements become its own next
exam. Then learning is mechanically checkable from bytes the estate already keeps:
the GPS capability ledger (I read tools/gps_mcp/ledger.py end to end this sitting;
verdict_log is append-only, evidence-gated at append, deduped on
(model_id,task_shape,evidence_hash), with momentum badges; live census: 34
capability rows, 707 verdict rows, 213 resolved). Two numbers per window:
(a) count of task-bank rows whose provenance is a prior divergence receipt,
(b) route-share migration per shape derived from capability rows before/after.
Both are one SQL query each. That is the instrument the acceptance bar demands.

Prior art worth folding, not rebuilding: the ledger already holds an
agreement-measured shape, arena-agreement-v1 (tools/arena_gwap.py:58; live rows
queried this sitting: 4 anthropic models, 71-148 verdicts each, pass rates 0.05 to
0.54). Its law is the independent-cop pattern: declared vs independently parsed
ruling, a claimed-but-unruled action scores as disagreement (arena_gwap.py:7-27).
The consensus harness should inherit that discipline: an answer nobody can
independently normalize is BLOCKED, not agreement. Also note the (model_id,
task_shape) primary key cannot hold a pairwise agreement matrix; the matrix needs
either a sibling table (task_id, model_a, model_b, agree) in gps_ledger.db3 or
receipts-only. Spec decision owed, name it now.

FALSIFIER: after a month of sweeps, replay the original task bank. If consensus and
routing statistics are indistinguishable from day one AND the task bank contains
zero divergence-provenance tasks, the network executed; it did not learn, and the
self-learning law failed its own bar. Conversely, a divergence task that later
converges (consensus rate rises on the promoted task) is the learning event, banked.

MOVE (60 min): write the divergence-promoter consumer spec (read latest consensus
receipts, rank cases by split entropy, append top-N to the task bank with
provenance) and add curriculum_out to the harness spec. The GPS ledger table
decision (sibling consensus_event table vs receipts-only) gets one paragraph in the
same spec.

## FINDING 4 (MARKETS): never-silent founder-mining has no byte instrument anywhere in the perimeter; the split receipt is what makes the supporter toggle mechanics instead of promise

The distribution thesis's one design decision: default wallet is the user's own,
supporter toggle default OFF, "the sovereignty product cannot silently mine for
the founder" (watch/inbox/gstd_distribution_thesis_20260109.md:21-33). The pitch
carries the toggle as the GB-blessing ask (gstd_gb_pitch_20261010/CARD.md:44-45,53).
The perimeter CARD, which is where the network's money behavior actually gets
tested, never mentions wallets, toggles, or splits: the harness asserts only
"payout delta asserted" (CARD.md:78). And the warning case is live on their side:
91% of visible emissions went to the operator's own gateway node address
(GSTD_TOKENOMICS_AUDIT.md:96-99, their bytes, their network, pre-return).

The beautiful version costs one field: every A1 payout assertion receipt names
every destination wallet and split pct (split: [{wallet, pct, role}]) and the
harness asserts the splits sum to the delta and to 1.0. Then "never silent" is
auditable by any grepper, and the supporter toggle's math is proven at fleet scale
in Phase 3 (the 1000-node payout test) BEFORE the installer ships it to real
users. The receipt is the disclosure; the market modality's instrument is the same
bytes as the law modality's proof (finding 1's payout_deltas field). One receipt,
two modalities paid.

FALSIFIER: any payout whose destination set is undeclared in the sweep manifest, or
whose split pct does not sum to the delta, is silent founder-mining caught by
bytes. If Phase 3 passes with no split receipts at all, we proved payout holds at
1000 participants but proved nothing about cleanliness, and the toggle ships on
faith, which is the exact Storm/Honeygain class the thesis names.

MOVE (30 min): add the split-assert block to the A1 harness spec (manifest declares
destination wallets and roles; receipt carries the split array; assert sum). Zero
spend, spec-class.

## FINDING 5 (ARCHITECTURE): node identity is pinned, model identity is self-reported, and the seed MCP's second-consumer proof is sitting in the same unattended sitting

The CARD pins node identity (persistent identity/volume, else a thousand ghost
rows, CARD.md:37-39) but the harness records only "model id, answer, latency,
payout delta" (CARD.md:78). The model id is self-reported. A container that claims
qwen2.5:7b and serves gemma corrupts the agreement matrix silently, and nothing in
the design fires. This is the ghost-row disease one layer up, and the estate
already owns the doctrine that convicts it: "an always-on MCP surface without a
parity check is a stale surface with a green heartbeat"
(watch/inbox/mcp_layer_status_20261010.md:71-74, law MCP-2 from
watch/inbox/ractor50/mcp.md:189-195). The parity tool exists as a pattern to copy:
tools/mcp_parity.py (on disk, read its presence this sitting) matches image
digests across surfaces; the same shape matches model digests (ollama show digest
or gguf sha256) across nodes.

The fold that makes the OURS layer load-bearing instead of decorative: the seed
MCP's named open item is exactly "a SECOND, different-client cold boot would
upgrade it from proved-once to proved-portable"
(mcp_layer_status_20261010.md:113-116). The perimeter's cold vast containers ARE
that second consumer. Each node boots through tools/seed_mcp.py join_protocol
(bounded sealed pointers hand it the task-bank context and law bytes in kilobytes,
never invented bytes, SEED_RIB_FORMAT_v0_20260926.md:96-99), and the same boot
asserts its model digest into the sweep manifest. One organ, two proofs: seed
portability at fleet scale, and consensus integrity against ghost models. This is
how the toggle layer earns its keep: not as a feature list beside HIS spec but as
the boot path the harness itself runs on.

FALSIFIER: swap a container's served model without changing its declared id; if the
per-sweep digest assert does not quarantine the node, the matrix is poisonable and
this finding stands. And if a cold vast container cannot rebuild its node context
from seed MCP alone (join_protocol fails or pointers come back stubs), the seed
stays proved-once and the portable claim dies in the honest direction.

MOVE (60-120 min): add to the harness spec the per-sweep node manifest
{node_id, model_id, model_digest, seed_join: bool}; Phase 1 (the $0 desktop rig,
CARD.md:65-67) boots at least one of its 3-5 nodes through seed_mcp join_protocol
and banks the second-consumer receipt beside the consensus receipts.

## The Lessig table, closed

| modality | instrument (this lens) | lie it catches |
|---|---|---|
| law | consensus receipt as SettleTaskWithProof message; mint gated on it | A1 green on theater (F1) |
| norms | dead-salmon + family-stratified arms on every consensus claim | family echo sold as heterogeneity (F2) |
| markets | split receipt on every payout assertion | silent founder-mining (F4) |
| architecture | model-digest parity + seed cold-boot per node; divergence curriculum into the task bank | ghost models; learning theater (F3, F5) |

The self-learning law's instrument, named once, is two SQL queries on organs that
already exist (F3): divergence-provenance task count + route-share migration from
the capability table. Everything else in this write-up exists to make those two
numbers mean something.

## Blind spots, honest

1. I did not fetch vast.ai pricing or either arXiv paper (2512.18792 dead salmons,
   2512.05117 unisub) this sitting; those claims ride the drop cards
   (dead_salmon_airllm_drop_20261010/CARD.md, unisub_drop_20261010/CARD.md), which
   say they were fetched first-hand on 2026-10-10. Treat paper claims as card-cited,
   not moonshot-verified.
2. No live network calls were made: the GSTD public platform, GB's staging
   endpoint (which does not exist yet on any side we can reach), and TON testnet
   are all outside this sitting. A1/A2 have never executed; no harness code exists
   yet (the perimeter folder holds CARD.md only; my grep for consensus code in
   tools/ and mag/ returned unrelated organs). Every finding here is spec-class by
   necessity.
3. Platform Workers code is not public (per the audit); whether staging emits real
   chain events is UNKNOWN and is finding 1's open falsifier, not a settled fact.
4. TON gas economics and Tact implementation cost for SettleTaskWithProof were not
   priced here; the 60-90 min move prices the schema, not the contract.
5. Sibling lens write-ups in this same folder were not visible when I wrote (only
   _list_new.ps1 present at my census); no convergence is claimed against them.
   The CONVERGENT flag on finding 1 is versus the 2026-10-09 audit bytes
   (re-derived independently from the clone this sitting).
6. The arena-agreement prior art was read at module-header depth plus live db
   queries; I did not re-run the arena feed or validate its graders this sitting.
