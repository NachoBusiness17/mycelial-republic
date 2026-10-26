# LOGIC LENS: THE SINGING NETWORK (ractor 2026-10-10, seat lens-logic)

Topic: GSTD closed perimeter + heterogeneous-model consensus (HIS spec,
CARD.md) folded with the estate MCP toggle layer (OURS). Frame: Lessig four
modalities. Law = the Tact contracts (mint gates, settlement authority, the
settlement-theater gap). Norms = the receipt culture (bytes banked, negative
controls). Markets = GSTD rewards (user's-own-wallet law, supporter toggle).
Architecture = the MCP + consensus layer. Every claim below cites what I read
or ran THIS sitting (2026-10-10). No em-dashes in this file.

## The inference rules the estate actually runs (the frame in one paragraph)

The estate's truth instruments are: the GPS capability ledger (SQLite,
record_verdict with the Q28 evidence-resolution gate and the a04 dedupe gate,
tools/gps_mcp/ledger.py:310-507), the router that reads it back into behavior
(tools/gps_mcp/router.py:226-355), the tri-state consensus gate with the CID
consensus-illusion law (mag/consensus_gate.py), the cross-family duel law
already coded into contender picking (tools/gps_mcp/router.py:618-620,
799-807), and the dual-verification Tact spine (mint authority in
GSTDJetton.tact, gateway-gated SettleTask in SettlementMaster.tact:128-129).
The singing network's learning claim rides ALL of these at once; the perimeter
card cites exactly one of them (the dead-salmon control). That gap is where my
findings live.

## F1. Two promote gates disagree and no adjudicator exists: the live router
promotes on ZERO sample support while the offline route table demands five
rows, and one lucky verdict live-captures a task shape (run this sitting)

Instruments checked live, command
`.venv/Scripts/python.exe` inline probe against the shipped test-double
registry (config.json, offline): recorded ONE verdict
(yesno-tiny / singing-probe-shape / pass / n=1 / rate 1.0 / evidence
resolved), then `Router.ask`. Output verbatim: chosen = yesno-tiny, reasons =
["1 candidate(s) pass constraints and pass-rate threshold 0.85; cheapest
wins"]. A fresh never-seen shape routed to flash-mid-1 with exploration true
("no ledger history ... exploration route"). So after a single verdict: (a)
the shape leaves exploration mode (ledger.py:723-728, task_shape_has_history
flips on ANY capability row), and (b) the n=1 rate-1.0 row passes the 0.85
threshold (router.py:245-268, passes_threshold checks rate only; sample_size
rides the Candidate but never gates). Meanwhile the generated ml3 route table
refuses rows below min_support=5 (watch/inbox/gstd_basecamp_20260109/
ROUTER_VOCAB_LANDED.md:16-19). Two promote gates, 1-vs-5, no document
adjudicates. Not flagged in any receipt I read this sitting (scoped:
ROUTER_VOCAB_LANDED.md, watch/inbox/mcp_layer_status_20261010.md,
watch/inbox/ractor50/mcp.md contain no such note). For the singing network
this is the noise-lock: the first model to touch a new task shape becomes the
router's default, every later dispatch reinforces it, and the agreement matrix
degenerates to one column: the network stops being heterogeneous the moment it
starts learning.

Falsifier: wire a min-sample floor (5, matching min_support) into
passes_threshold, rerun the same probe; if yesno-tiny still wins the n=1
shape, the floor is not on the path selection actually reads.
Move (one sitting, ~45 min): add min_sample_size to Constraints; a capability
row below the floor neither passes threshold nor ends exploration for the
shape; three tests (n=1 not eligible, n=5 eligible, below-floor shape stays
exploration-routed).

## F2. A2 as specced certifies family-correlated agreement as network
consensus: the estate's own CID law and cross-family law are cited nowhere in
the perimeter card

Ran `grep -n -i -E "consensus_gate|duel|family"
watch/inbox/gstd_perimeter_design_20261010/CARD.md` this sitting: zero hits
(exit 1). The card's A2 defines consensus as majority/exact-match across K
DIFFERENT models plus a dead-salmon label-shuffle control (CARD.md:15-20). But
the fleet it would run is family-concentrated: of 14 mapped garden models, 7
are qwen2-lineage (rows 1-7 of the vocab table, ROUTER_VOCAB_LANDED.md:34-49)
and 6 are gemma-lineage (rows 8-13). The CID law is precisely about this:
agreement among correlated samples is an anti-signal (mag/consensus_gate.py:1-26;
AUROC 0.62 at 2B, 0.09 at 120B), and the card's own sizing plans small models
per container (CARD.md:44-45, "1-2GB each with shared small models"), the
ladder's weakest zone. The label-shuffle control does NOT catch this class: it
controls for agreement-by-task-signature (easy answers), not
agreement-by-shared-lineage (the same wrong answer from siblings that trained
on the same corpus). Correlated wrongness survives the shuffle. The estate
already coded the correct control in the duel lane: a challenger must come
from a different family because "a same-family rematch measures the family
against itself" (router.py:799-807, family_of at router.py:618-620). I also
verified the consensus gate organ live this sitting: verdict(["same","same","same"],
2) = UNVERIFIED, at 30 = CONFIRMED, single-sample = UNVERIFIED, all-refusal =
UNVERIFIED, split = DISPUTED (the R3 floors hold).

Falsifier: run the same task bank through 7 qwen-siblings and through a
qwen+gemma split; if within-family agreement does not materially exceed
cross-family agreement, family stratification is decoration and the flat
matrix was honest. If it does exceed, the flat matrix was certifying lineage.
Move (one sitting, ~60 min, BEFORE Phase 1 fires): amend the harness spec so
the agreement matrix is family-blocked (cross-family cells are the headline
consensus number; within-family cells are reported as the correlated-error
ceiling) and mag/consensus_gate.verdict supplies the tri-state for each
consensus answer instead of raw majority.

## F3. A1 names two balances and the adjudicator between them is a phantom
method: the contract the signed lane targets greps to zero in the contracts
tree (re-verified on today's tree, CONVERGENT with the 2026-10-09 audit)

CARD.md:13-14: A1 asserts "the paying node's balance/ledger delta lands as
claimed" and claims this "closes our audit's settlement-theater finding on a
staging rail." Which balance? The platform D1 counter gstd_earned is the cheap
observable, and the audit proved that lane fabricates confirmation hashes
(watch/inbox/gstd_basecamp_20260109/GSTD_TOKENOMICS_AUDIT.md:19-24: token.ts
status confirmed on 'tx_'+randomBytes; whether the platform mints per payout
is unobservable). If the harness asserts only the D1 delta, A1 verifies the
theater's props, not payment. The real claim is the on-chain jetton balance,
and the contract machinery that would convert verified work into mint
authority does not exist: I re-ran the grep myself this sitting,
`grep -rn -E "verifyQuorum|SettleTaskWithProof" reference/gstdcoin/contracts |
wc -l` = 0 hits (convergent with the audit's same grep, 2026-10-09). What does
exist: SettleTask carries qualityScore and computeUnits as trusted message
fields (SettlementMaster.tact:16-21) and only DAO or Gateway may settle
(SettlementMaster.tact:128-129), with the mint authority in GSTDJetton.tact
(:89-108 area). So the adjudicator between the two balances is a method the
node code points at and the contracts do not hold: two instruments, the
arbitrating third is a phantom.

Falsifier: across a batch of N settled tasks, read the payout wallet's jetton
balance on a public TON API before and after; if D1 deltas land AND chain
balance moves by the same amount, the theater is closed. If balance never
moves while D1 accrues, A1's honest output is the measured gap, not a pass.
Move (one sitting, ~60 min total): add the chain-read arm to the harness spec
(a toncenter/tonapi GET wrapper, ~30 min code) and bank D1-vs-chain divergence
as a first-class receipt class. The perimeter then MEASURES the theater gap at
fleet scale instead of inheriting it; and GB's Tact leg gets its top priority
named: make verifyQuorum/SettleTaskWithProof real, because that method is the
missing adjudicator.

## F4. The toggle doctrine mislabels one organ: the GPS ledger is already
load-bearing in HIS harness spec while OURS is declared never-a-requirement,
and the ledger has no consensus-shaped write path

The ask's OURS framing: opt-in suggestions, never requirements. But HIS
harness spec already embeds the ledger: "Feeds the GPS capability ledger as
consensus-contrib rows" (CARD.md:80-81). That is not a toggle, that is a
dependency. And the write path it names does not exist: the ledger schema is
capability + verdict_log keyed (model_id, task_shape) with BINARY verdicts
only (ledger.py:5-34; record_verdict normalizes to 0/1, ledger.py:564-577).
A consensus-contrib row has no table. The tempting wiring (feed
agreed-with-majority as the verdict) is self-referential labeling: the graded
population defines the grader, which is the CID law one level up, the fleet
learning its own echo. The honest verdict source already exists as an
instrument: pace_run.py's direct-call-then-mechanical-grade loop
(ROUTER_VOCAB_LANDED.md:100-102). Meanwhile on GB's side the only persistent
memory is his D1 counters with an unpublished reputation formula
(GSTD_TOKENOMICS_AUDIT.md:75-81), so if the ledger truly were optional the
self-learning claim dies with it.

Falsifier: if the fold ships with the ledger still listed as optional while
the harness spec still names the ledger feed, the two documents contradict and
one must move. If any consensus row ever reaches capability without a
mechanical-grade source, the echo loop is live.
Move (one sitting, ~40 min): amend the fold's toggle list: the ledger is OUR
load-bearing instrument (we run it on our side regardless of GB's adoption;
his counters stay his); consensus outputs bank as divergence receipts (a new
append-only jsonl, not a capability mutation); capability writes only from
mechanical graders. Seed-rib cold boot, pin gate, profiles stay honestly
optional.

## F5. The self-learning law needs its instrument named: the
routing-differential test (currently its read path is hypersensitive, F1, and
its write path does not exist, F4)

"As a result, the network should learn on its own as it grows." The learning
loop as designed: verdicts accrue per model per shape, capability rates
update, the router's future dispatch composition changes (router.py:336-344
reads capability; the momentum tiebreak at router.py:281-295 is the only
sensitivity to verdict history beyond the threshold). THE instrument that
makes this measurable is the routing-differential test: dispatch the same task
bank twice, once against a frozen snapshot of the ledger and once against the
live ledger after N graded verdicts, and hash the routing decisions. Nothing
in the perimeter card names it; the card's aggregator spec stops at receipts
and ledger rows (CARD.md:75-81).

Falsifier (three arms, each catches a distinct fake):
(i) Frozen-ledger arm: routing under the snapshot must be byte-identical to a
rerun under the same snapshot; any drift means hidden state is steering, a
fabrication smell.
(ii) Decoration arm: after graded verdicts accrue, routing must shift; if it
never shifts (cost dominance pins every choice), the ledger is write-only
decoration and the learning claim is theater.
(iii) Echo arm: the shift must track mechanically-graded truth, not
majority-agreement; if it tracks majority-ness the network is learning its own
echo (CID at fleet scale).
Move (one sitting, ~50 min): implement the differential as a test (snapshot
db3, dispatch bank, hash decisions, add graded verdicts, rerun, assert shift
direction); make it the acceptance bar for Phase 1 tonight. This is the
instrument I name for the acceptance bar in my jacket.

## What would make it SING (and the lie waiting to be caught)

It sings when three loops close on one ledger: money (A1 dual-read, F3),
truth (family-stratified tri-state consensus, F2), and routing (the
differential test, F5), with promote gates that agree (F1). The beauty is that
every instrument needed already exists on this estate; the design's only real
debt is wiring and citation. The lie waiting to be caught: a Phase-1 demo
where consensus rate looks great, payout deltas land, and both are theater
(rate = family echo, payout = D1 bookkeeping), and nobody can tell because the
two adjudicators (chain read, mechanical graders) were never wired. That demo
would be the dead salmon of the whole project: plausible, unanimous, wrong.

## Checks run this sitting (and not run)

Run: (1) inline router probe proving n=1 capture (output quoted in F1);
(2) consensus_gate live tri-state checks (output in F2);
(3) grep CARD.md for consensus_gate|duel|family: zero hits;
(4) grep reference/gstdcoin/contracts for verifyQuorum|SettleTaskWithProof:
0 hits on today's tree; (5) personal line cites from SettlementMaster.tact
and GSTDJetton.tact (F3). Not run: the gps_mcp test suite (28 tests) was not
executed this sitting; no live platform or chain network reads (see blind
spots); no Tact contract execution.

## Blind spots (honest)

- No live GSTD platform reads this sitting: every platform-mechanism claim
  inherits the audit's 2026-10-09 data moments; GB's return could have
  changed tokenomics since (the pitch card's own falsifier says re-verify
  same-day before sending).
- vast.ai prices are ESTIMATE-CLASS per CARD.md:7-9; I did not fetch the
  pricing page, so all sizing economics are unverified by me.
- I did not diff contracts/build/*.fc artifacts against the .tact sources (a
  stale-build divergence class left uncensused).
- GB's staging platform behavior is unobservable from here (platform Workers
  code not public, per the audit's instruments note); whether staging settles
  on-chain at all is OWED until the chain-read arm exists.
- Sibling lenses' outputs are invisible to me; CONVERGENT flags are only vs
  prior receipts on disk (F3 is the one convergent finding: audit grep
  2026-10-09 plus my grep 2026-10-10, zero hits both).
- The seed-MCP second-consumer angle (perimeter nodes as the second cold-boot
  proof, mcp_layer_status_20261010.md:114-116) I assessed only at doctrine
  level, not by spawning a second client.

Primary sources read this sitting:
watch/inbox/gstd_perimeter_design_20261010/CARD.md,
watch/inbox/mcp_layer_status_20261010.md, watch/inbox/ractor50/mcp.md,
watch/inbox/SEED_RIB_FORMAT_v0_20260926.md,
watch/inbox/gstd_gb_pitch_20261010/CARD.md,
watch/inbox/gstd_basecamp_20260109/GSTD_TOKENOMICS_AUDIT.md,
watch/inbox/gstd_basecamp_20260109/ROUTER_VOCAB_LANDED.md,
watch/inbox/unisub_drop_20261010/CARD.md,
watch/inbox/dead_salmon_airllm_drop_20261010/CARD.md,
watch/inbox/garage_wizard_network_20261010/CARD.md,
watch/inbox/mag_magatama_primer_20261010/CARD.md,
memory/rib/RIB_LIVING_WEIGHTS_BY_NATURE.md,
watch/inbox/gstd_distribution_thesis_20260109.md, state/CURRENT.md,
mag/consensus_gate.py, tools/gps_mcp/router.py, tools/gps_mcp/ledger.py.
