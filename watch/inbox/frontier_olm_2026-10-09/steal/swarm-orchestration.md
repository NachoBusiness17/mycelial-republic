# STEAL CARD: swarm-orchestration (frontier OLM 2026-10-09, ROUND 3)

Round 3, surgical per the round-2 review: R3 is rewritten to the file-mtime byte
truth (the round-1 six-card read was a head-truncation undercount at its own moment,
not tree motion) and the two verification-log header timestamps are relabeled (local
EDT mislabeled as Z); every other section is verbatim from the approved round 2. The
round-1 critique's three blockers are fixed in place, each with its own named fix: (1) the probe was dead as written (its September log source is gone,
verified again this session) and is re-scoped to forward capture plus backward
calibration on the verified-surviving week; (2) the machine-readable card JSON is
appended to this file per the 10-07 sibling convention (blocker 2); (3) FIND 1 is
restated as an operator-owned AMENDMENT of AGENTS.md:36, scoped to pre-dispatch width
shaping with no mid-flight cuts (blocker 3). Prior holdings are named in their own
block (the 10-07 card's fix-2 pattern). Grounding rule: abstracts were byte-verified
against the arXiv Atom API in round 1 (8,712 bytes, all three titles, all three
find-quotes, all three published timestamps; log item V.3); paper-body numbers are
carried by today's estate sweep receipt, which read two full HTML bodies end to end
(watch/inbox/frontier_olm_2026-10-09/sweep/swarm-orchestration-arxiv.md:19), and stay
OWED until the CASAgentGovernor repro repo is fetched. No em dashes; citations are
path:line or URL.

## R0. ROUND-1 CARRYOVER CORRECTIONS (both landed in round 1, restated)

1. Trajectory self-hits: the broad memory+corpus grep for "cost-aware backoff" hits
   only memory/trajectory/steps.jsonl, and the hits are self-referential rows: this
   run's own step logs recording the grep commands themselves (session_ids of this
   dwf run's actors, ts 2026-10-09T20:15Z and later; count at this round's measurement:
   4 rows, grep -c this session). Not prior banked analysis. Precedent documented at
   watch/inbox/frontier_olm_2026-10-06/steal/swarm-orchestration via arxiv.md:10 per
   the round-1 critique (that file not re-opened this round).
2. Formula direction, corrected: round 1 wrote "r >= 1/3 puts p_apply at 1", which
   inverts the finder's formula. Correct semantics, per the abstract ("a backoff rule
   that reduces intervention probability using a moving average of known induced
   events") and today's sweep receipt (:26): r_new = 0.7 r_old + 0.3 on an induced
   failure, else 0.7 r_old; the governor APPLIES REGULATION with probability
   p_apply = 1 - min(1, k r). So high induced-failure EWMA means intervene LESS: the
   rule breaks the feedback loop where the governor's own actions cause the failures
   it then punishes. Port consequence below (FIND 1).

## R1. PRIOR HOLDINGS (checked before re-banking; re-banking known work is waste)

(a) The EWMA kernel already exists: mag/signals.py:93-95, def ewma_update(old, new,
    *, alpha=0.3) returning alpha*new + (1.0-alpha)*old - the exact 0.7/0.3 shape of
    the paper's update. Second in-estate precedent: mag/persona_key.py:48, REFINE = 0.3
    EWMA weight for baseline updates. FIND 1's port REUSES this kernel; no fresh build.
(b) Maat's gate-as-control-point shape is already swept and shape-mapped twice:
    watch/inbox/frontier_olm_2026-09-30/sweep/swarm-orchestration-arxiv.md:74-78
    ("puts deterministic gates BETWEEN agents on handoff edges - PASS/WARN/BLOCK
    verdicts from a versioned anchor contract with 'no language model in the
    validation or scoring path'") and
    watch/inbox/frontier_olm_2026-10-08/sweep/evals-and-self-improvement-arxiv.md:150-153.
    Round 1's "we converged on that shape independently" is RETRACTED as a novelty
    claim. The genuinely new bytes in FIND 3 are only the false-alarm accounting
    numbers and their port, narrowed below.
(c) Today's sweep receipt already carries the paper-body numbers:
    frontier_olm_2026-10-09/sweep/swarm-orchestration-arxiv.md:26 (EWMA constants,
    k = 3.0 best +0.42 success over cost-blind at intensity 2, block-storm collapse
    hard blocks 0.1 -> 4.0 -> 7.6 per episode, governed 0.19 below ungoverned 0.31,
    and the portability note "hold new dispatch" mapping), :23 (SquidAgent task-shape
    rule), :38 (Maat 94 halts hand-reviewed, 35 false = 37 percent, 22 from
    circuit-breaker state carryover, v1 scorer withdrawal flipping four of six
    workflows, "determinism does not remove specification risk"), :44-47 (the banked
    list with overlaps). OWED status is therefore narrowed: the numbers are estate
    sweep receipts, read end to end by the sweep lane; still not independently
    re-fetched by this seat, and the CASAgentGovernor repro repo remains unfetched.
(d) No paper is re-banked outright: per the round-1 critique's census of prior
    swarm-orchestration cards and sweeps (10-03 x2, 10-04, 10-05, 10-06, 10-07),
    none carries 2610.09037, 2610.08647, or 2609.34017 as a steal; the two partial
    overlaps above are the only holdings contact.

## FIND 1 (PRIMARY): governor-as-disturbance -> pre-dispatch EWMA width shaping (OPERATOR-OWNED AMENDMENT OF AGENTS.md:36)

Paper: "When the Governor Becomes the Disturbance: Control-Generated Disturbance and
Cost-Aware Backoff in Governed Tool-Using Agents", https://arxiv.org/abs/2610.09037
(published 2026-10-06T19:39:24Z per the Atom entry, round 1; arxiv:comment ships a
Python repro script and code at github.com/CriticalAttentionSystems/CASAgentGovernor,
unfetched). Mechanism per R0.2 and R1.c.

LAW AMENDMENT REQUIRED (spec-before-behavior; this is the blocker-3 fix). The port
contradicts the standing law it cites and cannot ship as a silent code change:
AGENTS.md:36 (max-concurrency standing law) currently reads "the first rate-limit
contact at that shape is a HOLD signal ... not a width cut". Draft amendment, for the
OPERATOR to accept or reject: first contact remains a HOLD of the current shape
(unchanged); NEW: the dispatcher additionally shapes the NEXT fan-out's admitted width
by the induced-failure EWMA, m = 1 - min(1, k r) with k = 3 (deterministic
expected-width form; the paper-faithful alternative is per-child admission with
probability m); NO mid-flight cuts of running children - their internal retry
absorption stays the in-flight mitigation, exactly as the law holds today; the same
law's existing automated mitigation ("routes overflow to free lanes when the account
caps") is unchanged and composes with m. The width law's measured envelope
(AGENTS.md:35: Task agents clean at 3/6/10/12, width 10 = 109.4M tok/h, workflow
children max_concurrency 3) stays the base_width input; m only scales it. Adoption is
gated on the probe passing (below); until then this card changes no behavior.

Reuse and host (no fresh build): r comes from the owed --dwf-run tally mode
(registered at watch/inbox/burn_wave_20260926/B2_443_dwf_error_census_20260926.md:20;
its current _belongs predicate at tools/provider_error_tally.py:63-67 can never match
a sess_dwf-* child, receipt line 9), computed with mag/signals.py:93 ewma_update, and
m is read at fan-out construction time in the workflow script (the ask/fan-out
construction sites are string-built, verified this session at
.zcode/workflows/olm-mine.dwf.ts:272-289 for sweep asks and :398-403 for steal asks).
Water meter: r and m logged beside token burn (memory/runs/hermes_burn/usage.jsonl,
702,596 bytes, mtime 2026-10-07, round 1) so cost-blind governing shows as spend;
flow-vocabulary home tools/k8s_water_sim.py (imported by tests/test_k8s_water.py:19).

Why the paper lands on us: our failures are self-induced by our own width (AGENTS.md:35:
workflow children get maxAttempts 0 and die on the first 429/1302; a 50-wide dig
429-storms the account), which makes the paper's oracle-attribution limitation trivial
here, per the finder's why and sweep :26. The operator HOLD at first contact
(AGENTS.md:36, receipt watch/inbox/ENVELOPE_50W_HIT_20260926.md:9 decision line) is
the manual form of exactly m collapsing toward 0; the port automates that one signal,
nothing more.

## FIND 2: SquidAgent -> parallelize test lands in the gate's existing width-check family; context pack stamped at ask-construction sites

Paper: "SquidAgent: Parallelize Wisely, Coordinate Efficiently",
https://arxiv.org/abs/2610.08647 (published 2026-10-06T16:35:28Z, NeurIPS 2026 per
arxiv:comment, round 1). Rule per sweep :23: parallelize a layer only when
critical-path plus re-exploration plus alignment costs, in PREDICTED OUTPUT TOKENS,
beat serial. 2.2x vs Claude Code via fork-from-orchestrator-session and a
pre-generated shared convention block (sweep :45; OWED to repo).

File anchors (the blocker-3 minor fix; round 1 had none): the natural host is the
workflow gate's existing width family, not the quantizer: tools/workflow_gate.py:385
g8_width_check and :427 g8_width_shape_ok already adjudicate declared width at submit,
and the scenario dir now carries G8_width_shape.card.json and
G8_width_exception.card.json (dir listing this session; see R3 count note). The
estate's quantizer family is NOT the host: mag/auto_quantize.py quantizes storage
states (class Quantum :56, class AutoQuantizer :110, storage fns :372-447, read this
session), not token budgets. Port: a sibling check in the G8 family - a fan-out
declaring width W must carry a predicted-token estimate (per-child predicted output
tokens x critical path + re-exploration + alignment) and passes only when the parallel
sum beats serial; the estimate is computed at the same ask/fan-out construction sites
named in FIND 1. Context pack: the shared convention block is stamped as a pack
pointer appended at every child-ask construction site (sites verified at
olm-mine.dwf.ts:272-289 and :398-403). Honest gap kept: daily demand is watch/cron
heavy (17 watch + 12 cron vs 11 one-shot, commit 46ddc9d73 message, not re-derived),
so this test's customer is burn-wave fan-outs, not daily lanes.

## FIND 3: Maat -> the false-alarm accounting port (shape already held, claim narrowed)

Paper: "Maat: Independent Deterministic Contract-Based Governance for Multi-Agent LLM
Workflows", https://arxiv.org/abs/2609.34017 (published 2026-09-27T23:23:52Z, round 1).
Per R1.b, the deterministic-gates shape is already in holdings twice; per R1.c today's
sweep :38 already carries the accounting numbers (35 of 94 halts false = 37 percent,
22 from circuit-breaker state carryover across trials, v1 scorer crediting any halt
withdrawn, flipping four of six workflows) AND its direct filings. What THIS card adds
is only the concrete port shapes, with the absence verified:

(a) Gate-state fingerprint on FAIL rows: a registry FAIL row sampled this session
    (memory/workflows/REGISTRY.jsonl, "tree-doctrine-dig", ts 2026-09-25T18:52:02Z)
    carries ts/name/digest/script/verdict/checks and NO gate-state fingerprint - no
    baseline hashes, no stop-cert set - so carryover false alarms like Maat's 22 are
    unattributable post-hoc today. Port: stamp each FAIL row with the violation and
    citation baseline hashes plus the stop-cert set at fail time
    (configs/violation_baseline.json, configs/citation_lint_baseline.json; gate state
    readers at tools/workflow_gate.py:485, :503, :532).
(b) Halts-as-costs in the same water ledger as token burn (a halt is spend, not
    safety), wired next to FIND 1's r and m meters.
(c) The withdrawn-scorer law, verbatim in receipt language: never count a gate halt
    as positive evidence.

## R3. SCENARIO CARD COUNT (round-3 correction: round-1 undercount, not tree motion)

Byte truth (ls -la --time-style=full-iso configs/workflow_gate_scenarios/, this
session): G1-G7 card files all carry 2026-09-26 mtimes (07:58:36 through 17:39:30
-0400), and G8_width_shape.card.json (2026-10-05 01:27:22 -0400) and
G8_width_exception.card.json (2026-10-05 01:27:24 -0400) complete the nine; fixtures/
dates 2026-10-05 01:19:33. The directory therefore held NINE card files at every
moment of 2026-10-09, including both of this card's listing moments, and round 2's
"both true at their moments" sentence is RETRACTED as false about this card's own
observation history. Root cause of the round-1 six-card read, reproduced this session
by re-running the exact round-1 command shape (ls of the two baseline config files
plus the scenarios dir, piped through head -10): the pipe cut the multi-argument
listing after the sixth card name - the INSTRUMENT truncated; the tree never moved.
The current count is nine card files plus fixtures/ (full listing this session, no
head). AGENTS.md's "seven per-gate scenario cards" phrasing has been stale against
this byte truth since 2026-10-05. This is the census-denominator-law fabrication-smell
case: a drift was mis-attributed to the tree, and the mtime check before refreshing
is what caught it.

## ESTATE MAP SUMMARY

- gopher fleet: FIND 1, pre-dispatch width shaping m at fan-out construction,
  operator-amended law (AGENTS.md:36), no mid-flight cuts, retry absorption and
  free-lane overflow unchanged; FIND 2, width declarations carry the predicted-token
  parallelize estimate; FIND 3, FAIL rows gain gate-state fingerprints.
- water graph: three meters beside token burn in one ledger: induced-failure EWMA r,
  shaped width m (FIND 1), and halt counts (FIND 3). Module home
  tools/k8s_water_sim.py; signal host tools/provider_error_tally.py --dwf-run (owed
  build, B2_443:20).
- gate width family (named host for FIND 2; the estate quantizer is NOT it):
  tools/workflow_gate.py:385/:427 plus the G8 scenario cards; mag/auto_quantize.py
  verified as storage-state quantization, out of scope for token budgets.
- context pack: pack pointer stamped at every child-ask construction site
  (olm-mine.dwf.ts:272-289, :398-403, verified).
- percolator: no direct feed this round. sovereign mirror: no direct feed this round.
  Stated as such, not stretched.

## PROBE (round-1 probe verified DEAD as written; re-scoped to forward capture plus backward calibration on verified-surviving data)

Why the round-1 probe is dead (verified again this session, not assumed): its data
source, the seven daily CLI logs ~/.zcode/cli/log/zcode-2026-09-2{0..6}.jsonl, no
longer exists - find over the log dir returns 0 September files (7-day retention) and
the dir holds only zcode-2026-10-03.jsonl through zcode-2026-10-09.jsonl (43-123 MB
each). Both round-1 PASS conditions referenced September moments (run dd7232ea's
first terminal failure; the clean B2-25 window), so its falsifier could never fire.
The 896-event series survives only as census prose (B2_443:5,:10,:12), not as
extracted rows; watch/inbox/burn_wave_20260926/ holds no event dump (round-1 critique,
confirmed by this seat's round-1 dir listing).

Re-scoped probe, four steps, zero paid dispatch:

- Step 0 (the owed build, prerequisite): implement --dwf-run mode in
  tools/provider_error_tally.py exactly as registered (B2_443:20): accept a dwfrun id
  or log window, attribute sess_dwf-* children by sessionId prefix, split 429-retryable
  vs 1302 by statusMessage, and emit terminal-actor cuts (no model.network.completed
  after an actor's last failure; event vocabulary calibrated at B2-443).
- Step 1 (kernel reuse): feed the tally's per-window induced-failure indicator through
  mag/signals.py:93 ewma_update (alpha 0.3) for r, compute m = 1 - min(1, 3 r), log r
  and m beside token burn. Windowing and k are PRE-REGISTERED in the tally receipt
  before any replay, so the test cannot be re-tuned after seeing outcomes.
- Step 2 (backward calibration on surviving data, present and heavy): classify the
  surviving 10-03..10-09 logs with the tally. Raw signal verified this session:
  model.network.failed counts by day 794/941/333/331/501/139/110 and [1302] counts
  2498/3563/954/610/2072/560/502 (10-03 through 10-09). Honest limit: these greps span
  ALL transports (mains, Task agents, workflow children); the dwf-child cut and
  terminal-actor classification are what Step 0 adds, so a storm/clean pair in-week is
  NOT yet claimed. If the classified week yields at least one storm day (>= 1
  terminal dwf cut) and one clean day (zero), run the pre-registered replay
  immediately; retention is 7 days, so classification must happen before 10-10 or the
  window starts sliding away. If no in-week pair exists, fall through to Step 3.
- Step 3 (forward capture): keep the meter live beside token burn; evaluate on the
  next real storm regardless of Step 2's outcome.
- PASS (both, pre-registered, correct directions per R0.2): (1) on every storm
  window, m drops below 0.5 (r exceeds 1/6) at or before the first terminal-actor
  failure - the automatic backoff would have throttled the NEXT dispatch before
  actors died; (2) on every clean window, m stays at or above 0.5 throughout - no
  false throttle of measured-good width. FALSIFIER: any miss on either side kills the
  k=3 transfer to our failure shape, and the AGENTS.md:36 amendment stays unfiled.
- Cost: one tally build plus offline passes over on-disk logs; no dispatch, no spend.

## V. VERIFICATION LOG

Round 1 (2026-10-09 local EDT afternoon; the round-1 file landed 20:19Z per the
round-2 review's ls, matching this seat's own round-1 ls display of 16:19 local - the
original "~16:10-16:25Z" stamps were local EDT mislabeled as Z, relabeled round 3;
retained from the round-1 card): overlap greps reproduced (catalog title phrases 0/1/0, arxiv ids 0/1/0, zero Maat hits in
memory/frontier); Atom API fetch of all three ids (8,712 bytes) with all three titles
and find-quotes byte-present; estate citations walked (AGENTS.md:35,:36,:54;
workflow_gate function map; receipts B2_25/B2_443/AFTERPARTY/ENVELOPE present;
ENVELOPE decision line read).

Round 2 (2026-10-09 local EDT late afternoon; the round-2 file landed 20:51:52Z,
re-verified this session as the card's pre-edit mtime - the original "~16:45-17:05Z"
stamps were local EDT mislabeled as Z, relabeled round 3; all checks below ran that
session):
1. Log retention + storm scan: ls -la ~/.zcode/cli/log/ shows only
   zcode-2026-10-03..10-09.jsonl (seven files, 43-123 MB); find for
   zcode-2026-09-*.jsonl returns 0. Per-day counts run with grep -c:
   model.network.failed = 794/941/333/331/501/139/110; [1302] =
   2498/3563/954/610/2072/560/502 (10-03..10-09). Blocker 1's premise confirmed
   first-hand; the surviving week's raw signal measured, storm/clean classification
   NOT claimed (needs the tally).
2. EWMA kernel: mag/signals.py:93-95 read (def ewma_update(old, new, *, alpha=0.3),
   returns alpha*new + (1.0-alpha)*old); mag/persona_key.py:48 read (REFINE = 0.3).
   Holdings (a) confirmed.
3. Maat prior sweeps: frontier_olm_2026-09-30/sweep/swarm-orchestration-arxiv.md:74-78
   and frontier_olm_2026-10-08/sweep/evals-and-self-improvement-arxiv.md:150-153 read.
   Holdings (b) confirmed; round-1 independence claim retracted.
4. Today's sweep receipt read at :14-53: :19 (two full HTML bodies read end to end),
   :23 (SquidAgent rule), :26 (EWMA constants, k=3.0, block-storm numbers,
   portability note), :38 (Maat accounting + direct filings), :44-47 (bank list).
   Holdings (c) confirmed.
5. Scenario cards: ls shows nine card files + fixtures (list in R3); round-1 moment
   showed six + fixtures. Count fix verified.
6. mag/auto_quantize.py inspected (grep def/class): Quantum :56, AutoQuantizer :110,
   storage functions :372-447 - storage-state quantization, not token budgets.
7. Registry FAIL row sampled: grep -m1 FAIL memory/workflows/REGISTRY.jsonl ->
   tree-doctrine-dig row carries ts/name/digest/script/verdict/checks, no
   gate-state fingerprint. FIND 3(a) novelty confirmed.
8. Workflow contract + plumbing: .zcode/workflows/olm-mine.dwf.ts:398-409 read (the
   steer contract reads the banked file AND the returned card JSON, :405-408) and
   :268-293 read (sweep child asks string-built at :272-289). Blocker 2's contract
   and FIND 2's plumbing anchor confirmed; 10-07 sibling convention
   (watch/inbox/frontier_olm_2026-10-07/steal/swarm-orchestration.md:292-305) read
   and copied for the JSON block below.
9. Trajectory self-hits recounted: grep -c "cost-aware backoff"
   memory/trajectory/steps.jsonl = 4 (round 1 measured 1; the run kept logging).
   R0.1 wording updated to mechanism-based.

Round 3 (2026-10-09, this session; surgical per the round-2 review):
1. ls -la --time-style=full-iso configs/workflow_gate_scenarios/: G1-G7 mtimes all
   2026-09-26 (07:58:36-17:39:30 -0400), G8_width_exception 2026-10-05 01:27:24
   -0400, G8_width_shape 2026-10-05 01:27:22 -0400, fixtures/ 2026-10-05 01:19:33
   -0400: the directory held nine card files all day on 2026-10-09.
2. Round-1 instrument reproduced: the exact round-1 command shape (two baseline
   config files plus the scenarios dir, 2>&1 piped through head -10) returns exactly
   six card names (G1-G6) before the cut - the round-1 six-card read was pipe
   truncation, an undercount at its own moment, not tree motion.
3. Card file pre-edit state: 25,171 chars, mtime 2026-10-09 16:51:52 -0400
   (= 20:51:52Z), matching the round-2 review's ls figure.
4. R3 rewritten to that byte truth and the two log-header timestamps relabeled;
   nothing else touched; the machine-readable card's chars field re-sealed after
   these edits.

## OWED (kept from round 1, narrowed per R1.c)

- Paper-body numbers (0.19 vs 0.31, EWMA constants, k=3.0, +0.42, 2.2x, 37/22,
  scorer withdrawal flipping 4/6) are carried by today's sweep receipt read end to
  end (R1.c) and by the finder's confirmed reads; this seat has not independently
  re-fetched them, and the CASAgentGovernor repro repo is unfetched. Stay OWED until
  that fetch.
- The G8-family shape of the FIND 2 check (exact card schema for a predicted-token
  estimate) is design, not landed code; the gate family verified is the anchor only.
- The tally build (Step 0) and the pre-registration receipt (Step 1) are not started;
  this card banks the design and the probe, not the build.
- Task-shape census split (17 watch / 12 cron / 11 one-shot) cited from commit
  46ddc9d73's message, not re-derived from its receipt.
- Maat benchmark/demo repos (arxiv:comment links) unfetched.

## Machine-readable card (identical to the returned StealCard JSON)

Appended by the drafting seat per the 10-07 sibling convention
(watch/inbox/frontier_olm_2026-10-07/steal/swarm-orchestration.md:292-305); chars
counts this file's characters including this block, measured after the append.

```json
{
 "area": "swarm-orchestration",
 "steal": "Three mechanisms, holdings-reconciled, round 2. (1) PRIMARY, arXiv 2610.09037 (abstract byte-verified via Atom API round 1; read end to end by today's sweep receipt, watch/inbox/frontier_olm_2026-10-09/sweep/swarm-orchestration-arxiv.md:26): cost-blind regulation causes block-storm collapse (hard blocks 0.1 to 4.0 to 7.6 per episode; governed 0.19 below ungoverned 0.31); the backoff rule ties intervention to the EWMA of induced events, r_new = 0.7 r_old + 0.3 on induced failure else 0.7 r_old, regulation applied with probability p_apply = 1 - min(1, k r), k = 3.0 best. Port = PRE-DISPATCH width shaping: the next fan-out's admitted width multiplier m = 1 - min(1, 3 r), which is the operator HOLD at first contact made automatic; it REQUIRES an operator-owned amendment of AGENTS.md:36 (spec-before-behavior), scoped to next-fan-out shaping only, NO mid-flight cuts (children's retry absorption stays the in-flight mitigation), overflow-to-free-lanes routing unchanged; adoption gated on the probe. Kernel REUSED from mag/signals.py:93 ewma_update (alpha 0.3, the exact 0.7/0.3 shape; second precedent mag/persona_key.py:48), hosted in the owed --dwf-run tally (B2_443:20), read at the string-built fan-out construction sites (olm-mine.dwf.ts:272-289, :398-403). (2) arXiv 2610.08647 SquidAgent: parallelize a layer only when critical-path plus re-exploration plus alignment costs in PREDICTED OUTPUT TOKENS beat serial; lands as a sibling in the gate's existing width family (tools/workflow_gate.py:385 g8_width_check, :427 g8_width_shape_ok, G8_width_shape/G8_width_exception cards present), NOT mag/auto_quantize.py (verified: storage-state quantization, Quantum :56, AutoQuantizer :110); 2.2x and fork-from-orchestrator carried by sweep :23/:45, OWED to repo; context pack stamped as a pointer at every child-ask construction site. (3) arXiv 2609.34017 Maat: the gate-as-control-point shape is already held twice (10-09-30 sweep :74-78, 10-08 sweep :150-153), round 1's independence claim retracted; the genuinely new bytes are the false-alarm accounting (94 halts hand-reviewed, 35 false = 37 percent, 22 from circuit-breaker state carryover, v1 any-halt-credited scorer withdrawn flipping four of six workflows; sweep :38) ported as: gate-state fingerprint on FAIL rows (verified absent from REGISTRY.jsonl this session), halts counted as costs in the water ledger, never credit a halt as a win.",
 "source_url": "https://arxiv.org/abs/2610.09037",
 "estate_map": "gopher fleet: pre-dispatch width shaping m at fan-out construction via an operator-owned amendment of AGENTS.md:36 (first contact stays a HOLD of the current shape; m scales only the NEXT fan-out; no mid-flight cuts; free-lane overflow routing unchanged); water graph: three meters beside token burn in one ledger (induced-failure EWMA r, shaped width m, halt counts), module home tools/k8s_water_sim.py, signal host tools/provider_error_tally.py --dwf-run (the owed build, B2_443:20); gate width family (named host for the SquidAgent test; the estate quantizer is NOT it, mag/auto_quantize.py verified as storage-state quantization): tools/workflow_gate.py:385/:427 plus the G8 scenario cards; context pack: pack pointer stamped at every child-ask construction site (olm-mine.dwf.ts:272-289, :398-403, verified); percolator and sovereign mirror: no direct feed this round, stated as such. Prior holdings honored: EWMA kernel reused not rebuilt (mag/signals.py:93); Maat shape credited to the two prior sweeps, only the accounting port claimed as new (FAIL-row fingerprint verified absent today).",
 "probe": "Re-scoped FORWARD after the round-1 probe verified dead: its September CLI log source is gone (find returns 0; dir holds only zcode-2026-10-03..10-09.jsonl, 7-day retention, verified this session) and both old PASS conditions referenced unrecoverable September moments. Step 0: build the owed --dwf-run tally (attribute sess_dwf-* children by prefix, 429/1302 split, terminal-actor cuts; B2_443:20). Step 1: r via mag/signals.py:93 ewma_update (alpha 0.3), m = 1 - min(1, 3 r), logged beside token burn; windowing and k pre-registered in the tally receipt before any replay. Step 2: classify the surviving 10-03..10-09 logs (raw signal verified this session: model.network.failed 794/941/333/331/501/139/110 and [1302] 2498/3563/954/610/2072/560/502 by day; the greps span all transports, the dwf-child cut is the tally's job, so an in-week storm/clean pair is NOT yet claimed); if a storm day (>=1 terminal dwf cut) and a clean day (zero) both exist in-week, run the pre-registered replay immediately (retention is 7 days; classify before 10-10), else Step 3. Step 3: keep the meter live and evaluate on the next real storm. PASS (both): m < 0.5 before the first terminal-actor failure on every storm window; m >= 0.5 throughout every clean window. Falsifier: any miss kills the k=3 transfer and the AGENTS.md:36 amendment stays unfiled. Cost: one tally build plus offline passes over on-disk logs, zero paid dispatch.",
 "chars": 27587
}
```
