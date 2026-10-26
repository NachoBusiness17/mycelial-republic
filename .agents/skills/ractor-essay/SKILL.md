---
name: ractor-essay
description: Run the ractor-essay pipeline — self-steal the estate's own corpus first, digest it with measured numbers, fan N grounded 5k-word lens essays, adversarially grade them, synthesize the strongest parts, then write the interpreted public piece. Use when the operator wants a deep research essay on a subject "ractored out" through multiple lenses, or says "self steal then ractor it."
---

# THE RACTOR-ESSAY PIPELINE

A repeatable research-essay pattern demonstrated on the Q operation (2026-09-29, `watch/inbox/Q_OPERATION_RACTOR_20260929/`) and formalized from it. Seven phases plus a frame. Every phase files a receipt; a window that dies mid-pipeline loses nothing.

## Phase 0 — SOCRATIC FRAME (added v1; the Q run skipped this)

Tease the ask out before choosing lenses. 3-5 questions of the form "when you say X, do you mean A or B?" — each question's answer changes the lens selection or the essay's spine. Derive the lenses FROM the ask; never default to a fixed trio. Output: the questions + chosen lenses + the voice brief (whose voices woven subtly, what tone), filed as FRAME.md.

## Phase 1 — SELF-STEAL (the highest-payoff phase; never skip)

Mine the estate's own record first: catalog/FTS, `watch/inbox/` receipts, `corpus/`, `memory/`, prior ractor runs. Operating assumption: **the estate already ran the research project once.** Output: `DIGEST.md` — the ground-truth contract, built from measured numbers (counts, dates, DOIs, hashes, byte sizes), every entry path-cited. Laws: the digest contains no speculation; speculation is the lenses' job.

## Phase 2 — LENSES

N essays (default 3), ~5k words each, each grounded ONLY in the digest. Dispatch ladder (v1.1 amendment, from dogfood run 1): (a) PREFERRED: Task agents at width 3 (envelope law); (b) FALLBACK: sequential same-author writing — permitted but GRADED.md MUST declare "authorship mode: same-session sequential" prominently, and the synthesis must weight the blind-divergence loss; (c) NEVER a wide workflow fan-out on accounts where workflow children die on 429. The laws ride INSIDE each ask: no fabrications (every claim traceable to the digest or a cited file), em-dash 0, tri-state claims (Supported/Disputed/Unproven), blind divergence (never read another lens before writing yours). File each lens as a receipt the moment it lands — **receipt before speech** (a killed window loses nothing).

## Phase 2.5 — BYTE CHECK (v1.1 amendment, from dogfood run 1)

Before grading: a mechanical pass writes the lens metadata itself — `wc -w` for word counts and a `U+2014` grep for the em-dash count — and inserts/replaces the count lines in each file. An author-written count line is itself a defect class (dogfood run 1's lens footers were all wrong by 5-12% while claiming verification). Never trust a hand-written count; the instrument writes the numbers. (v1.3 amendment, from the 2026-10-01 hermes-burn runs): the em-dash law binds the content channel and every assembled deliverable; a raw reasoning-channel dump is exempt by physics (the channel mints dashes mid-thought and no ask can police it), so the ASSEMBLED pass is the enforcement surface: assemblies must re-sweep clean before filing, and raw dumps are never cited as compliant artifacts.

## Phase 3 — ADVERSARIAL GRADE

One grader agent, separate from the lenses: (a) check every essay against the digest for fabrication — including beyond-digest grounding (any load-bearing claim tracing to a digest-CITED FILE rather than digest TEXT is a defect; v1.1 amendment: the digest must restate every load-bearing fact, so the lenses never need to open the sources), (b) score power, (c) map the cross-lens tensions the synthesis must resolve. Output: `GRADED.md`. Honesty flag is mandatory in the receipt: an LLM grader is not the human-blind A/B; say so, and declare the authorship mode from Phase 2.

## Phase 4 — CORRECT

Fix defects in-file with dated `CORRECTION:` notes. Never silently edit a graded essay.

## Phase 5 — SYNTHESIZE

Merge the grader's strongest-parts extraction. The synthesis's section skeleton = the grader's tension map, one-to-one: each mapped tension must be resolved or named as unresolvable. Output: `SYNTHESIS.md`.

## Phase 6 — THE INTERPRETED PIECE

The public layer, per the voice brief: whose voices woven subtly (Campbell, Jung, Bernays, vonnegut-style are house favorites), target length stated up front, sensitive subjects handled by the 1301 law (state the verdict, not the vocabulary; the receipts carry the clinical detail). Output: `FINAL_PIECE.md`.

## Phase 7 — RECEIPT AND SELF-FEED

`RECEIPT.md`: audit trail, token/width cost, honesty flags, what the next run should steal from this one. Register everything in `watch/inbox/index_events.jsonl`. **The pattern is a corpus compounder: this run's DIGEST is the next run's self-steal hit.** Keep the digest schema stable (subject, measured-numbers table, source paths) so future Phase-1 sweeps find it via FTS.

## Costs

Lens essays are the bulk: 3 × 5k words on free/cheap lanes is pennies. Judgment calls (grader, synthesis) are the only funded-tier moments. One run ≈ one evening.

## Improvement ledger (amend, never rewrite)

- v1 (2026-09-29): formalized from the Q operation run. Seeded improvements: P0 socratic frame added (lenses derived from the ask); digest measured-numbers quota (every lens must cite ≥5 digest numbers, grader-enforced); human-blind A/B offered as optional Phase 3.5; tension-map = synthesis skeleton, one-to-one; 1301 law applied to the final piece; pattern self-feed via stable digest schema.
- v1.1 (2026-09-29, dogfood run 1 — game-platform subject): three amendments applied from RECEIPT.md of watch/inbox/game_platform_essay_20260929/: (1) Phase 2 dispatch ladder (Task-width-3 preferred, same-session sequential permitted with declared authorship mode in GRADED.md, wide workflow fan-out forbidden); (2) Phase 2.5 byte check added (wc + U+2014 grep writes count lines; author-written counts are a defect class — run 1's footers were wrong by 5-12% while claiming verification); (3) Phase 3 digest-completeness rule (digest restates every load-bearing fact; beyond-digest grounding is a grader defect class). Unapplied seeded items remain: human-blind A/B, digest quota grader enforcement wiring.
- v1.2 (2026-09-29, Mickey17 W3o lane): Phase 2 lens asks adopt the house LANE_ASK_TEMPLATE v2 fields (`docs/ref/LANE_ASK_TEMPLATE.md`, receipt `watch/inbox/W3O_LANE_TEMPLATE.md`, from the S7 steal): every dispatched lens ask now carries an EFFORT BUDGET (max tool calls + max cycles; stop-and-file at the cap) and a NON-OVERLAP declaration naming what sibling lenses already cover, making blind divergence structural instead of behavioral; the ask also states the report cap and the death-receipt clause. Unapplied seeded items remain: human-blind A/B, digest quota grader enforcement wiring.
- v1.3 (2026-10-01, hermes-burn ractor turns T1W1_RACTOR + WINDOW2_RACTOR): two run shapes banked. T1W1_RACTOR (distillation ractor over 4 premium stranger-audit verdicts): 9 law rows + 14 tickets + 16 to-verify rows, every quote fixed-string byte-verified (57 candidates, 5 misses dropped); honored Phase 2.5 (0 em-dashes, instrument-written), Phase 1 moment law (chain pinned 8777 rows at distillation moment while live was already 8784, which is the moment law working, not violated), Phase 3 separation (D1/D2/D3 as declared graders). WINDOW2_RACTOR (window-close ractor): 5 law rows (W2-L1..L5) + the ELI12 register + a doors list. Amendments applied from these runs: (1) Phase 2.5 raw-channel exemption codified (assemblies are the em-dash enforcement surface; raw reasoning dumps exempt by physics); (2) run-shape vocabulary added to this ledger (distillation ractor vs window-close ractor) so future Phase-1 sweeps know both are self-steal hits. Defect this amendment closes: both runs minted 14 law rows total and initially fed none back (the ledger amendment happened only after DAY1_SKILLS_DOGFOOD flagged the Phase 7 gap); Phase 7 self-feed is same-sitting, not next-day debt. Unapplied seeded items remain: human-blind A/B, digest quota grader enforcement wiring.
- v1.4 (2026-10-18, tarot_july2024_ractor run): two amendments. (1) IMAGE-BLIND LENSES: lenses that Read the subject photo themselves (6-call cap, own identifications with confidence tags) produce a genuine inter-rater convergence datum - the grader's card-ID table measured certainty tracking printed text/number on the card face; adopt for any visual-subject run. (2) FUSE OWNERS AT PRE-REGISTRATION: pre-registered dated fuses must name their registered owner (scheduled task / instrument command) at pre-registration time, not after; this run registered its fuses to MagBackupBrainDaily same-sitting only because the grader flagged the lapse risk. Unapplied seeded items remain: human-blind A/B, digest quota grader enforcement wiring.
- (next run amends here)
