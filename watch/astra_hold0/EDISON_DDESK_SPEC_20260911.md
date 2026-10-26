# THE D-DESK — timed operator interface spec (Edison ractor organ, 2026-09-11)

==== FREEZE STAMP ====
artifact:     watch/astra_hold0/EDISON_DDESK_SPEC_20260911.md
sha256:       54b4033e290297d872fbc7b970cc8df727a3ebb0cdca9408b4a1c2097cea2087
frozen-at:    2026-09-10T00:06:43Z
author:       EDISON ractor (builder wave 09-11, zcode seat); stamp + row A1 by zcode seat (night watch lane)
amendments:   row A1 (AMENDMENT LEDGER, retrofitted; Astra v2 review adoption)
kit:          FEN_FREEZE_KIT_20260911.md
=======================

> **[AUDIT-TYPED]** status: SPEC — DESIGN, nothing built, nothing frozen ·
> provenance: watch/SALON_BUILD_DIRECTION_20260909.md (EDISON mandate: "the desk
> must be a timed interface... 240 seconds of cumulative work per episode...
> no off-clock prep... the fire window is a design parameter, not a habit") ·
> watch/ASTRA_FOLD3_20260909.md:29-36 (locked design: **D DESK** — no
> agent-to-agent; human folds and injects, 4-minute cap, the measured fire
> window) · companion builders' drafts read, not modified:
> astra_hold0/L0_CONTRACT_DRAFT_20260911.md · TASK_PACK_SKELETON_20260911.md ·
> BUDGET_MANIFEST_SKELETON_20260911.md (the D-arm arithmetic DISPUTED-TENSION
> §1 + F-B2 — this spec is the measuring instrument for that dispute) ·
> author: EDISON ractor, builder wave 09-11, operator GO.
> Scope: INTERFACE CONTRACT only — the harness implementation is a build; this
> file is what the build must satisfy. Read-only discipline honored: no
> builder file was touched.

## 0. WHAT THE D-ARM IS (pinned, SUPPORTED — FOLD3)

Four locked conditions; D is "the current product":

- A COLD · B WARM-TYPED · C WARM-FREE (token-budget matched to B) ·
  **D DESK: no agent-to-agent; the human folds and injects, 240 seconds of
  cumulative work per episode (reading, deciding, folding, injecting), no
  off-clock prep; waiting time recorded separately.**
- FOLD3's decision rule names the stakes: **D ≥ B, C = "you built a human
  editor. The fleet is scenery."** The desk arm must therefore be run HONESTLY
  — which means the time cap must be enforced, not aspirational. A desk that
  leaks prep or overruns silently measures a fifth condition nobody
  pre-registered.

## 1. THE D-DESK INTERFACE — what the operator sees inside the 240 seconds

The four mandate verbs are the interface. One screen (phone-readable —
operator cadence law), four panels, opened and closed by the harness. The
operator NEVER opens a repo, edits a file, or runs a script during an episode.

### Panel 1 — THE PACKET (READ)

- The worker's complete input world (L0 F1), pre-rendered by the harness:
  packet text above the cut line, desk-only material (hidden-rubric key
  excerpt) in a separate collapsible region below the mechanic cut line
  (`==== DESK ONLY — NEVER BELOW THIS LINE IN WORKER INPUTS ====`). The
  harness enforces the cut line mechanically: panel-1 content is what injects;
  the collapsible region is display-only and CANNOT pass through inject.
- Rendered state: objective (F2), legality list (F3), evidence shape (F5)
  pre-parsed and labeled — the operator reads a card, not a folder.

### Panel 2 — THE DECISION (DECIDE)

- The decision is a selection, never a composition. The packet's checklist
  posture (L0 §8, items 1-7) is pre-evaluated by the harness where
  deterministic (shape checks, seed re-derivation, cut-line integrity) and
  shown as PASS/FAIL/HUMAN chips. Only the HUMAN chips require operator
  judgment; the panel shows how many remain and the running seconds.
- Decision vocabulary is closed: CONTINUE to fold · QUEUE-EDGE (Mengxi rule:
  unavailable authorization = edge closed, request queued) · ABORT-EPISODE
  (records why, failure-classed per Gopher vocabulary).

### Panel 3 — THE FOLD (FOLD)

- One selection from a pre-priced menu. Each option auto-writes its receipt
  row; free text is optional and capped at 140 chars (counted in the ledger).
  Options are BOUND to existing organs, not invented:
  - `PASS-AS-IS` — episode proceeds; receipt = packet hash + fold timestamp.
  - `AMEND:<field>` — the L0 §7 amendment row, pre-formatted (field / what
    blocks / minimal change / why / receipt); adoption appends, override void.
  - `REJECT:<checklist-1..7>` — maps to the L0 §8 desk-review checklist item
    that fired; 3 consecutive rejects fire F-H0 (the contract is the bug).
  - `QUEUE-EDGE` — routed to the queue organ (Mengxi build), never dropped.
  - `DEFAULT-FOLD` — the pre-registered default (REJECT on incomplete
    review), applied at timeout; see §3 rollover.
- Fold pricing is stamped per option (harness-measured median, frozen before
  the run) so the manifest can pre-compute expected desk load per block.

### Panel 4 — THE INJECT (INJECT)

- The fold's receipt is injected into the episode by the harness. The operator
  CONFIRMS; he never touches worker input files. Confirm = one tap, ≤5
  seconds, counted. Inject closes the episode's work window and seals the
  ledger row (§2).

### THE PRE-STAGE MANIFEST — zero off-clock prep, by construction

An episode MAY NOT OPEN unless all five pre-staged artifacts exist:

1. Packet rendered (panel 1 complete, cut line mechanically verified).
2. Fold card priced (panel 3 options enumerated with stamped prices).
3. Ledger row pre-drafted (episode_id, timestamps blank, everything else
   filled — the operator's taps fill blanks, never author structure).
4. Timer armed with this episode's D-budget (240s minus any carried
   rollover debt — rollover-DEFER zeroes carry; see §3).
5. Prior episode's chain row sealed.

Missing any of the five at open time = `HARNESS_FAIL` row (falsifier F-E3) —
a harness defect, NEVER operator prep. Off-clock prep is defined precisely:
**any operator second spent on desk work while no episode window is open.**
The design goal, and the falsifiable claim, is zero.

## 2. THE TIME LEDGER — cumulative-seconds accounting, work vs waiting

Sibling to the budget manifest's metering schema (§5 there), joined on
`episode_id`. The meter (Tesla organ) counts tokens for the model; this ledger
counts SECONDS for the human. Same rigor, separate axis. Desk-side and
token-free (zero-cost scoring rule honored).

```json
{"episode_id":"B07-T3-D-P1-s2","block":7,"task_id":"I3","condition":"D",
 "work_seconds":{"read":0,"decide":0,"fold":0,"inject":0},
 "work_seconds_total":0,
 "waiting_seconds":{"harness_render":0,"worker_run":0,"score_exec":0,"idle_gap":0},
 "waiting_seconds_total":0,
 "windows":[{"open":"ISO","close":"ISO","verbs_touched":["read","fold"]}],
 "budget_remaining":0,"rollover":null,
 "overrun_seconds":0,"offclock_seconds":0,
 "fold":"PASS-AS-IS","fold_text_chars":0,
 "valid_for_D_claim":true}
```

### Accounting rules

- **Work** = operator action seconds inside an open window, segmented by verb
  (read/decide/fold/inject) so the ledger shows WHERE the 240 goes, not just
  that it went. Harness timestamps phase transitions (open/close, per-tap);
  idle time inside an open window with no tap is `idle_gap` — counted as
  WAITING, not work (an operator thinking is work only if the harness cannot
  distinguish it, so the rule is tap-to-tap; stated honestly, this UNDER-
  counts work and is conservative for the 240 cap).
- **Waiting** = recorded separately, NEVER against the 240 (mandate text):
  harness render time, worker-run wall clock, score execution, idle gaps.
  The prefetch pipeline (§4) overlaps most waiting with work; the ledger
  proves the overlap rather than assuming it.
- **Cumulative:** the 240 is per-EPISODE, not per-window. An episode may be
  closed and re-opened (PAUSE, not loss — durable-execution semantics, the
  CAMP STATE blob law of L0 F5). Each window's seconds accrue to the same
  counter; the timer displays REMAINING, never elapsed.
- **No laundering:** `work_seconds` must be exactly the sum of intervals the
  harness observed as taps inside windows. Any manual edit path to the ledger
  row does not exist (the file is harness-written; operators file disputes as
  amendment rows, not edits — L0 §7 discipline).

### The 240s enforcement rule

At `work_seconds_total >= 240` the desk goes READ-ONLY for that episode: the
fold menu locks to three pre-priced rollover dispositions (each ≤5s, itself
counted):

- `ROLLOVER-DEFER` — episode carries to the next sitting with budget reset;
  the pause-and-carry posture of the manifest §4. Default-safe.
- `ROLLOVER-CARRY` — overrun recorded as `overrun_seconds = actual − 240`,
  requires an operator GO (spend-gos are operator-only by design); legal but
  the row carries `valid_for_D_claim=false` unless Astra's ruling says
  max-not-mean. This is the DISPUTED-TENSION (manifest §1) made empirical.
- `ROLLOVER-DEFAULT` — the desk applies `DEFAULT-FOLD` (REJECT on incomplete
  review) with the work as-is shipped as a FAILURE-CLASS OVERRUN row (Gopher:
  nothing vanishes into a retry; the ugly book is wired).

Rollover is never free, never silent, never skipped. Overruns are scored
outcomes that stay in the denominator (L0 F5 already carries OVERRUN in its
failure vocabulary — reused verbatim).

## 3. THE FIRE WINDOW — when episodes fire so D is runnable at human cadence

The fire window is a design parameter, set in the manifest BEFORE the run and
frozen with it — not a habit that emerges from however the operator happens to
sit down.

- **Cadence:** 2 blocks/day (manifest §4 pacing: 20 blocks in ~10 days). A
  **sitting** = one block segment of **5-8 desk episodes** (the fleet's
  standing bulk-lane shape, groups of five-to-eight — measured, not guessed).
  Sittings are scheduled; the operator confirms presence, he does not
  improvise a window.
- **Sequencing inside a sitting:** one desk, one clock — never two episodes
  open at once. While the operator folds episode N, the harness PREFETCHES
  N+1 (worker run, render, pre-stage). Waiting is overlapped with work by
  design and recorded separately so the overlap is EVIDENCE, not assumption.
  This is the mechanism that makes the D-arm arithmetic survivable: wall clock
  per episode ≈ `work_seconds`, not work + waiting.
- **Fire rules:**
  1. An episode fires only when its five pre-stage artifacts exist; else
     HARNESS_FAIL and the slot advances (the sitting is never blocked on a
     broken organ mid-run).
  2. Unopened episodes decay to CAMP STATE carry at sitting close — resumable,
     never silently dropped (durable-execution semantics).
  3. The 240 cap is treated as MAX pending Astra's ruling (manifest §1
     resolutions: sub-sample D per block, max-not-mean, or raise the cap).
     This ledger is the instrument that resolves it: **after the first 20
     desk episodes, the harness posts observed mean / p50 / p95 work-seconds
     per task-slot.** If the mean lands well under 240, the arithmetic
     resolves as max-not-mean WITH DATA — an amendment row carrying evidence,
     not argument (F-B2 disarmed by measurement).
  4. Human-judgment hygiene: a sitting ends by operator choice or at the
     block's episode count, whichever first; fatigue is a real confound, so
     the ledger timestamps sittings and the run report can check D-arm scores
     against sitting position (first-5 vs last-3) as a free robustness check.

## 4. THE FALSIFIERS — detecting D-arm violations

**F-E1 — off-clock prep.** The harness timestamps all desk artifacts and
all operator taps. Any desk-relevant operator action outside an open window
(packet re-renders requested, fold-card edits, artifact touches) accrues
`offclock_seconds` on the nearest episode row. Any episode with
`offclock_seconds > 0` is marked `valid_for_D_claim=false` — recorded, not
hidden. >20% of a block's episodes invalidated = the desk DESIGN is the bug,
not the operator: halt, rebuild the pre-stage organ, re-run the block (the
F-H0 pattern — audit the organ before blaming the hands).

**F-E2 — over-run.** `work_seconds_total > 240` with no rollover disposition
recorded = hard violation: the episode row is invalid and the run report
flags the harness (a timer that permits silent overrun is a broken meter).
With `ROLLOVER-CARRY` GO = legal but flagged `overrun_seconds > 0` and
`valid_for_D_claim=false` unless the max-not-mean ruling is sealed. Carry-GOs
are visible gated line items, receipted like any spend.

**F-E3 — harness failure posing as desk work.** An episode that opens with
any of the five pre-stage artifacts missing is a `HARNESS_FAIL` row — never
counted as desk work, never silently repaired. ≥3 consecutive HARNESS_FAILs
on one slot = the pre-staging organ is the bug (mirrors F-H0's "the contract
is the bug" law); the sitting for that slot halts for repair.

**F-E4 — waiting laundering.** Mandate: waiting recorded separately —
enforced mechanically. `work_seconds` must equal the sum of observed tap
intervals inside windows; phase timestamps must show every work segment
contiguous within a window. Any mismatch (waiting seconds found inside
`work_seconds`, or work intervals outside `windows[]`) invalidates the row.
The desk never improves its time by reclassifying idle as work.

**Cross-falsifier linkage:** this ledger is the measuring instrument for the
budget manifest's F-B2 (D-arm arithmetic unresolved at freeze = stop, not
shortcut) and for FOLD3's pre-registered decision rule on D. A D-arm result
reported without a valid-ledger denominator (per F-E1/E2/E4) is not a result.

## 5. OPEN (tri-stated)

- **SUPPORTED:** the 240s cumulative cap, no agent-to-agent, waiting recorded
  separately — FOLD3 locked design, manifest §1.
- **DISPUTED:** the 480-episode D-arm arithmetic (manifest §1
  DISPUTED-TENSION) — carried, not sanded; §3 rule 3 is this spec's measured
  path to resolution.
- **UNPROVEN:** whether tap-to-tap work accounting under-counts genuine
  thinking time enough to distort the 240 measure (stated conservative; first
  20-episode calibration reports will show it against the fold-price stamps).
- **UNPROVEN:** inter-rater agreement of the desk interface itself — the
  ladder's HOLD 0 dogfood (desk reviews seed instance 001 against the L0
  checklist) is the first live fire of this interface; treat that dogfood as
  this spec's calibration run and file interface defects as amendment rows
  against THIS file (adoption appends; override void).

## 6. AMENDMENT — THE D-ARM RULING (row A1; Astra v2 review, ADOPTED 2026-09-11)

Her ruling, adopted: **DEFAULT-FOLD selected; D = 180 cumulative seconds; the
1,920-episode envelope is preserved.** Arithmetic: 480 desk episodes × 180s =
86,400s = **24.0 desk hours**, leaving ≈8 of the ≤32 operator hours for
carriage, adjudication, and sealing. The DISPUTED-TENSION (budget manifest §1)
is RESOLVED BY RULING; F-B2 stays disarmed ONLY IF the reserve pilot (below)
clears before the seal.

- **The cap is 180, not 240.** Wherever §1/§2 above read "240 seconds," read
  180 per this row; the original text stays verbatim as history (adoption
  appends, override void). The 180 is CUMULATIVE WORK per episode: reading,
  deciding, folding, injecting — waiting stays recorded separately.
- **Reading and thinking are CHARGED.** §2's tap-to-tap rule (idle inside an
  open window counted as waiting) is SUPERSEDED: within an open window, ALL
  operator time is WORK, including unbroken reading and thinking. At the 240
  cap that under-count was conservative; at 180 it would be generous — so the
  harness charges window time, not taps. F-E4's no-laundering rule is
  unchanged; the windows are the meter.
- **No rollover resets.** `ROLLOVER-DEFER`'s "budget reset" (§2) is VOID: a
  deferred episode resumes with its REMAINING seconds, never a fresh budget.
  `ROLLOVER-CARRY` is unchanged (GO-gated, `valid_for_D_claim=false` unless a
  sealed ruling says otherwise). `ROLLOVER-DEFAULT` is unchanged.
- **Timeout = DEFAULT-FOLD: frozen, scored, no authorization.** At 180s expiry
  the desk applies DEFAULT-FOLD (REJECT on incomplete review), the partial work
  FREEZES for scoring at Gopher's prescribed credit, and the timeout GRANTS NO
  AUTHORIZATION — the desk may not extend, re-open, or continue an expired
  episode for any reason.
- **Evaluator keys leave the participant interface.** Panel 1's collapsible
  desk-only region (the hidden-rubric key excerpt) is REMOVED from the
  participant-facing render. Keys render desk-side only, on the scoring
  surface, in a channel the worker-facing pipeline never touches. The
  participant sees the packet above the cut line — nothing below it, nothing of
  the key.
- **Pilot the reserve before sealing.** §3 rule 3's first-20-desk-episode
  measurement becomes the MANDATORY reserve pilot: observed mean / p50 / p95
  work-seconds at the 180s cap post as an amendment row BEFORE the seal. If the
  pilot shows the reserve does not survive real cadence (mean work pressing the
  cap, sittings degrading), the arithmetic REOPENS — by measurement, not
  argument. No off-clock preparation exists in the pilot either; §1's
  pre-stage manifest governs every pilot episode.

## AMENDMENT LEDGER (retrofitted per FEN kit §2b; rows append, never rewrite)

| seq | date(UTC) | field | what blocked | minimal change | why | adopted-by | prior-sha256 | new-sha256 |
|---|---|---|---|---|---|---|---|---|
| A1 | 2026-09-11 | D cap (§1/§2/§3), Panel 1 key render | 240s consumed the full ≤32h operator budget; evaluator key excerpt rendered in the participant-facing panel | §6 appended: 180s cap, window-time charging (thinking included), no rollover resets, DEFAULT-FOLD at timeout with no authorization, keys desk-side only, mandatory reserve pilot before seal | Astra v2 review ruling ("DEFAULT-FOLD... D = 180 cumulative seconds... remove evaluator keys from the participant interface") | zcode seat (night watch lane) | f68213658a647e15c8c5d7007713cfadd57f488ed556ca998473e31397c4a90c | = this restamp's header-stamp value |

*Caveat (kit §1 honesty): the header stamp is a display value per the kit's
paste ritual; the verification target for this file's raw bytes is the detached
manifest `watch/astra_hold0/BUNDLE_RAWBYTES_SHA256_20260911.txt` (kit §2d),
reproducible with `sha256sum -c`.*
