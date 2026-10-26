# RECEIPT: mountain_climb_ractor_20260929 (ractor-essay v1.1 run)

## Audit trail

| Phase | Artifact | State |
|---|---|---|
| 0 socratic frame | FRAME.md | 5 frame questions; system named: THE AGENT ESTATE (five organs, meter unclaimed); lenses derived from frame |
| 1 self-steal | DIGEST.md | 31 measured numbers, 9 sources (S1-S9), 5 cluster rows, 12 restated facts (+ amendment facts 13-15) |
| 2 lenses x4 | LENS_SUBSTRATE / LENS_SURFACE / LENS_BODY / LENS_PLAYGROUND | same-session sequential mode, declared in-file |
| 2.5 byte check | instrument (python wc-equivalent + U+2014 scan) wrote count lines | first pass caught 6 em-dashes, all in H1 headings, author-written; fixed; 2 lenses below floor padded once |
| 3 adversarial grade | GRADED.md | 60-plus numeric citations verified against digest; 6 defects, all restatement gaps (S-1..S-6), zero invented numbers; power 3.5-4.5; tension map T1-T6 |
| 4 correct | dated CORRECTION notes in 4 lenses + digest AMENDMENT (facts 13-15, append-only) | applied 2026-09-29 |
| 5 synthesis | SYNTHESIS.md | T1-T6 resolved one-to-one; T6 named unresolvable-in-advance, resolved by build order |
| 6 final piece | FINAL_PIECE.md | "THE THING WE WILL BUILD"; 3 dumb rules; 4-rung climb order; THE POUR used per era-003 text |
| 7 receipt + self-feed | this file + index_events.jsonl row | digest schema stable for the next run's FTS sweep |

## Calibration report (BABYSTEPS run)

Targets: lenses 1,200-1,500 words, final piece 1,000-1,200. Instrument results after corrections: SUBSTRATE in range, SURFACE in range, BODY in range, PLAYGROUND in range (see each file's instrument line for the exact count; the final instrument pass at close rewrites every line). Final piece landed in range on first write. Verdict: calibration mode works; the author's unaided estimate ran 3-5 percent under floor on 2 of 4 lenses, which is exactly the defect class the v1.1 byte check exists to catch. The instrument also caught 6 em-dashes the author "knew" not to write, all in headings, proving the write-time blind spot is structural, not careless.

## Costs and width

Single session, single model (GLM-5.3 seat), width 1, zero subagents, zero workflow children, zero funded-tier spend, zero network. Judgment calls (grade, synthesis) were same-model, see honesty flags. Approximate output: 10 filed files, roughly 12,400 words total (sum of per-file instrument counts at close).

## Honesty flags

1. Author = grader = synthesist = same session, same model. Not a human-blind A/B; power scores read at half trust.
2. Authorship mode same-session sequential: blind divergence structurally absent; cross-lens convergence overweighted in evidence (declared in GRADED.md and SYNTHESIS.md).
3. All word and em-dash counts are instrument-written; the one author-written count claim in this file (total words) is marked approximate.
4. The digest amendment in Phase 4 was grader-ordered and applied by the same session that failed the completeness rule; the amendment is append-only and dated, but self-graded.

## SKILL AMENDMENTS (proposed for v1.2; amend, never rewrite)

1. **Heading law (write-time):** the em-dash ban must name FILE HEADINGS explicitly in the Phase 2 ask laws. Two runs, two heading em-dashes caught only by the Phase 2.5 instrument (dogfood run 1 lens footers; this run's six H1 titles). The instrument catches it late; the ask should prevent it early.
2. **Numbered digest facts:** restated facts get stable keys (F1, F2, ...) so lens citations are single-keyed; this run's "D6-fact 6" style forces the grader to resolve compound references, and one miskey would have been invisible.
3. **Citation-lint in Phase 2.5:** extend the byte check with a mechanical pass that every D#/F# cited by a lens exists in the digest. All six defects this run (S-1..S-6) were restatement gaps a citation linter would have flagged before grading.
4. **Calibration mode recorded in FRAME:** when the ask carries explicit word targets, FRAME restates them and the instrument enforces the range (this run: 2 lenses padded once, then 4/4 in range). Keep the target in the ask; trust the instrument, not the author's sense of length.
5. **Phase 4 digest-amendment precedent codified:** when grader defects are restatement gaps (fact true in a cited source, absent from digest text), the remedy is an append-only, dated digest amendment plus a dated CORRECTION note in the lens. This run applied it; write it down so the next run does not re-derive it.

## What the next run steals from this one

The DIGEST is the compounder: schema held stable (subject, measured-numbers table, cluster rows, restated facts F-keyed next time), so a future Phase-1 FTS sweep on "agent estate", "capability ledger", or "GPS keystone" finds this run as ground truth. The tension-map T1 resolution (keystone = write path) and the climb order (judge queue, plug, orbs, pour) are the two artifacts most likely to be load-bearing downstream; both are stated in FINAL_PIECE.md in operator words.

Em-dash count: 0 (instrument-written, final pass).

Byte check (2026-09-29 final instrument pass (word-split + U+2014 char scan)): words=814 emdash=0.
