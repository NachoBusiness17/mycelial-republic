# ACCURACY LENS: the singing network (GSTD perimeter + heterogeneous consensus + MCP toggle layer), 2026-10-10

Seat: lens-accuracy, ractor on the Mag estate. Method: every primary card
named in the ask read in full this sitting; every organ claim below checked
against live code bytes or a live sqlite query run this sitting. Instrument
and moment for every count. No em-dashes. OWED marks anything I could not
verify.

## What I ran and read (the instrument list)

- Read whole: gstd_perimeter_design_20261010/CARD.md, mcp_layer_status_20261010.md,
  ractor50/mcp.md, SEED_RIB_FORMAT_v0_20260926.md, gstd_gb_pitch_20261010/CARD.md,
  gstd_basecamp_20260109/GSTD_TOKENOMICS_AUDIT.md + ROUTER_VOCAB_LANDED.md,
  unisub_drop_20261010/CARD.md, dead_salmon_airllm_drop_20261010/CARD.md,
  garage_wizard_network_20261010/CARD.md, mag_magatama_primer_20261010/CARD.md,
  memory/rib/RIB_LIVING_WEIGHTS_BY_NATURE.md, gstd_distribution_thesis_20260109.md,
  state/CURRENT.md (updated 2026-10-07, pre-dates today's cards; not load-bearing here).
- Code read: mag/consensus_gate.py (full), tools/gps_mcp/router.py (_evaluate/_select),
  tools/gps_mcp/ledger.py (schema, record_verdict, upsert_measurement, get_rate, momentum),
  tools/seed_mcp.py (refusal arms + join_protocol), mag/volume_fidelity.py (grep).
- Live query (this sitting, .venv python, tools/gps_mcp/gps_ledger.db3): 707 verdict_log
  rows total, 213 evidence_resolved=1; the 4 gstd-node-live-20261009 verdicts all
  resolved; capability rows qwen2.5:3b-instruct/classify = pass_rate 1.0 n=1,
  gemma2:2b/summarize 1.0 n=1, qwen2.5:7b/extract 1.0 n=1; 10 capability rows qualify
  at rate >= 0.85 and ZERO of them have zero resolved verdicts (the structural gap
  has not bitten yet, stated below as such).
- Grep over tools/*.py + mag/*.py: no consensus harness, no dead-salmon/label-shuffle
  instrument for MODEL consensus exists yet (the only label-shuffle control on disk
  is mag/volume_fidelity.py:13,414, a terrain-metrics NULL-MODEL CONTROL; the only
  consensus organ is mag/consensus_gate.py, unused by the perimeter CARD).

## Finding 1: A2 cites a paper negative control and ignores the estate's own live consensus law (CONVERGENT)

The perimeter CARD's A2 (gstd_perimeter_design_20261010/CARD.md:15-20) defines the
consensus metric as "majority/exact-match for closed-form shapes" with one guard:
the dead-salmon label-shuffle baseline (arXiv 2512.18792). The estate already holds
a stronger, code-live law the CARD never cites: mag/consensus_gate.py carries
LAW-CONS-ILLU-001 (memory/facts/ox_artifact.jsonl:348-354, verified to hold CID rows)
with a measured calibration ladder where unanimity is ANTI-SIGNAL at 120B (AUROC 0.09,
confident mode collapse) and barely above chance at 2B (0.62), plus two hard floors
already implemented: refusal-shaped responses stripped before unanimity is measured
(:70-94) and CONFIRMED unreachable below n >= 2 real answers (:62-64, :128-134, the
R3 fold row 4 degeneracy fixes). A raw majority rate over a small-model fleet is the
exact signal this law de-certifies; the CARD's heterogeneous models decorrelate errors
partially (different families) but the CARD never says so, never weights by tier,
never strips refusals. CONVERGENT: the dead-salmon card (dead_salmon_airllm_drop
CARD.md:21-26) independently demands mandatory negative-control arms on every
consensus-reading lane. Falsifier: dispatch K small models (2B class) on a task with
a planted wrong-majority answer; if the raw majority metric certifies it while
consensus_gate.verdict returns UNVERIFIED, the CARD's metric is the lie and the organ
is the truth. Move (45 min): harness v0 imports mag.consensus_gate.verdict per task,
aggregates consensus rate per (task shape, size tier), and the CARD's A2 gains the
organ citation + the two floors as acceptance clauses. The label-shuffle arm copies
the volume_fidelity.py NULL-MODEL CONTROL pattern.

## Finding 2: the network's memory banked the lax grader, not the receipt's honest reading

The toggle layer's "GPS capability ledger as the network's memory (measured pass-rate
per model per task shape)" is real and evidence-gated at the write path (Q28 recompute,
ledger.py:53-68, 310-355), but the memory itself disagrees with its own receipt. Live
query this sitting: capability (qwen2.5:3b-instruct, classify) = pass_rate 1.0,
sample_size 1. ROUTER_VOCAB_LANDED.md:117-124 says the same run's strict per-line
pairing was 3 of 5 and "treat qwen2.5:3b classify capability as weak, not proven-1.0".
The schema has no grader-class column (CREATE TABLE verdict_log, ledger.py:16-23:
ts/model/task/verdict/evidence fields only), so the honest downgrade lives in prose
the router never reads while the routing surface reads the inflated 1.0. This is the
self-learning law's fake-learning failure mode in miniature: the ledger learns the
grader's laxity, not the model's capability. Falsifier: re-run the classify task with
the strict pairing grader; if it still passes 5/5, the receipt's downgrade was the
error and the row stands; if it fails, the memory was inflated and every downstream
consensus-contrib row inherits the inflation. Move (60-90 min): add a grader field to
record_verdict + verdict_log, re-grade the 4 gstd-node-live rows under the strict
reader, and pin a test that a presence-only grader cannot write a 1.0 the strict
grader contradicts.

## Finding 3: the learning instrument has no sample-size floor and no evidence filter on the read path

"The network should learn on its own as it grows" currently accepts single-sample
learning as routing-grade truth. router.py:252-253: passes_threshold =
pass_rate >= constraints.pass_rate_threshold; sample_size is read into the Candidate
(:263) but never gates qualification, and the min_support=5 evidence gate exists only
in the generated route TABLE (gps_router_v0, per ROUTER_VOCAB_LANDED.md:15-19), not
the live router. Separately, the capability running mean (ledger.py:414-449) and the
router's hot read get_rate (ledger.py:712-721) do not filter on evidence_resolved:
494 of 707 verdict rows are self-attested (this sitting's count) and they move the
mean exactly like byte-verified rows. Byte-honest caveat: I counted the 10 qualifying
rows (rate >= 0.85) and zero of them have zero resolved verdicts, so TODAY's routing
surface does not ride purely unverified evidence; the gap is structural and unbitten,
stated as such. Falsifier: record three self-attested pass verdicts for a fabricated
(model, shape) pair through record_verdict with evidence_bytes absent; if the router
then qualifies that pair over an unresolved-but-real alternative, the read path
certifies self-attestation. Move (one sitting): Wilson lower bound (or a min-n floor
of 3) in _evaluate/get_rate, plus an evidence-weighted mean option; tests pinned
against both.

## Finding 4: A1's instrument is unnamed where the theater is proven, and Phase 3 has an unpriced scaler confound

The CARD's A1 (gstd_perimeter_design CARD.md:13-14) asserts "the paying node's
balance/ledger delta lands as claimed" without naming the read instrument. The audit
byte-proved why that matters: platform txHash values are fabricated (token.ts:387-396
'tx_'+randomBytes status 'confirmed'; /api/rewards/claim server.ts:3305 'tx_'+sha256;
GSTD_TOKENOMICS_AUDIT.md:20-25), gstd_earned is a platform D1 counter, the honest
public read is /api/v1/nodes (audit :131, "Permissionless read of the ledger: MET"),
idle accrual varies 152x between nodes via an unpublished scaler (Pi 0.0758/h vs our
0.000498/h, audit :70-72), and reputation moved 59 -> 49 WHILE earning (:75-78). Two
consequences: (a) a harness that cites txHash as settlement proof would certify the
theater A1 exists to catch; (b) the Phase 3 thousand-node payout test mixes node
ages/reputations/eras, so "payout holds at 1000 participants" is confounded by the
same scaler unless node age and reputation are recorded alongside every delta or the
fleet is age-matched. Falsifier: two nodes with equal task counts and different ages
diverge in per-task payout by more than noise; if the harness's A1 assertion passes
without controlling for it, it passed by luck, not mechanism. Move (20 min spec edit
+ one column in the harness): name /api/v1/nodes gstd_earned delta as THE A1
instrument, strike txHash from the assertion text, add node_age/reputation columns
to the aggregator's per-task rows.

## Finding 5: the unisub qualifier was dropped in translation (citation accuracy inside the fold)

The unisub drop card carries the paper's own qualifier verbatim: "(within shared
architectures - the abstract's own qualifier, do not overclaim cross-architecture)"
(unisub_drop_20261010/CARD.md:13-14). The perimeter CARD renders the same claim as
"the behavioral analog of today's unisub paper claim (disjoint models converge)"
(gstd_perimeter_design CARD.md:22-23), dropping the qualifier, and the GB addendum
(:84-87) repeats "the behavioral version of the convergence paper". Cross-model
behavioral agreement across DIFFERENT architectures is a fine standalone measurement;
calling it the analog of the paper's claim without the within-architecture scope is
the exact overclaim the source card forbade. OWED: I could not re-fetch arXiv
2512.05117 this sitting to re-derive the abstract's qualifier first-hand; the finding
stands on the disagreement between the two estate cards, both read this sitting.
Falsifier: the paper's abstract without the shared-architecture qualifier would void
the finding. Move (5 min): restore the qualifier in the perimeter CARD line and the
addendum, or scope the sentence to "behavioral agreement, which the paper does not
claim".

## What is decoration (priced)

- The CARD's "Feeds the GPS capability ledger as consensus-contrib rows" (CARD.md:80)
  names no write path. The ledger has an ungated fixture/operator door
  (upsert_measurement, ledger.py:579-619, "write a full measured row directly"); a
  harness that uses it bypasses Q28 entirely. Price: one line in the CARD naming
  record_verdict-with-inline-evidence as the only sanctioned write (fold into
  Finding 4's edit, same sitting).
- Seed-rib MCP cold boot: verified real this sitting, not decoration.
  tools/seed_mcp.py has the live refusal arms (void path :123,:161,:176; "SEAL
  MISMATCH vs source; bytes refused" :195) and join_protocol (:204). The mcp status
  doc's one honest gap stands: proved-once, not proved-portable
  (mcp_layer_status_20261010.md:114-117); the perimeter's new nodes are exactly the
  second consumer that would upgrade it.

## Blind spots (honest)

- No network fetches this sitting: arXiv 2512.05117 / 2512.18792 abstracts, the
  vast.ai pricing page, and the GSTD platform APIs were NOT re-hit; all platform
  data moments are the audit's 2026-10-09T05:03:47Z and the pitch card's own
  falsifier says re-verify same-day before sending GB anything.
- The Tact contract line cites (SettlementMaster.tact:120-135, GSTDJetton.tact:107-123)
  are quoted from the audit receipt, not re-read from reference/gstdcoin this sitting.
- I did not execute mag/consensus_gate.py or run the mcp_parity check; both organs
  were read as bytes, and their test suites were not run by me.
- The 707/213/10 counts are one db3 at one moment (2026-10-10, this sitting); the
  census denominator law applies, they are not constants.
- Win32 note: all my subprocess runs went through the harness Bash tool; no Python
  subprocess spawn was made by me, so CREATE_NO_WINDOW compliance is N/A this sitting.
