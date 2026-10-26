# L0 TASK CONTRACT — DRAFT 2 (the seed hold's constitution, 2026-09-11)

==== FREEZE STAMP ====
artifact:     watch/astra_hold0/L0_CONTRACT_DRAFT_20260911.md
sha256:       83e40878892748fe5c19fa417b57cfd66aa394be2d4bd20d9c6ce79fdef7b091
frozen-at:    2026-09-09T19:25:24Z
author:       zcode seat (HOLD 0 seed builder; night rotation, eval-upgrade lane)
amendments:   v2→v3 (§9 ledger; v2 trailing stamp below preserved as lineage)
kit:          FEN_FREEZE_KIT_20260911.md
=======================

> **[AUDIT-TYPED]** status: FROZEN-DRAFT-2 — pending desk review (HOLD 0 gate) ·
> v1→v2 adopts watch/SALON_BUILD_DIRECTION_20260909.md (Fen / Tesla / Gopher
> mandates; ledger in §9) ·
> author: zcode seat (HOLD 0 seed builder, operator GO 09-11) · provenance:
> watch/corpus/L0_CANONICAL.md (the canonical six-function room interface) ·
> watch/SUBAGENT_HOLD_LADDER_20260909.md (HOLD 0, desk dogfood, F-H0) ·
> watch/ASTRA_CAMPAIGN_LOG.md CHUNK 1 CAMP STATE v1 (the registration bundle's
> work list) · watch/astra_pilot/pilot-prompt-pack.md (the evaluator-cut-line and
> freeze disciplines) · .agents/skills/operator-corrections/SKILL.md (fleet law).
> **Falsifier F-H0 binds this document:** 3 consecutive desk rejections of seed
> instances = this contract is the bug, not the agents.

## 0. WHAT THIS CONTRACT IS

Astra's campaign log (CHUNK 1) demands the 12 task instances be authored "from the
game subsystem audit's L0 contracts." The audit names the convergence: **the game
L0 contract = event layer interface = room-as-benchmark spec.** A benchmark task
instance IS a room. Therefore the canonical six-function room interface
(watch/corpus/L0_CANONICAL.md §1) compiles 1:1 into the six specification duties
every task instance must satisfy. One machine, two vocabularies — this document is
the dictionary.

A conformant task instance MUST specify exactly six functions. Two equivalent
labelings exist; the **canonical binding** (SELF names, spec-level) is authoritative
and maps 1:1 onto the benchmark-face names:

| # | SELF name (canonical) | Benchmark-face name | What it pins |
|---|----------------------|---------------------|--------------|
| 1 | `setup` / STATE ENCODING | **THE PACKET** | the worker's complete input world; the information-separation boundary lives here |
| 2 | `turn` / INITIAL STATE | **THE OBJECTIVE** | the posed claim/task, seeded-deterministic from repo state |
| 3 | `legal` / LEGALITY | **LEGALITY & ANTI-GOALS** | `LEGAL?(action) -> {legal, reason}`; forbidden moves enumerated |
| 4 | `move` / TRANSITION | **THE BUDGET** | metered work moves: token allowance, tool calls, retries, deadline |
| 5 | `evaluate` / TERMINAL DETECTION | **THE EVIDENCE SHAPE** | what the terminal answer must look like; `TERMINAL?(answer)` is checkable |
| 6 | `render` / SCORING | **THE HIDDEN RUBRIC** | evaluator-only score rule; frozen before any scored run |

Per-function requirements follow. Each instance card must carry all six sections,
in this order, with these names.

## 1. F1 — THE PACKET (state encoding)

- The packet is the worker's **entire** world. Everything needed to attempt the
  task is inside it; everything that would leak the key is structurally outside it.
- **Structural separation, not promissory:** the evaluator key lives in a separate
  desk artifact (or below the cut line `==== DESK ONLY — NEVER BELOW THIS LINE IN
  WORKER INPUTS ====` — the pilot pack's own convention). The separation must
  survive a hostile reading: if the worker can reconstruct >50% of the rubric from
  the packet alone, the instance FAILS desk review (separation falsifier, §8).
- Inputs are carried canonically: file paths, row counts, and derivation
  procedures are named exactly, each stamped with an as-of date. A spoken sentence
  that contradicts the named artifact loses (L0 canonical rule: the encoded state
  is the only authority).
- The packet names its **novelty provenance**: which corpus regions the task draws
  from, so the desk can check it against the frozen wave-one novelty map (Astra
  bundle item 4) without asking the author.
- **Contamination canary (v3, AISI borrow):** every instance card carries a
  `canary:` line — a unique random string (≥32 chars, generated at authoring),
  quoted VERBATIM in the packet above the cut line, unaltered after freeze;
  the desk checks its presence byte-exact at HOLD 3. Any future training
  corpus containing the string is detectable evidence of contamination — the
  UK AISI mechanism, adopted whole. Sham twins and desk sub-forms inherit
  the canary.

## 2. F2 — THE OBJECTIVE (initial state)

- One posed claim or task, stated as a falsifiable sentence in the fleet's native
  tri-state vocabulary (Supported / Disputed / Unproven).
- **Seeded-deterministic, never improvised:** every input quantity is derived by a
  recorded procedure from repo state (chain file, audit card, manifest), like the
  L0 RNG law — `value = TABLE[game-id][mode][seed][draw-index]`, nothing guessed.
  A frozen instance does not hand-copy mutable numbers; it freezes the PROCEDURE
  and stamps the as-of measurement. If the repo moves, the procedure re-derives;
  the instance does not rot.
- The objective names what the worker must produce to settle or tri-state the
  claim — and explicitly does NOT promise the claim is true.

## 3. F3 — LEGALITY & ANTI-GOALS

- Enumerate the illegal moves. The fleet's standard set (instances may add, never
  subtract):
  - **Never invent objects** — a resolution, citation, or result not read from
    data is UNPROVEN, never Supported (corrections law 6, L0 "never invent
    objects").
  - **No silent flag upgrades** — `reconstructed`/`speculative`/`attested`
    (and Unproven/Disputed) statuses never upgrade without new evidence on record.
  - **No narrative override** — the canonical artifact governs; prose is
    decoration after the artifact, never a replacement.
  - **No rubric access, no other-instance drafts** (independence law, HOLD 1+).
  - **No repair scope creep** — if the task audits, it does not fix; if it drafts,
    it does not deploy. The instance's verb is its boundary.
  - **No network, no launches, no credential contact** unless the packet's budget
    section explicitly grants them.
- `LEGAL?` is authoritative: an answer that used an illegal move FAILS regardless
  of content quality (L0: `move` MUST reject any action not returned legal).

## 4. F4 — THE BUDGET (transition)

- Token allowance, metering method, retry policy, and deadline — per instance, so
  they aggregate into the registration bundle's budget manifest (Astra bundle
  item 6).
- Retry law inherits the pilot pack: transport/service failures get at most two
  retries of the unchanged request, all attempts logged; a completed malformed
  answer scores as-is, never silently repaired.
- Generation caps are set generous and FROZEN before the run, so hidden reasoning
  is not starved (pilot-pack freeze discipline).
- The lane is named (HOLD 0: free reasoning lane; premium tokens touch judgment
  only).
- **Meter granularity binds to the fleet meter** (Tesla's law,
  SALON_BUILD_DIRECTION_20260909.md): input, output, reasoning, prefix reads,
  cached reads reported SEPARATELY — instance budget fields must aggregate
  into the frozen manifest format without re-shaping. The meter is the
  instrument that makes the 1,920-episode floor runnable; the instance is
  where its rows are born.

## 5. F5 — THE EVIDENCE SHAPE (terminal detection)

- The terminal answer form is fully specified: mandatory sections, field names,
  label vocabulary. `TERMINAL?(answer)` must be checkable by shape alone before
  any scoring.
- The fleet's answer spine: **canonical restatement first** (reprint the inputs
  and procedure actually used), then the result, then the verdict; every verdict
  carries its evidence and its tri-state status.
- Every instance ends with a **CAMP STATE blob** (the chunked-campaign carry
  format): `decided / open / next` — one line each. The blob is what makes any
  instance resumable by a stranger (durable-execution semantics: interruption
  is PAUSE, not loss).
- **Failure evidence is shaped evidence** (Gopher's law,
  SALON_BUILD_DIRECTION_20260909.md): a stalled, refused, or overrun attempt
  still SHIPS. The answer card carries a FAILURE RECEIPT block — failure
  class from the fixed vocabulary (`STALL · REFUSAL · OVERRUN · TOOL_FAIL ·
  MALFORMED · TRANSPORT`), what was attempted, the last usable state, and
  whatever usable work exists. Nothing vanishes into a retry; the ugly book
  is wired, not hidden.

## 6. F6 — THE HIDDEN RUBRIC (scoring)

- Evaluator-only, below the cut line, frozen before any scored episode (Astra
  bundle item 3: executable checks preferred).
- Rubric seeds must satisfy the ripeness fields (ladder HOLD 2): **measurable**
  (executable diff/exists/count where possible; human-judgment items named as
  such), **inherited calibration** (the desk's own measured baseline is the
  calibration run), **generalizes** (the scoring rule transfers to sibling
  instances of the same slot, not just this one).
- Score only what the desk can verify deterministically. If a proposed score
  dimension's derivation is unpinned (e.g., an unknown hash scheme), it is
  tri-stated OUT of the rubric until pinned — never scored by vibes.
- No rescue clause (Astra's program-ender law, carried to task scale): a bad
  answer cannot be rescued by charm, length, or a favorable reading. Balance is
  documented like the pilot pack: what the key rewards, what it punishes, what
  it is blind to.
- **Failures score — they stay in the denominator** (Gopher's law): the rubric
  PRESCRIBES the credit for each failure class (an honest refusal keeps the
  points its honest restatement earned; an overrun is capped at work actually
  produced; a stall is a scored outcome, never a silently dropped row). The
  desk cannot heal a denominator by deleting its ugly rows.

## 6a. THE QA RECEIPT (per task family — AISI harness borrow, v3)

- Every instance card carries a `qa_receipt:` promise line (alongside the
  CAMP STATE blob): one completed END-TO-END sample per TASK FAMILY (each of
  I1-I6 and each sham twin S1-S6), agent-run or desk-run (the D-arm desk
  sub-form qualifies for its family), with its LOG stored in the bundle
  directory before the HOLD 3 gate — and the log manually checked for API
  errors and tool failures before the receipt signs. This is the UK AISI
  quality-assurance requirement, satisfied by artifacts HOLD 0 and HOLD 3
  were already going to produce; naming it now makes it a REQUIRED
  deliverable, not a souvenir. A family without its qa_receipt does not
  proceed to scored episodes.

## 7. THE AMENDMENT RULE (adoption ≠ override)

- Frozen fields are never rewritten in place. A blocked author or a desk
  rejection appends an **amendment row**: `{field, what blocks, minimal change,
  why, receipt}`. The desk adopts or rejects; adoption appends the row to the
  contract's amendment ledger and re-stamps the version; override is void.
- The template embeds this rule in every launch prompt (see
  PROMPT_TEMPLATE_DRAFT_20260911.md): an author who works around the contract
  silently has produced a non-conforming instance, desk-rejected on sight.
- Disagreements that survive adoption are preserved as explicit DISPUTED lines in
  both cards (costimulation law: convergence on broken means the template is the
  bug — surface the dispute, don't sand it).

### 7.1 THE FREEZE STAMP (Fen's law — author to freeze, not iterate)

- Every artifact this contract governs (contract, template, instance) ships
  with a **FREEZE STAMP the day it is born**, as its final line:

  `FREEZE STAMP: <ISO-8601 UTC> · sha256:<hex of every byte above this line> · author:<seat> · contract:v<N> · template:v<N>`

- Verification is mechanical and pinned: the hashed body is **every byte
  preceding the newline that precedes the stamp line** (the stamp line is
  appended after exactly one separator `\n`; verification truncates both). A
  stamp that does not verify voids the artifact's frozen status.
- Sequencing reconciles this with the amendment rule: iterate BEFORE the seal
  (the bundle seals at HOLD 4) — pre-seal changes append an amendment row and
  re-stamp as a new version, the old stamp surviving as lineage. AFTER the
  seal, registered artifacts are immutable: a change is a NEW artifact with
  its own stamp and a tombstone line on the old one. No live iteration on
  registered artifacts, ever.
- PENDING RECONCILIATION: FEN_FREEZE_KIT (ractor organ) had not landed at
  v2 stamping time. If the kit's canonical format differs, the kit wins and
  this §7.1 takes a receipted amendment — or a DISPUTED line if the formats
  genuinely conflict.

## 8. DESK-REVIEW CHECKLIST (the HOLD 0 dogfood)

The desk answers exactly these, in order:

1. **Separation:** can the rubric key be reconstructed from the packet alone?
   (>50% reconstructable = FAIL.)
2. **Seed:** is every input quantity re-derivable from the recorded procedure?
   (Any hand-copied mutable number in a frozen field = FAIL.)
3. **Legality:** are the illegal moves enumerated and enforcing (would `LEGAL?`
   catch the classic cheats: invention, upgrade, narrative override)?
4. **Budget:** are allowance/metering/retry/deadline named and aggregatable?
5. **Terminal:** is `TERMINAL?(answer)` checkable by shape alone?
6. **Rubric:** executable-first, frozen, ripeness-clean, no rescue clause?
7. **Honesty:** are open questions tri-stated in the card (not hidden)?
8. **Freeze stamp:** present as the final line, day-of-birth, mechanically
   verifiable per §7.1. Missing or non-verifying stamp = FAIL.

Three consecutive desk FAILs on seeds = F-H0 fires: audit this contract, not the
agents.

## 9. OPEN (tri-stated, carried in every conformant card's CAMP STATE)

- **UNPROVEN:** whether the six canonical functions fully cover non-room-shaped
  tasks (design drafts, prose synthesis). Seed instance 001 is linkage-audit
  shaped; HOLD 2's six slots will stress other shapes. If a shape resists the
  six-function binding, that is a Chunk 1 amendment request to Astra (F-H2 path).
- **UNPROVEN:** inter-rater agreement of this checklist itself — first measured
  at HOLD 1's divergence analysis.
- **DISPUTED:** none yet recorded against this draft.
- **AMENDMENT LEDGER** (adoption ≠ override; rows append, never rewrite):
  - **v1 → v2 (2026-09-11, adopting watch/SALON_BUILD_DIRECTION_20260909.md
    via operator relay):** §7.1 freeze stamp + §8 item 8 (Fen) · F4 meter
    granularity (Tesla) · F5 failure receipts + F6 failure-denominator
    (Gopher). DISPUTED lines: none — the apparent conflict between Fen's
    "never iterate" and §7's amendment rule is reconciled by SEQUENCING
    (pre-seal = amend + re-stamp; post-seal = immutable, new artifact).
    Pending: FEN_FREEZE_KIT and GOPHER_FAILURE_PLUMBING_SPEC reconciliation
    on arrival (§7.1 note).
  - **v2 → v3 (2026-09-11, night eval-upgrade wave — external-standards scan,
    watch/inbox/NIGHT_EXTERNAL_EVAL_20260911.md):** §1 canary field (AISI
    contamination mechanism) · new §6a qa_receipt promise per task family
    (AISI QA requirement) · STAMP FORMAT RECONCILED: the FEN kit's
    header-block stamp WINS per §7.1's pending-reconciliation note — v3 is
    stamped in kit format at the top of this file; the v2 trailing stamp
    below survives VERBATIM as lineage (kit §0: prior stamps are history).
    prior-sha256 = `2f9acde3a4734c831eb20217472b6446e99afa7de77e8a504cf3a5471074a5a1`
    (v2 stamp, §7.1 body-hash convention, verified 2026-09-09T19:23Z);
    new-sha256 = header-stamp value (kit convention; full-file post-paste
    hash witnessed by the desk in GROUNDING_WAVE at seal). Caveat: the scan
    rode a rate-limited search lane — GAIA / SWE-bench submission pages
    unfetched; that cross-check stays UNPROVEN (scan card §4); no verdict
    here depends on it.

---
*Frozen-draft-2. Desk review is the gate to HOLD 1. Adoption appends; override is void.*

*v3 note (2026-09-11): this draft is now FROZEN-DRAFT-3 — current stamp is the kit-format header block at the top; the draft-2 footer above and the v2 trailing stamp below survive as lineage, preserved verbatim (kit §0).*

FREEZE STAMP: 2026-09-09T17:19:37Z · sha256:2f9acde3a4734c831eb20217472b6446e99afa7de77e8a504cf3a5471074a5a1 · author:zcode-seat · contract:v2 · template:v2
