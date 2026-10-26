# G5-5 — DISPUTE TAXONOMY AS AUDIT TOOL (spawned from G3-3's bonus product)

2026-09-10 · zcode seat · $0, file-only — G3-3's 4-mechanism dispute taxonomy
compiled into a reusable 4-question corpus audit checklist, then fired on the
top 3 CONTROVERTED lines of `watch/INVARIANT_SHEET_V2.md`.

## THE POINT

G3-3's few-shot run found that the AGAINST sides of the 10 hardest-contested
lines deploy four distinct mechanisms, not one generic doubt. That taxonomy is
only a product if it survives being lifted out of context: a reviewer who has
never read the deepseek transcript should be able to pick up the four
questions, run them against any SUPPORTED label in the corpus, and get the
same closing moves G3-3 named. This file is that lift: the checklist, plus a
worked audit proving it reproduces the parent card's findings from the sheet
alone.

## THE 4-QUESTION AUDIT CHECKLIST (reusable tool)

Run all four questions against any claim carrying a status label (SUPPORTED /
UNPROVEN / DISPUTED) or any load-bearing line. A claim fails the audit on the
first question whose closing evidence does not exist.

**Q1 — LABEL INHERITANCE**
- Ask: *Is this label inherited from a source that defined it differently?*
- Catches: family/group/campaign-level labels laundering member claims; a
  row marked SUPPORTED because a parent document was; status granted at one
  granularity and reused at a finer one.
- Closing move: compare the label's original definition scope vs the scope it
  is now stamped on, line by line.

**Q2 — FORMAL VS REAL INDEPENDENCE**
- Ask: *Does the formal specification match the real-world referent?*
- Catches: "independent witness" = different seat, same assumptions/ledger/
  source; "re-run" = same inputs re-executed; "second verification" that
  shares the first's entire evidence chain.
- Closing move: for each formal property (independent, re-run, separate),
  list what the second instance actually touched. If any input overlaps the
  first, independence is nominal only.

**Q3 — PROVENANCE ≠ ACCURACY**
- Ask: *Does having a source make the claim true?*
- Catches: verbatim pinning, hash-witnessing, ledger entries, citations —
  all prove the text existed and is unaltered, never that its content is
  correct or that pinned versions are mutually consistent.
- Closing move: compare the preserved text against a refuting or later
  artifact (log entries, corrections, a second pin). Preservation history is
  not truth history.

**Q4 — NUMERIC DIES TO ONE COUNTER-COUNT**
- Ask: *Can this number be falsified by one counter-count?*
- Catches: counts, thresholds, denominators — any numeric claim where a
  single authoritative recount from the same store flips or kills it.
- Closing move: one direct query of the authoritative store + timestamp. If
  the recount differs, the claim is dead regardless of how many documents
  repeat the old number (duplication is emphasis, not confirmation).

**Usage laws:** (1) bind it to the CONTROVERTED shortlist first — clean lines
rarely need it. (2) The refutation counts feeding it are a negation-marker
heuristic; audit the line, not the count. (3) Answers must name artifacts and
comparison operations — the checklist triages, it never judges. "More research
needed" is a failed audit, not a verdict.

## AUDIT RESULTS — top 3 CONTROVERTED lines

Selection rule: highest combined dispute volume (agreement+refutation), same
ranking G3-3 used. Top 3: combined 15, 9, 9 (tie at 9 broken by sheet order).

---

### Claim 1 — [a=3 r=12 · net=-9] "per family references (the SUPPORTED tri-state row above, quoting her..."

| Q | Verdict | Finding |
|---|---------|---------|
| 1 label inheritance | **FAIL** | Home case. The family SUPPORTED label is inherited from one tri-state row quoting Astra's source; 12 refutations target the member-level arithmetic. Label granted at row granularity, stamped at family granularity — a family can read SUPPORTED while the arithmetic inside is disputed. |
| 2 formal vs real | FAIL | The formal grouping ("condition-arithmetic family") does not match the real referent — members refute independently, so the family is not one auditable unit. |
| 3 provenance | FAIL | The row's strength is a quotation. The quote proves what she wrote, not that the per-family arithmetic holds. |
| 4 numeric | FAIL | The claim embeds per-family numbers (bars, point deltas). Each family's number dies to one counter-count within that family — and members are exactly where the 12 refutations live. |

**Audit verdict: DISPUTED stands. Do not repair the label — split it.** Re-grade
each family member on its own numbers; the family label is unrecoverable as a
unit. Closing evidence: per-family member grades vs the quoted source row.

---

### Claim 2 — [a=2 r=7 · net=-5] "4. I4 falsifier re-run — A11 (same file, ledger)."

| Q | Verdict | Finding |
|---|---------|---------|
| 1 label inheritance | HIT | The implicit "verified" status is inherited from I4's original run. A re-run inherits the original's definitions of pass/fail — if those definitions were the disputed part, re-running inherits the dispute. |
| 2 formal vs real | **FAIL** | Core case, named in the line itself: "same file, ledger." Same file = same assumptions; same ledger = same state. A re-run reusing both is not an independent verification — it is the original computation executed twice. |
| 3 provenance | FAIL | The ledger entry proves the re-run happened at a time, not that it settled anything. 7 refutations say it did not settle it. |
| 4 numeric | FAIL | I4's verdict is a ratio with contested numerator/denominator (INSTANCE I4, sheet line: "FALSIFIER RE-RUN WITH CONTESTED DENOMINATORS"). One counter-count of the denominator flips the verdict — and the denominator is the disputed part. |

**Audit verdict: DISPUTED stands. The re-run is void as verification.** Closing
evidence: the A11 ledger entry — exact command, inputs, timestamp, and whether
the result differed from the original. If inputs are identical, demote the
"re-run" to "repeat" and find a witness that touches different inputs.

---

### Claim 3 — [a=2 r=7 · net=-5] "PROMOTION SUPPORTED requires >= 2 INDEPENDENT witnesses with the second at..." (truncated)

| Q | Verdict | Finding |
|---|---------|---------|
| 1 label inheritance | FAIL | "INDEPENDENT" is a label the witnesses inherit from the rule's own definition. If the defining text is truncated, the witnesses inherit an undefined property — no witness can be checked against a threshold nobody can read. |
| 2 formal vs real | **FAIL** | Core case. Sheet's sibling line names the mechanism: "witnesses partitioned across seats" — different seats, shared source = formal, not real, independence. Seat count is the formal spec; evidence-access is the real referent, and the line is cut off before either is specified. |
| 3 provenance | FAIL | A witness record in the ledger proves a witness existed, not that it was independent or met the threshold. |
| 4 numeric | FAIL | ">= 2" is a count, and it dies to one counter-count: one witness shown non-independent drops the count to 1, auto-demoting the claim to UNPROVEN by the rule's own demotion clause. The whole promotion regime is falsifiable by a single bad witness. |

**Audit verdict: DISPUTED stands, and the defect is upstream of any witness.**
The truncated rule cannot grant a checkable independence property. Closing
evidence: the full promotion-rule text, then seat-assignment records plus each
second witness's access path to the underlying evidence. Repair order: un-truncate
the rule, re-audit witnesses for real (not formal) independence, then recount.

---

## CROSS-CLAIM FINDING

All 3 claims fail all 4 questions — expected, since these are the corpus's
hardest-contested lines, but the *shape* of the failures matches G3-3's
mapping exactly: claim 1 dies on Q1, claims 2 and 3 die on Q2, and Q4 is live
in all three because Astra-arc disputes cluster on numbers and denominators.
The checklist also surfaced one thing the parent card only implied: Q1 and Q2
compound — a label inherited from a truncated definition (claim 3) cannot be
repaired by witness work until the definition itself is recovered. Suggested
run order when both fire: fix the definition, then re-audit.

## VALIDITY NOTES (tri-state)

- SUPPORTED: the checklist reproduces G3-3's mechanism mapping for all 3
  claims from the sheet text alone, with named closing moves for each.
- UNPROVEN: whether the checklist adds value on lines OUTSIDE the Astra arc —
  all 3 audited claims come from one document family (`ANSWER_2.md`), so
  cross-domain reach is untested. Next cheap probe: run the 4 questions on
  the CONTROVERTED lines sourced from `watch/TESUJI_MAP.md`.
- DISPUTED: none raised.

NEXT: if operator GOs, compile the checklist into the reviewer flow for any
new card carrying a status label (4 questions, ~2 min per claim), and file the
9 remaining G3-3 top-10 claims through it as the desk's dispute queue.

— MICKEY G5-5, zcode seat, 2026-09-10
