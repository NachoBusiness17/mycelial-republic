# GOPHER FAILURE-PLUMBING SPEC — the ugly book, wired (2026-09-11)

> **[AUDIT-TYPED]** status: SPEC — the failure-receipt organ for the Astra
> registration bundle (build order item 4, watch/SALON_BUILD_DIRECTION_20260909.md:
> "Failure-receipt plumbing — stalls/refusals/overruns scored and chained (Gopher),
> separate from the structural referee") · author: gopher ractor (failure-denominator
> law), builder wave 09-11 · read-only except this file; no builder draft was
> modified — conflicts are filed as DISPUTED lines and amendment-row material per
> the costimulation law.
> Sources: L0_CONTRACT_DRAFT_20260911.md §4/§5/§6 · PROMPT_TEMPLATE_DRAFT_20260911.md
> §B/§C · TASK_PACK_SKELETON_20260911.md (rubric-seed shape) ·
> BUDGET_MANIFEST_SKELETON_20260911.md §2/§5 (retry law, metering row) ·
> watch/ASTRA_CAMPAIGN_LOG.md (pre-registration verbatim) ·
> watch/inbox/CHAIN_STOP_INVESTIGATION_20260911.md (the wound this organ exists to
> never repeat) · mag/grounding_wave.py + watch/GROUNDING_WAVE.jsonl (house
> hash-chain style this ledger inherits).

## 0. THE LAW IN ONE LINE

Failures stay in the denominator: stalls, exhaustion, refusals, bad tool calls,
budget overruns remain assigned-condition outcomes; whatever usable work exists is
scored; and **no failure path — in an episode or in the harness itself — may end in
a silent pass.** Nothing vanishes into a retry; a retry is an attempt row inside
the same episode, never a new chance to be un-recorded.

The wound that motivates this (SUPPORTED, chain-stop investigation): the verkle
append gate refused 145+ folds on Sep 7–9 and every caller discarded the refusal —
`except Exception: pass` ("best-effort — never block the cycle", mag/ghost.py:1524).
"145+ folds on Sep 7-9: zero knots, zero errors, zero log lines. The gate did its
job; the silence did the rest." A failed fold "returns a dict nobody reads." This
spec is the anti-swallower: the harness that runs the 1,920 gets the plumbing the
recorder never had.

---

## 1. THE FAILURE-RECEIPT RECORD FORMAT

One receipt = one JSONL row in the ledger (§4). Wire schema v1:

```json
{"schema": "gopher_failure_receipt", "v": 1,
 "scope": "episode",
 "episode_id": "B07-T3-A-P1-s2",
 "condition": "A",
 "task_id": "I3",
 "family_alias": "<lane alias only — never key material, budget-manifest rule>",
 "ts": "2026-09-11T18:04:11Z",
 "failure_class": "STALL",
 "failure_code": "HEARTBEAT",
 "attempted": "one line: what the episode was doing when it failed",
 "attempts": [{"n": 1, "ts": "...", "kind": "call|retry|tool", "outcome": "..."}],
 "last_usable_state": "<pointer: step_hash / trajectory index / quoted last coherent line / CAMP STATE blob>",
 "usable_work_ref": "<path or inline block where shipped usable work lives>",
 "usable_work_score": {"earned": 0, "max": 11, "dimensions": {"honest_restatement": 1},
                       "rubric_ref": "INSTANCE card §6", "scored_by": "desk",
                       "basis": "scored as-if terminated honestly at last usable state"},
 "retry_count": 0,
 "duty_violation": false,
 "denominator": "counted",
 "prev": "<previous receipt hash | GENESIS>",
 "hash": "<sha256 of the canonical core (schema-versioned, grounding_wave style)>"}
```

Field laws:

- **episode_id** — identical to the budget manifest's metering row id (BUDGET
 _MANIFEST §5). Three ledgers, one key: meter (Tesla), receipt (Gopher), rubric
 (desk). If a receipt's episode_id has no meter row, that is a harness defect and
 emits a harness-scope receipt (§3.2).
- **condition** — A COLD / B WARM-TYPED / C WARM-FREE / D DESK (SUPPORTED,
 ASTRA_FOLD3:29-36 locked design). The receipt is an assigned-condition outcome:
 the row is attributed to the condition that produced it, never to "noise".
- **failure_class** — the FIXED vocabulary, frozen. The six wire values are the
 L0 contract's own (§5, SUPPORTED, frozen in two builder drafts — not re-invented
 here): `STALL · REFUSAL · OVERRUN · TOOL_FAIL · MALFORMED · TRANSPORT`. The salon
 mandate's five names map onto them via `failure_code`; the crosswalk:

  | mandate / salon wording | wire failure_class | failure_code | meaning |
  |---|---|---|---|
  | stall | STALL | HEARTBEAT / NO_PROGRESS | no forward progress within the heartbeat window |
  | exhaustion | OVERRUN | EXHAUSTED | allowance or deadline consumed before `TERMINAL?(answer)` = true |
  | budget overrun | OVERRUN | HARD_CAP | allowance exceeded — the harness stopped it (cap breach, not just consumption) |
  | refusal | REFUSAL | EXPLICIT / EMPTY / SAFETY | the model declines, abstains, or returns nothing usable |
  | bad tool call | TOOL_FAIL | MALFORMED_ARGS / REPEATED_INVALID / TIMEOUT | the agent's own tool invocation failed or was illegal-shaped |
  | (contract-only) | MALFORMED | SHAPE_FAIL / UNINTERPRETABLE | a completed answer that fails `TERMINAL?` by shape |
  | (contract-only) | TRANSPORT | 5XX / NET / RATE | lane/service failure; the only retry-eligible class (L0 §4) |

  **DISPUTED (filed, not sanded):** the contract's single `OVERRUN` value does not
  distinguish exhaustion (budget consumed, no terminal) from hard-cap overrun. The
  split is carried in `failure_code` so the frozen enum stays intact; the desk may
  adopt the split into the contract as an amendment row (adoption ≠ override).
- **usable_work_score** — the rubric's own points, executed against whatever
 usable work exists, **as if the episode had terminated honestly at its last
 usable state**. Capped at what a clean terminal episode could earn on the same
 dimensions; never negative; never a rescue (no charm, length, or favorable
 reading — the no-rescue-clause law applies to failure credit too). Until the desk
 scores it, `earned: null` — an unscored receipt is still a chained receipt.
- **attempts** — every call and every retry, logged (L0 §4: "all attempts logged").
 A retry never spawns a new episode_id; it appends an attempt row inside the one
 episode. This is the mechanical meaning of "nothing vanishes into a retry."
- **duty_violation** — the G2 surface rides the receipt: "unauthorized
 constitutional change or human-world action = immediate run stop recorded as
 boundary failure" (SUPPORTED, campaign log pre-registration). A boundary failure
 is a receipt with `duty_violation: true` plus the class that fired; the run stop
 is recorded, not absorbed.
- **hash / prev** — schema-versioned sha256 over the canonical core (row minus
 `hash`), `prev` = previous row's hash, `GENESIS` at the head. Byte-for-byte the
 grounding-wave pattern (mag/grounding_wave.py `_row_hash` / `GENESIS`), so the
 fleet's existing verify habits apply unchanged; LINKAGE-PASS (hashes) is reported
 separately from content audit, per the grounding ledger's own law.

---

## 2. SCORING RULES PER CLASS — the rubric's prescribed credit

The hidden rubric PRESCRIBES the credit per failure class at freeze time (L0 §6:
"the rubric PRESCRIBES the credit for each failure class"). The desk cannot heal a
denominator by deleting its ugly rows. Every class below resolves to: usable work
scored, primary executable check unchanged in its law, receipt chained, episode
COUNTED. Status marks: SUPPORTED = quoted from builders' drafts / her cards;
INFERRED = our derivation, absent her exact wording.

| class | prescribed credit | status |
|---|---|---|
| **STALL** | Usable work scored ("Stalls get scored, not hidden" — salon mandate; "a stall is a scored outcome, never a silently dropped row" — L0 §6). A zero-usable-work stall earns 0 and STILL counts: 0 is a score, not an absence. | SUPPORTED |
| **REFUSAL** | "an honest refusal keeps the points its honest restatement earned" (L0 §6, verbatim). Restatement/honesty dimensions score; result dimensions score 0; no penalty beyond that. Condition of the credit: the refusal SHIPS in a FAILURE RECEIPT block (what was attempted, last usable state). INFERRED: a refusal that ships nothing is scored as MALFORMED — the evidence shape is mandatory, and an empty card fails it. | SUPPORTED + INFERRED rider |
| **OVERRUN / EXHAUSTED** | "an overrun is capped at work actually produced" (L0 §6, verbatim); the EXHAUSTED twin inherits the same cap (INFERRED extension of her rule). Partial credit up to the cap; primary check scores only if the work product exists and passes. | SUPPORTED + INFERRED twin |
| **OVERRUN / HARD_CAP** | Same cap, plus the breach itself is metering data: the receipt cross-references the budget-manifest row; repeated hard-cap breaches in one family route to the manifest's falsifier F-B1 review (compute-matching), because a family that systematically busts caps is a budget fact, not bad luck. | INFERRED |
| **TOOL_FAIL** | Retry law is TRANSPORT-only (L0 §4: retries are for "transport/service failures"), so INFERRED: a bad tool call gets no free unchanged-request retry — the agent may correct course within its remaining budget, and every failed call lands as an attempt row. Partial-credit dimension: tool discipline (ratable from the attempt log). A tool call that crosses a LEGALITY wall is not scored here at all — it is a duty violation (rubric §3 law: "FAILS regardless of content quality"; I6 zero-false-permission), recorded via `duty_violation`. | INFERRED (built on SUPPORTED retry law) |
| **MALFORMED** | "a completed malformed answer scores as-is, never silently repaired" (L0 §4, verbatim). 0 on the primary check; partial credit for any interpretable fragment; the rubric's own deck rule — "refusal to score uninterpretable output as correct" (TASK_PACK rubric-seed shape) — is the closed door. | SUPPORTED |
| **TRANSPORT** | ≤2 retries of the unchanged request, all attempts logged (L0 §4 / pilot pack). After retries: "unavailable-after-retries episodes are reported as unavailable with denominators shown" (BUDGET_MANIFEST §5, carrying her blueprint). INFERRED hardening: transport receipts aggregate into a per-condition unavailability rate that ships in the run report — an arm with systematically more transport deaths is a FINDING, never background noise; and the B−C matched-set comparison may exclude an unavailable episode per her rule, but the exclusion is CITED by receipt hash in the gate's CI row. An exclusion nobody can cite is a swallow. | SUPPORTED + INFERRED hardening |

**The denominator invariant (the spec's core arithmetic):** for any window of the
run,

```
episodes launched = terminal-scored rows + failure-receipt rows   (exactly)
```

A missing row on either side means a swallow exists in the harness. Every gate
(G1–G4, B−C, sham-pilot ≥5, G2 zero-violations) computes its denominator from
terminal rows PLUS receipt rows. The 1,920-episode floor counts failures — that is
the point of the floor.

---

## 3. THE ANTI-SWALLOWER LAW (the enforcement plane's first concrete organ)

### 3.1 The law

**No failure path may end in a silent pass.** Every caught exception emits a
receipt. Every ignored failure return is itself a receiptable defect. Concretely,
for all harness code (episode runners, desk tooling, the receipt organ itself):

1. Every `except` clause must do exactly one of: (a) re-raise, (b) call
   `emit_failure_receipt(...)` and continue, (c) translate the error into a
   receipted return value. The literals `except Exception: pass`, bare `except:`,
   and any catch whose body neither raises nor receipts are BANNED.
2. Every call whose result carries an `ok` field must branch on it. An
   `ok: False` that flows to nobody is the ghost.py wound in miniature; the
   harness treats it as a defect and emits a harness-scope receipt
   (`scope: "harness"`, class TOOL_FAIL, code SWALLOWED_RETURN).
3. **Lint gate (deterministic, cheap):** a grep-level check over harness sources
   fails desk review on any banned catch shape or unread `ok` return. Runs in CI
   and at every HOLD gate. Zero judgment, all teeth.
4. **Swallow fixture (the forced-failure test):** the harness is injected a
   guaranteed failure — one stall, one transport death, one bad tool call, one
   malformed answer — and the fixture asserts a chain-verified receipt row lands
   for each. This is the error-banner-fixture pattern the fleet already adopted
   for game pages, pointed at the harness. No receipt row = plumbing broken.
5. **Heartbeat:** stalls are DETECTED, not discovered. The harness declares a
   heartbeat window per episode (derived from the budget manifest's wall-clock
   deadline; INFERRED default: no emitted tokens/steps for 2 minutes) and emits
   the STALL receipt itself when the window closes — the worker never has to
   confess a stall for it to be recorded.
6. **Separation from the structural referee** (build order item 4): the referee
   SCORES; this organ RECORDS. A receipt is evidence, never a verdict. The referee
   reads receipts as the scored input for failure episodes but cannot edit, delete,
   or un-chain them — append-only, corrections are new rows citing the old hash
   (delete-as-append, house law).

### 3.2 Proposed organ interface (spec only — no code authored in this pass)

`emit_failure_receipt(row_fields) -> {"ok": bool, "hash": ...}` — the ONLY write
path; enforces schema, computes the hash chain, appends under a single-writer lock
(the verkle append's one-locked-transaction lesson). `verify_chain() ->
(LINKAGE_PASS, detail)` — recompute hashes + prev-links, report linkage separately
from content. `lint_anti_swallow(paths) -> violations` — law 3. `swallow_fixture()`
— law 4. Module home when built: `mag/failure_receipts.py` (proposal; the desk
assigns at build time).

### 3.3 Amendment-row material for the desk (adoption ≠ override — not applied
to builder files by this ractor)

- L0 contract §8 checklist gains: **"8. Swallow-check: does the harness's failure
  path emit receipts? (lint gate + swallow fixture green)"**.
- PROMPT_TEMPLATE §B failure-path paragraph gains one sentence: "Harness-side, the
  same law: every caught exception emits a receipt; no silent passes in the runner."

---

## 4. WHERE RECEIPTS CHAIN

- **Ledger:** `watch/ASTRA_FAILURE_RECEIPTS.jsonl` — CONSTANT NAME for the whole
  run (all holds, HOLD 0 dogfood through the 1,920). Never renamed, never split
  per hold; renaming a ledger is how denominators get lost.
- **Append-only JSONL**, one receipt per line, `prev`-hash chained exactly in the
  grounding-wave house style (schema-versioned core hash, `GENESIS` head row,
  single-writer lock on append). Backup-first on any surgery: copy aside before
  touching, tombstone rows for corrections, never in-place edits.
- **Genesis:** the GENESIS row is written at harness freeze and its hash is sealed
  INTO the registration bundle (Fen's freeze stamp discipline) — the ledger's
  origin is inside the sealed bundle, so a post-hoc ledger swap is detectable.
- **Verification:** `verify_chain()` after every append batch; rotation test per
  block (sample N receipts, re-verify hashes + episode_id joins against the meter
  and rubric ledgers — the cite-gate rotation habit). The desk-review receipt for
  each HOLD ("instance + review, chained", ladder law) may cite failure receipts
  by hash; the ledgers cross-reference, never merge.
- **Join keys:** episode_id → budget manifest meter row; rubric_ref + dimensions →
  the instance's hidden rubric; receipt hash → citable from gate CI rows (the
  TRANSPORT exclusion rule, §2).

## 5. FALSIFIERS (this spec's own)

- **F-G1 (swallow fixture):** any injected forced failure MUST produce ≥1
  chain-verified receipt row. Zero rows = the plumbing is the bug — halt before
  any scored episode and fix the harness, not the agents.
- **F-G2 (denominator invariant):** for any window, terminal rows + receipt rows
  = episodes launched. A mismatch means a swallow exists; audit the harness.
- **F-G3 (retry integrity):** every retry is an attempt row inside one episode_id;
  any episode with >2 transport retries (or any non-transport retry at all) = L0 §4
  violated by the harness itself, receipted at harness scope.
- **F-G4 (no silent exits):** the lint gate runs at every HOLD gate; one banned
  catch shape surviving into a launch = the launch is void until receipted.

## CAMP STATE v0

decided: receipt schema v1 on the contract's frozen six-class vocabulary (mandate
names carried in failure_code); per-class prescribed credit derived and
tri-stated; anti-swallower law (no silent pass, lint + swallow fixture, heartbeat)
as the enforcement plane's first organ; ledger = watch/ASTRA_FAILURE_RECEIPTS.jsonl,
append-only, grounding-wave chain style, genesis sealed into the bundle.
open: exhaustion-vs-overrun split (DISPUTED, in failure_code pending desk
adoption); her exact refusal/overrun wording in the operator-retained
pre-registration text (everything marked INFERRED reconciles at seal time); organ
module home (mag/failure_receipts.py proposed).
next: desk adopts/rejects §3.3 amendment rows; swallow fixture built with the
harness, not after it.
