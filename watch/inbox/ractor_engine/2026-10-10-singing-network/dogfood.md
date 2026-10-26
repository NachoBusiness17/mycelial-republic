# DOGFOOD LENS: THE SINGING NETWORK (ractor 2026-10-10)

Lens: dogfood, the organ mapper. Jacket: the finding filed but never wired.
Every claim below cites bytes read or commands run THIS sitting unless the
citation names a filed receipt. No em-dashes.

## Organ map first (what the design lands on)

| design beat (perimeter CARD.md) | estate organ (verified this sitting) | state |
|---|---|---|
| consensus harness v0 (CARD.md:65-67) | NOTHING named; nearest organs: tools/duel_harness.py (581 lines, K=2 same-ask + blind judge) and router.py cascade() (sequential escalation, NOT parallel) | UNBORN, but two prior organs hold 80 percent of it |
| "Feeds the GPS capability ledger as consensus-contrib rows" (CARD.md:81) | tools/gps_mcp/ledger.py:5-38, capability(model_id, task_shape, pass_rate, sample_size) + verdict_log with Q28 hash-recompute gate and a04 dedupe | LIVE schema has NO pairwise/agreement table; per-model only |
| task bank from dogfood matrix S/C/E shapes (CARD.md:78) | ROUTER_VOCAB_LANDED.md:104-132, four live routed outcomes on summarize/classify/extract with honest downgrades | LIVE |
| seed-rib cold boot for new nodes (OUR toggle layer) | tools/seed_mcp.py:204-240 join_protocol, 7 steps; cold-join falsifier 10/10 (mcp_layer_status:20-22) | LIVE but proved-once, one client |
| receipts to watch/inbox/ (CARD.md:80) | mag/estate_bridge.py:482 estate_receipt_append (landed; mcp_layer_status:75-78) | LIVE |
| payout asserted per node (CARD.md:79) | prior paycheck receipt DAWN_REPORT via gb pitch CARD.md:11-12; audit knows the payout path is theater | assert design is WEAKER than known truth (finding 2) |

Census instruments, SCOPED (both run this sitting; corrected on the
second pass after a quantifier breach):
- `grep -ril "consensus" tools/gps_mcp/` returned ZERO hits: the GPS-ledger
  aggregation view is unborn on its own organ.
- Full-tree `grep -ril "consensus" mag/ tools/ scripts/ tests/` (pycache,
  .mimosa, hook-state excluded) returned 81 files, among them FOUR prior
  consensus organs my first pass missed by reading mimosa noise as the
  whole mag/ answer: mag/consensus_gate.py (the CID law as measured,
  machine-enforced code), mag/_consensus_witness.py (a ground-truth-armed
  K=3 consensus probe, verkle-folded 2026-08-25), mag/mixture_of_agents.py
  (MoA fan-out, preserve-dissent law), tests/test_consensus_degeneracy_
  20261005.py (adversarial pins on four degenerate consensus shapes). The
  consensus organ is NOT design-class estate-wide; only the GPS-ledger
  consensus-contrib view is.

## FINDING 1 (the loop already sings at K=2; the design never names it)

The self-learning law's acceptance bar ("the network should learn on its
own as it grows") is already MET, proven, inside the estate, at K=2:
duel_harness fires one ask to two model families plus a blinded judge and
banks a row to logs/duel/duels.jsonl (tools/duel_harness.py:1-50);
import_duel_bank() replays those rows into record_verdict() per contender
with the evidence hash recomputed from canonical bytes at append, idempotent
(tools/gps_mcp/router.py:549-571); the capability table moves; momentum
badges rise and fall over verdict windows (ledger.py:222-243, STEADY when
one data point must not pretend direction); pick_duel_contenders() reads
the badged table to choose the NEXT duel (router.py:572-573). Work, ledger,
selection, work. That is the singing network with two voices.

The perimeter CARD.md:75 does say "reuses estate organs" and :80 names
the GPS ledger feed, so it is not greenfield-intent; but it names NO
organ by file, and the estate holds FIVE prior organs to compose, two of
which my first pass missed entirely (second-pass correction): the duel
loop above, plus mag/consensus_gate.py, mag/_consensus_witness.py, and
mag/mixture_of_agents.py (MoA fan-out, law: "Preserve dissent. Consensus
without dissent is groupthink").

THE MISSED ORGAN IS THE LOAD-BEARING ONE (second-pass finding, stronger
than my original): mag/consensus_gate.py banks LAW-CONS-ILLU-001, the
CID/consensus-illusion law, as measured code: agreement among N
correlated samples does NOT imply correctness; unanimity is an
ANTI-SIGNAL at small model scale (measured ladder: AUROC 0.62 estimated
at 2B, 0.09 at 120B confident mode collapse where all 5 runs return the
same wrong answer; consensus_gate.py:3-14,45-54). It already carries the
two degeneracy floors an R3 fold proved necessary (:128-138): CONFIRMED
requires n>=2 over the REAL answer pool, and refusal-shaped responses
are stripped before unanimity is measured (a refusal abstains, it does
not disagree), pinned by tests/test_consensus_degeneracy_20261005.py
(the four refused shapes, including byte-identical quads flagged
independent). A2 CONSENSUS as speced (consensus rate per shape,
CARD.md:16-18) computes agreement WITHOUT this gate: at the perimeter's
small-model tier the estate's own measured law says high agreement is
more likely mode collapse than signal, and byte-identical answers from
K "different" models are correlated echoes, the ghost-row disease in
answer space. The harness aggregator must route every K-answer set
through mag.consensus_gate.verdict(responses, model_params_b) and bank
the tri-state, not a bare rate. That is the filed-never-wired jacket in
its pure form: the law is enforced inside mag/ and absent from the
perimeter design's aggregation spec.

CRITICAL semantics guard, already in the bytes: a duel-fed pass_rate reads
"judged win-rate on this shape", not absolute pass, "they are not the same
unit, and the receipt names the source" (router.py:573-576). A consensus
row is a THIRD unit (agreement rate): two mediocre-but-converged models
agreeing must never land in capability as if it were pass. The fork MUST
carry its own disclosure row in that exact pattern, or it poisons routing.

Falsifier: VERIFIED this sitting, the judge contract IS two-slot:
judge_prompt(task, a_text, b_text, ...) with hardcoded ANSWER_A/ANSWER_B
tags (duel_harness.py:230, 250-251). The K-fork stays one sitting ONLY
because CARD.md:16-18 makes closed shapes majority/exact-match and short
answers normalized-match: a deterministic comparator, no LLM judge. Open-
shape judging needs a generalized builder or K-choose-2 pairwise duels;
that is a second sitting, priced honestly. Second falsifier, sharper: if
the perimeter's K models are all small-tier (2-8B) and correlated, the
CID ladder predicts consensus_gate verdicts of UNVERIFIED across the
board (small-model floor 3.0B at consensus_gate.py:60); A2 then honestly
returns "no signal at this tier" on day one, which is the instrument
working, not the perimeter failing.
Move (one sitting, ~90 min): fork duel_harness.py to k_harness.py; K
contenders drawn from the 14 live gstd-tier providers in
tools/gps_mcp/config.gstd.json (ROUTER_VOCAB_LANDED.md:57-70); the
aggregator imports mag.consensus_gate.verdict for every K-answer set
(tri-state + model-size ladder, the estate's measured law) on top of the
CARD.md:16-18 comparator; rows to logs/consensus/; one import path into
record_verdict with the third-unit disclosure.

## FINDING 2 (law modality): A1 as written PASSES on settlement theater

The perimeter defines A1 as "the paying node's balance/ledger delta lands
as claimed" (CARD.md:13-14). The estate's own audit already proved the
delta WILL land, in a D1 counter, with a fabricated hash: token.ts:387-396
fabricates 'tx_'+randomBytes with status 'confirmed'; /api/rewards/claim
fabricates txHash 'tx_'+sha256 (server.ts:3305); the revenue engine
promises SettlementRouter.tact settlement containing zero chain-call code
(GSTD_TOKENOMICS_AUDIT.md:19-23); the signed lane points at phantom
methods (verifyQuorum/SettleTaskWithProof: grep of contracts/ returned
ZERO hits, audit:49-54); deployed SettleTask trusts gateway fields
(SettlementMaster.tact:128-135 via audit). A1 as written therefore
certifies the theater works, which we already know. This is the design's
lie waiting to be caught: a green A1 receipt would read as "rewards
verified" while settling nothing.

Falsifier: if GB's staging platform settles real TON testnet transactions
(platform-side, unobservable from this seat), the theater finding is stale
and A1-as-written becomes sufficient; the check is resolving one payout's
txHash against a testnet explorer.
Move (one sitting, ~30 min): make A1 two-armed in the harness assert:
(a) delta lands as claimed; (b) the txHash resolves on-chain via one
explorer GET, OR the receipt stamps OFF-CHAIN-THEATER with the audit
citation. The theater outcome is not failure, it is the receipt GB most
needs: his own spec asks for "verification the network pays rewards to
participants", and the honest answer today is "the counter pays, the chain
does not".

## FINDING 3 (norms modality; CORRECTED on the second pass): the dead-salmon controls exist as estate organs and the perimeter wires none of them

First-pass claim RETRACTED as a quantifier breach: I wrote "zero bytes of
instrument" off a tools/-scoped grep (`grep -rn "dead.salmon|dead_salmon|
label.shuffl" tools/ --include="*.py"` returned ZERO, true at that scope)
while the estate holds live instruments under mag/. Verified this sitting
after the second pass:

- mag/volume_fidelity.py:13-20 is the NULL-MODEL CONTROL kill test: K
  shuffled terrains, same deterministic carve, structure statistics
  z-scored against the null ensemble, "z < 1.5 => the layout is
  statistically indistinguishable from noise: the landscape is
  DECORATION"; :405-414 is a live label-shuffle null (20 shuffles,
  Spearman rho z-scored) for neighbor fidelity. The shuffle instrument
  EXISTS, proven pattern, on the terrain substrate.
- mag/consensus_gate.py:3-8 banks the shared-bias law I thought was my
  novel insight, MEASURED, not just argued: LAW-CONS-ILLU-001, correlated
  unanimity as anti-signal, AUROC 0.09 at 120B. My "sharper than the
  cards" line was two months late and under-measured relative to the
  estate's own bytes.
- mag/_consensus_witness.py ALREADY RAN the ground-truth arm my move
  proposed to build: one grounded question (12*13=156), three independent
  lanes, per-lane correctness + agreement, CONVERGED/MAJORITY/DIVERGED
  tri-state, persisted to logs/consensus_witness.jsonl and folded to the
  verkle chain via work_register (2026-08-25). One question, not a task
  bank, but the pattern is proven and filed.

What remains TRUE, scoped precisely: the two cards bank the dead-salmon
law for the CONSENSUS/LLM path (perimeter CARD.md:19-20, dead_salmon
CARD.md:21-23) and the perimeter harness spec wires NONE of these organs
(no consensus_gate, no witness pattern, no shuffle arm in CARD.md:75-81),
and tools/gps_mcp/ (the ledger the consensus rows would feed) carries
zero consensus bytes. The unisub card also carries the qualifier my
first pass dropped: convergence is measured WITHIN shared architectures
(unisub CARD.md:13-14, the abstract's own qualifier) so the
shared-bias prediction is strongest for same-family model sets, which a
heterogeneous perimeter partially escapes and a lazy same-family rig
does not.

Falsifier: if on a pilot shape the shuffled-label consensus rate already
sits near the true consensus rate, the shuffle arm fires on run one and
A2's signal claim dies its first day (the instrument working). If
consensus beats the shuffle but still misses ground truth, that gap is
the shared-bias catch, exactly what consensus_gate's ladder prices by
model size.
Move (one sitting, ~45 min, now CHEAPER than first priced because the
organs exist): in the k_harness fork, (a) port volume_fidelity's shuffle-
and-z-score pattern as label_shuffle_arm() over the task bank, (b)
reissue the _consensus_witness grounded-question pattern as the
ground-truth arm over N fixtures per shape (fixtures need shaping work
before they serve as task shapes, per the second pass; start from the
witness's closed-form integer class where ground truth is mechanical),
(c) bank DELTA and ground-truth gap on every consensus receipt.

## FINDING 4 (architecture modality): the perimeter's containers are the seed's missing second consumer, and the design leaves them unwired

The MCP layer's own open-item list says the seed is "proved-once" and
names the cure: "a SECOND, different-client cold boot (e.g. a
garage-guild bench or a Pierre-class external) would upgrade it from
proved-once to proved-portable" (mcp_layer_status_20261010.md:114-116).
The perimeter plans 50 containers in week one (CARD.md:69-70) and a
thousand at Phase 3, and its own identity-pinning law warns "each
container gets a persistent identity/volume, else the platform mints a
thousand ghost rows" (CARD.md:37-39). Nowhere does the design say how a
vast.ai container BOOTS. join_protocol already answers it (seed_mcp.py:
204-240): read seed, obey laws, rebuild, spot-check, fetch sealed
pointers, briefs, announce a receipt naming seed_sha256. The OURS toggle
layer is not a suggestion for the perimeter; it is the perimeter's
missing onboarding rail, unmentioned.

Falsifier: if a vast.ai container (foreign image, no estate repo, cold
disk) cannot complete join steps 1-7 from seed MCP alone, the seed's
portability claim downgrades to same-machine-only and the toggle layer's
cold-boot promise must be re-scoped in the pitch.
Move (one sitting, ~60 min + pocket change): rent ONE interruptible
entry instance (CARD.md:46 estimate-class), run tools/seed_mcp.py
join_protocol inside it, bank the join receipt through
estate_receipt_append (mag/estate_bridge.py:482, landed). One sitting
closes both the perimeter onboarding question AND the MCP layer's open
item 4: the perimeter becomes the seed's second consumer, and the toggle
layer stops being optional-decoration and becomes load-bearing.

## FINDING 5 (markets modality): Phase 3's 1000-node burst is founder-mining-shaped unless the receipt names the wallet

Phase 3: "burst to ~1000 nodes via interruptible vast for the launch-scale
reward test" (CARD.md:70-73). Those thousand nodes are OUR rented boxes on
GB's rail. The distribution thesis law: user's-own-wallet default, loud
opt-in supporter toggle, "never silent founder-mining"
(gstd_distribution_thesis_20260109.md:21-31). The audit's live-network
finding: 91 percent of all emissions went to the operator's own
node/gateway address (GSTD_TOKENOMICS_AUDIT.md:96-98). A thousand our-
controlled nodes paying rewards into an estate or operator wallet
recreates the 91 percent shape on staging. On a test rail this is legal
and it is exactly the load test GB asked for; the crime would be a
receipt that lets it read as demand evidence.

Falsifier: if the staging platform caps per-wallet or per-IP rewards
(platform-side, unobservable from this seat), the burst measures the cap,
not the payout, and Phase 3's number needs re-reading as "payout holds to
the cap".
Move (one sitting, ~15 min): two fields on every payout receipt,
rewards_wallet (the address) and rail_class (TEST-RAIL|MAINNET), plus one
disclosure line in the Phase 3 spec naming the receiving wallet before
the burst fires.

## What would make it SING (the beauty call)

Not a new network: the estate's own duel loop turned up from two voices
to fifty, each new voice booting from a kilobyte seed, each answer
landing as an evidence-gated row that changes who gets asked next, every
consensus claim carrying its own shuffled-baseline and ground-truth gap,
and the first receipt that honestly stamps OFF-CHAIN-THEATER being the
one GB thanks us for. The singing is the same loop at higher K with its
instruments in the same sitting as its claims.

## Blind spots (honest)

- GB's platform internals are unobservable from this seat (audit marks
  all platform-side mechanisms unobservable); every staging-behavior
  claim above names that limit rather than guessing.
- I did not fire the GPS router live this sitting; router behavior is
  cited from ROUTER_VOCAB_LANDED.md receipts (read, not rerun).
- I did not open the Tact contracts myself; SettlementMaster/token.ts
  line cites are the audit's filed receipts, not my reads.
- vast.ai prices are estimate-class per CARD.md:7-9; not re-fetched.
- One grep under mag/ was polluted by mimosa hook-state cache noise; I
  scoped around it instead of re-running it with exclusions, and that
  shortcut breached the quantifier law: two estate-wide universals in my
  first pass ("the consensus organ is design-class today", "zero bytes of
  dead-salmon instrument") were false at estate scope. The second pass
  caught both; the corrections above are verified against the named
  files, read this sitting (consensus_gate.py, _consensus_witness.py,
  volume_fidelity.py:13-20/:405-414, test_consensus_degeneracy, and the
  81-file full-tree census).
- I cannot see sibling lens runs; the CONVERGENT-quality evidence here is
  the perimeter card's own citations of the dogfood matrix and GPS ledger
  as priors, not cross-lens agreement.
