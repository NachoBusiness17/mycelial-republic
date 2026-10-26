# PA-D2-ds41 (deepseek-chat @ deepseek, turn 1, channel: content)

# ADJUDICATION, MOVEMENT 2: THE DOCTRINE ROAST

Conditions of this read. Instrument: I read the four evidence blocks as pasted into this session. I ran no commands and opened no files other than the pasted bytes. Moment: single pass, this session. Context assumption: the pasted bytes are byte-identical to the on-disk files, no reflow. Every `file:line` below is quoted from the pasted evidence; anything I infer rather than read is marked UNVERIFIED.

---

## (1) EXIT SEMANTICS: L1 amend, does not die

The cheap arm's claim: "grep counts ZERO `sys.exit(1)` sites" and "the docstring names exit 2 the only hard block." Both are byte-true against the pasted `tools/workflow_gate.py`:

- Line 10 (docstring): "exit 2 is the only hard block; every submission registers a row."
- Every return site in `main()`:
  - `return 1` on `OSError` reading the script (cannot-read-script; nothing registered)
  - `return 2 if failed else 0` on the `--no-register` path
  - `return 2` when `failed` after registering
  - `return 0` on clean pass
- `sys.exit(main())` at the module tail is the only `sys.exit` in the file.

So exit 1 exists in `main()` and is *not* a hard block. The docstring's "exit 2 is the only hard block" is literally correct.

**But my L1 objection survives in amended form.** The docstring asserts a *trivalent* contract (0 pass, 1 soft, 2 block). The actual code has **four** distinct exit-1 paths, and one of them is not "soft warn":

- Line "return 2 if failed else 0" under `args.no_register` collapses the no-register and block cases into 2, correct.
- The `OSError` path returns **1** with no registry row and no soft semantics: it is *"could not even read the input."* A caller switching on `1 = soft` will read an unreadable-file error as a soft warn.
- The docstring says "every submission registers a row." The `OSError` path registers nothing. So the docstring is byte-true for the *block* case (exit 2) but false for the *unreadable-input* case.

**Verdict: L1 AMENDS.** The block/pass contract holds. The trivalent claim holds *for well-formed input*. The docstring's "every submission registers a row" is falsified by the `OSError` return path, and the numeric meaning of 1 is overloaded: soft-warn in the check path, hard-error in the I/O path. The cheap arm's grep settled the *blocked-push* question; it did not settle the *I/O error is not a warn* question.

Positive example of a passing amendment. `return 2 if failed else 0` under `--no-register` preserves the block/pass contract for hook payloads without minting a dead-file row. This is the pattern the amendment should preserve.

Negative example of a failing case. `print(f"GATE ERROR: cannot read script: {exc}"); return 1` returns the same code a soft WARN returns at the call site. A hook switching on `1 = soft, non-blocking` will treat a missing/inaccessible script as a warn and let the push through.

---

## (2) REGISTRY ORDER: A4/O7 reconciliation HOLDS as census arithmetic

Read directly from the pasted `REGISTRY.jsonl`:

- Row 5 ts `2026-09-26T02:32:14Z` is the first `the-gala.dwf.ts` row. Rows are append-ordered in the paste.
- Row 40 is named `frontier-olm-mine` with ts `2026-09-30T01:18:10Z` per the cheap arm's quote.
- Rows 41-45 are `2026-10-01` per the cheap arm's quote.

The cheap arm's reconciliation: operations lane read "40 rows" pre-ractor50-final; accuracy lane read "45 rows" post-ractor50-final. Different moments, append-only file, both true. **This holds as arithmetic.** No census violation.

Positive example. Row 1 ts `2026-09-25T18:52:02Z` `tree-doctrine-dig` FAIL; row 2 ts `2026-09-25T18:52:43Z` same script PASS. Same moment-window, same script, two rows, append-only. That is the census law working in vivo.

Negative example (what would falsify the reconciliation and does not). If row 45's ts were **earlier** than row 40's, the append-only claim would break and one of the two counts would be a fabrication. The paste shows row 45's ts as `2026-10-02T01:52:29Z` on the `ractor-engine.dwf.ts` tail row, strictly later than row 40's `2026-09-30T01:18:10Z`. So the arithmetic is consistent.

**But A4's defect survives as a *reporting* defect, not a *census* defect.** My movement-1 objection named the missing moment, not a count error. accuracy.md still lacks a read timestamp; operations.md still lacks a read timestamp. The reconciliation is *derivable* but the chapters do not *state* the moments. The law "citations resolve to quoted bytes or are marked UNVERIFIED" is satisfied; the law "name the moment for any measurement" is not. A4 amends from "impossible ordering" to "unstamped moment."

**Verdict: A4/O7 census-arithmetic HOLDS. A4 reporting defect STANDS.**

---

## (3) UF-124: objection 1 stays OPEN, closing evidence named

The cheap arm reports the ticket's own premise files were NOT FOUND at the swept paths. The premise files (`DAY_PACK.md:2056`, `B2_16_uf_sweep_20260926.md:12`) are the *only* substrate for my movement-1 objection 1. Without those bytes, I have an assertion about a defect, not the defect. Per the estate law, a citation that does not resolve to quoted bytes is UNVERIFIED.

**What would close objection 1** (any one of these is sufficient; all three are ideal):

1. **The literal placeholder.** A quoted span from `B2_16_uf_sweep_20260926.md:12` containing the string `openreview.net/forum?id=XYZ` in the UF-124 answer body. That byte, if present, proves the citation never resolved to real fetched bytes and the proposed gate would have caught it. If the span instead shows a real openreview id, the objection weakens to "unverified."
2. **The misattribution.** A quoted span from the same file showing the claimed paper title attributed to the wrong lab (the movement-1 read names "Constitutional AI" as Anthropic's). The misattribution alone does not settle whether *existence* would pass the proposed gate; the placeholder alone does. Both are needed for the objection as originally written.
3. **The path resolution.** The output of `find . -name 'DAY_PACK.md' -o -name 'B2_16_uf_sweep_20260926.md'` from repo root, with the two resolved paths echoed. That closes the "file not found" procedural gap and re-enables the read of (1) and (2).

Until at least (1) lands as quoted bytes, **D1 objection 1 stays OPEN, not confirmed. Not refuted either.** An objection whose only substrate is an unfound file is a hypothesis, and the roast should say so.

---

## (4) ONE landable amendment from movement 1

**Chapter.** accuracy.md, §Incident 1 "Instrument upgrade" (and mapped to §Decision ledger).

**Paste-able sentence, replacing the acceptance clause:**

> A row carrying a citation or a tool-behavior claim lands LANDED only when the same session's receipt quotes, from fetched bytes or captured command output, the specific span carrying the claimed value (author, effect size, or default behavior); an id that resolves without that span lands UNVERIFIED, and until a resolver enforcing this exists in tracked code under `mag/` or `tools/`, this rule is stamped PROPOSED, not a changed contract.

**Why this is the amendment.** It closes A1 (id existence passes a misattributed but real citation), A2 (proposal stated as landed contract), and A3 (token match passes a wrong inference). Positive example: the UF-128 receipt would carry the `rg` output adjacent to the "rg skips symlinks" claim. Negative example: the UF-124 openreview id, even if it resolves to a real paper, lands UNVERIFIED because no quoted span carries the claimed effect size.

**Falsifier of this amendment.** If the pasted `tools/workflow_gate.py` already contains a citation-resolver function matching this specification, the amendment is dead because the contract is already enforced. I read the pasted file; no such resolver exists in the bytes shown. The amendment survives.

---

## (5) THE NEXT 3 DIG TICKETS

Each answerable from the corpus by a command; zero opinion.

1. **Which exit path in `tools/workflow_gate.py` does the pre-push hook actually consume, and with what switch?**
   `grep -rn 'workflow_gate' githooks/ .git/hooks/ || true; grep -rn 'no-register\|exit 1\|exit 2' githooks/pre-push`. 
   Closes the L1 amendment: does the hook treat exit 1 as soft or as a hard block, and does it call the gate with `--no-register`?

2. **What is the exact moment stamp on each REGISTRY read the two chapters cite?**
   `grep -n 'REGISTRY\.jsonl\|40 rows\|45 rows\|PASS 34\|FAIL 11' watch/inbox/model_garden/premium_autopsy/evidence/*/accuracy.md watch/inbox/model_garden/premium_autopsy/evidence/*/operations.md 2>/dev/null`.
   Closes A4 at the reporting layer: if neither chapter stamps a read moment, A4 stands as a reporting defect; if one does, that chapter's count is moment-pinned and only the other is naked.

3. **Does `B2_16_uf_sweep_20260926.md` exist anywhere reachable from repo root, and does its line 12 contain the placeholder `openreview.net/forum?id=XYZ` or a real id?**
   `find . -name 'B2_16_uf_sweep_20260926.md' -o -name 'DAY_PACK.md' 2>/dev/null; grep -n 'UF-124\|XYZ\|openreview' "$(find . -name 'B2_16_uf_sweep_20260926.md' -print -quit)" 2>/dev/null`.
   Closes D1 objection 1 either as CONFIRMED (placeholder present) or REFUTED (real id present), and re-tests the movement-2 cheap-arm claim that the file was not found.

---

## Falsifiers of this adjudication

- **L1.** A pre-push hook call site showing `exit 1` is treated as a hard block anywhere in `githooks/`. Then the L1 amendment overstates the defect; the defect would be worse, not smaller.
- **A4.** A read-moment stamp present in either chapter's cited span within the pasted bytes. Then A4 dies as a reporting defect and survives only as arithmetic-consistent-with-moments.
- **UF-124.** The file resolves and its line 12 shows a real, non-placeholder openreview id paired with a correct attribution. Then D1 objection 1 is REFUTED and the accuracy.md proposed gate would *not* have caught this instance.
- **Amendment.** A citation-resolver function already present in `tools/workflow_gate.py` matching the paste-able sentence. Then the amendment is dead on arrival.
