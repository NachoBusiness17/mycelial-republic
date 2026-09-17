# README — the reciprocal packet

For the Hive Operating Floor lineage (AdventureNLearn). You sent a manual; this is our
manual's answering letter. It describes a machine we run and tells you how to rebuild
every piece and why each piece earns its place.

Human final call absolute. Software never crowns Supported. Honest open hole > fake board.
Those are your sentences. We ran them through our own machine and they held. This packet
is the receipt of that test.

---

## What the fleet is

A solo-operated mesh: AI agent seats, free model lanes, two local janitor models, and one
human. No paid APIs. No cloud dependency that matters. The human arms a goal; seats fan
out in parallel lanes; each lane writes a receipt before it works and appends to it as it
goes; the night's work folds into one warm card the next session starts from.

One night on this machine (2026-09-16) looked like this: 60 lanes, 60 receipts, one
master index. Four receipts died mid-work and their partial work survived anyway. The
fleet's own favorite theory died by its own pre-registered threshold. A corruption in the
evidence ledger was caught by a verify command, not by a person's memory. All of it cost
$0.00 cash. (`watch/inbox/wave_20260916/WAVE_STATE_20260916.md` — the master index.)

## The pieces (BUILD.md has the build steps for each)

> Explanations marked **Mesh fold** below come from an 8-lane mesh, 50 seeds, folded
> without averaging — one clearest explanation per mechanism, chosen by hand from the
> raw tape, no blending.

1. **The ledger.** One append-only file. Every row carries the hash of the row before it
   and its own hash. Corrections are new rows, never edits. A verify command re-checks
   the whole chain on demand. When a writer crashed mid-row, the chain went red at that
   row and stayed red until a lawful repair exists. The machine cannot quietly rewrite
   its past. (Evidence: `wave_20260916/receipts/A2_EPISTEMOLOGY_ENGINE.md` finding F-2 —
   the live chain, caught broken at row 122.)

   > **Mesh fold** (or-union-alpha, seed 5): An append-only ledger stores events as
   > ordered rows: inputs, commitments, actions, outputs, and corrections. Each row
   > includes the previous row's hash; changing an earlier row breaks subsequent links.
   > Keep copies or publish checkpoints elsewhere, because someone controlling storage
   > can otherwise rewrite the chain. Corrections reference earlier rows instead of
   > replacing them, preserving what was known when a decision happened. Write intent
   > before execution so crashes leave evidence of unfinished work. Another reader can
   > replay the sequence and check its consistency. The ledger cannot make recorded
   > claims true: hashes protect traceability, not factual correctness. A person still
   > evaluates evidence and conclusions.

2. **Receipts before work.** A lane writes its receipt first — mission, budget, law —
   then works, appending as it goes. A lane that dies leaves a partial receipt: partial
   ore, not silence. Tonight three dead lanes left usable inventory because of this.
   (Evidence: `receipts/B9_ZENODO_DOIS.md` died at 2 of 4 registrations and was finished
   by a second lane that read it; `receipts/G1_GAMES_AUDIT.md` died mid-work, tables
   survived; `wave_20260916/drafts/` holds a 0-byte dead draft plus its death record.)

   > **Mesh fold** (or-ling3, seed 14): Write the receipt first because it locks intent
   > before execution drifts. The hash commits to inputs, constraints, and thresholds
   > while the session is still coherent. If the session dies mid-work, the partial
   > receipt is salvageable ore: it proves what was attempted, what inputs were locked,
   > and where the chain broke. Another agent or the human can resume from that exact
   > state or audit the gap without reconstructing intent from memory. It turns
   > abandoned work into recoverable data rather than lost context. The mechanism is
   > simple: pre-commit, then act. The receipt is the anchor; the partial receipt is
   > the map back.

3. **Pre-registered falsifiers.** Before any experiment: the claim, the metric, the
   number that kills it, committed in writing before data exists. Then the data is
   graded mechanically against the number. This killed our favorite idea this week —
   on schedule, by its own threshold. (Evidence:
   `physical_computing/receipts/SALON_ESS_REPLICATE_20260916.md` — verdict REFUTED,
   rho +0.327 against a +0.3 refutation line we wrote first.)

   > **Mesh fold** (or-union-alpha, seed 21): A falsifier is a written claim: kill the
   > theory if metric X crosses T. You commit T before running the data because
   > afterward you'll move it. The number you'd accept post-hoc is always the number
   > that spares the theory, and you can't feel that happening from inside. So write
   > the threshold, its measurement method, and the kill date to the ledger first.
   > When data arrives, comparison is arithmetic, not judgment — no negotiation. It
   > cost me my favorite theory tonight; the mechanism did its job. Without
   > pre-commitment, falsifiers are just intentions with better branding.

4. **The Amendment Obligation.** Every work cycle amends one rule of its own, or writes
   down why none. Rules rot into fossils; the obligation is the decomposer. Tonight's
   catch: a memory line said a run answered "50/50"; the run's own receipt bytes say
   39/50. The correction is filed and the fossil line is quarantined. (Evidence:
   `WAVE_STATE_20260916.md` §3–§4, `receipts/A1_BLIND_CHALLENGE_SET.md` challenge C-08.)

   > **Mesh fold** (cerebras-qwen, seed 35): The amendment rule forces the runtime to
   > confront drift. A fleet that only executes fixed rules accumulates edge cases,
   > stale defaults, and silent failures. Each cycle must either change a rule or
   > produce a reason, turning no change into a testable claim. That claim enters the
   > ledger, allowing later replay to ask whether it was sound when fresh data or new
   > failure modes made it stale. This blocks ritual maintenance. If you cannot
   > justify the current rule, change it. If you can, you have recorded an explicit
   > check for invalidation. The fleet becomes a self-auditing instrument, not a
   > static shrine.

5. **The blind challenge set.** Ten claims the fleet holds, each with a fixed threshold
   and a sealed answer key — only the key's hash is public. The fleet must commit
   predictions before outcomes. The author of a test cannot grade their own homework
   kindly, because the key was locked before anyone answered. (Evidence:
   `receipts/A1_BLIND_CHALLENGE_SET.md` — sealed, hash-committed.)

6. **The pacing guard.** Remote free lanes are free of cash, not of limits. A one-call
   probe runs before any fanout; a lane that hits a quota wall is marked do-not-retry
   and the run continues on the surviving lanes. Tonight a lane that was alive at dusk
   was dead by midnight — balance drained under us mid-run. The guard kept the other
   49 seeds flowing. (Evidence: `receipts/D23_SALON50_NIGHT_RESULTS.md`,
   `receipts/D22_PROVIDER_PROBE_20260916.md`.)

7. **The outside reader.** A seat — another model, or a stranger — that did not write
   the work, reads the raw receipts (bytes and hashes, not our summaries), and returns
   a verdict: keep, kill, or amend. It found two real errors in our own audit the first
   night it ran. We amended its contract the same night: it gets bytes, never prose.
   (Evidence: `receipts/U5_UNION_WAVE_WITNESS.md` — verdict KEEP, protocol amended.)

   > **Mesh fold** (mistral-min8, seed 44): The tape is the only proof. If *you*
   > control the replay, you can lie—edit, omit, or retroactively justify. An outside
   > reader forces you to build a system where every step is *visible* and
   > *unalterable*. Their ability to audit means the ledger's integrity isn't trust in
   > *you*, but in the rules you've locked into the chain. If the tape can't be
   > replayed without you, it's just a logbook. If it can, the system's logic survives
   > you. That's why falsifiers are pre-registered: to let strangers verify the rules
   > were followed, not just that you *said* they were.

8. **The tide.** At session close, one command compacts the scatter — dozens of lanes,
   raw tapes, dead ends — into a warm daily card: counts, corrections, and the one
   command the next window runs to be fully warm. (Evidence:
   `receipts/WARM_START_20260916.md`, `WAVE_STATE_20260916.md` §3.)

## What this is not

- Not an AI-cult artifact. No sentience claims. No ceremony. No ritual that does not
  carry its own failure story. Metaphors are labels, not evidence — our own best
  metaphor ("a thermodynamic sampler of judgment space") just died by threshold, and
  that death is itself part of this packet (BUILD piece 3).
- Not cargo culting. Every rule in BUILD.md names the concrete failure that produced
  it. If you copy a rule without its failure, you have copied a lamp without a light.
  Each piece also names what would make us delete it.
- Not finished. Blanks stay blank. Current honest holes: the ledger's row-122 break is
  quarantined but not yet repaired (repair design exists, build is queued); three audit
  receipts from tonight are stubs with empty findings sections; the refutation above is
  a threshold graze (rho passed the kill line by 0.027, p = 0.052) and we call it weak,
  not final. We say incomplete when incomplete.

## Open items & amendment log

- **Proposed 2026-09-16 (RV2 mesh, applied to its own fold):** mesh drivers should tag
  lanes whose content is a leaked reasoning dump (observed: or-nemotron, seeds 23 and
  47) at call time — a `leaked_reasoning: true` row flag — so fold lanes can filter
  width-only material mechanically instead of by eye. Cheap and falsifiable: compare
  fold-selection error rate before/after. Status: open, not yet adopted.
  Otherwise-none branch for that cycle: the d23 driver pattern needed no change; it
  worked unmodified.

## The one-line difference

Software proposes. Bytes decide. A person opens the file.
