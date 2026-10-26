# DOGFOOD LENS: the 12 saved workflows, racted (2026-10-03)

Lens: dogfood (organ mapper). Topic: ractor the 12 saved workflows (olm-mine, gap-analysis, fill-ball, ractor-engine, salon-mine, librarian-expedition, wide-dig, drop-dig, the-gala, mickey17-v2, the-50, tree-doctrine-dig): composition, overlap, theater, never-fired-twice, minimum viable fleet.

## Instruments run this session (no substitutes)

1. ListSavedWorkflows: 19 saved project-scope workflows (the topic's 12, plus 5 game-dig veins, game-mechanics-deep-dig, music-cut). Files confirmed on disk at `.zcode/workflows/` (19 `.dwf.ts` files, `ls` output this session).
2. `.zcode/workflow-runs/`: 103 files (101 `dwfrun-*.mjs` + 2 `dwfeval-*.mjs`), mtimes 2026-09-19 through 2026-10-03. Each dwfrun file embeds the full lowered script payload; there is no label field, so I fingerprinted payloads by family-unique strings across three grep passes (the first pass had a case-sensitivity confound on `gravedigger`, corrected in pass three; noted because the intermediate numbers were wrong).
3. `watch/inbox/` receipt-folder census + header reads: `gala_20260925/` (26 subdirs), `frontier_olm_*` (5), `gap_analysis_20261001` (1), `spiking_wide/`, `ractor_engine/` (6 subdirs), `localfirst_memory_landscape_signals.jsonl`.
4. `memory/workflows/REGISTRY.jsonl`: 75 gate rows, grouped by script (venv python, this session).
5. `mag/percolator.py` read at lines 20-50, 80-100, 500-560 + `memory/percolator/candidates.jsonl` row census.
6. Cross-reference grep across all 19 saved scripts + `diff` of the 5 game-dig vein files.
7. NOT RUN: ListWorkflowRuns / GetWorkflowRun (this session lacks workflow introspection; the tool returned `workflow_introspection_unavailable`). Run STATUS per fire (completed vs errored) is therefore UNVERIFIED; the census counts launched runs, not successful ones. Scoped claim: all run-journal numbers below are the project-workspace journal only.

## Census (fires by family, from the dwfrun journal mtimes)

| family | fires | span | receipts |
|---|---|---|---|
| game-dig veins | 34 | all on 09-26 18:22 to 09-27 01:36 | gala archive + wheel spec |
| the-gala family | ~20 | 09-25 to 10-03 | 26 subdirs under `gala_20260925/` |
| olm-mine | 13 | 09-29 to 10-03 (daily) | 5 `frontier_olm_*` dirs |
| gap/fill/gala entangled | 8 | 10-01 to 10-03 | 1 `gap_analysis_20261001`, `fillball-1001` |
| mickey17-v2 | 6 | 09-25, 10-01, 10-03 | `mickey/` + run specs |
| ractor-engine | 5 to 6 | 10-02 01:49 onward | 6 dirs under `ractor_engine/` |
| music-cut | 3 | 10-01, 10-03 | lyric + music receipts |
| the-50 | 1 | 09-19 | `THE_50_PROGRAM_20260918.md` |
| tree-doctrine-dig | 1 | 09-25 | `TREE_DOCTRINE_*_20260925.md` |
| wide-dig / drop-dig / salon-mine / librarian-expedition | 1 each (as saved: 0 verified for wide-dig) | 09-28 / 10-01 | see finding 1 |

## Finding 1: the fleet is three engines wearing twelve badges

The run journal and the receipts' own headers show that five of the twelve "workflows" did their only proving work inside the-gala's division machinery. `watch/inbox/spiking_wide/energy-frontier.md` line 3 self-describes as "gala spiking-wide, energy lane" and `event-driven-resonance.md` line 3 as "gala_20260925 spiking-wide, division B lane": wide-dig's claimed SpikingBrain proof (its saved description says "Proven on SpikingBrain 2026-10-01: 8/8 lanes") rode the gala engine. Same pattern: `watch/inbox/gala_20260925/fillball-1001_RECEIPT.md` header reads `by_division: {"B": 7}` (fill-ball = gala B lanes); `localfirst-steal` (Oct 1 05:06) is drop-dig's proof vehicle; `librarian-expedition` (Oct 1 20:00) and `salon-mine` (Oct 1 21:08) subdirs carry those workflows' only receipts, inside the gala archive rather than the `watch/inbox/salon_mine_<slug>/` and `watch/inbox/librarian_exp_<slug>/` paths their saved descriptions name (neither folder exists; verified by `ls watch/inbox | grep`, this session). The 10-01 "proof day" was one mega-battery riding gala + drafts; the saved workflows are post-hoc codifications of lanes that already ran.

Falsifier: a dwfrun payload matching the saved wide-dig/drop-dig/salon-mine/librarian-expedition script body on a second date, or a receipt dir in those workflows' own `<family>_<slug>` shape.
Move (one sitting): fire each of the four 10-01 codifications once standalone so they earn their badges, or amend their descriptions to name the gala chassis honestly. Cost: one ballroom evening, zero new code.

## Finding 2: the mine-to-percolator loop is filed but lapsed (my jacket, byte-backed)

`mag/percolator.py:23-27` and `mag/percolator.py:87-93` document the `--candidates` ingest (built by fillball-1001, 2026-10-01, GAP_REGISTER rank 6) exactly because "mine digests ... had ZERO consumers". The ingest function exists (`mag/percolator.py:544-557`). But the review-pass file `memory/percolator/candidates.jsonl` holds 16 rows, all `promoted: False`, mtime 2026-10-02T04:17Z, sourced only from the 09-28, 09-30 and 10-01 burns (16 rows = 5+6+5, matches). The 10-02 burn's 9 rows and the 10-03 burn's 5 rows (`watch/inbox/frontier_olm_2026-10-02/percolator_candidates.jsonl`, `..._2026-10-03/...`, line counts run this session) were never ingested. Zero candidates have ever promoted. The loop was wired on 10-01, fired once, and lapsed within a day.

Falsifier: a candidates.jsonl mtime after 10-02T04:17Z, or any row with promoted=true.
Move (one sitting, ~20 min): append one ingest line to olm-mine's fold step (`.zcode/workflows/olm-mine.dwf.ts`) so every future burn self-ingests, then run `mag/percolator.py --candidates watch/inbox/frontier_olm_*/percolator_candidates.jsonl` once now to absorb the 14 lapsed rows.

## Finding 3: never fired twice, and one never fired at all

As saved workflows: the-50 fired once (dwfrun-2656afad, 09-19) and its gate history is two FAILs then a PASS (`memory/workflows/REGISTRY.jsonl` rows 2026-09-26T05:30:44Z FAIL, 05:32:53Z FAIL, 05:36:09Z PASS). tree-doctrine-dig fired once (09-25, dwfrun-15738edf). wide-dig has no verified fire as its own saved script at all (finding 1). gap-analysis, fill-ball, salon-mine, librarian-expedition, drop-dig each have at most one self-shaped receipt (`gap_analysis_20261001` is the only folder of that shape in watch/inbox; verified this session). The estate's own Q7 sweep already reached the same verdict class for drafts: `.zcode/workflow-drafts/RETIRED.md` retires `THE-50--reset-day-fullsend.dwf.ts` as "same program" as the saved the-50, and the-gala's saved description says it is "amended from mickey17-v2 lineage".

Falsifier: a second receipt dir in any of these workflows' own shape, or a second dated dwfrun payload matching the saved body.
Move (one sitting): strike the-50 from the standing fleet (its program lives in the-gala), keep tree-doctrine-dig as a doctrine template, and re-fire the gap-analysis-to-fill-ball pair on the current burst (their own doctrine: weekly or per-burst) so the pair has two fires before it is called standing.

## Finding 4: theater and duplication census

The five game-dig vein saves are 85% byte-twins: `diff game-dig-coop-social.dwf.ts game-dig-{creature-farming,horror-maze,liveops-seasonal,roguelike-runs}.dwf.ts` reads 25-27 changed lines out of ~168 each (run this session; the twins differ mainly in description and lane lists). All 34 game-dig fires landed inside one 36-hour burst (09-26 18:22 to 09-27 01:36) and the family has been dark since, while `game-mechanics-deep-dig.dwf.ts` (161 lines) already parameterizes the identical shape (args: briefs_path, vein_slug). Six saved workflows where one engine plus five brief files would do. The 09-28 draft-era runs (11 dwfrun files, empty or weak signatures: ractorswarm, model-garden, firehose class) are one-shot drafts that never promoted and never re-fired.

Falsifier: a post-09-27 game-dig fire, or a structural difference between the vein saves beyond lane lists and prose.
Move (one sitting): retire the five vein saves per the Q7 precedent (amend-not-delete, keep bytes), keep `game-mechanics-deep-dig` as the single game engine.

## Minimum viable fleet (5 members)

1. olm-mine: the only daily cadence (13 fires, 5 receipt dirs). Keep.
2. the-gala: the battery chassis everything else actually rides (26 battery subdirs). Keep.
3. ractor-engine: the standing audit lens-set, 6 receipts in 3 days, the newest organ. Keep.
4. gap-analysis + fill-ball as ONE composite loop (the register IS the lane table; their saved descriptions say so and the XREF grep confirms fill-ball references gap-analysis and ractor-engine). Keep as a pair.
5. One dig primitive: wide-dig and drop-dig overlap heavily (both tri-state a drop against primaries with multi-lane lanes plus a synthesis and estate mapping; wide-dig = one subject, drop-dig = multi-system brief). Merge or keep drop-dig (the newer, citation-resolution-law shape) and demote wide-dig to a lane template inside it.

Retire: the-50, tree-doctrine-dig (template, not fleet), 5 game-dig veins. Watch: mickey17-v2 still fires for paced 50-wide burns (6 fires) but is the-gala's parent; fold it into gala when the next burn can ride gala divisions instead.

## Blind spots (honest)

- Run status per fire is unverified (no introspection this session): some of the 13 olm-mine fires may have errored; the draft `OLM-mine-daily-burn-1003-retry.dwf.ts` implies at least one retry.
- Family attribution for the 11 draft-era 09-28 runs and the exact gala-vs-fill-ball split on several 10-01/10-02 runs is string-marker inference, not label-backed; I flagged every place the markers collided (`gala_` archives both families).
- I did not read all 12 saved scripts line-by-line; composition claims rest on the cross-reference grep, receipt headers, and diff evidence named above.
- Global-scope workflows (`~/.zcode/workflows`) and other workspaces' journals were not censused; if another workspace fires these, my never-fired-twice counts undercount.
- I could not run ListWorkflowRuns (capability gap), so "which compose into mega-workflows" is answered from receipts and payload signatures, not from the run tree's parentage fields.

## CORRECTION ADDENDUM (2026-10-04, after hostile second pass)

The second pass verdicted findings 1 and 3 weakened. Re-verification this session accepts the critique's numbers and adds the byte layer that explains them. Every number below was re-run here, not copied from the critique.

Corrections accepted (re-verified by my own commands):
1. olm-mine is 9 body fires, not 13-14. Instrument: `grep -q "sweep miner" && grep -q "confirmer"` (both unique to the saved olm-mine body, 3x each per token count) over all payloads: 279d66b4, aa9969b0, c41194a8 (09-29 x3), a5abb24e, 618ca877 (09-30 x2), 22ad421a (10-01), bc564831 (10-02), 1759540b, 3cec1e3a (10-03 x2). My earlier "frontier_olm_" marker over-counted because mega-runs (Ouroboros-meta 4bacae38, Burn-48h-synthesis 3a094ea8) mention the mine's folder.
2. gap-analysis has 4 body fires, not 1. Instrument: `grep -q "a15" && grep -q "rollup"`: dfaaf421 (10-01 18:00 EDT, Gap-analysis-100m draft, exact mtime pair), 125a2278 (10-03 17:18), e3d51dd6 (10-03 18:38, Gap-analysis-amend draft pair), 53ba7956 (10-03 22:21 EDT = 10-04 02:21 UTC, Gap-analysis-evening draft pair). My mickey17-v2 attribution of these was wrong (the gap asks reference the mickey17 burst they audit).
3. fill-ball has 2 mission fires: 99126b18 (10-01 23:51, Fill-ball-one-sittings stub, exact mtime pair) and 6176a7ae (10-03 18:38, Fill-ball-amend stub pair). salon-mine has 5 payloads across 4 stubs (7128afa9 + rerun 1cd89983 at 21:07/21:09, 619d47ec 10:42, dbb3f798 10:45, cda8c867 10:53). librarian-expedition has 2 (c48601ef 18:54 draft pair + 5b23d7bb 18:57). wide-dig DID fire as its own named mission: Spiking-wide-dig stub 10-01 14:14 = dwfrun-3f5f5738, exact mtime pair. My "no verified fire" claim for wide-dig was false and is withdrawn.
4. watch/inbox/salon_mine/ and watch/inbox/librarian_exp/ exist as bare-named dirs; my absence claim globbed salon_mine_*/librarian_exp_* and missed them. Withdrawn.

The byte layer my re-check adds (beyond the critique):
- The nine "own named drafts" (Fill-ball-one-sittings, Salon-mine-20deep, Salon-vault-offpeak, Salon-vault-stragglers, Spiking-wide-dig, Localfirst-steal-wave, Librarian-gathering-expedition, Build-it-all, Hitler-dig-full-dogfood) are md5-identical to each other AND to the saved the-gala: all hash 8bf79d38ca3c3a6755a423fa33f088c9, and workflows/the-gala.dwf.ts hashes to the same. md5sum run this session.
- So "fired under their OWN named draft" and "ran the gala engine" are the same fact at byte level: the stubs ARE the-gala's bytes launched with different slug/lanes args. GALA_ROOT appears in exactly 30 of the 101 payloads and "owed waltz" in the same 30 (grep -l | wc -l = 30 both instruments). GALA_ROOT is the shared archive root, hardcoded at .zcode/workflows/fill-ball.dwf.ts:88 (`GALA_ROOT = ESTATE + "/watch/inbox/gala_20260925"`).
- The five workflows diverged from the-gala only at SAVE time: saved bodies are 22685 to 23137 bytes vs the-gala 22814 (fill-ball 22685, wide-dig 22901, drop-dig 22955, librarian-expedition 22956, salon-mine 23137). Fill-ball-amend.dwf.ts == saved fill-ball.dwf.ts (e9ef5d99). Salon-mine-offpeak.dwf.ts == saved salon-mine.dwf.ts (81b1b08c), whose run 619d47ec (10-02 10:42) is therefore the one verified fire of a saved diverged body in this whole family.
- Saved-body fires are another layer from mission fires: neither fill-ball-attributed run contains the saved body's "founder receipt" string (grep = 0 hits on 99126b18 and 6176a7ae; the saved body has it 1x), so the saved fill-ball body has zero verified fires; what fired were the-gala bytes under fill-ball names.

Corrected headline: the fleet is one battery engine (the-gala bytes, 30 of 101 fires) plus a small set of genuinely distinct bodies: olm-mine (9 fires), gap-analysis a15-rollup (4 fires), ractor-engine (6 receipt dirs, 10-02 onward), mickey17 lineage, music-cut, and the singles. The five "sibling workflows" are post-hoc specializations of the battery engine, diverged by 100-300 saved bytes, with 0-1 verified fires of their diverged bodies between them.
