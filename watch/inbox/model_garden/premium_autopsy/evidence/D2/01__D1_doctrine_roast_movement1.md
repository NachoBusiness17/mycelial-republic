# D1_doctrine_roast_movement1 (anthropic/claude-opus-5.5, turn 1, channel: content)

# Adversarial Read: Doctrine Roast, Movement 1

## Conditions of this read

These conditions apply to every verdict below.

- **Instrument.** I read the four evidence blocks exactly as pasted into this session. I ran no commands, opened no files on disk, and resolved no URLs.
- **Moment.** Single pass, this session.
- **Context assumption.** The pasted bytes are identical to the on-disk files, with no reflow.
- **Line numbers for `logic.md`.** These are my own hand count of the pasted block, with line 1 being the `# THE ESTATE'S IMPLIED LOGIC SYSTEM` heading. A hand count is itself the "hand-copied count" class (accuracy.md, Incident 6), so every `logic.md:N` below is UNVERIFIED against disk until a seat runs `grep -n`.
- **Line numbers for `accuracy.md` and `operations.md`.** Both are too long to hand-count reliably. I pin them by section heading plus the quoted bytes. Their line numbers are UNVERIFIED.
- **`socratic_results.jsonl`.** Pinned by row `id`.

Every quote below is copied from the pasted evidence. No claim about code on disk is made except as quoted from these chapters.

---

## CHAPTER 1: accuracy.md

### Cheap seat verdict (socratic-accuracy): premise refuted, worry verified, evidence replaced

- **Refuted premise.** "every incident is assumed to be a citation failure."
  - The chapter's class table names 12 distinct classes, each with a distinct catch.
  - Examples: "harness-attribution error | probe failure reported as target failure | probe-vs-target separation rule" and "state-doc verdict decay".
  - The citation gate is the catch for only incidents 1, 5, and 12 (accuracy.md, Decision ledger: "incidents 1, 5, 12").
- **Refuted evidence.** "the 12 corrected incidents include at least one that cleared the gate before being overturned."
  - No gate existed when any incident occurred. Every instrument upgrade in the chapter is future tense.
  - The cheap seat names no incident because none exists in the bytes. Its claim is unsupported.
- **Verified worry.** The gate certifies form, not substance.
  - That worry is real, and the chapter's own Incident 1 proves it more concretely than the cheap seat did. See below.

### (1) Strongest surviving objection

The chapter's only landing-contract change is a resolver that its own Incident 1 would pass.

**The upgrade's acceptance test is id existence.** accuracy.md §Incident 1, Instrument upgrade:

> "each id must resolve to fetched bytes in the same session, else the row lands as UNVERIFIED, never LANDED."

**The same incident's verbatim block names a defect that resolves cleanly.** accuracy.md §Incident 1, quoting B2_16:12:

> "misattributes Anthropic's paper; effect sizes unverifiable."

A real Anthropic paper resolves to real bytes. So the misattributed citation passes "resolve to fetched bytes" and lands LANDED under the proposed gate.

**The upgrade is weaker than the falsifier it cites.** That falsifier (B2_16:25, quoted in §Incident 1) demands two things:

> "resolving one named citation ... and quoting the effect size it claims."

The upgrade keeps the first half and drops the second.

**Incident 12 has the same shape.** "rg ... Follows symlinks by default" is a claim about a real tool, and the tool exists. The fold-in rule ("carry a one-line repro command, run at filing") checks that a command ran, not that its output contradicts the claim.

**The retro then promotes this gate to a changed contract while touching no code.**

- accuracy.md, Method: "No code under mag/ or tools/ was touched by this lane."
- accuracy.md, Decision ledger: "changes one dispatch contract plus one landing contract."

By the chapter's own Incident 5 law, "a correction banked is not a correction applied." The Decision ledger is therefore a 13th incident of the chapter's own class 1.

### (2) Line-pinned defects

| # | Location | Quoted bytes | Defect |
|---|---|---|---|
| A1 | §Incident 1, Instrument upgrade | "each id must resolve to fetched bytes in the same session" | Existence check. It passes a misattributed but real citation, which is the very defect named in the same incident at B2_16:12. |
| A2 | §Decision ledger | "This dance closes the accuracy-retro owed work and changes one dispatch contract plus one landing contract" | No enforcing code exists (§Method: "No code under mag/ or tools/ was touched"). This is a proposal stated as a landed contract, which is class "ok:true-equals-landed" applied to itself. |
| A3 | §Incident 5, Instrument upgrade | "(b) the line range is non-empty and mentions a token from the claim" | A token match is form. A wrong inference that names the right file and token passes. This is the cheap seat's worry, located at the exact bytes. |
| A4 | §Supporting observations | "my parse this session reads 45 rows, verdict PASS 34 / FAIL 11" | No timestamp, which breaks the chapter's own moment law. It conflicts with operations.md §3: "memory/workflows/REGISTRY.jsonl holds 40 rows". On an append-only file, 45 followed by 40 is impossible; only 40 followed by 45 is consistent. Neither chapter states the read moment, so the order cannot be reconstructed. |
| A5 | §Incident 10 | "both sha256 f873a43aaf1d241f" | 16 hex characters is a truncated digest presented as "sha256". "identical: True" carries the identity claim, but the label overstates the instrument. |
| A6 | §Incident 7 and §Incident 10 owner lines | "Owner: the close step of every lane that self-feeds briefs" / "Owner: the next bank-walking lane" | These are roles, not seats. Incident 11 is the same: "owner: whoever registers the next scheduled task". An owner that is a class of future actors cannot be held to an owed item. |
| A7 | §Finish-line self-check | "byte-verifies 34 quote spans against their named source files" | This proves quotes exist in their sources. It does not test any defect-class attribution or any "falsifier that would have fired" claim. The chapter's own success signal is the form-check it diagnoses. |

**Positive example worth keeping (not a defect).** §"The ask's named incident I could not confirm as stated" refuses to manufacture a "w4-20 placeholder" incident. That is the correct handling and should be the template.

### (3) Landable amendment

Paste this, replacing the first sentence of §Incident 1 "Instrument upgrade" and the "(2)" clause of §Decision ledger:

> A row carrying an external citation or a tool-behavior claim lands LANDED only when the same session's receipt quotes, from fetched bytes or captured command output, the span carrying the specific claimed value (author attribution, effect size, default behavior); an id that resolves without that span lands UNVERIFIED, and until a resolver enforcing this exists in tracked code this rule is PROPOSED, not a changed contract.

How the rule sorts cases:

- **Passes (positive).** The UF-128 receipt carries `rg PATTERN dir_with_symlink` output showing the symlinked file absent, next to the claim "rg skips symlinks unless --follow".
- **Fails, lands UNVERIFIED (negative).** The UF-124 openreview id resolves to a real paper, but no quoted span shows the claimed authors or effect size.

---

## CHAPTER 2: logic.md

### Cheap seat verdict (socratic-logic): evidence refuted, objection (3) out-done

- **Refuted evidence.** "the 874-drift-rows finding shows 'clean' meant well-formed."
  - The token "874" appears nowhere in logic.md, and "clean" does not appear as a redefined census term.
  - The cheap seat imported evidence that is not in the chapter. Its objection (2) inherits that fabrication.
- **Refuted conflation.** Its objection (2) also fuses law 2 (census denominator) with law 3 (0-corroborated). These are separate laws with separate quotes and separate falsifiers (logic.md:35-42 vs logic.md:43-54).
- **Out-done objection (3).** "who certifi
... [PREMIUM AUTOPSY REPLAY SIZING: file truncated, showing head 7875 + tail 2625 of 23030 chars; method head75+tail25, moment 2026-10-01; the premium original saw the full bytes] ... ...
ource.
- **Negative example (current practice).** "Quote X exists in file Y."
- **Positive example (what is missing).** "Rule X fired on case Z, and here is the refusal output."

---

## (5) THE NEXT LEG: three dig tickets

Each question is answerable from the corpus by a command, not by opinion.

1. **What do the exit codes in `tools/workflow_gate.py` actually mean?** Run `grep -n` on lines 1-30 of `tools/workflow_gate.py` (the docstring) and on every `sys.exit` / `return` site. Which exit code is documented as "undecidable" and which as "refutable violation" or "warn"? Does exit 1 ever block a push?
   - This settles L1.
   - It also tests the logic.md:85-87 claim that the 10-11 quote miss was only line wrapping.
2. **In what order were the two REGISTRY counts taken?** In `memory/workflows/REGISTRY.jsonl`, find the `ts` field of row 40 and of row 45. Was row 45 written before or after `2026-10-01T01:16:55Z` (the operations lane's own minted row)? Which of the accuracy lane's "45 rows" and the operations lane's "40 rows" was taken first?
   - This reconciles A4 and O7.
   - It establishes whether either chapter's census violates append-only arithmetic.
3. **Would the proposed resolver have caught UF-124?** In `DAY_PACK.md:2056` and `B2_16_uf_sweep_20260926.md:12`, which Anthropic paper is "misattributed", and what id does the UF-124 answer cite for it? Does that id resolve to real fetched bytes (arxiv or openreview lookup)?
   - If it resolves, the accuracy.md proposed gate would have passed it, confirming my objection (1).
   - If it does not resolve, that objection weakens to a hypothetical.

---

## Falsifier for this deliverable

This read is wrong, chapter by chapter, if any of the following holds:

- **Logic.** Ticket 1 shows `tools/workflow_gate.py` documents exit 1 as "warn" and exit 2 as "undecidable with evidence file", consistent with every sentence at logic.md:16-33. The L1 contradiction would then be one of prose wording only, and my strongest logic objection drops to a wording defect.
- **Accuracy.** Ticket 3 shows UF-124's misattributed paper was cited by a non-resolving id. The id-only resolver would then have caught it, and my strongest accuracy objection loses its in-chapter instance.
- **Operations.** `git ls-files .zcode/workflows/the-gala.dwf.ts` or any tracked mirror returns the rateLimitHold bytes with a commit sha. My strongest operations objection then dies.
- **All line pins.** `grep -n` on the on-disk `logic.md` disagrees with my hand count by more than one line at any pinned site. That falsifies those pins, which are already marked UNVERIFIED above.
