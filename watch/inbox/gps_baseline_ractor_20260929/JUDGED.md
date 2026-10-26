# JUDGED: THE RACTOR VERDICT ON THE THREE SEATS

Judge: the panel chair, 2026-09-29, after all three blind seats landed
(SEAT_A_SPEC.md, SEAT_B_ADVERSARY.md, SEAT_C_EVAL.md in this directory).
Method note for honesty: the seats were written sequentially by one model
under a no-cross-reading, no-post-hoc-revision discipline (procedural
blindness, not amnesia); the judge therefore discounts neat complementarity
and specifically hunts for overlap-shaped holes. Em-dash 0.

## 1. SEAT A (spec architect): kills and keeps

KEPT (load-bearing, survives into the baseline):
- Wilson 95% lower bound + n_min = 20 floor as the ONLY routing read
  (A section 2, 5.1). Kills v0's raw-mean threshold flip on noise.
- Verdicts bind to receipt_ref with UNIQUE (receipt_ref, gate_id)
  idempotency and chain+ed25519 per the gwap house pattern
  (`mag/gwap_payload.py`). Directly closes the hole v0 confessed
  (`watch/inbox/game_platform_basecamp_20260929/GPS_MCP_V0_20260929.md`
  critique item 2).
- Gate classes G0-G3 with weights 1.0/1.0/0.5/0.25 and the G3 cap
  (model-judge verdicts alone can never lift a cell over threshold).
  This is the correct trust ladder: deterministic > dual-independent >
  human > model-judge.
- T4 staleness trigger that schedules a PROBE instead of auto-climbing:
  staleness is a knowledge gap, not a difficulty signal. Genuinely good
  decision; frontier tokens must never patch measurement holes.
- Probe budget leash (0.50 USD/shape/week ESTIMATE) + probe_log. The
  anti-parosite organ control.
- Falsifiers F1-F5 with residuals named. Strong.

KILLED or DEMOTED:
- KILL cost_usd_ewma (alpha 0.25): speculative instrumentation with no
  billing feed to feed it; violates the no-fallback-branch-creep law
  (`AGENTS.md`, build discipline). Keep cost_usd_last only. EWMA returns
  when a real price feed exists.
- DEMOTED T2 economics trigger from firing to ADVISORY: the inequality
  multiplies a ledger estimate by an invented C_rework = 3x constant;
  precise-looking arithmetic on unmeasured inputs. T2 logs its fields on
  the receipt but may not fire alone until C_rework is measured by the
  eval (C's M1 rework data). Confidence-trigger T1 similarly only fires
  when calibration_state = verified, which A got right.
- TRIM task_shape_registry: keep (task_shape, version, canonical_gates,
  owner) and drop retired_utc ceremony. Registry stays because it is the
  only answer to B's P4, but it ships minimal.

## 2. SEAT B (adversary): kills and keeps

KEPT:
- P1 (SuperScout no-router ablation TIES: the handoff carries the result,
  `watch/inbox/game_platform_basecamp_20260929/DELEGATION_RESEARCH_20260929.md`)
  as a permanent design constraint: routing authority must be EARNED, not
  assumed. This becomes the baseline's provisional-authority clause.
- P2's two-case trap (verifier exists => per-instance signal dominates
  population priors; no verifier => ledger inputs are rumors). The
  baseline answers by making gates first-class and G3 capped, but B's
  trap stays as the reason the gate contract outranks the router in
  build order.
- P6 organ tax + the concession (kill the router, keep the instrument).
  The baseline adopts instrument-value-independent-of-routing as an
  explicit guarantee: report_capability is useful even if every kill rule
  fires.
- Pre-registration conditions C1-C7 adopted verbatim as the baseline's
  scope fences; C4 (confidently-wrong heterogeneity) is correctly
  identified as the scientific crux, and C's M6/ECE is the instrument
  that measures it.

KILLED or DEMOTED:
- P3's headline ("almost every cell is noise ... router spends its life
  unmeasured") is HALF-killed: B reasons about raw means, but an LB-based
  router REFUSES to route low-n cells rather than routing on noise
  (B could not know A's n_min). What survives of P3 is the organ
  complaint: unmeasured cells make the ledger behave like a hardcoded
  cascade minus the simplicity, which is a cost argument (P6), not a
  correctness argument. Reframed, kept under P6.
- B's absolutist framing ("should die in committee") overreaches its own
  evidence: the research brief it cites calls the combination open
  (the gap is real, same file, practice section) at confidence 0.7, and
  B's own concession keeps the instrument. B wins a scope reduction
  (provisional routing authority + mandatory eval), not a death verdict.
- P4's "gaming" sub-point (freeze a competitor model by feeding its cell
  hard instances) kept as a named residual of F1/F3, not a separate
  pillar: it requires write access the principal registry already gates.

## 3. SEAT C (eval designer): kills and keeps

KEPT:
- Four-arm paired design (ledger / cascade / classifier / fixed-mid
  floor) with identical gates and corpus, per-item paired deltas.
- Seed/eval split: the ledger arm's history comes from a DISJOINT seed
  corpus; eval items never feed the ledger before scoring. Without this
  the whole eval grades Arm 1 on its training set.
- M1 charging the WHOLE trace (gate costs + re-climb costs) to each arm;
  this imports the research brief's failed-tasks-cost-more economics
  (`watch/inbox/game_platform_basecamp_20260929/DELEGATION_RESEARCH_20260929.md`).
- M4 drift injection via test-double behavior swap (deterministic,
  $0) + detection latency. The single most decisive secondary
  experiment: it pits B's P5 against the ledger's update loop directly.
- K5 trust red team with fail-closed consequence.
- Frontier-as-double-only honesty and the explicit cannot-settle list.

KILLED or DEMOTED:
- FIXED: Arm 1 ambiguity ("tests the CONCEPT, possibly with threshold
  overridden"). The eval licenses an artifact, not a concept: Arm 1 runs
  THE BASELINE's v1 selection (LB + n_min + decay + T-triggers) exactly
  as specified in BASELINE_SPEC.md, or the eval result is unbindered.
  Amended in the baseline's acceptance-harness section.
- DEMOTED M2 to a pre-registered kill rule (C's own admission that
  n = 200 cannot power a non-inferiority test): correct and honest; the
  baseline keeps it as K2, not as a powered claim.
- TRIMMED the five-day schedule's D2 arm-wiring note to require arms as
  configs over the one router boundary (C already said this; baseline
  makes it binding so the four arms cannot fork the code).

## 4. WHAT ALL THREE SEATS COLLECTIVELY MISSED (blind spots)

- BLIND SPOT 1: CASCADE-STEP VERDICT ATTRIBUTION. No seat defines what a
  verdict means for the NON-FINAL steps of a cascade. Naive rule (final
  answer passed, so earlier tiers "failed") systematically poisons
  cheap-tier cells: a correct-but-unconfident first step would be
  counted a fail, and the ledger arm of the eval would poison its own
  seed corpus through ordinary cascade traffic. The baseline adds the
  attribution law: a verdict judges ONE step's OWN gated artifact;
  a step stopped for low confidence without gate evidence writes NO
  verdict; a cascade where only the final step was gated contributes
  exactly one verdict, to the final step's model.
- BLIND SPOT 2: LEDGER SELF-COST AMORTIZATION. C's M1 charges per-item
  costs honestly but bills the ledger's STANDING costs (forced-probe
  burn, seed-corpus construction, audit/operator time) to nobody, while
  Arm 2 (cascade) needs none of them. As written, the eval structurally
  favors the ledger. The baseline amends M1: Arm 1's cost-per-verified-
  solve includes amortized probe + seed + audit spend for the window
  (probe_log and M5 exist to measure exactly this).
- BLIND SPOT 3: PRINCIPAL LIFECYCLE AND JUDGE-RECUSAL. A's principal
  table has created/revoked and that is all. No key rotation, no
  compromise story, and no rule against the one funded judgment lane
  (Nous/Hermes per `AGENTS.md` DRIVING LADDER) acting as G3 judge over
  models its own operators run, i.e., grading work it will later be
  routed on. The baseline adds: rotation fields (rotated_from,
  expires_utc) with fail-closed expiry, and the recusal rule: a
  principal may not write verdicts on a (model, shape) cell its own
  principal family operates.

## 5. Scoreboard

| Seat | Kept core | Killed/Demoted | Verdict |
|---|---|---|---|
| A | LB+n_min, bound verdicts, G0-G3+cap, T1/T3/T4, probe leash, F1-F5 | EWMA, T2 firing, registry ceremony | spine of the baseline |
| B | P1, P2 trap, P6+concession, C1-C7 fences, C4 crux | P3 headline (half), absolutism, gaming-as-pillar | scope fences, all adopted |
| C | 4-arm pairing, seed/eval split, whole-trace M1, drift injection, K1-K5 | Arm-1 ambiguity (fixed), M2 overreach (demoted) | acceptance harness |

Em-dash count: 0.
