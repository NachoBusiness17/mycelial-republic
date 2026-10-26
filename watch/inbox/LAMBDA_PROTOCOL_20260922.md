# LAMBDA PROTOCOL — pre-registration (2026-09-22)

Filed 2026-09-22 by lane A9 (mickey-A9), ask A9, Mag Estate.
Status: **REGISTERED, NOT RUN.** Protocol only — no run is executed by this filing;
runs happen later under separate asks. Rules, metrics, and thresholds below are
frozen as of filing. Any change after data collection begins must be filed as a
dated amendment row at the bottom of this file, never silently. This file is
append-only.

## Question

Does the salon_50 shared journal make a swarm of k lanes better than k independent
lanes at EQUAL token budget — or is everything the swarm wins explained by the
budget alone?

- H1 (the shared-journal half): at equal total token budget, k lanes writing to and
  reading from the shared salon_50 journal (the append-only handoff tape) produce
  higher quorum-adjudicated task success than k lanes running in isolation.
- H0: the journal adds nothing; independent@k matches or beats swarm@k at equal budget.

## Arms

- **swarm@k** — k lanes in the salon_50 shared-journal shape: one append-only raw
  tape; every lane's answer ends `NEXT-STEAL: <instruction for the next pass>`;
  later lanes read the tape before answering (`mag/salon_50.py:14-32,184`).
- **independent@k** — N = k lanes, same model, same prompts, same tasks, no tape,
  no reads of any other lane's output, no handoffs, no message passing.
  Coordination impossible by construction (the COLD discipline of
  `FOUR_CONDITION_PREREGISTRATION_20260918.md:18-19`).

Budget parity (hard constraints):

1. Identical TOTAL token cap B_total per task, summed across all k lanes and all
   passes, input plus output. Equal, not merely similar.
2. The swarm's journal reads and writes count inside its own B_total. The
   independent arm is not compensated for lacking a journal and gets no extra
   budget in its place.
3. Same model, same decoding settings, same prompts, same held-out task set, same
   scoring procedure. The ONLY permitted difference between the arms is the shared
   journal.

## No cross-visible debate

Prohibited in both arms, by design, before any data exists. No lane sees another
lane's answers or reasoning except through the swarm arm's own journal tape; there
is no cross-arm visibility and no explicit debate protocol anywhere in this
experiment.

Precedent: Smit et al., "Should we be going MAD? A Look at Multi-Agent Debate
Strategies for LLMs", arXiv:2311.17371 — multi-agent debate failed a
matched-compute test of exactly this kind (verified 2026-09-22 against
arxiv.org/abs/2311.17371: MAD does not reliably outperform non-debate baselines
such as self-consistency). Any switch to a debate configuration after launch voids
the run and is filed as a violation row, not an amendment.

## 7-pass quorum reads

Every scored artifact — each lane's final answer per task, in BOTH arms
identically — is read 7 times by 7 independent scoring passes, no memory between
passes:

- An answer counts correct iff **≥5 of 7** passes score it correct (strict-majority
  quorum).
- **4/7 = CONTESTED**: recorded and reported separately, never rounded to correct.
- Passes are blind: a scorer sees only the answer and the rubric — never the arm
  label, never another pass's verdict.
- Where a task admits an exact mechanical check, the check IS the score (ordinary
  code, no LLM judge — the A3 compliance of
  `FOUR_CONDITION_PREREGISTRATION_20260918.md:72-74`), and the 7 passes become 7
  independent executions of that same check under the same quorum rule.
- Any journal-state read that decides a task's outcome (e.g. which committed answer
  counts as the swarm's final) is likewise a 7-pass quorum read.

## Primary metric and pre-committed acceptance bars (fixed now)

Primary metric: quorum-adjudicated success rate per arm on the shared held-out task
set — the fraction of tasks whose committed answer clears ≥5/7.

Let **d = success(swarm@k) − success(independent@k)** at equal B_total.

- **Bar W (support):** d ≥ +5 percentage points → the shared-journal half stands
  provisionally: the swarm wins at equal budget and the journal gets the credit.
- **Bar E (no effect):** 0 < d < +5 → inconclusive. The journal earns NO credit.
  Report verbatim; no post-hoc thresholding.
- **Bar F (FALSIFIER):** d ≤ 0 — i.e. **independent@k ≥ swarm@k at equal budget
  falsifies the shared-journal half.** No rescue hypotheses, no task subsetting, no
  re-weighting, no "the swarm would win with more lanes" without a new
  registration. File as falsified; next budget goes to independent lanes.

Secondary metrics (recorded, never gating): contested rate (4/7),
tokens-to-first-correct, per-lane variance, wall-clock. If a secondary metric flatters
the swarm while Bar F fires on the primary, the falsifier wins — it is primary.

## Run shape (for the later runs)

- Task set: held out, written and hashed BEFORE the first token of any run; the
  hash goes in the run manifest alongside this file's SHA-256.
- k: frozen in the run manifest before launch; both arms use the SAME k, and N = k
  independent lanes.
- Minimum run size: pre-registered per the house rule — if free-lane rate limits
  force fewer runs, below-minimum runs are reported as pilot, never as confirmation
  (`FOUR_CONDITION_PREREGISTRATION_20260918.md:39-42`).
- No peeking: fixed task set, fixed budget, fixed pass count; no interim analysis
  may stop or reshape a run.
- Deviations (crashes, retries, model drift) are logged in the run manifest under
  DEVIATIONS; retries spend the same B_total.
- This document is append-only after filing: corrections and outcomes land as dated
  amendment rows below; the frozen sections above are never edited.

## What this file is not

It is not evidence and contains no results. The experiment has not run. The
receipts below are filing receipts, not run receipts.

## Amendment rows

(none yet — append dated rows below this line; never edit anything above)

---

## Filing receipts (2026-09-22)

- arXiv verification: fetched `https://arxiv.org/abs/2311.17371` → "Should we be
  going MAD? A Look at Multi-Agent Debate Strategies for LLMs" — Andries Smit,
  Paul Duckworth, Nathan Grinsztajn, Thomas D. Barrett, Arnu Pretorius; abstract
  confirms MAD benchmarks with debate not reliably outperforming alternatives.
  (Self-reference note: this file's own SHA-256 is recorded in ask A9's filing
  result, not here — a file cannot contain its own hash.)
- salon_50 grounding: `mag/salon_50.py:14-32` (NEXT-STEAL handoff contract) and
  `mag/salon_50.py:184` (the fold extracts handoffs from the raw tape);
  `watch/inbox/NIGHT_AUDIT_20260916.md:48` (`memory/runs/salon_50_20260916/`, 53
  handoffs); `watch/inbox/SALON_PROMPT_MANUAL_20260920.md:37` (D23 salon50, 39/50
  at $0); `watch/inbox/physical_computing/receipts/SALON_ESS_20260916.md:13`
  (`mag/salon_50.py` writes `memory/runs/salon_50_20260916/raw.jsonl` +
  `receipt.json`).
- Preregistration style precedent:
  `watch/inbox/FOUR_CONDITION_PREREGISTRATION_20260918.md` (REGISTERED NOT RUN,
  fixed decision rules, confounds named in advance).
