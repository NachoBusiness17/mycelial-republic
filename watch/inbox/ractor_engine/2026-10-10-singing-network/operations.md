# OPERATIONS LENS: the singing network perimeter (ractor run 2026-10-10)

Lens: operations (dispatch shapes, fold integrity, silent failures, cadence,
theater surfaces). Frame: Lessig four modalities over the GSTD closed
perimeter + heterogeneous consensus design (HIS spec) with the MCP toggle
layer (OURS). Every claim below was read or run this sitting; citations
inline. No em-dashes in this file.

## What I read (the evidence base, this sitting)

- watch/inbox/gstd_perimeter_design_20261010/CARD.md (the design under
  raction; two assertions A1/A2, two arms, phased)
- watch/inbox/gstd_gb_pitch_20261010/CARD.md (measured rate bucket, receipts)
- watch/inbox/gstd_basecamp_20260109/GSTD_TOKENOMICS_AUDIT.md (settlement
  theater, payout math, genesis-seal gap)
- watch/inbox/gstd_basecamp_20260109/ROUTER_VOCAB_LANDED.md (live GPS
  routing, garden family map, 4 verdict rows)
- watch/inbox/mcp_layer_status_20261010.md + watch/inbox/ractor50/mcp.md
  (five MCP surfaces, parity + loop-closure closed, R2-R4 open)
- watch/inbox/SEED_RIB_FORMAT_v0_20260926.md, watch/inbox/unisub_drop_
  20261010/CARD.md, watch/inbox/dead_salmon_airllm_drop_20261010/CARD.md,
  watch/inbox/garage_wizard_network_20261010/CARD.md, watch/inbox/mag_
  magatama_primer_20261010/CARD.md, memory/rib/RIB_LIVING_WEIGHTS_BY_
  NATURE.md, watch/inbox/gstd_distribution_thesis_20260109.md
- Organs: mag/consensus_gate.py (full), tools/gps_mcp/ledger.py (schema +
  record_verdict), reference/gstdcoin/gstdbot/src/core/platform-link.ts
  (cadence sites), reference/gstdcoin/gstdbot/src/blockchain/token.ts
  (recordEarning), mag/volume_fidelity.py (label-shuffle null model)
- state/CURRENT.md (live window canon; d06 lane, 2026-10-07)

## F1. LAW: A1 as CARDed measures the theater, not the settlement

The perimeter's A1 ("balance/ledger delta lands as claimed", CARD.md:13-14)
aims to close the settlement-theater finding "on a staging rail". But every
observable the node itself produces is the theater: I read the gstdbot
source firsthand this sitting. recordEarning in reference/gstdcoin/gstdbot/
src/blockchain/token.ts mints `hash: 'tx_' + randomBytes(16).toString('hex')`
with `status: 'confirmed'` for earnings that never touched a chain. The
audit banked the same class platform-side (server.ts:3305 claim fabricates
txHash; gstd_earned is a D1 counter, GSTD_TOKENOMICS_AUDIT.md:19-23). If
A1's assert reads node-local tx rows or the platform counter, the perimeter
does not close the finding, it launders it with our receipt culture behind
it, which is worse than the finding itself because now the bytes look
trustworthy. CONVERGENT: re-derived from two independent sources (the
audit doc + my own read of token.ts this sitting).

The fix is cheap and law-shaped: A1 asserts against an ON-CHAIN jetton
balance read for the receiving wallet (testnet toncenter GET, $0, ~40
lines) taken before and after the sweep, banked beside the platform
counter. Divergence is not a failure of the perimeter, it is the
instrument catching the theater, which is the whole point of a closed
perimeter. The receipt names which rail paid.

Falsifier: an A1 receipt that asserts "paid" with only node-local or D1
evidence in it. If chain-read deltas equal platform-claimed deltas on
every staging task, A1 passes honestly and the finding closes for real.

Move (one sitting, ~45 min): amend the CARD A1 block + write the
balance-reader into the harness spec (toncenter getExtendedBalance,
before/after deltas per node, wallet named in the receipt).

## F2. NORMS: A2 must route through the estate's own consensus-illusion
gate or the receipts violate LAW-CONS-ILLU-001

The estate already holds the law that qualifies this exact design.
mag/consensus_gate.py: agreement among correlated samples is an anti-signal
at small scale (calibration ladder: 2B AUROC 0.62, 7B 0.71, threshold
0.85; sub-3B unanimity is auto-UNVERIFIED; 120B mode-collapses to 0.09).
The Phase 1 fleet per ROUTER_VOCAB_LANDED.md section 2 is 14 models
dominated by TWO families (5 qwen2-class, 5 gemma-class) at 2-8B params,
plus one 27B experiment with zero verdicts. The CARD's A2 control is the
dead-salmon label-shuffle (CARD.md:19-20), which tests signal-vs-noise but
NOT family-correlated error collapse: qwen2.5:7b agreeing with
qwen2.5:3b-instruct is closer to one model agreeing with itself twice.

So the A2 spec needs two additions, both one-sitting:
1. Every majority/unanimity claim the aggregator emits routes through
   mag.consensus_gate.verdict() (the organ exists; it is an import + call)
   so correctness-flavored language is stamped CONFIRMED / UNVERIFIED /
   DISPUTED by the calibration ladder, never by raw agreement count.
2. The agreement matrix ships with family-block annotation: cross-family
   agreement is the headline metric; within-family cells are flagged
   correlated. GB's requirement ("nodes confirm the ability of different
   models to generate a consensus answer", CARD.md:4-5) is a mechanism
   claim and survives intact; what must not happen is a receipt that lets
   a reader upgrade "the fleet agreed" into "the answer was right".

Reusable null-model code exists: mag/volume_fidelity.py:355,398,407
implements the K-shuffle control arm pattern the dead-salmon law wants.

Falsifier: if cross-family agreement statistically matches within-family
agreement on the S/C/E shapes (family blocks do not explain the matrix),
the correlation worry is empty and the plain consensus rate stands as
signal.

## F3. FOLD INTEGRITY: "consensus-contrib rows" name a row class that
does not exist, and learning stats must read verdict_log, not capability

CARD.md:80 says the aggregator "feeds the GPS capability ledger as
consensus-contrib rows". I read the schema: tools/gps_mcp/ledger.py has
exactly two tables (capability, verdict_log). There is no consensus row
class and no migration sketched. The clean landing (no schema change):
sweep results bank as ORDINARY record_verdict rows, one per model per
task, real task_shape (summarize/classify/extract), evidence_source
prefixed "consensus-sweep-<id>-family-<family>". The dedupe triple
(model_id, task_shape, evidence_hash) keeps per-model rows distinct
because model_id differs; the Q28 gate recomputes sha256 from the banked
answer bytes at append, so sweep evidence arrives evidence_resolved=1 by
construction. The agreement matrix stays a receipt artifact under
watch/inbox/, which is where the workflow gate wants it anyway.

Two disciplines this implies:
- Any aggregate the network computes for learning reads verdict_log (the
  raw audit table; fails always land there), never capability (whose
  running means carry the LM7 positive floor clamp, a deliberate steering
  protection, ledger.py record_verdict docstring). Steering-protected
  means are for routing morale, not for measurement.
- Single-writer law: the aggregator is the ONLY process that writes the
  ledger during a sweep (ledger.py connection() is one lazy shared conn,
  "v0 is single-threaded anyway"). K nodes answer; one process banks.
  This sidesteps the SQLite cross-process lock class entirely.

Falsifier (the theater-surface check for this run): if sweep rows land
and the router's subsequent receipts.jsonl reason lines never change
(which model wins an ask), the "feeds the ledger" line is decoration and
the matrix is running output nobody consumes.

## F4. MARKETS/ARCHITECTURE: Phase 2's own rate-bucket arithmetic does
not close at the stated sizing

Measured base (pitch card, receipt-backed): all traffic from one host
shares one IP bucket; 6 of 11 requests 429'd at a ~16/min self-rate;
sustained usable is ~1 request per 10-15s (4-6/min). Cadence sites read
firsthand this sitting: heartbeat default 60s (platform-link.ts:85,
`start(intervalMs = 60000)`; production observed 600s beats per the
audit), fallback task poll every 30s (platform-link.ts:253, M4 note says
push-primary made polling fallback-only). CARD Phase 2 sizes "5 instances
x 10 nodes" (CARD.md:68-69). Ten nodes on one instance at default
cadences generate 21-30 requests/min against a bucket that 429'd at
16/min: 3.5-7x over budget per instance. Even Phase 1 (3-5 desktop nodes
behind the one docker bridge IP, the exact measured worst case) sits at
6-15/min. The CARD names the RATE-BUCKET LAW (CARD.md:40-43) and offers
the two mitigations, but never runs the law against its own sizing; the
silent failure mode is a perimeter that spends its first night in 429
backoff and reports "consensus rates" measured on a throttled fleet.

Move (one sitting): one shared platform-link per host, K node containers
multiplexed behind it (identity is a header string per the audit's
address-as-auth finding, so multiplexing is trivial), or a fleet-wide
token bucket at 4/min with queue depth banked; Phase 2 GO gates on GB's
whitelist answer, and the harness logs per-instance 429 counts as a
first-class metric so throttling is visible in every receipt.

Falsifier: a 10-node single-instance rig that runs a full sweep at
default cadences with zero 429s on staging. Then the bucket arithmetic is
wrong for staging and the sizing stands.

## F5. OURS (the toggle): the perimeter banks seed-MCP MACHINE-portability
(the B2-539-class IOU), not the doctrine's CLIENT-portability; the
self-learning instrument is coverage growth plus changed routing

CORRECTED (hostile second pass 2026-10-10: the original headline claimed
the perimeter IS the doctrine's second consumer; re-checked against
B2_181 and mcp_layer_status, the claim conflated two portability rungs;
this section is the corrected form).

The portability ladder, re-read from the bytes:

- RUNG 0 (banked, 2026-09-26): cold-of-knowledge. B2_181 receipt line 5
  and falsifier line 31: the cold client was tools/seed_mcp_
  cold_client.py, ESTATE-AUTHORED (written by the same lane as the
  server), run "on this box with the venv present"; the receipt's own
  honesty clause: "cold means cold-of-knowledge, not cold-of-machine;
  a fresh git-clone join with no venv is filed as self-feed B2-539".
- RUNG 1 (what vast Phase 2 actually banks): cold-of-MACHINE. A vast
  Linux instance, fresh container, no estate venv, booting from the
  kilobyte seed (tools/seed_mcp.py: seed://current, bounded sealed
  pointers, join_protocol; stdlib-only transport) discharges the
  B2-539-class IOU and nothing more. It is a real upgrade (different OS,
  no shared state) but it is the SAME client class relocated: whoever
  drives the cold boot on vast is our harness seat, because the
  gstd-node containers are not MCP clients at all (gstdbot speaks
  platform HTTP; platform-link.ts heartbeat/poll are plain HTTP calls,
  read firsthand this sitting).
- RUNG 2 (the doctrine's proved-portable): mcp_layer_status_20261010.md
  section 6 item 4 asks for a DIFFERENT-CLIENT cold boot, examples "a
  garage-guild bench or a Pierre-class external". That banks only when a
  client NOT authored by this estate consumes the seed. On the perimeter
  this is reachable at Phase 3/guild, and only if the bench runs its own
  agent stack against the seed; if we ship our harness seat to the bench
  and call it a second consumer, we have relocated rung 0 again and the
  doctrine item stays open.

The fold itself is unchanged and still the right one-afternoon move:
wire seed boot into the perimeter (kilobytes in, sealed pointers out),
because rung 1 is owed anyway and the sweep machinery needs the task
bank regardless. What changes is what the receipt may CLAIM.

The self-learning instrument (the acceptance bar "the network should
learn on its own as it grows") is untouched by the correction: GPS
capability-ledger coverage, meaning the set of (model, shape) pairs
holding evidence_resolved=1 rows, grows per sweep, AND the router's
ask() decisions change accordingly (reason lines cite pass-rate
threshold + cheapest-wins, ROUTER_VOCAB_LANDED.md section 4). Growth is
the memory; changed routing is the learning.

Falsifiers, tightened per rung: (a) vast containers built from fat
images anyway = the toggle is dead weight, cut it from the spec; (b) a
cold-join check count below 10/10 on the vast/Linux client = rung 1
fails, the B2-539-class IOU stands; (c) any "proved-portable" claim
whose cold client turns out to be estate-authored code relocated =
rung 2 did NOT bank, strike the claim and keep the doctrine item open;
(d) ledger rows growing across a growth window while zero routing
decisions change = accumulation theater, not learning.

## Blind spots (honest)

- I did not run tools/mcp_parity.py this sitting; the "five surfaces OK"
  claim is cited from mcp_layer_status_20261010.md, which reports its run
  today. Not verified by me.
- vast.ai prices are ESTIMATE-CLASS per the CARD (dynamically loaded
  page); I did not re-fetch pricing. All sizing arithmetic above uses the
  estate's own measured rate bucket, not vast economics.
- The staging platform does not exist in evidence yet (no endpoint, no
  testnet config); every claim about staging behavior is prediction, and
  F4's falsifier is the test.
- No consensus harness code exists in the tree to audit (grep of tools/
  and mag/ for the dispatcher/aggregator named in CARD.md "The harness"
  returns only unrelated files; mag/consensus_gate.py is the gate, not a
  harness). These findings are spec-level by necessity, which matches the
  topic's maturity.
- GB-side facts (whitelist willingness, push-primary on staging,
  testnet vs mainnet for A1) are unobservable from this seat; OWED to the
  GB thread, not assumed.

## Verdict

The design sings where it reuses estate law instead of inventing
parallel machinery: the honest additions are A1-on-chain (F1),
gate-through-consensus_gate + family blocks (F2), and the seed-boot
toggle (F5), all one-sitting each, all riding organs that already exist.
The lie waiting to be caught is A1 asserting on fabricated tx rows, and
the theater surface is an agreement matrix nobody's routing consumes.
Phase 1 tonight is correctly shaped ($0, desktop, 3-5 nodes) EXCEPT its
shared-IP bucket is the measured worst case; size its poll cadence first
(F4).

Erratum (hostile second pass, 2026-10-10): F5's original headline claimed
the perimeter delivers the doctrine's proved-portable seed-MCP upgrade.
Wrong rung: vast banks cold-of-machine (the B2-539-class IOU), proved-
portable needs a non-estate client (guild bench Phase 3). Corrected in
section F5; the fold move and the learning instrument stand unchanged.
