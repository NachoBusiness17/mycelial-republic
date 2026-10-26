# THE ESTATE BASELINE: CAPABILITY-LEDGER SPEC v1 (2026-09-29)

Status: ESTATE BASELINE, produced by the ractor panel (SEAT_A_SPEC.md,
SEAT_B_ADVERSARY.md, SEAT_C_EVAL.md, JUDGED.md in this directory:
watch/inbox/gps_baseline_ractor_20260929/). This is the document the
frontier return (per the inverted ask,
watch/inbox/game_platform_basecamp_20260929/OPUS_ASK_DRAFT_20260929.md
AMENDMENT 1) will be diffed against. Quality bar: if Opus cannot beat
this, the estate does not need Opus for this job. Supersedes the v0
semantics in tools/gps_mcp/ledger.py and tools/gps_mcp/router.py
(v0 shipped 28/28 tests,
watch/inbox/game_platform_basecamp_20260929/GPS_MCP_V0_20260929.md).
All numeric constants are DESIGN DEFAULTS (tunable, named); estimates are
marked ESTIMATE. Em-dash 0.

## 0. Standing of this document: routing authority is PROVISIONAL

Two clauses outrank everything else in this spec:

- PROVISIONAL AUTHORITY (from the adversary seat, kept): the ledger's
  right to influence routing is earned by passing the acceptance harness
  (section 7), because the delegation research banked the no-router
  ablation TIE (SuperScout, arXiv:2608.04804: "the handoff rather than
  the routing decision carries the result",
  watch/inbox/game_platform_basecamp_20260929/DELEGATION_RESEARCH_20260929.md).
  Until the harness passes, gps-mcp runs in INSTRUMENT mode:
  report_capability and receipts live, routing authority withheld.
- INSTRUMENT GUARANTEE: the ledger, gates, and receipts are valuable
  even if every kill rule fires (the estate's product claim is auditable
  verification, OPUS_ASK_DRAFT why-this-ask-shape item 3). No eval
  outcome deletes the instrument; outcome only grants or withholds the
  router.

## 1. Definitions (normative)

- TASK SHAPE: named, versioned class of work (fixture taxonomy:
  code_review, summarize, yes_no_decision, tool_call_parse,
  design_judgment per tools/gps_mcp/seed_fixtures.py). Free strings are
  not shapes; the registry (section 2) is the gatekeeper.
- VERDICT: a signed, chained claim that ONE ANSWER passed/failed ONE
  gate. Verdicts attach to artifacts; the ledger aggregates them.
- GATE: procedure mapping (input, answer) to pass/fail plus retained
  evidence. Classes G0-G3 (section 3).
- lb95: Wilson 95% lower bound on the weighted pass-rate.
- EFFECTIVE lb95 (eff_lb95): decay-blended lb95; the only rate the
  router may read (section 4.1).
- PROBE: scheduled ask whose purpose is measurement, receipt-flagged,
  budgeted (section 4.4).
- PRINCIPAL: key-holding writer identity. Endpoints and models are
  never principals and never write verdicts about themselves.

## 2. Ledger schema v1 (SQLite DDL, judge-amended)

```sql
CREATE TABLE task_shape_registry (
    task_shape        TEXT NOT NULL,
    version           INTEGER NOT NULL,
    owner_principal   TEXT NOT NULL,
    description       TEXT NOT NULL,
    canonical_gates   TEXT NOT NULL,      -- JSON list of gate refs
    created_utc       TEXT NOT NULL,
    PRIMARY KEY (task_shape, version)
);

CREATE TABLE principal (
    principal_id      TEXT NOT NULL,
    pubkey            TEXT NOT NULL,      -- ed25519 hex
    allowed_gates     TEXT NOT NULL,      -- JSON subset of G0..G3
    created_utc       TEXT NOT NULL,
    rotated_from      TEXT,               -- predecessor id on rotation
    expires_utc       TEXT NOT NULL,      -- fail closed when passed
    revoked_utc       TEXT                -- NULL = active
);

CREATE TABLE capability (
    model_id            TEXT NOT NULL,
    task_shape          TEXT NOT NULL,
    task_shape_version  INTEGER NOT NULL,
    passes              REAL NOT NULL,    -- WEIGHTED pass count (s3 weights)
    fails               REAL NOT NULL,    -- weighted fail count
    sample_size         INTEGER NOT NULL, -- raw verdict count
    pass_rate_raw       REAL NOT NULL,    -- weighted running mean (audit)
    pass_rate_lb95      REAL NOT NULL,    -- Wilson lower bound (routing)
    cost_usd_last       REAL,             -- last billed single-call cost
    first_verdict_utc   TEXT NOT NULL,
    last_verdict_utc    TEXT NOT NULL,
    half_life_days      REAL NOT NULL DEFAULT 14.0,
    -- per-class decomposition (AMENDMENT 6; replaces the gate_class_mix JSON
    -- blob: raw counts, weights applied on read, so the G3 cap is a plain
    -- column predicate evaluated atomically in the single write transaction):
    g0_passes INTEGER NOT NULL DEFAULT 0,
    g0_fails  INTEGER NOT NULL DEFAULT 0,
    g1_passes INTEGER NOT NULL DEFAULT 0,
    g1_fails  INTEGER NOT NULL DEFAULT 0,
    g2_passes INTEGER NOT NULL DEFAULT 0,
    g2_fails  INTEGER NOT NULL DEFAULT 0,
    g3_passes INTEGER NOT NULL DEFAULT 0,
    g3_fails  INTEGER NOT NULL DEFAULT 0,
    quarantined         INTEGER NOT NULL DEFAULT 0,
    updated_utc         TEXT NOT NULL,
    PRIMARY KEY (model_id, task_shape, task_shape_version)
);

CREATE TABLE verdict (
    verdict_id         TEXT NOT NULL,     -- content hash, row minus hashes
    ts_utc             TEXT NOT NULL,
    model_id           TEXT NOT NULL,
    task_shape         TEXT NOT NULL,
    task_shape_version INTEGER NOT NULL,
    cascade_step       INTEGER NOT NULL DEFAULT 0,  -- which step was judged (s3.4)
    verdict            INTEGER NOT NULL,
    gate_class         TEXT NOT NULL,     -- G0|G1|G2|G3
    gate_id            TEXT NOT NULL,
    evidence_hash      TEXT NOT NULL,     -- sha256 of canonical evidence (s3.3)
    evidence_uri       TEXT NOT NULL,
    receipt_ref        TEXT NOT NULL,     -- decision_id of the judged step
    principal_id       TEXT NOT NULL,
    signature          TEXT NOT NULL,     -- ed25519 over canonical row
    prev_sha256        TEXT NOT NULL,     -- house chain, genesis 64 zeros
    row_sha256         TEXT NOT NULL,
    PRIMARY KEY (verdict_id),
    UNIQUE (receipt_ref, gate_id)         -- idempotency, replay rejected
);
CREATE INDEX ix_verdict_cell ON verdict(model_id, task_shape, task_shape_version);
CREATE INDEX ix_verdict_evidence ON verdict(evidence_hash);  -- recycle detection

CREATE TABLE probe_log (
    probe_id     TEXT NOT NULL,
    ts_utc       TEXT NOT NULL,
    model_id     TEXT NOT NULL,
    task_shape   TEXT NOT NULL,
    budget_usd   REAL NOT NULL,
    spent_usd    REAL NOT NULL,
    receipt_ref  TEXT NOT NULL,
    PRIMARY KEY (probe_id)
);
```

`capability` is a MATERIALIZATION of `verdict`, rebuildable by replay;
rows whose backing verdicts fail chain/signature verification are set
quarantined = 1 (routing ignores them; report_capability says so). Chain
and signature mechanics reuse the estate house pattern verbatim
(append-only rows, row hash covers the row minus its own hash field,
deterministic key derivation, fail-closed when the cryptography package
is absent: mag/gwap_payload.py header, v1 section). Judge kills from
seat A incorporated: NO cost EWMA column (cost_usd_last only; EWMA
returns with a real billing feed), NO registry retirement ceremony.

Wilson bound used everywhere (z = 1.96):

    center = (p + z*z/(2n)) / (1 + z*z/n)
    half   = z * sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    lb95   = center - half

## 3. The verification-gate contract

### 3.1 Gate classes, evidence minimums, weights

| Class | What it is | Minimum retained evidence | Weight |
|---|---|---|---|
| G0 machine-checkable | deterministic: tests pass, JSON schema, exact/regex match, parse-and-execute | input hash, answer hash, checker id+version, environment hash (model tag + prompt template id + temperature), checker log | 1.0 |
| G1 dual-independent rubric | two principals score independently; agreement within tolerance = pass, disagreement = CHALLENGE (no verdict written) | both rubrics, both principals, agreement score | 1.0 |
| G2 operator judgment | human signs pass/fail | principal, one-paragraph rationale, artifact hash | 0.5 |
| G3 model-judge | non-answerer model grades | judge model_id, judge prompt hash, grade + self-confidence | 0.25, CAPPED |

G3 CAP (hard rule): a cell whose verdicts are entirely G3 can never
present eff_lb95 above the routing threshold; at least one G0/G1/G2
verdict is required before a cell may qualify. Weighted update:
pass_rate_raw = sum(w*v)/sum(w); passes/fails accumulate weights;
sample_size counts raw verdicts; gate_class_mix exposes composition.

### 3.2 Who can write

- Principal must be unexpired, unrevoked, signature-valid, and
  allowed_gates must include the class (the shared-surface law that
  model text proposes and only authorized actors effect:
  watch/inbox/SHARED_SURFACE_CONTRACT.json law 5; a verdict is an
  effect, not a suggestion).
- SEPARATION OF DUTIES: the principal that submitted the ask may not
  score G1/G2/G3 on the same receipt_ref. G0 is exempt (deterministic
  checks are re-runnable by anyone to identical bytes).
- RECUSAL RULE (judge blind-spot fix): a principal may not write
  verdicts on a (model, task_shape) cell operated by its own principal
  family (rotation lineage via rotated_from). The funded judgment lane
  (Nous/Hermes tier per AGENTS.md DRIVING LADDER 202609-28) may G3-judge
  only cells it does not operate.
- Every verdict cites receipt_ref of the judged step; verdicts without a
  receipt are rejected (the v0 inflatable hole,
  tools/gps_mcp/README.md IF WE GROW THIS item 1).

### 3.3 What a pass/fail artifact IS

evidence_hash = sha256 over canonical serialization of: exact input
bytes (hash + durable URI), exact answer bytes, checker id+version,
environment identity (model tag, prompt template, temperature). A
verdict is a statement about a (model, task_shape_version, environment)
triple. Anything less is a vibe about a brand.

### 3.4 Cascade-step attribution law (judge blind-spot fix 1)

A verdict judges ONE cascade step's OWN gated artifact:

- A step stopped for LOW CONFIDENCE without gate evidence writes NO
  verdict. Unconfident is not wrong; counting it as fail systematically
  poisons cheap-tier cells through ordinary cascade traffic.
- A cascade where only the final step was gated contributes exactly one
  verdict, to the final step's model, citing that step's receipt
  decision_id (cascade_step recorded on the verdict row).
- Multi-step cascades MAY gate intermediate steps when a G0 gate exists;
  each gated step then contributes its own verdict. Ungated steps never
  do.

## 4. Routing and escalation policy v1

### 4.1 Selection (router reads ONLY these)

A candidate QUALIFIES iff all hold:
1. passes hard constraints (v0 rule a unchanged: max_cost_usd,
   max_latency_ms against live config price, never ledger price; truth
   and price stay on separate clocks, v0 design decision 3).
2. n >= n_min (DEFAULT 20) AND pass_rate_lb95 >= threshold (DEFAULT
   0.85, caller-overridable; v0 constant kept).
3. eff_lb95 >= threshold, where
       w = exp(-ln2 * age_days / half_life_days)
       eff_lb95 = w * lb95 + (1 - w) * 0.5
   with age_days since last_verdict_utc, p0 = 0.5 pessimistic prior.
   Decay only demotes; freshness is re-earned by new verdicts (answers
   v0 critique item 3, tools/gps_mcp/README.md not-doing list).

Choose cheapest qualifying (v0 rule c unchanged; deterministic tiebreak
by tier rank then model_id, v0 _select). If none qualify but rows exist:
route cheapest constraint-passing AND schedule a forced probe round
(k = DEFAULT 5 fresh G0-gated items) on the stalest rows.

### 4.2 Exploration

- No history (all cells n < n_min or absent): v0 rule kept, designated
  exploration tier, exploration: true.
- Exploration traffic is MEASUREMENT traffic: every exploration answer
  that can be G0-gated MUST be gated; those verdicts are the cell's seed
  history. Exploration is how cells graduate.
- No random epsilon, no UCB/bandit in v1 (deferred until the harness
  licenses them; the estate does not ship unmeasured cleverness).

### 4.3 Escalation decision boundaries (the amendment's core)

Four named triggers; each may authorize a climb; each writes itself to
the receipt as trigger. Max 3 tiers and prior-answer context attach are
inherited from v0 (tools/gps_mcp/router.py).

- T1 CONFIDENCE (earned only): conf < min_confidence (DEFAULT 0.8) AND
  calibration_state = verified for that (model, shape): rolling ECE over
  last m = DEFAULT 50 gated answers <= e_max = DEFAULT 0.10. If
  calibration is unverified or poor, a low confidence triggers T4, not
  T1: an uncalibrated confidence number is noise wearing a uniform.
- T2 ECONOMICS (ADVISORY until measured): fires only when
  P(fail_i) * (C_rework + price_j) > price_j + P(fail_j) * C_rework,
  with P(fail) = 1 - eff_lb95 (ledger estimate, not self-confidence) and
  C_rework a MEASURED constant from the acceptance harness rework data.
  Until C_rework is measured, T2 logs its fields on the receipt and
  DOES NOT fire (judge demotion: no precise-looking arithmetic on
  invented constants).
- T3 BLIND SPOT: chosen cell n < n_min: climb to cheapest model with
  n >= n_min that qualifies; if none, ship flagged low_evidence: true.
- T4 STALENESS: eff_lb95 < threshold while raw lb95 >= threshold (decay
  demotion): do NOT climb; ship current-tier answer flagged stale: true
  and schedule the forced probe. Staleness is a knowledge gap, not a
  difficulty signal; frontier tokens never patch measurement holes.

### 4.4 Probe budget (the organ's leash)

Forced probes are capped per shape per week at probe_budget_usd DEFAULT
0.50 USD (ESTIMATE; max 2.50 USD/week for a 5-shape fleet; recalibrate
from real billing after week one). Over-budget probes wait for the next
window; routing degrades to current behavior with stale flags.
probe_log makes the measurement appetite auditable.

## 5. Receipt-row grammar v1

Append-only JSONL, ONE ROW PER DECISION STEP (v0 invariant), hash-chained
per the house pattern. Required fields:

```json
{"seq": 0, "ts_utc": "", "decision_id": "", "trace_id": "",
 "cascade_step": 0, "task_shape": "", "task_shape_version": 0,
 "chosen": null, "considered": [], "reasons": [],
 "trigger": "none|T1_confidence|T2_economics|T3_blind_spot|T4_staleness",
 "cost_usd": 0.0, "cumulative_cost_usd": 0.0,
 "confidence": null, "confidence_source": "endpoint|none",
 "calibration_state": "verified|unverified|poor",
 "exploration": false, "probe": false, "stale": false, "low_evidence": false,
 "ledger_snapshot_hash": "", "principal_id": "",
 "prev_sha256": "", "row_sha256": ""}
```

Each considered[] entry: {model_id, n, lb95, eff_lb95, cost,
qualifies, reason_code}. decision_id is the verdict-binding key
(section 3.2). Receipts remain the audit spine: a decision we cannot
audit did not happen (v0 law).

## 6. Scope fences (pre-registration, from the adversary seat)

The ledger keeps routing authority only while these remain true; each is
falsifiable and the acceptance harness measures every one:

- F-S1 VERDICT SUPPLY: machine-gated verdicts fill an active cell to
  decision-grade n (order 300, ESTIMATE) within one drift half-life.
- F-S2 COST DISPERSION: qualifying models differ in stable price by
  >= 10x on the same shape (fixtures assert 30x mid-to-frontier,
  tools/gps_mcp/seed_fixtures.py; fixtures are literals, not
  measurements).
- F-S3 CONCENTRATION: top 5 shapes carry >= 80% of traffic (ESTIMATE).
- F-S4 INVISIBLE-FAILURE HETEROGENEITY: shapes exist where cheap models
  are confidently wrong often enough that per-instance confidence cannot
  catch it but the population rate would (THE crux; harness M6
  measures it).
- F-S5 DRIFT SLOWNESS: capability half-life exceeds verdict accumulation
  time.
- F-S6 GATE ECONOMICS: gate cost per cascade instance <= ~10% (ESTIMATE)
  of the escalations the ledger avoids.
- F-S7 HARNESS VICTORY: the ledger arm must win section 7 under its
  pre-registered kill rules, or routing authority is withheld
  (instrument mode, section 0).

## 7. Acceptance harness (from the eval seat, judge-fixed)

Four arms over ONE router boundary (arms are configs, never forks):
Arm 1 LEDGER runs THIS spec's selection exactly (4.1-4.4; the judge's
fix: the eval licenses an artifact, not a concept); Arm 2 CASCADE:
tier-order-first, confidence-gated, ledger blindfolded; Arm 3
CLASSIFIER: small local model picks tier from task text; Arm 4
FIXED-MID floor. Paired: every item runs through all arms; identical
gates; seed/eval split mandatory (ledger history from a DISJOINT seed
corpus, deterministic per tools/gps_mcp/seed_fixtures.py patterns);
frontier tier as test double only (unfunded per AGENTS.md DRIVING
LADDER; the harness measures routing quality at fixture prices, not
frontier economics).

Metrics: M1 cost-per-verified-solve (whole trace charged: calls + gates
+ re-climbs; ARM 1 ALSO CARRIES amortized probe + seed-corpus + audit
spend from probe_log and M5, judge blind-spot fix 2); M2 verified-solve
rate (kill rule, not a powered claim at n = 200); M3 escalation waste
(non-final tier cost / total); M4 stale-rate incidents via mid-run
test-double behavior collapse on one model/shape (50 fresh requests,
count routes to the collapsed model + detection latency in fresh
verdicts); M5 operator minutes per accepted verdict by gate class; M6
ECE per model per shape.

Kill rules (pre-registered): K1 Arm 1 not >= 10% better than BOTH Arm 2
and Arm 3 on M1 with paired 95% CI excluding zero => instrument mode
only. K2 Arm 1 solve rate > 3 points below Arm 2 (ESTIMATE threshold
visible at n = 200) => kill regardless of cost. K3 > 5 stale incidents
or detection latency > 10 fresh verdicts => update loop too slow,
redesign decay/probes before rerun. K4 G2 verdicts > 5 operator-minutes
each or seed filling > 1 operator-day => cap ledger at G0-only shapes.
K5 ANY red-team success (forged verdict accepted, replay
double-counted, one evidence_hash for two answers, cell inflated over
threshold with broken chain) => gate contract fails closed until patch
and rerun.

## 8. Falsifiers and residuals

| # | Failure mode | Defense | Residual |
|---|---|---|---|
| F1 | Verdict poisoning (colluding writer) | G0 determinism, G1 dual-independence, G3 cap, principal keys + recusal, chain audit | two-principal G1 collusion, operator capture; detected as verdict clusters from one pair |
| F2 | Stale-rate drift between verdicts | decay + forced probes | window up to half_life_days; K3 measures real incident rate |
| F3 | Exploration exploitation / cold-start lock-in | shape registry, probe budget, n_min = 20 fast graduation | operator-blessed shape with adversarial content mix poisons one cell |
| F4 | Taxonomy leak (Goodhart) | task_shape_version + environment hashes make drift visible | visible is not prevented; harness F4-check: within-name vs between-model variance |
| F5 | Evidence recycling / replay | UNIQUE (receipt_ref, gate_id), evidence_hash index, hash chain | mutated-artifact hash minting; detected by near-duplicate input clustering |

## 9. What this baseline deliberately does not do

No multi-tenant authz beyond the principal table; no streaming; no
bandit/UCB (deferred, 4.2); no automatic price feeds (cost_usd_last is
operator or fixture written); no frontier-tier real spend anywhere in
the harness (unfunded, AGENTS.md DRIVING LADDER 2026-09-28); single
writer SQLite; no claim that design_judgment at G2 weight is
decision-grade (it is directional). The spec defers rather than papers
with guesswork branches (build discipline, AGENTS.md).

## 10. How the frontier return beats this baseline (diff contract)

The Opus return is BETTER than this baseline only if it, concretely:
1. tightens a gate-class definition or evidence minimum without adding
   unfalsifiable ceremony;
2. replaces a DESIGN DEFAULT with a measured constant sourced from a
   runnable check (or argues a better prior with named evidence);
3. finds a falsifier not in section 8 AND a defense that survives its
   own stated residual;
4. simplifies (deletes a field/trigger/table) at equal auditable
   power; or
5. repairs a blind spot this panel named in JUDGED.md section 4 beyond
   the fixes already incorporated here.

Anything else (prose polish, re-derivation of commodity routing
plumbing, unearned thresholds) is noise by the estate's own no-fabrication
law. Em-dash count: 0.

## AMENDMENTS (append-only; Y9 lane, batch 2, 2026-09-29)

Patches from the night-burn hostile implementer read (N2,
watch/inbox/hydrology/X5_NIGHT_READ.md digest of
watch/inbox/mates_leave_protocol/NIGHT_BURN_output_20260930.jsonl):
three production-failure kills, one paragraph each, plus N2's five
missing test predicates. The body above is unchanged; where an
amendment contradicts a section above, the amendment wins (the same
rule the JUDGED.md fixes used).

### AMENDMENT 1 (kill 1: T1 n_min/m=50 dead-code gap; amends 4.3 T1)

The calibration window is m_eff = min(m, n) gated answers, floored at
n_min: a routing-qualified cell short of the old m = 50 (that is,
n_min <= n < m) computes its rolling ECE over the n gated answers it
actually has and may present calibration_state = verified from
n = n_min, so T1's reachability boundary now equals the routing
qualification boundary and the dead-code window (verdicts 20 through
49, where a cell could be routed to yet T1 could never fire because m
= 50 was unreachable) is closed. A cell with n < n_min stays
calibration_state = unverified and low confidence routes to T4 exactly
as before. The shorter window's extra ECE variance is not papered
over: harness M6 (ECE per model per shape) measures it and e_max =
0.10 remains a DESIGN DEFAULT tunable from that data.

### AMENDMENT 2 (kill 2: chain concurrency and fork story; amends 2 and 9)

The concurrency story is: one writer, serialized transactions, audit
with fork detection. Every verdict INSERT runs in WAL mode inside a
BEGIN IMMEDIATE transaction that reads the chain tip, checks
prev_sha256 against the tip's row_sha256, derives row_sha256, and
commits; on chain contention (tip moved between read and write, or
SQLITE_BUSY) the writer waits out busy_timeout (DESIGN DEFAULT
5000 ms) and re-bases the row onto the new tip inside a retried
transaction, so contention delays, never forks. The fork-test
predicate (N2's first-test-written ask) is: plant two rows sharing one
prev_sha256 in a test copy of the ledger and the audit must flag the
fork and quarantine every cell fed by the losing branch; drive N
concurrent submissions through the real writer path and the result
must be exactly one linear chain, zero forks. In production the
periodic audit (replay from genesis, recomputing every hash link)
resolves any detected fork by longest-valid-chain-wins: losing-branch
verdicts are quarantined, never deleted (append-only law), capability
rows rebuild by replay, the incident files a receipt, and K5 red-team
owns the forging paths that could still mint a fork.

### AMENDMENT 3 (kill 3: enforceable recusal; amends 2 principal DDL and 3.2)

The principal table gains `operator_id TEXT NOT NULL` (DESIGN DEFAULT
'estate'): a stable operator identity inherited unchanged across key
rotation, with the principal family defined as the closure of
rotated_from under one operator_id, which is the key the 3.2 recusal
rule needs and the v1 schema lacked. Enforcement is two-layer, not
aspirational: (a) insert-time, the single verdict writer resolves the
operators of a (model, task_shape) cell from the receipt spine
(principal_ids on decision steps whose chosen model is the cell's
model) plus the shape's registry owner_principal, and rejects any
G1/G2/G3 verdict whose scorer principal_id belongs to the same
operator family; (b) audit-time, the chain audit re-verifies recusal
for every committed verdict against the same receipt spine, and a
violation quarantines the affected cell (rebuilt by replay) rather
than silently persisting. G0 stays exempt per 3.2. K5 red-team adds
the same-operator verdict attempt: rejected at insert, and flagged by
audit if smuggled into a copy.

### AMENDMENT 4 (N2's five missing test predicates; first test wave of any build on this spec, before routing authority)

1. CHAIN FORK DETECTION: a planted fork (two rows sharing one
   prev_sha256) in a test copy is flagged by the audit and the cells
   fed by the losing branch are quarantined; N concurrent writer
   submissions through the real path yield exactly one linear chain.
2. G3 CAP TRANSITION: an all-G3 cell never qualifies above threshold
   regardless of eff_lb95; after exactly one G0/G1/G2 verdict lands,
   qualification flips iff the cap rule is now satisfied, and no
   observer can catch an intermediate state where the G3-only cell
   qualifies (the capability update is atomic inside the write
   transaction).
3. DECAY MONOTONICITY VS PROBE INJECTION: with no new verdicts,
   eff_lb95 is non-increasing in age; fresh forced-probe verdicts
   never lower eff_lb95; a probe round on a decayed cell restores
   eff_lb95 monotonically along the 4.1 arithmetic and never above the
   raw lb95 the same evidence supports.
4. IDEMPOTENCY UNDER REPLAY: re-inserting a committed verdict (same
   verdict_id, and the same (receipt_ref, gate_id) pair) is rejected
   and leaves passes, fails, sample_size, pass_rate_lb95, and eff_lb95
   byte-identical; rebuilding capability by replay from verdict
   reproduces the live rows exactly.
5. T2 ADVISORY DIFFERENTIAL: with C_rework unmeasured, a case
   engineered to satisfy T2's arithmetic fires no climb and logs its
   fields with trigger not equal to T2_economics, and the routing
   outcome is byte-identical to a run with T2 compiled out; once
   C_rework is set from harness rework data, the same case climbs.
   The paired runs prove the advisory branch cannot leak into routing
   and the measured branch engages.

Em-dash count in amendments: 0.

## AMENDMENTS, batch AD4 (append-only; 2026-09-30; the two N2 kills from
watch/inbox/last_mile_20260930/NIGHT_BURN_RECEIPT.md, the same burn batch 2
answered from the hydrology digest. Later amendments win over earlier ones
where they conflict, the same rule the body uses. One marked exception to
batch 2's "body unchanged" practice: AMENDMENT 6 applies its DDL delta to
section 2 in place, comment-marked, because a cap the schema cannot enforce
is the kill itself.)

### AMENDMENT 5 (kill 1: the T1 dead-code window; amends 4.1, 4.2, 4.3 T1 and T3; SUPERSEDES AMENDMENT 1)

The kill: a cell qualifies for routing at n_min = 20 but T1 needs a rolling
ECE over m = 50 gated answers, so for verdicts 20 through 49 a low-confidence
event fires nothing (T1 is unarmed because calibration over a full window
does not exist yet; T4 is inapplicable because a fresh cell cannot be
decayed): routed yet unescalatable. AMENDMENT 1 closed the window from the
calibration side (present calibration_state = verified from n = n_min over
m_eff = min(m, n) answers). This amendment supersedes it and closes the
window from the routing side, the fail-closed side:

- 4.1 rule 2 gains the conjunct n >= m: a cell QUALIFIES only when its
  calibration window is full (m = DEFAULT 50, the same constant T1 reads).
  n_min is RETIRED and m becomes the single boundary: the 4.2 exploration
  band is n < m, and 4.3 T3's predicate becomes "chosen cell n < m" with the
  climb target "cheapest model with n >= m that qualifies". Since
  min(m, n) = m for every routable cell, AMENDMENT 1's m_eff machinery is
  vacuous and retired with it.
- Cold-start behavior, explicit: n < m is measurement territory, never
  authority territory. Cells there are reached only by exploration (4.2) or
  the none-qualify fallback (4.1: cheapest constraint-passing plus a forced
  probe round on the stalest rows), and every receipt citing such a cell
  carries calibration_state: unverified. A low-confidence answer in this
  band DOES NOT climb: trigger stays none, the confidence value and
  calibration_state land on the receipt. The miss is auditable, not patched
  with frontier tokens (T4's law, applied to calibration holes).
- At n >= m the window is full by construction: T1 is reachable exactly when
  the cell is routable. ECE <= e_max gives verified and T1 may fire; ECE >
  e_max gives poor and a low confidence still does not climb, receipt says
  poor. The 4.3 sentence "If calibration is unverified or poor, a low
  confidence triggers T4, not T1" is corrected: T4 stays staleness-gated;
  unverified or poor calibration means no confidence-driven climb at all,
  trigger none.

Why this resolution is the fail-closed one and the other two candidates are
not: (a) arming T1 at n_min under a labeled unverified state would fire a
tier climb on a number the spec's own T1 preamble calls "noise wearing a
uniform", and the judge explicitly kept "T1 fires only when
calibration_state = verified" (JUDGED.md 40-41); (b) AMENDMENT 1's
verified-from-20 redefines the verification bar downward to make the trigger
reachable, which papers over the gap instead of closing it (the T2 precedent:
no precise-looking arithmetic on unproven quantities; M6 measuring the
short-window variance later does not verify the label now). Gating routing on
m keeps verified meaning exactly one thing, a full-window ECE, and withholds
routing authority until the instrument that justifies it exists (the section
0 pattern applied at cell granularity). Cost, named: graduation slows from
20 to 50 gated verdicts; F3's "n_min = 20 fast graduation" defense is
superseded; the forced-probe loop and exploration's G0-gated measurement
traffic already fill exactly this band, and F-S1 still expects machine-gated
fill to decision-grade n within one drift half-life, so the fence survives.

### AMENDMENT 6 (kill 2: the G3 cap made atomic; amends 2 DDL in place, 3.1, 4.1 rule 4)

The kill: the G3 cap is stated as a hard routing rule (3.1) but the v1
schema cannot enforce it atomically. gate_class_mix was a pre-blended JSON
blob, so "is this cell all-G3?" meant parsing a denormalized summary instead
of reading keys; and the behavior when the first G0 verdict lands on an
all-G3 cell was unspecified (blend the new weight into the running mean?
recompute from the verdict log? accept float drift between the two?). Fix in
three parts, the first applied to the section 2 DDL in place:

1. PER-CLASS DECOMPOSITION (in the DDL, comment-marked): capability drops
   gate_class_mix and carries eight raw counters, g0_passes / g0_fails /
   g1_passes / g1_fails / g2_passes / g2_fails / g3_passes / g3_fails
   (INTEGER NOT NULL DEFAULT 0). Raw counts, weights applied on read;
   report_capability derives the class mix from the columns; the counters
   rebuild exactly by replay (order-independent integers, no float drift,
   which also strengthens AMENDMENT 4 predicate 4).
2. ATOMIC UPDATE RULE: every verdict commit is the single AMENDMENT 2
   transaction and does exactly this: increment the one per-class counter
   pair the verdict's gate_class selects, then recompute the blended columns
   by closed form over all counters: passes = sum over classes of
   (w_c * passes_c), fails = sum over classes of (w_c * fails_c), with w
   from 3.1 (G0 = G1 = 1.0, G2 = 0.5, G3 = 0.25); sample_size = sum of raw
   counts over classes; pass_rate_raw = passes / (passes + fails);
   pass_rate_lb95 by the section 2 Wilson formula on the weighted counts
   (v1 convention unchanged). The v1 body's incremental running-mean update
   is superseded by this closed form: a cell is never a partially blended
   intermediate state.
3. RECOMPUTATION AT FIRST NON-G3 VERDICT: there is no special case, which is
   the fix. The first G0 (or G1 or G2; 3.1 lifts the cap on any of the
   three) is just another counter increment inside the same transaction, and
   the cap becomes a plain qualification conjunct, 4.1 rule 4: n_non_g3 =
   g0_passes + g0_fails + g1_passes + g1_fails + g2_passes + g2_fails >= 1,
   evaluated against committed columns at routing time. An all-G3 cell's
   qualification therefore flips exactly at the commit of that verdict and
   no observer can catch an intermediate state (single-writer SQLite,
   serialized transaction): AMENDMENT 4 predicate 2 becomes implementable
   as written. The 3.1 sentence "a cell whose verdicts are entirely G3 can
   never present eff_lb95 above the routing threshold" is restated: the cap
   is a composition gate on qualification, not a claim about the eff_lb95
   arithmetic (an all-G3 cell may hold a numerically high lb95; it still
   does not qualify).

No ledger migration: tools/gps_mcp/ledger.py is v0 code this spec already
supersedes; the production build implements the amended DDL, and
gps_ledger.db3 is fixture data.

Em-dash count in batch AD4: 0.

## AMENDMENTS, batch AH11 (append-only; 2026-09-30; the Wilson-denominator
kill from the V1 multifamily duel, deepseek's sharpest find in
watch/inbox/last_mile_20260930/V1_MULTIFAMILY_DUEL.md, adjudicated and
verified in watch/inbox/last_mile_20260930/AH11_WILSON_CHECK.md. Later
amendments win where they conflict, the same rule the body uses.)

### AMENDMENT 7 (kill: G3 flooding launders the Wilson denominator; amends the section 2 Wilson usage and AMENDMENT 6 part 2)

The kill: pass_rate_lb95 feeds the section 2 Wilson formula the RAW
sample_size while p_hat is the weighted rate, so a G3 verdict (weight
0.25) adds 1 to n but 0.25 to evidence mass; lb95 rises toward p_hat as
1/sqrt(n_raw) on volume that was never evidence. Fixture (numbers
verified in the AH11 receipt): 1 G0 FAIL + 100 G3 passes gives
p_hat = 25/26, n_raw = 101, lb95 = 0.9041 (qualifies vs 0.85) while the
weighted evidence mass n_eff = passes + fails = 26 gives lb95 = 0.8111
(correctly fails). The 4.1 rule 4 cap cannot see this (AMENDMENT 6's own
words: a composition gate, not a claim about the arithmetic): one
deterministic G0 fail satisfies n_non_g3 >= 1 and unlocks unlimited G3
volume. Fix, one clause: the Wilson denominator everywhere
(pass_rate_lb95 and therefore eff_lb95) is n_eff = passes + fails, the
weighted evidence mass the AMENDMENT 6 closed form already maintains
over the eight per-class counters; sample_size stays a raw audit column
and is never a bound input again. Pure-G0/G1 cells are byte-identical
under the fix (every weight 1.0, n_eff = n_raw); G2/G3-heavy cells can
only demote (n_eff <= n_raw at weights <= 1). Falsifier (first test of
any build on this amendment): the cell {g0_fails = 1, g3_passes = 100}
must NOT qualify, and a replayed all-weight-1.0 cell's lb95 must equal
the v1 value byte-for-byte. Drafted but NOT applied (operator's call,
AH11 receipt section 5): rule 2's n >= m boundary reading n_eff; a
honesty note that Wilson-on-weighted-counts is a conservative
approximation (bootstrap cross-check belongs to the harness); a G3
weight-share cap for the no-fail-evidence residual (case B in AH11).

Em-dash count in batch AH11: 0.

## AMENDMENTS, batch IMP3 (append-only; 2026-09-30; the AA1 read-side kill 3,
watch/inbox/last_mile_20260930/AA1_OPUS_REFIRE.md section 4: "IDENTITY IS A
LABEL, NOT BYTES. The ledger keys on a model_id string any operator can
repoint to different weights". Amendment numbers 8 and 9 are reserved for the
sibling delta lanes D1 and D2 of the same AA1 kill list (its section 6), so
this lane files AMENDMENT 10. Later amendments win where they conflict, the
same rule the body uses.)

### AMENDMENT 10 (kill 3: model_id is repointable; amends 1, 2 DDL delta, 3.3, 4.1, 5, 8)

The kill: the capability PK and every rate inside a cell are keyed on the
model_id string. A provider can serve different weights under one model_id
(quant swap, version bump, mid-flight repoint), so one cell can silently
average two different machines, and 3.3's environment hash carries only the
model TAG, which is exactly the repointable label (the estate's own law:
trust bytes, not labels; AA1 verdict section 4, kill 3). The fix binds every
cell to a measured bytes-level identity. Seven parts:

1. MODEL FINGERPRINT (new definition in section 1): model_fingerprint =
   sha256 hex over the canonical serialization of the PROBE BATTERY response
   (part 2), an observational identity of the served weights as visible
   through the API surface. It detects repoints and quant swaps that move
   first-token logprobs; it does not prove the weight matrix. The literal
   UNKNOWN is the pre-measurement state. The endpoint is NOT part of the
   fingerprint: same weights behind two endpoints are one machine, and the
   receipt spine keeps the endpoint separately.
2. THE PROBE BATTERY (reproducible recipe; every constant a DESIGN DEFAULT,
   frozen by this section): exactly five prompt literals, temperature 0,
   max_tokens 1, top_logprobs 20, no system prompt, no tools:
   P1 "Yes or no: is 17 a prime number? Answer:"
   P2 "def add(a, b):\n    return"
   P3 "{\"tool\": \"search\", \"query\":"
   P4 "The capital of France is"
   P5 "A verdict without evidence is"
   For each prompt retain the returned top-logprob list in rank order as
   returned. Canonical digest input: UTF-8 bytes of "gps-battery-v1" followed
   by compact JSON of the flat array [[prompt_sha256, rank, logprob_string,
   token_string], ...] in prompt order then rank order; logprob_string is the
   decimal EXACTLY as the API returned it, never reformatted; token_string
   exactly as returned. model_fingerprint = sha256 of those bytes. The
   battery version tag inside the digest makes any future battery change
   automatically open fresh cells fleet-wide (a battery edit is an amendment
   plus a mandated re-probe). Cost: five one-token completions per run,
   logged as a probe_log row (probe_kind = fingerprint; negligible against
   the 4.4 leash, free on the local fleet).
3. SCHEMA DELTA (amends 2; stated as an in-amendment DDL delta per the
   AMENDMENT 3 precedent, not an in-place edit, because sibling lanes 8/9
   may also touch section 2): capability gains model_fingerprint TEXT NOT
   NULL and its PRIMARY KEY becomes (model_id, model_fingerprint,
   task_shape, task_shape_version); verdict gains model_fingerprint TEXT
   NOT NULL DEFAULT 'UNKNOWN' inside the signed row_sha256 coverage (a
   verdict's identity attribution cannot be edited without breaking its
   signature and the chain); ix_verdict_cell covers the column; probe_log
   gains probe_kind TEXT NOT NULL DEFAULT 'shape'. A CELL is now that
   four-tuple.
4. GROUPING LAW (amends 4.1; the never-merge rule): rows group by
   (model_id, model_fingerprint). A fingerprint change is a NEW cell at
   cold start (n = 0, the AMENDMENT 5 exploration band): never merged,
   never averaged, and it receives no transfer of any kind from the old
   cell, which closes to new verdicts, keeps its history, and decays per
   4.1 exactly as if the machine behind the label had vanished. The single
   writer runs the battery at ledger session open and at the head of every
   verdict-insert transaction (the AMENDMENT 2 transaction); the measured
   fingerprint binds every verdict in that transaction; a verdict never
   guesses. Qualification gains one conjunct: a cell is ROUTABLE only
   while its fingerprint equals its model_id's last measured fingerprint;
   older-fingerprint cells remain in report_capability as history and are
   unreachable by the router (reason_code vocabulary gains
   fingerprint_mismatch). The fail direction is closed: any digest byte
   difference is a new cell, so a false split costs a cold start and a
   silent merge is impossible by construction.
5. 3.3 ENVIRONMENT IDENTITY: the evidence-hash environment input gains
   model_fingerprint next to the model tag. The tag was the label; the
   fingerprint is the bytes; together they are the triple 3.3 already
   claims to certify.
6. RECEIPTS (amends 5): chosen and every considered[] entry gain
   fingerprint_short, the first 12 hex of the cell fingerprint (UNKNOWN
   for grandfathered cells).
7. MIGRATION AND FALSIFIER: existing capability and verdict rows are
   grandfathered at model_fingerprint = 'UNKNOWN'; UNKNOWN cells keep
   their routing standing unchanged until their model's first battery
   probe, at which point the measured cell opens cold and the UNKNOWN
   cell closes to new verdicts; legacy verdicts replay into UNKNOWN
   cells; v0 gps_ledger.db3 is fixture data (AMENDMENT 6 note), so this is
   a fixture rebuild, not production surgery. Section 8 gains row F6:
   identity repoint or quant swap under one model_id; defense =
   fingerprint grouping + signed attribution + session-open battery;
   residual, named not papered: a repoint that preserves every returned
   logprob string is invisible (observational identity, not proof),
   float-serialization or serving jitter can only split cells (the safe
   direction), and detection latency is bounded by the next battery run.
   K5 red-team adds: plant a verdict with fingerprint F2 into a cell
   keyed F1 (insert rejects; audit quarantines a smuggled copy), and swap
   the served weights behind a model_id mid-test: after the next
   session-open battery the router must treat the old cell as history and
   the new cell must sit at n = 0 in the exploration band.

Em-dash count in batch IMP3: 0.

## AMENDMENTS, batch IMP2-D2 (append-only; 2026-09-30; the AA1 read-side
kill 2, banked verbatim in watch/inbox/last_mile_20260930/
AA1_OPUS_REFIRE.md section 4: "CALIBRATION IS CERTIFIED FROM THE WRONG
REGION. T1 verifies answers below min_confidence, but low-confidence stops
go ungated, so evidence is sampled almost entirely ABOVE the threshold:
survivorship bias in cell rates and ECE." This lane files AMENDMENT 9 per
the operator's D1/D2/D3 allocation (the IMP3 batch header reserves 8 and 9
for the sibling delta lanes). Later amendments win where they conflict,
the same rule the body uses. Drafting decision: the section 5 grammar
delta is stated in-amendment, not applied in place, per the AMENDMENT 10
part 3 precedent, because sibling lanes of the same kill list also touch
section 5 and colliding in-place JSON edits would fork the block.)

### AMENDMENT 9 (kill 2: calibration certified from the survivor region; amends 4.3 T1, 3.4, 5, harness M6, and AMENDMENT 5's verified sentence)

The kill, named precisely: T1's predicate reads conf < min_confidence
(DEFAULT 0.8), but verified was defined (4.3, as amended by AMENDMENT 5)
as a rolling ECE over the last m gated answers, and 3.4 routes
low-confidence stops out of the verdict stream: a stop without gate
evidence writes no verdict, and nothing obliges anyone to gate a stop
(3.4 says cascades MAY gate intermediate steps; the traffic default gates
final answers). Final answers are selected for confidence: a cascade ends
at a confident answer, and an unconfident step hands the work up-tier, so
gatedness rises with confidence and the window fills almost entirely from
[min_confidence, 1]. Low-confidence stops remove exactly the events T1
needs: the conf < min_confidence pairs never enter the window, so the ECE
certifies a region the trigger never acts in. A model calibrated above
0.8 and arbitrary below it presents a clean ECE, reaches verified, and T1
then spends climbs on a number certified where it is not read:
survivorship laundered into trigger authority, against JUDGED.md's own
kept clause that T1 fires only on calibration_state = verified. The
stop-rate, which is the censoring intensity, is currently recorded
nowhere. Five clauses fix it:

1. WINDOW MEMBERSHIP (amends the 4.3 T1 calibration clause): the ECE
   window is the cell's last m GATED answers, and NO gated answer may be
   excluded from it by stop status, confidence value, cascade position,
   or tier: a verdict written on a gate-terminated low-confidence stop is
   a gated answer (3.4 already permits exactly this) and counts. Each
   member contributes its (receipt.confidence, verdict bit) pair, joined
   on receipt_ref, which both rows already carry; no verdict-table
   change. The outcome is the verdict bit raw: gate-class weights govern
   the pass-rate (3.1), never this join. Answers with confidence_source
   none carry no confidence number, feed the pass-rate as usual, and
   never enter the window; the exclusion is symmetric (T1 cannot fire on
   them either), not survivorship. ECE uses 10 equal-width bins on
   [0, 1], deterministic and unstochastic (DESIGN DEFAULT; e_max stays
   0.10, tunable from harness data).
2. THE STOP IS MEASURED OR THE TRIGGER STAYS DISARMED (turns 3.4's MAY
   into an obligation, scoped): on a cell at n >= m seeking verified,
   every low-confidence stop is gated before the climb executes, at the
   shape's cheapest canonical gate (G0 when one exists). The gate outcome
   feeds the window for FUTURE T1 decisions; it does not gate the current
   climb (triggers stay orthogonal: per-instance climb-gating is T2's
   economics, not T1's). The gated stop's verdict is an ordinary verdict:
   a stop that passes is the underconfidence datum (conf 0.6 with PASS),
   a stop that fails is a real fail on the cell. 3.4's protection
   (unconfident is not wrong) is unchanged for UNGATED stops and for the
   n < m band: AMENDMENT 5's cold-start law stands (no verified is
   claimable there, so no stop-gating obligation, no T1, and exploration
   traffic keeps its 4.2 gate-what-you-can rule). Stop-gate spend is
   cascade gate cost charged to M1, never probe budget. The obligation
   binds only armed cells, is bounded by clause 4's s_max, and is exactly
   the price of certifying the region T1 reads; an operator who declines
   the price simply cannot claim verified (fail closed, the section 0
   pattern at trigger granularity).
3. REGION COVERAGE, AND THE WEIGHTING ALTERNATIVE: verified additionally
   requires n_low >= k_low (DESIGN DEFAULT 10) window pairs with recorded
   confidence < min_confidence. A window of survivors only (n_low = 0)
   can never present verified or poor: the state is unverified regardless
   of ECE, because the number was computed on a distribution the trigger
   does not act on. Where full stop-gating is declined, the sanctioned
   alternative is explicit inverse-stop-probability weighting with DESIGN
   weights, not modeled ones: gate a seeded random sample of
   low-confidence stops at rate p_stop (DESIGN DEFAULT 0.25), flag those
   receipts sampled_stop_gate: true, and weight each sampled pair by
   1/p_stop in its bin mass; certification then requires the same k_low
   floor on the WEIGHTED low-region mass and that no single sampled pair
   carry more than half its bin mass (variance guard). Modeled
   missing-at-random IPW is REFUSED: the stop decision is a deterministic
   function of the very variable being calibrated, so within-region
   selection is degenerate and its fitted weights are zero or infinite by
   construction. Either path failing its floor gives unverified.
4. HIGH STOP-RATE: the cell's rolling stop-rate s (low-confidence stops
   over the last m decision steps citing the cell, computed from the
   receipt spine; no schema change) is carried on every receipt citing a
   routable cell as stop_rate. When s > s_max (DESIGN DEFAULT 0.5),
   calibration_state = unverified, never poor and never verified,
   whatever the ECE says. Why fail closed in both directions: if the
   stops are ungated, the censored mass is the majority of traffic and
   the survivor ECE certifies almost nothing; if they are gated, T1's
   climb has become the standing policy for most traffic, which is a
   routing decision the ledger's pass-rate must license, not a confidence
   number (the T2 precedent: no precise arithmetic on unstable
   quantities). T1 disarms: a low-confidence answer logs trigger none
   with stop_rate on the receipt, exactly AMENDMENT 5's no-climb posture;
   the cell's fate runs through ordinary verdict accumulation and the
   forced-probe loop; s > s_max on a routed cell is an operator-visible
   anomaly auditable from the receipts, not an auto-remediation.
5. LABEL MAP (supersedes only AMENDMENT 5's "ECE <= e_max gives verified
   and T1 may fire; ECE > e_max gives poor" sentence): verified iff
   window full (n >= m, AMENDMENT 5) AND membership uncensored per clause
   1 AND n_low >= k_low (direct or by design weights) AND s <= s_max AND
   ECE <= e_max. poor iff every structural conjunct holds AND ECE >
   e_max. unverified otherwise; which conjunct failed is auditable from
   the receipt's stop_rate and calibration_state. Harness M6 gains: ECE
   reported per model per shape AND per region (below and above
   min_confidence) with n_low, because a coverage floor nobody prints is
   unauditable. Grammar delta (section 5, in-amendment per the batch
   preamble): the receipt row gains "stop_rate": null (the rolling cell
   stop-rate when the row cites a routable cell, else null) and
   "sampled_stop_gate": false (true only on stop rows gated by the clause
   3 sampling design).

Test predicates (first tests of any build on this amendment, before
routing authority, the AMENDMENT 4 spirit): (1) CENSORSHIP INJECTION: a
cell whose conf < min_confidence answers all stop ungated while its
conf >= min_confidence answers gate clean stays unverified at every n,
and a T1-eligible event logs trigger none with stop_rate present; (2)
REGION SEPARATION: two cells with byte-identical survivor pairs but
different low-region outcomes (calibrated below 0.8 vs garbage below
0.8, both n_low >= k_low) present different states (verified vs poor);
under the pre-amendment text they are indistinguishable, which is the
kill demonstrated; (3) DESIGN-WEIGHT EQUIVALENCE: with all stops gated,
the clause 3 estimator at p_stop = 1.0 equals the direct ECE
byte-for-byte, and at p_stop = 0.25 with seeded sampling agrees within a
named tolerance, and any row flipping sampled_stop_gate without a gate
behind it fails the audit (F5 recycle law); (4) HIGH STOP-RATE: s >
s_max over an otherwise compliant window presents unverified, T1 logs
trigger none, the receipt carries s; (5) GRAMMAR: every receipt citing a
routable cell carries stop_rate, and every gated stop row carries
non-null confidence.

Cost and residuals, named: clause 2 gates every stop on armed cells,
bounded by s <= s_max (a cell at that rate is already demotion-bound
through its landed fails); if that breaches the F-S6 ~10% gate-economics
fence the operator drops to clause 3 sampling at a quarter the stop-gate
cost. Residual A: k_low = 10 of m = 50 leaves the low-region ECE
high-variance; M6 owns the number. Residual B: the kill's own words say
"survivorship bias in cell rates AND ECE"; this amendment heals the cell
pass-rate only incidentally and only for armed cells (gated stop fails
land). Cold-start and never-armed cells keep survivor pass-rates BY
DESIGN, because 3.4's poison-protection (ungated stops counted as fails
poison cheap-tier cells) is load-bearing there; whether that boundary is
a defect is the kill 1 lane's and the harness's call, not papered over
here.

Em-dash count in batch IMP2-D2: 0.

## AMENDMENTS, batch IMP1-D1 (append-only; 2026-09-30; the AA1 read-side
kill 1, banked verbatim in watch/inbox/last_mile_20260930/
AA1_OPUS_REFIRE.md section 4: "DRIFT IS INVISIBLE INSIDE OUR OWN BUDGET.
Fail verdicts REFRESH freshness under 4.1 decay, so a collapsing cell
looks young; total collapse of a 300-verdict cell at 0.95 needs ~21 fresh
fails to demote, breaching K3's 10-verdict ceiling by arithmetic." Every
number below verified in watch/inbox/last_mile_20260930/
IMP1_D1_FRESHNESS.md. AMENDMENT 8 was reserved for this lane (D1) by the
IMP3 batch header and the operator's D1/D2/D3 allocation; batches append
in landing order, so 8 lands after 9 and 10. Later amendments win where
they conflict, the same rule the body uses. The body and DDL stay
untouched in place; the DDL delta lives here as text, the AMENDMENT 3
and 10 part 3 precedent, because sibling lanes of the same kill list
also touch section 2.)

### AMENDMENT 8 (kill 1: fail verdicts refresh the freshness clock, so collapse is invisible inside the budget; amends 4.1 rule 3, the capability DDL, 4.3 T4; carves AMENDMENT 4 predicate 3)

The kill: 4.1 computes age_days since last_verdict_utc and ANY verdict
refreshes that column. During an active collapse every fresh fail resets
the decay clock (w back to 1, eff_lb95 pinned to lb95) while lb95 falls
at O(1/sqrt(n)): a 300-verdict pure-G0 cell at 0.95 (285/300) demotes
only at its 21st consecutive fresh fail (lb95 = 0.8486 < 0.85 at
k = 21; 0.8517 at k = 20; receipt). K3 kills the design at detection
latency > 10 fresh verdicts, and M4's collapse test-double is exactly
this stream, so v1's own arithmetic breaches its own pre-registered
ceiling by 11 verdicts, deterministically, for every
comfortably-qualified cell. The root error is in 4.1's own sentence
"freshness is re-earned by new verdicts": it conflates two opposite
events. A pass is re-earned capability; a fail is evidence against it.
Under v1 both buy youth.

Fix, one mechanism on the one clock the router reads:

- DDL delta (capability; the cell is the AMENDMENT 10 four-tuple, the
  columns attach to it): last_verdict_utc stays as the raw audit column,
  but the decay clock stops reading it. Add last_pass_utc TEXT NOT NULL
  (refreshed only by pass verdicts) and fail_age_days_accrued REAL NOT
  NULL DEFAULT 0 (advanced by each fail verdict, zeroed by each pass;
  both maintained inside the AMENDMENT 6 atomic commit). 4.1 rule 3's
  age_days becomes effective_age_days = (now - last_pass_utc) +
  fail_age_days_accrued. Two asymmetries in one clause set: fails do not
  refresh the clock (asymmetry 1), and each fail advances it by
  fail_age_days DEFAULT 1.0 day (asymmetry 2: freshness decays on fails
  at a faster, verdict-driven rate). Passes reset both terms; a pass
  still buys instant youth, eff = lb95, the v1 re-earn semantics kept
  for the only event that deserves it.
- Demote-only clamp, the body's own prose law ("decay only demotes")
  made explicit in the arithmetic: eff_lb95 = min(w * lb95 + (1 - w) *
  0.5, lb95). Decay may never lift a cell, which also discharges the
  below-0.5 lift the AA1 verdict named in passing.
- THE INVARIANT (this amendment's contract): a cell whose last k
  verdicts are all fails must be demoted (its collapse detected) within
  the K3 ceiling. Closed form: demotion at threshold 0.85, p0 = 0.5
  needs w < 0.35 / (lb95 - 0.5); worst case lb95 = 1.0 needs w < 0.70,
  reached at k = ceil(half_life_days * log2(1/0.70) / fail_age_days) =
  ceil(14 * 0.5146 / 1.0) = 8. N_COLLAPSE = 8 consecutive fails demotes
  ANY cell at ANY n, with margin 2 under K3's 10; the fails' own drag on
  lb95 only makes real detection earlier (the AA1 example cell demotes
  at its 4th consecutive fail, receipt, which lands on the frontier's
  independently derived "4th fail in the last 10" guard constant).
  fail_age_days is tunable only down to the derived floor 0.7204 days
  (= half_life_days * log2(1/0.70) / 10); at or below that floor the
  worst-case bound reaches 10 and the tuning is illegal by this
  amendment.
- T4 predicate conjunct: T4 staleness now requires eff_lb95 < threshold
  AND raw lb95 >= threshold AND fail_age_days_accrued = 0. Any demotion
  with accrual present is evidence-driven (collapse suspect), not a
  knowledge gap: frontier tokens do not patch it, the forced probe
  does. Since only a pass zeroes accrual, T4 is now purely wall-clock
  staleness, exactly what its own prose always claimed.
- AMENDMENT 4 predicate 3 carve-out: "fresh forced-probe verdicts never
  lower eff_lb95" binds PASS verdicts only; a fail verdict lowering
  eff_lb95 is this amendment's designed demotion path. Paired check
  added: with fail_age_days fixed, k consecutive fails on an otherwise
  frozen cell demote at exactly the closed-form k, non-increasing in
  between. AMENDMENT 9 clause 2 lands gated-stop fails as ordinary
  fails: they advance the fail clock too, which is coherent, a real
  fail is a real fail.

Cost, named: a qualified cell sitting near the boundary takes a bigger
eff dip on one ordinary fail than v1 gave it (one accrued day costs
w = 0.9517; a post-fail lb95 below 0.8678 does not requalify until the
next pass zeroes the accrual), so boundary cells can transiently demote
on a single fail. The error is fail-closed (demote-only clamp) and
recoverable by one gated pass, while sprinkled fails on a healthy cell
never demote (a 0.92 cell survives 3 accrued days at eff = 0.8613,
receipt): only fails with no intervening pass accrue. The asymmetry is
the point: a false demotion of a boundary cell costs one probe round; a
false qualification of a collapsing cell is the disease K3 exists to
catch. Residual: a pass zeroes the accrual, so one curated pass can
launder k accrued fail-days; the fails' weighted damage to lb95 persists
(the slow path still holds), probe_log plus near-duplicate input
clustering (F5's defense) bound curated-pass minting, and the K3
detection promise covers all-fail streaks, which a genuine pass lawfully
interrupts.

Why the clock and not the frontier's count-window guard ("demote at the
4th fail in the last 10"): the guard demotes outside the currency the
router, receipts, considered[], and M4's detection-latency metric all
read, splitting detection into two definitions; the same policy
expressed on the decay clock keeps ONE number, eff_lb95, as the whole
demotion story, keeps T4-versus-collapse distinguishable by accrual
alone, and closes the slow-drift half of the kill (fails no longer
refresh the clock) in the same clause set, with no second trigger,
threshold, or reason_code. Pre-registered binomial arithmetic, not a
bandit, exactly as the verdict required.

Em-dash count in batch IMP1-D1: 0.
