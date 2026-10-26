# MOONSHOT-1: THE SINGING NETWORK (ractor_engine 2026-10-10 fold)

Lens: moonshot (no sacred cows, every swing grounded in a real organ). Frame: Lessig's
four modalities, operator's ponytail order. Topic: the GSTD closed-perimeter +
heterogeneous-model-consensus design folded with the estate's MCP concepts as an
opt-in suggestion-toggle. Acceptance bar (operator law): "the network should learn
on its own as it grows." Every claim below cites bytes I read or commands I ran this
sitting (2026-10-10); anything not verifiable is marked OWED, never asserted.

## The four modalities, mapped (CODE IS LAW)

- LAW = the Tact contracts: GSTDJetton mint gate, SettlementMaster authority. Read
  first-hand this sitting: SettleTask takes trusted gateway fields, replay-guarded
  on taskId, sender must be owner or gateway
  (reference/gstdcoin/contracts/SettlementMaster.tact:128-135); my grep of
  contracts/*.tact for verifyQuorum and SettleTaskWithProof returned ZERO hits
  (command: grep -n "SettleTask\|verifyQuorum\|SettleTaskWithProof"
  reference/gstdcoin/contracts/*.tact; only :16 message and :128 receive). The
  quorum lane in node code points at phantom methods; the deployed path trusts one
  address. CONVERGENT with GSTD_TOKENOMICS_AUDIT.md:49-54, now re-derived by my own
  grep.
- NORMS = the receipt culture: every consensus claim banked with bytes, dead-salmon
  controls on every read of model internals (dead_salmon_airllm_drop_20261010/
  CARD.md:21-26).
- MARKETS = GSTD rewards: user's-own-wallet default, loud opt-in supporter toggle,
  never silent founder-mining (gstd_distribution_thesis_20260109.md:21-32).
- ARCHITECTURE = the MCP + consensus layer: five live surfaces
  (mcp_layer_status_20261010.md:36-45), the GPS capability ledger, the seed MCP.

## FINDING 1 (LAW): A1 as written will PASS on theatrical settlement. The theater-catcher is chain resolution, not ledger deltas.

The perimeter card asserts A1 as "the paying node's balance/ledger delta lands as
claimed... closes our audit's settlement-theater finding on a staging rail"
(watch/inbox/gstd_perimeter_design_20261010/CARD.md:13-14). But the theater IS that
the counter and the local transaction list move while nothing touches a chain. Read
first-hand this sitting: recordEarning fabricates
hash: 'tx_' + randomBytes(16).toString('hex') with status: 'confirmed' and prepends
it to a local list (reference/gstdcoin/gstdbot/src/blockchain/token.ts:387-403). A
delta assert passes on exactly this code path. The audit already proved the live
counter moves with zero observable chain settlement
(gstd_basecamp_20260109/GSTD_TOKENOMICS_AUDIT.md:17-24, 58-59). The fix that makes
A1 honest: every claimed txHash must RESOLVE against TON testnet (a GET to
toncenter/tonapi per payout), plus a negative control: 'tx_'-prefixed non-resolving
hashes must be flagged as fabricated-class, hard-fail. One sitting, ~60 lines, $0.
FALSIFIER: if a staging payout whose txHash resolves nowhere still passes A1, then
A1 is theater verification wearing an audit's clothes. This also arms the swing:
GB's own "TON/Tact contract work" need is best served by the perimeter being the
first testbed for the MISSING SettleTaskWithProof: heterogeneous consensus IS the
quorum the audit says nothing enforces (GSTD_TOKENOMICS_AUDIT.md:133-134).

## FINDING 2 (ARCHITECTURE): "K DIFFERENT models" on this garden is ~2 weight lineages. Unpartitioned consensus measures family echo. The estate already built the law at the duel layer and the perimeter does not name it.

A2 says "K nodes running K DIFFERENT models" (CARD.md:15-16). Counted this sitting
from the live config (.venv/Scripts/python.exe -c over tools/gps_mcp/
config.gstd.json): 20 providers, 14 real (test_double false); by base weights that
is ~7 qwen-derived (qwen2.5 x3, qwen-desk, qwen2.5vl, qwen2.5-coder,
deepseek-r1:1.5b per ROUTER_VOCAB_LANDED.md:34-49), ~6 gemma-derived (gemma,
gemma2, gemma4, gemma4-desk, gemma4-hermes, athena-class), 1 experimental ternary.
The unisub paper's own abstract qualifies convergence as WITHIN shared
architectures (unisub_drop_20261010/CARD.md:13-15): disjoint data, same geometry.
So same-lineage agreement is the dead salmon of fleet consensus: plausible-looking
signal from shared weights. The estate's duel organ already enforces the honest
shape: pick_duel_contenders requires a cross-family challenger and a third-family
blind judge (tools/gps_mcp/router.py:766-841, the LW9 judge-bias law), with
family_of at router.py:618-620. CONVERGENT: the perimeter should port this law, not
re-derive it. Two gaps to fix: (a) the card never partitions the agreement matrix by
lineage; (b) family_of is prefix-based, so qwen-desk counts as a DIFFERENT family
from qwen2.5 today (router.py:618-620 splits on the prefix), understating
inbreeding. MOVE (one sitting): add a base-weights lineage key to each provider row
in config.gstd.json; the consensus aggregator reports within-lineage vs
cross-lineage agreement separately; require >=3 lineages per round (the desktop
garden alone cannot supply them; the vast arm or API tiers add the third). FALSIFIER:
if within-lineage agreement minus cross-lineage agreement is inside label-shuffle
noise, heterogeneity is decoration and A2 is family echo wearing a consensus badge.

## FINDING 3 (the acceptance-bar instrument): "learns on its own as it grows" has a data organ but no behavior-change organ. Name the instrument: the route-flip diff plus the ledger-shuffle control.

The design feeds consensus into the GPS capability ledger as consensus-contrib rows
(CARD.md:79-80) and the ledger already learns in place: momentum badges RISING/
STEADY/DECLINING are earned from verdict windows (tools/gps_mcp/ledger.py:623-633),
routing reads pass-rate with a 0.85 threshold and cheapest-wins
(tools/gps_mcp/router.py:40, 336-344), every decision emits an append-only receipt
(router.py:16-20, ReceiptLog at :201-223). But learning is a BEHAVIOR claim, and no
organ measures behavior change: which shapes gained first history (exploration ->
measured), which models crossed the threshold up or down, which chosen-model flipped
week-over-week. Without that diff, "the network learns" is a pile getting heavier.
MOVE (one sitting): tools/gps_mcp/learning_diff.py: diff two ledger snapshots plus
receipts.jsonl, emit route-flip rows (shape, old chosen, new chosen, the ledger
delta that caused it) to watch/inbox/. Then fire the falsifier once and bank it:
LEDGER-SHUFFLE CONTROL (the dead-salmon law applied to the router itself): shuffle
capability rows, re-run identical asks; if routing decisions do not change, the
ledger is not load-bearing. FALSIFIER: 30 days of perimeter growth with zero route
flips, or shuffle-invariant routing, means the network grows but does not learn; the
acceptance bar fails and the fix is the organ, not the claim.

## FINDING 4 (MARKETS, the 10x swing): divergence is not a receipt to file, it is the product. The consensus sweep is the network's demand mint and the ledger's ground-truth foundry.

The audit's verdict on GB's economy: emission ~1.53 GSTD/day network-wide, "the 400M
pool is not the binding constraint at that rate - demand is"
(GSTD_TOKENOMICS_AUDIT.md:82-84), with cold demand the named failure mode (:109-111)
and every task a net emission subsidy of 2-10x revenue (:91-94). The perimeter card
currently banks divergence cases passively ("divergence cases banked as receipts",
CARD.md:18). The inversion that makes it sing: a task shape where heterogeneous
LINEAGES disagree is precisely a task worth routing to a human for adjudication
(GWAP), and the human verdict is the graded ground-truth fixture the capability
ledger is starved for (record_verdict is evidence-gated, Q28; consensus gives cheap
pseudo-ground-truth, divergence marks where real ground truth is missing, humans
mint it, routing improves, better routing sharpens the next sweep). Organs exist on
disk: tools/arena_gwap.py (110/110 dirs banked, ARENA_GWAP_BACKLOG_R3_20261010.md
line 1), percolator novelty scoring as the ranking substrate
(garage_wizard_network_20261010/CARD.md:92-94), the ledger's record_verdict. The
loop closes demand by construction: every consensus sweep emits its own next task
batch. Market law rides unchanged: user's-own-wallet default, loud opt-in supporter
toggle, never silent founder-mining (gstd_distribution_thesis_20260109.md:21-32);
the perimeter is the dress rehearsal for the installer, so its reward path must
default to per-node test wallets from night one or it rehearses the wrong reflex.
MOVE (one sitting, then Phase-1 fold): add divergence_rank to the aggregator output
(shape, models, answers, disagreement metric); route top-ranked items into the GWAP
backlog format; after adjudication, feed verdicts back through record_verdict with
evidence_source prefixed gwap-adjudicated. FALSIFIER: if adjudicated divergence
cases produce zero capability-row changes within a week of closure, the loop does
not close and the demand-mint is theater.

## FINDING 5 (OUR toggle layer): the perimeter IS the seed MCP's second consumer, sitting one wire away from upgrading proved-once to proved-portable.

The MCP status names its own open item: "Seed MCP second-consumer proof: one
cold-join falsifier passed; a SECOND, different-client cold boot (e.g. a
garage-guild bench or a Pierre-class external) would upgrade it from proved-once to
proved-portable" (mcp_layer_status_20261010.md:111-116). The perimeter is that
second consumer at zero extra cost and it is the exact opt-in shape the fold
demands: HIS spec works without it; with it, each Phase-1 node boots via
tools/seed_mcp.py join_protocol (3 resources + 4 tools, bounded sealed pointers,
fetch capped at --max-fetch; verified structure by grep this sitting:
tools/seed_mcp.py:56-57, 174, 204, 264, 356) instead of a hand-built image, and
identity pinning (the ghost-row law, CARD.md:37-39) rides the same persistent
volume. The GPS capability ledger rides along as the network's memory via config +
pointer, and the pin gate + parity law (MCP-1/MCP-2, mcp_layer_status.md:71-84)
govern the tool surface the nodes see. MOVE (one sitting): wire ONE Phase-1 docker
node's bring-up through join_protocol; bank the cold-join receipt (node rebuilt its
law/config surface from the seed alone, hash-verified) as the second-consumer
proof. FALSIFIER: if the booted node cannot rebuild its surface from the seed alone
or a seal mismatch goes unreported, portability fails and the seed stays
proved-once; fix the seed, never hand-copy bytes into the image.

## What would make it SING (the one-paragraph answer)

Not the fleet size, not the payout math: the network composing its own curriculum.
Sweep -> lineages disagree -> a human adjudicates -> ground truth mints -> routing
flips -> the next sweep aims where the map was dark. Every layer pays and is paid in
the same currency, every claim resolves to bytes or fails loud, and the receipt
stream is the only memory the network needs to grow a brain. The current design has
all the organs and treats the most valuable one (divergence) as exhaust. The swing
is one inversion: stop testing consensus, start MINING disagreement.

## ERRATUM (hostile second pass, 2026-10-10, same sitting): FINDING 4 demand leg STRUCK

The second pass verdicted Finding 4 weakened and the verdict is correct on the bytes
(re-checked this sitting with sed/grep, commands and outputs below):

- The audit's named failure mode is COLD EXTERNAL demand: "post-dogfood external
  traffic was ~5 small tasks in ~20 min... our dogfood was the platform's biggest
  demand event" (GSTD_TOKENOMICS_AUDIT.md:109-111, sed -n '108,112p'). Internally
  generated sweeps are the same self-play class; they add zero external demand.
- The subsidy arithmetic runs the other way: "Fee income 0.001 GSTD/task submit vs
  payouts 0.002-0.0095/task: every task is net emission subsidy of 2-10x revenue...
  More nodes = more pool drain, zero added sink" (GSTD_TOKENOMICS_AUDIT.md:91-94,
  sed -n '88,95p'). A "demand mint" of internal tasks deepens the leak on the live
  platform.
- The leg I under-cited is the strong one: "Production ledger pre-lane: 13
  API/estate-tool animals, ZERO local animals, nothing anywhere passes the 0.85
  threshold, and the shapes summarize/classify/extract had NO history... the
  do-not-route death" (ROUTER_VOCAB_LANDED.md:25-31, sed -n '24,31p'). That is the
  starvation the divergence-adjudication loop actually cures: it mints graded
  fixtures for OUR capability ledger, independent of GSTD platform economics.
- Cite drift fixed: percolator novelty scoring is at garage
  garage_wizard_network_20261010/CARD.md:82 (grep -n "percolator" this sitting),
  not :92-94 (that block is the fox-counters paragraph).

CORRECTED CLAIM: divergence is the network's GROUND-TRUTH FOUNDRY, not its demand
engine. Strike "closes GB's demand gap by construction" and "the demand mint". The
adjudication surface is at most a FUTURE external demand door, unproven until a
non-estate human closes one adjudication. Perimeter sweeps run on staging/testnet
only (the subsidy arithmetic forbids mainnet sweeps until fees cover payouts).
Falsifier tightened to two arms: (1) within 20 adjudicated closures fed through
record_verdict (evidence_source gwp-adjudicated), zero capability-row changes (new
row, 0.85 threshold crossing, momentum badge flip) AND zero routing flips in
receipts.jsonl = the foundry loop is decorative; (2) if after 30 days every
adjudication and sweep task traces to estate-internal actors, the external-door
leg is self-play and is struck from every pitch. The one-sitting move is unchanged
(divergence_rank in the aggregator, GWAP backlog routing, record_verdict backfeed)
plus the one-line pitch fix in the perimeter card and GB reply addendum.

## Blind spots (honest)

1. I did not run any live TON testnet call: no staging endpoint exists yet (GB side
   pending); Finding 1's check is a spec, and its evidence is source bytes
   (token.ts, SettlementMaster.tact) I read this sitting, not an executed chain
   probe.
2. I did not verify server.ts:3305 or engine.ts line cites from the audit by
   opening those files this sitting (the two I leaned on hardest, token.ts and
   SettlementMaster.tact, I did re-read; the rest ride the audit's cites).
3. vast.ai pricing stays ESTIMATE-CLASS per the card (CARD.md:7-9); I did not fetch
   the pricing page; staging rate limits are UNOBSERVABLE until GB confirms
   (CARD.md:56-58).
4. The consensus harness v0 does not exist on disk yet (grep of tools/ for
   consensus returned only unrelated organs); Phase 1 is "tonight" per the card, so
   my moves assume the harness lands as the card describes, and the aggregator
   hooks (divergence_rank, lineage partition) are design-class until it does.
5. Sibling lenses' outputs unread by design (independence); convergence is flagged
   only against prior estate law (the duel cross-family law, the audit), which I
   re-derived or re-ran myself.
6. The GWAP adjudication path (Finding 4) names tools/arena_gwap.py as the organ
   but I did not open that file this sitting; its 110/110 claim is cited from
   ARENA_GWAP_BACKLOG_R3_20261010.md line 1, which itself carries the raw-check
   pointer.
