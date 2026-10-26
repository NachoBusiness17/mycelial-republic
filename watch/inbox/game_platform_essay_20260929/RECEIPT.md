# RECEIPT - ractor-essay dogfood run: the sovereign game platform (2026-09-29)

Run: watch/inbox/game_platform_essay_20260929/. Skill: ractor-essay v1 (its first end-to-end execution; the Q run formalized it, this run dogfoods it). Subject: the sovereign game platform (WoW-class world + GWAP verification backend) and what it says about AI-assisted building. Lens length calibrated to ~2,000-2,500 words per operator order, not the skill's 5k default.

## Audit trail (phase -> file -> bytes -> sha256 head)

| Phase | File | Bytes | sha256 (first 16) |
|---|---|---|---|
| 0 frame | FRAME.md | 4,778 | a3f9a9d4d37ca5c8 |
| 1 digest | DIGEST.md | 15,481 | 55cafb5fa3e0c88b |
| 2 lens 1 | LENS_ARCHITECT.md | 13,420 | 1f4f09db2a965abb |
| 2 lens 2 | LENS_MECHANIC.md | 12,489 | 9cb420a5456e7747 |
| 2 lens 3 | LENS_ECONOMIST.md | 12,137 | 7de38a921787ec8f |
| 3 grade | GRADED.md | 11,340 | fdc90717719dbc74 |
| 4 correct | (edits in all three lens files, dated notes) | +~1.4KB | post-correction hashes above |
| 5 synthesis | SYNTHESIS.md | 9,035 | 132563f2a5cbdd27 |
| 6 final | FINAL_PIECE.md | 7,726 | 86f09a79b71ad495 |
| 7 receipt | RECEIPT.md | this file | see index_events.jsonl |

Measured (wc -w, 2026-09-29): lenses 2,055 / 1,924 / 1,846 words; synthesis 1,433; final piece 1,304 words (target 1,200-1,500: in range). Em-dash count 0 in every file, verified by grep -o U+2014 after a correction pass (see honesty flags).

Ground truth read this run: docs/ref/GAME_PLATFORM_BASECAMP.md; watch/inbox/GWAP_BACKEND_RESEARCH_20260929.md; watch/inbox/game_platform_basecamp_20260929/LANES_20260929.md; watch/inbox/game_platform_basecamp_20260929/BOTSPORT_LEDGER_20260929.md; mag/wow_bones.py (header); memory/game/STATE.md; corpus/game_estate/FROM_MUD_TO_WOW_20260914.md (cold open, Part VIII, appendices by targeted grep only, per the run order); schema precedent watch/inbox/Q_OPERATION_RACTOR_20260929/DIGEST.md.

## Cost

One seat, zero subagents, zero workflow children: Phase 2 was written sequentially by the session author because this seat has no Task-agent tool and the envelope law caps workflow fan-out (see amendments). Tool calls this run: 21 (reads, writes, edits, one sed, measurement passes). Context: ~60KB of ground-truth source plus 86KB written. Token usage is an ESTIMATE, not a measurement (no meter on this seat): order 200-300k tokens on the session model. Cost in dollars: within the seat's existing subscription, $0 incremental. Wall time: one session. The skill's "one run is about one evening" held.

## Honesty flags (mandatory)

1. THE GRADER IS NOT INDEPENDENT. GRADED.md was written by the same LLM session that wrote the lenses, sequentially, with no sub-agent separation. The fabrication check was a real line-by-line reread and found real defects (all logged), but self-grading inherits its own blind spots. The skill's optional Phase 3.5 (human-blind A/B) was NOT run; no human reviewed anything.
2. Hand-written word counts appeared in lens footers (~2,310 / ~2,290 / ~2,280) and were wrong (measured 2,055 / 1,924 / 1,846). Corrected in-file with dated CORRECTION notes. The estate's own law (never trust a hand-written count) was violated by this run before it was enforced by it.
3. Em-dashes appeared in file headings and labels (5 files) while footers claimed count 0; body prose was clean. Fixed by a sed pass (spaced hyphen in headings), re-verified 0 everywhere by grep.
4. Two lenses landed below the run's 2,000-word floor (1,924 and 1,846 against a ~2,000-2,500 target). Logged, not padded.
5. Three lens claims grounded in digest-cited files rather than digest text (wow_player/wow_world ledger detail; "bot-shaped clients" phrasing); flagged by the grader as a digest-coverage gap, corrections logged in both lens files.
6. The 202/202 replay figure is carried everywhere with its PLAUSIBLE-not-re-executed caveat; the digest, all three lenses, the synthesis, and the final piece all repeat the caveat.
7. Zero fabricated numbers found across three lenses in the fabrication pass; defects found were rhetorical (invented precision once, unsourced absolutes twice, one charter miscount), all corrected with dated notes.

## Self-feed (what the next run steals)

- This DIGEST.md is the next game-platform run's Phase-1 hit: stable schema (subject, five numbered sections, measured-numbers table, source paths), ~60 path-cited numbers, FTS-findable.
- The six-tension map (GRADED.md section C) is reusable as the standing tension register for this subject; T3 (jurisdiction claimed vs hours spent, with B3-unclaimed as the tell) and T4 (federated ethics vs centralized economics, unresolvable) are the two the next run should re-check first.
- The frame's five questions and lens-to-question mapping are the template for any "what is X building and why" subject.

## SKILL AMENDMENTS (the dogfood's real product; amend, never rewrite)

1. **Phase 2 dispatch ladder is unspecified, and its default is impossible on some seats.** Friction: the skill mandates "Dispatch as Task agents at width 3"; this seat has no Task tool and workflows are envelope-capped (max_concurrency <= 3, gated), so lenses were written sequentially by one author, degrading blind divergence, and the grader inherited the author's blind spots. Amendment: add a dispatch ladder to Phase 2: (a) Task agents at width 3 where the tool exists; (b) any seat-native subagent mechanism; (c) sequential self-write as last resort, in which case GRADED.md's honesty flag must name the authorship mode and the fabrication check must run against both the digest and the cited files.
2. **No byte-verification step between writing and grading.** Friction: lens footers self-reported wrong word counts, and the em-dash claims were false until a grep pass; both survived into "finished" files because nothing checks bytes between Phase 2 and Phase 3. Amendment: add Phase 2.5 byte check: run wc -w per lens and count U+2014 per artifact; the check writes the count lines (an author-written count line is itself a defect); grade reads the verified counts.
3. **The em-dash law's scope is unstated.** Friction: body prose was clean but titles and labels used em-dashes. Amendment: the law should read "zero U+2014 anywhere in the file, headings and correction notes included, verified by grep," matching the estate's receipt discipline.
4. **Lens length is a constant in the skill but a parameter in practice.** Friction: the operator ordered 2-2.5k lenses for the dogfood; two still drifted under the floor unnoticed until after grading. Amendment: the Phase 0 frame states target length per lens (as Phase 6 already does for the final piece) and the Phase 2.5 byte check reports compliance.
5. **Digest-completeness is assumed, never enforced.** Friction: three lens claims traced to digest-cited files rather than digest text, violating "grounded ONLY in the digest." Amendment: Phase 1 law: the digest restates every load-bearing fact the frame's lenses will lean on; any lens claim sourced beyond digest text carries an inline [beyond-digest: path] marker, and the grader treats unmarked beyond-digest grounding as a fabrication-adjacent defect.
6. **Frame-to-lens traceability lives only in FRAME.md.** Friction: FRAME.md maps each lens to its frame questions, but no lens cites the mapping and nothing verifies derivation. Amendment: each lens header names the frame questions it answers; the grader checks the mapping one-to-one before scoring power.
7. **CORRECTION note format is unspecified.** Friction: Phase 4 was improvised as inline bracketed notes. Amendment: standardize: [CORRECTION YYYY-MM-DD, grader defect N: what was wrong; what replaced it], inline at the defect site.
8. **index_events.jsonl registration has no template.** Friction: the schema had to be reverse-engineered from the file's tail. Amendment: carry the entry template in Phase 7 (ts / op register / file / sha256 / class receipt / purpose).

Passed as-written (no amendment): Phase 0 socratic frame (lenses derived, not defaulted); the >=5 digest numbers per lens quota (all lenses cite 25+); receipt-before-speech filing (every phase filed the moment it landed); tension-map-as-synthesis-skeleton one-to-one (T1-T6 all resolved or named unresolvable); the 1301 law on the final piece; digest schema stability against the Q run's precedent.

## Filing

Registered in watch/inbox/index_events.jsonl after this file lands. Em-dash count in this file: 0 (verified by grep before filing).
