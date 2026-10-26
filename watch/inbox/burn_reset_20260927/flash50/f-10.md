# f-10 - TODO/FIXME/HACK/XXX census of the Mag estate (2026-09-28)

Census of every case-sensitive `TODO` / `FIXME` / `HACK` / `XXX` marker line in the
repo working tree, with per-hit git-blame age and a still-relevant verdict.
Mirror: this file is byte-identical to `todo-census.md` in the same directory.

## Headline numbers

- **753 marker lines in 441 tracked files** carry at least one
  case-sensitive marker (instrument: bytes-level `git grep -n -I -E "\b(TODO|FIXME|HACK|XXX)\b"`,
  scan artifacts written 2026-09-28 18:41:43 EDT).
- Per-marker line counts (a line can carry several markers): TODO 528, FIXME 37, HACK 34, XXX 193.
- Case-insensitive context total: 4,649 lines (lowercase prose todo/hack/xxx NOT itemized in
  this census; instrument `git grep -n -I -i -E` same moment).
- **True actionable debt tier: 13 hits in 6 files** (tier A below: 2 code stubs, 5 pre-push
  flip markers, 1 open license check, 4 audit-proposal gate TODOs, 1 ratchet baseline meta row).
- Everything else is detector vocabulary, vendored upstream code, diagram labels, data-index
  rows, book Roman numerals, receipts and model-output tapes.
- Blamed age: min 0d, max 55d, median 14d, mean 10.0d over 737 blameable hits; repo first commit 2026-08-04 (55d of history, so 55d is the ceiling).

## Method (every number below came from these commands)

1. `git grep -n -I -E "\b(TODO|FIXME|HACK|XXX)\b"` over all tracked files, run via subprocess
   with bytes-level output (split on `\n` only; a first attempt using Python str.splitlines
   fragmented binary lines on unicode boundaries like \x85 and mis-parsed 58 fragments - the
   bytes-level rerun parses 753/753 with 0 unparsed).
2. `git ls-files --others --exclude-standard` (190 untracked files) scanned with the same
   regex in-process (189 hits in 13 files, section below).
3. Age: `git blame --porcelain` per affected file (441 files, 8-way parallel), indexed by
   final line number; ages relative to 2026-09-28.
4. Per-marker counts: `git grep -n -I [-i] -E "\bMARKER\b"` per marker.
5. Relevance: each tier-A/B/C/D hit read in context (Read/sed on the file, commands noted
   per verdict); tier-E classes verified by sampling one matched line per class from the scan
   TSV.

## Instrument caveats (read before comparing these numbers)

- **The tree is live.** The same grep piped through bash returned 741 lines at 17:46 EDT, the
  census scan snapshot (753) was written 18:41:43 EDT, and a rerun at ~18:52 returned 757: sibling
  flash50 lanes landed 19 commits between 17:54 and 18:51 (git log --since 17:30). All counts
  in this file are the pinned ~18:05-18:15 snapshot; tracked files grew 47,405 (17:46) to
  47,528 (scan) during the same window. Never difference counts taken at different moments.
- **Blame age is landing age, not authoring age.** The f-21 skill census (read in the commit
  log this session) documents commit d575bc168 (2026-09-14) as a mass-add checkpoint: files
  authored earlier (e.g. docs/ref/MESH_PIPELINE_20260903.md, self-dated 09-03) blame to 09-14,
  reading 14d instead of 25d. Treat 09-14-dated rows as understatements.
- **16 rows have no age**: dashboard/data/ESTATE_INDEX.jsonl and its watch/ESTATE_INDEX twin
  (1.29 GB each, byte-identical twins) - git blame fails on them with `fatal: unable to
  generate diff`, both on the working tree and pinned at HEAD c1c0136cd. They are generated
  index rows whose indexed paths contain TODO; age not obtainable, stated as such.
- 2 rows are binary false positives inside Bartle PDF copies (tier F).

## Tier rollup

| Tier | Meaning | Hits | With blame age | Median age d |
|---|---|---|---|---|
| A - actionable estate debt (judged individually) | | 13 | 13 | 6 |
| B - vendored upstream code/docs TODOs | | 8 | 8 | 2.0 |
| C - marker used as detector vocab / fixture / label | | 17 | 17 | 1 |
| D - diagram node labels | | 2 | 2 | 55.0 |
| E - data: books, tapes, receipts, indexes, archives | | 711 | 695 | 14 |
| F - binary false positives | | 2 | 2 | 12.0 |

## Tier A - actionable debt, judged individually (13 hits, 6 files)

| file:line | marker(s) | landed | age d | author | verdict | evidence |
|---|---|---|---|---|---|---|
| audit_prep/cell_operator_gates_MAP_output.md:32 | TODO | 2026-09-14 | 14 | Codex | OPEN (partial supersession) | proposed mag/gate_dispatch.py never created (ls 2026-09-28: no such file); the operator_go gate later landed as tools/operator_go.py (B2-425 reader); no spend/keys/one_stop gate functions found in repo |
| audit_prep/cell_operator_gates_MAP_output.md:33 | TODO | 2026-09-14 | 14 | Codex | OPEN (partial supersession) | same as line 32 |
| audit_prep/cell_operator_gates_MAP_output.md:34 | TODO | 2026-09-14 | 14 | Codex | OPEN (partial supersession) | same as line 32 |
| audit_prep/cell_operator_gates_MAP_output.md:35 | TODO | 2026-09-14 | 14 | Codex | OPEN (partial supersession) | same as line 32 |
| configs/violation_baseline.json:3621 | TODO,FIXME | 2026-09-24 | 4 | Codex | ACTIVE META | this IS the ratchet's registered debt row: rule todo-undated, file mag/max_distill.py, accepted 2026-09-24 by operator:bootstrap; read at baseline lines 3620-3626 |
| docs/ref/MESH_PIPELINE_20260903.md:28 | TODO | 2026-09-14 | 14 | Codex | STILL RELEVANT | TRELLIS license verdict still Unproven in the doc; 2026-09-28 repo grep for TRELLIS+license finds only this TODO, no verdict recorded anywhere |
| githooks/pre-push:17 | TODO | 2026-09-26 | 2 | Codex | STILL RELEVANT | description_pin gate still WARN-ONLY (|| true at githooks/pre-push:21); flip to exit 1 is a pending operator decision |
| githooks/pre-push:38 | TODO | 2026-09-26 | 2 | Codex | STILL RELEVANT | freshness gate still WARN-ONLY (|| true tail); flip pending operator decision |
| githooks/pre-push:66 | TODO | 2026-09-26 | 2 | Codex | STILL RELEVANT | census patrol exit-1 STALE flip still pending (B2-277 landed the exit-2 block only; exit-1 stays WARN) |
| githooks/pre-push:137 | TODO | 2026-09-26 | 2 | Codex | STILL RELEVANT | caption_ledger_verify still WARN-ONLY; flip pending operator decision |
| githooks/pre-push:200 | TODO | 2026-09-26 | 2 | Codex | STILL RELEVANT | refold_gate still WARN-ONLY; flip pending operator decision |
| scripts/light_replay_falsifier.py:35 | TODO | 2026-09-14 | 14 | Codex | STILL RELEVANT | stale-light guard_check stub; file read in full 2026-09-28: no guard_check anywhere in it, docstring itself says STUBBED not implemented (conf-floor + VARIANT_GUARD also open) |
| tools/ox_heartbeat.py:17 | TODO | 2026-09-22 | 6 | Codex | STILL RELEVANT | all-fail ledger alerting not implemented; file read in full 2026-09-28: main() only probes + appends rows; comment says intentionally comment-only per ask A5 |

## Tier B - vendored upstream markers (8 hits)

- `docs/ref/zai_docs_mirror/api-reference/video/generate-video.md:166` [XXX] landed 2026-09-14 (14d, Codex): VENDORED, vendor docs - z.ai docs mirror; base64 image placeholder in vendor example
- `docs/ref/zai_docs_mirror/openapi.json:2168` [XXX] landed 2026-09-14 (14d, Codex): VENDORED, vendor docs - z.ai docs mirror; base64 image placeholder in vendor example
- `predictions_acnh.js:357` [TODO] landed 2026-09-27 (1d, Codex): VENDORED, upstream TODO - Animal Crossing turnip-pattern predictor code (PATTERN/PROBABILITY_MATRIX structure, header read 1-30); upstream algorithm question about fudge-factor probability; landed 2026-09-27 in commit 383fed94f
- `predictions_acnh.js:408` [TODO] landed 2026-09-27 (1d, Codex): VENDORED, upstream TODO - same upstream question, repeated per pattern branch
- `predictions_acnh.js:461` [TODO] landed 2026-09-27 (1d, Codex): VENDORED, upstream TODO - same upstream question, repeated per pattern branch
- `predictions_acnh.js:500` [TODO] landed 2026-09-27 (1d, Codex): VENDORED, upstream TODO - same upstream question, repeated per pattern branch
- `tools/bin/globalTypes.d.luau:6104` [TODO] landed 2026-09-25 (3d, Codex): VENDORED, upstream TODO - Roblox global type definitions dump; upstream unfinished API enum
- `tools/bin/globalTypes.d.luau:17930` [TODO] landed 2026-09-25 (3d, Codex): VENDORED, upstream TODO - Roblox global type definitions dump; upstream TODO color key

## Tier C - detector vocabulary, fixtures and labels (17 hits)

- `mag/canvas_bridge.py:312` [TODO] landed 2026-08-04 (55d, Nacho): NOT DEBT - kanban parser maps dashboard JS const TODO block to the Open section (context read 305-320)
- `mag/cross_version.py:537` [TODO] landed 2026-08-08 (51d, Codex): NOT DEBT - CLI status label string: prints x (TODO) for hypothesis modules whose files do not exist (context read 530-542)
- `mag/game_observer.py:42` [TODO] landed 2026-08-19 (40d, Codex): NOT DEBT - placeholder-detector regex vocab: TODO marks fallback text the writer leaked (context read 36-48)
- `mag/ghost.py:980` [TODO] landed 2026-08-19 (40d, Codex): NOT DEBT - section header naming the operator todo-attention feature; the feature is implemented right below at 984-1001 (read)
- `mag/max_distill.py:89` [TODO] landed 2026-09-14 (14d, Codex): NOT DEBT (but registered) - vocab token in the fork-state evaluability check (context read 80-95); the same file is the ratchet's single registered todo-undated debt row
- `mag/prompt_lance.py:25` [TODO,FIXME] landed 2026-09-27 (1d, Codex): NOT DEBT - this file IS the estate's prompt-leak detector; TODO/FIXME listed as leakage shapes it scans for (docstring read 1-30)
- `mag/prompt_lance.py:115` [TODO] landed 2026-09-27 (1d, Codex): NOT DEBT - detector pattern (re.compile TODO marker) in prompt_lance
- `mag/prompt_lance.py:116` [FIXME] landed 2026-09-27 (1d, Codex): NOT DEBT - detector pattern (FIXME marker) in prompt_lance
- `mag/prompt_lance.py:117` [XXX] landed 2026-09-27 (1d, Codex): NOT DEBT - detector pattern (XXX marker) in prompt_lance
- `tests/test_canvas_bridge.py:15` [TODO] landed 2026-08-04 (55d, Nacho): NOT DEBT - test fixture const named TODO
- `tests/test_prompt_lance.py:22` [TODO] landed 2026-09-27 (1d, Codex): NOT DEBT - test fixture feeding the leak detector
- `tests/test_prompt_lance.py:42` [TODO] landed 2026-09-27 (1d, Codex): NOT DEBT - test assertion on TODO leakage detection
- `tests/test_prompt_lance.py:148` [TODO] landed 2026-09-27 (1d, Codex): NOT DEBT - test fixture TODO x
- `tests/test_prompt_lance.py:192` [TODO] landed 2026-09-27 (1d, Codex): NOT DEBT - test fixture TODO wire the key
- `tools/queue_close.py:19` [XXX] landed 2026-09-27 (1d, Codex): NOT DEBT - docstring usage example placeholder Q-XXX
- `tools/violation_ratchet.py:195` [TODO,FIXME] landed 2026-09-24 (4d, Codex): NOT DEBT - the todo-undated RULE implementation itself (context read)
- `tools/violation_ratchet.py:196` [TODO,FIXME] landed 2026-09-24 (4d, Codex): NOT DEBT - todo-undated rule: records findings with rule name todo-undated

## Tier D - diagram labels (2 hits)

- `docs/ref/MAG_v2_PLAN.md:350` landed 2026-08-04 (55d): NOT DEBT - mermaid architecture-diagram node id named TODO (the queue/todo.md node), Aug-04 v2 plan artifact, historical
- `docs/ref/MAG_v2_PLAN.md:377` landed 2026-08-04 (55d): NOT DEBT - mermaid edge TODO --> AR, same diagram

## Tier F - binary false positives (2 hits)

- `memory/corpus/ai_canon/bartle_designing_virtual_worlds.pdf:3229` - matched byte stream inside a binary artifact (PDF), not a comment
- `memory/corpus/game_design_docs/bartle_designing_virtual_worlds_2003.pdf:3229` - matched byte stream inside a binary artifact (PDF), not a comment

## Tier E - data surfaces (711 hits)

Class rollup inside tier E (verified by sampling one matched line per class):
- VENDOR CORPUS: 326 hits
- RECEIPT / TAPE / PROSE: 201 hits
- DATA INDEX ROW: 96 hits
- BOOK TEXT: 80 hits
- ARCHIVED SNAPSHOT: 8 hits

Samples that fix each class (from the scan TSV, one per class):

- BOOK TEXT: `canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:1163` - `XXX. Knight Kadosh` (chapter heading); `scholem_ss.txt:26847` - `XXX, 414-16.` (volume citation)
- VENDOR CORPUS: `memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3d3yRs.fragment:1` - shadertoy JSON descriptor; `memory/corpus/ractors/cs_classics/texts/pg621.txt:19021` - `Op. cit., Letter XXX.`
- DATA INDEX ROW: `catalog/catalog.jsonl:8460` - row whose indexed path is `azerothcore-wow/deps/libmpq/TODO` (a mined third-party TODO file); ESTATE_INDEX rows index libmpq/TODO + TODO.md paths
- RECEIPT / TAPE / PROSE: `watch/inbox/desktop_bundle_20260901/wow.txt:7420` - a receipt quoting an `rg` command line containing `TODO`; `watch/inbox/union_fullsend_20260917/DAY_PACK.md:1015` - a receipt quoting another codebase's `# TODO: adapter...`; `memory/trajectory/steps.jsonl:2676` - model-output tape row; `memory/burns/LEDGER.jsonl:104` - ledger row gist; `dashboard/static/trails/research.jsonl:125` - trail event
- ARCHIVED SNAPSHOT: dist_audit/nacho_business_audit_20260912T214050Z/ carries frozen copies of the same markers (e.g. its mag/ghost.py:990 vs live mag/ghost.py:980 - the live file moved since the 09-12 snapshot)

Full tier-E per-hit table (file, line, marker, landed, age d, class):

| file:line | marker | landed | age d | class |
|---|---|---|---|---|
| .tmp_dig/ketubot111a_soncino.html:843 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| .tmp_dig/mead_vol2.txt:15626 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| .tmp_dig/sanhedrin97_soncino.html:129 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| .tmp_dig/sanhedrin97_soncino.html:143 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| boe003.html:251 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| boe003.html:268 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/crowley_magick_aba.txt:1559 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/crowley_magick_aba.txt:1925 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/crowley_magick_aba.txt:2377 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/crowley_magick_aba.txt:2743 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/crowley_magick_aba.txt:3203 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/crowley_magick_aba.txt:3569 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/crowley_magick_aba.txt:6410 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/crowley_magick_aba.txt:7971 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/crowley_magick_aba.txt:9540 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:1163 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:2844 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:5932 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:10346 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:15630 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:17449 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:19124 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:20877 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:22846 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:24851 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:26760 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:29005 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:31109 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:33438 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:35821 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:38372 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:40011 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:41698 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:45539 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:49284 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:51610 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:53543 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:55224 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:57313 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:59780 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:64737 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:72109 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:78530 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:80157 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:98623 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:99536 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:100560 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:100595 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:100621 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:100694 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:100730 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:100734 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:100988 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:100992 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:101254 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:101258 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| canon/riddler_corpus/esoteric_wave/open_copies/pike_morals_dogma.txt:102825 | XXX | 2026-09-19 | 9 | BOOK TEXT |
| catalog/catalog.jsonl:8460 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:31889 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:32152 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:35244 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:39736 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:39826 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:39916 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:40005 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:40095 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:40185 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:40275 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:40365 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:40455 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:40545 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:40635 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:40724 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:40814 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:40904 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:40994 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:41083 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:41173 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:41263 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:41353 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:41443 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:41532 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:41621 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:41710 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:41799 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:41889 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:41978 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:42067 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:42156 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:42245 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:42334 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:42424 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:42514 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:42603 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:42693 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:42783 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:42873 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:42963 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:43053 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:43143 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:43233 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:43323 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:43413 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:43502 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:43592 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:43681 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:43771 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:43861 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:43951 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:44040 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:44130 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:44219 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:44309 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:44399 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:44489 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:44578 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:350669 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:350957 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:351167 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:358495 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:360172 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:364036 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:387915 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:437588 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:480440 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:483505 | TODO | 2026-09-27 | 1 | DATA INDEX ROW |
| catalog/catalog.jsonl:565329 | TODO | 2026-09-28 | 0 | DATA INDEX ROW |
| catalog/catalog.jsonl:568985 | TODO | 2026-09-28 | 0 | DATA INDEX ROW |
| catalog/catalog.jsonl:571118 | TODO | 2026-09-28 | 0 | DATA INDEX ROW |
| catalog/tags.jsonl:8460 | TODO | 2026-09-28 | 0 | DATA INDEX ROW |
| catalog/tags.jsonl:31889 | TODO | 2026-09-28 | 0 | DATA INDEX ROW |
| catalog/tags.jsonl:350669 | TODO | 2026-09-28 | 0 | DATA INDEX ROW |
| catalog/tags.jsonl:351167 | TODO | 2026-09-28 | 0 | DATA INDEX ROW |
| catalog/tags.jsonl:358495 | TODO | 2026-09-28 | 0 | DATA INDEX ROW |
| catalog/tags.jsonl:387915 | TODO | 2026-09-28 | 0 | DATA INDEX ROW |
| catalog/tags.jsonl:480440 | TODO | 2026-09-28 | 0 | DATA INDEX ROW |
| catalog/tags.jsonl:483505 | TODO | 2026-09-28 | 0 | DATA INDEX ROW |
| corpus/steal/MASTER_MICKEY17_V2.md:87 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/steal/ZCODE_RATCHET_LANDED_20260924.md:25 | TODO,FIXME | 2026-09-24 | 4 | RECEIPT / TAPE / PROSE |
| corpus/steal/ZCODE_RATCHET_LANDED_20260924.md:41 | TODO | 2026-09-24 | 4 | RECEIPT / TAPE / PROSE |
| corpus/steal/ZCODE_RATCHET_LANDED_20260924.md:63 | TODO | 2026-09-24 | 4 | RECEIPT / TAPE / PROSE |
| corpus/steal/ZCODE_RATCHET_WAVE2_20260925.md:31 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/telegram/MrPool_Q.jsonl:946 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| corpus/telegram/MrPool_Q.jsonl:957 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| corpus/telegram/MrPool_Q.jsonl:1283 | HACK | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| corpus/telegram/MrPool_Q.jsonl:1824 | HACK | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe012.htm:251 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe012.htm:268 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe012.txt:5 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe013.htm:251 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe013.htm:268 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe013.txt:5 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe014.htm:251 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe014.htm:268 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe014.txt:5 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe015.htm:251 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe015.htm:268 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe015.txt:5 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe016.htm:251 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe016.htm:268 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe016.txt:5 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe017.htm:251 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe017.htm:268 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe017.txt:5 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe019.htm:251 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe019.htm:268 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/tmp_enoch/boe019.txt:5 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| corpus/training_materials/tesla/colorado_springs_notes_1899_1900_djvu.txt:19363 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| corpus/training_materials/tesla/colorado_springs_notes_1899_1900_djvu.txt:22548 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| corpus/training_materials/tesla/martin_inventions_researches_writings_1894_gutenberg_39272.txt:274 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| corpus/training_materials/tesla/martin_inventions_researches_writings_1894_gutenberg_39272.txt:13572 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| dashboard-deploy/static/trails/research.jsonl:125 | TODO | 2026-09-25 | 3 | ARCHIVED SNAPSHOT |
| dashboard/data/ESTATE_INDEX.jsonl:360151 | TODO | NA | NA | DATA INDEX ROW |
| dashboard/data/ESTATE_INDEX.jsonl:469841 | TODO | NA | NA | DATA INDEX ROW |
| dashboard/data/ESTATE_INDEX.jsonl:485905 | TODO | NA | NA | DATA INDEX ROW |
| dashboard/data/ESTATE_INDEX.jsonl:493566 | TODO | NA | NA | DATA INDEX ROW |
| dashboard/data/ESTATE_INDEX.jsonl:2303192 | TODO | NA | NA | DATA INDEX ROW |
| dashboard/data/ESTATE_INDEX.jsonl:2319889 | TODO | NA | NA | DATA INDEX ROW |
| dashboard/data/ESTATE_INDEX.jsonl:2320713 | TODO | NA | NA | DATA INDEX ROW |
| dashboard/data/ESTATE_INDEX.jsonl:2359821 | TODO | NA | NA | DATA INDEX ROW |
| dashboard/static/trails/research.jsonl:125 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/trails/research.jsonl:125 | TODO | 2026-09-14 | 14 | ARCHIVED SNAPSHOT |
| dist_audit/nacho_business_audit_20260912T214050Z/mag/canvas_bridge.py:312 | TODO | 2026-09-14 | 14 | ARCHIVED SNAPSHOT |
| dist_audit/nacho_business_audit_20260912T214050Z/mag/cross_version.py:537 | TODO | 2026-09-14 | 14 | ARCHIVED SNAPSHOT |
| dist_audit/nacho_business_audit_20260912T214050Z/mag/game_observer.py:42 | TODO | 2026-09-14 | 14 | ARCHIVED SNAPSHOT |
| dist_audit/nacho_business_audit_20260912T214050Z/mag/ghost.py:990 | TODO | 2026-09-14 | 14 | ARCHIVED SNAPSHOT |
| dist_audit/nacho_business_audit_20260912T214050Z/mag/max_distill.py:89 | TODO | 2026-09-14 | 14 | ARCHIVED SNAPSHOT |
| dist_audit/nacho_business_audit_20260912T214050Z/scripts/light_replay_falsifier.py:35 | TODO | 2026-09-14 | 14 | ARCHIVED SNAPSHOT |
| enoch_charles.txt:1730 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| handoff/OX_MEGA3_t0134.json:8 | TODO | 2026-08-25 | 34 | RECEIPT / TAPE / PROSE |
| handoff/OX_MEGA3_t0311.json:8 | TODO | 2026-08-25 | 34 | RECEIPT / TAPE / PROSE |
| handoff/OX_MEGA_short_reasoning_full_code.json:7 | TODO | 2026-08-25 | 34 | RECEIPT / TAPE / PROSE |
| handoff/OX_MEGA_short_reasoning_full_code.json:8 | TODO | 2026-08-25 | 34 | RECEIPT / TAPE / PROSE |
| handoff/OX_RESIDENT_res-1606e394a2-serialize.json:10 | TODO | 2026-08-25 | 34 | RECEIPT / TAPE / PROSE |
| handoff/OX_RESIDENT_res-d9cc4530c8-serialize.json:9 | TODO | 2026-08-25 | 34 | RECEIPT / TAPE / PROSE |
| je5.txt:31474 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| je5.txt:38741 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| mathers_ku.txt:10746 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| memory/audit_20260926/lane10_adversarial.json:63 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| memory/audit_20260926/lane3_gates.json:138 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| memory/audit_20260926/lane3_gates.json:149 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| memory/audit_20260926/lane3_gates.json:162 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| memory/audit_20260926/w2l2_push.json:210 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| memory/audit_20260926/w2l2_push.json:277 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| memory/burns/LEDGER.jsonl:104 | TODO | 2026-09-26 | 2 | RECEIPT / TAPE / PROSE |
| memory/burns/LEDGER.jsonl:154 | TODO | 2026-09-26 | 2 | RECEIPT / TAPE / PROSE |
| memory/burns/LEDGER.jsonl:392 | TODO | 2026-09-26 | 2 | RECEIPT / TAPE / PROSE |
| memory/continuity/seat_memory_20260927/flash-lane-burn-20260926.md:69 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| memory/corpus/ai_canon/chapters/dlb_rnn.html:5675 | XXX | 2026-09-16 | 12 | VENDOR CORPUS |
| memory/corpus/augmentation_canon/engelbart_mother_of_all_demos_1968.html:91 | TODO | 2026-09-16 | 12 | VENDOR CORPUS |
| memory/corpus/esoteric_canon/falkener_games_ancient_and_oriental_1892.txt:502 | XXX | 2026-09-16 | 12 | VENDOR CORPUS |
| memory/corpus/esoteric_canon/falkener_games_ancient_and_oriental_1892.txt:30045 | XXX | 2026-09-16 | 12 | VENDOR CORPUS |
| memory/corpus/game_design_docs/nethack_guidebook_367.txt:5752 | HACK | 2026-09-16 | 12 | VENDOR CORPUS |
| memory/corpus/game_design_docs/nethack_guidebook_367.txt:5756 | HACK | 2026-09-16 | 12 | VENDOR CORPUS |
| memory/corpus/ractors/crowd_media/texts/pg77019.txt:9058 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/cs_classics/texts/pg16287.txt:4940 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/cs_classics/texts/pg1998.txt:129 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/cs_classics/texts/pg1998.txt:4614 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/cs_classics/texts/pg1998.txt:14368 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/cs_classics/texts/pg2084.txt:4702 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/cs_classics/texts/pg2084.txt:6930 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/cs_classics/texts/pg2084.txt:6931 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/cs_classics/texts/pg56852.txt:402 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/cs_classics/texts/pg621.txt:19021 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/esoterica/texts/pg17368.txt:6466 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/esoterica/texts/pg42055.txt:123 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/esoterica/texts/pg42055.txt:4669 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/esoterica/texts/pg56880.txt:71 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/esoterica/texts/pg56880.txt:11216 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/jung/texts/pg48225.txt:4423 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/scifi_pd/texts/pg1322.txt:14302 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/scifi_pd/texts/pg25525.txt:31120 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/steiner/texts/pg3261.txt:7153 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/voltaire/texts/pg1998.txt:123 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/voltaire/texts/pg1998.txt:4608 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/voltaire/texts/pg1998.txt:14362 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/voltaire/texts/pg76.txt:150 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/voltaire/texts/pg76.txt:8435 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/weird_prophetic/texts/pg103.txt:70 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/weird_prophetic/texts/pg103.txt:6365 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/weird_prophetic/texts/pg1640.txt:6368 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/weird_prophetic/texts/pg2885.txt:7680 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/weird_prophetic/texts/pg3261.txt:7155 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/weird_prophetic/texts/pg4791.txt:6461 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/weird_prophetic/texts/pg61077.txt:106 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/weird_prophetic/texts/pg61077.txt:5816 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/weird_prophetic/texts/pg8778.txt:159 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/ractors/weird_prophetic/texts/pg8778.txt:12628 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3d3yRs.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3dBfW3.fragment:1 | TODO,HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3dcfzn.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3dlGDM.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3l23Wc.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3l33DB.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3lSSDG.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3lXXR8.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3lcGR2.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3ldSRj.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3llSz8.fragment:1 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3lsSz4.fragment:1 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3ltBRX.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3ltcR4.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3sKXWh.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3sVXWw.fragment:1 | TODO,HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3sfGR2.fragment:1 | FIXME | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3slSzn.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3ssXRH.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3syGWc.fragment:1 | FIXME | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3tBBWh.fragment:1 | FIXME | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3tVGRz.fragment:1 | TODO,HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3tccRn.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/3/3tsBDX.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4d2czc.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4dG3RV.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4dGXW1.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4dKSWG.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4dKcRG.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4dVGzD.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4dXBD4.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4dfXWX.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4djfz3.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4dtXzX.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4l23Dd.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4l2Xzd.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4l2cRt.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4l2fRW.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4l3XD8.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4lBfRV.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4lSSDW.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4lXSDr.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4lcfR4.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4ljBzK.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4ljGRR.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4ljcWd.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4ljcWm.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4lsXzs.fragment:1 | FIXME | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4ltGDl.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4s3XDN.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4sVSRd.fragment:1 | TODO,FIXME,XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4sXSRX.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4sXXz7.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4ssSDn.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4styzM.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4t2cDy.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4t2fWm.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4tBSzm.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4tGBDG.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4tGXWd.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4tKXD3.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4tKfWG.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4tdGzr.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4tfGWn.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4tjXWt.fragment:1 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4tjcWR.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4ts3RN.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/4/4ttfW4.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/7/7dKXDW.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/7/7dyGDh.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/7/7l3GW2.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/7/7lGGRV.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/7/7s2SRz.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/7/7sBGzR.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/7/7tdGDs.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MdXyz8.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MddXDs.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/Ml3SRs.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MlByz3.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MlVcDh.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MlcBWl.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MlfGz8.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/Mll3Wl.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MllfW2.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MltXWl.fragment:1 | FIXME | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/Mltyz8.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MlyGzd.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/Ms3SR2.fragment:1 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/Ms3Sz2.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MsGGDW.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MscSWl.fragment:1 | HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MscXDf.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MsjyRK.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MstSDB.fragment:1 | TODO,FIXME | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MsyGDh.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MtB3WW.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MtGBRm.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MtSXR3.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MtVBR3.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MtVfRw.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MtXfWS.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MtcXWr.fragment:1 | FIXME | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MtjGWm.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/Mty3Rc.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MtyGDV.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/M/MtySDD.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/N/NdKSDV.fragment:1 | TODO,FIXME | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/N/NdSSWz.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/N/NdSXWW.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/N/NdsSW4.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/N/NlSXW3.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/N/NlcGDN.fragment:1 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/N/NljGR1.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/N/NljXDK.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/N/NlsXzf.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/N/Ns2SWm.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/N/NscXR4.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/N/Nt2GRW.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/N/NtS3Dm.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/N/Ntc3R7.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/N/NtdGDs.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/N/Ntj3RW.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/N/NtjGWw.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/Wd2cDh.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/Wd33Dr.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/WdXfDM.fragment:1 | TODO,FIXME,HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/WdfBD7.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/WdfSRS.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/Wdl3W4.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/WdsfD7.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/WdyXzz.fragment:1 | FIXME | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/Wl2yzW.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/WlByzc.fragment:1 | TODO,FIXME,HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/WldGWB.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/Wllczj.fragment:1 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/WlsSRH.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/WsGGRD.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/WsGyDW.fragment:1 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/Wsc3Rn.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/WsfXW2.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/Wt2Xzz.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/WtK3W1.fragment:1 | HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/WtccWN.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/WtdGWB.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/WtjGRc.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wdGSDd.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wdGczD.fragment:1 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wdVSDc.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wdXSWs.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wdcBz4.fragment:1 | FIXME | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wdffzS.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wdtXDl.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wdtXW8.fragment:1 | FIXME | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wl3Sz2.fragment:1 | HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wlBfzW.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wlGGW3.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wlcXRr.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wlsfRj.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/ws2BRm.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/ws3XRj.fragment:1 | FIXME | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wsK3z3.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wsKfDz.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wsXcW7.fragment:1 | TODO,FIXME | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wslBDM.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wstfDr.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wt3SW8.fragment:1 | TODO,FIXME | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wt3Sz2.fragment:1 | FIXME,HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wtB3Rz.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wtXXzs.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wtcSRX.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/W/wttXD7.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XdXBDH.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XdXcRN.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XdcyW8.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XdfXRN.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XdjXDV.fragment:1 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XdjyDm.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XdlXDr.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/Xdtfzr.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/Xl2BRR.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/Xl2GWw.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/Xl2XW1.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/Xl3XzS.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/Xl3yRr.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XlGXRm.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XlKBWD.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XlSGRt.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XlVBDR.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XlXGWM.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XlfXWB.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XljBRK.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XllfD8.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/Xs3GRM.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XsKfzz.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XsXyzj.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XslSDN.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/Xslyzn.fragment:1 | TODO,FIXME | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/Xt23zG.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XtSGzh.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XtVBDz.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XtXfDS.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XtdGRl.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XtdfW8.fragment:1 | HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/Xtj3zt.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/Xtl3zM.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XtsBRN.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XtsBzN.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/X/XtsSWH.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/f/fd3Gzl.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/f/fdfSDB.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/f/fl2SzG.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/f/flBSDy.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/f/flfXDn.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/f/flj3WR.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/f/flsGzH.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/f/fsKSWD.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/f/ftB3Rw.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/f/ftSXWK.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/f/ftlXz8.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/ld3XRr.fragment:1 | TODO,FIXME,HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/ldBcDt.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/ldGSRh.fragment:1 | HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/ldKXRm.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/ldfXzB.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/ldt3Dr.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/ldyXWz.fragment:1 | HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/llBXR3.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/llGBRy.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/llKcR3.fragment:1 | FIXME | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/llX3Rn.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/llXBzB.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/lldGRM.fragment:1 | HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/llfGRn.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/lljfD1.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/lllGR7.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/lllfzX.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/lls3zr.fragment:1 | FIXME | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/lltGzB.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/ls2yzw.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/lsXBDl.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/lsccWX.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/lscfz8.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/lsfGDN.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/lstGzS.fragment:1 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/lt23WK.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/ltBXW1.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/ltSGRG.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/ltjfzG.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/ltlXRB.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/lttBzN.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/l/ltyfDd.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/s/sdGXzK.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/s/sdfGWX.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/s/sdfXz7.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/s/slSSzW.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/s/sldGWj.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/s/ss23Dm.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/s/ssyXzy.fragment:1 | HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/s/st33Wj.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/s/stjSRG.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/s/sts3zn.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/s/stt3Wr.fragment:1 | FIXME,HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tdKBRW.fragment:1 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tdKcWm.fragment:1 | XXX | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tddBDr.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tddGzf.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tddfRB.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tdjczc.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tdlyzN.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tdsBWf.fragment:1 | TODO,FIXME,HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tlBSzh.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tlXSR2.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tlXXWs.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tljGzD.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tllyWf.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/ts2SzR.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tsByRh.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tsKcR1.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tsSBRd.fragment:1 | TODO,FIXME,HACK | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tsfyz4.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tslXR2.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tst3Wn.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tstXR7.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/tsyGW3.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/ttSfRy.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/corpus/shadertoy21k/codes/shader_codes/shadertoy/t/ttlGRn.fragment:1 | TODO | 2026-09-14 | 14 | VENDOR CORPUS |
| memory/research_polished/substrate_gpu.md:20 | HACK | 2026-09-21 | 7 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:543 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:1073 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:1183 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:1639 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:2054 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:2055 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:2056 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:2687 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:2688 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:2689 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:3234 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:4251 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:4312 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:6005 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:6138 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:6535 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:6883 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:7631 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:8552 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:8977 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/thinking/app_reasoning.jsonl:8983 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:2676 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:3670 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:6745 | TODO | 2026-09-19 | 9 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:7290 | XXX | 2026-09-19 | 9 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:7355 | XXX | 2026-09-19 | 9 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:8237 | TODO | 2026-09-19 | 9 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:10361 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:13445 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:13689 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:14664 | TODO,FIXME,HACK,XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:14799 | TODO,FIXME | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:15833 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:15843 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:15891 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:18517 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:20224 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:20225 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:20377 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:28002 | TODO | 2026-09-28 | 0 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:30227 | TODO | 2026-09-28 | 0 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:30253 | TODO,FIXME,HACK,XXX | 2026-09-28 | 0 | RECEIPT / TAPE / PROSE |
| memory/trajectory/steps.jsonl:30283 | TODO | 2026-09-28 | 0 | RECEIPT / TAPE / PROSE |
| memory/vault/astra_v2_companions/moonshot-v2-registration-review.md:53 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| outputs/wandr_selfeval_cache/pages.jsonl:8 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| outputs/wandr_selfeval_cache/pages.jsonl:16 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| outputs/wandr_selfeval_cache/pages.jsonl:25 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| outputs/wandr_selfeval_cache/pages.jsonl:33 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| outputs/wandr_selfeval_cache/pages.jsonl:42 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| outputs/wandr_selfeval_cache/pages.jsonl:50 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| queue/lanes/research/trail.jsonl:125 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| research/surface_audit/df3.json:102 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| scholem_mt.txt:13016 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_mt.txt:14757 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_mt.txt:15669 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_mt.txt:16529 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_mt.txt:16688 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_mt.txt:17194 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_mt.txt:17389 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_ss.txt:9920 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_ss.txt:14567 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_ss.txt:20320 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_ss.txt:26847 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_ss.txt:30520 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_ss.txt:30981 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_ss.txt:31440 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_ss.txt:32187 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_ss.txt:32303 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_ss.txt:32357 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_ss.txt:32460 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| scholem_ss.txt:32564 | XXX | 2026-09-25 | 3 | BOOK TEXT |
| training/refined_training_data.jsonl:846 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| training/refined_training_data.jsonl:847 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/ESTATE_INDEX/ESTATE_INDEX.jsonl:360151 | TODO | NA | NA | DATA INDEX ROW |
| watch/ESTATE_INDEX/ESTATE_INDEX.jsonl:469841 | TODO | NA | NA | DATA INDEX ROW |
| watch/ESTATE_INDEX/ESTATE_INDEX.jsonl:485905 | TODO | NA | NA | DATA INDEX ROW |
| watch/ESTATE_INDEX/ESTATE_INDEX.jsonl:493566 | TODO | NA | NA | DATA INDEX ROW |
| watch/ESTATE_INDEX/ESTATE_INDEX.jsonl:2303192 | TODO | NA | NA | DATA INDEX ROW |
| watch/ESTATE_INDEX/ESTATE_INDEX.jsonl:2319889 | TODO | NA | NA | DATA INDEX ROW |
| watch/ESTATE_INDEX/ESTATE_INDEX.jsonl:2320713 | TODO | NA | NA | DATA INDEX ROW |
| watch/ESTATE_INDEX/ESTATE_INDEX.jsonl:2359821 | TODO | NA | NA | DATA INDEX ROW |
| watch/MCP_AWESOME_DIGEST.md:1316 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/SELF_STEAL_ASTRA_SEAT_20260905.md:26 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/astra_hold0/FEN_FREEZE_KIT_20260911.md:148 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/inbox/ADAM_ONBOARDING_FULL_20260924.md:319 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| watch/inbox/ADAM_ONBOARDING_FULL_20260924.md:337 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| watch/inbox/ADAM_ONBOARDING_FULL_20260924.md:339 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| watch/inbox/GAMEDIG_horror-maze-DOORSLethal-vein_20260926.md:287 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/GAMEDIG_horror-maze-DOORSLethal-vein_20260926.md:497 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/HEAD_MUSEUM_PLAN_20260912.md:12 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/inbox/NIGHT_AUDIT_20260916.md:60 | TODO | 2026-09-16 | 12 | RECEIPT / TAPE / PROSE |
| watch/inbox/QUOTE_AUDIT_WIDE_20260925.results.json:326 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| watch/inbox/QUOTE_AUDIT_WIDE_20260925.results.json:327 | TODO | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| watch/inbox/TRAJECTORY_SWEEP_20260923.md:222 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| watch/inbox/TRAJECTORY_SWEEP_20260923.md:267 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| watch/inbox/TRAJECTORY_SWEEP_20260923.md:337 | XXX | 2026-09-25 | 3 | RECEIPT / TAPE / PROSE |
| watch/inbox/audit_20260926/LANE10_ADVERSARIAL.md:161 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/audit_20260926/LANE3_GATE_ENFORCEMENT.md:339 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/audit_20260926/WAVE2_LANE2_PUSH_BLOCKERS.md:73 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/audit_20260926/WAVE2_LANE2_PUSH_BLOCKERS.md:76 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/audit_20260926/WAVE2_LANE2_PUSH_BLOCKERS.md:78 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/audit_20260926/WAVE2_LANE2_PUSH_BLOCKERS.md:94 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/audit_20260926/WAVE2_LANE2_PUSH_BLOCKERS.md:166 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_reset_20260927/flash50/deep-chaos-governance.md:36 | TODO | 2026-09-28 | 0 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_reset_20260927/flash50/deep-genre-lattice.md:16 | TODO | 2026-09-28 | 0 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_reset_20260927/flash50/deep-genre-lattice.md:116 | TODO | 2026-09-28 | 0 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_reset_20260927/flash50/deep-infinite-cathedral.md:31 | TODO | 2026-09-28 | 0 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_reset_20260927/flash50/deep-recipes-as-types.md:124 | TODO | 2026-09-28 | 0 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_reset_20260927/flash50/deep-zero-operator.md:32 | TODO | 2026-09-28 | 0 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_reset_20260927/flash50/deep-zero-operator.md:54 | TODO | 2026-09-28 | 0 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_reset_20260927/flash50/f-08.md:603 | TODO | 2026-09-28 | 0 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_reset_20260927/flash50/ledger-truth.md:603 | TODO | 2026-09-28 | 0 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_reset_20260927/flash50/w3-theater-audit.md:50 | TODO | 2026-09-28 | 0 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_wave_20260926/B2_260_verifier_gate_20260926.md:19 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_wave_20260926/B2_277_blind_exit_split_20260926.md:5 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_wave_20260926/B2_277_blind_exit_split_20260926.md:9 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_wave_20260926/B2_277_blind_exit_split_20260926.md:18 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_wave_20260926/B2_277_blind_exit_split_20260926.md:24 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_wave_20260926/B2_328_refold_gate_20260926.md:22 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_wave_20260926/B2_59_dspy_grounded_proposer.py:14 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_wave_20260926/B2_59_dspy_miprov2.py:665 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_wave_20260926/B2_59_miprov2_dig_20260926.md:12 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_wave_20260926/QUEUE.md:339 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_wave_20260926/SW00_lane_helpers.py:4 | XXX | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/burn_wave_20260926/b2_201_dspy/copro_optimizer.py:187 | TODO | 2026-09-27 | 1 | RECEIPT / TAPE / PROSE |
| watch/inbox/desktop_bundle_20260901/wow.txt:7420 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/inbox/desktop_bundle_20260901/wow.txt:7426 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/inbox/desktop_bundle_20260901/wow.txt:10422 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/inbox/desktop_bundle_20260901/wow.txt:10488 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/inbox/desktop_bundle_20260901/wow.txt:10578 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/inbox/desktop_bundle_20260901/wow.txt:11303 | TODO,FIXME | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/inbox/gala_20260925/afterparty/lanes/t40.json:5 | TODO | 2026-09-26 | 2 | RECEIPT / TAPE / PROSE |
| watch/inbox/gala_20260925/afterparty/lanes/t40.json:13 | TODO | 2026-09-26 | 2 | RECEIPT / TAPE / PROSE |
| watch/inbox/gala_20260925/afterparty/lanes/t51.json:3 | TODO | 2026-09-26 | 2 | RECEIPT / TAPE / PROSE |
| watch/inbox/gala_20260925/afterparty/lanes/t51.json:5 | TODO | 2026-09-26 | 2 | RECEIPT / TAPE / PROSE |
| watch/inbox/gala_20260925/afterparty/lanes/t51.json:17 | TODO | 2026-09-26 | 2 | RECEIPT / TAPE / PROSE |
| watch/inbox/gala_20260925/afterparty/lanes/t62.json:17 | TODO | 2026-09-26 | 2 | RECEIPT / TAPE / PROSE |
| watch/inbox/gala_20260925/afterparty/lanes/t69.json:17 | TODO | 2026-09-26 | 2 | RECEIPT / TAPE / PROSE |
| watch/inbox/gala_20260925/afterparty/lanes/t76.json:14 | TODO | 2026-09-26 | 2 | RECEIPT / TAPE / PROSE |
| watch/inbox/mrpool_export/ledger.jsonl:250 | HACK | 2026-09-18 | 10 | RECEIPT / TAPE / PROSE |
| watch/inbox/mrpool_export/ledger.jsonl:795 | HACK | 2026-09-18 | 10 | RECEIPT / TAPE / PROSE |
| watch/inbox/mrpool_export/ledger.jsonl:1132 | XXX | 2026-09-18 | 10 | RECEIPT / TAPE / PROSE |
| watch/inbox/mrpool_export/ledger.jsonl:1143 | XXX | 2026-09-18 | 10 | RECEIPT / TAPE / PROSE |
| watch/inbox/mrpool_export/ledger_full.jsonl:250 | HACK | 2026-09-18 | 10 | RECEIPT / TAPE / PROSE |
| watch/inbox/mrpool_export/ledger_full.jsonl:795 | HACK | 2026-09-18 | 10 | RECEIPT / TAPE / PROSE |
| watch/inbox/mrpool_export/ledger_full.jsonl:1132 | XXX | 2026-09-18 | 10 | RECEIPT / TAPE / PROSE |
| watch/inbox/mrpool_export/ledger_full.jsonl:1143 | XXX | 2026-09-18 | 10 | RECEIPT / TAPE / PROSE |
| watch/inbox/qdrop_export/qdrops.jsonl:184 | XXX | 2026-09-18 | 10 | RECEIPT / TAPE / PROSE |
| watch/inbox/qdrop_export/qdrops.jsonl:1977 | HACK | 2026-09-18 | 10 | RECEIPT / TAPE / PROSE |
| watch/inbox/qdrop_export/qdrops.jsonl:3998 | HACK | 2026-09-18 | 10 | RECEIPT / TAPE / PROSE |
| watch/inbox/qdrop_export/qdrops.jsonl:4977 | HACK | 2026-09-18 | 10 | RECEIPT / TAPE / PROSE |
| watch/inbox/qdrop_export/qdrops.jsonl:5144 | HACK | 2026-09-18 | 10 | RECEIPT / TAPE / PROSE |
| watch/inbox/union_fullsend_20260917/DAY_PACK.md:1015 | TODO | 2026-09-17 | 11 | RECEIPT / TAPE / PROSE |
| watch/inbox/union_fullsend_20260917/DAY_PACK.md:1022 | TODO | 2026-09-17 | 11 | RECEIPT / TAPE / PROSE |
| watch/inbox/union_fullsend_20260917/DAY_PACK.md:1031 | TODO | 2026-09-17 | 11 | RECEIPT / TAPE / PROSE |
| watch/inbox/union_fullsend_20260917/DAY_PACK.md:1040 | TODO | 2026-09-17 | 11 | RECEIPT / TAPE / PROSE |
| watch/inbox/union_fullsend_20260917/DAY_PACK.md:1053 | TODO | 2026-09-17 | 11 | RECEIPT / TAPE / PROSE |
| watch/inbox/union_fullsend_20260917/DAY_PACK.md:1063 | TODO | 2026-09-17 | 11 | RECEIPT / TAPE / PROSE |
| watch/inbox/union_fullsend_20260917/DAY_PACK.md:1075 | TODO | 2026-09-17 | 11 | RECEIPT / TAPE / PROSE |
| watch/inbox/union_fullsend_20260917/raw.jsonl:33 | TODO | 2026-09-17 | 11 | RECEIPT / TAPE / PROSE |
| watch/inbox/v41_paces/LANE8_new_work.md:5 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/inbox/v41_paces/LANE8_new_work.md:11 | TODO,FIXME,HACK | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/inbox/v41_paces/LANE8_new_work.md:64 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/inbox/v41_paces/LANE8_new_work.md:67 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/inbox/wave_20260916/receipts/G1_GAMES_AUDIT.md:86 | TODO,FIXME,XXX | 2026-09-16 | 12 | RECEIPT / TAPE / PROSE |
| watch/probe_mag_gateway.md:30 | TODO | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/vault/passports/meditations_marcus_aurelius_pd.txt:1749 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/vault/passports/meditations_marcus_aurelius_pd.txt:2364 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/vault/passports/meditations_marcus_aurelius_pd.txt:2658 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/vault/passports/meditations_marcus_aurelius_pd.txt:3248 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/vault/passports/meditations_marcus_aurelius_pd.txt:3692 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/vault/passports/meditations_marcus_aurelius_pd.txt:4294 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/vault/passports/meditations_marcus_aurelius_pd.txt:4838 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/vault/passports/meditations_marcus_aurelius_pd.txt:5373 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/vault/passports/meditations_marcus_aurelius_pd.txt:6463 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |
| watch/vault/passports/meditations_marcus_aurelius_pd.txt:6550 | XXX | 2026-09-14 | 14 | RECEIPT / TAPE / PROSE |

## Untracked estate surface (189 hits, 13 files, no blame possible)

`git ls-files --others --exclude-standard` = 190 files at scan time; 13 carry markers, 189
hit lines. Untracked files have no git history, so no blame age exists; all are scratch or
vendored copies of third-party sources, so none is estate debt:

-   60 tmp_gopher/amdgpu_usage.rst
-   33 watch/inbox/burn_reset_20260927/flash50/work/llama-context.cpp
-   22 watch/inbox/burn_reset_20260927/flash50/work/llama-kv-cache.cpp
-   20 watch/inbox/burn_reset_20260927/flash50/work/llama-graph.cpp
-   17 watch/inbox/burn_reset_20260927/flash50/work/ggml.h
-   12 watch/inbox/burn_reset_20260927/flash50/work/llama.h
-    8 watch/inbox/burn_reset_20260927/flash50/work/llama-model.cpp
-    5 tmp_gopher/llama_arg.cpp
-    5 watch/inbox/burn_reset_20260927/flash50/work/arg.cpp
-    2 tmp_gopher/ggml_vulkan.cpp
-    2 tmp_gopher/opencl.md
-    2 watch/inbox/burn_reset_20260927/flash50/work/ggml-vulkan.cpp
-    1 watch/inbox/burn_reset_20260927/flash50/work/vecdotq.cuh

Classes: tmp_gopher/amdgpu_usage.rst (60) is Linux amdgpu documentation; the flash50/work/
llama* + ggml* files (120) are vendored llama.cpp sources staged by a sibling dig; tmp_gopher
llama_arg.cpp / ggml_vulkan.cpp / opencl.md (9) same. Upstream TODO/FIXME comments, not ours.

## Findings

1. **The estate's real TODO debt is tiny and self-aware: 13 actionable hits, of which the
   largest block (5) is the deliberate TODO-FLIP-TO-ENFORCE convention in githooks/pre-push**
   (each gate landed WARN-ONLY per the t40 no-lockout precedent; flipping is an explicit
   operator decision, still pending as of 2026-09-28). The 2026-09-26 theater audit's
   F9-F14 (seven WARN-ONLY gates, zero true catches) is the same surface seen from the gate
   side.
2. **The estate already meters part of this census**: tools/violation_ratchet.py:195-196
   implements a `todo-undated` rule (TODO/FIXME without a year = debt) scoped to mag/+tools/,
   and configs/violation_baseline.json carries exactly one registered row for it
   (mag/max_distill.py, accepted 2026-09-24 by operator:bootstrap). This census found no
   NEW unregistered TODO/FIXME comment in mag/, tools/ or scripts/ - the only hits there are
   the vocabulary uses listed in tier C. (The ratchet gate itself was NOT run this ask.)
3. **mag/prompt_lance.py is the estate's own standing TODO-scanner organ** (prompt/context
   leak detector whose vocab is exactly these markers, landed 2026-09-27): the right
   long-term home if this census ever needs to run on a cadence, pointed at prompts.
4. **Marker mass is data, not debt**: 711/753 tracked hits (94.4%) live in book texts,
   scraped corpora, model-output tapes, receipts, catalog/index rows and archived deploy/audit
   snapshots (dist_audit, dashboard-deploy); 8 more are vendored upstream code/docs; 17 are
   detector vocab; 2 are binary false
   positives. Any naive rg-based debt metric over this estate overstates actionable debt by
   roughly 50x.
5. **Oldest blamed markers are 55d = the age of the repo** (first commit 2026-08-04):
   docs/ref/MAG_v2_PLAN.md mermaid labels and the mag/canvas_bridge.py /
   tests/test_canvas_bridge.py vocabulary pair from the initial import.

## Not run / OWED

- The case-insensitive 4,649 matches were counted, not itemized (prose todo/hack/xxx).
- tools/violation_ratchet.py check and pytest were NOT run (not part of this ask).
- Blame for the 16 ESTATE_INDEX rows is unobtainable (git blame fatal on the 1.29 GB blob),
  reported as NA above rather than guessed.
- Relevance verdicts for tier E are class-level (one sample per class read), not per-row
  hand-reads; every tier A/B/C/D row was read in context individually.
- Self-reference note: this receipt contains the literal markers and will be a hit in the
  next census of this directory.

## Age distribution (all blameable tracked hits)

- 0-7d: 240
- 8-30d: 484
- 31-90d: 13
- 91-180d: 0
- 181-365d: 0
- >365d: 0

