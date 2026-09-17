# RV2B — PACKET FOLD (receipt-first, appended as work proceeds)

- **Wave lane:** wave_20260916 / RV2B (fold lane for RV2)
- **Date:** 2026-09-16
- **Mission:** Fold the five README-ready explanations from `RV2_MESH_EXPLAIN_FLEET.md` (FIVE CLEAREST section, verbatim) into the reciprocal packet `watch/inbox/outbound/adventurelearn_packet/README.md` — splice each segment's clearest explanation into the README's matching section, keep RV1's structure, add the credit line "8-lane mesh, 50 seeds, folded without averaging", and append RV2's one amendment proposal (mechanical `leaked_reasoning` flag) to the packet's changelog/open-items section. No JS touched → no `node --check` expected; verify the five sections read cleanly at close.
- **Laws:** receipt before work · Write/Edit only · no git · no paid APIs · $0.
- **Segment → README section map:**
  - S1 append-only ledger → piece 1 ("The ledger.")
  - S2 receipt-first work → piece 2 ("Receipts before work.")
  - S3 pre-registered falsifiers → piece 3 ("Pre-registered falsifiers.")
  - S4 amendment obligation → piece 4 ("The Amendment Obligation.")
  - S5 outside reader → piece 7 ("The outside reader.")
  - (Pieces 5, 6, 8 — blind challenge set, pacing guard, the tide — had no RV2 segment; untouched.)

## Work log (appended as it happens)

- [t0] Receipt written BEFORE any README edit. Wave-lane law held.
- [t1] Read `receipts/RV2_MESH_EXPLAIN_FLEET.md` — FIVE CLEAREST section located, five verbatim explanations + amendment proposal extracted. Read `outbound/adventurelearn_packet/README.md` (RV1 structure: 8 numbered pieces, "What this is not", "The one-line difference"). Map above fixed.
- [t2] Spliced all five verbatim explanations into `outbound/adventurelearn_packet/README.md` as indented blockquotes ("**Mesh fold** (lane, seed): …") inside their matching numbered pieces — RV1's 8-piece structure, wording, and evidence lines untouched; pieces 5/6/8 (no RV2 segment) untouched. Credit line added under "## The pieces": "Explanations marked **Mesh fold** below come from an 8-lane mesh, 50 seeds, folded without averaging…". One splice retry (piece 2: my first old_string had wrong leading whitespace; second attempt clean). Added "## Open items & amendment log" section (packet had no CHANGELOG; this is its first) carrying RV2's amendment proposal verbatim in substance: mechanical `leaked_reasoning: true` row flag for leaked reasoning dumps (observed or-nemotron s=23/s=47), falsifiable via fold-selection error rate before/after, status open — plus the otherwise-none branch (d23 driver pattern needed no change).
- [t3] Sanity: no JS touched (two .md files only) → `node --check` not applicable, none run. Structural grep verify: credit line at line 28; Mesh fold splices at lines 39, 57, 74, 89, 118 = pieces 1/2/3/4/7 in order, one per section, no duplicates; amendment section at line 147; all 47 blockquote lines well-formed. Read-through of the five sections: each blockquote continues its list item cleanly, bold/italics/em-dashes preserved verbatim, sections read as one voice per piece (RV1 claim + mesh explanation + evidence line intact).
- [t4] CLOSE. $0, no paid API, no git, Write/Edit only. Fold complete.

## Fold summary

RV2's five README-ready explanations (one per mechanism, hand-picked from the 50-seed/8-lane tape) now sit verbatim inside the reciprocal packet's matching sections as quoted "Mesh fold" blocks: S1 ledger → piece 1, S2 receipt-first → piece 2, S3 falsifiers → piece 3, S4 amendment obligation → piece 4, S5 outside reader → piece 7. The packet's own voice (RV1 claims + evidence pointers) is preserved; the mesh explanations are layered in as attributed quote material, not blended. Credit line added once under the pieces heading. RV2's single amendment proposal (mechanical `leaked_reasoning` flag) filed in the packet's new "Open items & amendment log" section with its otherwise-none branch. Verified clean by grep placement check and read-through. No JS touched.

## The five verbatim explanations as they now sit in the README

**1. The append-only ledger** — README piece 1 (spliced from or-union-alpha, seed 5):
An append-only ledger stores events as ordered rows: inputs, commitments, actions, outputs, and corrections. Each row includes the previous row's hash; changing an earlier row breaks subsequent links. Keep copies or publish checkpoints elsewhere, because someone controlling storage can otherwise rewrite the chain. Corrections reference earlier rows instead of replacing them, preserving what was known when a decision happened. Write intent before execution so crashes leave evidence of unfinished work. Another reader can replay the sequence and check its consistency. The ledger cannot make recorded claims true: hashes protect traceability, not factual correctness. A person still evaluates evidence and conclusions.

**2. Receipt-first work** — README piece 2 (spliced from or-ling3, seed 14):
Write the receipt first because it locks intent before execution drifts. The hash commits to inputs, constraints, and thresholds while the session is still coherent. If the session dies mid-work, the partial receipt is salvageable ore: it proves what was attempted, what inputs were locked, and where the chain broke. Another agent or the human can resume from that exact state or audit the gap without reconstructing intent from memory. It turns abandoned work into recoverable data rather than lost context. The mechanism is simple: pre-commit, then act. The receipt is the anchor; the partial receipt is the map back.

**3. Pre-registered falsifiers** — README piece 3 (spliced from or-union-alpha, seed 21):
A falsifier is a written claim: kill the theory if metric X crosses T. You commit T before running the data because afterward you'll move it. The number you'd accept post-hoc is always the number that spares the theory, and you can't feel that happening from inside. So write the threshold, its measurement method, and the kill date to the ledger first. When data arrives, comparison is arithmetic, not judgment — no negotiation. It cost me my favorite theory tonight; the mechanism did its job. Without pre-commitment, falsifiers are just intentions with better branding.

**4. The amendment obligation** — README piece 4 (spliced from cerebras-qwen, seed 35):
The amendment rule forces the runtime to confront drift. A fleet that only executes fixed rules accumulates edge cases, stale defaults, and silent failures. Each cycle must either change a rule or produce a reason, turning no change into a testable claim. That claim enters the ledger, allowing later replay to ask whether it was sound when fresh data or new failure modes made it stale. This blocks ritual maintenance. If you cannot justify the current rule, change it. If you can, you have recorded an explicit check for invalidation. The fleet becomes a self-auditing instrument, not a static shrine.

**5. The outside reader** — README piece 7 (spliced from mistral-min8, seed 44):
The tape is the only proof. If *you* control the replay, you can lie—edit, omit, or retroactively justify. An outside reader forces you to build a system where every step is *visible* and *unalterable*. Their ability to audit means the ledger's integrity isn't trust in *you*, but in the rules you've locked into the chain. If the tape can't be replayed without you, it's just a logbook. If it can, the system's logic survives you. That's why falsifiers are pre-registered: to let strangers verify the rules were followed, not just that you *said* they were.
