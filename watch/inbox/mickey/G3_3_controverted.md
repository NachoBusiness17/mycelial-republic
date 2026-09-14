# G3-3 — CONTROVERTED FEW-SHOT EXPANSION (spawned from G2-7's NEXT)

2026-09-10 · zcode seat · deepseek-chat (T2) fired once on the top-10 CONTROVERTED
lines of `watch/INVARIANT_SHEET_V2.md`, ranked by combined agreement+refutation.
Selection base: the 15 rows the sheet lists under CONTROVERTED (run found 30; report
surfaces 15). Tie-break cut: `[a=3 r=2]` "S4 (twin I4)" — lowest combined count (5).

## THE POINT

G2-7 built the disagreement detector; its NEXT asked whether a cheap model can
*argue* a disputed line better than the negation-marker classifier that found it.
Test: fire deepseek-flash on the 10 hardest-contested lines with the fixed prompt
(FOR / AGAINST / resolving evidence, no hedging), then grade — resolvable disputes
or both-sidesism?

## RUN RECEIPT (1 call, within bounds)

- model=deepseek-chat · max_tokens=6000 · temp=0.3 · finish=stop (no truncation)
- usage: 711 prompt + 1,473 completion = 2,184 tokens · latency 8.3s · pennies
- raw: `_g33_ds_raw.txt` (root scratch) · repro: `_g33_deepseek_fewshot.py`
- key read from `.env`, header use only, never echoed

## THE 10 CLAIMS (verbatim sheet lines, FOR/AGAINST/EVIDENCE from deepseek)

**1. [a=3 r=12 · combined 15]** "per family references (the SUPPORTED tri-state row above, quoting her...)" — Astra condition-arithmetic family; hardest-contested line in the corpus.
- FOR: family treated as a coherent, cross-referenced unit; enough internal consistency to be a usable classification.
- AGAINST: 12 refutations say the family label is contradicted, overbroad, or laundering unsupported subclaims — a row can be "supported" at family level while the arithmetic inside is disputed.
- RESOLVING EVIDENCE: the quoted SUPPORTED tri-state row vs the 12 negative lines, compared line-by-line — do they refute the family label itself or only members?

**2. [a=2 r=7 · combined 9]** "4. I4 falsifier re-run — A11 (same file, ledger)."
- FOR: tied to A11 in same file + ledger → traceable provenance; a recorded re-run is legitimate verification.
- AGAINST: 7v2 says the re-run did not settle it — a re-run reusing the same assumptions, ledger state, or witness seat is not independent.
- RESOLVING EVIDENCE: the A11 ledger entry — exact command, inputs, timestamp, and whether the re-run's result differed from the original.

**3. [a=2 r=7 · combined 9]** "PROMOTION SUPPORTED requires >= 2 INDEPENDENT witnesses with the second at..."
- FOR: explicit procedural gate against single-source promotion.
- AGAINST: 7 refutations = violated or disputed in practice; the line is truncated ("with the second at ...") so the threshold itself may be ambiguous; nominal independence ≠ real.
- RESOLVING EVIDENCE: the full promotion-rule text plus witness records for a disputed claim — did the second witness meet the threshold and was it independent?

**4. [a=2 r=6 · combined 8]** "Dimensions 1-5 are how ANY solution (ours, Astra's, a...) [no solution] — deck falsifier F-D1"
- FOR: dimensions framed as universal across any solution — a valid comparative framework if F-D1 tests solution-independence.
- AGAINST: 6 refutations suggest universality is contested — the dimensions may encode assumptions specific to one solution family.
- RESOLVING EVIDENCE: F-D1's definition and results — do dimensions 1-5 hold for at least one non-Astra, non-ours solution?

**5. [a=2 r=6 · combined 8]** "UNPROVEN, hash-witnessed at watch/GROUNDING_WAVE.md) is the DEMOTION..."
- FOR: demotion anchored to a hash-witnessed artifact — tamper-evident, procedurally traceable.
- AGAINST: hash-witnessing proves the text existed, not that the demotion was correct; the UNPROVEN status itself may be contested.
- RESOLVING EVIDENCE: the hash-witnessed content vs the demotion rule it triggers, checked against the affected claim's actual label history.

**6. [a=2 r=6 · combined 8]** "any SUPPORTED label the witnesses carry."
- FOR: narrow claim — if witnesses carry SUPPORTED status, the label follows the witness set, consistent with witness-based promotion.
- AGAINST: circular unless witness independence and count are specified; otherwise any witness carries SUPPORTED without meeting the >=2 rule.
- RESOLVING EVIDENCE: the witness list for a disputed SUPPORTED label — does each witness independently satisfy the promotion criteria?

**7. [a=2 r=6 · combined 8]** "| C2 | The knot store holds 21,264 knots. |"
- FOR: concrete, checkable count; verifiable directly if the store is append-only or hash-witnessed.
- AGAINST: 6v2 says wrong, stale, or disputed — a numeric claim dies to one contradictory count from the same store.
- RESOLVING EVIDENCE: a direct query or dump of the knot store — current count plus timestamp.
- (zcode note: ALREADY RESOLVED in-fleet — the DISPUTED→13,678 correction lives one line away in the sheet. The model independently named the exact resolving move the fleet actually ran. Predictive hit.)

**8. [a=3 r=4 · combined 7]** "| CAMP STATE v0 + v1, pinned verbatim | SUPPORTED — watch/ASTRA_CAMPAIGN_LOG.md |"
- FOR: verbatim pinning plus a named log is strong provenance.
- AGAINST: pinning preserves text, does not prove it correct or that v0+v1 are mutually consistent.
- RESOLVING EVIDENCE: the pinned text vs the log's refuting entries, compared for direct contradiction.

**9. [a=3 r=4 · combined 7]** "second witness auto-demotes to UNPROVEN); witnesses partitioned across seats."
- FOR: seat partitioning is a real independence mechanism against correlated witnesses.
- AGAINST: witnesses partitioned across seats but sharing a source = formal, not real, independence; auto-demotion may not be applied.
- RESOLVING EVIDENCE: seat assignment records — different seat, and did that seat have independent access to the underlying evidence?

**10. [a=3 r=4 · combined 7]** "pages unfetched; that cross-check stays UNPROVEN (scan card §4); nothing..."
- FOR: epistemically sound — no fetch, no verification, UNPROVEN is the correct label.
- AGAINST: status challenged — pages may have been fetched elsewhere, or §4 resolved by another route.
- RESOLVING EVIDENCE: the fetch log for those pages vs scan card §4 — were they fetched, and was the cross-check completed?

## GRADING — resolvable disputes or both-sidesism?

**Verdict: resolvable. 8/10 strong, 2/10 soft. Not both-sidesism.**

What earns the verdict:

1. **10/10 RESOLVING EVIDENCE entries name a specific artifact AND a specific
   comparison operation** (ledger entry vs original result; pinned text vs log rows;
   store dump + timestamp; seat records vs access independence). Nothing says
   "more research needed". Every dispute has a named closing move.
2. **The AGAINST sides deploy distinct mechanisms, not one generic doubt** — four
   recur across the set and map the fleet's actual failure modes:
   - *label inheritance* — family/row-level SUPPORTED launders member claims (1)
   - *formal vs real independence* — same assumptions, ledger, or source defeat the witness count (2, 3, 9)
   - *provenance ≠ accuracy* — pinning and hashing preserve text, never truth (5, 8)
   - *numeric claims die to one counter-count* (7)
   That taxonomy is the real product: it is a checklist for auditing ANY supported
   label in the corpus, not just these ten.
3. **Honest fragment handling**: on the two truncated lines (3, 6) it flagged the
   truncation/ambiguity as the dispute instead of inventing content.

Where it is soft:

- Claims 4 and 6 are pure fragments carrying no adjudicable content; there the
  FOR/AGAINST leans on the agree/refute counts rather than the claim — the one
  place both-sidesism genuinely threatens, and it correlates exactly with the
  sheet's weakest lines, not with the model.
- Everything resolves only against artifacts deepseek never saw. It triages and
  names the evidence; the fleet must still produce it. Zero-context role is
  arguer, never judge — which is the correct shape for a penny lane.
- Inherited noise: the sheet's refutation column is negation-marker + token-overlap
  (G2-7's own falsifier notes precision-not-recall), so some "refutations" are
  likely false positives. deepseek argued every refutation as if real; a v2 should
  tell it the counts are heuristic.

## INSTRUMENT VERDICT

**Useful — keep it.** One call, 8.3s, 2,184 tokens, zero truncation, and the
output is a dispute taxonomy + 10 audit to-dos the fleet can execute against its
own files. It converts G2-7's mechanical "contested" flag into named, checkable
closures — including one (claim 7) the fleet had already resolved the same way,
which is the cheapest possible validation that the instrument aims true.
Bound it to the CONTROVERTED shortlist only (as BOT B proposed), and prepend one
line of prompt context ("counts come from a negation-marker heuristic") to stop it
defending the classifier's noise.

NEXT: if operator GOs, run the 20 remaining surfaced CONTROVERTED lines through
the same prompt (~2 more calls, still pennies) and file the closing-evidence
checklist as the desk's dispute queue.

— MICKEY G3-3, zcode seat, 2026-09-10
