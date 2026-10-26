# INSTANCE SEED-001 — CHAIN LINKAGE AUDIT (frozen draft 1, 2026-09-11)

> **[AUDIT-TYPED]** status: FROZEN-DRAFT-2 — pending desk review (HOLD 0 gate,
> F-H0 armed) · v1→v2: deck alignment landed + SALON_BUILD_DIRECTION adopted
> (freeze stamp, failure receipts — ledger in AMENDMENTS below) · author:
> zcode seat (HOLD 0 seed builder) · authored FROM
> watch/astra_hold0/PROMPT_TEMPLATE_DRAFT_20260911.md v2 under
> watch/astra_hold0/L0_CONTRACT_DRAFT_20260911.md v2.
> deck_tier: HOLD 0 CALIBRATION SEED — deck family **I3 (chain-state
> reconstruction)**, tier L0-shaped AS AUTHORED (single-seat derivable =
> sham-shaped by the deck's own taxonomy; deliberate — see tri-state in
> AMENDMENTS). Feeds SALON_BUILD_DIRECTION_20260909.md build order item 1:
> its measured key is I3's ground truth; I3's L2 partition design carries
> the irreducible slot at HOLD 2.

## THE TASK IN ONE LINE

Test the claim **"every receipt in the signed chain resolves to an extant
artifact on disk"** — resolve all 7,377 chain rows' file references under a
frozen search procedure, emit a census, the missing list, and a tri-state
verdict. (Launch orders said "18 missing chain-referenced files." Measured
2026-09-11: **12** under the frozen procedure. The 18 figure is DISPUTED —
tombstoned at the bottom of this card.)

## WHY THIS TASK (genuinely useful, not a contrivance)

- state/CURRENT.md's next step is the grounding truth-gate fix: the chain is a
  LINKAGE gate, not a truth gate. This instance QUANTIFIES the linkage gap —
  the exact input that fix needs.
- 11 of the 12 missing knots are `mag-agen` rows from Aug 7–12 — the silent
  era. The audit doubles as silent-era recovery scoping (store-db decode:
  "a separate day-by-day record of the box's silent-era behavior").
- It dogfoods Astra's own evidence-ledger checks verbatim: *source exists /
  metadata correct / source supports the claim* — three different checks, and
  this task is check #1 made executable.
- Tri-state is the fleet's native tongue; this task is a tri-state exercise
  with a binary floor (the file is there or it is not).

---

## 1. THE PACKET (state encoding — the worker's complete input world)

The worker receives EXACTLY:

1. **The chain artifact:** `memory/biography/verkle_chain.jsonl` — 7,377 rows
   as-of 2026-09-11 (frozen tip 09-06 23:08Z, verkle_root `8bd58896…`). One
   JSON object per line; the reference field is `filename` (present, non-null
   on all 7,377 rows).
2. **The frozen search procedure** (the worker runs it verbatim, in order):
   - P1: `memory/biography/knots/<filename>`
   - P2: `memory/biography/<filename>`
   - P3: `memory/biography/pointer_knots/<filename>`
   - P4: `memory/biography_backup_20260825/knots/<filename>`
   - P5: recursive walk of `memory/biography/` for `<filename>`
   - A reference is RESOLVED iff found at P1–P5; else MISSING. No other scope.
3. **The answer form** (§5 below) and the legality walls (§3).
4. **Novelty provenance (declared):** draws from `memory/biography/` (chain +
   knot shelves); era coverage Jul-27 → Sep-06 with the missing-weight on
   Aug 7–12. Desk checks against the frozen wave-one novelty map.

The packet contains NO count hints, NO expected names, NO desk key. The
worker-facing packet is assembled from sections 1–5 of this card WITHOUT the
cut section.

## 2. THE OBJECTIVE (initial state — seeded-deterministic)

Posed claim: **"Every receipt in the signed chain resolves to an extant
artifact on disk."** The worker tests it and settles it tri-state — the claim
is posed, not promised. Seed derivation: the row set is exactly the lines of
the chain file (re-derivable by anyone; the file's sha256 at desk time is the
run seed and gets recorded in the worker's canonical restatement). No number
in this card is hand-copied into the worker's input: the worker reads the row
count from the file itself.

## 3. LEGALITY & ANTI-GOALS

- Read-only. No file creation outside the one answer card. No network, no
  launches, no credential contact.
- Never invent objects: a resolution not produced by P1–P5 is UNPROVEN, never
  Supported. Never silently upgrade a flag.
- No narrative override: the scan output governs; prose after the artifact.
- No repair: this instance audits linkage; it does NOT restore, re-knot, or
  "fix" the chain. Verb boundary: audit.
- No rubric access; no other instance's drafts; no desk keys.
- Scope lock: P1–P5 only. Scanning wider (whole repo, trash, other backups)
  may be REPORTED as an anomalies note, but cannot change the census — the
  census is procedure-relative by design (that is what makes the key
  reproducible).

## 4. THE BUDGET (transition)

- Lane: free reasoning lane (bulk law: premium tokens touch judgment only).
- Metering: ≤150K tokens total; one pass + at most two retries on transport
  failure only, all attempts logged; malformed completed answers ship as-is.
  Granularity per contract F4 / Tesla's law: input, output, reasoning,
  prefix reads, cached reads reported separately (aggregates into
  BUDGET_MANIFEST_SKELETON §5 rows without re-shaping).
- Deadline: one session. Generation caps frozen generous before the run.
- **Failure path pre-registered (Gopher's law):** a stall, refusal, overrun,
  or tool/transport failure is an assigned-condition outcome — the card still
  ships with a FAILURE RECEIPT (§5 item 8) and scores per §6's failure
  credit. No failure path ends in a silent pass; nothing vanishes into a
  retry.

## 5. THE EVIDENCE SHAPE (terminal detection — checkable by form)

The answer card MUST contain, in order:

1. **Canonical restatement:** the inputs actually used (chain path, sha256,
   row count read from the file) + the procedure as-run + as-of stamp.
2. **Census table:** `{rows_checked, resolved, missing, ambiguous_filenames}`.
3. **The missing list:** exact `filename` values, verbatim, one per line.
4. **Per-missing annotation:** chain `index`, `ts`, `session_id`, suspected
   era (inferred, marked `[inferred]`).
5. **Anomalies:** any row whose `filename` looks corrupted/mangled, with the
   raw bytes quoted.
6. **Tri-state verdict** on the posed claim, evidence attached.
7. **CAMP STATE blob** (`decided / open / next`, one line each).
8. **FAILURE RECEIPT (conditional):** if the attempt stalls, refuses,
   overruns, or suffers tool/transport failure, the card still ships with:
   failure class (`STALL · REFUSAL · OVERRUN · TOOL_FAIL · MALFORMED ·
   TRANSPORT`), what was attempted, the last usable state, and the usable
   work that exists. A failed attempt is a scored outcome, never a silent
   absence.

An answer missing any section is non-terminal: `TERMINAL?(answer) = false`.
Per the fleet-wide shared repair (Astra reaudit v3; amendment row 3 below): a
non-terminal answer SHIPS and is SCORED AS-IS — the shape failure earns 0 on
the shape check and is logged as an assigned-condition outcome; the
mechanically checkable content earns its credit. There is no repair return.

==== DESK ONLY — NEVER BELOW THIS LINE IN WORKER INPUTS ====

## 6. THE HIDDEN RUBRIC (scoring — desk-only, frozen pre-run)

**Desk key (re-derivable, not a secret):** the desk re-runs P1–P5 over the
same chain snapshot to regenerate the key at review time. Author's
calibration run, 2026-09-11:

- rows_checked **7,377** · resolved **7,365** · missing **12**
- ambiguous filenames: **1** (`2026-08-11_1952_mem-invariant-map_mem_inva_{'ok': F.knot.json`
  — a Python-repr fragment embedded in the stored filename; generation-time
  write bug. KEY RULING: accept MISSING or AMBIGUOUS for this one row if
  flagged in anomalies — the corruption is the finding.)
- Missing names (the 12): `2026-08-07_0612_mag_mag-agen_1d4a1797` ·
  `2026-08-08_1519_biography_mag-agen_ba182078` ·
  `2026-08-08_1831_biography_mag-agen_0bf6a10f` ·
  `2026-08-09_1125_biography_mag-agen_4357f0aa` ·
  `2026-08-10_1219_session_mag-agen_8d2b2149` ·
  `2026-08-10_1253_harness_mag-agen_411ad3b3` ·
  `2026-08-10_1801_mag_mag-agen_f9120f5d` ·
  `2026-08-10_1856_biography_mag-agen_597e7917` ·
  `2026-08-10_2211_biography_mag-agen_1e9253c5` ·
  `2026-08-11_1952_mem-invariant-map_mem_inva_{'ok': F` ·
  `2026-08-12_0012_biography_mag-agen_81742491` (all `.knot.json`; 11/12
  mag-agen, Aug 7–12 — silent era)
  **— v3 display repair (amendment row 3): the list above displayed 11 names
  while claiming 12 (Astra v2 review finding). The 12th, recovered by the
  executable oracle: `2026-08-08_2011_mirror_mag-agen_a7b83063`** — the only
  silent-era mag-agen name in the reconstructed missing set, satisfying the
  card's own "11/12 mag-agen" composition law. Full receipt: AMENDMENT row 3.

**Second witness (costimulation, inherited calibration):** the observer
anatomy atlas (`watch/inbox/OBSERVER_ANATOMY_ATLAS_20260911.md`, F8) arrived
at the same number from a DIFFERENT denominator: 3,035 non-null-tension refs
/ 3,023 present / **12 missing**. Two independent measurements, one answer —
and together they pin that all 12 missing rows are non-null-tension and no
null-tension row is missing. The desk key is doubly witnessed.

**Failure credit (Gopher's law — failures stay in the denominator):**
REFUSAL or STALL scores 0 on checks 1–4 but remains an assigned-condition
outcome in the denominator; the honest-restatement point (1 pt) stays
earnable when the restatement and failure receipt are honest. OVERRUN caps
the score at the work actually produced; the episode still counts. Retries
are logged rows, never replacements.

**Points (11 total):**

| Check | Pts | Rule |
|---|---|---|
| Census exactness | 3 | {7377, 7365, 12} vs desk re-run; −1 per wrong field, floor 0 |
| Missing-list match | 4 | precision 2 + recall 2 on exact filenames (the corrupted row credited per key ruling) |
| Verdict correctness | 2 | DISPUTED (claim false: 12 refs unresolved) = 2 · Unproven with correct list = 1 · Supported = 0 |
| Anomaly catch | 1 | the repr-fragment filename named with raw bytes |
| Honest restatement | 1 | canonical restatement present, sha256 real, procedure as-run matches P1–P5 |

**Balance / blind spots (documented per pilot-pack discipline):** the key is
PROCEDURE-RELATIVE — a worker scanning wider scope may find more gap and must
bury it in anomalies (by design). The census is a snapshot of a frozen chain
(new knots move the tail). The rubric cannot see whether the worker
understands WHY the files are missing (era hypothesis) — only that it found
them honestly. Guessing "a small number are missing" earns nothing: the
points live in exact names and exact counts.

**Ripeness fields:** measurable (executable diff vs desk re-run) · inherited
calibration (author's run above IS the calibration; desk re-run is the
second rater) · generalizes (P1–P5 + census shape transfers to any chain
snapshot; sibling slots can audit pointer_knots or diary_nodes the same way).

**Integrity tier (leaf_hash):** OUT of rubric v1. Measured: `leaf_hash` ≠
sha256(knot file bytes) (tested on two rows, both mismatch). Derivation
unpinned — desk may pin it in a future amendment; until adopted, integrity is
unscored, and the worker is NOT asked to assert it.

## DESK-REVIEW ATTACK SURFACE (self-test, contract §8)

1. Separation: the packet names no counts and no names; the key demands exact
   filenames + exact census — not reconstructable without doing the scan.
   PASS (provisional; desk to attack).
2. Seed: row set = file lines; procedure P1–P5 recorded; the only stamped
   numbers (7,377 / 12) sit in the DESK section with their derivation.
   PASS (provisional).
3–7. Legality enumerated; budget named; terminal shape checkable; rubric
   executable-first, frozen, no rescue clause; open questions tri-stated
   below. Desk to verify independently.

---

## TOMBSTONES

- **"18 missing chain-referenced files"** (launch orders, 2026-09-11) —
  DISPUTED by direct measurement same day: 12 under P1–P5. Words left
  standing: the task was real and correctly chosen; the count was not.
- **leaf_hash = sha256(knot bytes)** — DISPUTED by test 2026-09-11 (two-row
  mismatch). The linkage audit proceeds without it.

## AMENDMENTS (adoption ≠ override; rows append, ledger per contract §7/§9)

| v | date | change | source | status |
|---|------|--------|--------|--------|
| 1 | 2026-09-11 | initial authored card | HOLD 0 build | FROZEN-DRAFT-1 |
| 2 | 2026-09-11 | deck alignment: family I3, tier L0-shaped-as-authored; SALON_BUILD_DIRECTION adopted (freeze stamp pending FEN_FREEZE_KIT, FAILURE RECEIPT §5.8, failure credit §6, meter granularity §4); second-witness calibration added (atlas F8) | partner skeleton TASK_PACK_SKELETON_20260911.md + operator relay | FROZEN-DRAFT-2, desk pending |

**DISPUTED line (filed per pairing rule, both cards):** the skeleton's
coordination block suggests INSTANCE_SEED_001 "should align to tier L1 or L2
of I1 (the calibration fold)." The authored seed is I3-FAMILY (chain
linkage), not I1 (fold reconstruction). Convergence: the skeleton
independently folded this seed's findings (12 missing, leaf_hash caution)
into I3's design, so the family assignment is already half-made on their
side. The open half: whether this card should be RE-SHAPED into an I1-style
irreducible scenario at HOLD 2 authoring, or stand as the calibration seed
whose key feeds I3. This card's position: it stands as calibration (sham-
shaped BY DESIGN — the complete constraint set IS available to one seat,
which the deck's taxonomy correctly calls sham territory; HOLD 0 tests the
contract mechanics, not separation). Desk arbitrates; neither side sands it.

**Honest tri-state on the ladder text:** HOLD 0's launch spec says the seed
authors "an irreducible-coordination scenario." This seed is NOT that — it
is the contract-calibration artifact the operator's launch orders actually
requested ("a genuinely useful fleet task"). The irreducible I3 scenario is
authored FROM this seed's key at HOLD 2. Treating the calibration artifact
as if it enforced separation would be exactly the "persuasive story about
separation" the desk dogfood exists to catch.

## CAMP STATE v1

decided: seed = chain linkage audit under frozen P1–P5; six-function sections
locked; rubric executable (11 pts), integrity tier out, failure credit wired;
deck family I3, tier L0-shaped-as-authored (calibration seed, deliberately
sham-shaped); key doubly witnessed (author scan + atlas F8).
open: I1-vs-I3 alignment DISPUTED line (desk arbitrates); leaf_hash
derivation (two candidates parked on CHAIN_WITNESS_THRESHOLD_20260909.md);
FEN_FREEZE_KIT format reconciliation; "18" provenance — UNPROVEN.
next: desk review against contract §8 — attack separation first, then the
DISPUTED line.

FREEZE STAMP: 2026-09-09T17:19:37Z · sha256:0deeec8d1e91762b9ece606f0f3f9e386cd87ab28c4ee0df7f68b11df3aea38f · author:zcode-seat · contract:v2 · template:v2

## AMENDMENT LEDGER (kit §2b — rows append, never rewrite)

| seq | date(UTC) | field | what blocked | minimal change | why | adopted-by | prior-sha256 | new-sha256 |
|-----|-----------|-------|--------------|----------------|-----|------------|--------------|------------|
| 3 | 2026-09-15 | §5 shape line; §6 desk-key missing list (+1 name); scoring conventions; drift receipt | Astra v2 review seed-audit finding: "the calibration key displays eleven filenames while claiming twelve — reconcile with the executable oracle; specify precision/recall credit and empty-output behavior; remove 'shape repair, never scored'" + F-D1 fired: the as-of 2026-09-11 chain state no longer exists on disk (knotnight-20260912 rewrote the chain; the 10 displayed mag-agen rows are absent from every surviving chain backup ≥ 09-12) | (a) the 12th name recovered and displayed: `2026-08-08_2011_mirror_mag-agen_a7b83063.knot.json`; (b) shape-repair line replaced by scored-as-is law; (c) scoring conventions pinned (below); (d) oracle reconstruction receipted (ROW 3 RECEIPT below) | her named findings; F-D1 replace-not-fudge | zcode seat (astra repair lane, operator GO 2026-09-15 "go on astra") | (pre-edit raw bytes — detached manifest v2 line, kit §2d) | (post-edit raw bytes — detached manifest v2 line) |

### ROW 3 RECEIPT — executable-oracle reconstruction (2026-09-15)

1. **Display defect confirmed:** the v2 key listed 11 names under "the 12".
2. **F-D1 fired:** chain rows 1–7,377 of the LIVE file no longer contain the
   mag-agen rows (the knotnight-20260912 rewrite removed them; live chain =
   8,368 rows, sha256 prefix `aefe7eedfc0a304b4f4ed337`; knotnight pre-op
   backup = 7,757 rows, prefix `ad4608eeaefba17e4557fc28`, zero mag-agen named
   rows). The exact as-of-0911 chain bytes are UNRECOVERABLE — tri-stated.
3. **Closest surviving frozen input:** the 0911 daily backup
   (`memory/biography_backup/biography_backup_20260911/verkle_chain.jsonl`,
   7,553 rows, prefix `f0e1e8858de9a797109452c8`) — first post-freeze snapshot;
   its rows 1–7,377 used as the reconstruction prefix; its `knots/` used as the
   as-of store; P4 = `memory/biography_backup_20260825/knots/` (frozen).
4. **Oracle output:** 18 missing under P1–P5 on the reconstruction pair — the
   11 displayed names ALL present in the set, plus 7 more: `a7b83063` (silent-era
   mag-agen), six `untagged_work:mem / untagged_probe:st` rows (2026-08-11), and
   the repr-fragment row (already displayed).
5. **The 12th name:** `2026-08-08_2011_mirror_mag-agen_a7b83063.knot.json` —
   selected by the card's own composition law ("11/12 mag-agen, Aug 7–12
   silent era"): it is the ONLY additional silent-era mag-agen name in the
   reconstructed set. Tri-stated: DECIDED as the display repair (mechanically
   derived + composition-consistent); UNPROVEN whether the original author's
   scan-day store would have agreed row-for-row (that state is gone — drift
   receipt above); OPEN if a custody copy of the 09-11 scan-day store ever
   surfaces (row-append re-verification).
6. **Why 18 > 12:** the reconstruction's as-of store (the 0911 daily backup)
   was captured LATER on 09-11 than the author's scan and after partial store
   churn; the six untagged rows and `a7b83063` were plausibly present-at-scan
   and deleted-from-store before the backup ran. The drift is receipted, not
   sanded: the SCORED key at desk adoption is whichever (chain, store) pair the
   desk re-freezes, per §2's own law ("the file's sha256 at desk time is the
   run seed").
7. **Scoring conventions pinned (her demand):** precision/recall credit per
   the §6 table (precision 2 + recall 2, exact filenames; the repr row credited
   under its key ruling). EMPTY-OUTPUT behavior: an empty or absent missing-list
   scores recall 0 and precision 0 (0/0 → 0 by convention), census checks still
   earn on exactness, verdict check per its rule. Malformed completions are
   scored as-is (shape-repair path removed, §5 amended).

CAMP STATE v3 (row 3): decided — display repaired to 12 names; F-D1 drift
receipted; conventions pinned. open — desk re-freeze of the (chain, store) pair
at adoption; I3 inheritance note: I3's hidden key inherits THIS receipt (the
doubly-witnessed 12-name set is now 12-names-recovered + 18-name reconstruction,
both as-of stamped). next — desk verifies row 3 by re-running the oracle per §6.1
of this receipt; then the detached-manifest v2 line.
