# SEAT A: CAPABILITY-LEDGER SPEC v1 (SPEC ARCHITECT DRAFT)

Written blind (procedurally independent of Seats B and C; no cross-reading,
no post-hoc revision). Author: ractor seat A, 2026-09-29. Supersedes the v0
schema and router semantics in `tools/gps_mcp/ledger.py`,
`tools/gps_mcp/router.py`, `tools/gps_mcp/providers.py` (path-cited; v0
shipped 28/28 tests per `watch/inbox/game_platform_basecamp_20260929/GPS_MCP_V0_20260929.md`).
Every numeric default below is a DESIGN DEFAULT (tunable constant named at
first use), not a measured fact. Where I estimate estate-scale quantities I
mark ESTIMATE.

Design goal, one sentence: v0 measured pass-rates but trusted them blindly;
v1 makes every routing input (rate, confidence, cost) carry its own
provenance, uncertainty, and expiry, so a routing decision is a checkable
claim about evidence rather than a lookup of a bare number.

## 0. What v0 got right and is kept verbatim

- One SQLite ledger, plain schema, PRIMARY KEY (model_id, task_shape)
  (`tools/gps_mcp/ledger.py` SCHEMA_SQL).
- Routing priority: constraints, then measured pass-rate, then cost, then
  calibrated confidence (`tools/gps_mcp/router.py` docstring rules a-d).
- Per-decision-step JSONL receipts, cascade steps sharing trace_id
  (`tools/gps_mcp/router.py` ReceiptLog, MAX_CASCADE_TIERS = 3).
- Truth and price on separate clocks: verdicts never write cost
  (`tools/gps_mcp/ledger.py` record_verdict, cost column nullable).
- Test doubles behind the same call boundary as real providers, zero
  router-internal test branches (`tools/gps_mcp/providers.py` per
  `tools/gps_mcp/README.md`).

## 1. Definitions (normative)

- TASK SHAPE: a named, versioned class of work (e.g. the five fixture
  shapes in `tools/gps_mcp/seed_fixtures.py`: code_review, summarize,
  yes_no_decision, tool_call_parse, design_judgment). A shape has a
  REGISTRY ENTRY (owner, version, canonical gate list, description); free
  strings are not shapes.
- VERDICT: a signed claim that one ANSWER (not one model in the abstract)
  passed or failed one gate. Verdicts attach to artifacts, never directly
  to models; the ledger is their aggregation.
- GATE: a machine-runnable or operator-run procedure that maps
  (input, answer) to pass/fail plus an evidence artifact. Gate classes
  G0-G3 defined in section 4.
- EFFECTIVE RATE: the decay-blended Wilson lower bound the router is
  allowed to read (section 5.1). The raw mean exists for audit only.
- PROBE: a deliberately scheduled ask whose purpose is measurement
  (fighting staleness), flagged on its receipt, budgeted (section 5.4).
- PRINCIPAL: a key-holding writer identity (operator keys, tooling keys,
  gate-runner keys). Endpoints/models are NOT principals and can never
  write verdicts about their own answers.

## 2. Ledger schema v1 (SQLite DDL)

```sql
CREATE TABLE task_shape_registry (
    task_shape        TEXT NOT NULL,          -- canonical slug
    version           INTEGER NOT NULL,       -- bumped on definition change
    owner             TEXT NOT NULL,          -- principal id
    description       TEXT NOT NULL,
    canonical_gates   TEXT NOT NULL,          -- JSON list of gate class refs
    created_utc       TEXT NOT NULL,
    retired_utc       TEXT,                   -- NULL = active
    PRIMARY KEY (task_shape, version)
);

CREATE TABLE principal (
    principal_id      TEXT NOT NULL,
    pubkey            TEXT NOT NULL,          -- ed25519, hex
    allowed_gates     TEXT NOT NULL,          -- JSON list: subset of G0..G3
    created_utc       TEXT NOT NULL,
    revoked_utc       TEXT                    -- NULL = active; fail closed
);

CREATE TABLE capability (
    model_id            TEXT NOT NULL,
    task_shape          TEXT NOT NULL,
    task_shape_version  INTEGER NOT NULL,
    passes              INTEGER NOT NULL,     -- weighted pass count (weights s4.3)
    fails               INTEGER NOT NULL,
    sample_size         INTEGER NOT NULL,     -- raw verdict count
    pass_rate_raw       REAL NOT NULL,        -- running weighted mean (v0 legacy)
    pass_rate_lb95      REAL NOT NULL,        -- Wilson 95% lower bound
    cost_usd_last       REAL,                 -- last billed cost of one call
    cost_usd_ewma       REAL,                 -- exponential weighted mean, alpha DEFAULT 0.25
    first_verdict_utc   TEXT NOT NULL,
    last_verdict_utc    TEXT NOT NULL,
    half_life_days      REAL NOT NULL DEFAULT 14.0,   -- DESIGN DEFAULT (tunable)
    gate_class_mix      TEXT NOT NULL,        -- JSON {G0: n0, G1: n1, G2: n2, G3: n3}
    updated_utc         TEXT NOT NULL,
    PRIMARY KEY (model_id, task_shape, task_shape_version)
);

CREATE TABLE verdict (
    verdict_id        TEXT NOT NULL,          -- content hash of the row minus hashes
    ts_utc            TEXT NOT NULL,
    model_id          TEXT NOT NULL,
    task_shape        TEXT NOT NULL,
    task_shape_version INTEGER NOT NULL,
    verdict           INTEGER NOT NULL,       -- 1 pass, 0 fail
    gate_class        TEXT NOT NULL,          -- G0 | G1 | G2 | G3
    gate_id           TEXT NOT NULL,          -- registry ref of the concrete gate
    evidence_hash     TEXT NOT NULL,          -- sha256 of the retained evidence artifact
    evidence_uri      TEXT NOT NULL,          -- where the artifact lives (repo-relative)
    receipt_ref       TEXT NOT NULL,          -- decision_id of the ask/cascade step judged
    principal_id      TEXT NOT NULL,
    signature         TEXT NOT NULL,          -- ed25519 over canonical row
    prev_sha256       TEXT NOT NULL,          -- chain, house pattern
    row_sha256        TEXT NOT NULL,
    PRIMARY KEY (verdict_id),
    UNIQUE (receipt_ref, gate_id)             -- idempotency: same answer re-judged
);                                            -- by same gate is a protocol error
CREATE INDEX ix_verdict_cell ON verdict(model_id, task_shape, task_shape_version);

CREATE TABLE probe_log (
    probe_id          TEXT NOT NULL,
    ts_utc            TEXT NOT NULL,
    model_id          TEXT NOT NULL,
    task_shape        TEXT NOT NULL,
    budget_usd        REAL NOT NULL,
    spent_usd         REAL NOT NULL,
    receipt_ref       TEXT NOT NULL,
    PRIMARY KEY (probe_id)
);
```

Why lower bounds instead of means: v0 routes on `pass_rate >= 0.85`
(`tools/gps_mcp/router.py` DEFAULT_PASS_RATE_THRESHOLD) with sample_size
carried but unused. A 0.86 mean on n=18 (fixture: frontier-opus
design_judgment, seeded 0.96 at n=52, `tools/gps_mcp/seed_fixtures.py`)
has a Wilson 95% lower bound near 0.87, but a 0.86 on n=5 has an LB near
0.49. v1 rule: the router reads pass_rate_lb95 only; rows below
n_min (DEFAULT 20) are treated as UNMEASURED for routing (still visible to
report_capability). Formula (Wilson, 1927, standard):

    center = (p + z^2/2n) / (1 + z^2/n)
    half   = z * sqrt(p(1-p)/n + z^2/4n^2) / (1 + z^2/n)
    lb95   = center - half,  z = 1.96

## 3. Verdict rows are the source of truth

`capability` becomes a MATERIALIZATION of `verdict` (rebuildable by
replay; the v0 verdict_log side table
`tools/gps_mcp/ledger.py` verdict_log is its ancestor). Any capability row
whose backing verdicts fail chain verification is quarantined (routing
ignores it, report_capability flags `quarantined: true`).

Chain and signature reuse the estate house pattern verbatim: append-only
rows, row hash covers the row minus its own hash field, genesis prev = 64
zeros, ed25519 with deterministic key derivation and fail-closed
HAS_CRYPTO (all specified in the `mag/gwap_payload.py` header, v1
section). No new cryptography is invented here.

## 4. The verification-gate contract

### 4.1 Gate classes and minimum evidence

| Class | What it is | Minimum evidence retained | Verdict weight |
|---|---|---|---|
| G0 machine-checkable | deterministic check: tests pass, JSON-schema validation, exact/regex match, parse-and-execute | input hash, answer hash, checker version, environment hash (model tag, prompt template id), checker output log | 1.0 |
| G1 dual-independent rubric | two principals score the same rubric independently; agreement within tolerance passes (the gwap agreement idea, `mag/gwap_payload.py` verdict ladder) | both scored rubrics, author principals, agreement score | 1.0 when agreeing, else CHALLENGE (no verdict) |
| G2 operator judgment | a human principal signs pass/fail | operator principal, one-paragraph rationale, artifact hash | 0.5 |
| G3 model-judge | a non-answerer model grades | judge model_id, judge prompt hash, grade + self-confidence | 0.25, and CAPPED: G3-only verdicts can never lift pass_rate_lb95 above the routing threshold |

Weights are DESIGN DEFAULTS (tunable). Weighted update: each verdict
contributes weight w; pass_rate_raw = sum(w * v) / sum(w);
sample_size counts raw verdicts; gate_class_mix records the composition so
a mostly-G3 cell is visible at a glance.

### 4.2 Who can write

- Only principals whose `allowed_gates` includes the gate class, key not
  revoked, signature verifies. The shared-surface law that model text
  proposes and only authorized actors effect
  (`watch/inbox/SHARED_SURFACE_CONTRACT.json`, law 5) is the house
  precedent: a verdict is an effect, not a suggestion.
- SEPARATION OF DUTIES: the principal that submitted the ask may not be
  the scoring principal for a G1/G2/G3 verdict on that same receipt_ref.
  G0 is exempt because anyone can re-run a deterministic check and get
  identical bytes; that is the point of G0.
- A verdict MUST cite the receipt_ref of the answer it judges. Verdicts
  about answers that have no receipt row are rejected (they are exactly
  the inflatable kind; the v0 README itself flags this hole as critique
  item 2, `tools/gps_mcp/README.md` IF WE GROW THIS 1).

### 4.3 What a pass/fail artifact IS

An evidence artifact is REUSABLE only if it contains: (1) the exact input
bytes (or their hash plus a durable URI), (2) the exact answer bytes, (3)
the checker identity + version, (4) the environment identity (model tag,
prompt template, temperature) so the verdict is a statement about a
(model, task_shape_version, environment) triple, not a vibe about a brand.
evidence_hash = sha256 over the canonical serialization of those four.

## 5. Routing and escalation policy v1

### 5.1 Selection (replaces v0 rule b)

A candidate qualifies iff ALL of:
- passes hard constraints (v0 rule a, unchanged: max_cost_usd,
  max_latency_ms against live config price);
- n >= n_min (DEFAULT 20) AND pass_rate_lb95 >= threshold (DEFAULT 0.85,
  caller-overridable, unchanged from v0);
- effective_lb95 >= threshold where effective_lb95 = w * lb95 + (1 - w)
  * p0, with p0 = 0.5 (pessimistic prior, DESIGN DEFAULT), w =
  exp(-ln2 * age_days / half_life_days), age_days since last_verdict_utc.
  Decay therefore only ever DEMOTES over time; freshness must be re-earned
  by new verdicts. This answers v0 critique item 3 (no time decay,
  `tools/gps_mcp/README.md` What v0 deliberately does not do, last bullet).
- If NO candidate in a shape qualifies but rows exist: route cheapest
  constraint-passing candidate AND schedule a forced probe round
  (k = DEFAULT 5 fresh G0-gated items) for the top stale rows.

Choose cheapest qualifying (v0 rule c, unchanged; cost read from live
config, never from the ledger: v0 design decision 3 kept,
`watch/inbox/game_platform_basecamp_20260929/GPS_MCP_V0_20260929.md`).

### 5.2 Exploration

- No history for the shape (all rows n < n_min or absent): v0 rule kept,
  route the designated exploration tier with exploration: true
  (`tools/gps_mcp/router.py` _select exploration branch).
- v1 ADDS: exploration traffic is measurement traffic; every exploration
  ask whose answer can be G0-gated MUST be gated, and its verdict is the
  seed of the cell's history. Exploration is how a cell graduates, not a
  fallback flavor.
- No random epsilon and no UCB bandit in v1: both are deferred until the
  eval (Seat C's domain, and the estate's honesty about not shipping
  unmeasured cleverness). v1 explores only via no-history routing and
  forced probes.

### 5.3 Escalation decision boundaries (the frontier-amendment core)

v0 escalates on ONE bit: returned confidence < 0.8
(`tools/gps_mcp/router.py` DEFAULT_CASCADE_MIN_CONFIDENCE). v1 replaces
the single bit with four named triggers, any of which authorizes the
climb, all recorded on the receipt as `trigger`:

- T1 CONFIDENCE (usable only when earned): conf < min_confidence AND the
  model's calibration on this shape is VERIFIED: rolling reliability check
  on its last m = DEFAULT 50 gated answers, ECE <= e_max = DEFAULT 0.10.
  If calibration is unverified or poor, low confidence triggers T4
  (probe), not T1: an uncalibrated confidence number is noise wearing a
  uniform.
- T2 ECONOMICS: expected cost of staying exceeds climbing:
      P(fail_i) * (C_rework + price_j)  >  price_j + P(fail_j) * C_rework
  where P(fail) = 1 - effective_lb95 (NOT self-confidence; the ledger's
  own estimate), C_rework = DEFAULT 3x current-step price (DESIGN DEFAULT
  representing downstream cost of shipping a wrong answer; replace with a
  measured number after the first eval), j = candidate one tier up.
- T3 BLIND SPOT: the chosen row has n < n_min (routing was effectively
  unmeasured): climb to the cheapest model with n >= n_min that
  qualifies; if none, the answer ships flagged `low_evidence: true`.
- T4 STALENESS/PROBE: effective_lb95 < threshold while raw lb95 >=
  threshold (decay demoted the row): do NOT climb automatically; ship
  current-tier answer AND schedule the forced probe. Rationale: staleness
  is a knowledge gap, not a difficulty signal; paying frontier prices to
  patch a measurement hole is the exact waste the ledger exists to stop.

Cap of 3 tiers retained (v0). Prior-answer context attach retained (v0).
Every trigger writes itself into the receipt row (section 6).

### 5.4 Probe budget (the organ's leash)

Forced probes cost money. Per shape per week: probe_budget_usd DEFAULT
0.50 USD (ESTIMATE, sized so a 5-shape fleet spends at most 2.50 USD/week
on measurement; recalibrate from real billing after week one). Probes
beyond budget wait for the next window; the router falls back to
current behavior with `stale: true` flags. probe_log makes the organ's
appetite auditable, which is the actual difference between an instrument
and a parasite.

## 6. Receipt-row grammar v1

Append-only JSONL, one row per decision step (v0 invariant kept:
`watch/inbox/game_platform_basecamp_20260929/GPS_MCP_V0_20260929.md`
design decision 2). v1 extends the v0 row
(`tools/gps_mcp/router.py` RECEIPT_REQUIRED_KEYS) with provenance and
chain:

```json
{"seq": 142,
 "ts_utc": "...",
 "decision_id": "dcd_...",        // content hash; verdicts cite this
 "trace_id": "csc_...",          // cascade grouping (v0)
 "cascade_step": 1,              // v0; 0 for single ask
 "task_shape": "summarize",
 "task_shape_version": 3,
 "chosen": "flash-mid-1",
 "considered": [ {"model_id": "...", "n": 45, "lb95": 0.91,
                  "eff_lb95": 0.89, "cost": 0.004, "qualifies": true} ],
 "reasons": ["..."],
 "trigger": "T1_confidence",     // none | T1 | T2 | T3 | T4
 "cost_usd": 0.004,
 "cumulative_cost_usd": 0.0082,
 "confidence": 0.71,
 "confidence_source": "endpoint",
 "calibration_state": "verified", // verified | unverified | poor
 "exploration": false,
 "probe": false,                  // true when this ask is a probe
 "stale": false,                  // true when decay demoted a candidate
 "ledger_snapshot_hash": "sha256 of the capability rows read at decision time",
 "principal_id": "operator-main",
 "prev_sha256": "...",
 "row_sha256": "..."}
```

Chaining identical to `mag/gwap_payload.py` (hash covers row minus its
own hash field; verify reads the FILE). Receipts remain the audit spine:
a decision we cannot audit did not happen (v0 law, kept).

## 7. Tool-surface deltas (MCP tools)

- ask / cascade: unchanged signatures, richer receipts.
- report_capability: now returns {n, pass_rate_raw, lb95, eff_lb95,
  age_days, gate_class_mix, cost_usd_last, cost_usd_ewma, quarantined}.
- record_verdict: now requires {principal_id, signature, gate_class,
  gate_id, evidence_hash, evidence_uri, receipt_ref}; rejects unbound or
  replayed verdicts (idempotency via UNIQUE (receipt_ref, gate_id)).
- NEW probe_status: shows probe budget/spend per shape (operator leash).

## 8. FALSIFIERS (five specific ways this design fails or is gamed)

- F1 VERDICT POISONING. A colluding caller+principal inflates a cell.
  Bind to G0 evidence makes inflation require forging deterministic
  checker output (hard); G1 requires two colluding principals; G3 is
  weight-capped and cannot alone lift a cell over threshold. RESIDUAL:
  two-principal G1 collusion and G2 operator capture remain possible;
  detection is the chain audit showing verdict clusters from one
  principal pair. If a poisoning red team lifts any cell's eff_lb95 over
  threshold with garbage evidence, the gate contract FAILS its acceptance
  test.
- F2 STALE-RATE DRIFT. An upstream re-pull/quantization silently changes
  a local model's ability between verdicts (the fixtures pin
  last_measured to a seed date, `tools/gps_mcp/seed_fixtures.py`; nothing
  in v0 notices). Decay + forced probes shrink the window; the residual
  window is up to half_life_days. Falsified if measured
  stale-routing incidents (routes to a model whose fresh true rate is
  below threshold) exceed 1 per 1000 routed asks after decay is on
  (ESTIMATE threshold; the eval sets the real number).
- F3 EXPLORATION EXPLOITATION / COLD-START LOCK-IN. A bad first k
  verdicts permanently freeze a cheap model out of a shape, or an
  adversary manufactures no-history shapes to force exploration-tier
  burn. Mitigations: shape registry (renames need operator signature),
  probe budget cap, n_min low enough to graduate quickly. Residual: an
  operator-blessed shape name with adversarial content distribution
  poisons one cell. Falsified if graduation from n=0 to n_min costs more
  than the cell saves in its first month (ESTIMATE, eval measures).
- F4 TAXONOMY LEAK (Goodhart). Models optimize the named shape instead
  of the work (prompt-template drift inside a stable shape name).
  task_shape_version bumps + environment hashes in evidence make drift
  VISIBLE; they do not stop it. Falsified if within-name drift explains
  more verdict variance than between-model variance in the eval corpus
  (measurable; the eval computes it).
- F5 EVIDENCE RECYCLING / REPLAY. One good artifact's hash submitted for
  many verdicts, or a verdict replayed after chain splice. UNIQUE
  (receipt_ref, gate_id) kills the replay; evidence_hash equality checks
  across distinct receipt_refs kill the recycle; the hash chain kills
  silent edits (house pattern, `mag/gwap_payload.py`). Residual: an
  attacker mutating artifacts slightly to mint "new" hashes; detection
  is input-hash clustering in the audit (near-duplicate inputs with
  identical verdicts). Falsified if the red team lands any recycled
  verdict that survives audit.

## 9. Honest scope fences (what v1 still does not do)

No multi-tenant authz beyond the principal table; no streaming; no
bandit/UCB (deferred by design, section 5.2); no automatic price feeds
(cost_usd_ewma needs a billing integration the estate does not have; the
driving ladder's funded tier is Nous/Hermes with metered credits,
`AGENTS.md` DRIVING LADDER, and Anthropic keys are unfunded, so frontier
cells will be G2/G3-poor until that changes); concurrency remains
single-writer SQLite. The spec deliberately defers all of these rather
than papering them with guesswork branches (build discipline: no
fallback-branch creep, `AGENTS.md`).

Em-dash count: 0.
