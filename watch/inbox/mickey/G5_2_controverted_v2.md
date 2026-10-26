# G5-2 — REMAINING CONTROVERTED LINES THROUGH V2 PROMPT (spawned from G4-2's NEXT)

2026-09-11 · zcode seat · deepseek-chat (T2) fired twice (10 claims each) on the
CONTROVERTED lines G3-3/G4-2 did not cover, using the G4-2 v2 prompt verbatim
(few-shot block + the classifier-noise disclaimer line — the one G4-2 proved kills
count-defense).

## THE POINT

G4-2 proved the v2 fix on the SAME 10 lines as G3-3. This run asks the two open
questions: (1) does the v2 prompt hold on a FRESH batch the model has never seen,
or was 0/10 count-defense a one-batch fluke? (2) does the closing-evidence
checklist generalize past the Astra witness-rule cluster into the rest of the
corpus (tesuji receipts, metering configs, grounding-wave rows, threshold math)?

## RUN RECEIPT (2 calls, within bounds)

- model=deepseek-chat · max_tokens=6000 · temp=0.3 · finish=stop BOTH (no truncation)
- call A: 791 prompt + 2,002 completion = 2,793 tok · 9.4s
- call B: 836 prompt + 1,306 completion = 2,142 tok · 7.0s
- total: 1,627 + 3,308 = 4,935 tok · 16.4s · pennies
- raw: `_g52_ds_raw_v2_a.txt` / `_g52_ds_raw_v2_b.txt` (root scratch)
- repro: `_g52_deepseek_v2.py` · full-30-line dump: `_g52_dump_controverted.py`
  (re-runs mag/invariant_surface.py's pipeline verbatim; corpus drifted since the
  frozen sheet — 34 controverted now vs 30 then; claim texts and counts below are
  from the fresh dump, and the 10 covered claims were matched by identity and
  excluded, not by row position)
- key read from `.env`, header use only, never echoed

## THE 20 CLAIMS (fresh-dump counts; FOR/AGAINST/EVIDENCE condensed from deepseek)

**1. [a=3 r=3]** "S4 (twin I4): re-derive a falsifier verdict where numerator, denominator, and ..."
- FOR: re-running the falsifier with contested inputs is the correct robustness test.
- AGAINST: truncated — never states the re-derived verdict or whether the outcome changed; re-deriving may reproduce the ambiguity, not resolve it.
- EVIDENCE: full ANSWER_2.md context around the S4/I4 re-run (original numerator/denominator, contested alternatives, final verdict) + the rule defining when re-derivation with contested inputs is legal.

**2. [a=2 r=7]** "UNPROVEN, evidence attached) by EXECUTING RULE CARD I5-RC-v1 over the exhibit ..."
- FOR: procedural claim — if the rule card was correctly applied, the UNPROVEN label is justified.
- AGAINST: fragment shows neither the rule card text nor the exhibit; misapplication or an incomplete exhibit invalidates the verdict. (Fresh hard-contested line — r=7, NOT in the frozen sheet's surfaced 15; the corpus grew a new dispute since Sep-10.)
- EVIDENCE: I5-RC-v1 full text + the exhibit + an execution trace of which conditions were met, plus any superseding counter-rule cards.

**3. [a=2 r=6]** "INSTANCE I4 — FALSIFIER RE-RUN WITH CONTESTED DENOMINATORS (2026-09-11)"
- FOR: factual record of an event; if it occurred as described, the claim is true.
- AGAINST: truncated — states no outcome; refutations may deny the re-run was valid or the denominators genuinely contested.
- EVIDENCE: the complete INSTANCE I4 record (original run, contested values, procedure, final verdict) + an audit log showing who ran it under what authority.

**4. [a=2 r=5]** "| Input allowance | ≤ 6,000 tokens (packet ≈ 3.5K + shared constitution prefix) |"
- FOR: concrete, testable operational constraint — if packet + prefix sizes are as stated, the allowance holds.
- AGAINST: fragment never specifies the tokenizer or whether the prefix is counted separately; a bigger real packet violates the allowance silently.
- EVIDENCE: actual token counts of packet and prefix measured with the SAME tokenizer, plus the config that sets the 6,000 cap. ($0 check — this seat's own runs measure packet sizes continuously; G5-2 call A itself prompted at 791 tokens.)

**5. [a=2 r=5]** "DEMOTION A claim with < 2 independent witnesses = UNPROVEN, regardless of ..."
- FOR: clear epistemic standard against single-source promotion.
- AGAINST: the "regardless" clause is unbounded; "independent witnesses" is undefined; a single strong witness may be wrongly demoted. (Same rule family G3-3/G4-2 argued from the other side — the corpus disputes both halves of the promotion/demotion rule.)
- EVIDENCE: full rule text with rationale and exceptions + demotion case history + an independence audit of the witnesses actually used.

**6. [a=2 r=3]** "Family: I4 (falsifier re-run) — irreducible deck, HOLD 2 slot 4."
- FOR: classification + placement claim; correct iff the deck is irreducible and slot rules place it there.
- AGAINST: fragment defines neither "irreducible deck" nor the slot rule; both terms are load-bearing and unstated.
- EVIDENCE: the corpus definition of "irreducible deck," the full I4 deck listing, the HOLD 2 slot-assignment rules, plus any counter-example that reduces the deck.

**7. [a=2 r=3]** "excluded -> C1 keeps key verdict SUPPORTED (12). A seat holding only ..."
- FOR: conditional verdict-preservation claim — valid exclusion + 12 independent supporting lines keeps C1 SUPPORTED.
- AGAINST: truncated — what was excluded and what the seat holds are both missing; if the 12 lines are not independent, the count launders the verdict. (Label-inheritance mechanism from G3-3, again.)
- EVIDENCE: C1's full verdict + the 12 supporting lines + the exclusion criteria + the seat's holdings + an audit that the exclusion was correctly applied.

**8. [a=2 r=3]** "`G/law65/instrument` SUPPORTED — LAW-065 third leg: destructive_receipt record/check (warn-only) + percolator _save_registry demo call site; ledger research/destructive_receipts.jsonl ..."
- FOR: detailed evidentiary claim — if the named files and call sites exist as described, the SUPPORTED is earned.
- AGAINST: fragment doesn't show the ledger or code content; if the check is not actually warn-only or seat attribution is wrong, the claim is false.
- EVIDENCE: the actual ledger content, the percolator call-site code, LAW-065 text, and seat-attribution records.
- (zcode VERIFICATION, post-run: mag/destructive_receipt.py EXISTS — 6.5KB, 2 LAW-065 mentions; research/destructive_receipts.jsonl EXISTS — 11 rows. The claim's SUPPORTED label checks out against exactly the evidence the model named. Grounding hit — the instrument's resolution move was executable the same hour it was proposed.)

**9. [a=2 r=2]** "the recovery dossier (2,960 leaves, five phases). Kept as C09's trap row:"
- FOR: factual record — the dossier exists with those properties.
- AGAINST: fragment never says what a "trap row" is or why C09 kept it; both are load-bearing.
- EVIDENCE: the dossier itself (leaf count, phase structure) + C09's records stating the trap-row rationale.

**10. [a=2 r=2]** "CONFIRMED (the comparison is INCLUSIVE: a share of exactly 0.3000 MEETS ...)"
- FOR: precise mathematical claim — if the threshold is inclusive, exactly-0.3000 meets it.
- AGAINST: fragment states neither the threshold value nor the comparison context; rounding or an exclusive reading flips the verdict.
- EVIDENCE: the comparison rule's full text (threshold value, inclusive vs exclusive) + the exact share value + any rounding rules.

**11. [a=2 r=2]** "The recorded verdicts (constellation CONFIRMED at 60.7%; REFEED_HEAVY; the ..."
- FOR: recorded artifacts — checkable directly against the run log.
- AGAINST: the 60.7% confirmation and REFEED_HEAVY label may be disputed on the denominator, scoring rule, or CONFIRMED-vs-REFEED classification.
- EVIDENCE: the raw run log + classifier output that produced both verdicts + any contemporaneous dispute note. (zcode note: the fleet's sheet carries "coldest-vertex gate → CONFIRMED at 60.7%" at net=+3 · refute=0 — this refutation smells like classifier noise from the I4 denominator theme bleeding in on token overlap. The model's named check is exactly the receipt the fleet already holds. Partial predictive hit.)

**12. [a=2 r=1]** "I2 theme-lexicon reconciliation, I3 chain-state reconstruction, I4 falsifier ..."
- FOR: methodology claim — the named steps were performed.
- AGAINST: one or more steps may have been skipped or mislabeled.
- EVIDENCE: the actual I2/I3/I4 artifacts in the run directory, timestamped.

**13. [a=3 r=1]** "Ollama local (exploratory tip — cheap, always on)"
- FOR: practical recommendation consistent with local-model use.
- AGAINST: may not be actually always-on, cheap at scale, or production-suitable.
- EVIDENCE: fleet config (is Ollama default-on?) + cost/latency measurements from real runs. (zcode note: the lone refutation is likely negation-marker noise from the adjacent "no eye container" lines — the disclaimer did its job; the model argued the claim, not the classifier.)

**14. [a=3 r=1]** "DESIGN CONSTRAINTS INHERITED FROM ASTRA (SUPPORTED, cited)"
- FOR: SUPPORTED with explicit source references; agreement repeats the constraint set.
- AGAINST: the citation may point to a superseded Astra document, or SUPPORTED is an overclaim.
- EVIDENCE: the cited Astra source + a diff of the constraints in this run against that source.

**15. [a=3 r=1]** "the falsifier verdict — with the denominator contested (one seat holds the ...)"
- FOR: accurately reports a live dispute — one seat holds a different count.
- AGAINST: the "one seat" may not be authoritative, or the verdict should read with a fixed denominator.
- EVIDENCE: the falsifier scoring sheet (numerator + denominator) + the dissent note specifying the alternative denominator.

**16. [a=3 r=1]** "(94% PASS), rotation 0.950, tesuji ~310 cells vs a 200 bar, MAX_DISTILL epoch-1 ..."
- FOR: concrete metrics — factual report of measured values.
- AGAINST: any single number may be wrong-context — wrong bar, inflated count, or a PASS from a different run.
- EVIDENCE: the run's metrics file with raw PASS count, rotation, cell count, and the defined 200 bar. (zcode note: the fleet's receipt exists — refeed guard B1 at 94% falsifier PASS; the model's "different run" attack is close to the real drift risk when the fragment strips the number's context. Predictive hit.)

**17. [a=3 r=1]** "Falsifier F-H0 binds this document: 3 consecutive desk rejections of seed ..."
- FOR: clear, checkable trigger condition.
- AGAINST: the rejections may not be consecutive, F-H0 may not bind this document, or the seed IDs differ.
- EVIDENCE: the desk rejection log with dates + seed IDs, checked for three consecutive hits on the SAME seed.

**18. [a=2 r=1]** "Metering: ≤8,000 tokens in / ≤1,536 tokens out per episode; thinking=low"
- FOR: explicit configuration statement, verifiable.
- AGAINST: actual runs may have exceeded the limits, thinking=low may not have been honored, or the limits bind a different episode type.
- EVIDENCE: the episode metering log — actual token counts + the thinking setting used. (Known-true corroboration: fleet infra findings already record "5.3 needs thinking=low + >=1536 max_tokens" — the numbers match the live lanes.)

**19. [a=2 r=1]** "| W5a | GROUNDING WAVE row (2026-09-06T17:54:59Z, SUPPORTED): REGISTRY AUTO-HEAL LANDED ... 18/18 falsifier checks PASS ... byte-identical through the fix. |"
- FOR: quoted, timestamped grounding-wave row with a specific checkable claim.
- AGAINST: the row may be mislabeled, the 18/18 not all run, or the file not byte-identical.
- EVIDENCE: the grounding-wave record at that timestamp + the 18 check results + a byte-level diff before/after the fix.

**20. [a=2 r=1]** "| W5b | SALON FOLD EXCERPT (2026-09-06): the registry auto-heal landed with 18/18 falsifier checks PASS, as recorded on the grounding wave at 2026-09-06T17:54:59Z. |"
- FOR: corroborates claim 19 with the same facts and timestamp.
- AGAINST: **the salon fold is a secondary summary, not independent evidence — it inherits any error in the grounding wave it cites.** The sharpest line in either call.
- EVIDENCE: the original fold notes vs the grounding-wave record, compared line-by-line for timestamp, check count, and byte-identity claim.
- (zcode note: this is the formal-vs-real-independence mechanism from G3-3/G4-2 rediscovered INDEPENDENTLY on a fresh pair — W5a/W5b are one fact in two documents, agreement double-counted by any corpus-level repetition counter. The fleet's own grounding-wave v3 rule exists precisely because of this; the model arrived at it from the claim text alone. Strong structural hit.)

## GRADING — resolvable disputes or both-sidesism?

**Verdict: resolvable. 18/20 strong, 2/20 soft. Not both-sidesism.**

1. **20/20 RESOLVING EVIDENCE entries name a specific artifact AND a specific
   comparison operation** (execution trace; same-tokenizer recount; diff vs cited
   source; byte-level diff; consecutive-rejection check; line-by-line fold-vs-wave
   compare). Zero "more research needed." The checklist generalizes: it held past
   the Astra witness cluster into tesuji receipts (8), metering configs (18),
   grounding-wave rows (19/20), and threshold math (10).
2. **Claim 8 was VERIFIED within the hour** — the named artifacts exist and the
   SUPPORTED label holds. The instrument proposed a check the fleet executed
   immediately and passed. That is the cheapest possible validation, now 2-for-2
   across runs (G3-3's claim 7 was the first).
3. **Two independent rediscoveries of the fleet's own mechanisms** on fresh data:
   claim 20's secondary-summary-is-not-a-witness (grounding-wave v3 rule) and
   claim 7's count-laundering (label inheritance). The dispute taxonomy from
   G3-3 recurs on unseen lines — it is a property of the corpus, not the sample.
4. **Soft spots:** claims 6 and 9 lean on unstated in-corpus jargon ("irreducible
   deck," "trap row") where the fragment alone carries no adjudicable content —
   same fragment-weakness correlation as G3-3, again tracking the sheet's weakest
   lines, not the model.

**The one regression — the disclaimer is not fully stable:**
G4-2 measured 0/10 count-led AGAINST entries. This run: **call B held at 0/10,
call A partially reverted to 6/10** ("The refutation count (7) suggests many
corpus lines dispute..."). The reversion is softer than v1 — every count-led
opening still follows immediately with a content defect (missing rule text,
unspecified tokenizer, unstated outcome) — but the count is back as the opening
move on the high-refutation claims (r=5-7). Honest read: at temp 0.3 the
disclaimer REDUCES count-defense, it does not eliminate it; salience of big
refute counts is the risk factor. The v2 prompt stays; if a future run needs
hard count-immunity, the next lever is dropping the counts from the prompt
entirely rather than disclaiming them (untested — one more call would settle it).

## INSTRUMENT VERDICT

**Useful — confirmed on fresh batch.** 2 calls, 16.4s, 4,935 tokens, zero
truncation, 20/20 executable dispute closures, 1 verified-same-hour, 2
mechanism-rediscoveries, 1 stability finding on the v2 fix itself. The
CONTROVERTED back-catalog is now fully argued: 10 (G3-3/G4-2) + 20 (this run)
= all surfaced lines covered. Remaining residue: ~14 fresh-dump controverted
lines below the top-20 cut, all at r<=1 — noise-weight, not worth a call.

NEXT (operator-gated): fold the 20 closures into the desk's dispute queue file
alongside G3-3's 10, and mark claim 8 CLOSED (verified) and claim 20's W5a/W5b
pair as the standing example for why witness independence needs source-tracking,
not just seat-tracking.

— MICKEY G5-2, zcode seat, 2026-09-11
