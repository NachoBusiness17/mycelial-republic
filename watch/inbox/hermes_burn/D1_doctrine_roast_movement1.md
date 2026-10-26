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
- **Out-done objection (3).** "who certifies the outside" is sharper when made concrete.
  - Law 4's steal is "run a caller count" (logic.md:61).
  - Law 4's own falsifier names the blind spot of that exact instrument: "a proved zero-text-caller mechanism nonetheless load-bearing through dynamic dispatch" (logic.md:63).
  - The "outside" is a text grep, which is an inside instrument with a self-declared hole.
- **The cheap seat missed the chapter's actual crack**, which is in law 1.

### (1) Strongest surviving objection

The chapter's foundational law states two incompatible exit mappings, and both laws that cite code cite the spans the chapter's own sweep rejected.

**Mapping 1.** logic.md:16-17:

> "exit 0 banks, exit 1 warns with reason, exit 2 blocks with its own evidence file"

Here exit 1 is a warning and exit 2 is a block.

**Mapping 2.** logic.md:27-28 and logic.md:29-30:

> "exit 2 blocks with its own evidence file, the undecidable middle escalates to a human wire"

> "pass, refutable violation, undecidable"

Taking the quoted triple in order, exit 1 is "refutable violation" and exit 2 is "undecidable". Yet lines 27-28 call undecidable "the middle".

**What the readings disagree on.** Exit 1 is a "warn" in one reading and a "refutable violation" in the other. "Undecidable" is the middle value in one reading and value 2 in the other. The falsifier at logic.md:33 ("a landed gate whose exit 1 silently blocks a push") only makes sense under mapping 1.

**What the chapter rests on to settle it.** The one artifact that would settle the mapping is the steal target "the tools/workflow_gate.py:10-11 shape" (logic.md:32). That is exactly the span the lane's sweep recorded as a miss and rejected:

> "2 misses honestly recorded and those quote forms rejected (wrapped-line spans in tools/workflow_gate.py:10-11 and tools/drift_pairs_stamp.py:65-67)" (logic.md:85-87)

**Law 5 repeats the pattern.** It cites the second rejected span as its mechanism: "(tools/drift_pairs_stamp.py:65-67, REFERENT_MATURE_DAYS=7)" (logic.md:69).

**Result.** Two of the five laws cite as authority the bytes the chapter admits it could not verify. The chapter's header promises "those quote forms were rejected, not repaired" (logic.md:11-12). The laws then use those spans anyway, as steal targets and mechanism citations.

### (2) Line-pinned defects

| # | Location | Quoted bytes | Defect |
|---|---|---|---|
| L1 | logic.md:16-17 vs 27-30 | "exit 1 warns with reason" / "pass, refutable violation, undecidable" | Two incompatible exit-code mappings in one chapter's central law. |
| L2 | logic.md:32 | "(the tools/workflow_gate.py:10-11 shape)" | Steal target is the span rejected at logic.md:86-87. |
| L3 | logic.md:69 | "(tools/drift_pairs_stamp.py:65-67, REFERENT_MATURE_DAYS=7)" | Mechanism citation is the second rejected span. The constant 7 is therefore UNVERIFIED in this chapter. |
| L4 | logic.md:37-38 | "(AGENTS.md, byte-hit 1; ...)" | No line number. This breaks the file:line law the estate imposes. |
| L5 | logic.md:40-42 | "Falsifier: a same-instrument delta reconciling byte-exactly with zero named landings in the window." | This does not falsify "never difference two counts taken at different moments". A true falsifier would be cross-moment differencing that repeatedly yields correct deltas with no attribution. As written, the falsifier tests something else. |
| L6 | logic.md:50-52 | "witness one sibling lane's grounding_wave claim row under your own seat name - the second distinct seat makes corroboration reachable" | This counts seat names, not independence. Fleet seats can satisfy "two distinct non-author witnesses" (logic.md:44) without independent evidence. That games the threshold the law describes. accuracy.md §Incident 1 shows free seats shipping fabricated citations, which is exactly the witness pool this steal recruits. |
| L7 | logic.md:98-99 | "so a 40/41 verify count overstates nothing about liveness." | This contradicts the decision it concludes. The decision ("stop scoring verified organs as wired organs", logic.md:95) is only needed if the verify count, read as wiring, overstates liveness. |
| L8 | logic.md:8-9 | "copied from the lane JSON / check transcript, none re-derived." | A doctrine chapter that is a report-of-a-report. This is accuracy.md class "hand-copied count", self-declared. |
| L9 | logic.md:85 | "11 candidate quotes: 9 byte-hits used, 2 misses" | Only 5 quotes appear in the chapter, one per law. The 4 other "used" hits are unaccounted for. |
| L10 | logic.md:104-106 | "all 6 sibling chapters PROVEN at re-probe, bytes: accuracy 27274, ..." | PROVEN backed by byte size alone. This is "ok:true-equals-landed" (accuracy.md class table row 1) applied to the fold note. |

### (3) Landable amendment

Paste this as a new sentence immediately after logic.md:22, ending "(rewritten 2026-09-30).":

> Law 1's mapping of exit 1 and exit 2 onto "refutable violation" and "undecidable" is UNVERIFIED until a quote from tools/workflow_gate.py byte-verifies under newline-normalized matching (the 10-11 span missed in check 3), and no law in this chapter may cite, as steal target or mechanism, a span its own sweep rejected.

How the rule sorts cases:

- **Passes (positive).** Law 1 cites `tools/workflow_gate.py:10-11` with a newline-joined quote that the check transcript marks as a hit.
- **Fails (negative).** Law 5 cites `drift_pairs_stamp.py:65-67` while check 3 still lists that span as a miss.

---

## CHAPTER 3: operations.md

### Cheap seat verdict (socratic-operations): mostly refuted

- **Refuted: F7 is misquoted.** The cheap seat calls F7 "fold preserves ask-shape identity". The chapter's F7 actually reads: "Fold outputs are durable before the receipt is written: receipt existence is verified by a single-file glob wrapped in catch" (operations.md §Fold-shape rules, F7). The cheap seat's "recorded failures show folds that re-emitted a mutated ask under the original wave id" matches no failure in §"The eight failures".
- **Refuted: invented vocabulary.** "the fuzzer emits them" and "card-to-commit mapping" appear nowhere in the chapter.
- **Refuted: "Nothing in the chapter tests whether waves overlap."** §5 "Shared-index commit races" documents exactly that: "its surface rebuild absorbed other lanes' 130 concurrent registers".
- **Partly refuted: "never prices" coordination.** The chapter prices throughput ("burn wave width 10 x3 waves clean at 109.4M tok/h", §8) and states "rolling throughput is the binding constraint" (§4).
- **What survives.** A residue of its premise survives, sharpened as defect O4 below.

### (1) Strongest surviving objection

The chapter's headline claim, "moves owed laws from prose to code", lands that code on an untracked surface. That reproduces accuracy.md's Incident 3 class inside the doctrine meant to prevent it.

**The claim.** operations.md §Decision ledger:

> "moves owed laws from prose to code: two in the saved the-gala workflow (rate-limit refire hold per B2-476; truncation caps)"

**The surface.** operations.md, Gate paragraph:

> "the edited surfaces are .zcode/workflows/the-gala.dwf.ts (gitignored, .gitignore:198)"

**Why this matters, by the chapter's own evidence:**

- A gitignored file has no commit history. accuracy.md §Incident 3 names the cost of that: "The four fold outputs are untracked in git with no committed history, so the predecessor text is not recoverable."
- The chapter itself already cites an unrecoverable pre-edit location in that same file: "(the-gala.dwf.ts:269 pre-edit)" (§1). The citation cannot be resolved by anyone now, because the pre-edit bytes are not tracked anywhere.
- The 127 fix has the same exposure. "estate-root `bash.exe` shim (cwd-precedence interception to Git Bash, gitignored ...)" (§1). The one mechanism that makes failure 1 not recur exists on one host's working tree.

**Result.** Two of the three "wired this sitting" changes, and the failure-1 shim, are invisible to `git log`, to pre-push, and to any other clone. They are one overwrite away from becoming prose again.

### (2) Line-pinned defects

| # | Location | Quoted bytes | Defect |
|---|---|---|---|
| O1 | §Gate paragraph | "the edited surfaces are .zcode/workflows/the-gala.dwf.ts (gitignored, .gitignore:198)" | Doctrine-as-code on an untracked path. This is the Incident 3 class. |
| O2 | §Decision ledger vs §"What this lane wired" | "two wired this sitting" vs items "1. `rateLimitHold`", "2. Truncation caps", "3. fold_gate.sh shape guard" | Count mismatch, 2 vs 3. The ledger's own earlier sentence also lists three changes ("two in the saved the-gala workflow ... and one in the shared fold gate"). |
| O3 | §Ask-shape rules, A1 | "keep max_concurrency at 3 or less on this account" | §4 says "workflow children have NO measured clean rung". A ceiling of 3 is therefore unanchored, and §8 says unanchored rows must be "named as unanchored". A1 does not name it. |
| O4 | A3 vs F6 | "batch all report()s after allSettled in that fixed order" vs "every landed lane is reported the moment it banks" | F6 is unconditional, while A3 carves out "a wide same-shape fan-out". "Wide" is undefined, so a seat cannot decide which rule binds. This is the surviving residue of the cheap seat's "discrete unit" worry: the ask/fold boundary is shape-dependent and the shape threshold is unwritten. |
| O5 | §"What this lane wired", item 1 | "Hold failure or timeout degrades to the old immediate refire, logged" | This is an outcome-dependent branch inside a script whose determinism law reads "replayable scripts cannot read clocks" (§2). Whether a timeout outcome replays identically is not shown. This is my inference, UNVERIFIED against the script bytes. "The powershell hold spawn shape was tested on this host this session (exit 0)" tests the spawn, not the hold in a real 1302 death path. |
| O6 | §3 | "verified on disk at the argparse block, lines ~283-287" | An approximate line citation. A "~" is not file:line. |
| O7 | §3 | "memory/workflows/REGISTRY.jsonl holds 40 rows" | No timestamp. It conflicts with accuracy.md's 45 (see A4). The chapter's own row mint is stamped "ts 2026-10-01T01:16:55Z", but the census moment is not. |
| O8 | §Fold-shape rules, F3 | "ok-false with banked evidence (rows or checks) is danced, not failed" | "Banked" is an existence test. Content is not checked, so a lane whose banked rows are fabricated (accuracy.md §Incident 1) counts as danced. |

### (3) Landable amendment

Paste this as the first sentence of §Decision ledger, replacing "Closes: ... and moves owed laws from prose to code:":

> A mechanism counts as moved from prose to code only when its bytes live at a git-tracked path and the receipt cites the commit sha; the-gala.dwf.ts changes (rateLimitHold, truncation caps) and the estate-root bash.exe shim stand as UNTRACKED-WIRED until committed or mirrored to a tracked path, and this sitting wired three changes, of which one (fold_gate.sh) is tracked-eligible.

How the rule sorts cases:

- **Passes (positive).** "fold_gate.sh guard, commit <sha>, fold_gate.sh:14-24."
- **Fails (negative).** "the-gala.dwf.ts:269 pre-edit" cited with no tracked predecessor.

---

## (4) THE PATTERN: the fleet's doctrine blind spot

**All three chapters certify that the record exists and then treat that existence as the law being in force.** This is the estate's own class "ok:true-equals-landed" (accuracy.md class table, row 1), turned on the doctrine itself. The estate already wrote the counter-law ("a correction banked is not a correction applied", accuracy.md §Incident 5). None of the three chapters applies it to its own landing.

| Chapter | Existence signal used as proof | What is never checked |
|---|---|---|
| accuracy.md | "34/34 spans pass" (§Finish-line self-check); "changes ... one landing contract" (§Decision ledger) | Whether any contract is enforced. No code was touched. |
| logic.md | "PROVEN ... bytes: accuracy 27274" (logic.md:105); "none re-derived" (logic.md:9) | Whether the five laws agree with each other or with the cited code. L1 shows they do not. |
| operations.md | "moves owed laws from prose to code" (§Decision ledger) | Whether that code is tracked. It is gitignored (.gitignore:198). |

**The mechanical form of the blind spot:**

- Every finish line in the three chapters is a quote-match, a byte count, or an exit 0.
- No finish line resolves a law against its referent. The referent would be the enforcing code at a tracked path, the exit semantics in the cited file, or a claimed value in a fetched source.
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
