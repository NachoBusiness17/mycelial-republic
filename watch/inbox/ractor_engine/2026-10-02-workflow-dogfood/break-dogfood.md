# BREAK-DOGFOOD: hostile second pass on dogfood.md (2026-10-04)

Target: `watch/inbox/ractor_engine/2026-10-02-workflow-dogfood/dogfood.md` (the dogfood lens report, 10,147 bytes, mtime 10-04 03:18). Every evidence cite in its findings and blind spots was re-checked against estate bytes this session. Nothing was taken from the lens on faith; every number below was re-derived here or marked OWED.

## Instruments run this session (no substitutes)

- Full journal census: python script over all 101 `dwfrun-*.mjs` payloads in `.zcode/workflow-runs/` (dir holds 104 entries = 101 dwfrun + 2 dwfeval + `.gitignore`), parsing each embedded payload JSON (`json.JSONDecoder().raw_decode` after `export const payload = `) and counting family-distinctive strings per payload. Output: per-payload mtime (UTC), size, body-shape head, marker counts.
- Payload keys census: every payload has keys exactly `['args','lowered','maxOldSpaceSizeMb']`. There is no workflow-name or label field anywhere in the journal. The lens's blind spot 2 is structurally true.
- Draft ledger: listing of `.zcode/workflow-drafts/` (63 entries) with mtimes, matched against payload mtimes.
- Targeted reads: `mag/percolator.py` lines 23-27, 87-93, 544-557; `memory/percolator/candidates.jsonl` (row count, promoted values, mtime); `watch/inbox/frontier_olm_*/percolator_candidates.jsonl` row counts; `memory/workflows/REGISTRY.jsonl` (75 rows, per-script census); `.zcode/workflow-drafts/RETIRED.md` (full read); `watch/inbox/spiking_wide/energy-frontier.md` and `event-driven-resonance.md` heads; `watch/inbox/gala_20260925/fillball-1001_RECEIPT.md` (full read); `watch/inbox/gala_20260925/` and `watch/inbox/ractor_engine/` dir listings with mtimes; saved-script profile of all 18 `.dwf.ts` files in `.zcode/workflows/`; unified diffs of the 5 game-dig veins; global archive check of `~/.zcode/workflows` and `~/.zcode/workflow-runs`.
- Not run: `ListWorkflowRuns` (returned `workflow_introspection_unavailable` in this session too, same capability gap the lens hit). Run completion status per fire remains unverifiable from inside a child session. All fire counts here are payload-launch counts, not completed-run counts.

Timezone note: the lens quoted local times without saying so; every wall-clock claim below is given in UTC with the EDT equivalence where it matters.

## Verdicts on the lens findings

### Finding 1 (three engines wearing twelve badges): WEAKENED

Byte-true: `watch/inbox/gala_20260925/` holds exactly 26 subdirs (lens: "26 battery subdirs") and 18 `*_RECEIPT.md` files; `watch/inbox/ractor_engine/` holds exactly 6 dirs spanning 10-02..10-04 (lens: "6 receipt dirs in 3 days"); `frontier_olm_*` receipt dirs number exactly 5; 101 dwfrun payloads confirmed; `fillball-1001_RECEIPT.md` does carry `by_division {"B": 7}` (lines 15 and 24, not the literal header); `spiking_wide/energy-frontier.md` line 1 (not line 3) carries "gala spiking-wide, energy lane"; `event-driven-resonance.md:3` confirms; localfirst-steal (10-01 09:06Z = 05:06 EDT), librarian-expedition (10-02 00:00Z = Oct 1 20:00 EDT), salon-mine (10-02 01:08Z = Oct 1 21:08 EDT) subdirs confirmed.

Byte-false or un-reproducible:
1. "olm-mine 13 fires": my body-shape census reads 9 olm-mine fires (3 on 09-29 writing `frontier_olm_20260928`: dwfrun-279d66b4, -aa9969b0, -c41194a8; plus 6 slug-arg daily burns: -a5abb24e, -618ca877, -22ad421a, -bc564831, -1759540b, -3cec1e3a). 15 payloads mention `frontier_olm` but 6 of those are gala/meta runs referencing it. 13 matches neither count under my instrument.
2. "the-gala ~20 fires": 30 payloads carry the gala chassis (`GALA_ROOT` + `rung` probes, 09-29 through 10-03). The lens undercounted its own headline family by a third.
3. "five of the twelve did their only proving work as gala divisions": the five (drop-dig, wide-dig, salon-mine, librarian-expedition, fill-ball) each fired under their OWN named draft with their OWN receipt dirs (Localfirst-steal-wave, Spiking-wide-dig, Salon-mine-20deep/-offpeak/-vault-stragglers, Librarian-gathering-expedition, Fill-ball-one-sittings/-amend). The gala_ prefix is shared chassis infrastructure hardcoded in the saved scripts, not shared ownership: `drop-dig.dwf.ts`, `fill-ball.dwf.ts`, `librarian-expedition.dwf.ts`, `salon-mine.dwf.ts`, `wide-dig.dwf.ts`, `the-gala.dwf.ts` each carry `GALA_ROOT` x5 and `gala_20260925` x4 in their own source. The receipts self-brand as gala divisions (division B), so the lens's textual reading was receipt-true and archive-blind at the same time.

Survives: the three-engine composition (olm daily burn, gala chassis, ractor swarm) is confirmed and strengthened. Also confirmed: the retry-draft inference (`.zcode/workflow-drafts/OLM-mine-daily-burn-1003-retry.dwf.ts` exists, 10-03 23:30, matching dwfrun-3cec1e3a 10-03 23:30:43Z).

### Finding 2 (olm-mine to percolator loop filed but lapsed): CONFIRMED, byte-exact, CONVERGENT

Every cite reproduced:
- `mag/percolator.py:23-27` and `mag/percolator.py:87-93` document the `--candidates` ingest exactly as quoted ("mine digests ... had ZERO consumers (grep mag/ tools/ tests/ = 0 hits)", fillball-1001, GAP_REGISTER rank 6).
- `mag/percolator.py:544-557` is the `ingest_candidates` function, verbatim.
- `memory/percolator/candidates.jsonl`: 16 rows, 0 rows with promoted=true, mtime 2026-10-02T04:17:43Z (lens said 04:17Z).
- `wc -l` equivalent: `frontier_olm_2026-10-02/percolator_candidates.jsonl` = 9 rows, `frontier_olm_2026-10-03` = 5 rows, both after the ingest moment: 14 lapsed rows confirmed.
- Source split confirmed exactly: 20260928 = 5 rows, 2026-09-30 = 6 rows, 2026-10-01 = 5 rows (5+6+5 = 16).

One reframe the lens missed: zero-of-16 promoted is the documented design, not a failure signal. `mag/percolator.py:25-27` and `:554-557` state promotion never happens at ingestion; the gate stays alpha-budget and promotion happens only through the standing percolate() path. Whether percolate() ever promoted a candidate-sourced row was NOT CHECKED here (OWED-1). The real defect is exactly what the lens said: the two newest burns' 14 rows were never ingested. The move is feasible as stated: the olm-mine fold step is `folder.ask` based (`.zcode/workflows/olm-mine.dwf.ts:412-477`), so one added line telling the folder to run the ingest command works, and `mag/percolator.py:551-552` guarantees rerun idempotency.

### Finding 3 (six of the twelve never fired twice as themselves): WEAKENED, core broken by the draft ledger

Byte-true: REGISTRY rows for the-50 confirmed exactly (`.zcode/workflows/the-50.dwf.ts`: 2026-09-26T05:30:44Z FAIL, 05:32:53Z FAIL, 05:36:09Z PASS in `memory/workflows/REGISTRY.jsonl`); dwfrun-2656afad (2026-09-19) is the only the-50 body payload; dwfrun-15738edf (09-25) the only tree-doctrine payload; `watch/inbox/gap_analysis_20261001` is the only gap_analysis_* dir; `.zcode/workflow-drafts/RETIRED.md` retires `THE-50--reset-day-fullsend.dwf.ts` verbatim as "older/smaller than the saved the-50 ... same program"; the-gala's saved description verbatim says "amended from mickey17-v2 lineage" (`.zcode/workflows/the-gala.dwf.ts:1-3`).

Byte-false: the lens never opened `.zcode/workflow-drafts/`, which maps named drafts to launch payloads 1:1 by mtime. Resolved fire counts:
- gap-analysis: 4 fires, not "at most one" (Gap-analysis-100m 10-01 22:00 = dwfrun-dfaaf421; unnamed amend 10-03 21:18 = dwfrun-125a2278; Gap-analysis-amend 10-03 22:38 = dwfrun-e3d51dd6; Gap-analysis-evening 10-04 02:21 = dwfrun-53ba7956; all four carry the saved script's `a15-rollup` string).
- fill-ball: 2 fires (Fill-ball-one-sittings 10-02 03:51 = dwfrun-99126b18; Fill-ball-amend 10-03 22:38 = dwfrun-6176a7ae).
- salon-mine: 5 payloads across 4 named drafts (Salon-mine-20deep x2 payloads 10-02 01:07/01:09, Salon-mine-offpeak 14:42, Salon-vault-offpeak 14:45, Salon-vault-stragglers 14:53).
- librarian-expedition: 2 payloads on 1 draft (10-01 22:54:56 + 22:57:52), 1 receipt.
- wide-dig: "no verified fire as its own saved script at all" is FALSE. Spiking-wide-dig draft (10-01 18:14) = dwfrun-3f5f5738 (10-01 18:14:03Z, the only SpikingBrain-carrying gala payload) = `watch/inbox/gala_20260925/spiking-wide/` dir (10-01 18:15) + receipt (10-01 19:36); the saved description "Proven on SpikingBrain 2026-10-01: 8/8 lanes" (`wide-dig.dwf.ts:8-9`) matches this fire. One verified fire, not zero.

Only the-50 (1 fire) and tree-doctrine-dig (1 fire) survive the never-fired-twice claim. The headline also says "Six" while enumerating seven families, an internal inconsistency. The move is half moot: gap-analysis already has 4 fires and fill-ball 2; re-firing them to "earn two fires" is already-satisfied work. Strike-the-50 stays defensible; the 4th REGISTRY row (2026-10-04T02:34:03Z PASS, digest 84cecee2c6d3) shows the gate was just re-run on it, which is a promotion signal, not a fire.

### Finding 4 (game-dig veins are near-clones, one evening of fires): CONFIRMED, byte-exact, CONVERGENT

- Diffs run this session (difflib unified, vs `game-dig-coop-social.dwf.ts`, 168 lines): creature-farming 26 changed, horror-maze 27, liveops-seasonal 27, roguelike-runs 25. Lens said "25-27 changed lines of ~168": exact.
- All 34 game-dig payloads (GAMES_BRIEFS reads) fall 2026-09-26 22:22:38Z through 2026-09-27 05:36:37Z UTC, which is 18:22 through 01:36 EDT: the lens's window matches under EDT, a timezone it never named (minor defect, bytes right).
- `game-mechanics-deep-dig.dwf.ts` is 161 lines (splitlines count) taking `briefs_path` + `vein_slug` args (2 occurrences each in source): confirmed. The ask's copy of this finding truncates mid-word ("taking briefs_path + vein_"), so the verdict covers the recoverable portion only.

## What the lens missed (additions)

1. THE DRAFT LEDGER. `.zcode/workflow-drafts/` holds 63 named drafts whose mtimes match launch payloads to the minute (examples: OLM-mine-daily-burn-1003.dwf.ts 10-03 14:01 = dwfrun-1759540b 14:01:57Z; the -retry variant 23:30 = dwfrun-3cec1e3a 23:30:43Z; Salon-mine-20deep 10-02 01:07 = dwfrun-7128afa9 01:07:29Z; Spiking-wide-dig 10-01 18:14 = dwfrun-3f5f5738 18:14:03Z; Gap-analysis-100m 10-01 22:00 = dwfrun-dfaaf421 22:00:28Z; Fill-ball-amend 10-03 22:38 = dwfrun-6176a7ae 22:38:56Z; Ractor-dogfood-workflows 10-04 02:21 = dwfrun-ed1dbbae 02:21:43Z, the run this session executes inside). This converts the lens's string-marker inference into named-run attribution and is the single fact that breaks finding 3. Falsifier: a systematic >2-minute skew between draft mtimes and payload mtimes across the census would collapse the mapping. Move: have `tools/workflow_gate.py` stamp the draft name into each future run receipt, 15 minutes.
2. THE ABSENCE CLAIM THAT WASN'T. `watch/inbox/salon_mine/` (10-02 16:07: RESEARCH_BRIEF.md + 19 m*.md transcripts) and `watch/inbox/librarian_exp/` (10-01 23:53: inventory.md, cited-missing.md, foundational-gaps.md, gathering-log.md) both exist. The lens claimed these folders "do not exist (ls grep this session)" because it globbed `salon_mine_*` / `librarian_exp_*` with a trailing-date shape; the real names are bare. A quantifier-law instance: the absence claim named a pattern, not the ground truth. Move: none needed beyond correcting the record.
3. THE 02:33-02:34Z GATE WAVE. `memory/workflows/REGISTRY.jsonl` re-registered all 12 saved scripts in a 19-second window early 10-04 (olm-mine 02:33:47Z, gap-analysis 02:33:48Z, fill-ball 02:33:49Z, ractor-engine 02:33:51Z, salon-mine 02:33:53Z, librarian-expedition 02:33:55Z, wide-dig 02:33:58Z, drop-dig 02:34:00Z, the-gala 02:34:01Z, mickey17-v2 02:34:02Z, the-50 02:34:03Z, tree-doctrine-dig 02:34:06Z), immediately after this dogfood run launched (02:21). These rows are artifacts of the dogfood run itself; any future REGISTRY citation must date-scope. ractor-engine.dwf.ts and the-gala.dwf.ts are the most-gated scripts (13 rows each).
4. MUSIC-CUT: GATED, NEVER FIRED. `music-cut.dwf.ts` has one gate row (2026-10-03T21:56:30Z PASS) and zero payload matches by body probe (no standalone OWED WALTZ/audio-dna pipeline payload among the 101; gala payloads carry owed-waltz lane TEXT only). Also: the fleet on disk is 18 saved scripts, not 12 (the topic's 12 plus 5 game-dig veins, game-mechanics-deep-dig, music-cut). The lens's instrument note counted 19 files including the `.mimosa` entry; its finding set never returned to the extra 6.
5. RETIRED.md CONTRADICTS THE JOURNAL. `.zcode/workflow-drafts/RETIRED.md` (09-27 03:10) says `ractor_panel_20260926.dwf.ts` "the draft never fired", yet dwfrun-fde62465 (09-27 00:11Z) and dwfrun-e12efd2d (09-27 06:47Z) carry its ROOT (`watch/inbox/ractor_panel_20260926`), and REGISTRY holds ractor-panel-judgment-burn rows 09-27 00:06/00:07 plus ractor-panel-repair 06:46. Either two payloads fired a different script to the same ROOT or the retirement note is wrong. Either way the ractor program has 09-27 ancestry the lens's "3 days" window missed. Falsifier: an honest write-up in the panel receipts naming which script actually launched.
6. AN UNTIMELY CANDIDATES FILE. `watch/inbox/frontier_olm_2026-09-30/percolator_candidates.jsonl` has mtime 10-02 04:10Z, seven minutes before the 04:17:43Z ingest, though its burn fired 09-30. A late fold, a touch, or a copy at ingest time; unresolved here. OWED-2: diff that file's rows against candidates.jsonl to see which of the 16 ingested rows came from it.
7. THE 11 DRAFT-ERA 09-28 RUNS RESOLVED. The lens hedged their family attribution; the draft ledger names all 11 (flash50, wide37, deep-mining, mickey17-wave3, burn48, firehose, firehose2, mirror-mine, wave4, stealth-wide, mcp-grind), each a one-off board-declaring burn shape matching no saved script. None of the 12; the hedge can close.

## Corrected census (instrument: full-payload body-shape census, 101 payloads, moment 2026-10-04)

- olm-mine: 9 body fires (3 on 09-29 + 6 daily), 5 receipt dirs. Lens said 13.
- the-gala chassis: 30 fires 09-29..10-03, 26 subdirs, 18 receipts, 2 subdirs with no receipt (salon-mine 10-02 01:08, build-it-all 10-03 21:28). Lens said ~20.
- ractor-engine: 7-9 fires 10-02..10-04 (6 with the saved lens/moonshots/slug/topic args) + 2 panel ancestors 09-27, 6 receipt dirs. Lens's dir count exact, ancestry short.
- game-dig veins: 34 fires in one 7-hour window. Exact match.
- mickey17-v2: 2 proper fires (09-25, 10-03). gap-analysis: 4 (borrows the mickey17 fold chassis, `gap-analysis.dwf.ts` carries mickey17 x6 in source). fill-ball: 2. salon-mine: 5 payloads / 4 named drafts. librarian-expedition: 2 payloads / 1 receipt. wide-dig: 1. drop-dig: 1. the-50: 1. tree-doctrine-dig: 1. music-cut: 0.

## Minimum viable fleet (the topic question, evidence answer)

Keep as standing engines: olm-mine (daily frontier, self-ingest fix from finding 2), ractor-engine (the swarm; every dogfood pass including this one rides it), the-gala (the owed-work battery; 30 fires in 5 days). Keep as on-demand codifications that already earned their badges: mickey17-v2, gap-analysis, fill-ball, salon-mine, wide-dig, drop-dig, librarian-expedition. Strike or archive: the-50 (1 fire, superseded program, RETIRED.md already calls the draft "same program"), tree-doctrine-dig (1 fire; keep only as the doctrine-dig template), music-cut (gated, never fired). Minimum viable = 3 engines + 7 on-demand + 2 templates = 12 scripts of the 18 on disk, with the 6 non-topic scripts (5 veins + deep-dig template) already consolidated by design.

Laws honored: no em-dashes; every claim above cites a path or a command run this session; unverifiable items are OWED-1 (whether percolate() ever promoted a candidate-sourced invariant) and OWED-2 (the 04:10 candidates-file anomaly); no subprocess was spawned by this pass, so the CREATE_NO_WINDOW law had no occasion to apply.
